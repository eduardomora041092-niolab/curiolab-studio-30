"""Video 073 — ¿Cómo imprime una impresora de tinta?
Science: an inkjet printer moves a print head back and forth across the paper while the paper advances. The underside
of the head has many tiny nozzles, each fed from a small ink chamber. In thermal inkjet heads a tiny resistor heats the
ink for an instant, a vapour bubble forms and expands, and it pushes a droplet out of the nozzle; when the bubble
collapses, fresh ink refills the chamber. In piezoelectric heads a piezo crystal flexes when a voltage is applied,
squeezing the chamber and ejecting the droplet. The droplets are smaller than the thickness of a hair; many tiny dots
placed side by side, in a few ink colours, build up text and images.
(No exact nozzle counts, droplet volumes or speeds are claimed.)
"""
import math

ID = "073"
TITLE = "¿Cómo imprime una impresora de tinta?"
SUBTITLE = "CÓMO FUNCIONA"
LINES = [
    "¿Cómo imprime una impresora de tinta?",
    "Un cabezal se desliza sobre el papel de un lado a otro.",
    "Por debajo tiene muchísimas boquillas diminutas llenas de tinta.",
    "En unas, una resistencia calienta la tinta y forma una burbuja.",
    "La burbuja empuja y dispara una gota más fina que un cabello.",
    "En otras, un cristal piezoeléctrico se dobla y expulsa la gota.",
    "Miles de puntos juntos forman letras, fotos y colores.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"impresora", "tinta", "cabezal", "desliza", "papel", "boquillas", "diminutas", "resistencia", "calienta",
            "burbuja", "empuja", "dispara", "gota", "cabello", "cristal", "piezoeléctrico", "dobla", "expulsa",
            "puntos", "letras", "fotos", "colores"}

INK = (60, 200, 230)
MAG = (230, 70, 160)
YEL = (250, 220, 60)
PAPER = (240, 240, 232)


def paper(E, d, y0=760, y1=1150, x0=140, x1=940):
    E.rrect(d, x0, y0, x1, y1, 6, PAPER)


def head(E, d, x, y=600, w=220, h=130):
    E.rrect(d, x - w / 2, y - h / 2, x + w / 2, y + h / 2, 16, E.SIL_D, outline=E.SIL_H, w=3)
    for k, c in enumerate((INK, MAG, YEL)):
        E.rrect(d, x - w / 2 + 20 + k * 64, y - h / 2 + 18, x - w / 2 + 70 + k * 64, y + h / 2 - 30, 6, c)
    for k in range(7):
        E.circle(d, x - 75 + k * 25, y + h / 2 + 4, 5, fill=E.BG1)


def rail(E, d, y=600):
    E.line(d, [(110, y), (970, y)], E.SIL_D, 10)


def dots(E, d, n, y0=800, rows=8, cols=24):
    cnt = 0
    for r in range(rows):
        for c in range(cols):
            if cnt >= n: return
            col = (INK, MAG, YEL, E.BG1)[(r + c) % 4]
            E.circle(d, 180 + c * 31, y0 + r * 40, 11, fill=col); cnt += 1


def chamber(E, d, cx=540, top=360, bot=900, w=300):
    E.rrect(d, cx - w / 2 - 30, top, cx + w / 2 + 30, bot, 20, E.SIL_D)
    E.rrect(d, cx - w / 2, top + 30, cx + w / 2, bot - 60, 12, INK)
    E.rrect(d, cx - 22, bot - 62, cx + 22, bot, 4, INK)     # nozzle
    E.rrect(d, cx - w / 2 - 30, bot - 62, cx - 22, bot, 0, E.SIL_D)
    E.rrect(d, cx + 22, bot - 62, cx + w / 2 + 30, bot, 0, E.SIL_D)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: head already moving and dropping dots on paper
        paper(E, d)
        rail(E, d)
        x = 540 + 300 * math.sin(u * 3.0)
        n = int(60 + u * 40)
        dots(E, d, n)
        head(E, d, x)
        for k in range(4):
            yy = 680 + ((k * 40 + u * 400) % 140)
            E.circle(d, x - 40 + k * 25, yy, 7, fill=(INK, MAG, YEL, INK)[k])
    elif i == 1:  # head slides left-right over the paper
        paper(E, d)
        rail(E, d)
        x = 540 + 320 * math.sin(u * 2.2)
        head(E, d, x)
        E.arrow(d, 400, 470, 180, 470, E.AMB, 9, 30)
        E.arrow(d, 680, 470, 900, 470, E.AMB, 9, 30)
        E.label(d, "CABEZAL", 540, 370, 56, color=E.AMB)
        E.label(d, "PAPEL", 540, 1000, 52, color=E.BG1)
    elif i == 2:  # underside: many tiny nozzles full of ink
        E.rrect(d, 160, 380, 920, 900, 24, E.SIL_D, outline=E.SIL_H, w=4)
        for r in range(6):
            for c in range(16):
                g = 0.5 + 0.5 * math.sin(u * 4 + r + c)
                E.circle(d, 215 + c * 44, 470 + r * 72, 12, fill=E.mix(E.BG1, INK, g))
        E.label(d, "BOQUILLAS", 540, 990, 56, color=E.AMB)
    elif i == 3:  # thermal: resistor heats ink, bubble forms
        chamber(E, d)
        g = 0.5 + 0.5 * math.sin(u * 6)
        E.rrect(d, 430, 400, 650, 430, 6, E.mix(E.HOT_D, E.HOT, g))
        r = 30 + 70 * E.ease(u / (L * 0.8))
        E.circle(d, 540, 430 + r, r, fill=E.WHITE, outline=E.SIL_H, w=3)
        E.label(d, "RESISTENCIA", 540, 320, 48, color=E.HOT)
        E.label(d, "BURBUJA", 820, 640, 44, color=E.WHITE)
    elif i == 4:  # bubble pushes a droplet out of the nozzle
        chamber(E, d)
        E.rrect(d, 430, 400, 650, 430, 6, E.HOT)
        E.circle(d, 540, 560, 130, fill=E.WHITE, outline=E.SIL_H, w=3)
        k = (u * 0.9) % 1.0
        E.circle(d, 540, 930 + 220 * k, 14, fill=INK)
        E.arrow(d, 540, 700, 540, 820, E.AMB, 9, 30)
        E.line(d, [(720, 1060), (1000, 1060)], E.BRA, 26)   # a hair for scale (thicker than the drop)
        E.label(d, "CABELLO", 860, 1000, 40, color=E.BRA)
        E.label(d, "GOTA", 400, 1080, 44, color=INK)
    elif i == 5:  # piezo crystal bends and squeezes the chamber
        chamber(E, d)
        b = 40 * abs(math.sin(u * 4))
        pts = [(390, 420), (540, 420 + b * 2.0), (690, 420)]
        E.rrect(d, 380, 380, 700, 418, 6, E.AMB)
        E.line(d, pts, E.AMB, 18)
        k = (u * 1.1) % 1.0
        E.circle(d, 540, 930 + 220 * k, 14, fill=INK)
        E.label(d, "PIEZOELÉCTRICO", 540, 320, 46, color=E.AMB)
        E.arrow(d, 540, 560, 540, 700, E.AMB, 9, 30)
    elif i == 6:  # thousands of dots build letters and colours
        paper(E, d, 360, 1150)
        n = int(80 + u * 120)
        cnt = 0
        for r in range(9):
            for c in range(24):
                if cnt >= n: break
                col = (INK, MAG, YEL)[(c // 8) % 3]
                E.circle(d, 180 + c * 31, 900 + r * 26, 9, fill=col); cnt += 1
        E.label(d, "ABC", 540, 560, 150, color=E.BG1)
        E.label(d, "PUNTOS", 540, 760, 48, color=E.HOT)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("zip", s[0] + 0.2), ("whoosh", s[1] + 0.4, 0.8), ("click", s[2] + 0.6), ("pop", s[3] + 0.8),
            ("pop", s[4] + 0.6), ("click", s[5] + 0.6), ("zip", s[6] + 0.5)]
