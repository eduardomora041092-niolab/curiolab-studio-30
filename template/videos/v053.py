"""Video 053 — ¿Cómo funciona un cortaúñas?
Science: a typical nail clipper is a compound lever: two levers acting one after the other. The first is the handle
(top lever): it pivots on the pin at the front and, when you press its long end, it pushes on the jaws with a larger
force than the finger's. The second lever is formed by the two jaws, joined at the back; when the top jaw is pushed
down, the cutting edges at the front come together and cut the nail. Together they multiply the finger's force
several times.
(The exact mechanical advantage depends on the model and is not stated; lever classes are not narrated.)
"""
import math

ID = "053"
TITLE = "¿Cómo funciona un cortaúñas?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo corta un cortaúñas con tan poco esfuerzo?",
    "Por dentro tiene dos palancas, una encima de la otra.",
    "La de arriba es el mango y gira sobre el perno.",
    "Al apretar su extremo largo, empuja las hojas con más fuerza.",
    "Las hojas son la segunda palanca, unidas por detrás.",
    "Al bajar, sus filos se juntan y cortan la uña.",
    "Juntas, multiplican varias veces la fuerza de tu dedo.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"cortaúñas", "esfuerzo", "palancas", "mango", "gira", "perno", "apretar", "extremo", "hojas",
            "fuerza", "segunda", "palanca", "detrás", "filos", "uña", "multiplican", "dedo"}

RX, RY = 900, 820        # rivet joining the jaws (back)
FX = 230                 # front (cutting edges)
PINX = 330               # pin position
LOW_F = 880              # lower jaw front y
NAIL = (246, 214, 200)
NAIL_D = (214, 170, 150)


def up_front(c):
    return 760 + 98 * c   # upper jaw front y (c: 0 open .. 1 closed)


def jaw_y(front_y, x, back_y):
    t = (x - FX) / (RX - FX)
    return front_y + (back_y - front_y) * t


def clipper(E, d, c, hi_handle=False, hi_jaws=False, hi_pin=False, hi_rivet=False, nail=True, cut=False):
    uf = up_front(c)
    # nail between the edges
    if nail:
        if cut:
            E.rrect(d, 70, 836, 210, 872, 14, NAIL, outline=NAIL_D, w=3)
            E.rrect(d, 120, 960 + 60 * min(1, c), 190, 990 + 60 * min(1, c), 10, NAIL, outline=NAIL_D, w=3)
        else:
            E.rrect(d, 70, 836, 262, 872, 14, NAIL, outline=NAIL_D, w=3)
    jc = E.AMB if hi_jaws else E.SIL_D
    # lower jaw
    E.poly(d, [(FX, LOW_F - 22), (RX, RY + 8), (RX, RY + 40), (FX + 10, LOW_F + 24)], fill=E.SIL, outline=jc, w=4)
    E.poly(d, [(FX - 12, LOW_F - 22), (FX + 30, LOW_F - 22), (FX + 10, LOW_F - 46)], fill=E.SIL_H)   # lower edge
    # upper jaw
    E.poly(d, [(FX + 10, uf - 24), (RX, RY - 40), (RX, RY - 8), (FX, uf + 22)], fill=E.SIL_H, outline=jc, w=4)
    E.poly(d, [(FX - 12, uf + 22), (FX + 30, uf + 22), (FX + 10, uf + 46)], fill=E.SIL_H)            # upper edge
    E.circle(d, RX, RY, 24, fill=E.AMB if hi_rivet else E.SIL_D)
    # pin, fixed to the lower jaw, passes through the upper one
    py_low = jaw_y(LOW_F, PINX, RY)
    head = py_low - 220
    E.line(d, [(PINX, py_low), (PINX, head)], E.SIL_D, 14)
    # handle: pivots at the pin head; a bump presses on the upper jaw; the long end goes to the back
    ang = math.radians(24 - 22 * c)
    ex, ey = PINX + 640 * math.cos(ang), head - 640 * math.sin(ang)
    hc = E.AMB if hi_handle else E.SIL_D
    E.line(d, [(PINX, head), (ex, ey)], E.SIL, 34)
    E.line(d, [(PINX, head), (ex, ey)], hc, 4)
    bx = PINX + 70
    by_top = head - 70 * math.tan(ang)
    by_jaw = jaw_y(uf, bx, RY - 40) - 24
    E.rrect(d, bx - 16, by_top, bx + 16, max(by_top + 20, by_jaw), 8, E.SIL_D)
    E.circle(d, PINX, head, 22, fill=E.AMB if hi_pin else E.SIL_H, outline=E.SIL_D, w=3)
    return (ex, ey), (bx, by_jaw)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: handle going down, edges closing on the nail
        c = 0.5 + 0.5 * math.sin(u * 2.6 - 1.2)
        (ex, ey), _ = clipper(E, d, c)
        E.arrow(d, ex, ey - 150, ex, ey - 40, E.AMB, 8, 28)
        E.pill(d, "POCO ESFUERZO", 540, 1110, 42)
    elif i == 1:  # two levers, one above the other
        clipper(E, d, 0.2, hi_handle=True, hi_jaws=True)
        E.label(d, "PALANCA 1", 760, 400, 46, color=E.AMB)
        E.label(d, "PALANCA 2", 640, 1040, 46, color=E.AMB)
    elif i == 2:  # the handle pivots on the pin
        c = 0.3 + 0.25 * math.sin(u * 2)
        clipper(E, d, c, hi_handle=True, hi_pin=True)
        E.label(d, "PERNO", PINX - 110, 560, 46, color=E.AMB)
        E.label(d, "MANGO", 760, 400, 46, color=E.WHITE)
    elif i == 3:  # pressing the long end -> bigger push on the jaws
        k = E.ease(min(1, u / (L * 0.7)))
        (ex, ey), (bx, by) = clipper(E, d, 0.6 * k, hi_handle=True)
        E.arrow(d, ex - 30, ey - 160, ex - 30, ey - 40, E.AMB, 7, 24)
        E.label(d, "TU DEDO", ex - 60, ey - 200, 40, color=E.AMB)
        E.arrow(d, bx + 70, by - 120, bx + 70, by + 10, E.HOT, 16, 42)
        E.label(d, "MÁS FUERZA", bx + 110, 1000, 42, color=E.HOT)
    elif i == 4:  # jaws joined at the back
        c = 0.3 + 0.2 * math.sin(u * 2)
        clipper(E, d, c, hi_jaws=True, hi_rivet=True)
        E.label(d, "UNIDAS", RX - 40, RY + 120, 46, color=E.AMB)
        E.label(d, "HOJAS", 560, 1040, 46, color=E.WHITE)
    elif i == 5:  # edges close and cut the nail
        k = E.ease(min(1, u / (L * 0.5)))
        clipper(E, d, k, cut=k > 0.95)
        E.label(d, "FILOS", 200, 650, 44, color=E.AMB)
        if k > 0.95:
            E.pill(d, "¡CORTE!", 540, 1110, 42)
    elif i == 6:  # small finger force -> big force at the edges
        (ex, ey), _ = clipper(E, d, 0.7)
        E.arrow(d, ex - 30, ey - 120, ex - 30, ey - 40, E.MUTED, 5, 20)
        E.label(d, "DEDO", ex - 40, ey - 160, 40, color=E.MUTED)
        E.arrow(d, 240, 620, 240, 780, E.AMB, 18, 48)
        E.label(d, "FILOS", 200, 570, 44, color=E.AMB)
        E.pill(d, "VARIAS VECES MÁS", 540, 1110, 42)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("click", s[0] + 0.3), ("pop", s[1] + 0.6), ("zip", s[2] + 0.4, 0.8), ("whoosh", s[3] + 0.3, 1.0),
            ("pop", s[4] + 0.6), ("click", s[5] + 1.0), ("whoosh", s[6] + 0.3, 1.0)]
