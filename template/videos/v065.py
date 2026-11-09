"""Video 065 — ¿Cómo sabe el GPS dónde estás?
Science: GPS satellites carry very precise atomic clocks and continuously broadcast radio signals that include the
time each signal was sent and the satellite's position. A GPS receiver (in a phone) only listens; it sends nothing to
the satellites. It measures how long each signal took to arrive and, because the signals travel at the speed of
light, turns each delay into a distance. Each distance places the receiver somewhere on a sphere centred on that
satellite; with several satellites the spheres intersect at a single point: the receiver's position (trilateration).
Because the phone's clock is not as precise as the satellites' clocks, a fourth satellite is needed to solve for that
clock error as well as the three position coordinates.
(No numbers of satellites in the constellation, orbits, accuracies or speeds are claimed.)
"""
import math

ID = "065"
TITLE = "¿Cómo sabe el GPS dónde estás?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo sabe el GPS dónde estás?",
    "Varios satélites envían señales con la hora exacta de salida.",
    "Tu móvil solo escucha: no envía nada a los satélites.",
    "Mide cuánto tardó cada señal en llegar y calcula la distancia.",
    "Cada distancia dibuja una esfera alrededor de un satélite.",
    "Con varios satélites, las esferas se cruzan en un solo punto.",
    "Ese punto es tu posición; un cuarto satélite corrige el reloj.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"gps", "estás", "satélites", "señales", "hora", "exacta", "móvil", "escucha", "envía", "tardó",
            "señal", "distancia", "esfera", "satélite", "cruzan", "punto", "posición", "cuarto", "reloj"}

SIG = (120, 220, 255)
PIN = (238, 84, 54)
EARTH = (40, 90, 150)
LAND = (70, 150, 100)
C1, C2, C3 = (255, 176, 32), (120, 220, 255), (200, 130, 255)

SATS = [(240, 520, C1), (840, 500, C2), (540, 420, C3)]
ME = (560, 900)


def satellite(E, d, x, y, s=1.0, col=None):
    E.rrect(d, x - 35 * s, y - 30 * s, x + 35 * s, y + 30 * s, 8, E.SIL, outline=E.SIL_H, w=3)
    for side in (-1, 1):
        x0 = x + side * 45 * s
        x1 = x + side * 125 * s
        E.rrect(d, min(x0, x1), y - 22 * s, max(x0, x1), y + 22 * s, 4, (40, 80, 160), outline=E.SIL, w=3)
    if col:
        E.circle(d, x, y, 10 * s, fill=col)


def ground(E, d):
    E.circle(d, 540, 2300, 1350, fill=EARTH)
    E.circle(d, 300, 1080, 120, fill=LAND)
    E.circle(d, 820, 1050, 90, fill=LAND)


def phone(E, d, x, y, s=1.0):
    E.rrect(d, x - 40 * s, y - 70 * s, x + 40 * s, y + 70 * s, 12, (35, 42, 60), outline=E.SIL, w=4)
    E.rrect(d, x - 30 * s, y - 55 * s, x + 30 * s, y + 50 * s, 6, (60, 110, 170))


def pulses(E, d, sx, sy, tx, ty, u, col, n=3):
    for k in range(n):
        f = (u * 0.7 + k / n) % 1.0
        x, y = sx + (tx - sx) * f, sy + (ty - sy) * f
        E.circle(d, x, y, 12, fill=col)


def ring(E, d, x, y, r, col, w=5):
    pts = [(x + r * math.cos(a / 90 * 2 * math.pi), y + r * math.sin(a / 90 * 2 * math.pi)) for a in range(91)]
    E.line(d, pts, col, w)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: satellites beaming to a phone, pin pulsing
        ground(E, d)
        for sx, sy, c in SATS:
            satellite(E, d, sx, sy, 0.8, c)
            pulses(E, d, sx, sy, ME[0], ME[1] - 80, u, c)
        phone(E, d, ME[0], ME[1])
        r = 40 + 25 * abs(math.sin(u * 4))
        ring(E, d, ME[0], ME[1], r + 60, PIN, 5)
    elif i == 1:  # satellites send signals with the exact departure time
        ground(E, d)
        for sx, sy, c in SATS:
            satellite(E, d, sx, sy, 0.8, c)
            for k in range(3):
                rr = ((u * 0.8 + k / 3) % 1.0) * 100
                ring(E, d, sx, sy, 60 + rr, E.mix(c, (11, 18, 32), rr / 130), 4)
        E.pill(d, "12:00:00.000", 540, 720, 44)
        E.label(d, "HORA DE SALIDA", 540, 810, 44, color=E.WHITE)
    elif i == 2:  # phone only listens
        ground(E, d)
        phone(E, d, 540, 820, 1.6)
        for sx, sy, c in SATS:
            satellite(E, d, sx, sy, 0.7, c)
            pulses(E, d, sx, sy, 540, 700, u, c)
        E.label(d, "SOLO ESCUCHA", 540, 1080, 50, color=E.AMB)
    elif i == 3:  # measure delay, compute distance
        sx, sy, c = 220, 420, C1
        satellite(E, d, sx, sy, 0.8, c)
        phone(E, d, 820, 900, 1.2)
        f = min(1.0, u / (L * 0.6))
        x, y = sx + (820 - sx) * f, sy + (820 - sy) * f
        E.line(d, [(sx, sy), (x, y)], c, 5)
        E.circle(d, x, y, 14, fill=c)
        if f >= 1.0:
            E.label(d, "TIEMPO = DISTANCIA", 540, 1080, 46, color=E.AMB)
        E.label(d, "RETRASO", 400, 720, 44, color=E.WHITE)
    elif i == 4:  # each distance = sphere around the satellite
        sx, sy, c = 380, 620, C1
        k = E.ease(u / 0.8)
        ring(E, d, sx, sy, 330 * k, c, 6)
        satellite(E, d, sx, sy, 0.7, c)
        E.line(d, [(sx, sy), (sx + 330 * k * 0.8, sy + 330 * k * 0.6)], E.WHITE, 3)
        E.label(d, "ESTÁS EN ALGÚN PUNTO", 540, 1050, 44, color=E.WHITE)
        E.label(d, "DE ESTA ESFERA", 540, 1110, 44, color=E.WHITE)
    elif i == 5:  # several spheres cross at one point
        P = (540, 760)
        ctrs = [(361, 590, C1), (743, 634, C2), (523, 934, C3)]
        n = 1 + int(min(2.99, u / (L * 0.25)))
        for sx, sy, c in ctrs[:n]:
            r = math.hypot(P[0] - sx, P[1] - sy)
            ring(E, d, sx, sy, r, c, 6)
            E.circle(d, sx, sy, 14, fill=c)
        if n == 3:
            E.circle(d, P[0], P[1], 20, fill=PIN, outline=E.WHITE, w=4)
        E.label(d, "UN SOLO PUNTO", 540, 300, 50, color=E.AMB)
    elif i == 6:  # position + fourth satellite fixes the clock
        ground(E, d)
        phone(E, d, ME[0], ME[1])
        E.circle(d, ME[0], ME[1] - 150, 34, fill=PIN, outline=E.WHITE, w=4)
        E.poly(d, [(ME[0] - 26, ME[1] - 130), (ME[0] + 26, ME[1] - 130), (ME[0], ME[1] - 90)], fill=PIN)
        sx, sy = 820, 420
        satellite(E, d, sx, sy, 0.8, (90, 210, 120))
        pulses(E, d, sx, sy, ME[0] + 30, ME[1] - 80, u, (90, 210, 120))
        E.label(d, "4.º SATÉLITE: RELOJ", 400, 380, 42, color=(90, 210, 120))
        E.label(d, "TU POSICIÓN", 540, 1100, 46, color=E.WHITE)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 0.8), ("pop", s[1] + 0.6), ("zip", s[2] + 0.4), ("zip", s[3] + 0.9),
            ("pop", s[4] + 0.5), ("pop", s[5] + 1.0), ("click", s[6] + 0.6)]
