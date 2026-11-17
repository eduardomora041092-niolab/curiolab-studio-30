"""Video 089 — ¿Cómo se ajusta una llave inglesa?
Science: an adjustable wrench has a fixed jaw that is part of the handle and a movable jaw that slides in a channel in
the head. The underside of the movable jaw carries a row of teeth (a rack). A worm screw (a small knurled wheel with a
helical thread) sits in the head and meshes with that rack. Turning the worm with the thumb makes its thread push the
teeth, so the movable jaw slides and the opening widens or narrows to fit the nut. The thread of the worm does not let
the jaw push it back, so the jaw does not open by itself under load.
(No dimensions, head angles, inventors or dates are claimed.)
"""
import math

ID = "089"
TITLE = "¿Cómo se ajusta una llave inglesa?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo puede una sola llave agarrar tuercas de muchos tamaños?",
    "Tiene una mandíbula fija y otra que se desliza.",
    "Bajo la mandíbula móvil hay una fila de dientes.",
    "Esos dientes encajan en un tornillo sin fin: una ruedita con rosca.",
    "Al girarlo con el pulgar, su rosca empuja los dientes.",
    "La mandíbula se mueve y la abertura se agranda o se achica.",
    "Así encaja justo en la tuerca, y la rosca impide que se abra sola.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"llave", "tuercas", "tamaños", "mandíbula", "fija", "desliza", "móvil", "dientes", "encajan",
            "tornillo sin fin", "rosca", "girarlo", "pulgar", "empuja", "abertura", "agranda", "achica", "tuerca",
            "abra sola"}

STEEL = (150, 160, 175)
STEEL_D = (95, 105, 120)
FX = 430          # inner face of the fixed jaw
JT, JB = 380, 560  # jaw top/bottom
RACK_Y = 580
WORM_X0, WORM_X1, WORM_Y0, WORM_Y1 = 560, 720, 612, 690


def wrench(E, d, gap, phase=0.0, hl_fixed=False, hl_move=False, hl_rack=False, hl_worm=False, nut=None):
    # handle
    E.rrect(d, 470, 690, 610, 1160, 40, STEEL_D)
    E.rrect(d, 490, 710, 590, 1140, 30, STEEL)
    # head with channel
    E.rrect(d, 300, 560, 910, 710, 30, STEEL_D)
    E.rrect(d, 330, 572, 890, 700, 14, E.CAV)
    # fixed jaw
    E.rrect(d, 300, JT, FX, 600, 18, E.AMB if hl_fixed else STEEL)
    # movable jaw + rack under it
    mx = FX + gap
    mc = E.AMB if hl_move else STEEL
    E.rrect(d, mx, JT + 20, mx + 120, JB + 10, 18, mc)
    rc = E.AMB if hl_rack else (200, 205, 215)
    E.rrect(d, mx + 10, RACK_Y - 14, mx + 200, RACK_Y + 8, 4, rc)
    k = 0
    while True:
        tx = mx + 20 + k * 26
        if tx > mx + 180:
            break
        E.poly(d, [(tx, RACK_Y + 8), (tx + 18, RACK_Y + 8), (tx + 9, RACK_Y + 26)], fill=rc)
        k += 1
    # worm screw (threads slide sideways as it turns)
    wc = E.AMB if hl_worm else (190, 175, 140)
    E.rrect(d, WORM_X0, WORM_Y0, WORM_X1, WORM_Y1, 20, wc)
    for j in range(-1, 8):
        x = WORM_X0 + ((j * 24 + phase * 24) % 192) - 10
        if WORM_X0 + 6 < x < WORM_X1 - 22:
            E.line(d, [(x, WORM_Y0 + 4), (x + 16, WORM_Y1 - 4)], (90, 80, 60), 6)
    E.line(d, [(WORM_X0 - 20, (WORM_Y0 + WORM_Y1) / 2), (WORM_X1 + 20, (WORM_Y0 + WORM_Y1) / 2)], E.SIL_D, 6)
    if nut:
        cx, size = nut
        r = size / 2
        pts = [(cx + r * math.cos(math.pi / 3 * k), 470 + r * math.sin(math.pi / 3 * k)) for k in range(6)]
        E.poly(d, pts, fill=(120, 130, 150))
        E.circle(d, cx, 470, r * 0.45, fill=E.CAV)


def osc(u, a, b, rate=0.35):
    return a + (b - a) * (0.5 - 0.5 * math.cos(2 * math.pi * u * rate))


def turn_arrow(E, d, up=True):
    y = 760
    if up:
        E.arrow(d, 600, y, 700, y, E.WHITE, 6, 22)
    else:
        E.arrow(d, 700, y, 600, y, E.WHITE, 6, 22)
    E.label(d, "GIRA", 650, 820, 40, color=E.WHITE)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: worm turning, jaw sliding open and closed
        g = osc(u + 0.6, 90, 240)
        wrench(E, d, g, phase=g / 26.0)
        E.arrow(d, FX + 20, 330, FX + g - 20, 330, E.WHITE, 5, 20)
        E.arrow(d, FX + g - 20, 330, FX + 20, 330, E.WHITE, 5, 20)
    elif i == 1:  # one fixed jaw, one sliding jaw
        g = osc(u, 120, 220)
        wrench(E, d, g, phase=g / 26.0, hl_fixed=True, hl_move=True)
        E.label(d, "FIJA", 365, 320, 44, color=E.AMB)
        E.label(d, "MÓVIL", FX + g + 60, 330, 44, color=E.AMB)
    elif i == 2:  # row of teeth under the movable jaw
        wrench(E, d, 170, hl_rack=True)
        E.label(d, "DIENTES", 880, 470, 44, color=E.AMB)
        E.arrow(d, 860, 500, 740, 570, E.AMB, 5, 20)
    elif i == 3:  # teeth mesh with a worm screw
        wrench(E, d, 170, phase=u * 2, hl_worm=True, hl_rack=True)
        E.label(d, "TORNILLO SIN FIN", 640, 880, 44, color=E.AMB)
        E.arrow(d, 640, 845, 640, 705, E.AMB, 5, 20)
    elif i == 4:  # turning it with the thumb, the thread pushes the teeth
        g = 120 + min(1.0, u / max(1.0, L * 0.8)) * 110
        wrench(E, d, g, phase=g / 26.0, hl_worm=True)
        turn_arrow(E, d)
        E.circle(d, 650, 960, 48, fill=(214, 168, 140))
        E.label(d, "PULGAR", 650, 1060, 38, color=(214, 168, 140))
        E.arrow(d, FX + g + 130, 470, FX + g + 220, 470, E.AMB, 6, 22)
    elif i == 5:  # the opening widens or narrows
        g = osc(u, 90, 250, 0.4)
        wrench(E, d, g, phase=g / 26.0, hl_move=True)
        E.line(d, [(FX, 330), (FX + g, 330)], E.AMB, 6)
        E.line(d, [(FX, 310), (FX, 350)], E.AMB, 6)
        E.line(d, [(FX + g, 310), (FX + g, 350)], E.AMB, 6)
        E.label(d, "ABERTURA", FX + g / 2, 290, 40, color=E.AMB)
    elif i == 6:  # it fits the nut exactly and does not open by itself
        size = 150
        g = max(size, 240 - min(1.0, u / max(1.0, L * 0.5)) * 90)
        wrench(E, d, g, phase=g / 26.0, nut=(FX + g / 2, size + 6))
        if g <= size + 1:
            E.label(d, "AJUSTADA", 560, 300, 46, color=E.AMB)
            E.label(d, "NO SE ABRE SOLA", 560, 900, 40, color=E.WHITE)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("zip", s[0] + 0.3), ("click", s[1] + 0.5), ("pop", s[2] + 0.5), ("click", s[3] + 0.6),
            ("zip", s[4] + 0.5), ("whoosh", s[5] + 0.4, 0.8), ("click", s[6] + 0.8)]
