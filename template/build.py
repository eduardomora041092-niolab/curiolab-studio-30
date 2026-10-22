"""Build one CurioLab Short from a spec module.
Usage:  python3 build.py videos/v002.py            # full build + QA
        python3 build.py videos/v002.py --preview  # narration + scene-midpoint stills only
Outputs: /home/claude/curiolab/out/CurioLab_<ID>.mp4 and /home/claude/curiolab/work/<ID>/ (wav, segs, qa.json, sheets)
"""
import importlib.util, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_spec(path):
    sp = importlib.util.spec_from_file_location("spec", path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    for k, v in (("VOICE", "em_alex"), ("SPEED", 1.08), ("SUBTITLE", "¿CÓMO FUNCIONA POR DENTRO?")):
        if not hasattr(m, k): setattr(m, k, v)
    if not hasattr(m, "sfx"): m.sfx = lambda segs: []
    return m

def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate:format=duration",
                        "-of", "json", path], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)

def loudness(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    return float(m[-1]) if m else None

def qa(spec, segs, mp4, work):
    info = probe(mp4); v = [s for s in info["streams"] if s["codec_type"] == "video"][0]
    a = [s for s in info["streams"] if s["codec_type"] == "audio"]
    dur = float(info["format"]["duration"]); expected = segs[-1]["end"] + 1.0
    checks = {
        "resolution_1080x1920": (v["width"], v["height"]) == (1080, 1920),
        "fps_30": v["r_frame_rate"] == "30/1",
        "video_h264": v["codec_name"] == "h264",
        "audio_aac": bool(a) and a[0]["codec_name"] == "aac",
        "duration_25_35s": 25.0 <= dur <= 35.5,
        "duration_matches_narration": abs(dur - expected) < 0.2,
        "one_scene_per_line": len(segs) == len(spec.LINES),
        "segments_ordered": all(segs[i]["end"] <= segs[i + 1]["start"] for i in range(len(segs) - 1)),
        "narration_ends_before_video": segs[-1]["end"] < dur,
    }
    lufs = loudness(mp4); checks["loudness_-17_to_-12_LUFS"] = lufs is not None and -17 <= lufs <= -12
    # sync evidence: one frame per narration line, extracted from the FINAL mp4
    frames = []
    for s in segs:
        t = round(s["start"] + 0.75 * (s["end"] - s["start"]), 2)
        p = f"{work}/final_{t:.2f}.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", mp4, "-frames:v", "1", p], check=True); frames.append(p)
    sheet = E.contact_sheet(frames, f"{work}/final_sheet.png")
    rep = {"id": spec.ID, "file": mp4, "duration_s": round(dur, 3), "lufs": lufs, "video": v, "checks": checks,
           "all_pass": all(checks.values()), "sync_sheet": sheet, "segments": segs}
    json.dump(rep, open(f"{work}/qa.json", "w"), ensure_ascii=False, indent=1)
    return rep

def main():
    spec = load_spec(sys.argv[1]); work = f"{ROOT}/work/{spec.ID}"; os.makedirs(work, exist_ok=True); os.makedirs(f"{ROOT}/out", exist_ok=True)
    segs_p, wav = f"{work}/segs.json", f"{work}/narr.wav"
    # regenerate narration whenever ANY line changed (previously only the first line was compared)
    if not os.path.exists(segs_p) or [s["text"] for s in json.load(open(segs_p))] != list(spec.LINES):
        segs = E.tts(spec.LINES, spec.VOICE, spec.SPEED, wav, segs_p)
    segs = json.load(open(segs_p))
    if "--preview" in sys.argv:
        times = [round(s["start"] + 0.75 * (s["end"] - s["start"]), 2) for s in segs]
        paths = E.preview(spec, segs, times, f"{work}/prev")
        print("sheet", E.contact_sheet(paths, f"{work}/preview_sheet.png")); return
    E.sfx_mix(segs, wav, spec.sfx(segs), f"{work}/mix.wav")
    E.render(spec, segs, f"{work}/video_noaudio.mp4")
    out = f"{ROOT}/out/CurioLab_{spec.ID}.mp4"
    E.mux(f"{work}/video_noaudio.mp4", f"{work}/mix.wav", out)
    rep = qa(spec, segs, out, work)
    print(json.dumps({k: rep[k] for k in ("id", "file", "duration_s", "lufs", "all_pass", "checks")}, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
