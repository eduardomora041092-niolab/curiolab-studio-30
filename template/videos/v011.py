"""Video 011 — ¿Cómo calienta un microondas?
Mechanism (dielectric heating): a magnetron produces microwaves (invisible electromagnetic waves) that a
waveguide carries into the metal cooking cavity, where the walls reflect them until they are absorbed by the
food. Water molecules are polar: the oxygen side is slightly negative and the hydrogen side slightly
positive. The microwaves' electric field reverses billions of times per second, twisting the molecules back
and forth; as they jostle their neighbours that motion becomes heat. Air absorbs almost no microwave energy,
so it is not heated directly. Standing waves leave hotter and colder spots, so the turntable moves the food
through them. (Microwaves penetrate only a few cm — the "inside-out" myth is not claimed; no resonance claim;
the 2.45 GHz figure is not narrated.)
"""
import math

ID = "011"
TITLE = "¿Cómo calienta un microondas?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "Tu microondas calienta la comida sin calentar el aire.",
    "El magnetrón fabrica ondas invisibles: las microondas.",
    "Rebotan en las paredes de metal hasta llegar a la comida.",
    "Las moléculas de agua tienen un lado positivo y otro negativo.",
    "Las ondas las hacen girar de un lado a otro, miles de millones de veces por segundo.",
    "Al chocar con sus vecinas, ese movimiento se convierte en calor.",
    "El plato gira porque las ondas dejan zonas calientes y frías.",
    "Sígueme para ver cómo funcionan las cosas por dentro.",
]
KEYWORDS = {"microondas", "comida", "aire", "magnetrón", "ondas", "invisibles", "rebotan", "paredes", "metal",
            "moléculas", "agua", "positivo", "negativo", "girar", "segundo", "chocar", "vecinas", "calor",
            "plato", "gira", "calientes", "frías", "dentro"}

WAVE = (120, 220, 255)
O_COL, H_COL = (225, 70, 70), (235, 240, 245)
CAB, PANEL = (52, 62, 82), (40, 48, 66)
FOOD = (215, 120, 70)

def oven(E, d, glow=0.0):
    E.rrect(d, 60, 440, 1020, 1010, 30, CAB, outline=E.SIL, w=4)
    E.rrect(d, 100, 480, 740, 970, 14, E.CAV, outline=E.SIL_D, w=4)
    E.rrect(d, 770, 480, 990, 970, 14, PANEL)
    for k in range(3):
        E.rrect(d, 820, 790 + k * 55, 940, 825 + k * 55, 10, (70, 82, 104))
    # plate and bowl
    d.ellipse(E.P(190, 905, 650, 945), fill=(90, 104, 128))
    E.poly(d, [(320, 840), (520, 840), (495, 905), (345, 905)], fill=E.mix(FOOD, E.HOT, glow))
    d.ellipse(E.P(320, 828, 520, 852), fill=E.mix((235, 160, 110), E.HOT, glow))

def magnetron(E, d, hl=False):
    c = E.AMB if hl else E.SIL_D
    E.rrect(d, 830, 520, 930, 650, 14, (90, 96, 110), outline=c, w=4)
    for k in range(5):
        E.line(d, [(838, 540 + k * 24), (922, 540 + k * 24)], E.SIL_D, 4)
    E.rrect(d, 740, 545, 830, 595, 4, (78, 86, 100), outline=c, w=3)   # waveguide into the cavity

def molecule(E, d, x, y, th, s=1.0, signs=True):
    ro, rh = 44 * s, 26 * s
    for a in (th - math.radians(52), th + math.radians(52)):
        hx, hy = x + 58 * s * math.cos(a), y + 58 * s * math.sin(a)
        E.line(d, [(x, y), (hx, hy)], E.SIL, 8 * s)
        E.circle(d, hx, hy, rh, fill=H_COL)
    E.circle(d, x, y, ro, fill=O_COL)
    if signs:
        px, py = x + 92 * s * math.cos(th), y + 92 * s * math.sin(th)
        nx, ny = x - 70 * s * math.cos(th), y - 70 * s * math.sin(th)
        E.label(d, "+", px, py, int(54 * s), color=E.AMB)
        E.label(d, "−", nx, ny, int(54 * s), color=E.COLD)

def zoom_box(E, d):
    E.rrect(d, 100, 330, 980, 1160, 40, (18, 26, 44), outline=E.SIL_D, w=4)

def scene(i, u, L, E, im, d):
    if i == 0:  # food hot, air not heated
        oven(E, d, glow=E.ease(u / 1.2))
        for k in range(3):
            x = 370 + k * 50
            E.wave(d, x, 820, x, 700, 45, 10, E.HOT, w=6, phase=u * 9, head=False)
        for k in range(12):
            x = 140 + (k * 113) % 560; y = 520 + (k * 47) % 140
            E.circle(d, x, y, 8, fill=E.COLD)
        if u > 0.4: E.label(d, "COMIDA CALIENTE", 420, 1060, 42, color=E.HOT)
        if u > 1.0: E.label(d, "AIRE", 420, 395, 46, color=E.COLD)
    elif i == 1:  # magnetron makes microwaves
        oven(E, d); magnetron(E, d, True)
        p = E.ease(u / 1.0)
        E.wave(d, 860, 570, E.lerp(860, 520, p), 570, 50, 16, WAVE, w=6, phase=u * 10)
        if u > 0.3: E.label(d, "MAGNETRÓN", 880, 400, 44)
        if u > 1.0: E.label(d, "MICROONDAS", 420, 1060, 44, color=WAVE)
    elif i == 2:  # bounce off metal walls to the food
        oven(E, d); magnetron(E, d)
        pts = [(740, 570), (300, 480), (110, 660), (430, 860)]
        p = E.ease(u / (L * 0.7)) * 3
        for k in range(3):
            q = max(0.0, min(1.0, p - k))
            if q > 0:
                a, b = pts[k], pts[k + 1]
                E.wave(d, a[0], a[1], E.lerp(a[0], b[0], q), E.lerp(a[1], b[1], q), 40, 10, WAVE, w=5, phase=u * 10, head=(q < 1 or k == 2))
        for x, y in pts[1:3]:
            if p > pts.index((x, y)): E.circle(d, x, y, 14, outline=E.AMB, w=4)
        if u > 0.6: E.label(d, "PAREDES DE METAL", 540, 1060, 42)
    elif i == 3:  # water: positive and negative side
        zoom_box(E, d)
        k = E.back_out(u / 0.6)
        if k > 0.05: molecule(E, d, 540, 720, -math.pi / 2, 2.0 * k)
        if u > 0.6:
            E.label(d, "POSITIVO", 540, 400, 44, color=E.AMB)
            E.label(d, "NEGATIVO", 540, 1080, 44, color=E.COLD)
        if u > 1.0: E.label(d, "AGUA", 830, 720, 46, color=E.WHITE)
    elif i == 4:  # field flips, molecules twist back and forth
        zoom_box(E, d)
        sgn = math.sin(u * 7)
        for x in (300, 780):
            if sgn > 0: E.arrow(d, x, 1060, x, 420, color=WAVE, w=8, head=34)
            else: E.arrow(d, x, 420, x, 1060, color=WAVE, w=8, head=34)
        th = -math.pi / 2 + (0 if sgn > 0 else math.pi)
        tw = -math.pi / 2 + math.pi * (0.5 - 0.5 * math.copysign(min(1, abs(sgn) * 1.6), sgn))
        for (x, y) in ((540, 560), (540, 900)):
            molecule(E, d, x, y, tw, 1.1)
        if u > 0.8: E.pill(d, "MILES DE MILLONES / SEGUNDO", 540, 1110, 32)
    elif i == 5:  # collisions -> heat
        zoom_box(E, d)
        heat = E.ease(u / (L * 0.8))
        im_c = E.mix((18, 26, 44), (90, 30, 24), heat)
        E.rrect(d, 104, 334, 976, 1156, 38, im_c)
        pos = [(300, 480), (560, 450), (800, 520), (380, 700), (680, 720), (260, 930), (520, 960), (790, 920)]
        for k, (x, y) in enumerate(pos):
            j = 14 * math.sin(u * 13 + k * 1.7)
            molecule(E, d, x + j, y + 0.7 * j, u * 6 * (1 if k % 2 else -1) + k, 0.75, signs=False)
        if u > 0.5:
            for x in (440, 640):
                E.wave(d, x, 880, x, 820 - 60 * heat, 40, 9, E.HOT, w=6, phase=u * 9)
        if u > 0.9: E.label(d, "CALOR", 540, 600, 62, color=E.HOT)
    elif i == 6:  # turntable through hot and cold spots (top view)
        for r in range(4):
            for c in range(4):
                hot = (r + c) % 2 == 0
                E.circle(d, 210 + c * 220, 420 + r * 200, 80, fill=(120, 40, 34) if hot else (30, 60, 110))
        cx, cy = 540, 720
        E.circle(d, cx, cy, 330, outline=E.SIL, w=6)
        a0 = u * 1.6
        for k in range(3):
            a = a0 + k * 2 * math.pi / 3
            x, y = cx + 200 * math.cos(a), cy + 200 * math.sin(a)
            E.rrect(d, x - 50, y - 36, x + 50, y + 36, 14, FOOD)
        d.arc(E.P(cx - 380, cy - 380, cx + 380, cy + 380), 300, 350, fill=E.AMB, width=8 * E.S)
        E.arrow(d, cx + 380 * math.cos(math.radians(345)), cy + 380 * math.sin(math.radians(345)),
                cx + 380 * math.cos(math.radians(352)), cy + 380 * math.sin(math.radians(352)), color=E.AMB, w=8, head=30)
        if u > 0.5: E.label(d, "CALIENTE", 430, 1140, 38, color=E.HOT)
        if u > 0.5: E.label(d, "FRÍA", 650, 1140, 38, color=E.COLD)
        if u > 1.0: E.pill(d, "EL PLATO GIRA", 540, 315, 34)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("pop", s[0] + 0.5), ("whoosh", s[1] + 0.2, 0.8), ("click", s[2] + 0.6), ("click", s[2] + 1.2),
            ("pop", s[3] + 0.3), ("whoosh", s[4] + 0.3, 0.6), ("whoosh", s[5] + 0.4, 0.7), ("pop", s[6] + 0.5)]
