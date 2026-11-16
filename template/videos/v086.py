"""Video 086 — ¿Cómo aspira una aspiradora?
Science: an electric motor spins a fan at high speed. The fan pushes air out through the exhaust, so the pressure
inside the machine drops (a partial vacuum, not a perfect one). Outside air, at higher (atmospheric) pressure, rushes in
through the nozzle and hose towards the low-pressure region. That incoming stream of air drags dust and crumbs along:
the dirt is not "pulled" by the machine but pushed in by the outside air. A bag or filter traps the dirt and lets the
air pass, and the air leaves through the exhaust.
(No suction figures, power or pressures are claimed.)
"""
import math

ID = "086"
TITLE = "¿Cómo aspira una aspiradora?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Por qué una aspiradora se traga el polvo del suelo?",
    "Dentro, un motor hace girar un ventilador muy rápido.",
    "El ventilador expulsa aire hacia fuera, por detrás.",
    "Así, dentro queda menos aire: la presión baja.",
    "Fuera, el aire tiene más presión y entra por el tubo.",
    "Ese aire que entra arrastra el polvo y las migas.",
    "Una bolsa atrapa la suciedad y deja salir el aire.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"aspiradora", "polvo", "suelo", "motor", "ventilador", "rápido", "expulsa", "fuera", "menos aire",
            "presión", "baja", "más presión", "entra", "tubo", "arrastra", "migas", "bolsa", "atrapa", "suciedad"}

FLOOR = 1100
TX = 230                       # hose x
BX0, BX1, BY0, BY1 = 400, 920, 520, 820   # body
BAG1 = 640                     # bag/filter right edge
FANX = 760
EXH = 920
CY = (BY0 + BY1) / 2
DUST = (196, 170, 130)
SHELL = (70, 86, 120)

# air path: floor nozzle -> hose up -> into body -> through bag -> fan -> out the exhaust
PATH = [(TX, FLOOR - 20), (TX, 640), (TX + 40, 600), (BX0 + 20, 600), (BAG1 - 20, CY), (FANX, CY), (1060, CY)]


def _seg_lengths():
    ls = []
    for a, b in zip(PATH, PATH[1:]):
        ls.append(math.hypot(b[0] - a[0], b[1] - a[1]))
    return ls


SEGL = _seg_lengths()
TOT = sum(SEGL)


def at(q):
    s = q * TOT
    for (a, b), l in zip(zip(PATH, PATH[1:]), SEGL):
        if s <= l:
            t = s / l
            return a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        s -= l
    return PATH[-1]


Q_BAG = sum(SEGL[:4]) / TOT     # where dust stops (bag)


def machine(E, d, hl_motor=False, hl_bag=False, hl_hose=False):
    # floor
    E.line(d, [(40, FLOOR + 6), (1040, FLOOR + 6)], E.MUTED, 6)
    # hose + nozzle
    hc = E.AMB if hl_hose else E.SIL_D
    E.line(d, [(TX, FLOOR - 30), (TX, 640), (TX + 40, 600), (BX0, 600)], hc, 46)
    E.line(d, [(TX, FLOOR - 30), (TX, 640), (TX + 40, 600), (BX0, 600)], E.CAV, 30)
    E.rrect(d, TX - 90, FLOOR - 40, TX + 90, FLOOR, 12, hc)
    E.rrect(d, TX - 18, FLOOR - 40, TX + 18, FLOOR - 4, 4, E.CAV)
    # body
    E.rrect(d, BX0 - 16, BY0 - 16, BX1 + 16, BY1 + 16, 40, SHELL)
    E.rrect(d, BX0, BY0, BX1, BY1, 24, E.CAV)
    # bag / filter
    bc = E.AMB if hl_bag else (150, 140, 120)
    E.rrect(d, BX0 + 14, BY0 + 20, BAG1, BY1 - 20, 30, None, outline=bc, w=5)
    for k in range(9):
        y = BY0 + 40 + k * 28
        E.line(d, [(BAG1 - 3, y), (BAG1 + 6, y + 12)], bc, 3)
    # motor + fan
    mc = E.AMB if hl_motor else E.BRA_D
    E.rrect(d, 800, CY - 50, 880, CY + 50, 14, mc)
    # exhaust grille
    for k in range(5):
        y = CY - 70 + k * 35
        E.line(d, [(BX1 + 4, y), (BX1 + 26, y)], E.SIL_D, 6)
    # wheels
    E.circle(d, BX0 + 60, BY1 + 40, 26, fill=E.SIL_D)
    E.circle(d, BX1 - 60, BY1 + 40, 26, fill=E.SIL_D)
    E.line(d, [(BX0 + 60, BY1 + 30), (BX0 + 60, BY1 + 16)], E.SIL_D, 8)


def fan(E, d, phase, hl=False):
    c = E.AMB if hl else E.SIL
    for k in range(3):
        a = phase * 2 * math.pi + k * 2 * math.pi / 3
        h = 90 * math.cos(a)
        w = 14 * abs(math.sin(a)) + 5
        E.poly(d, [(FANX - w, CY), (FANX + w, CY), (FANX + w * 0.6, CY - h), (FANX - w * 0.6, CY - h)], fill=c)
    E.circle(d, FANX, CY, 12, fill=E.SIL_D)
    E.line(d, [(FANX, CY), (800, CY)], E.SIL, 8)


def air(E, d, u, q0=0.0, q1=1.0, speed=1.0, n=26, col=None):
    col = col or E.COLD
    for j in range(n):
        q = (u * 0.35 * speed + j / n) % 1.0
        if q < q0 or q > q1:
            continue
        x, y = at(q)
        E.circle(d, x + ((j * 13) % 3 - 1) * 6, y + ((j * 7) % 3 - 1) * 6, 6, fill=col)


def dust(E, d, u, moving=True, n=14, kept=10):
    # dust kept in the bag
    for j in range(kept):
        x = BX0 + 50 + (j * 53) % 170
        y = BY1 - 40 - (j * 31) % 90
        E.circle(d, x, y, 8, fill=DUST)
    if not moving:
        for j in range(n):
            E.circle(d, 330 + j * 45, FLOOR - 10, 7 + (j % 3), fill=DUST)
        return
    for j in range(n):
        q = (u * 0.3 + j / n) % 1.0
        q = q * Q_BAG
        x, y = at(q)
        E.circle(d, x + (j % 3 - 1) * 7, y, 8, fill=DUST)
    for j in range(8):
        x = 420 + j * 70 - (u * 60) % 70
        if x > TX + 100:
            E.circle(d, x, FLOOR - 10, 7, fill=DUST)


def signs(E, d, inside=True, outside=True):
    if inside:
        for x, y in ((470, 600), (560, 720), (700, 600), (700, 760)):
            E.label(d, "-", x, y, 64, color=E.COLD)
    if outside:
        for x, y in ((120, 470), (560, 440), (980, 460), (120, 860), (600, 960), (960, 960)):
            E.label(d, "+", x, y, 56, color=E.HOT)


def scene(i, u, L, E, im, d):
    ph = u * 3.0
    if i == 0:  # in action from frame 0: air and dust flowing up the hose into the bag, fan spinning
        machine(E, d)
        fan(E, d, ph)
        air(E, d, u + 0.5)
        dust(E, d, u + 0.5)
    elif i == 1:  # a motor spins a fan very fast
        machine(E, d, hl_motor=True)
        fan(E, d, ph * 1.5, hl=True)
        E.label(d, "MOTOR", 840, 430, 46, color=E.AMB)
        E.arrow(d, 840, 460, 840, 600, E.AMB, 5, 20)
        E.label(d, "VENTILADOR", 700, 900, 40, color=E.AMB)
        E.arrow(d, 740, 875, 760, 770, E.AMB, 5, 20)
    elif i == 2:  # the fan throws air out of the back
        machine(E, d)
        fan(E, d, ph * 1.5)
        air(E, d, u, q0=0.78, speed=1.4, n=40)
        E.label(d, "SALE AIRE", 900, 440, 44, color=E.COLD)
        E.arrow(d, 960, 480, 1040, 600, E.COLD, 6, 22)
    elif i == 3:  # less air inside: pressure drops
        machine(E, d)
        fan(E, d, ph * 1.5)
        air(E, d, u, q0=0.78, speed=1.4, n=40)
        signs(E, d, inside=True, outside=False)
        E.label(d, "MENOS PRESIÓN", 640, 440, 46, color=E.COLD)
    elif i == 4:  # outside air has more pressure and comes in through the hose
        machine(E, d, hl_hose=True)
        fan(E, d, ph * 1.5)
        signs(E, d, inside=True, outside=True)
        air(E, d, u, q1=0.45, speed=1.2, n=40, col=E.WHITE)
        E.label(d, "MÁS PRESIÓN", 330, 1000, 42, color=E.HOT)
        E.label(d, "ENTRA", 120, 760, 42, color=E.WHITE)
    elif i == 5:  # the incoming air drags dust and crumbs
        machine(E, d)
        fan(E, d, ph * 1.5)
        air(E, d, u, speed=1.2)
        dust(E, d, u)
        E.label(d, "POLVO Y MIGAS", 640, 1000, 42, color=DUST)
        E.label(d, "LO EMPUJA EL AIRE", 640, 430, 40, color=E.WHITE)
    elif i == 6:  # the bag traps the dirt, the air goes on and out
        machine(E, d, hl_bag=True)
        fan(E, d, ph * 1.5)
        air(E, d, u, speed=1.2)
        dust(E, d, u, kept=16)
        E.label(d, "BOLSA", 520, 440, 46, color=E.AMB)
        E.label(d, "SALE AIRE", 940, 440, 40, color=E.COLD)
        E.label(d, "LA SUCIEDAD SE QUEDA", 560, 940, 38, color=DUST)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.2, 0.8), ("click", s[1] + 0.4), ("whoosh", s[2] + 0.4, 0.8), ("pop", s[3] + 0.6),
            ("whoosh", s[4] + 0.5, 0.8), ("zip", s[5] + 0.5), ("pop", s[6] + 0.7)]
