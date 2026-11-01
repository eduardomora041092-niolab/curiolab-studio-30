"""Video 040 — ¿Por qué cocina más rápido una olla a presión?
Science: in an open pot at sea level water boils at about 100 °C; while it boils, the steam escapes and the water
temperature does not rise any further. A pressure cooker seals the lid with a rubber gasket, so the steam is trapped
and the pressure inside rises. The boiling point of water increases with pressure, so the water boils above 100 °C.
At that higher temperature food cooks faster. A valve releases the excess steam so the pressure does not keep rising.
(No exact temperatures, pressures, times or energy savings are claimed.)
"""
import math

ID = "040"
TITLE = "¿Por qué cocina más rápido una olla a presión?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Por qué cocina más rápido una olla a presión?",
    "En una olla normal, el agua hierve a unos cien grados.",
    "El vapor escapa y la temperatura no sube más.",
    "La olla a presión cierra la tapa herméticamente.",
    "El vapor queda atrapado y la presión dentro aumenta.",
    "Con más presión, el agua hierve a más de cien grados.",
    "Más calor cocina antes; una válvula libera el vapor sobrante.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"cocina", "rápido", "olla", "presión", "agua", "hierve", "cien", "grados", "vapor", "escapa",
            "temperatura", "tapa", "herméticamente", "atrapado", "aumenta", "calor", "válvula", "sobrante"}

WATER = (90, 170, 255)
FLAME = (255, 120, 40)

def flame(E, d, u, y=1000, x0=380, x1=700):
    for k in range(6):
        x = x0 + (x1 - x0) * k / 5
        h = 60 + 20 * math.sin(u * 9 + k * 1.7)
        E.poly(d, [(x - 22, y), (x, y - h), (x + 22, y)], fill=FLAME)
        E.poly(d, [(x - 10, y), (x, y - h * 0.55), (x + 10, y)], fill=E.AMB)

def pot(E, d, y0=620, y1=940, x0=300, x1=780, water_y=760, u=0.0, bubbles=1.0):
    E.rrect(d, x0, y0, x1, y1, 26, E.SIL_D)
    E.rrect(d, x0 + 20, water_y, x1 - 20, y1 - 20, 16, E.mix(E.BG2, WATER, 0.65))
    for k in range(12):
        f = (u * 1.3 + k * 0.13) % 1
        bx = x0 + 50 + (k * 37) % (x1 - x0 - 100)
        by = y1 - 40 - (y1 - water_y - 60) * f
        E.circle(d, bx, by, (6 + 6 * f) * bubbles, outline=E.WHITE, w=3)
    E.rrect(d, x0 - 70, y0 + 40, x0, y0 + 70, 10, E.SIL_D)
    E.rrect(d, x1, y0 + 40, x1 + 70, y0 + 70, 10, E.SIL_D)

def lid(E, d, y=620, x0=290, x1=790, lift=0.0):
    E.rrect(d, x0, y - 40 - lift, x1, y - lift, 18, E.SIL)
    E.rrect(d, 510, y - 80 - lift, 570, y - 40 - lift, 10, E.SIL_D)

def steam(E, d, u, x, y, n=4, spread=40, rise=260, alpha=0.6):
    for k in range(n):
        f = (u * 0.8 + k / n) % 1
        E.circle(d, x + spread * math.sin(u * 3 + k), y - rise * f, 18 + 26 * f,
                 fill=E.mix(E.BG1, E.SIL, alpha * (1 - f)))

def thermo(E, d, x, y, level, col):
    E.rrect(d, x - 22, y - 300, x + 22, y, 22, E.BG2)
    E.circle(d, x, y + 10, 36, fill=col)
    E.rrect(d, x - 12, y - 300 * level, x + 12, y, 12, col)

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: pressure cooker hissing, valve jiggling and venting steam
        flame(E, d, u, y=1010)
        pot(E, d, u=u)
        lid(E, d)
        jig = 6 * math.sin(u * 20)
        E.rrect(d, 520, 500 + jig, 560, 540 + jig, 8, E.AMB)
        steam(E, d, u * 1.5, 540, 480, n=5, spread=30, rise=150, alpha=0.8)
        E.pill(d, "OLLA A PRESIÓN", 540, 1110, 42)
    elif i == 1:  # open pot: water boils at about 100 degrees
        flame(E, d, u, y=1010)
        pot(E, d, u=u)
        thermo(E, d, 900, 900, 0.55, E.AMB)
        E.label(d, "100 °C", 900, 520, 50, color=E.AMB)
        E.label(d, "OLLA NORMAL", 540, 400, 46, color=E.WHITE)
    elif i == 2:  # steam escapes, temperature stops rising
        flame(E, d, u, y=1010)
        pot(E, d, u=u)
        for x in (380, 540, 700):
            steam(E, d, u, x, 600, n=3, rise=260)
        thermo(E, d, 900, 900, 0.55, E.AMB)
        E.label(d, "100 °C", 900, 520, 50, color=E.AMB)
        E.label(d, "EL VAPOR ESCAPA", 540, 1110, 44, color=E.SIL_H)
    elif i == 3:  # pressure cooker seals the lid
        flame(E, d, u, y=1010)
        pot(E, d, u=u)
        lift = 160 * (1 - E.ease(min(1, u / (L * 0.5))))
        lid(E, d, lift=lift)
        if lift < 5:
            E.rrect(d, 290, 612, 790, 628, 6, E.HOT)
            E.label(d, "CIERRE HERMÉTICO", 540, 400, 44, color=E.HOT)
        else:
            E.label(d, "TAPA", 540, 400, 46, color=E.SIL_H)
    elif i == 4:  # steam trapped, pressure rises
        pot(E, d, u=u, water_y=820)
        lid(E, d)
        k = min(1, u / L)
        for j in range(int(10 + 14 * k)):
            a = j * 2.39 + u * 2
            x = 540 + (190 - 10 * (j % 3)) * math.sin(a)
            y = 715 + 70 * math.cos(a * 1.3)
            E.circle(d, x, y, 12, fill=E.SIL_H)
        for ang in (math.pi, 0):
            E.arrow(d, 540 + 140 * math.cos(ang), 700, 540 + 230 * math.cos(ang), 700, E.HOT, 7, 24)
        E.arrow(d, 540, 680, 540, 630, E.HOT, 7, 24)
        E.label(d, "VAPOR ATRAPADO", 540, 420, 44, color=E.SIL_H)
        E.pill(d, "MÁS PRESIÓN", 540, 1080, 42, bg=E.HOT, fg=E.WHITE)
    elif i == 5:  # higher pressure, water boils above 100 degrees
        flame(E, d, u, y=1010)
        pot(E, d, u=u)
        lid(E, d)
        lvl = 0.55 + 0.3 * E.ease(min(1, u / (L * 0.6)))
        thermo(E, d, 900, 900, lvl, E.HOT)
        E.label(d, "100 °C", 900, 990, 30, color=E.MUTED)
        E.line(d, [(860, 900 - 300 * 0.55), (940, 900 - 300 * 0.55)], E.MUTED, 4)
        E.label(d, "MÁS DE 100 °C", 540, 420, 50, color=E.HOT)
    elif i == 6:  # hotter cooks faster; valve releases excess steam
        flame(E, d, u, y=1010)
        pot(E, d, u=u, bubbles=1.3)
        lid(E, d)
        jig = 6 * math.sin(u * 20)
        E.rrect(d, 520, 500 + jig, 560, 540 + jig, 8, E.AMB)
        steam(E, d, u * 1.5, 540, 480, n=5, spread=30, rise=150, alpha=0.8)
        E.label(d, "VÁLVULA", 760, 470, 44, color=E.AMB)
        E.arrow(d, 690, 480, 580, 515, E.AMB, 6, 22)
        E.pill(d, "COCINA ANTES", 540, 1110, 42, bg=E.HOT, fg=E.WHITE)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.05, 1.0), ("pop", s[1] + 0.5), ("whoosh", s[2] + 0.4, 0.8), ("click", s[3] + 1.0),
            ("zip", s[4] + 0.5, 1.0), ("pop", s[5] + 0.8), ("whoosh", s[6] + 0.3, 1.2)]
