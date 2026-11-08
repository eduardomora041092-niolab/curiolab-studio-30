"""Video 062 — ¿Cómo se recarga una batería de litio?
Science: a lithium-ion cell has two electrodes, usually a metal-oxide cathode and a graphite anode, separated by an
electrolyte (and a porous separator) that lets lithium ions through but not electrons. When charging, the charger
pushes electrons through the external wire from the cathode side to the anode; at the same time lithium ions leave the
cathode, cross the electrolyte and are stored between the layers of the graphite anode. The cell then holds energy.
When the phone uses the battery, the process reverses: ions travel back through the electrolyte to the cathode and
electrons travel back through the phone's circuit, powering it.
(No voltages, capacities or cycle numbers are claimed.)
"""
import math

ID = "062"
TITLE = "¿Cómo se recarga una batería de litio?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo se recarga la batería de tu móvil?",
    "Dentro hay dos electrodos separados por un líquido llamado electrolito.",
    "Al cargar, el cargador empuja electrones por el cable hacia un electrodo.",
    "Los iones de litio cruzan el electrolito y se guardan en ese lado.",
    "Así la batería queda cargada de energía.",
    "Al usar el móvil, los iones vuelven al otro electrodo.",
    "Y los electrones regresan por el circuito, dando energía al móvil.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"recarga", "batería", "móvil", "electrodos", "líquido", "electrolito", "cargar", "cargador", "empuja",
            "electrones", "cable", "electrodo", "iones", "litio", "cruzan", "guardan", "cargada", "energía",
            "vuelven", "regresan", "circuito"}

CATH = (150, 90, 70)      # cathode (metal oxide)
ANOD = (70, 75, 85)       # anode (graphite)
ELY = (40, 70, 110)       # electrolyte
ION = (120, 220, 140)     # lithium ions
ELE = (255, 176, 32)

CX0, CX1 = 160, 360       # cathode
AX0, AX1 = 720, 920       # anode
TOP, BOT = 560, 1000
SLOTS_C = [(CX0 + 50 + 100 * (k % 2), TOP + 60 + 70 * (k // 2)) for k in range(12)]
SLOTS_A = [(AX0 + 50 + 100 * (k % 2), TOP + 60 + 70 * (k // 2)) for k in range(12)]


def cell(E, d):
    E.rrect(d, CX0 - 20, TOP - 20, AX1 + 20, BOT + 20, 20, ELY, outline=E.SIL, w=5)
    E.rrect(d, CX0, TOP, CX1, BOT, 10, CATH, outline=E.SIL_D, w=3)
    E.rrect(d, AX0, TOP, AX1, BOT, 10, ANOD, outline=E.SIL_D, w=3)
    for k in range(6):
        E.line(d, [(AX0 + 10, TOP + 35 + 70 * k), (AX1 - 10, TOP + 35 + 70 * k)], (110, 115, 125), 3)
    for y in range(TOP, BOT, 40):
        E.line(d, [(540, y), (540, y + 22)], E.SIL_D, 4)
    E.label(d, "CÁTODO", (CX0 + CX1) / 2, BOT + 70, 38, color=E.WHITE)
    E.label(d, "ÁNODO", (AX0 + AX1) / 2, BOT + 70, 38, color=E.WHITE)


def ions(E, d, frac_to_anode, u=0.0):
    """frac_to_anode: 0 = all ions in cathode, 1 = all in anode; moving ions drawn mid-way."""
    n = 12; pos = frac_to_anode * n
    for k in range(n):
        f = max(0.0, min(1.0, pos - k))
        ax, ay = SLOTS_C[k]; bx, by = SLOTS_A[k]
        x = ax + (bx - ax) * f; y = ay + (by - ay) * f + 30 * math.sin(math.pi * f)
        E.circle(d, x, y, 17, fill=ION, outline=(220, 255, 230), w=2)


def wire(E, d, box_label, u, direction=1, box_col=(60, 70, 90), lit=False):
    """Wire over the top from cathode to anode through a box. direction=1: electrons cathode->anode."""
    path = [((CX0 + CX1) / 2, TOP), ((CX0 + CX1) / 2, 380), ((AX0 + AX1) / 2, 380), ((AX0 + AX1) / 2, TOP)]
    E.line(d, path, E.SIL, 7)
    E.rrect(d, 400, 320, 680, 440, 18, (255, 240, 180) if lit else box_col, outline=E.SIL, w=4)
    E.label(d, box_label, 540, 380, 38, color=E.BG1 if lit else E.WHITE)
    total = (380 - TOP) * -1 * 2 + ((AX0 + AX1) / 2 - (CX0 + CX1) / 2)
    for k in range(8):
        s = ((u * 0.4 * direction + k / 8) % 1.0) * total
        a, b = (CX0 + CX1) / 2, (AX0 + AX1) / 2; h = TOP - 380
        if s < h: x, y = a, TOP - s
        elif s < h + (b - a): x, y = a + (s - h), 380
        else: x, y = b, 380 + (s - h - (b - a))
        if 400 < x < 680 and y == 380: continue
        E.circle(d, x, y, 11, fill=ELE)


def phone(E, d, x, y, level, glow=0.0):
    E.rrect(d, x - 120, y - 230, x + 120, y + 230, 34, (30, 34, 44), outline=E.SIL, w=6)
    E.rrect(d, x - 100, y - 200, x + 100, y + 200, 18, E.mix((20, 30, 50), (70, 110, 170), glow))
    E.rrect(d, x - 45, y - 90, x + 45, y + 90, 10, None, outline=E.WHITE, w=5)
    E.rrect(d, x - 18, y - 106, x + 18, y - 90, 4, E.WHITE)
    h = 166 * level
    E.rrect(d, x - 33, y + 78 - h, x + 33, y + 78, 6, ION)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: phone charging, electrons along the cable, level rising
        lvl = 0.25 + 0.6 * min(1.0, u / L)
        phone(E, d, 540, 640, lvl, glow=0.4)
        path = [(540, 870), (540, 960), (300, 960), (300, 1120)]
        E.line(d, path, E.SIL, 9)
        E.rrect(d, 250, 1100, 350, 1180, 12, E.SIL_D)
        for k in range(6):
            q = (u * 0.6 + k / 6) % 1.0
            s = q * 480
            if s < 160: x, y = 300, 1120 - s
            elif s < 400: x, y = 300 + (s - 160), 960
            else: x, y = 540, 960 - (s - 400)
            E.circle(d, x, y, 11, fill=ELE)
        E.pill(d, "CARGANDO", 540, 330, 44)
    elif i == 1:  # two electrodes separated by electrolyte
        cell(E, d)
        ions(E, d, 0.0)
        E.label(d, "ELECTROLITO", 540, 470, 46, color=E.COLD)
        E.label(d, "DOS ELECTRODOS", 540, 350, 50, color=E.AMB)
    elif i == 2:  # charger pushes electrons along the wire to one electrode
        cell(E, d)
        ions(E, d, 0.0)
        wire(E, d, "CARGADOR", u, 1)
        E.label(d, "ELECTRONES", 540, 1140, 44, color=ELE)
    elif i == 3:  # lithium ions cross the electrolyte and are stored on that side
        cell(E, d)
        wire(E, d, "CARGADOR", u, 1)
        ions(E, d, min(1.0, 0.1 + u / (L * 0.85)), u)
        E.arrow(d, 400, 500, 680, 500, ION, 7, 26)
        E.label(d, "IONES DE LITIO", 540, 1140, 44, color=ION)
    elif i == 4:  # battery charged
        cell(E, d)
        ions(E, d, 1.0)
        E.pill(d, "CARGADA", 540, 400, 50)
        E.label(d, "ENERGÍA GUARDADA", 540, 1140, 44, color=E.AMB)
    elif i == 5:  # in use: ions go back
        cell(E, d)
        wire(E, d, "MÓVIL", u, -1, lit=True)
        ions(E, d, max(0.0, 1.0 - u / (L * 0.85)), u)
        E.arrow(d, 680, 500, 400, 500, ION, 7, 26)
        E.label(d, "IONES DE VUELTA", 540, 1140, 44, color=ION)
    elif i == 6:  # electrons back through the phone's circuit
        cell(E, d)
        ions(E, d, 0.0)
        wire(E, d, "MÓVIL", u, -1, lit=True)
        E.label(d, "ENERGÍA AL MÓVIL", 540, 1140, 44, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 0.8), ("pop", s[1] + 0.6), ("zip", s[2] + 0.5), ("zip", s[3] + 0.4),
            ("click", s[4] + 0.6), ("whoosh", s[5] + 0.5, 0.8), ("zip", s[6] + 0.4)]
