"""Video 012 — ¿Por qué vemos el rayo antes de oír el trueno?
Science: a lightning stroke heats the air in its channel extremely quickly; the air expands violently and
launches a sound wave, the thunder. Light and sound are produced at the same moment, but light travels so
fast that it reaches us practically instantly, while sound in air travels at roughly 340 m/s, taking about
3 seconds per kilometre. So the seconds between flash and thunder divided by 3 give the distance in km.
If you can hear thunder, the storm is close enough to be dangerous: seek shelter.
(No channel temperature and no exact danger radius are claimed.)
"""
import math

ID = "012"
TITLE = "¿Por qué vemos el rayo antes de oír el trueno?"
SUBTITLE = "CURIOSIDADES DE LA CIENCIA"
LINES = [
    "Cuenta los segundos entre el rayo y el trueno, y sabrás la distancia.",
    "El rayo calienta el aire de golpe; al expandirse, suena el trueno.",
    "La luz y el sonido nacen a la vez, pero viajan muy distinto.",
    "La luz llega casi al instante.",
    "El sonido es mucho más lento: tarda unos tres segundos por kilómetro.",
    "Divide los segundos entre tres y tendrás los kilómetros.",
    "Y si oyes truenos, la tormenta está cerca: busca refugio.",
    "Sígueme para más curiosidades de la ciencia.",
]
KEYWORDS = {"segundos", "rayo", "trueno", "distancia", "aire", "golpe", "expandirse", "luz", "sonido", "vez",
            "instante", "lento", "tres", "kilómetro", "divide", "kilómetros", "truenos", "tormenta", "cerca", "refugio", "ciencia"}

CLOUD, CLOUD_D = (120, 132, 156), (86, 96, 118)
BOLT = (255, 240, 150)
SOUND = (150, 200, 255)
GROUND = (44, 70, 60)

def cloud(E, d, x, y, s=1.0):
    for dx, dy, r in ((-110, 20, 70), (-40, -20, 90), (50, -10, 85), (120, 25, 65), (0, 40, 80)):
        E.circle(d, x + dx * s, y + dy * s, r * s, fill=CLOUD_D)
    for dx, dy, r in ((-100, 5, 62), (-35, -32, 80), (50, -22, 76), (115, 12, 56)):
        E.circle(d, x + dx * s, y + dy * s, r * s, fill=CLOUD)

def bolt(E, d, x, y0, y1, w=1.0, col=BOLT):
    n = 6; pts = []
    for k in range(n + 1):
        yy = y0 + (y1 - y0) * k / n
        pts.append((x + (0 if k in (0, n) else (36 if k % 2 else -36)) * w, yy))
    E.line(d, pts, col, 14 * w)
    E.line(d, pts, E.WHITE, 5 * w)

def person(E, d, x, y, s=1.0):
    E.circle(d, x, y - 120 * s, 30 * s, fill=E.SIL)
    E.line(d, [(x, y - 90 * s), (x, y - 20 * s)], E.SIL, 14 * s)
    E.line(d, [(x, y - 20 * s), (x - 26 * s, y + 40 * s)], E.SIL, 12 * s)
    E.line(d, [(x, y - 20 * s), (x + 26 * s, y + 40 * s)], E.SIL, 12 * s)
    E.line(d, [(x - 40 * s, y - 70 * s), (x + 40 * s, y - 70 * s)], E.SIL, 10 * s)

def ground(E, d):
    E.rrect(d, 60, 1040, 1020, 1170, 0, GROUND)

def stopwatch(E, d, x, y, txt, r=110):
    E.circle(d, x, y, r, fill=E.CAV, outline=E.SIL_H, w=8)
    E.rrect(d, x - 20, y - r - 34, x + 20, y - r - 4, 6, E.SIL_H)
    E.label(d, txt, x, y, int(r * 0.9), color=E.WHITE)

def eye(E, d, x, y, r=36):
    E.poly(d, [(x - r * 1.6, y), (x, y - r), (x + r * 1.6, y), (x, y + r)], fill=E.WHITE)
    E.circle(d, x, y, r * 0.55, fill=(40, 60, 92))

def lanes(E, d, pl, ps, ul=True):
    x0, x1 = 210, 880
    E.label(d, "LUZ", 540, 440, 46, color=BOLT)
    E.label(d, "SONIDO", 540, 790, 46, color=SOUND)
    E.line(d, [(x0, 560), (x1, 560)], E.GRID, 4); E.line(d, [(x0, 910), (x1, 910)], E.GRID, 4)
    bolt(E, d, 140, 470, 640, 0.6); bolt(E, d, 140, 820, 990, 0.6)
    if pl > 0: E.arrow(d, x0, 560, E.lerp(x0, x1 - 20, pl), 560, color=BOLT, w=10, head=34)
    if ps > 0:
        xs = E.lerp(x0, x1 - 20, ps)
        for k in range(3):
            r = 40 + k * 26
            d.arc(E.P(xs - r, 910 - r, xs + r, 910 + r), -50, 50, fill=SOUND, width=6 * E.S)
    eye(E, d, 940, 560, 30); eye(E, d, 940, 910, 30)

def scene(i, u, L, E, im, d):
    if i == 0:  # count the seconds
        ground(E, d); cloud(E, d, 300, 420)
        if (u % 1.2) < 0.25 or u < 0.3: bolt(E, d, 300, 480, 1040)
        person(E, d, 840, 1000)
        n = min(3, int(u / (L / 3.2)) + 1)
        stopwatch(E, d, 760, 560, str(n))
        if u > 0.6: E.label(d, "SEGUNDOS", 760, 735, 42)
    elif i == 1:  # heated air expands -> thunder
        ground(E, d); cloud(E, d, 300, 420)
        bolt(E, d, 300, 480, 1040, 1.2)
        for k in range(4):
            r = ((u * 260 + k * 110) % 440) + 40
            fade = 1 - (r - 40) / 440
            d.arc(E.P(300 - r, 760 - r, 300 + r, 760 + r), -60, 60, fill=E.mix(E.BG2, SOUND, fade), width=8 * E.S)
        E.circle(d, 300, 760, 70, outline=E.HOT, w=6)
        if u > 0.3: E.label(d, "AIRE MUY CALIENTE", 540, 1105, 40, color=E.HOT)
        if u > 1.0: E.label(d, "¡TRUENO!", 800, 560, 64, color=SOUND)
    elif i == 2:  # born together, travel very differently
        p = E.ease((u - 0.3) / 1.6)
        lanes(E, d, min(1, p * 6), p * 0.2)
        if u > 0.2: E.pill(d, "A LA VEZ", 140, 715, 34)
    elif i == 3:  # light arrives almost instantly
        lanes(E, d, 1.0, 0.2 + 0.05 * E.ease(u / L))
        E.circle(d, 940, 560, 60, outline=BOLT, w=6)
        if u > 0.3: E.label(d, "CASI AL INSTANTE", 540, 650, 44, color=BOLT)
    elif i == 4:  # sound: about 3 s per km
        E.line(d, [(140, 760), (940, 760)], E.SIL, 8)
        for x, t in ((140, "0"), (940, "1 km")):
            E.line(d, [(x, 730), (x, 790)], E.SIL, 8); E.label(d, t, x if x < 900 else 900, 840, 44, color=E.WHITE)
        bolt(E, d, 140, 480, 720, 0.7)
        p = E.ease(u / (L * 0.85))
        xs = E.lerp(160, 920, p)
        for k in range(3):
            r = 40 + k * 28
            d.arc(E.P(xs - r, 760 - r, xs + r, 760 + r), -50, 50, fill=SOUND, width=7 * E.S)
        stopwatch(E, d, 700, 470, f"{min(3, int(p * 3 + 0.001)) if p < 1 else 3}", r=100)
        if u > 0.8: E.label(d, "≈ 3 s POR km", 540, 1040, 52, color=SOUND)
    elif i == 5:  # divide by three
        k1, k2, k3 = (E.back_out((u - t) / 0.4) for t in (0.1, 0.7, 1.3))
        if k1 > 0.05: stopwatch(E, d, 300, 560, "9", r=int(120 * k1))
        if k2 > 0.05: E.label(d, "÷ 3", 650, 560, int(110 * k2), color=E.AMB)
        if k3 > 0.05: E.label(d, "= 3 km", 540, 860, int(120 * k3), color=E.WHITE)
        if u > 1.3: E.label(d, "9 SEGUNDOS", 300, 735, 40, color=E.MUTED)
    elif i == 6:  # hear thunder -> seek shelter
        ground(E, d); cloud(E, d, 560, 420, 1.2)
        if (u % 1.0) < 0.2: bolt(E, d, 520, 500, 1040, 1.0)
        # house
        E.poly(d, [(700, 760), (880, 640), (1000, 760)], fill=HOUSE_ROOF)
        E.rrect(d, 720, 760, 980, 1040, 0, HOUSE)
        E.rrect(d, 820, 880, 890, 1040, 6, E.CAV)
        x = E.lerp(260, 760, E.ease(u / (L * 0.8)))
        person(E, d, x, 1000, 0.9)
        E.arrow(d, 300, 1110, 760, 1110, color=E.AMB, w=6)
        if u > 0.5: E.pill(d, "BUSCA REFUGIO", 300, 640, 38)
    else:
        E.outro(d, u, "SÍGUEME")

HOUSE, HOUSE_ROOF = (150, 120, 96), (176, 70, 56)

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("pop", s[0] + 0.1), ("click", s[0] + 1.0), ("click", s[0] + 2.0), ("whoosh", s[1] + 0.3, 1.2),
            ("whoosh", s[2] + 0.4, 0.6), ("pop", s[3] + 0.2), ("whoosh", s[4] + 0.2, 1.5), ("pop", s[5] + 1.3), ("whoosh", s[6] + 0.3, 0.9)]
