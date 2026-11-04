"""Video 049 — ¿Cómo sale el líquido de un aerosol?
Science: an aerosol can holds the liquid product together with a propellant gas kept at a pressure higher than the
outside air. The gas presses down on the surface of the liquid. A dip tube runs from the bottom of the can up to a
valve in the lid. Pressing the button opens the valve: the gas pressure pushes the liquid up the tube and out through
the small nozzle, where it leaves as a spray. Releasing the button, a spring closes the valve and the can is sealed.
(No pressures, propellant types, droplet sizes or exact valve designs are claimed.)
"""
import math

ID = "049"
TITLE = "¿Cómo sale el líquido de un aerosol?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Por qué sale el líquido solo al presionar un aerosol?",
    "Dentro del bote hay líquido y un gas a presión.",
    "Ese gas empuja con fuerza sobre la superficie del líquido.",
    "Un tubo va desde el fondo hasta una válvula en la tapa.",
    "Al presionar el botón, la válvula se abre.",
    "El gas empuja el líquido por el tubo y sale por la boquilla.",
    "Al soltar, un muelle cierra la válvula y el bote queda sellado.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"líquido", "presionar", "aerosol", "bote", "gas", "presión", "empuja", "superficie", "tubo", "fondo",
            "válvula", "tapa", "botón", "abre", "boquilla", "muelle", "cierra", "sellado"}

LIQ = (110, 190, 255)
CAN = (210, 70, 90)
GAS = (190, 200, 220)
CX = 620           # can centre x
LTOP = 860         # liquid surface y


def can(E, d, cut=True, level=LTOP):
    E.rrect(d, CX - 180, 560, CX + 180, 1160, 36, CAN if not cut else E.mix(E.BG2, CAN, 0.45),
            outline=CAN, w=5)
    E.poly(d, [(CX - 180, 580), (CX - 90, 500), (CX + 90, 500), (CX + 180, 580)], fill=E.mix(E.BG2, CAN, 0.6),
           outline=CAN, w=4)                                              # dome
    if cut:
        E.rrect(d, CX - 168, level, CX + 168, 1148, 28, E.mix(E.BG2, LIQ, 0.6))


def gas(E, d, u, strong=False, level=LTOP):
    for j in range(16):
        gx = CX - 145 + (j * 137) % 290
        gy = 625 + (j * 89 + j * j * 7) % max(40, level - 665) + 10 * math.sin(u * 3 + j)
        E.circle(d, gx, gy, 9 if strong else 7, fill=GAS)


def tube(E, d, filled=0.0, flow_u=None):
    E.line(d, [(CX, 1135), (CX, 495)], E.SIL_D, 14)
    if filled > 0:
        E.line(d, [(CX, 1135), (CX, 1135 - 640 * filled)], LIQ, 8)
    if flow_u is not None:
        for j in range(6):
            f = (flow_u * 1.4 + j / 6) % 1
            E.circle(d, CX, 1120 - 620 * f, 8, fill=E.WHITE)


def valve(E, d, open_=False):
    E.rrect(d, CX - 40, 470, CX + 40, 510, 8, E.SIL)
    y = 492 if open_ else 482
    E.rrect(d, CX - 16, y - 20, CX + 16, y + 20, 6, E.AMB if open_ else E.SIL_D)


def button(E, d, press=0.0):
    y = 400 + 30 * press
    E.rrect(d, CX - 70, y, CX + 70, y + 70, 16, E.SIL_H)
    E.rrect(d, CX - 100, y + 20, CX - 70, y + 44, 6, E.SIL_D)          # nozzle (points left)
    return y + 32


def spray(E, d, u, ny, n=34):
    for j in range(n):
        f = (u * 1.4 + j / n) % 1
        a = math.pi + 0.42 * math.sin(j * 2.1)
        r = 15 + 380 * f
        E.circle(d, CX - 100 + r * math.cos(a), ny + r * math.sin(a), max(2, 10 - 7 * f),
                 fill=E.mix(E.BG1, LIQ, 0.95 - 0.5 * f))


def finger(E, d, press):
    y = 300 + 30 * press
    E.rrect(d, CX - 55, y - 40, CX + 55, y + 100, 50, (230, 190, 160))


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: button pressed, spray coming out
        p = 0.85 + 0.15 * math.sin(u * 5)
        can(E, d, cut=False); ny = button(E, d, p); finger(E, d, p)
        spray(E, d, u, ny)
        E.pill(d, "AEROSOL", CX, 1080, 44, bg=E.WHITE)
    elif i == 1:  # liquid + gas under pressure
        can(E, d); gas(E, d, u); tube(E, d); valve(E, d); button(E, d)
        E.label(d, "GAS A PRESIÓN", CX, 700, 44, color=E.WHITE)
        E.label(d, "LÍQUIDO", CX, 1010, 48, color=E.WHITE)
    elif i == 2:  # gas pushes down on liquid surface
        can(E, d); gas(E, d, u, strong=True); tube(E, d); valve(E, d); button(E, d)
        for k, x in enumerate((CX - 120, CX - 60, CX + 60, CX + 120)):
            o = 10 * math.sin(u * 6 + k)
            E.arrow(d, x, 720 + o, x, 840 + o, E.AMB, 7, 24)
        E.label(d, "EMPUJA", 230, 790, 50, color=E.AMB)
    elif i == 3:  # dip tube from bottom to valve
        can(E, d); gas(E, d, u); tube(E, d, filled=0.45); valve(E, d); button(E, d)
        k = E.ease(min(1, u / (L * 0.6)))
        E.arrow(d, CX + 40, 1110, CX + 40, 1110 - 580 * k, E.AMB, 7, 26)
        E.label(d, "TUBO", CX + 120, 1000, 46, color=E.WHITE)
        E.pill(d, "VÁLVULA", 360, 470, 40)
        E.arrow(d, 470, 475, 570, 488, E.AMB, 6, 22)
    elif i == 4:  # pressing button opens valve
        p = E.ease(min(1, u / (L * 0.5)))
        can(E, d); gas(E, d, u); tube(E, d, filled=0.45); valve(E, d, open_=p > 0.5); button(E, d, p)
        finger(E, d, p)
        E.label(d, "SE ABRE", 330, 520, 48, color=E.AMB)
    elif i == 5:  # gas pushes liquid up the tube and out of nozzle
        can(E, d); gas(E, d, u, strong=True); tube(E, d, filled=1.0, flow_u=u); valve(E, d, True)
        ny = button(E, d, 1.0); finger(E, d, 1.0)
        spray(E, d, u, ny, n=26)
        for x in (CX - 120, CX + 120):
            E.arrow(d, x, 730, x, 840, E.AMB, 6, 22)
        E.label(d, "BOQUILLA", 260, 360, 44, color=E.WHITE)
    elif i == 6:  # release: spring closes valve, sealed
        p = 1 - E.ease(min(1, u / (L * 0.5)))
        can(E, d); gas(E, d, u); tube(E, d, filled=0.45); valve(E, d, open_=p > 0.5); button(E, d, p)
        E.line(d, [(CX + 60, 520)] + [(CX + 50 + (24 if k % 2 else 0), 530 + 10 * k) for k in range(6)], E.SIL_H, 5)
        E.label(d, "MUELLE", 870, 540, 42, color=E.SIL_H)
        E.pill(d, "SELLADO", CX, 1080, 44)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 1.2), ("pop", s[1] + 0.6), ("zip", s[2] + 0.4, 0.8), ("zip", s[3] + 0.4, 0.8),
            ("click", s[4] + 0.8), ("whoosh", s[5] + 0.3, 1.2), ("click", s[6] + 0.8)]
