"""Video 052 — ¿Por qué las tijeras cortan?
Science: scissors are two levers (blade + handle each) joined by a pivot screw. Closing the handles makes each blade
rotate about the pivot. The blades cross and their edges touch at a single point at any moment: the cutting point.
There each blade pushes the material in the opposite direction to the other (shear) and splits it. As the scissors
close, the cutting point travels along the blades from the pivot towards the tip. By the lever law, material placed
close to the pivot receives a larger force for the same force on the handles.
(No sharpening angles, blade curvature, materials or force figures are claimed.)
"""
import math

ID = "052"
TITLE = "¿Por qué las tijeras cortan?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo cortan las tijeras si sus hojas apenas se tocan?",
    "Son dos palancas unidas en el centro por un eje.",
    "Al cerrar los mangos, cada hoja gira sobre ese eje.",
    "Las hojas se cruzan y se tocan en un solo punto.",
    "Ahí empujan el papel en sentidos opuestos y lo parten.",
    "Al seguir cerrando, ese punto de corte avanza hacia la punta.",
    "Cerca del eje cortan con más fuerza: ahí se corta mejor lo duro.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"tijeras", "hojas", "palancas", "eje", "mangos", "gira", "cruzan", "punto", "papel", "opuestos",
            "parten", "corte", "avanza", "punta", "fuerza"}

PX, PY = 300, 720          # pivot
H = 30                     # edge offset at the pivot (blades cross further out)
LB = 590                   # blade length
LH = 180                   # handle length
PAPER = (236, 232, 222)
PAPER_D = (190, 184, 170)
STEEL_B = (150, 170, 196)


def edge_y(sign, a, s):
    """Cutting-edge y at distance s from the pivot. sign=+1: upper blade (edge rises), -1: lower blade."""
    return PY + sign * H - sign * math.tan(a) * s


def cut_x(a):
    return PX + H / max(0.02, math.tan(a))


def paper(E, d, a, x_start=PX + 40):
    """Sheet fed into the jaws; slit from its left edge up to the current cutting point."""
    xc = min(cut_x(a), 1040)
    E.rrect(d, x_start, PY - 170, 1060, PY + 170, 8, PAPER, outline=PAPER_D, w=3)
    if xc > x_start:
        E.line(d, [(x_start, PY), (xc, PY)], E.BG1, 6)


def scissors(E, d, a, hi_pivot=False, paper_on=False):
    if paper_on:
        paper(E, d, a)
    for sign, col in ((-1, E.SIL), (1, STEEL_B)):
        # blade: polygon between cutting edge and back edge, tapering to the tip
        pts_e = [(PX + s, edge_y(sign, a, s)) for s in (-30, LB)]
        back = [(PX + LB, edge_y(sign, a, LB) + sign * -6),
                (PX + LB * 0.5, edge_y(sign, a, LB * 0.5) - sign * 48),
                (PX - 30, edge_y(sign, a, -30) - sign * 60)]
        E.poly(d, pts_e + back, fill=col, outline=E.SIL_D, w=3)
        # handle continues the blade line behind the pivot (goes the other way)
        hx, hy = PX - LH, PY + sign * (math.tan(a) * LH + 48)
        E.line(d, [(PX - 10, PY + sign * 14), (hx + 40, hy)], col, 30)
        E.circle(d, hx, hy, 52, outline=E.AMB if sign > 0 else E.HOT, w=18)
    E.circle(d, PX, PY, 20, fill=E.AMB if hi_pivot else E.SIL_H, outline=E.SIL_D, w=3)


def cut_point(E, d, a, r=22):
    xc = cut_x(a)
    if xc < PX + LB:
        E.circle(d, xc, PY, r, outline=E.AMB, w=7)
    return xc


def osc(u, lo, hi, w=2.4):
    return lo + (hi - lo) * (0.5 + 0.5 * math.cos(u * w))


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: blades opening/closing, paper being cut
        a = math.radians(osc(u, 5, 20))
        scissors(E, d, a, paper_on=True)
        cut_point(E, d, a)
        E.pill(d, "¡CRIS, CRAS!", 540, 400, 42)
    elif i == 1:  # two levers joined by a pivot
        a = math.radians(16)
        scissors(E, d, a, hi_pivot=True)
        E.label(d, "EJE", PX, PY + 110, 50, color=E.AMB)
        E.label(d, "PALANCA 1", 720, 470, 42, color=E.WHITE)
        E.label(d, "PALANCA 2", 720, 980, 42, color=E.WHITE)
    elif i == 2:  # closing the handles: each blade rotates about the pivot
        k = E.ease(min(1, u / (L * 0.8)))
        a = math.radians(24 - 16 * k)
        scissors(E, d, a, hi_pivot=True)
        E.arrow(d, 120, 430, 120, 520, E.AMB, 7, 24)
        E.arrow(d, 120, 1010, 120, 920, E.HOT, 7, 24)
        E.label(d, "GIRAN", 760, 420, 48, color=E.AMB)
    elif i == 3:  # blades cross, touch at one point
        a = math.radians(12)
        scissors(E, d, a)
        xc = cut_point(E, d, a, r=26 + 6 * math.sin(u * 5))
        E.line(d, [(xc, PY - 34), (xc + 60, 480)], E.AMB, 5)
        E.label(d, "PUNTO DE CORTE", 720, 440, 44, color=E.AMB)
    elif i == 4:  # opposite pushes on the paper (shear)
        a = math.radians(12)
        scissors(E, d, a, paper_on=True)
        xc = cut_point(E, d, a)
        E.arrow(d, xc + 70, PY - 150, xc + 70, PY - 30, E.AMB, 8, 26)
        E.arrow(d, xc + 70, PY + 150, xc + 70, PY + 30, E.HOT, 8, 26)
        E.pill(d, "SENTIDOS OPUESTOS", 540, 1120, 40)
    elif i == 5:  # cutting point travels towards the tip
        k = E.ease(min(1, u / (L * 0.85)))
        a = math.radians(22 - 17 * k)
        scissors(E, d, a, paper_on=True)
        x0 = cut_x(math.radians(22))
        xc = cut_point(E, d, a)
        for j in range(6):
            x = x0 + (xc - x0) * j / 6
            E.circle(d, x, PY, 6, fill=E.AMB)
        E.arrow(d, 560, 1060, 860, 1060, E.AMB, 8, 28)
        E.label(d, "HACIA LA PUNTA", 710, 1120, 40, color=E.AMB)
    elif i == 6:  # more force near the pivot, less at the tip
        a = math.radians(9)
        scissors(E, d, a)
        E.arrow(d, 420, 420, 420, PY - 70, E.AMB, 16, 44)
        E.label(d, "MÁS FUERZA", 420, 360, 44, color=E.AMB)
        E.arrow(d, 840, 540, 840, PY - 30, E.MUTED, 5, 20)
        E.label(d, "MENOS", 840, 490, 40, color=E.MUTED)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("zip", s[0] + 0.1, 1.0), ("pop", s[1] + 0.6), ("whoosh", s[2] + 0.3, 1.0), ("pop", s[3] + 0.7),
            ("zip", s[4] + 0.4, 0.8), ("whoosh", s[5] + 0.3, 1.0), ("click", s[6] + 0.6)]
