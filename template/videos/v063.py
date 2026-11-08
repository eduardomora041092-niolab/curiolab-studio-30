"""Video 063 — ¿Por qué la cebolla te hace llorar?
Science: onion cells keep sulfur-containing compounds and an enzyme (alliinase) in separate compartments. Cutting
the onion breaks the cells, the two mix, and a chain of reactions produces a volatile irritant gas (syn-propanethial
S-oxide, the lachrymatory factor). This is thought to be a chemical defence that discourages animals from eating the
bulb. The gas drifts up to the eyes and stimulates sensory nerves in the surface of the eye, and the eyes respond by
producing tears that wash the irritant away.
(No concentrations, timings or anti-crying tricks are claimed; the chemical names are not said aloud.)
"""
import math

ID = "063"
TITLE = "¿Por qué la cebolla te hace llorar?"
SUBTITLE = "CIENCIA EN 30 SEGUNDOS"
LINES = [
    "¿Por qué lloras al cortar una cebolla?",
    "La cebolla guarda sustancias y enzimas en compartimentos separados.",
    "Al cortarla, rompes sus células y se mezclan.",
    "La reacción produce un gas irritante que flota en el aire.",
    "Es una defensa química que ahuyenta a los animales.",
    "El gas llega a tus ojos y estimula sus nervios.",
    "Tus ojos responden con lágrimas para lavar el irritante.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"lloras", "cortar", "cebolla", "sustancias", "enzimas", "compartimentos", "separados", "cortarla",
            "células", "mezclan", "reacción", "gas", "irritante", "aire", "defensa", "química", "ahuyenta",
            "animales", "ojos", "nervios", "lágrimas", "lavar"}

ONI = (215, 170, 210)
ONI_D = (150, 100, 150)
SUB = (255, 176, 32)       # sulfur compounds
ENZ = (120, 220, 140)      # enzyme
GAS = (230, 235, 140)
TEAR = (120, 190, 255)


def onion(E, d, x, y, r=170, cut=0.0):
    E.circle(d, x, y, r, fill=ONI, outline=ONI_D, w=6)
    for k in range(1, 4):
        E.circle(d, x, y, r - 38 * k, outline=ONI_D, w=3)
    E.poly(d, [(x - 22, y - r + 6), (x, y - r - 60), (x + 22, y - r + 6)], fill=(170, 200, 110))


def knife(E, d, x, y):
    E.poly(d, [(x - 260, y - 30), (x + 40, y - 30), (x + 40, y + 10), (x - 230, y + 30)], fill=E.SIL, outline=E.SIL_D, w=3)
    E.rrect(d, x + 40, y - 34, x + 220, y + 14, 14, (90, 60, 40))


def gas(E, d, u, x0, y0, spread=260, n=10, height=380):
    for k in range(n):
        q = (u * 0.45 + k / n) % 1.0
        x = x0 + spread * ((k * 0.37) % 1.0 - 0.5) + 30 * math.sin(u * 2 + k)
        y = y0 - q * height
        E.circle(d, x, y, 10 + 10 * q, outline=E.mix(GAS, (60, 70, 90), q * 0.8), w=4)


def cellbox(E, d, broken=0.0, u=0.0):
    """One cell with two compartments; broken=1 means membranes torn and contents mixed."""
    E.rrect(d, 200, 480, 880, 1000, 40, (70, 50, 80), outline=ONI, w=6)
    if broken < 0.5:
        E.rrect(d, 240, 520, 520, 960, 30, (90, 70, 100), outline=E.WHITE, w=4)
        E.rrect(d, 560, 520, 840, 960, 30, (90, 70, 100), outline=E.WHITE, w=4)
        for k in range(9):
            E.circle(d, 290 + (k % 3) * 90, 600 + (k // 3) * 130, 18, fill=SUB)
            E.circle(d, 610 + (k % 3) * 90, 600 + (k // 3) * 130, 18, fill=ENZ)
    else:
        m = E.ease((broken - 0.5) * 2)
        for k in range(9):
            ax, ay = 290 + (k % 3) * 90, 600 + (k // 3) * 130
            bx, by = 610 + (k % 3) * 90, 600 + (k // 3) * 130
            E.circle(d, ax + 130 * m * ((k % 2) * 2 - 0.6) + 8 * math.sin(u * 4 + k), ay + 30 * m * math.sin(k), 18, fill=SUB)
            E.circle(d, bx - 130 * m * ((k % 2) * 2 - 0.6) + 8 * math.cos(u * 4 + k), by - 30 * m * math.sin(k), 18, fill=ENZ)


def eye(E, d, x, y, w=300):
    E.poly(d, [(x - w, y), (x - w / 2, y - 120), (x + w / 2, y - 120), (x + w, y), (x + w / 2, y + 120), (x - w / 2, y + 120)],
           fill=(245, 240, 235), outline=E.SIL_D, w=5)
    E.circle(d, x, y, 95, fill=(90, 140, 90))
    E.circle(d, x, y, 45, fill=(15, 15, 20))
    E.circle(d, x + 25, y - 25, 14, fill=E.WHITE)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: knife cutting the onion, gas already rising
        E.rrect(d, 140, 900, 940, 980, 16, (150, 110, 70))
        onion(E, d, 540, 740)
        k = (u * 1.4) % 1.0
        ky = 480 + 260 * (k if k < 0.6 else (1 - k) / 0.4 * 0.6)
        knife(E, d, 620, ky)
        gas(E, d, u + 0.6, 540, 640, spread=360, n=12, height=330)
    elif i == 1:  # separate compartments
        cellbox(E, d)
        E.label(d, "SUSTANCIAS", 380, 420, 42, color=SUB)
        E.label(d, "ENZIMAS", 700, 420, 42, color=ENZ)
        E.label(d, "SEPARADAS", 540, 1080, 46, color=E.WHITE)
    elif i == 2:  # cutting breaks the cells and they mix
        b = min(1.0, u / (L * 0.7))
        cellbox(E, d, broken=b, u=u)
        kx = 540; ky = 300 + 600 * E.ease(min(1.0, u / (L * 0.35)))
        if b < 0.9:
            knife(E, d, kx + 80, ky)
        E.label(d, "SE MEZCLAN", 540, 1080, 46, color=E.AMB)
    elif i == 3:  # reaction makes an irritant gas
        cellbox(E, d, broken=1.0, u=u)
        gas(E, d, u, 540, 520, spread=560, n=14, height=190)
        E.label(d, "GAS IRRITANTE", 540, 1080, 48, color=GAS)
    elif i == 4:  # chemical defence against animals: the bitten onion releases gas
        onion(E, d, 540, 760)
        E.circle(d, 705, 700, 60, fill=E.BG1)           # bite mark
        for k in range(3):
            E.circle(d, 662 + 30 * k, 648 + 40 * k, 14, fill=E.BG1)
        gas(E, d, u, 660, 660, spread=300, n=12, height=300)
        E.pill(d, "DEFENSA QUÍMICA", 540, 1060, 46)
    elif i == 5:  # gas reaches the eyes and stimulates nerves
        eye(E, d, 540, 520)
        gas(E, d, u, 540, 1100, spread=520, n=14, height=420)
        on = 0.5 + 0.5 * math.sin(u * 8)
        col = E.mix((120, 90, 60), E.AMB, on)
        for sx in (-1, 1):
            for k in range(3):
                x0 = 540 + sx * (330 + 10 * k); y0 = 440 + 80 * k
                E.line(d, [(x0, y0), (x0 + sx * 40, y0 - 20), (x0 + sx * 70, y0 + 15), (x0 + sx * 110, y0 - 10)], col, 6)
        E.label(d, "NERVIOS", 540, 360, 46, color=E.AMB)
    elif i == 6:  # tears wash the irritant away
        eye(E, d, 540, 560)
        for k in range(4):
            q = (u * 0.7 + k / 4) % 1.0
            x = 360 + k * 110; y = 700 + q * 380
            E.poly(d, [(x, y - 30), (x + 20, y + 5), (x, y + 25), (x - 20, y + 5)], fill=TEAR)
            E.circle(d, x, y + 8, 18, fill=TEAR)
        E.label(d, "LÁGRIMAS", 540, 340, 52, color=TEAR)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("click", s[0] + 0.2), ("click", s[0] + 0.9), ("pop", s[1] + 0.6), ("click", s[2] + 0.5),
            ("whoosh", s[3] + 0.4, 0.9), ("pop", s[4] + 0.6), ("whoosh", s[5] + 0.4, 0.8), ("pop", s[6] + 0.7)]
