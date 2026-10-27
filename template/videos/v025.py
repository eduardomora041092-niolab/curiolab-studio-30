"""Video 025 — ¿Cómo se infla un airbag tan rápido?
Mechanism: in a crash, a sensor detects the sudden deceleration of the car and the control unit sends an electric
signal to the inflator (gas generator). There a chemical reaction (or a stored-gas cartridge) produces a large amount
of gas almost instantly. The gas fills the folded nylon bag, which bursts out of the steering-wheel cover and inflates
in a fraction of a second, so it cushions the occupant who keeps moving forward. The bag has vent holes: the gas
escapes through them and the bag deflates straight away, absorbing the movement and leaving room to move.
(No times in milliseconds, speeds or chemical names are claimed; the drawings are simplified and not to scale.)
"""
import math

ID = "025"
TITLE = "¿Cómo se infla un airbag tan rápido?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo se infla un airbag tan rápido?",
    "En un choque, un sensor detecta el frenazo brusco del coche.",
    "Al instante envía una señal eléctrica al generador de gas.",
    "Allí, una reacción química produce muchísimo gas de golpe.",
    "Ese gas llena la bolsa plegada, que sale del volante.",
    "La bolsa recibe tu cuerpo y lo frena con suavidad.",
    "Luego el gas escapa por unos orificios y la bolsa se desinfla.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"airbag", "infla", "rápido", "choque", "sensor", "detecta", "frenazo", "brusco", "señal", "eléctrica",
            "generador", "gas", "reacción", "química", "golpe", "bolsa", "plegada", "volante", "cuerpo", "frena",
            "suavidad", "escapa", "orificios", "desinfla", "funcionan"}

BAG, BAG_D = (236, 238, 242), (175, 182, 195)
WHEEL, WHEEL_D = (60, 66, 80), (35, 40, 52)
CAR, CAR_D = (43, 108, 176), (30, 78, 130)
GASC = (255, 210, 120)

def ell(cx, cy, a, b, ang=0.0, n=48):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + a * math.cos(t) * c - b * math.sin(t) * s, cy + a * math.cos(t) * s + b * math.sin(t) * c)
            for t in (2 * math.pi * k / n for k in range(n))]

def front_wheel(E, d, cx, cy, r):
    E.circle(d, cx, cy, r, outline=WHEEL, w=46)
    E.circle(d, cx, cy, r, outline=WHEEL_D, w=4)
    for a in (math.pi / 2, math.pi * 0.12 + math.pi, -math.pi * 0.12):
        E.line(d, [(cx, cy), (cx + (r - 20) * math.cos(a), cy + (r - 20) * math.sin(a))], WHEEL, 34)
    E.circle(d, cx, cy, 110, fill=WHEEL_D)

# side view: steering column from the dashboard (right) to the wheel; the driver is on the left
CX, CY = 700, 760
COL = (math.cos(math.radians(20)), math.sin(math.radians(20)))     # column direction (towards the dashboard)
PER = (COL[1], -COL[0])                                              # wheel plane direction

def side_wheel(E, d):
    E.line(d, [(CX, CY), (CX + 360 * COL[0], CY + 360 * COL[1])], WHEEL_D, 34)
    E.rrect(d, 980, 820, 1080, 1190, 0, (40, 46, 60))
    E.line(d, [(CX + 210 * PER[0], CY + 210 * PER[1]), (CX - 210 * PER[0], CY - 210 * PER[1])], WHEEL, 30)
    E.circle(d, CX, CY, 46, fill=WHEEL_D)

def side_bag(E, d, k, holes=False):
    """k: 0 folded .. 1 fully inflated; grows from the hub towards the driver (left)."""
    if k <= 0.02:
        return
    a = 40 + 230 * k; b = 50 + 200 * k
    ang = math.atan2(-COL[1], -COL[0])
    cx, cy = CX + a * math.cos(ang) * 0.92, CY + a * math.sin(ang) * 0.92
    E.poly(d, ell(cx, cy, a, b, ang), fill=BAG, outline=BAG_D, w=3)
    if holes and k > 0.2:
        for sgn in (-1, 1):
            hx, hy = cx + sgn * b * 0.82 * math.cos(ang + math.pi / 2), cy + sgn * b * 0.82 * math.sin(ang + math.pi / 2)
            E.circle(d, hx, hy, 16, fill=(40, 46, 60))
    return cx, cy, a, b, ang

def car(E, d, x, y):
    E.rrect(d, x - 190, y - 70, x + 190, y + 20, 26, CAR)
    E.poly(d, [(x - 110, y - 70), (x - 60, y - 150), (x + 70, y - 150), (x + 120, y - 70)], fill=CAR_D)
    E.poly(d, [(x - 90, y - 76), (x - 50, y - 136), (x + 0, y - 136), (x + 0, y - 76)], fill=(150, 200, 240))
    E.poly(d, [(x + 14, y - 76), (x + 14, y - 136), (x + 62, y - 136), (x + 100, y - 76)], fill=(150, 200, 240))
    for wx in (x - 110, x + 110):
        E.circle(d, wx, y + 20, 46, fill=(30, 30, 36)); E.circle(d, wx, y + 20, 18, fill=E.SIL_D)

def dummy(E, d, x, y, lean=0.0):
    """Generic seated figure (simple shapes), x,y = hip. lean>0 tilts the torso forward (to the right)."""
    a = math.radians(-8 + 32 * lean)
    sx, sy = x + 260 * math.sin(a), y - 260 * math.cos(a)
    E.line(d, [(x, y), (sx, sy)], (255, 150, 60), 70)
    E.circle(d, sx + 70 * math.sin(a), sy - 70 * math.cos(a), 62, fill=(255, 170, 80))
    E.line(d, [(x, y), (x + 230, y + 10), (x + 250, y + 200)], (255, 150, 60), 56)
    E.line(d, [(sx, sy + 30), (sx + 140, sy + 120)], (240, 135, 50), 40)

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: the bag is already bursting out of the steering wheel
        front_wheel(E, d, 540, 720, 300)
        k = E.ease(0.25 + u / (L * 0.55))
        r = 110 + 250 * k
        E.circle(d, 540, 720, r, fill=BAG, outline=BAG_D, w=4)
        for m in range(1, 4):
            E.circle(d, 540, 720, r * m / 4, outline=BAG_D, w=2)
        for k2 in range(8):
            a = k2 * math.pi / 4 + 0.3
            E.arrow(d, 540 + (r + 20) * math.cos(a), 720 + (r + 20) * math.sin(a), 540 + (r + 80) * math.cos(a),
                    720 + (r + 80) * math.sin(a), color=E.AMB, w=6, head=20)
    elif i == 1:  # crash: the sensor detects the sudden stop
        E.rrect(d, 880, 560, 960, 1000, 6, (120, 90, 70))
        for yy in range(580, 1000, 60):
            E.line(d, [(880, yy), (960, yy)], (90, 66, 50), 3)
        E.rrect(d, 60, 1000, 1020, 1030, 6, (70, 78, 96))
        t = min(1.0, u / (L * 0.45))
        x = 230 + 450 * (1 - (1 - t) ** 2)
        car(E, d, x, 930)
        E.rrect(d, x + 120, 870, x + 168, 900, 6, E.AMB if t >= 1 else E.SIL_D)
        if t < 1:
            for k in range(3):
                E.line(d, [(x - 230 - 40 * k, 860 + 25 * k), (x - 300 - 40 * k, 860 + 25 * k)], E.MUTED, 5)
        else:
            E.arrow(d, x + 144, 860, x + 144, 640, color=E.AMB, w=6, head=22)
            E.pill(d, "SENSOR", x + 40, 590, 40)
            E.label(d, "¡FRENAZO!", 380, 470, 64, color=E.HOT)
    elif i == 2:  # electric signal travels to the gas generator
        E.rrect(d, 120, 520, 330, 680, 20, (40, 46, 60), outline=E.AMB, w=4)
        E.label(d, "SENSOR", 225, 600, 38, color=E.AMB)
        E.rrect(d, 700, 800, 960, 980, 30, E.SIL_D, outline=E.SIL_H, w=4)
        E.label(d, "GENERADOR", 830, 1040, 40, color=E.WHITE)
        E.label(d, "DE GAS", 830, 1090, 40, color=E.WHITE)
        pts = [(330, 600), (520, 600), (520, 890), (700, 890)]
        E.line(d, pts, E.MUTED, 8)
        f = (u * 1.4) % 1
        seg = [(330, 600, 520, 600), (520, 600, 520, 890), (520, 890, 700, 890)]
        lens = [190, 290, 180]; tot = sum(lens); s = f * tot
        for (x0, y0, x1, y1), ln in zip(seg, lens):
            if s <= ln:
                px, py = E.lerp(x0, x1, s / ln), E.lerp(y0, y1, s / ln)
                break
            s -= ln
        E.circle(d, px, py, 26, fill=(255, 235, 120))
        E.poly(d, [(px - 8, py - 22), (px + 10, py - 2), (px - 2, py + 2), (px + 8, py + 22), (px - 12, py), (px, py - 4)], fill=E.BG1)
        E.pill(d, "SEÑAL ELÉCTRICA", 540, 420, 40)
    elif i == 3:  # chemical reaction makes a lot of gas at once
        E.rrect(d, 360, 640, 720, 900, 40, E.SIL_D, outline=E.SIL_H, w=4)
        E.rrect(d, 400, 680, 680, 860, 24, (70, 50, 40))
        g = E.ease(u / (L * 0.6))
        for k in range(26):
            a = k * 2 * math.pi / 26 + 0.2
            rr = 60 + 360 * ((g * 0.8 + (k % 5) * 0.11 + u * 0.4) % 1) * g
            E.circle(d, 540 + rr * math.cos(a), 770 + 0.8 * rr * math.sin(a), 16 + 6 * (k % 3), fill=GASC)
        E.circle(d, 540, 770, 40 + 30 * g, fill=(255, 140, 50))
        E.pill(d, "REACCIÓN QUÍMICA", 540, 420, 40)
        E.label(d, "GAS", 540, 1110, 60, color=E.AMB)
    elif i == 4:  # gas fills the folded bag, which comes out of the wheel
        side_wheel(E, d)
        k = E.ease(u / (L * 0.7))
        side_bag(E, d, k)
        for m in range(3):
            f = (u * 1.5 + m / 3) % 1
            E.arrow(d, CX - 30 * COL[0] - 160 * f * COL[0], CY - 30 * COL[1] - 160 * f * COL[1] + (m - 1) * 40,
                    CX - 80 * COL[0] - 160 * f * COL[0], CY - 80 * COL[1] - 160 * f * COL[1] + (m - 1) * 40, color=E.HOT, w=9, head=26)
        E.label(d, "VOLANTE", 900, 470, 44, color=E.WHITE)
        E.pill(d, "BOLSA", 260, 1110, 44)
    elif i == 5:  # the bag receives the body and slows it down gently
        side_wheel(E, d)
        t = E.ease(u / (L * 0.8))
        c = side_bag(E, d, 1.0 - 0.15 * t)
        dummy(E, d, 170, 1000, lean=0.2 + 0.6 * t)
        E.label(d, "FRENA SUAVE", 540, 1140, 48, color=E.AMB)
    elif i == 6:  # gas escapes through vent holes: the bag deflates
        side_wheel(E, d)
        k = 1.0 - 0.6 * E.ease(u / (L * 0.85))
        c = side_bag(E, d, k, holes=True)
        if c:
            cx, cy, a, b, ang = c
            for sgn in (-1, 1):
                nx, ny = math.cos(ang + math.pi / 2) * sgn, math.sin(ang + math.pi / 2) * sgn
                hx, hy = cx + b * 0.82 * nx, cy + b * 0.82 * ny
                for m in range(2):
                    f = (u * 1.6 + m / 2) % 1
                    E.arrow(d, hx + nx * (30 + 90 * f), hy + ny * (30 + 90 * f), hx + nx * (80 + 90 * f), hy + ny * (80 + 90 * f),
                            color=GASC, w=6, head=18)
        E.pill(d, "ORIFICIOS", 300, 420, 42)
        E.label(d, "SE DESINFLA", 540, 1120, 50, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("pop", s[0] + 0.05), ("whoosh", s[0] + 0.1, 0.9), ("click", s[1] + 1.2), ("click", s[2] + 0.4),
            ("whoosh", s[3] + 0.3, 1.0), ("whoosh", s[4] + 0.2, 1.4), ("pop", s[5] + 0.6), ("whoosh", s[6] + 0.3, 1.5)]
