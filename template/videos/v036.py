"""Video 036 — ¿Por qué se empaña el espejo del baño?
Science: hot shower water evaporates, so the bathroom air fills with water vapour. Water vapour is an invisible gas
mixed with the air (the visible "steam" is already tiny droplets). The mirror is colder than that warm, humid air.
Air touching the cold glass cools down; cooler air can hold less water vapour, so part of the vapour condenses into
tiny liquid droplets on the surface. Those droplets scatter light in all directions instead of reflecting it as a
smooth mirror, so we see a white layer instead of a clear reflection. (No temperatures, humidity values or dew
point figures are claimed; anti-fog products are not discussed.)
"""
import math, random

ID = "036"
TITLE = "¿Por qué se empaña el espejo del baño?"
SUBTITLE = "CURIOSIDADES DE LA CIENCIA"
LINES = [
    "¿Por qué se empaña el espejo del baño?",
    "El agua caliente de la ducha se evapora y llena el aire de vapor.",
    "Ese vapor es un gas invisible, mezclado con el aire.",
    "El espejo está más frío que ese aire caliente y húmedo.",
    "Al tocarlo, el aire se enfría y el vapor se condensa.",
    "Se forman gotitas diminutas que desvían la luz en todas direcciones.",
    "Por eso ves una capa blanca y no tu reflejo.",
    "Sígueme para más curiosidades de la ciencia.",
]
KEYWORDS = {"empaña", "espejo", "baño", "agua", "caliente", "ducha", "aire", "vapor", "gas", "invisible",
            "frío", "húmedo", "enfría", "evapora", "direcciones", "condensa", "gotitas", "diminutas", "luz", "capa", "blanca", "reflejo"}

GLASS, GLASS_H = (120, 160, 190), (175, 205, 225)
FOG = (215, 222, 230)
WATER = (90, 170, 255)
rnd = random.Random(36)
DROPS = [(rnd.random(), rnd.random(), rnd.random()) for _ in range(420)]

def mirror(E, d, x0, y0, x1, y1, fog=0.0, reflect=True):
    E.rrect(d, x0 - 16, y0 - 16, x1 + 16, y1 + 16, 18, E.SIL_D)
    E.rrect(d, x0, y0, x1, y1, 10, GLASS)
    E.line(d, [(x0 + 30, y1 - 60), (x0 + 120, y0 + 40)], GLASS_H, 10)
    if reflect:   # a generic reflected object: a cup with a toothbrush
        cx, cy = (x0 + x1) / 2, y1 - 40
        c = E.mix(E.BLUE, GLASS, fog)
        E.rrect(d, cx - 45, cy - 120, cx + 45, cy, 14, c)
        E.line(d, [(cx + 10, cy - 110), (cx + 40, cy - 230)], E.mix(E.AMB, GLASS, fog), 12)
    if fog > 0:
        n = int(len(DROPS) * min(1.0, fog))
        for fx, fy, fr in DROPS[:n]:
            E.circle(d, x0 + 8 + fx * (x1 - x0 - 16), y0 + 8 + fy * (y1 - y0 - 16), 10 + 12 * fr, fill=E.mix(GLASS, FOG, 0.55 + 0.45 * fog))

def shower(E, d, u, x, y, steam=True):
    E.rrect(d, x - 70, y - 30, x + 70, y + 10, 10, E.SIL)
    E.line(d, [(x, y - 30), (x, y - 120), (x - 120, y - 120)], E.SIL_D, 14)
    for k in range(14):   # falling water
        f = (u * 1.6 + k / 14) % 1
        xx = x - 60 + (k * 37) % 120
        E.line(d, [(xx, y + 20 + f * 520), (xx - 4, y + 60 + f * 520)], WATER, 6)
    if steam:
        for k in range(8):
            f = (u * 0.35 + k / 8) % 1
            sx = x - 80 + (k * 53) % 180 + 30 * math.sin(u * 1.5 + k)
            E.circle(d, sx, y + 560 - f * 560, 30 + 30 * f, fill=E.mix(E.BG2, FOG, 0.35 + 0.45 * (1 - f)))

def molecules(E, d, u, x0, y0, x1, y1, n, color, r=9, seed=0, speed=1.0, vx=0.0):
    g = random.Random(seed)
    for _ in range(n):
        px, py, ph, sp = g.random(), g.random(), g.random() * 6.28, 0.5 + g.random()
        x = x0 + ((px + vx * u * 0.1) % 1) * (x1 - x0) + 30 * math.sin(u * sp * 3 * speed + ph)
        y = y0 + py * (y1 - y0) + 30 * math.cos(u * sp * 2.6 * speed + ph)
        E.circle(d, x, y, r, fill=color)

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: hot shower running and the mirror already fogging up
        shower(E, d, u, 280, 430)
        mirror(E, d, 600, 380, 980, 980, fog=0.35 + 0.65 * E.ease(u / L))
        E.pill(d, "ESPEJO", 790, 320, 42)
    elif i == 1:  # hot water fills the air with vapour
        shower(E, d, u, 300, 420, steam=False)
        for k in range(30):   # water molecules rising from the water
            f = (u * 0.4 + (k * 0.377) % 1) % 1
            x = 180 + (k * 137) % 700 + 25 * math.sin(u * 3 + k)
            E.circle(d, x, 1050 - f * 650, 10, fill=WATER)
        E.label(d, "AGUA CALIENTE", 300, 1080, 46, color=E.HOT)
        E.label(d, "VAPOR", 760, 420, 52, color=E.COLD)
    elif i == 2:  # vapour is an invisible gas mixed with the air
        E.rrect(d, 120, 380, 960, 1000, 30, E.BG2)
        molecules(E, d, u, 170, 430, 910, 950, 40, E.SIL, seed=1)
        molecules(E, d, u, 170, 430, 910, 950, 22, WATER, r=11, seed=2)
        E.pill(d, "GAS INVISIBLE", 540, 330, 42)
        E.label(d, "AIRE", 300, 1060, 44, color=E.SIL)
        E.label(d, "VAPOR", 780, 1060, 44, color=E.COLD)
    elif i == 3:  # the mirror is colder than the warm air
        mirror(E, d, 620, 400, 960, 980, reflect=False)
        E.rrect(d, 140, 420, 520, 960, 30, E.mix(E.BG2, E.HOT_D, 0.35))
        molecules(E, d, u, 180, 460, 480, 920, 18, WATER, r=10, seed=3, speed=1.4)
        for x, top, col in ((330, 600, E.HOT), (790, 820, E.COLD)):   # thermometers
            E.rrect(d, x - 18, 470, x + 18, 860, 18, E.SIL_H)
            E.rrect(d, x - 10, top, x + 10, 860, 10, col)
            E.circle(d, x, 880, 32, fill=col)
        E.label(d, "AIRE CALIENTE", 330, 1060, 44, color=E.HOT)
        E.label(d, "ESPEJO FRÍO", 790, 1060, 44, color=E.COLD)
    elif i == 4:  # air cools on the glass and vapour condenses
        E.rrect(d, 760, 360, 1000, 1000, 10, GLASS)
        E.label(d, "ESPEJO", 880, 330, 42, color=E.MUTED)
        k = E.ease(u / L)
        g = random.Random(4)
        for j in range(24):
            y = 400 + g.random() * 560; ph = g.random()
            f = (u * 0.35 + ph) % 1
            x = 120 + f * 620
            sz = 10 + 10 * max(0, f - 0.7) / 0.3
            E.circle(d, x, y, sz, fill=E.mix(WATER, E.SIL_H, max(0, f - 0.6)))
        for j in range(int(26 * k)):   # droplets collecting on the cold glass
            E.circle(d, 778 + (j * 37) % 40, 400 + (j * 83) % 560, 16, fill=E.SIL_H)
        E.arrow(d, 300, 1060, 560, 1060, E.COLD, 7, 26)
        E.pill(d, "SE CONDENSA", 380, 330, 42)
    elif i == 5:  # tiny droplets scatter the light
        E.rrect(d, 120, 640, 960, 700, 8, GLASS)
        for j in range(9):
            E.circle(d, 170 + j * 95, 620, 26, fill=E.SIL_H)
        k = E.ease(u / (L * 0.6))
        x, y = 540 - 190 + 190, 620
        E.arrow(d, 200, 360, 200 + 300 * k, 360 + 240 * k, E.AMB, 8, 26) if k < 0.98 else E.line(d, [(200, 360), (520, 610)], E.AMB, 8)
        if k > 0.95:
            for ang in (-2.6, -2.0, -1.2, -0.5):
                E.arrow(d, 540, 600, 540 + 300 * math.cos(ang), 600 + 300 * math.sin(ang), E.AMB, 6, 22)
        E.label(d, "GOTITAS", 540, 800, 50, color=E.WHITE)
        E.label(d, "LUZ", 160, 320, 46, color=E.AMB)
    elif i == 6:  # a white layer instead of the reflection
        k = E.ease(u / (L * 0.7))
        mirror(E, d, 260, 380, 820, 1000, fog=k)
        if k > 0.6:
            E.pill(d, "CAPA BLANCA", 540, 1080, 44)
        else:
            E.label(d, "REFLEJO", 540, 1080, 46, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.05, 1.0), ("zip", s[1] + 0.4, 1.0), ("click", s[2] + 0.6), ("pop", s[3] + 0.8),
            ("whoosh", s[4] + 0.5, 0.8), ("click", s[5] + 1.0), ("whoosh", s[6] + 0.3, 1.2)]
