"""Video 019 — ¿Cómo funciona un candado de combinación?
Mechanism: inside a combination padlock there is a stack of discs (wheels), one per number of the combination.
Each disc has a small notch (gate) cut into its edge. Turning the dial moves the discs to new positions. When the
right number is set, that disc's notch stops at one precise position. A locking bar rests on the edges of the
discs: if any disc is out of place, its solid edge holds the bar up and the shackle stays locked. When every notch
is aligned, the bar drops into the notches and the shackle is released.
(How the dial drives each disc, number of turns or combinations is model-dependent and not claimed.)
"""
import math

ID = "019"
TITLE = "¿Cómo funciona un candado de combinación?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo se abre un candado con solo tres números?",
    "Dentro del candado hay tres discos apilados, uno por número.",
    "Cada disco tiene una pequeña muesca en el borde.",
    "Al girar la rueda, los discos cambian de posición.",
    "Con el número correcto, cada muesca queda en su sitio.",
    "Si un solo disco está mal, la barra no puede bajar.",
    "Con las tres alineadas, la barra cae en las muescas y suelta el arco.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"candado", "tres", "números", "discos", "apilados", "muesca", "borde", "girar", "rueda", "posición",
            "correcto", "sitio", "mal", "barra", "bajar", "alineadas", "cae", "suelta", "arco", "funcionan"}

BODY, BODY_D = (200, 60, 50), (140, 40, 35)
TOP = -math.pi / 2           # notch "in place" = pointing up, under the bar
DX = (330, 540, 750)         # disc centres (x)
DY, DR = 860, 95             # disc centre y, radius
NOTCH = 26                   # notch depth

def shackle(E, d, lift=0.0, x0=330, x1=750, base=600, top=390, color=None):
    color = color or E.SIL
    y = base - lift
    cx, r = (x0 + x1) / 2, (x1 - x0) / 2
    cy = top - lift + r
    pts = [(x0, y)] + [(cx + r * math.cos(math.pi * (1 - t / 24)), cy - r * math.sin(math.pi * (1 - t / 24))) for t in range(25)] + [(x1, y)]
    if lift > 0:
        pts = [(x0, base)] + pts   # the long leg stays inside the body when the shackle pops up
    E.line(d, pts, E.SIL_D, 52)
    E.line(d, pts, color, 38)

def body(E, d, alpha_open=False):
    E.rrect(d, 200, 580, 880, 1150, 60, BODY_D)
    E.rrect(d, 215, 590, 865, 1135, 52, BODY)
    if alpha_open:
        E.rrect(d, 245, 620, 835, 1105, 40, E.CAV)

def disc(E, d, i, ang, hl=False, bad=False):
    x = DX[i]
    E.circle(d, x, DY, DR, fill=E.SIL_D)
    E.circle(d, x, DY, DR - 8, fill=E.AMB if hl else E.SIL)
    E.circle(d, x, DY, 16, fill=E.SIL_D)
    # notch: a dark slot cut into the rim at angle ang
    pts = []
    for a, r in ((ang - 0.2, DR + 2), (ang - 0.15, DR - NOTCH), (ang + 0.15, DR - NOTCH), (ang + 0.2, DR + 2)):
        pts.append((x + r * math.cos(a), DY + r * math.sin(a)))
    E.poly(d, pts, fill=E.CAV)
    if bad:
        E.cross(d, x, DY + 10, 34)

def bar(E, d, drop=0.0):
    """Locking bar with three teeth that rest on the disc rims (drop up to NOTCH px into aligned notches)."""
    y = DY - DR - 54 + drop
    E.rrect(d, 250, y, 830, y + 30, 8, E.BRA_D)
    E.rrect(d, 254, y + 3, 826, y + 26, 6, E.BRA)
    for x in DX:
        E.rrect(d, x - 14, y + 28, x + 14, y + 54, 4, E.BRA)

def dial(E, d, cx, cy, r, rot):
    E.circle(d, cx, cy, r + 10, fill=E.SIL_D)
    E.circle(d, cx, cy, r, fill=(30, 36, 50))
    for k in range(10):
        a = rot + k * 2 * math.pi / 10
        E.label(d, str(k), cx + (r - 34) * math.cos(a), cy + (r - 34) * math.sin(a), 34, color=E.WHITE)
    E.poly(d, [(cx, cy - r - 30), (cx - 16, cy - r - 58), (cx + 16, cy - r - 58)], fill=E.AMB)
    E.circle(d, cx, cy, 26, fill=E.SIL)

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: the dial is already spinning, then the shackle pops open
        spin = 9.0 * (1 - math.exp(-1.2 * u))
        k = E.back_out((u - L * 0.62) / 0.4) if u > L * 0.62 else 0.0
        shackle(E, d, 90 * k)
        body(E, d)
        dial(E, d, 540, 870, 190, spin)
        if u < L * 0.62:
            for s in range(3):  # motion arcs around the spinning dial
                a0 = spin * 1.0 + s * 2.1
                pts = [(540 + 228 * math.cos(a0 + t * 0.06), 870 + 228 * math.sin(a0 + t * 0.06)) for t in range(12)]
                E.line(d, pts, E.AMB, 7)
        else:
            E.pill(d, "¡ABIERTO!", 540, 1115, 40)
    elif i == 1:  # three stacked discs inside
        shackle(E, d)
        body(E, d, alpha_open=True)
        for j in range(3):
            k = E.back_out((u - j * 0.35) / 0.45)
            if k > 0.02:
                disc(E, d, j, TOP + 1.3 + j * 1.7)
        E.label(d, "3 DISCOS", 540, 1060, 50, color=E.AMB)
    elif i == 2:  # each disc has a notch
        shackle(E, d)
        body(E, d, alpha_open=True)
        for j in range(3):
            a = TOP + 1.3 + j * 1.7
            disc(E, d, j, a)
            if (u * 2.2) % 1 < 0.7:
                nx, ny = DX[j] + (DR + 34) * math.cos(a), DY + (DR + 34) * math.sin(a)
                E.circle(d, DX[j] + (DR - 10) * math.cos(a), DY + (DR - 10) * math.sin(a), 22, outline=E.AMB, w=6)
        E.label(d, "MUESCA", 540, 1060, 50, color=E.AMB)
    elif i == 3:  # turning the dial moves the discs
        shackle(E, d)
        body(E, d, alpha_open=True)
        for j in range(3):
            disc(E, d, j, TOP + 1.3 + j * 1.7 + u * (1.6 - 0.5 * j))
        E.arrow(d, 300, 1065, 780, 1065, color=E.WHITE, w=7)
        E.label(d, "GIRA", 540, 1020, 44, color=E.AMB)
    elif i == 4:  # with the right number each notch comes to its place (one by one)
        shackle(E, d)
        body(E, d, alpha_open=True)
        for j in range(3):
            t0 = j * L / 3.4
            k = E.ease((u - t0) / (L / 4))
            a0 = TOP + 1.3 + j * 1.7 + L * (1.6 - 0.5 * j)
            a0 = a0 - 2 * math.pi * math.floor((a0 - TOP) / (2 * math.pi))
            disc(E, d, j, E.lerp(a0, TOP + 2 * math.pi, k), hl=k >= 1)
        bar(E, d, 0)
        E.label(d, "NÚMERO CORRECTO", 540, 1070, 44, color=E.AMB)
    elif i == 5:  # one disc wrong: its rim holds the bar up
        shackle(E, d)
        body(E, d, alpha_open=True)
        disc(E, d, 0, TOP, hl=True)
        disc(E, d, 1, TOP + 1.9, bad=u > 0.6)
        disc(E, d, 2, TOP, hl=True)
        jig = 6 * abs(math.sin(u * 9)) if u > 0.3 else 0
        bar(E, d, -jig)
        E.label(d, "BLOQUEADO", 540, 1070, 48, color=E.HOT)
    elif i == 6:  # all three aligned: the bar drops and the shackle is released
        k = E.ease((u - 0.3) / 0.6)
        k2 = E.back_out((u - 1.0) / 0.5) if u > 1.0 else 0.0
        shackle(E, d, 90 * k2)
        body(E, d, alpha_open=True)
        for j in range(3):
            disc(E, d, j, TOP, hl=True)
        bar(E, d, NOTCH * k)
        if k2 > 0.3:
            E.pill(d, "¡SE ABRE!", 540, 1070, 46)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 1.2), ("click", s[0] + 1.9), ("pop", s[1] + 0.3), ("pop", s[1] + 0.7), ("pop", s[1] + 1.0),
            ("whoosh", s[3] + 0.2, 1.0), ("click", s[4] + 0.6), ("click", s[4] + 1.2), ("click", s[4] + 1.8),
            ("click", s[5] + 0.5), ("click", s[6] + 0.6), ("pop", s[6] + 1.1)]
