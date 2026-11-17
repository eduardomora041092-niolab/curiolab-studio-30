"""Video 088 — ¿Cómo funciona una tecla de teclado mecánico?
Science: in a mechanical keyboard every key sits on its own independent switch. Inside the switch there is a plastic
stem, a spring underneath it and two thin metal contact leaves. At rest the stem holds the moving leaf away from the
fixed one, so the circuit is open and no current flows. Pressing the key pushes the stem down, compressing the spring,
and releases the leaf, which touches the other one: the circuit closes and the keyboard registers that key. On release
the spring pushes the stem back up, the leaves separate and the circuit opens again.
(No actuation forces, travel distances or lifetimes are claimed.)
"""
import math

ID = "088"
TITLE = "¿Cómo funciona una tecla de teclado mecánico?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo sabe el ordenador qué tecla has pulsado?",
    "En un teclado mecánico, cada tecla tiene su propio interruptor.",
    "Dentro hay una pieza que baja, un muelle y dos láminas metálicas.",
    "En reposo, la pieza mantiene las láminas separadas y no pasa corriente.",
    "Al pulsar, la pieza baja, aprieta el muelle y las láminas se tocan.",
    "El circuito se cierra y el teclado recibe la señal de esa tecla.",
    "Al soltar, el muelle la sube y el circuito se abre.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"ordenador", "tecla", "pulsado", "teclado", "mecánico", "interruptor", "pieza", "baja", "muelle",
            "láminas", "metálicas", "reposo", "separadas", "corriente", "pulsar", "aprieta", "tocan", "circuito",
            "cierra", "señal", "soltar", "sube", "abre"}

CX = 540
TRAVEL = 120
KEYC = (60, 72, 100)
STEM = (200, 70, 70)
COPPER = (222, 150, 80)
HX0, HX1, HY0, HY1 = 380, 700, 600, 1000


def closed_of(off):
    return max(0.0, min(1.0, (off - 50) / 45.0))


def switch(E, d, off, hl_stem=False, hl_spring=False, hl_leaf=False, hl_wire=False, letter=True):
    c = closed_of(off)
    # housing
    E.rrect(d, HX0 - 14, HY0 - 14, HX1 + 14, HY1 + 14, 26, E.SIL_D)
    E.rrect(d, HX0, HY0, HX1, HY1, 18, E.CAV)
    # spring (zig-zag from stem bottom to housing floor)
    top, bot = 770 + off, HY1 - 16
    n = 9
    pts = [(CX, top)]
    for k in range(1, n):
        y = top + (bot - top) * k / n
        pts.append((CX + (34 if k % 2 else -34), y))
    pts.append((CX, bot))
    E.line(d, pts, E.AMB if hl_spring else E.SIL, 8)
    # stem with side tab that holds the moving leaf open
    sc = E.AMB if hl_stem else STEM
    E.rrect(d, 500, 540 + off, 580, 770 + off, 10, sc)
    E.rrect(d, 578, 690 + off, 606, 722 + off, 6, sc)
    # contact leaves
    lc = E.AMB if hl_leaf else COPPER
    E.line(d, [(650, HY1 - 10), (650, 720)], lc, 9)
    tx = 608 + (642 - 608) * c
    E.line(d, [(620, HY1 - 10), (620, 860), (tx, 728)], lc, 9)
    if c >= 1.0:
        E.circle(d, 646, 728, 16, fill=E.AMB)
    # wires to the keyboard chip
    wc = (E.AMB if c >= 1.0 else E.SIL_D) if not hl_wire else E.AMB
    E.line(d, [(650, HY1), (650, 1080), (880, 1080), (880, 960)], wc, 7)
    E.line(d, [(620, HY1), (620, 1120), (950, 1120), (950, 960)], wc, 7)
    E.rrect(d, 820, 850, 1010, 960, 16, (40, 60, 52) if c < 1.0 else (40, 120, 80))
    if letter and c >= 1.0:
        E.label(d, "A", 915, 905, 64, color=E.WHITE)
    # key cap on top (drawn last)
    E.rrect(d, 360, 440 + off, 720, 545 + off, 26, KEYC)
    E.rrect(d, 380, 452 + off, 700, 520 + off, 20, (80, 95, 128))


def press(u, rate=1.4):
    s = math.sin(2 * math.pi * u * rate)
    return TRAVEL * max(0.0, s) ** 0.6


def keyrow(E, d, hl=2):
    for k in range(5):
        x0 = 150 + k * 160
        col = E.AMB if k == hl else KEYC
        E.rrect(d, x0, 300, x0 + 140, 400, 16, col)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: the key is being pressed and the letter appears
        switch(E, d, press(u + 0.18))
        E.arrow(d, 250, 330, 250, 470, E.WHITE, 6, 24)
    elif i == 1:  # every key has its own switch
        keyrow(E, d)
        switch(E, d, 0)
        E.line(d, [(CX, 405), (CX, 432)], E.AMB, 6)
        E.label(d, "INTERRUPTOR", 200, 760, 40, color=E.AMB)
        E.arrow(d, 220, 795, 370, 820, E.AMB, 5, 20)
    elif i == 2:  # stem, spring, two metal leaves
        off = press(u, 0.6) * 0.3
        switch(E, d, off, hl_stem=True, hl_spring=True, hl_leaf=True)
        E.label(d, "PIEZA", 200, 640, 44, color=E.AMB)
        E.arrow(d, 260, 670, 490, 690, E.AMB, 5, 20)
        E.label(d, "MUELLE", 200, 900, 44, color=E.AMB)
        E.arrow(d, 260, 900, 495, 900, E.AMB, 5, 20)
        E.label(d, "LÁMINAS", 880, 640, 44, color=E.AMB)
        E.arrow(d, 860, 670, 665, 760, E.AMB, 5, 20)
    elif i == 3:  # at rest the leaves are held apart: no current
        switch(E, d, 0, hl_leaf=True)
        E.label(d, "SEPARADAS", 880, 640, 42, color=E.AMB)
        E.arrow(d, 860, 670, 640, 728, E.AMB, 5, 20)
        E.cross(d, 760, 1100, 34)
        E.label(d, "SIN CORRIENTE", 230, 1060, 40, color=E.HOT)
    elif i == 4:  # pressing: stem goes down, spring squeezes, leaves touch
        off = TRAVEL * min(1.0, u / max(0.8, L * 0.6))
        switch(E, d, off, hl_stem=True, hl_spring=True)
        E.arrow(d, 250, 330, 250, 520, E.WHITE, 7, 26)
        E.label(d, "PULSAS", 250, 300, 42, color=E.WHITE)
        if closed_of(off) >= 1.0:
            E.label(d, "SE TOCAN", 880, 640, 42, color=E.AMB)
    elif i == 5:  # circuit closes, chip gets the key signal
        switch(E, d, TRAVEL, hl_wire=True)
        q = (u * 0.6) % 1.0
        x = 650 + (880 - 650) * q
        E.circle(d, x, 1080, 12, fill=E.WHITE)
        E.label(d, "CIRCUITO CERRADO", 540, 330, 46, color=E.AMB)
        E.label(d, "SEÑAL", 915, 800, 42, color=E.WHITE)
    elif i == 6:  # release: spring pushes it up, circuit opens
        off = TRAVEL * (1.0 - min(1.0, u / max(0.8, L * 0.6)))
        switch(E, d, off, hl_spring=True)
        E.arrow(d, 250, 520, 250, 330, E.WHITE, 7, 26)
        E.label(d, "SUELTAS", 250, 560, 40, color=E.WHITE)
        if closed_of(off) < 1.0:
            E.label(d, "CIRCUITO ABIERTO", 540, 330, 44, color=E.COLD)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("click", s[0] + 0.3), ("pop", s[1] + 0.5), ("whoosh", s[2] + 0.4, 0.8), ("pop", s[3] + 0.6),
            ("click", s[4] + 0.8), ("zip", s[5] + 0.4), ("click", s[6] + 0.6)]
