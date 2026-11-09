"""Video 064 — ¿Cómo carga el móvil sin cables?
Science: a wireless (inductive, Qi-type) charging pad contains a flat coil of copper wire. An alternating current
flows through that coil, changing direction many times per second, so it produces a magnetic field that keeps
changing. The phone has a second coil just above the pad. The changing magnetic field passes through the phone's
coil and, by electromagnetic induction (Faraday's law), induces an alternating current in it. Circuitry in the phone
converts (rectifies) that current to direct current, which charges the battery. The coils must be close and aligned.
(No frequencies, powers, efficiencies or distances are claimed.)
"""
import math

ID = "064"
TITLE = "¿Cómo carga el móvil sin cables?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo carga el móvil sin cables?",
    "Dentro de la base hay una bobina de cable de cobre.",
    "Por ella pasa una corriente que cambia de sentido muy rápido.",
    "Esa corriente crea un campo magnético que también cambia sin parar.",
    "El móvil tiene otra bobina justo encima de la base.",
    "El campo variable atraviesa esa bobina e induce una corriente.",
    "Esa corriente, ya convertida, va cargando la batería.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"carga", "móvil", "cables", "base", "bobina", "cobre", "corriente", "sentido", "rápido",
            "campo", "magnético", "cambia", "encima", "variable", "atraviesa", "induce", "convertida",
            "cargando", "batería"}

COP = (215, 130, 70)       # copper
PAD = (60, 70, 90)
PHONE = (35, 42, 60)
FIELD = (120, 220, 255)
GREEN = (90, 210, 120)
ELE = (255, 176, 32)


def coil(E, d, cx, cy, rx, ry, turns=5, color=COP, w=7):
    for k in range(turns):
        f = 1 - k / (turns + 1)
        pts = [(cx + rx * f * math.cos(a / 40 * 2 * math.pi), cy + ry * f * math.sin(a / 40 * 2 * math.pi))
               for a in range(41)]
        E.line(d, pts, color, w)


def pad(E, d, cy=880):
    E.rrect(d, 200, cy - 40, 880, cy + 60, 30, PAD, outline=E.SIL_D, w=4)


def phone(E, d, cy=620, battery=None):
    E.rrect(d, 300, cy - 70, 780, cy + 50, 26, PHONE, outline=E.SIL, w=5)
    if battery is not None:
        bx, by = 870, 440
        E.rrect(d, bx - 65, by - 120, bx + 65, by + 120, 14, None, outline=E.WHITE, w=6)
        E.rrect(d, bx - 28, by - 142, bx + 28, by - 120, 6, E.WHITE)
        h = 220 * battery
        E.rrect(d, bx - 53, by + 108 - h, bx + 53, by + 108, 8, GREEN)


def field_lines(E, d, cx, y0, y1, u, strength=1.0):
    # loops of magnetic field rising from the pad coil; pulsing to show it keeps changing
    s = strength * (0.55 + 0.45 * math.sin(u * 9))
    col = E.mix((40, 60, 90), FIELD, max(0.15, abs(s)))
    for k in range(4):
        w = 60 + 70 * k
        top = y0 - (y0 - y1) * (0.55 + 0.15 * k) * (0.7 + 0.3 * abs(s))
        pts = []
        for n in range(31):
            t = n / 30 * math.pi
            pts.append((cx + w * math.cos(t), y0 - (y0 - top) * math.sin(t)))
        E.line(d, pts, col, 5)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: phone on pad, field pulsing, battery filling
        pad(E, d, 900)
        field_lines(E, d, 540, 870, 560, u)
        phone(E, d, 760, battery=0.35 + 0.5 * min(1.0, u / max(L, 0.1)))
    elif i == 1:  # copper coil inside the base
        k = E.ease(u / 0.8)
        E.rrect(d, 160, 520, 920, 1040, 40, PAD, outline=E.SIL_D, w=4)
        coil(E, d, 540, 780, 330 * (0.4 + 0.6 * k), 200 * (0.4 + 0.6 * k), turns=6)
        E.label(d, "BOBINA DE COBRE", 540, 420, 50, color=COP)
        E.label(d, "BASE", 540, 1100, 44, color=E.WHITE)
    elif i == 2:  # alternating current: direction keeps flipping
        E.rrect(d, 160, 520, 920, 1040, 40, PAD, outline=E.SIL_D, w=4)
        coil(E, d, 540, 780, 330, 200, turns=6)
        sgn = 1 if math.sin(u * 6) >= 0 else -1
        for k in range(12):
            a = 2 * math.pi * (k / 12 + sgn * u * 0.6)
            E.circle(d, 540 + 270 * math.cos(a), 780 + 165 * math.sin(a), 13, fill=ELE)
        if sgn > 0:
            E.arrow(d, 400, 420, 680, 420, ELE, 8, 30)
        else:
            E.arrow(d, 680, 420, 400, 420, ELE, 8, 30)
        E.label(d, "CAMBIA DE SENTIDO", 540, 1100, 46, color=E.AMB)
    elif i == 3:  # changing magnetic field
        pad(E, d, 900)
        coil(E, d, 540, 900, 300, 40, turns=4, w=6)
        field_lines(E, d, 540, 880, 420, u, strength=1.0)
        E.label(d, "CAMPO MAGNÉTICO", 540, 340, 50, color=FIELD)
        E.label(d, "VARIABLE", 540, 1060, 46, color=E.AMB)
    elif i == 4:  # phone has another coil just above
        pad(E, d, 960)
        coil(E, d, 540, 960, 300, 40, turns=4, w=6)
        y = 700 - 120 * (1 - E.ease(u / 0.8))
        E.rrect(d, 260, y - 120, 820, y + 70, 30, PHONE, outline=E.SIL, w=5)
        coil(E, d, 540, y - 20, 240, 50, turns=4, color=COP, w=6)
        E.label(d, "BOBINA DEL MÓVIL", 540, 400, 48, color=COP)
        E.label(d, "BASE", 540, 1080, 44, color=E.WHITE)
    elif i == 5:  # field through phone coil induces current
        pad(E, d, 960)
        coil(E, d, 540, 960, 300, 40, turns=4, w=6)
        E.rrect(d, 260, 580, 820, 770, 30, PHONE, outline=E.SIL, w=5)
        field_lines(E, d, 540, 940, 520, u, strength=1.0)
        coil(E, d, 540, 680, 240, 50, turns=4, color=COP, w=6)
        for k in range(8):
            a = 2 * math.pi * (k / 8 + u * 0.5)
            E.circle(d, 540 + 210 * math.cos(a), 680 + 44 * math.sin(a), 11, fill=ELE)
        E.label(d, "CORRIENTE INDUCIDA", 540, 420, 48, color=E.AMB)
    elif i == 6:  # converted current charges the battery
        bx, by = 540, 720
        E.rrect(d, bx - 130, by - 260, bx + 130, by + 260, 24, None, outline=E.WHITE, w=8)
        E.rrect(d, bx - 55, by - 300, bx + 55, by - 260, 10, E.WHITE)
        lvl = 0.25 + 0.7 * E.ease(u / max(L, 0.1))
        h = 500 * lvl
        E.rrect(d, bx - 110, by + 240 - h, bx + 110, by + 240, 14, GREEN)
        for k in range(5):
            y = 1120 - ((u * 0.8 + k / 5) % 1.0) * 130
            E.circle(d, bx, y, 11, fill=ELE)
        E.label(d, "BATERÍA", 540, 360, 52, color=GREEN)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 0.8), ("pop", s[1] + 0.6), ("zip", s[2] + 0.4), ("whoosh", s[3] + 0.5, 0.8),
            ("pop", s[4] + 0.7), ("zip", s[5] + 0.4), ("click", s[6] + 0.6)]
