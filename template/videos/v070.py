"""Video 070 — ¿Cómo cambia de marcha una bicicleta?
Science: the rear wheel carries a stack of sprockets (cogs) of different sizes side by side (the cassette). The rear
derailleur hangs below them. Moving the shifter lever changes the tension of a cable that moves the derailleur
sideways on its parallelogram linkage. The derailleur's guide pulley pushes the moving chain sideways until it lines
up with a neighbouring cog; while the rider pedals, that cog's teeth catch the chain and carry it round. A spring in the
derailleur cage, with its two small pulleys, keeps the chain taut and takes up the slack. A large rear cog makes pedalling
easier; a small rear cog moves the bike further for each turn of the pedals.
(Whether the cable pulls towards the large or the small cog depends on the system and is not claimed; no ratios or
numbers of gears; front derailleur and hub gears are not covered.)
"""
import math

ID = "070"
TITLE = "¿Cómo cambia de marcha una bicicleta?"
SUBTITLE = "CÓMO FUNCIONA"
LINES = [
    "¿Cómo cambia de marcha una bicicleta sin que se caiga la cadena?",
    "Detrás hay varios piñones de distintos tamaños, uno junto a otro.",
    "Al mover la palanca, un cable desplaza el cambio trasero.",
    "El cambio empuja la cadena hacia un lado, hasta otro piñón.",
    "Los dientes del piñón nuevo atrapan la cadena y la arrastran.",
    "Un muelle y dos ruedecillas mantienen la cadena siempre tensa.",
    "Piñón grande: pedaleas más fácil. Piñón pequeño: avanzas más por pedalada.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"marcha", "bicicleta", "cadena", "piñones", "tamaños", "palanca", "cable", "desplaza", "cambio",
            "trasero", "empuja", "lado", "piñón", "dientes", "atrapan", "arrastran", "muelle", "ruedecillas", "tensa",
            "grande", "fácil", "pequeño", "avanzas", "pedalada"}

CHAIN = (150, 160, 175)
CHAIN_H = (215, 222, 232)
CABLE = (90, 170, 255)

# rear view of the cassette: cog k at x = X0 + k*DX, big (k=0) to small (k=6)
X0, DX, CY = 300, 80, 600
NC = 7


def cog_h(k):
    return 520 - 45 * k


def cassette(E, d, hi=None, grow=1.0):
    E.rrect(d, X0 - 40, CY - 14, X0 + DX * (NC - 1) + 40, CY + 14, 6, E.SIL_D)   # axle
    for k in range(NC):
        h = cog_h(k) * grow
        col = E.AMB if hi == k else E.SIL
        E.rrect(d, X0 + DX * k - 16, CY - h / 2, X0 + DX * k + 16, CY + h / 2, 10, col, outline=E.SIL_H, w=2)


def chain_on(E, d, pos, u):
    """Chain seen from behind running over the top of cog at (fractional) position pos, down to the derailleur."""
    x = X0 + DX * pos
    k = int(round(pos)); top = CY - cog_h(min(NC - 1, max(0, k))) / 2 - 18
    E.line(d, [(x, top), (x, 1000)], CHAIN, 22)
    for j in range(14):  # moving links
        y = top + ((j * 60 + u * 240) % (1000 - top))
        E.rrect(d, x - 13, y - 10, x + 13, y + 10, 5, CHAIN_H)
    return x


def derailleur(E, d, x):
    E.rrect(d, x - 40, 930, x + 40, 1120, 18, E.SIL_D, outline=E.SIL_H, w=3)
    E.circle(d, x, 975, 26, fill=E.BG1, outline=E.SIL_H, w=4)
    E.circle(d, x, 1075, 26, fill=E.BG1, outline=E.SIL_H, w=4)
    # parallelogram arms up to the frame
    E.line(d, [(x - 30, 930), (960, 870)], E.SIL_D, 10)
    E.line(d, [(x + 30, 960), (960, 920)], E.SIL_D, 10)


def gear(E, d, x, y, r, rot, n, color):
    pts = []
    for k in range(2 * n):
        a = rot + k * math.pi / n
        rr = r if k % 2 == 0 else r - 16
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    E.poly(d, pts, fill=color, outline=E.SIL_H, w=2)
    E.circle(d, x, y, 22, fill=E.BG1)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: chain already sliding from one cog to the next while it runs
        pos = 3 - min(1.0, E.ease(u / (L * 0.7)))
        cassette(E, d, hi=int(round(pos)))
        x = chain_on(E, d, pos, u)
        derailleur(E, d, x)
        E.arrow(d, x + 90, 380, x - 40, 380, E.AMB, 8, 28)
        E.label(d, "CAMBIO", 840, 1060, 46, color=E.AMB)
    elif i == 1:  # cassette: cogs of different sizes side by side
        cassette(E, d, grow=0.3 + 0.7 * E.ease(u / 0.8))
        E.label(d, "GRANDE", X0, 300, 46, color=E.SIL_H)
        E.label(d, "PEQUEÑO", X0 + DX * 6, 400, 46, color=E.SIL_H)
        E.label(d, "PIÑONES", 540, 1000, 56, color=E.AMB)
    elif i == 2:  # lever moves, cable moves the derailleur
        k = E.ease(u / (L * 0.6))
        cassette(E, d)
        pos = 3 - k
        x = chain_on(E, d, pos, u)
        derailleur(E, d, x)
        # shifter lever top right with cable running to the derailleur
        a = -0.4 - 0.7 * k
        E.circle(d, 900, 330, 34, fill=E.SIL_D)
        E.line(d, [(900, 330), (900 + 120 * math.cos(a), 330 + 120 * math.sin(a))], E.AMB, 18)
        E.line(d, [(900, 364), (1000, 500), (1000, 900), (960, 900)], CABLE, 6)
        for j in range(4):
            yy = 520 + ((j * 90 + u * 260) % 360)
            E.arrow(d, 1000, yy, 1000, yy + 40, CABLE, 5, 18)
        E.label(d, "PALANCA", 860, 450, 42, color=E.AMB)
        E.label(d, "CABLE", 960, 1000, 42, color=CABLE)
    elif i == 3:  # derailleur pushes chain sideways to the next cog
        k = E.ease(u / (L * 0.7))
        pos = 2 - k
        cassette(E, d, hi=1 if k > 0.5 else 2)
        x = chain_on(E, d, pos, u)
        derailleur(E, d, x)
        E.arrow(d, x + 60, 1180 - 120, x - 80, 1180 - 120, E.AMB, 8, 28)
        E.label(d, "EMPUJA", 540, 300, 52, color=E.AMB)
    elif i == 4:  # side view: teeth catch the chain and carry it round
        rot = u * 1.2
        gear(E, d, 540, 700, 280, rot, 20, E.SIL)
        for j in range(20):  # chain links riding on the upper half of the cog, moving with it
            a = math.pi + ((j * math.pi / 20 + rot) % math.pi)
            E.circle(d, 540 + 292 * math.cos(a), 700 + 292 * math.sin(a), 15, fill=CHAIN_H, outline=E.BG1, w=2)
        E.line(d, [(250, 700), (180, 1150)], CHAIN_H, 10)
        E.arrow(d, 420, 350, 660, 350, E.AMB, 8, 28)
        E.label(d, "LOS DIENTES ATRAPAN", 540, 1080, 48, color=E.AMB)
    elif i == 5:  # side view of the cage: spring + two pulleys keep chain taut
        sw = 10 * math.sin(u * 3)
        E.rrect(d, 430, 420, 650, 1060, 40, E.SIL_D)
        gear(E, d, 540, 500, 70, u * 3, 10, E.SIL)
        gear(E, d, 540 + sw, 960, 70, u * 3, 10, E.SIL)
        E.line(d, [(380, 300), (470, 500), (610, 960), (900, 1000)], CHAIN, 14)
        # coil spring at the pivot
        for c in range(6):
            E.circle(d, 760, 430 + c * 30, 26, outline=E.HOT, w=6)
        E.label(d, "MUELLE", 860, 330, 46, color=E.HOT)
        E.label(d, "TENSA", 860, 760, 52, color=E.AMB)
        E.arrow(d, 760, 640, 650, 900, E.AMB, 7, 24)
    elif i == 6:  # big cog = easier, small cog = further per turn
        rot = u * 1.5
        gear(E, d, 290, 640, 200, rot, 18, E.SIL)
        gear(E, d, 800, 640, 100, rot * 2, 9, E.SIL)
        E.label(d, "MÁS FÁCIL", 290, 950, 50, color=E.COLD)
        E.label(d, "MÁS LEJOS", 800, 950, 50, color=E.AMB)
        E.label(d, "GRANDE", 290, 360, 42, color=E.SIL_H)
        E.label(d, "PEQUEÑO", 800, 460, 42, color=E.SIL_H)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("zip", s[0] + 0.3), ("pop", s[1] + 0.5), ("click", s[2] + 0.6), ("whoosh", s[3] + 0.4, 0.8),
            ("click", s[4] + 0.6), ("pop", s[5] + 0.6), ("zip", s[6] + 0.5)]
