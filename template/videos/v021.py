"""Video 021 — ¿Por qué la Luna cambia de forma?
Science: the Moon makes no light of its own; it reflects sunlight. The Sun always lights the half of the Moon that
faces it. As the Moon orbits the Earth we see that lit half from different angles. When the Moon is between the
Earth and the Sun its lit half faces away from us and we see the dark side: new moon. When it is on the opposite
side of the Earth from the Sun we see the whole lit half: full moon. In between we see only part of the lit half
(crescent, quarter, gibbous).
(Phases are NOT caused by the Earth's shadow; no cycle length is claimed.)
"""
import math

ID = "021"
TITLE = "¿Por qué la Luna cambia de forma?"
SUBTITLE = "CURIOSIDADES DE LA CIENCIA"
LINES = [
    "¿Por qué la Luna cambia de forma cada noche?",
    "La Luna no brilla sola: la ilumina el Sol.",
    "Siempre tiene una mitad iluminada y otra a oscuras.",
    "Mientras gira alrededor de la Tierra, la vemos desde ángulos distintos.",
    "Entre la Tierra y el Sol, vemos su cara oscura: luna nueva.",
    "En el lado opuesto, vemos toda la mitad iluminada: luna llena.",
    "Entre medias, solo vemos un trozo de la parte iluminada.",
    "Sígueme para más curiosidades de la ciencia.",
]
KEYWORDS = {"luna", "forma", "noche", "brilla", "sola", "ilumina", "sol", "mitad", "iluminada", "oscuras", "gira",
            "tierra", "ángulos", "oscura", "nueva", "opuesto", "llena", "trozo", "ciencia"}

LIT, DARK = (238, 236, 222), (52, 58, 76)
SUN = (255, 196, 60)
EX, EY, OR = 560, 760, 290      # Earth centre, orbit radius

def phase(E, d, cx, cy, r, phi):
    """Moon as seen from Earth. phi: 0 new, pi/2 first quarter (right half lit), pi full, 3pi/2 last quarter."""
    S = E.S
    phi = phi % (2 * math.pi)
    E.circle(d, cx, cy, r, fill=DARK, outline=(90, 98, 120), w=3)
    box = [(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S]
    if phi < math.pi:
        d.pieslice(box, -90, 90, fill=LIT)
    else:
        d.pieslice(box, 90, 270, fill=LIT)
    k = math.cos(phi); rx = abs(k) * r
    eb = [(cx - rx) * S, (cy - r) * S, (cx + rx) * S, (cy + r) * S]
    if rx > 1:
        d.ellipse(eb, fill=DARK if k > 0 else LIT)

def half_lit(E, d, cx, cy, r):
    """Moon seen from the side: the half facing the Sun (left) is lit."""
    S = E.S
    E.circle(d, cx, cy, r, fill=DARK, outline=(90, 98, 120), w=3)
    d.pieslice([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], 90, 270, fill=LIT)

def sun_rays(E, d, u, ys=(520, 760, 1000), x1=200):
    E.circle(d, -70, EY, 150, fill=SUN)
    for y in ys:
        x0 = 90 + 30 * ((u * 1.5) % 1)
        E.arrow(d, x0, y, x0 + x1 - 90, y, color=SUN, w=6, head=20)

def orbit(E, d, u, theta, inset=None):
    sun_rays(E, d, u)
    pts = [(EX + OR * math.cos(t * math.pi / 40), EY + OR * math.sin(t * math.pi / 40)) for t in range(81)]
    E.line(d, pts, (70, 85, 120), 4)
    E.circle(d, EX, EY, 70, fill=E.BLUE)
    E.circle(d, EX - 20, EY - 15, 28, fill=(70, 160, 90)); E.circle(d, EX + 25, EY + 22, 18, fill=(70, 160, 90))
    mx, my = EX + OR * math.cos(theta), EY + OR * math.sin(theta)
    E.line(d, [(EX + 75 * math.cos(theta), EY + 75 * math.sin(theta)), (mx - 52 * math.cos(theta), my - 52 * math.sin(theta))], E.WHITE, 3)
    half_lit(E, d, mx, my, 46)
    if inset is not None:
        E.circle(d, 880, 400, 96, fill=E.CAV, outline=E.MUTED, w=3)
        phase(E, d, 880, 400, 78, inset)
        E.label(d, "DESDE LA TIERRA", 820, 300, 30, color=E.MUTED)

def window(E, d, u):
    E.rrect(d, 170, 330, 910, 1050, 20, (70, 52, 40))
    E.rrect(d, 200, 360, 880, 1020, 10, (14, 22, 46))
    for k in range(14):
        sx, sy = 230 + (k * 137) % 620, 390 + (k * 89) % 600
        if (k * 7 + int(u * 6)) % 5:
            E.circle(d, sx, sy, 4 if k % 3 else 6, fill=E.WHITE)

def scene(i, u, L, E, im, d):
    if i == 0:  # everyday + in action from frame 0: through the window, the Moon is already changing night after night
        window(E, d, u)
        phi = 0.55 + u * 1.25
        phase(E, d, 680, 560, 120, phi)
        E.rrect(d, 528, 360, 552, 1020, 4, (70, 52, 40))
        E.rrect(d, 200, 750, 880, 774, 4, (70, 52, 40))
        E.pill(d, f"NOCHE {1 + int(u * 3.2) * 2}", 540, 1110, 40)
    elif i == 1:  # the Moon is lit by the Sun
        E.circle(d, -40, 720, 240, fill=SUN)
        for k in range(5):
            y = 520 + k * 100
            x0 = 230 + 60 * ((u * 1.2 + k * 0.2) % 1)
            E.arrow(d, x0, y, x0 + 260, y, color=SUN, w=7)
        half_lit(E, d, 790, 720, 150)
        E.label(d, "SOL", 110, 720, 52, color=E.BG1)
        E.label(d, "LUZ DEL SOL", 540, 1080, 50, color=E.AMB)
    elif i == 2:  # always one half lit, the other dark
        for k in range(4):
            y = 560 + k * 110; x0 = 40 + 50 * ((u * 1.2 + k * 0.25) % 1)
            E.arrow(d, x0, y, x0 + 150, y, color=SUN, w=6, head=20)
        half_lit(E, d, 590, 720, 240)
        E.line(d, [(590, 450), (590, 990)], E.AMB, 4)
        E.label(d, "ILUMINADA", 450, 1060, 42, color=E.WHITE)
        E.label(d, "A OSCURAS", 760, 1060, 42, color=E.MUTED)
    elif i == 3:  # orbit: seen from different angles
        orbit(E, d, u, math.pi * 1.6 - u * 0.9)
        E.label(d, "ÓRBITA", EX, 1120, 48, color=E.AMB)
    elif i == 4:  # between Earth and Sun: new moon
        orbit(E, d, u, math.pi, inset=0.0)
        E.label(d, "LUNA NUEVA", EX, 1120, 48, color=E.AMB)
    elif i == 5:  # opposite side: full moon
        orbit(E, d, u, 0.0, inset=math.pi)
        E.label(d, "LUNA LLENA", EX, 1120, 48, color=E.AMB)
    elif i == 6:  # in between: only part of the lit half
        th = math.pi * 0.88 - (math.pi * 0.76) * E.ease(u / L)   # counter-clockwise (seen from the north): waxing
        orbit(E, d, u, th, inset=math.pi - th)
        E.label(d, "UN TROZO", EX, 1120, 48, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 1.5), ("pop", s[1] + 0.4), ("pop", s[2] + 0.5), ("whoosh", s[3] + 0.2, 1.2),
            ("pop", s[4] + 0.6), ("pop", s[5] + 0.6), ("whoosh", s[6] + 0.2, 1.2)]
