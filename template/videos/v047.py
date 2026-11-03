"""Video 047 — ¿Cómo funciona un pulverizador de gatillo?
Science: a trigger sprayer is a small hand pump. Squeezing the trigger pushes a piston into a cylinder full of
liquid. The pressure closes the inlet one-way (check) valve and opens the outlet valve, so the liquid is forced
through a very small hole in the nozzle; the fast jet breaks up into tiny droplets (a fine mist). Releasing the
trigger, a spring returns trigger and piston; the cylinder volume grows, the outlet valve closes, the inlet valve
opens and liquid is drawn up the dip tube from the bottle, ready for the next squeeze.
(No pressures, droplet sizes or specific valve designs are claimed.)
"""
import math

ID = "047"
TITLE = "¿Cómo funciona un pulverizador de gatillo?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Cómo lanza una nube tan fina un pulverizador?",
    "Al apretar el gatillo, empujas un pistón dentro de un cilindro.",
    "El pistón presiona el líquido, que cierra una válvula y abre otra.",
    "El líquido sale a presión por un agujero diminuto de la boquilla.",
    "Allí se rompe en gotitas muy finas: una nube.",
    "Al soltar, un muelle devuelve el gatillo y el pistón.",
    "Eso aspira líquido de la botella por el tubo, listo para otro apretón.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"nube", "fina", "pulverizador", "gatillo", "pistón", "cilindro", "presiona", "líquido", "válvula",
            "presión", "agujero", "boquilla", "gotitas", "muelle", "aspira", "tubo", "botella"}

LIQ = (110, 190, 255)
BODY = (60, 170, 140)
BOTTLE = (200, 225, 245)


def bottle(E, d, level=0.7):
    E.rrect(d, 380, 660, 820, 1160, 40, E.mix(E.BG2, BOTTLE, 0.35), outline=BOTTLE, w=4)
    top = 1150 - 470 * level
    E.rrect(d, 390, top, 810, 1150, 34, E.mix(E.BG2, LIQ, 0.55))
    E.line(d, [(640, 600), (640, 1130)], E.SIL_H, 8)  # dip tube


def head(E, d, press=0.0, liquid=0.8, inlet_open=False, outlet_open=False):
    E.rrect(d, 200, 400, 760, 640, 30, BODY)
    E.rrect(d, 400, 470, 720, 560, 10, E.BG1)                 # cylinder
    px = 420 + 110 * press                                    # piston left face
    E.rrect(d, px + 40, 476, 714, 554, 8, E.mix(E.BG1, LIQ, 0.4 + 0.5 * liquid))
    E.rrect(d, px, 474, px + 40, 556, 6, E.SIL)               # piston
    E.line(d, [(px, 515), (330 + 30 * press, 515)], E.SIL_D, 12)  # rod
    E.line(d, [(700, 470), (700, 440), (215, 440)], E.mix(E.BG1, LIQ, 0.7), 12)  # outlet channel
    E.rrect(d, 190, 425, 220, 455, 6, E.SIL_H)                # nozzle
    oy = 440 - (14 if outlet_open else 0)
    E.circle(d, 650, oy, 14, fill=E.AMB if outlet_open else E.SIL_D)   # outlet valve
    iy = 575 + (14 if inlet_open else 0)
    E.circle(d, 640, iy, 14, fill=E.AMB if inlet_open else E.SIL_D)    # inlet valve
    E.line(d, [(640, 556), (640, 600)], E.SIL_H, 8)


def trigger(E, d, press=0.0):
    x = 300 + 30 * press
    E.poly(d, [(250, 640), (300, 640), (x + 20, 860), (x - 30, 860)], fill=E.SIL)


def mist(E, d, u, k=1.0, n=26):
    for j in range(n):
        f = (u * 1.3 + j / n) % 1
        a = math.pi + 0.45 * math.sin(j * 2.3)
        r = 20 + 260 * f
        E.circle(d, 190 + r * math.cos(a), 440 + r * math.sin(a), max(2, 9 - 6 * f) * k,
                 fill=E.mix(E.BG1, LIQ, 0.95 - 0.5 * f))


OX = 170  # horizontal shift so the mist stays on screen


class _Shift:
    """Wraps the engine so every drawing call is shifted OX px to the right."""
    def __init__(self, E):
        self._E = E

    def __getattr__(self, k):
        return getattr(self._E, k)

    def rrect(self, d, x0, y0, x1, y1, *a, **k):
        return self._E.rrect(d, x0 + OX, y0, x1 + OX, y1, *a, **k)

    def circle(self, d, x, y, *a, **k):
        return self._E.circle(d, x + OX, y, *a, **k)

    def line(self, d, pts, *a, **k):
        return self._E.line(d, [(x + OX, y) for x, y in pts], *a, **k)

    def poly(self, d, pts, *a, **k):
        return self._E.poly(d, [(x + OX, y) for x, y in pts], *a, **k)

    def arrow(self, d, x0, y0, x1, y1, *a, **k):
        return self._E.arrow(d, x0 + OX, y0, x1 + OX, y1, *a, **k)

    def label(self, d, t, x, y, *a, **k):
        return self._E.label(d, t, x + OX, y, *a, **k)

    def pill(self, d, t, x, y, *a, **k):
        return self._E.pill(d, t, x + OX, y, *a, **k)


def scene(i, u, L, E, im, d):
    if i == 7:
        E.outro(d, u, "SÍGUEME")
        return
    _scene(i, u, L, _Shift(E), im, d)


def _scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: trigger being squeezed, mist coming out
        p = 0.5 + 0.5 * math.sin(u * 4)
        bottle(E, d); head(E, d, press=p, outlet_open=True); trigger(E, d, p)
        mist(E, d, u)
        E.pill(d, "PULVERIZADOR", 420, 320, 42)
    elif i == 1:  # trigger pushes a piston into a cylinder
        p = E.ease(min(1, u / (L * 0.6)))
        bottle(E, d); head(E, d, press=p); trigger(E, d, p)
        E.label(d, "PISTÓN", 440, 340, 44, color=E.SIL_H)
        E.label(d, "CILINDRO", 610, 600, 40, color=E.WHITE)
        E.label(d, "GATILLO", 140, 920, 42, color=E.AMB)
    elif i == 2:  # pressure closes inlet, opens outlet
        bottle(E, d); head(E, d, press=0.7, outlet_open=True); trigger(E, d, 0.7)
        E.pill(d, "SE ABRE", 640, 330, 38)
        E.arrow(d, 650, 365, 650, 420, E.AMB, 6, 22)
        E.label(d, "SE CIERRA", 760, 720, 40, color=E.SIL_H)
        E.arrow(d, 720, 690, 660, 600, E.SIL_H, 6, 22)
    elif i == 3:  # liquid forced through tiny nozzle hole
        bottle(E, d); head(E, d, press=0.85, outlet_open=True); trigger(E, d, 0.85)
        for j in range(5):
            f = (u * 1.6 + j / 5) % 1
            E.circle(d, 690 - 470 * f, 440, 8, fill=E.WHITE)
        E.label(d, "AGUJERO DIMINUTO", 330, 330, 40, color=E.AMB)
        E.arrow(d, 260, 360, 210, 420, E.AMB, 6, 22)
    elif i == 4:  # breaks into fine droplets
        bottle(E, d); head(E, d, press=1.0, outlet_open=True); trigger(E, d, 1.0)
        mist(E, d, u, n=40)
        E.pill(d, "GOTITAS FINAS", 160, 960, 42)
    elif i == 5:  # spring returns trigger and piston
        p = 1 - E.ease(min(1, u / (L * 0.6)))
        bottle(E, d); head(E, d, press=p, liquid=0.3); trigger(E, d, p)
        zx = 330 + 30 * p
        pts = [(zx + 15 * k, 600 + (14 if k % 2 else -14)) for k in range(7)]
        E.line(d, pts, E.SIL_H, 5)
        E.label(d, "MUELLE", 420, 700, 40, color=E.SIL_H)
        E.arrow(d, 300, 360, 470, 360, E.AMB, 6, 22)
    elif i == 6:  # suction draws liquid up the dip tube
        k = min(1, u / (L * 0.8))
        bottle(E, d, level=0.7 - 0.05 * k); head(E, d, press=0.0, liquid=k, inlet_open=True)
        trigger(E, d, 0.0)
        for j in range(5):
            f = (u * 1.2 + j / 5) % 1
            E.circle(d, 640, 1110 - 520 * f, 9, fill=LIQ)
        E.label(d, "ASPIRA", 200, 900, 44, color=LIQ)
        E.arrow(d, 260, 860, 620, 760, LIQ, 6, 22)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 1.0), ("click", s[1] + 0.8), ("pop", s[2] + 0.8), ("zip", s[3] + 0.4, 0.8),
            ("whoosh", s[4] + 0.2, 1.2), ("click", s[5] + 0.8), ("zip", s[6] + 0.4, 1.0)]
