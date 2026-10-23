"""Video 013 — ¿Cómo sabe la tostadora cuándo parar?
Science: pushing the lever down lowers the bread carriage and compresses (stretches) a spring that wants to lift it.
In many modern pop-up toasters, an electromagnet holds the carriage down, and closing the lever also switches on
the heating elements (nichrome wires that glow red-hot and toast the bread by radiant heat).
A timer, set with the browning dial, counts the chosen time (electronic RC timer in modern toasters; older ones use
a bimetallic strip). When the time is up the timer cuts the current to the electromagnet, which releases the carriage;
the spring pulls it up, the switch opens and the elements turn off.
(No temperatures, timings or wattages are claimed; older bimetal designs are not described in the narration.)
"""
ID = "013"
TITLE = "¿Cómo sabe la tostadora cuándo parar?"
SUBTITLE = "ASÍ FUNCIONAN LAS COSAS"
LINES = [
    "Nadie la apaga, pero la tostadora salta sola.",
    "Al bajar la palanca, la bandeja tensa un muelle.",
    "Abajo, un electroimán la sujeta y se encienden las resistencias.",
    "Las resistencias se ponen al rojo y tuestan el pan.",
    "Un temporizador cuenta el tiempo que elegiste.",
    "Cuando se acaba, corta la corriente del electroimán y este suelta la bandeja.",
    "El muelle la sube, se apagan las resistencias y la tostada salta.",
    "Sígueme para descubrir cómo funcionan las cosas.",
]
KEYWORDS = {"tostadora", "salta", "sola", "palanca", "bandeja", "muelle", "electroimán", "sujeta", "resistencias",
            "rojo", "pan", "temporizador", "tiempo", "corriente", "suelta", "sube", "apagan", "tostada", "cosas"}

BODY, BODY_D = (196, 204, 216), (120, 130, 146)
BREAD, CRUST, TOAST = (236, 200, 140), (196, 140, 70), (170, 104, 44)
COIL = (176, 112, 60)
MAG = (90, 170, 255)

# Cut-away toaster: outer body x 200..880, y 470..1080; slot cavity x 330..750
X0, X1, Y0, Y1 = 200, 880, 470, 1080

def toaster(E, d, cut=True):
    E.rrect(d, X0, Y0, X1, Y1, 60, BODY, outline=BODY_D, w=6)
    E.rrect(d, X0 + 40, Y1 - 10, X0 + 120, Y1 + 30, 10, BODY_D)
    E.rrect(d, X1 - 120, Y1 - 10, X1 - 40, Y1 + 30, 10, BODY_D)
    if cut:
        E.rrect(d, 330, 500, 750, 1040, 20, E.CAV)
    # slot opening on top
    E.rrect(d, 360, Y0 - 6, 720, Y0 + 14, 8, (40, 46, 60))

def elements(E, d, glow):
    col = E.mix(COIL, E.HOT, glow)
    for x in (360, 720):
        pts = [(x + (14 if k % 2 else -14), 560 + k * 30) for k in range(16)]
        E.line(d, pts, col, 7)
        if glow > 0.5:
            E.line(d, pts, E.mix(col, (255, 200, 120), glow - 0.5), 3)

def carriage(E, d, ytop, toast=0.0):
    """ytop = top of the bread slice."""
    c = E.mix(BREAD, TOAST, toast)
    E.rrect(d, 430, ytop, 650, ytop + 320, 50, E.mix(CRUST, (120, 70, 30), toast))
    E.rrect(d, 448, ytop + 18, 632, ytop + 302, 40, c)
    # tray under the bread
    E.rrect(d, 410, ytop + 320, 670, ytop + 340, 6, E.SIL_D)

def lever(E, d, yl):
    E.line(d, [(X1, 600), (X1, 1000)], (60, 66, 80), 10)
    E.rrect(d, X1 - 10, yl - 26, X1 + 110, yl + 26, 18, E.SIL_H, outline=E.SIL_D, w=4)

def spring(E, d, ytray, top=520):
    # spring between top of body (anchor) and the tray arm on the right of the cavity
    x = 790; n = 12; pts = []
    for k in range(n + 1):
        y = E.lerp(top, ytray, k / n)
        pts.append((x + (0 if k in (0, n) else (22 if k % 2 else -22)), y))
    E.line(d, pts, E.AMB, 6)
    E.line(d, [(670, ytray), (x, ytray)], E.SIL_D, 8)

def magnet(E, d, on, x=790, y=990):
    E.rrect(d, x - 40, y - 30, x + 40, y + 30, 8, E.mix((70, 80, 100), MAG, 1 if on else 0.15))
    for k in range(4):
        E.line(d, [(x - 36 + k * 22, y - 30), (x - 30 + k * 22, y + 30)], (230, 120, 60), 4)
    if on:
        for r in (54, 72):
            d.arc(E.P(x - r, y - r, x + r, y + r), 200, 340, fill=MAG, width=4 * E.S)

def dial(E, d, x, y, r, frac):
    import math
    E.circle(d, x, y, r, fill=E.CAV, outline=E.SIL_H, w=6)
    a = -math.pi / 2 + 2 * math.pi * frac
    if frac > 0.002:
        d.pieslice(E.P(x - r + 10, y - r + 10, x + r - 10, y + r - 10), -90, -90 + 360 * frac, fill=E.AMB)
    E.line(d, [(x, y), (x + (r - 16) * math.cos(a), y + (r - 16) * math.sin(a))], E.WHITE, 6)

UP, DOWN = 300, 690   # bread top when up / down
TRAY_UP, TRAY_DOWN = UP + 330, DOWN + 330

def scene(i, u, L, E, im, d):
    if i == 0:  # pops by itself
        k = E.back_out((u - 0.5) / 0.5) if u > 0.5 else 0
        yb = E.lerp(DOWN, UP, k)
        toaster(E, d, cut=False)
        # bread peeking out of the top slot
        if yb < Y0 - 60:
            E.rrect(d, 430, yb, 650, Y0 + 10, 40, CRUST)
            E.rrect(d, 448, yb + 18, 632, Y0 + 10, 30, E.mix(BREAD, TOAST, 0.8))
        E.rrect(d, 360, Y0 - 6, 720, Y0 + 14, 8, (40, 46, 60))
        lever(E, d, 620 if k > 0.5 else 960)
        if k > 0.3:
            E.label(d, "¡CLIC!", 820, 360, 64, color=E.AMB)
        E.pill(d, "NADIE LA APAGA", 540, 1140, 38)
    elif i == 1:  # lever down -> spring stretched
        p = E.ease(u / (L * 0.6))
        yb = E.lerp(UP + 200, DOWN, p)
        toaster(E, d); elements(E, d, 0)
        spring(E, d, yb + 330); carriage(E, d, yb)
        lever(E, d, E.lerp(620, 960, p))
        E.arrow(d, 1000, 560, 1000, 900, color=E.WHITE, w=8)
        if u > 0.6: E.label(d, "MUELLE TENSO", 790, 420, 40, color=E.AMB)
    elif i == 2:  # electromagnet holds, elements on
        toaster(E, d); elements(E, d, E.ease(u / L) * 0.6)
        spring(E, d, TRAY_DOWN); carriage(E, d, DOWN)
        magnet(E, d, True)
        lever(E, d, 960)
        if u > 0.2: E.label(d, "ELECTROIMÁN", 790, 1130, 38, color=MAG)
        if u > 1.0: E.label(d, "RESISTENCIAS", 540, 400, 44, color=E.HOT)
    elif i == 3:  # elements red-hot toast the bread
        toaster(E, d); elements(E, d, 1.0)
        spring(E, d, TRAY_DOWN); carriage(E, d, DOWN, toast=E.ease(u / L) * 0.7)
        magnet(E, d, True); lever(E, d, 960)
        ph = u * 6
        for x0, x1 in ((380, 440), (700, 640)):
            for yy in (760, 880):
                E.wave(d, x0, yy, x1, yy, 24, 6, E.HOT, w=4, phase=ph)
        E.label(d, "AL ROJO", 540, 400, 54, color=E.HOT)
    elif i == 4:  # timer counts the chosen time
        frac = E.ease(u / L)
        dial(E, d, 340, 650, 170, 1 - frac)
        E.label(d, "TEMPORIZADOR", 340, 880, 42, color=E.AMB)
        # browning knob the user turned
        E.circle(d, 780, 650, 110, fill=E.SIL, outline=E.SIL_D, w=6)
        E.line(d, [(780, 650), (850, 590)], E.CAV, 14)
        for k, t in enumerate(("1", "2", "3", "4", "5")):
            import math
            a = math.radians(200 + k * 35)
            E.label(d, t, 780 + 150 * math.cos(a), 650 + 150 * math.sin(a), 36, color=E.WHITE)
        E.label(d, "TIEMPO ELEGIDO", 780, 880, 40, color=E.MUTED)
    elif i == 5:  # cuts current -> magnet releases
        off = u > L * 0.4
        toaster(E, d); elements(E, d, 1.0)
        spring(E, d, TRAY_DOWN); carriage(E, d, DOWN, toast=0.75)
        magnet(E, d, not off); lever(E, d, 960)
        # wire from timer to magnet
        dial(E, d, 110, 900, 50, 0.0 if off else 0.05)
        E.line(d, [(110, 950), (110, 1060), (790, 1060), (790, 1020)], E.AMB if not off else E.SIL_D, 6)
        if off:
            E.cross(d, 110, 1060, 26)
            E.label(d, "SIN CORRIENTE", 540, 400, 48, color=E.HOT)
            E.label(d, "SUELTA", 790, 1130, 40, color=MAG)
    elif i == 6:  # spring lifts, elements off, toast pops
        k = E.back_out(u / 0.45)
        yb = E.lerp(DOWN, UP, k)
        toaster(E, d); elements(E, d, max(0, 1 - u * 1.5))
        spring(E, d, yb + 330); carriage(E, d, yb, toast=0.75)
        magnet(E, d, False); lever(E, d, E.lerp(960, 620, min(1, k)))
        E.arrow(d, 1000, 900, 1000, 560, color=E.AMB, w=8)
        if u > 0.6: E.pill(d, "¡LISTA!", 540, 1140, 40)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("pop", s[0] + 0.6), ("click", s[1] + 0.8), ("whoosh", s[2] + 0.3, 0.6), ("whoosh", s[3] + 0.2, 1.2),
            ("click", s[4] + 0.3), ("click", s[5] + 1.2), ("pop", s[6] + 0.2), ("whoosh", s[6] + 0.3, 0.6)]
