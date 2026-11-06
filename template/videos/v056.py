"""Video 056 — ¿Cómo funciona la válvula de un neumático?
Science: a common tyre valve has a core with a sealing plug and a spring. The spring presses the plug against a seat
and keeps the valve closed. The air pressure inside the tyre also pushes the plug against the seat, so the higher the
pressure inside, the tighter it seals. When inflating, the pump head presses the central pin and/or the pump's air,
at a higher pressure, pushes the plug inwards: the valve opens and air goes in. When the pump is removed, the spring
and the inside pressure close it again.
(No sizes, pressures, brand names or other valve types are claimed.)
"""
import math

ID = "056"
TITLE = "¿Cómo funciona la válvula de un neumático?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "¿Por qué el aire entra en la rueda pero no sale?",
    "La válvula tiene dentro un tapón y un pequeño muelle.",
    "El muelle aprieta el tapón contra un asiento y la cierra.",
    "Además, el aire de la rueda empuja el tapón hacia fuera.",
    "Cuanta más presión hay dentro, más fuerte queda cerrada.",
    "Al inflar, el inflador empuja el tapón hacia dentro y el aire entra.",
    "Al retirarlo, el muelle y la presión la cierran otra vez.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"aire", "entra", "rueda", "sale", "válvula", "tapón", "muelle", "aprieta", "asiento", "cierra",
            "empuja", "fuera", "presión", "cerrada", "inflar", "inflador", "dentro", "retirarlo"}

TX0, TX1 = 440, 640       # stem outer walls
IX0, IX1 = 478, 602       # inner bore
TOP, BOT = 330, 960       # stem top / bottom (bottom opens into the tyre)
SEAT = 600                # seat (narrowing) y
CX = 540
RUB = (40, 42, 50)
AIR = (150, 205, 255)
PUMP = (52, 96, 150)


def valve(E, d, open_=0.0, hi_plug=False, hi_spring=False, hi_seat=False, tyre_air=20, pressure_arrows=False,
          flow=None, pump=False, pin_push=0.0):
    dy = 50 * open_
    # tyre (inside) below the stem
    E.rrect(d, 80, BOT - 10, 1000, 1180, 30, (30, 36, 54), outline=RUB, w=8)
    E.label(d, "DENTRO DE LA RUEDA", 540, 1130, 36, color=E.MUTED)
    for k in range(tyre_air):
        fx = ((k * 37) % 23) / 22.0; fy = ((k * 53) % 7) / 6.0
        x = 120 + fx * 840
        if IX0 - 20 < x < IX1 + 20 and fy < 0.4: x += 160
        E.circle(d, x, BOT + 30 + fy * 70, 8, fill=AIR)
    # stem body
    E.rrect(d, TX0, TOP, TX1, BOT, 16, E.SIL_D)
    E.rrect(d, TX0 - 40, BOT - 70, TX1 + 40, BOT, 14, RUB)          # rubber base
    E.rrect(d, IX0, TOP - 4, IX1, BOT + 4, 8, (22, 30, 50))          # bore
    # seat (narrowing ring)
    sc = E.AMB if hi_seat else E.SIL
    E.poly(d, [(IX0, SEAT - 30), (IX0 + 30, SEAT), (IX0, SEAT + 6)], fill=sc)
    E.poly(d, [(IX1, SEAT - 30), (IX1 - 30, SEAT), (IX1, SEAT + 6)], fill=sc)
    # spring: from plug bottom down to a fixed bar
    bar = 840
    E.rrect(d, IX0, bar, IX1, bar + 16, 4, E.SIL)
    py = SEAT + 4 + dy                    # plug top
    pb = py + 34                          # plug bottom
    spc = E.AMB if hi_spring else E.SIL_H
    n = 7; pts = []
    for k in range(n * 2 + 1):
        y = pb + (bar - pb) * k / (n * 2)
        x = CX + (34 if k % 2 else -34) * (0 if k in (0, n * 2) else 1)
        pts.append((x, y))
    E.line(d, pts, spc, 6)
    # plug (rubber seal on a metal disc) + central pin going out of the top
    pc = E.AMB if hi_plug else (230, 90, 70)
    E.line(d, [(CX, py), (CX, TOP + 20 + dy * 0 + 40 * pin_push)], E.SIL_H, 10)
    E.rrect(d, IX0 + 14, py, IX1 - 14, pb, 10, pc, outline=E.SIL_D, w=3)
    # air flowing in through the open valve
    if flow is not None and open_ > 0.3:
        for k in range(6):
            s = (flow + k / 6) % 1.0
            y = TOP + s * (BOT - TOP + 60)
            x = CX + (0 if y < SEAT - 30 else (IX0 + 22 - CX if k % 2 else IX1 - 22 - CX) if y < pb + 10 else 0)
            E.circle(d, x, y, 8, fill=AIR)
    if pressure_arrows:
        for x in (CX - 50, CX + 50):
            E.arrow(d, x, bar + 90, x, pb + 18, E.HOT, 5, 20)
    if pump:   # pump head on top of the stem
        E.rrect(d, TX0 - 50, TOP - 90 + 40 * pin_push, TX1 + 50, TOP + 60, 20, PUMP, outline=E.BLUE_D, w=4)
        E.line(d, [(CX, TOP - 90 + 40 * pin_push), (CX, 270)], (60, 66, 80), 30)
    return py, pb


def scene(i, u, L, E, im, d):
    if i == 0:  # in action from frame 0: pump pushes air in, then the valve shuts and the air stays
        ph = u / L
        op = 1.0 if ph < 0.55 else max(0.0, 1 - (ph - 0.55) * 8)
        valve(E, d, op, flow=u * 1.4, pump=ph < 0.55, pin_push=1.0 if ph < 0.55 else 0, tyre_air=14 + int(10 * ph),
              pressure_arrows=ph >= 0.7)
        E.pill(d, "ENTRA" if ph < 0.55 else "NO SALE", 820, 460, 44)
    elif i == 1:  # plug and spring
        valve(E, d, 0, hi_plug=True, hi_spring=True)
        E.label(d, "TAPÓN", 790, SEAT + 20, 46, color=E.AMB)
        E.label(d, "MUELLE", 790, 740, 46, color=E.AMB)
    elif i == 2:  # spring presses plug against the seat
        k = E.ease(min(1, u / (L * 0.5)))
        valve(E, d, 1 - k, hi_spring=True, hi_seat=True)
        E.arrow(d, 390, 820, 390, SEAT + 30, E.AMB, 9, 30)
        E.label(d, "EMPUJA", 270, 720, 42, color=E.AMB)
        E.label(d, "ASIENTO", 790, SEAT - 30, 44, color=E.AMB)
        if k > 0.95:
            E.pill(d, "CERRADA", 820, 460, 42)
    elif i == 3:  # tyre air pushes the plug outwards
        valve(E, d, 0, hi_plug=True, pressure_arrows=True, tyre_air=24)
        E.label(d, "PRESIÓN", 800, 900, 44, color=E.HOT)
        E.label(d, "HACIA FUERA", 800, 520, 40, color=E.HOT)
        E.arrow(d, 800, 840, 800, 570, E.HOT, 8, 26)
    elif i == 4:  # more pressure -> tighter seal
        k = E.ease(min(1, u / (L * 0.7)))
        valve(E, d, 0, hi_plug=True, hi_seat=True, pressure_arrows=True, tyre_air=20 + int(18 * k))
        E.label(d, "+ PRESIÓN", 800, 900, 44, color=E.HOT)
        E.pill(d, "MÁS CERRADA", 820, 460, 42)
    elif i == 5:  # pump pushes the plug inwards: air goes in
        k = E.ease(min(1, u / (L * 0.4)))
        valve(E, d, k, pump=True, pin_push=k, flow=u * 1.4, tyre_air=24 + int(10 * u / L))
        E.label(d, "INFLADOR", 820, 380, 42, color=E.AMB)
        E.arrow(d, 300, 500, 300, 760, E.AMB, 9, 30)
        E.label(d, "ENTRA", 300, 440, 44, color=E.AMB)
        if k > 0.5:
            yy = BOT - 40 + 40 * ((u * 1.5) % 1.0)
            E.arrow(d, CX, yy - 50, CX, yy + 30, E.COLD, 7, 22)
    elif i == 6:  # pump removed: spring + pressure close it again
        k = E.ease(min(1, u / (L * 0.5)))
        valve(E, d, 1 - k, hi_spring=True, pressure_arrows=k > 0.5, tyre_air=34)
        if k > 0.95:
            E.pill(d, "CERRADA OTRA VEZ", 700, 460, 40)
    else:
        E.outro(d, u, "SÍGUEME")


def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.1, 0.8), ("pop", s[1] + 0.6), ("click", s[2] + 0.9), ("pop", s[3] + 0.6),
            ("click", s[4] + 0.8), ("whoosh", s[5] + 0.4, 1.0), ("click", s[6] + 0.9)]
