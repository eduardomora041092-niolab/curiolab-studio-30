"""Video 006 — ¿Por qué el mar es salado?
Science: rain is slightly acidic (dissolved CO2) and slowly weathers rock, releasing ions such as
sodium; rivers carry them to the sea (in river water they are very dilute, so it tastes fresh).
Evaporation removes water from the sea but leaves dissolved salts behind; over millions of years salts
built up. Average seawater salinity ≈ 35 g of salt per kg (≈ per litre) of water.
(Chloride comes largely from volcanic/hydrothermal sources; the script only claims sodium from rocks.)
"""
import math, random

ID = "006"
TITLE = "¿Por qué el mar es salado?"
SUBTITLE = "CURIOSIDADES DE LA CIENCIA"
LINES = [
    "Los ríos son de agua dulce. ¿Entonces por qué el mar es salado?",
    "La lluvia es ligeramente ácida y, poco a poco, desgasta las rocas.",
    "Así se liberan minerales, como el sodio, que los ríos llevan hasta el mar.",
    "En el río están tan diluidos que no los notamos.",
    "En el mar, el Sol evapora el agua, pero la sal se queda.",
    "Durante millones de años, la sal se ha ido acumulando.",
    "Hoy, cada litro de agua de mar tiene unos treinta y cinco gramos de sal.",
    "Sígueme para más curiosidades de la ciencia.",
]
KEYWORDS = {"ríos", "dulce", "mar", "salado", "lluvia", "ácida", "rocas", "minerales", "sodio", "diluidos", "evapora", "sal", "millones", "gramos", "ciencia"}

SEA, SEA_D = (40, 110, 200), (25, 75, 150)
RIVER = (90, 170, 235)
ROCK, ROCK_D = (120, 110, 100), (80, 72, 64)
LAND = (60, 130, 80)
SALT = (250, 250, 250)
SUN = (255, 220, 120)

def landscape(E, d, sea_level=900):
    E.poly(d, [(60, 640), (300, 470), (480, 600), (620, 520), (760, 700), (760, 1180), (60, 1180)], fill=LAND)
    E.poly(d, [(120, 640), (260, 520), (380, 640)], fill=ROCK, outline=ROCK_D, w=3)
    E.rrect(d, 700, sea_level, 1020, 1180, 0, SEA)
    # river from the hills to the sea
    E.line(d, [(330, 640), (380, 760), (470, 830), (600, 880), (720, sea_level + 30)], RIVER, 26)

def salt_dots(E, d, n, x0, y0, x1, y1, seed=3, u=0.0, r=7):
    rnd = random.Random(seed)
    for k in range(n):
        x = rnd.uniform(x0, x1) + 4 * math.sin(u * 3 + k); y = rnd.uniform(y0, y1) + 4 * math.cos(u * 2 + k)
        E.circle(d, x, y, r, fill=SALT)

def glass(E, d, x, y, label, col, salty=False):
    E.poly(d, [(x - 90, y - 160), (x + 90, y - 160), (x + 70, y + 120), (x - 70, y + 120)], fill=(40, 52, 78), outline=E.SIL, w=4)
    E.poly(d, [(x - 82, y - 100), (x + 82, y - 100), (x + 68, y + 112), (x - 68, y + 112)], fill=col)
    if salty: salt_dots(E, d, 22, x - 60, y - 90, x + 60, y + 100, r=6)
    E.label(d, label, x, y + 190, 44)

def scene(i, u, L, E, im, d):
    cx = 540
    if i == 0:  # fresh river vs salty sea
        glass(E, d, 320, 720, "RÍO: DULCE", RIVER)
        k = E.back_out((u - 0.8) / 0.4)
        if k > 0.05: glass(E, d, 760, 720, "MAR: SALADO", SEA, salty=True)
        E.label(d, "?", cx, 470, 120)
    elif i == 1:  # acidic rain weathers rock
        E.rrect(d, 80, 300, 1000, 420, 60, (120, 130, 150))
        E.label(d, "CO2 + AGUA", cx, 360, 46, color=E.WHITE)
        E.poly(d, [(200, 1150), (380, 820), (560, 760), (760, 860), (900, 1150)], fill=ROCK, outline=ROCK_D, w=4)
        for k in range(18):
            x = 120 + (k * 53) % 860; y = 440 + ((u * 600 + k * 97) % 380)
            E.line(d, [(x, y), (x - 8, y + 34)], RIVER, 6)
        for k in range(int(6 * E.ease(u / L))):  # chips falling off the rock
            E.circle(d, 420 + k * 60, 900 + (k % 2) * 40 + 30 * math.sin(u * 2 + k), 12, fill=ROCK_D)
        if u > 0.6: E.pill(d, "LIGERAMENTE ÁCIDA", cx, 520, 38)
    elif i == 2:  # minerals carried by the river to the sea
        landscape(E, d)
        path = [(330, 640), (380, 760), (470, 830), (600, 880), (720, 930)]
        for k in range(8):
            f = ((u * 0.35 + k / 8) % 1.0) * (len(path) - 1)
            a = int(f); b = min(a + 1, len(path) - 1); t = f - a
            x = E.lerp(path[a][0], path[b][0], t); y = E.lerp(path[a][1], path[b][1], t)
            E.circle(d, x, y, 11, fill=SALT, outline=E.AMB, w=2)
        salt_dots(E, d, 10, 740, 940, 1000, 1170, u=u)
        if u > 0.6:
            E.label(d, "SODIO", 250, 860, 48); E.arrow(d, 300, 830, 410, 790, w=5)
            E.label(d, "MAR", 860, 860, 44, color=E.WHITE)
    elif i == 3:  # dilute in river water (zoom)
        E.circle(d, cx, 740, 330, fill=RIVER, outline=E.AMB, w=6)
        for k in range(26):  # many water molecules, very few salt particles
            a = k * 2.4; r = 60 + (k * 37) % 240
            E.circle(d, cx + r * math.cos(a + u * 0.4), 740 + r * math.sin(a + u * 0.4), 16, fill=(160, 210, 250))
        for k in range(2):
            a = k * 3.1 + 1; E.circle(d, cx + 150 * math.cos(a + u * 0.4), 740 + 150 * math.sin(a + u * 0.4), 14, fill=SALT, outline=E.AMB, w=3)
        E.pill(d, "MUY DILUIDOS", cx, 330, 42)
    elif i == 4:  # evaporation: water leaves, salt stays
        E.rrect(d, 60, 820, 1020, 1180, 0, SEA)
        E.circle(d, 860, 400, 90, fill=SUN)
        for k in range(10):  # vapour (water) rising
            x = 120 + k * 85; y = 800 - ((u * 220 + k * 60) % 420)
            E.circle(d, x, y, 13, fill=(170, 215, 255))
            if k % 3 == 0: E.arrow(d, x + 20, y + 40, x + 20, y - 10, color=(170, 215, 255), w=4, head=16)
        salt_dots(E, d, 30, 90, 860, 990, 1160, u=u)
        if u > 0.6:
            E.label(d, "AGUA", 200, 480, 46, color=(170, 215, 255))
            E.label(d, "LA SAL SE QUEDA", cx, 760, 46)
    elif i == 5:  # accumulation over millions of years
        E.rrect(d, 60, 560, 1020, 1180, 0, SEA)
        p = E.ease(u / (L * 0.9))
        salt_dots(E, d, int(8 + 90 * p), 90, 600, 990, 1160, u=u)
        E.label(d, "MILLONES DE AÑOS", cx, 440, 52)
        E.rrect(d, 140, 330, 940, 360, 14, (40, 52, 78))
        E.rrect(d, 140, 330, 140 + 800 * p + 1, 360, 14, E.AMB)
    elif i == 6:  # 35 g per litre
        E.rrect(d, 250, 420, 500, 1060, 40, (40, 52, 78), outline=E.SIL, w=5)
        E.rrect(d, 262, 520, 488, 1048, 30, SEA)
        E.label(d, "1 L", 375, 790, 70, color=E.WHITE)
        k = E.ease(u / 1.0)
        E.poly(d, [(620, 1060), (920, 1060), (770, 1060 - 230 * k)], fill=SALT)
        if u > 0.8: E.label(d, "≈ 35 g", 770, 720, 80)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("pop", s[0] + 0.9), ("whoosh", s[2], 0.6), ("whoosh", s[4] + 0.3, 0.8), ("pop", s[6] + 0.9)]
