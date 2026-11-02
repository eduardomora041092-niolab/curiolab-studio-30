"""Video 043 — ¿Cómo hace chispa un encendedor de clic?
Science: pressing the button of a piezo lighter compresses a spring inside. At the end of the stroke the spring is
released and fires a small hammer, which strikes a piezoelectric crystal. When a piezoelectric material is suddenly
squeezed it produces a high voltage between its faces. Wires lead that voltage to two electrodes separated by a small
gap, where it jumps as a spark. The spark ignites the gas released through the nozzle at the same moment.
(No voltages, materials or gas types are claimed.)
"""
import math

ID = "043"
TITLE = "¿Cómo hace chispa un encendedor de clic?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo hace chispa un encendedor de clic?",
    "Al pulsar el botón, comprimes un muelle que hay por dentro.",
    "El muelle se suelta y lanza un pequeño martillo.",
    "El martillo golpea con fuerza un cristal piezoeléctrico.",
    "Al deformarse, el cristal genera un voltaje muy alto.",
    "Ese voltaje salta entre dos puntas como una chispa.",
    "La chispa enciende el gas que sale por la boquilla a la vez.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"chispa", "encendedor", "clic", "botón", "muelle", "martillo", "golpea", "cristal",
            "piezoeléctrico", "voltaje", "alto", "puntas", "enciende", "gas"}

SPARK = (190, 225, 255)
FLAME = (255, 120, 40)


def spark(E, d, x0, y0, x1, y1, u, w=6):
    pts = [(x0, y0)]
    n = 6
    for k in range(1, n):
        t = k / n
        off = 18 * math.sin(u * 40 + k * 2.3)
        pts.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + off))
    pts.append((x1, y1))
    E.line(d, pts, SPARK, w)
    E.line(d, pts, E.WHITE, max(2, w - 3))


def flame(E, d, x, y, u, s=1.0):
    h = (120 + 20 * math.sin(u * 11)) * s
    E.poly(d, [(x, y - 40 * s), (x - h, y - 10 * s + 10 * math.sin(u * 7)), (x, y + 40 * s)], fill=FLAME)
    E.poly(d, [(x, y - 20 * s), (x - h * 0.55, y), (x, y + 20 * s)], fill=E.AMB)


def body(E, d):
    # cutaway lighter: barrel to the left, handle on the right
    E.rrect(d, 160, 640, 300, 700, 14, E.SIL_D)       # barrel
    E.rrect(d, 300, 600, 920, 780, 30, E.mix(E.BG2, E.SIL_D, 0.6), outline=E.SIL, w=3)
    E.rrect(d, 120, 650, 170, 690, 10, E.SIL)          # nozzle


def button(E, d, press):
    y = 560 + 34 * press
    E.rrect(d, 700, y, 820, y + 50, 14, E.HOT)


def spring(E, d, x0, x1, y=690, coils=7, col=None):
    col = col or E.SIL_H
    pts = []
    for k in range(coils * 2 + 1):
        x = x0 + (x1 - x0) * k / (coils * 2)
        pts.append((x, y + (-26 if k % 2 else 26)))
    E.line(d, pts, col, 5)


def crystal(E, d, glow=0.0, squeeze=0.0):
    c = E.mix(E.BLUE, E.COLD, glow)
    E.rrect(d, 430 + 8 * squeeze, 640, 540, 740, 10, c, outline=E.WHITE, w=3)


def hammer(E, d, x):
    E.rrect(d, x, 650, x + 70, 730, 10, E.AMB)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: lighter clicking, sparks and flame at the tip
        body(E, d)
        button(E, d, 0.5 + 0.5 * math.sin(u * 12))
        flame(E, d, 120, 670, u, s=1.1)
        spark(E, d, 110, 640, 110, 700, u)
        E.pill(d, "CLIC", 600, 900, 46)
    elif i == 1:  # button compresses a spring
        body(E, d)
        k = E.ease(min(1, u / (L * 0.6)))
        button(E, d, k)
        crystal(E, d)
        hammer(E, d, 560)
        spring(E, d, 630, 880 - 150 * k)
        E.arrow(d, 760, 470, 760, 545, E.HOT, 7, 24)
        E.label(d, "MUELLE", 760, 880, 46, color=E.SIL_H)
    elif i == 2:  # spring released, launches hammer
        body(E, d)
        button(E, d, 1)
        crystal(E, d)
        k = E.ease(min(1, u / (L * 0.5)))
        hx = 700 - 160 * k
        hammer(E, d, hx)
        spring(E, d, hx + 70, 880)
        E.arrow(d, hx + 30, 850, hx - 80, 850, E.AMB, 7, 24)
        E.label(d, "MARTILLO", 600, 420, 48, color=E.AMB)
    elif i == 3:  # hammer hits the crystal
        body(E, d)
        button(E, d, 1)
        crystal(E, d, squeeze=1)
        hammer(E, d, 540)
        spring(E, d, 610, 880)
        f = (u * 3) % 1
        for a in range(6):
            ang = a * math.pi / 3 + 0.3
            E.line(d, [(540 + 40 * math.cos(ang), 690 + 40 * math.sin(ang)),
                       (540 + (70 + 40 * f) * math.cos(ang), 690 + (70 + 40 * f) * math.sin(ang))], E.WHITE, 5)
        E.label(d, "CRISTAL", 485, 420, 50, color=E.COLD)
        E.label(d, "PIEZOELÉCTRICO", 485, 490, 44, color=E.COLD)
        E.arrow(d, 485, 530, 485, 625, E.COLD, 6, 22)
    elif i == 4:  # deformed crystal generates high voltage
        body(E, d)
        crystal(E, d, glow=0.5 + 0.5 * math.sin(u * 8), squeeze=1)
        hammer(E, d, 540)
        for k in range(3):
            E.label(d, "+", 445, 660 + 30 * k, 34, color=E.HOT)
            E.label(d, "−", 525, 660 + 30 * k, 34, color=E.COLD)
        E.line(d, [(450, 640), (450, 560), (240, 560), (240, 640)], E.HOT, 5)
        E.line(d, [(520, 740), (520, 840), (240, 840), (240, 700)], E.COLD, 5)
        E.pill(d, "VOLTAJE MUY ALTO", 540, 980, 42, bg=E.HOT, fg=E.WHITE)
    elif i == 5:  # voltage jumps between two tips as a spark
        E.rrect(d, 300, 600, 920, 780, 30, E.mix(E.BG2, E.SIL_D, 0.6), outline=E.SIL, w=3)
        E.line(d, [(450, 640), (450, 540), (300, 540)], E.HOT, 6)
        E.line(d, [(520, 740), (520, 860), (300, 860)], E.COLD, 6)
        E.poly(d, [(300, 530), (300, 550), (220, 640)], fill=E.SIL_H)
        E.poly(d, [(300, 850), (300, 870), (220, 760)], fill=E.SIL_H)
        spark(E, d, 220, 645, 220, 755, u, w=8)
        crystal(E, d, glow=0.6, squeeze=1)
        E.label(d, "CHISPA", 220, 960, 52, color=SPARK)
    elif i == 6:  # spark ignites the gas released at the same time
        body(E, d)
        k = min(1, u / (L * 0.4))
        for j in range(8):
            f = (u * 1.2 + j / 8) % 1
            E.circle(d, 300 - 160 * f, 670 + 12 * math.sin(j * 1.7 + u * 4), 10, fill=E.mix(E.BG2, E.SIL, 0.7))
        spark(E, d, 110, 640, 110, 700, u)
        if k > 0.3:
            flame(E, d, 120, 670, u, s=1.2)
        E.label(d, "GAS", 380, 520, 46, color=E.SIL_H)
        E.arrow(d, 360, 560, 290, 640, E.SIL_H, 6, 22)
        E.pill(d, "SE ENCIENDE", 540, 940, 44, bg=E.HOT, fg=E.WHITE)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("click", s[0] + 0.05), ("click", s[1] + 0.8), ("whoosh", s[2] + 0.3, 0.8), ("pop", s[3] + 0.4),
            ("zip", s[4] + 0.4, 1.0), ("click", s[5] + 0.5), ("whoosh", s[6] + 0.5, 1.2)]
