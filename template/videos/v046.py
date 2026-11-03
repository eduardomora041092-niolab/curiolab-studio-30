"""Video 046 — ¿Cómo funciona el picaporte de una puerta?
Science: inside the door edge there is a latch bolt whose tip is bevelled (slanted on one side). A spring keeps the
latch pushed out of the door edge. Turning the handle rotates a square spindle; a cam/retractor on the spindle pulls
the latch back into the door, so the door can open. When the handle is released, the spring pushes the latch out
again and returns the handle. When the door is closed, the slanted face of the latch rubs against the strike plate
on the frame, which pushes it in; once it is level with the hole in the strike plate, the spring snaps it in.
(No dimensions, lock types or deadbolts are described.)
"""
import math

ID = "046"
TITLE = "¿Cómo funciona el picaporte de una puerta?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo funciona el picaporte de una puerta?",
    "Dentro de la puerta hay un pestillo con la punta inclinada.",
    "Un muelle empuja el pestillo hacia fuera, hacia el marco.",
    "Al girar la manilla, el eje mueve una pieza que tira del pestillo.",
    "El pestillo se esconde y la puerta se puede abrir.",
    "Sueltas la manilla y el muelle lo devuelve a su sitio.",
    "Al cerrar, su cara inclinada roza el marco, entra y luego encaja en el hueco.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"picaporte", "puerta", "pestillo", "punta", "inclinada", "muelle", "marco", "manilla", "eje",
            "esconde", "abrir", "devuelve", "cerrar", "roza", "encaja", "hueco"}

WOOD = (150, 100, 60)
WOOD_D = (110, 72, 42)
FRAME = (120, 82, 50)
Y = 780  # latch axis


def door(E, d, dx=0):
    E.rrect(d, 120 + dx, 520, 640 + dx, 1100, 14, WOOD)
    E.rrect(d, 330 + dx, 700, 640 + dx, 860, 8, WOOD_D)  # mortise for latch


def frame(E, d):
    E.rrect(d, 700, 520, 860, 1100, 10, FRAME)
    E.rrect(d, 694, 680, 712, 880, 4, E.SIL)          # strike plate
    E.rrect(d, 694, Y - 40, 790, Y + 40, 6, E.CAV)    # hole


def spring(E, d, x0, x1, dx=0):
    n = 8
    pts = []
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        pts.append((x + dx, Y + (26 if k % 2 else -26)))
    E.line(d, pts, E.SIL_H, 6)


def latch(E, d, ext, dx=0, show_spring=True):
    tip = 640 + 80 * ext + dx
    back = tip - 220
    if show_spring:
        spring(E, d, 345, back - dx, dx)
    E.rrect(d, back, Y - 30, tip - 50, Y + 30, 6, E.BRA)
    E.poly(d, [(tip - 52, Y - 30), (tip, Y - 30), (tip - 52, Y + 30)], fill=E.BRA_H)  # bevelled tip
    return tip


def handle(E, d, a, dx=0):
    cx, cy = 450 + dx, 620
    E.circle(d, cx, cy, 34, fill=E.SIL_D)
    E.line(d, [(cx, cy), (cx - 200 * math.cos(a), cy + 200 * math.sin(a))], E.SIL, 22)
    E.rrect(d, cx - 12, cy - 12, cx + 12, cy + 12, 3, E.BG1)  # square spindle
    return cx, cy


def cam_link(E, d, a, ext, dx=0):
    cx, cy = 450 + dx, 620
    ax, ay = cx + 50 * math.cos(-a - 1.2), cy + 60 + 30 * a
    back = 640 + 80 * ext + dx - 220
    E.line(d, [(cx, cy), (ax, ay), (back + 10, Y - 30)], E.AMB, 8)


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: handle turning, latch going in and out
        k = 0.5 + 0.5 * math.sin(u * 3.2)
        door(E, d); frame(E, d)
        latch(E, d, 1 - 0.85 * k)
        handle(E, d, 0.55 * k)
        E.pill(d, "PICAPORTE", 540, 1150, 42)
    elif i == 1:  # latch with slanted tip inside the door
        door(E, d); frame(E, d)
        tip = latch(E, d, 1, show_spring=False)
        E.label(d, "PESTILLO", 480, 940, 46, color=E.BRA_H)
        E.arrow(d, 760, 640, tip - 20, Y - 40, E.AMB, 6, 22)
        E.label(d, "PUNTA INCLINADA", 620, 590, 40, color=E.AMB)
    elif i == 2:  # spring pushes latch outwards
        door(E, d); frame(E, d)
        k = E.ease(min(1, u / (L * 0.5)))
        latch(E, d, 0.3 + 0.7 * k)
        E.label(d, "MUELLE", 380, 660, 44, color=E.SIL_H)
        E.arrow(d, 520, 940, 680, 940, E.AMB, 8, 28)
        E.label(d, "HACIA EL MARCO", 560, 1010, 40, color=E.AMB)
    elif i == 3:  # turn handle: spindle + cam pull the latch
        k = E.ease(min(1, u / (L * 0.6)))
        ext = 1 - 0.95 * k
        door(E, d); frame(E, d)
        latch(E, d, ext)
        cam_link(E, d, 0.6 * k, ext)
        handle(E, d, 0.6 * k)
        E.label(d, "EJE", 450, 460, 44, color=E.SIL_H)
        E.label(d, "TIRA DEL PESTILLO", 420, 1020, 40, color=E.AMB)
        E.arrow(d, 600, 960, 470, 960, E.AMB, 6, 22)
    elif i == 4:  # latch hidden, door opens
        k = E.ease(min(1, u / (L * 0.6)))
        dx = -160 * k
        frame(E, d); door(E, d, dx)
        latch(E, d, 0.05, dx)
        handle(E, d, 0.6, dx)
        E.arrow(d, 560, 470, 400, 470, E.AMB, 8, 28)
        E.pill(d, "SE ABRE", 780, 420, 44)
    elif i == 5:  # release handle, spring returns latch
        k = E.ease(min(1, u / (L * 0.5)))
        door(E, d); frame(E, d)
        latch(E, d, 0.05 + 0.95 * k)
        handle(E, d, 0.6 * (1 - k))
        E.label(d, "MUELLE", 380, 680, 44, color=E.SIL_H)
        E.arrow(d, 560, 960, 700, 960, E.AMB, 8, 28)
        E.label(d, "VUELVE", 620, 1030, 42, color=E.AMB)
    elif i == 6:  # closing: bevel pushed in by strike, then snaps into hole
        p = min(1, u / (L * 0.8))
        dx = -150 * (1 - E.ease(p))
        if dx < -60:
            ext = 1.0
        elif dx < -6:
            ext = max(0.05, (-dx - 6) / 54)
        else:
            ext = 1.0
        frame(E, d); door(E, d, dx)
        latch(E, d, ext, dx)
        E.arrow(d, 300, 470, 470, 470, E.AMB, 8, 28)
        if -60 <= dx < -6:
            E.label(d, "ENTRA", 780, 420, 46, color=E.AMB)
        elif dx >= -6:
            E.pill(d, "ENCAJA", 780, 420, 44)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("click", s[0] + 0.3), ("pop", s[1] + 0.6), ("zip", s[2] + 0.4, 0.8), ("click", s[3] + 1.0),
            ("whoosh", s[4] + 0.4, 1.0), ("click", s[5] + 1.0), ("click", s[6] + 2.2)]
