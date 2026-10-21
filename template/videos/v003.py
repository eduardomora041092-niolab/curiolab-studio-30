"""Video 003 — ¿Por qué el cielo es azul?
Physics (Rayleigh scattering): white sunlight contains all colours. Air molecules (N2, O2) are far
smaller than the wavelength of light and scatter short wavelengths (blue) much more strongly than
long ones (red) — intensity ∝ 1/λ⁴. Scattered blue light reaches us from every direction, so the sky
looks blue. At sunset light crosses much more air; most blue is scattered out of the beam before it
reaches us, leaving oranges and reds.
"""
import math

ID = "003"
TITLE = "¿Por qué el cielo es azul?"
SUBTITLE = "CURIOSIDADES DE LA CIENCIA"
VOICE = "em_alex"; SPEED = 1.08
LINES = [
    "¿Por qué el cielo es azul, si la luz del Sol es blanca?",
    "La luz blanca es una mezcla de todos los colores.",
    "Al entrar en la atmósfera, choca con moléculas diminutas de nitrógeno y oxígeno.",
    "Esas moléculas desvían mucho más la luz azul, de onda corta, que la roja.",
    "La luz azul se dispersa en todas direcciones y llena el cielo: por eso lo vemos azul.",
    "Al atardecer, la luz recorre mucho más aire, y casi todo el azul se pierde por el camino.",
    "Solo nos llegan los naranjas y los rojos.",
    "Sígueme para más curiosidades de la ciencia.",
]
KEYWORDS = {"cielo", "azul", "blanca", "colores", "atmósfera", "moléculas", "nitrógeno", "oxígeno", "corta", "roja", "dispersa", "atardecer", "aire", "naranjas", "rojos", "ciencia"}

SPEC = [(230, 60, 50), (250, 140, 40), (250, 220, 60), (80, 200, 100), (60, 130, 240), (140, 90, 220)]
RED, BLU = SPEC[0], SPEC[4]
SKY_DAY = (70, 140, 230)
SUN = (255, 236, 160)

def sky(E, d, top_col, bot_col, x0=60, y0=290, x1=1020, y1=1180):
    for y in range(y0, y1, 6):
        E.rrect(d, x0, y, x1, min(y + 7, y1), 0, E.mix(top_col, bot_col, (y - y0) / (y1 - y0)))

def person(E, d, x, y, s=1.0, col=(20, 28, 46)):
    E.circle(d, x, y - 70 * s, 18 * s, fill=col)
    E.line(d, [(x, y - 52 * s), (x, y - 10 * s)], col, 10 * s)
    E.line(d, [(x, y - 10 * s), (x - 16 * s, y + 25 * s)], col, 9 * s)
    E.line(d, [(x, y - 10 * s), (x + 16 * s, y + 25 * s)], col, 9 * s)
    E.line(d, [(x - 24 * s, y - 40 * s), (x + 24 * s, y - 40 * s)], col, 8 * s)

def molecule(E, d, x, y, r=26, col=(200, 215, 240), label=None):
    E.circle(d, x - r * 0.55, y, r, fill=col, outline=E.BG1, w=3)
    E.circle(d, x + r * 0.55, y, r, fill=col, outline=E.BG1, w=3)
    if label: E.label(d, label, x, y + r + 38, 38, color=E.WHITE)

def scene(i, u, L, E, im, d):
    cx = 540
    if i == 0:  # hook: white sun, blue sky
        sky(E, d, (40, 105, 210), (130, 190, 250))
        E.circle(d, 820, 470, 95, fill=SUN, outline=(255, 250, 220), w=6)
        for k in range(12):
            a = k * math.pi / 6 + u * 0.4
            E.line(d, [(820 + 120 * math.cos(a), 470 + 120 * math.sin(a)), (820 + 160 * math.cos(a), 470 + 160 * math.sin(a))], (255, 250, 220), 8)
        p = E.ease(u / 1.0)
        E.line(d, [(740, 540), (740 - 520 * p, 540 + 520 * p)], (255, 255, 255), 22)
        if u > 0.9:
            E.pill(d, "LUZ BLANCA", 300, 560, 38, fg=E.BG1, bg=(255, 255, 255))
            E.pill(d, "CIELO AZUL", 300, 1000, 38, fg=E.WHITE, bg=(40, 105, 210))
    elif i == 1:  # white light = all colours (prism)
        p = E.ease(u / 0.8)
        E.line(d, [(60, 760), (60 + 400 * p, 760)], (255, 255, 255), 24)
        tri = [(540, 560), (700, 900), (380, 900)]
        E.poly(d, tri, fill=(120, 150, 200), outline=E.WHITE, w=4)
        if u > 0.6:
            q = E.ease((u - 0.6) / 0.8)
            for k, c in enumerate(SPEC):
                y_end = 600 + k * 90
                E.line(d, [(610, 760 + k * 6), (610 + 400 * q, 760 + (y_end - 760) * q)], c, 18)
        if u > 1.4:
            E.label(d, "TODOS LOS", cx, 420, 50); E.label(d, "COLORES", cx, 475, 50)
    elif i == 2:  # atmosphere + molecules (zoom inset)
        E.circle(d, cx, 2550, 1500, fill=(40, 70, 130))                       # atmosphere band
        E.circle(d, cx, 2550, 1400, fill=(45, 120, 70))                       # Earth
        E.label(d, "ATMÓSFERA", cx, 1110, 40, color=E.WHITE)
        k = E.back_out(u / 0.6)
        if k > 0.05:
            r = 330 * k
            E.circle(d, cx, 650, r, fill=(24, 36, 64), outline=E.AMB, w=6)
            if u > 0.6:
                mols = [(430, 520, "NITRÓGENO"), (650, 690, "OXÍGENO"), (430, 820, None), (690, 470, None), (600, 870, None)]
                for j, (mx, my, lab) in enumerate(mols):
                    molecule(E, d, mx + 6 * math.sin(u * 7 + j), my + 6 * math.cos(u * 6 + j * 2), 34 if lab else 26,
                             (200, 215, 240) if j % 2 == 0 else (255, 200, 200), lab)
            E.line(d, [(cx, 980), (cx, 1050)], E.AMB, 5)
    elif i == 3:  # blue (short wave) scattered much more than red (long wave)
        molecule(E, d, cx, 760, 34)
        p = E.ease(u / 1.0)
        E.wave(d, 60, 560, 60 + (cx - 100) * p, 560 + 140 * p, 120, 22, RED, w=8, phase=u * 6, head=p < 1)
        E.wave(d, 60, 960, 60 + (cx - 100) * p, 960 - 140 * p, 40, 18, BLU, w=8, phase=u * 12, head=p < 1)
        if u > 0.3:
            E.label(d, "ONDA LARGA", 230, 470, 40, color=RED)
            E.label(d, "ONDA CORTA", 230, 1060, 40, color=BLU)
        if u > 1.0:
            q = E.ease((u - 1.0) / 0.9)
            E.wave(d, cx + 60, 760, cx + 60 + 380 * q, 760 + 140 * q, 120, 22, RED, w=8, phase=u * 6)   # red: keeps going straight
            for k in range(7):  # blue: sprayed in every direction
                a = -math.pi * 0.9 + k * (math.pi * 1.8 / 6)
                r = 70 + 250 * q
                E.wave(d, cx + 60 * math.cos(a), 760 + 60 * math.sin(a), cx + r * math.cos(a), 760 + r * math.sin(a), 40, 10, BLU, w=6, phase=u * 12)
    elif i == 4:  # observer sees scattered blue from every direction
        t = E.ease(u / (L * 0.7))
        sky(E, d, E.mix(E.BG1, (40, 105, 210), t), E.mix(E.BG2, (130, 190, 250), t))
        E.rrect(d, 60, 1090, 1020, 1180, 0, (45, 120, 70))
        person(E, d, cx, 1080, 1.2)
        rng = [(170, 380), (900, 420), (300, 700), (820, 760), (540, 360), (120, 900), (960, 950)]
        for j, (x0, y0) in enumerate(rng):
            ph = (u * 0.7 + j * 0.17) % 1
            ex, ey = cx, 990
            x1, y1 = x0 + (ex - x0) * ph, y0 + (ey - y0) * ph
            E.wave(d, x0, y0, x1, y1, 40, 9, (190, 220, 255), w=6, phase=u * 12)
    elif i == 5:  # sunset geometry: much longer path through air
        E.circle(d, cx, 2400, 1550, fill=(40, 70, 130))
        E.circle(d, cx, 2400, 1350, fill=(45, 120, 70))
        person(E, d, cx, 1048, 0.9)
        # noon: short path
        E.circle(d, cx, 360, 50, fill=SUN)
        E.line(d, [(cx, 850), (cx, 990)], (255, 255, 255), 10)
        E.label(d, "MEDIODÍA", cx + 170, 360, 38, color=E.WHITE)
        # sunset: long path along the horizon
        p = E.ease(u / 1.2)
        E.circle(d, 70, 1010, 50, fill=(255, 150, 60))
        E.line(d, [(120, 1010), (120 + (cx - 150) * p, 1010 + 20 * p)], (255, 255, 255), 10)
        for k in range(5):  # blue peeling off along the long path
            bx = 160 + k * 70
            if p * (cx - 150) + 120 > bx:
                q = min(1.0, (p * (cx - 150) + 120 - bx) / 120)
                E.wave(d, bx, 1005, bx - 10, 1005 - 160 * q, 30, 8, BLU, w=5, phase=u * 12)
        if u > 1.0:
            E.label(d, "MUCHO MÁS AIRE", cx, 760, 50)
    elif i == 6:  # sunset sky: only orange & red arrive
        sky(E, d, (60, 40, 110), (250, 120, 50))
        E.circle(d, cx, 1090, 120, fill=(255, 170, 70))
        E.rrect(d, 60, 1090, 1020, 1180, 0, (30, 40, 60))
        person(E, d, 820, 1085, 1.0, col=(10, 14, 24))
        for k, c in enumerate((SPEC[1], SPEC[0], SPEC[1])):
            ph = (u * 0.8 + k * 0.3) % 1
            E.wave(d, 640, 1060 - k * 40, 640 + 150 * ph, 1060 - k * 40 + 10 * ph, 60, 10, c, w=6, phase=u * 8)
        if u > 0.4: E.pill(d, "NARANJAS Y ROJOS", cx, 420, 42, bg=(250, 140, 40))
    else:
        E.outro(d, u)
    clip_visual(E, im)

def clip_visual(E, im, y=1190):
    """Keep scene art inside the visual area so captions sit on the brand background."""
    im.paste(E.BG.crop((0, y * E.S, E.W * E.S, E.H * E.S)), (0, y * E.S))

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", 0.1, 0.6), ("whoosh", s[1] + 0.6, 0.5), ("pop", s[2] + 0.1), ("pop", s[3] + 1.0), ("whoosh", s[5], 0.6), ("whoosh", s[7], 0.4)]
