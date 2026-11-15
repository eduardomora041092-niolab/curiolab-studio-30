"""Video 082 — ¿Cómo muele un molinillo de pimienta?
Science: a burr pepper mill has a conical, grooved burr (rotor) that turns inside a fixed, toothed ring (stator).
Turning the top turns a central shaft, which turns the cone; the ring does not move. Peppercorns fall by gravity into
the gap between cone and ring, which is wide at the top and narrow at the bottom. As they move down they are trapped,
sheared and crushed into smaller and smaller pieces until they leave at the bottom. An adjustment nut moves the cone
relative to the ring: a smaller gap gives a finer grind.
(No particle sizes, tooth counts or materials are claimed.)
"""
import math

ID = "082"
TITLE = "¿Cómo muele un molinillo de pimienta?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo convierte un molinillo los granos de pimienta en polvo?",
    "Al girar la tapa, gira un eje central.",
    "El eje mueve una muela cónica con estrías.",
    "La muela gira dentro de un anillo fijo, también dentado.",
    "Los granos caen al hueco, ancho arriba y estrecho abajo.",
    "Al bajar, se parten en trozos cada vez más pequeños.",
    "Si acercas la muela al anillo, el molido sale más fino.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"molinillo", "granos", "pimienta", "polvo", "tapa", "eje", "central", "muela", "cónica", "estrías",
            "anillo", "fijo", "dentado", "hueco", "ancho", "estrecho", "parten", "pequeños", "acercas", "fino"}

CX = 540
Y0, Y1 = 860, 1060          # burr zone
BX0, BX1 = 320, 760         # mill body
CAV = 195                   # cavity half-width
WOOD = (120, 78, 48)
WOOD_D = (84, 52, 30)
PEP = (110, 82, 62)
PEP_H = (175, 145, 115)
POW = (200, 175, 150)


def ring_hw(y):
    t = (y - Y0) / (Y1 - Y0)
    return 160 - 30 * t


def cone_hw(y, dy=0.0):
    t = (y - (Y0 - dy)) / (Y1 - Y0)
    return 50 + 72 * t


def grain(E, d, x, y, r):
    E.circle(d, x, y, r, fill=PEP)
    if r > 5:
        E.circle(d, x - r * 0.3, y - r * 0.3, r * 0.35, fill=PEP_H)


def mill(E, d, phase=0.0, dy=0.0, hl_shaft=False, hl_cone=False, hl_ring=False, chamber=True):
    # body (cut-away)
    E.rrect(d, BX0, 380, BX1, 1080, 40, WOOD)
    E.rrect(d, CX - CAV, 400, CX + CAV, 1062, 20, E.mix(WOOD_D, E.BG1, 0.55))
    # cap + nut
    E.rrect(d, 390, 300, 690, 392, 36, WOOD_D)
    E.circle(d, CX, 285, 30, fill=E.SIL_D)
    for j in range(6):
        x = 410 + ((j * 52 + phase * 60) % 260)
        E.line(d, [(x, 310), (x, 382)], E.mix(WOOD_D, E.BG1, 0.3), 4)
    # peppercorns in the chamber
    if chamber:
        for j in range(46):
            gx = CX - 168 + 336 * ((math.sin(j * 12.9898) * 43758.5453) % 1.0)
            gy = 560 + 270 * ((math.sin(j * 78.233) * 12345.678) % 1.0)
            if abs(gx - CX) < 24:
                continue
            grain(E, d, gx, gy, 13)
    # shaft
    E.rrect(d, CX - 11, 300, CX + 11, Y0 - dy + 6, 5, E.AMB if hl_shaft else E.SIL)
    # fixed ring (both halves of the cross-section) with inner teeth
    rc = E.AMB if hl_ring else E.SIL_D
    for s in (-1, 1):
        E.poly(d, [(CX + s * CAV, Y0), (CX + s * ring_hw(Y0), Y0), (CX + s * ring_hw(Y1), Y1), (CX + s * CAV, Y1)],
               fill=rc)
        for j in range(8):
            y = Y0 + 10 + j * 24
            x = CX + s * ring_hw(y)
            E.poly(d, [(x, y), (x - s * 14, y + 10), (x, y + 20)], fill=rc)
    # conical burr (rotor) with moving grooves
    cc = E.AMB if hl_cone else E.SIL
    top, bot = Y0 - dy, Y1 - dy
    E.poly(d, [(CX - 50, top), (CX + 50, top), (CX + 122, bot), (CX - 122, bot)], fill=cc)
    gcol = E.mix(cc, E.BG1, 0.45)
    for k in range(12):
        f = -1.0 + ((k / 6.0 + phase) % 2.0)
        fb = f + 0.25
        if fb > 1.0:
            continue
        E.line(d, [(CX + 50 * f, top + 4), (CX + 122 * fb, bot - 4)], gcol, 5)
    E.circle(d, CX, top, 12, fill=E.SIL_D)


def gap_grains(E, d, u, n=5, dy=0.0, speed=0.45):
    for s in (-1, 1):
        for j in range(n):
            q = (u * speed + j / n + (0.1 if s > 0 else 0)) % 1.0
            y = Y0 - 30 + q * (Y1 - Y0 + 10)
            yy = min(max(y, Y0), Y1)
            gap = ring_hw(yy) - cone_hw(yy, dy)
            r = max(3.0, min(13.0, gap / 2 - 2))
            x = CX + s * (ring_hw(yy) + cone_hw(yy, dy)) / 2
            grain(E, d, x, y, r)


def powder(E, d, u, dense=1.0):
    for j in range(int(26 * dense)):
        q = (u * 0.9 + j * 0.137) % 1.0
        x = CX + (-1 if j % 2 else 1) * (40 + (j * 23) % 80)
        y = 1068 + q * 105
        E.circle(d, x, y, 4, fill=POW)


def spin_arrow(E, d):
    E.arrow(d, 640, 270, 440, 270, E.AMB, 7, 26)


def scene(i, u, L, E, im, d):
    ph = u * 0.6
    if i == 0:  # in action from frame 0: cap turning, grains being ground, powder falling
        mill(E, d, phase=ph)
        gap_grains(E, d, u + 0.3)
        powder(E, d, u)
        spin_arrow(E, d)
    elif i == 1:  # turning the cap turns the central shaft
        mill(E, d, phase=ph, hl_shaft=True)
        spin_arrow(E, d)
        E.label(d, "GIRAS", 850, 300, 46, color=E.AMB)
        E.label(d, "EJE", 190, 520, 48, color=E.AMB)
        E.arrow(d, 240, 520, 515, 520, E.AMB, 5, 20)
    elif i == 2:  # the shaft turns a conical, grooved burr
        mill(E, d, phase=ph, hl_cone=True)
        E.label(d, "MUELA", 900, 900, 44, color=E.AMB)
        E.label(d, "CÓNICA", 900, 950, 44, color=E.AMB)
        E.arrow(d, 840, 980, 650, 1000, E.AMB, 5, 20)
        E.arrow(d, 600, 1110, 480, 1110, E.WHITE, 5, 20)
        E.label(d, "GIRA", 680, 1120, 38, color=E.WHITE)
    elif i == 3:  # it turns inside a fixed toothed ring
        mill(E, d, phase=ph, hl_ring=True)
        E.label(d, "ANILLO", 170, 900, 44, color=E.AMB)
        E.label(d, "FIJO", 170, 950, 44, color=E.AMB)
        E.arrow(d, 210, 990, 355, 1000, E.AMB, 5, 20)
        E.label(d, "NO GIRA", 900, 900, 40, color=E.WHITE)
        E.arrow(d, 880, 930, 725, 990, E.WHITE, 5, 20)
    elif i == 4:  # grains fall into the gap, wide at the top, narrow at the bottom
        mill(E, d, phase=ph)
        gap_grains(E, d, u)
        E.label(d, "ANCHO", 150, Y0 + 5, 42, color=E.AMB)
        E.arrow(d, 230, Y0 + 5, 405, Y0 + 5, E.AMB, 5, 20)
        E.label(d, "ESTRECHO", 900, Y1 - 10, 40, color=E.AMB)
        E.arrow(d, 805, Y1 - 10, 680, Y1 - 10, E.AMB, 5, 20)
    elif i == 5:  # going down, they break into smaller and smaller pieces
        mill(E, d, phase=ph)
        gap_grains(E, d, u, n=7, speed=0.6)
        powder(E, d, u, 1.4)
        E.label(d, "SE PARTEN", 900, 940, 42, color=E.AMB)
        E.label(d, "POLVO", 860, 1140, 42, color=E.WHITE)
    elif i == 6:  # bringing the cone closer to the ring: finer grind
        dy = 22 * E.ease(u / (L * 0.8))
        mill(E, d, phase=ph, dy=dy, hl_cone=True)
        gap_grains(E, d, u, n=6, dy=dy)
        powder(E, d, u, 1.4)
        E.arrow(d, 300, 1050, 300, 900, E.AMB, 7, 24)
        E.label(d, "ACERCAS", 160, 820, 40, color=E.AMB)
        E.label(d, "MÁS FINO", 900, 1140, 42, color=E.AMB)
        E.label(d, "HUECO MENOR", 900, 820, 38, color=E.WHITE)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("zip", s[0] + 0.2), ("whoosh", s[1] + 0.4, 0.8), ("click", s[2] + 0.6), ("pop", s[3] + 0.6),
            ("zip", s[4] + 0.5), ("whoosh", s[5] + 0.5, 0.8), ("pop", s[6] + 0.8)]
