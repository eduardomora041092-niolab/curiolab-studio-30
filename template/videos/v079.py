"""Video 079 — ¿Por qué la rueda de la bici gira sin pedalear?
Science: the rear hub of a bicycle contains a freewheel (ratchet) mechanism. The sprocket side carries small pawls
that small springs push outward; the wheel side has a ring of angled (saw-tooth) teeth. When you pedal, the pawls
catch the steep face of the teeth and drive the wheel. When you stop pedalling, the wheel keeps turning faster than
the sprocket: the sloped side of each tooth pushes the pawls down and they slide over, so the wheel spins freely.
The clicking you hear while coasting is the pawls snapping back against the teeth.
(No number of pawls/teeth or engagement angle is claimed; other freewheel designs are not covered.)
"""
import math

ID = "079"
TITLE = "¿Por qué la rueda de la bici gira sin pedalear?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Por qué la rueda de la bici gira aunque no pedalees?",
    "Dentro del buje trasero hay un mecanismo llamado rueda libre.",
    "El piñón lleva unas pequeñas uñas, y la rueda, un anillo de dientes.",
    "Unos muelles empujan las uñas contra los dientes.",
    "Al pedalear, las uñas se enganchan y arrastran la rueda.",
    "Si dejas de pedalear, los dientes inclinados empujan las uñas hacia abajo y pasan por encima.",
    "Ese roce es el clic clic que oyes al bajar sin pedalear.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"rueda", "bici", "pedalees", "buje", "trasero", "rueda libre", "piñón", "uñas", "dientes", "muelles",
            "pedalear", "enganchan", "arrastran", "inclinados", "abajo", "encima", "clic", "roce"}

CX, CY = 540, 720
R_OUT = 330          # outer body of the wheel-side ring
R_CREST, R_DEEP = 262, 292   # inner tooth surface (crest = closest to centre)
R_HUB = 228          # sprocket-side disc
N = 16
STEP = 2 * math.pi / N
NP = 3
TIP_OFF = 0.20       # pawl tip angle ahead of its pivot
RING = (150, 160, 175)
TIRE = (40, 44, 52)


def surf(phi, th_o):
    """Radius of the toothed inner surface at absolute angle phi when the ring is rotated th_o."""
    f = ((phi - th_o) % STEP) / STEP
    if f < 0.88:
        return R_CREST + (R_DEEP - R_CREST) * f / 0.88
    return R_DEEP


def pol(r, a):
    return CX + r * math.cos(a), CY + r * math.sin(a)


def ratchet(E, d, th_o, th_i, hl_pawl=False, hl_spring=False, hl_teeth=False, engaged=None):
    # wheel-side ring with saw-tooth inner surface
    E.circle(d, CX, CY, R_OUT, fill=RING)
    E.circle(d, CX, CY, R_OUT, outline=E.SIL_H, w=4)
    pts = []
    for k in range(N):
        a = th_o + k * STEP
        for j in range(9):
            f = 0.88 * j / 8
            pts.append(pol(R_CREST + (R_DEEP - R_CREST) * f / 0.88, a + f * STEP))
        pts.append(pol(R_DEEP, a + STEP - 0.001))
    E.poly(d, pts, fill=E.CAV)
    if hl_teeth:
        for k in range(N):
            a = th_o + k * STEP
            x0, y0 = pol(R_DEEP, a + STEP)
            x1, y1 = pol(R_CREST, a + STEP)
            E.line(d, [(x0, y0), (x1, y1)], E.AMB, 6)
    # sprocket-side disc
    E.circle(d, CX, CY, R_HUB, fill=E.BRA_D)
    E.circle(d, CX, CY, R_HUB - 18, fill=E.BRA)
    E.circle(d, CX, CY, 60, fill=E.BRA_D)
    for p in range(NP):
        b = th_i + p * 2 * math.pi / NP
        tipa = b + TIP_OFF
        rt = surf(tipa, th_o) - 6 if engaged is None else engaged
        rt = min(rt, R_DEEP - 6)
        pv = pol(R_HUB - 4, b)
        tip = pol(rt, tipa)
        base2 = pol(R_HUB - 4, b + 0.17)
        mid = pol((R_HUB + rt) / 2 + 10, b + 0.07)
        col = E.AMB if hl_pawl else E.SIL
        E.poly(d, [pv, mid, tip, base2], fill=col, outline=E.BG1, w=3)
        E.circle(d, pv[0], pv[1], 11, fill=E.SIL_D)
        # spring under the pawl: zig-zag from disc to pawl middle
        sa = b + 0.12
        r0, r1 = R_HUB - 45, R_HUB + 2
        zz = []
        for z in range(9):
            r = r0 + (r1 - r0) * z / 8
            off = (0.035 if z % 2 else -0.035) if 0 < z < 8 else 0
            zz.append(pol(r, sa + off))
        E.line(d, zz, E.HOT if hl_spring else E.SIL_D, 5 if hl_spring else 3)


def bike_wheel(E, d, x, y, R, ang, hub_hl=0.0):
    E.circle(d, x, y, R, outline=TIRE, w=26)
    E.circle(d, x, y, R - 14, outline=E.SIL_D, w=6)
    for k in range(16):
        a = ang + k * math.pi / 8
        E.line(d, [(x + 30 * math.cos(a), y + 30 * math.sin(a)), (x + (R - 16) * math.cos(a), y + (R - 16) * math.sin(a))],
               E.SIL, 3)
    E.circle(d, x, y, 40, fill=E.mix(E.SIL_D, E.AMB, hub_hl))
    E.circle(d, x, y, 14, fill=E.BG1)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: wheel spinning fast while the pedals stay still
        ang = 0.6 + u * 5.0
        bike_wheel(E, d, 600, 720, 300, ang)
        # frame stays + crank that does not move
        E.line(d, [(600, 720), (270, 640)], E.BLUE, 16)
        E.line(d, [(600, 720), (330, 900)], E.BLUE, 16)
        E.circle(d, 300, 900, 46, fill=E.BRA_D)
        E.line(d, [(300, 900), (300, 1040)], E.SIL_D, 14)
        E.rrect(d, 250, 1030, 350, 1060, 8, E.SIL)
        for k in range(3):
            a0 = ang + k * 2.1
            pts = [(600 + 335 * math.cos(a0 - t * 0.06), 720 + 335 * math.sin(a0 - t * 0.06)) for t in range(10)]
            E.line(d, pts, E.AMB, 6)
        E.label(d, "SIN PEDALEAR", 300, 1120, 40, color=E.MUTED)
    elif i == 1:  # rear hub → freewheel inside
        k = E.ease(u / (L * 0.6))
        bike_wheel(E, d, 330, 720, 220, 0.3 + u * 1.5, hub_hl=1.0)
        E.circle(d, 330, 720, 60, outline=E.AMB, w=6)
        E.line(d, [(380, 680), (640, 560)], E.AMB, 4)
        E.line(d, [(380, 760), (640, 880)], E.AMB, 4)
        s = 0.2 + 0.25 * k
        E.circle(d, 790, 720, 175, fill=E.mix(E.BG1, RING, k), outline=E.AMB, w=6)
        E.circle(d, 790, 720, 120 * (0.5 + 0.5 * k), fill=E.BRA)
        E.label(d, "BUJE", 330, 1010, 46, color=E.AMB)
        E.label(d, "RUEDA LIBRE", 790, 960, 46, color=E.WHITE)
    elif i == 2:  # pawls on the sprocket side, teeth on the wheel side
        ratchet(E, d, 0.15, -0.5, hl_pawl=True, hl_teeth=True)
        E.label(d, "UÑAS (PIÑÓN)", 540, 330, 46, color=E.AMB)
        E.label(d, "DIENTES (RUEDA)", 540, 1110, 46, color=E.WHITE)
    elif i == 3:  # springs push pawls outward
        bump = 0.5 + 0.5 * math.sin(u * 7)
        ratchet(E, d, 0.15, -0.5, hl_spring=True, engaged=R_CREST - 20 + 26 * bump)
        E.label(d, "MUELLES", 540, 330, 50, color=E.HOT)
        b = -0.5 + 0.11
        x0, y0 = pol(R_HUB - 30, b)
        x1, y1 = pol(R_HUB + 40, b)
        E.arrow(d, x0, y0, x1, y1, E.WHITE, 5, 18)
    elif i == 4:  # pedalling: pawls caught, ring dragged along
        th = u * 1.2
        th_o = th
        # put pawl tips in the deep zone just before each wall
        th_i = th_o - TIP_OFF + 0.95 * STEP + 0.0
        ratchet(E, d, th_o, th_i)
        for k in range(2):
            a = th + k * math.pi
            E.arrow(d, *pol(R_OUT + 40, a), *pol(R_OUT + 40, a + 0.35), E.AMB, 7, 24)
        E.pill(d, "ENGANCHADAS", 540, 330, 42)
        E.label(d, "PIÑÓN + RUEDA GIRAN JUNTOS", 540, 1120, 38, color=E.WHITE)
    elif i == 5:  # coasting: ring turns, sprocket still, teeth push pawls down and slide over
        th_o = u * 0.9
        th_i = -TIP_OFF + 0.95 * STEP
        ratchet(E, d, th_o, th_i, hl_pawl=True)
        E.arrow(d, *pol(R_OUT + 40, th_o - 1.2), *pol(R_OUT + 40, th_o - 0.85), E.AMB, 7, 24)
        E.label(d, "RUEDA GIRA", 860, 330, 40, color=E.AMB)
        E.label(d, "PIÑÓN QUIETO", 240, 330, 40, color=E.MUTED)
        E.label(d, "LAS UÑAS PASAN POR ENCIMA", 540, 1120, 38, color=E.WHITE)
    elif i == 6:  # the click
        th_o = u * 0.9
        th_i = -TIP_OFF + 0.95 * STEP
        ratchet(E, d, th_o, th_i)
        for p in range(NP):
            tipa = th_i + p * 2 * math.pi / NP + TIP_OFF
            f = ((tipa - th_o) % STEP) / STEP
            if f > 0.88:
                x, y = pol(R_OUT + 70, tipa)
                E.label(d, "CLIC", x, y, 44, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.2, 0.8), ("pop", s[1] + 0.5), ("pop", s[2] + 0.6), ("click", s[3] + 0.5),
            ("whoosh", s[4] + 0.5, 0.8), ("click", s[5] + 0.8), ("click", s[6] + 0.4), ("click", s[6] + 0.9)]
