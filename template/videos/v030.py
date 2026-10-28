"""Video 030 — ¿Por qué burbujea un refresco?
Science: at the factory, carbon dioxide (CO2) is added to the drink under pressure. While the bottle stays closed and
pressurised, that gas stays dissolved in the liquid, so no bubbles are seen. When the bottle is opened the pressure
drops suddenly (the hiss is gas escaping from the neck). At the lower pressure the liquid can no longer hold all the
dissolved gas, so it comes out of solution. The bubbles form mainly at tiny imperfections (rough spots, specks,
fibres) on the container walls and rise to the surface. (No pressures, volumes or temperatures are claimed.)
"""
import math

ID = "030"
TITLE = "¿Por qué burbujea un refresco?"
SUBTITLE = "CURIOSIDADES DE LA CIENCIA"
LINES = [
    "¿Por qué tu refresco burbujea al abrirlo?",
    "En la fábrica le meten dióxido de carbono a presión.",
    "Con la botella cerrada, ese gas queda disuelto en el líquido.",
    "La presión lo mantiene escondido: por eso no ves burbujas.",
    "Al abrirla, la presión baja de golpe con un siseo.",
    "El gas ya no cabe disuelto en el líquido y empieza a escapar.",
    "Forma burbujas en pequeñas imperfecciones del envase y suben.",
    "Sígueme para más curiosidades de la ciencia.",
]
KEYWORDS = {"refresco", "burbujea", "abrirlo", "fábrica", "dióxido", "carbono", "presión", "cerrada", "gas",
            "disuelto", "líquido", "escondido", "burbujas", "abrirla", "golpe", "siseo", "escapar",
            "imperfecciones", "envase", "suben", "ciencia"}

DRINK, DRINK_D = (150, 75, 40), (110, 52, 28)
GLASS = (190, 215, 235)
CAP = (220, 60, 60)
GAS = (235, 240, 250)

def bottle(E, d, cx, top, fill=0.85, cap=0.0, show_cap=True, capdx=0.0):
    """Generic bottle; body 300 wide from y=top+260 to y=top+820, neck up to y=top. cap: lift of cap (px)."""
    body = [(cx - 50, top + 20), (cx + 50, top + 20), (cx + 55, top + 150), (cx + 150, top + 270),
            (cx + 150, top + 800), (cx + 130, top + 830), (cx - 130, top + 830), (cx - 150, top + 800),
            (cx - 150, top + 270), (cx - 55, top + 150)]
    E.poly(d, body, fill=E.mix(GLASS, E.BG1, 0.55), outline=GLASS, w=5)
    ly = top + 830 - (830 - 200) * fill
    E.poly(d, [(cx - 145, max(ly, top + 275)), (cx + 145, max(ly, top + 275)), (cx + 145, top + 798),
               (cx + 127, top + 825), (cx - 127, top + 825), (cx - 145, top + 798)], fill=DRINK)
    if show_cap:
        E.rrect(d, cx - 60 + capdx, top - 30 - cap, cx + 60 + capdx, top + 20 - cap, 10, CAP)
    return ly

def dots(E, d, cx, y0, y1, u, n=26, speed=0.0, r=7, color=GAS, seed=1.0, wob=1.0):
    for k in range(n):
        fx = (math.sin(k * 12.9898 + seed * 7.1) * 43758.5453) % 1 * 2 - 1
        fy = (math.sin(k * 78.233 + seed * 3.7) * 12345.6789) % 1
        y = y1 - ((fy + u * speed) % 1) * (y1 - y0)
        x = cx + 120 * fx + 10 * wob * math.sin(u * 3 + k)
        E.circle(d, x, y, r, fill=color)

def gauge(E, d, x, y, v):
    E.circle(d, x, y, 80, fill=E.CAV, outline=E.SIL, w=6)
    a = math.pi * (1.15 - 0.9 * v)
    E.line(d, [(x, y), (x + 62 * math.cos(a), y - 62 * math.sin(a))], E.HOT, 8)
    E.circle(d, x, y, 10, fill=E.SIL)

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: the cap is already coming off and bubbles rush up
        k = min(1.0, 0.25 + u / 1.2)
        bottle(E, d, 540, 380, 0.85, cap=80 * math.sin(math.pi * 0.5 * k), capdx=260 * k)
        dots(E, d, 540, 560, 1190, u, n=34, speed=1.6, r=8)
        for k in range(6):
            f = (u * 1.5 + k / 6) % 1
            a = -math.pi / 2 + (k - 2.5) * 0.25
            E.circle(d, 540 + 90 * f * math.cos(a), 372 + 85 * f * math.sin(a), 10 * (1 - f) + 4, fill=GAS)
        E.pill(d, "¡ABIERTO!", 830, 560, 40)
    elif i == 1:  # CO2 pushed in under pressure at the factory
        bottle(E, d, 650, 380, 0.85, show_cap=False)
        E.rrect(d, 110, 420, 290, 980, 60, E.SIL_D)
        E.label(d, "CO2", 200, 700, 54, color=E.WHITE)
        E.line(d, [(290, 520), (650, 520), (650, 400)], E.SIL, 22)
        k = E.ease(u / (L * 0.8))
        for j in range(6):
            f = (u * 0.8 + j / 6) % 1
            px, py = (300 + 350 * f * 2, 520) if f < 0.5 else (650, 520 + 300 * (f - 0.5) * 2)
            E.circle(d, px, py, 10, fill=GAS)
        dots(E, d, 650, 680, 1180, u, n=int(6 + 22 * k), r=6, seed=0.3)
        gauge(E, d, 200, 1090, 0.2 + 0.7 * k)
        E.label(d, "PRESIÓN", 380, 1090, 40, color=E.AMB, anchor="lm")
    elif i == 2:  # closed bottle: gas dissolved, spread through the liquid
        bottle(E, d, 540, 380, 0.85)
        dots(E, d, 540, 690, 1180, u, n=30, r=6, seed=0.7, wob=2.0)
        E.label(d, "GAS DISUELTO", 540, 330, 48, color=E.AMB)
    elif i == 3:  # pressure keeps it dissolved: no bubbles
        ly = bottle(E, d, 540, 380, 0.85)
        dots(E, d, 540, 690, 1180, u, n=30, r=6, seed=0.7, wob=2.0)
        for k in range(3):
            x = 450 + 90 * k
            o = 12 * math.sin(u * 4 + k)
            E.arrow(d, x, ly - 120 + o, x, ly - 20 + o, color=E.AMB, w=8, head=26)
        gauge(E, d, 880, 520, 0.9)
        E.label(d, "SIN BURBUJAS", 540, 330, 48, color=E.AMB)
    elif i == 4:  # opening: pressure drops suddenly with a hiss
        k = E.ease(u / (L * 0.4))
        bottle(E, d, 540, 380, 0.85, cap=80 * k, capdx=-300 * k)
        dots(E, d, 540, 690, 1180, u, n=30, r=6, seed=0.7, wob=2.0)
        for j in range(3):
            E.wave(d, 540 + (j - 1) * 30, 365, 540 + (j - 1) * 120, 300, 30, 8, GAS, w=4, phase=u * 12, head=False)
        gauge(E, d, 880, 520, 0.9 - 0.75 * k)
        E.label(d, "PRESIÓN BAJA", 880, 650, 40, color=E.AMB)
    elif i == 5:  # the gas no longer fits dissolved and starts to escape
        ly = bottle(E, d, 540, 380, 0.85, show_cap=False)
        dots(E, d, 540, 760, 1180, u, n=16, r=6, seed=0.7, wob=2.0)
        dots(E, d, 540, ly, 1150, u, n=20, speed=0.6, r=11, seed=0.2)
        for j in range(4):
            f = (u * 0.7 + j / 4) % 1
            E.arrow(d, 480 + 40 * j, ly - 10 - 200 * f, 480 + 40 * j, ly - 60 - 200 * f, color=E.WHITE, w=6, head=20)
        E.label(d, "EL GAS ESCAPA", 540, 330, 48, color=E.AMB)
    elif i == 6:  # bubbles form at tiny imperfections of the container and rise
        E.rrect(d, 120, 380, 960, 1170, 30, DRINK)
        E.rrect(d, 120, 380, 200, 1170, 20, E.mix(GLASS, E.BG1, 0.3))
        sites = [(205, 520), (205, 760), (205, 1000)]
        for k, (x, y) in enumerate(sites):
            E.line(d, [(195, y - 24), (215, y - 8), (198, y + 6), (215, y + 22)], E.AMB, 7)
            g = (u * 0.9 + k * 0.3) % 1
            if g < 0.5:
                r = 8 + 40 * g
                E.circle(d, x + r, y, r, fill=GAS)
            else:
                f = (g - 0.5) * 2
                E.circle(d, x + 28 + 120 * f, y - 520 * f, 28, fill=GAS)
        E.arrow(d, 760, 900, 760, 520, color=E.WHITE, w=8, head=30)
        E.label(d, "IMPERFECCIONES", 560, 1110, 44, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("pop", s[0] + 0.05), ("whoosh", s[1] + 0.4, 1.2), ("click", s[2] + 0.6), ("click", s[3] + 0.8),
            ("whoosh", s[4] + 0.2, 1.4), ("whoosh", s[5] + 0.4, 1.0), ("pop", s[6] + 0.8)]
