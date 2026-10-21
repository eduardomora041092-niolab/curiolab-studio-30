"""One-shot check of the environment-preparation step: install -> load model -> synthesize voice.
Writes evidence/setup/setup_check_<timestamp>.json. Does not publish anything."""
import datetime as dt, json, os, subprocess, sys, time
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
res = {"started": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "steps": {}}
def step(name, fn):
    t = time.time()
    try: out = fn(); res["steps"][name] = {"ok": True, "seconds": round(time.time() - t, 1), "detail": out}
    except Exception as e: res["steps"][name] = {"ok": False, "error": f"{type(e).__name__}: {e}"}; finish(1)
def finish(code):
    p = f"{REPO}/evidence/setup/setup_check_{dt.datetime.now().strftime('%Y%m%d_%H%M')}.json"
    json.dump(res, open(p, "w"), ensure_ascii=False, indent=1); print(json.dumps(res, ensure_ascii=False, indent=1)); sys.exit(code)
def install():
    r = subprocess.run(["bash", f"{REPO}/setup.sh"], capture_output=True, text=True)
    if r.returncode: raise RuntimeError((r.stdout + r.stderr)[-800:])
    import importlib.metadata as md
    return {p: md.version(p) for p in ("kokoro-onnx", "onnxruntime", "phonemizer", "espeakng-loader", "soundfile", "pillow", "numpy")}
def load():
    from kokoro_onnx import Kokoro
    global K; K = Kokoro(f"{REPO}/models/kokoro-v1.0.onnx", f"{REPO}/models/voices-v1.0.bin")
    return {"voices_es": [v for v in K.get_voices() if v[:2] in ("ef", "em")]}
def voice():
    import soundfile as sf
    s, sr = K.create("Prueba de voz de CurioLab Studio treinta.", voice="em_alex", speed=1.08, lang="es")
    p = f"{REPO}/evidence/setup/voice_sample.wav"; sf.write(p, s, sr)
    peak = float(abs(s).max())
    if len(s) / sr < 1.0 or peak < 0.01: raise RuntimeError(f"audio inválido dur={len(s)/sr:.2f}s peak={peak:.3f}")
    return {"seconds": round(len(s) / sr, 2), "sample_rate": sr, "peak": round(peak, 3), "file": "evidence/setup/voice_sample.wav"}
step("install", install); step("load_model", load); step("voice", voice); finish(0)
