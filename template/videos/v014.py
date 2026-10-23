"""Video 014 — ¿Cómo dobla una grapa la grapadora?
Science: staples sit in a row inside the magazine (channel), pushed forward by a spring-loaded follower.
Pressing the top drives a thin metal blade (the driver) down; it shears off only the front staple of the strip
and pushes it down. The two legs pierce the paper. Under the paper is the anvil, a metal plate with two curved
grooves; as the legs hit the grooves they are guided to curl inwards, clinching the paper. Many staplers have a
rotating anvil whose other position bends the legs outwards (temporary "pinning"), which is easy to remove.
(No forces or dimensions are claimed.)
"""
ID = "014"
TITLE = "¿Cómo dobla una grapa la grapadora?"
SUBTITLE = "ASÍ FUNCIONAN LAS COSAS"
LINES = [
    "La grapa entra recta y sale doblada.",
    "Las grapas esperan en fila, empujadas por un muelle.",
    "Al apretar, una cuchilla fina empuja solo la primera grapa.",
    "Sus dos patas atraviesan el papel.",
    "Debajo las espera el yunque, una placa de metal con dos ranuras curvas.",
    "Las ranuras doblan las patas hacia dentro, y la grapa abraza el papel.",
    "En muchas, si giras el yunque, se doblan hacia fuera.",
    "Sígueme para descubrir cómo funcionan las cosas.",
]
KEYWORDS = {"grapa", "recta", "doblada", "grapas", "fila", "muelle", "apretar", "cuchilla", "primera", "patas",
            "papel", "yunque", "metal", "ranuras", "curvas", "dentro", "abraza", "giras", "fuera", "cosas"}

STAPLE = (226, 232, 240)
PAPER, PAPER_E = (250, 248, 240), (200, 196, 186)
BLADE = (255, 176, 32)
ANVIL, ANVIL_D = (150, 160, 176), (96, 104, 120)

PY = 820      # paper top (front cut view)
AY = 880      # anvil top

def staple_front(E, d, cx, top, legs, bend=0.0, out=False, w=200, col=STAPLE):
    """Front view of a staple: crown at y=top, legs of length `legs`. bend 0..1 curls legs in (or out)."""
    x0, x1 = cx - w / 2, cx + w / 2
    E.line(d, [(x0, top), (x1, top)], col, 14)
    straight = legs * (1 - bend * 0.45)
    for x, sgn in ((x0, 1), (x1, -1)):
        if out: sgn = -sgn
        pts = [(x, top), (x, top + straight)]
        if bend > 0:
            r = legs * 0.45 * bend
            pts.append((x + sgn * r * 0.6, top + straight + r * 0.7))
            pts.append((x + sgn * r * 1.4, top + straight + r * 0.55))
        E.line(d, pts, col, 14)

def paper(E, d, holes=False):
    for k in range(3):
        E.rrect(d, 200, PY + k * 14, 880, PY + k * 14 + 10, 2, PAPER if k % 2 == 0 else PAPER_E)

def anvil(E, d, glow=False, flip=False):
    E.rrect(d, 260, AY, 820, AY + 70, 10, ANVIL, outline=ANVIL_D, w=4)
    col = E.AMB if glow else ANVIL_D
    for cx in (440, 640):
        # curved groove (seen in cut)
        if not flip:
            d.arc(E.P(cx - 50, AY - 40, cx + 50, AY + 50), 20, 160, fill=col, width=8 * E.S)
        else:
            d.arc(E.P(cx - 50, AY - 40, cx + 50, AY + 50), 20, 160, fill=col, width=8 * E.S)

def scene(i, u, L, E, im, d):
    if i == 0:  # straight in, bent out
        staple_front(E, d, 300, 520, 200)
        E.label(d, "RECTA", 300, 820, 48, color=E.WHITE)
        E.arrow(d, 440, 620, 620, 620, color=E.AMB, w=10, head=34)
        k = E.ease((u - 0.3) / 0.8)
        staple_front(E, d, 780, 560, 160, bend=k)
        if u > 0.8: E.label(d, "DOBLADA", 780, 820, 48, color=E.AMB)
    elif i == 1:  # row of staples pushed by a spring (side view of magazine)
        E.rrect(d, 120, 600, 960, 780, 16, E.CAV, outline=E.SIL_D, w=6)
        n = 18; x = 180
        for k in range(n):
            E.rrect(d, x + k * 26, 640, x + k * 26 + 16, 740, 3, STAPLE)
        sx = x + n * 26 + 10; push = 4 * (1 + __import__("math").sin(u * 5))
        E.rrect(d, sx + push, 630, sx + 40 + push, 750, 6, E.SIL_D)
        pts = [(sx + 40 + push, 690)]
        for k in range(1, 13):
            pts.append((E.lerp(sx + 40 + push, 930, k / 12), 690 + (24 if k % 2 else -24)))
        pts.append((930, 690))
        E.line(d, pts, E.AMB, 6)
        E.arrow(d, 640, 560, 260, 560, color=E.AMB, w=8)
        E.label(d, "MUELLE", 820, 860, 44, color=E.AMB)
        E.label(d, "GRAPAS EN FILA", 380, 860, 44, color=E.WHITE)
    elif i == 2:  # blade pushes only the first staple (side view)
        p = E.ease(u / (L * 0.8))
        E.rrect(d, 120, 600, 960, 780, 16, E.CAV, outline=E.SIL_D, w=6)
        for k in range(1, 18):
            E.rrect(d, 180 + k * 26, 640, 180 + k * 26 + 16, 740, 3, STAPLE)
        drop = p * 300
        E.rrect(d, 180, 640 + drop, 196, 740 + drop, 3, E.AMB)
        E.rrect(d, 170, 360 + drop, 206, 640 + drop, 4, BLADE)
        E.arrow(d, 260, 380, 260, 520, color=E.WHITE, w=8)
        E.label(d, "CUCHILLA", 380, 330, 44, color=BLADE)
        if u > 0.6: E.label(d, "SOLO LA PRIMERA", 560, 1000, 44, color=E.WHITE)
    elif i in (3, 4, 5):  # front cut view: paper + anvil
        paper(E, d); anvil(E, d, glow=(i >= 4))
        if i == 3:
            p = E.ease(u / (L * 0.8))
            top = E.lerp(480, PY - 50, p)
        elif i == 4:
            top = PY - 50
        else:
            k = E.ease(u / (L * 0.6))
            top = E.lerp(PY - 50, PY - 10, k)
        E.rrect(d, 300, top - 290, 780, top - 30, 10, (60, 68, 86))
        E.rrect(d, 330, top - 30, 750, top - 8, 4, BLADE)
        staple_front(E, d, 540, top, 110, bend=(k if i == 5 else 0))
        if i == 3 and u > 0.5: E.label(d, "PAPEL", 960, PY + 14, 40, color=E.WHITE)
        if i == 4:
            E.label(d, "YUNQUE", 540, AY + 150, 52, color=E.AMB)
            if u > 0.6:
                for cx in (440, 640):
                    E.circle(d, cx, AY + 5, 66, outline=E.AMB, w=4)
                E.label(d, "RANURAS CURVAS", 540, AY + 230, 40, color=E.WHITE)
        if i == 5 and k > 0.6:
            E.arrow(d, 360, AY + 120, 450, AY + 120, color=E.AMB, w=6)
            E.arrow(d, 720, AY + 120, 630, AY + 120, color=E.AMB, w=6)
            E.label(d, "HACIA DENTRO", 540, AY + 210, 46, color=E.AMB)
    elif i == 6:  # rotate anvil -> legs bend outwards
        import math
        a = E.ease(u / (L * 0.4))
        E.rrect(d, 260, 820, 820, 890, 10, ANVIL, outline=ANVIL_D, w=4)
        d.arc(E.P(490, 760, 590, 860), 200 if a < 0.5 else 20, 340 if a < 0.5 else 160, fill=E.AMB, width=8 * E.S)
        d.arc(E.P(460, 330, 620, 490), -60, 240, fill=E.WHITE, width=6 * E.S)
        E.arrow(d, 600, 370, 615, 400, color=E.WHITE, w=6)
        E.label(d, "GIRA", 760, 410, 44, color=E.WHITE)
        if u > L * 0.4:
            staple_front(E, d, 540, 640, 140, bend=E.ease((u - L * 0.4) / 0.6), out=True)
            E.label(d, "HACIA FUERA", 540, 1000, 50, color=E.AMB)
            E.arrow(d, 470, 940, 360, 940, color=E.AMB, w=6)
            E.arrow(d, 610, 940, 720, 940, color=E.AMB, w=6)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("pop", s[0] + 0.4), ("whoosh", s[1] + 0.3, 0.6), ("click", s[2] + 0.8), ("click", s[3] + 0.8),
            ("pop", s[4] + 0.8), ("click", s[5] + 0.6), ("whoosh", s[6] + 0.2, 0.6)]
