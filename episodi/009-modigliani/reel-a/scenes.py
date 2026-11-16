import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from mod import *
W, H = 1080, 1920
FY = 1300
CB = (20, 560, 1060, 1340)
GB = (40, 560, 1040, 1340)
HEADS = [(2, STONE), (5, STONE), (3, GRANITE)]

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
        ti = T("I") - 0.3; tu = T("Una") - 0.3; tc = T("con") - 0.3
        sc.add(Text("3 teste di pietra\nin un *canale*", (540, 330), a, ti, size=80, anchor="ma", align="m"))
        sc.add(Canal(CB, a + 0.1, ti, digs=[a + 0.1], finds=[(a + 0.4, 2, STONE), (a + 1.0, 5, STONE), (a + 1.6, 3, GRANITE)], crowd=a, label=""))
        sc.add(Icon("critic", (540, 800), ti, tu, size=480), "stamp")
        sc.add(Pill("\"SONO DI MODIGLIANI\"", (540, 470), ti + 0.2, tu, size=56, accent=True))
        sc.add(Img(stone_head(360, 494, 5, STONE, mud=0.3), (540, 900), tu, anim="drop"))
        sc.add(Text("Una l'avevano fatta\n*tre studenti*", (540, 330), tu, size=76, anchor="ma", align="m"))
        sc.add(Icon("drill", (800, 1160), tc, size=340), "hit")
        sc.footer = "Fonti: Il Fatto Quotidiano · Geopop · Artribune · teste stilizzate"
    elif i == 1:
        tc = T("La") - 0.6; tu = T("La") + 0.6
        sc.add(MapEl((40, 420, 1040, 1320), [(a, (10.8, 43.2), 200), (tc, (10.31, 43.55), 900)], a, tc + 0.3,
                     pins=[dict(at="Livorno", label="LIVORNO", t=a + 0.2, side="r", color=RED)], title="mappa: Natural Earth"))
        sc.add(Calendar((880, 560), 180, [(a, "ESTATE", "1984")], a, tu), "paper")
        sc.add(Icon("book", (540, 860), tc + 0.2, tu, size=480, label="LA LEGGENDA"), "pop")
        sc.add(Pill("LA LEGGENDA DEL 1909", (540, 480), tu, size=52, accent=True))
        sc.add(Canal(CB, tu + 0.3, None, drop=[(T("gettò") - 0.2, 2), (T("gettò") + 0.6, 5)], ruspa=False, label="leggenda · non verificata"))
        sc.add(Pill("FOSSO REALE", (540, 1280), T("Fosso") - 0.2, size=52))
        sc.footer = "Fonti: Il Fatto Quotidiano · Artribune · The Local"
    elif i == 2:
        td = a + 1.0; t24 = T("24") - 0.3; tp = T("Poi") - 0.3; tp2 = tp + 0.8
        sc.add(Canal(CB, a, None, digs=[a + 0.2, a + 2.4], finds=[(T("dal") - 0.2, 2, STONE), (tp + 0.1, 5, STONE), (tp2 + 0.1, 3, GRANITE)], crowd=a + 0.5, label=""))
        sc.add(Pill("ARRIVA LA RUSPA", (540, 480), a + 0.1, td, size=52, accent=True))
        sc.add(ClockFace((880, 420), 110, td, t24, start=8.0, speed=3.0, label="UNA SETTIMANA"))
        sc.add(Calendar((860, 450), 160, [(t24, "LUGLIO 1984", "24")], t24, tp + 0.6), "paper")
        sc.add(Pill("UNA · DUE · TRE TESTE", (540, 470), tp2, size=56, accent=True))
        sc.footer = "Fonti: Il Fatto Quotidiano · Geopop · Libreriamo · schema non in scala"
    elif i == 3:
        tg = T("Giulio") + 0.6
        sc.add(Gallery((40, 820, 1040, 1390), a, None, heads=[(a + 0.2 * k, s_, tn) for k, (s_, tn) in enumerate(HEADS)], label="", labels=["?", "?", "?"]))
        sc.add(Pill("ESPOSTE AL MUSEO", (540, 400), a + 0.1, tg, size=56, accent=True))
        sc.add(Img(person_card("G. C. ARGAN", "critico d'arte", 300), (540, 590), tg, anim="drop", rot=-3), "paper")
        sc.add(Stamp("AUTENTICHE", (540, 770), T("autentiche") - 0.2, color=(40, 120, 60), size=80, rot=-8))
        sc.footer = "Fonti: Il Fatto Quotidiano · Artribune · modigliani1909.com"
    elif i == 4:
        tl_ = T("la") - 0.3; tc = T("con") - 0.3; te = T("E") - 0.3
        sc.add(Icon("magazine", (540, 780), a, tl_, size=560, label="PANORAMA"), "paper")
        for k in range(3): sc.add(Figure([(0, 240 + k * 300, FY)], tl_ + 0.15 * k, tc, kind="man", s=0.9), "pop" if k == 0 else None)
        sc.add(Bubble((540, 640), 190, tl_, tc, inner="head", text="FATTA DA NOI"), "pop")
        sc.add(Icon("drill", (540, 800), T("trapano") - 0.2, te, size=420), "hit")
        sc.add(Icon("tvlive", (540, 840), te, size=600), "pop")
        sc.add(Pill("IN DIRETTA TV", (540, 480), T("diretta") - 0.2, size=56, accent=True))
        sc.footer = "Fonti: Geopop · Il Fatto Quotidiano · Artribune · attrezzi generici"
    elif i == 5:
        tl_ = T("Le", 1) - 0.3; tu = T("un") - 0.3
        sc.add(Gallery(GB, a, tl_ + 1.0, heads=[(a, s_, tn) for s_, tn in HEADS], fakes=[(a + 0.1, 1)], label="", labels=["?", "STUDENTI", "?"]))
        sc.add(Img(person_card("ANGELO FROGLIA", "portuale e artista", 320), (540, 860), tl_ + 1.0, anim="drop", rot=-3), "paper")
        sc.add(Icon("head", (230, 1200), tl_ + 1.4, tu, size=220), "pop")
        sc.add(Icon("head_g", (850, 1200), tl_ + 1.6, tu, size=220), "pop")
        sc.add(Icon("tv", (260, 820), tu + 0.2, size=240, label="MEDIA"), "pop")
        sc.add(Icon("critic", (820, 820), tu + 0.6, size=240, label="ESPERTI"), "pop")
        sc.add(Pill("UN ESPERIMENTO", (540, 480), tu, size=56, accent=True))
        sc.footer = "Fonti: Artribune · Geopop · modigliani1909.com · sagoma, nessuna foto"
    elif i == 6:
        sc.add(Text("Ci avresti\n*creduto?*", (540, 330), a, size=110, anchor="ma", align="m"))
        sc.add(Gallery((90, 640, 990, 1150), a + 0.2, None, heads=[(a + 0.2, s_, tn) for s_, tn in HEADS], fakes=[(a + 0.6 + 0.2 * k, k) for k in range(3)], label="", labels=["", "", ""]))
        sc.add(Text("Storia completa su YouTube", (540, 1185), T("storia"), size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(90), (540, 1345), T("Fascicolo"), anim="pop", shadow=False), "hit")
        sc.footer = "Ricostruzione a scopo divulgativo"
    return sc
