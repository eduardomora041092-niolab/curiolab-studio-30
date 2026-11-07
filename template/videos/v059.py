"""Video 059 — ¿Por qué gira el brazo del lavavajillas?
Science: the dishwasher pump pushes water under pressure into the spray arms, which are hollow and turn freely on a
central hub. The water leaves through small nozzles. Some nozzles, especially near the ends, point sideways, in
opposite directions at each end. Pushing a jet of water one way pushes the arm the other way (action and reaction,
Newton's third law), so the arm spins without a motor of its own and its jets sweep the whole rack.
(No pressures, flow rates, speeds or numbers of nozzles are claimed.)
"""
import math

ID = "059"
TITLE = "¿Por qué gira el brazo del lavavajillas?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Por qué gira el brazo del lavavajillas sin motor propio?",
    "Una bomba empuja agua dentro del brazo, que está hueco.",
    "El agua sale a presión por pequeños agujeros.",
    "En cada extremo, algunos agujeros apuntan hacia un lado.",
    "Al lanzar el agua hacia atrás, el brazo recibe un empujón hacia delante.",
    "Es acción y reacción, como un globo que se desinfla.",
    "Así gira y reparte el agua por toda la vajilla.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"gira", "brazo", "lavavajillas", "motor", "bomba", "agua", "hueco", "presión", "agujeros",
            "extremo", "lado", "atrás", "empujón", "delante", "acción", "reacción", "globo", "reparte", "vajilla"}

CX, CY = 540, 700
R = 380
WATER = (120, 190, 255)
ARM = (200, 206, 216)


def arm_top(E, d, th, jets=0.0, hi_ends=False, hi_holes=False, push=False, t=0.0):
    """Top view of the arm rotating about (CX, CY). Positive th turns clockwise on screen."""
    c, s = math.cos(th), math.sin(th)
    nx, ny = -s, c                         # perpendicular (direction of motion at the +end)
    w = 44
    p1 = (CX + R * c, CY + R * s); p2 = (CX - R * c, CY - R * s)
    E.poly(d, [(p1[0] + nx * w, p1[1] + ny * w), (p1[0] - nx * w, p1[1] - ny * w),
               (p2[0] - nx * w, p2[1] - ny * w), (p2[0] + nx * w, p2[1] + ny * w)], fill=ARM, outline=E.SIL_D, w=4)
    E.circle(d, p1[0], p1[1], w, fill=ARM, outline=E.SIL_D, w=4)
    E.circle(d, p2[0], p2[1], w, fill=ARM, outline=E.SIL_D, w=4)
    E.circle(d, CX, CY, 58, fill=E.SIL_D, outline=E.SIL_H, w=4)
    E.circle(d, CX, CY, 18, fill=E.SIL_H)
    # holes along the arm
    for f in (0.3, 0.5, 0.7):
        for sg in (1, -1):
            E.circle(d, CX + sg * R * f * c, CY + sg * R * f * s, 9, fill=E.AMB if hi_holes else (60, 70, 90))
    # side-pointing nozzles at the ends: jet goes opposite to the motion
    for sg in (1, -1):
        ex, ey = CX + sg * R * 0.9 * c, CY + sg * R * 0.9 * s
        jx, jy = -sg * nx, -sg * ny       # jet direction (backwards)
        E.circle(d, ex, ey, 13, fill=E.AMB if hi_ends else (60, 70, 90), outline=E.AMB, w=3)
        if jets > 0:
            for k in range(5):
                q = (t * 2.0 + k / 5) % 1.0
                L = 30 + 150 * q * jets
                E.circle(d, ex + jx * L, ey + jy * L, 9 - 5 * q, fill=WATER)
        if push:
            E.arrow(d, ex - jx * 20, ey - jy * 20, ex - jx * 130, ey - jy * 130, E.AMB, 9, 28)


def side(E, d, flow=None, spray=0.0, hi_pump=False, t=0.0):
    """Side view: pump below, pipe up to the hub, hollow arm, water inside and jets going up."""
    E.rrect(d, 120, 1060, 960, 1080, 6, (70, 80, 100))                   # tub floor
    E.rrect(d, 430, 960, 650, 1060, 18, E.AMB if hi_pump else E.BLUE, outline=E.BLUE_D, w=4)   # pump
    if hi_pump:
        E.label(d, "BOMBA", 800, 1010, 46, color=E.AMB)
    else:
        E.label(d, "BOMBA", 540, 1010, 40, color=E.WHITE)
    E.rrect(d, 505, 760, 575, 960, 10, E.SIL_D)                           # pipe
    E.rrect(d, 150, 700, 930, 770, 26, ARM, outline=E.SIL_D, w=4)         # arm (section)
    E.rrect(d, 170, 718, 910, 752, 14, (40, 50, 70))                      # hollow inside
    holes = [250, 360, 450, 630, 720, 830]
    for x in holes:
        E.rrect(d, x - 8, 696, x + 8, 706, 3, (40, 50, 70))
    if flow is not None:
        for k in range(10):          # rising in the pipe
            q = (flow + k / 10) % 1.0
            E.circle(d, 540, 950 - q * 200, 10, fill=WATER)
        for k in range(14):          # spreading inside the arm
            q = (flow + k / 14) % 1.0
            sg = 1 if k % 2 else -1
            E.circle(d, 540 + sg * q * 360, 735, 9, fill=WATER)
    if spray > 0:
        for x in holes:
            for k in range(4):
                q = (t * 1.8 + k / 4 + x / 300) % 1.0
                E.circle(d, x + 6 * math.sin(7 * q + x), 690 - q * 330 * spray, 9 - 4 * q, fill=WATER)


def balloon(E, d, u, L):
    k = min(1.0, u / L)
    bx = 320 + 420 * E.ease(k)
    r = 120 - 40 * k
    E.circle(d, bx, 600, r, fill=E.HOT, outline=E.HOT_D, w=4)
    E.poly(d, [(bx - r + 6, 600), (bx - r - 26, 580), (bx - r - 26, 620)], fill=E.HOT_D)
    for j in range(5):
        q = ((u * 2) + j / 5) % 1.0
        E.circle(d, bx - r - 40 - q * 160, 600 + 20 * math.sin(9 * q + j), 10 - 5 * q, fill=(220, 230, 245))
    E.arrow(d, bx - r - 60, 760, bx - r - 220, 760, WATER, 8, 26)
    E.label(d, "AIRE", bx - r - 140, 830, 40, color=WATER)
    E.arrow(d, bx + r + 20, 760, bx + r + 170, 760, E.AMB, 8, 26)
    E.label(d, "GLOBO", bx + r + 95, 830, 40, color=E.AMB)


def scene(i, u, L, E, im, d):
    th0 = 0.35
    if i == 0:  # in action from frame 0: arm already spinning with jets
        arm_top(E, d, th0 + u * 1.6, jets=1.0, t=u + 0.3)
        E.pill(d, "SIN MOTOR", 540, 1130, 44)
    elif i == 1:  # pump pushes water into the hollow arm
        side(E, d, flow=u * 0.9 + 0.2, hi_pump=True)
        E.label(d, "HUECO", 540, 620, 50, color=E.AMB)
        E.arrow(d, 640, 640, 760, 715, E.AMB, 7, 24)
    elif i == 2:  # water leaves through small holes under pressure
        side(E, d, flow=u * 0.9, spray=1.0, t=u)
        E.label(d, "AGUJEROS", 800, 860, 48, color=E.AMB)
        E.arrow(d, 800, 820, 830, 720, E.AMB, 7, 24)
    elif i == 3:  # end nozzles point sideways
        arm_top(E, d, th0, jets=0.6, hi_ends=True, t=u)
        E.label(d, "HACIA UN LADO", 540, 330, 48, color=E.AMB)
    elif i == 4:  # water thrown backwards -> arm pushed forwards
        k = E.ease(min(1.0, u / L))
        arm_top(E, d, th0 + 0.6 * k, jets=1.0, push=True, t=u)
        E.label(d, "AGUA", 300, 330, 44, color=WATER)
        E.label(d, "EMPUJÓN", 790, 330, 44, color=E.AMB)
    elif i == 5:  # action-reaction, like a balloon
        balloon(E, d, u, L)
        E.label(d, "ACCIÓN", 300, 400, 48, color=WATER)
        E.label(d, "REACCIÓN", 780, 400, 48, color=E.AMB)
    elif i == 6:  # it spins and spreads the water over the dishes
        arm_top(E, d, th0 + u * 2.2, jets=1.0, t=u)
        for k in range(10):
            a = k * 2 * math.pi / 10
            E.rrect(d, CX + 470 * math.cos(a) - 18, CY + 470 * math.sin(a) * 0.85 - 18,
                    CX + 470 * math.cos(a) + 18, CY + 470 * math.sin(a) * 0.85 + 18, 18, (90, 100, 125))
        E.pill(d, "TODA LA VAJILLA", 540, 1140, 40)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 0.8), ("zip", s[1] + 0.5), ("pop", s[2] + 0.6), ("click", s[3] + 0.8),
            ("whoosh", s[4] + 0.5, 0.9), ("pop", s[5] + 0.7), ("whoosh", s[6] + 0.4, 1.0)]
