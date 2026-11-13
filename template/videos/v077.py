"""Video 077 — ¿Por qué un ascensor necesita contrapeso?
Science: in a traction elevator the car hangs from steel ropes that run over a driven pulley (sheave) at the top of
the shaft. At the other end of the ropes hangs a heavy counterweight, usually as heavy as the car plus part of its
rated load. When the car goes up the counterweight goes down, and vice versa, so the two loads largely balance. The
motor therefore only has to overcome the difference in weight (plus friction), not the whole weight of the car and
passengers, so it uses much less energy and can be smaller.
(No percentages of balanced load or energy savings are claimed.)
"""
import math

ID = "077"
TITLE = "¿Por qué un ascensor necesita contrapeso?"
SUBTITLE = "CÓMO FUNCIONA"
LINES = [
    "¿Por qué un ascensor necesita un contrapeso?",
    "La cabina cuelga de cables de acero que pasan por una polea arriba.",
    "Al otro lado de los cables cuelga un bloque pesado: el contrapeso.",
    "Pesa como la cabina más una parte de la carga habitual.",
    "Así, cuando la cabina sube, el contrapeso baja, y los dos se equilibran.",
    "El motor solo tiene que mover la diferencia de peso, no todo.",
    "Por eso gasta mucha menos energía y el motor puede ser más pequeño.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"ascensor", "contrapeso", "cabina", "cables", "acero", "polea", "pesado", "pesa", "carga", "sube",
            "baja", "equilibran", "motor", "diferencia", "peso", "energía", "pequeño"}

CAR = (200, 210, 225)
CW = (110, 120, 140)
ROPE = (180, 186, 196)


def shaft(E, d, car_y, cw_y, rot=0.0, px=540, py=430, r=150, carx=None, cwx=None):
    carx = px - r if carx is None else carx
    cwx = px + r if cwx is None else cwx
    E.line(d, [(carx, py), (carx, car_y - 110)], ROPE, 5)
    E.line(d, [(cwx, py), (cwx, cw_y - 70)], ROPE, 5)
    E.circle(d, px, py, r, fill=E.SIL_D, outline=E.SIL, w=5)
    for k in range(4):
        a = rot + k * math.pi / 2
        E.line(d, [(px, py), (px + (r - 10) * math.cos(a), py + (r - 10) * math.sin(a))], E.SIL, 6)
    E.circle(d, px, py, 16, fill=E.SIL)
    car(E, d, carx, car_y)
    cweight(E, d, cwx, cw_y)


def car(E, d, x, y, people=2):
    E.rrect(d, x - 120, y - 110, x + 120, y + 110, 10, CAR, outline=E.SIL_D, w=4)
    E.line(d, [(x, y - 100), (x, y + 100)], E.SIL_D, 3)
    for k in range(people):
        px = x - 50 + k * 100
        E.circle(d, px, y - 30, 20, fill=E.BLUE_D)
        E.rrect(d, px - 22, y - 8, px + 22, y + 80, 10, E.BLUE_D)


def cweight(E, d, x, y):
    E.rrect(d, x - 55, y - 70, x + 55, y + 70, 6, CW, outline=E.SIL_D, w=3)
    for k in range(3):
        E.line(d, [(x - 50, y - 35 + k * 35), (x + 50, y - 35 + k * 35)], E.SIL_D, 3)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: car rising, counterweight falling, pulley turning
        s = 0.5 + 0.5 * math.sin(u * 1.6 - math.pi / 2)
        car_y = 1050 - 330 * s
        cw_y = 720 + 330 * s
        shaft(E, d, car_y, cw_y, rot=u * 3)
        E.arrow(d, 150, car_y + 40, 150, car_y - 60, E.AMB, 6, 24)
        E.arrow(d, 930, cw_y - 40, 930, cw_y + 60, E.COLD, 6, 24)
    elif i == 1:  # car hangs from steel ropes over a pulley at the top
        shaft(E, d, 900, 700, rot=u * 0.5)
        E.label(d, "POLEA", 540, 430, 46, color=E.AMB)
        E.label(d, "CABLES", 220, 640, 42, color=E.WHITE)
        E.label(d, "CABINA", 390, 1060, 44, color=E.WHITE)
    elif i == 2:  # other side: counterweight
        shaft(E, d, 900, 700)
        k = 0.5 + 0.5 * math.sin(u * 6)
        E.rrect(d, 620, 615, 760, 785, 10, None, outline=E.mix(E.AMB, E.WHITE, k), w=6)
        E.label(d, "CONTRAPESO", 760, 870, 46, color=E.AMB)
    elif i == 3:  # weighs like car + part of the load: balance
        tilt = 0.06 * math.sin(u * 2)
        cx, cy = 540, 560
        dx = 330
        y1, y2 = cy - dx * tilt, cy + dx * tilt
        E.poly(d, [(cx, cy), (cx - 50, 1080), (cx + 50, 1080)], fill=E.SIL_D)
        E.line(d, [(cx - dx, y1), (cx + dx, y2)], E.SIL, 10)
        E.line(d, [(cx - dx, y1), (cx - dx, y1 + 90)], ROPE, 4)
        E.line(d, [(cx + dx, y2), (cx + dx, y2 + 90)], ROPE, 4)
        car(E, d, cx - dx, y1 + 200)
        E.rrect(d, cx + dx - 90, y2 + 90, cx + dx + 90, y2 + 310, 8, CW, outline=E.SIL_D, w=3)
        E.label(d, "CABINA + CARGA", 230, 960, 40, color=E.WHITE)
        E.label(d, "CONTRAPESO", 830, 960, 40, color=E.AMB)
    elif i == 4:  # car up, counterweight down: they balance
        k = E.ease(u / (L * 0.9))
        shaft(E, d, 1050 - 330 * k, 720 + 330 * k, rot=k * 4)
        E.arrow(d, 150, 760, 150, 560, E.AMB, 7, 28)
        E.label(d, "SUBE", 150, 500, 40, color=E.AMB)
        E.arrow(d, 930, 560, 930, 760, E.COLD, 7, 28)
        E.label(d, "BAJA", 930, 820, 40, color=E.COLD)
    elif i == 5:  # motor only moves the difference
        E.rrect(d, 120, 360, 500, 760, 16, CAR, outline=E.SIL_D, w=4)
        E.label(d, "TODO EL PESO", 310, 320, 40, color=E.WHITE)
        E.cross(d, 310, 860, 55)
        h = 80 + 20 * math.sin(u * 5)
        E.rrect(d, 700, 760 - h, 860, 760, 10, E.AMB)
        E.label(d, "DIFERENCIA", 780, 840, 44, color=E.AMB)
        E.rrect(d, 700, 380, 860, 520, 20, E.SIL_D, outline=E.SIL, w=4)
        E.label(d, "MOTOR", 780, 450, 36, color=E.WHITE)
        E.arrow(d, 780, 530, 780, 640, E.WHITE, 6, 24)
    elif i == 6:  # less energy, smaller motor
        k = E.ease(u / (L * 0.8))
        E.rrect(d, 160, 420, 460, 760, 24, E.SIL_D, outline=E.SIL, w=4)
        E.label(d, "MOTOR", 310, 590, 40, color=E.WHITE)
        E.label(d, "SIN CONTRAPESO", 310, 840, 36, color=E.MUTED)
        s = 1.0 - 0.45 * k
        E.rrect(d, 780 - 150 * s, 590 - 170 * s, 780 + 150 * s, 590 + 170 * s, 24, E.AMB)
        E.label(d, "MOTOR", 780, 590, 30, color=E.WHITE)
        E.label(d, "CON CONTRAPESO", 780, 840, 36, color=E.AMB)
        E.label(d, "MENOS ENERGÍA", 540, 1000, 52, color=E.WHITE)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.2, 0.8), ("click", s[1] + 0.5), ("pop", s[2] + 0.6), ("click", s[3] + 0.5),
            ("whoosh", s[4] + 0.5, 0.8), ("pop", s[5] + 0.6), ("pop", s[6] + 0.6)]
