"""Video 083 — ¿Cómo sube el agua una bomba manual?
Science: a hand lift pump has a cylinder with a piston and two one-way (check) valves: a foot valve at the bottom of
the cylinder and a valve in the piston itself. A lever moves the piston: pushing the handle down raises the piston.
When the piston rises its valve is closed, so the pressure below it drops; the pressure of the air on the water in
the well then pushes water up the pipe through the foot valve. When the piston goes down, the foot valve closes (the
water cannot return to the well) and the piston valve opens, so the water passes above the piston. On the next
upstroke the piston lifts that water out through the spout while more water enters from below.
(No maximum suction depth, flow rate or dimensions are claimed.)
"""
import math

ID = "083"
TITLE = "¿Cómo sube el agua una bomba manual?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo sube el agua del pozo con solo mover una palanca?",
    "El tubo tiene un pistón y dos válvulas de un solo sentido.",
    "Al bajar la manija, el pistón sube y debajo baja la presión.",
    "La presión del aire empuja el agua del pozo hacia arriba.",
    "Al bajar el pistón, la válvula de abajo se cierra.",
    "El agua pasa por la válvula del pistón y queda encima.",
    "En la siguiente subida, el pistón la saca por el caño.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"agua", "pozo", "palanca", "tubo", "pistón", "válvulas", "válvula", "un solo sentido", "manija", "sube",
            "presión", "aire", "empuja", "arriba", "abajo", "cierra", "encima", "subida", "caño"}

CX = 540
CYL_T, CYL_B = 600, 960
IX0, IX1 = 452, 628          # cylinder inner walls
FOOT_Y = 940
GROUND = 1000
WATER_Y = 1090
PIV = (700, 490)
YP_UP, YP_DN = 680, 880
PH = 36                      # piston height
SP_Y0, SP_Y1 = 640, 672      # spout opening
WAT = (60, 140, 230)
WAT_D = (40, 100, 180)
EARTH = (70, 58, 48)


def rod_top(yp):
    return yp - 260


def handle_end(yp):
    rt = rod_top(yp)
    return PIV[0] + 1.5 * (PIV[0] - CX - 30), PIV[1] + 1.5 * (PIV[1] - rt)


def flap(E, d, y, opened, col):
    if opened:
        E.line(d, [(CX - 20, y), (CX + 8, y - 34)], col, 7)
    else:
        E.line(d, [(CX - 20, y), (CX + 24, y)], col, 7)
    E.circle(d, CX - 20, y, 6, fill=col)


def pump(E, d, yp, below=True, above_top=None, foot_open=False, pist_open=False, flow=0.0, u=0.0,
         hl_piston=False, hl_foot=False, hl_pvalve=False, pipe_lvl=None):
    # ground + well
    E.rrect(d, 120, GROUND, 960, 1188, 0, EARTH)
    E.rrect(d, 360, GROUND, 720, 1188, 0, E.mix(E.BG1, EARTH, 0.3))
    E.rrect(d, 360, WATER_Y, 720, 1188, 0, WAT_D)
    for j in range(5):
        x = 380 + j * 70 + 20 * math.sin(u * 2 + j)
        E.line(d, [(x, WATER_Y + 4), (x + 30, WATER_Y + 4)], WAT, 4)
    # bucket
    E.poly(d, [(770, 900), (870, 900), (855, GROUND), (785, GROUND)], fill=E.SIL_D)
    # pipe
    E.rrect(d, 518, CYL_B - 10, 562, 1160, 6, E.SIL_D)
    E.rrect(d, 528, CYL_B - 10, 552, 1160, 4, E.CAV)
    lvl = pipe_lvl if pipe_lvl is not None else (CYL_B if below else WATER_Y)
    if lvl < 1160:
        E.rrect(d, 528, max(lvl, CYL_B - 10), 552, 1160, 4, WAT)
    # cylinder + spout
    E.rrect(d, 436, CYL_T, 644, CYL_B, 14, E.SIL_D)
    E.rrect(d, IX0, CYL_T, IX1, FOOT_Y, 6, E.CAV)
    E.rrect(d, 620, SP_Y0 - 14, 790, SP_Y1 + 14, 10, E.SIL_D)
    E.rrect(d, 620, SP_Y0, 790, SP_Y1, 6, E.CAV)
    # water below the piston
    if below:
        E.rrect(d, IX0, yp + PH, IX1, FOOT_Y, 4, WAT)
    elif lvl < FOOT_Y:
        E.rrect(d, IX0, max(lvl, yp + PH), IX1, FOOT_Y, 4, WAT)
    # water above the piston
    if above_top is not None:
        top = max(above_top, SP_Y0)
        if top < yp:
            E.rrect(d, IX0, top, IX1, yp, 4, WAT)
        if flow > 0:
            E.rrect(d, 620, SP_Y0 + 4, 790, SP_Y1, 4, WAT)
            for j in range(9):
                q = (u * 1.6 + j / 9) % 1.0
                E.circle(d, 800 + 8 * q, SP_Y1 + 10 + q * 220, 10, fill=WAT)
            E.rrect(d, 782, 960, 858, GROUND - 4, 4, WAT)
    # foot valve
    E.rrect(d, IX0, FOOT_Y, IX1, FOOT_Y + 14, 3, E.SIL)
    E.rrect(d, CX - 20, FOOT_Y, CX + 20, FOOT_Y + 14, 2, WAT if below or lvl < FOOT_Y else E.CAV)
    flap(E, d, FOOT_Y, foot_open, E.AMB if hl_foot else E.HOT)
    # piston + its valve + rod
    pc = E.AMB if hl_piston else E.SIL
    E.rrect(d, IX0 + 2, yp, IX1 - 2, yp + PH, 8, pc)
    E.rrect(d, CX - 20, yp, CX + 20, yp + PH, 2, WAT if (above_top is not None or below) else E.CAV)
    flap(E, d, yp, pist_open, E.AMB if hl_pvalve else E.HOT)
    rt = rod_top(yp)
    E.line(d, [(CX + 30, yp), (CX + 30, rt)], E.SIL_H, 10)
    # lever
    hx, hy = handle_end(yp)
    E.line(d, [(PIV[0], PIV[1]), (660, CYL_T)], E.SIL_D, 14)
    E.line(d, [(CX + 30, rt), (hx, hy)], E.BRA, 18)
    E.circle(d, PIV[0], PIV[1], 12, fill=E.BRA_D)
    E.circle(d, hx, hy, 18, fill=E.BRA)
    return hx, hy


def handle_arrow(E, d, yp, down=True):
    hx, hy = handle_end(yp)
    if down:
        E.arrow(d, hx + 50, hy - 60, hx + 50, hy + 30, E.AMB, 7, 24)
    else:
        E.arrow(d, hx + 50, hy + 60, hx + 50, hy - 30, E.AMB, 7, 24)


def scene(i, u, L, E, im, d):
    e = E.ease(min(1.0, u / max(0.5, L * 0.85)))
    if i == 0:  # in action from frame 0: handle going down, water pouring from the spout
        yp = 760 - 70 * e
        pump(E, d, yp, below=True, above_top=yp - 180, foot_open=True, flow=1.0, u=u)
        handle_arrow(E, d, yp, down=True)
    elif i == 1:  # piston + two one-way valves
        pump(E, d, 780, below=False, pipe_lvl=WATER_Y, hl_piston=True, hl_foot=True, hl_pvalve=True, u=u)
        E.label(d, "PISTÓN", 220, 790, 44, color=E.AMB)
        E.arrow(d, 310, 790, 445, 795, E.AMB, 5, 20)
        E.label(d, "VÁLVULA", 220, 700, 40, color=E.AMB)
        E.arrow(d, 300, 720, 520, 775, E.AMB, 4, 18)
        E.label(d, "VÁLVULA", 220, 900, 40, color=E.AMB)
        E.arrow(d, 300, 915, 520, 938, E.AMB, 4, 18)
    elif i == 2:  # handle down: piston rises, lower pressure below
        yp = YP_DN - (YP_DN - YP_UP) * e
        lvl = WATER_Y - (WATER_Y - (yp + PH)) * e
        pump(E, d, yp, below=False, pipe_lvl=lvl, foot_open=e > 0.1, u=u, hl_piston=True)
        handle_arrow(E, d, yp, down=True)
        E.arrow(d, 400, 800, 400, 660, E.AMB, 6, 22)
        E.label(d, "SUBE", 300, 730, 42, color=E.AMB)
        E.label(d, "MENOS", 230, 880, 38, color=E.WHITE)
        E.label(d, "PRESIÓN", 230, 920, 38, color=E.WHITE)
        E.arrow(d, 340, 900, 470, 900, E.WHITE, 5, 20)
    elif i == 3:  # air pressure pushes the well water up the pipe
        pump(E, d, YP_UP, below=True, foot_open=True, u=u)
        for x in (400, 640, 690):
            E.arrow(d, x, WATER_Y - 70, x, WATER_Y - 8, E.WHITE, 6, 22)
        E.arrow(d, 600, 1170, 600, 1010, E.AMB, 6, 22)
        E.label(d, "AIRE", 230, WATER_Y - 40, 46, color=E.WHITE)
        E.label(d, "AGUA", 860, 1100, 44, color=E.COLD)
    elif i == 4:  # piston goes down: foot valve closes
        yp = YP_UP + 100 * e
        pump(E, d, yp, below=True, above_top=YP_UP, foot_open=False, pist_open=True, u=u, hl_foot=True)
        E.arrow(d, 400, 760, 400, 880, E.AMB, 6, 22)
        E.label(d, "BAJA", 300, 820, 42, color=E.AMB)
        E.label(d, "CERRADA", 220, 945, 40, color=E.AMB)
        E.arrow(d, 330, 945, 445, 945, E.AMB, 5, 20)
    elif i == 5:  # water passes through the piston valve and ends up above
        yp = YP_UP + 100 + 100 * e
        pump(E, d, yp, below=True, above_top=YP_UP, foot_open=False, pist_open=True, u=u, hl_pvalve=True)
        E.arrow(d, CX - 50, yp + 80, CX - 50, yp - 30, E.COLD, 6, 22)
        E.label(d, "ABIERTA", 220, yp + 10, 40, color=E.AMB)
        E.arrow(d, 320, yp + 10, 445, yp + 10, E.AMB, 5, 20)
        E.label(d, "ENCIMA", 220, 660, 40, color=E.COLD)
    elif i == 6:  # next upstroke lifts it out of the spout
        yp = YP_DN - (YP_DN - YP_UP) * e
        top = yp - (YP_DN - YP_UP)
        pump(E, d, yp, below=True, above_top=top, foot_open=True, flow=1.0 if top <= SP_Y0 + 2 else 0.0, u=u,
             hl_piston=True)
        handle_arrow(E, d, yp, down=True)
        E.label(d, "CAÑO", 930, 780, 42, color=E.AMB)
        E.arrow(d, 900, 750, 800, SP_Y1 + 20, E.AMB, 5, 20)
        E.arrow(d, 400, 900, 400, 760, E.AMB, 6, 22)
        E.label(d, "SUBE", 300, 830, 42, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.2, 0.8), ("click", s[1] + 0.6), ("zip", s[2] + 0.4), ("whoosh", s[3] + 0.5, 0.8),
            ("click", s[4] + 0.6), ("pop", s[5] + 0.6), ("whoosh", s[6] + 0.5, 0.8)]
