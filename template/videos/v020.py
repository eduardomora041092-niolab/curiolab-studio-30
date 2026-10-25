"""Video 020 — ¿Cómo mide el tiempo un reloj mecánico?
Mechanism: winding a mechanical watch coils the mainspring, a flat spiral spring that stores the energy that runs
the watch. The energy flows through a train of gears to the escape wheel. The balance wheel (with its hairspring)
swings back and forth at a regular rate. On each swing the pallet fork (lever) lets the escape wheel advance by a
single tooth, and gives the balance a small push that keeps it swinging. So the gears, and the hands, move forward
in small, equal steps instead of spinning freely.
(No beat rates, power reserve or accuracy figures are claimed; steps are not claimed to be exactly one second.)
"""
import math

ID = "020"
TITLE = "¿Cómo mide el tiempo un reloj mecánico?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo marca los segundos un reloj sin pilas?",
    "Al darle cuerda, se enrolla un muelle en espiral.",
    "Ese muelle guarda la energía que mueve todo el reloj.",
    "La energía pasa por engranajes hasta la rueda de escape.",
    "Un volante oscila de un lado a otro a ritmo constante.",
    "En cada vaivén, el áncora deja pasar un solo diente.",
    "Así los engranajes y las agujas avanzan a pasos iguales.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"segundos", "reloj", "pilas", "cuerda", "enrolla", "muelle", "espiral", "energía", "engranajes",
            "rueda", "escape", "volante", "oscila", "ritmo", "constante", "vaivén", "áncora", "diente", "agujas",
            "pasos", "iguales", "funcionan"}

FACE, FACE_D = (238, 232, 218), (150, 140, 120)
CX, CY, CR = 540, 720, 320

def gear(E, d, cx, cy, r, n, rot, fill=None, dark=None, tooth=14):
    fill = fill or E.BRA; dark = dark or E.BRA_D
    pts = []
    for k in range(n):
        a = rot + 2 * math.pi * k / n; s = math.pi / n
        for da, rr in ((-0.5 * s, r - tooth), (-0.3 * s, r), (0.3 * s, r), (0.5 * s, r - tooth)):
            pts.append((cx + rr * math.cos(a + da), cy + rr * math.sin(a + da)))
    E.poly(d, pts, fill=dark)
    E.circle(d, cx, cy, r - tooth - 4, fill=fill)
    E.circle(d, cx, cy, max(8, r * 0.12), fill=dark)

def escape_wheel(E, d, cx, cy, r, rot, hl=None):
    n = 15
    pts = []
    for k in range(n):
        a = rot + 2 * math.pi * k / n; s = 2 * math.pi / n
        pts += [(cx + (r - 30) * math.cos(a), cy + (r - 30) * math.sin(a)), (cx + r * math.cos(a + 0.55 * s), cy + r * math.sin(a + 0.55 * s))]
    E.poly(d, pts, fill=E.SIL_D)
    E.circle(d, cx, cy, r - 36, fill=E.SIL)
    for k in range(5):
        a = rot + k * 2 * math.pi / 5
        E.line(d, [(cx, cy), (cx + (r - 40) * math.cos(a), cy + (r - 40) * math.sin(a))], E.SIL_D, 10)
    E.circle(d, cx, cy, 16, fill=E.SIL_D)
    if hl is not None:
        a = rot + 2 * math.pi * hl / n + 0.55 * 2 * math.pi / n
        E.circle(d, cx + r * math.cos(a), cy + r * math.sin(a), 16, fill=E.AMB)

def spiral(E, d, cx, cy, turns, rot, r0=20, r1=200, color=None, w=9):
    n = int(48 * turns); pts = []
    for k in range(n + 1):
        t = k / n; a = rot + t * turns * 2 * math.pi
        pts.append((cx + (r0 + (r1 - r0) * t) * math.cos(a), cy + (r0 + (r1 - r0) * t) * math.sin(a)))
    E.line(d, pts, color or E.SIL, w)

def balance(E, d, cx, cy, r, ang, spring=True):
    E.circle(d, cx, cy, r, outline=E.BRA_D, w=int(r * 0.16))
    for k in range(3):
        a = ang + k * 2 * math.pi / 3
        E.line(d, [(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))], E.BRA_D, max(6, int(r * 0.08)))
    if spring:
        spiral(E, d, cx, cy, 3, ang * 2, r0=8, r1=r * 0.45, color=E.SIL, w=4)
    E.circle(d, cx, cy, max(8, r * 0.1), fill=E.HOT)

def face(E, d, sec_ang, min_ang=-1.2, window=None):
    E.circle(d, CX, CY, CR + 22, fill=E.SIL_D)
    E.circle(d, CX, CY, CR, fill=FACE)
    for k in range(60):
        a = -math.pi / 2 + k * math.pi / 30; r0 = CR - (40 if k % 5 == 0 else 20)
        E.line(d, [(CX + r0 * math.cos(a), CY + r0 * math.sin(a)), (CX + (CR - 8) * math.cos(a), CY + (CR - 8) * math.sin(a))], (60, 60, 70), 8 if k % 5 == 0 else 3)
    if window is not None:
        E.circle(d, CX, CY + 150, 92, fill=E.CAV)
        balance(E, d, CX, CY + 150, 70, window, spring=False)
    E.line(d, [(CX, CY), (CX + 190 * math.cos(min_ang), CY + 190 * math.sin(min_ang))], (40, 40, 50), 16)
    E.line(d, [(CX, CY), (CX + 130 * math.cos(min_ang * 0.3 + 2.2), CY + 130 * math.sin(min_ang * 0.3 + 2.2))], (40, 40, 50), 20)
    E.line(d, [(CX - 40 * math.cos(sec_ang), CY - 40 * math.sin(sec_ang)), (CX + 270 * math.cos(sec_ang), CY + 270 * math.sin(sec_ang))], E.HOT, 6)
    E.circle(d, CX, CY, 16, fill=E.HOT)

def tick_angle(u, period, start=-math.pi / 2, step=math.pi / 30):
    k = math.floor(u / period); f = E_ease((u / period - k) / 0.25)
    return start + step * (k + f)

def E_ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: the second hand is already ticking and the balance is swinging
        osc = 1.1 * math.sin(2 * math.pi * 1.6 * u + 0.6)
        face(E, d, tick_angle(u + 0.2, 0.5), window=osc)
        for s in (-1, 1):
            a0 = -math.pi / 2 + s * 0.9 + osc * 0.3
            pts = [(CX + 110 * math.cos(a0 + t * 0.07 * s), CY + 150 + 110 * math.sin(a0 + t * 0.07 * s)) for t in range(10)]
            E.line(d, pts, E.AMB, 6)
        E.label(d, "TIC", 230, 1110, 50, color=E.AMB) if (u * 3.2) % 2 < 1 else E.label(d, "TAC", 850, 1110, 50, color=E.AMB)
    elif i == 1:  # winding coils the mainspring
        k = E.ease(u / (L * 0.85))
        E.circle(d, 500, 760, 245, fill=E.SIL_D); E.circle(d, 500, 760, 232, fill=E.CAV)
        spiral(E, d, 500, 760, 3 + 4 * k, -u * 4, r0=26, r1=225 - 90 * k)
        E.rrect(d, 745, 735, 860, 785, 8, E.SIL)
        cw = 880 + 0
        E.rrect(d, cw, 690, cw + 70, 830, 16, E.BRA_D)
        for g in range(6):
            y = 700 + ((g * 22 + u * 160) % 130)
            E.line(d, [(cw + 4, y), (cw + 66, y)], E.BRA, 6)
        E.label(d, "CUERDA", 915, 620, 40, color=E.WHITE)
        E.label(d, "MUELLE EN ESPIRAL", 540, 1100, 46, color=E.AMB)
    elif i == 2:  # the spring stores the energy
        glow = 0.5 + 0.5 * math.sin(u * 6)
        E.circle(d, 540, 760, 245, fill=E.SIL_D); E.circle(d, 540, 760, 232, fill=E.CAV)
        spiral(E, d, 540, 760, 7, 0, r0=26, r1=135, color=E.mix(E.SIL, E.AMB, glow), w=10)
        for k in range(8):
            a = k * math.pi / 4 + u
            r = 150 + 50 * ((u * 1.5 + k * 0.3) % 1)
            E.circle(d, 540 + r * math.cos(a), 760 + r * math.sin(a), 9, fill=E.AMB)
        E.label(d, "ENERGÍA", 540, 1100, 54, color=E.AMB)
    elif i == 3:  # energy through the gear train to the escape wheel
        rot = u * 0.6
        gear(E, d, 290, 960, 160, 30, rot)
        gear(E, d, 540, 790, 95, 18, -rot * 160 / 95 + 0.1)
        gear(E, d, 710, 620, 70, 14, rot * 160 / 70)
        escape_wheel(E, d, 830, 450, 95, -rot * 3)
        path = [(290, 960), (540, 790), (710, 620), (830, 450)]
        for k in range(3):
            f = (u * 0.7 + k / 3) % 1; seg = min(2, int(f * 3)); t = f * 3 - seg
            x = E.lerp(path[seg][0], path[seg + 1][0], t); y = E.lerp(path[seg][1], path[seg + 1][1], t)
            E.circle(d, x, y, 16, fill=E.AMB, outline=E.WHITE, w=3)
        E.label(d, "ENGRANAJES", 300, 1120, 44, color=E.WHITE)
        E.label(d, "RUEDA DE ESCAPE", 700, 310, 40, color=E.AMB)
    elif i == 4:  # the balance swings at a steady rhythm
        ang = 1.2 * math.sin(2 * math.pi * 0.9 * u)
        balance(E, d, 540, 720, 230, ang - math.pi / 2)
        for s in (-1, 1):
            a0 = -math.pi / 2 + s * 0.5
            pts = [(540 + 290 * math.cos(a0 + t * 0.06 * s), 720 + 290 * math.sin(a0 + t * 0.06 * s)) for t in range(12)]
            E.line(d, pts, E.AMB, 7)
        E.label(d, "VOLANTE", 540, 1100, 54, color=E.AMB)
    elif i == 5:  # each swing: the pallet fork lets exactly one tooth pass
        per = 1.0
        ph = math.sin(2 * math.pi * u / per)
        rock = 0.16 * max(-1, min(1, ph * 2.5))
        k = math.floor(u / per); f = E.ease((u / per - k) / 0.2)
        rot = -(k + f) * 2 * math.pi / 15
        balance(E, d, 540, 390, 95, rock * 6 - math.pi / 2, spring=False)
        WX, WY, WR = 540, 900, 190
        escape_wheel(E, d, WX, WY, WR, rot, hl=(-(k + 3)) % 15 if f < 1 else None)
        PX, PY = 540, 620
        pts = []
        for side in (-1, 1):
            a = -math.pi / 2 + side * 0.42
            tx, ty = WX + (WR - 6) * math.cos(a), WY + (WR - 6) * math.sin(a)
            dx, dy = tx - PX, ty - PY
            c, s_ = math.cos(rock), math.sin(rock)
            pts.append((PX + dx * c - dy * s_, PY + dx * s_ + dy * c))
        for (x, y) in pts:
            E.line(d, [(PX, PY), (x, y)], E.BLUE, 22)
            E.rrect(d, x - 14, y - 22, x + 14, y + 22, 4, E.HOT)
        E.line(d, [(PX, PY), (PX - 160 * math.sin(rock), PY - 120)], E.BLUE, 18)
        E.circle(d, PX, PY, 18, fill=E.SIL)
        E.label(d, "ÁNCORA", 830, 620, 42, color=E.WHITE)
        E.label(d, "UN DIENTE", 540, 1150, 44, color=E.AMB)
    elif i == 6:  # hands move in equal steps
        face(E, d, tick_angle(u, 0.55, start=0.3), min_ang=-1.2 + u * 0.02, window=1.1 * math.sin(2 * math.pi * 1.8 * u))
        E.label(d, "PASOS IGUALES", 540, 1110, 50, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    cues = [("click", s[0] + 0.1 + 0.5 * k) for k in range(5)]
    cues += [("whoosh", s[1] + 0.3, 1.2), ("pop", s[2] + 0.4), ("whoosh", s[3] + 0.2, 1.2), ("whoosh", s[4] + 0.3, 0.8)]
    cues += [("click", s[5] + 0.05 + 1.0 * k) for k in range(3)]
    cues += [("click", s[6] + 0.05 + 0.55 * k) for k in range(5)]
    return cues
