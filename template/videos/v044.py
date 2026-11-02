"""Video 044 — ¿Cómo apaga el fuego un extintor?
Science: a fire needs heat, fuel and oxygen (the fire triangle); removing any one puts it out. Inside an extinguisher
the extinguishing agent is kept under pressure by a gas. Squeezing the lever opens a valve, and the pressure pushes
the agent up a siphon tube that reaches the bottom, out through the hose and nozzle. It is aimed at the base of the
flames. Depending on the type, the agent cools the fire (water) or smothers it, cutting off oxygen (foam, powder, CO2).
(No pressures, specific gases or fire classes are claimed.)
"""
import math

ID = "044"
TITLE = "¿Cómo apaga el fuego un extintor?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo apaga el fuego un extintor?",
    "El fuego necesita tres cosas: calor, combustible y oxígeno.",
    "Dentro del extintor, un gas mantiene el agente a presión.",
    "Al apretar la palanca de arriba, se abre una válvula.",
    "La presión empuja el agente por un tubo hasta la manguera.",
    "El chorro se dirige a la base de las llamas, no a la punta.",
    "El agente enfría el fuego o lo tapa sin oxígeno, y se apaga.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"apaga", "fuego", "extintor", "calor", "combustible", "oxígeno", "gas", "presión", "palanca",
            "válvula", "agente", "tubo", "manguera", "base", "llamas", "enfría", "tapa"}

FLAME = (255, 120, 40)
AGENT = (225, 232, 245)


def fire(E, d, x, y, u, s=1.0):
    if s <= 0.02:
        return
    for k in range(5):
        dx = (k - 2) * 40 * s
        h = (150 - abs(k - 2) * 35 + 25 * math.sin(u * 9 + k * 1.3)) * s
        E.poly(d, [(x + dx - 34 * s, y), (x + dx, y - h), (x + dx + 34 * s, y)], fill=FLAME)
        E.poly(d, [(x + dx - 16 * s, y), (x + dx, y - h * 0.55), (x + dx + 16 * s, y)], fill=E.AMB)
    E.rrect(d, x - 120, y, x + 120, y + 30, 8, (120, 80, 50))


def cylinder(E, d, x=700, y0=520, y1=1080, cut=False, fill_k=0.6):
    E.rrect(d, x - 110, y0, x + 110, y1, 50, E.HOT_D if cut else E.HOT)
    if cut:
        E.rrect(d, x - 90, y0 + 30, x + 90, y1 - 25, 40, E.BG2)
        ya = y1 - 25 - (y1 - y0 - 55) * fill_k
        E.rrect(d, x - 90, ya, x + 90, y1 - 25, 30, E.mix(E.BG2, AGENT, 0.75))
        E.line(d, [(x, y0 + 10), (x, y1 - 50)], E.SIL_H, 8)   # siphon tube
    E.rrect(d, x - 40, y0 - 50, x + 40, y0 + 5, 10, E.SIL_D)    # valve body


def lever(E, d, x=700, y=470, k=0.0):
    a = -0.35 + 0.35 * k
    E.line(d, [(x - 20, y), (x - 20 - 170 * math.cos(a), y + 170 * math.sin(a))], E.SIL, 14)
    E.line(d, [(x - 20, y + 30), (x - 190, y + 40)], E.SIL_D, 12)


def hose(E, d, x=700, tip=(330, 760)):
    E.line(d, [(x + 40, 470), (x + 160, 520), (x + 170, 700), (x + 60, 860), (520, 880), tip], (40, 40, 48), 16)


def spray(E, d, u, x0, y0, x1, y1, n=18, spread=60):
    for j in range(n):
        f = (u * 1.5 + j / n) % 1
        off = spread * f * math.sin(j * 2.1)
        E.circle(d, x0 + (x1 - x0) * f, y0 + (y1 - y0) * f + off, 8 + 10 * f, fill=E.mix(E.BG1, AGENT, 0.9 - 0.4 * f))


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: extinguisher already spraying at a fire
        cylinder(E, d, x=800, y0=600, y1=1100)
        lever(E, d, x=800, y=550, k=1)
        E.line(d, [(840, 550), (900, 620), (880, 820), (700, 860), (560, 860)], (40, 40, 48), 16)
        fire(E, d, 230, 1000, u, s=1.0 - 0.3 * min(1, u / L))
        spray(E, d, u, 560, 860, 260, 960)
        E.pill(d, "EXTINTOR", 800, 420, 44, bg=E.HOT, fg=E.WHITE)
    elif i == 1:  # fire triangle
        fire(E, d, 540, 830, u, s=0.8)
        pts = [(540, 400), (240, 960), (840, 960)]
        E.line(d, pts + [pts[0]], E.AMB, 8)
        E.label(d, "CALOR", 540, 340, 46, color=E.HOT)
        E.label(d, "COMBUSTIBLE", 260, 1040, 40, color=E.AMB)
        E.label(d, "OXÍGENO", 830, 1040, 40, color=E.COLD)
    elif i == 2:  # inside, gas keeps everything under pressure
        cylinder(E, d, x=540, cut=True)
        for k in range(6):
            a = k * math.pi / 3 + u
            E.circle(d, 540 + 55 * math.cos(a), 660 + 40 * math.sin(a), 10, fill=E.COLD)
        p = 10 * math.sin(u * 6)
        for sx in (-1, 1):
            E.arrow(d, 540 + sx * 40, 760, 540 + sx * (75 + p), 760, E.COLD, 6, 20)
        E.arrow(d, 540, 700, 540, 760 + p, E.COLD, 6, 20)
        E.label(d, "GAS", 540, 600, 40, color=E.COLD)
        E.label(d, "AGENTE", 830, 960, 40, color=E.SIL_H)
        E.arrow(d, 760, 960, 640, 960, E.SIL_H, 6, 22)
        E.pill(d, "A PRESIÓN", 540, 1140, 40, bg=E.COLD, fg=E.BG1)
    elif i == 3:  # squeeze lever, valve opens
        cylinder(E, d, x=640, cut=True)
        k = E.ease(min(1, u / (L * 0.5)))
        lever(E, d, x=640, y=470, k=k)
        E.arrow(d, 400, 330, 420, 400, E.AMB, 6, 22)
        gap = 20 * k
        E.rrect(d, 620, 430 - gap, 660, 450 - gap, 6, E.AMB)
        E.label(d, "PALANCA", 330, 300, 42, color=E.AMB)
        E.label(d, "VÁLVULA", 880, 440, 42, color=E.AMB)
        E.arrow(d, 800, 445, 690, 445, E.AMB, 6, 22)
    elif i == 4:  # pressure pushes the agent up the tube to the hose
        cylinder(E, d, x=540, cut=True)
        lever(E, d, x=540, y=470, k=1)
        E.line(d, [(580, 470), (760, 470), (860, 560), (860, 760)], (40, 40, 48), 16)
        for j in range(8):
            f = (u * 1.2 + j / 8) % 1
            if f < 0.6:
                y = 1030 - (1030 - 480) * (f / 0.6)
                E.circle(d, 540, y, 10, fill=AGENT)
            else:
                g = (f - 0.6) / 0.4
                E.circle(d, 580 + 280 * g, 470 + 120 * g, 10, fill=AGENT)
        E.label(d, "TUBO", 400, 760, 42, color=E.SIL_H)
        E.arrow(d, 440, 760, 525, 760, E.SIL_H, 6, 22)
        E.label(d, "MANGUERA", 880, 840, 40, color=E.SIL_H)
    elif i == 5:  # aim at the base of the flames
        fire(E, d, 300, 980, u, s=1.0)
        E.rrect(d, 760, 760, 900, 800, 12, (40, 40, 48))
        spray(E, d, u, 760, 780, 320, 990, spread=30)
        E.circle(d, 300, 995, 70, outline=E.AMB, w=6)
        E.label(d, "BASE DE LAS LLAMAS", 540, 420, 46, color=E.AMB)
    elif i == 6:  # agent cools or smothers the fire, it goes out
        k = min(1, u / (L * 0.8))
        fire(E, d, 540, 980, u, s=1.0 - k)
        lay = 1000 - 60 * k
        E.rrect(d, 380, lay, 700, 1020, 20, E.mix(E.BG2, AGENT, 0.8))
        E.label(d, "ENFRÍA", 330, 520, 46, color=E.COLD)
        E.label(d, "O TAPA", 750, 520, 46, color=E.SIL_H)
        if k > 0.7:
            E.pill(d, "SE APAGA", 540, 700, 48, bg=E.COLD, fg=E.BG1)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.05, 1.0), ("pop", s[1] + 0.6), ("zip", s[2] + 0.5, 0.8), ("click", s[3] + 0.8),
            ("whoosh", s[4] + 0.4, 1.0), ("whoosh", s[5] + 0.3, 0.8), ("pop", s[6] + 1.2)]
