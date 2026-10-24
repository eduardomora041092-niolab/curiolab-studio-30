"""Video 016 — ¿Cómo se abre un paraguas?
Mechanism: the long ribs of an umbrella are hinged at their top end to a crown (top notch) fixed at the tip of the
shaft. Lower down, a sliding collar (the runner) surrounds the shaft. Each rib is joined to the runner by a short
stretcher, hinged at both ends. Pushing the runner up the shaft makes the stretchers push the ribs outward, so all
ribs open at once and pull the canopy taut. Near the top a small spring latch on the shaft pops out under the runner
and holds it up; pressing the latch lets the runner slide down and the umbrella closes.
(No sizes, rib counts or automatic-umbrella spring details are claimed.)
"""
import math

ID = "016"
TITLE = "¿Cómo se abre un paraguas?"
SUBTITLE = "¿CÓMO FUNCIONA POR DENTRO?"
LINES = [
    "Un solo empujón abre todas las varillas del paraguas.",
    "Las varillas largas cuelgan de una corona en la punta.",
    "Más abajo, la corredera rodea el mástil y se desliza.",
    "Una varilla corta une cada varilla larga a la corredera.",
    "Al subir la corredera, las cortas empujan las largas hacia fuera.",
    "Todas se abren a la vez y estiran la tela.",
    "Un pestillo con muelle sujeta la corredera; al apretarlo, se cierra.",
    "Sígueme para descubrir cómo funcionan más cosas.",
]
KEYWORDS = {"empujón", "varillas", "paraguas", "corona", "mástil", "corredera", "desliza", "corta", "largas",
            "fuera", "abren", "tela", "pestillo", "muelle", "sujeta", "cierra", "funcionan"}

CX, CY = 540, 430            # crown
R, F, SL = 420, 0.45, 220    # rib length, stretcher attach fraction, stretcher length
TH_CLOSED, TH_OPEN = math.radians(8), math.radians(74)
CLOTH, CLOTH_E = (52, 86, 150), (80, 120, 190)
SHAFT_BOTTOM = 1000

def geom(th):
    """Returns per-side list of (tip, attach) and the runner y for rib angle th (from the downward vertical)."""
    sides = []
    for s in (-1, -0.45, 0.45, 1):
        tip = (CX + s * R * math.sin(th), CY + R * math.cos(th))
        att = (CX + s * F * R * math.sin(th), CY + F * R * math.cos(th))
        sides.append((s, tip, att))
    ax, ay = F * R * math.sin(th), F * R * math.cos(th)
    ry = CY + ay + math.sqrt(max(0.0, SL * SL - ax * ax))
    return sides, ry

def umbrella(E, d, th, hl=None, cloth=True):
    sides, ry = geom(th)
    # shaft + handle
    E.line(d, [(CX, CY - 40), (CX, SHAFT_BOTTOM)], E.SIL, 12)
    hook = [(CX + 50 - 50 * math.cos(a), SHAFT_BOTTOM + 50 * math.sin(a)) for a in [k * math.pi / 12 for k in range(13)]]
    E.line(d, hook, E.BRA, 18)
    # canopy
    if cloth:
        tips = [t for s, t, a in sorted(sides, key=lambda x: x[0])]
        pts = [tips[0]]
        for k in range(1, len(tips)):
            a, b = tips[k - 1], tips[k]
            pts.append(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 10))
            pts.append(b)
        E.poly(d, [(CX, CY - 20)] + pts, fill=CLOTH)
        E.line(d, [(CX, CY - 20), tips[0]], CLOTH_E, 4); E.line(d, [(CX, CY - 20), tips[-1]], CLOTH_E, 4)
    rib_c = E.AMB if hl == "ribs" else E.SIL_H
    str_c = E.AMB if hl == "stretchers" else E.SIL_D
    for s, tip, att in sides:
        w = 7 if abs(s) == 1 else 4
        E.line(d, [(CX, CY), tip], rib_c, w)
        E.line(d, [att, (CX, ry)], str_c, w + (3 if hl == "stretchers" else 0))
        E.circle(d, att[0], att[1], 7, fill=str_c)
    run_c = E.AMB if hl == "runner" else E.SIL
    E.rrect(d, CX - 26, ry - 22, CX + 26, ry + 22, 8, run_c, outline=E.SIL_D, w=3)
    E.circle(d, CX, CY, 20, fill=E.AMB if hl == "crown" else E.SIL_H)
    return ry

def scene(i, u, L, E, im, d):
    if i == 0:  # one push opens everything
        k = E.ease(max(0.0, u - 0.3) / (L * 0.5))
        ry = umbrella(E, d, E.lerp(TH_CLOSED, TH_OPEN, k))
        E.arrow(d, CX + 90, ry + 110, CX + 90, ry + 10, color=E.AMB, w=9)
        E.label(d, "UN EMPUJÓN", 540, 1130, 50, color=E.AMB)
    elif i == 1:  # ribs hang from the crown
        umbrella(E, d, math.radians(30), hl="ribs", cloth=False)
        E.label(d, "CORONA", 780, 360, 46, color=E.AMB)
        E.arrow(d, 690, 375, 570, 420, color=E.AMB, w=6)
        if u > 0.6: E.label(d, "VARILLAS LARGAS", 540, 1130, 46, color=E.WHITE)
    elif i == 2:  # runner slides on the shaft
        th = math.radians(30) + math.radians(8) * math.sin(u * 2.5)
        ry = umbrella(E, d, th, hl="runner", cloth=False)
        E.label(d, "CORREDERA", 820, ry, 46, color=E.AMB)
        E.arrow(d, 640, ry - 40, 640, ry - 110, color=E.WHITE, w=6)
        E.arrow(d, 640, ry + 40, 640, ry + 110, color=E.WHITE, w=6)
    elif i == 3:  # stretchers join ribs to runner
        umbrella(E, d, math.radians(40), hl="stretchers", cloth=False)
        if u > 0.5: E.label(d, "VARILLA CORTA", 540, 1130, 46, color=E.AMB)
    elif i == 4:  # pushing the runner up opens the ribs
        k = E.ease(u / (L * 0.8))
        th = E.lerp(math.radians(15), TH_OPEN, k)
        ry = umbrella(E, d, th, hl="stretchers", cloth=False)
        E.arrow(d, CX + 80, ry + 120, CX + 80, ry + 20, color=E.AMB, w=9)
        sides, _ = geom(th)
        for s, tip, att in sides:
            if abs(s) == 1:
                E.arrow(d, tip[0], tip[1], tip[0] + s * 50, tip[1] - 30, color=E.WHITE, w=6, head=20)
        E.label(d, "HACIA FUERA", 540, 1130, 46, color=E.WHITE)
    elif i == 5:  # all open, canopy taut
        umbrella(E, d, TH_OPEN + math.radians(1.5) * math.sin(u * 5))
        if u > 0.5: E.pill(d, "TELA TENSA", 540, 1120, 40)
    elif i == 6:  # spring latch holds the runner; pressing it closes
        X0, X1 = 490, 590
        E.rrect(d, X0, 300, X1, 1150, 12, E.SIL)
        E.line(d, [(X0 + 15, 300), (X0 + 15, 1150)], E.SIL_H, 6)
        k1 = E.ease(u / (L * 0.35))
        t0 = L * 0.55
        press = u > t0
        top_latch = 720
        if not press:
            ry = E.lerp(1050, top_latch - 110, k1)
            out = 1.0 if ry < top_latch - 90 else 0.0
        else:
            out = 1.0 - E.ease(min(1.0, (u - t0) / 0.3))
            ry = E.lerp(top_latch - 110, 1050, E.ease(max(0.0, u - t0 - 0.6) / (L * 0.35)))
        # slot + latch: triangle that pops out of the shaft under the runner
        E.rrect(d, X1 - 10, top_latch - 40, X1 + 4, top_latch + 40, 4, E.CAV)
        E.poly(d, [(X1, top_latch - 40), (X1 + max(2, 55 * out), top_latch - 40), (X1, top_latch + 40)], fill=E.AMB)
        sp = [(X1 - 10 - 10 * (k % 2), top_latch - 30 + k * 7) for k in range(10)]
        E.line(d, sp, E.SIL_D, 4)
        E.rrect(d, X0 - 60, ry - 50, X1 + 60, ry + 50, 14, E.SIL_H, outline=E.SIL_D, w=4)
        E.label(d, "CORREDERA", 300, ry, 40, color=E.WHITE)
        E.label(d, "PESTILLO", 840, top_latch + 90, 44, color=E.AMB)
        if not press:
            if out > 0.5: E.label(d, "SUJETA", 840, top_latch - 160, 44, color=E.WHITE)
        else:
            E.arrow(d, 880, top_latch - 20, 665, top_latch - 20, color=E.WHITE, w=9)
            E.label(d, "APRIETA", 840, top_latch - 90, 44, color=E.WHITE)
            E.label(d, "SE CIERRA", 300, 1100, 44, color=E.AMB)
    else:
        E.outro(d, u, "SÍGUEME")

def sfx(segs):
    s = [x["start"] for x in segs]
    return [("whoosh", s[0] + 0.3, 0.8), ("pop", s[0] + 1.0), ("pop", s[1] + 0.4), ("whoosh", s[2] + 0.3, 0.8),
            ("pop", s[3] + 0.6), ("whoosh", s[4] + 0.2, 1.0), ("pop", s[5] + 0.5), ("click", s[6] + 1.0)]
