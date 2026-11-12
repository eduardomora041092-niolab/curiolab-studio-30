"""Video 074 — ¿Cómo cancelan el ruido unos auriculares?
Science: sound is a pressure wave. Active noise-cancelling headphones have small microphones that continuously pick up
the ambient noise. Electronics (a processing chip) generate an "anti-noise" signal with the same shape but inverted
phase (where the noise pressure rises, the anti-noise falls). The headphone speaker plays this signal together with
the music. At the ear the two waves add up and largely cancel by destructive interference, so the noise is greatly
reduced. It works best on steady, low-frequency sounds such as engine hum; sudden or high-pitched sounds are harder to
cancel and are blocked mainly by the ear cushions (passive isolation).
(No decibel figures or frequency limits are claimed; cancellation is "casi", never total.)
"""
import math

ID = "074"
TITLE = "¿Cómo cancelan el ruido unos auriculares?"
SUBTITLE = "CÓMO FUNCIONA"
LINES = [
    "¿Cómo crean silencio unos auriculares con más sonido?",
    "El ruido llega al oído como una onda de presión.",
    "Un micrófono en el auricular escucha ese ruido sin parar.",
    "Un chip calcula una onda igual, pero invertida.",
    "El altavoz la reproduce: donde el ruido sube, ella baja.",
    "Al sumarse, las dos ondas se anulan y el ruido casi desaparece.",
    "Funciona mejor con zumbidos constantes, como el motor de un avión.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"silencio", "auriculares", "sonido", "ruido", "oído", "onda", "presión", "micrófono", "chip", "invertida",
            "altavoz", "sube", "baja", "sumarse", "anulan", "desaparece", "zumbidos", "constantes", "motor", "avión"}

NOISE = (238, 84, 54)
ANTI = (90, 170, 255)
SUM = (120, 230, 160)


def sine(E, d, x0, x1, y, amp, wl, ph, color, w=7, sign=1.0):
    pts = []
    for k in range(121):
        x = x0 + (x1 - x0) * k / 120
        pts.append((x, y - sign * amp * math.sin(2 * math.pi * (x - x0) / wl - ph)))
    E.line(d, pts, color, w)


def headphone(E, d, x, y, s=1.0, glow=0.0):
    E.line(d, [(x - 170 * s, y), (x - 170 * s, y - 120 * s), (x, y - 230 * s), (x + 170 * s, y - 120 * s),
               (x + 170 * s, y)], E.SIL_D, 26 * s)
    for sx in (-1, 1):
        E.rrect(d, x + sx * 170 * s - 60 * s, y - 40 * s, x + sx * 170 * s + 60 * s, y + 130 * s, 40 * s,
                E.mix(E.BLUE_D, E.BLUE, glow), outline=E.SIL_H, w=3)


def ear(E, d, x, y):
    E.circle(d, x, y, 80, fill=E.BRA_D)
    E.circle(d, x, y, 36, fill=E.BRA)


def scene(i, u, L, E, im, d):
    ph = u * 6
    if i == 0:  # in action from frame 0: noise wave hits headphone and gets flattened
        headphone(E, d, 700, 760, 1.0, 0.6)
        sine(E, d, 60, 480, 700, 80, 160, ph, NOISE)
        sine(E, d, 620, 1020, 1000, 6, 160, ph, SUM, 6)
        E.label(d, "RUIDO", 220, 560, 48, color=NOISE)
    elif i == 1:  # sound = pressure wave arriving at the ear
        ear(E, d, 880, 720)
        for k in range(10):
            x = 120 + ((k * 70 + u * 160) % 700)
            dens = 0.5 + 0.5 * math.sin(2 * math.pi * x / 140 - ph)
            E.line(d, [(x, 560), (x, 880)], E.mix(E.BG2, NOISE, dens), 6 + 8 * dens)
        sine(E, d, 120, 780, 1020, 60, 140, ph, NOISE, 6)
        E.label(d, "ONDA DE PRESIÓN", 450, 470, 50, color=NOISE)
    elif i == 2:  # microphone listens all the time
        headphone(E, d, 540, 760, 1.2)
        E.circle(d, 290, 680, 22, fill=E.AMB, outline=E.WHITE, w=3)
        sine(E, d, 60, 260, 540, 50, 120, ph, NOISE, 6)
        E.label(d, "MICRÓFONO", 330, 1050, 50, color=E.AMB)
        E.arrow(d, 330, 1010, 300, 720, E.AMB, 7, 26)
    elif i == 3:  # chip computes the inverted wave
        E.rrect(d, 400, 600, 680, 800, 18, E.BG1, outline=E.SIL_H, w=4)
        for k in range(6):
            E.line(d, [(420 + k * 48, 590), (420 + k * 48, 560)], E.SIL_D, 6)
            E.line(d, [(420 + k * 48, 810), (420 + k * 48, 840)], E.SIL_D, 6)
        E.label(d, "CHIP", 540, 700, 54, color=E.WHITE)
        sine(E, d, 100, 900, 430, 60, 200, ph, NOISE, 6)
        sine(E, d, 100, 900, 1010, 60, 200, ph, ANTI, 6, sign=-1.0)
        E.label(d, "INVERTIDA", 540, 1120, 46, color=ANTI)
    elif i == 4:  # speaker plays it: noise up where anti-noise down
        sine(E, d, 100, 980, 560, 110, 300, ph, NOISE, 7)
        sine(E, d, 100, 980, 900, 110, 300, ph, ANTI, 7, sign=-1.0)
        xm = 100 + 75   # first crest of the noise (sin peak at quarter wavelength when ph=0); marker follows phase
        xm = 100 + ((75 + ph / (2 * math.pi) * 300) % 300)
        E.arrow(d, xm, 500, xm, 420, NOISE, 8, 26)
        E.arrow(d, xm, 960, xm, 1040, ANTI, 8, 26)
        E.label(d, "SUBE", 860, 360, 44, color=NOISE)
        E.label(d, "BAJA", 860, 1110, 44, color=ANTI)
    elif i == 5:  # sum cancels
        k = E.ease(u / (L * 0.7))
        sine(E, d, 100, 980, 420, 70, 300, ph, NOISE, 6)
        sine(E, d, 100, 980, 640, 70, 300, ph, ANTI, 6, sign=-1.0)
        E.label(d, "+", 540, 760, 70, color=E.WHITE)
        sine(E, d, 100, 980, 940, 70 * (1 - k) + 4, 300, ph, SUM, 7)
        E.label(d, "SILENCIO", 540, 1080, 52, color=SUM)
    elif i == 6:  # best for steady hum like a plane engine
        E.poly(d, [(120, 640), (900, 600), (980, 640), (900, 680), (120, 660)], fill=E.SIL)
        E.poly(d, [(480, 630), (380, 470), (440, 470), (600, 630)], fill=E.SIL_D)
        E.rrect(d, 500, 680, 640, 740, 26, E.SIL_D)
        for k in range(3):
            E.circle(d, 570, 710, 50 + k * 40 + (u * 60) % 40, outline=E.mix(NOISE, E.BG2, k / 3), w=4)
        sine(E, d, 120, 960, 960, 40, 220, ph, NOISE, 6)
        E.label(d, "ZUMBIDO CONSTANTE", 540, 1100, 46, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.2, 0.8), ("pop", s[1] + 0.5), ("click", s[2] + 0.6), ("zip", s[3] + 0.5),
            ("pop", s[4] + 0.6), ("whoosh", s[5] + 0.5, 0.8), ("click", s[6] + 0.6)]
