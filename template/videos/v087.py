"""Video 087 — ¿Cómo flota un barco de acero?
Science: Archimedes' principle: anything placed in water pushes aside (displaces) some water and receives an upward
push (buoyancy) equal to the weight of the water displaced. A solid steel ball displaces only its own small volume; that
water weighs less than the ball, so the ball sinks (steel is denser than water). The same steel shaped into a hollow,
air-filled hull takes up a much larger volume and can displace much more water. The ship settles until the water it
displaces weighs as much as the ship; then buoyancy equals weight and it floats.
(No densities, tonnages or draughts are claimed.)
"""
import math

ID = "087"
TITLE = "¿Cómo flota un barco de acero?"
SUBTITLE = "CIENCIA EN 30 SEGUNDOS"
LINES = [
    "¿Por qué un barco de acero flota y una bola se hunde?",
    "Todo objeto en el agua aparta un poco de agua.",
    "El agua lo empuja hacia arriba con el peso del agua apartada.",
    "Una bola maciza de acero aparta poca agua: su empuje es pequeño.",
    "Pesa más que ese empuje, y se hunde.",
    "Con ese mismo acero, un casco hueco aparta muchísima agua.",
    "Baja hasta que el agua apartada pesa lo mismo que él, y flota.",
    "Sígueme para descubrir más ciencia.",
]
KEYWORDS = {"barco", "acero", "flota", "bola", "hunde", "objeto", "aparta", "agua", "empuja", "arriba", "peso",
            "apartada", "maciza", "poca", "empuje", "pequeño", "pesa", "casco", "hueco", "muchísima"}

SURF = 640
BOT = 1170
WATER = (36, 92, 150)
WATER_H = (70, 140, 205)
DISP = (120, 200, 255)
STEEL = (150, 160, 175)


def water(E, d, u, x0=40, x1=1040, level=SURF):
    E.rrect(d, x0, level, x1, BOT, 6, WATER)
    pts = []
    for k in range(60):
        x = x0 + (x1 - x0) * k / 59
        pts.append((x, level + 5 * math.sin(x / 40 + u * 3)))
    E.line(d, pts, WATER_H, 6)


def ball(E, d, x, y, r=60):
    E.circle(d, x, y, r, fill=STEEL)
    E.circle(d, x - r * 0.35, y - r * 0.35, r * 0.25, fill=(215, 222, 232))


def hull_pts(x, y, w=300, h=150):
    """Hull cross-section; (x, y) = centre of the deck line."""
    return [(x - w / 2, y), (x + w / 2, y), (x + w / 2 - 50, y + h), (x - w / 2 + 50, y + h)]


def ship(E, d, x, y, w=300, h=150, hl=False):
    pts = hull_pts(x, y, w, h)
    E.poly(d, pts, fill=E.AMB if hl else STEEL)
    inner = [(x - w / 2 + 16, y), (x + w / 2 - 16, y), (x + w / 2 - 58, y + h - 16), (x - w / 2 + 58, y + h - 16)]
    E.poly(d, inner, fill=E.CAV)          # hollow, full of air
    E.rrect(d, x - 50, y - 80, x + 40, y, 8, (200, 205, 215))   # cabin
    E.rrect(d, x - 30, y - 64, x - 6, y - 40, 4, E.CAV)


def disp_region(E, d, x, y, level, w=300, h=150):
    """Part of the hull below the waterline = displaced water (light blue)."""
    pts = hull_pts(x, y, w, h)
    if level >= pts[2][1]:
        return
    dl = max(level, y)
    t = (dl - y) / h
    xl = x - w / 2 + 50 * t
    xr = x + w / 2 - 50 * t
    q = [(xl - 8, dl), (xr + 8, dl), (pts[2][0] + 6, pts[2][1] + 8), (pts[3][0] - 6, pts[3][1] + 8)]
    E.line(d, q + [q[0]], DISP, 9)


def up(E, d, x, y, length, label=None, col=None):
    col = col or E.AMB
    E.arrow(d, x, y, x, y - length, col, 9, 30)
    if label:
        E.label(d, label, x, y - length - 34, 40, color=col)


def down(E, d, x, y, length, label=None, col=None):
    col = col or E.HOT
    E.arrow(d, x, y, x, y + length, col, 9, 30)
    if label:
        E.label(d, label, x, y + length + 34, 40, color=col)


def scene(i, u, L, E, im, d):
    bob = 6 * math.sin(u * 3.2)
    if i == 0:  # in action from frame 0: ball already sinking, ship bobbing on the surface
        water(E, d, u)
        by = min(BOT - 70, SURF + 40 + u * 140)
        ball(E, d, 260, by, 55)
        for k in range(4):
            E.circle(d, 260 + (k - 1.5) * 20, by - 80 - ((u * 120 + k * 30) % 120), 6, fill=WATER_H)
        ship(E, d, 720, SURF - 60 + bob)
        E.label(d, "SE HUNDE", 260, 520, 42, color=E.HOT)
        E.label(d, "FLOTA", 720, 440, 42, color=E.AMB)
    elif i == 1:  # an object in water pushes some water aside: the level rises
        k = E.ease(u / (L * 0.7))
        lvl = SURF - 60 * k
        E.rrect(d, 290, 440, 790, BOT, 10, None, outline=E.SIL_D, w=5)
        water(E, d, u, 300, 780, level=lvl)
        E.line(d, [(270, SURF), (310, SURF)], E.MUTED, 4)
        ball(E, d, 540, 380 + 420 * k, 70)
        if k > 0.3:
            E.label(d, "SUBE", 900, lvl, 44, color=DISP)
            E.arrow(d, 900, SURF + 30, 900, lvl + 30, DISP, 6, 22)
            E.label(d, "AGUA APARTADA", 540, 1100, 40, color=DISP)
    elif i == 2:  # water pushes up with the weight of the water displaced
        water(E, d, u)
        E.rrect(d, 400, SURF - 40, 680, SURF + 160, 10, STEEL)
        for x in (450, 540, 630):
            up(E, d, x, 1000, 160 + 20 * math.sin(u * 4 + x))
        E.label(d, "EMPUJE", 540, 1080, 48, color=E.AMB)
        E.label(d, "= PESO DEL AGUA APARTADA", 540, 470, 38, color=E.WHITE)
    elif i == 3:  # a solid steel ball displaces little water: small push
        water(E, d, u)
        ball(E, d, 400, 850, 70)
        E.circle(d, 760, 850, 70, fill=DISP)
        E.label(d, "POCA AGUA", 760, 970, 40, color=DISP)
        E.label(d, "APARTADA", 760, 1015, 40, color=DISP)
        up(E, d, 400, 760, 70, "EMPUJE PEQUEÑO")
    elif i == 4:  # heavier than that push: it sinks
        water(E, d, u)
        by = 820 + min(1.0, u / (L * 0.8)) * 210
        ball(E, d, 540, by, 70)
        up(E, d, 540, by - 80, 60, "EMPUJE")
        down(E, d, 540, by + 80, 0 if by > 1000 else 70)
        E.label(d, "PESO", 760, by + 60, 44, color=E.HOT)
        E.label(d, "SE HUNDE", 540, 440, 50, color=E.HOT)
    elif i == 5:  # same steel, hollow hull: displaces lots of water
        water(E, d, u)
        y = SURF - 60 + bob
        ship(E, d, 540, y, 440, 190, hl=True)
        disp_region(E, d, 540, y, SURF, 440, 190)
        E.label(d, "CASCO HUECO", 540, 400, 46, color=E.AMB)
        E.label(d, "MUCHA AGUA APARTADA", 540, 940, 40, color=DISP)
    elif i == 6:  # it settles until the displaced water weighs as much as the ship: floats
        k = E.ease(u / (L * 0.6))
        y = SURF - 140 + 80 * k + bob * k
        water(E, d, u)
        ship(E, d, 540, y, 440, 190)
        disp_region(E, d, 540, y, SURF, 440, 190)
        up(E, d, 540, 1080, 120 + 40 * k, None)
        E.label(d, "EMPUJE", 760, 1010, 42, color=E.AMB)
        E.label(d, "PESO = EMPUJE", 540, 330, 46, color=E.WHITE)
        if k > 0.9:
            E.label(d, "FLOTA", 540, 400, 50, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.2, 0.8), ("pop", s[1] + 0.6), ("zip", s[2] + 0.5), ("click", s[3] + 0.6),
            ("whoosh", s[4] + 0.4, 0.8), ("pop", s[5] + 0.6), ("zip", s[6] + 0.8)]
