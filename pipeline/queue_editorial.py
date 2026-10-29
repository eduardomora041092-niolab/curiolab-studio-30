"""CurioLab Studio 30 — dynamic Buffer queue, publication reconciliation, editorial feedback, cycle check.

Called through daily.py:
  python3 daily.py snapshot-query [PURPOSE]   -> JSON request: the exact read-only Buffer MCP calls (list_posts x3 +
                                              get_account) and the directory where each raw output must be saved
  python3 daily.py snapshot-links DIR        -> get_post calls still needed (sent posts without a public link)
  python3 daily.py queue DIR [--for-create]  -> validates + archives the raw MCP outputs, reconciles state with Buffer,
                                              computes free slots, prints the plan; only --for-create (fresh) authorises it
  (legacy, only if Buffer ever exposes execute_query again: snapshot-query PURPOSE --graphql + queue SNAP.json)
  python3 daily.py create-next             -> next authorised post to create, one at a time (record after each)
  python3 daily.py editorial               -> recomputes pipeline/editorial.json from logs/metrics.csv and logs changes
  python3 daily.py cycle                   -> PASS/PENDING per stage of the autonomous cycle (evidence for the owner)

Design rules (unchanged controls): never more than limit-1 scheduled posts in the organisation; one post per
video and channel (duplicates are reported, never deleted); a post in `error` is recreated once at most; future
calendar slots are scheduled for their time (customScheduled), never earlier.
"""
import csv, datetime as dt, hashlib, json, os, re, secrets, statistics, sys
import daily as D

SAFETY_MARGIN = 1          # keep one slot free: "si hay 9 o más, no crees más"
RECENT_DAYS = 5            # window of posts fetched for reconciliation / duplicate detection
EDITORIAL = f"{D.REPO}/pipeline/editorial.json"
EDITORIAL_LOG = f"{D.REPO}/logs/editorial_log.md"
QUEUE_LOG = f"{D.REPO}/logs/queue_log.csv"
PLAN = f"{D.REPO}/pipeline/queue_plan.json"
REQUESTS = f"{D.REPO}/pipeline/snapshot_requests.json"   # nonces issued by snapshot-query (evidence of freshness)
SNAP_DIR = f"{D.REPO}/evidence/buffer"                    # raw Buffer responses, byte for byte, + index.csv
FRESH_MIN = 10             # a snapshot used to create posts must come from a query issued <= 10 min ago
PLATFORM_OF = {v: k for k, v in D.CHANNELS.items()}
DEFAULT_RULES = {"target_max_s": 33.0, "hook_max_words": 12, "caption_cta": False, "weak_category": None,
                 "applies_from": None}

# ---------------------------------------------------------------- Buffer snapshot via MCP tools (default since 2026-10-29)
# The Buffer connector has no execute_query (verified 2026-10-29: tools = get_account, list_channels, get_channel,
# list_posts, get_post, create_post, edit_post, delete_post, ideas, templates, get_aggregated_post_metrics).
# Verified capabilities: get_account -> organizations[].limits.scheduledPosts + currentTime (server clock, with offset);
# list_posts -> id, status, dueAt, sentAt, channelId, channelService, error, assets[].video{title,durationMs} and
# pageInfo{hasNextPage,endCursor} (max 100 per page), but NO externalLink; get_post -> externalLink.
# NOT available through any tool: per-channel daily posting limits (GraphQL dailyPostingLimits).
SNAP_ROOT = "/tmp/curiolab_snap"
LIST_FILES = ("open", "errors", "recent")
NODE_KEYS = ("id", "status", "channelId", "dueAt", "sentAt", "assets")
MISSING_INFO = ["límite diario de publicación por canal (dailyPostingLimits): ninguna herramienta MCP de Buffer lo expone; "
                "si Buffer rechaza un create_post por ese límite, se registra como failed y el plan se detiene"]

def mcp_calls(since):
    org, ch, srt = D.ORG, list(D.CHANNELS.values()), [{"field": "dueAt", "direction": "asc"}]
    return [  # order matters: get_account LAST, so its server currentTime is not earlier than the lists
        {"file": "open.json", "tool": "list_posts", "args": {"organizationId": org, "status": ["scheduled", "sending"], "first": 100, "sort": srt}},
        {"file": "errors.json", "tool": "list_posts", "args": {"organizationId": org, "status": ["error"], "first": 100, "sort": srt}},
        {"file": "recent.json", "tool": "list_posts", "args": {"organizationId": org, "channelIds": ch, "dueAt": {"start": since}, "first": 100, "sort": srt}},
        {"file": "account.json", "tool": "get_account", "args": {}},
    ]

def raw_obj(path):
    """First JSON value of a raw MCP output file (the tool appends a separate {"rateLimit": ...} object)."""
    return json.JSONDecoder().raw_decode(open(path, encoding="utf-8").read().strip())[0]

def load_mcp_dir(d, req=None):
    """Validates the raw MCP outputs saved in directory d and returns (data, files, error). data has the same shape the
    planner uses (account/open/errors/recent) plus _source/_missing. Nothing is invented: a list with hasNextPage=true
    must come with its next page (<name>.p2.json, .p3.json …); a missing key or a node that does not match the filter
    of its call makes the whole snapshot incomplete."""
    req = req or {}; since = utc(req.get("since")) if req.get("since") else None
    files = sorted(f for f in os.listdir(d) if f.endswith(".json"))
    data = {"_source": "mcp", "_missing": list(MISSING_INFO), "limits": None}
    try:
        acct = raw_obj(f"{d}/account.json")
    except FileNotFoundError:
        return None, files, "falta account.json (salida de get_account)"
    except ValueError as e:
        return None, files, f"account.json ilegible: {e}"
    org = next((o for o in acct.get("organizations") or [] if o.get("id") == D.ORG), None)
    if org is None: return None, files, f"account.json no contiene la organización {D.ORG}"
    if not isinstance((org.get("limits") or {}).get("scheduledPosts"), int): return None, files, "account.json sin organizations[].limits.scheduledPosts"
    try:
        ct = dt.datetime.fromisoformat(acct["currentTime"])
        if ct.tzinfo is None: raise ValueError("sin zona horaria")
    except (KeyError, ValueError, TypeError) as e:
        return None, files, f"account.json sin currentTime válido ({e})"
    data["account"] = acct; data["_server_time"] = ct.isoformat()
    for name in LIST_FILES:
        merged, seen, page, last_due = [], set(), 1, ""
        while True:
            fn = f"{name}.json" if page == 1 else f"{name}.p{page}.json"
            if not os.path.exists(f"{d}/{fn}"):
                if page == 1: return None, files, f"falta {fn} (salida de list_posts)"
                return None, files, (f"{prev} tiene hasNextPage=true: llama a list_posts con los mismos argumentos y "
                                     f"after=\"{end}\" y guarda la salida completa en {fn}")
            try:
                obj = raw_obj(f"{d}/{fn}")
            except ValueError as e:
                return None, files, f"{fn} ilegible: {e}"
            pi = obj.get("pageInfo") if isinstance(obj, dict) else None
            if not isinstance(obj, dict) or not isinstance(obj.get("edges"), list) or not isinstance(pi, dict) or not isinstance(pi.get("hasNextPage"), bool):
                return None, files, f"{fn} no es una respuesta de list_posts (faltan edges/pageInfo.hasNextPage)"
            for e in obj["edges"]:
                n = (e or {}).get("node") or {}
                miss = [k for k in NODE_KEYS if k not in n]
                if miss: return None, files, f"{fn}: el post {n.get('id')} no trae {miss}"
                bad = ((name == "open" and n["status"] not in ("scheduled", "sending")) or (name == "errors" and n["status"] != "error")
                       or (name == "recent" and (n["channelId"] not in D.CHANNELS.values() or (since and n["dueAt"] and utc(n["dueAt"]) < since))))
                if bad: return None, files, f"{fn}: el post {n['id']} ({n['status']}, {n['channelId']}, {n['dueAt']}) no corresponde al filtro de la llamada"
                if n["id"] in seen: return None, files, f"{fn}: el post {n['id']} se repite entre páginas (paginación incorrecta)"
                if (n.get("dueAt") or "") < last_due: return None, files, f"{fn}: orden por dueAt roto entre páginas (¿after incorrecto?)"
                seen.add(n["id"]); last_due = n.get("dueAt") or last_due
                n.setdefault("externalLink", None); merged.append(n)
            if not pi["hasNextPage"]: break
            prev, end, page = fn, pi.get("endCursor"), page + 1
        data[name] = {"pageInfo": {"hasNextPage": False}, "edges": [{"node": n} for n in merged], "_pages": page}
    for fn in files:   # get_post outputs for sent posts: only source of the public link
        m = re.match(r"link_([a-f\d]{24})\.json$", fn)
        if not m: continue
        try:
            g = raw_obj(f"{d}/{fn}")
        except ValueError as e:
            return None, files, f"{fn} ilegible: {e}"
        if g.get("id") != m.group(1): return None, files, f"{fn} no es la salida de get_post({m.group(1)})"
        for k in LIST_FILES:
            for e in data[k]["edges"]:
                if e["node"]["id"] == g["id"]:
                    e["node"]["externalLink"] = g.get("externalLink"); e["node"]["status"] = g.get("status", e["node"]["status"])
    return data, files, None

def links_needed(data, st):
    out = []
    for n in nodes(data, "recent"):
        plat = PLATFORM_OF.get(n["channelId"]); vid, _ = vid_of(n)
        if n["status"] == "sent" and not n.get("externalLink") and vid in st["videos"]:
            rec = st["videos"][vid]["posts"].get(plat, {})
            if not (rec.get("post_id") == n["id"] and rec.get("url")): out.append({"video_id": vid, "platform": plat, "post_id": n["id"]})
    return out

def cmd_snapshot_links(args):
    """snapshot-links DIR -> get_post calls still needed: sent posts whose public link is not yet in state.json."""
    data, _, err = load_mcp_dir(args[0], next((r for r in D.load(REQUESTS, []) or [] if r.get("dir") == args[0].rstrip("/")), None))
    if err: print(f"INCOMPLETE: {err}"); sys.exit(5)
    need = links_needed(data, D.state())
    print(json.dumps([{"tool": "get_post", "args": {"postId": x["post_id"]}, "file": f"{args[0].rstrip('/')}/link_{x['post_id']}.json", **x} for x in need], ensure_ascii=False, indent=1))

def cmd_snapshot_query(args):
    if "--graphql" in args: return cmd_snapshot_query_graphql([a for a in args if a != "--graphql"])
    purpose = args[0] if args else "reconcile"
    rid = secrets.token_hex(6); now = D.now_local(); d = f"{SNAP_ROOT}/{purpose}_{rid}"; os.makedirs(d, exist_ok=False)
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=RECENT_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    reqs = D.load(REQUESTS, []) or []
    reqs.append({"nonce": rid, "mode": "mcp", "issued": now.isoformat(timespec="seconds"), "purpose": purpose, "since": since, "dir": d, "used": None})
    D.save(REQUESTS, reqs[-200:])
    print(json.dumps({"request_id": rid, "dir": d, "issued": now.isoformat(timespec="seconds"), "calls": mcp_calls(since),
                      "instructions": ("Haz las llamadas en este orden (get_account la última) y guarda con Write la salida COMPLETA de "
                                       "cada una, sin editar, en dir/file. Si una lista trae hasNextPage=true, repite la misma llamada con "
                                       "after=endCursor y guárdala como <nombre>.p2.json (p3, …). Después: snapshot-links dir → get_post de "
                                       "cada post indicado → dir/link_<id>.json. Por último: queue dir [--for-create]."),
                      "missing_info": MISSING_INFO}, ensure_ascii=False, indent=1))

def cmd_snapshot_query_graphql(args):
    """snapshot-query [PURPOSE] -> query + variables. Each call issues a one-time nonce that Buffer echoes back as the
    alias `req_<nonce>` in its response, so `queue --for-create` can prove the snapshot answers a query issued just now."""
    purpose = args[0] if args else "reconcile"
    q = "\n".join(l for l in open(f"{D.REPO}/pipeline/buffer_snapshot.graphql").read().splitlines() if not l.startswith("#"))
    nonce = secrets.token_hex(6)
    q = q.replace("  account {", f"  req_{nonce}: account {{ id }}\n  account {{", 1)
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=RECENT_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    reqs = D.load(REQUESTS, []) or []
    reqs.append({"nonce": nonce, "issued": D.now_local().isoformat(timespec="seconds"), "purpose": purpose, "used": None})
    D.save(REQUESTS, reqs[-200:])
    print(json.dumps({"query": q, "variables": {"org": D.ORG, "since": since, "channels": list(D.CHANNELS.values())},
                      "nonce": nonce}, ensure_ascii=False, indent=1))

def check_and_archive(path, for_create, now):
    if os.path.isdir(path): return check_and_archive_mcp(path, for_create, now)
    return check_and_archive_graphql(path, for_create, now)

def check_and_archive_mcp(d, for_create, now):
    """MCP snapshot directory: validates every raw output, checks freshness against the request (and against Buffer's own
    currentTime from get_account), refuses reuse, archives every file byte for byte under evidence/buffer/<name>/."""
    d = d.rstrip("/"); reqs = D.load(REQUESTS, []) or []
    req = next((r for r in reqs if r.get("mode") == "mcp" and r.get("dir") == d), None)
    if req is None: return None, f"{d} no corresponde a ninguna petición emitida por snapshot-query"
    data, files, err = load_mcp_dir(d, req)
    if err: return None, f"instantánea incompleta: {err}"
    issued = dt.datetime.fromisoformat(req["issued"]); ct = dt.datetime.fromisoformat(data["_server_time"])
    if ct < issued - dt.timedelta(minutes=2): return None, f"get_account.currentTime {ct.isoformat()} es anterior a la petición ({req['issued']}): salida reutilizada"
    if ct > issued + dt.timedelta(minutes=FRESH_MIN): return None, f"las llamadas se hicieron {(ct - issued).total_seconds() / 60:.0f} min después de la petición (> {FRESH_MIN})"
    if for_create:
        age = (now - ct).total_seconds() / 60
        if age > FRESH_MIN: return None, f"instantánea de hace {age:.0f} min (> {FRESH_MIN}) según el reloj de Buffer: consulta de nuevo"
        if req.get("used"): return None, f"la instantánea {req['nonce']} ya se usó ({req['used']}): consulta Buffer de nuevo"
    req["used"] = req.get("used") or now.isoformat(timespec="seconds"); D.save(REQUESTS, reqs)
    label = "pre-create" if for_create else req.get("purpose", "mcp")
    name = f"{now.strftime('%Y%m%dT%H%M%S')}_{label}_{req['nonce']}"; out = f"{SNAP_DIR}/{name}"; os.makedirs(out, exist_ok=True)
    idx = f"{SNAP_DIR}/index.csv"; new = not os.path.exists(idx); shas = {}
    with open(idx, "a", newline="") as fh:
        w = csv.writer(fh)
        if new: w.writerow(["ingested_local", "file", "sha256", "bytes", "nonce", "nonce_issued", "for_create"])
        for f in files:
            raw = open(f"{d}/{f}", "rb").read(); open(f"{out}/{f}", "wb").write(raw); shas[f] = hashlib.sha256(raw).hexdigest()
            w.writerow([now.isoformat(timespec="seconds"), f"{name}/{f}", shas[f], len(raw), req["nonce"], req["issued"], for_create])
    return {"file": f"evidence/buffer/{name}/", "files": shas, "nonce": req["nonce"], "nonce_issued": req["issued"],
            "buffer_time": data["_server_time"], "source": "mcp", "pages": {k: data[k]["_pages"] for k in LIST_FILES}}, None

def check_and_archive_graphql(path, for_create, now):
    """Validates a raw snapshot file (the execute_query output saved unedited) and archives it byte for byte under
    evidence/buffer/. Returns (info, error). For posts creation it must answer a nonce issued <= FRESH_MIN min ago
    and not consumed before; a reused or old snapshot is refused."""
    raw = open(path, "rb").read(); sha = hashlib.sha256(raw).hexdigest()
    try:
        obj, _ = json.JSONDecoder().raw_decode(raw.decode("utf-8").strip())
    except ValueError as e:
        return None, f"instantánea ilegible: {e}"
    if isinstance(obj.get("data"), dict): obj = obj["data"]
    missing = [k for k in ("account", "limits", "open", "errors", "recent") if k not in obj]
    if missing: return None, f"instantánea incompleta (faltan {missing}): no es la respuesta de la consulta de snapshot-query"
    orgs = [o.get("id") for o in (obj["account"] or {}).get("organizations") or []]
    if D.ORG not in orgs: return None, f"la instantánea no contiene la organización {D.ORG}"
    nonces = [k[4:] for k in obj if k.startswith("req_")]
    reqs = D.load(REQUESTS, []) or []; req = next((r for r in reqs if r["nonce"] in nonces), None)
    if for_create:
        if req is None: return None, "la instantánea no responde a ninguna consulta emitida por snapshot-query (falta req_<nonce>)"
        age = (now - dt.datetime.fromisoformat(req["issued"])).total_seconds() / 60
        if age > FRESH_MIN: return None, f"instantánea de hace {age:.0f} min (> {FRESH_MIN}): consulta Buffer de nuevo"
        if req.get("used"): return None, f"la instantánea {req['nonce']} ya se usó ({req['used']}): consulta Buffer de nuevo"
    if req: req["used"] = req.get("used") or now.isoformat(timespec="seconds"); D.save(REQUESTS, reqs)
    os.makedirs(SNAP_DIR, exist_ok=True)
    label = ("pre-create" if for_create else (req or {}).get("purpose", "sin-nonce"))
    name = f"{now.strftime('%Y%m%dT%H%M%S')}_{label}_{(req or {}).get('nonce', sha[:12])}.json"
    open(f"{SNAP_DIR}/{name}", "wb").write(raw)
    idx = f"{SNAP_DIR}/index.csv"; new = not os.path.exists(idx)
    with open(idx, "a", newline="") as fh:
        w = csv.writer(fh)
        if new: w.writerow(["ingested_local", "file", "sha256", "bytes", "nonce", "nonce_issued", "for_create"])
        w.writerow([now.isoformat(timespec="seconds"), name, sha, len(raw), (req or {}).get("nonce", ""), (req or {}).get("issued", ""), for_create])
    return {"file": f"evidence/buffer/{name}", "sha256": sha, "nonce": (req or {}).get("nonce"),
            "nonce_issued": (req or {}).get("issued")}, None

def read_snapshot(paths):
    if len(paths) == 1 and os.path.isdir(paths[0]):
        data, _, err = load_mcp_dir(paths[0].rstrip("/"), next((r for r in D.load(REQUESTS, []) or [] if r.get("dir") == paths[0].rstrip("/")), None))
        if err: raise SystemExit(f"INCOMPLETE: {err}")
        return data
    dec, data = json.JSONDecoder(), {}
    for p in paths:
        obj, _ = dec.raw_decode(open(p).read().strip())   # MCP output may carry a trailing rateLimit object
        if isinstance(obj.get("data"), dict): obj = obj["data"]
        for k, v in obj.items():
            if k in ("open", "errors", "recent") and k in data: data[k]["edges"] += v.get("edges") or []
            else: data[k] = v
    return data

def nodes(data, key):
    return [e["node"] for e in ((data.get(key) or {}).get("edges") or [])]

def vid_of(node):
    for a in node.get("assets") or []:
        v = (a or {}).get("video") or {}
        m = re.match(r"CurioLab_(\d{3})(?:_FINAL)?\.mp4$", v.get("title") or "")
        if m: return m.group(1), v.get("durationMs")
    return None, None

def utc(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None

def slot_dt(r):
    return dt.datetime.combine(dt.date.fromisoformat(r["fecha"]), dt.time.fromisoformat(D.SLOT_TIMES[r["slot"]]), D.TZ)

# ---------------------------------------------------------------- queue (reconcile + capacity + plan)
def plan_queue(data, st, cal, now):
    orgs = (data.get("account") or {}).get("organizations") or []
    org = next((o for o in orgs if o.get("id") == D.ORG), orgs[0] if orgs else {})
    limit = (org.get("limits") or {}).get("scheduledPosts") or 10
    open_n, recent, errs = nodes(data, "open"), nodes(data, "recent"), nodes(data, "errors")
    posts = {n["id"]: n for n in recent + errs + open_n}
    # org-wide occupied slots; cross-checked with the channel window in case one list comes back short
    occupied = {n["id"] for n in open_n} | {n["id"] for n in recent if n["status"] in ("scheduled", "sending")}
    used = len(occupied); free = max(0, limit - SAFETY_MARGIN - used)
    warnings, reconciled, blocked = [], [], []
    for k in ("open", "errors", "recent"):
        if (data.get(k) or {}).get("pageInfo", {}).get("hasNextPage"): warnings.append(f"lista '{k}' truncada a 100: capacidad calculada de forma conservadora"); free = 0
    by = {}
    for n in posts.values():
        plat = PLATFORM_OF.get(n["channelId"]); vid, dur = vid_of(n)
        if not plat or vid not in st["videos"]: continue
        by.setdefault((vid, plat), []).append(n)
        if dur: st["videos"][vid]["duration_ms"] = dur
    for (vid, plat), ns in sorted(by.items()):
        v = st["videos"][vid]; rec = v["posts"].get(plat, {})
        live = sorted([n for n in ns if n["status"] != "error"], key=lambda n: n.get("dueAt") or "")
        if len(live) > 1: warnings.append(f"DUPLICADO {vid} {plat}: {[n['id'] for n in live]} (no se borra nada; revisar)")
        pick = next((n for n in ns if n["id"] == rec.get("post_id")), None)
        if (pick is None or pick["status"] == "error") and live: pick = live[0]
        pick = pick or ns[-1]
        url = pick.get("externalLink") or ""
        if (rec.get("post_id"), rec.get("status"), rec.get("url") or "") != (pick["id"], pick["status"], url or rec.get("url") or ""):
            v["posts"][plat] = {"post_id": pick["id"], "status": pick["status"], "url": url or rec.get("url", ""),
                                "recorded": now.isoformat(timespec="seconds")}
            if pick["status"] == "error": v["posts"][plat]["error"] = (pick.get("error") or {}).get("message", "")
            reconciled.append(f"{vid} {plat} {pick['id']} {pick['status']} {url}".strip())
        due = utc(pick.get("dueAt"))
        if pick["status"] in ("scheduled", "sending") and due and due < now - dt.timedelta(minutes=45):
            warnings.append(f"RETRASO {vid} {plat} {pick['id']}: debía salir {pick['dueAt']} y sigue {pick['status']}")
        if pick["status"] == "sent" and not url and not v["posts"][plat].get("url"):
            warnings.append(f"SIN ENLACE {vid} {plat} {pick['id']}: sent sin externalLink (get_post {pick['id']} → link_{pick['id']}.json); se reintenta en la próxima ejecución")
        if all(v["posts"].get(p, {}).get("status") == "sent" for p in D.CHANNELS): v["estado"] = "PUBLISHED"
    cands = []
    for vid, r in cal.items():
        v = st["videos"][vid]
        if not v.get("media_url") or not (v.get("qa") or {}).get("all_pass"): continue
        for plat in D.CHANNELS:
            ns = by.get((vid, plat), [])
            if any(n["status"] != "error" for n in ns): continue
            if not ns and v["posts"].get(plat, {}).get("status") in ("sent", "scheduled", "sending"): continue  # older than window
            nerr = sum(1 for n in ns if n["status"] == "error")
            if nerr >= 2:
                blocked.append(f"{vid} {plat}: {nerr} intentos en error; ya se recreó una vez, no se reintenta"); continue
            cands.append((slot_dt(r), 0 if plat == "youtube" else 1, vid, plat, "recrear tras error" if nerr else "nuevo"))
    cands.sort()
    lim = {l["channelId"]: l for l in data.get("limits") or []}
    create, waiting = [], []
    for due, _, vid, plat, why in cands:
        if lim.get(D.CHANNELS[plat], {}).get("isAtLimit") and due.date() == now.date():
            waiting.append({"id": vid, "platform": plat, "dueAt": due.isoformat(), "reason": "límite diario del canal"}); continue
        if free <= 0:
            waiting.append({"id": vid, "platform": plat, "dueAt": due.isoformat(), "reason": "cola de Buffer llena"}); continue
        c = D.caption(vid, now)
        item = {"id": vid, "platform": plat, "channelId": D.CHANNELS[plat], "reason": why, "mode": c["mode"], "dueAt": c["dueAt"],
                "text": c["text"], "asset": {"url": st["videos"][vid]["media_url"], "title": c["asset_title"],
                         **({"thumbnailOffset": c["tiktok_cover_offset_ms"]} if plat == "tiktok" and c.get("tiktok_cover_offset_ms") else {})}}
        item["metadata"] = ({"youtube": {"title": c["youtube_title"], "categoryId": "27", "privacy": "public", "madeForKids": False, "isAiGenerated": True}}
                            if plat == "youtube" else {"tiktok": {"isAiGenerated": True}})
        create.append(item); free -= 1
    if lim:
        per_ch = [{k: l.get(k) for k in ("channelId", "scheduled", "sent", "limit", "isAtLimit")} for l in lim.values()]
    else:   # MCP snapshot: counts from the posts themselves (local day, America/New_York); the limit itself is unknown
        per_ch = []
        for plat, ch in D.CHANNELS.items():
            day = [n for n in posts.values() if n["channelId"] == ch and n.get("dueAt") and utc(n["dueAt"]).astimezone(D.TZ).date() == now.date()]
            per_ch.append({"channelId": ch, "platform": plat, "scheduled": sum(n["status"] in ("scheduled", "sending") for n in day),
                           "sent": sum(n["status"] == "sent" for n in day), "limit": None, "isAtLimit": None})
    return {"generated": now.isoformat(timespec="seconds"), "limit": limit, "safety_margin": SAFETY_MARGIN, "occupied": used,
            "free_after_plan": free, "per_channel_today": per_ch, "missing_info": data.get("_missing") or [],
            "reconciled": reconciled, "create": create, "waiting": waiting, "blocked": blocked, "warnings": warnings}

def cmd_queue(args):
    """queue SNAP.json [--for-create]. Without the flag the plan is informative only (create items are NOT authorised).
    With it, the snapshot must be fresh (nonce <= FRESH_MIN min, never used before); the plan then authorises its
    `create` items for FRESH_MIN min, handed out one at a time by `create-next`."""
    for_create = "--for-create" in args; paths = [a for a in args if not a.startswith("--")]
    now = D.now_local(); infos = []
    base = os.path.basename(paths[0].rstrip("/")) if paths else ""
    purpose = "pre-create" if for_create else (base.split("_")[0] if os.path.isdir(paths[0]) else "reconcile")
    for pth in paths:
        info, err = check_and_archive(pth, for_create, now)
        if err:
            D.log("ERROR", f"queue: {err}"); D.stage(purpose, "BLOCKED", err); print(f"REFUSED: {err}"); sys.exit(5)
        infos.append(info)
    data = read_snapshot(paths); st = D.state(); cal = {r["id"]: r for r in D.load(D.CAL)}
    plan = plan_queue(data, st, cal, now)
    plan.update({"snapshots": infos, "for_create": for_create,
                 "valid_until": (now + dt.timedelta(minutes=FRESH_MIN)).isoformat(timespec="seconds") if for_create else None,
                 "offered": []})
    D.save(D.STATE, st); D.save(PLAN, plan)
    new = not os.path.exists(QUEUE_LOG)
    with open(QUEUE_LOG, "a", newline="") as fh:
        w = csv.writer(fh)
        if new: w.writerow(["timestamp_local", "limit", "occupied", "to_create", "waiting", "reconciled", "warnings", "blocked"])
        w.writerow([plan["generated"], plan["limit"], plan["occupied"], len(plan["create"]), len(plan["waiting"]), len(plan["reconciled"]),
                    len(plan["warnings"]), len(plan["blocked"])])
    for r in plan["reconciled"]: D.log("INFO", f"conciliado {r}")
    for x in plan["warnings"]: D.log("WARN", x)
    for x in plan["blocked"]: D.log("ERROR", x)
    if plan["waiting"]: D.log("INFO", "en espera por capacidad: " + ", ".join(f"{w['id']} {w['platform']} ({w['reason']})" for w in plan["waiting"]))
    dup = [w for w in plan["warnings"] if w.startswith("DUPLICADO")]
    bad = dup + plan["blocked"] + ([f"{len(plan['create'])} sin programar tras crear"] if purpose == "confirm" and plan["create"] else [])
    D.stage(purpose, "FAIL" if bad else "PASS", "; ".join(bad) if bad else
            f"ocupados {plan['occupied']}/{plan['limit']}, crear {len(plan['create'])}, en espera {len(plan['waiting'])}")
    print(json.dumps(plan, ensure_ascii=False, indent=1))

def cmd_create_next(_):
    """create-next -> the next post to create from an authorised, still-valid plan, one at a time. Refuses while the
    previously offered item has not been recorded (`record ... <post_id> <status>` or `record ... - failed`), never
    offers an item twice and never offers an item whose (video, channel) already has a live post in state."""
    plan = D.load(PLAN, {}) or {}; now = D.now_local(); st = D.state()
    if not plan.get("for_create"):
        print("REFUSED: el plan no autoriza crear; ejecuta snapshot-query pre-create + execute_query + queue --for-create"); sys.exit(5)
    if now > dt.datetime.fromisoformat(plan["valid_until"]):
        print(f"STALE: plan caducado ({plan['valid_until']}); consulta Buffer de nuevo"); sys.exit(5)
    if plan.get("stop"):
        print("STOP: una creación falló en este plan (p. ej. LimitReachedError); no se crean más en esta ejecución"); sys.exit(3)
    for o in plan.get("offered", []):
        if not o.get("result"):
            print(f"PENDING_RECORD {o['id']} {o['platform']}: registra el resultado con record antes de crear otro"); sys.exit(6)
    done = {(o["id"], o["platform"]) for o in plan.get("offered", [])}
    for c in plan.get("create", []):
        if (c["id"], c["platform"]) in done: continue
        cur = st["videos"][c["id"]]["posts"].get(c["platform"], {})
        if cur.get("status") in ("scheduled", "sending", "sent") and cur.get("recorded", "") > plan["generated"]:
            print(f"REFUSED: {c['id']} {c['platform']} ya tiene post {cur['post_id']} registrado tras el plan"); sys.exit(5)
        plan.setdefault("offered", []).append({"id": c["id"], "platform": c["platform"], "offered": now.isoformat(timespec="seconds"), "result": None})
        D.save(PLAN, plan); print(json.dumps(c, ensure_ascii=False, indent=1)); return
    ok = [o for o in plan.get("offered", []) if (o.get("result") or {}).get("status") not in (None, "failed")]
    D.stage("scheduling", "PASS", f"{len(ok)} creados y registrados de {len(plan.get('create', []))} autorizados")
    print("NONE"); sys.exit(3)

def record_result(vid, platform, post_id, status):
    """Called by `daily.py record`: closes the offered item of the current plan. Returns a warning or None."""
    plan = D.load(PLAN, None)
    if not plan: return None
    o = next((o for o in plan.get("offered", []) if o["id"] == vid and o["platform"] == platform and not o.get("result")), None)
    if o is None:
        return None if not plan.get("for_create") else f"record {vid} {platform} sin create-next previo en el plan vigente"
    o["result"] = {"post_id": post_id, "status": status, "at": D.now_local().isoformat(timespec="seconds")}
    if status == "failed": plan["stop"] = True     # e.g. LimitReachedError: no more creates in this run
    D.save(PLAN, plan); return None

# ---------------------------------------------------------------- editorial feedback
def latest_metrics():
    p = f"{D.REPO}/logs/metrics.csv"; last = {}
    if os.path.exists(p):
        for r in csv.DictReader(open(p)):
            try: last[(r["video_id"], r["platform"], r["metric"])] = float(r["value"])
            except ValueError: pass
    return last

def video_rows(st, cal, m):
    rows = []
    for vid in sorted({k[0] for k in m}):
        v = st["videos"].get(vid) or {}
        dur = (v.get("duration_ms") or 0) / 1000 or ((v.get("qa") or {}).get("duration_s"))
        aw = m.get((vid, "tiktok", "averageTimeWatched"))
        rows.append({"id": vid, "categoria": cal[vid]["categoria"], "slot": cal[vid]["slot"], "duration_s": dur,
                     "tt_views": m.get((vid, "tiktok", "views")), "yt_views": m.get((vid, "youtube", "views")),
                     "tt_avg_watch_s": aw, "tt_retention": round(aw / dur, 3) if aw and dur else None,
                     "comments": sum(m.get((vid, p, "comments"), 0) for p in D.CHANNELS),
                     "comment_metrics": sum(1 for p in D.CHANNELS if (vid, p, "comments") in m)})
    return rows

def next_unproduced(st, cal):
    """First calendar video after the last one that already has a script (rules never apply retroactively)."""
    have = [v for v in cal if os.path.exists(f"{D.REPO}/template/videos/v{v}.py")]
    last = max(have) if have else "000"
    return next((v for v in sorted(cal) if v > last), None)

def experiment_active(prev, nxt):
    ex = prev.get("experiment") or {}
    return bool(ex) and nxt is not None and ex.get("applies_from", "999") <= nxt <= ex.get("freeze_until", "000")

def compute_rules(rows, prev, nxt):
    rules = dict(DEFAULT_RULES); rules.update({k: v for k, v in (prev.get("rules") or {}).items() if k in rules})
    if experiment_active(prev, nxt):   # one change at a time: R1–R3 stay frozen while the experiment runs
        ex = prev["experiment"]
        return rules, [f"Reglas R1–R3 congeladas por el experimento '{ex['name']}' ({ex['applies_from']}–{ex['freeze_until']})"], {}
    why = []
    rets = [r["tt_retention"] for r in rows if r["tt_retention"]]
    # R1 — retention -> duration ceiling and hook length (needs >= 4 videos with TikTok watch time)
    if len(rets) >= 4:
        med = statistics.median(rets)
        tgt, hook = (28.0, 9) if med < 0.40 else ((33.0, 12) if med >= 0.50 else (30.0, 10))
        ev = (prev.get("evaluation") or {}).get("R1")
        if ev and ev.get("verdict") == "sin mejora": tgt, hook = 33.0, 12   # reverted after a failed trial
        why.append(f"R1: proporción media vista (visionado medio / duración) mediana TikTok {med:.0%} en {len(rets)} vídeos (umbral 40 %/50 %) → duración máx {tgt:g} s, gancho ≤ {hook} palabras")
        rules["target_max_s"], rules["hook_max_words"] = tgt, hook
    else:
        why.append(f"R1: solo {len(rets)} vídeos con tiempo de visionado (<4): sin cambio")
    # R2 — no comments at all -> explicit question in the caption (needs >= 6 posts measured)
    n = sum(r["comment_metrics"] for r in rows); tot = sum(r["comments"] for r in rows)
    rules["caption_cta"] = n >= 6 and tot == 0
    why.append(f"R2: {tot:g} comentarios en {n} publicaciones medidas → pregunta en el texto: {'sí' if rules['caption_cta'] else 'no'}")
    # R3 — category with clearly lower watch time gets a stricter hook rule (needs >= 3 videos per category)
    cats = {}
    for r in rows:
        if r["tt_avg_watch_s"]: cats.setdefault(r["categoria"], []).append(r["tt_avg_watch_s"])
    rules["weak_category"] = None
    if len(cats) >= 2 and all(len(v) >= 3 for v in cats.values()):
        med = {c: statistics.median(v) for c, v in cats.items()}; lo, hi = min(med, key=med.get), max(med, key=med.get)
        if med[lo] <= 0.8 * med[hi]: rules["weak_category"] = lo
        why.append(f"R3: visionado medio TikTok {', '.join(f'{c} {v:.1f} s' for c, v in med.items())} → categoría débil: {rules['weak_category'] or 'ninguna'}")
    else:
        why.append("R3: menos de 3 vídeos medidos en alguna categoría: sin cambio (" + ", ".join(f"{c}={len(v)}" for c, v in cats.items()) + ")")
    changed = {k: (prev.get("rules", {}).get(k), rules[k]) for k in ("target_max_s", "hook_max_words", "caption_cta", "weak_category")
               if prev.get("rules", {}).get(k, DEFAULT_RULES[k]) != rules[k]}
    if changed or not rules.get("applies_from"): rules["applies_from"] = nxt
    return rules, why, changed

def evaluate(rows, rules, prev):
    """After >= 6 videos produced under the R1 ceiling, compare their TikTok retention with the 6 before."""
    ev = dict(prev.get("evaluation") or {}); af = rules.get("applies_from")
    if not af or rules["target_max_s"] >= 33.0: return ev
    after = [r["tt_retention"] for r in rows if r["id"] >= af and r["tt_retention"]]
    before = [r["tt_retention"] for r in rows if r["id"] < af and r["tt_retention"]][-6:]
    if len(after) >= 6 and before:
        d = statistics.median(after) - statistics.median(before)
        ev["R1"] = {"before": round(statistics.median(before), 3), "after": round(statistics.median(after), 3), "delta": round(d, 3),
                    "verdict": "mejora" if d >= 0.03 else "sin mejora"}
    return ev

def cmd_editorial(_):
    st = D.state(); cal = {r["id"]: r for r in D.load(D.CAL)}; m = latest_metrics()
    rows = video_rows(st, cal, m); prev = D.load(EDITORIAL, {}) or {}
    rules, why, changed = compute_rules(rows, prev, next_unproduced(st, cal))
    ev = evaluate(rows, rules, prev)
    if ev.get("R1") and ev["R1"] != (prev.get("evaluation") or {}).get("R1") and ev["R1"]["verdict"] == "sin mejora":
        rules2, why2, changed2 = compute_rules(rows, {**prev, "evaluation": ev, "rules": rules}, next_unproduced(st, cal))
        rules, why, changed = rules2, why + ["R1 evaluada sin mejora → se revierte"], {**changed, **changed2}
    out = {"updated": D.now_local().isoformat(timespec="seconds"), "rules": rules, "reasons": why, "evaluation": ev,
           "inputs": rows, "videos_measured": [r["id"] for r in rows]}
    if prev.get("experiment"): out["experiment"] = prev["experiment"]
    D.save(EDITORIAL, out)
    if changed or not prev:
        new = not os.path.exists(EDITORIAL_LOG)
        with open(EDITORIAL_LOG, "a") as fh:
            if new: fh.write("# CurioLab — registro de decisiones editoriales (generado por `daily.py editorial`)\n")
            fh.write(f"\n## {out['updated']} — aplica desde el vídeo {rules['applies_from']}\n")
            for k, (a, b) in changed.items(): fh.write(f"- **{k}**: {a} → {b}\n")
            if not changed: fh.write("- Reglas iniciales (sin cambios respecto a los valores por defecto).\n")
            fh.write("- Motivos:\n" + "".join(f"  - {w}\n" for w in why))
            fh.write("- Datos: " + "; ".join(f"{r['id']} ret {r['tt_retention'] if r['tt_retention'] is not None else '—'} vis {r['tt_avg_watch_s'] or '—'} s com {r['comments']:g}" for r in rows) + "\n")
        D.log("INFO", f"editorial: cambios {changed} aplican desde {rules['applies_from']}")
    print(json.dumps({k: out[k] for k in ("rules", "reasons", "evaluation", "videos_measured")}, ensure_ascii=False, indent=1))

def editorial_check(vid, lines, duration_s):
    """Used by `daily.py render`: True/False/None (None = rules do not apply to this video)."""
    ed = D.load(EDITORIAL, None)
    if not ed or not ed["rules"].get("applies_from") or vid < ed["rules"]["applies_from"]: return None, {}
    r = ed["rules"]; hook = len(lines[0].split())
    res = {"duration_s": duration_s, "target_max_s": r["target_max_s"], "duration_ok": duration_s <= r["target_max_s"] + 0.3,
           "hook_words": hook, "hook_max_words": r["hook_max_words"], "hook_ok": hook <= r["hook_max_words"],
           "rules_updated": ed["updated"], "measured": ed.get("videos_measured", [])}
    ex = ed.get("experiment") or {}
    if ex and vid >= ex.get("applies_from", "999"):
        # experiment "gancho en acción": first line is ONE clear question (the in-action first scene is checked visually)
        q = lines[0].strip(); res["experiment"] = ex.get("name")
        res["hook_question_ok"] = q.startswith("¿") and q.endswith("?") and q.count("?") == 1
        return res["duration_ok"] and res["hook_ok"] and res["hook_question_ok"], res
    return res["duration_ok"] and res["hook_ok"], res

# ---------------------------------------------------------------- cycle evidence
def cmd_cycle(_):
    st = D.state(); cal = {r["id"]: r for r in D.load(D.CAL)}; m = latest_metrics(); ed = D.load(EDITORIAL, {}) or {}
    first = (D.load(D.CONFIG, {}) or {}).get("cycle_from_id", "010")
    rep = {"cycle_from_id": first, "stages": {}}
    A = None
    for vid in sorted(cal):
        if vid < first: continue
        v = st["videos"][vid]
        ok = {"produced_qa": bool((v.get("qa") or {}).get("all_pass")), "hosted": bool(v.get("media_url")),
              "scheduled_both": all(p in v["posts"] for p in D.CHANNELS),
              "published_both_with_url": all(v["posts"].get(p, {}).get("status") == "sent" and v["posts"][p].get("url") for p in D.CHANNELS),
              "metrics_both": all((vid, p, "views") in m for p in D.CHANNELS),
              "fed_editorial": vid in (ed.get("videos_measured") or [])}
        if A is None or sum(ok.values()) > sum(rep["stages"]["A"]["checks"].values()):
            A = vid; rep["stages"]["A"] = {"id": vid, "checks": ok}
        if all(ok.values()): break
    B = None
    if A and all(rep["stages"]["A"]["checks"].values()):
        for vid in sorted(cal):
            if vid <= A: continue
            q = st["videos"][vid].get("qa") or {}; e = q.get("editorial") or {}
            if A not in (e.get("measured") or []): continue      # produced with rules that already included A's metrics
            ok = {"produced_under_rules_with_A": True, "editorial_pass": bool(q.get("editorial_pass")),
                  "scheduled_both": all(p in st["videos"][vid]["posts"] for p in D.CHANNELS)}
            B = vid; rep["stages"]["B"] = {"id": vid, "checks": ok}
            if all(ok.values()): break
    else:
        rep["stages"]["B"] = {"id": None, "checks": {"waiting_for_A": False}}
    allok = A and B and all(rep["stages"]["A"]["checks"].values()) and all(rep["stages"]["B"]["checks"].values())
    rep["verdict"] = "PASS" if allok else "PENDING"
    # THIS run: production passing is not a complete cycle. Reconcile, metrics, pre-create, scheduling and confirm
    # must all PASS in this run; otherwise the run is PARCIAL (or BLOQUEADO if Buffer could not even be read).
    rs = D.load(D.RUN_STATUS, None) or {"stages": {}}; sg = rs.get("stages", {})
    req = ("reconcile", "metrics", "pre-create", "scheduling", "confirm")
    missing = [k for k in req if sg.get(k, {}).get("status") != "PASS"]
    run_v = "BLOQUEADO" if sg.get("reconcile", {}).get("status") != "PASS" else ("COMPLETO" if not missing else "PARCIAL")
    out = {"run": {"run_id": rs.get("run_id"), "started": rs.get("started"), "verdict": run_v,
                   "required": {k: sg.get(k, {"status": "NO EJECUTADA"}) for k in req},
                   "production": {k: v for k, v in sg.items() if k.startswith("production_")},
                   "not_passed": missing},
           "verdict": run_v, "historical_cycle": rep}
    print(json.dumps(out, ensure_ascii=False, indent=1))
