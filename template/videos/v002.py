"""Video 002 — ¿Por qué un termo mantiene el café caliente?
Physics: heat leaves by conduction, convection and radiation. A vacuum flask has a double wall
with (near) vacuum between them -> blocks conduction and convection; reflective (silvered) walls
reflect radiant heat; the stopper closes the top. Works the same for cold drinks.
"""
import math

ID = "002"
TITLE = "¿Por qué un termo mantiene el café caliente?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
VOICE = "em_alex"; SPEED = 1.08
LINES = [
    "¿Por qué un termo mantiene el café caliente durante horas?",
    "El calor escapa de tres formas: por contacto, por el aire que circula y por radiación.",
    "El termo tiene dos paredes, y entre ellas casi no hay aire: hay vacío.",
    "Sin partículas en medio, el calor no puede pasar por contacto ni con corrientes de aire.",
    "Además, las paredes son brillantes y reflejan el calor radiante hacia dentro.",
    "Y el tapón cierra la salida de arriba.",
    "Por eso también funciona con bebidas frías: el calor de fuera no entra.",
    "Sígueme para ver cómo funcionan las cosas por dentro.",
]
KEYWORDS = {"termo", "caliente", "contacto", "aire", "radiación", "vacío", "paredes", "brillantes", "reflejan", "tapón", "frías", "dentro"}

COFFEE, COFFEE_D = (150, 86, 44), (105, 58, 28)
ICE_BLUE, ICE_BLUE_D = (70, 140, 220), (40, 95, 170)

def thermos(E, d, cx=540, top=470, bot=1130, liquid=COFFEE, liquid_d=COFFEE_D, cap_dy=0.0, shiny=0.0, gap_mark=False):
    """Cutaway vacuum flask. Outer wall, vacuum gap, inner (silvered) wall, liquid, stopper."""
    ow, iw = 220, 178  # half widths
    E.rrect(d, cx - ow, top, cx + ow, bot, 70, (52, 66, 98), outline=E.SIL_D, w=4)          # outer wall
    E.rrect(d, cx - ow + 12, top + 12, cx + ow - 12, bot - 12, 60, (14, 20, 34))              # vacuum gap (dark)
    if gap_mark:
        for k in range(7):  # a few sparse dots: "casi no hay aire"
            yy = top + 90 + k * 85
            E.circle(d, cx - ow + 21, yy, 3, fill=(80, 95, 125)); E.circle(d, cx + ow - 21, yy + 40, 3, fill=(80, 95, 125))
    wall = E.mix(E.SIL, E.WHITE, shiny)
    E.rrect(d, cx - iw, top + 40, cx + iw, bot - 36, 52, wall, outline=E.SIL_D, w=3)         # inner silvered wall
    E.rrect(d, cx - iw + 12, top + 130, cx + iw - 12, bot - 48, 44, liquid)                    # liquid
    E.rrect(d, cx - iw + 12, top + 130, cx + iw - 12, top + 150, 10, E.mix(liquid, E.WHITE, 0.25))
    # neck + stopper
    E.rrect(d, cx - 110, top - 30, cx + 110, top + 60, 18, (52, 66, 98), outline=E.SIL_D, w=4)
    cy = top - 95 + cap_dy
    E.rrect(d, cx - 125, cy, cx + 125, cy + 85, 22, E.AMB, outline=(200, 130, 10), w=4)
    E.rrect(d, cx - 95, cy + 85, cx + 95, cy + 125, 10, (230, 150, 20))

def steam(E, d, x, y, u, n=3, h=150, col=(200, 210, 225)):
    for k in range(n):
        ph = u * 3 + k * 2.1; xo = x + (k - 1) * 40
        pts = [(xo + 14 * math.sin(ph + s / 22), y - s - (u * 40 % 30)) for s in range(0, h, 6)]
        E.line(d, pts, col, 6)

def scene(i, u, L, E, im, d):
    cx = 540
    if i == 0:  # hook: flask + steaming cup + clock
        E.rrect(d, 250, 470, 530, 1130, 80, E.BLUE, outline=E.BLUE_D, w=5)
        E.rrect(d, 290, 360, 490, 470, 26, E.AMB, outline=(200, 130, 10), w=4)
        E.rrect(d, 600, 900, 860, 1130, 30, E.WHITE, outline=E.SIL_D, w=4)               # cup
        d.arc(E.P(830, 950, 930, 1060), 270, 90, fill=E.WHITE, width=16 * E.S)
        E.rrect(d, 615, 915, 845, 960, 20, COFFEE)
        steam(E, d, 730, 880, u)
        # clock
        E.circle(d, 760, 560, 110, fill=(30, 44, 72), outline=E.AMB, w=8)
        a = u * 4.0
        E.line(d, [(760, 560), (760 + 80 * math.sin(a), 560 - 80 * math.cos(a))], E.WHITE, 9)
        E.line(d, [(760, 560), (760 + 50 * math.sin(a / 12), 560 - 50 * math.cos(a / 12))], E.AMB, 11)
        E.circle(d, 760, 560, 12, fill=E.AMB)
        if u > 0.8: E.pill(d, "HORAS DESPUÉS…", 760, 735, 34)
    elif i == 1:  # three ways heat escapes
        rows = [(430, "CONTACTO"), (720, "AIRE"), (1010, "RADIACIÓN")]
        for r, (y, name) in enumerate(rows):
            k = E.back_out((u - r * (L / 3.4)) / 0.4)
            if k <= 0.02: continue
            E.label(d, name, 250, y, 52)
            if r == 0:  # conduction: chain of particles, heat travels particle to particle
                for j in range(5):
                    heat = max(0.0, 1 - abs(((u * 1.6) % 5) - j))
                    col = E.mix((90, 110, 150), E.HOT, heat if j else 1)
                    jit = 6 * heat * math.sin(u * 40 + j)
                    E.circle(d, 520 + j * 105 + jit, y, 38, fill=col, outline=E.BG1, w=3)
            elif r == 1:  # convection: circulating loop
                d.arc(E.P(560, y - 120, 920, y + 120), 0, 360, fill=(90, 110, 150), width=10 * E.S)
                for j in range(3):
                    a = u * 2.2 + j * 2.09
                    px, py = 740 + 180 * math.cos(a), y + 120 * math.sin(a)
                    E.arrow(d, px + 40 * math.sin(a), py - 30 * math.cos(a), px, py, color=E.HOT, w=10, head=40)
            else:  # radiation: waves from a hot source
                E.circle(d, 560, y, 50, fill=E.HOT, outline=E.HOT_D, w=4)
                for j, ang in enumerate((-0.5, 0.0, 0.5)):
                    ln = 140 + 120 * E.ease((u * 1.2 + j * 0.3) % 1)
                    E.wave(d, 620, y + 60 * ang, 620 + ln, y + 60 * ang + ln * ang * 0.6, 40, 12, E.HOT, w=6, phase=u * 10)
    elif i == 2:  # cutaway reveal: double wall + vacuum
        thermos(E, d, gap_mark=True)
        if u > 0.5:
            E.label(d, "DOBLE", 145, 640, 46); E.label(d, "PARED", 145, 690, 46)
            E.arrow(d, 210, 720, 310, 760, w=5)
        if u > L * 0.55:
            E.label(d, "VACÍO", 935, 820, 54); E.arrow(d, 905, 860, 757, 900, w=5)
    elif i == 3:  # zoomed wall section: conduction & convection blocked
        E.rrect(d, 70, 360, 420, 1130, 20, COFFEE)                                             # hot coffee
        E.rrect(d, 420, 360, 460, 1130, 6, E.SIL, outline=E.SIL_D, w=2)                        # inner wall
        E.rrect(d, 460, 360, 650, 1130, 0, (14, 20, 34))                                       # vacuum
        E.rrect(d, 650, 360, 690, 1130, 6, (52, 66, 98), outline=E.SIL_D, w=2)                 # outer wall
        for j in range(16):  # agitated hot particles
            px = 110 + (j * 97) % 280 + 10 * math.sin(u * 30 + j); py = 400 + (j * 211) % 700 + 10 * math.cos(u * 27 + j * 2)
            E.circle(d, px, py, 16, fill=E.HOT)
        for j in range(8):  # calm outside air
            px = 760 + (j * 83) % 240 + 3 * math.sin(u * 6 + j); py = 420 + (j * 173) % 650
            E.circle(d, px, py, 14, fill=(90, 110, 150))
        E.label(d, "VACÍO", 555, 330, 46)
        if u > 0.6:
            E.arrow(d, 300, 620, 520, 620, color=E.HOT, w=10); E.cross(d, 555, 620, 34)
            E.label(d, "CONTACTO", 250, 560, 40, color=E.WHITE)
        if u > L * 0.5:
            d.arc(E.P(250, 800, 520, 1000), 200, 340, fill=E.HOT, width=10 * E.S)
            E.arrow(d, 500, 870, 522, 905, color=E.HOT, w=10); E.cross(d, 555, 900, 34)
            E.label(d, "AIRE", 250, 1050, 40, color=E.WHITE)
    elif i == 4:  # radiation reflected by shiny walls
        shine = E.ease(u / 0.8)
        thermos(E, d, shiny=shine)
        for j, (yy, side) in enumerate(((660, -1), (780, 1), (900, -1), (1010, 1))):
            ph = (u * 0.8 + j * 0.25) % 1.0
            wx = cx + side * 160
            if ph < 0.5:  # travelling out to the wall
                x1 = cx - side * 60 + side * (220 * ph / 0.5)
                E.wave(d, cx - side * 60, yy, x1, yy - 40 * ph, 46, 16, E.HOT, w=9, phase=u * 12)
            else:         # reflected back inside by the shiny wall
                q = (ph - 0.5) / 0.5
                E.circle(d, wx, yy - 20, 22 * (1 - q) + 4, fill=E.WHITE)
                E.wave(d, wx, yy - 20, wx - side * 220 * q, yy - 20 - 50 * q, 46, 16, E.AMB, w=9, phase=u * 12)
        if u > 0.6:
            E.label(d, "PAREDES", 150, 560, 44); E.label(d, "BRILLANTES", 150, 610, 44)
            E.arrow(d, 150, 640, 340, 700, w=5)
    elif i == 5:  # stopper closes the top
        dy = -260 * (1 - E.ease(u / 0.9))
        thermos(E, d, cap_dy=dy, shiny=1.0)
        if u < 0.9:
            E.wave(d, cx, 520, cx, 330, 40, 12, E.HOT, w=6, phase=u * 12)
        else:
            E.cross(d, cx, 300, 30)
        if u > 0.9:
            E.label(d, "TAPÓN", 870, 400, 56); E.arrow(d, 820, 420, 680, 400, w=5)
    elif i == 6:  # cold drink: outside heat cannot get in
        thermos(E, d, liquid=ICE_BLUE, liquid_d=ICE_BLUE_D, shiny=1.0)
        for j, (x0, y0) in enumerate(((90, 700), (990, 850), (90, 1000))):
            side = 1 if x0 < cx else -1
            ph = (u * 0.8 + j * 0.3) % 1
            reach = cx - side * 226
            if ph < 0.6:
                E.wave(d, x0, y0, x0 + (reach - x0) * ph / 0.6, y0, 44, 16, E.HOT, w=9, phase=u * 10)
            else:
                E.cross(d, reach - side * 30, y0, 26)
        for j in range(3):  # ice cubes
            x = 470 + j * 70; y = 680 + 40 * math.sin(u * 2 + j)
            E.rrect(d, x - 28, y - 28, x + 28, y + 28, 10, (215, 238, 255), outline=(150, 200, 240), w=3)
        E.pill(d, "TAMBIÉN EN FRÍO", cx, 330, 40, bg=E.COLD)
    else:
        E.outro(d, u)

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[2], 0.5), ("pop", s[3] + 0.6), ("pop", s[3] + 0.5 * (s[4] - s[3])), ("click", s[5] + 0.9), ("whoosh", s[7], 0.4)]
