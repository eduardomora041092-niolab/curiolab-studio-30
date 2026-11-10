"""Video 069 — ¿Por qué titilan las estrellas?
Science: stars do not actually flicker; the twinkling (astronomical scintillation) is caused by Earth's atmosphere.
Stars are so far away that, seen from Earth, they are effectively point sources of light. Before reaching our eyes
their light passes through the atmosphere, which contains moving pockets/layers of air at different temperatures and
densities, and therefore slightly different refractive indices. Each pocket bends (refracts) the light a little, and
because the air is turbulent and keeps moving, these deflections change constantly. The result is that the star's
apparent brightness and position jitter rapidly: we see it twinkle.
(No altitudes, frequencies or the planets-vs-stars comparison are claimed.)
"""
import math

ID = "069"
TITLE = "¿Por qué titilan las estrellas?"
SUBTITLE = "CIENCIA EN 30 SEGUNDOS"
LINES = [
    "¿Por qué titilan las estrellas?",
    "Las estrellas no parpadean: lo que cambia es nuestro aire.",
    "Están tan lejos que su luz nos llega como un punto finísimo.",
    "Antes de llegar a tus ojos, esa luz atraviesa toda la atmósfera.",
    "El aire tiene bolsas que se mueven, con distinta temperatura y densidad.",
    "Cada bolsa desvía un poco la luz, y ese desvío cambia sin parar.",
    "Por eso la estrella parece temblar y cambiar de brillo.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"titilan", "estrellas", "parpadean", "aire", "lejos", "luz", "punto", "finísimo", "ojos", "atraviesa",
            "atmósfera", "bolsas", "mueven", "temperatura", "densidad", "desvía", "desvío", "temblar", "brillo"}

STAR = (255, 240, 180)
AIR_W = (255, 150, 90)
AIR_C = (90, 170, 255)
SKY = (8, 12, 26)


def star(E, d, x, y, r, b=1.0):
    c = E.mix(SKY, STAR, b)
    E.circle(d, x, y, r * 2.2, fill=E.mix(SKY, STAR, 0.15 * b))
    E.poly(d, [(x, y - r * 2), (x + r * 0.4, y - r * 0.4), (x + r * 2, y), (x + r * 0.4, y + r * 0.4),
               (x, y + r * 2), (x - r * 0.4, y + r * 0.4), (x - r * 2, y), (x - r * 0.4, y - r * 0.4)], fill=c)
    E.circle(d, x, y, r * 0.6, fill=c)


def night(E, d):
    E.rrect(d, 40, 280, 1040, 1180, 30, SKY)
    for k in range(18):
        x = 80 + (k * 197) % 920
        y = 320 + (k * 131) % 380
        E.circle(d, x, y, 3, fill=(120, 130, 160))


def air_band(E, d, y0, y1, u, cells=True):
    E.rrect(d, 40, y0, 1040, y1, 0, (20, 32, 58))
    if cells:
        for k in range(7):
            x = 130 + ((k * 170 + u * 120 * (1 if k % 2 else -1)) % 820)
            y = y0 + 40 + (k * 53) % max(1, (y1 - y0 - 80))
            col = AIR_W if k % 2 else AIR_C
            E.circle(d, x, y, 50 + 10 * math.sin(u * 2 + k), fill=E.mix((20, 32, 58), col, 0.35))


def eye(E, d, x, y):
    E.poly(d, [(x - 90, y), (x, y - 50), (x + 90, y), (x, y + 50)], fill=E.WHITE)
    E.circle(d, x, y, 34, fill=E.BLUE)
    E.circle(d, x, y, 15, fill=E.BG1)


def bent_ray(E, d, x0, y0, x1, y1, u, amp, color=STAR, w=5, n=24):
    pts = []
    for k in range(n + 1):
        t = k / n
        o = amp * math.sin(t * math.pi * 3 + u * 5) * math.sin(t * math.pi)
        pts.append((x0 + (x1 - x0) * t + o, y0 + (y1 - y0) * t))
    E.line(d, pts, color, w)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: star already twinkling over a night horizon
        night(E, d)
        b = 0.55 + 0.45 * abs(math.sin(u * 7) * math.cos(u * 3.1))
        star(E, d, 540 + 6 * math.sin(u * 9), 620 + 4 * math.cos(u * 11), 40 + 10 * b, b)
        E.poly(d, [(40, 1180), (40, 1020), (300, 960), (560, 1010), (820, 950), (1040, 1000), (1040, 1180)],
               fill=(14, 20, 36))
    elif i == 1:  # star steady, air changes
        night(E, d)
        star(E, d, 540, 420, 40, 1.0)
        E.label(d, "ESTRELLA: LUZ CONSTANTE", 540, 560, 42, color=STAR)
        air_band(E, d, 760, 1060, u)
        E.label(d, "AIRE QUE CAMBIA", 540, 1110, 44, color=AIR_W)
    elif i == 2:  # so far away → a tiny point
        night(E, d)
        k = E.ease(u / (L * 0.7))
        r = 120 * (1 - k) + 8
        star(E, d, 540, 640, r, 1.0)
        E.label(d, "MUY LEJOS", 540, 360, 50, color=E.AMB)
        if k > 0.8:
            E.label(d, "UN PUNTO", 540, 900, 50, color=STAR)
    elif i == 3:  # light crosses the whole atmosphere before reaching the eye
        night(E, d)
        star(E, d, 540, 340, 14, 1.0)
        air_band(E, d, 560, 940, u, cells=False)
        E.label(d, "ATMÓSFERA", 880, 600, 42, color=AIR_C)
        f = min(1.0, u / (L * 0.7))
        E.arrow(d, 540, 380, 540, 380 + (680 * f), STAR, 6, 24)
        eye(E, d, 540, 1110)
    elif i == 4:  # moving pockets of air with different temperature/density
        night(E, d)
        air_band(E, d, 360, 1120, u)
        E.pill(d, "MÁS CALIENTE", 300, 420, 36, bg=AIR_W)
        E.pill(d, "MÁS FRÍO", 800, 1060, 36, bg=AIR_C)
        for k in range(3):
            y = 560 + 180 * k
            E.arrow(d, 420 + 60 * math.sin(u * 2 + k), y, 660 + 60 * math.sin(u * 2 + k), y, E.MUTED, 5, 20)
    elif i == 5:  # each pocket bends light; bending keeps changing
        night(E, d)
        star(E, d, 540, 330, 14, 1.0)
        air_band(E, d, 480, 960, u)
        bent_ray(E, d, 540, 370, 540, 1060, u, 70)
        eye(E, d, 540, 1110)
        E.label(d, "LA LUZ SE DESVÍA", 300, 430, 44, color=STAR)
    elif i == 6:  # star seems to shake and change brightness
        night(E, d)
        b = 0.4 + 0.6 * abs(math.sin(u * 8) * math.cos(u * 3.7))
        star(E, d, 540 + 14 * math.sin(u * 13), 600 + 10 * math.cos(u * 17), 34 + 14 * b, b)
        E.label(d, "TIEMBLA", 300, 900, 50, color=E.AMB)
        E.label(d, "CAMBIA DE BRILLO", 680, 1000, 46, color=STAR)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 0.8), ("pop", s[1] + 0.6), ("zip", s[2] + 0.4), ("whoosh", s[3] + 0.4, 0.8),
            ("pop", s[4] + 0.6), ("zip", s[5] + 0.5), ("click", s[6] + 0.6)]
