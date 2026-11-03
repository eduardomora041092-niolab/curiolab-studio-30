"""Video 048 — ¿Cómo se forma el granizo?
Science: hail forms inside tall thunderstorm clouds (cumulonimbus). High up in the cloud the air is well below
freezing even in summer. There, many water droplets remain liquid below 0 °C (supercooled). Strong updrafts carry
small ice particles (embryos) upward; when these collide with supercooled droplets, the droplets freeze onto them, so
the hailstone grows in layers. When it becomes too heavy for the updraft to hold it up, it falls to the ground as hail.
(No sizes, temperatures, speeds or the "up-and-down recycling" model are claimed.)
"""
import math

ID = "048"
TITLE = "¿Cómo se forma el granizo?"
SUBTITLE = "CIENCIA EN 30 SEGUNDOS"
LINES = [
    "¿Cómo puede caer hielo del cielo en pleno verano?",
    "El granizo nace en nubes de tormenta muy altas.",
    "Arriba hace mucho frío, aunque abajo sea verano.",
    "Allí hay gotitas de agua muy frías que siguen líquidas.",
    "Fuertes corrientes de aire suben pequeñas bolitas de hielo.",
    "Al chocar con esas gotitas, se congelan encima y la bola crece capa a capa.",
    "Cuando pesa demasiado para que el aire la sostenga, cae como granizo.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"hielo", "cielo", "verano", "granizo", "nubes", "tormenta", "altas", "frío", "gotitas", "agua",
            "líquidas", "corrientes", "aire", "suben", "bolitas", "congelan", "crece", "capa", "pesa", "cae"}

CLOUD = (150, 160, 180)
CLOUD_D = (95, 105, 125)
ICE = (215, 240, 255)
DROP = (90, 170, 255)
GRASS = (70, 160, 70)
SUN = (255, 210, 60)


def cloud(E, d, x=540, y=560, s=1.0, col=CLOUD):
    E.rrect(d, x - 380 * s, y - 60 * s, x + 380 * s, y + 70 * s, int(40 * s), col)   # anvil top
    E.rrect(d, x - 220 * s, y, x + 220 * s, y + 420 * s, int(80 * s), col)           # tower
    for k, (dx, r) in enumerate(((-200, 110), (0, 140), (200, 110))):
        E.circle(d, x + dx * s, y + 430 * s, r * s, fill=col)


def ground(E, d):
    E.rrect(d, 60, 1110, 1020, 1185, 10, GRASS)


def stone(E, d, x, y, layers=1, r0=10):
    for k in range(layers, 0, -1):
        E.circle(d, x, y, r0 + 9 * k, fill=E.mix(ICE, E.WHITE, 0.5 if k % 2 else 0.0), outline=E.mix(ICE, E.BG1, 0.3), w=2)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: hail falling on a summer day
        E.circle(d, 900, 330, 60, fill=SUN)
        cloud(E, d, 470, 360, s=0.7, col=CLOUD_D)
        ground(E, d)
        for j in range(14):
            f = (u * 0.9 + j / 14) % 1
            x = 200 + (j * 73) % 560
            stone(E, d, x, 700 + 400 * f, 1, 6)
        E.pill(d, "GRANIZO", 800, 1060, 42)
    elif i == 1:  # tall thunderstorm cloud
        cloud(E, d, 540, 360, s=1.0, col=CLOUD_D)
        ground(E, d)
        k = E.ease(min(1, u / (L * 0.6)))
        E.arrow(d, 960, 1000, 960, 1000 - 620 * k, E.AMB, 6, 24)
        E.label(d, "MUY ALTA", 880, 1050, 44, color=E.AMB)
    elif i == 2:  # cold above, warm below
        cloud(E, d, 540, 360, s=1.0)
        ground(E, d)
        E.pill(d, "MUCHO FRÍO", 540, 330, 44, bg=E.COLD, fg=E.BG1)
        E.circle(d, 900, 1000, 50, fill=SUN)
        E.label(d, "VERANO", 540, 1060, 46, color=E.HOT)
    elif i == 3:  # supercooled droplets still liquid
        cloud(E, d, 540, 360, s=1.0)
        for j in range(18):
            x = 380 + (j * 53) % 330
            y = 420 + (j * 97) % 330 + 8 * math.sin(u * 3 + j)
            E.circle(d, x, y, 12, fill=DROP)
        E.pill(d, "AGUA LÍQUIDA BAJO 0 °C", 540, 920, 36, bg=DROP, fg=E.BG1)
    elif i == 4:  # updrafts lift small ice pellets
        cloud(E, d, 540, 360, s=1.0)
        for x in (420, 540, 660):
            for j in range(3):
                f = (u * 0.8 + j / 3) % 1
                E.arrow(d, x, 1000 - 500 * f, x, 940 - 500 * f, E.AMB, 6, 20)
        for j in range(5):
            f = (u * 0.5 + j / 5) % 1
            stone(E, d, 480 + 30 * j, 900 - 450 * f, 1, 4)
        E.label(d, "CORRIENTES QUE SUBEN", 540, 1080, 40, color=E.AMB)
    elif i == 5:  # droplets freeze on, hailstone grows layer by layer
        cloud(E, d, 540, 360, s=1.0)
        layers = 1 + int(min(4, u / (L / 5)))
        stone(E, d, 540, 640, layers, 18)
        for j in range(8):
            a = j * math.pi / 4 + u
            r = 220 - (u * 120 + j * 20) % 140
            E.circle(d, 540 + r * math.cos(a), 640 + r * math.sin(a), 10, fill=DROP)
        E.label(d, "CAPA A CAPA", 540, 1060, 46, color=ICE)
    elif i == 6:  # too heavy: falls
        cloud(E, d, 540, 360, s=1.0, col=CLOUD_D)
        ground(E, d)
        k = E.ease(min(1, u / (L * 0.8)))
        y = 700 + 360 * k
        stone(E, d, 540, y, 4, 14)
        E.arrow(d, 680, 700, 680, 760, E.AMB, 6, 20)
        E.arrow(d, 400, 700 + 200 * k, 400, 860 + 200 * k, E.WHITE, 8, 26)
        E.label(d, "PESA DEMASIADO", 760, 960, 44, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.05, 1.0), ("pop", s[1] + 0.6), ("zip", s[2] + 0.5, 0.8), ("pop", s[3] + 0.8),
            ("whoosh", s[4] + 0.4, 1.2), ("pop", s[5] + 1.0), ("zip", s[6] + 0.6, 1.0)]
