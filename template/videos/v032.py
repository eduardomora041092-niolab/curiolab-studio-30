"""Video 032 — ¿Cómo convierte un micrófono tu voz en electricidad?
Science: the voice makes the air vibrate, and these pressure waves push the thin membrane (diaphragm) of the
microphone back and forth. In a dynamic microphone the membrane is attached to a small coil of wire that sits in the
field of a permanent magnet. When the coil moves inside the magnetic field, electromagnetic induction produces an
electric current in the wire. That current rises and falls with the same rhythm as the sound wave: it is the audio
signal. It is the same principle as a dynamic loudspeaker working the other way round. (Condenser microphones are not
covered; no voltages, sensitivities or frequency ranges are claimed.)
"""
import math

ID = "032"
TITLE = "¿Cómo convierte un micrófono tu voz en electricidad?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo convierte un micrófono tu voz en electricidad?",
    "Tu voz hace vibrar el aire, que empuja una membrana.",
    "En uno dinámico, la membrana lleva una bobina junto a un imán.",
    "Al vibrar, la bobina se mueve dentro del campo magnético.",
    "Mover un cable en un campo magnético genera corriente.",
    "Esa corriente sube y baja al ritmo de tu voz.",
    "Es un altavoz funcionando al revés: sonido convertido en señal.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"micrófono", "voz", "electricidad", "vibrar", "aire", "membrana", "dinámico", "bobina", "imán",
            "campo", "magnético", "cable", "corriente", "ritmo", "altavoz", "revés", "sonido", "señal"}

COPPER = (214, 128, 64)
CY = 700
MEM_X = 430          # membrane rest position
MAG_X0, MAG_X1 = 600, 800

def mic_icon(E, d, x, y, s=1.0):
    E.rrect(d, x - 50 * s, y + 120 * s, x + 50 * s, y + 420 * s, 30 * s, E.SIL_D)
    E.circle(d, x, y, 150 * s, fill=E.SIL)
    for k in range(-4, 5):
        E.line(d, [(x + k * 30 * s, y - 135 * s * math.sqrt(max(0, 1 - (k / 5) ** 2))),
                   (x + k * 30 * s, y + 135 * s * math.sqrt(max(0, 1 - (k / 5) ** 2)))], E.SIL_D, 4)

def voice_waves(E, d, u, x0, x1, y, n=4, speed=1.0):
    for k in range(n):
        f = (u * speed + k / n) % 1
        x = x0 + (x1 - x0) * f
        pts = [(x + 40 * math.cos(t), y + 170 * math.sin(t)) for t in [-1.0 + 2.0 * j / 20 for j in range(21)]]
        E.line(d, pts, E.mix(E.AMB, E.BG2, 0.15 + f * 0.4), 9)

def capsule(E, d, dx=0.0, field=False, labels=False, wires=False):
    # permanent magnet with a centre pole entering the coil
    E.rrect(d, MAG_X0, CY - 190, MAG_X1, CY + 190, 16, E.HOT_D)
    E.rrect(d, MAG_X0 - 110, CY - 40, MAG_X0 + 10, CY + 40, 8, E.SIL_D)
    if field:
        for j, yy in enumerate((-70, -105, 70, 105)):
            E.line(d, [(MAG_X0 - 100, CY + yy), (MAG_X0 - 10, CY + yy)], E.mix(E.COLD, E.BG2, 0.2 + 0.2 * (j % 2)), 4)
    # membrane (bulges with dx)
    x = MEM_X + dx
    pts = [(MEM_X + dx * math.cos(t * math.pi / 2), CY + 260 * t) for t in [-1 + j / 10 for j in range(21)]]
    E.line(d, pts, E.SIL_H, 12)
    # coil glued to the membrane, around the pole
    cx = x + 20
    E.rrect(d, cx, CY - 70, cx + 90, CY + 70, 10, COPPER)
    for k in range(6):
        yy = CY - 55 + k * 22
        E.line(d, [(cx + 4, yy), (cx + 86, yy)], E.mix(COPPER, E.BG1, 0.45), 4)
    if wires:
        E.line(d, [(cx + 45, CY + 70), (cx + 45, 1060), (900, 1060)], E.COLD, 6)
        E.line(d, [(cx + 70, CY + 70), (cx + 70, 1110), (900, 1110)], E.COLD, 6)
    if labels:
        E.label(d, "MEMBRANA", MEM_X - 20, CY - 330, 44, color=E.AMB)
        E.label(d, "BOBINA", cx + 45, CY + 190, 44, color=E.AMB)
        E.label(d, "IMÁN", (MAG_X0 + MAG_X1) / 2, CY - 250, 46, color=E.AMB)

def trace(E, d, u, x0, y0, w, h, color, speed=4.0):
    pts = [(x0 + w * j / 70, y0 - h * math.sin(j / 70 * 5 * math.pi - u * speed) * (0.55 + 0.45 * math.sin(j / 11 - u))) for j in range(71)]
    E.line(d, pts, color, 6)

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: voice waves already reaching a generic microphone
        voice_waves(E, d, u, 170, 520, 640, n=4, speed=1.1)
        o = 0.6 + 0.4 * abs(math.sin(u * 2 * math.pi * 1.8))   # generic talking mouth (no face, no person)
        E.circle(d, 110, 640, 70, fill=E.HOT_D)
        E.rrect(d, 70, 640 - 34 * o, 150, 640 + 34 * o, 30, (40, 14, 20))
        mic_icon(E, d, 720, 620)
        trace(E, d, u, 600, 1110, 360, 40, E.COLD)
        E.pill(d, "VOZ", 140, 470, 44)
    elif i == 1:  # the voice vibrates the air, which pushes a membrane
        dx = 22 * math.sin(u * 2 * math.pi * 1.6)
        for k in range(6):   # air molecules bunching towards the membrane
            f = (u * 0.8 + k / 6) % 1
            xx = 90 + f * (MEM_X - 130)
            for j in range(9):
                E.circle(d, xx + 10 * math.sin(j * 1.9), 470 + j * 58, 8, fill=E.mix(E.WHITE, E.BG2, 0.2 + f * 0.4))
        capsule(E, d, dx)
        E.label(d, "AIRE", 200, 380, 48, color=E.WHITE)
        E.label(d, "MEMBRANA", MEM_X, CY + 330, 46, color=E.AMB)
    elif i == 2:  # dynamic mic: membrane carries a coil next to a magnet
        capsule(E, d, 0, labels=E.ease(u / (L * 0.4)) > 0.2)
        E.label(d, "DINÁMICO", 540, 1060, 50, color=E.WHITE)
    elif i == 3:  # the coil moves inside the magnetic field
        s = math.sin(u * 2 * math.pi * 1.0)
        capsule(E, d, 30 * s, field=True)
        cx = MEM_X + 30 * s + 65
        E.arrow(d, cx - 60, CY - 120, cx - 150, CY - 120, E.AMB, 8, 28)
        E.arrow(d, cx + 10, CY - 120, cx + 100, CY - 120, E.AMB, 8, 28)
        E.label(d, "CAMPO MAGNÉTICO", 540, 1150, 48, color=E.COLD)
    elif i == 4:  # moving a wire in a magnetic field makes a current
        s = math.sin(u * 2 * math.pi * 1.0)
        capsule(E, d, 30 * s, field=True, wires=True)
        sgn = 1 if math.cos(u * 2 * math.pi * 1.0) > 0 else -1
        for k in range(6):
            f = ((u * 0.9 * sgn) + k / 6) % 1
            E.circle(d, MEM_X + 140 + f * (900 - MEM_X - 140), 1060, 10, fill=E.AMB)
        E.rrect(d, 900, 1020, 1000, 1150, 14, E.BLUE)
        E.label(d, "CORRIENTE", 700, 990, 48, color=E.AMB)
    elif i == 5:  # current rises and falls with the rhythm of the voice
        trace(E, d, u, 120, 520, 840, 110, E.AMB, speed=3.0)
        trace(E, d, u, 120, 900, 840, 110, E.COLD, speed=3.0)
        E.label(d, "VOZ", 160, 360, 46, color=E.AMB, anchor="lm")
        E.label(d, "CORRIENTE", 160, 1100, 46, color=E.COLD, anchor="lm")
        E.label(d, "MISMO RITMO", 540, 710, 50, color=E.WHITE)
    elif i == 6:  # a speaker working backwards: sound in, signal out
        k = E.ease(u / (L * 0.5))
        E.label(d, "ALTAVOZ", 540, 330, 46, color=E.MUTED)
        trace(E, d, u, 110, 470, 260, 40, E.COLD)
        E.arrow(d, 400, 470, 680, 470, E.MUTED, 6, 24)
        voice_waves(E, d, u, 720, 960, 470, n=3, speed=0.8)
        if k > 0.2:
            E.label(d, "MICRÓFONO", 540, 690, 54, color=E.AMB)
            voice_waves(E, d, u, 110, 360, 880, n=3, speed=0.8)
            E.arrow(d, 400, 880, 680, 880, E.AMB, 8, 28)
            trace(E, d, u, 720, 880, 260, 50, E.COLD)
            E.label(d, "SONIDO", 230, 1100, 44, color=E.AMB)
            E.label(d, "SEÑAL", 850, 1100, 44, color=E.COLD)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.05, 1.0), ("whoosh", s[1] + 0.4, 0.8), ("click", s[2] + 0.7), ("pop", s[3] + 0.8),
            ("zip", s[4] + 0.4, 1.0), ("click", s[5] + 0.6), ("whoosh", s[6] + 0.3, 1.2)]
