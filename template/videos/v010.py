"""Video 010 — ¿Cómo enfría un refrigerador?
Mechanism (vapour-compression cycle): a fridge does not make "cold"; it pumps heat from the inside to the
outside. A refrigerant circulates in a closed loop. In the evaporator (inside the cabinet) the refrigerant,
at low pressure, boils and absorbs heat from the food and air. The compressor squeezes that gas, raising its
pressure and temperature. In the condenser (at the back/outside) the hot gas gives its heat to the kitchen
air and condenses back into a liquid. An expansion valve (or capillary tube) drops the pressure so the
refrigerant leaves very cold and returns to the evaporator. Because the compressor's work is added, the
fridge releases more heat than it removes: it warms the kitchen slightly while cooling its inside.
(No refrigerant names, temperatures or pressures are given.)
"""
import math

ID = "010"
TITLE = "¿Cómo enfría un refrigerador?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "Tu nevera no crea frío: saca el calor de dentro.",
    "Por un circuito cerrado circula un líquido refrigerante.",
    "Dentro, en el evaporador, el refrigerante hierve y absorbe calor.",
    "El compresor aprieta ese gas, que sube de presión y se calienta.",
    "Atrás, en el condensador, suelta ese calor y vuelve a ser líquido.",
    "Una válvula estrecha le baja la presión, y sale muy frío.",
    "Por eso, la nevera calienta un poco la cocina mientras enfría por dentro.",
    "Sígueme para ver cómo funcionan las cosas por dentro.",
]
KEYWORDS = {"nevera", "frío", "calor", "circuito", "cerrado", "refrigerante", "evaporador", "hierve", "absorbe",
            "compresor", "gas", "presión", "calienta", "condensador", "líquido", "válvula", "estrecha", "cocina", "dentro"}

CABINET, INTERIOR, DOOR = (30, 44, 72), (38, 66, 108), (24, 34, 56)
LX = 320   # label column (over the lower door)
WARM = (240, 150, 60)
SUCT = (130, 190, 240)

def _rows():
    pts = []
    for k in range(10):
        y = 940 - 60 * k
        a, b = (920, 640) if k % 2 == 0 else (640, 920)
        pts += [(a, y), (b, y)]
    return pts

# loop groups in flow order: (name, points, colour)
VALVE_OUT = [(140, 372), (140, 420), (170, 420)]
EVAP = [(170, 420), (490, 420), (490, 470), (170, 470), (170, 520), (490, 520)]
SUCTION = [(490, 520), (600, 520), (600, 1030), (660, 1030)]
COMP = [(660, 1030), (840, 990)]
DISCH = [(840, 990), (920, 990), (920, 940)]
COND = _rows()
LIQ = [(920, 400), (920, 300), (140, 300), (140, 348)]
GROUPS = [("valve", VALVE_OUT, None), ("evap", EVAP, None), ("suct", SUCTION, None), ("comp", COMP, None),
          ("disch", DISCH, None), ("cond", COND, None), ("liq", LIQ, None)]

def gcol(E, name, f=0.0):
    return {"valve": E.COLD, "evap": E.mix(E.COLD, SUCT, f), "suct": SUCT, "comp": E.mix(SUCT, E.HOT, f),
            "disch": E.HOT, "cond": E.mix(E.HOT, WARM, f), "liq": WARM}[name]

def _flat():
    seq = []
    for name, pts, _ in GROUPS:
        n = len(pts) - 1
        for j in range(n):
            seq.append((name, pts[j], pts[j + 1], j / max(1, n)))
    return seq
SEQ = _flat()
SEG_L = [math.hypot(b[0] - a[0], b[1] - a[1]) for _, a, b, _ in SEQ]
TOTAL = sum(SEG_L)

def at(s):
    s %= TOTAL
    for (name, a, b, f), l in zip(SEQ, SEG_L):
        if s <= l:
            q = s / l
            return (a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q), name, f
        s -= l
    return SEQ[-1][2], SEQ[-1][0], 1.0

def cabinet(E, d):
    E.rrect(d, 80, 330, 560, 1150, 30, CABINET, outline=E.SIL, w=4)
    E.rrect(d, 110, 370, 530, 820, 18, INTERIOR)
    E.rrect(d, 110, 850, 530, 1120, 18, DOOR)

def pipes(E, d, hl=None, upto=1.0):
    drawn = 0.0; limit = TOTAL * upto
    for (name, a, b, f), l in zip(SEQ, SEG_L):
        if name == "comp" or drawn >= limit:
            drawn += l; continue
        q = min(1.0, (limit - drawn) / l)
        w = 14 if hl == name or (hl == "cond" and name == "cond") else 9
        c = gcol(E, name, f) if (hl is None or hl == name) else E.mix(gcol(E, name, f), E.BG2, 0.55)
        E.line(d, [a, (a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q)], c, w)
        drawn += l

def compressor(E, d, hl=False, u=0.0):
    E.rrect(d, 660, 960, 840, 1100, 44, (70, 78, 94) if not hl else (96, 104, 122), outline=E.SIL_H if hl else E.SIL_D, w=4)
    if hl:   # piston pumping inside
        y = 1030 + 22 * math.sin(u * 12)
        E.rrect(d, 715, 990, 785, 1080, 8, E.CAV, outline=E.SIL, w=3)
        E.rrect(d, 720, y - 12, 780, y + 12, 4, E.SIL)

def valve(E, d, hl=False):
    c = E.AMB if hl else E.SIL
    E.poly(d, [(118, 342), (162, 342), (146, 360), (162, 378), (118, 378), (134, 360)], fill=c)

def dots(E, d, u, n=22, speed=160):
    for k in range(n):
        (x, y), name, f = at(k * TOTAL / n + u * speed)
        E.circle(d, x, y, 9, fill=E.mix(gcol(E, name, f), E.WHITE, 0.35))

def full(E, d, u, hl=None):
    cabinet(E, d); pipes(E, d, hl); compressor(E, d, hl == "comp", u); valve(E, d, hl == "valve"); dots(E, d, u)

def scene(i, u, L, E, im, d):
    if i == 0:  # no cold is made: heat is taken out
        cabinet(E, d)
        E.label(d, "FRÍO", 230, 650, 64, color=E.COLD)
        for k in range(3):
            y = 470 + k * 120; p = E.ease((u - 0.2 * k) / 0.9)
            if p > 0:
                E.wave(d, 400, y, E.lerp(400, 1040, p), y, 70, 14, E.HOT, w=7, phase=u * 8)
        if u > 1.0: E.label(d, "CALOR", 820, 820, 54, color=E.HOT)
        if u > 0.5: E.pill(d, "SACA EL CALOR", LX, 985, 36)
    elif i == 1:  # closed loop with refrigerant
        cabinet(E, d); p = E.ease(u / (L * 0.6))
        pipes(E, d, upto=p); compressor(E, d); valve(E, d)
        if p >= 1: dots(E, d, u)
        if u > 0.6: E.label(d, "CIRCUITO", LX, 950, 44, color=E.WHITE)
        if u > 0.6: E.label(d, "CERRADO", LX, 1010, 44, color=E.WHITE)
        if u > 1.3: E.label(d, "REFRIGERANTE", LX, 1080, 38)
    elif i == 2:  # evaporator: boils, absorbs heat
        full(E, d, u, "evap")
        E.rrect(d, 260, 690, 380, 800, 12, (200, 120, 80))   # a warm food container
        for k, x in enumerate((240, 320, 400)):
            p = E.ease((u - 0.25 * k) / 0.8)
            if p > 0: E.wave(d, x, 680, x, E.lerp(680, 545, p), 40, 10, E.HOT, w=6, phase=u * 9)
        for k in range(8):   # bubbles of boiling refrigerant along the coil
            s = (u * 0.6 + k / 8) % 1.0
            row = (420, 470, 520)[k % 3]
            E.circle(d, 170 + 320 * s, row - 12, 7, outline=E.WHITE, w=3)
        if u > 0.4: E.label(d, "EVAPORADOR", LX, 960, 42)
        if u > 1.0: E.label(d, "ABSORBE CALOR", LX, 1050, 36, color=E.HOT)
    elif i == 3:  # compressor: pressure and temperature up
        full(E, d, u, "comp")
        E.line(d, [(840, 990), (920, 990), (920, 940)], E.HOT, 14)
        E.arrow(d, 470, 990, 645, 1025, color=E.AMB, w=6)
        if u > 0.3: E.label(d, "COMPRESOR", LX, 960, 42)
        if u > 1.0: E.label(d, "+ PRESIÓN", LX, 1030, 38, color=E.WHITE)
        if u > 1.4: E.label(d, "+ CALOR", LX, 1090, 38, color=E.HOT)
    elif i == 4:  # condenser: releases heat, becomes liquid
        full(E, d, u, "cond")
        for k, y in enumerate((460, 640, 820)):
            p = E.ease((u - 0.2 * k) / 0.8)
            if p > 0: E.wave(d, 935, y, E.lerp(935, 1060, p), y - 40 * p, 40, 9, E.HOT, w=6, phase=u * 9)
        E.arrow(d, 470, 990, 625, 900, color=E.AMB, w=6)
        if u > 0.3: E.label(d, "CONDENSADOR", LX, 960, 40)
        if u > 1.1: E.label(d, "SE HACE LÍQUIDO", LX, 1050, 34, color=E.WHITE)
    elif i == 5:  # expansion valve: pressure drops, very cold
        full(E, d, u, "valve")
        E.line(d, VALVE_OUT + EVAP[1:2], E.COLD, 14)
        for k in range(6):   # frost sparkle after the valve
            x, y = 150 + k * 55, 405 + 6 * math.sin(u * 6 + k)
            E.circle(d, x, y - 20, 5, fill=E.WHITE)
        if u > 0.3: E.label(d, "VÁLVULA", 320, 343, 34)
        if u > 1.0: E.label(d, "MUY FRÍO", LX, 990, 48, color=E.COLD)
    elif i == 6:  # cools inside, warms the kitchen
        full(E, d, u)
        E.label(d, "FRÍO", 320, 680, 60, color=E.COLD)
        for k, y in enumerate((450, 620, 790, 940)):
            p = E.ease((u - 0.15 * k) / 0.7)
            if p > 0: E.wave(d, 935, y, E.lerp(935, 1065, p), y - 50 * p, 40, 9, E.HOT, w=7, phase=u * 9)
        if u > 0.8: E.label(d, "COCINA", LX, 970, 44, color=E.HOT)
        if u > 0.8: E.label(d, "+ CALIENTE", LX, 1040, 40, color=E.HOT)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.3, 0.8), ("click", s[1] + 0.2), ("pop", s[2] + 0.6), ("click", s[3] + 0.2),
            ("click", s[3] + 0.5), ("whoosh", s[4] + 0.3, 0.7), ("pop", s[5] + 0.4), ("whoosh", s[6] + 0.2, 0.8)]
