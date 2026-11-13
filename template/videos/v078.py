"""Video 078 — ¿Por qué cambian de color las hojas en otoño?
Science: in summer leaves are full of chlorophyll, the green pigment that captures sunlight for photosynthesis (making
sugars, the plant's food). Leaves also contain yellow and orange pigments (carotenoids) that are masked by the much
more abundant green. In autumn, as days shorten and it gets colder, the tree stops making chlorophyll and the existing
chlorophyll breaks down. With the green gone, the yellows and oranges that were there all along become visible. Reds
and purples (anthocyanins) are different: some species make them new in autumn.
(No day-length or temperature thresholds are claimed; the role of anthocyanins is not claimed.)
"""
import math

ID = "078"
TITLE = "¿Por qué cambian de color las hojas en otoño?"
SUBTITLE = "CIENCIA EN 30 SEGUNDOS"
LINES = [
    "¿Por qué las hojas cambian de color en otoño?",
    "En verano, las hojas están llenas de clorofila, un pigmento verde.",
    "La clorofila capta la luz del sol para fabricar alimento.",
    "Pero la hoja también tiene pigmentos amarillos y naranjas, tapados por el verde.",
    "En otoño los días se acortan y el árbol deja de fabricar clorofila.",
    "El verde se descompone y aparecen los amarillos que siempre estuvieron ahí.",
    "Los rojos, en cambio, se fabrican nuevos en algunas hojas.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"hojas", "color", "otoño", "verano", "clorofila", "pigmento", "verde", "luz", "sol", "alimento",
            "amarillos", "naranjas", "tapados", "días", "acortan", "árbol", "descompone", "rojos", "nuevos"}

GREEN = (60, 160, 70)
YEL = (245, 200, 40)
ORA = (240, 130, 30)
RED = (200, 40, 40)
TRUNK = (110, 75, 45)


def leaf(E, d, x, y, s, col, ang=0.0, vein=True):
    pts = []
    for k in range(24):
        t = k / 23 * math.pi
        lx = -100 + 200 * k / 23
        ly = 45 * math.sin(t)
        pts.append((lx, ly))
    for k in range(23, -1, -1):
        t = k / 23 * math.pi
        pts.append((-100 + 200 * k / 23, -45 * math.sin(t)))
    ca, sa = math.cos(ang), math.sin(ang)
    P = [(x + s * (px * ca - py * sa), y + s * (px * sa + py * ca)) for px, py in pts]
    E.poly(d, P, fill=col)
    if vein:
        E.line(d, [(x - 115 * s * ca, y - 115 * s * sa), (x + 95 * s * ca, y + 95 * s * sa)],
               E.mix(col, (40, 30, 20), 0.4), max(2, 4 * s))


def big_leaf(E, d, col, x=540, y=680, s=4.0):
    leaf(E, d, x, y, s, col, ang=-0.35)


def dots(E, d, x, y, n, col, r=12, spread=280, seed=0):
    for k in range(n):
        a = (k * 2.39996 + seed)
        rr = spread * math.sqrt((k + 0.5) / n)
        E.circle(d, x + rr * math.cos(a), y + 0.45 * rr * math.sin(a), r, fill=col)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: crown turning from green to yellow/red, leaves falling
        E.rrect(d, 500, 760, 580, 1150, 10, TRUNK)
        k = min(1.0, u / max(0.5, L * 0.8))
        for j in range(18):
            a = j * 2.39996
            r = 230 * math.sqrt((j + 0.5) / 18)
            x, y = 540 + r * math.cos(a), 580 + 0.7 * r * math.sin(a)
            target = (YEL, ORA, RED)[j % 3]
            leaf(E, d, x, y, 0.75, E.mix(GREEN, target, k), ang=a, vein=False)
        for j in range(4):
            f = ((u * 0.5) + j / 4) % 1.0
            leaf(E, d, 300 + j * 160 + 40 * math.sin(f * 6), 700 + 440 * f, 0.5, (YEL, ORA, RED, ORA)[j],
                 ang=f * 5, vein=False)
    elif i == 1:  # summer leaf full of green chlorophyll
        big_leaf(E, d, GREEN)
        dots(E, d, 540, 680, 26, (30, 120, 40), r=13)
        E.label(d, "CLOROFILA", 540, 380, 56, color=(120, 220, 120))
        E.label(d, "VERDE", 540, 1060, 50, color=E.WHITE)
    elif i == 2:  # chlorophyll captures sunlight to make food
        big_leaf(E, d, GREEN, y=820, s=3.2)
        E.circle(d, 180, 380, 70, fill=E.AMB)
        for k in range(3):
            E.wave(d, 250, 420 + k * 40, 480 + k * 80, 720 + k * 20, 50, 10, E.AMB, 4, u * 8)
        k = E.ease(u / (L * 0.8))
        E.pill(d, "ALIMENTO", 820, 420 + 40 * (1 - k), 42)
        E.arrow(d, 700, 720, 800, 500, E.WHITE, 6, 24)
        E.label(d, "LUZ", 110, 500, 44, color=E.AMB)
    elif i == 3:  # yellow/orange pigments hidden under green
        big_leaf(E, d, GREEN)
        dots(E, d, 540, 680, 14, YEL, r=12, seed=1.1)
        dots(E, d, 540, 680, 8, ORA, r=12, seed=2.3)
        k = 0.5 + 0.5 * math.sin(u * 4)
        dots(E, d, 540, 680, 26, E.mix(GREEN, (30, 120, 40), k), r=17)
        E.label(d, "AMARILLO Y NARANJA", 540, 380, 46, color=YEL)
        E.label(d, "TAPADOS", 540, 1060, 50, color=E.WHITE)
    elif i == 4:  # shorter days, no new chlorophyll
        k = E.ease(u / (L * 0.9))
        E.line(d, [(120, 900), (960, 900)], E.SIL_D, 4)
        hh = 420 - 180 * k
        pts = [(540 + 380 * math.cos(t / 30 * math.pi), 900 - hh * math.sin(t / 30 * math.pi)) for t in range(31)]
        E.line(d, pts, E.mix(E.AMB, E.MUTED, 0.3), 5)
        sx = 540 + 380 * math.cos(0.5 * math.pi)
        E.circle(d, sx, 900 - hh, 55, fill=E.AMB)
        E.label(d, "DÍAS MÁS CORTOS", 540, 360, 50, color=E.WHITE)
        leaf(E, d, 540, 1050, 1.2, E.mix(GREEN, (130, 150, 60), k), ang=-0.2)
        E.cross(d, 820, 1050, 40)
        E.label(d, "CLOROFILA", 820, 1130, 34, color=E.MUTED)
    elif i == 5:  # green breaks down, yellow appears
        k = E.ease(u / (L * 0.85))
        big_leaf(E, d, E.mix(GREEN, YEL, k))
        dots(E, d, 540, 680, 14, YEL, r=12, seed=1.1)
        dots(E, d, 540, 680, 8, ORA, r=12, seed=2.3)
        if k < 0.95:
            dots(E, d, 540, 680, int(26 * (1 - k)), (30, 120, 40), r=17)
        E.label(d, "SIEMPRE ESTUVIERON AHÍ", 540, 380, 44, color=YEL)
    elif i == 6:  # reds made new in some leaves
        leaf(E, d, 330, 700, 2.0, YEL, ang=-0.4)
        k = E.ease(u / (L * 0.85))
        leaf(E, d, 760, 700, 2.0, E.mix(YEL, RED, k), ang=0.4)
        dots(E, d, 760, 700, int(1 + 14 * k), (150, 20, 30), r=9, spread=130)
        E.label(d, "AMARILLO", 330, 960, 42, color=YEL)
        E.label(d, "ROJO NUEVO", 760, 960, 42, color=RED)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.2, 0.8), ("pop", s[1] + 0.5), ("whoosh", s[2] + 0.5, 0.8), ("pop", s[3] + 0.6),
            ("click", s[4] + 0.6), ("whoosh", s[5] + 0.5, 0.8), ("pop", s[6] + 0.6)]
