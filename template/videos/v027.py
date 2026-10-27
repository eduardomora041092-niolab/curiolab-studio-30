"""Video 027 — ¿Por qué los gatos suelen caer de pie?
Science: cats have a righting reflex. The vestibular system of the inner ear (helped by vision) tells the cat which way
is up. In the air there is nothing to push against, so the cat bends at the waist and turns the two halves of its
body separately: it tucks in its front legs and twists the front half round a lot (the rear half turns a little the
other way, with legs extended), then tucks the rear legs and twists the rear half round. This lets it turn over
without pushing on anything, and it usually reaches the ground feet first, flexing its legs to cushion the landing.
(Side-view sketch; no heights, times or survival figures are claimed; "suele" because it does not always work.)
"""
import math

ID = "027"
TITLE = "¿Por qué los gatos suelen caer de pie?"
SUBTITLE = "CURIOSIDADES DE LA CIENCIA"
LINES = [
    "¿Por qué tu gato cae de pie al saltar?",
    "Su oído interno le indica en todo momento dónde está arriba.",
    "En el aire no tiene ningún sitio en el que apoyarse.",
    "Por eso dobla el cuerpo por la cintura.",
    "Recoge las patas delanteras y gira primero la mitad delantera.",
    "Después recoge las traseras y gira la mitad trasera.",
    "Así suele llegar al suelo con las patas abajo, amortiguando.",
    "Sígueme para más curiosidades de la ciencia.",
]
KEYWORDS = {"gato", "cae", "pie", "saltar", "oído", "interno", "arriba", "aire", "apoyarse", "dobla", "cuerpo",
            "cintura", "recoge", "patas", "delanteras", "gira", "delantera", "traseras", "trasera", "suelo", "abajo",
            "amortiguando", "ciencia"}

FUR, FUR_D, BELLY = (235, 150, 70), (190, 110, 45), (250, 225, 190)
SOFA, SOFA_D = (110, 90, 160), (80, 64, 120)
FLOOR = (90, 70, 55)

def rot(x, y, a):
    c, s = math.cos(a), math.sin(a); return x * c - y * s, x * s + y * c

def ell(cx, cy, a, b, ang=0.0, n=40):
    return [(cx + p[0], cy + p[1]) for p in (rot(a * math.cos(t), b * math.sin(t), ang) for t in (2 * math.pi * k / n for k in range(n)))]

def cat(E, d, cx, cy, pf, pb, bend=0.0, tf=0.0, tb=0.0, s=1.0, tilt=0.0, hl=None):
    """Side-view cat, facing right. pf/pb: roll of front/back half (0 = upright, pi = upside down).
    bend: V-bend at the waist (radians). tf/tb: how much front/back legs are tucked (0..1). hl: 'F' or 'B' outline."""
    def half(sign, phi, tuck, ang):
        hx, hy = rot(sign * 95 * s, 0, ang)
        hx += cx; hy += cy
        cphi = math.cos(phi)
        legL = 120 * s * (1 - 0.55 * tuck)
        for off in (-35, 35):
            ax, ay = rot(sign * (55 + off * 0.6) * s, 30 * s * cphi, ang)
            lx, ly = rot(sign * 25 * tuck * s, legL * cphi, ang)
            E.line(d, [(cx + ax, cy + ay), (cx + ax + lx, cy + ay + ly)], FUR_D, 24 * s)
        E.poly(d, ell(hx, hy, 110 * s, 62 * s, ang), fill=FUR)
        bx, by = rot(sign * 95 * s, 30 * s * cphi, ang)
        E.poly(d, ell(cx + bx, cy + by, 85 * s, max(6, 26 * s * abs(cphi)), ang), fill=BELLY if abs(cphi) > 0.15 else FUR)
        if hl == ("F" if sign > 0 else "B"):
            E.poly(d, ell(hx, hy, 118 * s, 70 * s, ang), outline=E.AMB, w=6)
        return cphi
    aF, aB = tilt - bend, tilt + bend
    half(-1, pb, tb, aB)
    tx, ty = rot(-200 * s, -10 * s, aB)
    tx2, ty2 = rot(-300 * s, -80 * s * math.cos(pb), aB)
    E.line(d, [(cx + tx, cy + ty), (cx + tx2, cy + ty2)], FUR_D, 20 * s)
    cphi = half(1, pf, tf, aF)
    hx, hy = rot(210 * s, -25 * s * cphi, aF)
    hx += cx; hy += cy
    for ex in (-28, 22):
        bx, by = rot(ex * s, -48 * s * cphi, aF)
        tx_, ty_ = rot((ex + 6) * s, -95 * s * cphi, aF)
        cx2, cy2 = rot((ex + 30) * s, -48 * s * cphi, aF)
        E.poly(d, [(hx + bx, hy + by), (hx + tx_, hy + ty_), (hx + cx2, hy + cy2)], fill=FUR_D)
    E.circle(d, hx, hy, 58 * s, fill=FUR)
    ex_, ey_ = rot(26 * s, -10 * s * cphi, aF)
    E.circle(d, hx + ex_, hy + ey_, 8 * s, fill=E.BG1)
    return hx, hy

def arc(E, d, cx, cy, r, a0, a1, color, w=8):
    pts = [(cx + r * math.cos(E.lerp(a0, a1, k / 20)), cy + r * math.sin(E.lerp(a0, a1, k / 20))) for k in range(21)]
    E.line(d, pts[:-2], color, w)
    E.arrow(d, pts[-3][0], pts[-3][1], pts[-1][0], pts[-1][1], color=color, w=w, head=28)

def scene(i, u, L, E, im, d):
    if i == 0:  # everyday + in action from frame 0: the cat has already jumped off the sofa and is turning in the air
        E.rrect(d, 60, 640, 380, 760, 30, SOFA); E.rrect(d, 60, 760, 380, 1060, 20, SOFA_D)
        E.rrect(d, 40, 1060, 1040, 1100, 8, FLOOR)
        t = min(1.0, 0.15 + u / (L * 0.85))
        x = E.lerp(330, 760, t); y = 600 + (1060 - 600 - 140) * t * t - 160 * math.sin(math.pi * t) * (1 - t)
        r = E.ease(t / 0.8)
        cat(E, d, x, y, math.pi * 0.85 * (1 - r), math.pi * 0.85 * (1 - E.ease((t - 0.15) / 0.75)), s=0.62,
            tilt=-0.25 * (1 - r))
        E.pill(d, "¡AL SALTAR!", 760, 420, 42)
    elif i == 1:  # inner ear tells which way is up
        a = math.sin(u * 2.2) * 0.9
        hx, hy = 540, 760
        for ex in (-1, 1):
            p = [rot(ex * 70, -150, a), rot(ex * 150, -270, a), rot(ex * 170, -110, a)]
            E.poly(d, [(hx + q[0], hy + q[1]) for q in p], fill=FUR_D)
        E.circle(d, hx, hy, 220, fill=FUR)
        ix, iy = rot(150, -10, a)
        E.circle(d, hx + ix, hy + iy, 58, fill=(255, 235, 200), outline=E.AMB, w=6)
        pts = [(hx + ix + (8 + 3.2 * k) * math.cos(k * 0.5), hy + iy + (8 + 3.2 * k) * math.sin(k * 0.5)) for k in range(14)]
        E.line(d, pts, E.HOT, 5)
        for ex in (-70, 70):
            qx, qy = rot(ex, -40, a); E.circle(d, hx + qx, hy + qy, 16, fill=E.BG1)
        E.arrow(d, 900, 900, 900, 470, color=E.AMB, w=10, head=34)
        E.label(d, "ARRIBA", 900, 420, 44, color=E.AMB)
        E.label(d, "OÍDO INTERNO", 420, 1110, 46, color=E.WHITE)
    elif i == 2:  # nothing to push against in the air
        y = 620 + 60 * math.sin(u * 1.5)
        cat(E, d, 540, y, math.pi, math.pi, s=0.95)
        for k in range(5):
            x = 300 + 120 * k; f = (u * 1.2 + k * 0.2) % 1
            E.line(d, [(x, 900 - 300 * f), (x, 960 - 300 * f)], E.MUTED, 4)
        E.label(d, "SIN APOYO", 540, 1080, 56, color=E.AMB)
    elif i == 3:  # it bends at the waist
        b = 0.42 * E.ease(u / (L * 0.6))
        cat(E, d, 540, 720, math.pi, math.pi, bend=b, s=0.95)
        E.circle(d, 540, 720, 26, outline=E.AMB, w=6)
        E.pill(d, "CINTURA", 540, 1050, 44)
    elif i == 4:  # tuck front legs, the front half turns (rear turns a little the other way)
        k = E.ease(u / (L * 0.8))
        cat(E, d, 540, 720, math.pi * (1 - k), math.pi + 0.35 * k, bend=0.42, tf=1.0, tb=0.0, s=0.95, hl="F")
        arc(E, d, 700, 640, 190, -2.3, -0.2 + 1.4 * k, E.AMB)
        E.pill(d, "MITAD DELANTERA", 540, 1100, 40)
    elif i == 5:  # tuck rear legs, the rear half turns
        k = E.ease(u / (L * 0.8))
        cat(E, d, 540, 720, 0.0, (math.pi + 0.35) * (1 - k), bend=0.42 * (1 - k), tf=0.0, tb=1.0, s=0.95, hl="B")
        arc(E, d, 380, 720, 190, -2.0, -0.6 + 1.2 * k, E.AMB)
        E.pill(d, "MITAD TRASERA", 540, 1100, 40)
    elif i == 6:  # lands feet first, flexing the legs to cushion
        E.rrect(d, 40, 1020, 1040, 1060, 8, FLOOR)
        t = min(1.0, u / (L * 0.45))
        y = E.lerp(560, 840, t * t)
        sq = 0.0 if t < 1 else 0.35 * math.sin(min(math.pi, (u - L * 0.45) * 5))
        cat(E, d, 540, y + 60 * sq, 0.0, 0.0, tf=0.3 + sq, tb=0.3 + sq, s=0.95)
        E.label(d, "PATAS ABAJO", 540, 420, 54, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.05, 1.4), ("pop", s[1] + 0.6), ("whoosh", s[2] + 0.2, 1.0), ("click", s[3] + 0.8),
            ("whoosh", s[4] + 0.3, 1.4), ("whoosh", s[5] + 0.3, 1.4), ("pop", s[6] + 1.2)]
