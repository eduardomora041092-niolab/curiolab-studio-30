"""Master manifest for CurioLab Studio 30 (reads the calendar + per-video QA files).
Run after build_calendar.py:  python3 build_manifest.py
"""
import csv, json, os, datetime as dt

ROOT = "/home/claude/curiolab"
cal = json.load(open(f"{ROOT}/calendar/calendar.json"))

qa = {}
for vid in ("002", "003"):
    p = f"{ROOT}/work/{vid}/qa.json"
    if os.path.exists(p):
        qa[vid] = json.load(open(p))

counts = {}
for r in cal:
    counts[r["estado"]] = counts.get(r["estado"], 0) + 1

manifest = {
    "proyecto": "CurioLab Studio 30 (AI SHORTS 30)",
    "generado": dt.datetime.now().isoformat(timespec="seconds"),
    "resumen_estados": counts,
    "costo_real_usd": 0,
    "creditos_vidiq_usados_en_produccion": 0,
    "creditos_vidiq_usados_en_investigacion": 20,
    "herramientas": {
        "investigacion": "vidIQ (trending_videos, keyword_research, outliers, instagram_tiktok_outlier_search) — 20 créditos del plan, US$0",
        "produccion": "Python 3 + Pillow + NumPy (animación), Kokoro ONNX v1.0 voz em_alex (narración local), ffmpeg libx264/aac (montaje y loudness)",
        "distribucion": "Buffer (organización 'My organization' 6ad737f3bb7377f2534a518d); canales YouTube 6ad73b1a778b240e2f677dbf y TikTok 6ad739bd778b240e2f677654",
    },
    "rutas": {
        "calendario_csv": f"{ROOT}/calendar/CurioLab_calendario_90.csv",
        "plantilla_motor": f"{ROOT}/template/engine.py",
        "plantilla_build": f"{ROOT}/template/build.py",
        "specs_videos": f"{ROOT}/template/videos/",
        "salidas_mp4": f"{ROOT}/out/",
        "fuente_video_001": "/home/claude/v001/render.py (archivado, no modificado)",
        "modelos_voz": "/home/claude/v001/models/",
    },
    "entregables": [],
}
for r in cal:
    e = {k: r[k] for k in ("id", "fecha", "categoria", "titulo", "estado", "archivo", "buffer_post_ids", "youtube_url", "tiktok_url", "notas")}
    if r["id"] in qa:
        q = qa[r["id"]]
        e["qa"] = {"all_pass": q["all_pass"], "duracion_s": q["duration_s"], "lufs": q["lufs"], "checks": q["checks"], "sync_sheet": q["sync_sheet"]}
    if r["estado"] != "PLANNED":
        manifest["entregables"].append(e)
manifest["planificados"] = [r["id"] for r in cal if r["estado"] == "PLANNED"]

json.dump(manifest, open(f"{ROOT}/manifest/CurioLab_manifiesto.json", "w"), ensure_ascii=False, indent=1)

# Readable markdown: manifest + calendar summary
L = ["# CurioLab Studio 30 — Manifiesto maestro", "",
     f"Generado: {manifest['generado']} · Costo real: **US$0** · Créditos vidIQ en producción: **0**", "",
     "## Estado", ""]
L += [f"- **{k}**: {v}" for k, v in sorted(counts.items())]
L += ["", "## Entregables con archivo", "", "| ID | Título | Estado | Archivo | QA / evidencia |", "|---|---|---|---|---|"]
for e in manifest["entregables"]:
    ev = e["notas"] or ""
    if "qa" in e:
        ev = f"QA {'PASS' if e['qa']['all_pass'] else 'FAIL'} · {e['qa']['duracion_s']} s · {e['qa']['lufs']} LUFS"
    if e["buffer_post_ids"]:
        ev = f"{ev} · Buffer: {e['buffer_post_ids']}"
    L.append(f"| {e['id']} | {e['titulo']} | {e['estado']} | `{e['archivo']}` | {ev} |")
L += ["", f"Planificados: {len(manifest['planificados'])} vídeos ({manifest['planificados'][0]}–{manifest['planificados'][-1]}).", "",
      "## Herramientas", ""] + [f"- **{k}**: {v}" for k, v in manifest["herramientas"].items()]
L += ["", "## Rutas", ""] + [f"- {k}: `{v}`" for k, v in manifest["rutas"].items()]
L += ["", "## Calendario de 30 días (3 vídeos/día: 2 mecanismos + 1 ciencia)", ""]
day = None
for r in cal:
    if r["dia"] != day:
        day = r["dia"]; L += ["", f"**Día {day} · {r['fecha']}**"]
    L.append(f"- {r['id']} · {r['categoria']} · {r['titulo']} — _{r['gancho']}_ ({r['duracion_objetivo']}, {r['dificultad']}) · {r['estado']}")
open(f"{ROOT}/manifest/CurioLab_manifiesto.md", "w").write("\n".join(L) + "\n")
print(counts)
