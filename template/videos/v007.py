"""Video 007 — ¿Cómo funciona el clic de un bolígrafo? (bolígrafo retráctil)
Mechanism: the push button drives a rotating cam (leva) that rests on top of the ink cartridge.
A spring near the tip always pushes the cartridge and cam back up toward the button. The cam has
angled teeth/lugs and the inside of the barrel has ribs that form alternating short stops and long
channels. Each press pushes the lugs past the ribs; the angled faces make the cam rotate one step,
and when released the spring pushes it up onto the next position. On a short stop the cartridge is
held low and the tip stays out; on the next click the lugs drop into a long channel, the spring lifts
everything, and the tip retracts. Drawn here as an "unrolled" view of the cam and barrel.
"""
from PIL import Image, ImageDraw

ID = "007"
TITLE = "¿Cómo funciona el clic de un bolígrafo?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "Un clic sale, otro clic entra. ¿Qué hay dentro?",
    "El botón empuja una pieza giratoria, la leva, y el cartucho de tinta.",
    "Abajo, un muelle empuja el cartucho siempre hacia arriba.",
    "La leva tiene dientes inclinados, y el tubo tiene topes y ranuras por dentro.",
    "Cada clic hace que los dientes resbalen y la leva gire un paso.",
    "Si cae sobre un tope, la leva se queda baja y la punta, fuera.",
    "Al siguiente clic, cae en una ranura larga, sube, y la punta se esconde.",
    "Sígueme para ver cómo funcionan las cosas por dentro.",
]
KEYWORDS = {"clic", "botón", "leva", "giratoria", "cartucho", "muelle", "arriba", "dientes", "inclinados",
            "topes", "ranuras", "ranura", "resbalen", "gire", "paso", "tope", "punta", "esconde", "dentro"}

INK = (40, 90, 200)
CX = 540

# ---------------- side cut-away of the pen ----------------
def pen_cut(E, d, ext, hl_spring=False, hl=None):
    """ext: 0 = tip retracted, 1 = tip out, >1 = pressed further."""
    ct = 430 + 70 * ext                      # cartridge top
    E.rrect(d, CX - 80, 330, CX + 80, 990, 18, E.CAV, outline=E.SIL, w=4)
    E.poly(d, [(CX - 80, 985), (CX + 80, 985), (CX + 24, 1072), (CX - 24, 1072)], fill=E.CAV, outline=E.SIL, w=4)
    # barrel ribs near the cam + shoulder for the spring
    for sx in (-1, 1):
        E.rrect(d, CX + sx * 72 - 6, 360, CX + sx * 72 + 6, 470, 3, E.SIL_D)
    E.line(d, [(CX - 76, 988), (CX - 36, 988)], E.SIL_D, 8); E.line(d, [(CX + 36, 988), (CX + 76, 988)], E.SIL_D, 8)
    # cartridge + metal tip
    E.rrect(d, CX - 20, ct, CX + 20, ct + 560, 8, INK, outline=(25, 60, 140), w=2)
    E.poly(d, [(CX - 20, ct + 558), (CX + 20, ct + 558), (CX + 7, ct + 620), (CX - 7, ct + 620)], fill=E.SIL, outline=E.SIL_D, w=2)
    # collar + spring
    E.rrect(d, CX - 36, ct + 425, CX + 36, ct + 440, 4, E.SIL_D)
    y0, y1 = ct + 440, 986; n = 7
    pts = [(CX + (42 if k % 2 else -42), y0 + (y1 - y0) * k / n) for k in range(n + 1)]
    E.line(d, pts, E.AMB if hl_spring else E.SIL, 6)
    # cam with angled teeth
    cam_c = E.AMB if hl == "cam" else E.BRA
    E.rrect(d, CX - 60, ct - 80, CX + 60, ct - 12, 6, cam_c, outline=E.BRA_D, w=3)
    for k in range(4):
        x = CX - 60 + 30 * k
        E.poly(d, [(x, ct - 12), (x + 30, ct - 12), (x + 30, ct)], fill=cam_c, outline=E.BRA_D, w=2)
    # push button
    E.rrect(d, CX - 38, ct - 160, CX + 38, ct - 80, 14, E.AMB if hl == "btn" else E.SIL, outline=E.SIL_D, w=3)
    return ct

# ---------------- "unrolled" view of cam lugs vs. barrel ribs ----------------
TOPBAR = 420
PITCH = 120
X_L, X_R = 80, 1000
BLOCK_L, BLOCK_R = 700, 740            # slanted bottom edge of a stop (left, right)
Y_CHANNEL, Y_STOP, Y_PRESS = 440, 712, 800

def centre(k):
    return 200 + PITCH * k

def barrel(E, d, hl=False):
    E.rrect(d, X_L, TOPBAR - 22, X_R, TOPBAR, 6, E.SIL_D)
    for k in range(0, 7, 2):           # even positions: short stops; odd positions: open channels
        x0 = centre(k) - PITCH / 2; x1 = x0 + PITCH
        E.poly(d, [(x0, TOPBAR), (x1, TOPBAR), (x1, BLOCK_R), (x0, BLOCK_L)], fill=(70, 84, 112), outline=E.SIL_D, w=3)
        if hl: E.line(d, [(x0, BLOCK_L), (x1, BLOCK_R)], E.AMB, 8)

def cam(E, im, ty, pos, hl=False):
    """Lugs at positions pos, pos+2, pos+4 ... (pos may be fractional while rotating); clipped to the barrel width."""
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(layer)
    for m in range(-2, 6):
        x = centre(pos + 2 * m)
        E.poly(dl, [(x - 35, ty), (x + 35, ty + 40), (x + 35, ty + 330), (x - 35, ty + 330)], fill=E.BRA, outline=E.BRA_D, w=3)
        if hl: E.line(dl, [(x - 35, ty), (x + 35, ty + 40)], E.AMB, 8)
    E.rrect(dl, X_L, ty + 325, X_R, ty + 375, 10, E.BRA, outline=E.BRA_D, w=3)
    box = (X_L * E.S, 0, X_R * E.S, im.size[1]); crop = layer.crop(box)
    im.paste(crop, box[:2], crop)

def click_motion(E, u, L, y_from, y_to, k_from):
    """press down, rotate one step at the bottom, rise to the new resting height."""
    a = E.ease((u - 0.2) / (L * 0.25)); b = E.ease((u - 0.2 - L * 0.25) / (L * 0.2)); c = E.ease((u - 0.2 - L * 0.45) / (L * 0.3))
    ty = y_from + (Y_PRESS - y_from) * a
    ty = ty + (y_to - Y_PRESS) * c
    return ty, k_from + b, (a, b, c)

def scene(i, u, L, E, im, d):
    if i == 0:  # click out, click in
        ph = (u % 1.8) / 1.8
        ext = E.ease((ph - 0.05) / 0.12) if ph < 0.5 else 1 - E.ease((ph - 0.55) / 0.12)
        press = 0.3 * (max(0, 1 - abs(ph - 0.1) / 0.08) + max(0, 1 - abs(ph - 0.6) / 0.08))
        pen_cut(E, d, ext + press)
        if press > 0.05: E.pill(d, "CLIC", 800, 330, 48)
        E.label(d, "?", 800, 720, 120)
    elif i == 1:  # button pushes cam + cartridge
        press = E.ease((u - 0.8) / 0.4) - E.ease((u - 1.6) / 0.4) * 0.25
        ct = pen_cut(E, d, 1.25 * press, hl="btn" if u < 1.6 else "cam")
        E.label(d, "BOTÓN", 250, ct - 120, 46); E.arrow(d, 330, ct - 120, CX - 46, ct - 120, w=5)
        if u > 1.4: E.label(d, "LEVA", 250, ct - 30, 46); E.arrow(d, 320, ct - 40, CX - 66, ct - 46, w=5)
        if u > 2.2: E.label(d, "CARTUCHO", 830, 760, 46); E.arrow(d, 830, 790, CX + 28, 820, w=5)
        if press > 0.05: E.arrow(d, 760, ct - 200, 760, ct - 90, color=E.WHITE, w=7)
    elif i == 2:  # spring pushes the cartridge up
        ext = 1.0 - 0.35 * E.ease((u - 0.6) / 0.8)
        pen_cut(E, d, ext, hl_spring=True)
        E.label(d, "MUELLE", 850, 930, 48); E.arrow(d, 760, 930, CX + 52, 935, w=5)
        E.arrow(d, 690, 900, 690, 700, color=E.AMB, w=9, head=32)
    elif i == 3:  # unrolled view: angled teeth, stops and channels
        barrel(E, d, hl=u > 0.4)
        cam(E, im, Y_STOP, 0, hl=u > 0.4)
        E.label(d, "TUBO: TOPES Y RANURAS", 540, 330, 46, color=E.WHITE)
        if u > 0.4: E.pill(d, "LEVA: DIENTES INCLINADOS", 540, 1138, 36)
    elif i == 4:  # one click = one step of rotation
        ty, k, (a, b, c) = click_motion(E, u, L, Y_CHANNEL, Y_STOP, -1)
        barrel(E, d); cam(E, im, ty, k)
        E.label(d, "GIRA UN PASO", 540, 310, 48)
        if b > 0.02: E.arrow(d, 400, 365, 400 + 280 * b, 365, color=E.AMB, w=8)
        if a > 0.05 and c < 0.95: E.arrow(d, 960, 300 + 0 * a, 960, 380, color=E.WHITE, w=7)
    elif i == 5:  # resting on a stop: tip out
        barrel(E, d); cam(E, im, Y_STOP, 0)
        for k in (0, 2, 4, 6):
            if u > 0.5: E.circle(d, centre(k), BLOCK_L + 20, 12, fill=E.HOT)
        if u > 0.8: E.pill(d, "PUNTA FUERA", 540, 320, 44)
    elif i == 6:  # next click: into a long channel, tip hides
        ty, k, (a, b, c) = click_motion(E, u, L, Y_STOP, Y_CHANNEL, 0)
        barrel(E, d); cam(E, im, ty, k)
        if c > 0.6: E.pill(d, "PUNTA DENTRO", 540, 320, 44, bg=(80, 200, 120))
        elif a > 0.05: E.pill(d, "CLIC", 540, 320, 44)
    else:
        E.outro(d, u)

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("click", 0.3), ("click", 1.2), ("click", s[1] + 0.8), ("whoosh", s[3], 0.5),
            ("click", s[4] + 0.2 + 0.3), ("click", s[6] + 0.2 + 0.3 * (s[7] - s[6])), ("pop", s[7] + 0.3)]
