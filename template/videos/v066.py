"""Video 066 — ¿Por qué brillan los ojos de los gatos en la oscuridad?
Science: cats' eyes do not make light; they reflect it. Behind the retina, cats (like many nocturnal animals) have a
reflective layer of tissue called the tapetum lucidum. Light that enters the eye and passes through the retina
without being absorbed is reflected back by this layer, so it passes through the light-sensitive cells of the retina
a second time. This gives the photoreceptors a second chance to detect it and improves vision in dim light. Some of
the reflected light leaves the eye again through the pupil, and that is the "eyeshine" we see when a torch or headlight
shines on a cat at night. Humans lack a tapetum lucidum.
(No colours of eyeshine, percentages of light or comparisons in numbers are claimed.)
"""
import math

ID = "066"
TITLE = "¿Por qué brillan los ojos de los gatos en la oscuridad?"
SUBTITLE = "CIENCIA EN 30 SEGUNDOS"
LINES = [
    "¿Por qué brillan los ojos de los gatos en la oscuridad?",
    "No producen luz propia: solo reflejan la que les llega.",
    "Detrás de la retina tienen una capa que funciona como un espejo.",
    "Se llama tapetum lucidum.",
    "La luz atraviesa la retina y esa capa la devuelve.",
    "Así la retina capta la luz dos veces y ve mejor de noche.",
    "Parte de esa luz sale del ojo, y por eso lo vemos brillar.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"brillan", "ojos", "gatos", "oscuridad", "producen", "luz", "propia", "reflejan", "llega", "retina", "capa",
            "espejo", "tapetum", "lucidum", "atraviesa", "devuelve", "dos", "veces", "noche", "sale",
            "ojo", "brillar"}

LIGHT = (255, 230, 120)
GLOW = (190, 255, 140)
FUR = (70, 74, 90)
RET = (220, 90, 110)
TAP = (120, 230, 200)
EYEC = (40, 50, 75)

# cross-section of an eye: light enters from the left through the pupil, retina + tapetum on the back (right)
CX, CY, R = 520, 720, 300


def cat_face(E, d, cx, cy, glow):
    E.poly(d, [(cx - 260, cy - 120), (cx - 200, cy - 330), (cx - 90, cy - 200)], fill=FUR)
    E.poly(d, [(cx + 260, cy - 120), (cx + 200, cy - 330), (cx + 90, cy - 200)], fill=FUR)
    E.circle(d, cx, cy, 270, fill=FUR)
    for sx in (-1, 1):
        ex = cx + sx * 110
        if glow > 0:
            E.circle(d, ex, cy - 30, 80 + 20 * glow, fill=E.mix(FUR, GLOW, 0.35 * glow))
        E.circle(d, ex, cy - 30, 62, fill=E.mix((20, 25, 35), GLOW, glow))
        E.rrect(d, ex - 10, cy - 80, ex + 10, cy + 20, 8, (15, 18, 26))
    E.poly(d, [(cx - 22, cy + 70), (cx + 22, cy + 70), (cx, cy + 95)], fill=(200, 120, 140))


def eye_section(E, d, tapetum=True, labels=False):
    E.circle(d, CX, CY, R, fill=EYEC, outline=E.SIL, w=5)
    # retina along the back wall (right side arc)
    pts = [(CX + (R - 18) * math.cos(a / 30 * math.pi - math.pi / 2), CY + (R - 18) * math.sin(a / 30 * math.pi - math.pi / 2))
           for a in range(31)]
    if tapetum:
        tp = [(CX + (R - 4) * math.cos(a / 30 * math.pi - math.pi / 2), CY + (R - 4) * math.sin(a / 30 * math.pi - math.pi / 2))
              for a in range(31)]
        E.line(d, tp, TAP, 12)
    E.line(d, pts, RET, 12)
    # pupil / lens on the left
    E.rrect(d, CX - R - 14, CY - 70, CX - R + 14, CY + 70, 8, (15, 18, 26))
    E.circle(d, CX - R + 70, CY, 55, fill=(150, 170, 200), outline=E.SIL_H, w=3)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: torch beam sweeping, cat eyes glowing
        g = 0.6 + 0.4 * abs(math.sin(u * 3))
        cat_face(E, d, 540, 780, g)
        ax = 190 + 50 * math.sin(u * 2)
        E.poly(d, [(ax, 320), (ax + 40, 300), (500, 650), (380, 760)], fill=E.mix((11, 18, 32), LIGHT, 0.25))
        E.rrect(d, ax - 70, 290, ax + 40, 350, 14, E.SIL, outline=E.SIL_H, w=3)
    elif i == 1:  # they reflect, not produce
        cat_face(E, d, 540, 820, 0.8)
        E.wave(d, 100, 400, 420, 760, 50, 10, LIGHT, 5, phase=u * 8)
        E.wave(d, 650, 760, 980, 420, 50, 10, GLOW, 5, phase=u * 8)
        E.label(d, "REFLEJA", 860, 360, 48, color=GLOW)
        E.label(d, "LUZ", 140, 340, 48, color=LIGHT)
    elif i == 2:  # layer behind the retina like a mirror
        k = E.ease(u / 0.8)
        E.circle(d, CX, CY, R, fill=EYEC, outline=E.SIL, w=5)
        pts = [(CX + (R - 18) * math.cos(a / 30 * math.pi - math.pi / 2), CY + (R - 18) * math.sin(a / 30 * math.pi - math.pi / 2))
               for a in range(31)]
        E.line(d, pts, RET, 12)
        if k > 0.1:
            n = max(2, int(31 * k))
            tp = [(CX + (R - 4) * math.cos(a / 30 * math.pi - math.pi / 2), CY + (R - 4) * math.sin(a / 30 * math.pi - math.pi / 2))
                  for a in range(n)]
            E.line(d, tp, TAP, 12)
        E.rrect(d, CX - R - 14, CY - 70, CX - R + 14, CY + 70, 8, (15, 18, 26))
        E.label(d, "RETINA", 660, 1080, 44, color=RET)
        E.label(d, "ESPEJO", 920, 360, 46, color=TAP)
        E.arrow(d, 920, 400, CX + 230, CY - 180, TAP, 6, 22)
    elif i == 3:  # name: tapetum lucidum
        eye_section(E, d)
        E.pill(d, "TAPETUM LUCIDUM", 540, 340, 48, bg=TAP)
        E.arrow(d, 780, 380, CX + 250, CY - 150, TAP, 6, 22)
    elif i == 4:  # light crosses retina, layer sends it back
        eye_section(E, d)
        f = min(1.0, u / (L * 0.5))
        x1 = CX - R + 20 + (2 * R - 30) * f
        E.wave(d, 60, CY - 20, x1, CY - 20, 50, 10, LIGHT, 5, phase=u * 8, head=f < 1)
        if f >= 1:
            g = min(1.0, (u - L * 0.5) / (L * 0.4))
            x2 = CX + R - 30 - (2 * R - 60) * g
            E.wave(d, CX + R - 30, CY + 30, x2, CY + 30, 50, 10, GLOW, 5, phase=u * 8)
        E.label(d, "IDA", 200, CY - 90, 42, color=LIGHT)
        E.label(d, "VUELTA", 540, CY + 130, 42, color=GLOW)
    elif i == 5:  # retina catches the light twice
        eye_section(E, d)
        E.wave(d, 60, CY - 20, CX + R - 30, CY - 20, 50, 10, LIGHT, 5, phase=u * 8, head=False)
        E.wave(d, CX + R - 30, CY + 30, CX - 100, CY + 30, 50, 10, GLOW, 5, phase=u * 8)
        p = abs(math.sin(u * 5))
        E.circle(d, CX + R - 18, CY - 20, 22 + 8 * p, outline=E.WHITE, w=4)
        E.circle(d, CX + R - 18, CY + 30, 22 + 8 * p, outline=E.WHITE, w=4)
        E.pill(d, "1", CX + R + 60, CY - 30, 40)
        E.pill(d, "2", CX + R + 60, CY + 40, 40)
        E.label(d, "VE MEJOR DE NOCHE", 540, 340, 48, color=E.AMB)
    elif i == 6:  # some light leaves the eye: we see the glow
        g = E.ease(u / 0.8)
        cat_face(E, d, 540, 780, g)
        for sx in (-1, 1):
            ex = 540 + sx * 110
            E.wave(d, ex, 700, ex + sx * 160, 380, 50, 8, GLOW, 5, phase=u * 8)
        E.label(d, "POR ESO BRILLAN", 540, 1110, 48, color=GLOW)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 0.8), ("pop", s[1] + 0.6), ("zip", s[2] + 0.4), ("pop", s[3] + 0.5),
            ("whoosh", s[4] + 0.5, 0.8), ("pop", s[5] + 0.9), ("click", s[6] + 0.6)]
