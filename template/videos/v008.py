"""Video 008 — ¿Cómo funciona la cisterna del inodoro?
Mechanism: the flush lever pulls a chain that lifts the rubber flapper (flush valve) at the bottom of the
tank; the water drains by gravity into the bowl. As the level drops, the float drops and opens the fill
(inlet) valve. When the tank is nearly empty the flapper falls back onto its seat and the tank refills.
The float rises with the water and, at the set level, closes the fill valve — that is why the tank always
fills to the same level. The overflow tube sends any excess to the bowl if the fill valve fails.
(A classic ball float on an arm is drawn; volumes per flush are not claimed.)
"""
import math

ID = "008"
TITLE = "¿Cómo funciona la cisterna del inodoro?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "Siempre se llena justo hasta el mismo nivel. ¿Cómo lo sabe?",
    "La palanca levanta una tapa de goma en el fondo.",
    "Y el agua cae de golpe hacia la taza.",
    "Al bajar el agua, baja el flotador y se abre la válvula de entrada.",
    "La tapa se cierra y el tanque vuelve a llenarse.",
    "El flotador sube con el agua y, al llegar al nivel, cierra la válvula.",
    "Si algo falla, un tubo de rebose envía el exceso a la taza.",
    "Sígueme para descubrir cómo funcionan las cosas.",
]
KEYWORDS = {"nivel", "palanca", "tapa", "goma", "fondo", "agua", "taza", "flotador", "válvula", "entrada", "cierra",
            "llenarse", "sube", "rebose", "exceso", "cosas"}

WATER, WATER_D = (60, 140, 220), (40, 105, 180)
TANK = (40, 52, 78)
RUBBER = (200, 70, 60)
FLOAT = (240, 244, 248)

TX0, TX1, TY0, TY1 = 140, 940, 360, 1000      # tank interior
FULL = 640                                     # set water level
OV_X, OV_TOP = 330, 560                        # overflow tube (x centre, top)
FV_X0, FV_X1 = 440, 560                        # flush-valve opening at the bottom
PIV = (860, 430)                               # fill-valve outlet / float-arm pivot

def tank(E, d, level, flap_open=0.0, valve_open=False, lever=0.0, flow_down=False, u=0.0, ov_flow=False):
    E.rrect(d, TX0 - 20, TY0 - 20, TX1 + 20, TY1 + 20, 26, TANK, outline=E.SIL, w=5)
    # water
    if level < TY1:
        E.rrect(d, TX0, level, TX1, TY1, 0, WATER)
        for k in range(6):
            x = TX0 + 40 + k * 130 + 20 * math.sin(u * 2 + k)
            E.line(d, [(x, level + 10), (x + 50, level + 10)], WATER_D, 4)
    # drain pipe to the bowl
    E.rrect(d, FV_X0 + 10, TY1 + 20, FV_X1 - 10, 1180, 0, TANK, outline=E.SIL, w=4)
    if flow_down:
        for k in range(4):
            y = TY1 + 30 + ((u * 300 + k * 40) % 150)
            E.arrow(d, 500, y, 500, y + 30, color=WATER, w=8, head=20)
    # overflow tube (rises from the flush valve)
    E.rrect(d, OV_X - 20, OV_TOP, OV_X + 20, TY1, 6, (70, 84, 112), outline=E.SIL, w=3)
    E.line(d, [(OV_X, TY1), (OV_X, TY1 + 10), (FV_X0, TY1 + 10)], (70, 84, 112), 14)
    if ov_flow:
        for k in range(3):
            y = OV_TOP + 20 + ((u * 260 + k * 140) % 420)
            E.arrow(d, OV_X, y, OV_X, y + 30, color=E.WHITE, w=6, head=18)
    # flapper hinged at the left edge of the opening
    ang = math.radians(-70 * flap_open)
    hx, hy = FV_X0 - 10, TY1 - 8
    pts = [(0, -10), (140, -10), (140, 10), (0, 10)]
    rot = [(hx + px * math.cos(ang) - py * math.sin(ang), hy + px * math.sin(ang) + py * math.cos(ang)) for px, py in pts]
    E.poly(d, rot, fill=RUBBER, outline=(130, 40, 30), w=2)
    tip = (hx + 120 * math.cos(ang), hy + 120 * math.sin(ang))
    # lever + chain
    la = math.radians(-14 * lever)
    lx0, ly0 = TX0 + 10, 410
    lx1, ly1 = lx0 + 360 * math.cos(la), ly0 + 360 * math.sin(la)
    E.rrect(d, TX0 - 90, 380, TX0 - 10, 440, 14, E.SIL)
    E.line(d, [(lx0, ly0), (lx1, ly1)], E.SIL, 12)
    E.line(d, [(lx1, ly1), tip], E.SIL_D, 4)
    # fill valve: vertical pipe from below, outlet near the top
    E.rrect(d, PIV[0] - 18, PIV[1], PIV[0] + 18, TY1 + 40, 6, (110, 120, 140), outline=E.SIL, w=3)
    E.circle(d, PIV[0], PIV[1], 30, fill=(150, 160, 180), outline=E.SIL, w=3)
    if valve_open:
        for k in range(4):
            y = PIV[1] + 50 + ((u * 320 + k * 60) % 240)
            E.arrow(d, PIV[0] - 50, y, PIV[0] - 50, y + 26, color=(170, 215, 255), w=6, head=16)
    # float on an arm: ball centre sits at the water surface
    by = max(min(level, PIV[1] + 330), PIV[1] + 60)   # the arm limits how low the float can hang
    bx = PIV[0] - math.sqrt(max(0, 360 ** 2 - (by - PIV[1]) ** 2))
    E.line(d, [PIV, (bx, by)], E.SIL, 8)
    E.circle(d, bx, by, 55, fill=FLOAT, outline=E.SIL_D, w=4)
    return (bx, by)

def scene(i, u, L, E, im, d):
    cx = 540
    if i == 0:  # always the same level
        tank(E, d, FULL, u=u)
        for x in range(TX0, TX1, 50):
            E.line(d, [(x, FULL), (x + 28, FULL)], E.AMB, 5)
        E.label(d, "MISMO NIVEL", cx, 500, 52)
        if u > 0.8: E.label(d, "?", 940, 300, 110)
    elif i == 1:  # lever lifts the rubber flapper
        p = E.ease(u / 0.9)
        tank(E, d, FULL, flap_open=p, lever=p, u=u)
        E.arrow(d, 60, 290, 60, 380, w=6)
        if u > 0.7:
            E.label(d, "TAPA DE GOMA", 640, 900, 42)
            E.label(d, "PALANCA", 300, 310, 42, color=E.WHITE)
    elif i == 2:  # water drains to the bowl
        p = E.ease(u / L)
        tank(E, d, E.lerp(FULL, 930, p), flap_open=1, lever=1, flow_down=True, u=u)
        E.label(d, "A LA TAZA", 760, 1120, 46)
    elif i == 3:  # level drops, float drops, inlet opens
        p = E.ease(u / (L * 0.8))
        bx, by = tank(E, d, E.lerp(930, 960, p), flap_open=1 - p, lever=1 - p, valve_open=u > 0.8, u=u)
        E.label(d, "FLOTADOR", bx - 130, by - 110, 42)
        if u > 0.8: E.label(d, "ENTRA AGUA", 660, 380, 44, color=(170, 215, 255))
    elif i == 4:  # flapper closed, tank refills
        p = E.ease(u / L)
        tank(E, d, E.lerp(960, 760, p), valve_open=True, u=u)
        E.arrow(d, 250, 900, 250, 760, color=(170, 215, 255), w=6)
        if u > 0.5: E.label(d, "CERRADA", 500, 1110, 44)
    elif i == 5:  # float rises and shuts the valve at the set level
        p = E.ease(u / (L * 0.5))
        tank(E, d, E.lerp(760, FULL, p), valve_open=p < 1, u=u)
        for x in range(TX0, TX1, 50):
            E.line(d, [(x, FULL), (x + 28, FULL)], E.AMB, 5)
        if p >= 1:
            E.pill(d, "VÁLVULA CERRADA", cx, 300, 40)
            E.cross(d, PIV[0] - 50, 600, 30)
    elif i == 6:  # overflow tube safety
        tank(E, d, OV_TOP + 4, valve_open=True, u=u, ov_flow=True)
        E.label(d, "TUBO DE REBOSE", 470, 480, 42)
        E.arrow(d, 390, 510, OV_X + 30, OV_TOP + 20, w=5)
        if u > 0.6: E.label(d, "A LA TAZA", 760, 1120, 46)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("click", s[1] + 0.3), ("whoosh", s[2], 1.2), ("pop", s[3] + 0.9), ("click", s[5] + 1.6), ("whoosh", s[6] + 0.4, 0.6)]
