"""CurioLab Studio 30 — dynamic Buffer queue, publication reconciliation, editorial feedback, cycle check.

Called through daily.py:
  python3 daily.py snapshot-query          -> JSON {query, variables} for Buffer execute_query (read-only)
  python3 daily.py queue SNAP.json [...]   -> reconciles state with Buffer, computes free slots, prints the plan:
                                              which (video, platform) posts to create NOW and which must wait
  python3 daily.py editorial               -> recomputes pipeline/editorial.json from logs/metrics.csv and logs changes
  python3 daily.py cycle                   -> PASS/PENDING per stage of the autonomous cycle (evidence for the owner)

Design rules (unchanged controls): never more than limit-1 scheduled posts in the organisation; one post per
video and channel (duplicates are reported, never deleted); a post in `error` is recreated once at most; future
calendar slots are scheduled for their time (customScheduled), never earlier.
"""
import csv, datetime as dt, json, os, re, statistics
import daily as D

SAFETY_MARGIN = 1          # keep one slot free: "si hay 9 o más, no crees más"
RECENT_DAYS = 5            # window of posts fetched for reconciliation / duplicate detection
EDITORIAL = f"{D.REPO}/pipeline/editorial.json"
EDITORIAL_LOG = f"{D.REPO}/logs/editorial_log.md"
QUEUE_LOG = f"{D.REPO}/logs/queue_log.csv"
PLAN = f"{D.REPO}/pipeline/queue_plan.json"
PLATFORM_OF = {v: k for k, v in D.CHANNELS.items()}
DEFAULT_RULES = {"target_max_s": 33.0, "hook_max_words": 12, "caption_cta": False, "weak_category": None,
                 "applies_from": None}

# ---------------------------------------------------------------- Buffer snapshot
def cmd_snapshot_query(_):
    q = "\n".join(l for l in open(f"{D.REPO}/pipeline/buffer_snapshot.graphql").read().splitlines() if not l.startswith("#"))
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=RECENT_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(json.dumps({"query": q, "variables": {"org": D.ORG, "since": since, "channels": list(D.CHANNELS.values())}}, ensure_ascii=False, indent=1))

def read_snapshot(paths):
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
        if pick["status"] == "sent" and not url:
            warnings.append(f"SIN ENLACE {vid} {plat} {pick['id']}: sent sin externalLink; se reintenta en la próxima ejecución")
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
    return {"generated": now.isoformat(timespec="seconds"), "limit": limit, "safety_margin": SAFETY_MARGIN, "occupied": used,
            "free_after_plan": free, "per_channel_today": [{k: l.get(k) for k in ("channelId", "scheduled", "sent", "limit", "isAtLimit")} for l in lim.values()],
            "reconciled": reconciled, "create": create, "waiting": waiting, "blocked": blocked, "warnings": warnings}

def cmd_queue(args):
    data = read_snapshot(args); st = D.state(); cal = {r["id"]: r for r in D.load(D.CAL)}
    plan = plan_queue(data, st, cal, D.now_local())
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
    print(json.dumps(plan, ensure_ascii=False, indent=1))

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
    print(json.dumps(rep, ensure_ascii=False, indent=1))
