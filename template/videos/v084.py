"""Video 084 — ¿Por qué el agua hierve antes en la montaña?
Science: water boils when the pressure of its vapour equals the pressure of the surrounding air; then bubbles of
vapour can form inside the liquid. Heating water raises its vapour pressure. Higher up there is less air above, so
the atmospheric pressure is lower and the vapour reaches it at a lower temperature: on a mountain top water boils
below 100 °C (100 °C is the boiling point at sea-level pressure). Because the boiling water is less hot, food takes
longer to cook. A pressure cooker does the opposite: it raises the pressure, so water boils at a higher temperature.
(No temperature for any specific altitude is claimed.)
"""
import math

ID = "084"
TITLE = "¿Por qué el agua hierve antes en la montaña?"
SUBTITLE = "CIENCIA EN 30 SEGUNDOS"
LINES = [
    "¿Por qué el agua hierve antes en lo alto de una montaña?",
    "Hierve cuando su vapor empuja tan fuerte como el aire que la rodea.",
    "Al calentarla, el vapor empuja cada vez más.",
    "Arriba, en la montaña, hay menos aire encima: menos presión.",
    "Así el vapor la iguala antes, por debajo de cien grados.",
    "Por eso, allí la pasta tarda más en cocerse.",
    "La olla a presión hace lo contrario: el agua hierve más caliente.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"agua", "hierve", "montaña", "vapor", "empuja", "aire", "calentarla", "menos aire", "menos presión",
            "iguala", "cien grados", "pasta", "tarda", "olla a presión", "contrario", "caliente"}

WAT = (60, 140, 230)
WAT_D = (40, 100, 180)
ROCK = (90, 98, 120)
SNOW = (235, 240, 248)
FL1, FL2 = (255, 120, 40), (255, 200, 60)
PASTA = (240, 205, 110)
TH_X = 860
TH_TOP, TH_BOT = 470, 1000


def temp_y(t):
    return TH_BOT - (t / 120.0) * (TH_BOT - TH_TOP)


def thermo(E, d, t, col=None):
    col = col or E.HOT
    E.rrect(d, TH_X - 20, TH_TOP - 20, TH_X + 20, TH_BOT + 10, 20, E.SIL_D)
    E.rrect(d, TH_X - 9, temp_y(t), TH_X + 9, TH_BOT + 10, 8, col)
    E.circle(d, TH_X, TH_BOT + 30, 34, fill=col)
    y = temp_y(100)
    E.line(d, [(TH_X - 34, y), (TH_X + 34, y)], E.WHITE, 5)
    E.label(d, "100 °C", TH_X + 20, y - 40, 34, color=E.WHITE)


def flames(E, d, u, size=1.0):
    for j in range(5):
        x = 420 + j * 60
        h = (50 + 25 * math.sin(u * 9 + j * 1.7)) * size
        E.poly(d, [(x - 24, 1040), (x, 1040 - h), (x + 24, 1040)], fill=FL1)
        E.poly(d, [(x - 12, 1040), (x, 1040 - h * 0.55), (x + 12, 1040)], fill=FL2)


def pot(E, d, u, boil=0.0, lid=False, pasta=False):
    E.rrect(d, 330, 1040, 750, 1060, 6, E.SIL_D)                       # burner
    E.rrect(d, 360, 690, 720, 990, 26, E.SIL_D)                        # pot wall
    E.rrect(d, 378, 690, 702, 972, 18, E.CAV)
    E.rrect(d, 378, 740, 702, 972, 16, WAT)
    E.rrect(d, 330, 700, 362, 720, 8, E.SIL_D)
    E.rrect(d, 718, 700, 750, 720, 8, E.SIL_D)
    if pasta:
        for j in range(7):
            x = 410 + j * 42
            E.line(d, [(x, 960), (x + 30 + 8 * math.sin(u * 2 + j), 770)], PASTA, 7)
    if boil > 0:
        n = int(12 * boil)
        for j in range(n):
            q = (u * 0.9 + j / max(1, n)) % 1.0
            E.circle(d, 405 + (j * 53) % 270, 960 - q * 215, 8 + 8 * q, fill=E.mix(WAT, E.WHITE, 0.55))
        for j in range(4):
            q = (u * 0.5 + j / 4) % 1.0
            E.line(d, [(440 + j * 70, 730 - q * 120), (452 + j * 70, 690 - q * 120)], E.mix(E.MUTED, E.BG1, q), 6)
    if lid:
        E.rrect(d, 340, 650, 740, 700, 18, E.SIL)
        E.rrect(d, 520, 610, 560, 652, 8, E.SIL_D)
        for x in (350, 730):
            E.rrect(d, x - 14, 640, x + 14, 730, 6, E.BRA)


def air_arrows(E, d, n=3, length=90, w=7):
    xs = [540] if n == 1 else [420 + k * 240 / (n - 1) for k in range(n)]
    for x in xs:
        E.arrow(d, x, 650 - length, x, 650, E.WHITE, w, 10 + 2 * w)


def mountain_bg(E, d):
    E.poly(d, [(60, 690), (230, 420), (330, 520), (420, 380), (560, 690)], fill=E.mix(ROCK, E.BG1, 0.55))
    E.poly(d, [(230, 420), (200, 470), (255, 455)], fill=E.mix(SNOW, E.BG1, 0.4))
    E.poly(d, [(420, 380), (390, 430), (450, 425)], fill=E.mix(SNOW, E.BG1, 0.4))


def scene(i, u, L, E, im, d):
    e = E.ease(min(1.0, u / max(0.5, L * 0.85)))
    if i == 0:  # in action from frame 0: pot boiling on a mountain, thermometer below 100 °C
        mountain_bg(E, d)
        flames(E, d, u)
        pot(E, d, u, boil=1.0)
        thermo(E, d, 82)
    elif i == 1:  # boiling: vapour pushes as hard as the air around it
        flames(E, d, u)
        pot(E, d, u)
        r = 60
        E.circle(d, 540, 860, r, fill=E.mix(WAT, E.WHITE, 0.6))
        for k in range(6):
            a = k * math.pi / 3 + 0.5
            E.arrow(d, 540 + (r - 10) * math.cos(a), 860 + (r - 10) * math.sin(a),
                    540 + (r + 40) * math.cos(a), 860 + (r + 40) * math.sin(a), E.AMB, 6, 20)
        air_arrows(E, d, 3, 110, 8)
        E.label(d, "VAPOR", 190, 860, 46, color=E.AMB)
        E.arrow(d, 270, 860, 460, 860, E.AMB, 5, 20)
        E.label(d, "AIRE", 190, 600, 46, color=E.WHITE)
        thermo(E, d, 100)
    elif i == 2:  # heating raises the vapour push
        flames(E, d, u, 1.0 + 0.4 * e)
        pot(E, d, u, boil=0.4 * e)
        r = 30 + 30 * e
        E.circle(d, 540, 860, r, fill=E.mix(WAT, E.WHITE, 0.6))
        for k in range(6):
            a = k * math.pi / 3 + 0.5
            ln = 20 + 40 * e
            E.arrow(d, 540 + r * math.cos(a), 860 + r * math.sin(a),
                    540 + (r + ln) * math.cos(a), 860 + (r + ln) * math.sin(a), E.AMB, 6, 20)
        thermo(E, d, 40 + 50 * e)
        E.label(d, "CALOR", 190, 1010, 44, color=E.HOT)
        E.label(d, "MÁS VAPOR", 200, 760, 40, color=E.AMB)
    elif i == 3:  # higher up: less air above, lower pressure
        E.poly(d, [(80, 1180), (540, 560), (1000, 1180)], fill=ROCK)
        E.poly(d, [(540, 560), (470, 655), (540, 630), (610, 655)], fill=SNOW)
        for j in range(320):
            x = 60 + 960 * ((math.sin(j * 12.9898) * 43758.5453) % 1.0)
            y = 300 + 880 * ((math.sin(j * 78.233) * 12345.678) % 1.0)
            keep = ((math.sin(j * 3.3) * 999.1) % 1.0) < ((y - 300) / 880) ** 1.4
            mx = 540 - abs(x - 540)
            if keep and y < 1180 - (1180 - 560) * (mx - 80) / 460 - 10:
                E.circle(d, x, y, 7, fill=E.MUTED)
        for x in (500, 580):
            E.arrow(d, x, 460, x, 540, E.WHITE, 5, 18)
        E.label(d, "MENOS AIRE", 820, 420, 42, color=E.AMB)
        E.label(d, "MENOS PRESIÓN", 820, 470, 38, color=E.WHITE)
        E.label(d, "MÁS AIRE", 190, 1120, 40, color=E.MUTED)
    elif i == 4:  # vapour matches it sooner: boils below 100 °C
        mountain_bg(E, d)
        flames(E, d, u)
        pot(E, d, u, boil=1.0)
        air_arrows(E, d, 2, 50, 5)
        thermo(E, d, 82)
        E.label(d, "MENOS", 190, 870, 42, color=E.AMB)
        E.label(d, "DE 100 °C", 190, 920, 42, color=E.AMB)
        E.arrow(d, 700, temp_y(82), 820, temp_y(82), E.AMB, 5, 20)
    elif i == 5:  # pasta takes longer to cook
        mountain_bg(E, d)
        flames(E, d, u)
        pot(E, d, u, boil=1.0, pasta=True)
        thermo(E, d, 82)
        cx, cy = 190, 860
        E.circle(d, cx, cy, 80, fill=E.WHITE)
        E.circle(d, cx, cy, 70, fill=E.BG2)
        a = -math.pi / 2 + u * 2.2
        E.line(d, [(cx, cy), (cx + 55 * math.cos(a), cy + 55 * math.sin(a))], E.AMB, 8)
        E.line(d, [(cx, cy), (cx, cy - 40)], E.WHITE, 8)
        E.label(d, "TARDA MÁS", 190, 990, 42, color=E.AMB)
    elif i == 6:  # pressure cooker: higher pressure, hotter boiling
        flames(E, d, u)
        pot(E, d, u, boil=0.8, lid=True)
        for x in (440, 540, 640):
            E.arrow(d, x, 705, x, 760, E.AMB, 7, 22)
        thermo(E, d, 115)
        E.label(d, "OLLA A", 180, 600, 44, color=E.WHITE)
        E.label(d, "PRESIÓN", 180, 650, 44, color=E.WHITE)
        E.label(d, "MÁS", 180, 860, 44, color=E.HOT)
        E.label(d, "DE 100 °C", 180, 910, 44, color=E.HOT)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.2, 0.8), ("pop", s[1] + 0.6), ("zip", s[2] + 0.4), ("whoosh", s[3] + 0.5, 0.8),
            ("pop", s[4] + 0.6), ("click", s[5] + 0.6), ("zip", s[6] + 0.5)]
