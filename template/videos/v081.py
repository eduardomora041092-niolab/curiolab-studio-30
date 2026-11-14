"""Video 081 — ¿Qué es el eco?
Science: sound is a wave that travels through the air. When it reaches a large, hard surface such as a cliff or a
wall, it is reflected and travels back. The reflected sound reaches the listener later than the original, and the
delay grows with the distance to the surface. If the surface is far enough away, the reflection is heard as a
separate repetition: that is an echo. If it is close, the reflection arrives so soon that it blends with the original
sound (reverberation). Soft, porous surfaces such as curtains absorb much of the sound and reflect little.
(No minimum delay or distance figures are claimed; no speed of sound is stated.)
"""
import math

ID = "081"
TITLE = "¿Qué es el eco?"
SUBTITLE = "CIENCIA EN 30 SEGUNDOS"
LINES = [
    "¿Por qué tu voz vuelve cuando gritas frente a una montaña?",
    "El sonido es una onda que viaja por el aire.",
    "Cuando choca con una superficie grande y dura, rebota.",
    "La onda rebotada vuelve hacia ti, un poco más tarde.",
    "Si la pared está lejos, oyes la repetición separada: eso es el eco.",
    "Si está cerca, el rebote llega tan rápido que se mezcla con tu voz.",
    "Las superficies blandas, como las cortinas, absorben el sonido y casi no rebota.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"voz", "vuelve", "gritas", "montaña", "sonido", "onda", "aire", "superficie", "dura", "rebota",
            "rebotada", "tarde", "lejos", "repetición", "eco", "cerca", "rápido", "mezcla", "blandas", "cortinas",
            "absorben"}

ROCK = (110, 100, 120)
ROCK_H = (150, 140, 160)
SKIN = (230, 190, 150)
CURT = (170, 60, 80)
WALL = (150, 155, 165)


def arc(E, d, cx, cy, r, a0, a1, col, w=6):
    pts = [(cx + r * math.cos(a0 + (a1 - a0) * t / 20), cy + r * math.sin(a0 + (a1 - a0) * t / 20)) for t in range(21)]
    E.line(d, pts, col, w)


def person(E, d, x, y, shout=True):
    E.circle(d, x, y - 120, 46, fill=SKIN)
    E.rrect(d, x - 40, y - 70, x + 40, y + 70, 24, E.BLUE)
    E.line(d, [(x - 22, y + 70), (x - 26, y + 180)], E.BLUE_D, 18)
    E.line(d, [(x + 22, y + 70), (x + 26, y + 180)], E.BLUE_D, 18)
    E.line(d, [(x + 30, y - 50), (x + 70, y - 110)], SKIN, 14)
    if shout:
        E.circle(d, x + 28, y - 112, 11, fill=E.BG1)


def mountain(E, d, x0, base=1150, h=560, w=360):
    E.poly(d, [(x0, base), (x0 + w * 0.45, base - h), (x0 + w * 0.6, base - h + 70), (x0 + w, base - h + 160),
               (x0 + w + 60, base)], fill=ROCK)
    E.poly(d, [(x0 + w * 0.45, base - h), (x0 + w * 0.36, base - h + 90), (x0 + w * 0.53, base - h + 60)], fill=E.WHITE)


def pulses(E, d, sx, sy, wx, t, n=3, speed=320, col_out=None, col_back=None, absorb=False):
    """Expanding arcs from (sx,sy) to a reflector at x=wx, then reflected arcs coming back."""
    col_out = col_out or E.AMB
    col_back = col_back or E.COLD
    D = wx - sx
    for j in range(n):
        s = (t * speed - j * 140)
        if s <= 0:
            continue
        s = s % (2 * D + 200)
        if s < D:
            arc(E, d, sx, sy, s, -0.45, 0.45, col_out, 7)
        elif s < 2 * D:
            r = s - D
            fade = 0.75 if absorb else 0.0
            col = E.mix(col_back, E.BG1, fade)
            arc(E, d, wx, sy, r, math.pi - 0.45, math.pi + 0.45, col, 7 if not absorb else 3)


def timeline(E, d, y, gap, merged=False):
    E.line(d, [(140, y + 50), (940, y + 50)], E.SIL_D, 3)
    E.rrect(d, 160, y - 20, 440, y + 40, 14, E.AMB)
    E.label(d, "¡HOLA!", 300, y + 10, 36, color=E.WHITE)
    x0 = 160 + gap
    E.rrect(d, x0, y - 10 + (0 if not merged else 0), x0 + 280, y + 40, 14, E.mix(E.COLD, E.BG1, 0.3))
    E.label(d, "hola", x0 + 140, y + 15, 32, color=E.WHITE)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: shout travelling to the mountain and the echo coming back
        person(E, d, 180, 900)
        mountain(E, d, 640)
        pulses(E, d, 250, 790, 790, u + 1.6, n=4, speed=360)
    elif i == 1:  # sound = wave through the air
        for j in range(5):
            y = 520 + j * 120
            for k in range(14):
                x = 150 + k * 60 + 18 * math.sin(k * 0.9 - u * 6 + j)
                E.circle(d, x, y, 8, fill=E.mix(E.SIL_D, E.BG1, 0.2))
        E.wave(d, 150, 760, 930, 760, 180, 60, E.AMB, 7, u * 8)
        E.label(d, "ONDA", 540, 400, 54, color=E.AMB)
        E.label(d, "AIRE", 540, 1110, 44, color=E.MUTED)
    elif i == 2:  # hits a big hard surface and bounces
        E.rrect(d, 820, 380, 940, 1150, 10, WALL)
        for j in range(6):
            E.line(d, [(820, 420 + j * 120), (940, 420 + j * 120)], E.SIL_D, 3)
        k = (u / max(0.5, L)) * 2
        if k < 1:
            arc(E, d, 160, 760, 200 + 460 * k, -0.4, 0.4, E.AMB, 8)
        else:
            arc(E, d, 820, 760, 40 + 400 * (k - 1), math.pi - 0.4, math.pi + 0.4, E.COLD, 8)
        E.arrow(d, 560, 640, 780, 700, E.AMB, 6, 22)
        E.arrow(d, 780, 820, 560, 880, E.COLD, 6, 22)
        E.label(d, "REBOTA", 600, 1020, 50, color=E.COLD)
        E.label(d, "DURA", 880, 330, 40, color=E.WHITE)
    elif i == 3:  # reflected wave comes back a little later
        person(E, d, 180, 900, shout=False)
        mountain(E, d, 640)
        k = min(1.0, u / max(0.5, L * 0.8))
        arc(E, d, 790, 790, 40 + 500 * k, math.pi - 0.45, math.pi + 0.45, E.COLD, 8)
        E.arrow(d, 620, 480, 360, 480, E.COLD, 6, 22)
        E.label(d, "VUELVE", 490, 410, 46, color=E.COLD)
    elif i == 4:  # far wall → separate repetition = echo
        person(E, d, 140, 760)
        mountain(E, d, 700, base=980, h=440, w=280)
        pulses(E, d, 200, 670, 820, u + 0.4, n=2, speed=420)
        E.label(d, "LEJOS", 840, 380, 44, color=E.WHITE)
        k = E.ease(u / (L * 0.6))
        timeline(E, d, 1080, int(160 + 420 * k))
        E.pill(d, "ECO", 540, 380, 46)
    elif i == 5:  # near wall → reflection blends with the voice
        person(E, d, 300, 760)
        E.rrect(d, 560, 420, 660, 980, 10, WALL)
        pulses(E, d, 360, 670, 560, u, n=4, speed=300)
        E.label(d, "CERCA", 610, 370, 44, color=E.WHITE)
        timeline(E, d, 1080, 70, merged=True)
        E.label(d, "SE MEZCLA", 820, 700, 44, color=E.COLD)
    elif i == 6:  # soft curtains absorb sound
        for j in range(7):
            x = 760 + j * 30
            pts = [(x + 12 * math.sin(yy / 40 + j), yy) for yy in range(400, 1121, 20)]
            E.line(d, pts, E.mix(CURT, E.BG1, 0.15 * (j % 2)), 30)
        E.rrect(d, 740, 380, 980, 400, 6, E.SIL_D)
        pulses(E, d, 160, 760, 760, u, n=4, speed=320, absorb=True)
        E.label(d, "ABSORBE", 480, 520, 50, color=E.AMB)
        E.label(d, "CORTINA", 860, 330, 40, color=E.WHITE)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.2, 0.8), ("pop", s[1] + 0.5), ("click", s[2] + 0.7), ("whoosh", s[3] + 0.4, 0.8),
            ("pop", s[4] + 0.8), ("pop", s[5] + 0.6), ("whoosh", s[6] + 0.6, 0.8)]
