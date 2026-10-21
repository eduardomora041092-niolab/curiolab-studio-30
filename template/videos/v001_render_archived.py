"""CurioLab Studio 30 — Video 001: ¿Cómo funciona una cremallera por dentro?
Renders a 1080x1920 30fps schematic animation synced to the narration segments.
Usage: python3 render.py <segs.json> <out_video_noaudio.mp4> [preview_times...]
"""
import json, math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, S = 1080, 1920, 30, 2  # S = supersampling factor
FONT_B = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FONT_X = "/usr/share/fonts/truetype/google-fonts/Poppins-ExtraBold.ttf"
try:
    ImageFont.truetype(FONT_X, 10)
except OSError:
    FONT_X = FONT_B

BG1, BG2 = (11, 18, 32), (22, 33, 58)
TAPE, TAPE_D = (43, 108, 176), (30, 78, 130)
SIL, SIL_D, SIL_H = (205, 212, 222), (128, 138, 152), (240, 244, 248)
BRA, BRA_D, BRA_H = (224, 179, 90), (160, 118, 45), (250, 220, 150)
AMB = (255, 176, 32)
WHITE = (245, 247, 250)
CAV = (20, 27, 44)

segs = json.load(open(sys.argv[1]))
TOTAL = segs[-1]["end"] + 1.0
KEYWORDS = {"cremallera", "dientes", "cursor", "saliente", "hueco", "cuña", "trabados", "desfasadas", "imanes", "pegamento", "dentro"}

_font_cache = {}
def font(size, path=FONT_B):
    k = (size, path)
    if k not in _font_cache:
        _font_cache[k] = ImageFont.truetype(path, int(size * S))
    return _font_cache[k]

def P(*v):  # scale coordinates
    return [x * S for x in v]

def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)

def back_out(x):
    x = max(0.0, min(1.0, x)); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

# ---------- background ----------
def make_bg():
    im = Image.new("RGB", (W * S, H * S))
    d = ImageDraw.Draw(im)
    for y in range(H * S):
        t = y / (H * S)
        c = tuple(int(BG1[i] + (BG2[i] - BG1[i]) * t) for i in range(3))
        d.line([(0, y), (W * S, y)], fill=c)
    # subtle grid ("lab" feel)
    for x in range(0, W, 60):
        d.line(P(x, 0, x, H), fill=(28, 40, 66), width=S)
    for y in range(0, H, 60):
        d.line(P(0, y, W, y), fill=(28, 40, 66), width=S)
    return im
BG = make_bg()

# ---------- primitives ----------
def rrect(d, x0, y0, x1, y1, r, fill, outline=None, w=2):
    d.rounded_rectangle(P(x0, y0, x1, y1), radius=r * S, fill=fill, outline=outline, width=w * S if outline else 0)

def arrow(d, x0, y0, x1, y1, color=AMB, w=6):
    d.line(P(x0, y0, x1, y1), fill=color, width=w * S)
    a = math.atan2(y1 - y0, x1 - x0); L = 26
    pts = [(x1, y1), (x1 - L * math.cos(a - 0.5), y1 - L * math.sin(a - 0.5)), (x1 - L * math.cos(a + 0.5), y1 - L * math.sin(a + 0.5))]
    d.polygon([(x * S, y * S) for x, y in pts], fill=color)

def label(d, text, x, y, size=54, color=AMB, anchor="mm", alpha=1.0):
    if alpha <= 0: return
    f = font(size, FONT_X)
    d.text((x * S, y * S), text, font=f, fill=color, anchor=anchor, stroke_width=int(5 * S), stroke_fill=BG1)

def pill(d, text, x, y, size=40, fg=BG1, bg=AMB):
    f = font(size, FONT_X)
    bb = d.textbbox((0, 0), text, font=f)
    tw, th = (bb[2] - bb[0]) / S, (bb[3] - bb[1]) / S
    rrect(d, x - tw / 2 - 28, y - th / 2 - 18, x + tw / 2 + 28, y + th / 2 + 22, 40, bg)
    d.text((x * S, y * S), text, font=f, fill=fg, anchor="mm")

# ---------- front view zipper ----------
PITCH = 44
def sep_at(y, ys, maxsep):
    return max(0.0, min(maxsep, (ys - 70 - y) * 0.42))

def zipper_front(d, cx, top, bottom, ys, maxsep=170, slider=True, cutaway=False, im=None, wedge_glow=0.0):
    # tapes
    for side in (-1, 1):
        pts_in, pts_out = [], []
        y = top
        while y <= bottom:
            e = cx + side * (52 + sep_at(y, ys, maxsep))
            pts_in.append((e, y)); pts_out.append((e + side * 170, y)); y += 8
        poly = pts_in + pts_out[::-1]
        d.polygon([(x * S, yy * S) for x, yy in poly], fill=TAPE)
        d.line([(x * S, yy * S) for x, yy in pts_in], fill=TAPE_D, width=4 * S)
    # teeth (left row silver at k*p, right row brass offset by p/2)
    th = PITCH * 0.42
    k = 0
    while top + k * PITCH <= bottom:
        for side, off, col, dark in ((-1, 0, SIL, SIL_D), (1, PITCH / 2, BRA, BRA_D)):
            y = top + k * PITCH + off
            if y > bottom: continue
            s = sep_at(y, ys, maxsep)
            hi = SIL_H if side < 0 else BRA_H
            sh = th * 0.62; hh = PITCH * 0.47
            if side < 0:
                x0, x1, hx = cx - 64 - s, cx - 4 - s, cx + 4 - s
            else:
                x0, x1, hx = cx + 4 + s, cx + 64 + s, cx - 4 + s
            rrect(d, x0, y - sh / 2, x1, y + sh / 2, 5, col, outline=dark, w=2)
            d.ellipse(P(hx - 24, y - hh / 2, hx + 24, y + hh / 2), fill=col, outline=dark, width=2 * S)
            d.ellipse(P(hx - 12, y - hh / 2 + 3, hx + 6, y - 1), fill=hi)
        k += 1
    if slider:
        draw_slider(d, cx, ys, cutaway=cutaway, im=im, wedge_glow=wedge_glow)

def draw_slider(d, cx, ys, cutaway=False, im=None, wedge_glow=0.0):
    body = [(cx - 118, ys - 95), (cx + 118, ys - 95), (cx + 92, ys + 95), (cx - 92, ys + 95)]
    if cutaway and im is not None:
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        od.polygon([(x * S, y * S) for x, y in body], fill=(215, 221, 229, 70), outline=(240, 244, 248, 255), width=5 * S)
        im.paste(Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB"))
        # Y channel guide lines
        d.line(P(cx - 100, ys - 95, cx - 26, ys + 10, cx - 26, ys + 95), fill=WHITE, width=4 * S)
        d.line(P(cx + 100, ys - 95, cx + 26, ys + 10, cx + 26, ys + 95), fill=WHITE, width=4 * S)
        g = 1 + 0.15 * wedge_glow
        wpts = [(cx, ys - 95), (cx + 46 * g, ys - 40), (cx, ys + 10), (cx - 46 * g, ys - 40)]
        d.polygon([(x * S, y * S) for x, y in wpts], fill=AMB, outline=(255, 230, 170), width=3 * S)
    else:
        d.polygon([(x * S, y * S) for x, y in body], fill=(214, 220, 228), outline=(150, 160, 175), width=4 * S)
        d.polygon([(x * S, y * S) for x, y in [(cx - 100, ys - 80), (cx + 100, ys - 80), (cx + 84, ys - 60), (cx - 84, ys - 60)]], fill=SIL_H)
        # pull tab
        rrect(d, cx - 40, ys + 40, cx + 40, ys + 250, 28, (198, 205, 215), outline=(140, 150, 165), w=4)
        rrect(d, cx - 16, ys + 185, cx + 16, ys + 225, 12, (60, 72, 96))

# ---------- side profile tooth ----------
TW, THH = 300, 110
def tooth_side(d, cx, cy, col, dark, hi, scale=1.0, hollow=True, bump=True, bump_hl=False, hollow_hl=False):
    w, h = TW * scale, THH * scale
    if bump:
        d.ellipse(P(cx - 62 * scale, cy - h / 2 - 32 * scale, cx + 62 * scale, cy - h / 2 + 30 * scale), fill=AMB if bump_hl else col, outline=dark, width=3 * S)
    rrect(d, cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, 22 * scale, col, outline=dark, w=3)
    d.line(P(cx - w / 2 + 20 * scale, cy - h / 2 + 14 * scale, cx + w / 2 - 20 * scale, cy - h / 2 + 14 * scale), fill=hi, width=int(6 * scale) * S)
    if hollow:
        d.ellipse(P(cx - 68 * scale, cy + h / 2 - 38 * scale, cx + 68 * scale, cy + h / 2 + 28 * scale), fill=CAV, outline=AMB if hollow_hl else dark, width=(6 if hollow_hl else 3) * S)
        d.arc(P(cx - 56 * scale, cy + h / 2 - 30 * scale, cx + 56 * scale, cy + h / 2 + 20 * scale), 200, 340, fill=(60, 72, 100), width=int(4 * scale) * S)

# ---------- captions ----------
def captions(d, t):
    cur = None
    for s in segs:
        if s["start"] - 0.05 <= t < s["end"] + 0.25:
            cur = s
    if cur is None: return
    words = cur["text"].split()
    n = len(words); dur = cur["end"] - cur["start"]
    f = font(66, FONT_X)
    lines, line, lw = [], [], 0
    space = d.textlength(" ", font=f) / S
    for wd in words:
        wl = d.textlength(wd, font=f) / S
        if line and lw + space + wl > 800:
            lines.append(line); line, lw = [], 0
        line.append((wd, wl)); lw += (space if lw else 0) + wl
    lines.append(line)
    y = 1370 - (len(lines) - 1) * 44
    idx = 0
    for ln in lines:
        total = sum(w for _, w in ln) + space * (len(ln) - 1)
        x = W / 2 - total / 2
        for wd, wl in ln:
            appear = cur["start"] + dur * idx / n
            if t >= appear - 0.02:
                core = wd.strip("¿?¡!,.:").lower()
                col = AMB if (core in KEYWORDS or wd == "Y") else WHITE
                d.text((x * S, y * S), wd, font=f, fill=col, anchor="lm", stroke_width=int(7 * S), stroke_fill=(5, 9, 18))
            x += wl + space; idx += 1
        y += 88

def header(d, t):
    d.text((W / 2 * S, 175 * S), "CURIOLAB STUDIO 30", font=font(34, FONT_X), fill=(170, 185, 210), anchor="mm")
    d.text((W / 2 * S, 222 * S), "¿CÓMO FUNCIONA POR DENTRO?", font=font(30, FONT_B), fill=AMB, anchor="mm")

# ---------- scenes ----------
def seg_bounds(i):
    a = 0.0 if i == 0 else segs[i]["start"]
    b = segs[i + 1]["start"] if i + 1 < len(segs) else TOTAL
    return a, b

def scene(i, t, im, d):
    a, b = seg_bounds(i); u = t - a; L = b - a
    cx = W / 2
    if i == 0:  # hook: fast zip-up
        ys = 1080 - 640 * ease(u / 1.3)
        zipper_front(d, cx, 300, 1130, ys)
        if u > 1.3:
            k = back_out((u - 1.3) / 0.4)
            if k > 0.05:
                pill(d, "SIN IMANES", cx - 225, 1195, 38)
                pill(d, "SIN PEGAMENTO", cx + 185, 1195, 38)
    elif i == 1:  # teeth + slider labels
        zipper_front(d, cx, 300, 1130, 760)
        k1 = back_out(u / 0.4); k2 = back_out((u - L * 0.55) / 0.4)
        if k1 > 0:
            label(d, "DIENTES", 205, 420, 54); arrow(d, 260, 460, 430, 520)
        if u > L * 0.55:
            label(d, "CURSOR", 870, 640, 54); arrow(d, 840, 680, 680, 740)
    elif i == 2:  # tooth close-up
        k = back_out(u / 0.5)
        sc = 2.0 * max(k, 0.05)
        tooth_side(d, cx, 760, SIL, SIL_D, SIL_H, scale=sc, bump_hl=u > 0.9, hollow_hl=u > L * 0.6)
        if u > 0.9:
            label(d, "SALIENTE", cx, 470, 62); arrow(d, cx + 150, 500, cx + 80, 590)
        if u > L * 0.6:
            label(d, "HUECO", cx, 1080, 62); arrow(d, cx + 150, 1050, cx + 90, 900)
    elif i == 3:  # rows offset half a tooth
        shift = (PITCH * 1.6 / 2) * ease((u - 0.3) / 0.9)
        p = PITCH * 1.6; th = p * 0.42
        for k in range(10):
            yl = 380 + k * p
            rrect(d, cx - 230, yl - th / 2, cx - 70, yl + th / 2, 10, SIL, outline=SIL_D, w=2)
            yr = 380 + k * p + shift
            rrect(d, cx + 70, yr - th / 2, cx + 230, yr + th / 2, 10, BRA, outline=BRA_D, w=2)
        rrect(d, cx - 330, 330, cx - 230, 1130, 10, TAPE); rrect(d, cx + 230, 330, cx + 330, 1130, 10, TAPE)
        if u > 1.2:
            yb = 380 + 4 * p
            for yy in (yb, yb + p / 2):
                d.line(P(cx - 60, yy, cx + 60, yy), fill=AMB, width=4 * S)
            label(d, "½", cx, yb + p / 4, 70)
            label(d, "MEDIO DIENTE", cx, 1195, 50)
    elif i == 4:  # Y channel cutaway
        top, merge, bot = 400, 760, 1100
        body = [(cx - 330, top - 40), (cx + 330, top - 40), (cx + 200, bot), (cx - 200, bot)]
        d.polygon([(x * S, y * S) for x, y in body], fill=(40, 52, 80), outline=SIL, width=6 * S)
        for side in (-1, 1):
            d.line(P(cx + side * 250, top - 40, cx + side * 30, merge, cx + side * 30, bot), fill=(70, 86, 120), width=60 * S)
        wpts = [(cx, top - 40), (cx + 130, top + 120), (cx, merge - 30), (cx - 130, top + 120)]
        d.polygon([(x * S, y * S) for x, y in wpts], fill=(60, 74, 104), outline=SIL_D, width=3 * S)
        # teeth flowing down the arms and merging
        speed, gap = 130.0, 70.0
        arm = math.hypot(220, merge - (top - 40)); total = arm + (bot - merge)
        for side, col, dark, ph in ((-1, SIL, SIL_D, 0.0), (1, BRA, BRA_D, gap / 2)):
            for j in range(-2, 22):
                s = (u * speed + j * gap + ph) % (total + gap * 2) - gap
                if s < 0 or s > total: continue
                if s < arm:
                    f_ = s / arm
                    x = cx + side * (250 - 220 * f_); y = top - 40 + (merge - top + 40) * f_
                else:
                    x = cx + side * 30 - side * 12; y = merge + (s - arm)
                rrect(d, x - 36, y - 13, x + 36, y + 13, 7, col, outline=dark, w=2)
        label(d, "CANAL EN Y", cx, top - 110, 58)
        arrow(d, cx + 300, bot - 20, cx + 300, bot - 220, color=WHITE, w=5)
        label(d, "SUBE", cx + 300, bot + 30, 40, color=WHITE)
    elif i == 5:  # interlock in side profile
        base = 1010; step = THH + 2
        order = [(SIL, SIL_D, SIL_H), (BRA, BRA_D, BRA_H), (SIL, SIL_D, SIL_H), (BRA, BRA_D, BRA_H), (SIL, SIL_D, SIL_H)]
        clicks = [0.0, 0.8, 1.6, 2.4, 3.2]
        drawn = []
        for n_, (col, dark, hi) in enumerate(order):
            land = clicks[n_]
            if n_ > 0 and u < land - 0.7: continue
            f_ = ease((u - land + 0.7) / 0.7) if n_ > 0 else 1.0
            side = -1 if n_ % 2 == 0 else 1
            tx = cx + side * 300 * (1 - f_); ty = base - n_ * step - 240 * (1 - f_)
            drawn.append((ty, tx, col, dark, hi, n_ > 0 and abs(u - land) < 0.3))
        for ty, tx, col, dark, hi, flash in sorted(drawn):  # top first: lower bumps drawn inside upper hollows
            tooth_side(d, tx, ty, col, dark, hi, scale=1.0, hollow_hl=flash)
        if u > 0.9:  # callouts beside the stack, pointing at the first nested joint
            jy = base - step / 2 - 6
            label(d, "SALIENTE", 160, jy - 50, 44); arrow(d, 110, jy, cx - 168, jy, w=5)
            label(d, "HUECO", 920, jy - 50, 44); arrow(d, 970, jy, cx + 168, jy, w=5)
        if u > 1.0:
            pill(d, "¡TRABADOS!", cx, 380, 52)
    elif i == 6:  # wedge separates
        ys = 420 + 640 * ease(u / (L * 0.85))
        zipper_front(d, cx, 300, 1130, ys, cutaway=True, im=im, wedge_glow=math.sin(u * 8))
        d2 = ImageDraw.Draw(im)
        label(d2, "CUÑA", 150, ys - 40, 56); arrow(d2, 225, ys - 40, cx - 238, ys - 40)
        return d2
    elif i == 7:  # outro
        k = back_out(u / 0.5)
        ys = 1100 - 300 * ease(u / 1.0)
        zipper_front(d, cx, 700, 1150, ys, maxsep=120)
        d.text((cx * S, 470 * S), "CurioLab", font=font(110, FONT_X), fill=WHITE, anchor="mm")
        d.text((cx * S, 590 * S), "STUDIO 30", font=font(60, FONT_X), fill=AMB, anchor="mm")
        if u > 0.8:
            pill(d, "SÍGUEME", cx, 380, 46)
    return d

def scene_img(i, t):
    im = BG.copy(); d = ImageDraw.Draw(im)
    scene(i, t, im, d)
    a, b = seg_bounds(i)
    z = 1.0 + 0.035 * ease((t - a) / (b - a))
    cxs, cys = 540 * S, 760 * S
    w2, h2 = W * S / z / 2, H * S / z / 2
    return im.resize((W, H), Image.LANCZOS, box=(cxs - w2, cys - h2 * (760 / 960), cxs + w2, cys + h2 * (2 - 760 / 960)))

XF = 0.25
def render_frame(t):
    i = 0
    for j in range(len(segs)):
        if t >= seg_bounds(j)[0]: i = j
    frame = scene_img(i, t)
    a = seg_bounds(i)[0]
    if i > 0 and t - a < XF:
        frame = Image.blend(scene_img(i - 1, t), frame, ease((t - a) / XF))
    ov = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    header(od, t); captions(od, t)
    ov = ov.resize((W, H), Image.LANCZOS)
    return Image.alpha_composite(frame.convert("RGBA"), ov).convert("RGB")

if __name__ == "__main__":
    out = sys.argv[2]
    if len(sys.argv) > 3:  # preview stills
        for ts in sys.argv[3:]:
            render_frame(float(ts)).save(f"{out}_{ts}.png")
        sys.exit()
    nfr = int(TOTAL * FPS)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for n in range(nfr):
        ff.stdin.write(render_frame(n / FPS).tobytes())
    ff.stdin.close(); ff.wait()
    print("frames", nfr, "dur", round(TOTAL, 2))
