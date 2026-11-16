"""Video 085 — ¿Cómo funciona un secador de pelo?
Science: switching on a hair dryer powers a small electric motor that spins a fan. The fan draws air in through the
rear grille and pushes it along the barrel. Inside, the air passes over a heating element: a resistance wire (usually
nichrome) wound in a coil on an insulating support. The electric current heats the wire (Joule heating) until it glows
red; the air flowing past takes up that heat and leaves the nozzle hot. A thermal protector (bimetallic thermostat or
thermal fuse) cuts the current if the dryer overheats, for example when the inlet is blocked.
(No power ratings, air temperatures or speeds are claimed.)
"""
import math

ID = "085"
TITLE = "¿Cómo funciona un secador de pelo?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo saca aire caliente un secador en solo unos segundos?",
    "Al encenderlo, un pequeño motor hace girar un ventilador.",
    "El ventilador aspira aire por la rejilla de atrás.",
    "Ese aire pasa por una resistencia: un hilo enrollado en espiral.",
    "La corriente calienta el hilo hasta ponerlo al rojo.",
    "El aire se lleva ese calor y sale caliente por la boquilla.",
    "Si se recalienta, un protector térmico corta la corriente.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"aire", "caliente", "secador", "segundos", "motor", "ventilador", "aspira", "rejilla", "resistencia",
            "hilo", "espiral", "corriente", "calienta", "rojo", "calor", "boquilla", "recalienta", "protector",
            "térmico", "corta"}

BY0, BY1 = 560, 760          # barrel top / bottom
BX0, BX1 = 170, 860          # barrel left (grille) / right (start of nozzle)
NZ1 = 960                    # nozzle tip
CY = (BY0 + BY1) / 2
FANX = 270
MOT0, MOT1 = 300, 380
COIL0, COIL1 = 480, 790
BODY = (70, 86, 120)
BODY_D = (48, 60, 88)


def body(E, d, hl_grille=False):
    # handle
    E.poly(d, [(330, BY1 - 10), (450, BY1 - 10), (420, 1120), (300, 1120)], fill=BODY_D)
    E.rrect(d, 345, 860, 395, 930, 12, E.SIL_D)                        # switch
    # barrel shell (cut-away: dark interior)
    E.rrect(d, BX0 - 20, BY0 - 30, BX1, BY1 + 30, 50, BODY)
    E.rrect(d, BX0, BY0, BX1, BY1, 20, E.CAV)
    # nozzle
    E.poly(d, [(BX1, BY0 - 30), (NZ1, BY0 + 20), (NZ1, BY1 - 20), (BX1, BY1 + 30)], fill=BODY)
    E.poly(d, [(BX1, BY0), (NZ1 - 8, BY0 + 34), (NZ1 - 8, BY1 - 34), (BX1, BY1)], fill=E.CAV)
    # rear grille
    gc = E.AMB if hl_grille else E.SIL_D
    for k in range(7):
        y = BY0 - 10 + k * 37
        E.line(d, [(BX0 - 30, y), (BX0 - 6, y)], gc, 7)
    E.line(d, [(BX0 - 18, BY0 - 20), (BX0 - 18, BY1 + 20)], gc, 6)


def fan(E, d, phase, hl=False):
    c = E.AMB if hl else E.SIL
    for k in range(3):
        a = phase * 2 * math.pi + k * 2 * math.pi / 3
        h = 80 * math.cos(a)
        w = 16 * abs(math.sin(a)) + 5
        E.poly(d, [(FANX - w, CY), (FANX + w, CY), (FANX + w * 0.6, CY - h), (FANX - w * 0.6, CY - h)], fill=c)
    E.circle(d, FANX, CY, 14, fill=E.SIL_D)


def motor(E, d, hl=False):
    E.rrect(d, MOT0, CY - 42, MOT1, CY + 42, 14, E.AMB if hl else E.BRA_D)
    E.line(d, [(FANX, CY), (MOT0, CY)], E.SIL, 8)
    for k in range(4):
        x = MOT0 + 14 + k * 18
        E.line(d, [(x, CY - 30), (x, CY + 30)], E.mix(E.BRA_D, E.BG1, 0.4), 4)


def coil(E, d, heat=0.0, hl=False):
    # insulating support
    E.rrect(d, COIL0 - 10, CY - 6, COIL1 + 10, CY + 6, 4, (190, 180, 160))
    col = E.mix(E.SIL_D, E.HOT, heat)
    if hl:
        col = E.mix(E.AMB, E.HOT, heat)
    n = 13
    for k in range(n):
        x = COIL0 + (COIL1 - COIL0) * k / n
        x2 = x + (COIL1 - COIL0) / n
        E.line(d, [(x, CY - 62), (x2, CY + 62)], col, 7)
        E.line(d, [(x2, CY + 62), (x2, CY - 62)], E.mix(col, E.BG1, 0.35), 6)
    if heat > 0.5:
        for k in range(n):
            x = COIL0 + (COIL1 - COIL0) * (k + 0.5) / n
            E.circle(d, x, CY, 5, fill=(255, 210, 120))


def air(E, d, u, heat=1.0, speed=1.0, stop_at=None, n=34):
    """Air parcels: enter at the rear grille, cold (blue) until the coil, hot (red) after it."""
    for j in range(n):
        q = (u * 0.42 * speed + j / n) % 1.0
        x = 40 + q * (1040 - 40)
        lane = ((j * 37) % 5) - 2
        y = CY + lane * 34
        if x > BX1:
            y = CY + lane * 34 * (1 - 0.35 * (x - BX1) / (NZ1 - BX1)) if x < NZ1 else CY + lane * 22
        if stop_at is not None and x > stop_at:
            continue
        t = 0.0 if x < COIL0 else (min(1.0, (x - COIL0) / (COIL1 - COIL0)) * heat)
        col = E.mix(E.COLD, E.HOT, t)
        E.circle(d, x, y, 7, fill=col)


def protector(E, d, hl=False, tripped=False):
    x, y = 640, BY0 + 6
    E.rrect(d, x - 34, y - 2, x + 34, y + 22, 6, E.AMB if hl else E.SIL_D)
    # wire from switch along handle to coil, via the protector
    wc = E.AMB if hl else E.MUTED
    E.line(d, [(370, 860), (430, BY1 + 6)], wc, 4)
    E.line(d, [(430, BY1 + 6), (470, BY1 - 8)], wc, 4)
    if tripped:
        E.line(d, [(x - 34, y + 10), (x - 70, y + 10)], wc, 4)
        E.line(d, [(x + 34, y + 10), (x + 52, y - 12)], wc, 4)
    else:
        E.line(d, [(x - 34, y + 10), (x + 34, y + 10)], wc, 4)


def scene(i, u, L, E, im, d):
    ph = u * 3.0
    if i == 0:  # in action from frame 0: fan spinning, coil red, cold air in, hot air out
        body(E, d)
        coil(E, d, heat=1.0)
        motor(E, d)
        fan(E, d, ph)
        air(E, d, u + 0.6)
        E.label(d, "FRÍO", 120, 470, 44, color=E.COLD)
        E.label(d, "CALIENTE", 920, 470, 44, color=E.HOT)
    elif i == 1:  # switch on: motor turns the fan
        body(E, d)
        coil(E, d, heat=0.0)
        motor(E, d, hl=True)
        fan(E, d, ph * E.ease(u / 0.8), hl=True)
        E.label(d, "MOTOR", 340, 400, 46, color=E.AMB)
        E.arrow(d, 340, 430, 340, 600, E.AMB, 5, 20)
        E.label(d, "VENTILADOR", 230, 860, 40, color=E.AMB)
        E.arrow(d, 230, 830, 262, 730, E.AMB, 5, 20)
    elif i == 2:  # fan draws air in through the rear grille
        body(E, d, hl_grille=True)
        coil(E, d, heat=0.0)
        motor(E, d)
        fan(E, d, ph)
        air(E, d, u, heat=0.0, stop_at=COIL0)
        E.label(d, "REJILLA", 160, 420, 44, color=E.AMB)
        E.label(d, "ENTRA AIRE", 150, 880, 42, color=E.COLD)
        E.arrow(d, 150, 850, 150, 790, E.COLD, 6, 22)
    elif i == 3:  # air passes a resistance: a coiled wire
        body(E, d)
        coil(E, d, heat=0.0, hl=True)
        motor(E, d)
        fan(E, d, ph)
        air(E, d, u, heat=0.0)
        E.label(d, "RESISTENCIA", 635, 430, 44, color=E.AMB)
        E.arrow(d, 635, 460, 635, 580, E.AMB, 5, 20)
        E.label(d, "HILO EN ESPIRAL", 635, 880, 40, color=E.WHITE)
    elif i == 4:  # current heats the wire until it glows red
        body(E, d)
        h = E.ease(u / (L * 0.7))
        coil(E, d, heat=h)
        motor(E, d)
        fan(E, d, ph)
        E.label(d, "CORRIENTE", 300, 1010, 40, color=E.AMB)
        E.arrow(d, 400, 960, 470, 790, E.AMB, 6, 22)
        E.label(d, "AL ROJO", 635, 430, 50, color=E.HOT)
    elif i == 5:  # the air takes the heat and leaves the nozzle hot
        body(E, d)
        coil(E, d, heat=1.0)
        motor(E, d)
        fan(E, d, ph)
        air(E, d, u, heat=1.0, speed=1.3)
        E.label(d, "BOQUILLA", 920, 450, 42, color=E.AMB)
        E.arrow(d, 920, 480, 915, 560, E.AMB, 5, 20)
        E.label(d, "SALE CALIENTE", 760, 900, 42, color=E.HOT)
    elif i == 6:  # overheating: the thermal protector cuts the current
        trip = u > L * 0.35
        body(E, d)
        coil(E, d, heat=1.0 if not trip else max(0.0, 1.0 - (u - L * 0.35) / (L * 0.5)))
        motor(E, d)
        fan(E, d, ph if not trip else ph * 0.2)
        protector(E, d, hl=True, tripped=trip)
        E.label(d, "PROTECTOR", 640, 380, 44, color=E.AMB)
        E.label(d, "TÉRMICO", 640, 430, 44, color=E.AMB)
        E.arrow(d, 640, 460, 640, 552, E.AMB, 5, 20)
        if trip:
            E.cross(d, 590, BY0 + 16, 22, E.HOT, 8)
            E.label(d, "CORTA", 640, 900, 50, color=E.HOT)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.2, 0.8), ("click", s[1] + 0.3), ("whoosh", s[2] + 0.4, 0.8), ("pop", s[3] + 0.6),
            ("zip", s[4] + 0.4), ("whoosh", s[5] + 0.4, 0.8), ("click", s[6] + 1.0)]
