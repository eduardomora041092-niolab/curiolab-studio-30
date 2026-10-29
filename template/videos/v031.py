"""Video 031 — ¿Cómo convierte un altavoz electricidad en sonido?
Science: a dynamic loudspeaker has a cone (diaphragm) glued to a coil of wire (the voice coil) that sits next to a
permanent magnet. The audio signal is an electric current that keeps changing in strength and direction. Flowing
through the coil, it turns the coil into an electromagnet whose field interacts with the magnet's field, so the coil is
pushed and pulled back and forth. The coil drags the cone with it; the vibrating cone pushes the air and makes pressure
waves, which we hear as sound. (No powers, frequencies or impedances are claimed; other speaker types are not covered.)
"""
import math

ID = "031"
TITLE = "¿Cómo convierte un altavoz electricidad en sonido?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo convierte un altavoz electricidad en sonido?",
    "Detrás del cono hay una bobina de cable, justo al lado de un imán.",
    "Por ella pasa la corriente de la música, que cambia sin parar.",
    "Esa corriente convierte la bobina en un electroimán.",
    "El imán la empuja y la atrae, adelante y atrás, muy rápido.",
    "La bobina arrastra el cono, que vibra al mismo ritmo.",
    "El cono empuja el aire y crea ondas de sonido.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"altavoz", "electricidad", "sonido", "cono", "bobina", "cable", "imán", "corriente", "música",
            "electroimán", "empuja", "atrae", "vibra", "ritmo", "aire", "ondas"}

COPPER = (214, 128, 64)
CY = 720          # axis of the speaker
MAG_X0, MAG_X1 = 150, 330
COIL_X = 400      # rest position of the coil's left edge
CONE_X0, CONE_X1 = 470, 700

def speaker(E, d, dx=0.0, coil_hot=False, labels=False):
    # permanent magnet (N/S halves) and pole piece
    E.rrect(d, MAG_X0, CY - 140, MAG_X1, CY + 140, 14, E.HOT_D)
    E.rrect(d, MAG_X0 + 20, CY - 120, MAG_X1 - 20, CY + 120, 10, E.mix(E.HOT_D, E.BG1, 0.25))
    E.rrect(d, MAG_X1 - 4, CY - 34, COIL_X + 70, CY + 34, 8, E.SIL_D)
    # basket (frame) lines
    E.line(d, [(MAG_X1, CY - 150), (CONE_X1 + 10, 420)], E.MUTED, 4)
    E.line(d, [(MAG_X1, CY + 150), (CONE_X1 + 10, 1020)], E.MUTED, 4)
    # cone
    x0, x1 = CONE_X0 + dx, CONE_X1 + dx
    E.poly(d, [(x0, CY - 50), (x1, 440), (x1, 1000), (x0, CY + 50)], fill=E.SIL, outline=E.SIL_D, w=3)
    E.circle(d, x1, 440, 18, fill=E.SIL_D); E.circle(d, x1, 1000, 18, fill=E.SIL_D)
    E.circle(d, x1 - 10, CY, 40, fill=E.SIL_H)  # dust cap
    # voice coil wrapped around the pole, glued to the cone neck
    cx = COIL_X + dx
    col = E.mix(COPPER, E.AMB, 0.6) if coil_hot else COPPER
    E.rrect(d, cx, CY - 62, cx + 80, CY + 62, 10, col)
    for k in range(6):
        y = CY - 50 + k * 20
        E.line(d, [(cx + 4, y), (cx + 76, y)], E.mix(col, E.BG1, 0.45), 4)
    E.line(d, [(cx + 80, CY), (x0, CY)], E.SIL_D, 10)
    if labels:
        E.label(d, "IMÁN", (MAG_X0 + MAG_X1) / 2, CY - 210, 46, color=E.AMB)
        E.label(d, "BOBINA", cx + 40, CY + 190, 46, color=E.AMB)
        E.label(d, "CONO", 860, 520, 50, color=E.AMB)

def waves(E, d, u, dx=0.0, n=4, speed=1.2, strength=1.0):
    for k in range(n):
        f = (u * speed + k / n) % 1
        r = 60 + f * 300
        a = 0.75 - 0.25 * f
        pts = [(CONE_X1 + 30 + dx + r * math.cos(t), CY + r * 1.35 * math.sin(t)) for t in [-a + 2 * a * j / 20 for j in range(21)]]
        E.line(d, pts, E.mix(E.AMB, E.BG2, f * 0.8 + (1 - strength) * 0.5), 9 * (1 - 0.5 * f))

def signal(E, d, u, x0, y0, w, h=60):
    pts = [(x0 + w * j / 60, y0 - h * math.sin(j / 60 * 4 * math.pi + u * 6) * (0.6 + 0.4 * math.sin(j / 9 + u))) for j in range(61)]
    E.line(d, pts, E.COLD, 6)

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: cone already vibrating and sending out sound waves
        dx = 22 * math.sin(u * 2 * math.pi * 3.2)
        speaker(E, d, dx, coil_hot=True)
        waves(E, d, u, dx * 0.3, n=5, speed=1.4)
        for k in range(3):
            f = (u * 0.5 + k / 3) % 1
            x, y = 820 + 140 * f, 1080 - 640 * f - 60 * k
            E.circle(d, x, y, 18, fill=E.WHITE); E.line(d, [(x + 16, y), (x + 16, y - 60)], E.WHITE, 6)
        E.pill(d, "SONIDO", 880, 330, 44)
    elif i == 1:  # coil of wire next to a magnet, behind the cone
        speaker(E, d, 0, labels=E.ease(u / (L * 0.4)) > 0.2)
    elif i == 2:  # changing current from the music runs through the coil
        speaker(E, d, 0)
        cx = COIL_X + 40
        E.line(d, [(cx, CY + 62), (cx, 1080), (140, 1080)], E.COLD, 6)
        E.line(d, [(cx + 30, CY + 62), (cx + 30, 1120), (140, 1120)], E.COLD, 6)
        E.rrect(d, 60, 1040, 150, 1160, 14, E.BLUE)
        signal(E, d, u, 560, 1100, 420, 50)
        sgn = 1 if math.sin(u * 2 * math.pi * 0.9) > 0 else -1
        for k in range(6):
            f = ((u * 0.9 * sgn) + k / 6) % 1
            E.circle(d, 150 + f * (cx - 150), 1080, 10, fill=E.AMB)
        E.label(d, "CORRIENTE", 770, 990, 50, color=E.AMB)
        E.label(d, "MÚSICA", 105, 990, 40, color=E.COLD)
    elif i == 3:  # the current turns the coil into an electromagnet
        speaker(E, d, 0, coil_hot=True)
        cx = COIL_X + 40
        k = E.ease(u / (L * 0.5))
        for j, r in enumerate((95, 145, 195)):
            rr = r * k
            if rr > 10:
                pts = [(cx + rr * 0.8 * math.cos(t), CY + rr * math.sin(t)) for t in [2 * math.pi * s / 40 for s in range(41)]]
                E.line(d, pts, E.mix(E.AMB, E.BG2, j * 0.3), 5)
        flip = int(u * 1.6) % 2
        E.label(d, "N" if flip else "S", cx - 10, CY - 100, 44, color=E.WHITE)
        E.label(d, "S" if flip else "N", cx + 95, CY - 100, 44, color=E.WHITE)
        E.label(d, "ELECTROIMÁN", 540, 1150, 52, color=E.AMB)
    elif i == 4:  # the magnet pushes and pulls the coil, back and forth
        s = math.sin(u * 2 * math.pi * 0.8)
        dx = 34 * s
        speaker(E, d, dx, coil_hot=True)
        cx = COIL_X + dx + 40
        if s > 0:
            E.arrow(d, cx + 10, CY - 120, cx + 130, CY - 120, E.AMB, 10, 34); E.label(d, "EMPUJA", cx + 70, CY - 190, 46)
        else:
            E.arrow(d, cx + 70, CY - 120, cx - 50, CY - 120, E.COLD, 10, 34); E.label(d, "ATRAE", cx + 10, CY - 190, 46, color=E.COLD)
        E.label(d, "ADELANTE Y ATRÁS", 540, 1150, 48, color=E.WHITE)
    elif i == 5:  # the coil drags the cone, which vibrates at the same rhythm
        s = math.sin(u * 2 * math.pi * 1.4)
        dx = 30 * s
        speaker(E, d, dx, coil_hot=True)
        E.arrow(d, 780, 380, 680, 380, E.AMB, 8, 28); E.arrow(d, 800, 380, 900, 380, E.AMB, 8, 28)
        signal(E, d, u * 1.4, 560, 1110, 420, 40)
        E.label(d, "VIBRA", 860, 1020, 54, color=E.AMB)
    elif i == 6:  # the cone pushes the air: sound waves
        dx = 22 * math.sin(u * 2 * math.pi * 2.5)
        speaker(E, d, dx, coil_hot=True)
        for k in range(5):   # air molecules bunching in compressions
            f = (u * 0.9 + k / 5) % 1
            x = CONE_X1 + 60 + f * 280
            for j in range(9):
                E.circle(d, x + 10 * math.sin(j * 1.7), 470 + j * 62, 8, fill=E.mix(E.WHITE, E.BG2, f * 0.7))
        waves(E, d, u, dx * 0.3, n=4, speed=0.9)
        E.label(d, "ONDAS DE SONIDO", 540, 1150, 52, color=E.AMB)
        E.label(d, "AIRE", 960, 330, 44, color=E.WHITE)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.05, 1.0), ("click", s[1] + 0.6), ("zip", s[2] + 0.4, 1.0), ("pop", s[3] + 0.8),
            ("whoosh", s[4] + 0.3, 0.8), ("click", s[5] + 0.7), ("whoosh", s[6] + 0.3, 1.2)]
