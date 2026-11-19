import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from wm import *
W, H = 1080, 1920
FY = 1300
BB = (40, 640, 1040, 1300)
MT = "mappa: Natural Earth · schema non in scala"
WHO = (300, 1270)

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
        tp = T("Poi") - 0.3; tm = T("malocchio") - 0.3; tq = T("quattro") - 0.3
        sc.add(Text("Il sale del\n*malocchio*", (540, 330), a, size=110, anchor="ma", align="m"))
        sc.add(Icon("salt", (540, 960), a, tp + 0.2, size=480), "hit")
        sc.add(Pill("SALE DA CUCINA", (540, 1290), a + 0.4, tp, size=56))
        sc.add(Salotto(BB, tp, tm + 0.2, ring=(tp, tm)), "whoosh")
        sc.add(Figure([(tp, *WHO)], tp, tm + 0.2, kind="expert", s=0.45))
        sc.add(Icon("glass_salt", (800, 880), T("sciolto") - 0.3, tm + 0.2, size=220), "pop")
        sc.add(Icon("eye", (540, 940), tm, tq, size=600), "hit")
        sc.add(Icon("lire", (540, 940), tq, size=520), "hit")
        sc.add(Pill("4 MILIONI DI LIRE", (540, 1290), tq + 0.3, size=64, accent=True))
        sc.footer = "Fonti: Il Post · il Giornale (2005) · Fanpage · ricostruzione"
    elif i == 1:
        tw = T("Wanna") - 0.3; ts = T("Stefania") - 0.3; tm = T("sedicente") - 0.3
        sc.add(Text("La regina delle\n*televendite*", (540, 330), a, tm, size=96, anchor="ma", align="m"))
        sc.add(Tele(BB, a, tw + 0.2, items=[(a + 0.3, "jar"), (a + 0.6, "algae"), (a + 0.9, "salt")], calls=(a, tw), sign="TELEVENDITE"), "whoosh")
        sc.add(Board({"w": dict(xy=(320, 1020), name="WANNA MARCHI", role="televenditrice", t=tw, rot=-3),
                      "s": dict(xy=(760, 1020), name="STEFANIA NOBILE", role="la figlia", t=ts, rot=3)},
                     [("w", "s", ts + 0.4)], tw, tm + 0.2, cw=330))
        sc.add(Text("silhouette · nessuna foto reale", (540, 1330), tw + 0.3, tm, size=26, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Text("e un «maestro\n*di vita*»", (540, 330), tm, size=96, anchor="ma", align="m"))
        sc.add(Tele(BB, tm, None, mood="luck", sign="", items=[(tm + 0.3, "lotto"), (tm + 0.5, "amulet"), (tm + 0.7, "ivy")]), "whoosh")
        sc.add(Figure([(tm, 860, 1230)], tm, None, kind="mage", s=0.45), "pop")
        sc.add(Pill("SEDICENTE · BRASILIANO", (540, 590), tm + 0.4, size=50, accent=True))
        sc.footer = "Fonti: Il Post · Fanpage · QuiFinanza · schema"
    elif i == 2:
        tav = T("avvisa") - 0.3; tf = T("Finge") - 0.3; tc = T("telecamere") - 0.3
        sc.add(Text("La *trappola*", (540, 330), a, size=110, anchor="ma", align="m"))
        sc.add(Salotto(BB, a, None, cams=[(tc, (.46, .22)), (tc + 0.4, (.15, .30)), (tc + 0.8, (.62, .56))]))
        sc.add(Calendar((700, 830), 150, [(a, "ANNO", "2001")], a, tav), "paper")
        sc.add(Figure([(a, *WHO)], a, None, kind="expert", s=0.45, label="TELESPETTATRICE"), "pop")
        sc.add(Icon("studio_tv", (780, 880), tav, tf, size=300), "pop")
        sc.add(Pill("STRISCIA LA NOTIZIA", (540, 570), T("Striscia") - 0.2, tf, size=56, accent=True))
        sc.add(Pill("FINGE DI STARE AL GIOCO", (540, 570), tf, tc, size=56, accent=True))
        sc.add(Pill("TELECAMERE NASCOSTE", (540, 570), tc, size=56, accent=True))
        sc.footer = "Fonti: il Giornale (2005) · Il Post · QuiFinanza · schema"
    elif i == 3:
        ti = T("Il", 1) - 0.3; tm = T("maestro") - 0.3
        sc.add(Icon("studio_tv", (540, 900), a, ti, size=520), "hit")
        sc.add(Text("Il servizio\nva *in onda*", (540, 330), a, ti, size=100, anchor="ma", align="m"))
        sc.add(Calendar((540, 660), 220, [(ti, "GENNAIO 2002", "24")], ti, tm), "paper")
        sc.add(Text("*Arrestate*", (540, 300), ti, tm, size=110, anchor="ma", align="m"))
        sc.add(Icon("gdf", (300, 1000), ti + 0.4, tm, size=320, label="GUARDIA DI FINANZA"), "pop")
        sc.add(Icon("handcuffs", (780, 1000), T("arresta") - 0.2, tm, size=320), "hit")
        sc.add(Pill("MADRE E FIGLIA", (540, 1300), T("madre") - 0.2, tm, size=56, accent=True))
        sc.add(Text("Il «maestro»\nè in *Brasile*", (540, 300), tm, size=100, anchor="ma", align="m"))
        sc.add(WorldMap(BB, [(tm, (-20, 15), 6.0)], tm, None,
                        pins=[dict(at="Milano", label="ITALIA", t=tm + 0.2, side="r", color=GOLD),
                              dict(at="Brasile", label="BRASILE", t=tm + 1.0, side="r", color=RED)],
                        routes=[dict(pts=["Milano", "Brasile"], t=tm + 0.2, d=1.0, icon="person", color=RED)], title=MT))
        sc.footer = "Fonti: Il Post · Fanpage · QuiFinanza · Natural Earth"
    elif i == 4:
        tn = T("nove") - 0.3; tn2 = T("nove", 1) - 0.3
        sc.add(Text("Condanne\n*definitive*", (540, 300), a, size=110, anchor="ma", align="m"))
        sc.add(Calendar((300, 720), 200, [(a, "MARZO", "2009")], a, None), "paper")
        sc.add(Icon("court", (760, 700), a + 0.3, size=220, label="CASSAZIONE"), "pop")
        sc.add(Img(sentence_card(["Wanna Marchi", "9 anni e 6 mesi"], w=560, title="DEFINITIVA", seed=43), (540, 1000), tn, anim="drop", rot=-2), "paper")
        sc.add(Img(sentence_card(["Stefania Nobile", "9 anni e 4 mesi"], w=560, title="DEFINITIVA", seed=44), (540, 1250), tn2, anim="drop", rot=2), "paper")
        sc.footer = "Fonti: VareseNews · Blitz quotidiano · Il Post · ricostruzione grafica"
    elif i == 5:
        sc.add(Text("Come si cade\nin una trappola\n*così?*", (540, 300), a, size=96, anchor="ma", align="m"))
        sc.add(Tele((90, 700, 990, 1110), a + 0.2, None, mood="luck", sign="", items=[(a + 0.3, "salt"), (a + 0.5, "ivy"), (a + 0.7, "eye")]))
        sc.add(Text("Storia completa su YouTube", (540, 1185), T("storia"), size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(90), (540, 1345), T("Fascicolo"), anim="pop", shadow=False), "hit")
        sc.footer = "Ricostruzione a scopo divulgativo · voce generata con sintesi vocale"
    return sc
