"""Video 005 — ¿Cómo escribe un bolígrafo?
Mechanism: a metal ball (≈0.5–1 mm) sits in a socket at the tip; it can rotate but not fall out.
Thick, oil-based ink from the reservoir wets the back of the ball. Rolling the ball over paper carries
the ink film around to the paper (like a roller) leaving a thin, even line. When idle the ball closes
the tip, which helps keep the ink from drying out.
"""
import math

ID = "005"
TITLE = "¿Cómo escribe un bolígrafo?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo escribe un bolígrafo sin mancharlo todo?",
    "Todo depende de una bolita metálica de apenas un milímetro, en la punta.",
    "La bolita está encajada en un asiento: puede girar, pero no salirse.",
    "Por detrás, la toca la tinta espesa del depósito.",
    "Al mover el bolígrafo, la bolita rueda y lleva la tinta hasta el papel.",
    "Funciona como un rodillo: deja una línea fina y uniforme.",
    "Y cuando no escribes, la bolita tapa la punta y ayuda a que la tinta no se seque.",
    "Sígueme para ver cómo funcionan las cosas por dentro.",
]
KEYWORDS = {"bolígrafo", "bolita", "milímetro", "punta", "asiento", "girar", "tinta", "depósito", "rueda", "papel", "rodillo", "uniforme", "tapa", "seque", "dentro"}

INK, INK_D = (40, 90, 200), (25, 60, 140)
PAPER = (240, 238, 228)
BALL, BALL_D = (190, 198, 212), (110, 120, 138)
BODY = (60, 74, 104)

def paper(E, d, y0=900, y1=1170):
    E.rrect(d, 60, y0, 1020, y1, 16, PAPER)
    for y in range(y0 + 50, y1, 55):
        E.line(d, [(80, y), (1000, y)], (200, 205, 220), 2)

def big_ball(E, d, cx, cy, r, ang, ink_frac=0.5):
    E.circle(d, cx, cy, r, fill=BALL, outline=BALL_D, w=4)
    # ink film on the back half, rotating with the ball
    a0 = math.degrees(ang)
    d.pieslice(E.P(cx - r, cy - r, cx + r, cy + r), a0 + 180, a0 + 180 + 360 * ink_frac, fill=INK)
    E.circle(d, cx, cy, r * 0.82, fill=BALL)
    E.circle(d, cx - r * 0.3, cy - r * 0.3, r * 0.18, fill=(235, 240, 248))
    # rotation marker
    E.line(d, [(cx, cy), (cx + r * 0.7 * math.cos(ang), cy + r * 0.7 * math.sin(ang))], BALL_D, 6)

def tip_section(E, d, cx, cy, s, ang=0.0, ink=True):
    """Cut-away pen tip pointing down. Ball centre at (cx, cy), scale s."""
    r = 90 * s
    E.poly(d, [(cx - 170 * s, cy - 420 * s), (cx + 170 * s, cy - 420 * s), (cx + r * 1.05, cy - r * 0.2), (cx - r * 1.05, cy - r * 0.2)], fill=E.SIL, outline=E.SIL_D, w=4)
    E.poly(d, [(cx - 60 * s, cy - 420 * s), (cx + 60 * s, cy - 420 * s), (cx + 40 * s, cy - r * 0.8), (cx - 40 * s, cy - r * 0.8)], fill=INK if ink else (40, 50, 70))
    big_ball(E, d, cx, cy, r, ang)
    # socket lips that hold the ball in
    E.poly(d, [(cx - r * 1.05, cy - r * 0.2), (cx - r * 0.75, cy + r * 0.62), (cx - r * 0.95, cy + r * 0.2)], fill=E.SIL_D)
    E.poly(d, [(cx + r * 1.05, cy - r * 0.2), (cx + r * 0.75, cy + r * 0.62), (cx + r * 0.95, cy + r * 0.2)], fill=E.SIL_D)

def scene(i, u, L, E, im, d):
    cx = 540
    if i == 0:  # pen writing a squiggle
        paper(E, d, 700, 1170)
        n = int(60 * E.ease(u / (L * 0.9)))
        pts = [(160 + k * 12.5, 930 + 60 * math.sin(k * 0.35)) for k in range(n + 1)]
        if len(pts) > 1: E.line(d, pts, INK, 9)
        px, py = pts[-1]
        E.poly(d, [(px, py), (px + 40, py - 90), (px + 220, py - 520), (px + 300, py - 480), (px + 70, py - 70)], fill=BODY, outline=E.SIL_D, w=3)
        E.poly(d, [(px, py), (px + 40, py - 90), (px + 70, py - 70)], fill=E.SIL)
        E.label(d, "SIN MANCHAR", 300, 420, 52)
    elif i == 1:  # zoom to tip: tiny ball
        k = E.ease(u / 1.0)
        tip_section(E, d, cx, 880, 0.5 + 0.8 * k, ang=u * 2)
        if u > 1.0:
            E.pill(d, "≈ 1 mm", 850, 1060, 44)
            E.arrow(d, 800, 1030, 660, 960, w=5)
    elif i == 2:  # socket: rotates but can't fall out
        tip_section(E, d, cx, 880, 1.3, ang=u * 3)
        for k in (-1, 1):
            a0 = -math.pi / 2 + k * 0.9
            E.arrow(d, cx + 180 * math.cos(a0), 880 + 180 * math.sin(a0), cx + 180 * math.cos(a0 + 0.6 * k), 880 + 180 * math.sin(a0 + 0.6 * k), w=7)
        if u > 0.6:
            E.label(d, "ASIENTO", 180, 980, 46); E.arrow(d, 180, 950, 420, 930, w=5)
        if u > L * 0.6:
            E.arrow(d, cx, 1010, cx, 1110, color=E.HOT, w=8); E.cross(d, cx, 1145, 26)
    elif i == 3:  # reservoir ink reaches the back of the ball
        # long reservoir tube + tip
        E.rrect(d, cx - 70, 300, cx + 70, 640, 20, (40, 50, 70), outline=E.SIL_D, w=4)
        lvl = 330 + 40 * (1 - E.ease(u / 1.2))
        E.rrect(d, cx - 58, lvl, cx + 58, 636, 14, INK)
        tip_section(E, d, cx, 900, 1.0, ang=0.0)
        E.label(d, "DEPÓSITO", 240, 470, 46); E.arrow(d, 300, 500, cx - 80, 520, w=5)
        if u > 0.8:
            E.label(d, "TINTA", 860, 760, 46, color=(120, 160, 255)); E.arrow(d, 830, 790, cx + 30, 840, w=5, color=(120, 160, 255))
    elif i == 4:  # rolling carries ink to paper
        paper(E, d, 1000, 1170)
        ang = u * 2.4  # rolling to the right -> clockwise
        tip_section(E, d, cx, 900, 1.0, ang=ang)
        n = int(26 * E.ease(u / L))
        E.line(d, [(cx - k * 16, 990) for k in range(n + 1)] or [(cx, 990), (cx, 990)], INK, 10)
        E.arrow(d, cx - 220, 1080, cx + 160, 1080, color=E.AMB, w=7)
        d.arc(E.P(cx - 140, 760, cx + 140, 1040), 200, 320, fill=E.AMB, width=7 * E.S)
        E.label(d, "RUEDA", 860, 820, 46)
    elif i == 5:  # roller analogy + uniform line
        paper(E, d, 900, 1170)
        p = E.ease(u / (L * 0.9))
        x = 140 + 760 * p
        E.line(d, [(140, 1010), (max(141, x), 1010)], INK, 14)
        E.circle(d, x, 975, 40, fill=BALL, outline=BALL_D, w=4)
        E.line(d, [(x, 975), (x + 30 * math.cos(-u * 8), 975 + 30 * math.sin(-u * 8))], BALL_D, 5)
        # paint roller icon
        E.rrect(d, 330, 470, 750, 590, 50, INK, outline=INK_D, w=4)
        E.line(d, [(540, 470), (540, 380), (800, 380), (800, 300)], E.SIL, 14)
        E.label(d, "COMO UN RODILLO", 540, 680, 50)
    elif i == 6:  # idle: ball closes the tip
        tip_section(E, d, cx, 880, 1.3, ang=0.0)
        for k in range(6):
            ax = 160 + (k * 151) % 760; ay = 1080 + 40 * math.sin(u * 2 + k)
            E.circle(d, ax, ay, 12, fill=(150, 165, 195))
        if u > 0.8:
            E.arrow(d, cx - 260, 1120, cx - 110, 1020, color=(150, 165, 195), w=6); E.cross(d, cx - 90, 1005, 24)
            E.pill(d, "PUNTA TAPADA", cx, 330, 42)
    else:
        E.outro(d, u)

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[1], 0.5), ("click", s[2] + 0.4), ("whoosh", s[4] + 0.2, 0.6), ("pop", s[6] + 0.9)]
