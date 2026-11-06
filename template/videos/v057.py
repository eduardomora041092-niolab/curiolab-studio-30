"""Video 057 — ¿Por qué ocurren los terremotos?
Science: the Earth's rigid outer layer is broken into large tectonic plates that move very slowly (of the order of
centimetres per year). Along faults, friction keeps the blocks of rock locked while the motion goes on, so the rock on
both sides deforms elastically and stores strain energy, like a spring. When the stress exceeds the frictional
resistance, the fault slips suddenly (elastic rebound). The released energy travels as seismic waves that make the
ground shake: that is the earthquake.
(No magnitudes, depths, number of plates or exact speeds are claimed; prediction is not discussed.)
"""
import math

ID = "057"
TITLE = "¿Por qué ocurren los terremotos?"
SUBTITLE = "CIENCIA EN 30 SEGUNDOS"
LINES = [
    "¿Por qué de repente tiembla el suelo bajo tus pies?",
    "La corteza de la Tierra está dividida en grandes placas.",
    "Las placas se mueven muy despacio, unos centímetros al año.",
    "En las fallas, el roce las deja atascadas.",
    "La roca se deforma y acumula tensión, como un muelle.",
    "Cuando la tensión vence al roce, la falla se desliza de golpe.",
    "La energía sale en ondas sísmicas: eso es el terremoto.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"tiembla", "suelo", "corteza", "tierra", "placas", "despacio", "centímetros", "fallas", "roce",
            "atascadas", "roca", "deforma", "tensión", "muelle", "vence", "falla", "desliza", "golpe", "energía",
            "ondas", "sísmicas", "terremoto"}

GROUND = (96, 76, 60)
GROUND_D = (66, 52, 42)
GRASS = (70, 130, 80)
ROAD = (60, 64, 74)
STRIPE = (250, 230, 150)
SKY_LINE = 700
FX = 540             # fault x in map view


def section(E, d, shake=0.0, t=0.0, waves=0.0):
    """Cross-section: ground with a house; optional shaking and seismic waves from a focus."""
    dx = shake * math.sin(t * 40 + 1.2)
    E.rrect(d, 40, SKY_LINE, 1040, 1180, 20, GROUND, outline=GROUND_D, w=4)
    E.rrect(d, 40, SKY_LINE, 1040, SKY_LINE + 22, 10, GRASS)
    # fault line in the section
    E.line(d, [(560, SKY_LINE + 20), (620, 1180)], GROUND_D, 6)
    fx, fy = 600, 1040
    if waves > 0:
        for k in range(4):
            r = ((waves + k / 4) % 1.0) * 320
            if r > 20:
                d.arc([(fx - r) * 2, (fy - r) * 2, (fx + r) * 2, (fy + r) * 2], 180, 360, fill=E.AMB, width=10)
        E.circle(d, fx, fy, 16, fill=E.HOT)
    # house
    hx, hy = 300 + dx, SKY_LINE
    E.rrect(d, hx - 90, hy - 150, hx + 90, hy, 6, (220, 210, 190), outline=E.SIL_D, w=3)
    E.poly(d, [(hx - 115, hy - 145), (hx, hy - 240), (hx + 115, hy - 145)], fill=E.HOT_D)
    E.rrect(d, hx - 25, hy - 80, hx + 25, hy, 4, (120, 80, 50))
    # tree
    tx = 820 + dx * 1.3
    E.rrect(d, tx - 12, SKY_LINE - 110, tx + 12, SKY_LINE, 4, (110, 75, 45))
    E.circle(d, tx, SKY_LINE - 150, 62, fill=GRASS)
    return fx, fy


def mapview(E, d, slip=0.0, bend=0.0, hi_fault=False, arrows=True, lock=False):
    """Top view of two blocks separated by a fault; a road crosses it. bend = elastic strain, slip = offset."""
    E.rrect(d, 80, 330, FX - 4, 1170, 16, (110, 92, 72), outline=GROUND_D, w=4)
    E.rrect(d, FX + 4, 330, 1000, 1170, 16, (98, 84, 68), outline=GROUND_D, w=4)
    E.line(d, [(FX, 330), (FX, 1170)], E.AMB if hi_fault else GROUND_D, 10 if hi_fault else 6)
    # road: left part shifted down, right part shifted up by `slip`; elastic bend near the fault
    yc = 750
    def road_y(x):
        side = -1 if x < FX else 1                    # left block moves up (-y), right block down (+y)
        e = 1 - math.exp(-abs(x - FX) / 160)          # locked near the fault, free far from it
        return yc + side * 70 * (bend * e + slip)
    pts_l = [(x, road_y(x)) for x in range(80, FX - 2, 8)]
    pts_r = [(x, road_y(x)) for x in range(FX + 4, 1001, 8)]
    for pts in (pts_l, pts_r):
        E.line(d, pts, ROAD, 60)
        E.line(d, pts, STRIPE, 5)
    if arrows:
        E.arrow(d, 300, 1100, 300, 980, E.AMB, 9, 30)    # left block moves "up" (north)
        E.arrow(d, 780, 980, 780, 1100, E.AMB, 9, 30)    # right block moves "down"
        E.arrow(d, 300, 480, 300, 360, E.AMB, 9, 30)
        E.arrow(d, 780, 360, 780, 480, E.AMB, 9, 30)
    if lock:
        for y in (560, 940):
            E.circle(d, FX, y, 24, fill=E.HOT)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: the ground is shaking, waves spreading
        section(E, d, shake=10, t=u, waves=0.15 + u * 1.2)
        E.pill(d, "¡TIEMBLA!", 820, 400, 44)
    elif i == 1:  # crust divided into plates
        k = E.ease(min(1, u / (L * 0.6)))
        cx, cy, R = 540, 760, 330
        E.circle(d, cx, cy, R, fill=(40, 90, 150), outline=E.SIL_D, w=4)
        # plate boundaries
        E.line(d, [(cx - R * 0.95, cy - 80), (cx - 120, cy - 40), (cx + 60, cy - 200), (cx + R * 0.7, cy - R * 0.7)], E.AMB, 8)
        E.line(d, [(cx + 60, cy - 200), (cx + 120, cy + 60), (cx + R * 0.92, cy + 130)], E.AMB, 8)
        E.line(d, [(cx - 120, cy - 40), (cx - 60, cy + 180), (cx - 200, cy + R * 0.82)], E.AMB, 8)
        E.line(d, [(cx - 60, cy + 180), (cx + 120, cy + 60)], E.AMB, 8)
        if k > 0.3:
            E.label(d, "PLACA", cx - 180, cy - 170, 40, color=E.WHITE)
            E.label(d, "PLACA", cx + 200, cy - 40, 40, color=E.WHITE)
            E.label(d, "PLACA", cx - 210, cy + 100, 40, color=E.WHITE)
            E.label(d, "PLACA", cx + 110, cy + 220, 40, color=E.WHITE)
    elif i == 2:  # plates move slowly, in opposite directions along the fault
        mapview(E, d, bend=0.0)
        E.label(d, "MUY DESPACIO", 540, 1140, 40, color=E.AMB)
    elif i == 3:  # friction locks the fault
        mapview(E, d, hi_fault=True, lock=True)
        E.label(d, "FALLA", FX + 120, 400, 44, color=E.AMB)
        E.label(d, "ROCE", FX + 100, 640, 44, color=E.HOT)
    elif i == 4:  # rock deforms, stores strain like a spring
        k = E.ease(min(1, u / (L * 0.85)))
        mapview(E, d, bend=k, lock=True)
        E.label(d, "TENSIÓN", 300, 560, 44, color=E.HOT)
    elif i == 5:  # sudden slip: the road snaps to an offset
        k = 1.0 if u > L * 0.3 else 0.0
        mapview(E, d, bend=1 - k, slip=k, hi_fault=k > 0, arrows=False)
        if k > 0:
            E.pill(d, "¡DE GOLPE!", 540, 420, 44)
    elif i == 6:  # energy released as seismic waves
        section(E, d, shake=8 * (1 - u / L), t=u, waves=0.15 + u * 1.2)
        E.label(d, "ONDAS SÍSMICAS", 760, 1110, 40, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 1.2), ("pop", s[1] + 0.8), ("whoosh", s[2] + 0.4, 0.8), ("click", s[3] + 0.8),
            ("zip", s[4] + 0.3, 1.2), ("click", s[5] + 0.5 + 0.3 * (s[6] - s[5])), ("whoosh", s[6] + 0.2, 1.2)]
