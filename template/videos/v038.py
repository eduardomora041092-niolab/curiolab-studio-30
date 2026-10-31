"""Video 038 — ¿Cómo calienta una placa de inducción?
Science: under the glass-ceramic top of an induction hob there is a flat coil of copper wire. An alternating current
flows through the coil, constantly reversing direction, so it produces a magnetic field that also keeps changing.
That changing field passes through the metal base of a suitable (ferromagnetic) pan and, by electromagnetic
induction, induces electric currents (eddy currents) inside the metal. The metal resists those currents and heats up,
so the heat is generated in the pan itself, not in the glass; the glass only warms up later from contact with the
hot pan. (No frequencies, powers or efficiencies are claimed; magnetic hysteresis losses are not discussed.)
"""
import math

ID = "038"
TITLE = "¿Cómo calienta una placa de inducción?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo calienta una placa de inducción?",
    "Bajo el cristal hay una bobina de cobre enrollada.",
    "Por ella pasa corriente alterna, que cambia de sentido sin parar.",
    "Eso crea un campo magnético que también cambia todo el tiempo.",
    "Ese campo atraviesa la base metálica de la sartén.",
    "Allí induce corrientes eléctricas que calientan el propio metal.",
    "Por eso el calor nace en la sartén, no en el cristal.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"calienta", "placa", "inducción", "cristal", "bobina", "cobre", "corriente", "alterna", "sentido",
            "campo", "magnético", "cambia", "base", "metálica", "sartén", "induce", "corrientes", "eléctricas",
            "metal", "calor"}

COPPER = (214, 128, 64)
GLASS = (40, 48, 60)
WATER = (90, 170, 255)

def hob(E, d, y=760, x0=120, x1=960, ring=True):
    E.rrect(d, x0, y, x1, y + 50, 12, GLASS)
    if ring:
        E.rrect(d, 340, y + 14, 740, y + 22, 4, E.SIL_D)

def coil(E, d, cx=540, cy=900, n=6, glow=0.0):
    for k in range(n):
        rx, ry = 60 + k * 36, 16 + k * 9
        d.ellipse(E.P(cx - rx, cy - ry, cx + rx, cy + ry), outline=E.mix(COPPER, E.AMB, glow), width=int(9 * E.S))

def pan(E, d, y=760, heat=0.0, water=True, u=0.0):
    base = E.mix(E.SIL_D, E.HOT, heat)
    E.rrect(d, 300, y - 150, 780, y, 24, E.SIL_D)
    E.rrect(d, 300, y - 34, 780, y, 10, base)
    E.rrect(d, 780, y - 130, 1020, y - 100, 12, E.SIL_D)   # handle
    if water:
        E.rrect(d, 320, y - 120, 760, y - 40, 14, E.mix(E.BG2, WATER, 0.6))
        for k in range(10):
            f = (u * 1.4 + k * 0.17) % 1
            E.circle(d, 350 + (k * 43) % 400, y - 50 - 70 * f, 8 + 6 * f, outline=E.WHITE, w=4)

def field_lines(E, d, u, cx=540, top=600, bottom=900, flip=1.0, alpha=1.0):
    col = E.mix(E.BG2, E.COLD, alpha)
    for k, w in enumerate((90, 170, 250)):
        y0, y1 = bottom - 20, top
        pts = [(cx - w * math.sin(math.pi * t), y0 - (y0 - y1) * t) for t in [j / 20 for j in range(21)]]
        E.line(d, pts, col, 5)
        pts2 = [(cx + w * math.sin(math.pi * t), y0 - (y0 - y1) * t) for t in [j / 20 for j in range(21)]]
        E.line(d, pts2, col, 5)
    if flip >= 0:
        E.arrow(d, cx, bottom - 40, cx, top + 10, col, 7, 26)
    else:
        E.arrow(d, cx, top + 10, cx, bottom - 40, col, 7, 26)

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: pan on the hob, water already boiling
        hob(E, d, y=820)
        pan(E, d, y=820, heat=0.6, u=u)
        for k in range(4):
            f = (u * 0.5 + k / 4) % 1
            E.circle(d, 400 + k * 90, 620 - 300 * f, 26 + 20 * f, fill=E.mix(E.BG2, E.SIL, 0.5 * (1 - f)))
        E.pill(d, "INDUCCIÓN", 540, 1000, 44)
    elif i == 1:  # copper coil under the glass
        hob(E, d, y=560, ring=False)
        coil(E, d, cy=820)
        E.label(d, "CRISTAL", 540, 470, 44, color=E.MUTED)
        E.label(d, "BOBINA DE COBRE", 540, 1060, 46, color=COPPER)
    elif i == 2:  # alternating current, reversing direction
        coil(E, d, cy=720)
        s = 1 if math.sin(u * 4) >= 0 else -1
        y = 1000
        if s > 0:
            E.arrow(d, 300, y, 780, y, E.AMB, 9, 32)
        else:
            E.arrow(d, 780, y, 300, y, E.AMB, 9, 32)
        E.wave(d, 260, 430, 820, 430, 140, 50, E.AMB, 6, phase=u * 6, head=False)
        E.pill(d, "CORRIENTE ALTERNA", 540, 1090, 40)
    elif i == 3:  # changing magnetic field
        coil(E, d, cy=960)
        a = 0.4 + 0.6 * abs(math.sin(u * 4))
        field_lines(E, d, u, top=430, bottom=960, flip=math.sin(u * 4), alpha=a)
        E.label(d, "CAMPO MAGNÉTICO", 540, 340, 46, color=E.COLD)
    elif i == 4:  # field passes through the pan base
        hob(E, d, y=800)
        coil(E, d, cy=960)
        pan(E, d, y=800, water=False)
        field_lines(E, d, u, top=520, bottom=960, flip=math.sin(u * 4), alpha=0.5 + 0.5 * abs(math.sin(u * 4)))
        E.label(d, "BASE METÁLICA", 540, 480, 44, color=E.SIL_H)
    elif i == 5:  # induced eddy currents heat the metal
        k = E.ease(u / L)
        E.rrect(d, 160, 560, 920, 760, 24, E.mix(E.SIL_D, E.HOT, 0.8 * k))
        for j, cx in enumerate((330, 540, 750)):
            ang = u * 4 + j
            d.ellipse(E.P(cx - 80, 610, cx + 80, 710), outline=E.AMB, width=int(12 * E.S))
            E.circle(d, cx + 80 * math.cos(ang), 660 + 50 * math.sin(ang), 12, fill=E.AMB)
        E.label(d, "CORRIENTES INDUCIDAS", 540, 480, 44, color=E.AMB)
        E.label(d, "EL METAL SE CALIENTA", 540, 860, 44, color=E.HOT)
    elif i == 6:  # heat born in the pan, not the glass
        hob(E, d, y=820)
        pan(E, d, y=820, heat=0.9, water=False)
        for k in range(3):
            f = (u * 0.6 + k / 3) % 1
            E.wave(d, 420 + 120 * k, 620 - 180 * f, 420 + 120 * k, 560 - 180 * f, 30, 8, E.HOT, 5, head=False)
        E.label(d, "SARTÉN CALIENTE", 540, 400, 46, color=E.HOT)
        E.label(d, "CRISTAL", 540, 960, 42, color=E.MUTED)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.05, 1.0), ("click", s[1] + 0.4), ("zip", s[2] + 0.6, 1.0), ("whoosh", s[3] + 0.5, 0.8),
            ("pop", s[4] + 0.8), ("zip", s[5] + 0.5, 1.0), ("click", s[6] + 0.6)]
