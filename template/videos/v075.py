"""Video 075 — ¿Cómo se forma una nube?
Science: the Sun warms the ground, which warms the air above it; warm, moist air is less dense and rises (clouds also
form when air is pushed up over mountains or fronts). That air carries water vapour, an invisible gas. As it rises the
surrounding pressure falls, so the air expands and cools (adiabatic cooling). Cooler air can hold less water vapour;
when it cools to its dew point the vapour condenses into tiny liquid droplets (or ice crystals) on microscopic
particles such as dust, salt or smoke (condensation nuclei). Huge numbers of these droplets together scatter light and
form the visible cloud. The droplets are so small that rising air keeps them aloft, which is why a cloud can contain
a lot of water and still float.
(No altitudes, lapse rates or cloud masses are claimed.)
"""
import math

ID = "075"
TITLE = "¿Cómo se forma una nube?"
SUBTITLE = "CIENCIA EN 30 SEGUNDOS"
LINES = [
    "¿Cómo se forma una nube en el cielo?",
    "El sol calienta el suelo y el aire húmedo empieza a subir.",
    "Ese aire lleva vapor de agua, un gas invisible que no vemos.",
    "Al subir, la presión baja, el aire se expande y se enfría.",
    "El aire frío no puede guardar tanto vapor.",
    "El vapor se condensa en gotitas sobre motas de polvo y sal.",
    "Millones de gotitas juntas forman la nube blanca que vemos.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"nube", "cielo", "sol", "calienta", "suelo", "aire", "húmedo", "subir", "vapor", "agua", "gas",
            "invisible", "presión", "expande", "enfría", "frío", "condensa", "gotitas", "polvo", "sal", "millones"}

CLOUD = (235, 240, 248)
GROUND = (70, 120, 70)
VAP = (150, 200, 255)


def sun(E, d, x=880, y=360, r=60):
    E.circle(d, x, y, r, fill=E.AMB)
    for k in range(8):
        a = k * math.pi / 4
        E.line(d, [(x + (r + 15) * math.cos(a), y + (r + 15) * math.sin(a)),
                   (x + (r + 45) * math.cos(a), y + (r + 45) * math.sin(a))], E.AMB, 6)


def ground(E, d):
    E.rrect(d, 0, 1080, 1080, 1190, 0, GROUND)


def puff(E, d, x, y, s, col=CLOUD):
    for dx, dy, r in ((-90, 10, 60), (-30, -30, 75), (50, -20, 70), (110, 15, 55), (10, 30, 70)):
        E.circle(d, x + dx * s, y + dy * s, r * s, fill=col)


def parcel(E, d, x, y, r, col):
    E.circle(d, x, y, r, outline=col, w=4)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: cloud already growing above rising air
        ground(E, d); sun(E, d)
        k = 0.4 + 0.6 * E.ease(u / (L * 0.9))
        for j in range(5):
            yy = 1050 - ((j * 110 + u * 200) % 550)
            E.arrow(d, 300 + j * 120, yy + 60, 300 + j * 120, yy, VAP, 6, 22)
        puff(E, d, 540, 440, 0.8 + 0.6 * k)
    elif i == 1:  # sun heats the ground, moist air rises
        ground(E, d); sun(E, d)
        for k in range(5):
            E.wave(d, 860 - k * 40, 440, 520 - k * 80, 1060, 70, 10, E.AMB, 4, u * 6)
        y = 1000 - 380 * E.ease(u / (L * 0.9))
        parcel(E, d, 300, y, 80, VAP)
        E.arrow(d, 300, y - 90, 300, y - 180, VAP, 8, 28)
        E.label(d, "AIRE CALIENTE", 300, 1130, 42, color=E.WHITE)
    elif i == 2:  # vapour, invisible gas
        parcel(E, d, 540, 720, 260, VAP)
        for k in range(26):
            a = k * 2.4 + u * 1.5
            r = 40 + (k * 37) % 210
            E.circle(d, 540 + r * math.cos(a), 720 + r * math.sin(a), 7, fill=E.mix(E.BG2, VAP, 0.45))
        E.label(d, "VAPOR DE AGUA", 540, 380, 52, color=VAP)
        E.label(d, "INVISIBLE", 540, 1080, 48, color=E.MUTED)
    elif i == 3:  # rising: pressure drops, air expands and cools
        k = E.ease(u / (L * 0.9))
        y = 1000 - 520 * k
        r = 70 + 90 * k
        parcel(E, d, 540, y, r, E.mix(E.HOT, E.COLD, k))
        for a in range(8):
            ang = a * math.pi / 4
            E.arrow(d, 540 + (r - 20) * math.cos(ang), y + (r - 20) * math.sin(ang),
                    540 + (r + 20) * math.cos(ang), y + (r + 20) * math.sin(ang), E.WHITE, 4, 14)
        E.label(d, "MENOS PRESIÓN", 830, 380, 40, color=E.WHITE)
        E.label(d, "SE ENFRÍA", 830, 1080, 44, color=E.COLD)
        E.line(d, [(160, 1100), (160, 360)], E.SIL_D, 6)
        E.arrow(d, 160, 500, 160, 380, E.SIL_D, 6, 24)
    elif i == 4:  # cold air can't hold as much vapour
        parcel(E, d, 540, 720, 260, E.COLD)
        for k in range(26):
            a = k * 2.4 + u * 0.6
            r = 40 + (k * 37) % 210
            c = VAP if k < 16 else E.WHITE
            E.circle(d, 540 + r * math.cos(a), 720 + r * math.sin(a), 8, fill=c)
        E.label(d, "AIRE FRÍO", 540, 380, 52, color=E.COLD)
        E.label(d, "SOBRA VAPOR", 540, 1080, 48, color=E.WHITE)
    elif i == 5:  # condensation onto dust and salt
        for k, (x, y, nm) in enumerate(((330, 640, "POLVO"), (750, 640, "SAL"))):
            g = E.ease(u / (L * 0.8))
            E.circle(d, x, y, 60 + 80 * g, fill=E.mix(E.BG2, CLOUD, 0.85))
            E.rrect(d, x - 18, y - 18, x + 18, y + 18, 4, E.BRA_D if k == 0 else E.WHITE)
            for j in range(6):
                a = j * math.pi / 3 + u
                rr = 220 - 140 * ((u * 0.8 + j * 0.15) % 1.0)
                E.circle(d, x + rr * math.cos(a), y + rr * math.sin(a), 7, fill=VAP)
            E.label(d, nm, x, 920, 44, color=E.AMB)
        E.label(d, "GOTITAS", 540, 1060, 50, color=CLOUD)
    elif i == 6:  # millions of droplets = cloud
        ground(E, d); sun(E, d, 900, 330, 50)
        puff(E, d, 520, 620, 2.0)
        for k in range(40):
            x = 330 + (k * 47) % 400
            y = 560 + (k * 29) % 140
            E.circle(d, x, y, 4, fill=E.mix(CLOUD, VAP, 0.6))
        E.label(d, "MILLONES DE GOTITAS", 540, 960, 46, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.2, 0.8), ("whoosh", s[1] + 0.5, 0.8), ("pop", s[2] + 0.6), ("zip", s[3] + 0.5),
            ("click", s[4] + 0.6), ("pop", s[5] + 0.6), ("pop", s[6] + 0.6)]
