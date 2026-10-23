"""Video 015 — ¿Por qué el hielo flota?
Science: for most substances the solid is denser than the liquid and sinks in it; water is an exception.
Water molecules attract each other through hydrogen bonds. In the liquid they move, the bonds constantly break and
re-form, and the molecules can pack relatively closely. On freezing, each molecule bonds to four neighbours in a
fixed open hexagonal lattice that leaves empty spaces, so the same mass occupies more volume: ice is less dense
than liquid water and floats. Consequently lakes freeze from the top down; the ice layer insulates the water below,
where life continues.
(No exact density figures or percentage of submerged ice are claimed.)
"""
import math

ID = "015"
TITLE = "¿Por qué el hielo flota?"
SUBTITLE = "CURIOSIDADES DE LA CIENCIA"
LINES = [
    "El hielo flota, aunque casi todo sólido se hunde.",
    "Las moléculas de agua se atraen mucho entre sí.",
    "En el líquido se mueven sin parar y se apretujan.",
    "Al congelarse, se enganchan en una red fija de hexágonos con huecos.",
    "Los huecos hacen que ocupe más espacio con la misma masa.",
    "Así es menos denso que el agua líquida, y por eso flota.",
    "Por eso los lagos se hielan por arriba, y debajo sigue la vida.",
    "Sígueme para más curiosidades de la ciencia.",
]
KEYWORDS = {"hielo", "flota", "sólido", "hunde", "moléculas", "agua", "atraen", "líquido", "mueven", "apretujan",
            "congelarse", "red", "hexágonos", "huecos", "espacio", "masa", "denso", "lagos", "arriba", "vida", "ciencia"}

WATER, WATER_D = (40, 110, 190), (28, 80, 150)
ICE, ICE_E = (200, 232, 250), (150, 200, 235)
OXY = (232, 80, 70)
HYD = (240, 244, 248)
WAX, WAX_D = (240, 200, 120), (190, 150, 80)

def glass(E, d, x0, x1, y0, y1, level, col=WATER):
    E.rrect(d, x0, level, x1, y1, 10, col)
    E.line(d, [(x0, y0), (x0, y1), (x1, y1), (x1, y0)], E.SIL_H, 8)

def molecule(E, d, x, y, a=0.0, s=1.0):
    for da in (-0.9, 0.9):
        hx, hy = x + 30 * s * math.cos(a + da), y + 30 * s * math.sin(a + da)
        E.line(d, [(x, y), (hx, hy)], HYD, 5 * s)
        E.circle(d, hx, hy, 12 * s, fill=HYD)
    E.circle(d, x, y, 22 * s, fill=OXY)

def hex_points(cx, cy, r):
    return [(cx + r * math.cos(math.pi / 6 + k * math.pi / 3), cy + r * math.sin(math.pi / 6 + k * math.pi / 3)) for k in range(6)]

def ice_lattice(E, d, cx, cy, r=95, links=1.0, hole=False):
    centres = [(cx, cy), (cx + r * 1.732, cy), (cx - r * 1.732, cy), (cx + r * 0.866, cy - r * 1.5),
               (cx - r * 0.866, cy - r * 1.5), (cx + r * 0.866, cy + r * 1.5), (cx - r * 0.866, cy + r * 1.5)]
    seen = set()
    for (hx, hy) in centres:
        pts = hex_points(hx, hy, r)
        if hole:
            E.poly(d, pts, fill=(18, 30, 52))
        for k in range(6):
            a, b = pts[k], pts[(k + 1) % 6]
            if links > 0:
                E.line(d, [a, (E.lerp(a[0], b[0], links), E.lerp(a[1], b[1], links))], E.mix(E.BG2, E.COLD, 0.9), 4)
    for (hx, hy) in centres:
        for (px, py) in hex_points(hx, hy, r):
            key = (round(px), round(py))
            if key in seen: continue
            seen.add(key)
            molecule(E, d, px, py, a=math.atan2(py - cy, px - cx) + math.pi / 2, s=0.75)

def scene(i, u, L, E, im, d):
    if i == 0:  # ice floats, a typical solid sinks
        glass(E, d, 140, 500, 520, 1060, 620)
        glass(E, d, 580, 940, 520, 1060, 620, col=(200, 150, 70))
        k = E.ease(u / (L * 0.7))
        bob = 6 * math.sin(u * 4)
        E.rrect(d, 250, 570 + bob, 390, 690 + bob, 14, ICE, outline=ICE_E, w=4)
        y = E.lerp(560, 920, k)
        E.rrect(d, 690, y, 830, y + 120, 14, WAX, outline=WAX_D, w=4)
        E.label(d, "HIELO EN AGUA", 320, 460, 40, color=E.COLD)
        E.label(d, "CERA EN CERA", 760, 460, 40, color=WAX)
        if u > 0.8:
            E.label(d, "FLOTA", 320, 1120, 44, color=E.WHITE)
            E.label(d, "SE HUNDE", 760, 1120, 44, color=E.WHITE)
    elif i == 1:  # water molecules attract each other
        molecule(E, d, 380, 680, a=-math.pi / 2, s=2.2)
        molecule(E, d, 700, 760, a=math.pi / 2 + 0.4, s=2.2)
        p = 0.5 + 0.5 * math.sin(u * 3)
        for k in range(5):
            x = E.lerp(420, 650, k / 4)
            y = E.lerp(700, 740, k / 4)
            E.circle(d, x, y, 7, fill=E.mix(E.AMB, E.BG2, p * 0.6))
        E.label(d, "MOLÉCULAS DE AGUA", 540, 420, 46, color=E.WHITE)
        E.label(d, "SE ATRAEN", 540, 980, 50, color=E.AMB)
    elif i == 2:  # liquid: moving and packed
        E.rrect(d, 160, 380, 920, 1100, 30, (24, 52, 92), outline=WATER, w=6)
        rnd = [(0.12, 0.2), (0.35, 0.15), (0.6, 0.22), (0.85, 0.18), (0.2, 0.42), (0.45, 0.4), (0.7, 0.45),
               (0.9, 0.5), (0.1, 0.65), (0.33, 0.62), (0.58, 0.68), (0.8, 0.72), (0.22, 0.88), (0.48, 0.86), (0.75, 0.9)]
        for k, (fx, fy) in enumerate(rnd):
            x = 220 + fx * 640 + 18 * math.sin(u * 3 + k)
            y = 440 + fy * 600 + 18 * math.cos(u * 2.5 + k * 1.7)
            molecule(E, d, x, y, a=u * 2 + k, s=1.0)
        E.label(d, "LÍQUIDO", 540, 330, 48, color=E.COLD)
    elif i == 3:  # freezing: hexagonal network with holes
        links = E.ease(u / (L * 0.7))
        ice_lattice(E, d, 540, 730, links=links, hole=False)
        E.label(d, "HIELO", 540, 330, 48, color=E.COLD)
        if u > L * 0.5:
            E.label(d, "HUECO", 540, 730, 36, color=E.AMB)
    elif i == 4:  # same mass, more space
        # left: liquid packed; right: ice lattice, same number of molecules
        E.rrect(d, 90, 520, 470, 900, 20, (24, 52, 92), outline=WATER, w=5)
        for k in range(12):
            fx, fy = (k % 4), (k // 4)
            molecule(E, d, 150 + fx * 85 + (fy % 2) * 30, 600 + fy * 110, a=k, s=0.75)
        E.rrect(d, 560, 440, 1010, 980, 20, (30, 50, 80), outline=E.COLD, w=5)
        for k in range(12):
            fx, fy = (k % 3), (k // 3)
            molecule(E, d, 640 + fx * 150 + (fy % 2) * 50, 510 + fy * 135, a=k, s=0.75)
        E.label(d, "AGUA", 280, 450, 44, color=WATER)
        E.label(d, "HIELO", 785, 400, 44, color=E.COLD)
        if u > 0.6:
            E.pill(d, "MISMA MASA", 280, 1000, 34)
            E.pill(d, "MÁS ESPACIO", 785, 1060, 34)
    elif i == 5:  # less dense -> floats
        glass(E, d, 240, 840, 480, 1080, 640)
        k = E.ease(u / (L * 0.6))
        y = E.lerp(800, 600, k) + 4 * math.sin(u * 4)
        E.rrect(d, 440, y, 640, y + 150, 16, ICE, outline=ICE_E, w=4)
        E.arrow(d, 920, 900, 920, 640, color=E.AMB, w=8)
        E.label(d, "MENOS DENSO", 540, 400, 50, color=E.AMB)
    elif i == 6:  # lakes freeze from the top; life below
        E.rrect(d, 80, 560, 1000, 1150, 0, WATER_D)
        th = E.lerp(0, 70, E.ease(u / (L * 0.6)))
        if th > 2:
            E.rrect(d, 80, 560, 1000, 560 + th, 0, ICE)
        # fish
        fx = 300 + 400 * ((u * 0.15) % 1)
        E.poly(d, [(fx, 900), (fx + 90, 860), (fx + 140, 900), (fx + 90, 940)], fill=E.AMB)
        E.poly(d, [(fx, 900), (fx - 50, 860), (fx - 50, 940)], fill=E.AMB)
        E.circle(d, fx + 110, 892, 7, fill=E.CAV)
        for k in range(3):
            E.circle(d, 760 + 20 * k, 800 - ((u * 60 + k * 40) % 160), 9, outline=E.WHITE, w=3)
        E.label(d, "HIELO ARRIBA", 540, 470, 46, color=E.COLD)
        if u > 0.8: E.label(d, "VIDA DEBAJO", 540, 1080, 44, color=E.WHITE)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("pop", s[0] + 0.3), ("whoosh", s[0] + 0.5, 0.8), ("pop", s[1] + 0.3), ("whoosh", s[2] + 0.2, 1.0),
            ("click", s[3] + 0.5), ("pop", s[4] + 0.6), ("whoosh", s[5] + 0.2, 0.8), ("pop", s[6] + 0.8)]
