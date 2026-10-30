"""Video 035 — ¿Cómo genera luz la dinamo de una bicicleta?
Science (bottle/sidewall dynamo): a small roller rests on the tyre, so the turning wheel spins the roller and the
shaft of the dynamo. On the shaft there is a permanent magnet surrounded by a coil of wire. As the magnet turns, the
magnetic field passing through the coil keeps changing. A changing magnetic field through a coil induces an electric
current in it (electromagnetic induction, the same principle as any generator). The wires carry that current to the
lamp, which lights up. With no battery, when the wheel stops the magnet stops, the field no longer changes and the
light goes out. (No voltages, powers or speeds are claimed; hub dynamos are not discussed.)
"""
import math

ID = "035"
TITLE = "¿Cómo genera luz la dinamo de una bicicleta?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo genera luz la dinamo de una bicicleta?",
    "La rueda hace girar una ruedecita de la dinamo.",
    "Dentro, un imán gira rodeado por una bobina de cable.",
    "Al girar, cambia el campo magnético dentro de la bobina.",
    "Ese cambio genera corriente eléctrica en el cable: es la inducción.",
    "La corriente viaja por los cables y enciende la luz.",
    "Si dejas de pedalear, el imán se detiene y la luz se apaga.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"luz", "dinamo", "bicicleta", "rueda", "girar", "ruedecita", "imán", "gira", "bobina", "cable",
            "campo", "magnético", "cambio", "corriente", "eléctrica", "inducción", "cables", "enciende", "pedalear",
            "detiene", "apaga"}

COPPER = (214, 128, 64)
N_COL, S_COL = (226, 70, 60), (60, 120, 220)
LAMP_ON = (255, 236, 150)

def wheel(E, d, x, y, r, a):
    E.circle(d, x, y, r, fill=None, outline=(60, 66, 78), w=34)
    E.circle(d, x, y, r - 22, fill=None, outline=E.SIL_D, w=6)
    for k in range(12):
        b = a + k * math.pi / 6
        E.line(d, [(x, y), (x + (r - 24) * math.cos(b), y + (r - 24) * math.sin(b))], E.SIL, 3)
    E.circle(d, x, y, 22, fill=E.SIL_H)

def lamp(E, d, x, y, b):
    """b = brightness 0..1"""
    E.rrect(d, x - 60, y - 45, x + 50, y + 45, 18, E.SIL_D)
    E.circle(d, x + 55, y, 42, fill=E.mix(E.SIL_D, LAMP_ON, b))
    if b > 0.05:
        for k in range(-2, 3):
            ang = k * 0.22
            E.line(d, [(x + 110 * math.cos(ang) + 10, y + 110 * math.sin(ang)), (x + (110 + 120 * b) * math.cos(ang) + 10, y + (110 + 120 * b) * math.sin(ang))],
                   E.mix(E.BG2, LAMP_ON, b), 8)

def magnet_rotor(E, d, x, y, a, r=120):
    ca, sa = math.cos(a), math.sin(a); nx, ny = -sa, ca; w = 55
    for sgn, col, p in ((1, N_COL, "N"), (-1, S_COL, "S")):
        ex, ey = x + sgn * r * ca, y + sgn * r * sa
        E.poly(d, [(x + nx * w, y + ny * w), (x - nx * w, y - ny * w), (ex - nx * w, ey - ny * w), (ex + nx * w, ey + ny * w)], fill=col)
        E.label(d, p, x + sgn * r * 0.6 * ca, y + sgn * r * 0.6 * sa, 50, color=E.WHITE)
    E.circle(d, x, y, 16, fill=E.SIL_H)

def coil(E, d, x, y, r=200):
    for side in (-1, 1):
        x0 = x + side * r
        E.rrect(d, x0 - 45, y - 150, x0 + 45, y + 150, 14, COPPER)
        for k in range(8):
            yy = y - 130 + k * 37
            E.line(d, [(x0 - 40, yy), (x0 + 40, yy)], E.mix(COPPER, E.BG1, 0.45), 4)
    E.line(d, [(x - r, y - 150), (x - r, y - 190), (x + r, y - 190), (x + r, y - 150)], COPPER, 10)

def dynamo(E, d, wire):
    """Bottle dynamo resting on the tyre of the wheel centred at (460, 780), r=330 (contact at -45 degrees)."""
    E.line(d, [(735, 500), (712, 528)], E.SIL_D, 10)
    E.rrect(d, 690, 360, 780, 505, 20, E.SIL)        # body
    E.circle(d, 722, 522, 26, fill=E.SIL_H)          # roller touching the tyre
    E.line(d, [(735, 362), (735, 330), (840, 330)], wire, 5)

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: wheel turning, dynamo on the tyre, lamp already lit
        a = u * 4.0
        wheel(E, d, 460, 780, 330, a)
        dynamo(E, d, E.AMB)
        lamp(E, d, 900, 330, 0.85 + 0.15 * math.sin(u * 7))
        E.pill(d, "DINAMO", 300, 340, 44)
    elif i == 1:  # the wheel spins the small roller
        a = u * 2.0
        E.circle(d, 540, 1450, 900, fill=None, outline=(60, 66, 78), w=60)   # big tyre arc
        for k in range(18):   # tread marks moving with the tyre
            b = -math.pi / 2 + (k - 9) * 0.06 + (a * 0.12) % 0.06
            E.line(d, [(540 + 880 * math.cos(b), 1450 + 880 * math.sin(b)), (540 + 920 * math.cos(b), 1450 + 920 * math.sin(b))], E.SIL_D, 6)
        E.circle(d, 540, 460, 70, fill=E.SIL)
        for k in range(6):
            b = -a * 12.0 + k * math.pi / 3
            E.line(d, [(540 + 20 * math.cos(b), 460 + 20 * math.sin(b)), (540 + 64 * math.cos(b), 460 + 64 * math.sin(b))], E.SIL_D, 6)
        E.arrow(d, 300, 640, 420, 600, E.AMB, 7, 26)
        E.label(d, "RUEDA", 540, 760, 50, color=E.AMB)
        E.label(d, "RUEDECITA", 810, 400, 44, color=E.AMB)
    elif i == 2:  # inside: a magnet turns surrounded by a coil
        coil(E, d, 540, 680)
        magnet_rotor(E, d, 540, 680, u * 2.2)
        E.label(d, "IMÁN", 540, 920, 48, color=E.AMB)
        E.label(d, "BOBINA", 540, 380, 48, color=E.AMB)
    elif i == 3:  # the field inside the coil keeps changing
        a = u * 2.2
        coil(E, d, 540, 640)
        magnet_rotor(E, d, 540, 640, a)
        for k in (-60, 0, 60):   # field lines leaving the N end
            ca, sa = math.cos(a), math.sin(a)
            ex, ey = 540 + 130 * ca - sa * k, 640 + 130 * sa + ca * k
            E.line(d, [(ex, ey), (ex + 90 * ca, ey + 90 * sa)], E.COLD, 5)
        m = math.cos(a)   # field through the coil (horizontal component)
        E.rrect(d, 240, 1000, 840, 1040, 18, E.BG2)
        E.rrect(d, 540 + min(0, m * 290), 1004, 540 + max(0, m * 290), 1036, 14, E.COLD)
        E.label(d, "CAMPO MAGNÉTICO", 540, 950, 44, color=E.COLD)
    elif i == 4:  # the change induces a current: induction
        a = u * 2.2
        coil(E, d, 540, 640)
        magnet_rotor(E, d, 540, 640, a)
        sgn = 1 if math.sin(a) > 0 else -1
        for k in range(7):
            f = ((u * 0.8 * sgn) + k / 7) % 1
            E.circle(d, 340 + 400 * f, 450, 10, fill=E.AMB)
        E.line(d, [(340, 790), (340, 980)], COPPER, 8)
        E.line(d, [(740, 790), (740, 980)], COPPER, 8)
        E.label(d, "CORRIENTE", 540, 340, 48, color=E.AMB)
        E.pill(d, "INDUCCIÓN", 540, 1040, 46)
    elif i == 5:  # current flows to the lamp and lights it
        k = E.ease(u / (L * 0.6))
        E.rrect(d, 120, 560, 300, 820, 24, E.SIL)
        E.label(d, "DINAMO", 210, 880, 42, color=E.MUTED)
        E.line(d, [(300, 620), (760, 620)], E.COLD, 7)
        E.line(d, [(300, 760), (760, 760)], E.COLD, 7)
        for j in range(6):
            f = (u * 0.7 + j / 6) % 1
            E.circle(d, 300 + 460 * f, 620, 9, fill=E.AMB)
            E.circle(d, 760 - 460 * f, 760, 9, fill=E.AMB)
        lamp(E, d, 820, 690, k)
        E.label(d, "LUZ", 880, 500, 52, color=E.AMB)
    elif i == 6:  # stop pedalling: the magnet stops and the light goes out
        s = max(0.0, 1 - u / (L * 0.6))
        a = 4.0 * (u - u * u / (2 * L * 0.6)) if s > 0 else 4.0 * L * 0.3
        wheel(E, d, 460, 780, 330, a)
        dynamo(E, d, E.SIL_D)
        lamp(E, d, 900, 330, s)
        if s == 0:
            E.pill(d, "SIN GIRO, SIN LUZ", 460, 1060, 42, bg=E.HOT)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.05, 1.0), ("zip", s[1] + 0.4, 1.0), ("click", s[2] + 0.6), ("whoosh", s[3] + 0.4, 0.8),
            ("pop", s[4] + 0.9), ("click", s[5] + 1.0), ("whoosh", s[6] + 0.3, 1.2)]
