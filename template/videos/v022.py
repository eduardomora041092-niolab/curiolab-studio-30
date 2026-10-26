"""Video 022 — ¿Cómo suena una tecla de piano?
Mechanism: each piano key is a lever that pivots on a balance point. Pressing the front of the key down raises its
back end, which (through the action) throws a felt-covered hammer up towards the string. The hammer strikes the
string and immediately falls back (escapement), so it does not stay pressed against the string and the string can
vibrate. At the same time the key lifts the damper (a felt pad that normally rests on the string), so the string
vibrates freely and sounds. When the key is released the damper falls back on the string and stops the sound.
(Simplified side view: the wippen/jack is drawn as one pusher; no numbers of parts, strings or forces are claimed.)
"""
import math

ID = "022"
TITLE = "¿Cómo suena una tecla de piano?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Qué pasa dentro del piano al pulsar una tecla?",
    "Cada tecla es una palanca que gira sobre un punto.",
    "Al bajar la parte delantera, la trasera sube.",
    "Ese impulso lanza un martillo forrado de fieltro.",
    "El martillo golpea la cuerda y rebota al instante.",
    "A la vez se levanta el apagador y la cuerda vibra libre.",
    "Al soltar la tecla, el apagador baja y el sonido para.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"piano", "tecla", "palanca", "gira", "punto", "delantera", "trasera", "sube", "impulso", "martillo",
            "fieltro", "golpea", "cuerda", "rebota", "instante", "apagador", "vibra", "libre", "soltar", "baja",
            "sonido", "para", "funcionan"}

KEY_W, KEY_D = (246, 244, 236), (190, 186, 175)
WOOD, WOOD_D = (150, 100, 60), (105, 68, 38)
FELT = (200, 70, 60)
DFELT = (90, 90, 100)
PX, PY = 520, 980                 # key balance point
KL0, KL1 = 400, 380               # key length in front of / behind the pivot
SY, SX0, SX1 = 560, 110, 1000     # string
HPX, HPY, HL = 900, 720, 260      # hammer pivot (right), shank length to the head (left)
DX = 770                          # damper x

def strike_cycle(t, C=1.2):
    """Returns press, hammer, damper, vibration for time t inside a press-and-release cycle of length C."""
    t = t % C
    press = E_ease(t / 0.14) if t < 0.75 * C else 1 - E_ease((t - 0.75 * C) / 0.12)
    if t < 0.12: ham = E_ease(t / 0.12)
    elif t < 0.26: ham = 1 - 0.7 * E_ease((t - 0.12) / 0.14)
    elif t < 0.75 * C: ham = 0.3
    else: ham = 0.3 * (1 - E_ease((t - 0.75 * C) / 0.12))
    vib = 0.0
    if t >= 0.12:
        vib = math.exp(-(t - 0.12) * 1.2) * (press if t > 0.75 * C else 1.0)
    return press, ham, press, vib

def E_ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def rot(px, py, x, y, a):
    c, s = math.cos(a), math.sin(a); dx, dy = x - px, y - py
    return px + dx * c - dy * s, py + dx * s + dy * c

def string(E, d, u, vib, color=None):
    pts = []
    for k in range(81):
        x = SX0 + (SX1 - SX0) * k / 80
        y = SY + 16 * vib * math.sin(math.pi * k / 80) * math.sin(u * 55)
        pts.append((x, y))
    E.line(d, pts, color or E.SIL_H, 6)
    E.rrect(d, SX0 - 30, SY - 30, SX0, SY + 30, 6, E.SIL_D)
    E.rrect(d, SX1, SY - 30, SX1 + 30, SY + 30, 6, E.SIL_D)
    if vib > 0.08:
        for k in range(3):
            r = 60 + 50 * k + 40 * ((u * 2) % 1)
            a = int(255 * min(1, vib))
            d.arc(E.P(560 - r, SY - 40 - r, 560 + r, SY - 40 + r), 215, 325, fill=E.mix(E.BG2, E.AMB, vib), width=5 * E.S)

def key_angle(press):
    return -0.10 * press          # negative: front (left) goes down, back (right) goes up

def mechanism(E, d, u, press, ham, damp, vib, hl=None, dim=False):
    a = key_angle(press)
    # string and damper
    string(E, d, u, vib)
    dy = -70 * damp
    E.rrect(d, DX - 10, 390 + dy, DX + 10, SY - 30 + dy, 4, E.SIL_D)
    E.rrect(d, DX - 45, SY - 34 + dy, DX + 45, SY - 4 + dy, 8, DFELT if hl != "damper" else E.AMB)
    # damper lift rod from the back of the key
    bx, by = rot(PX, PY, PX + 340, PY - 20, a)
    E.line(d, [(bx + 40, by - 10), (bx + 40, 640)], E.SIL_D, 8)
    E.line(d, [(bx + 40, 640), (DX + 30, SY - 30 + dy)], E.SIL_D, 6)
    # hammer
    th = 0.42 * ham
    hx, hy = HPX - HL * math.cos(th), HPY - HL * math.sin(th)
    E.line(d, [(HPX, HPY), (hx, hy)], WOOD, 14)
    E.circle(d, HPX, HPY, 16, fill=E.SIL)
    E.circle(d, hx, hy, 36, fill=FELT if hl != "hammer" else E.AMB)
    E.circle(d, hx, hy, 18, fill=WOOD_D)
    # pusher from the back of the key to the hammer shank
    jx, jy = rot(PX, PY, PX + 300, PY - 22, a)
    sx = HPX - 80; sy = HPY - 80 * math.sin(th) + 10
    E.line(d, [(jx, jy), (sx, sy)], E.BRA_D, 14)
    # key (lever)
    pts = [rot(PX, PY, x, y, a) for x, y in ((PX - KL0, PY - 40), (PX + KL1, PY - 40), (PX + KL1, PY), (PX - KL0, PY))]
    E.poly(d, pts, fill=WOOD if hl != "key" else E.BRA)
    top = [rot(PX, PY, x, y, a) for x, y in ((PX - KL0, PY - 70), (PX - 160, PY - 70), (PX - 160, PY - 40), (PX - KL0, PY - 40))]
    E.poly(d, top, fill=KEY_W, outline=KEY_D, w=2)
    E.poly(d, [(PX, PY + 4), (PX - 30, PY + 50), (PX + 30, PY + 50)], fill=E.AMB if hl == "pivot" else E.SIL)
    E.rrect(d, 80, PY + 50, 1000, PY + 70, 6, WOOD_D)
    return a

def finger(E, d, a, down):
    fx, fy = rot(PX, PY, PX - 330, PY - 70, a)
    E.rrect(d, fx - 34, fy - 190, fx + 34, fy - 4, 34, (232, 180, 140))
    E.rrect(d, fx - 20, fy - 60, fx + 20, fy - 20, 12, (245, 215, 190))

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: the finger is already pressing and the hammer is flying to the string
        press, ham, damp, vib = strike_cycle(u + 0.08)
        a = mechanism(E, d, u, press, ham, damp, vib)
        finger(E, d, a, press)
        E.label(d, "TECLA", 230, 1110, 46, color=E.WHITE)
        E.label(d, "CUERDA", 900, 470, 40, color=E.MUTED)
    elif i == 1:  # the key is a lever on a balance point
        press = 0.5 + 0.5 * math.sin(u * 3.2)
        mechanism(E, d, u, press, 0.25 * press, press, 0, hl="pivot")
        E.label(d, "PALANCA", 300, 800, 50, color=E.AMB)
        E.label(d, "PUNTO DE APOYO", PX, 1110, 44, color=E.AMB)
    elif i == 2:  # front down, back up
        press = E.ease(u / (L * 0.5))
        a = mechanism(E, d, u, press, 0.3 * press, press, 0, hl="key")
        fx, fy = rot(PX, PY, PX - 330, PY - 80, a)
        E.arrow(d, fx, fy - 170, fx, fy - 40, color=E.AMB, w=10)
        bx, by = rot(PX, PY, PX + 360, PY + 40, a)
        E.arrow(d, bx + 70, by + 90, bx + 70, by - 40, color=E.AMB, w=10)
        E.label(d, "BAJA", 190, 1110, 48, color=E.WHITE)
        E.label(d, "SUBE", 940, 1110, 48, color=E.WHITE)
    elif i == 3:  # the impulse throws the felt hammer
        k = E.ease(u / (L * 0.45))
        mechanism(E, d, u, 1.0, 0.95 * k, 1.0, 0, hl="hammer")
        E.label(d, "MARTILLO DE FIELTRO", 540, 1110, 46, color=E.AMB)
    elif i == 4:  # strikes and rebounds at once
        t = (u % 1.4)
        ham = E.ease(t / 0.15) if t < 0.15 else 1 - 0.7 * E.ease((t - 0.15) / 0.25)
        vib = 0 if t < 0.15 else 1.0
        mechanism(E, d, u, 1.0, ham, 1.0, vib if u > 0.15 else 0, hl="hammer")
        E.label(d, "GOLPEA", 300, 470, 46, color=E.AMB)
        E.label(d, "REBOTA", 540, 1110, 48, color=E.AMB)
    elif i == 5:  # the damper lifts and the string vibrates freely
        mechanism(E, d, u, 1.0, 0.3, 1.0, 1.0, hl="damper")
        E.label(d, "APAGADOR", DX - 190, 420, 44, color=E.AMB)
        E.label(d, "VIBRA LIBRE", 540, 1110, 48, color=E.AMB)
    elif i == 6:  # release: the damper falls and the sound stops
        k = E.ease(u / (L * 0.4))
        press = 1 - k
        vib = max(0.0, 1 - E.ease(u / (L * 0.5)) * 1.3)
        a = mechanism(E, d, u, press, 0.3 * press, press, vib, hl="damper")
        E.label(d, "APAGADOR", DX - 190, 420, 44, color=E.AMB)
        E.label(d, "SILENCIO", 540, 1110, 48, color=E.AMB if k > 0.9 else E.WHITE)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("click", s[0] + 0.05), ("click", s[0] + 1.25), ("click", s[0] + 2.45), ("pop", s[1] + 0.5),
            ("whoosh", s[2] + 0.2, 0.8), ("whoosh", s[3] + 0.2, 0.8), ("click", s[4] + 0.15), ("click", s[4] + 1.55),
            ("pop", s[5] + 0.4), ("pop", s[6] + 0.6)]
