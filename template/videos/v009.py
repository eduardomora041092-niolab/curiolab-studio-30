"""Video 009 — ¿Cómo se forma un arcoíris?
Science: sunlight looks white but is a mixture of colours. When light enters a (nearly spherical) raindrop
it is refracted, and each colour is refracted by a slightly different amount (dispersion), so the drop acts
like a small prism. In the primary bow the light reflects once off the back of the drop and is refracted
again on leaving, with the colours spread out. The Sun must be behind the observer. Each drop sends mainly
one colour to a given eye, depending on its angle; all drops at the same angle from the antisolar point
form an arc, red on the outside (top) and violet on the inside.
(Ray paths in the drop are computed with Snell's law; dispersion is exaggerated so the colours are visible.
Exact angles, ≈42° red / ≈40° violet, are not narrated.)
"""
import math

ID = "009"
TITLE = "¿Cómo se forma un arcoíris?"
SUBTITLE = "CURIOSIDADES DE LA CIENCIA"
LINES = [
    "Cada gota de lluvia funciona como un pequeño prisma.",
    "La luz del Sol parece blanca, pero mezcla todos los colores.",
    "Al entrar en la gota, la luz se dobla, y cada color, un poco distinto.",
    "Se refleja en el fondo y sale con los colores separados.",
    "Por eso, el Sol tiene que estar a tu espalda.",
    "Cada gota te envía un solo color según su posición.",
    "Las gotas al mismo ángulo forman un arco, con el rojo arriba.",
    "Sígueme para más curiosidades de la ciencia.",
]
KEYWORDS = {"gota", "lluvia", "prisma", "luz", "sol", "blanca", "colores", "dobla", "color", "refleja", "fondo", "separados",
            "espalda", "posición", "ángulo", "arco", "rojo", "arriba", "ciencia"}

SPEC = [(230, 50, 50), (250, 140, 40), (250, 225, 60), (70, 200, 90), (60, 150, 240), (80, 80, 210), (150, 80, 220)]
N_IDX = [1.330 + 0.010 * k for k in range(7)]   # exaggerated dispersion (real: 1.331 red .. 1.343 violet)
DROP = (150, 200, 245)
SUN = (255, 220, 120)
GROUND = (50, 110, 70)

def _refract(dx, dy, nx, ny, eta):
    cosi = -(nx * dx + ny * dy); k = 1 - eta * eta * (1 - cosi * cosi)
    c = eta * cosi - math.sqrt(max(0.0, k))
    tx, ty = eta * dx + c * nx, eta * dy + c * ny; m = math.hypot(tx, ty)
    return tx / m, ty / m

def _next_hit(px, py, dx, dy, cx, cy):
    t = -2 * ((px - cx) * dx + (py - cy) * dy)
    return px + t * dx, py + t * dy

def trace(cx, cy, R, n, b=0.86):
    """Primary-bow ray: horizontal ray (+x) entering the upper half of the drop. Returns P1, P2, P3, exit dir."""
    px, py = cx - R * math.sqrt(1 - b * b), cy - R * b
    nx, ny = (px - cx) / R, (py - cy) / R
    dx, dy = _refract(1.0, 0.0, nx, ny, 1 / n)
    qx, qy = _next_hit(px, py, dx, dy, cx, cy)
    nx, ny = (qx - cx) / R, (qy - cy) / R
    dot = dx * nx + dy * ny; rx, ry = dx - 2 * dot * nx, dy - 2 * dot * ny
    sx, sy = _next_hit(qx, qy, rx, ry, cx, cy)
    nx, ny = (sx - cx) / R, (sy - cy) / R
    ex, ey = _refract(rx, ry, -nx, -ny, n)   # leaving: normal pointing into the drop's inside for the formula
    return (px, py), (qx, qy), (sx, sy), (ex, ey)

def big_drop(E, d, cx, cy, R):
    E.circle(d, cx, cy, R, fill=(40, 60, 92), outline=DROP, w=6)
    E.circle(d, cx - R * 0.45, cy - R * 0.45, R * 0.12, fill=(90, 120, 160))

def drop_rays(E, d, cx, cy, R, stage, out_len=330):
    p1 = trace(cx, cy, R, N_IDX[0])[0]
    E.line(d, [(60, p1[1]), p1], E.WHITE, 10)
    for k, col in reversed(list(enumerate(SPEC))):
        a, b_, c, e = trace(cx, cy, R, N_IDX[k])
        q = E.lerp(0, 1, min(1, stage))
        E.line(d, [a, (E.lerp(a[0], b_[0], q), E.lerp(a[1], b_[1], q))], col, 4)
        if stage > 1:
            q = min(1, stage - 1)
            E.line(d, [b_, (E.lerp(b_[0], c[0], q), E.lerp(b_[1], c[1], q))], col, 4)
        if stage > 2:
            q = min(1, stage - 2)
            E.line(d, [c, (c[0] + e[0] * out_len * q, c[1] + e[1] * out_len * q)], col, 6)

def prism(E, d, x, y, s):
    E.poly(d, [(x, y - s), (x + s * 0.9, y + s * 0.6), (x - s * 0.9, y + s * 0.6)], fill=(60, 80, 115), outline=E.SIL_H, w=4)

def eye(E, d, x, y, r=34):
    E.poly(d, [(x - r * 1.6, y), (x, y - r), (x + r * 1.6, y), (x, y + r)], fill=E.WHITE)
    E.circle(d, x, y, r * 0.55, fill=(40, 60, 92))

def scene(i, u, L, E, im, d):
    cx = 540
    if i == 0:  # a raindrop is a tiny prism
        prism(E, d, 280, 700, 170)
        E.line(d, [(60, 700), (230, 700)], E.WHITE, 8)
        for k, col in enumerate(SPEC):
            E.line(d, [(330, 700), (470, 780 + k * 14)], col, 5)
        E.label(d, "=", 540, 700, 110, color=E.WHITE)
        k = E.back_out((u - 0.4) / 0.5)
        if k > 0.05:
            E.circle(d, 800, 700, 150 * k, fill=(40, 60, 92), outline=DROP, w=6)
        for j in range(14):
            x = 100 + (j * 71) % 880; y = 330 + ((u * 260 + j * 53) % 220)
            E.circle(d, x, y, 9, fill=DROP)
        if u > 0.9: E.label(d, "PRISMA", 280, 960, 46); E.label(d, "GOTA", 800, 960, 46)
    elif i == 1:  # white light = mixture of colours
        E.circle(d, 150, 420, 80, fill=SUN)
        E.line(d, [(210, 470), (420, 690)], E.WHITE, 12)
        prism(E, d, 480, 720, 150)
        p = E.ease((u - 0.3) / 0.8)
        for k, col in enumerate(SPEC):
            ex, ey = 980, 720 + (k - 3) * 55
            E.line(d, [(540, 730), (E.lerp(540, ex, p), E.lerp(730, ey, p))], col, 10)
        E.label(d, "LUZ BLANCA", 260, 620, 40, color=E.WHITE)
        if u > 1.0: E.label(d, "TODOS LOS COLORES", 760, 1010, 42)
    elif i == 2:  # refraction, each colour a little different
        big_drop(E, d, cx, 720, 300)
        drop_rays(E, d, cx, 720, 300, E.ease(u / (L * 0.7)))
        if u > 0.6: E.label(d, "SE DOBLA", 300, 340, 50)
    elif i == 3:  # reflection at the back, exits separated
        big_drop(E, d, cx, 720, 300)
        drop_rays(E, d, cx, 720, 300, 1 + 2 * E.ease(u / (L * 0.8)), out_len=360)
        if u > 0.5: E.label(d, "SE REFLEJA", 880, 360, 46)
        if u > 1.2: E.label(d, "COLORES SEPARADOS", cx, 1130, 42)
    elif i == 4:  # Sun behind you
        E.rrect(d, 60, 1000, 1020, 1180, 0, GROUND)
        E.circle(d, 140, 380, 70, fill=SUN)
        for k in range(4):
            y0 = 360 + k * 70
            E.arrow(d, 230, y0, 430, y0 + 90, color=SUN, w=5, head=18)
        # observer facing the rain (to the right)
        E.circle(d, 330, 820, 34, fill=E.SIL)
        E.line(d, [(330, 855), (330, 950)], E.SIL, 14)
        E.line(d, [(330, 950), (300, 1000)], E.SIL, 12); E.line(d, [(330, 950), (360, 1000)], E.SIL, 12)
        E.arrow(d, 370, 820, 470, 820, color=E.WHITE, w=5, head=18)
        for j in range(16):
            x = 600 + (j * 37) % 400; y = 360 + ((u * 300 + j * 61) % 600)
            E.line(d, [(x, y), (x - 6, y + 26)], DROP, 4)
        for k, col in enumerate(SPEC):
            r = 220 - k * 12
            d.arc(E.P(800 - r, 1000 - r, 800 + r, 1000 + r), 180, 360, fill=col, width=12 * E.S)
        E.rrect(d, 60, 1000, 1020, 1180, 0, GROUND)
        if u > 0.6: E.pill(d, "SOL A TU ESPALDA", cx, 300, 40)
    elif i == 5:  # each drop sends one colour, depending on its position
        ex_, ey_ = 180, 1050
        el = math.radians(15)                  # sunlight travels down-right at 15°
        for k in range(4):
            x0, y0 = 120 + k * 230, 330
            E.arrow(d, x0, y0, x0 + 150 * math.cos(el), y0 + 150 * math.sin(el), color=SUN, w=4, head=16)
        for ang, col, name in ((42, SPEC[0], "ROJO"), (34, SPEC[6], "VIOLETA")):   # violet angle exaggerated for clarity
            a = math.radians(ang) - el
            dx_, dy_ = ex_ + 800 * math.cos(a), ey_ - 800 * math.sin(a)
            p = E.ease((u - (0.2 if name == "ROJO" else 0.8)) / 0.6)
            E.circle(d, dx_, dy_, 34, fill=(40, 60, 92), outline=DROP, w=4)
            if p > 0:
                E.line(d, [(dx_, dy_), (E.lerp(dx_, ex_, p), E.lerp(dy_, ey_, p))], col, 8)
                E.label(d, name, dx_ + 20, dy_ - 70, 40, color=col)
        eye(E, d, ex_, ey_)
    elif i == 6:  # same angle -> an arc, red on top
        E.rrect(d, 60, 1000, 1020, 1180, 0, GROUND)
        ax, ay = cx, 1110
        p = E.ease(u / (L * 0.6))
        for k, col in enumerate(SPEC):
            r = 520 - k * 14
            d.arc(E.P(ax - r, ay - r, ax + r, ay + r), 180 + 90 * (1 - p), 360 - 90 * (1 - p), fill=col, width=14 * E.S)
        E.rrect(d, 60, 1000, 1020, 1180, 0, GROUND)
        eye(E, d, ax, 1080, 28)
        if u > 0.8:
            for a in (200, 270, 340):
                t = math.radians(a)
                E.line(d, [(ax, 1080), (ax + 480 * math.cos(t), ay + 480 * math.sin(t))], E.MUTED, 3)
            E.label(d, "MISMO ÁNGULO", cx, 820, 46, color=E.WHITE)
            E.label(d, "ROJO", 870, 520, 44, color=SPEC[0])
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("pop", s[0] + 0.5), ("whoosh", s[1] + 0.3, 0.8), ("whoosh", s[3], 0.6), ("pop", s[5] + 0.3), ("pop", s[5] + 0.9), ("whoosh", s[6], 0.8)]
