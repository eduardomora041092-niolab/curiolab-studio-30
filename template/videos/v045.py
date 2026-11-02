"""Video 045 — ¿Cómo cambia de color un camaleón?
Science: chameleon skin has a layer of cells (iridophores) containing guanine nanocrystals arranged in an ordered
lattice. The lattice selectively reflects light of certain colours (structural colour, not a new pigment). In a
relaxed animal the crystals are closer together and reflect short wavelengths (blue); a yellow pigment in the upper
layer makes that blue look green. When the animal is excited the spacing between crystals increases and longer
wavelengths (yellow, orange) are reflected, so the skin changes colour.
(No nanometre spacings, deep iridophore layer or reasons for the change are claimed.)
"""
import math

ID = "045"
TITLE = "¿Cómo cambia de color un camaleón?"
SUBTITLE = "CIENCIA EN 30 SEGUNDOS"
LINES = [
    "¿Cómo cambia de color un camaleón?",
    "Su piel tiene una capa con diminutos cristales ordenados.",
    "Esos cristales reflejan la luz de un color concreto.",
    "Relajado, los cristales están juntos y reflejan azul.",
    "Un pigmento amarillo encima hace que se vea verde.",
    "Excitado, los cristales se separan un poco más.",
    "Así reflejan amarillo o naranja, y la piel cambia.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"cambia", "color", "camaleón", "piel", "capa", "cristales", "ordenados", "reflejan", "luz",
            "juntos", "azul", "pigmento", "amarillo", "verde", "separan", "naranja"}

GREEN = (70, 190, 90)
BLUEC = (60, 130, 255)
YEL = (250, 215, 60)
ORANGE = (255, 140, 40)
BRANCH = (120, 80, 50)


def chameleon(E, d, x, y, col, s=1.0, u=0.0):
    E.line(d, [(x - 330 * s, y + 95 * s), (x + 330 * s, y + 95 * s)], BRANCH, int(26 * s))
    for lx in (-110, 90):
        E.line(d, [(x + lx * s, y + 40 * s), (x + (lx - 20) * s, y + 95 * s)], col, int(20 * s))
    E.circle(d, x - 230 * s, y + 10 * s, 50 * s, outline=col, w=int(18 * s))   # curled tail
    E.poly(d, [(x - 200 * s, y + 10 * s), (x - 170 * s, y - 20 * s), (x - 170 * s, y + 40 * s)], fill=col)
    E.rrect(d, x - 180 * s, y - 70 * s, x + 170 * s, y + 50 * s, int(60 * s), col)
    E.poly(d, [(x + 140 * s, y - 80 * s), (x + 290 * s, y - 10 * s), (x + 140 * s, y + 40 * s)], fill=col)
    E.circle(d, x + 190 * s, y - 30 * s, 24 * s, fill=E.WHITE)
    E.circle(d, x + 190 * s + 6 * math.sin(u * 3) * s, y - 30 * s, 10 * s, fill=E.BG1)


def cycle(E, u):
    t = 0.5 + 0.5 * math.sin(u * 2.2)
    return E.mix(GREEN, ORANGE, t)


def lattice(E, d, cx, cy, gap, n=5, col=None):
    col = col or E.SIL_H
    for r in range(n):
        for c in range(n):
            x = cx + (c - (n - 1) / 2) * gap
            y = cy + (r - (n - 1) / 2) * gap * 0.7
            E.rrect(d, x - 18, y - 6, x + 18, y + 6, 4, col)


def skin(E, d, pig=True):
    E.rrect(d, 120, 470, 960, 1120, 30, E.mix(E.BG2, (200, 150, 120), 0.25))
    if pig:
        E.rrect(d, 120, 470, 960, 560, 30, E.mix(E.BG2, YEL, 0.85))


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: chameleon shifting colour
        chameleon(E, d, 560, 760, cycle(E, u), s=1.0, u=u)
        E.pill(d, "CAMBIA DE COLOR", 540, 1080, 42)
    elif i == 1:  # skin layer with tiny ordered crystals
        skin(E, d)
        lattice(E, d, 540, 840, 90)
        E.label(d, "PIEL", 220, 420, 44, color=E.SIL_H)
        E.pill(d, "CRISTALES ORDENADOS", 540, 1060, 38)
    elif i == 2:  # crystals reflect light of one colour
        skin(E, d, pig=False)
        lattice(E, d, 640, 860, 80)
        ph = u * 8
        E.wave(d, 180, 360, 520, 760, 50, 14, E.WHITE, 6, ph)
        E.wave(d, 560, 760, 900, 360, 50, 14, E.AMB, 6, ph)
        E.label(d, "LUZ", 200, 310, 44, color=E.WHITE)
        E.label(d, "UN COLOR", 880, 310, 44, color=E.AMB)
    elif i == 3:  # relaxed: crystals close, reflect blue
        skin(E, d, pig=False)
        lattice(E, d, 640, 860, 60)
        ph = u * 8
        E.wave(d, 180, 360, 560, 780, 50, 14, E.WHITE, 6, ph)
        E.wave(d, 600, 780, 900, 360, 36, 14, BLUEC, 6, ph)
        E.label(d, "JUNTOS", 640, 1060, 46, color=E.SIL_H)
        E.pill(d, "AZUL", 880, 310, 44, bg=BLUEC, fg=E.WHITE)
    elif i == 4:  # yellow pigment above makes it look green
        skin(E, d, pig=True)
        lattice(E, d, 540, 870, 60)
        E.pill(d, "PIGMENTO AMARILLO", 540, 515, 34, bg=YEL, fg=E.BG1)
        E.label(d, "AZUL", 260, 1060, 44, color=BLUEC)
        E.label(d, "+ AMARILLO", 540, 1060, 44, color=YEL)
        k = min(1, u / (L * 0.5))
        E.circle(d, 540, 340, 60, fill=E.mix(BLUEC, GREEN, k))
        E.label(d, "VERDE", 820, 340, 50, color=GREEN)
    elif i == 5:  # excited: crystals move apart
        skin(E, d, pig=False)
        k = E.ease(min(1, u / (L * 0.6)))
        gap = 60 + 40 * k
        lattice(E, d, 540, 820, gap)
        for sx, sy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            E.arrow(d, 540 + sx * 250, 820 + sy * 190, 540 + sx * (300 + 40 * k), 820 + sy * (220 + 30 * k), E.AMB, 6, 22)
        E.label(d, "SE SEPARAN", 540, 400, 50, color=E.AMB)
    elif i == 6:  # reflect yellow/orange; skin changes
        skin(E, d, pig=False)
        lattice(E, d, 400, 860, 95, n=4)
        ph = u * 8
        E.wave(d, 640, 820, 940, 470, 70, 14, ORANGE, 6, ph)
        chameleon(E, d, 760, 1000, ORANGE, s=0.35, u=u)
        E.label(d, "AMARILLO / NARANJA", 540, 380, 44, color=ORANGE)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.05, 1.0), ("pop", s[1] + 0.6), ("zip", s[2] + 0.5, 0.8), ("pop", s[3] + 1.0),
            ("click", s[4] + 1.0), ("zip", s[5] + 0.5, 1.0), ("whoosh", s[6] + 0.4, 1.2)]
