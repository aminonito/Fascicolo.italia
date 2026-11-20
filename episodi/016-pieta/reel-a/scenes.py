import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from pt import *
W, H = 1080, 1920
CR = (40, 560, 1040, 1260)
WT = "mappa: Natural Earth · percorso indicativo"
SAG = "sagoma stilizzata, non l'opera"

def build(i, dur, a, words):
    T0 = Clock(words, a)
    def T(p, n=0):
        cs = lambda s: re.sub(r"[^\w']", "", s.lower())
        hits = [w for w in words if cs(w[0]) == cs(p)]
        if hits: return a + hits[min(n, len(hits) - 1)][1]
        try: return T0(p, n)
        except KeyError: return a + 0.5
    sc = Scene(dur)
    if i == 0:
        ts = T("sulla") - 0.2
        hits = [a + 0.4 + k * 0.3 for k in range(8)]
        sc.add(Text("circa *15*\ncolpi di martello", (540, 380), a, ts, size=110, anchor="ma", align="m"))
        sc.add(Pieta((540, 1250), 620, a, None, hits=hits, label=None))
        sc.add(Swing((720, 760), 180, a, None, hits=hits))
        sc.add(Text("sulla statua più famosa\ndi *Michelangelo*", (540, 380), ts, size=80, anchor="ma", align="m"))
        sc.add(Pill("LA PIETÀ · ROMA 1972", (540, 1320), ts + 0.3, size=54, accent=True))
        sc.footer = "Fonti: Il Post · Finestre sull'Arte · Wikipedia (circa 15 colpi; per altre fonti 12) · " + SAG
    elif i == 1:
        ti = T("In") - 0.3; te = T("e") - 0.2
        hits = [te + 0.6 + k * 0.35 for k in range(5)]
        sc.add(Calendar((540, 520), 240, [(a, "MAGGIO 1972", "21")], a, ti), "paper")
        sc.add(Icon("basilica", (540, 960), a + 0.3, ti, size=420), "pop")
        sc.add(Pill("ROMA · SAN PIETRO", (540, 1320), a + 0.4, ti, size=54, accent=True))
        sc.add(Cappella(CR, ti, None, pk=dict(hits=hits), label=""), "whoosh")
        sc.add(Figure([(ti + 0.2, 140, 1200), (te, 420, 1130)], ti + 0.2, None, kind="man", s=0.45, arms=[(te, "up")]))
        sc.add(Swing((490, 820), 120, te, None, hits=hits))
        sc.add(Pill("SCAVALCA LA BALAUSTRA", (540, 440), T("scavalca") - 0.1, te, size=52, accent=True))
        sc.add(Pill("MARTELLO DA GEOLOGO", (540, 440), te, size=52, accent=True))
        sc.add(Icon("geo", (900, 450), te, size=150), "pop")
        sc.footer = "Fonti: Il Post · Finestre sull'Arte · Geopop · " + SAG
    elif i == 2:
        tn = T("Il", 1) - 0.2; ta = T("A") - 0.3
        sc.add(Pieta((540, 1220), 600, a, None, arm_t=a + 0.5, nose_t=tn + 0.2, label=SAG))
        sc.add(Pill("BRACCIO SINISTRO", (540, 440), a + 0.3, tn, size=58, accent=True))
        sc.add(Pill("NASO IN PEZZI", (540, 440), tn, ta - 0.3, size=58, accent=True))
        sc.add(Frags((60, 1080, 1020, 1300), ta, None, n=100, counter=False))
        sc.add(Big("100", (540, 470), ta + 0.2, size=160, color=RED, sub="frammenti circa", subsize=50))
        sc.footer = "Fonti: Wikipedia · Wanted in Rome · Reuters (2013) · Finestre sull'Arte · " + SAG
    elif i == 3:
        tm = T("Mesi") - 0.3; td = T("dagli") - 0.2
        sc.add(Figure([(a, 300, 1150), (tm, 900, 1150)], a, tm, kind="suit", s=0.6, arms=[(a, "hold")]))
        sc.add(Icon("pieces", (540, 700), a + 0.2, tm, size=320), "pop")
        sc.add(Pill("UN FRAMMENTO IN TASCA", (540, 440), a + 0.3, tm, size=56, accent=True))
        sc.add(WorldMap((40, 560, 1040, 1260), [(tm, (-31, 42), 10.5)], tm, None,
                        routes=[dict(pts=["NewYork", "Roma"], t=tm + 0.3, d=1.6, icon="envelope", color=GOLD, bend=-0.2)],
                        pins=[dict(at="NewYork", label="USA", t=tm + 0.2, side="r", color=GOLD),
                              dict(at="Roma", label="ROMA", t=tm + 0.4, side="l")], title=WT))
        sc.add(Pill("RISPEDITO IN FORMA ANONIMA", (540, 440), tm + 0.3, size=52, accent=True))
        sc.footer = "Fonti: Wikipedia · Wanted in Rome · Reuters (2013) · " + WT
    elif i == 4:
        te = T("è") - 0.2
        sc.add(Icon("court", (540, 900), a, size=380), "pop")
        sc.add(Stamp("MAI PROCESSATO", (540, 1180), a + 0.6, size=90, rot=-8))
        sc.add(Img(label_card(["giudicato", "infermo di mente"], 700, title="PERIZIA"), (540, 560), te, anim="drop", rot=2), "paper")
        sc.footer = "Fonti: Il Post · Finestre sull'Arte · Wikipedia · Wanted in Rome"
    elif i == 5:
        td = T("Dieci") - 0.3; tde = T("dietro") - 0.2
        sc.add(Frags((60, 600, 1020, 1300), a, td, n=100, sort_t=a + 0.2, sort_d=1.8, counter=False))
        sc.add(Pill("OGNI PEZZO AL SUO POSTO", (540, 440), a + 0.3, td, size=56, accent=True))
        sc.add(Pieta((540, 1250), 640, td, None, glass_t=tde, label=SAG))
        sc.add(Pill("10 MESI DOPO", (540, 440), td + 0.2, tde, size=58, accent=True))
        sc.add(Pill("VETRO ANTIPROIETTILE", (540, 440), tde, size=58, accent=True))
        sc.footer = "Fonti: Il Post · Wikipedia · Reuters (2013) · Geopop · " + SAG
    elif i == 6:
        tl = T("La") - 0.3
        sc.add(Text("Era giusto\ncancellare\ni *segni*?", (540, 360), a, tl, size=110, anchor="ma", align="m"))
        sc.add(Icon("debate", (540, 1000), a + 0.3, tl, size=380), "pop")
        sc.add(Img(cover_folder(760), (540, 760), tl, anim="drop"), "paper")
        sc.add(Pill("LA STORIA COMPLETA SU YOUTUBE", (540, 1150), tl + 0.3, size=48, accent=True))
        sc.footer = "Fascicolo Italia · le fonti sono nella descrizione del video lungo"
    return sc
