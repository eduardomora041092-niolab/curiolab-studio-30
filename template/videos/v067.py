"""Video 067 — ¿Cómo lee un escáner el código de barras?
Science: a linear barcode stores a number as a pattern of dark bars and light spaces of different widths. The scanner
lights the code with a red laser line or a red LED/light source. Light (white) spaces reflect much of that light back,
dark (black) bars absorb most of it and reflect very little. A light sensor (photodiode or camera sensor) receives the
reflected light and turns it into an electrical signal that goes up and down as the beam crosses spaces and bars. The
decoder measures the widths of those pulses and translates the pattern into digits; the shop computer then looks up
that number in its database to show the product and its price.
(No specific barcode standard, digit counts, wavelengths or scan speeds are claimed.)
"""
import math

ID = "067"
TITLE = "¿Cómo lee un escáner el código de barras?"
SUBTITLE = "CÓMO FUNCIONA"
LINES = [
    "¿Cómo lee un escáner el código de barras?",
    "Las barras negras y los espacios blancos guardan un número.",
    "El escáner ilumina el código con un láser o una luz roja.",
    "Los espacios blancos reflejan mucha luz y las barras negras casi nada.",
    "Un sensor recibe esos reflejos y los convierte en una señal eléctrica.",
    "Según el ancho de cada barra, ese patrón se traduce en dígitos.",
    "El ordenador busca ese número y muestra el producto y su precio.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"escáner", "código", "barras", "negras", "espacios", "blancos", "número", "ilumina", "láser", "luz", "roja",
            "reflejan", "nada", "sensor", "reflejos", "señal", "eléctrica", "ancho", "patrón", "dígitos", "ordenador",
            "producto", "precio"}

RED = (255, 60, 60)
PAPER = (245, 247, 250)
INK = (15, 18, 26)
# bar pattern (widths in units; even index = black bar, odd = white space)
PATTERN = [2, 1, 1, 2, 3, 1, 1, 1, 2, 2, 1, 3, 1, 1, 2, 1, 3, 2, 1, 1, 2, 2, 1, 1, 1]
BX0, BX1 = 180, 900


def bars(x0=BX0, x1=BX1, y0=420, y1=820):
    tot = sum(PATTERN)
    out, x = [], x0
    for k, w in enumerate(PATTERN):
        ww = (x1 - x0) * w / tot
        out.append((x, x + ww, k % 2 == 0))
        x += ww
    return out


def code(E, d, y0=420, y1=820, digits=True):
    E.rrect(d, BX0 - 50, y0 - 40, BX1 + 50, y1 + (100 if digits else 40), 18, PAPER)
    for a, b, black in bars(y0=y0, y1=y1):
        if black:
            E.rrect(d, a, y0, b, y1, 0, INK)
    if digits:
        d.text(((BX0 + BX1) / 2 * E.S, (y1 + 55) * E.S), "1  234567  890128", font=E.font(46), fill=INK, anchor="mm")


def scanner(E, d, x, y):
    E.poly(d, [(x - 120, y - 70), (x + 120, y - 70), (x + 90, y + 40), (x - 90, y + 40)], fill=E.SIL_D, outline=E.SIL, w=3)
    E.rrect(d, x - 40, y + 30, x + 40, y + 200, 20, E.SIL_D, outline=E.SIL, w=3)
    E.rrect(d, x - 95, y + 30, x + 95, y + 44, 6, RED)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: red scan line sweeping across the code
        code(E, d, y0=440, y1=840)
        x = BX0 - 30 + (BX1 - BX0 + 60) * (0.5 + 0.5 * math.sin(u * 3))
        E.rrect(d, x - 4, 380, x + 4, 960, 3, RED)
        E.circle(d, x, 400, 14, fill=RED)
        E.label(d, "BIP", 880, 330, 60, color=RED)
    elif i == 1:  # bars and spaces store a number
        code(E, d)
        k = E.ease(u / 0.8)
        E.label(d, "BARRA", 300, 340, 44, color=E.AMB)
        E.arrow(d, 300, 365, 200, 420, E.AMB, 6, 20)
        E.label(d, "ESPACIO", 760, 340, 44, color=E.COLD)
        E.arrow(d, 760, 365, 700, 420, E.COLD, 6, 20)
        if k > 0.1:
            E.pill(d, "UN NÚMERO", 540, 1060, 48)
    elif i == 2:  # scanner lights the code with red light
        code(E, d, y0=620, y1=980, digits=False)
        scanner(E, d, 540, 330)
        f = E.ease(u / 0.6)
        w = (BX1 - BX0) / 2 * f
        E.poly(d, [(450, 374), (630, 374), (540 + w, 800), (540 - w, 800)], fill=E.mix((11, 18, 32), RED, 0.35))
        E.rrect(d, 540 - w, 796, 540 + w, 804, 3, RED)
        E.label(d, "LUZ ROJA", 860, 520, 46, color=RED)
    elif i == 3:  # white spaces reflect, black bars absorb
        code(E, d, y0=620, y1=980, digits=False)
        bs = bars(y0=620, y1=980)
        for k, (a, b, black) in enumerate(bs):
            if k in (5, 9, 13, 17):  # white spaces: strong reflection back up
                cx = (a + b) / 2
                E.arrow(d, cx - 40, 400, cx - 6, 600, RED, 5, 18)
                E.arrow(d, cx + 6, 600, cx + 40 + 10 * math.sin(u * 6), 400, E.WHITE, 6, 22)
            if k in (4, 16):  # black bars: light goes in, almost nothing comes out
                cx = (a + b) / 2
                E.arrow(d, cx - 40, 400, cx - 6, 600, RED, 5, 18)
        E.label(d, "BLANCO: REFLEJA", 540, 300, 46, color=E.WHITE)
        E.label(d, "NEGRO: ABSORBE", 540, 1080, 46, color=E.AMB)
    elif i == 4:  # sensor turns reflections into an electrical signal
        code(E, d, y0=300, y1=520, digits=False)
        E.rrect(d, 120, 640, 280, 760, 16, E.SIL_D, outline=E.SIL, w=3)
        E.label(d, "SENSOR", 200, 800, 38, color=E.SIL_H)
        E.wave(d, 260, 560, 210, 640, 40, 6, RED, 5, phase=u * 8)
        f = min(1.0, u / (L * 0.8))
        pts = []
        xe = BX0 + (BX1 - BX0) * f
        for a, b, black in bars():
            if a > xe:
                break
            yy = 1030 if black else 900
            pts += [(320 + (a - BX0) * 0.8, yy), (320 + (min(b, xe) - BX0) * 0.8, yy)]
        if len(pts) >= 2:
            E.line(d, pts, E.AMB, 6)
        E.arrow(d, 280, 700, 320, 900, E.AMB, 5, 18)
        E.label(d, "SEÑAL", 960, 840, 40, color=E.AMB)
    elif i == 5:  # pulse widths become digits
        pts = []
        for a, b, black in bars():
            yy = 640 if black else 480
            pts += [(a, yy), (b, yy)]
        E.line(d, pts, E.AMB, 6)
        bs = bars()
        for k in (0, 4, 10):
            a, b, _ = bs[k]
            E.line(d, [(a, 700), (b, 700)], E.COLD, 5)
            E.line(d, [(a, 690), (a, 710)], E.COLD, 4)
            E.line(d, [(b, 690), (b, 710)], E.COLD, 4)
        E.label(d, "ANCHO", 540, 760, 44, color=E.COLD)
        k = E.ease(u / 0.9)
        shown = "1234567890128"[: max(1, int(13 * k))]
        E.rrect(d, 170, 880, 910, 1020, 20, E.CAV, outline=E.SIL_D, w=3)
        E.label(d, shown, 540, 950, 64, color=E.WHITE)
    elif i == 6:  # computer looks up number → product and price
        E.rrect(d, 200, 360, 880, 860, 24, E.CAV, outline=E.SIL, w=5)
        E.rrect(d, 480, 860, 600, 960, 0, E.SIL_D)
        E.rrect(d, 360, 960, 720, 990, 12, E.SIL_D)
        E.label(d, "1234567890128", 540, 440, 46, color=E.MUTED)
        k = E.ease(u / 0.6)
        if k > 0.2:
            E.rrect(d, 300, 520, 780, 660, 16, E.BLUE_D)
            E.label(d, "PRODUCTO", 540, 590, 56, color=E.WHITE)
        if k > 0.6:
            E.rrect(d, 300, 690, 780, 820, 16, E.mix(E.BLUE_D, E.AMB, 0.4))
            E.label(d, "PRECIO", 540, 755, 56, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("click", s[0] + 0.2), ("pop", s[1] + 0.6), ("zip", s[2] + 0.3), ("whoosh", s[3] + 0.4, 0.8),
            ("zip", s[4] + 0.4), ("pop", s[5] + 0.9), ("click", s[6] + 0.6)]
