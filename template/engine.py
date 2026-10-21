"""CurioLab Studio 30 — reusable Shorts engine (extracted from the approved Video 001 pipeline).

A video is a small Python "spec" module that defines:
    ID          "002"
    TITLE       on-screen/working title
    SUBTITLE    header line under the brand, e.g. "¿CÓMO FUNCIONA POR DENTRO?"
    VOICE       Kokoro voice id ("em_alex" default, "ef_dora", "em_santa")
    SPEED       narration speed (1.08 used in 001)
    LINES       list of narration sentences (one scene per line)
    KEYWORDS    set of lowercase words highlighted in amber in captions
    scene(i, u, L, E, im, d)   draws scene i at local time u (seconds) of length L
    sfx(segs)   optional -> list of ("zip"|"click"|"whoosh"|"pop", t_seconds[, dur])

Everything else (background, header, captions, camera push-in, crossfades, TTS, SFX mix,
loudness, encode 1080x1920/30fps H.264+AAC, QA) lives here and is shared by all videos.
"""
import json, math, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, S = 1080, 1920, 30, 2
FONT_B = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FONT_X = "/usr/share/fonts/truetype/google-fonts/Poppins-ExtraBold.ttf"
try:
    ImageFont.truetype(FONT_X, 10)
except OSError:
    FONT_X = FONT_B
MODELS = os.environ.get("CURIOLAB_MODELS", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models"))

# Brand palette
BG1, BG2 = (11, 18, 32), (22, 33, 58)
AMB = (255, 176, 32)
WHITE = (245, 247, 250)
MUTED = (170, 185, 210)
GRID = (28, 40, 66)
SIL, SIL_D, SIL_H = (205, 212, 222), (128, 138, 152), (240, 244, 248)
BRA, BRA_D, BRA_H = (224, 179, 90), (160, 118, 45), (250, 220, 150)
BLUE, BLUE_D = (43, 108, 176), (30, 78, 130)
HOT, HOT_D = (238, 84, 54), (170, 50, 30)
COLD = (90, 170, 255)
CAV = (20, 27, 44)

# Safe zone for captions (YouTube Shorts / TikTok): centred, max 800 px wide, block centred near y=1370
CAP_MAX_W, CAP_Y = 800, 1370
VISUAL_BOTTOM = 1190  # scene art is clipped below this line

_font_cache = {}
def font(size, bold_x=True):
    path = FONT_X if bold_x else FONT_B
    k = (size, path)
    if k not in _font_cache:
        _font_cache[k] = ImageFont.truetype(path, int(size * S))
    return _font_cache[k]

def P(*v):
    return [x * S for x in v]

def ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def back_out(x):
    x = max(0.0, min(1.0, x)); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

def lerp(a, b, t):
    return a + (b - a) * t

def mix(c1, c2, t):
    return tuple(int(lerp(c1[i], c2[i], max(0, min(1, t)))) for i in range(3))

# ---------- background ----------
def make_bg():
    im = Image.new("RGB", (W * S, H * S)); d = ImageDraw.Draw(im)
    for y in range(H * S):
        c = mix(BG1, BG2, y / (H * S)); d.line([(0, y), (W * S, y)], fill=c)
    for x in range(0, W, 60):
        d.line(P(x, 0, x, H), fill=GRID, width=S)
    for y in range(0, H, 60):
        d.line(P(0, y, W, y), fill=GRID, width=S)
    return im
BG = make_bg()

# ---------- primitives ----------
def rrect(d, x0, y0, x1, y1, r, fill, outline=None, w=2):
    d.rounded_rectangle(P(x0, y0, x1, y1), radius=r * S, fill=fill, outline=outline, width=w * S if outline else 0)

def poly(d, pts, fill=None, outline=None, w=2):
    d.polygon([(x * S, y * S) for x, y in pts], fill=fill, outline=outline, width=w * S if outline else 0)

def line(d, pts, color, w=4):
    d.line([(x * S, y * S) for x, y in pts], fill=color, width=int(w * S), joint="curve")

def circle(d, x, y, r, fill=None, outline=None, w=2):
    d.ellipse(P(x - r, y - r, x + r, y + r), fill=fill, outline=outline, width=w * S if outline else 0)

def arrow(d, x0, y0, x1, y1, color=AMB, w=6, head=26):
    d.line(P(x0, y0, x1, y1), fill=color, width=int(w * S))
    a = math.atan2(y1 - y0, x1 - x0)
    pts = [(x1, y1), (x1 - head * math.cos(a - 0.5), y1 - head * math.sin(a - 0.5)), (x1 - head * math.cos(a + 0.5), y1 - head * math.sin(a + 0.5))]
    poly(d, pts, fill=color)

def wave(d, x0, y0, x1, y1, wavelength, amp, color, w=5, phase=0.0, head=True):
    """Sine wave travelling from (x0,y0) to (x1,y1); used for light/heat/sound."""
    L = math.hypot(x1 - x0, y1 - y0)
    if L < 2: return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    pts = []
    n = max(8, int(L / 4))
    for k in range(n + 1):
        s = L * k / n
        o = amp * math.sin(2 * math.pi * s / wavelength - phase)
        pts.append((x0 + ux * s + nx * o, y0 + uy * s + ny * o))
    line(d, pts, color, w)
    if head:
        arrow(d, x1 - ux * 2, y1 - uy * 2, x1, y1, color=color, w=w, head=22)

def label(d, text, x, y, size=54, color=AMB, anchor="mm"):
    d.text((x * S, y * S), text, font=font(size), fill=color, anchor=anchor, stroke_width=int(5 * S), stroke_fill=BG1)

def pill(d, text, x, y, size=40, fg=BG1, bg=AMB):
    f = font(size)
    bb = d.textbbox((0, 0), text, font=f)
    tw, th = (bb[2] - bb[0]) / S, (bb[3] - bb[1]) / S
    rrect(d, x - tw / 2 - 28, y - th / 2 - 18, x + tw / 2 + 28, y + th / 2 + 22, 40, bg)
    d.text((x * S, y * S), text, font=f, fill=fg, anchor="mm")

def cross(d, x, y, r=40, color=HOT, w=12):
    d.line(P(x - r, y - r, x + r, y + r), fill=color, width=w * S)
    d.line(P(x - r, y + r, x + r, y - r), fill=color, width=w * S)

def outro(d, u, subtitle_cta="SÍGUEME"):
    d.text((W / 2 * S, 560 * S), "CurioLab", font=font(120), fill=WHITE, anchor="mm")
    d.text((W / 2 * S, 690 * S), "STUDIO 30", font=font(64), fill=AMB, anchor="mm")
    k = back_out(u / 0.5)
    if k > 0.05:
        pill(d, subtitle_cta, W / 2, 860, 50)

# ---------- header & captions ----------
def header(d, subtitle):
    d.text((W / 2 * S, 175 * S), "CURIOLAB STUDIO 30", font=font(34), fill=MUTED, anchor="mm")
    d.text((W / 2 * S, 222 * S), subtitle, font=font(30, False), fill=AMB, anchor="mm")

def captions(d, t, segs, keywords):
    cur = None
    for s in segs:
        if s["start"] - 0.05 <= t < s["end"] + 0.25:
            cur = s
    if cur is None: return
    words = cur["text"].split(); n = len(words); dur = cur["end"] - cur["start"]
    f = font(66); space = d.textlength(" ", font=f) / S
    lines, ln, lw = [], [], 0
    for wd in words:
        wl = d.textlength(wd, font=f) / S
        if ln and lw + space + wl > CAP_MAX_W:
            lines.append(ln); ln, lw = [], 0
        ln.append((wd, wl)); lw += (space if lw else 0) + wl
    lines.append(ln)
    y = CAP_Y - (len(lines) - 1) * 44; idx = 0
    for ln in lines:
        total = sum(w for _, w in ln) + space * (len(ln) - 1); x = W / 2 - total / 2
        for wd, wl in ln:
            if t >= cur["start"] + dur * idx / n - 0.02:
                core = wd.strip("¿?¡!,.:;").lower()
                col = AMB if core in keywords else WHITE
                d.text((x * S, y * S), wd, font=f, fill=col, anchor="lm", stroke_width=int(7 * S), stroke_fill=(5, 9, 18))
            x += wl + space; idx += 1
        y += 88

# ---------- timeline / frame composition ----------
XF = 0.25  # crossfade seconds

class Timeline:
    def __init__(self, spec, segs):
        self.spec, self.segs = spec, segs
        self.total = segs[-1]["end"] + 1.0
    def bounds(self, i):
        a = 0.0 if i == 0 else self.segs[i]["start"]
        b = self.segs[i + 1]["start"] if i + 1 < len(self.segs) else self.total
        return a, b
    def index(self, t):
        i = 0
        for j in range(len(self.segs)):
            if t >= self.bounds(j)[0]: i = j
        return i
    def scene_img(self, i, t):
        im = BG.copy(); d = ImageDraw.Draw(im)
        a, b = self.bounds(i)
        self.spec.scene(i, t - a, b - a, __import__(__name__), im, d)
        # keep scene art out of the caption zone (safe-zone guard shared by every video)
        im.paste(BG.crop((0, VISUAL_BOTTOM * S, W * S, H * S)), (0, VISUAL_BOTTOM * S))
        z = 1.0 + 0.035 * ease((t - a) / (b - a))  # gentle push-in
        cxs, cys = 540 * S, 760 * S; w2, h2 = W * S / z / 2, H * S / z / 2
        return im.resize((W, H), Image.LANCZOS, box=(cxs - w2, cys - h2 * (760 / 960), cxs + w2, cys + h2 * (2 - 760 / 960)))
    def frame(self, t):
        i = self.index(t); fr = self.scene_img(i, t); a = self.bounds(i)[0]
        if i > 0 and t - a < XF:
            fr = Image.blend(self.scene_img(i - 1, t), fr, ease((t - a) / XF))
        ov = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        header(od, self.spec.SUBTITLE); captions(od, t, self.segs, self.spec.KEYWORDS)
        ov = ov.resize((W, H), Image.LANCZOS)
        return Image.alpha_composite(fr.convert("RGBA"), ov).convert("RGB")

# ---------- narration (Kokoro, local) ----------
def tts(lines, voice, speed, wav_path, segs_path, gap=0.25):
    import soundfile as sf
    from kokoro_onnx import Kokoro
    k = Kokoro(f"{MODELS}/kokoro-v1.0.onnx", f"{MODELS}/voices-v1.0.bin")
    out, segs, t, sr = [], [], 0.0, 24000
    for i, l in enumerate(lines):
        s, sr = k.create(l, voice=voice, speed=speed, lang="es")
        d_ = len(s) / sr
        segs.append({"i": i, "text": l, "start": round(t, 3), "end": round(t + d_, 3)})
        out += [s, np.zeros(int(gap * sr), dtype=s.dtype)]; t += d_ + gap
    sf.write(wav_path, np.concatenate(out), sr)
    json.dump(segs, open(segs_path, "w"), ensure_ascii=False, indent=1)
    return segs

# ---------- sound effects (synthesised, copyright-free) ----------
def sfx_mix(segs, narr_wav, cues, out_wav):
    import soundfile as sf
    narr, sr = sf.read(narr_wav)
    total = segs[-1]["end"] + 1.0; n = int(total * sr); m = np.zeros(n); m[:len(narr)] += narr
    rng = np.random.default_rng(7)
    def put(t0, sig):
        i = int(t0 * sr); j = min(n, i + len(sig)); m[i:j] += sig[: j - i]
    for c in cues:
        kind, t0 = c[0], c[1]; dur = c[2] if len(c) > 2 else None
        if kind == "zip":
            dur = dur or 1.2; L = int(dur * sr); tt = np.arange(L) / sr; noise = rng.standard_normal(L)
            rate = np.linspace(28, 70, L); tick = (np.sin(2 * np.pi * np.cumsum(rate) / sr) > 0.92).astype(float)
            sig = np.convolve(noise * tick, np.ones(12) / 12, "same") + 0.15 * np.convolve(noise, np.ones(40) / 40, "same")
            env = np.minimum(1, tt / 0.05) * np.minimum(1, (dur - tt) / 0.15)
            put(t0, 0.16 * sig * env / np.abs(sig).max())
        elif kind == "click":
            L = int(0.06 * sr); tt = np.arange(L) / sr
            put(t0, 0.35 * (np.sin(2 * np.pi * 2400 * tt) * np.exp(-tt * 90) + 0.5 * rng.standard_normal(L) * np.exp(-tt * 200)))
        elif kind == "whoosh":
            dur = dur or 0.5; L = int(dur * sr); tt = np.arange(L) / sr
            sig = np.convolve(rng.standard_normal(L), np.ones(30) / 30, "same")
            put(t0, 0.25 * sig * np.sin(np.pi * tt / dur) ** 2 / np.abs(sig).max())
        elif kind == "pop":
            L = int(0.12 * sr); tt = np.arange(L) / sr
            f = np.linspace(900, 300, L)
            put(t0, 0.25 * np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-tt * 30))
    m /= max(1.0, np.abs(m).max() / 0.95)
    sf.write(out_wav, m, sr)

# ---------- render + mux ----------
def render(spec, segs, out_mp4):
    tl = Timeline(spec, segs); nfr = int(tl.total * FPS)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                           "-pix_fmt", "yuv420p", out_mp4], stdin=subprocess.PIPE)
    for k in range(nfr):
        ff.stdin.write(tl.frame(k / FPS).tobytes())
    ff.stdin.close(); ff.wait()
    return tl

def mux(video, wav, out):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", wav, "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", out], check=True)

def preview(spec, segs, times, prefix):
    tl = Timeline(spec, segs); paths = []
    for t in times:
        p = f"{prefix}_{t:.2f}.png"; tl.frame(t).save(p); paths.append(p)
    return paths

def contact_sheet(paths, out, cols=4, w=270, h=480):
    rows = math.ceil(len(paths) / cols); sheet = Image.new("RGB", (cols * w, rows * h))
    for i, p in enumerate(paths):
        sheet.paste(Image.open(p).resize((w, h)), ((i % cols) * w, (i // cols) * h))
    sheet.save(out); return out
