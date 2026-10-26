"""Video 023 — ¿Por qué el cinturón se bloquea en un frenazo?
Mechanism: the seat-belt webbing is wound on a spool inside the retractor; a coiled spring turns the spool to keep
the belt wound in. Pulled slowly, the spool turns freely and the belt comes out. The spool carries a toothed
ratchet wheel, and next to it sits a pawl (trinquete). In a sudden stop a small pendulum (or weighted sensor) keeps
moving forward by inertia, swings, and pushes the pawl into the ratchet teeth, so the spool cannot turn and the
belt locks. Most retractors also have a second sensor that locks the spool when the belt itself is pulled out
sharply.
(Schematic side view; no forces, decelerations or thresholds are claimed.)
"""
import math

ID = "023"
TITLE = "¿Por qué el cinturón se bloquea en un frenazo?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Por qué el cinturón se traba si tiras rápido?",
    "La cinta se enrolla en un carrete con un muelle.",
    "Si tiras despacio, el carrete gira y la cinta sale.",
    "Junto al carrete hay una rueda dentada y un trinquete.",
    "En un frenazo, un péndulo sigue hacia delante por inercia.",
    "Ese péndulo empuja el trinquete contra los dientes.",
    "Un tirón brusco también activa el bloqueo del carrete.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"cinturón", "traba", "rápido", "cinta", "enrolla", "carrete", "muelle", "despacio", "gira", "sale",
            "rueda", "dentada", "trinquete", "frenazo", "péndulo", "delante", "inercia", "empuja", "dientes",
            "tirón", "brusco", "bloqueo", "funcionan"}

CX, CY, RW, NT = 520, 700, 200, 12          # ratchet wheel
BELT, BELT_D = (70, 90, 120), (45, 60, 85)
CASE = (36, 46, 70)
ENG = (655, 845)                             # pawl tip engaged (between teeth)
RAD = ((ENG[0] - CX) / 198.0, (ENG[1] - CY) / 198.0)
PIV = (531, 961)                             # pawl pivot
PEND = (760, 1000)                           # pendulum pivot

def ratchet(E, d, rot, hl=False):
    pts = []
    for k in range(NT):
        a = rot + 2 * math.pi * k / NT; s = 2 * math.pi / NT
        pts += [(CX + (RW - 26) * math.cos(a), CY + (RW - 26) * math.sin(a)),
                (CX + RW * math.cos(a + 0.75 * s), CY + RW * math.sin(a + 0.75 * s)),
                (CX + (RW - 26) * math.cos(a + 0.78 * s), CY + (RW - 26) * math.sin(a + 0.78 * s))]
    E.poly(d, pts, fill=E.AMB if hl else E.SIL_D)
    E.circle(d, CX, CY, RW - 30, fill=E.SIL)

def spool(E, d, rot, wound=1.0, spring_hl=False):
    r = 95 + 40 * wound
    E.circle(d, CX, CY, r, fill=BELT)
    for k in range(int(3 + 5 * wound)):
        E.circle(d, CX, CY, r - 8 - k * 6, outline=BELT_D, w=2)
    E.circle(d, CX, CY, 80, fill=E.CAV)
    pts = []
    for k in range(120):
        t = k / 119; a = rot * 0.3 + t * 3.5 * 2 * math.pi
        pts.append((CX + (12 + 58 * t) * math.cos(a), CY + (12 + 58 * t) * math.sin(a)))
    E.line(d, pts, E.AMB if spring_hl else E.SIL, 5)
    E.circle(d, CX, CY, 12, fill=E.SIL_D)
    return r

def belt(E, d, r, slide):
    x = CX - r
    E.rrect(d, x - 22, 290, x + 22, CY, 4, BELT)
    for k in range(6):
        y = 300 + ((k * 70 - slide * 70) % 420)
        if y < CY - 10:
            E.line(d, [(x - 18, y), (x + 18, y)], BELT_D, 4)
    E.rrect(d, x - 40, 270, x + 40, 300, 8, E.SIL)

def pawl(E, d, k, hl=False):
    tip = (ENG[0] + RAD[0] * 45 * (1 - k), ENG[1] + RAD[1] * 45 * (1 - k))
    E.line(d, [PIV, tip], E.AMB if hl else E.BLUE, 22)
    E.circle(d, tip[0], tip[1], 13, fill=E.AMB if hl else E.BLUE)
    E.circle(d, PIV[0], PIV[1], 16, fill=E.SIL)
    return tip

def pendulum(E, d, phi, hl=False):
    px, py = PEND
    bx, by = px + 140 * math.sin(phi), py + 140 * math.cos(phi)
    cx_, cy_ = px - 50 * math.sin(phi), py - 50 * math.cos(phi)
    E.line(d, [(cx_, cy_), (bx, by)], E.SIL_D, 10)
    E.circle(d, bx, by, 34, fill=E.AMB if hl else E.HOT)
    E.circle(d, px, py, 10, fill=E.SIL)
    # cap pushes the pawl arm
    mx, my = E.lerp(PIV[0], ENG[0], 0.55), E.lerp(PIV[1], ENG[1], 0.55) + 18
    E.line(d, [(cx_, cy_), (mx + 30, my + 10)], E.SIL_D, 6)

def assembly(E, d, u, rot, slide, k, phi, hl=None, wound=0.9):
    E.rrect(d, 260, 430, 900, 1160, 30, CASE)
    ratchet(E, d, rot, hl == "ratchet")
    r = spool(E, d, rot, wound, hl == "spring")
    belt(E, d, r, slide)
    pawl(E, d, k, hl == "pawl")
    pendulum(E, d, phi, hl == "pend")

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: the belt is already sliding out; a sharp tug locks it
        if u < 1.2:
            slide, k, lab, col = u * 1.2, 0.0, "DESPACIO: SALE", E.WHITE
        elif u < 1.5:
            slide, k, lab, col = 1.44 + (u - 1.2) * 6, 0.0, "RÁPIDO...", E.WHITE
        else:
            slide, k, lab, col = 3.24, 1.0, "SE TRABA", E.AMB
        assembly(E, d, u, slide * 0.55, slide, k, 0.0, hl="pawl" if k else None)
        x = CX - 135
        E.rrect(d, x - 50, 300 - 10 * min(slide, 3.24), x + 50, 360 - 10 * min(slide, 3.24), 26, (232, 180, 140))
        E.arrow(d, x + 90, 420, x + 90, 300, color=E.AMB, w=8)
        E.pill(d, lab, 540, 1110, 44) if k else E.label(d, lab, 540, 1110, 48, color=col)
    elif i == 1:  # belt wound on a spool with a spring
        assembly(E, d, u, -u * 0.4, -u * 0.6, 0.0, 0.0, hl="spring")
        E.label(d, "CARRETE", 760, 380, 44, color=E.WHITE)
        E.label(d, "MUELLE", CX, 1110, 50, color=E.AMB)
    elif i == 2:  # slow pull: spool turns, belt comes out
        assembly(E, d, u, u * 0.6, u * 1.1, 0.0, 0.0)
        a = u * 0.6
        d.arc(E.P(CX - 240, CY - 240, CX + 240, CY + 240), -150 + math.degrees(a) % 30, -80 + math.degrees(a) % 30, fill=E.AMB, width=8 * E.S)
        E.label(d, "GIRA", 800, 420, 46, color=E.AMB)
        E.label(d, "LA CINTA SALE", 540, 1110, 48, color=E.AMB)
    elif i == 3:  # ratchet wheel and pawl
        hl = "ratchet" if (u % 1.6) < 0.8 else "pawl"
        assembly(E, d, u, 0.2, 0, 0.0, 0.0, hl=hl)
        E.label(d, "RUEDA DENTADA", 640, 380, 44, color=E.AMB if hl == "ratchet" else E.WHITE)
        E.label(d, "TRINQUETE", 380, 1110, 44, color=E.AMB if hl == "pawl" else E.WHITE)
    elif i == 4:  # sudden stop: the pendulum keeps going forward by inertia
        phi = 0.45 * E.ease(u / (L * 0.4))
        assembly(E, d, u, 0.2, 0, 0.0, phi, hl="pend")
        E.arrow(d, 650, 385, 890, 385, color=E.AMB, w=10)
        E.label(d, "INERCIA", 535, 385, 44, color=E.AMB)
        E.label(d, "PÉNDULO", 400, 1110, 46, color=E.WHITE)
    elif i == 5:  # pendulum pushes the pawl into the teeth
        k = E.ease(u / (L * 0.35))
        assembly(E, d, u, 0.2, 0, k, 0.45, hl="pawl")
        E.label(d, "TRINQUETE", 380, 1110, 44, color=E.AMB)
        E.label(d, "DIENTES", 790, 760, 40, color=E.WHITE)
        if k > 0.95:
            E.pill(d, "BLOQUEADO", 760, 380, 40)
    else:
        if i == 6:  # a sharp tug of the belt also locks the spool
            t = u % 1.6
            k = 1.0 if t > 0.35 else 0.0
            slide = min(t, 0.35) * 5
            assembly(E, d, u, slide * 0.55, slide, k, 0.0, hl="pawl" if k else None)
            E.arrow(d, CX - 45, 420, CX - 45, 290, color=E.AMB, w=10)
            E.label(d, "TIRÓN", 270, 380, 44, color=E.WHITE)
            if k:
                E.pill(d, "BLOQUEO", 540, 1110, 44)
        else:
            E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("zip", s[0] + 0.0, 1.4), ("click", s[0] + 1.5), ("whoosh", s[1] + 0.2, 1.0), ("zip", s[2] + 0.1, 1.6),
            ("pop", s[3] + 0.3), ("whoosh", s[4] + 0.2, 0.8), ("click", s[5] + 0.6), ("click", s[6] + 0.35),
            ("click", s[6] + 1.95)]
