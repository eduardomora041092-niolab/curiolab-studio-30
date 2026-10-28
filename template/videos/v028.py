"""Video 028 — ¿Cómo detecta el humo un detector?
Science: an optical (photoelectric) smoke alarm has a dark chamber with a light source (an LED) and a light sensor
(a photodiode). They are placed at an angle so that, in clean air, the beam goes straight past and no light reaches
the sensor. When smoke enters the chamber, its particles scatter part of the light in other directions, and some of it
reaches the sensor. The sensor turns that light into an electrical signal; when the signal passes a set threshold,
the circuit sounds the alarm. (No angles, wavelengths or sensitivities are claimed; ionisation alarms are not covered.)
"""
import math

ID = "028"
TITLE = "¿Cómo detecta el humo un detector?"
LINES = [
    "¿Cómo detecta el humo tu detector sin ojos?",
    "Dentro tiene una cámara oscura con una luz y un sensor.",
    "La luz y el sensor no se miran: están en ángulo.",
    "Con aire limpio, la luz sigue recta y nunca llega al sensor.",
    "Cuando entra humo, sus partículas desvían parte de la luz.",
    "Esa luz desviada llega al sensor, que avisa al circuito.",
    "Si la señal supera un límite fijado, suena la alarma.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"humo", "detector", "ojos", "cámara", "oscura", "luz", "sensor", "ángulo", "limpio", "recta",
            "partículas", "desvían", "desviada", "circuito", "señal", "límite", "alarma"}

SMOKE = (150, 155, 165)
CEIL = (60, 72, 98)
# chamber geometry (cross-section)
CX0, CY0, CX1, CY1 = 130, 420, 950, 1110
LED = (230, 640)
ABS_X = 880
SEN = (640, 1010)
SCAT = (640, 640)

def detector_body(E, d, x, y, blink):
    E.rrect(d, x - 150, y - 26, x + 150, y + 26, 20, E.SIL)
    E.rrect(d, x - 110, y + 20, x + 110, y + 60, 18, E.SIL_D)
    E.circle(d, x + 70, y + 40, 9, fill=E.HOT if blink else E.HOT_D)

def puff(E, d, x, y, r, c=SMOKE):
    for dx, dy, k in ((-0.5, 0.1, 0.7), (0.45, 0.15, 0.75), (0, -0.25, 0.85), (0, 0.2, 0.9)):
        E.circle(d, x + dx * r, y + dy * r, r * k, fill=c)

def chamber(E, d, beam=True, beam_len=1.0):
    E.rrect(d, CX0, CY0, CX1, CY1, 40, E.CAV, outline=E.SIL_D, w=6)
    # labyrinth vanes on the walls (let smoke in, keep outside light out)
    for k in range(6):
        x = CX0 + 70 + k * 135
        E.line(d, [(x, CY0 + 6), (x + 40, CY0 + 50)], E.SIL_D, 8)
    # light absorber at the end of the beam
    E.rrect(d, ABS_X, 580, ABS_X + 40, 700, 8, (40, 40, 48))
    # LED
    E.rrect(d, LED[0] - 70, LED[1] - 34, LED[0] - 10, LED[1] + 34, 10, E.SIL_D)
    E.circle(d, LED[0], LED[1], 34, fill=(255, 220, 120) if beam else (120, 100, 60))
    # sensor (photodiode) looking up, below the beam
    E.rrect(d, SEN[0] - 50, SEN[1], SEN[0] + 50, SEN[1] + 60, 10, E.SIL_D)
    if beam:
        x1 = LED[0] + 36 + (ABS_X - LED[0] - 36) * beam_len
        E.line(d, [(LED[0] + 36, LED[1]), (x1, LED[1])], (255, 230, 140), 18)

def sensor_cap(E, d, lit):
    E.poly(d, [(SEN[0] - 42, SEN[1] + 4), (SEN[0] + 42, SEN[1] + 4), (SEN[0], SEN[1] - 40)],
           fill=E.AMB if lit else (70, 80, 100))

def particles(E, d, u, n=14, seed=3):
    pts = []
    for k in range(n):
        a = (k * 2.399 + seed) % (2 * math.pi)
        x = SCAT[0] + 170 * math.cos(a + u * 0.25) * (0.3 + 0.7 * ((k * 37) % 10) / 10)
        y = SCAT[1] + 110 * math.sin(a * 1.3 + u * 0.3) * (0.3 + 0.7 * ((k * 53) % 10) / 10)
        E.circle(d, x, y, 9, fill=SMOKE)
        pts.append((x, y))
    return pts

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: smoke from a pan is already rising to the ceiling detector
        E.rrect(d, 330, 1080, 750, 1110, 10, E.SIL_D)  # hob
        E.poly(d, [(360, 1010), (720, 1010), (690, 1070), (390, 1070)], fill=(60, 60, 70))  # pan
        E.line(d, [(720, 1030), (900, 1010)], (60, 60, 70), 22)
        for k in range(7):
            f = (u * 0.45 + k / 7) % 1
            x = 540 + 90 * math.sin(f * 6 + k) * (1 - f)
            puff(E, d, x, 990 - 520 * f, 40 + 50 * f, c=E.mix(SMOKE, E.BG2, f * 0.6))
        E.rrect(d, 40, 300, 1040, 330, 6, CEIL)
        detector_body(E, d, 540, 356, int(u * 3) % 2 == 0)
        E.pill(d, "HUMO", 860, 760, 44)
    elif i == 1:  # dark chamber with a light and a sensor
        chamber(E, d, beam=False)
        sensor_cap(E, d, False)
        k = E.ease(u / (L * 0.5))
        if k > 0.1:
            E.label(d, "LUZ", LED[0], 520, 50, color=E.AMB)
            E.label(d, "SENSOR", SEN[0], 900, 50, color=E.AMB)
        E.label(d, "CÁMARA OSCURA", 540, 1160, 46, color=E.WHITE)
    elif i == 2:  # light and sensor at an angle: they don't face each other
        chamber(E, d, beam=False)
        sensor_cap(E, d, False)
        E.line(d, [(LED[0] + 40, LED[1]), (ABS_X - 20, LED[1])], E.MUTED, 4)
        E.line(d, [(SEN[0], SEN[1] - 50), (SEN[0], LED[1] + 40)], E.MUTED, 4)
        r = 70 * E.ease(u / (L * 0.6))
        if r > 5:
            pts = [(SEN[0] + r * math.cos(a), LED[1] + r * math.sin(a)) for a in [math.pi / 2 * t / 12 for t in range(13)]]
            E.line(d, pts, E.AMB, 6)
        E.label(d, "EN ÁNGULO", 540, 1160, 50, color=E.AMB)
    elif i == 3:  # clean air: the beam goes straight, the sensor gets nothing
        chamber(E, d, beam=True, beam_len=min(1.0, u / (L * 0.4)))
        sensor_cap(E, d, False)
        E.cross(d, SEN[0] + 120, SEN[1] - 10, 30)
        E.label(d, "AIRE LIMPIO", 540, 1160, 50, color=E.AMB)
    elif i == 4:  # smoke enters: particles scatter part of the light
        chamber(E, d)
        sensor_cap(E, d, False)
        pts = particles(E, d, u)
        k = E.ease(u / (L * 0.5))
        for j, (x, y) in enumerate(pts):
            if abs(y - LED[1]) < 40 and k > 0.2:
                for a in (-2.4, -1.2, 0.6, 2.0):
                    a2 = a + j * 0.3
                    E.line(d, [(x, y), (x + 70 * k * math.cos(a2), y + 70 * k * math.sin(a2))], (255, 230, 140), 4)
        for k2 in range(4):
            f = (u * 0.5 + k2 / 4) % 1
            puff(E, d, 300 + 140 * k2, CY0 - 20 + 120 * f, 26, c=E.mix(SMOKE, E.BG1, 0.3))
        E.label(d, "PARTÍCULAS DE HUMO", 540, 1160, 46, color=E.AMB)
    elif i == 5:  # scattered light reaches the sensor, which signals the circuit
        chamber(E, d)
        particles(E, d, u)
        t = min(1.0, u / (L * 0.35))
        E.line(d, [SCAT, (SCAT[0], SCAT[1] + (SEN[1] - 50 - SCAT[1]) * t)], (255, 230, 140), 8)
        lit = t >= 1.0
        sensor_cap(E, d, lit)
        if lit:
            E.line(d, [(SEN[0] + 50, SEN[1] + 30), (840, SEN[1] + 30), (840, 900)], E.AMB, 8)
            E.rrect(d, 760, 790, 920, 900, 14, E.BLUE)
            E.label(d, "CHIP", 840, 845, 36, color=E.WHITE)
        E.label(d, "SEÑAL", 540, 1160, 50, color=E.AMB)
    elif i == 6:  # signal above the threshold -> alarm
        detector_body(E, d, 540, 380, True)
        level = E.ease(u / (L * 0.6))
        E.rrect(d, 300, 560, 380, 1060, 16, E.CAV, outline=E.SIL_D, w=4)
        h = 480 * level
        E.rrect(d, 308, 1052 - h, 372, 1052, 12, E.HOT if level > 0.6 else E.AMB)
        E.line(d, [(270, 770), (420, 770)], E.WHITE, 6)
        E.label(d, "LÍMITE", 520, 770, 40, color=E.WHITE)
        if level > 0.6:
            for k in range(3):
                r = 60 + ((u * 1.6 + k / 3) % 1) * 200
                pts = [(540 + r * math.cos(a), 400 + r * math.sin(a)) for a in [0.2 + 0.1 * j for j in range(11)]]
                E.line(d, pts, E.AMB, 7)
            E.label(d, "¡ALARMA!", 740, 940, 70, color=E.HOT)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.05, 1.2), ("click", s[1] + 0.6), ("pop", s[2] + 0.8), ("whoosh", s[3] + 0.2, 1.0),
            ("whoosh", s[4] + 0.4, 1.2), ("pop", s[5] + 0.9), ("click", s[6] + 1.0)]
