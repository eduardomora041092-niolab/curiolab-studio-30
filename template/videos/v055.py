"""Video 055 — ¿Cómo funciona un inflador de bicicleta?
Science: a hand pump has a cylinder, a piston moved by the handle and a one-way (check) valve on the way out to the
wheel. Pushing the handle down reduces the volume of the air trapped in the cylinder, so its pressure rises. When it
exceeds the pressure on the other side, the valve opens and the air goes towards the wheel. When the piston goes back
up the pressure in the cylinder drops and the valve closes, so the wheel's air cannot come back. Meanwhile new air
enters the cylinder, ready for the next stroke; every stroke adds a little more air to the tyre.
(No pressures, volumes or where exactly the valve or the air inlet sit in each model are claimed.)
"""
import math

ID = "055"
TITLE = "¿Cómo funciona un inflador de bicicleta?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Por qué el aire de un inflador no vuelve atrás?",
    "Por dentro tiene un cilindro, un pistón y una válvula.",
    "Al bajar el mango, el pistón comprime el aire del cilindro.",
    "La presión sube, abre la válvula y el aire pasa a la rueda.",
    "Al subir el pistón, la válvula se cierra sola.",
    "Mientras, entra aire nuevo en el cilindro para el siguiente bombeo.",
    "Así, cada bombeo mete un poco más de aire en la rueda.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"inflador", "aire", "atrás", "cilindro", "pistón", "válvula", "mango", "comprime", "presión", "abre",
            "rueda", "cierra", "nuevo", "bombeo"}

CX0, CX1 = 380, 560          # cylinder walls
CYT, CYB = 420, 1000         # cylinder top / bottom
VX, VY = 470, 1030           # check valve centre (below the cylinder)
WX, WY, WR = 830, 760, 190   # wheel
TYRE = (52, 56, 66)
AIR = (150, 205, 255)


def head_y(p):
    return 515 + 400 * p      # p: 0 top .. 1 bottom


def pump(E, d, p, valve_open=False, flow=None, hi_cyl=False, hi_pis=False, hi_valve=False, wheel_fill=0.4, n_air=26):
    hy = head_y(p)
    # wheel (tyre ring + rim), air dots inside the tyre
    E.circle(d, WX, WY, WR, fill=TYRE, outline=(30, 32, 40), w=4)
    E.circle(d, WX, WY, WR - 46, fill=E.BG2, outline=E.SIL_D, w=6)
    E.circle(d, WX, WY, 16, fill=E.SIL_D)
    for k in range(10):
        a = 2 * math.pi * k / 10
        E.line(d, [(WX, WY), (WX + (WR - 50) * math.cos(a), WY + (WR - 50) * math.sin(a))], E.SIL_D, 2)
    nd = int(6 + 18 * wheel_fill)
    for k in range(nd):
        a = 2 * math.pi * k / nd + 0.2
        E.circle(d, WX + (WR - 23) * math.cos(a), WY + (WR - 23) * math.sin(a), 6, fill=AIR)
    # hose: valve -> wheel valve stem (bottom-left of the rim)
    sx, sy = WX - (WR - 30) * 0.72, WY + (WR - 30) * 0.72
    hose = [(VX, VY + 22), (VX, 1120), (sx, 1120), (sx, sy)]
    E.line(d, hose, (60, 66, 80), 26)
    E.line(d, hose, (90, 98, 116), 14)
    if flow is not None:   # air travelling along the hose
        segs = [(hose[i], hose[i + 1]) for i in range(3)]
        lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]; tot = sum(lens)
        for k in range(5):
            s = ((flow + k / 5) % 1.0) * tot
            for (a, b), l in zip(segs, lens):
                if s <= l:
                    f = s / l; E.circle(d, a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, 7, fill=AIR); break
                s -= l
    # cylinder
    cc = E.AMB if hi_cyl else E.SIL_D
    E.rrect(d, CX0, CYT, CX1, CYB, 14, (34, 48, 78), outline=cc, w=6)
    # air in the chamber under the piston (denser when compressed)
    top = hy + 30; bot = CYB - 14
    for k in range(n_air):
        fx = ((k * 37) % 13) / 12.0; fy = ((k * 53) % 17) / 16.0
        E.circle(d, CX0 + 26 + fx * (CX1 - CX0 - 52), top + fy * max(4, bot - top), 7, fill=AIR)
    # piston + rod + handle
    pc = E.AMB if hi_pis else E.SIL
    E.rrect(d, CX0 + 8, hy - 8, CX1 - 8, hy + 22, 8, pc, outline=E.SIL_D, w=3)
    E.rrect(d, (CX0 + CX1) / 2 - 10, hy - 190, (CX0 + CX1) / 2 + 10, hy - 8, 6, E.SIL_H)
    E.rrect(d, (CX0 + CX1) / 2 - 130, hy - 230, (CX0 + CX1) / 2 + 130, hy - 190, 18, E.BLUE, outline=E.BLUE_D, w=3)
    E.rrect(d, CX0 - 6, CYT - 14, CX1 + 6, CYT + 8, 6, E.SIL_D)   # cap
    # check valve: housing + flap
    vc = E.AMB if hi_valve else E.SIL_D
    E.rrect(d, VX - 44, CYB - 4, VX + 44, VY + 24, 10, (40, 52, 80), outline=vc, w=5)
    if valve_open:
        E.line(d, [(VX - 30, VY - 10), (VX + 10, VY + 18)], E.AMB if hi_valve else E.SIL_H, 9)
    else:
        E.line(d, [(VX - 32, VY), (VX + 32, VY)], E.AMB if hi_valve else E.SIL_H, 9)
    return hy


def scene(i, u, L, E, im, d):
    cx = (CX0 + CX1) / 2
    if i == 0:  # in action from frame 0: pumping, air pushed into the wheel
        ph = (u * 1.6) % 1.0
        p = 0.5 - 0.5 * math.cos(2 * math.pi * ph)
        down = ph < 0.5
        hy = pump(E, d, p, valve_open=down, flow=u * 1.2 if down else None, wheel_fill=0.3 + 0.1 * u / L)
        E.arrow(d, cx + 180, hy - 240, cx + 180, hy - 150, E.AMB, 8, 26) if down else None
        E.pill(d, "¿NO VUELVE?", 830, 420, 42)
    elif i == 1:  # parts
        pump(E, d, 0.3, hi_cyl=True, hi_pis=True, hi_valve=True)
        E.label(d, "CILINDRO", 230, 820, 42, color=E.AMB)
        E.label(d, "PISTÓN", 690, head_y(0.3) - 20, 42, color=E.AMB)
        E.label(d, "VÁLVULA", 250, 1060, 42, color=E.AMB)
    elif i == 2:  # downstroke compresses the air
        k = E.ease(min(1, u / (L * 0.8)))
        p = 0.1 + 0.55 * k
        hy = pump(E, d, p, hi_pis=True, n_air=26)
        E.arrow(d, cx + 180, hy - 260, cx + 180, hy - 150, E.AMB, 9, 28)
        E.label(d, "COMPRIME", 230, 1000 - (1000 - hy) / 2 + 40, 42, color=E.AMB)
    elif i == 3:  # pressure rises, valve opens, air goes to the wheel
        k = E.ease(min(1, u / (L * 0.8)))
        p = 0.65 + 0.3 * k
        pump(E, d, p, valve_open=True, flow=u * 1.3, hi_valve=True, wheel_fill=0.4 + 0.2 * k)
        E.label(d, "PRESIÓN", 230, 900, 42, color=E.HOT)
        E.label(d, "SE ABRE", 250, 1080, 40, color=E.AMB)
        E.arrow(d, 640, 1120, 690, 1120, E.AMB, 7, 22)
    elif i == 4:  # upstroke: valve closes by itself
        k = E.ease(min(1, u / (L * 0.8)))
        p = 0.95 - 0.7 * k
        hy = pump(E, d, p, valve_open=False, hi_valve=True, wheel_fill=0.6, n_air=10 + int(10 * k))
        E.arrow(d, cx + 180, hy - 150, cx + 180, hy - 260, E.AMB, 9, 28)
        E.label(d, "SE CIERRA", 245, 1080, 40, color=E.AMB)
        E.cross(d, 690, 1060, 26, E.HOT, 9)
    elif i == 5:  # new air enters the cylinder for the next stroke
        k = E.ease(min(1, u / (L * 0.8)))
        p = 0.25 - 0.15 * k
        hy = pump(E, d, p, wheel_fill=0.6, n_air=12 + int(14 * k))
        for sx in (CX0 + 30, CX1 - 30):
            yy = hy - 10 + 60 * ((u * 1.5) % 1.0)
            E.arrow(d, sx, yy - 40, sx, yy + 30, E.COLD, 6, 20)
        E.label(d, "AIRE NUEVO", 230, 760, 42, color=E.AMB)
    elif i == 6:  # every stroke adds a bit more air
        ph = (u * 1.4) % 1.0
        p = 0.5 - 0.5 * math.cos(2 * math.pi * ph)
        down = ph < 0.5
        pump(E, d, p, valve_open=down, flow=u * 1.2 if down else None, wheel_fill=0.6 + 0.4 * u / L)
        E.label(d, "+ AIRE", WX, WY, 50, color=E.AMB)
        E.pill(d, "CADA BOMBEO SUMA", 790, 420, 40)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 0.4), ("pop", s[1] + 0.6), ("whoosh", s[2] + 0.3, 0.9), ("click", s[3] + 0.8),
            ("click", s[4] + 0.9), ("whoosh", s[5] + 0.3, 0.9), ("pop", s[6] + 0.6)]
