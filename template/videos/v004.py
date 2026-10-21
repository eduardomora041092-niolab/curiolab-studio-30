"""Video 004 — ¿Cómo abre una llave una cerradura? (cerradura de pines / pin tumbler)
Mechanism: a rotating plug sits inside a fixed housing. Each pin stack = key pin (bottom, varying
length) + driver pin (top) pushed down by a spring. With no key, driver pins cross the shear line and
block rotation. The right key lifts every stack so the gap between key pin and driver pin sits exactly
at the shear line; the plug turns and its cam pulls the bolt. A wrong key leaves at least one pin
crossing the line, so the plug stays locked.
"""
import math

ID = "004"
TITLE = "¿Cómo abre una llave una cerradura?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Por qué solo tu llave abre tu cerradura?",
    "Dentro hay un cilindro que debe girar, atravesado por columnas de pernos.",
    "Cada columna tiene dos pernos y un muelle que los empuja hacia abajo.",
    "Sin llave, los pernos de arriba cruzan la línea de corte y bloquean el giro.",
    "La llave correcta sube cada columna a la altura exacta.",
    "Los huecos entre pernos quedan alineados en la línea de corte, y el cilindro gira.",
    "Con una llave equivocada, basta un perno fuera de sitio para que no gire.",
    "Sígueme para ver cómo funcionan las cosas por dentro.",
]
KEYWORDS = {"llave", "cerradura", "cilindro", "pernos", "muelle", "línea", "corte", "bloquean", "exacta", "alineados", "gira", "equivocada", "dentro"}

HOUSING, HOUSING_D = (70, 84, 112), (45, 56, 80)
PLUG, PLUG_D = (150, 160, 178), (100, 110, 128)
KEYC, KEYC_D = (224, 179, 90), (160, 118, 45)
GREEN = (80, 200, 120)

X0, X1 = 170, 910            # plug horizontal extent
SHEAR = 640                   # shear line y
PLUG_BOT = 820
PINS_X = [300, 420, 540, 660, 780]
KEY_LEN = [70, 120, 50, 100, 80]        # key pin lengths (different per stack)
DRIVER = 90; PIN_W = 54

def key_cut(j, correct=True):
    """Height the key lifts the bottom of pin j to (y of key pin bottom)."""
    target = SHEAR + KEY_LEN[j]            # correct: key pin top lands exactly on shear line
    if correct: return target
    wrong = [0, 0, 34, 0, 0]               # wrong key: pin 3 lifted 34 px too high
    return target - wrong[j]

def lock_body(E, d, rot=0.0):
    E.rrect(d, 110, 330, 970, 900, 40, HOUSING, outline=HOUSING_D, w=5)
    # plug (shown in section); rotation suggested by a shading band
    E.rrect(d, X0, SHEAR, X1, PLUG_BOT, 26, PLUG, outline=PLUG_D, w=4)
    if rot > 0:
        E.rrect(d, X0, SHEAR + 10, X1, SHEAR + 10 + 160 * rot, 20, E.mix(PLUG, E.WHITE, 0.25))
    E.rrect(d, X0 + 10, SHEAR + 70, X1 - 10, SHEAR + 110, 14, (60, 70, 92))   # keyway
    for x in PINS_X:  # pin chambers
        E.rrect(d, x - PIN_W / 2 - 6, 360, x + PIN_W / 2 + 6, SHEAR + 140, 10, (34, 44, 66))

def pin_stack(E, d, j, lift_y, highlight=False):
    """lift_y = y of the key pin bottom. Spring above driver pin."""
    x = PINS_X[j]
    kb = lift_y; kt = kb - KEY_LEN[j]
    dt = kt - DRIVER
    # spring
    pts = []
    for s in range(0, 13):
        yy = 370 + (dt - 370) * s / 12
        pts.append((x + (18 if s % 2 else -18), yy))
    E.line(d, pts, (200, 205, 215), 5)
    E.rrect(d, x - PIN_W / 2, dt, x + PIN_W / 2, kt, 12, E.SIL, outline=E.SIL_D, w=3)          # driver pin
    E.rrect(d, x - PIN_W / 2, kt, x + PIN_W / 2, kb, 12, KEYC, outline=KEYC_D, w=3)            # key pin
    d.polygon([(x * E.S, (kb + 22) * E.S), ((x - PIN_W / 2) * E.S, kb * E.S), ((x + PIN_W / 2) * E.S, kb * E.S)], fill=KEYC)
    if highlight:
        ok = abs(kt - SHEAR) < 3
        E.circle(d, x, SHEAR, 14, fill=GREEN if ok else E.HOT)

def shear_line(E, d, alpha=1.0):
    for x in range(120, 960, 40):
        E.line(d, [(x, SHEAR), (x + 22, SHEAR)], E.AMB, 5)

def key(E, d, x_tip, correct=True):
    """Key blade entering from the right; its top edge follows key_cut under each pin."""
    base = SHEAR + 175
    pts = [(x_tip, base - 30)]
    for j in range(5):
        px = PINS_X[j]
        if px >= x_tip - 10:
            top = key_cut(j, correct) + 22
            pts += [(px - 44, top + 34), (px, top), (px + 44, top + 34)]
    pts += [(1000, SHEAR + 140), (1000, base + 40), (x_tip + 30, base + 40), (x_tip, base)]
    pts = [(min(max(x, x_tip), 1000), y) for x, y in pts]
    E.poly(d, pts, fill=KEYC, outline=KEYC_D, w=3)
    E.circle(d, 1030, SHEAR + 160, 70, fill=KEYC, outline=KEYC_D, w=4)   # key bow
    E.circle(d, 1040, SHEAR + 160, 22, fill=E.BG2)

def resting_lift(j):
    # without key the spring pushes the stack down: key pin top sits 45 px below the shear line,
    # so every 90 px driver pin straddles the shear line and blocks rotation
    return SHEAR + 45 + KEY_LEN[j]

def scene(i, u, L, E, im, d):
    if i == 0:  # hook: key + padlock-ish front view, wrong keys bounce
        E.rrect(d, 330, 520, 750, 1000, 60, HOUSING, outline=HOUSING_D, w=6)
        E.circle(d, 540, 760, 120, fill=PLUG, outline=PLUG_D, w=6)
        E.rrect(d, 528, 700, 552, 820, 8, (40, 50, 70))
        k = E.ease(u / 1.2)
        ang = 0 if u < 1.4 else min(90, (u - 1.4) * 160)
        r = math.radians(ang)
        E.line(d, [(540, 760), (540 + 95 * math.sin(r), 760 - 95 * math.cos(r))], (40, 50, 70), 22)
        E.label(d, "¿POR QUÉ SOLO LA TUYA?", 540, 420, 50)
    elif i == 1:  # cylinder + pin columns
        lock_body(E, d)
        for j in range(5): pin_stack(E, d, j, resting_lift(j))
        if u > 0.4:
            E.label(d, "CILINDRO", 540, 960, 50); E.arrow(d, 540, 925, 540, PLUG_BOT + 8, w=5)
        if u > L * 0.55:
            E.label(d, "PERNOS", 540, 290, 50)
    elif i == 2:  # two pins + spring, highlight one column
        lock_body(E, d)
        for j in range(5): pin_stack(E, d, j, resting_lift(j))
        x = PINS_X[2]; bounce = 8 * math.sin(u * 6)
        E.rrect(d, x - 70, 350, x + 70, PLUG_BOT, 20, None, outline=E.AMB, w=5)
        if u > 0.5:
            E.label(d, "MUELLE", 150, 410, 40); E.arrow(d, 150, 440, x - 40, 470, w=5)
            E.label(d, "PERNO", 930, 520, 40, color=E.SIL); E.arrow(d, 930, 550, x + 40, 560, w=5, color=E.SIL)
            E.label(d, "PERNO", 930, 760, 40, color=KEYC); E.arrow(d, 930, 730, x + 40, 720, w=5, color=KEYC)
    elif i == 3:  # no key: driver pins cross shear line -> blocked
        lock_body(E, d)
        shear_line(E, d)
        for j in range(5): pin_stack(E, d, j, resting_lift(j))
        E.label(d, "LÍNEA DE CORTE", 540, 290, 46)
        if u > 0.8:
            wob = 6 * math.sin(u * 30) * (1 if u < L - 0.3 else 0)
            for x in PINS_X: E.cross(d, x + wob, SHEAR, 24)
            E.pill(d, "BLOQUEADO", 540, 975, 40, bg=E.HOT, fg=E.WHITE)
    elif i == 4:  # correct key slides in, pins rise to cut heights
        lock_body(E, d); shear_line(E, d)
        tip = 1060 - 960 * E.ease(u / (L * 0.8))
        for j in range(5):
            x = PINS_X[j]
            if tip <= x:
                f = E.ease((x - tip) / 60)
                pin_stack(E, d, j, E.lerp(resting_lift(j), key_cut(j), f))
            else:
                pin_stack(E, d, j, resting_lift(j))
        key(E, d, tip)
        E.label(d, "LLAVE CORRECTA", 540, 290, 46, color=GREEN)
    elif i == 5:  # gaps aligned -> plug rotates
        lock_body(E, d, rot=E.ease((u - 1.2) / 1.5))
        shear_line(E, d)
        for j in range(5): pin_stack(E, d, j, key_cut(j), highlight=u > 0.5)
        key(E, d, 100)
        if u > 1.2:
            E.pill(d, "GIRA", 540, 975, 44, bg=GREEN)
            r = math.radians(min(90, (u - 1.2) * 120))
            E.circle(d, 820, 1060, 60, fill=PLUG, outline=PLUG_D, w=4)
            E.line(d, [(820, 1060), (820 + 50 * math.sin(r), 1060 - 50 * math.cos(r))], (40, 50, 70), 14)
    elif i == 6:  # wrong key: one pin out of place
        lock_body(E, d); shear_line(E, d)
        for j in range(5): pin_stack(E, d, j, key_cut(j, correct=False), highlight=u > 0.4)
        key(E, d, 100, correct=False)
        E.label(d, "LLAVE EQUIVOCADA", 540, 290, 46, color=E.HOT)
        if u > 0.9:
            E.pill(d, "NO GIRA", 540, 975, 44, bg=E.HOT, fg=E.WHITE)
    else:
        E.outro(d, u)

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("click", s[3] + 0.8), ("whoosh", s[4] + 0.2, 0.8), ("click", s[5] + 0.6), ("click", s[5] + 1.2), ("pop", s[6] + 0.9)]
