"""Video 018 — ¿Qué causa las mareas?
Science: tides are the regular rise and fall of sea level, seen at the coast as high and low tide. They are caused
mainly by the Moon's gravity (the Sun also contributes, less). The Moon pulls more strongly on the ocean on the side
of the Earth nearest to it than on the Earth's centre, so water bulges towards the Moon. On the opposite side the
Moon pulls the water less than it pulls the Earth's centre, and a second bulge forms there. As the Earth rotates,
a given coast passes through the bulges (high tide) and the regions between them (low tide); many places get two
high tides a day.
(No exact periods, heights or the Sun's share are claimed.)
"""
import math

ID = "018"
TITLE = "¿Qué causa las mareas?"
SUBTITLE = "CURIOSIDADES DE LA CIENCIA"
LINES = [
    "Tu toalla, lejos de la orilla, acaba mojada.",
    "Es la marea: el nivel del mar sube y baja cada día.",
    "La causa principal es la gravedad de la Luna.",
    "La Luna atrae con más fuerza el agua del lado que tiene más cerca.",
    "Allí el océano se abulta hacia ella.",
    "En el lado opuesto la atrae menos, y se forma otro abultamiento.",
    "La Tierra gira bajo ellos, y tu playa pasa por marea alta y marea baja.",
    "Sígueme para más curiosidades de la ciencia.",
]
KEYWORDS = {"toalla", "orilla", "mojada", "marea", "mar", "sube", "baja", "gravedad", "luna", "atrae", "fuerza",
            "cerca", "océano", "abulta", "opuesto", "abultamiento", "tierra", "gira", "playa", "alta", "ciencia"}

SAND, SAND_D = (225, 190, 120), (180, 145, 85)
SEA, SEA_D = (40, 110, 190), (28, 80, 150)
LAND = (70, 160, 90)
EX, EY, ER = 420, 720, 190      # Earth
MX, MY, MR = 930, 720, 55       # Moon

def beach(E, d, level, towel=True):
    """Top view. level 0..1: how far the water line has advanced over the sand (1 = under the towel)."""
    E.rrect(d, 80, 560, 1000, 1150, 0, SAND)
    if towel:
        E.rrect(d, 660, 790, 900, 930, 10, E.HOT)
        for k in range(3):
            E.rrect(d, 660, 810 + k * 40, 900, 826 + k * 40, 0, E.WHITE)
    wx = E.lerp(300, 760, level)
    pts = [(80, 1150), (80, 560)]
    for k in range(13):
        y = 560 + k * 49
        pts.append((wx + 18 * math.sin(k * 0.9 + level * 6), y))
    pts.append((wx, 1150))
    E.poly(d, pts, fill=SEA)
    E.line(d, pts[2:-1], E.WHITE, 5)
    for k in range(3):
        E.line(d, [(110, 640 + k * 180), (wx - 60, 640 + k * 180)], SEA_D, 4)

def ocean(E, d, near, far, rot=0.0):
    pts = []
    for k in range(120):
        a = 2 * math.pi * k / 120
        c = math.cos(a)
        bulge = near * max(0.0, c) ** 2 + far * max(0.0, -c) ** 2
        r = ER + 18 + bulge
        pts.append((EX + r * math.cos(a), EY + r * math.sin(a)))
    E.poly(d, pts, fill=SEA)
    E.circle(d, EX, EY, ER, fill=(40, 70, 60))
    for k in range(5):
        a = rot + k * 1.3
        E.circle(d, EX + 110 * math.cos(a), EY + 110 * math.sin(a) * 0.9, 45 - k * 4, fill=LAND)

def moon(E, d):
    E.circle(d, MX, MY, MR, fill=(215, 218, 225))
    E.circle(d, MX - 15, MY - 12, 12, fill=(180, 184, 192)); E.circle(d, MX + 18, MY + 16, 9, fill=(180, 184, 192))

def scene(i, u, L, E, im, d):
    if i == 0:  # everyday: the towel ends up wet
        k = E.ease(u / (L * 0.85))
        beach(E, d, k)
        E.label(d, "HACE UN RATO", 540, 400, 40, color=E.MUTED) if u < L * 0.4 else E.label(d, "HORAS DESPUÉS", 540, 400, 40, color=E.WHITE)
        if k > 0.85: E.label(d, "¡MOJADA!", 780, 1040, 46, color=E.AMB)
    elif i == 1:  # sea level rises and falls
        lv = 0.5 + 0.45 * math.sin(u * 2.2)
        beach(E, d, lv)
        E.arrow(d, 960, 640, 960, 470, color=E.WHITE, w=7)
        E.arrow(d, 960, 680, 960, 850, color=E.WHITE, w=7)
        E.label(d, "MAREA", 540, 400, 50, color=E.AMB)
    elif i == 2:  # Moon's gravity
        ocean(E, d, 0, 0)
        moon(E, d)
        for k in range(3):
            x = EX + ER + 40 + ((u * 120 + k * 80) % 200)
            E.arrow(d, x, EY - 60 + k * 60, x + 50, EY - 60 + k * 60, color=E.AMB, w=5, head=18)
        E.label(d, "GRAVEDAD", 720, 480, 46, color=E.AMB)
        E.label(d, "LUNA", MX, MY + 100, 40, color=E.WHITE)
    elif i == 3:  # stronger pull on the near side (differential)
        ocean(E, d, 0, 0)
        moon(E, d)
        k = E.ease(u / (L * 0.5))
        E.arrow(d, EX + ER + 25, EY, EX + ER + 25 + 150 * k, EY, color=E.AMB, w=10)
        E.arrow(d, EX - 30, EY, EX - 30 + 95 * k, EY, color=E.WHITE, w=8)
        E.arrow(d, EX - ER - 30, EY, EX - ER - 30 + 50 * k, EY, color=E.MUTED, w=7, head=20)
        E.label(d, "MÁS FUERZA", 720, 560, 42, color=E.AMB)
        if u > 0.8: E.label(d, "MÁS CERCA", 720, 900, 40, color=E.WHITE)
    elif i == 4:  # near-side bulge
        k = E.ease(u / (L * 0.7))
        ocean(E, d, 75 * k, 0)
        moon(E, d)
        E.label(d, "ABULTAMIENTO", EX + 200, 480, 42, color=E.AMB)
    elif i == 5:  # opposite-side bulge
        k = E.ease(u / (L * 0.7))
        ocean(E, d, 75, 75 * k)
        moon(E, d)
        E.label(d, "MENOS FUERZA", 300, 460, 40, color=E.WHITE)
        if u > 0.6: E.label(d, "OTRO ABULTAMIENTO", 420, 1050, 42, color=E.AMB)
    elif i == 6:  # Earth turns: your beach goes through high and low tide
        rot = u * 1.4
        ocean(E, d, 75, 75, rot=rot)
        moon(E, d)
        a = rot + math.pi * 0.75
        c = math.cos(a)
        r = ER + 18 + 75 * c * c
        px, py = EX + (r + 10) * math.cos(a), EY + (r + 10) * math.sin(a)
        E.circle(d, px, py, 16, fill=E.AMB, outline=E.WHITE, w=4)
        E.label(d, "TU PLAYA", 540, 400, 44, color=E.AMB)
        E.label(d, "MAREA ALTA" if c * c > 0.5 else "MAREA BAJA", 540, 1080, 46, color=E.WHITE)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.3, 1.2), ("pop", s[0] + 1.6), ("whoosh", s[1] + 0.3, 1.0), ("pop", s[2] + 0.5),
            ("pop", s[3] + 0.6), ("whoosh", s[4] + 0.2, 0.8), ("whoosh", s[5] + 0.3, 0.8), ("pop", s[6] + 0.8)]
