import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from euf import *
import fx
W, H = 1080, 1920
FY = 1300
BB = (40, 640, 1040, 1320)
MT = "mappa: Natural Earth · percorsi indicativi · schema non in scala"

def build(i, dur, a, words):
    def T(p, n=0):
        cs = lambda s: re.sub(r"[^\w']", "", s.lower())
        hits = [w for w in words if cs(w[0]) == cs(p)] or [w for w in words if cs(w[0]).startswith(cs(p))]
        return a + hits[min(n, len(hits) - 1)][1] if hits else a + 0.5
    sc = Scene(dur)
    if i == 0:
        tv = T("vaso") - 0.3; ts = T("star") - 0.3; tn = T("New") - 0.3
        sc.add(Text("Oltre\n*30 anni*", (540, 300), a, tv, size=120, anchor="ma", align="m"))
        sc.add(Icon("hourglass", (540, 920), a, tv, size=480), "pop")
        sc.add(Text("Un vaso\n*scavato di nascosto*", (540, 300), tv, ts, size=96, anchor="ma", align="m"))
        sc.add(Icon("krater_dirty", (540, 920), tv, ts, size=560), "pop")
        sc.add(Text("La *star*\ndi un museo", (540, 300), ts, size=104, anchor="ma", align="m"))
        sc.add(Icon("temple", (540, 900), ts, tn, size=520), "pop")
        sc.add(Icon("krater", (540, 1000), ts + 0.3, size=300), "pop")
        sc.add(Icon("skyline", (540, 900), tn, size=560), "pop")
        sc.add(Pill("NEW YORK", (540, 1290), tn + 0.2, size=56, accent=True))
        sc.footer = "Fonti: Wikipedia · Trafficking Culture · Smarthistory · Ministero della Cultura"
    elif i == 1:
        td = T("dipinto") - 0.3; tn = T("1971") - 0.3; tc = T("Cerveteri") - 0.3
        sc.add(Text("Il cratere\ndi *Eufronio*", (540, 300), a, td, size=110, anchor="ma", align="m"))
        sc.add(Icon("krater", (540, 920), a, tn, size=600), "pop")
        sc.add(Pill("ATENE · CIRCA 515 a.C.", (540, 1320), td, tn, size=52, accent=True))
        sc.add(Text("*1971*\ni tombaroli", (540, 300), tn, size=110, anchor="ma", align="m"))
        sc.add(Icon("tomb", (540, 900), tn, tc, size=520), "pop")
        sc.add(Icon("spade", (860, 1150), tn + 0.4, tc, size=260), "pop")
        sc.add(Icon("moon", (220, 700), tn + 0.2, tc, size=180), "pop")
        sc.add(WorldMap(BB, [(tc, "Cerveteri", 600), (a + dur, "Cerveteri", 900)], tc,
                        pins=[dict(at="Cerveteri", label="CERVETERI", t=tc + 0.2, side="r", color=RED), dict(at="Roma", label="ROMA", t=tc + 0.5, side="r", color=GOLD)], title=MT))
        sc.footer = "Fonti: Wikipedia · Trafficking Culture · Smarthistory · FutureLearn · Ministero della Cultura"
    elif i == 2:
        te = T("E") - 0.3; tu = T("milione") - 0.3; tr = T("record") - 0.4
        sc.add(Text("In *Svizzera*", (540, 300), a, te, size=120, anchor="ma", align="m"))
        sc.add(WorldMap(BB, [(a, (8.0, 44.5), 180), (te, (8.0, 44.5), 200)], a, te,
                        pins=[dict(at="Cerveteri", label="CERVETERI", t=a + 0.2, side="r", color=RED), dict(at="Zurigo", label="ZURIGO", t=a + 0.8, side="r", color=GOLD)],
                        routes=[dict(pts=["Cerveteri", "Zurigo"], t=a + 0.5, d=1.0, icon="truck", color=RED)], title=MT))
        sc.add(Text("*1972*\nil Metropolitan", (540, 300), te, tu, size=104, anchor="ma", align="m"))
        sc.add(Icon("temple", (540, 900), te, tu, size=500), "pop")
        sc.add(Big("$ 1.000.000", (540, 820), tu, tr, size=150, color=GOLD, sub="dollari · 1972"))
        sc.add(Icon("dollar_bag", (540, 1180), tu + 0.3, tr, size=260), "pop")
        sc.add(Text("Prezzo\n*record*", (540, 300), tr, size=120, anchor="ma", align="m"))
        sc.add(Icon("trophy", (540, 920), tr, size=480), "pop")
        sc.footer = "Fonti: Trafficking Culture · FutureLearn · Smarthistory · Wikipedia (per una fonte 1,2 mln)"
    elif i == 3:
        tg = T("porto") - 0.3; tm = T("Migliaia") - 0.3; tt = T("terra") - 0.6
        sc.add(Text("*1995*\ni carabinieri", (540, 300), a, tg, size=110, anchor="ma", align="m"))
        sc.add(Figure([(a, -100, FY), (a + 1.6, 380, FY)], a, tg, kind="police", s=1.3), "pop")
        sc.add(Figure([(a + 0.3, -100, FY), (a + 1.9, 640, FY)], a + 0.3, tg, kind="police", s=1.3), "pop")
        sc.add(Icon("lock", (540, 850), a + 0.5, tg, size=300), "pop")
        sc.add(Text("Porto franco\ndi *Ginevra*", (540, 300), tg, tm, size=104, anchor="ma", align="m"))
        sc.add(Icon("warehouse", (540, 920), tg, tm, size=560), "pop")
        sc.add(Text("Migliaia\ndi *Polaroid*", (540, 300), tm, tt, size=110, anchor="ma", align="m"))
        sc.add(Polaroids((40, 640, 1040, 1320), tm, tt, n=18))
        sc.add(Text("Appena usciti\ndalla *terra*", (540, 300), tt, size=104, anchor="ma", align="m"))
        sc.add(Icon("polaroid", (540, 940), tt, size=560), "pop")
        sc.footer = "Fonti: Trafficking Culture · Swissinfo · Lithub · NPR (The Medici Conspiracy) · Archaeology"
    elif i == 4:
        te = T("E") - 0.3; tc = T("condannato") - 0.3
        sc.add(Text("*2008*\ntorna in Italia", (540, 300), a, te, size=110, anchor="ma", align="m"))
        sc.add(WorldMap(BB, [(a, (-32.0, 42.0), 9), (te, (-32.0, 42.0), 10)], a, te,
                        pins=[dict(at="New York", label="NEW YORK", t=a + 0.2, side="r", color=GOLD), dict(at="Roma", label="ROMA", t=a + 1.0, side="r", color=RED)],
                        routes=[dict(pts=["New York", "Roma"], t=a + 0.4, d=1.2, icon="plane", color=RED)], title=MT))
        sc.add(Text("Il mercante\n*Giacomo Medici*", (540, 300), te, tc, size=100, anchor="ma", align="m"))
        sc.add(Icon("nophoto", (540, 920), te, tc, size=440), "pop")
        sc.add(Text("Condanna\n*definitiva*", (540, 300), tc, size=110, anchor="ma", align="m"))
        sc.add(Img(label_card(["Corte di Cassazione · 2011", "ricorso respinto", "condanna definitiva"], 900, title="GIACOMO MEDICI"), (540, 900), tc, anim="drop", rot=-2), "paper")
        sc.add(Icon("gavel", (860, 1250), tc + 0.4, size=220), "pop")
        sc.footer = "Fonti: Trafficking Culture · UNODC SHERLOC (Cass. 2011) · Swissinfo · Wikipedia · FutureLearn"
    elif i == 5:
        ts = T("storia") - 0.2
        sc.add(Text("Oggi a\n*Cerveteri*", (540, 300), a, ts, size=120, anchor="ma", align="m"))
        sc.add(Icon("krater", (540, 900), a + 0.2, ts, size=480), "pop")
        sc.add(Icon("tomb", (860, 1240), a + 0.8, ts, size=220), "pop")
        sc.add(Text("Storia completa su YouTube", (540, 1185), ts, size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(90), (540, 1345), T("Fascicolo"), anim="pop", shadow=False), "hit")
        sc.footer = "Fonti: Ministero della Cultura (2015) · Wikipedia · Smarthistory"
    return sc
