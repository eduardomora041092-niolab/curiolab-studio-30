"""Video 034 — ¿Cómo gira un motor eléctrico?
Science (simple brushed DC motor): a coil of wire that can turn sits between the poles of permanent magnets. When a
current flows through the coil it becomes an electromagnet with its own north and south poles. Like poles repel and
opposite poles attract, so the coil is pushed round. On its own it would stop once its poles face the opposite
poles of the magnets. A commutator (a split ring touched by two brushes) reverses the direction of the current in
the coil every half turn, right at that point, so the coil's poles swap and the push continues in the same
direction: the motor keeps turning. (Brushless and AC motors are not covered; no speeds, voltages or powers claimed.)
"""
import math

ID = "034"
TITLE = "¿Cómo gira un motor eléctrico?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo gira un motor eléctrico?",
    "Dentro, una bobina de cable puede girar entre dos imanes.",
    "Al pasar corriente, la bobina se convierte en un electroimán.",
    "Sus polos son atraídos y repelidos por los imanes, y la bobina gira.",
    "Pero al quedar frente a los polos opuestos, se pararía.",
    "Justo ahí, el conmutador invierte el sentido de la corriente.",
    "Los polos de la bobina se intercambian y sigue girando sin parar.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"motor", "eléctrico", "bobina", "cable", "girar", "imanes", "corriente", "electroimán", "polos",
            "atraídos", "repelidos", "gira", "opuestos", "pararía", "conmutador", "invierte", "sentido",
            "intercambian", "girando", "parar"}

COPPER = (214, 128, 64)
CX, CY, R = 540, 660, 210     # rotor centre and half-length
N_COL, S_COL = (226, 70, 60), (60, 120, 220)

def magnets(E, d, labels=True):
    E.rrect(d, 110, CY - 230, 250, CY + 230, 22, N_COL)
    E.rrect(d, 830, CY - 230, 970, CY + 230, 22, S_COL)
    if labels:
        E.label(d, "N", 180, CY, 80, color=E.WHITE)
        E.label(d, "S", 900, CY, 80, color=E.WHITE)

def rotor(E, d, a, pole_a=None, current=False, u=0.0):
    """Coil seen from above as a bar. pole_a: polarity of end A ('N'/'S') or None (no current)."""
    ca, sa = math.cos(a), math.sin(a); nx, ny = -sa, ca; w = 46
    ax, ay = CX + R * ca, CY + R * sa; bx, by = CX - R * ca, CY - R * sa
    E.poly(d, [(ax + nx * w, ay + ny * w), (ax - nx * w, ay - ny * w), (bx - nx * w, by - ny * w), (bx + nx * w, by + ny * w)], fill=COPPER)
    for k in range(-7, 8):   # windings
        px, py = CX + k * 26 * ca, CY + k * 26 * sa
        E.line(d, [(px + nx * w, py + ny * w), (px - nx * w, py - ny * w)], E.mix(COPPER, E.BG1, 0.45), 4)
    E.circle(d, CX, CY, 20, fill=E.SIL_D)
    if current:
        for k in range(5):   # charges travelling along the coil
            f = (u * 0.9 + k / 5) % 1
            px, py = CX + (2 * f - 1) * R * ca + nx * 30, CY + (2 * f - 1) * R * sa + ny * 30
            E.circle(d, px, py, 9, fill=E.AMB)
    if pole_a:
        pb = "S" if pole_a == "N" else "N"
        for (x, y, p) in ((ax, ay, pole_a), (bx, by, pb)):
            E.circle(d, x, y, 44, fill=N_COL if p == "N" else S_COL)
            E.label(d, p, x, y, 50, color=E.WHITE)

def pole_of(a):
    """End A is N while heading towards the right S magnet (a in (pi, 2pi)), S otherwise: the commutator swaps it."""
    return "N" if (a % (2 * math.pi)) > math.pi else "S"

def commutator(E, d, a, x, y, r, big=False):
    w = 14 if big else 8
    for h, col in ((0, E.BRA), (math.pi, E.BRA_D)):
        pts = [(x + r * math.cos(a + h + 0.2 + t * (math.pi - 0.4) / 16), y + r * math.sin(a + h + 0.2 + t * (math.pi - 0.4) / 16)) for t in range(17)]
        E.line(d, pts, col, w * 2)
    bw = 34 if big else 20
    E.rrect(d, x - r - bw - 10, y - bw / 2, x - r - 6, y + bw / 2, 4, E.SIL_D)
    E.rrect(d, x + r + 6, y - bw / 2, x + r + bw + 10, y + bw / 2, 4, E.SIL_D)

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: a motor already spinning a fan
        E.circle(d, CX, 720, 230, fill=E.SIL_D)
        E.circle(d, CX, 720, 200, fill=E.SIL)
        a = u * 9.0
        for k in range(3):
            b = a + k * 2 * math.pi / 3
            p = [(CX, 720), (CX + 330 * math.cos(b - 0.25), 720 + 330 * math.sin(b - 0.25)),
                 (CX + 360 * math.cos(b + 0.05), 720 + 360 * math.sin(b + 0.05)), (CX + 300 * math.cos(b + 0.3), 720 + 300 * math.sin(b + 0.3))]
            E.poly(d, p, fill=E.mix(E.COLD, E.BG2, 0.25))
        E.circle(d, CX, 720, 50, fill=E.SIL_H)
        for k in range(3):
            b = a * 0.9 + k * 2.1
            E.line(d, [(CX + 400 * math.cos(b + t / 10), 720 + 400 * math.sin(b + t / 10)) for t in range(8)], E.AMB, 6)
        E.pill(d, "MOTOR", CX, 1110, 46)
    elif i == 1:  # a coil that can turn between two magnets
        magnets(E, d)
        rotor(E, d, -0.5 + 0.25 * math.sin(u * 2.0))
        E.label(d, "IMÁN", 180, CY - 290, 46, color=E.AMB)
        E.label(d, "IMÁN", 900, CY - 290, 46, color=E.AMB)
        E.label(d, "BOBINA", CX, 1000, 48, color=E.AMB)
    elif i == 2:  # current flows: the coil becomes an electromagnet
        magnets(E, d)
        k = E.ease(u / (L * 0.5))
        rotor(E, d, 3 * math.pi / 2 - 0.4, pole_a="N" if k > 0.5 else None, current=True, u=u)
        E.label(d, "CORRIENTE", CX, 330, 48, color=E.AMB)
        E.label(d, "ELECTROIMÁN", CX, 1010, 50, color=E.WHITE)
    elif i == 3:  # attraction and repulsion make it turn
        magnets(E, d)
        a = 3 * math.pi / 2 - 0.4 + 0.9 * E.ease(u / L)
        rotor(E, d, a, pole_a=pole_of(a), current=True, u=u)
        ax, ay = CX + R * math.cos(a), CY + R * math.sin(a)
        bx, by = CX - R * math.cos(a), CY - R * math.sin(a)
        E.arrow(d, ax + 40, ay + 10, 790, CY - 60, E.AMB, 7, 26)
        E.arrow(d, bx - 40, by - 10, 290, CY + 60, E.AMB, 7, 26)
        E.label(d, "SE ATRAEN", CX, 330, 48, color=E.AMB)
        E.label(d, "GIRA", CX, 1010, 52, color=E.WHITE)
    elif i == 4:  # facing the opposite poles it would stop
        magnets(E, d)
        a = 2 * math.pi - 0.5 * (1 - E.ease(u / (L * 0.6))) + 0.04 * math.sin(u * 6) * (1 - E.ease(u / L))
        rotor(E, d, a, pole_a="N", current=True, u=u)
        E.label(d, "N FRENTE A S", CX, 330, 48, color=E.AMB)
        if u > L * 0.5:
            E.pill(d, "SE PARARÍA", CX, 1020, 46, bg=E.HOT)
    elif i == 5:  # the commutator reverses the current
        k = E.ease(u / (L * 0.8))
        a = math.pi / 2 - 0.6 + math.pi * k
        commutator(E, d, a, CX, 640, 170, big=True)
        E.line(d, [(CX - 230, 640), (200, 640), (200, 420)], E.HOT, 8)
        E.line(d, [(CX + 230, 640), (880, 640), (880, 420)], E.COLD, 8)
        E.label(d, "+", 200, 380, 70, color=E.HOT)
        E.label(d, "-", 880, 380, 80, color=E.COLD)
        E.label(d, "CONMUTADOR", CX, 900, 52, color=E.AMB)
        E.label(d, "ESCOBILLA", 200, 760, 40, color=E.MUTED)
        E.label(d, "ESCOBILLA", 880, 760, 40, color=E.MUTED)
        if k > 0.55:
            E.pill(d, "CORRIENTE INVERTIDA", CX, 1040, 40)
    elif i == 6:  # poles swap and it keeps turning
        magnets(E, d)
        a = 2 * math.pi - 0.3 + u * 3.2
        rotor(E, d, a, pole_a=pole_of(a), current=True, u=u)
        commutator(E, d, a, CX, 1060, 50)
        E.label(d, "GIRO CONTINUO", CX, 330, 50, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.05, 1.0), ("click", s[1] + 0.6), ("zip", s[2] + 0.4, 1.0), ("whoosh", s[3] + 0.5, 0.8),
            ("pop", s[4] + 1.2), ("click", s[5] + 1.2), ("whoosh", s[6] + 0.3, 1.2)]
