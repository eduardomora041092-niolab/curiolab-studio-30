"""Video 058 — ¿Cómo funciona una escalera mecánica?
Science: the steps of an escalator are fixed to a chain (in practice one at each side) that forms a closed loop.
An electric motor at the top turns the drive gear that pulls the chain continuously. Every step has two pairs of
wheels that run on two different tracks. On the inclined part the two tracks are apart in height, so each step is
held level and the steps form a staircase; at both ends the tracks come together and the steps flatten into a smooth
platform. After the top, the steps turn round and travel back underneath, upside down, to the start.
(No speeds, powers, step counts, angles or brands are claimed; the handrail is not explained.)
"""
import math

ID = "058"
TITLE = "¿Cómo funciona una escalera mecánica?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿De dónde salen los escalones de una escalera mecánica?",
    "Todos los escalones van unidos a una cadena que forma un bucle.",
    "Un motor arriba hace girar la cadena sin parar.",
    "Cada escalón tiene ruedas que van por dos carriles distintos.",
    "En la cuesta, los carriles se separan y forman los peldaños.",
    "Arriba, los carriles se juntan y los escalones quedan planos.",
    "Luego dan la vuelta por debajo y regresan al principio.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"escalones", "escalera", "mecánica", "cadena", "bucle", "motor", "girar", "ruedas", "carriles",
            "cuesta", "separan", "peldaños", "juntan", "planos", "vuelta", "debajo", "regresan", "principio"}

XL, XA, XB, XR = 100, 340, 820, 980   # bottom landing start, incline start, incline end, top landing end
YB, YT = 900, 420                     # bottom / top walking level
SP = 70                               # step pitch (x)
OFFB = 60                             # x offset of the trailing wheel
RA, RB = 40, 40                       # wheel depth below tread
RET = 200                             # return run below the walking line
STEP = (150, 160, 175)
TREAD = (205, 212, 222)
CHAIN = (255, 176, 32)
RAIL_A = (90, 170, 255)
RAIL_B = (238, 84, 54)


def yb(x):
    if x <= XA: return YB
    if x >= XB: return YT
    return YB + (YT - YB) * (x - XA) / (XB - XA)


def rail_a(x): return yb(x) + RA
def rail_b(x): return yb(x - OFFB) + RB


def steps(E, d, off, hi_wheels=False, hi_chain=False, flat_hi=False):
    n = int((XR - XL) / SP) + 2
    xs = sorted(XL + ((k * SP + off) % ((n) * SP)) for k in range(n))
    for x in xs:
        if x < XL or x + SP - 6 > XR + 4: continue
        y = yb(x)
        yprev = yb(x - SP)
        # riser (front face) from tread down to the previous step level
        if yprev - y > 2:
            E.rrect(d, x, y, x + 10, yprev, 2, STEP)
        col = E.AMB if (flat_hi and x >= XB - 10) else TREAD
        E.rrect(d, x, y - 4, x + SP - 6, y + 12, 3, col, outline=E.SIL_D, w=2)
        # step body link to wheels
        wa = (x + 6, rail_a(x + 6))
        wb = (x + 6 + OFFB, rail_b(x + 6 + OFFB))
        E.line(d, [(x + 6, y + 12), wa], E.SIL_D, 6)
        E.line(d, [(x + SP - 10, y + 12), wb], E.SIL_D, 6)
        ca = E.AMB if hi_wheels else E.SIL_H
        E.circle(d, wa[0], wa[1], 11, fill=RAIL_A if hi_wheels else ca, outline=E.BG1, w=2)
        E.circle(d, wb[0], wb[1], 11, fill=RAIL_B if hi_wheels else ca, outline=E.BG1, w=2)


def rails(E, d, hi=False, sep_hi=False):
    xs = list(range(XL, XR + 1, 10))
    wa = 8 if hi else 5
    E.line(d, [(x, rail_a(x)) for x in xs], RAIL_A if hi else (70, 90, 120), wa)
    E.line(d, [(x, rail_b(x)) for x in xs], RAIL_B if hi else (70, 90, 120), wa)


def loop_pts():
    pts = [(x, rail_a(x)) for x in range(XL, XR + 1, 10)]
    cy, r = (YT + RA + YT + RET) / 2, (RET - RA) / 2
    for k in range(1, 18):
        a = -math.pi / 2 + math.pi * k / 18
        pts.append((XR + r * math.cos(a), cy + r * math.sin(a)))
    pts += [(x, yb(x) + RET) for x in range(XR, XL - 1, -10)]
    cy2 = (YB + RA + YB + RET) / 2
    for k in range(1, 18):
        a = math.pi / 2 + math.pi * k / 18
        pts.append((XL + r * math.cos(a), cy2 + r * math.sin(a)))
    pts.append(pts[0])
    return pts


def chain(E, d, off, hi=False, show_return=True, ret_dots=False):
    pts = loop_pts()
    if not show_return:
        pts = [(x, rail_a(x)) for x in range(XL, XR + 1, 10)]
    E.line(d, pts, CHAIN if hi else (110, 90, 50), 7 if hi else 4)
    if ret_dots:   # upside-down steps travelling back underneath (right to left)
        for k in range(12):
            x = XR - ((k * 80 + off * 1.0) % (XR - XL))
            y = yb(x) + RET
            E.rrect(d, x - 26, y + 6, x + 26, y + 20, 3, E.AMB)
            E.circle(d, x - 18, y, 7, fill=E.SIL_H)
            E.circle(d, x + 18, y, 7, fill=E.SIL_H)


def sprocket(E, d, ang, hi=False):
    cx, cy = XR, (YT + RA + YT + RET) / 2
    col = E.AMB if hi else E.SIL
    E.circle(d, cx, cy, 70, fill=(40, 50, 70), outline=col, w=6)
    for k in range(8):
        a = ang + k * math.pi / 4
        E.line(d, [(cx, cy), (cx + 62 * math.cos(a), cy + 62 * math.sin(a))], col, 6)
    E.circle(d, cx, cy, 16, fill=col)


def base(E, d, off, ang=0.0, **kw):
    E.line(d, [(XL - 40, YB - 4), (XA, YB - 4)], (60, 70, 90), 2)
    chain(E, d, off, hi=kw.get("hi_chain", False), ret_dots=kw.get("ret_dots", False))
    sprocket(E, d, ang, hi=kw.get("hi_motor", False))
    rails(E, d, hi=kw.get("hi_rails", False))
    steps(E, d, off, hi_wheels=kw.get("hi_wheels", False), flat_hi=kw.get("flat_hi", False))


def scene(i, u, L, E, im, d):
    off = 24 + u * 70          # steps already moving at frame 0
    ang = u * 2.2
    if i == 0:  # in action: steps appear flat at the bottom and rise
        base(E, d, off, ang)
        E.pill(d, "¿DE DÓNDE SALEN?", 330, 380, 44)
        E.arrow(d, 200, 820, 380, 820, E.AMB, 8, 26)
    elif i == 1:  # chain loop
        base(E, d, off, ang, hi_chain=True)
        E.label(d, "CADENA", 290, 560, 52, color=E.AMB)
        E.label(d, "BUCLE", 820, 980, 50, color=E.AMB)
    elif i == 2:  # motor at the top turns the chain
        base(E, d, off, ang * 2, hi_motor=True)
        E.label(d, "MOTOR", 880, 330, 52, color=E.AMB)
        E.arrow(d, 880, 360, 950, 470, E.AMB, 8, 26)
        E.label(d, "SIN PARAR", 290, 560, 46, color=E.WHITE)
    elif i == 3:  # wheels on two tracks
        base(E, d, off * 0.3, ang, hi_rails=True, hi_wheels=True)
        E.label(d, "CARRIL 1", 260, 520, 46, color=E.COLD)
        E.label(d, "CARRIL 2", 260, 600, 46, color=E.HOT)
        E.label(d, "RUEDAS", 800, 1000, 50, color=E.AMB)
    elif i == 4:  # tracks apart on the incline -> stairs
        base(E, d, off * 0.5, ang, hi_rails=True)
        xm = 560
        ya, yb2 = rail_a(xm), rail_b(xm)
        E.circle(d, xm, (ya + yb2) / 2, 75, outline=E.AMB, w=6)
        E.line(d, [(xm + 75, (ya + yb2) / 2 + 40), (760, 880)], E.AMB, 4)
        E.label(d, "SE SEPARAN", 830, 940, 48, color=E.AMB)
        E.label(d, "PELDAÑOS", 290, 560, 52, color=E.AMB)
    elif i == 5:  # tracks join at the top -> flat steps
        base(E, d, off * 0.5, ang, hi_rails=True, flat_hi=True)
        E.label(d, "SE JUNTAN", 300, 560, 50, color=E.AMB)
        E.pill(d, "PLANOS", 890, 330, 44)
    elif i == 6:  # they turn round and come back underneath
        base(E, d, off, ang, hi_chain=True, ret_dots=True)
        E.label(d, "VUELTA", 830, 940, 50, color=E.AMB)
        E.label(d, "POR DEBAJO", 830, 1010, 46, color=E.WHITE)
        E.arrow(d, 760, 1080, 520, 1080, E.AMB, 8, 26)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 0.8), ("click", s[1] + 0.6), ("zip", s[2] + 0.5), ("pop", s[3] + 0.6),
            ("click", s[4] + 0.8), ("pop", s[5] + 0.8), ("whoosh", s[6] + 0.4, 1.0)]
