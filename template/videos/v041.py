"""Video 041 — ¿Cómo funciona una cafetera italiana?
Science: a moka pot has three parts: a lower boiler with water, a funnel-shaped filter basket holding ground coffee,
and an upper collecting chamber. When the boiler is heated, water starts to evaporate; the water vapour and the air
trapped in the top of the boiler raise the pressure there. That pressure pushes the hot water up through the funnel
tube, through the bed of ground coffee in the filter, and then up the central column, from which the coffee pours
into the upper chamber. (No pressures in bar, temperatures or comparisons with espresso machines are claimed; the
safety valve is not discussed.)
"""
import math

ID = "041"
TITLE = "¿Cómo funciona una cafetera italiana?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo funciona una cafetera italiana?",
    "Tiene tres partes: depósito de agua, filtro con café y jarra.",
    "Al calentar el depósito, el agua empieza a evaporarse.",
    "El aire y el vapor atrapados arriba aumentan la presión.",
    "Esa presión empuja el agua hacia arriba por un embudo.",
    "El agua caliente atraviesa el café molido del filtro.",
    "Sale por la columna central y llena la jarra de café.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"cafetera", "italiana", "depósito", "agua", "filtro", "café", "jarra", "calentar", "evaporarse",
            "aire", "vapor", "atrapados", "presión", "empuja", "embudo", "caliente", "molido", "columna", "central"}

WATER = (90, 170, 255)
COFFEE = (120, 72, 40)
GROUNDS = (90, 55, 30)
FLAME = (255, 120, 40)
CX = 540

def flame(E, d, u, y=1100):
    for k in range(5):
        x = CX - 120 + 60 * k
        h = 50 + 18 * math.sin(u * 9 + k * 1.7)
        E.poly(d, [(x - 20, y), (x, y - h), (x + 20, y)], fill=FLAME)
        E.poly(d, [(x - 9, y), (x, y - h * 0.55), (x + 9, y)], fill=E.AMB)

# section view geometry
BOIL = (380, 760, 700, 1040)      # lower boiler
FILT = (400, 680, 680, 760)       # filter basket
JAR = (370, 360, 710, 660)        # upper jar

def body(E, d):
    x0, y0, x1, y1 = BOIL
    E.poly(d, [(x0, y0), (x1, y0), (x1 + 20, y1), (x0 - 20, y1)], fill=E.SIL_D)
    E.poly(d, [(x0 + 18, y0 + 14), (x1 - 18, y0 + 14), (x1, y1 - 16), (x0, y1 - 16)], fill=E.CAV)
    x0, y0, x1, y1 = JAR
    E.poly(d, [(x0 + 20, y0), (x1 - 20, y0), (x1, y1), (x0, y1)], fill=E.SIL_D)
    E.poly(d, [(x0 + 36, y0 + 14), (x1 - 36, y0 + 14), (x1 - 16, y1 - 10), (x0 + 16, y1 - 10)], fill=E.CAV)
    E.rrect(d, x1, y0 + 60, x1 + 70, y0 + 90, 10, E.SIL_D)    # handle top
    E.rrect(d, x1 + 40, y0 + 60, x1 + 70, y0 + 220, 10, E.SIL_D)
    E.rrect(d, 360, 660, 720, 690, 8, E.SIL)                  # joint

def filter_(E, d, wet=0.0):
    x0, y0, x1, y1 = FILT
    E.rrect(d, x0, y0, x1, y1, 10, E.SIL)
    E.rrect(d, x0 + 12, y0 + 10, x1 - 12, y1 - 10, 8, E.mix(GROUNDS, COFFEE, wet))
    E.rrect(d, CX - 18, y1, CX + 18, 960, 6, E.SIL)           # funnel tube
    E.rrect(d, CX - 10, y1, CX + 10, 958, 4, E.CAV)

def column(E, d):
    E.rrect(d, CX - 16, 450, CX + 16, 690, 6, E.SIL)
    E.rrect(d, CX - 8, 450, CX + 8, 688, 4, E.CAV)

def water(E, d, level, col=WATER):
    x0, y0, x1, y1 = BOIL
    top = y1 - 16 - (y1 - y0 - 30) * level
    E.poly(d, [(x0 + 4, top), (x1 - 4, top), (x1, y1 - 16), (x0, y1 - 16)], fill=E.mix(E.BG2, col, 0.75))
    return top

def jar_fill(E, d, level):
    if level <= 0: return
    x0, y0, x1, y1 = JAR
    top = y1 - 10 - (y1 - y0 - 40) * level
    E.poly(d, [(x0 + 16 + 20 * (1 - (top - y0) / (y1 - y0)), top), (x1 - 16 - 20 * (1 - (top - y0) / (y1 - y0)), top),
               (x1 - 16, y1 - 10), (x0 + 16, y1 - 10)], fill=COFFEE)

def spout(E, d, u, col=COFFEE):
    for k in range(5):
        f = (u * 1.5 + k / 5) % 1
        side = -1 if k % 2 else 1
        x = CX + side * 70 * f
        y = 450 - 30 * math.sin(math.pi * f) + 160 * f * f
        E.circle(d, x, y, 10, fill=col)

def rising(E, d, u, y_from, y_to, col):
    for k in range(5):
        f = (u * 1.2 + k / 5) % 1
        E.circle(d, CX, y_from - (y_from - y_to) * f, 8, fill=col)

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: coffee already spurting from the column into the jar
        flame(E, d, u)
        body(E, d); filter_(E, d, wet=1.0); column(E, d)
        water(E, d, 0.3)
        jar_fill(E, d, 0.25 + 0.15 * min(1, u / L))
        spout(E, d, u)
        E.pill(d, "CAFETERA ITALIANA", 540, 318, 36)
    elif i == 1:  # three parts
        body(E, d); filter_(E, d); column(E, d)
        water(E, d, 0.75)
        k = u / L
        E.label(d, "JARRA", 860, 470, 44, color=E.SIL_H)
        if k > 0.3: E.label(d, "FILTRO", 860, 720, 44, color=E.BRA)
        if k > 0.55: E.label(d, "DEPÓSITO", 180, 900, 44, color=WATER)
        E.label(d, "CAFÉ", 540, 720, 30, color=E.WHITE)
    elif i == 2:  # heating the boiler, water starts to evaporate
        flame(E, d, u)
        body(E, d); filter_(E, d); column(E, d)
        top = water(E, d, 0.75)
        for k in range(8):
            f = (u * 1.1 + k * 0.125) % 1
            E.circle(d, 410 + (k * 37) % 260, 1010 - (1010 - top) * f, 6 + 4 * f, outline=E.WHITE, w=3)
        for k in range(4):
            f = (u * 0.7 + k / 4) % 1
            E.circle(d, 420 + 70 * k, top - 10 - 40 * f, 10, fill=E.mix(E.BG1, E.SIL_H, 1 - f))
        E.label(d, "CALOR", 540, 1150, 40, color=FLAME)
        E.label(d, "VAPOR", 180, 800, 44, color=E.SIL_H)
    elif i == 3:  # air and steam trapped above the water raise the pressure
        flame(E, d, u)
        body(E, d); filter_(E, d); column(E, d)
        top = water(E, d, 0.7)
        for k in range(10):
            a = k * 2.4 + u * 3
            E.circle(d, 540 + 120 * math.sin(a), (770 + top) / 2 + 12 * math.cos(a * 1.7), 9, fill=E.SIL_H)
        for x in (420, 660):
            E.arrow(d, x, 800, x, top - 4, E.HOT, 7, 22)
        E.pill(d, "MÁS PRESIÓN", 180, 820, 36, bg=E.HOT, fg=E.WHITE)
    elif i == 4:  # pressure pushes water up the funnel
        flame(E, d, u)
        body(E, d); filter_(E, d); column(E, d)
        k = min(1, u / L)
        top = water(E, d, 0.65 - 0.15 * k)
        E.rrect(d, CX - 10, 760, CX + 10, 958, 4, E.mix(E.BG2, WATER, 0.9))
        rising(E, d, u, 950, 770, E.WHITE)
        for x in (420, 660):
            E.arrow(d, x, 790, x, top + 30, E.HOT, 7, 22)
        E.label(d, "EMBUDO", 180, 860, 44, color=WATER)
        E.arrow(d, 290, 860, 515, 860, WATER, 6, 22)
    elif i == 5:  # hot water passes through the ground coffee
        body(E, d); filter_(E, d, wet=E.ease(min(1, u / L))); column(E, d)
        water(E, d, 0.45)
        E.rrect(d, CX - 10, 760, CX + 10, 958, 4, E.mix(E.BG2, WATER, 0.9))
        for k in range(6):
            f = (u * 1.0 + k / 6) % 1
            E.circle(d, 430 + 44 * k, 750 - 60 * f, 8, fill=E.mix(WATER, COFFEE, f))
        E.label(d, "CAFÉ MOLIDO", 910, 720, 38, color=E.BRA)
        E.arrow(d, 760, 720, 692, 720, E.BRA, 6, 22)
    elif i == 6:  # out of the central column into the jar
        body(E, d); filter_(E, d, wet=1.0); column(E, d)
        water(E, d, 0.3)
        E.rrect(d, CX - 8, 452, CX + 8, 688, 4, COFFEE)
        jar_fill(E, d, 0.2 + 0.5 * E.ease(min(1, u / L)))
        spout(E, d, u)
        E.label(d, "COLUMNA CENTRAL", 240, 470, 34, color=E.SIL_H)
        E.arrow(d, 240, 500, 515, 470, E.SIL_H, 5, 20)
        E.label(d, "CAFÉ", 860, 560, 46, color=E.BRA)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.05, 1.0), ("pop", s[1] + 0.6), ("zip", s[2] + 0.5, 0.8), ("click", s[3] + 0.8),
            ("whoosh", s[4] + 0.5, 1.0), ("pop", s[5] + 0.8), ("whoosh", s[6] + 0.3, 1.2)]
