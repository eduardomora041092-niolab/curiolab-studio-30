"""Video 051 — ¿Por qué vemos siempre la misma cara de la Luna?
Science: the Moon does rotate on its axis. It takes the same time to turn once on its axis as to go once around the
Earth (synchronous rotation, also called tidal locking). Because of that, as it moves along its orbit it always keeps
the same hemisphere facing the Earth. Earth's gravity stretches the Moon slightly (a tidal bulge); over a very long
time this slowed the Moon's spin until it became synchronised. The far side is not a "dark side": it is lit by the
Sun too, just at different phases.
(No periods in days, distances, time to lock or libration percentages are claimed.)
"""
import math

ID = "051"
TITLE = "¿Por qué vemos siempre la misma cara de la Luna?"
SUBTITLE = "CIENCIA EN 30 SEGUNDOS"
LINES = [
    "¿Por qué vemos siempre la misma cara de la Luna?",
    "Parece que la Luna no gira, pero sí gira sobre sí misma.",
    "Tarda lo mismo en dar una vuelta sobre sí misma que en rodear la Tierra.",
    "Por eso, mientras avanza en su órbita, siempre nos enseña el mismo lado.",
    "A esto se le llama rotación sincronizada.",
    "La gravedad de la Tierra la estiró un poco y, con mucho tiempo, frenó su giro.",
    "La otra cara no es oscura: también recibe la luz del Sol.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"misma", "cara", "luna", "gira", "vuelta", "tierra", "órbita", "lado", "rotación", "sincronizada",
            "gravedad", "estiró", "frenó", "giro", "oscura", "luz", "sol"}

EARTH = (60, 140, 230)
LAND = (80, 180, 110)
MOON = (200, 200, 205)
MOON_D = (150, 150, 158)
FACE = (255, 176, 32)
SUNC = (255, 210, 60)
EX, EY, R = 540, 720, 330


def earth(E, d, x=EX, y=EY, r=95):
    E.circle(d, x, y, r, fill=EARTH)
    E.circle(d, x - 30, y - 25, r * 0.35, fill=LAND)
    E.circle(d, x + 35, y + 30, r * 0.25, fill=LAND)


def orbit(E, d):
    for k in range(48):
        a = 2 * math.pi * k / 48
        E.circle(d, EX + R * math.cos(a), EY + R * math.sin(a), 3, fill=E.MUTED)


def moon(E, d, x, y, face_angle, r=60, mark=True):
    E.circle(d, x, y, r, fill=MOON)
    E.circle(d, x + 0.3 * r, y - 0.35 * r, 0.18 * r, fill=MOON_D)
    if mark:  # the "face": an amber arc on one side
        fx, fy = x + 0.62 * r * math.cos(face_angle), y + 0.62 * r * math.sin(face_angle)
        E.circle(d, fx, fy, 0.32 * r, fill=FACE)


def moon_on_orbit(E, d, a, locked=True):
    x, y = EX + R * math.cos(a), EY + R * math.sin(a)
    face = (a + math.pi) if locked else math.pi   # locked: face points to Earth
    moon(E, d, x, y, face)
    return x, y


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: Moon already orbiting, face always towards Earth
        a = -math.pi / 2 + u * 0.9
        orbit(E, d); earth(E, d)
        moon_on_orbit(E, d, a)
        E.pill(d, "SIEMPRE LA MISMA CARA", 540, 1130, 40)
    elif i == 1:  # it does rotate on itself
        ang = u * 1.6
        moon(E, d, 540, 700, ang, r=200)
        for k in range(3):
            a0 = ang + k * 2.1
            E.arrow(d, 540 + 250 * math.cos(a0), 700 + 250 * math.sin(a0),
                    540 + 250 * math.cos(a0 + 0.5), 700 + 250 * math.sin(a0 + 0.5), E.AMB, 7, 26)
        E.pill(d, "SÍ GIRA", 540, 1060, 44)
    elif i == 2:  # one spin = one orbit
        a = -math.pi / 2 + u * 0.9
        orbit(E, d); earth(E, d)
        moon_on_orbit(E, d, a)
        E.label(d, "1 GIRO", 250, 330, 46, color=E.AMB)
        E.label(d, "=", 540, 330, 50, color=E.WHITE)
        E.label(d, "1 VUELTA", 820, 330, 46, color=E.AMB)
    elif i == 3:  # several positions along the orbit, face always to Earth, + eye on Earth
        orbit(E, d); earth(E, d)
        for k in range(6):
            a = 2 * math.pi * k / 6 + u * 0.4
            x, y = EX + R * math.cos(a), EY + R * math.sin(a)
            moon(E, d, x, y, a + math.pi, r=48)
        E.pill(d, "MISMO LADO", 540, 1130, 42)
    elif i == 4:  # name
        a = -math.pi / 2 + u * 0.9
        orbit(E, d); earth(E, d)
        moon_on_orbit(E, d, a)
        k = E.back_out(min(1, u / 0.5))
        if k > 0.05:
            E.pill(d, "ROTACIÓN SINCRONIZADA", 540, 1130, 40)
    elif i == 5:  # Earth's gravity stretches it slightly and slowed its spin
        earth(E, d, x=280, y=720, r=120)
        s = 1 + 0.12 * E.ease(min(1, u / (L * 0.5)))
        mx, my = 780, 720
        E.circle(d, mx, my, 110, fill=MOON)  # base
        E.rrect(d, mx - 110 * s - 10, my - 95, mx + 110 * s + 10, my + 95, 95, MOON)  # stretched along Earth line
        E.circle(d, mx - 85, my, 34, fill=FACE)
        E.arrow(d, 640, 720, 440, 720, E.AMB, 8, 28)
        E.label(d, "GRAVEDAD", 540, 640, 42, color=E.AMB)
        E.label(d, "GIRO FRENADO", 780, 900, 42, color=E.WHITE)
    elif i == 6:  # far side is lit by the Sun too: Moon between Earth and Sun, far side towards the Sun
        a = -0.2 + 0.1 * math.sin(u * 1.5)
        orbit(E, d); earth(E, d)
        x, y = moon_on_orbit(E, d, a)
        E.circle(d, 1000, 420, 55, fill=SUNC)
        E.label(d, "SOL", 1000, 505, 38, color=SUNC)
        for k in range(3):
            E.arrow(d, 960, 450 + 25 * k, x + 45, y - 30 + 25 * k, SUNC, 4, 18)
        E.label(d, "CARA OCULTA", 850, 860, 40, color=E.WHITE)
        E.arrow(d, 860, 825, x + 40, y + 50, E.WHITE, 5, 20)
        E.pill(d, "TAMBIÉN TIENE LUZ", 540, 1130, 40, bg=E.WHITE)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 1.2), ("zip", s[1] + 0.4, 0.8), ("pop", s[2] + 0.8), ("whoosh", s[3] + 0.3, 1.0),
            ("pop", s[4] + 0.4), ("zip", s[5] + 0.4, 1.0), ("whoosh", s[6] + 0.3, 1.0)]
