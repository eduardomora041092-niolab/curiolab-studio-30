"""Video 080 — ¿Cómo funciona un sacacorchos de alas?
Science: a wing (double-lever) corkscrew is a rack-and-pinion mechanism. The central shaft carries teeth (the rack);
at the base of each wing there is a toothed wheel (pinion) meshing with it. The body rests on the bottle neck; turning
the handle screws the spiral (worm) into the cork, so the shaft moves down relative to the body, turning both
pinions and raising the wings. Pushing the wings down turns the pinions back, which drives the rack (and the cork
attached to the worm) upward. The long wings act as levers, so a small push on them becomes a larger pull on the cork.
(No force ratio is claimed.)
"""
import math

ID = "080"
TITLE = "¿Cómo funciona un sacacorchos de alas?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Por qué suben solas las alas del sacacorchos?",
    "Al girar la manija, la espiral se clava en el corcho.",
    "El eje central tiene dientes, como una cremallera.",
    "Esos dientes engranan con una rueda dentada en la base de cada ala.",
    "Mientras la espiral baja, el eje gira las ruedas y las alas suben.",
    "Luego bajas las alas y las ruedas empujan el eje hacia arriba.",
    "Las alas son palancas largas: con poca fuerza sacas el corcho.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"alas", "sacacorchos", "manija", "espiral", "corcho", "eje", "dientes", "cremallera", "engranan",
            "rueda dentada", "ruedas", "suben", "bajas", "arriba", "palancas", "poca fuerza"}

CX = 540
PIV_Y = 610
PIV_DX = 62
WING_L = 270
BODY_TOP, BODY_BOT = 570, 860
GLASS = (40, 95, 70)
GLASS_H = (70, 140, 105)
CORK = (196, 150, 95)
CORK_D = (150, 108, 62)


def draw(E, d, k, cork_up=0.0, spin=0.0, hl_rack=False, hl_pinion=False, hl_worm=False, hl_wing=False):
    """k: 0 = wings down / shaft high, 1 = wings up / shaft low. cork_up: 0..1 how far the cork has been pulled."""
    handle_y = 340 + 190 * k
    worm_top = handle_y + 330
    worm_tip = worm_top + 210
    cork_top = 875 - 190 * cork_up
    # bottle
    E.rrect(d, 300, 1080, 780, 1300, 60, GLASS)
    E.rrect(d, 478, 860, 602, 1120, 16, GLASS)
    E.rrect(d, 470, 852, 610, 880, 8, GLASS_H)
    E.rrect(d, 494, 880, 586, 1110, 8, E.mix(GLASS, E.BG1, 0.4))
    # body (cut-away)
    E.rrect(d, 462, BODY_TOP, 618, BODY_BOT, 22, E.mix(E.SIL_D, E.BG1, 0.55), outline=E.SIL_D, w=4)
    # cork
    E.rrect(d, 494, cork_top, 586, cork_top + 165, 8, CORK)
    for j in range(4):
        E.circle(d, 515 + 18 * j, cork_top + 40 + 30 * (j % 2), 5, fill=CORK_D)
    # shaft (rack) + teeth
    E.rrect(d, CX - 18, handle_y, CX + 18, worm_top, 6, E.SIL)
    tcol = E.AMB if hl_rack else E.SIL_D
    for j in range(14):
        y = handle_y + 120 + j * 16
        if y > worm_top - 6:
            break
        E.rrect(d, CX - 30, y, CX - 18, y + 8, 2, tcol)
        E.rrect(d, CX + 18, y, CX + 30, y + 8, 2, tcol)
    # worm spiral
    pts = []
    for j in range(61):
        t = j / 60
        pts.append((CX + 24 * math.sin(t * 6 * 2 * math.pi + spin), worm_top + t * (worm_tip - worm_top)))
    E.line(d, pts, E.AMB if hl_worm else E.SIL_H, 7)
    # handle (cap)
    E.rrect(d, CX - 70, handle_y - 40, CX + 70, handle_y + 8, 20, E.SIL)
    for j in range(5):
        x = CX - 50 + 25 * j + 12 * math.sin(spin)
        if CX - 64 < x < CX + 64:
            E.line(d, [(x, handle_y - 34), (x, handle_y + 2)], E.SIL_D, 3)
    # wings with pinions
    for side in (-1, 1):
        px = CX + side * PIV_DX
        th = math.radians(115 + 130 * k) if side < 0 else math.radians(65 - 130 * k)
        ex, ey = px + WING_L * math.cos(th), PIV_Y + WING_L * math.sin(th)
        E.line(d, [(px, PIV_Y), (ex, ey)], E.AMB if hl_wing else E.SIL, 24)
        E.circle(d, ex, ey, 22, fill=E.AMB if hl_wing else E.SIL)
        # pinion
        gc = E.AMB if hl_pinion else E.BRA
        E.circle(d, px, PIV_Y, 34, fill=gc)
        for t in range(10):
            a = th + t * 2 * math.pi / 10
            E.circle(d, px + 38 * math.cos(a), PIV_Y + 38 * math.sin(a), 7, fill=gc)
        E.circle(d, px, PIV_Y, 10, fill=E.BG1)
    return handle_y, worm_top, worm_tip


def wing_end(k, side):
    px = CX + side * PIV_DX
    th = math.radians(115 + 130 * k) if side < 0 else math.radians(65 - 130 * k)
    return px + WING_L * math.cos(th), PIV_Y + WING_L * math.sin(th)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: handle turning, wings already rising
        k = 0.15 + 0.6 * min(1.0, u / max(0.5, L * 0.9))
        h, _, _ = draw(E, d, k, spin=u * 9)
        E.arrow(d, CX + 110, h - 60, CX - 110, h - 60, E.AMB, 6, 22)
        for side in (-1, 1):
            x, y = wing_end(k, side)
            E.arrow(d, x, y + 10, x, y - 60, E.AMB, 6, 22)
    elif i == 1:  # turning the handle drives the spiral into the cork
        k = 0.5 * E.ease(u / (L * 0.9))
        h, wt, tip = draw(E, d, k, spin=u * 9, hl_worm=True)
        E.arrow(d, CX + 110, h - 60, CX - 110, h - 60, E.AMB, 6, 22)
        E.label(d, "GIRAS", CX + 230, h - 60, 42, color=E.AMB)
        E.label(d, "ESPIRAL", 200, 980, 42, color=E.AMB)
        E.label(d, "CORCHO", 880, 960, 42, color=CORK)
    elif i == 2:  # rack: teeth on the central shaft
        draw(E, d, 0.5, hl_rack=True)
        E.label(d, "CREMALLERA", 820, 760, 42, color=E.AMB)
        E.arrow(d, 700, 760, 580, 760, E.AMB, 5, 20)
    elif i == 3:  # pinions at the base of each wing
        draw(E, d, 0.5, hl_rack=True, hl_pinion=True)
        E.label(d, "RUEDA", 230, 520, 42, color=E.AMB)
        E.label(d, "RUEDA", 850, 520, 42, color=E.AMB)
        E.arrow(d, 300, 545, 440, 595, E.AMB, 5, 20)
        E.arrow(d, 780, 545, 640, 595, E.AMB, 5, 20)
    elif i == 4:  # shaft goes down → pinions turn → wings rise
        k = 0.5 + 0.5 * E.ease(u / (L * 0.9))
        h, wt, tip = draw(E, d, k, spin=u * 9, hl_pinion=True)
        E.arrow(d, CX + 120, h + 20, CX + 120, h + 120, E.WHITE, 6, 22)
        for side in (-1, 1):
            x, y = wing_end(k, side)
            E.arrow(d, x + side * 40, y + 30, x + side * 40, y - 50, E.AMB, 6, 22)
        E.label(d, "EL EJE BAJA", 230, 960, 40, color=E.WHITE)
        E.label(d, "ALAS SUBEN", 850, 960, 40, color=E.AMB)
    elif i == 5:  # pushing wings down pulls the shaft (and the cork) up
        e = E.ease(u / (L * 0.9))
        k = 1.0 - e
        h, wt, tip = draw(E, d, k, cork_up=e, hl_wing=True)
        for side in (-1, 1):
            x, y = wing_end(k, side)
            E.arrow(d, x + side * 40, y - 50, x + side * 40, y + 30, E.AMB, 6, 22)
        E.arrow(d, CX + 120, h + 120, CX + 120, h + 20, E.WHITE, 6, 22)
        E.label(d, "BAJAS LAS ALAS", 220, 960, 38, color=E.AMB)
        E.label(d, "EL EJE SUBE", 860, 960, 38, color=E.WHITE)
    elif i == 6:  # levers: small push on the long wing, big pull on the cork
        draw(E, d, 0.0, cork_up=1.0)
        for side in (-1, 1):
            x, y = wing_end(0.0, side)
            E.arrow(d, x + side * 30, y - 70, x + side * 30, y - 10, E.AMB, 4, 18)
        E.label(d, "POCA FUERZA", 190, 790, 38, color=E.AMB)
        E.arrow(d, CX + 120, 700, CX + 120, 520, E.HOT, 12, 36)
        E.label(d, "MÁS FUERZA", 860, 480, 40, color=E.HOT)
        E.label(d, "PALANCAS", 880, 790, 40, color=E.WHITE)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("zip", s[0] + 0.2), ("whoosh", s[1] + 0.4, 0.8), ("click", s[2] + 0.6), ("pop", s[3] + 0.6),
            ("zip", s[4] + 0.5), ("whoosh", s[5] + 0.5, 0.8), ("pop", s[6] + 0.8)]
