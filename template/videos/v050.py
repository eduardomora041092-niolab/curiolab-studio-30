"""Video 050 — ¿Cómo mezcla agua fría y caliente un grifo monomando?
Science: a single-lever mixer tap contains a cartridge with two ceramic discs pressed against each other. The lower
disc is fixed and has one inlet for cold water and one for hot water. The upper disc is moved by the lever and has an
opening (mixing chamber) that connects the inlets to the outlet. Lifting the lever slides the upper disc so that more
of the inlet holes are uncovered: more flow. Turning the lever to one side or the other changes how much of the hot
and of the cold inlet is uncovered: the mix (temperature) changes. The discs are polished very smooth and flat, so they
seal against each other and stop the water when closed.
(No specific hole shapes, materials, pressures or which side is hot on every tap are claimed.)
"""
import math

ID = "050"
TITLE = "¿Cómo mezcla agua fría y caliente un grifo monomando?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo controla una sola palanca el chorro y la temperatura?",
    "Dentro del grifo hay un cartucho con dos discos de cerámica.",
    "El disco de abajo está fijo, con una entrada fría y otra caliente.",
    "El de arriba se mueve con la palanca y tiene una abertura.",
    "Al subir la palanca, la abertura destapa más agujero y sale más agua.",
    "Al girarla, destapa más el caliente o el frío y cambia la mezcla.",
    "Los discos son tan lisos que, al cerrar, no dejan pasar el agua.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"palanca", "chorro", "temperatura", "grifo", "cartucho", "discos", "cerámica", "fijo", "fría",
            "caliente", "abertura", "subir", "agujero", "agua", "girarla", "frío", "mezcla", "lisos", "cerrar"}

WATER = (110, 190, 255)
CER = (235, 230, 220)
CER_D = (190, 182, 168)


def tap(E, d, lift=0.5, turn=0.0, flow=1.0, u=0.0, mix=0.5):
    """Side view of a mixer tap: body, spout, lever; water stream coloured by mix (0 cold .. 1 hot)."""
    E.rrect(d, 470, 560, 610, 1120, 30, E.SIL)                        # body
    E.rrect(d, 380, 1110, 700, 1160, 16, E.SIL_D)                     # base
    E.rrect(d, 260, 600, 520, 660, 26, E.SIL)                         # spout
    E.rrect(d, 260, 640, 310, 690, 12, E.SIL_H)                       # aerator
    a = math.radians(-10 - 40 * lift)
    x0, y0 = 560, 560
    x1, y1 = x0 + 260 * math.cos(a), y0 + 260 * math.sin(a)
    E.line(d, [(x0, y0), (x1, y1)], E.SIL_H, 34)                     # lever
    E.circle(d, x1, y1, 22, fill=E.mix(E.HOT, E.COLD, 0.5 - turn * 0.5) if turn else E.SIL_H)
    if flow > 0.02:
        col = E.mix(E.COLD, E.HOT, mix)
        w = 10 + 30 * flow
        E.rrect(d, 285 - w / 2, 690, 285 + w / 2, 1100, int(w / 2), E.mix(E.BG1, col, 0.8))
        for j in range(6):
            f = (u * 1.6 + j / 6) % 1
            E.circle(d, 285, 700 + 400 * f, w / 3, fill=E.mix(col, E.WHITE, 0.4))


def lower_disc(E, d, cy=800):
    E.circle(d, 540, cy, 260, fill=CER, outline=CER_D, w=6)
    E.circle(d, 450, cy - 40, 62, fill=E.HOT)       # hot inlet (left)
    E.circle(d, 630, cy - 40, 62, fill=E.COLD)      # cold inlet (right)
    E.rrect(d, 400, cy + 150, 680, cy + 200, 20, E.BG1)  # outlet slot


def upper_disc(E, d, dx=0.0, dy=0.0, cy=800, alpha=0.75):
    """Upper disc drawn as a ring; its opening (window) shows the inlets below it."""
    ox, oy = 540 + dx, cy + 60 + dy
    E.circle(d, 540, cy, 268, outline=CER_D, w=10)
    # shade everything except the window, drawn as four rects around it
    win = (ox - 140, oy - 120, ox + 140, oy + 30)
    shade = E.mix(E.BG2, CER, alpha)
    X0, X1, Y0, Y1 = 330, 750, cy - 225, cy + 225
    wx0, wx1 = max(X0, win[0]), min(X1, win[2])
    wy0, wy1 = max(Y0, win[1]), min(Y1, win[3])

    def box(a, b, c, e, r=4):
        if c - a > 2 and e - b > 2:
            E.rrect(d, a, b, c, e, r, shade)
    box(X0, Y0, X1, wy0, 30)
    box(X0, wy1, X1, Y1, 30)
    box(X0, wy0, wx0, wy1)
    box(wx1, wy0, X1, wy1)
    E.rrect(d, *win, 30, None, outline=E.AMB, w=6)
    return win


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: lever moving, water already flowing and changing colour
        t = 0.5 + 0.5 * math.sin(u * 2.2)
        tap(E, d, lift=0.6, turn=0.0, flow=0.8, u=u, mix=t)
        E.pill(d, "UNA SOLA PALANCA", 620, 360, 42)
    elif i == 1:  # cartridge with two ceramic discs
        tap(E, d, lift=0.5, flow=0.0)
        E.rrect(d, 650, 760, 960, 1040, 26, E.mix(E.BG2, E.SIL, 0.35), outline=E.SIL_H, w=4)
        k = E.ease(min(1, u / (L * 0.5)))
        E.rrect(d, 690, 860 - 40 * k, 920, 900 - 40 * k, 10, CER, outline=CER_D, w=3)   # upper disc
        E.rrect(d, 690, 910, 920, 950, 10, CER, outline=CER_D, w=3)                   # lower disc
        E.line(d, [(560, 700), (680, 790)], E.AMB, 5)
        E.label(d, "CARTUCHO", 805, 720, 44, color=E.WHITE)
        E.label(d, "DISCOS DE CERÁMICA", 760, 1095, 38, color=E.AMB)
    elif i == 2:  # fixed lower disc with cold and hot inlets
        lower_disc(E, d)
        E.label(d, "CALIENTE", 410, 500, 44, color=E.HOT)
        E.label(d, "FRÍA", 680, 500, 44, color=E.COLD)
        E.arrow(d, 430, 530, 445, 760, E.HOT, 6, 22)
        E.arrow(d, 670, 530, 640, 760, E.COLD, 6, 22)
        E.label(d, "SALIDA", 540, 975, 34, color=E.WHITE)
        E.pill(d, "FIJO", 540, 1130, 40, bg=E.WHITE)
    elif i == 3:  # moving upper disc with opening, driven by lever
        dx = 30 * math.sin(u * 2)
        lower_disc(E, d); upper_disc(E, d, dx=dx, dy=0)
        E.label(d, "ABERTURA", 540 + dx, 1000, 44, color=E.AMB)
        E.pill(d, "SE MUEVE", 540, 1130, 40)
    elif i == 4:  # lift lever: window uncovers more of the holes -> more water
        k = E.ease(min(1, u / (L * 0.6)))
        lower_disc(E, d); upper_disc(E, d, dy=120 - 140 * k)
        E.arrow(d, 860, 900, 860, 740, E.AMB, 8, 28)
        E.label(d, "SUBE", 880, 960, 44, color=E.AMB)
        E.pill(d, "MÁS AGUA", 540, 1130, 40)
    elif i == 5:  # turn lever: window over hot or cold -> mix changes
        dx = -95 * math.sin(u * 1.8)
        lower_disc(E, d); upper_disc(E, d, dx=dx, dy=-20)
        side = "MÁS CALIENTE" if dx < 0 else "MÁS FRÍA"
        E.pill(d, side, 540, 1130, 40, bg=E.HOT if dx < 0 else E.COLD)
        E.arrow(d, 400, 470, 300, 470, E.AMB, 7, 24)
        E.arrow(d, 680, 470, 780, 470, E.AMB, 7, 24)
        E.label(d, "GIRA", 540, 470, 44, color=E.AMB)
    elif i == 6:  # smooth discs seal: closed, no water
        k = E.ease(min(1, u / (L * 0.5)))
        lower_disc(E, d); upper_disc(E, d, dy=40 + 110 * k, alpha=0.95)
        E.label(d, "MUY LISOS", 540, 470, 48, color=E.WHITE)
        E.pill(d, "CERRADO", 540, 1130, 40, bg=E.WHITE)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 1.2), ("pop", s[1] + 0.6), ("pop", s[2] + 0.6), ("zip", s[3] + 0.4, 0.8),
            ("whoosh", s[4] + 0.3, 1.0), ("zip", s[5] + 0.4, 1.0), ("click", s[6] + 0.8)]
