"""Video 061 — ¿Cómo convierte un panel solar la luz en electricidad?
Science: a solar panel is made of cells, usually of silicon. Each cell has two layers of silicon treated (doped) in
different ways: an n-type layer with spare electrons and a p-type layer with a shortage of electrons. Where they meet
(the p-n junction) an electric field forms. When light is absorbed in the silicon, its energy frees electrons from
their atoms. The field at the junction pushes the freed electrons towards the n layer, so they cannot simply recombine.
If the two sides are joined by a wire, the electrons flow out through the external circuit and back into the cell:
that flow is an electric current, which can light a bulb (photovoltaic effect).
(No efficiencies, voltages or power figures are claimed.)
"""
import math

ID = "061"
TITLE = "¿Cómo convierte un panel solar la luz en electricidad?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo convierte un panel solar la luz en electricidad?",
    "Cada célula tiene dos capas de silicio tratadas de forma distinta.",
    "Donde se tocan, aparece un campo eléctrico.",
    "La luz golpea el silicio y suelta electrones de sus átomos.",
    "El campo eléctrico empuja esos electrones hacia una sola capa.",
    "Con un cable, los electrones recorren el circuito y vuelven.",
    "Ese flujo es la corriente eléctrica que enciende la bombilla.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"panel", "solar", "luz", "electricidad", "célula", "capas", "silicio", "distinta", "tocan",
            "campo", "eléctrico", "golpea", "electrones", "átomos", "empuja", "capa", "cable", "circuito",
            "vuelven", "flujo", "corriente", "eléctrica", "bombilla"}

NCOL = (70, 120, 200)      # n-type layer
PCOL = (180, 80, 90)       # p-type layer
SUNY = (255, 210, 70)
ELE = (255, 176, 32)

X0, X1 = 170, 910          # cell cross-section
NY0, JY, PY1 = 470, 700, 930


def sun(E, d, x, y, u, r=70):
    for k in range(12):
        a = k * math.pi / 6 + u * 0.6
        E.line(d, [(x + (r + 15) * math.cos(a), y + (r + 15) * math.sin(a)),
                   (x + (r + 45) * math.cos(a), y + (r + 45) * math.sin(a))], SUNY, 8)
    E.circle(d, x, y, r, fill=SUNY)


def bulb(E, d, x, y, on=0.0):
    if on > 0:
        for k in range(3):
            E.circle(d, x, y, 70 + 25 * k + 10 * on, outline=E.mix((60, 60, 40), SUNY, on * (1 - k / 3)), w=4)
    E.circle(d, x, y, 60, fill=E.mix((90, 95, 110), (255, 235, 150), on), outline=E.SIL, w=4)
    E.rrect(d, x - 30, y + 55, x + 30, y + 100, 8, E.SIL_D)


def cell(E, d, junction=False, signs=False):
    E.rrect(d, X0, NY0, X1, JY, 10, NCOL, outline=E.SIL, w=4)
    E.rrect(d, X0, JY, X1, PY1, 10, PCOL, outline=E.SIL, w=4)
    E.label(d, "CAPA N", X0 + 130, NY0 + 50, 40, color=E.WHITE)
    E.label(d, "CAPA P", X0 + 130, PY1 - 50, 40, color=E.WHITE)
    if junction:
        E.rrect(d, X0, JY - 40, X1, JY + 40, 6, (235, 200, 110))
    if signs:
        for k in range(7):
            x = X0 + 70 + k * 100
            E.label(d, "+", x, JY - 18, 50, color=E.HOT)
            E.label(d, "-", x, JY + 18, 56, color=E.COLD)


def contacts(E, d):
    E.rrect(d, X0 + 40, NY0 - 26, X1 - 40, NY0, 6, E.SIL_D)
    E.rrect(d, X0, PY1, X1, PY1 + 26, 6, E.SIL_D)


def loop_path():
    # out of the top contact, round the right side through the bulb, back into the bottom contact
    return [(540, NY0 - 26), (540, 360), (1000, 360), (1000, 1000), (540, 1000), (540, PY1 + 26)]


def along(path, s):
    segs = [(path[k], path[k + 1]) for k in range(len(path) - 1)]
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]
    tot = sum(lens); s = (s % 1.0) * tot
    for (a, b), L in zip(segs, lens):
        if s <= L:
            f = s / L; return a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
        s -= L
    return path[-1]


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: sunlight on a panel, current lighting a bulb
        sun(E, d, 190, 400, u)
        for k in range(3):
            E.wave(d, 260 + k * 40, 470 + k * 30, 470 + k * 110, 700 + k * 40, 50, 12, SUNY, 5, phase=u * 8)
        E.poly(d, [(380, 760), (900, 700), (960, 960), (420, 1030)], fill=(30, 60, 120), outline=E.SIL, w=5)
        for k in range(1, 4):
            E.line(d, [(380 + 13 * k * 3.3, 760 + 67 * k), (900 + 15 * k, 700 + 65 * k)], (80, 120, 190), 3)
            E.line(d, [(380 + 130 * k, 760 - 15 * k), (420 + 135 * k, 1030 - 18 * k)], (80, 120, 190), 3)
        path = [(930, 830), (1000, 830), (1000, 520), (820, 520)]
        E.line(d, path, E.SIL, 6)
        for k in range(6):
            x, y = along(path, u * 0.5 + k / 6)
            E.circle(d, x, y, 10, fill=ELE)
        bulb(E, d, 760, 470, on=0.6 + 0.4 * abs(math.sin(u * 3)))
    elif i == 1:  # two differently treated silicon layers
        cell(E, d)
        E.label(d, "SILICIO", 540, 400, 52, color=E.AMB)
        E.label(d, "DOS CAPAS DISTINTAS", 540, 1050, 44, color=E.WHITE)
    elif i == 2:  # electric field where they meet
        cell(E, d, junction=True, signs=E.ease(u / 0.6) > 0.5)
        E.label(d, "CAMPO ELÉCTRICO", 540, 400, 50, color=E.AMB)
        E.arrow(d, 960, 1050, 930, JY + 50, E.AMB, 6, 24)
        E.label(d, "UNIÓN", 860, 1080, 40, color=E.AMB)
    elif i == 3:  # light frees electrons from atoms
        cell(E, d, junction=True)
        k = E.ease(min(1.0, u / (L * 0.5)))
        for n, (ax, ay) in enumerate(((360, 760), (560, 820), (760, 760))):
            E.circle(d, ax, ay, 34, fill=E.SIL, outline=E.SIL_H, w=3)
            E.wave(d, ax - 140, 300, ax - 140 + 120 * k, 300 + (ay - 340) * k, 50, 12, SUNY, 5, head=k > 0.2)
            if k > 0.85:
                q = E.ease((u - L * 0.5) / (L * 0.4))
                E.circle(d, ax + 40 + 40 * q, ay - 40 - 20 * q, 14, fill=ELE)
        E.label(d, "LUZ", 260, 300, 46, color=SUNY)
        E.label(d, "ELECTRÓN LIBRE", 640, 1050, 44, color=ELE)
    elif i == 4:  # field pushes electrons towards one layer (n)
        cell(E, d, junction=True)
        for k in range(8):
            x = X0 + 80 + k * 85
            q = (u * 0.7 + k / 8) % 1.0
            y = 820 - q * 280
            E.circle(d, x, y, 13, fill=ELE)
        for x in (300, 540, 780):
            E.arrow(d, x, 880, x, 560, E.WHITE, 7, 26)
        E.label(d, "HACIA LA CAPA N", 540, 400, 48, color=E.AMB)
    elif i == 5:  # external circuit: electrons leave and come back
        cell(E, d)
        contacts(E, d)
        path = loop_path()
        E.line(d, path, E.SIL, 7)
        bulb(E, d, 1000, 680, on=0.0)
        for k in range(10):
            x, y = along(path, u * 0.35 + k / 10)
            E.circle(d, x, y, 12, fill=ELE)
        E.label(d, "CIRCUITO", 300, 360, 46, color=E.AMB)
    elif i == 6:  # the flow is the current that lights the bulb
        cell(E, d)
        contacts(E, d)
        path = loop_path()
        E.line(d, path, E.SIL, 7)
        on = E.ease(u / 0.8)
        for k in range(10):
            x, y = along(path, u * 0.35 + k / 10)
            E.circle(d, x, y, 12, fill=ELE)
        bulb(E, d, 1000, 680, on=on)
        E.label(d, "CORRIENTE", 300, 360, 46, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 0.8), ("pop", s[1] + 0.6), ("zip", s[2] + 0.4), ("pop", s[3] + 0.9),
            ("whoosh", s[4] + 0.5, 0.8), ("zip", s[5] + 0.4), ("click", s[6] + 0.6)]
