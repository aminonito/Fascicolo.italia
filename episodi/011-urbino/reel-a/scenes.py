import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from urb import *
W, H = 1080, 1920
FY = 1300
BB = (40, 640, 1040, 1300)
MT = "mappa: Natural Earth · schema non in scala"

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

def build(i, dur, a, words):
    T0 = Clock(words, a)
    def T(p, n=0):
        nrm = lambda s: re.sub(r"[^\w']", "", s.lower())
        cs = lambda s: re.sub(r"[^\w']", "", s)
        hits = [w for w in words if cs(w[0]) == cs(p)] or [w for w in words if nrm(w[0]) == nrm(p)]
        if hits: return a + hits[min(n, len(hits) - 1)][1]
        try: return T0(p, n)
        except KeyError: return a + 0.5
    sc = Scene(dur)
    if i == 0:
        te = T("E") - 0.3
        sc.add(Text("Il furto\ndel *secolo*", (540, 330), a, size=110, anchor="ma", align="m"))
        sc.add(Sala(BB, a, te + 0.6, gone={0: a + 0.5, 1: a + 0.9, 2: a + 1.3}, night=True, torch=a, captions=False, label=""))
        sc.add(Icon("velvet", (540, 960), te, size=460), "hit")
        sc.add(Pill("UN ACQUISTO DI VELLUTO", (540, 1290), T("velluto") - 0.2, size=56, accent=True))
        sc.footer = "Fonti: ANSA · San Marino RTV · Affaritaliani · sagome stilizzate"
    elif i == 1:
        tn = T("Nebbia") - 0.3; tm = T("museo") - 0.3; td = T("Dal") - 0.3
        sc.add(Calendar((880, 450), 170, [(a, "URBINO", "1975")], a, td), "paper")
        sc.add(Palazzo(BB, a + 0.2, td + 0.2, night=True, fog=True, scaf_t=T("un'impalcatura") - 0.3, label=""))
        sc.add(Pill("NEBBIA", (540, 570), tn, T("un'impalcatura") - 0.2, size=56))
        sc.add(Pill("IMPALCATURA", (540, 570), T("un'impalcatura") - 0.2, tm, size=56, accent=True))
        sc.add(Pill("NESSUN ALLARME", (540, 570), tm, td, size=56, accent=True))
        sc.add(Sala(BB, td, None, gone={0: T("Piero") + 0.2, 1: T("Francesca") + 0.2, 2: T("Raffaello") + 0.2}, captions=False, label=""))
        sc.add(Pill("2 PIERO DELLA FRANCESCA + 1 RAFFAELLO", (540, 570), T("due") - 0.2, size=44, accent=True))
        sc.add(Text("Palazzo Ducale", (540, 330), td, size=100, anchor="ma", align="m"))
        sc.footer = "Fonti: ANSA · Il Giornale dell'Arte · Prima Bergamo · schema non in scala"
    elif i == 2:
        tp = T("Proprio") - 0.3
        sc.add(Text("Poche ore\n*dopo*", (540, 330), a, tp, size=110, anchor="ma", align="m"))
        sc.add(Icon("shop", (540, 860), a + 0.2, T("velluto") - 0.2, size=480, label="PESARO"), "pop")
        sc.add(Icon("velvet", (540, 880), T("velluto") - 0.2, size=480), "hit")
        sc.add(Pill("PER IL FIDANZATO", (540, 1240), T("fidanzato") - 0.2, tp, size=56, accent=True))
        sc.add(Text("L'appello:\n*«avvolgeteli nel velluto»*", (540, 330), tp + 0.1, size=84, anchor="ma", align="m"))
        sc.add(Icon("megaphone", (820, 1200), tp + 0.3, size=220), "pop")
        sc.footer = "Fonti: San Marino RTV · Affaritaliani · archeosardegna"
    elif i == 3:
        ti = T("I") - 0.3; tc = T("riscatto") - 0.6
        sc.add(Figure([(0, 340, FY)], a, ti, kind="police", s=1.2), "pop")
        sc.add(Figure([(0, 700, FY)], a + 0.3, ti, kind="police", s=1.2, flip=-1), "pop")
        sc.add(Text("La *pista*", (540, 330), a, ti, size=110, anchor="ma", align="m"))
        for k, (kind, _, _, _) in enumerate(ART):
            sc.add(Icon("art_" + kind, (220 + k * 320, 860), ti + 0.2 * k, tc, size=280), "pop" if k == 0 else None)
        sc.add(Text("Troppo\n*famosi*", (540, 330), ti, tc, size=110, anchor="ma", align="m"))
        sc.add(Stamp("INVENDIBILI", (540, 1150), T("famosi") - 0.1, tc, size=90, rot=-8))
        sc.add(Text("Il *riscatto*", (540, 330), tc, size=110, anchor="ma", align="m"))
        sc.add(Icon("ear", (540, 900), tc, size=440), "hit")
        sc.footer = "Fonti: San Marino RTV · archeosardegna · Affaritaliani"
    elif i == 4:
        ti = T("Il") - 0.3; tt = T("i", 0) - 0.3
        sc.add(Figure([(0, 330, FY)], a, ti, kind="suit", s=1.2, label="FINTI ACQUIRENTI"), "pop")
        sc.add(Figure([(0, 560, FY)], a + 0.3, ti, kind="suit", s=1.2), None)
        sc.add(Icon("money", (820, 900), a + 0.6, ti, size=260), "pop")
        sc.add(MapEl(BB, [(ti, (11.0, 44.9), 230)], ti, tt + 0.4,
                     pins=[dict(at="Urbino", label="URBINO", t=ti + 0.2, side="r", color=GOLD),
                           dict(at="Locarno", label="LOCARNO", t=ti + 0.6, side="r", color=RED)],
                     routes=[dict(pts=["Urbino", "Bologna", "Locarno"], t=ti + 0.4, d=1.6, icon="painting", color=RED)], title=""))
        sc.add(Calendar((540, 470), 200, [(ti, "MARZO 1976", "23")], ti, tt), "paper")
        sc.add(Icon("hotel", (540, 900), tt, size=420), "pop")
        sc.add(Flash(tt))
        for k, (kind, _, _, _) in enumerate(ART):
            sc.add(Icon("art_" + kind, (220 + k * 320, 1200), tt + 0.3 + 0.25 * k, size=240), "pop" if k == 0 else None)
        sc.add(Stamp("RITROVATI", (540, 520), T("ritrovati") - 0.1, size=100, rot=-8))
        sc.footer = "Fonti: ANSA · Prima Bergamo · Il Giornale dell'Arte · " + MT
    elif i == 5:
        sc.add(Text("Perché rubare\nquadri *invendibili?*", (540, 330), a, size=92, anchor="ma", align="m"))
        sc.add(Sala((90, 560, 990, 1110), a + 0.2, None, captions=False, label=""))
        sc.add(Text("Storia completa su YouTube", (540, 1185), T("storia"), size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(90), (540, 1345), T("Fascicolo"), anim="pop", shadow=False), "hit")
        sc.footer = "Ricostruzione a scopo divulgativo · voce generata con sintesi vocale"
    return sc
