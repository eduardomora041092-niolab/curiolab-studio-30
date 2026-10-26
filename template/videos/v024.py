"""Video 024 — ¿Por qué existen las estaciones?
Science: the seasons are not caused by changes in the Earth's distance from the Sun (the orbit is nearly circular,
and the Earth is actually closest to the Sun in the northern winter). They are caused by the tilt of the Earth's
axis, which keeps pointing the same way in space as the Earth orbits the Sun. So for part of the year one
hemisphere is tilted towards the Sun: there sunlight arrives more directly (closer to perpendicular) and its energy
is concentrated on a smaller area, and the days are longer: summer. In the other hemisphere the light arrives at a
low angle and spreads over a larger area, and the days are shorter: winter.
(No tilt angle, distances or dates are claimed; the diagrams are not to scale.)
"""
import math

ID = "024"
TITLE = "¿Por qué existen las estaciones?"
SUBTITLE = "CURIOSIDADES DE LA CIENCIA"
LINES = [
    "¿Por qué en verano el sol calienta más?",
    "No es porque la Tierra esté más cerca del Sol.",
    "El eje sobre el que gira la Tierra está inclinado.",
    "Durante el año, un hemisferio queda inclinado hacia el Sol.",
    "Allí los rayos llegan más directos y concentran su calor.",
    "Además, allí los días son más largos: es verano.",
    "En el otro hemisferio, la luz llega inclinada y se reparte: invierno.",
    "Sígueme para más curiosidades de la ciencia.",
]
KEYWORDS = {"verano", "sol", "calienta", "tierra", "gira", "cerca", "eje", "inclinado", "año", "hemisferio", "rayos",
            "directos", "concentran", "calor", "días", "largos", "inclinada", "reparte", "invierno", "ciencia"}

SUN = (255, 196, 60)
SKY, SKY_W = (110, 175, 235), (70, 95, 140)
GRASS, GRASS_D = (80, 160, 90), (55, 120, 65)
OCEAN, OCEAN_D = (43, 108, 176), (30, 78, 130)
TILT = math.radians(23)

def sun(E, d, x, y, r, u=0.0):
    for k in range(12):
        a = k * math.pi / 6 + u * 0.6
        E.line(d, [(x + (r + 12) * math.cos(a), y + (r + 12) * math.sin(a)), (x + (r + 40) * math.cos(a), y + (r + 40) * math.sin(a))], SUN, 6)
    E.circle(d, x, y, r, fill=SUN)

def tf(cx, cy, x, y, tilt):
    c, s = math.cos(tilt), math.sin(tilt)
    return cx + x * c - y * s, cy + x * s + y * c

def earth(E, d, cx, cy, r, tilt, u, hl=None):
    """hl: 'N' or 'S' hemisphere highlighted. Axis tilted by `tilt` (top leaning right for positive)."""
    E.circle(d, cx, cy, r, fill=OCEAN)
    if hl:
        sgn = -1 if hl == "N" else 1
        pts = [tf(cx, cy, r * math.cos(t * math.pi / 40), sgn * r * abs(math.sin(t * math.pi / 40)), tilt) for t in range(41)]
        E.poly(d, pts, fill=(250, 190, 70))
    for lat in (-50, -25, 25, 50):
        f = math.radians(lat); rr = r * math.cos(f); yy = -r * math.sin(f)
        pts = [tf(cx, cy, rr * math.cos(t * math.pi / 20), yy + 0.22 * rr * math.sin(t * math.pi / 20), tilt) for t in range(21)]
        E.line(d, pts, OCEAN_D, 3)
    pts = [tf(cx, cy, r * math.cos(t * math.pi / 20), 0.22 * r * math.sin(t * math.pi / 20), tilt) for t in range(21)]
    E.line(d, pts, E.WHITE, 4)
    for m in range(3):
        ph = (u * 0.8 + m / 3) % 1
        xx = r * math.cos(math.pi * ph)
        pts = [tf(cx, cy, xx * math.cos(math.radians(a)), -r * math.sin(math.radians(a)), tilt) for a in range(-90, 91, 10)]
        E.line(d, pts, OCEAN_D, 3)
    E.circle(d, cx, cy, r, outline=E.BLUE_D, w=3)
    a0 = tf(cx, cy, 0, -r - 0.45 * r, tilt); a1 = tf(cx, cy, 0, r + 0.45 * r, tilt)
    E.line(d, [a0, a1], E.WHITE, 5)

def street(E, d, u, sun_hi=True):
    E.rrect(d, 100, 330, 980, 1150, 24, SKY if sun_hi else SKY_W)
    E.rrect(d, 100, 960, 980, 1150, 24, GRASS)
    E.rrect(d, 100, 960, 980, 990, 0, GRASS_D)

def scene(i, u, L, E, im, d):
    if i == 0:  # everyday + in action from frame 0: summer street, the sun is already climbing and the thermometer rising
        street(E, d, u)
        t = 0.25 + 0.5 * E.ease(u / L)
        sx, sy = 160 + 760 * t, 900 - 470 * math.sin(math.pi * t)
        sun(E, d, sx, sy, 62, u)
        E.rrect(d, 230, 760, 260, 965, 6, (120, 80, 50))
        E.circle(d, 245, 720, 95, fill=GRASS_D)
        E.poly(d, [(330, 965), (470, 965), (430, 1010), (290, 1010)], fill=GRASS_D)
        TX = 850
        E.rrect(d, TX - 34, 560, TX + 34, 960, 34, E.WHITE)
        lvl = 0.35 + 0.55 * E.ease(u / (L * 0.9))
        E.rrect(d, TX - 16, 940 - 340 * lvl, TX + 16, 940, 16, E.HOT)
        E.circle(d, TX, 940, 46, fill=E.HOT)
        E.pill(d, "VERANO", 540, 1100, 44)
    elif i == 1:  # it is not the distance to the Sun
        E.circle(d, 540, 720, 330, outline=(70, 85, 120), w=4)
        sun(E, d, 540, 720, 95, u)
        a = -math.pi * 0.2 + u * 0.5
        ex, ey = 540 + 330 * math.cos(a), 720 + 330 * math.sin(a)
        earth(E, d, ex, ey, 48, TILT, u)
        E.line(d, [(540 + 105 * math.cos(a), 720 + 105 * math.sin(a)), (ex - 55 * math.cos(a), ey - 55 * math.sin(a))], E.MUTED, 3)
        E.label(d, "DISTANCIA", 540, 1110, 50, color=E.WHITE)
        if u > 0.6:
            E.cross(d, 540, 1110, 60, w=10)
    elif i == 2:  # the axis is tilted
        for k in range(4):
            y = 480 + k * 160; x0 = 60 + 50 * ((u * 1.2 + k * 0.25) % 1)
            E.arrow(d, x0, y, x0 + 140, y, color=SUN, w=6, head=20)
        earth(E, d, 590, 720, 250, TILT * E.ease(u / (L * 0.5)), u)
        E.line(d, [(590, 380), (590, 1060)], E.MUTED, 2)
        E.label(d, "EJE INCLINADO", 590, 1120, 48, color=E.AMB)
    elif i == 3:  # through the year one hemisphere tilts towards the Sun (axis keeps pointing the same way)
        A, B = 380, 150
        pts = [(540 + A * math.cos(t * math.pi / 40), 720 + B * math.sin(t * math.pi / 40)) for t in range(81)]
        E.line(d, pts, (70, 85, 120), 4)
        a = math.pi * (1.0 + 2.0 * E.ease(u / L))      # starts on the left, goes once around
        ex, ey = 540 + A * math.cos(a), 720 + B * math.sin(a)
        hl = "N" if ex < 400 else ("S" if ex > 680 else None)
        if ey < 720:
            earth(E, d, ex, ey, 72, TILT, u, hl); sun(E, d, 540, 720, 95, u)
        else:
            sun(E, d, 540, 720, 95, u); earth(E, d, ex, ey, 72, TILT, u, hl)
        E.label(d, "HACIA EL SOL", 540, 1110, 48, color=E.AMB if hl else E.WHITE)
    elif i in (4, 6):  # direct vs slanted light on the same ground
        direct = i == 4
        E.rrect(d, 100, 960, 980, 1150, 24, GRASS)
        ang = 0.0 if direct else math.radians(55)
        w = 260
        for k in range(5):
            off = -w / 2 + k * w / 4
            x1 = 540 + off / math.cos(ang); y1 = 960
            x0 = x1 - 560 * math.sin(ang); y0 = y1 - 560 * math.cos(ang)
            f = (u * 0.9 + k * 0.17) % 1
            E.arrow(d, E.lerp(x0, x1, f * 0.3), E.lerp(y0, y1, f * 0.3), E.lerp(x0, x1, 0.3 + f * 0.65), E.lerp(y0, y1, 0.3 + f * 0.65), color=SUN, w=7, head=22)
        half = w / 2 / math.cos(ang)
        E.rrect(d, 540 - half, 950, 540 + half, 975, 10, (255, 120, 40) if direct else (250, 215, 120))
        sun(E, d, 540 - 640 * math.sin(ang), 960 - 640 * math.cos(ang) + 40, 70, u)
        if direct:
            E.label(d, "MÁS DIRECTOS", 540, 1110, 50, color=E.AMB)
            E.label(d, "VERANO", 860, 420, 44, color=E.WHITE)
        else:
            E.label(d, "SE REPARTE", 540, 1110, 50, color=E.AMB)
            E.pill(d, "INVIERNO", 800, 420, 44, bg=E.COLD)
    elif i == 5:  # longer days: summer
        street(E, d, u)
        pts = [(160 + 760 * t / 40, 900 - 470 * math.sin(math.pi * t / 40)) for t in range(41)]
        E.line(d, pts, E.WHITE, 3)
        t = E.ease(u / L)
        sun(E, d, 160 + 760 * t, 900 - 470 * math.sin(math.pi * t), 55, u)
        E.rrect(d, 140, 1060, 940, 1110, 14, (30, 36, 60))
        E.rrect(d, 140, 1060, 140 + 560 * min(1, u / (L * 0.6)), 1110, 14, E.AMB)
        E.label(d, "DÍA", 300, 1085, 36, color=E.WHITE)
        E.label(d, "NOCHE", 830, 1085, 34, color=E.MUTED)
        E.pill(d, "DÍAS MÁS LARGOS", 540, 400, 40)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 1.5), ("pop", s[1] + 0.7), ("whoosh", s[2] + 0.2, 1.0), ("whoosh", s[3] + 0.2, 1.6),
            ("pop", s[4] + 0.5), ("pop", s[5] + 0.5), ("whoosh", s[6] + 0.2, 1.0)]
