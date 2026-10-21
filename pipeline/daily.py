"""CurioLab Studio 30 — daily orchestrator (deterministic parts of the pipeline).

The scheduled Claude session follows RUNBOOK.md and calls these sub-commands; the steps that
need MCP connectors (Buffer, Drive) or judgement (writing scripts, checking visuals) are done by
Claude itself, and their results are written back here with `record` / `log`.

  python3 daily.py guard                       -> ACTIVE | ENDED (experiment window, America/New_York)
  python3 daily.py status [--date YYYY-MM-DD]  -> JSON work list: due videos and what each still needs
  python3 daily.py render ID                   -> build + QA (template/build.py); marks PRODUCED if QA passes
  python3 daily.py host ID                     -> copies MP4 into media/, commits+pushes, verifies the public URL
  python3 daily.py caption ID                  -> JSON with caption text, YouTube title, scheduled time
  python3 daily.py record ID PLATFORM POST_ID STATUS [URL]
  python3 daily.py metrics FILE.json           -> appends Buffer per-post metrics to metrics.csv
  python3 daily.py log LEVEL MESSAGE           -> appends to logs/run_log.csv
  python3 daily.py export                      -> regenerates calendar CSV + manifest (MD/JSON)
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

def cmd_guard(_):
    today = now_local().date()
    st = state()
    done = all(v["estado"] == "PUBLISHED" for v in st["videos"].values())
    print("ENDED" if today > END or done else ("WAITING" if today < START else "ACTIVE"))

def published_platforms(v):
    return sorted(p for p, x in v["posts"].items() if x.get("status") in ("sent", "scheduled", "sending"))

def cmd_status(args):
    day = dt.date.fromisoformat(args[1]) if len(args) > 1 and args[0] == "--date" else now_local().date()
    cal = {r["id"]: r for r in load(CAL)}; st = state(); out = []
    for vid, r in cal.items():
        if dt.date.fromisoformat(r["fecha"]) > day: continue
        v = st["videos"][vid]
        missing = [p for p in CHANNELS if p not in published_platforms(v)]
        if not missing: continue
        spec = os.path.exists(f"{REPO}/template/videos/v{vid}.py")
        mp4 = os.path.exists(f"{REPO}/out/CurioLab_{vid}.mp4")
        out.append({"id": vid, "fecha": r["fecha"], "slot": r["slot"], "titulo": r["titulo"], "categoria": r["categoria"],
                    "gancho": r["gancho"], "concepto_visual": r["concepto_visual"], "estado": v["estado"],
                    "needs": [n for n, c in (("spec", not spec), ("render", not (mp4 and v["qa"] and v["qa"]["all_pass"])),
                                             ("host", not v["media_url"]), ("publish", True)) if c],
                    "missing_platforms": missing, "overdue": dt.date.fromisoformat(r["fecha"]) < day})
    print(json.dumps({"date": day.isoformat(), "pending": out}, ensure_ascii=False, indent=1))

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
    if qa["all_pass"] and v["estado"] == "PLANNED": v["estado"] = "PRODUCED"
    save(STATE, st); log("INFO" if qa["all_pass"] else "ERROR", f"{vid} QA all_pass={qa['all_pass']}")
    sys.exit(0 if qa["all_pass"] else 2)

def cmd_host(args):
    """Publish the MP4 in the public media repo and verify Buffer can download it."""
    vid = args[0]; cfg = load(CONFIG, {})
    if not cfg.get("media_raw_base"):
        print("BLOCKED: pipeline/config.json has no media_raw_base (public GitHub repo not configured)"); sys.exit(3)
    src = f"{REPO}/out/CurioLab_{vid}.mp4"; os.makedirs(f"{REPO}/media", exist_ok=True)
    dst = f"{REPO}/media/CurioLab_{vid}.mp4"; shutil.copy2(src, dst)
    subprocess.run(["git", "-C", REPO, "add", dst], check=True)
    subprocess.run(["git", "-C", REPO, "commit", "-m", f"media: CurioLab_{vid}.mp4"], check=False)
    subprocess.run(["git", "-C", REPO, "push"], check=True)
    url = f"{cfg['media_raw_base'].rstrip('/')}/media/CurioLab_{vid}.mp4"
    size = os.path.getsize(dst); ok = False
    for _ in range(12):
        h = subprocess.run(["curl", "-sSIL", "--max-time", "20", url], capture_output=True, text=True).stdout.lower()
        if " 200" in h and f"content-length: {size}" in h: ok = True; break
        subprocess.run(["sleep", "10"])
    st = state()
    if ok:
        st["videos"][vid]["media_url"] = url; save(STATE, st); log("INFO", f"{vid} hosted {url}"); print(url)
    else:
        log("ERROR", f"{vid} public URL not verified {url}"); print("FAILED " + url); sys.exit(1)

def cmd_caption(args):
    vid = args[0]; r = {x["id"]: x for x in load(CAL)}[vid]
    tags = "#CurioLab #ComoFunciona #Curiosidades #Ciencia" if r["categoria"] == "Mecanismo" else "#CurioLab #Ciencia #Curiosidades #Naturaleza"
    text = f"{r['gancho']} {r['titulo']}\n\nExplicado en menos de 35 segundos.\n\n{tags} #Shorts"
    due = dt.datetime.combine(dt.date.fromisoformat(r["fecha"]), dt.time.fromisoformat(SLOT_TIMES[r["slot"]]), TZ)
    mode = "customScheduled" if due > now_local() + dt.timedelta(minutes=20) else "shareNow"
    print(json.dumps({"id": vid, "text": text, "youtube_title": r["titulo"][:100], "youtube_categoryId": "27",
                      "asset_title": f"CurioLab_{vid}.mp4", "mode": mode, "dueAt": due.isoformat() if mode == "customScheduled" else None,
                      "channels": CHANNELS, "organizationId": ORG}, ensure_ascii=False, indent=1))

def cmd_record(args):
    vid, platform, post_id, status = args[:4]; url = args[4] if len(args) > 4 else ""
    st = state(); v = st["videos"][vid]
    v["posts"][platform] = {"post_id": post_id, "status": status, "url": url, "recorded": now_local().isoformat(timespec="seconds")}
    if all(v["posts"].get(p, {}).get("status") == "sent" for p in CHANNELS): v["estado"] = "PUBLISHED"
    save(STATE, st); log("INFO", f"{vid} {platform} {post_id} {status} {url}")

def cmd_metrics(args):
    rows = json.load(open(args[0])); p = f"{REPO}/logs/metrics.csv"; new = not os.path.exists(p)
    with open(p, "a", newline="") as fh:
        w = csv.writer(fh)
        if new: w.writerow(["captured_local", "video_id", "platform", "post_id", "metric", "value"])
        for r in rows:
            for m in r.get("metrics", []):
                w.writerow([now_local().isoformat(timespec="seconds"), r["video_id"], r["platform"], r["post_id"], m["type"], m["value"]])
    log("INFO", f"metrics appended for {len(rows)} posts")

def cmd_log(args):
    log(args[0], " ".join(args[1:]))

def cmd_export(_):
    cal = load(CAL); st = state()
    for r in cal:
        v = st["videos"][r["id"]]; r["estado"] = v["estado"]
        r["youtube_url"] = v["posts"].get("youtube", {}).get("url", "")
        r["tiktok_url"] = v["posts"].get("tiktok", {}).get("url", "")
        r["buffer_post_ids"] = "; ".join(f"{p}:{x['post_id']}" for p, x in v["posts"].items())
        mp4 = f"{REPO}/out/CurioLab_{r['id']}.mp4"
        if os.path.exists(mp4): r["archivo"] = mp4
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
     "record": cmd_record, "metrics": cmd_metrics, "log": cmd_log, "export": cmd_export}[sys.argv[1]](sys.argv[2:])
