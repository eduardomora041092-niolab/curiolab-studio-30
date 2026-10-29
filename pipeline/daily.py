"""CurioLab Studio 30 — daily orchestrator (deterministic parts of the pipeline).

The scheduled Claude session follows RUNBOOK.md and calls these sub-commands; the steps that
need MCP connectors (Buffer, Drive) or judgement (writing scripts, checking visuals) are done by
Claude itself, and their results are written back here with `record` / `log`.

  python3 daily.py guard                       -> ACTIVE | ENDED (experiment window, America/New_York)
  python3 daily.py status [--date YYYY-MM-DD]  -> JSON work list: due videos and what each still needs
  python3 daily.py render ID                   -> build + QA (template/build.py); marks PRODUCED if QA passes
  python3 daily.py host ID                     -> copies MP4 into media/, commits+pushes, verifies the public URL
  python3 daily.py caption ID                  -> JSON with caption text, YouTube title, scheduled time
  python3 daily.py record ID PLATFORM POST_ID STATUS [URL]   (failed create: record ID PLATFORM - failed "MSG")
  python3 daily.py lock acquire|check|release   -> run lock with owner token (see cmd_lock)
  python3 daily.py metrics FILE.json           -> appends Buffer per-post metrics to metrics.csv
  python3 daily.py log LEVEL MESSAGE           -> appends to logs/run_log.csv
  python3 daily.py export                      -> regenerates calendar CSV + manifest (MD/JSON)
  python3 daily.py stage NAME STATUS [MSG]     -> records a stage outcome of THIS run in pipeline/run_status.json
  python3 daily.py snapshot-links DIR          -> get_post calls needed for public links (MCP snapshot)
  python3 daily.py snapshot-query | queue SNAP.json | editorial | cycle   -> see queue_editorial.py
"""
import csv, datetime as dt, json, os, shutil, subprocess, sys
from zoneinfo import ZoneInfo

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TZ = ZoneInfo("America/New_York")
START, END = dt.date(2026, 10, 20), dt.date(2026, 11, 18)
STATE = f"{REPO}/pipeline/state.json"
CAL = f"{REPO}/calendar/calendar.json"
CHANNELS = {"youtube": "6ad73b1a778b240e2f677dbf", "tiktok": "6ad739bd778b240e2f677654"}
ORG = "6ad737f3bb7377f2534a518d"
SLOT_TIMES = {1: "09:00", 2: "13:00", 3: "18:00"}   # local publish times per daily slot
CONFIG = f"{REPO}/pipeline/config.json"
MAX_NEW_PER_RUN = 3   # at most 3 new videos (one calendar day) produced per run

def now_local():
    return dt.datetime.now(TZ)

def load(p, default=None):
    return json.load(open(p)) if os.path.exists(p) else default

def save(p, obj):
    tmp = p + ".tmp"; json.dump(obj, open(tmp, "w"), ensure_ascii=False, indent=1); os.replace(tmp, p)

def state():
    st = load(STATE)
    if st is None:
        st = {"videos": {r["id"]: {"estado": r["estado"], "posts": {}, "qa": None, "media_url": None, "errors": []} for r in load(CAL)}}
    return st

def log(level, msg):
    os.makedirs(f"{REPO}/logs", exist_ok=True); p = f"{REPO}/logs/run_log.csv"; new = not os.path.exists(p)
    with open(p, "a", newline="") as fh:
        w = csv.writer(fh)
        if new: w.writerow(["timestamp_local", "level", "message"])
        w.writerow([now_local().isoformat(timespec="seconds"), level, msg])

RUN_STATUS = f"{REPO}/pipeline/run_status.json"
STAGE_STATES = ("PASS", "FAIL", "BLOCKED", "PENDING", "SKIP")

def stage(name, status, msg=""):
    """Outcome of one stage of THIS run (reset by `lock acquire`). `cycle` derives the run verdict from it: production
    alone never makes a run complete — reconcile, metrics, pre-create, scheduling and confirm must all PASS."""
    assert status in STAGE_STATES, status
    rs = load(RUN_STATUS, None) or {"run_id": None, "started": now_local().isoformat(timespec="seconds"), "stages": {}}
    rs["stages"][name] = {"status": status, "msg": msg, "at": now_local().isoformat(timespec="seconds")}
    save(RUN_STATUS, rs); log("INFO" if status in ("PASS", "SKIP") else "ERROR" if status in ("FAIL", "BLOCKED") else "WARN", f"etapa {name}: {status} {msg}".strip())

def cmd_stage(args):
    stage(args[0], args[1], " ".join(args[2:]))

def cmd_guard(_):
    today = now_local().date()
    st = state()
    done = all(v["estado"] == "PUBLISHED" for v in st["videos"].values())
    print("ENDED" if today > END or done else ("WAITING" if today < START else "ACTIVE"))

def published_platforms(v):
    return sorted(p for p, x in v["posts"].items() if x.get("status") in ("sent", "scheduled", "sending"))

def cmd_status(args):
    # default: everything due through TOMORROW (one day of production slack); publishing respects the Buffer limit
    day = dt.date.fromisoformat(args[1]) if len(args) > 1 and args[0] in ("--date", "--through") else now_local().date() + dt.timedelta(days=1)
    cal = {r["id"]: r for r in load(CAL)}; st = state(); out = []
    for vid, r in cal.items():
        if dt.date.fromisoformat(r["fecha"]) > day: continue
        v = st["videos"][vid]
        missing = [p for p in CHANNELS if p not in published_platforms(v)]
        if not missing: continue
        spec = os.path.exists(f"{REPO}/template/videos/v{vid}.py")
        mp4 = os.path.exists(f"{REPO}/out/CurioLab_{vid}.mp4")
        if not spec and sum(1 for o in out if "spec" in o["needs"]) >= MAX_NEW_PER_RUN: continue
        out.append({"id": vid, "fecha": r["fecha"], "slot": r["slot"], "titulo": r["titulo"], "categoria": r["categoria"],
                    "gancho": r["gancho"], "concepto_visual": r["concepto_visual"], "estado": v["estado"],
                    "needs": [n for n, c in (("spec", not spec), ("render", not (mp4 and v["qa"] and v["qa"]["all_pass"])),
                                             ("host", not v["media_url"]), ("publish", True)) if c],
                    "missing_platforms": missing, "overdue": dt.date.fromisoformat(r["fecha"]) < day})
    ed = load(f"{REPO}/pipeline/editorial.json", {}) or {}
    print(json.dumps({"date": day.isoformat(), "editorial_rules": ed.get("rules"), "editorial_reasons": ed.get("reasons"),
                      "pending": out}, ensure_ascii=False, indent=1))

def cmd_render(args):
    vid = args[0]; spec = f"{REPO}/template/videos/v{vid}.py"
    r = subprocess.run([sys.executable, f"{REPO}/template/build.py", spec], capture_output=True, text=True)
    print(r.stdout[-3000:]); print(r.stderr[-3000:], file=sys.stderr)
    qa = load(f"{REPO}/work/{vid}/qa.json")
    st = state(); v = st["videos"][vid]
    if r.returncode != 0 or not qa:
        v["errors"].append(f"{now_local().isoformat(timespec='seconds')} render failed rc={r.returncode}")
        save(STATE, st); log("ERROR", f"{vid} render failed"); sys.exit(1)
    v["qa"] = {k: qa[k] for k in ("all_pass", "duration_s", "lufs", "checks")}
    # editorial rules derived from metrics (pipeline/editorial.json); they apply from rules.applies_from onwards
    import importlib.util, queue_editorial as QE
    sp = importlib.util.spec_from_file_location("spec", spec); mod = importlib.util.module_from_spec(sp); sp.loader.exec_module(mod)
    ok, info = QE.editorial_check(vid, mod.LINES, qa["duration_s"])
    if ok is not None:
        v["qa"]["editorial"] = info; v["qa"]["editorial_pass"] = ok
        qa["editorial"] = info; qa["all_pass"] = qa["all_pass"] and ok; v["qa"]["all_pass"] = qa["all_pass"]
        json.dump(qa, open(f"{REPO}/work/{vid}/qa.json", "w"), ensure_ascii=False, indent=1)
        print(f"EDITORIAL {'PASS' if ok else 'FAIL'} {json.dumps(info, ensure_ascii=False)}")
    ev = f"{REPO}/evidence/{vid}"; os.makedirs(ev, exist_ok=True)   # evidence kept in the repo
    for f in ("qa.json", "segs.json", "final_sheet.png", "preview_sheet.png"):
        if os.path.exists(f"{REPO}/work/{vid}/{f}"): shutil.copy2(f"{REPO}/work/{vid}/{f}", f"{ev}/{f}")
    if qa["all_pass"] and v["estado"] == "PLANNED": v["estado"] = "PRODUCED"
    save(STATE, st); log("INFO" if qa["all_pass"] else "ERROR", f"{vid} QA all_pass={qa['all_pass']}")
    stage(f"production_{vid}", "PASS" if qa["all_pass"] else "FAIL", f"{qa['duration_s']} s")
    sys.exit(0 if qa["all_pass"] else 2)

def cmd_host(args):
    """Publish the MP4 as a one-file orphan branch `media-NNN` (no fetch needed, clone of main stays small)
    and verify the public raw URL serves the exact file size."""
    vid = args[0]; cfg = load(CONFIG, {}); repo_url = cfg.get("repo_url"); base = cfg.get("media_raw_base")
    if not repo_url or not base:
        print("BLOCKED: pipeline/config.json needs repo_url and media_raw_base"); sys.exit(3)
    src = f"{REPO}/out/CurioLab_{vid}.mp4"; size = os.path.getsize(src)
    branch = f"media-{vid}"; url = f"{base.rstrip('/')}/{branch}/CurioLab_{vid}.mp4"
    def verify():
        h = subprocess.run(["curl", "-sSIL", "--max-time", "30", url], capture_output=True, text=True).stdout.lower()
        return " 200" in h and f"content-length: {size}" in h
    if not verify():
        tmp = f"/tmp/curiolab_media_{vid}"; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
        g = lambda *a: subprocess.run(["git", "-C", tmp, *a], check=True, capture_output=True, text=True)
        g("init", "-q"); g("checkout", "-q", "--orphan", branch); shutil.copy2(src, f"{tmp}/CurioLab_{vid}.mp4")
        g("add", f"CurioLab_{vid}.mp4")
        g("-c", "user.name=CurioLab bot", "-c", "user.email=noreply@anthropic.com", "commit", "-qm", f"media CurioLab_{vid}.mp4")
        g("push", "-q", "-f", repo_url, f"{branch}:refs/heads/{branch}")
        for _ in range(18):
            if verify(): break
            subprocess.run(["sleep", "10"])
    st = state()
    if verify():
        st["videos"][vid]["media_url"] = url; save(STATE, st); log("INFO", f"{vid} hosted {url}"); print(url)
    else:
        log("ERROR", f"{vid} public URL not verified {url}"); print("FAILED " + url); sys.exit(1)

CTA_LINE = "¿Qué objeto o fenómeno quieres que expliquemos? Te leemos en comentarios."

def caption(vid, now=None):
    r = {x["id"]: x for x in load(CAL)}[vid]
    tags = "#CurioLab #ComoFunciona #Curiosidades #Ciencia" if r["categoria"] == "Mecanismo" else "#CurioLab #Ciencia #Curiosidades #Naturaleza"
    ed = load(f"{REPO}/pipeline/editorial.json", {}) or {}
    rules = ed.get("rules", {}) or {}
    if rules.get("applies_from") and vid < rules["applies_from"] and ed.get("rules_before"):
        rules = ed["rules_before"]   # never retroactive: videos before applies_from keep the rules they were made with
    cta = bool(rules.get("caption_cta"))          # editorial rule R2 (metrics-driven)
    text = f"{r['gancho']} {r['titulo']}\n\nExplicado en menos de 35 segundos." + (f"\n\n{CTA_LINE}" if cta else "") + f"\n\n{tags} #Shorts"
    due = dt.datetime.combine(dt.date.fromisoformat(r["fecha"]), dt.time.fromisoformat(SLOT_TIMES[r["slot"]]), TZ)
    # Calendar slot in the future -> scheduled for that slot (normal design). Slot already passed -> shareNow.
    # If a safety check denies an action, it is recorded and reported; it is never worked around.
    mode = "customScheduled" if due > (now or now_local()) + dt.timedelta(minutes=5) else "shareNow"
    # TikTok cover: frame where the whole first line (the hook question) is already on screen, instead of frame 0
    segs = load(f"{REPO}/evidence/{vid}/segs.json") or load(f"{REPO}/work/{vid}/segs.json")
    cover_ms = int(max(0.0, segs[0]["end"] - 0.15) * 1000) if segs else None
    return {"id": vid, "text": text, "youtube_title": r["titulo"][:100], "youtube_categoryId": "27",
            "asset_title": f"CurioLab_{vid}.mp4", "mode": mode, "dueAt": due.isoformat() if mode == "customScheduled" else None,
            "channels": CHANNELS, "organizationId": ORG, "editorial_cta": cta, "tiktok_cover_offset_ms": cover_ms}

def cmd_caption(args):
    print(json.dumps(caption(args[0]), ensure_ascii=False, indent=1))

def cmd_record(args):
    """record ID PLATFORM POST_ID STATUS [URL]; after a failed create_post: record ID PLATFORM - failed "MESSAGE"."""
    import queue_editorial as QE
    vid, platform, post_id, status = args[:4]; url = args[4] if len(args) > 4 else ""
    warn = QE.record_result(vid, platform, post_id, status)
    if warn: log("WARN", warn); print(f"WARN {warn}")
    if status == "failed":
        log("ERROR", f"create_post {vid} {platform} falló: {url}"); stage("scheduling", "FAIL", f"create_post {vid} {platform}: {url}")
        print("OK (fallo registrado; no se crean más en este plan)"); return
    st = state(); v = st["videos"][vid]
    v["posts"][platform] = {"post_id": post_id, "status": status, "url": url, "recorded": now_local().isoformat(timespec="seconds")}
    if all(v["posts"].get(p, {}).get("status") == "sent" for p in CHANNELS): v["estado"] = "PUBLISHED"
    save(STATE, st); log("INFO", f"{vid} {platform} {post_id} {status} {url}")

def norm_vid(x):
    """Video id as the 3-digit calendar string. Accepts the legacy metrics-due shape [id, durationMs]."""
    if isinstance(x, (list, tuple)): x = x[0] if x else None
    if isinstance(x, int): x = f"{x:03d}"
    return x if isinstance(x, str) and len(x) == 3 and x.isdigit() else None

def cmd_metrics(args):
    rows = json.load(open(args[0])); p = f"{REPO}/logs/metrics.csv"
    cal = {r["id"] for r in load(CAL)}; bad = []
    for r in rows:   # validate everything first: nothing is written if any row is malformed
        v = norm_vid(r.get("video_id"))
        if v is None or v not in cal or r.get("platform") not in CHANNELS or not r.get("post_id"): bad.append(r.get("video_id"))
        else: r["video_id"] = v
    if bad:
        print(f"ERROR: filas de métricas no válidas (video_id/platform/post_id): {bad}; no se escribe nada"); sys.exit(2)
    new = not os.path.exists(p)
    with open(p, "a", newline="") as fh:
        w = csv.writer(fh)
        if new: w.writerow(["captured_local", "video_id", "platform", "post_id", "metric", "value"])
        for r in rows:
            for m in r.get("metrics", []):
                w.writerow([now_local().isoformat(timespec="seconds"), r["video_id"], r["platform"], r["post_id"], m["type"], m["value"]])
    log("INFO", f"metrics appended for {len(rows)} posts"); stage("metrics", "PASS", f"{len(rows)} posts capturados")

SENT_AT = f"{REPO}/logs/sent_at.json"
BANDS = {"24h": (21, 45), "72h": (69, 93)}

def cmd_metrics_due(args):
    """metrics-due SNAP.json -> posts to capture now: first capture inside the ~24 h band (21–45 h) and inside the
    ~72 h band (69–93 h), plus the usual one-per-day capture. Also records each post's real sentAt in logs/sent_at.json."""
    import queue_editorial as QE
    snap = QE.read_snapshot([args[0]]); sent = load(SENT_AT, {}) or {}
    caps = {}
    if os.path.exists(f"{REPO}/logs/metrics.csv"):
        for r in csv.DictReader(open(f"{REPO}/logs/metrics.csv")): caps.setdefault(r["post_id"], set()).add(r["captured_local"])
    now = now_local(); due = []
    for n in QE.nodes(snap, "recent") + QE.nodes(snap, "open"):
        if n.get("status") != "sent" or not n.get("sentAt"): continue
        vid, _dur = QE.vid_of(n)   # vid_of returns (id, durationMs); only the id identifies the video
        if not vid: continue
        sa = dt.datetime.fromisoformat(n["sentAt"].replace("Z", "+00:00")); sent[n["id"]] = n["sentAt"]
        age = (now - sa).total_seconds() / 3600
        ages = [(dt.datetime.fromisoformat(c) - sa).total_seconds() / 3600 for c in caps.get(n["id"], ())]
        band = next((b for b, (lo, hi) in BANDS.items() if lo <= age <= hi and not any(lo <= a <= hi for a in ages)), None)
        today = any(dt.datetime.fromisoformat(c).date() == now.date() for c in caps.get(n["id"], ()))
        if band or (age >= 21 and not today):
            due.append({"video_id": vid, "platform": n.get("channelService") or ("youtube" if n["channelId"] == CHANNELS["youtube"] else "tiktok"),
                        "post_id": n["id"], "age_h": round(age, 1), "band": band})
    save(SENT_AT, sent); print(json.dumps(due, ensure_ascii=False, indent=1))
    stage("metrics", "PENDING" if due else "PASS", f"{len(due)} capturas pendientes" if due else "sin capturas pendientes")

GROUPS = [("001-012", "antes de reglas", "001", "012"), ("013-015", "R1+R2", "013", "015"),
          ("016-018", "R1+R2+R3", "016", "018"), ("019-027", "R1+R2+R3 + gancho_en_accion", "019", "027")]

def cmd_compare(args):
    """compare [24h|72h] -> per-video metrics at equal age. Shows the EXACT age of every measurement (hours since
    the real sentAt); the band only limits which captures qualify. 'prop. media vista' = average watch time /
    video duration (TikTok): an average share of the video watched, NOT the share of people who finished it."""
    import statistics
    band = args[0] if args else "24h"; lo, hi = BANDS[band]; centre = 72 if band == "72h" else 24
    sent = load(SENT_AT, {}) or {}; cal = {r["id"]: r for r in load(CAL)}; st = state()
    rows = {}
    for r in csv.DictReader(open(f"{REPO}/logs/metrics.csv")):
        if r["post_id"] not in sent: continue
        a = (dt.datetime.fromisoformat(r["captured_local"]) - dt.datetime.fromisoformat(sent[r["post_id"]].replace("Z", "+00:00"))).total_seconds() / 3600
        if lo <= a <= hi: rows.setdefault((r["video_id"], r["platform"], r["captured_local"]), {"age": a})[r["metric"]] = float(r["value"])
    best = {}
    for (v, p, c), m in rows.items():
        if (v, p) not in best or abs(m["age"] - centre) < abs(best[(v, p)]["age"] - centre): best[(v, p)] = m
    print(f"Captura más cercana a {centre} h dentro de {lo}-{hi} h. La antigüedad exacta de cada medición va en cada fila.")
    print("prop. media vista = visionado medio / duración del vídeo (NO es el % de personas que lo terminaron).")
    for name, rule, a, b in GROUPS:
        ids = [v for v in sorted(cal) if a <= v <= b]
        print(f"\n[{name}] {rule}")
        tt_prop, tt_watch, tt_views, yt_views = [], [], [], []
        for v in ids:
            t, y = best.get((v, "tiktok")), best.get((v, "youtube"))
            if not t and not y: continue
            d = (st["videos"][v].get("qa") or {}).get("duration_s")
            if t:
                pr = t.get("averageTimeWatched", 0) / d if d else None
                tt = f"TT medido a {t['age']:.1f} h: vistas {t.get('views',0):.0f}, visionado medio {t.get('averageTimeWatched',0):.2f} s, prop. media vista {pr:.0%}" if pr is not None else f"TT medido a {t['age']:.1f} h: vistas {t.get('views',0):.0f}"
                tt_views.append(t.get("views", 0)); tt_watch.append(t.get("averageTimeWatched", 0))
                if pr is not None: tt_prop.append(pr)
            else: tt = "TT sin medición en la franja"
            if y: yv = f"YT medido a {y['age']:.1f} h: vistas {y.get('views',0):.0f}"; yt_views.append(y.get("views", 0))
            else: yv = "YT sin medición en la franja"
            print(f"  {v} {cal[v]['categoria'][:5]:5} franja {cal[v]['slot']} | {tt} | {yv}")
        med = lambda x: f"{statistics.median(x):.2f}" if x else "—"
        print(f"  mediana (n TT={len(tt_views)}, n YT={len(yt_views)}): TT vistas {med(tt_views)}, visionado medio {med(tt_watch)} s, "
              f"prop. media vista {statistics.median(tt_prop):.0%}" if tt_prop else f"  sin datos en esta franja (n=0)", end="")
        print(f", YT vistas {med(yt_views)}" if tt_prop else "")

LOCK_TTL = dt.timedelta(hours=2)

def cmd_lock(args):
    """lock acquire|check|release — one run at a time. The lock lives in the repo (pipeline/lock.json) so a second
    session sees it after cloning. acquire writes a random token, kept by this clone in .git/curiolab_lock_token
    (never committed). check/release only act if the remote lock carries THIS clone's token, so a run never frees a
    lock that another run took over. A lock older than LOCK_TTL is stale and may be taken over (logged as WARN).
    release requires a clean worktree (commit the run first) and fails loudly if pull/commit/push fail; in that case
    the remote lock stays and expires after LOCK_TTL."""
    import secrets
    action = args[0]; p = f"{REPO}/pipeline/lock.json"; tokfile = f"{REPO}/.git/curiolab_lock_token"
    git = lambda *a: subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True)
    mine = open(tokfile).read().strip() if os.path.exists(tokfile) else None
    f = git("fetch", "-q", "origin", "main")   # read the REMOTE lock without touching the worktree
    if f.returncode != 0:
        print(f"ERROR: git fetch falló: {f.stderr.strip()[:300]}"); sys.exit(8 if action == "release" else 4)
    shown = git("show", "origin/main:pipeline/lock.json")
    cur = json.loads(shown.stdout) if shown.returncode == 0 and shown.stdout.strip() else None
    owner = bool(cur and mine and cur.get("token") == mine)
    if action == "check":
        print("OWNER" if owner else ("NOT_OWNER" if cur else "NONE")); sys.exit(0 if owner else 7)
    if action == "release":
        if not cur: print("OK (sin candado)"); return
        if not owner:
            print(f"NOT_OWNER: el candado ({cur['since']}) es de otra ejecución; no se toca"); log("WARN", "release: candado ajeno, no se libera"); sys.exit(7)
        dirty = [l for l in git("status", "--porcelain").stdout.splitlines() if not l.endswith("pipeline/lock.json")]
        if dirty:
            print(f"ERROR: cambios sin commit ({len(dirty)}); haz commit y push de la ejecución antes de liberar"); sys.exit(8)
    if action == "acquire" and cur and now_local() - dt.datetime.fromisoformat(cur["since"]) < LOCK_TTL:
        print(f"BUSY since {cur['since']}"); log("WARN", f"run skipped: lock held since {cur['since']}"); sys.exit(4)
    r = git("pull", "-q", "--rebase", "origin", "main")
    if r.returncode != 0:
        print(f"ERROR: git pull falló: {r.stderr.strip()[:300]}"); sys.exit(8 if action == "release" else 4)
    if action == "acquire":
        if cur: log("WARN", f"lock caducado desde {cur['since']} retomado")
        tok = secrets.token_hex(8); save(p, {"since": now_local().isoformat(timespec="seconds"), "token": tok})
        open(tokfile, "w").write(tok)
        save(RUN_STATUS, {"run_id": tok[:6], "started": now_local().isoformat(timespec="seconds"), "stages": {}})
    else:   # release (ownership checked above against the remote lock)
        if os.path.exists(p): os.remove(p)
    git("add", "-A", "pipeline/lock.json")
    if action == "acquire" and os.path.exists(f"{REPO}/logs/run_log.csv"): git("add", "logs/run_log.csv")   # keeps a takeover WARN
    if action == "acquire": git("add", "pipeline/run_status.json")   # fresh stage journal for this run
    c = git("-c", "user.name=CurioLab bot", "-c", "user.email=noreply@anthropic.com", "commit", "-qm", f"lock {action}")
    if c.returncode != 0:
        print(f"ERROR: commit del candado falló: {(c.stderr or c.stdout).strip()[:300]}"); sys.exit(8 if action == "release" else 4)
    r = git("push", "-q", "origin", "main")
    if r.returncode != 0 and action == "release":   # someone pushed meanwhile: rebase once and retry
        if git("pull", "-q", "--rebase", "origin", "main").returncode == 0: r = git("push", "-q", "origin", "main")
    if r.returncode != 0:
        if action == "acquire":
            git("reset", "-q", "HEAD~1")   # undo only our lock commit; nothing else is touched
            if git("cat-file", "-e", "HEAD:pipeline/lock.json").returncode == 0: git("checkout", "-q", "HEAD", "--", "pipeline/lock.json")
            elif os.path.exists(p): os.remove(p)
            if os.path.exists(tokfile): os.remove(tokfile)
            print("BUSY (push rejected)"); sys.exit(4)
        print(f"ERROR: push de la liberación falló: {r.stderr.strip()[:300]}; el candado caducará en {LOCK_TTL}"); sys.exit(8)
    if action == "release" and os.path.exists(tokfile): os.remove(tokfile)
    print("OK")

def cmd_log(args):
    log(args[0], " ".join(args[1:]))

def cmd_export(_):
    cal = load(CAL); st = state()
    for r in cal:
        v = st["videos"][r["id"]]; r["estado"] = v["estado"]
        r["youtube_url"] = v["posts"].get("youtube", {}).get("url", "")
        r["tiktok_url"] = v["posts"].get("tiktok", {}).get("url", "")
        r["buffer_post_ids"] = "; ".join(f"{p}:{x['post_id']}" for p, x in v["posts"].items())
        r["archivo"] = v.get("media_url") or ""
        if v["estado"] == "PUBLISHED": r["notas"] = ""
    with open(f"{REPO}/calendar/CurioLab_calendario_90.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cal[0].keys())); w.writeheader(); w.writerows(cal)
    counts = {}
    for r in cal: counts[r["estado"]] = counts.get(r["estado"], 0) + 1
    L = ["# CurioLab Studio 30 — Manifiesto maestro", "", f"Actualizado: {now_local().isoformat(timespec='minutes')} (America/New_York) · Costo real: US$0", "",
         "## Estado", ""] + [f"- **{k}**: {v}" for k, v in sorted(counts.items())]
    L += ["", "## Vídeos con actividad", "", "| ID | Fecha | Título | Estado | YouTube | TikTok | QA |", "|---|---|---|---|---|---|---|"]
    for r in cal:
        v = st["videos"][r["id"]]
        if r["estado"] == "PLANNED" and not v["posts"]: continue
        qa = v["qa"]; qas = f"{'PASS' if qa['all_pass'] else 'FAIL'} {qa['duration_s']} s {qa['lufs']} LUFS" if qa else "verificado (fase anterior)"
        L.append(f"| {r['id']} | {r['fecha']} | {r['titulo']} | {r['estado']} | {r['youtube_url'] or '—'} | {r['tiktok_url'] or '—'} | {qas} |")
    L += ["", "## Calendario completo", ""]
    for r in cal:
        L.append(f"- {r['id']} · {r['fecha']} · {r['categoria']} · {r['titulo']} · {r['estado']}")
    open(f"{REPO}/manifest/CurioLab_manifiesto.md", "w").write("\n".join(L) + "\n")
    save(f"{REPO}/manifest/CurioLab_manifiesto.json", {"actualizado": now_local().isoformat(timespec="minutes"), "estados": counts,
         "costo_real_usd": 0, "videos": {r["id"]: {**{k: r[k] for k in ("fecha", "titulo", "categoria", "estado")}, **st["videos"][r["id"]]} for r in cal}})
    print(counts)

if __name__ == "__main__":
    {"guard": cmd_guard, "status": cmd_status, "render": cmd_render, "host": cmd_host, "caption": cmd_caption,
     "record": cmd_record, "lock": cmd_lock, "metrics-due": cmd_metrics_due, "compare": cmd_compare, "metrics": cmd_metrics, "log": cmd_log, "export": cmd_export, "stage": cmd_stage,
     **{k: (lambda a, k=k: getattr(__import__("queue_editorial"), "cmd_" + k.replace("-", "_"))(a))
        for k in ("snapshot-query", "snapshot-links", "queue", "create-next", "editorial", "cycle")}}[sys.argv[1]](sys.argv[2:])
