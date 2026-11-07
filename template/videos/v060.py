"""Video 060 — ¿Por qué la sal derrite el hielo?
Science: the surface of ice usually carries a very thin film of liquid water. At the melting point, at the boundary
between ice and water, some molecules freeze onto the ice while others melt away, at the same rate (a dynamic
balance). Salt dissolves in that water and makes brine. The dissolved particles get in the way of water molecules
joining the ice, so less water freezes while melting goes on, and the ice shrinks. Salty water therefore freezes at a
lower temperature than pure water, which is why salt melts ice below 0 °C. The salt does not heat the ice.
(The lowest working temperature and amounts are not claimed.)
"""
import math

ID = "060"
TITLE = "¿Por qué la sal derrite el hielo?"
SUBTITLE = "CIENCIA EN 30 SEGUNDOS"
LINES = [
    "¿Cómo derrite la sal el hielo si no lo calienta?",
    "Sobre el hielo siempre hay una capa finísima de agua líquida.",
    "Ahí, unas moléculas se congelan y otras se funden a la vez.",
    "La sal se disuelve en esa agua y forma salmuera.",
    "Sus partículas estorban a las moléculas que intentan congelarse.",
    "Se funde más agua de la que se congela, y el hielo mengua.",
    "Por eso el agua salada se congela por debajo de cero grados.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"derrite", "sal", "hielo", "calienta", "capa", "agua", "líquida", "moléculas", "congelan", "funden",
            "disuelve", "salmuera", "partículas", "estorban", "congelarse", "funde", "mengua", "salada",
            "congela", "cero", "grados"}

ICE = (150, 205, 240)
ICE_D = (90, 150, 200)
WAT = (60, 130, 220)
NA = (255, 176, 32)
CL = (120, 220, 140)


def macro(E, d, u, salt=True, melt=0.0):
    """Ice slab on the ground, salt grains falling, puddle growing."""
    E.rrect(d, 80, 980, 1000, 1060, 10, (70, 70, 80))                      # pavement
    top = 760 + 140 * melt
    E.rrect(d, 180, top, 900, 980, 18, ICE, outline=ICE_D, w=5)
    for k in range(5):
        E.line(d, [(240 + k * 140, top + 30), (300 + k * 140, top + 90)], (230, 245, 255), 4)
    pw = 120 + 300 * melt
    E.rrect(d, 540 - pw - 300, 965, 540 + pw + 300, 990, 12, WAT)          # puddle around
    if salt:
        for k in range(18):
            q = (u * 0.9 + k / 18) % 1.0
            x = 230 + (k * 97) % 640
            y = 380 + q * (top - 390)
            E.rrect(d, x - 9, y - 9, x + 9, y + 9, 3, (240, 240, 245))
        for k in range(12):    # grains already on the ice
            x = 220 + (k * 61) % 660
            E.rrect(d, x - 7, top - 12, x + 7, top + 2, 3, (240, 240, 245))


ROWS, COLS = 3, 8
GX0, GY0, GS = 150, 760, 100


def ice_lattice(E, d, missing=()):
    for r in range(ROWS):
        for c in range(COLS):
            if (r, c) in missing: continue
            x, y = GX0 + c * GS + (GS / 2 if r % 2 else 0) * 0, GY0 + r * GS
            E.rrect(d, x, y, x + GS - 10, y + GS - 10, 12, ICE, outline=ICE_D, w=3)
            E.circle(d, x + 45, y + 45, 16, fill=(230, 245, 255))


def water_layer(E, d, u, n=12, salt=0, block=False):
    E.rrect(d, 120, 470, 960, 750, 24, (24, 52, 96), outline=WAT, w=4)
    for k in range(n):
        x = 170 + (k * 137 + 60 * math.sin(u * 2 + k)) % 740
        y = 520 + (k * 53) % 190 + 12 * math.sin(u * 3 + k * 1.7)
        E.circle(d, x, y, 18, fill=WAT, outline=(150, 200, 255), w=3)
    for k in range(salt):
        x = 200 + (k * 173 + 40 * math.sin(u * 1.5 + k)) % 680
        y = 540 + (k * 71) % 170 + 10 * math.cos(u * 2 + k)
        E.circle(d, x, y, 15, fill=NA if k % 2 else CL)


def exchange(E, d, u, down=1.0, up=1.0, blocked=False):
    """Arrows across the ice/water boundary: freezing (down) and melting (up)."""
    for k, x in enumerate((250, 460, 670, 880)):
        if k % 2 == 0:
            if down > 0:
                E.arrow(d, x, 650, x, 650 + 110 * down, E.COLD, 7, 24)
                if blocked:
                    E.cross(d, x, 720, 28, E.HOT, 9)
        else:
            if up > 0:
                E.arrow(d, x, 790, x, 790 - 120 * up, E.HOT, 7, 24)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: salt falling on ice, puddle forming
        macro(E, d, u + 0.35, salt=True, melt=min(1.0, 0.15 + u / L))
        E.pill(d, "SIN CALOR", 540, 330, 44)
    elif i == 1:  # thin liquid film on the ice
        ice_lattice(E, d)
        water_layer(E, d, u, n=10)
        E.label(d, "AGUA LÍQUIDA", 540, 410, 50, color=WAT)
        E.label(d, "HIELO", 540, 1150, 50, color=ICE)
    elif i == 2:  # freezing and melting at the same time
        ice_lattice(E, d)
        water_layer(E, d, u, n=10)
        exchange(E, d, u)
        E.label(d, "SE CONGELAN", 300, 410, 42, color=E.COLD)
        E.label(d, "SE FUNDEN", 780, 410, 42, color=E.HOT)
        E.label(d, "A LA VEZ", 540, 1150, 46, color=E.AMB)
    elif i == 3:  # salt dissolves -> brine
        k = min(1.0, u / (L * 0.6))
        ice_lattice(E, d)
        water_layer(E, d, u, n=10, salt=int(2 + 10 * k))
        E.label(d, "SALMUERA", 540, 410, 52, color=E.AMB)
        E.circle(d, 250, 1150, 15, fill=NA); E.circle(d, 290, 1150, 15, fill=CL)
        E.label(d, "PARTÍCULAS DE SAL", 580, 1150, 40, color=E.WHITE)
    elif i == 4:  # particles get in the way of freezing
        ice_lattice(E, d)
        water_layer(E, d, u, n=10, salt=12)
        exchange(E, d, u, down=1.0, up=1.0, blocked=True)
        E.label(d, "ESTORBAN", 540, 410, 52, color=E.HOT)
    elif i == 5:  # more melts than freezes: ice shrinks
        k = E.ease(min(1.0, u / (L * 0.8)))
        gone = [(0, c) for c in range(COLS) if c < int(1 + 7 * k)]
        ice_lattice(E, d, missing=gone)
        water_layer(E, d, u, n=10 + len(gone), salt=12)
        exchange(E, d, u, down=0.3, up=1.0)
        E.label(d, "EL HIELO MENGUA", 540, 410, 48, color=E.AMB)
    elif i == 6:  # salty water freezes below zero
        # thermometer scale
        E.rrect(d, 500, 320, 580, 1060, 40, (40, 50, 70), outline=E.SIL, w=5)
        E.circle(d, 540, 1080, 60, fill=E.COLD, outline=E.SIL, w=5)
        k = E.ease(min(1.0, u / (L * 0.5)))
        E.rrect(d, 522, 700 + 200 * k, 558, 1060, 18, E.COLD)
        y0, y1 = 620, 880
        E.line(d, [(470, y0), (610, y0)], E.WHITE, 6)
        E.label(d, "0 °C", 400, y0, 46, color=E.WHITE)
        E.label(d, "AGUA", 780, y0 - 30, 42, color=WAT)
        E.label(d, "SE CONGELA", 780, y0 + 25, 36, color=E.WHITE)
        E.line(d, [(470, y1), (610, y1)], E.AMB, 6)
        E.label(d, "MÁS FRÍO", 330, y1, 40, color=E.AMB)
        E.label(d, "AGUA SALADA", 800, y1 - 30, 40, color=E.AMB)
        E.label(d, "SE CONGELA", 800, y1 + 25, 36, color=E.WHITE)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 0.8), ("pop", s[1] + 0.6), ("click", s[2] + 0.8), ("zip", s[3] + 0.5),
            ("pop", s[4] + 0.7), ("whoosh", s[5] + 0.5, 0.9), ("click", s[6] + 0.9)]
