"""Video 039 — ¿Qué son las auroras boreales?
Science: the Sun continuously releases a stream of electrically charged particles (mainly electrons and protons),
the solar wind. Earth's magnetic field deflects most of them around the planet. Near the magnetic poles the field
lines guide some charged particles down into the upper atmosphere. There they collide with gas atoms and molecules,
mainly oxygen and nitrogen, transferring energy and leaving them in an excited state. When those atoms and molecules
return to their normal state they release the energy as light. Oxygen gives mostly green (and sometimes red) light;
nitrogen gives blue and purple tones. In the north they are called aurora borealis and in the south aurora australis.
(No altitudes, speeds, energies or wavelengths are claimed.)
"""
import math, random

ID = "039"
TITLE = "¿Qué son las auroras boreales?"
SUBTITLE = "CURIOSIDADES DE LA CIENCIA"
LINES = [
    "¿Qué son las auroras boreales?",
    "El Sol lanza sin parar partículas con carga eléctrica: el viento solar.",
    "El campo magnético de la Tierra desvía casi todas.",
    "Pero cerca de los polos, algunas se cuelan hacia la atmósfera.",
    "Allí chocan con gases como el oxígeno y el nitrógeno.",
    "Los choques excitan esos gases, que liberan la energía como luz.",
    "El oxígeno brilla sobre todo en verde; el nitrógeno, en azul o violeta.",
    "Sígueme para más curiosidades de la ciencia.",
]
KEYWORDS = {"auroras", "boreales", "sol", "partículas", "carga", "eléctrica", "viento", "solar", "campo",
            "magnético", "tierra", "desvía", "polos", "atmósfera", "chocan", "gases", "oxígeno", "nitrógeno",
            "choques", "excitan", "energía", "luz", "verde", "azul", "violeta"}

GREEN, VIOLET = (90, 255, 150), (170, 110, 255)
SUN = (255, 200, 60)
EARTH, LAND = (40, 110, 200), (60, 160, 90)
rnd = random.Random(39)
STARS = [(rnd.random() * 1080, 260 + rnd.random() * 500, rnd.random()) for _ in range(60)]

def aurora(E, d, u, y=520, col=GREEN, amp=60, alpha=1.0, x0=60, x1=1020):
    n = 70
    for k in range(n):
        x = x0 + (x1 - x0) * k / (n - 1)
        top = y + amp * math.sin(u * 1.6 + k * 0.16) - 40 * math.sin(k * 0.32)
        h = 260 + 60 * math.sin(u * 2.1 + k * 0.25)
        for j in range(12):
            f = j / 12
            E.line(d, [(x, top + h * f), (x, top + h * (f + 1 / 12))], E.mix(E.BG1, col, alpha * (1 - f) * 0.9), 15)

def night(E, d, u):
    for x, y, b in STARS:
        E.circle(d, x, y, 2 + 2 * b, fill=E.mix(E.BG1, E.WHITE, 0.5 + 0.5 * b))

def mountains(E, d):
    E.poly(d, [(0, 1190), (0, 960), (220, 820), (380, 930), (560, 780), (760, 950), (900, 860), (1080, 960), (1080, 1190)],
           fill=(14, 22, 34))

def earth(E, d, cx, cy, r=170):
    E.circle(d, cx, cy, r, fill=EARTH)
    E.poly(d, [(cx - 80, cy - 60), (cx - 10, cy - 100), (cx + 40, cy - 40), (cx - 20, cy + 10)], fill=LAND)
    E.poly(d, [(cx + 30, cy + 40), (cx + 110, cy + 20), (cx + 90, cy + 110)], fill=LAND)

def field(E, d, cx, cy, r=170):
    for s in (1.6, 2.2, 2.9):
        for side in (-1, 1):
            pts = []
            for j in range(41):
                th = 0.25 + (math.pi - 0.5) * j / 40
                rr = r * s * math.sin(th) ** 2
                pts.append((cx + side * rr * math.sin(th), cy - rr * math.cos(th)))
            E.line(d, pts, E.mix(E.BG2, E.COLD, 0.7), 4)

def wind(E, d, u, x0, x1, ys, deflect=None):
    for k, y in enumerate(ys):
        f = (u * 0.5 + k * 0.137) % 1
        x = x0 + (x1 - x0) * f
        yy = y
        if deflect is not None:
            cx, cy, R = deflect
            if x > cx - R - 60:
                yy = y + (1 if y > cy else -1) * min(260, (x - (cx - R - 60)) * 1.1)
        E.circle(d, x, yy, 10, fill=SUN)

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: auroras already waving in the night sky
        night(E, d, u)
        aurora(E, d, u + 2, y=600, col=VIOLET, amp=40, alpha=0.45, x0=200, x1=900)
        aurora(E, d, u, y=400)
        mountains(E, d)
        E.pill(d, "AURORA BOREAL", 540, 1080, 42)
    elif i == 1:  # the Sun releases charged particles: solar wind
        E.circle(d, 120, 690, 220, fill=SUN)
        wind(E, d, u, 340, 1020, [440 + 40 * k for k in range(13)])
        E.label(d, "VIENTO SOLAR", 680, 340, 50, color=SUN)
        E.label(d, "SOL", 140, 1040, 46, color=SUN)
    elif i == 2:  # Earth's magnetic field deflects most of them
        cx, cy = 720, 700
        field(E, d, cx, cy)
        earth(E, d, cx, cy)
        wind(E, d, u, 40, 1040, [480 + 30 * k for k in range(15)], deflect=(cx, cy, 420))
        E.label(d, "CAMPO MAGNÉTICO", 540, 330, 44, color=E.COLD)
        E.label(d, "TIERRA", cx, 1080, 44, color=E.WHITE)
    elif i == 3:  # near the poles some get in
        cx, cy = 540, 720
        field(E, d, cx, cy)
        earth(E, d, cx, cy)
        for k in range(4):
            f = (u * 0.5 + k / 4) % 1
            side = -1 if k % 2 else 1
            th = 0.25 + (1 - f) * 0.9
            rr = 170 * 1.6 * math.sin(th) ** 2
            E.circle(d, cx + side * rr * math.sin(th), cy - rr * math.cos(th), 12, fill=SUN)
        E.circle(d, cx, cy - 170, 30, outline=GREEN, w=6)
        E.pill(d, "CERCA DE LOS POLOS", 540, 330, 40)
    elif i == 4:  # collisions with oxygen and nitrogen
        E.rrect(d, 120, 420, 960, 1000, 30, E.BG2)
        g = random.Random(4)
        for j in range(10):
            x, y = 220 + g.random() * 640, 520 + g.random() * 400
            col = GREEN if j % 2 == 0 else VIOLET
            E.circle(d, x, y, 22, fill=col)
        f = (u * 0.6) % 1
        for k in range(3):
            E.circle(d, 200 + 600 * f + 40 * k, 470 + 120 * k + 200 * f, 11, fill=SUN)
        E.label(d, "OXÍGENO", 330, 1060, 44, color=GREEN)
        E.label(d, "NITRÓGENO", 760, 1060, 44, color=VIOLET)
        E.pill(d, "CHOQUES", 540, 340, 42)
    elif i == 5:  # excited gas releases light
        k = E.ease(min(1, u / (L * 0.5)))
        x, y = 540, 700
        E.circle(d, x, y, 60, fill=E.mix(E.SIL_D, GREEN, k))
        E.circle(d, x - 260 + 200 * min(1, u / (L * 0.4)), y, 14, fill=SUN)
        if k > 0.9:
            for ang in (-1.2, -0.4, 0.4, 1.2, 2.0, 2.8):
                E.wave(d, x + 80 * math.cos(ang), y + 80 * math.sin(ang), x + 260 * math.cos(ang), y + 260 * math.sin(ang),
                       34, 9, GREEN, 5)
            E.pill(d, "LUZ", 540, 1040, 46, bg=GREEN)
        else:
            E.label(d, "ENERGÍA", 540, 1040, 46, color=E.AMB)
    elif i == 6:  # oxygen green, nitrogen blue/violet
        night(E, d, u)
        aurora(E, d, u, y=380, alpha=1.0, x0=60, x1=520)
        aurora(E, d, u + 1, y=380, col=VIOLET, alpha=1.0, x0=560, x1=1020)
        mountains(E, d)
        E.label(d, "OXÍGENO", 290, 1080, 44, color=GREEN)
        E.label(d, "NITRÓGENO", 790, 1080, 44, color=VIOLET)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.05, 1.0), ("zip", s[1] + 0.4, 1.0), ("whoosh", s[2] + 0.6, 0.8), ("click", s[3] + 0.8),
            ("pop", s[4] + 0.6), ("pop", s[5] + 1.0), ("whoosh", s[6] + 0.3, 1.2)]
