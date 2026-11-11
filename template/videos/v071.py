"""Video 071 — ¿Cómo sabe una puerta automática que llegas?
Science: an automatic sliding door has a sensor mounted above the doorway that watches the approach area. Many opening
sensors are active: they send out invisible waves (microwave radar or active infrared) towards the area in front of the
door and analyse what is reflected back. When a person walks in, the reflected waves change (for radar, a Doppler shift
caused by the movement); the sensor detects the change and signals the door controller. The controller runs an
electric motor that drives a toothed belt, and the belt slides the door leaves apart. Separate safety/presence sensors
check that nobody is standing in the doorway before the door is allowed to close.
(No frequencies, ranges or timings are claimed; other sensor types such as pressure mats or passive infrared exist.)
"""
import math

ID = "071"
TITLE = "¿Cómo sabe una puerta automática que llegas?"
SUBTITLE = "CÓMO FUNCIONA"
LINES = [
    "¿Cómo sabe una puerta automática que te acercas?",
    "Encima de la puerta hay un sensor que vigila la entrada.",
    "Muchos envían ondas invisibles, de radio o infrarrojas, hacia delante.",
    "Cuando caminas, las ondas rebotan en ti y vuelven cambiadas.",
    "El sensor nota ese cambio y avisa al controlador de la puerta.",
    "Un motor mueve una correa que desliza las hojas hacia los lados.",
    "Otro sensor comprueba que no hay nadie en medio antes de cerrar.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"puerta", "automática", "acercas", "sensor", "vigila", "entrada", "ondas", "invisibles", "radio",
            "infrarrojas", "caminas", "rebotan", "cambiadas", "cambio", "avisa", "controlador", "motor", "correa",
            "desliza", "hojas", "lados", "nadie", "cerrar"}

GLASS = (120, 180, 230)
GLASS_D = (70, 120, 170)
WAVE = (120, 230, 200)
FX0, FX1, FY0, FY1 = 170, 910, 420, 1150   # door opening


def frame_(E, d):
    E.rrect(d, FX0 - 30, FY0 - 90, FX1 + 30, FY0, 10, E.SIL_D)          # header box (motor housing)
    E.rrect(d, FX0 - 30, FY0, FX0, FY1, 0, E.SIL_D)
    E.rrect(d, FX1, FY0, FX1 + 30, FY1, 0, E.SIL_D)


def sensor(E, d, glow=0.0):
    E.rrect(d, 480, 300, 600, 340, 12, E.mix(E.SIL, E.AMB, glow), outline=E.SIL_H, w=2)
    E.circle(d, 540, 320, 9, fill=E.HOT if glow > 0.3 else E.BG1)


def leaves(E, d, open_=0.0):
    mid = (FX0 + FX1) / 2; half = (FX1 - FX0) / 2
    s = half * 0.9 * open_
    E.rrect(d, FX0 - s, FY0 + 6, mid - s, FY1, 4, GLASS_D, outline=GLASS, w=4)
    E.rrect(d, mid + s, FY0 + 6, FX1 + s, FY1, 4, GLASS_D, outline=GLASS, w=4)
    # cover leaves sliding behind the wall: redraw side walls on top
    E.rrect(d, 0, FY0, FX0, FY1, 0, E.BG2)
    E.rrect(d, FX1, FY0, 1080, FY1, 0, E.BG2)
    E.rrect(d, FX0 - 30, FY0, FX0, FY1, 0, E.SIL_D)
    E.rrect(d, FX1, FY0, FX1 + 30, FY1, 0, E.SIL_D)


def person(E, d, x, y, s=1.0, ph=0.0):
    E.circle(d, x, y - 210 * s, 42 * s, fill=E.BRA)
    E.rrect(d, x - 48 * s, y - 165 * s, x + 48 * s, y - 20 * s, 24 * s, E.AMB)
    sw = 30 * s * math.sin(ph)
    E.line(d, [(x - 18 * s, y - 25 * s), (x - 18 * s + sw, y + 80 * s)], E.AMB, 22 * s)
    E.line(d, [(x + 18 * s, y - 25 * s), (x + 18 * s - sw, y + 80 * s)], E.AMB, 22 * s)


def arcs(E, d, u, color, n=4, up=False):
    for k in range(n):
        r = 60 + ((k * 90 + u * 220) % 360)
        if up:
            r = 420 - ((k * 90 + u * 220) % 360)
        bb = E.P(540 - r, 340 - r, 540 + r, 340 + r)
        d.arc(bb, 40, 140, fill=color, width=6 * E.S)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: person walking in, doors already sliding open, sensor waves
        k = min(1.0, 0.25 + u / (L * 0.8))
        leaves(E, d, E.ease(k))
        frame_(E, d)
        sensor(E, d, 0.8)
        arcs(E, d, u, WAVE)
        person(E, d, 540, 1080 - 120 * k, 1.0 - 0.25 * k, u * 8)
    elif i == 1:  # sensor above the door watching the entrance
        leaves(E, d, 0.0)
        frame_(E, d)
        g = 0.5 + 0.5 * math.sin(u * 5)
        sensor(E, d, g)
        E.circle(d, 540, 320, 70 + 10 * g, outline=E.AMB, w=5)
        E.label(d, "SENSOR", 540, 520, 56, color=E.AMB)
        E.poly(d, [(540, 345), (230, 1100), (850, 1100)], outline=E.mix(E.BG2, E.AMB, 0.6), w=3)
    elif i == 2:  # invisible waves sent forward
        leaves(E, d, 0.0)
        frame_(E, d)
        sensor(E, d, 0.6)
        arcs(E, d, u, WAVE, 5)
        E.label(d, "ONDAS INVISIBLES", 540, 1090, 50, color=WAVE)
    elif i == 3:  # waves bounce off the walking person and come back changed
        leaves(E, d, 0.0)
        frame_(E, d)
        sensor(E, d, 0.6)
        arcs(E, d, u, WAVE, 3)
        px = 540
        person(E, d, px, 1080, 0.85, u * 8)
        for k in range(3):
            yy = 820 - ((k * 140 + u * 300) % 420)
            E.arrow(d, px + 90, yy + 90, px + 90, yy, E.AMB, 9, 30)
        E.label(d, "REBOTAN EN TI", 330, 700, 46, color=E.AMB)
    elif i == 4:  # sensor detects change, signals controller
        leaves(E, d, 0.0)
        frame_(E, d)
        f = abs(math.sin(u * 6))
        sensor(E, d, f)
        E.rrect(d, 700, 520, 940, 680, 18, E.BLUE_D, outline=E.COLD, w=4)
        E.label(d, "CONTROL", 820, 600, 40, color=E.WHITE)
        p = (u * 1.5) % 1.0
        E.line(d, [(600, 320), (820, 320), (820, 520)], E.COLD, 6)
        x = 600 + 220 * min(1, p * 2) if p < 0.5 else 820
        y = 320 if p < 0.5 else 320 + 200 * (p - 0.5) * 2
        E.circle(d, x, y, 16, fill=E.AMB)
        person(E, d, 360, 1080, 0.85, u * 8)
        E.label(d, "¡CAMBIO!", 300, 520, 50, color=E.AMB)
    elif i == 5:  # motor drives a belt that slides the leaves apart
        k = E.ease(u / (L * 0.8))
        leaves(E, d, k)
        frame_(E, d)
        # belt loop in the header and motor
        E.rrect(d, 200, 345, 880, 395, 25, None, outline=E.BG1, w=8)
        for j in range(12):
            xx = 220 + ((j * 56 + u * 200) % 640)
            E.rrect(d, xx - 10, 341, xx + 10, 351, 3, E.BG1)
        E.circle(d, 880, 370, 36, fill=E.HOT, outline=E.SIL_H, w=3)
        E.label(d, "MOTOR", 880, 470, 42, color=E.HOT)
        E.label(d, "CORREA", 420, 470, 42, color=E.SIL_H)
        E.arrow(d, 400, 800, 230, 800, E.AMB, 9, 30)
        E.arrow(d, 680, 800, 850, 800, E.AMB, 9, 30)
    elif i == 6:  # safety sensor: person in the doorway, doors stay open
        leaves(E, d, 1.0)
        frame_(E, d)
        sensor(E, d, 0.3)
        person(E, d, 540, 1080, 1.0, 0.0)
        on = math.sin(u * 8) > 0
        E.line(d, [(FX0 + 10, 900), (FX1 - 10, 900)], E.HOT if on else E.mix(E.HOT, E.BG1, 0.5), 6)
        E.label(d, "NADIE EN MEDIO", 540, 520, 50, color=E.HOT)
        E.cross(d, 840, 640, 34, E.HOT, 10)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.2, 0.8), ("pop", s[1] + 0.5), ("zip", s[2] + 0.5), ("pop", s[3] + 0.6),
            ("click", s[4] + 0.6), ("whoosh", s[5] + 0.5, 0.8), ("click", s[6] + 0.6)]
