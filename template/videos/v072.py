"""Video 072 — ¿Por qué los copos de nieve tienen seis puntas?
Science: a snowflake starts as a tiny ice crystal that forms in a cloud, usually around a small particle. When water
freezes, its molecules link up through hydrogen bonds into a crystal lattice with hexagonal (six-fold) symmetry
(ordinary ice, Ih). That six-sided lattice gives the young crystal the shape of a small hexagonal prism. As the crystal
falls through humid air, water vapour deposits on it, and the six corners stick out further into the vapour, so they
grow faster and sprout six arms. All six arms grow at the same time under the same temperature and humidity, so they
look alike. Each flake follows its own path through the cloud, so it is very unlikely for two to be identical.
(No specific temperatures, angles or molecular distances are claimed; "never two alike" is softened to "almost never".)
"""
import math

ID = "072"
TITLE = "¿Por qué los copos de nieve tienen seis puntas?"
SUBTITLE = "CIENCIA EN 30 SEGUNDOS"
LINES = [
    "¿Por qué los copos de nieve tienen seis puntas?",
    "Un copo empieza como un cristal de hielo diminuto dentro de una nube.",
    "Al congelarse, las moléculas de agua se enlazan formando hexágonos.",
    "Esa red de seis lados da al cristal su forma hexagonal.",
    "El vapor de agua se pega más rápido en las seis esquinas.",
    "Así crecen seis brazos parecidos, porque todos viven el mismo aire.",
    "Cada copo sigue su propio camino, por eso casi nunca hay dos iguales.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"copos", "nieve", "seis", "puntas", "cristal", "hielo", "diminuto", "nube", "congelarse", "moléculas",
            "agua", "enlazan", "hexágonos", "red", "lados", "hexagonal", "vapor", "esquinas", "brazos", "parecidos",
            "aire", "camino", "iguales"}

ICE = (200, 235, 255)
ICE_D = (110, 170, 220)
VAP = (150, 200, 255)


def hexagon(E, d, x, y, r, rot=0.0, fill=None, outline=ICE, w=4):
    pts = [(x + r * math.cos(rot + k * math.pi / 3), y + r * math.sin(rot + k * math.pi / 3)) for k in range(6)]
    E.poly(d, pts, fill=fill, outline=outline, w=w)


def flake(E, d, x, y, size, rot=0.0, branch=1.0, var=0.0, col=ICE):
    hexagon(E, d, x, y, size * 0.22, rot, fill=ICE_D, outline=col, w=3)
    for k in range(6):
        a = rot + k * math.pi / 3
        L = size * (0.25 + 0.75 * branch)
        ex, ey = x + L * math.cos(a), y + L * math.sin(a)
        E.line(d, [(x, y), (ex, ey)], col, max(3, size * 0.06))
        if branch > 0.4:
            for f in (0.45, 0.7):
                bx, by = x + L * f * math.cos(a), y + L * f * math.sin(a)
                bl = size * (0.32 - 0.25 * f) * min(1, (branch - 0.4) / 0.6) * (1 + var)
                for s in (-1, 1):
                    b = a + s * math.pi / 3
                    E.line(d, [(bx, by), (bx + bl * math.cos(b), by + bl * math.sin(b))], col, max(2, size * 0.04))


def cloud(E, d, x, y, s=1.0):
    for dx, dy, r in ((-160, 20, 110), (-40, -40, 140), (110, 0, 120), (220, 40, 90), (0, 60, 130)):
        E.circle(d, x + dx * s, y + dy * s, r * s, fill=(60, 75, 105))


def molecule(E, d, x, y, rot):
    E.circle(d, x, y, 18, fill=E.HOT)
    for s in (-1, 1):
        a = rot + s * 0.9
        E.circle(d, x + 26 * math.cos(a), y + 26 * math.sin(a), 10, fill=E.WHITE)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: flakes falling and spinning, big flake growing
        for k in range(9):
            x = 100 + (k * 113) % 900
            y = 300 + ((k * 170 + u * 160) % 880)
            flake(E, d, x, y, 40 + 10 * (k % 3), rot=u * (0.5 + 0.2 * k), branch=1.0)
        flake(E, d, 540, 720, 230, rot=u * 0.4, branch=0.6 + 0.4 * min(1.0, u / L))
        E.label(d, "6", 860, 380, 90, color=E.AMB)
    elif i == 1:  # tiny ice crystal born inside a cloud
        cloud(E, d, 540, 560, 1.4)
        k = E.ease(u / (L * 0.6))
        hexagon(E, d, 540, 640, 12 + 40 * k, u * 0.5, fill=ICE_D, outline=ICE, w=4)
        E.label(d, "CRISTAL DE HIELO", 540, 960, 50, color=ICE)
        E.label(d, "NUBE", 540, 360, 46, color=E.SIL_H)
    elif i == 2:  # water molecules link into hexagons
        k = E.ease(u / (L * 0.7))
        R = 90
        centers = [(540, 700), (540 + 1.5 * R, 700 - R * 0.866), (540 + 1.5 * R, 700 + R * 0.866),
                   (540 - 1.5 * R, 700 - R * 0.866), (540 - 1.5 * R, 700 + R * 0.866)]
        for (cx, cy) in centers:
            for j in range(6):
                a = j * math.pi / 3
                tx, ty = cx + R * math.cos(a), cy + R * math.sin(a)
                sx, sy = tx + (1 - k) * 200 * math.cos(j * 2.1 + cx), ty + (1 - k) * 200 * math.sin(j * 1.7 + cy)
                molecule(E, d, sx, sy, u + j)
            if k > 0.8:
                hexagon(E, d, cx, cy, R, 0, outline=E.AMB, w=3)
        E.label(d, "HEXÁGONOS", 540, 1060, 54, color=E.AMB)
    elif i == 3:  # six-sided lattice -> hexagonal crystal
        k = E.ease(u / (L * 0.6))
        hexagon(E, d, 540, 700, 80 + 180 * k, 0, fill=ICE_D, outline=ICE, w=6)
        for j in range(6):
            a = j * math.pi / 3 + math.pi / 6
            r = (80 + 180 * k) * 0.866 + 50
            E.label(d, str(j + 1), 540 + r * math.cos(a), 700 + r * math.sin(a), 46, color=E.AMB)
        E.label(d, "6 LADOS", 540, 1080, 56, color=E.AMB)
    elif i == 4:  # vapour sticks faster to the six corners
        hexagon(E, d, 540, 700, 200, 0, fill=ICE_D, outline=ICE, w=6)
        for j in range(6):
            a = j * math.pi / 3
            cx, cy = 540 + 200 * math.cos(a), 700 + 200 * math.sin(a)
            for m in range(2):
                p = ((u * 0.8 + m * 0.5 + j * 0.13) % 1.0)
                r = 260 - 200 * p
                E.circle(d, 540 + (200 + r) * math.cos(a + 0.08 * (m - 0.5)), 700 + (200 + r) * math.sin(a + 0.08 * (m - 0.5)), 12, fill=VAP)
            E.circle(d, cx, cy, 22 + 6 * abs(math.sin(u * 4)), outline=E.AMB, w=5)
        E.label(d, "ESQUINAS", 540, 330, 52, color=E.AMB)
        E.label(d, "VAPOR", 900, 1080, 44, color=VAP)
    elif i == 5:  # six similar arms grow
        k = min(1.0, 0.2 + u / (L * 0.8))
        flake(E, d, 540, 700, 330, 0, branch=k)
        E.label(d, "6 BRAZOS", 540, 1110, 54, color=E.AMB)
    elif i == 6:  # different paths -> different flakes
        for j, (x, y) in enumerate(((270, 520), (810, 520), (270, 920), (810, 920))):
            trail = [(x + (25 + 15 * j) * math.sin(t * (0.5 + 0.25 * j) + j), y - 200 + t * 14) for t in range(0, 11)]
            E.line(d, trail, E.mix(E.BG2, VAP, 0.6), 4)
            flake(E, d, x, y, 120 + 15 * j, rot=u * 0.3 + j * 0.2, branch=0.45 + 0.18 * j, var=0.25 * j)
        E.label(d, "CASI NUNCA IGUALES", 540, 330, 50, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("pop", s[0] + 0.3), ("zip", s[1] + 0.5), ("click", s[2] + 0.8), ("pop", s[3] + 0.6),
            ("whoosh", s[4] + 0.4, 0.8), ("zip", s[5] + 0.5), ("pop", s[6] + 0.6)]
