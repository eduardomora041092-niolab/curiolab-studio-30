"""Video 026 — ¿Cómo frena un coche con frenos de disco?
Mechanism: the brake pedal is a lever that pushes a piston in the master cylinder. The brake fluid is practically
incompressible, so the pressure is transmitted through the brake lines to the wheels. At each wheel a caliper
straddles a disc (rotor) that turns with the wheel. The fluid pressure pushes the caliper piston(s), which press two
pads against both faces of the disc. Friction between pads and disc slows the disc and therefore the wheel. The
kinetic energy of the car is converted into heat, so the disc and pads get hot.
(Simplified drawings; no pressures, temperatures, forces or masses are claimed; booster and ABS are not shown.)
"""
import math

ID = "026"
TITLE = "¿Cómo frena un coche con frenos de disco?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo frena un coche con frenos de disco?",
    "Al pisar el pedal, empujas un pistón con líquido.",
    "El líquido no se comprime y lleva la presión a la rueda.",
    "Allí, una pinza abraza un disco que gira con la rueda.",
    "La presión empuja dos pastillas contra las caras del disco.",
    "El rozamiento frena el disco, y con él la rueda.",
    "El movimiento se convierte en calor: el disco se calienta.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"frena", "coche", "frenos", "disco", "pisar", "pedal", "empujas", "pistón", "líquido", "comprime",
            "presión", "rueda", "pinza", "abraza", "gira", "pastillas", "caras", "rozamiento", "movimiento", "calor",
            "calienta", "funcionan"}

FLUID, FLUID_D = (90, 170, 255), (50, 110, 190)
DISC, DISC_D = (190, 196, 206), (130, 138, 150)
CAL = (220, 70, 50)
PAD = (90, 80, 70)
TIRE = (34, 34, 40)

def disc_front(E, d, cx, cy, r, ang, glow=0.0):
    E.circle(d, cx, cy, r + 70, fill=TIRE)
    E.circle(d, cx, cy, r + 70, outline=(60, 60, 70), w=6)
    col = E.mix(DISC, (255, 110, 40), glow)
    E.circle(d, cx, cy, r, fill=col, outline=DISC_D, w=4)
    E.circle(d, cx, cy, r * 0.42, fill=E.mix(DISC_D, (200, 80, 30), glow * 0.6))
    for k in range(5):
        a = ang + k * 2 * math.pi / 5
        E.circle(d, cx + r * 0.25 * math.cos(a), cy + r * 0.25 * math.sin(a), 14, fill=(60, 64, 74))
    for k in range(10):
        a = ang + k * 2 * math.pi / 10 + 0.3
        E.circle(d, cx + r * 0.72 * math.cos(a), cy + r * 0.72 * math.sin(a), 11, fill=E.mix(DISC_D, (150, 50, 20), glow))

def caliper_front(E, d, cx, cy, r, side="top", glow=0.0):
    if side == "top":
        E.rrect(d, cx - 150, cy - r - 40, cx + 150, cy - r + 110, 34, CAL)
        E.label(d, "", cx, cy - r, 10)
    else:
        E.rrect(d, cx + r - 110, cy - 150, cx + r + 40, cy + 150, 34, CAL)

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: the wheel is already spinning and starts to brake, pads glowing
        sp = 7.0 * (1 - E.ease(u / (L * 1.1)))
        ang = 7.0 * u - 3.5 * u * u / (L * 1.1)
        disc_front(E, d, 540, 760, 260, ang)
        caliper_front(E, d, 540, 760, 260, "top")
        for k in range(6):
            a = -math.pi / 2 + (k - 2.5) * 0.12
            f = (u * 3 + k * 0.17) % 1
            x0, y0 = 540 + 250 * math.cos(a), 760 + 250 * math.sin(a)
            E.line(d, [(x0, y0), (x0 + (60 + 80 * f) * math.cos(a + 1.4), y0 + (60 + 80 * f) * math.sin(a + 1.4))], (255, 200, 80), 5)
        for k in range(3):
            a = ang * 0.0 + math.pi * (0.15 + 0.3 * k)
            E.arrow(d, 540 + 380 * math.cos(a), 760 + 380 * math.sin(a), 540 + 380 * math.cos(a + 0.35 * min(1, sp / 3)),
                    760 + 380 * math.sin(a + 0.35 * min(1, sp / 3)), color=E.AMB, w=7, head=22)
    elif i == 1:  # pedal (lever) pushes the master-cylinder piston
        t = E.ease((u % 2.2) / 1.0) if (u % 2.2) < 1.0 else 1.0 - E.ease(((u % 2.2) - 1.4) / 0.8) if (u % 2.2) > 1.4 else 1.0
        pa = math.radians(-60 + 22 * t)
        px, py = 300, 450
        fx, fy = px + 420 * math.cos(-pa) * 0 + 420 * math.sin(math.radians(22 * t)), py + 420
        E.circle(d, px, py, 22, fill=E.SIL_H)
        ex, ey = px + 420 * math.sin(math.radians(12 + 22 * t)), py + 420 * math.cos(math.radians(12 + 22 * t))
        E.line(d, [(px, py), (ex, ey)], E.SIL_D, 26)
        E.rrect(d, ex - 20, ey - 50, ex + 60, ey + 50, 12, (60, 64, 74))
        E.poly(d, [(ex - 180, ey - 10), (ex - 10, ey - 60), (ex + 0, ey + 30), (ex - 200, ey + 70)], fill=(120, 80, 60))
        rx, ry = px + 160 * math.sin(math.radians(12 + 22 * t)), py + 160 * math.cos(math.radians(12 + 22 * t))
        cx0 = 640
        E.rrect(d, cx0, 520, 1000, 680, 20, E.SIL_D, outline=E.SIL_H, w=4)
        pist = cx0 + 40 + 120 * t
        E.rrect(d, pist + 30, 540, 980, 660, 12, FLUID)
        E.rrect(d, pist, 540, pist + 30, 660, 6, E.SIL_H)
        E.line(d, [(rx, ry), (pist, 600)], E.SIL_H, 12)
        E.label(d, "PEDAL", 200, 980, 48, color=E.WHITE)
        E.label(d, "PISTÓN", 820, 470, 44, color=E.WHITE)
        E.label(d, "LÍQUIDO", 820, 740, 44, color=FLUID)
    elif i == 2:  # incompressible fluid carries the pressure to the wheel
        E.rrect(d, 80, 520, 300, 680, 20, E.SIL_D, outline=E.SIL_H, w=4)
        E.rrect(d, 120, 540, 280, 660, 10, FLUID)
        pts = [(300, 600), (560, 600), (560, 860), (800, 860)]
        E.line(d, pts, FLUID_D, 40); E.line(d, pts, FLUID, 26)
        disc_front(E, d, 900, 860, 70, u * 2)
        f = (u * 0.9) % 1
        for k in range(4):
            g = (f + k / 4) % 1; s = g * 620
            if s < 260: x, y, dx, dy = 300 + s, 600, 1, 0
            elif s < 520: x, y, dx, dy = 560, 600 + (s - 260), 0, 1
            else: x, y, dx, dy = 560 + (s - 520), 860, 1, 0
            E.arrow(d, x - 30 * dx, y - 30 * dy, x + 30 * dx, y + 30 * dy, color=E.WHITE, w=6, head=20)
        E.pill(d, "NO SE COMPRIME", 540, 420, 42)
        E.label(d, "PRESIÓN", 330, 800, 50, color=E.AMB)
    elif i == 3:  # caliper straddles the disc that turns with the wheel
        disc_front(E, d, 500, 760, 280, u * 2.5)
        caliper_front(E, d, 500, 760, 280, "right")
        E.label(d, "PINZA", 880, 500, 50, color=CAL)
        E.label(d, "DISCO", 500, 1120, 50, color=E.WHITE)
        E.arrow(d, 500 + 330 * math.cos(2.4), 760 + 330 * math.sin(2.4), 500 + 330 * math.cos(2.9), 760 + 330 * math.sin(2.9),
                color=E.AMB, w=7, head=24)
    elif i == 4:  # section: pistons push two pads against both faces of the disc
        k = E.ease(u / (L * 0.5))
        E.rrect(d, 500, 380, 580, 1140, 10, DISC, outline=DISC_D, w=3)
        E.rrect(d, 230, 560, 850, 960, 40, CAL)
        E.rrect(d, 300, 600, 780, 920, 20, E.BG1)
        E.rrect(d, 500, 560, 580, 960, 0, DISC)
        gap = 70 * (1 - k)
        E.rrect(d, 440 - gap, 640, 496 - gap, 880, 8, PAD)
        E.rrect(d, 584 + gap, 640, 640 + gap, 880, 8, PAD)
        E.rrect(d, 330 - gap, 670, 440 - gap, 850, 10, E.SIL_H)
        E.rrect(d, 640 + gap, 670, 750 + gap, 850, 10, E.SIL_H)
        for sgn in (-1, 1):
            x = 540 + sgn * (300 + 40 * (1 - k))
            E.arrow(d, x, 760, x - sgn * 60, 760, color=FLUID, w=10, head=28)
        E.pill(d, "PASTILLAS", 540, 440, 42)
        E.label(d, "DISCO", 540, 1160, 40, color=E.WHITE)
    elif i == 5:  # friction slows the disc and the wheel
        ang = 4.0 * u - 1.8 * u * u / L
        disc_front(E, d, 540, 760, 280, ang)
        caliper_front(E, d, 540, 760, 280, "top")
        for k in range(5):
            a = -math.pi / 2 + (k - 2) * 0.1
            f = (u * 3 + k * 0.2) % 1
            x0, y0 = 540 + 270 * math.cos(a), 760 + 270 * math.sin(a)
            E.circle(d, x0 - 60 * f, y0 - 40 * f, 8, fill=(255, 200, 80))
        sp = max(0.15, 1 - u / L)
        E.arrow(d, 540 + 380 * math.cos(-1.0), 760 + 380 * math.sin(-1.0), 540 + 380 * math.cos(-1.0 + 0.6 * sp),
                760 + 380 * math.sin(-1.0 + 0.6 * sp), color=E.AMB, w=8, head=26)
        E.label(d, "ROZAMIENTO", 540, 1130, 54, color=E.AMB)
    elif i == 6:  # kinetic energy becomes heat: the disc gets hot
        g = E.ease(u / (L * 0.8))
        disc_front(E, d, 540, 760, 280, 0.3 + 0.2 * u * (1 - g), glow=g)
        caliper_front(E, d, 540, 760, 280, "top")
        for k in range(4):
            x = 360 + 120 * k
            E.wave(d, x, 420 + 30 * ((u + k * 0.3) % 1), x, 330, 60, 12, E.HOT, w=5, phase=u * 6 + k, head=False)
        E.label(d, "CALOR", 540, 1130, 60, color=E.HOT)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.05, 1.6), ("click", s[1] + 0.9), ("whoosh", s[2] + 0.3, 1.2), ("pop", s[3] + 0.6),
            ("click", s[4] + 0.8), ("whoosh", s[5] + 0.2, 1.2), ("pop", s[6] + 0.8)]
