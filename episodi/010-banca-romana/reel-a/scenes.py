import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from rom import *
W, H = 1080, 1920
FY = 1300
BB = (40, 640, 1040, 1300)

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
        ts = T("stesso") - 0.3; tn = T("stesso", 1) - 0.3
        sc.add(Text("Banconote\n*gemelle*", (540, 330), a, size=110, anchor="ma", align="m"))
        sc.add(Img(banknote(680, serial="N. 048217", hl=False), (540, 810), a + 0.2, tn + 0.3, anim="drop", rot=-4), "paper")
        sc.add(Img(banknote(680, serial="N. 048217", hl=False), (540, 1160), a + 0.6, tn + 0.3, anim="drop", rot=3), "paper")
        sc.add(Pill("STESSO VALORE", (540, 985), ts, tn, size=56, accent=True))
        sc.add(Img(banknote(680, serial="N. 048217", hl=True), (540, 810), tn + 0.1, anim="pop", rot=-4))
        sc.add(Img(banknote(680, serial="N. 048217", hl=True), (540, 1160), tn + 0.1, anim="pop", rot=3))
        sc.add(Stamp("STESSO NUMERO", (540, 985), tn + 0.4, size=80, rot=-8))
        sc.footer = "Fonti: Wikipedia · moruzzi.it · IMF WP 17/274 · banconote ricostruite"
    elif i == 1:
        tg = T("Gli") - 0.3; tb = T("un") - 0.3; te = T("e") - 0.3
        sc.add(Calendar((540, 760), 300, [(a, "ROMA", "1889")], a, tg + 0.3), "paper")
        sc.add(Bank(BB, tg, None, level=[(tg, 0.8), (tg + 0.8, 1.4)], hole_t=tb, insp=[(tg, "suit"), (tg + 0.2, "expert")], label=""))
        sc.add(Pill("OLTRE IL LIMITE DI LEGGE", (540, 500), tg + 0.5, tb, size=52, accent=True))
        sc.add(Pill("UN BUCO IN CASSA", (540, 500), tb, te, size=56, accent=True))
        sc.add(Icon("serial", (540, 440), te, size=300), "pop")
        sc.add(Pill("NUMERI DI SERIE DOPPI", (540, 620), te + 0.2, size=56, accent=True))
        sc.footer = "Fonti: Filodiritto · Skuola.net · IMF WP 17/274 · schema non in scala"
    elif i == 2:
        tp = T("Per") - 0.3
        sc.add(Icon("report", (540, 760), a, tp + 0.4, size=420), "pop")
        sc.add(Icon("drawer", (540, 820), tp, size=520), "paper")
        sc.add(Text("Tre anni\nnel *cassetto*", (540, 330), a + 0.3, size=100, anchor="ma", align="m"))
        sc.add(Calendar((860, 1180), 180, [(tp, "ANNO", "1890"), (tp + 0.5, "ANNO", "1891"), (tp + 1.0, "ANNO", "1892")], tp), "paper")
        sc.footer = "Fonti: Wikipedia · moruzzi.it · Skuola.net"
    elif i == 3:
        ts = T("Scoppia") - 0.3
        sc.add(Calendar((860, 470), 180, [(a, "DICEMBRE", "1892")], a, ts), "paper")
        sc.add(Hemicycle((40, 640, 1040, 1300), a + 0.2, None, speak_t=T("Napoleone") - 0.2, stir_t=ts, label=""))
        sc.add(Pill("NAPOLEONE COLAJANNI", (420, 470), T("Napoleone") - 0.2, ts, size=52, accent=True))
        sc.add(Text("Lo *scandalo*\nesplode", (540, 330), ts + 0.3, size=100, anchor="ma", align="m"))
        sc.footer = "Fonti: Wikipedia · Skuola.net · IMF WP 17/274 · schema, sagome"
    elif i == 4:
        tm = T("Ma") - 0.3
        sc.add(Figure([(0, 380, FY)], a, tm, kind="suit", s=1.2, label="B. TANLONGO"), "pop")
        sc.add(Figure([(0, 720, FY)], a + 0.3, tm, kind="police", s=1.2, flip=-1), "pop")
        sc.add(Icon("handcuffs", (550, 1000), T("arrestato") - 0.2, tm, size=220), "hit")
        sc.add(Pill("ARRESTATO · 1893", (540, 480), T("arrestato") - 0.1, tm, size=56, accent=True))
        sc.add(Aula((40, 640, 1040, 1300), tm, None, judges_t=tm, cage_t=tm, who=True, label="", motto=False))
        sc.add(Stamp("TUTTI ASSOLTI", (540, 900), T("assolve") - 0.1, color=(40, 150, 70), size=100, rot=-8))
        sc.add(Pill("1894", (540, 480), tm + 0.2, size=60, accent=True))
        sc.footer = "Fonti: Wikipedia · IMF WP 17/274 · Filodiritto · moruzzi.it"
    elif i == 5:
        sc.add(Icon("newbank", (540, 880), a + 0.4, size=560, label="BANCA D'ITALIA · 1893"), "hit")
        sc.add(Flash(a + 0.4))
        sc.add(Text("Dallo scandalo,\nuna *nuova banca*", (540, 330), a, size=90, anchor="ma", align="m"))
        sc.footer = "Fonti: Banca d'Italia · IMF WP 17/274 · Wikipedia"
    elif i == 6:
        sc.add(Text("Quella sentenza\nti *convince?*", (540, 330), a, size=100, anchor="ma", align="m"))
        sc.add(Img(banknote(560, serial="N. 048217", hl=True), (540, 820), a + 0.2, anim="drop", rot=-3), "paper")
        sc.add(Text("Storia completa su YouTube", (540, 1185), T("storia"), size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(90), (540, 1345), T("Fascicolo"), anim="pop", shadow=False), "hit")
        sc.footer = "Ricostruzione a scopo divulgativo"
    return sc
