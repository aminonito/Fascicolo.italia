import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from cir import *
import fx
W, H = 1080, 1920
FY = 1300
BB = (40, 640, 1040, 1320)
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
        te = T("E") - 0.3; to = T("obbligazioni") - 0.2
        sc.add(Text("Torino\n*1856*", (540, 300), a, te, size=110, anchor="ma", align="m"))
        sc.add(Icon("can", (540, 900), a, te, size=520), "pop")
        sc.add(Icon("tomato", (300, 1200), a + 0.5, te, size=200), "pop")
        sc.add(Icon("peas", (780, 1200), a + 0.8, te, size=200), "pop")
        sc.add(Text("*35.000*\nrisparmiatori", (540, 340), te, size=104, anchor="ma", align="m"))
        sc.add(Savers((80, 900, 1000, 1260), 4, te, None, drop_t=to + 0.4, s=1.3))
        sc.add(Stamp("BLOCCATE", (540, 1000), T("bloccate") + 0.1, size=120, rot=-8))
        sc.footer = "Fonti: Focus · Wikipedia (Cirio) · Blitz quotidiano · Money.it"
    elif i == 1:
        tn = T("Negli") - 0.3; tf = T("presidente") - 0.3; ts = T("campione") - 0.4
        sc.add(Text("La *Cirio*", (540, 320), a, tn, size=120, anchor="ma", align="m"))
        sc.add(Icon("can", (540, 900), a, tn, size=480), "pop")
        sc.add(Text("Anni *Novanta*", (540, 320), tn, size=110, anchor="ma", align="m"))
        sc.add(Img(label_card(["Sergio Cragnotti", "nato a Roma, 1940", "presidente della Lazio", "dal 1992"], 820, title="SCHEDA"), (540, 660), tn, anim="drop", rot=-2), "paper")
        sc.add(Figure(walk([(-100, FY), (300, FY)], tn, 300), tn, kind="suit", s=0.9, label="SAGOMA · NESSUNA FOTO"), "pop")
        sc.add(Icon("ball", (720, 1180), tf, size=180), "pop")
        sc.add(Icon("shield_q", (880, 1150), ts, size=240, label="SCUDETTO 2000"), "pop")
        sc.footer = "Fonti: Lazio Stories · WSC · UEFA · Wikipedia"
    elif i == 2:
        tl_ = T("tramite") - 0.3; tf = T("Finiscono") - 0.2; tp = tf - 0.2
        sc.add(Text("*7* prestiti\nobbligazionari", (540, 300), a, size=100, anchor="ma", align="m"))
        for k in range(7):
            sc.add(Img(bond17(300, lines=("2000-2002",), seed=k + 2), (200 + (k % 4) * 230, 760 + (k // 4) * 240), a + 0.2 + k * 0.25, tl_, anim="drop", rot=-4 + k), "paper")
        sc.add(WorldMap(BB, [(tl_, (6.5, 47.5), 9), (dur, (7.5, 47.0), 7)], tl_, tp + 0.2,
                        pins=[dict(at="Lussemburgo", label="LUSSEMBURGO", t=tl_ + 0.3, side="r", color=GOLD),
                              dict(at="Roma", label="ROMA", t=tl_ + 0.2, side="r", color=RED)],
                        routes=[dict(pts=["Roma", "Lussemburgo"], t=tl_ + 0.4, d=1.0, icon="money", color=GOLD)], title=MT))
        sc.add(Icon("family", (540, 1000), tf, size=460, label="LE FAMIGLIE"), "pop")
        sc.add(Icon("piggy", (860, 1200), tf + 0.5, size=200), "pop")
        sc.footer = "Fonti: Blitz quotidiano · Luiss CERADI · Lazio Stories · Il Giornale"
    elif i == 3:
        tu = T("Un") - 0.3; tc = T("catena") - 0.4; tm = T("miliardo") - 0.3
        sc.add(Calendar((540, 900), 360, [(a, "NOVEMBRE", "2002")], a, tu + 0.2), "paper")
        sc.add(Img(bond17(860, lines=("150 milioni di euro", "scadenza: novembre 2002")), (540, 900), tu, tc, anim="drop", rot=-2), "paper")
        sc.add(Stamp("NON RIMBORSATO", (540, 960), T("rimborsato") - 0.1, tc, size=96, rot=-8))
        for k in range(6):
            sc.add(Img(bond17(300, lines=("default",), seed=k + 9), (200 + (k % 3) * 340, 760 + (k // 3) * 300), tc + k * 0.18, anim="drop", rot=-6 + k * 2), "paper")
        sc.add(Text("Effetto *domino*", (540, 300), tc, tm, size=110, anchor="ma", align="m"))
        sc.add(Text("*1,125*\nmiliardi di euro", (540, 340), tm, size=110, anchor="ma", align="m"))
        sc.add(Stamp("DEFAULT", (540, 1000), tm + 0.4, size=150, rot=-10))
        sc.footer = "Fonti: Il Giornale · Luiss CERADI · Blitz quotidiano · Lazio Stories"
    elif i == 4:
        ta = T("venduti") - 0.1; tp = T("Per", 1) - 0.3
        sc.add(Text("Secondo\ni *giudici*", (540, 300), a, ta, size=110, anchor="ma", align="m"))
        sc.add(DebtShift(BB, a, tp + 0.2, shift=[(a + 0.4, 0.7)], zero_t=ta + 1.8, n=8))
        sc.add(Text("Dalle *banche*\nai risparmiatori", (540, 330), ta, tp, size=96, anchor="ma", align="m"))
        sc.add(Img(sentence_card(["Sergio Cragnotti", "bancarotta", "5 anni e 3 mesi", "Cassazione, 2021"], w=840), (540, 930), tp, anim="drop", rot=-2), "paper")
        sc.add(Icon("gavel", (860, 1300), tp + 0.4, size=220), "pop")
        sc.add(Text("La *condanna*", (540, 320), tp, size=110, anchor="ma", align="m"))
        sc.add(Stamp("DEFINITIVA", (540, 1180), T("5") + 0.3, size=100, rot=-8))
        sc.footer = "Fonti: La Notizia · Blitz quotidiano · Calcio e Finanza · Money.it"
    elif i == 5:
        sc.add(Text("Come si riconosce\nun bond *rischioso?*", (540, 330), a, size=80, anchor="ma", align="m"))
        sc.add(Img(bond17(640, lines=("rendimento alto", "rating?", "prospetto?")), (540, 900), a + 0.2, T("storia") - 0.2, anim="drop", rot=-3), "paper")
        sc.add(Icon("magnifier", (800, 1080), a + 0.8, T("storia") - 0.2, size=240), "pop")
        sc.add(Text("Storia completa su YouTube", (540, 1185), T("storia"), size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(90), (540, 1345), T("Fascicolo"), anim="pop", shadow=False), "hit")
        sc.footer = "Ricostruzione divulgativa · non è consulenza finanziaria"
    return sc
