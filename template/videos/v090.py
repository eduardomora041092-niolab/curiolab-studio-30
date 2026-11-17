"""Video 090 — ¿Cómo trepa un gecko por el cristal?
Science: a gecko's toes use no suction cups and no glue; the adhesion is dry. Under each toe there are ridges covered
with a huge number of microscopic hairs (setae), and each hair branches into even finer tips (spatulae). These tips get
so close to the surface that weak attractive forces between molecules (van der Waals forces) act between them and the
glass. Each force is tiny, but added over all the tips they hold the animal, even on smooth glass. To let go, the gecko
peels its toes off starting from the tip, changing the angle of the hairs, and they detach easily.
(No counts of hairs, load figures or claims about every gecko species are made.)
"""
import math

ID = "090"
TITLE = "¿Cómo trepa un gecko por el cristal?"
SUBTITLE = "CIENCIA EN 30 SEGUNDOS"
LINES = [
    "¿Cómo trepa un gecko por un cristal liso sin resbalar?",
    "No usa ventosas ni pegamento: sus dedos están secos.",
    "Bajo cada dedo hay muchísimos pelos microscópicos.",
    "Cada pelo se divide en puntas todavía más finas.",
    "Esas puntas se acercan tanto al cristal que sus moléculas se atraen.",
    "Cada atracción es diminuta, pero sumadas todas sostienen al gecko entero.",
    "Para soltarse, levanta el dedo desde la punta y se despega fácilmente.",
    "Sígueme para descubrir más ciencia.",
]
KEYWORDS = {"gecko", "cristal", "liso", "resbalar", "ventosas", "pegamento", "secos", "dedo", "pelos",
            "microscópicos", "puntas", "finas", "moléculas", "atraen", "atracción", "diminuta", "sumadas",
            "sostienen", "soltarse", "despega"}

GLASS = (46, 82, 118)
GLASS_H = (110, 160, 205)
SKIN = (120, 175, 90)
SKIN_D = (80, 130, 60)
HAIR = (200, 220, 170)
GX0, GX1 = 780, 870   # glass slab (close-up scenes)


def window(E, d):
    E.rrect(d, 180, 300, 900, 1180, 10, GLASS)
    for k in range(3):
        x = 260 + k * 90
        E.line(d, [(x, 1100), (x + 220, 380)], GLASS_H, 6)


def gecko(E, d, x, y, u, s=1.0):
    st = math.sin(u * 2 * math.pi * 1.2)
    # tail
    pts = [(x + 18 * math.sin(u * 6 + k * 0.6) * s * (k / 8), y + (120 + k * 22) * s) for k in range(9)]
    E.line(d, [(x, y + 100 * s)] + pts, SKIN_D, int(26 * s))
    # legs (diagonal pairs alternate)
    for sx, sy, ph in ((-1, 0, 1), (1, 0, -1), (-1, 1, -1), (1, 1, 1)):
        by = y + (20 if sy == 0 else 110) * s
        fx = x + sx * 90 * s
        fy = by + (-30 + 25 * st * ph) * s
        E.line(d, [(x, by), (x + sx * 55 * s, by + 10 * s), (fx, fy)], SKIN, int(18 * s))
        for t in (-1, 0, 1):
            E.circle(d, fx + sx * 14 * s + t * 6 * s, fy - 14 * s + t * 12 * s * sx, 9 * s, fill=SKIN)
    # body + head
    E.line(d, [(x, y - 20 * s), (x, y + 120 * s)], SKIN, int(60 * s))
    E.circle(d, x, y - 60 * s, 42 * s, fill=SKIN)
    E.circle(d, x - 18 * s, y - 72 * s, 8 * s, fill=E.CAV)
    E.circle(d, x + 18 * s, y - 72 * s, 8 * s, fill=E.CAV)


def glass_slab(E, d):
    E.rrect(d, GX0, 300, GX1, 1180, 6, GLASS)
    E.line(d, [(GX0, 300), (GX0, 1180)], GLASS_H, 5)


def toe(E, d, lift=0.0, hl=False):
    """Big toe pad seen from the side, pressed against the glass on the right."""
    c = E.AMB if hl else SKIN
    E.rrect(d, 200, 600, 700, 820, 90, c)
    # ridges (lamellae) on the glass-facing side
    for k in range(5):
        y = 630 + k * 40
        E.line(d, [(640 - lift * 40 * (k / 4), y), (700 - lift * 60 * (k / 4), y + 10)], SKIN_D, 8)


def hairs(E, d, x0, x1, y0, y1, n, lift=0.0):
    for k in range(n):
        y = y0 + (y1 - y0) * k / (n - 1)
        frac = k / (n - 1)
        detach = max(0.0, lift * 1.6 - (1 - frac))  # tip end (bottom) lets go first
        xe = x1 - min(1.0, detach) * 140
        E.line(d, [(x0, y), ((x0 + xe) / 2, y + 6), (xe, y)], HAIR, 4)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: gecko already climbing the window
        window(E, d)
        y = 980 - (u * 90) % 520
        gecko(E, d, 540, y, u)
    elif i == 1:  # no suction cups, no glue
        window(E, d)
        gecko(E, d, 540, 760, u * 0.3)
        E.label(d, "VENTOSAS", 330, 400, 42, color=E.WHITE)
        E.cross(d, 330, 470, 30)
        E.label(d, "PEGAMENTO", 760, 400, 42, color=E.WHITE)
        E.cross(d, 760, 470, 30)
        E.label(d, "DEDOS SECOS", 540, 1120, 44, color=E.AMB)
    elif i == 2:  # many microscopic hairs under each toe
        glass_slab(E, d)
        toe(E, d, hl=False)
        hairs(E, d, 700, GX0, 610, 810, 18)
        E.label(d, "PELOS MICROSCÓPICOS", 480, 450, 42, color=E.AMB)
        E.arrow(d, 600, 485, 735, 600, E.AMB, 5, 20)
        E.label(d, "DEDO", 420, 560, 44, color=E.WHITE)
    elif i == 3:  # each hair branches into finer tips
        glass_slab(E, d)
        E.line(d, [(200, 740), (520, 740)], HAIR, 16)
        for k in range(7):
            yt = 540 + k * 66
            E.line(d, [(520, 740), (640, (740 + yt) / 2), (GX0 - 4, yt)], HAIR, 6)
            E.circle(d, GX0 - 8, yt, 8, fill=E.AMB)
        E.label(d, "UN PELO", 330, 680, 44, color=E.WHITE)
        E.label(d, "PUNTAS", 620, 420, 44, color=E.AMB)
    elif i == 4:  # tips so close that molecules attract each other
        glass_slab(E, d)
        for k in range(5):
            yt = 470 + k * 140
            E.line(d, [(300, yt), (GX0 - 76, yt)], HAIR, 10)
            E.circle(d, GX0 - 70, yt, 16, fill=E.AMB)
            E.circle(d, GX0 + 22, yt, 16, fill=GLASS_H)
            p = 0.5 + 0.5 * math.sin(u * 5 + k)
            E.arrow(d, GX0 - 52, yt - 30, GX0 - 52 + 30 + 10 * p, yt - 30, E.WHITE, 5, 14)
            E.arrow(d, GX0 + 4, yt + 30, GX0 + 4 - 30 - 10 * p, yt + 30, E.WHITE, 5, 14)
        E.label(d, "SE ATRAEN", 450, 380, 46, color=E.AMB)
        E.label(d, "MOLÉCULAS", 450, 1130, 42, color=GLASS_H)
    elif i == 5:  # tiny forces add up and hold the whole gecko
        window(E, d)
        gecko(E, d, 540, 700, u * 0.3)
        for fx, fy in ((450, 690), (630, 690), (450, 780), (630, 780)):
            E.circle(d, fx, fy, 40, outline=E.AMB, w=6)
        E.label(d, "TODAS SUMADAS", 540, 380, 46, color=E.AMB)
    elif i == 6:  # peel from the tip to let go
        lift = min(1.0, u / max(1.0, L * 0.7))
        glass_slab(E, d)
        toe(E, d, lift=lift)
        hairs(E, d, 700, GX0, 610, 810, 18, lift=lift)
        E.arrow(d, 660, 900, 520, 1000, E.WHITE, 6, 22)
        E.label(d, "SE DESPEGA", 400, 450, 46, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.2, 0.8), ("pop", s[1] + 0.5), ("zip", s[2] + 0.5), ("pop", s[3] + 0.6),
            ("click", s[4] + 0.6), ("whoosh", s[5] + 0.5, 0.8), ("zip", s[6] + 0.7)]
