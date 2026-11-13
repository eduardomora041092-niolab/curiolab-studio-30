"""Video 076 — ¿Cómo funciona un mando a distancia?
Science: the tip of an infrared remote holds an LED that emits infrared light, invisible to the human eye (many phone
cameras do pick it up). When a button is pressed, a chip in the remote switches the LED on and off very quickly; the
pattern of pulses is a code that is different for each button. In the TV, an infrared receiver (a photodiode) detects
the light pulses and turns them into an electrical signal. A microcontroller decodes that signal and carries out the
command, such as raising the volume or changing channel.
(No carrier frequencies, wavelengths or protocol names are claimed.)
"""
import math

ID = "076"
TITLE = "¿Cómo funciona un mando a distancia?"
SUBTITLE = "CÓMO FUNCIONA"
LINES = [
    "¿Cómo funciona el mando a distancia de la tele?",
    "En la punta del mando hay un LED que emite luz infrarroja.",
    "Esa luz es invisible para tus ojos, pero muchas cámaras de móvil sí la captan.",
    "Al pulsar un botón, el LED se enciende y se apaga muy rápido.",
    "Esos destellos forman un código distinto para cada botón.",
    "En la tele, un receptor detecta los pulsos y los convierte en señal eléctrica.",
    "Un chip lee el código y sube el volumen o cambia de canal.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"mando", "distancia", "tele", "led", "luz", "infrarroja", "invisible", "ojos", "cámaras", "móvil",
            "botón", "enciende", "apaga", "rápido", "destellos", "código", "receptor", "pulsos", "eléctrica",
            "chip", "volumen", "canal"}

IR = (200, 80, 220)
DARK = (40, 46, 60)
SCREEN = (60, 110, 190)


def remote(E, d, x, y, s=1.0, led_on=True):
    """Horizontal remote, LED tip on the right at (x + 230*s, y)."""
    E.rrect(d, x - 230 * s, y - 55 * s, x + 220 * s, y + 55 * s, 40 * s, DARK, outline=E.SIL_D, w=3)
    for k in range(4):
        for j in range(2):
            E.circle(d, x - 150 * s + k * 70 * s, y - 22 * s + j * 44 * s, 14 * s, fill=E.SIL_D)
    E.circle(d, x + 105 * s, y, 22 * s, fill=E.HOT)
    E.circle(d, x + 228 * s, y, 18 * s, fill=IR if led_on else E.SIL_D)


def tv(E, d, x, y, w=300, h=200, scr=SCREEN):
    E.rrect(d, x - w / 2 - 14, y - h / 2 - 14, x + w / 2 + 14, y + h / 2 + 14, 16, DARK, outline=E.SIL_D, w=3)
    E.rrect(d, x - w / 2, y - h / 2, x + w / 2, y + h / 2, 8, scr)
    E.rrect(d, x - 40, y + h / 2 + 14, x + 40, y + h / 2 + 50, 6, DARK)
    E.circle(d, x + w / 2 - 20, y + h / 2 + 2, 8, fill=E.HOT)  # receiver window


def pulses(E, d, x0, y0, x1, n, u, col=IR, r=10):
    for k in range(n):
        f = ((u * 0.9) + k / n) % 1.0
        E.circle(d, x0 + (x1 - x0) * f, y0, r, fill=col)


def code(E, d, x0, y, bits, w=60, h=70, col=IR):
    pts = [(x0, y)]
    x = x0
    for b in bits:
        yy = y - h if b else y
        pts += [(x, yy), (x + w, yy)]
        x += w
    pts.append((x, y))
    E.line(d, pts, col, 6)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: pulses already flying to a TV that changes channel
        remote(E, d, 300, 820, 0.9, led_on=int(u * 8) % 2 == 0)
        tv(E, d, 820, 640, 340, 230, scr=[SCREEN, (190, 90, 60), (70, 160, 90)][int(u * 2.5) % 3])
        pulses(E, d, 520, 820, 900, 6, u * 2)
        E.wave(d, 520, 820, 860, 760, 60, 12, IR, 4, u * 10)
    elif i == 1:  # LED at the tip emits infrared
        remote(E, d, 420, 720, 1.4)
        for k in range(3):
            E.wave(d, 760, 720 - 60 + k * 60, 1040, 720 - 140 + k * 140, 50, 10, IR, 4, u * 8)
        E.label(d, "LED", 740, 590, 52, color=IR)
        E.label(d, "LUZ INFRARROJA", 540, 1000, 50, color=E.WHITE)
    elif i == 2:  # invisible to the eye, phone camera sees it
        # eye
        E.poly(d, [(110, 560), (250, 480), (390, 560), (250, 640)], fill=E.WHITE)
        E.circle(d, 250, 560, 45, fill=E.BLUE)
        E.circle(d, 250, 560, 20, fill=E.BG1)
        E.label(d, "OJO", 250, 720, 46, color=E.MUTED)
        E.cross(d, 250, 860, 50)
        # phone with camera view
        E.rrect(d, 640, 380, 960, 1000, 36, DARK, outline=E.SIL_D, w=4)
        E.rrect(d, 665, 420, 935, 960, 20, (25, 30, 45))
        remote(E, d, 760, 690, 0.55)
        glow = 0.6 + 0.4 * math.sin(u * 12)
        E.circle(d, 886, 690, 30 * glow + 10, fill=E.mix((25, 30, 45), IR, 0.6))
        E.circle(d, 886, 690, 14, fill=(250, 220, 255))
        E.label(d, "CÁMARA", 800, 1070, 46, color=IR)
    elif i == 3:  # LED switches on and off very fast
        on = int(u * 10) % 2 == 0
        remote(E, d, 420, 600, 1.4, led_on=on)
        if on:
            E.circle(d, 740, 600, 60, fill=E.mix(E.BG2, IR, 0.5))
            E.circle(d, 740, 600, 26, fill=IR)
        E.label(d, "ENCENDIDO" if on else "APAGADO", 540, 820, 54, color=IR if on else E.MUTED)
        k = E.ease(u / (L * 0.9))
        code(E, d, 150, 1060, [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1][:max(1, int(13 * k))], w=60, h=80)
    elif i == 4:  # each button has its own code
        E.pill(d, "VOL +", 230, 470, 44)
        code(E, d, 400, 500, [1, 1, 0, 1, 0, 0, 1, 1], w=70, h=70, col=E.AMB)
        E.pill(d, "CANAL", 230, 760, 44)
        code(E, d, 400, 790, [1, 0, 0, 1, 1, 0, 1, 0], w=70, h=70, col=E.COLD)
        x = 400 + 560 * ((u * 0.6) % 1.0)
        E.line(d, [(x, 400), (x, 860)], E.WHITE, 3)
        E.label(d, "CÓDIGO", 540, 1020, 54, color=E.WHITE)
    elif i == 5:  # receiver detects pulses and makes an electrical signal
        tv(E, d, 680, 520, 520, 330)
        E.circle(d, 920, 702, 26, outline=E.AMB, w=6)
        pulses(E, d, 120, 702, 900, 5, u * 2)
        E.label(d, "RECEPTOR", 920, 790, 44, color=E.AMB)
        E.line(d, [(920, 730), (920, 880), (420, 880)], E.SIL_D, 5)
        code(E, d, 440, 1040, [1, 0, 1, 1, 0, 1, 0], w=60, h=70, col=E.AMB)
        E.label(d, "SEÑAL ELÉCTRICA", 540, 1120, 42, color=E.WHITE)
    elif i == 6:  # chip decodes and acts
        tv(E, d, 540, 520, 600, 360)
        k = E.ease(u / (L * 0.8))
        for b in range(10):
            col = E.AMB if b < 3 + int(7 * k) else E.SIL_D
            E.rrect(d, 300 + b * 48, 600 - b * 16, 334 + b * 48, 640, 4, col)
        E.label(d, "VOLUMEN", 540, 420, 48, color=E.WHITE)
        E.rrect(d, 430, 860, 650, 1000, 12, (30, 70, 50), outline=E.SIL, w=3)
        for j in range(6):
            E.line(d, [(450 + j * 38, 860), (450 + j * 38, 830)], E.SIL, 4)
            E.line(d, [(450 + j * 38, 1000), (450 + j * 38, 1030)], E.SIL, 4)
        E.label(d, "CHIP", 540, 930, 46, color=E.WHITE)
        E.arrow(d, 540, 820, 540, 740, E.AMB, 6, 24)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("click", s[0] + 0.2), ("pop", s[1] + 0.5), ("click", s[2] + 0.6), ("zip", s[3] + 0.5),
            ("click", s[4] + 0.6), ("whoosh", s[5] + 0.5, 0.8), ("pop", s[6] + 0.6)]
