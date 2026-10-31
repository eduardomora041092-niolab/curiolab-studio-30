"""Video 037 — ¿Cómo produce luz un LED?
Science: an LED is a diode made of a semiconductor crystal with two regions: an n-type region with extra free
electrons and a p-type region with "holes" (places where an electron is missing). Where they meet there is a p-n
junction. When the LED is connected the right way to a battery, electrons and holes are pushed toward the junction.
There an electron falls into a hole (recombination) and drops to a lower energy level; the energy it loses is
released as a photon, a particle of light. The colour depends on the semiconductor material. Because light comes
from this process and not from heating a filament, much less energy is wasted as heat than in an incandescent bulb.
(No efficiencies, voltages, wavelengths or specific materials are claimed.)
"""
import math, random

ID = "037"
TITLE = "¿Cómo produce luz un LED?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo produce luz un LED?",
    "Dentro hay un cristal semiconductor con dos zonas distintas.",
    "Una zona tiene electrones de sobra; la otra, huecos libres.",
    "Al conectar la pila, ambos se empujan hacia la unión.",
    "Cuando un electrón cae en un hueco, suelta energía.",
    "Esa energía sale como una partícula de luz: un fotón.",
    "No calienta ningún filamento, por eso desperdicia mucho menos calor.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"luz", "led", "cristal", "semiconductor", "zonas", "electrones", "huecos", "pila", "unión",
            "electrón", "hueco", "energía", "partícula", "fotón", "filamento", "calor"}

N_COL, P_COL = (60, 120, 220), (226, 90, 70)
GLOW = (120, 255, 170)
EL, HOLE = (120, 200, 255), (255, 200, 200)

def led_bulb(E, d, x, y, on=1.0, u=0.0):
    """Generic 5 mm style LED: dome + two legs."""
    if on > 0:
        for r, a in ((230, 0.12), (170, 0.22), (120, 0.38)):
            E.circle(d, x, y - 40, r * (0.9 + 0.1 * math.sin(u * 6)), fill=E.mix(E.BG1, GLOW, a * on))
    E.rrect(d, x - 70, y - 120, x + 70, y + 60, 60, E.mix((60, 90, 80), GLOW, 0.75 * on))
    E.rrect(d, x - 85, y + 50, x + 85, y + 80, 8, E.mix((60, 90, 80), GLOW, 0.5 * on))
    E.line(d, [(x - 35, y + 80), (x - 35, y + 300)], E.SIL_D, 12)
    E.line(d, [(x + 35, y + 80), (x + 35, y + 260)], E.SIL_D, 12)

def photon(E, d, x, y, ang, f, col=GLOW):
    r = 40 + 300 * f
    E.wave(d, x + r * math.cos(ang), y + r * math.sin(ang), x + (r + 90) * math.cos(ang), y + (r + 90) * math.sin(ang),
           36, 9, col, 5, head=True)

def crystal(E, d, x0=140, y0=430, x1=940, y1=930):
    xm = (x0 + x1) / 2
    E.rrect(d, x0, y0, xm, y1, 24, E.mix(E.BG2, N_COL, 0.45))
    E.rrect(d, xm, y0, x1, y1, 24, E.mix(E.BG2, P_COL, 0.45))
    E.line(d, [(xm, y0), (xm, y1)], E.AMB, 6)
    return xm

def carriers(E, d, u, x0, x1, y0, y1, n, kind, seed, drift=0.0, xmax=None):
    g = random.Random(seed)
    for _ in range(n):
        px, py, ph = g.random(), g.random(), g.random() * 6.28
        x = x0 + px * (x1 - x0) + drift + 18 * math.sin(u * 3 + ph)
        if xmax is not None:
            x = min(x, xmax) if kind == "e" else max(x, xmax)
        y = y0 + py * (y1 - y0) + 18 * math.cos(u * 2.6 + ph)
        if kind == "e":
            E.circle(d, x, y, 15, fill=EL)
        else:
            E.circle(d, x, y, 15, outline=HOLE, w=5)

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: LED already glowing and emitting light
        led_bulb(E, d, 540, 640, on=1.0, u=u)
        for k in range(8):
            photon(E, d, 540, 600, -math.pi / 2 + (k - 3.5) * 0.38, (u * 0.8 + k * 0.13) % 1)
        E.pill(d, "LED", 540, 1060, 46)
    elif i == 1:  # semiconductor crystal with two regions
        crystal(E, d)
        E.label(d, "ZONA N", 340, 990, 46, color=E.COLD)
        E.label(d, "ZONA P", 740, 990, 46, color=E.HOT)
        E.pill(d, "SEMICONDUCTOR", 540, 360, 40)
    elif i == 2:  # extra electrons on one side, holes on the other
        xm = crystal(E, d)
        carriers(E, d, u, 180, xm - 40, 470, 890, 14, "e", 1)
        carriers(E, d, u, xm + 40, 900, 470, 890, 14, "h", 2)
        E.label(d, "ELECTRONES", 340, 990, 44, color=EL)
        E.label(d, "HUECOS", 740, 990, 44, color=HOLE)
    elif i == 3:  # battery pushes both toward the junction
        xm = crystal(E, d, y0=470)
        k = E.ease(u / L)
        carriers(E, d, u, 180, xm - 40, 510, 890, 14, "e", 1, drift=120 * k, xmax=xm - 18)
        carriers(E, d, u, xm + 40, 900, 510, 890, 14, "h", 2, drift=-120 * k, xmax=xm + 18)
        E.arrow(d, 230, 430, 470, 430, EL, 7, 26)
        E.arrow(d, 850, 430, 610, 430, HOLE, 7, 26)
        E.rrect(d, 400, 1010, 680, 1090, 14, E.SIL_D)     # battery
        E.rrect(d, 680, 1030, 705, 1070, 6, E.SIL)
        E.label(d, "PILA", 540, 1050, 40, color=E.WHITE)
        E.label(d, "UNIÓN", 540, 330, 44, color=E.AMB)
    elif i == 4:  # electron falls into a hole and releases energy
        xm = crystal(E, d)
        k = E.ease(min(1, u / (L * 0.6)))
        ex = 380 + (xm - 380) * k
        E.circle(d, xm + 4, 680, 26, outline=HOLE, w=6)
        E.circle(d, ex, 680 - 40 * math.sin(math.pi * k), 24, fill=EL)
        if k > 0.95:
            for r in (60, 90):
                E.circle(d, xm, 680, r, outline=E.AMB, w=5)
            E.pill(d, "ENERGÍA", xm, 380, 42)
        E.label(d, "ELECTRÓN", 300, 990, 42, color=EL)
        E.label(d, "HUECO", 780, 990, 42, color=HOLE)
    elif i == 5:  # energy leaves as a photon
        xm = crystal(E, d)
        E.circle(d, xm, 680, 30, fill=E.AMB)
        f = (u * 0.7) % 1
        E.wave(d, xm, 650 - 40 - 320 * f, xm, 650 - 140 - 320 * f, 36, 12, GLOW, 7, head=True) if f < 0.9 else None
        E.wave(d, xm + 20, 660, xm + 260, 470, 36, 10, GLOW, 6)
        E.wave(d, xm - 20, 660, xm - 260, 470, 36, 10, GLOW, 6)
        E.pill(d, "FOTÓN", xm, 340, 44, bg=GLOW)
    elif i == 6:  # no filament: much less heat
        led_bulb(E, d, 300, 640, on=1.0, u=u)
        E.label(d, "LED", 300, 1060, 44, color=GLOW)
        x, y = 780, 600   # generic incandescent bulb, hot
        E.circle(d, x, y, 140, fill=E.mix(E.BG2, E.AMB, 0.35))
        E.line(d, [(x - 50, y + 20), (x - 25, y - 30), (x, y + 20), (x + 25, y - 30), (x + 50, y + 20)], E.AMB, 6)
        E.rrect(d, x - 60, y + 130, x + 60, y + 210, 10, E.SIL_D)
        for k in range(3):
            f = (u * 0.6 + k / 3) % 1
            E.wave(d, x - 60 + 60 * k, y - 160 - 140 * f, x - 60 + 60 * k, y - 230 - 140 * f, 30, 8, E.HOT, 5, head=False)
        E.label(d, "FILAMENTO", 780, 1060, 44, color=E.HOT)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.05, 1.0), ("click", s[1] + 0.4), ("pop", s[2] + 0.6), ("zip", s[3] + 0.5, 1.0),
            ("pop", s[4] + 1.2), ("whoosh", s[5] + 0.4, 0.8), ("click", s[6] + 0.6)]
