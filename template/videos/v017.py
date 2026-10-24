"""Video 017 — ¿Por qué la cinta métrica vuelve sola?
Mechanism: inside the case of a tape measure the steel blade is wound on a reel (drum). A flat spiral spring sits
inside the reel: one end is fixed to the stationary central post, the other to the reel. Pulling the blade out
turns the reel and winds the spring tighter, storing elastic energy, as in a wind-up toy. A lock (brake) button
presses on the blade and holds it extended. When the lock is released, the spring unwinds, turns the reel back and
pulls the blade into the case; a hook at the tip stops it at the mouth of the case.
(No spring force, blade length or speed figures are claimed.)
"""
import math

ID = "017"
TITLE = "¿Por qué la cinta métrica vuelve sola?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "Suéltala y la cinta métrica regresa a toda velocidad.",
    "Dentro de la carcasa, la cinta está enrollada en un carrete.",
    "En el centro del carrete hay un muelle plano en espiral.",
    "Al sacar la cinta, el carrete gira y aprieta el muelle.",
    "El muelle guarda esa energía, como un juguete de cuerda.",
    "Un botón de freno pisa la cinta para que no vuelva.",
    "Al soltar el freno, el muelle se desenrolla y tira de la cinta hacia dentro.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"cinta", "métrica", "regresa", "velocidad", "carcasa", "enrollada", "carrete", "muelle", "espiral",
            "gira", "aprieta", "energía", "cuerda", "freno", "desenrolla", "dentro", "funcionan"}

CASE = (120, 520, 560, 940)
RC = (330, 720)              # reel centre
MOUTH_X, BLADE_Y = 560, 910
CASE_C, CASE_E = (200, 60, 50), (140, 40, 35)
BLADE, BLADE_D = (250, 205, 60), (190, 150, 30)

def spiral(E, d, cx, cy, turns, rot, r0=14, r1=72, color=None, w=5):
    n = int(40 * turns)
    pts = []
    for k in range(n + 1):
        t = k / n
        a = rot + t * turns * 2 * math.pi
        r = r0 + (r1 - r0) * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    E.line(d, pts, color or E.SIL_H, w)

def tape(E, d, ext, hl=None, brake=0.0, cut=True):
    """ext 0..1 = how much blade is out. Draws case cutaway, coil, spring and blade."""
    x0, y0, x1, y1 = CASE
    E.rrect(d, x0, y0, x1, y1, 60, CASE_C, outline=CASE_E, w=6)
    if cut:
        E.circle(d, RC[0], RC[1], 190, fill=E.CAV)
    rot = -ext * 9.0
    coil_r = E.lerp(180, 105, ext)
    rim = E.AMB if hl == "reel" else BLADE
    # coil of blade (rings) around the reel
    rings = int(E.lerp(10, 3, ext))
    for k in range(rings):
        rr = 100 + (coil_r - 100) * (k + 1) / max(1, rings)
        E.circle(d, RC[0], RC[1], rr, outline=rim if k == rings - 1 else BLADE_D, w=6)
    E.circle(d, RC[0], RC[1], 98, fill=(40, 50, 70), outline=E.SIL_D, w=4)
    # spoke mark showing the reel rotation
    E.line(d, [(RC[0] + 80 * math.cos(rot), RC[1] + 80 * math.sin(rot)), (RC[0] + 96 * math.cos(rot), RC[1] + 96 * math.sin(rot))], E.WHITE, 8)
    # spiral spring: more turns in the same space = wound tighter
    sc = E.AMB if hl == "spring" else E.SIL_H
    spiral(E, d, RC[0], RC[1], E.lerp(2.5, 5.0, ext), rot * 0.5, color=sc, w=6 if hl == "spring" else 4)
    E.circle(d, RC[0], RC[1], 12, fill=E.SIL_D)
    # blade leaving the coil towards the mouth
    E.line(d, [(RC[0] + coil_r * 0.2, RC[1] + coil_r), (MOUTH_X, BLADE_Y)], BLADE, 10)
    tip = MOUTH_X + 20 + ext * 440
    E.rrect(d, MOUTH_X, BLADE_Y - 14, tip, BLADE_Y + 14, 3, BLADE)
    for k in range(int((tip - MOUTH_X) // 40)):
        x = MOUTH_X + 20 + k * 40
        E.line(d, [(x, BLADE_Y - 14), (x, BLADE_Y - (2 if k % 2 else -4))], (40, 40, 40), 3)
    E.rrect(d, tip, BLADE_Y - 34, tip + 14, BLADE_Y + 18, 3, E.SIL)   # hook
    # brake button on top of the mouth
    by = E.lerp(560, 600, brake)
    bc = E.AMB if hl == "brake" else E.SIL
    E.rrect(d, 470, by - 40, 540, by + 30, 12, bc, outline=E.SIL_D, w=3)
    if brake > 0.5:
        E.line(d, [(505, by + 30), (505, BLADE_Y - 16)], bc, 10)
    return tip

def scene(i, u, L, E, im, d):
    if i == 0:  # it comes back fast
        k = E.ease(min(1.0, max(0.0, u - 0.5) / 0.6))
        tip = tape(E, d, 1.0 - k, cut=False)
        if 0.4 < u < 1.3:
            for j in range(3):
                E.line(d, [(tip + 30 + j * 40, BLADE_Y - 40 + j * 30), (tip + 110 + j * 40, BLADE_Y - 40 + j * 30)], E.WHITE, 5)
        E.label(d, "VUELVE SOLA", 540, 1100, 50, color=E.AMB)
    elif i == 1:  # wound on a reel
        tape(E, d, 0.15, hl="reel")
        E.label(d, "CARRETE", 800, 640, 48, color=E.AMB)
        E.arrow(d, 690, 670, 530, 700, color=E.AMB, w=6)
        E.label(d, "CARCASA", 340, 460, 40, color=E.WHITE)
    elif i == 2:  # spiral spring in the centre
        tape(E, d, 0.15, hl="spring")
        p = 0.5 + 0.5 * math.sin(u * 5)
        E.circle(d, RC[0], RC[1], 92 + 6 * p, outline=E.AMB, w=3)
        E.label(d, "MUELLE EN ESPIRAL", 540, 1100, 46, color=E.AMB)
    elif i == 3:  # pulling turns the reel and winds the spring
        k = E.ease(u / (L * 0.85))
        tip = tape(E, d, E.lerp(0.1, 1.0, k), hl="spring")
        E.arrow(d, 700, 1010, 880, 1010, color=E.WHITE, w=8)
        E.label(d, "GIRA", RC[0], 440, 46, color=E.WHITE)
        if u > L * 0.5: E.label(d, "SE APRIETA", 540, 1100, 46, color=E.AMB)
    elif i == 4:  # stored energy, like a wind-up toy
        tape(E, d, 1.0, hl="spring")
        for j in range(3):
            r = 80 + ((u * 90 + j * 40) % 120)
            E.circle(d, RC[0], RC[1], r, outline=E.mix(E.AMB, E.BG2, (r - 80) / 120), w=4)
        E.pill(d, "ENERGÍA GUARDADA", 540, 1100, 40)
    elif i == 5:  # brake holds the blade
        k = E.ease(u / (L * 0.4))
        tape(E, d, 1.0, hl="brake", brake=k)
        E.label(d, "FRENO", 505, 400, 48, color=E.AMB)
        E.arrow(d, 505, 440, 505, 505, color=E.AMB, w=7)
    elif i == 6:  # release: spring unwinds and pulls the blade in
        rel = E.ease(min(1.0, u / 0.5))
        k = E.ease(max(0.0, u - 0.6) / (L * 0.6))
        tip = tape(E, d, 1.0 - k, hl="spring", brake=1.0 - rel)
        E.arrow(d, 880, 1010, 700, 1010, color=E.WHITE, w=8)
        E.label(d, "SE DESENROLLA", RC[0], 440, 44, color=E.AMB)
        if u > L * 0.5: E.label(d, "HACIA DENTRO", 540, 1100, 46, color=E.WHITE)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.5, 0.6), ("click", s[0] + 1.1), ("pop", s[1] + 0.4), ("pop", s[2] + 0.4),
            ("whoosh", s[3] + 0.2, 1.2), ("pop", s[4] + 0.5), ("click", s[5] + 0.6), ("whoosh", s[6] + 0.6, 0.8)]
