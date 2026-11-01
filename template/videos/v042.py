"""Video 042 — ¿Cómo brillan las luciérnagas?
Science: a firefly's light is not fire or electricity but bioluminescence, a chemical reaction. It takes place in the
light organ in the last segments of the abdomen. There a molecule called luciferin reacts with oxygen, and an enzyme,
luciferase, speeds up (catalyses) that reaction. The energy released comes out mostly as light and very little as
heat, which is why it is called "cold light". Fireflies use their flashes to find a mate.
(ATP, magnesium and the nitric-oxide control of flashing are omitted; no efficiency percentages are claimed.)
"""
import math, random

ID = "042"
TITLE = "¿Cómo brillan las luciérnagas?"
SUBTITLE = "CURIOSIDADES DE LA CIENCIA"
LINES = [
    "¿Cómo brillan las luciérnagas?",
    "Su luz no viene del fuego ni de la electricidad.",
    "Nace de una reacción química en la parte final de su abdomen.",
    "Allí, una molécula llamada luciferina reacciona con oxígeno.",
    "Una enzima, la luciferasa, acelera esa reacción.",
    "La energía sale sobre todo como luz y apenas da calor.",
    "Por eso se llama luz fría; la usan para encontrar pareja.",
    "Sígueme para más curiosidades de la ciencia.",
]
KEYWORDS = {"brillan", "luciérnagas", "luz", "fuego", "electricidad", "reacción", "química", "abdomen",
            "molécula", "luciferina", "oxígeno", "enzima", "luciferasa", "acelera", "energía", "calor", "fría",
            "pareja"}

GLOW = (200, 255, 90)
BODY = (60, 50, 40)
WING = (150, 160, 175)
OXY = (90, 170, 255)
LUCI = (255, 200, 60)
ENZ = (200, 120, 255)
rnd = random.Random(42)
FLIES = [(80 + rnd.random() * 920, 330 + rnd.random() * 760, rnd.random() * 6.28) for _ in range(14)]
GRASS = [(x, 1190 - 60 - rnd.random() * 120) for x in range(0, 1100, 28)]

def grass(E, d):
    for x, top in GRASS:
        E.poly(d, [(x - 12, 1190), (x + 4, top), (x + 14, 1190)], fill=(20, 52, 40))

def glow(E, d, x, y, k, r=40):
    for j in range(5, 0, -1):
        E.circle(d, x, y, r * j / 5 * (0.6 + 0.6 * k), fill=E.mix(E.BG1, GLOW, k * (1.1 - j / 5)))

def firefly(E, d, x, y, s=1.0, k=1.0, ang=0.0):
    # head, thorax, abdomen along a body axis; glowing tail at the end of the abdomen
    ca, sa = math.cos(ang), math.sin(ang)
    def at(t): return (x + ca * t * s, y + sa * t * s)
    for side in (-1, 1):
        wx, wy = at(-5)
        E.poly(d, [(wx, wy), (wx - ca * 45 * s - sa * side * 60 * s, wy - sa * 45 * s + ca * side * 60 * s),
                   (wx + ca * 5 * s - sa * side * 55 * s, wy + sa * 5 * s + ca * side * 55 * s)],
               fill=E.mix(E.BG2, WING, 0.5))
    tx, ty = at(-60)
    glow(E, d, tx, ty, k, 60 * s)
    E.circle(d, *at(-55), 26 * s, fill=E.mix(BODY, GLOW, k))
    E.circle(d, *at(-15), 30 * s, fill=BODY)
    E.circle(d, *at(25), 24 * s, fill=(170, 60, 50))
    E.circle(d, *at(50), 16 * s, fill=BODY)

def swarm(E, d, u, n=14):
    for j, (x, y, ph) in enumerate(FLIES[:n]):
        k = max(0.0, math.sin(u * 3 + ph)) ** 2
        xx, yy = x + 30 * math.sin(u * 0.8 + ph), y + 20 * math.cos(u * 0.9 + ph)
        glow(E, d, xx, yy, k, 34)
        E.circle(d, xx, yy, 6, fill=E.mix(E.BG2, GLOW, 0.4 + 0.6 * k))

def molecule(E, d, x, y, col, r=34, label=None, size=34):
    E.circle(d, x, y, r, fill=col)
    if label:
        E.label(d, label, x, y + r + 34, size, color=col)

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: fireflies already flashing over the grass at night
        swarm(E, d, u + 0.6)
        grass(E, d)
        firefly(E, d, 540, 640, 1.4, 0.5 + 0.5 * abs(math.sin(u * 3)), ang=-0.3)
    elif i == 1:  # not fire, not electricity
        firefly(E, d, 540, 560, 1.4, 1.0)
        E.poly(d, [(250, 940), (300, 820), (350, 940)], fill=E.HOT)          # flame icon
        E.poly(d, [(275, 940), (300, 880), (325, 940)], fill=E.AMB)
        E.cross(d, 300, 890, 70)
        E.poly(d, [(800, 810), (750, 890), (785, 890), (760, 960), (830, 870), (793, 870)], fill=E.COLD)  # bolt
        E.cross(d, 780, 890, 70)
        E.label(d, "FUEGO", 300, 1040, 44, color=E.HOT)
        E.label(d, "ELECTRICIDAD", 780, 1040, 44, color=E.COLD)
    elif i == 2:  # chemical reaction at the end of the abdomen
        firefly(E, d, 620, 620, 2.2, 0.6 + 0.4 * abs(math.sin(u * 3)))
        E.arrow(d, 230, 980, 440, 720, E.AMB, 7, 26)
        E.label(d, "FINAL DEL ABDOMEN", 300, 1040, 42, color=E.AMB)
        E.pill(d, "REACCIÓN QUÍMICA", 540, 340, 42)
    elif i == 3:  # luciferin reacts with oxygen
        f = E.ease(min(1, u / (L * 0.7)))
        molecule(E, d, 260 + 200 * f, 700, LUCI, 60, "LUCIFERINA" if f < 0.95 else None, 40)
        molecule(E, d, 820 - 200 * f, 690, OXY, 30)
        molecule(E, d, 850 - 200 * f, 720, OXY, 30)
        if f < 0.95:
            E.label(d, "OXÍGENO", 820, 820, 40, color=OXY)
        else:
            E.label(d, "LUCIFERINA + OXÍGENO", 540, 880, 40, color=E.WHITE)
        E.rrect(d, 120, 420, 960, 1000, 30, None, outline=E.mix(E.BG2, GLOW, 0.5), w=4)
    elif i == 4:  # luciferase speeds up the reaction
        cx, cy = 540, 720
        E.poly(d, [(cx - 200, cy + 30), (cx - 200, cy - 120), (cx - 80, cy - 120), (cx - 80, cy - 30), (cx + 80, cy - 30),
                   (cx + 80, cy - 120), (cx + 200, cy - 120), (cx + 200, cy + 30)], fill=ENZ)
        f = (u * 1.2) % 1
        molecule(E, d, cx - 30, cy - 60, LUCI, 40)
        molecule(E, d, cx + 40, cy - 70, OXY, 22)
        if f > 0.6:
            for ang in (-2.2, -1.6, -1.0):
                E.wave(d, cx + 80 * math.cos(ang), cy - 60 + 80 * math.sin(ang), cx + 220 * math.cos(ang),
                       cy - 60 + 220 * math.sin(ang), 30, 8, GLOW, 5)
        E.label(d, "LUCIFERASA", 540, 830, 48, color=ENZ)
        E.label(d, "ENZIMA", 540, 900, 36, color=E.MUTED)
        E.pill(d, "MÁS RÁPIDO", 540, 1060, 40, bg=ENZ, fg=E.BG1)
    elif i == 5:  # energy out mostly as light, very little heat
        glow(E, d, 540, 640, 1.0, 120)
        E.circle(d, 540, 640, 40, fill=GLOW)
        for ang in [k * math.pi / 4 for k in range(8)]:
            E.wave(d, 540 + 110 * math.cos(ang), 640 + 110 * math.sin(ang), 540 + 300 * math.cos(ang),
                   640 + 300 * math.sin(ang), 40, 10, GLOW, 5, phase=u * 6)
        E.label(d, "LUZ", 300, 1040, 54, color=GLOW)
        E.label(d, "POCO CALOR", 760, 1040, 40, color=E.MUTED)
    elif i == 6:  # cold light; used to find a mate
        swarm(E, d, u, n=8)
        grass(E, d)
        k1 = max(0.0, math.sin(u * 4)) ** 2
        k2 = max(0.0, math.sin(u * 4 - 1.2)) ** 2
        firefly(E, d, 320, 620, 1.1, k1, ang=0.2)
        firefly(E, d, 760, 760, 1.1, k2, ang=math.pi - 0.2)
        E.pill(d, "LUZ FRÍA", 540, 360, 44, bg=GLOW, fg=E.BG1)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.05, 1.0), ("click", s[1] + 0.8), ("pop", s[2] + 0.6), ("zip", s[3] + 0.6, 0.8),
            ("click", s[4] + 0.8), ("pop", s[5] + 0.6), ("whoosh", s[6] + 0.3, 1.2)]
