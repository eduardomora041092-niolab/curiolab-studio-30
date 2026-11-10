"""Video 068 — ¿Cómo funciona un abrelatas?
Science: a common manual can opener has two wheels that clamp the rim of the can. One is a sharp circular cutting
wheel (blade) that sits on top of the lid, just inside the rim; the other is a toothed (serrated) feed wheel that grips
the rim from the side/underneath. Squeezing the two handles together works as a lever: a small force on the long
handles becomes a large force at the short distance where the blade meets the lid, so the blade pierces the thin metal.
Turning the key rotates the toothed wheel, which drags the rim along and makes the can turn; as the can turns, the
blade rolls around the lid and cuts a continuous circle until the lid comes free.
(No forces in newtons, metal thicknesses or lever ratios are claimed; side-cutting openers are not covered.)
"""
import math

ID = "068"
TITLE = "¿Cómo funciona un abrelatas?"
SUBTITLE = "CÓMO FUNCIONA"
LINES = [
    "¿Cómo corta el metal un abrelatas sin esfuerzo?",
    "Tiene dos ruedas: una cuchilla circular y una rueda dentada.",
    "Al cerrar los mangos, actúan como palanca y aprietan la cuchilla contra la tapa.",
    "La cuchilla, muy afilada, perfora el metal fino de la tapa.",
    "La rueda dentada muerde el borde de la lata por el costado.",
    "Al girar la llave, esa rueda arrastra el borde y hace girar la lata.",
    "La cuchilla rueda por todo el borde y corta un círculo completo.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"corta", "metal", "abrelatas", "esfuerzo", "ruedas", "cuchilla", "circular", "dentada", "mangos",
            "palanca", "aprietan", "tapa", "afilada", "perfora", "fino", "muerde", "borde", "lata", "girar", "llave",
            "arrastra", "rueda", "círculo", "completo"}

CAN = (180, 190, 205)
CAN_D = (120, 130, 148)
LID = (210, 216, 226)
CUT = (255, 210, 90)

# top view of the can (ellipse-ish circle), opener at the right rim
CX, CY, R = 470, 730, 300


def can_top(E, d, cut=0.0, rot=0.0):
    E.circle(d, CX, CY, R + 18, fill=CAN_D)
    E.circle(d, CX, CY, R, fill=LID, outline=CAN, w=6)
    for k in range(3):  # lid rings, rotate with the can to show it turning
        E.circle(d, CX, CY, R - 60 - 50 * k, outline=E.mix(LID, CAN_D, 0.4), w=3)
    for k in range(6):
        a = rot + k * math.pi / 3
        E.circle(d, CX + (R - 30) * math.cos(a), CY + (R - 30) * math.sin(a), 6, fill=CAN_D)
    if cut > 0:
        n = max(2, int(60 * cut))
        pts = [(CX + (R - 14) * math.cos(-a / 60 * 2 * math.pi), CY + (R - 14) * math.sin(-a / 60 * 2 * math.pi))
               for a in range(n + 1)]
        E.line(d, pts, CUT, 7)


def gear(E, d, x, y, r, rot, color):
    pts = []
    for k in range(24):
        a = rot + k * math.pi / 12
        rr = r if k % 2 == 0 else r - 14
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    E.poly(d, pts, fill=color, outline=E.SIL_H, w=2)
    E.circle(d, x, y, 10, fill=E.BG1)


def blade(E, d, x, y, r, rot):
    E.circle(d, x, y, r, fill=E.SIL, outline=E.WHITE, w=4)
    for k in range(4):
        a = rot + k * math.pi / 2
        E.line(d, [(x, y), (x + (r - 10) * math.cos(a), y + (r - 10) * math.sin(a))], E.SIL_D, 4)
    E.circle(d, x, y, 10, fill=E.BG1)


def side_view(E, d, squeeze=0.0, pierce=0.0):
    # side cross-section of the rim: can wall + lid, blade above inside rim, gear outside rim
    E.rrect(d, 200, 700, 700, 1150, 0, CAN_D)
    E.rrect(d, 200, 690, 700, 715, 4, LID)
    E.rrect(d, 680, 650, 720, 720, 6, CAN)          # rim lip
    by = 560 + 120 * pierce
    blade(E, d, 620, by, 70, 0)
    gear(E, d, 800, 690, 60, 0, E.BRA)
    # handles (lever) pivoting near the wheels
    o = 140 * (1 - squeeze)
    E.line(d, [(720, 580), (980, 300 - o * 0.3)], E.SIL_D, 26)
    E.line(d, [(760, 760), (1000, 380 + o)], E.SIL_D, 26)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: can turning, blade already cutting
        cut = 0.25 + 0.6 * min(1.0, u / L)
        can_top(E, d, cut=cut, rot=-u * 1.5)
        blade(E, d, CX + R - 14, CY, 46, u * 6)
        gear(E, d, CX + R + 70, CY, 50, -u * 4, E.BRA)
        E.label(d, "CORTA", 860, 380, 52, color=CUT)
    elif i == 1:  # two wheels
        k = E.ease(u / 0.7)
        blade(E, d, 330, 640, 140 * k + 1, u)
        gear(E, d, 760, 640, 140 * k + 1, -u, E.BRA)
        E.label(d, "CUCHILLA", 330, 880, 48, color=E.SIL_H)
        E.label(d, "RUEDA DENTADA", 760, 880, 48, color=E.BRA)
    elif i == 2:  # handles = lever, push blade onto lid
        k = E.ease(u / (L * 0.6))
        side_view(E, d, squeeze=k, pierce=0.3 * k)
        E.arrow(d, 1000, 250, 960, 330, E.AMB, 7, 24)
        E.arrow(d, 1010, 560, 990, 470, E.AMB, 7, 24)
        E.label(d, "PALANCA", 860, 1040, 48, color=E.AMB)
        E.arrow(d, 620, 380, 620, 470, E.HOT, 7, 24)
    elif i == 3:  # sharp blade pierces thin lid
        k = E.ease(u / (L * 0.5))
        side_view(E, d, squeeze=1.0, pierce=0.3 + 0.7 * k)
        if k > 0.9:
            E.circle(d, 620, 700, 30 + 8 * abs(math.sin(u * 6)), outline=CUT, w=5)
        E.label(d, "PERFORA LA TAPA", 450, 340, 48, color=CUT)
    elif i == 4:  # toothed wheel bites the rim from the side
        side_view(E, d, squeeze=1.0, pierce=1.0)
        p = abs(math.sin(u * 4))
        E.circle(d, 735, 690, 40 + 8 * p, outline=E.AMB, w=5)
        E.label(d, "MUERDE EL BORDE", 540, 340, 48, color=E.BRA)
        E.arrow(d, 860, 400, 790, 620, E.BRA, 6, 22)
    elif i == 5:  # key turns gear, gear drags the can round
        can_top(E, d, cut=0.15, rot=-u * 1.5)
        blade(E, d, CX + R - 14, CY, 46, u * 6)
        gear(E, d, CX + R + 70, CY, 50, -u * 4, E.BRA)
        # key handle on the gear
        a = -u * 4
        E.line(d, [(CX + R + 70, CY), (CX + R + 70 + 150 * math.cos(a), CY + 150 * math.sin(a))], E.SIL_D, 22)
        E.circle(d, CX + R + 70 + 150 * math.cos(a), CY + 150 * math.sin(a), 26, fill=E.SIL)
        E.label(d, "LLAVE", 900, 1080, 46, color=E.SIL_H)
        for k in range(3):
            b = -u * 1.5 + math.pi * 0.6 + k * 0.3
            E.arrow(d, CX + (R + 60) * math.cos(b), CY + (R + 60) * math.sin(b),
                    CX + (R + 60) * math.cos(b - 0.25), CY + (R + 60) * math.sin(b - 0.25), E.AMB, 6, 20)
        E.label(d, "GIRA LA LATA", 470, 330, 48, color=E.AMB)
    elif i == 6:  # full circle cut
        cut = min(1.0, 0.2 + 0.8 * u / (L * 0.8))
        can_top(E, d, cut=cut, rot=-u * 1.5)
        blade(E, d, CX + R - 14, CY, 46, u * 6)
        gear(E, d, CX + R + 70, CY, 50, -u * 4, E.BRA)
        E.label(d, "CÍRCULO COMPLETO", 540, 330, 50, color=CUT)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("zip", s[0] + 0.2), ("pop", s[1] + 0.6), ("click", s[2] + 0.8), ("pop", s[3] + 0.7),
            ("click", s[4] + 0.6), ("whoosh", s[5] + 0.5, 0.8), ("zip", s[6] + 0.5)]
