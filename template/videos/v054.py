"""Video 054 — ¿Por qué erupciona un volcán?
Science: beneath many volcanoes there is a magma chamber: molten rock that has accumulated underground. Magma is less
dense than the solid rock around it, so it tends to rise. It carries dissolved gases (mainly water vapour, also carbon
dioxide) under high pressure. As it rises the pressure drops and the gases come out of solution as bubbles. The
bubbles grow and push the magma upwards; if the rock above gives way, magma reaches the surface: an eruption.
(No temperatures, depths, gas percentages or eruption types are claimed.)
"""
import math

ID = "054"
TITLE = "¿Por qué erupciona un volcán?"
SUBTITLE = "CIENCIA EN 30 SEGUNDOS"
LINES = [
    "¿Qué hace que un volcán entre en erupción?",
    "Bajo el volcán hay una cámara con magma: roca fundida.",
    "El magma es menos denso que la roca y tiende a subir.",
    "Lleva gases disueltos, como vapor de agua, a mucha presión.",
    "Al subir, la presión baja y los gases forman burbujas.",
    "Las burbujas crecen y empujan el magma hacia arriba.",
    "Si la roca de encima cede, el magma sale: es la erupción.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"volcán", "erupción", "cámara", "magma", "roca", "fundida", "denso", "subir", "gases", "disueltos",
            "vapor", "presión", "burbujas", "crecen", "empujan", "cede"}

ROCK = (92, 70, 58)
ROCK_D = (64, 48, 40)
ROCK_L = (122, 96, 78)
MAGMA = (238, 96, 40)
MAGMA_L = (255, 170, 60)
ASH = (120, 124, 134)
CX = 540
CRATER_Y = 620
CH_Y, CH_RX, CH_RY = 1050, 230, 75


def volcano(E, d, level=1.0, plug=False):
    """Cross-section: cone, ground, magma chamber and conduit filled up to `level` (0 chamber .. 1 crater)."""
    E.poly(d, [(40, 1190), (CX - 90, CRATER_Y), (CX + 90, CRATER_Y), (1040, 1190)], fill=ROCK, outline=ROCK_D, w=4)
    for k, y in enumerate((760, 900, 1040)):
        E.line(d, [(60 + k * 10, y + 90), (1020 - k * 10, y + 90)], ROCK_D, 3)
    E.rrect(d, CX - CH_RX, CH_Y - CH_RY, CX + CH_RX, CH_Y + CH_RY, CH_RY, MAGMA, outline=ROCK_D, w=5)
    top = CH_Y - CH_RY - (CH_Y - CH_RY - CRATER_Y) * level
    E.rrect(d, CX - 34, CRATER_Y, CX + 34, CH_Y - CH_RY + 10, 6, ROCK_D)       # conduit (empty)
    E.rrect(d, CX - 30, top, CX + 30, CH_Y - CH_RY + 20, 6, MAGMA)              # magma in conduit
    if plug:
        E.rrect(d, CX - 40, CRATER_Y - 6, CX + 40, CRATER_Y + 40, 8, ROCK_L, outline=ROCK_D, w=3)
    return top


def bubbles(E, d, u, top, grow=1.0, n=7, speed=1.0):
    span = CH_Y - CH_RY - top
    for j in range(n):
        f = (u * 0.35 * speed + j / n) % 1
        y = CH_Y - CH_RY - span * f
        r = 4 + 14 * f * grow
        x = CX + 12 * math.sin(j * 2.1 + u * 3)
        E.circle(d, x, y, r, fill=MAGMA_L, outline=E.WHITE, w=2)


def dissolved(E, d, u, n=18):
    for j in range(n):
        x = CX - CH_RX + 50 + ((j * 97) % (2 * CH_RX - 100)) + 6 * math.sin(u * 3 + j)
        y = CH_Y - 40 + ((j * 53) % 80) + 4 * math.cos(u * 3 + j)
        E.circle(d, x, y, 5, fill=E.WHITE)


def eruption(E, d, u, k=1.0):
    for j in range(14):
        f = (u * 0.45 + j / 14) % 1
        x = CX + (j % 5 - 2) * 46 * f + 20 * math.sin(j + u)
        y = CRATER_Y - 20 - 200 * f
        E.circle(d, x, y, (26 + 34 * f) * k, fill=E.mix(ASH, E.BG2, f * 0.6))
    for j in range(8):
        f = (u * 0.9 + j / 8) % 1
        sx = (j - 3.5) * 60
        x = CX + sx * f
        y = CRATER_Y - 10 - 200 * k * (f * (1.6 - f))
        E.circle(d, x, y, 12, fill=MAGMA_L)
    for sgn in (-1, 1):  # lava running down both flanks
        x0 = CX + sgn * 94
        E.line(d, [(x0, CRATER_Y + 4), (x0 + sgn * 137 * k, CRATER_Y + 4 + 190 * k)], MAGMA, 22)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: erupting
        volcano(E, d, 1.0)
        bubbles(E, d, u, CRATER_Y, grow=1.2, speed=2)
        eruption(E, d, u)
    elif i == 1:  # magma chamber
        volcano(E, d, 0.0)
        E.label(d, "MAGMA", CX, CH_Y, 50, color=E.WHITE)
        E.pill(d, "ROCA FUNDIDA", CX, 420, 42)
        E.line(d, [(CX, 460), (CX, 610)], E.AMB, 4)
    elif i == 2:  # less dense -> rises
        k = E.ease(min(1, u / (L * 0.9)))
        top = volcano(E, d, 0.15 + 0.4 * k)
        for j in range(3):
            f = (u * 0.6 + j / 3) % 1
            E.arrow(d, CX + 90, CH_Y - 120 - 260 * f + 60, CX + 90, CH_Y - 120 - 260 * f, E.AMB, 6, 20)
        E.pill(d, "MENOS DENSO", CX, 420, 42)
        E.label(d, "SUBE", CX + 190, 780, 46, color=E.AMB)
    elif i == 3:  # dissolved gas under pressure
        volcano(E, d, 0.25)
        dissolved(E, d, u)
        E.pill(d, "GASES DISUELTOS", CX, 420, 42)
        E.label(d, "PRESIÓN", CX + 200, 930, 44, color=E.WHITE)
    elif i == 4:  # pressure drops while rising -> bubbles form
        top = volcano(E, d, 0.6)
        bubbles(E, d, u, top, grow=0.8, n=6)
        E.pill(d, "MENOS PRESIÓN", CX, 420, 42)
        E.label(d, "BURBUJAS", CX + 200, 760, 44, color=E.AMB)
    elif i == 5:  # bubbles grow and push magma up
        k = E.ease(min(1, u / (L * 0.9)))
        top = volcano(E, d, 0.6 + 0.4 * k, plug=True)
        bubbles(E, d, u, top, grow=1.4, n=7, speed=1.6)
        E.arrow(d, CX + 110, 860, CX + 110, 660, E.AMB, 10, 32)
        E.pill(d, "EMPUJAN", CX, 420, 42)
    elif i == 6:  # rock gives way: eruption
        k = E.ease(min(1, u / (L * 0.4)))
        volcano(E, d, 1.0)
        bubbles(E, d, u, CRATER_Y, grow=1.2, speed=2)
        eruption(E, d, u, k=max(0.2, k))
        E.pill(d, "ERUPCIÓN", 210, 440, 44)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 1.4), ("pop", s[1] + 0.6), ("zip", s[2] + 0.4, 1.0), ("pop", s[3] + 0.6),
            ("pop", s[4] + 1.0), ("whoosh", s[5] + 0.3, 1.0), ("whoosh", s[6] + 0.8, 1.4)]
