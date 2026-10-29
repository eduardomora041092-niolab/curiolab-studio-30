"""Video 033 — ¿Por qué crece el pan?
Science: baker's yeast is made of tiny living single-celled fungi. In the dough they feed on sugars that come from the
flour and, as they ferment them, release carbon dioxide gas (and a little alcohol). Kneading flour with water forms
gluten, a stretchy network of proteins. That network traps the gas in many small bubbles, which inflate the dough.
In the oven the gas expands with the heat and the structure sets, leaving the spongy crumb. (No temperatures, times
or quantities are claimed; chemical leaveners and enzyme details are not covered.)
"""
import math

ID = "033"
TITLE = "¿Por qué crece el pan?"
SUBTITLE = "CURIOSIDADES DE LA CIENCIA"
LINES = [
    "¿Qué hace crecer la masa del pan?",
    "En la masa viven levaduras: hongos diminutos, de una sola célula.",
    "Se alimentan de los azúcares que vienen de la harina.",
    "Y, al comerlos, sueltan un gas: el dióxido de carbono.",
    "Al amasar, el gluten de la harina forma una red elástica.",
    "Esa red atrapa el gas en muchas burbujas que inflan la masa.",
    "En el horno, el gas se expande y el calor fija la miga.",
    "Sígueme para más curiosidades de la ciencia.",
]
KEYWORDS = {"crecer", "masa", "pan", "levaduras", "hongos", "célula", "azúcares", "harina", "gas", "dióxido",
            "carbono", "amasar", "gluten", "red", "elástica", "burbujas", "inflan", "horno", "calor", "miga"}

DOUGH, DOUGH_D = (238, 214, 170), (200, 170, 120)
CRUST = (196, 120, 52)
YEAST = (232, 200, 110)
LENS = (540, 660, 370)   # magnifier circle (x, y, r)

def bowl(E, d, rise):
    E.poly(d, [(200, 900), (880, 900), (780, 1120), (300, 1120)], fill=E.BLUE)
    E.rrect(d, 180, 880, 900, 920, 18, E.BLUE_D)
    h = 70 + 260 * rise
    pts = [(540 + 330 * math.cos(t), 890 - h * math.sin(t)) for t in [math.pi * j / 40 for j in range(41)]]
    E.poly(d, pts, fill=DOUGH)
    return h

def lens_bg(E, d):
    x, y, r = LENS
    E.circle(d, x, y, r + 14, fill=E.SIL_D)
    E.circle(d, x, y, r, fill=E.mix(DOUGH, E.BG1, 0.15))

def yeast_cell(E, d, x, y, s=1.0, bud=True):
    E.circle(d, x, y, 46 * s, fill=YEAST, outline=E.BRA_D, w=4)
    E.circle(d, x - 8 * s, y - 6 * s, 14 * s, fill=E.BRA_D)
    if bud:
        E.circle(d, x + 44 * s, y - 30 * s, 20 * s, fill=YEAST, outline=E.BRA_D, w=3)

CELLS = [(420, 530), (660, 590), (480, 760), (690, 800)]

def wobble(u, k):
    return 10 * math.sin(u * 2 + k * 1.7), 8 * math.cos(u * 1.6 + k)

def gluten(E, d, u, inflate=0.0, color=None):
    col = color or E.BRA_D
    for k in range(6):  # crossing stretchy strands
        y = 480 + k * 85
        pts = [(170 + j * 37, y + 22 * math.sin(j * 0.9 + k + u * 1.2)) for j in range(21)]
        E.line(d, pts, col, 7)
        x = 220 + k * 130
        pts = [(x + 22 * math.sin(j * 0.9 + k * 1.3 + u), 440 + j * 30) for j in range(18)]
        E.line(d, pts, col, 7)

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: dough already swelling in a bowl, bubbles at the surface
        rise = 0.35 + 0.65 * E.ease(u / L)
        h = bowl(E, d, rise)
        for k in range(6):
            f = (u * 0.7 + k / 6) % 1
            a = 0.4 + k * 0.42
            E.circle(d, 540 + 300 * math.cos(a) * 0.9, 890 - h * math.sin(a) * 0.9, 8 + 14 * f, outline=DOUGH_D, w=4)
        E.arrow(d, 920, 860, 920, 600, E.AMB, 10, 34)
        E.pill(d, "MASA", 540, 1000, 44)
    elif i == 1:  # yeasts: tiny living fungi in the dough
        lens_bg(E, d)
        for k, (x, y) in enumerate(CELLS):
            dx, dy = wobble(u, k)
            yeast_cell(E, d, x + dx, y + dy, 1.0, bud=k % 2 == 0)
        E.label(d, "LEVADURAS", 540, 1110, 52, color=E.AMB)
    elif i == 2:  # they feed on sugars from the flour
        lens_bg(E, d)
        for k, (x, y) in enumerate(CELLS):
            dx, dy = wobble(u, k)
            yeast_cell(E, d, x + dx, y + dy, 1.0, bud=False)
            for j in range(3):
                f = (u * 0.6 + j / 3 + k * 0.2) % 1
                a = k * 1.6 + j * 2.1
                sx = x + dx + (130 * (1 - f)) * math.cos(a); sy = y + dy + (130 * (1 - f)) * math.sin(a)
                if f < 0.85:
                    E.rrect(d, sx - 10, sy - 10, sx + 10, sy + 10, 3, E.WHITE)
        E.label(d, "AZÚCARES", 540, 1110, 52, color=E.WHITE)
    elif i == 3:  # and release a gas: carbon dioxide
        lens_bg(E, d)
        for k, (x, y) in enumerate(CELLS):
            dx, dy = wobble(u, k)
            yeast_cell(E, d, x + dx, y + dy, 1.0, bud=False)
            for j in range(3):
                f = (u * 0.5 + j / 3 + k * 0.3) % 1
                bx = x + dx + 60 + 30 * math.sin(j + u); by = y + dy - 40 - 120 * f
                if (bx - LENS[0]) ** 2 + (by - LENS[1]) ** 2 < (LENS[2] - 20) ** 2:
                    E.circle(d, bx, by, 10 + 10 * f, outline=E.COLD, w=4)
        E.label(d, "DIÓXIDO DE CARBONO", 540, 1110, 48, color=E.COLD)
        E.pill(d, "GAS", 900, 360, 40, bg=E.COLD)
    elif i == 4:  # kneading: gluten forms a stretchy network
        k = E.ease(u / (L * 0.6))
        E.rrect(d, 140, 400, 940, 1100, 40, E.mix(DOUGH, E.BG1, 0.15))
        gluten(E, d, u * k)
        s = 40 * math.sin(u * 2 * math.pi * 0.8)
        E.arrow(d, 300 - s, 340, 160 - s, 340, E.AMB, 8, 28); E.arrow(d, 780 + s, 340, 920 + s, 340, E.AMB, 8, 28)
        E.label(d, "RED DE GLUTEN", 540, 1150, 52, color=E.AMB)
    elif i == 5:  # the network traps the gas in bubbles that inflate the dough
        g = E.ease(u / (L * 0.8))
        E.rrect(d, 140, 400, 940, 1100, 40, E.mix(DOUGH, E.BG1, 0.15))
        for k in range(9):
            x = 270 + (k % 3) * 270; y = 520 + (k // 3) * 220
            E.circle(d, x, y, 30 + 60 * g, fill=E.mix(E.BG1, DOUGH, 0.35), outline=E.COLD, w=4)
        gluten(E, d, u * 0.4)
        E.arrow(d, 1000, 900, 1000, 560, E.AMB, 10, 34)
        E.label(d, "BURBUJAS", 540, 1150, 52, color=E.COLD)
    elif i == 6:  # in the oven: gas expands, heat sets the crumb
        t = E.ease(u / (L * 0.55))
        E.rrect(d, 110, 320, 970, 760, 30, E.SIL_D)
        E.rrect(d, 150, 360, 930, 720, 20, (50, 30, 26))
        for k in range(4):
            pts = [(260 + k * 180 + 14 * math.sin(j * 0.8 + u * 4), 390 + j * 8) for j in range(8)]
            E.line(d, pts, E.HOT, 5)
        h = 90 + 110 * t
        pts = [(540 + 260 * math.cos(a), 690 - h * math.sin(a)) for a in [math.pi * j / 40 for j in range(41)]]
        E.poly(d, pts, fill=E.mix(DOUGH, CRUST, t))
        E.label(d, "HORNO", 540, 300, 42, color=E.WHITE)
        if u > L * 0.5:   # slice: spongy crumb with holes
            E.circle(d, 540, 960, 190, fill=CRUST)
            E.circle(d, 540, 960, 168, fill=DOUGH)
            for k in range(14):
                a = k * 2.4; r = 30 + (k * 41) % 120
                E.circle(d, 540 + r * math.cos(a), 960 + r * math.sin(a), 8 + (k % 4) * 6, fill=DOUGH_D)
            E.label(d, "MIGA", 830, 960, 50, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("pop", s[0] + 0.5), ("pop", s[1] + 0.6), ("click", s[2] + 0.6), ("pop", s[3] + 0.7),
            ("whoosh", s[4] + 0.3, 0.8), ("pop", s[5] + 0.9), ("whoosh", s[6] + 0.3, 1.2)]
