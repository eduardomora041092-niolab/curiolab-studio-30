"""Video 029 — ¿Cómo sabe la pantalla dónde la tocas?
Science: most phones use a projected-capacitive touchscreen. Under the glass there is a grid of transparent
electrodes: some run in rows and others in columns, and they carry electric charge. A controller chip keeps measuring
the charge (capacitance) at every crossing of the grid. A finger conducts electricity, so when it comes close it
alters the electric field and the charge at the crossings right under it. The chip finds the crossing that changed
and works out the position of the touch. An ordinary glove is an insulator, so it does not alter the charge and the
screen does not notice it. (No scan rates, electrode counts or materials are claimed.)
"""
import math

ID = "029"
TITLE = "¿Cómo sabe la pantalla dónde la tocas?"
LINES = [
    "¿Cómo sabe tu móvil dónde lo tocas?",
    "Bajo el cristal hay una rejilla de electrodos transparentes.",
    "Unos van en filas y otros en columnas, con carga eléctrica.",
    "Un chip mide sin parar la carga en cada cruce.",
    "Tu dedo conduce la electricidad y altera la carga justo debajo.",
    "El chip encuentra el cruce que cambió: ahí está tu dedo.",
    "Un guante normal no conduce, así que la pantalla no lo nota.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"móvil", "tocas", "cristal", "rejilla", "electrodos", "transparentes", "filas", "columnas", "carga",
            "eléctrica", "chip", "cruce", "dedo", "conduce", "electricidad", "altera", "cambió", "guante", "nota"}

SKIN, SKIN_D = (236, 188, 150), (200, 150, 115)
GLOVE, GLOVE_D = (120, 70, 150), (90, 50, 115)
# grid geometry (top view of the screen)
GX0, GY0, GX1, GY1 = 270, 450, 810, 1060
NC, NR = 5, 6
TX, TY = 3, 3   # touched crossing (column, row)

def col_x(c): return GX0 + 60 + c * (GX1 - GX0 - 120) / (NC - 1)
def row_y(r): return GY0 + 60 + r * (GY1 - GY0 - 120) / (NR - 1)

def phone(E, d, glow=0.0):
    E.rrect(d, GX0 - 40, GY0 - 70, GX1 + 40, GY1 + 70, 60, (30, 34, 44), outline=E.SIL_D, w=6)
    E.rrect(d, GX0, GY0, GX1, GY1, 20, E.mix(E.BLUE_D, E.BLUE, glow))

def finger(E, d, x, y, c=SKIN, cd=SKIN_D, thick=1.0):
    """Finger seen from above-front, fingertip at (x, y), coming from the lower right."""
    w = 62 * thick
    E.line(d, [(x + 10, y + 20), (x + 260, y + 330)], cd, w * 2 + 8)
    E.line(d, [(x + 10, y + 20), (x + 260, y + 330)], c, w * 2)
    E.circle(d, x, y, w, fill=c)

def grid(E, d, rows=1.0, cols=1.0, dim=False):
    rc = E.mix(E.BG2, E.COLD, 0.55 if dim else 1.0)
    cc = E.mix(E.BG2, E.AMB, 0.55 if dim else 1.0)
    for r in range(NR):
        x1 = GX0 + 20 + (GX1 - GX0 - 40) * rows
        E.line(d, [(GX0 + 20, row_y(r)), (x1, row_y(r))], rc, 10)
    for c in range(NC):
        y1 = GY0 + 20 + (GY1 - GY0 - 40) * cols
        E.line(d, [(col_x(c), GY0 + 20), (col_x(c), y1)], cc, 10)

def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: a finger is already tapping the phone, ripples where it touches
        phone(E, d, 0.3)
        for k, (cx, cy) in enumerate(((430, 600), (650, 820), (480, 960))):
            f = ((u * 0.9) - k * 0.33) % 1
            E.circle(d, cx, cy, 20 + 110 * f, outline=E.mix(E.AMB, E.BLUE, f), w=6)
        k = int((u * 0.9) % 1 * 3)
        tx, ty = ((430, 600), (650, 820), (480, 960))[int(u * 0.9) % 3]
        finger(E, d, tx, ty)
        E.pill(d, "¿DÓNDE?", 540, 320, 40)
    elif i == 1:  # under the glass: a grid of transparent electrodes
        phone(E, d, 0.0)
        grid(E, d, dim=True)
        k = E.ease(u / (L * 0.7))
        E.rrect(d, GX0 + 10 + 430 * k, GY0 + 10, GX1 - 10 + 430 * k, GY1 - 10, 20, (170, 200, 230))
        E.label(d, "CRISTAL", (GX0 + 10 + 430 * k + min(1070, GX1 - 10 + 430 * k)) / 2, 750, 46, color=E.BG1)
        if k > 0.6:
            E.label(d, "REJILLA", 540, 1160, 50, color=E.AMB)
    elif i == 2:  # rows and columns, with electric charge
        phone(E, d, 0.0)
        a = E.ease(u / (L * 0.4)); b = E.ease((u - L * 0.3) / (L * 0.4))
        grid(E, d, rows=a, cols=b)
        for r in range(NR):
            for c in range(NC):
                if b > 0.9:
                    E.circle(d, col_x(c), row_y(r), 12 + 3 * math.sin(u * 5 + r + c), fill=E.WHITE)
        E.label(d, "FILAS", 160, row_y(1), 40, color=E.COLD)
        E.label(d, "COLUMNAS", 540, 330, 44, color=E.AMB)
    elif i == 3:  # the chip keeps measuring every crossing
        phone(E, d, 0.0)
        grid(E, d)
        n = NR * NC
        cur = int(u * 14) % n
        for idx in range(n):
            r, c = divmod(idx, NC)
            E.circle(d, col_x(c), row_y(r), 22 if idx == cur else 12, fill=E.WHITE if idx == cur else E.MUTED)
        E.rrect(d, 450, 1135, 630, 1185, 12, E.SIL_D)
        E.label(d, "CHIP", 540, 1160, 32, color=E.WHITE)
        E.label(d, "MIDE CADA CRUCE", 540, 330, 44, color=E.AMB)
    elif i == 4:  # finger conducts and alters the charge right under it
        phone(E, d, 0.0)
        grid(E, d)
        x, y = col_x(TX), row_y(TY)
        k = E.ease(u / (L * 0.5))
        for r in range(NR):
            for c in range(NC):
                hot = (r, c) == (TY, TX) and k > 0.9
                E.circle(d, col_x(c), row_y(r), 22 if hot else 12, fill=E.HOT if hot else E.WHITE)
        if k > 0.9:
            for a in range(8):
                ang = a * math.pi / 4 + u
                E.line(d, [(x + 30 * math.cos(ang), y + 30 * math.sin(ang)), (x + 60 * math.cos(ang), y + 60 * math.sin(ang))], E.HOT, 5)
        finger(E, d, x + 75 + 200 * (1 - k), y + 75 + 200 * (1 - k))
        E.label(d, "EL DEDO CONDUCE", 540, 330, 44, color=E.AMB)
    elif i == 5:  # chip finds the crossing that changed
        phone(E, d, 0.0)
        grid(E, d, dim=True)
        x, y = col_x(TX), row_y(TY)
        k = E.ease(u / (L * 0.5))
        E.line(d, [(GX0 + 20, y), (GX0 + 20 + (GX1 - GX0 - 40) * k, y)], E.COLD, 14)
        E.line(d, [(x, GY0 + 20), (x, GY0 + 20 + (GY1 - GY0 - 40) * k)], E.AMB, 14)
        if k > 0.95:
            E.circle(d, x, y, 50, outline=E.HOT, w=8)
            E.circle(d, x, y, 18, fill=E.HOT)
        E.label(d, f"FILA {TY + 1}, COLUMNA {TX + 1}", 540, 330, 44, color=E.WHITE)
    elif i == 6:  # an ordinary glove does not conduct: nothing changes
        phone(E, d, 0.0)
        grid(E, d)
        for r in range(NR):
            for c in range(NC):
                E.circle(d, col_x(c), row_y(r), 12, fill=E.WHITE)
        x, y = col_x(1), row_y(2)
        k = E.ease(u / (L * 0.4))
        finger(E, d, x + 85 + 200 * (1 - k), y + 85 + 200 * (1 - k), GLOVE, GLOVE_D, thick=1.25)
        if k > 0.95:
            E.cross(d, x - 110, y + 20, 40)
        E.label(d, "GUANTE: NO CONDUCE", 540, 330, 44, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("click", s[0] + 0.1), ("whoosh", s[1] + 0.3, 1.2), ("pop", s[2] + 0.8), ("click", s[3] + 0.5),
            ("pop", s[4] + 0.9), ("pop", s[5] + 1.0), ("click", s[6] + 0.9)]
