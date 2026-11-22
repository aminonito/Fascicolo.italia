import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from tot import *
import fx
W, H = 1080, 1920
FY = 1300
BB = (40, 640, 1040, 1320)
MT = "mappa: Natural Earth · schema non in scala"

def build(i, dur, a, words):
    def T(p, n=0):
        cs = lambda s: re.sub(r"[^\w']", "", s.lower())
        hits = [w for w in words if cs(w[0]) == cs(p)] or [w for w in words if cs(w[0]).startswith(cs(p))]
        return a + hits[min(n, len(hits) - 1)][1] if hits else a + 0.5
    sc = Scene(dur)
    if i == 0:
        tf = T("fine") - 0.3; te = T("forze") - 0.3; tp = T("portano") - 0.3; tt = T("telecamere") - 0.3
        sc.add(Text("Domenica\n*23 marzo 1980*", (540, 300), a, tf, size=104, anchor="ma", align="m"))
        sc.add(Calendar((540, 900), 420, [(a, "DOMENICA", "23 MARZO")], a, tf), "paper")
        sc.add(Text("Fine\n*partita*", (540, 300), tf, te, size=120, anchor="ma", align="m"))
        sc.add(Icon("stadium", (540, 920), tf, te, size=620), "pop")
        sc.add(Campo((80, 700, 1000, 1260), te, tt, t_pol=te + 0.2, minute=(88, 90), label="SERIE A · 1980"))
        sc.add(Text("Entrano le\n*forze dell'ordine*", (540, 300), te, tp, size=96, anchor="ma", align="m"))
        sc.add(Text("Portano via\ni *calciatori*", (540, 300), tp, tt, size=104, anchor="ma", align="m"))
        sc.add(Text("Davanti alle\n*telecamere*", (540, 300), tt, size=104, anchor="ma", align="m"))
        sc.add(Icon("tvcam", (380, 920), tt, size=420), "pop")
        sc.add(Icon("tv", (760, 1000), tt + 0.4, size=300), "pop")
        sc.footer = "Fonti: Il Post (2012, 2020) · Linkiesta · Gli Eroi del Calcio · TMW · Wikipedia"
    elif i == 1:
        tr = T("ristoratore") - 0.3; tf = T("fornitore") - 0.3; ts = T("scommettono") - 0.3; tg = T("pagano") - 0.3
        sc.add(Text("A *Roma*", (540, 300), a, tr, size=120, anchor="ma", align="m"))
        sc.add(WorldMap(BB, [(a, "Roma", 160), (tr, "Roma", 200)], a, tr,
                        pins=[dict(at="Roma", label="ROMA", t=a + 0.2, side="r", color=RED)], title=MT))
        sc.add(Text("Ristoratore\ne *fornitore*", (540, 300), tr, ts, size=110, anchor="ma", align="m"))
        sc.add(Icon("restaurant", (300, 880), tr, ts, size=380, label="IL RISTORATORE"), "pop")
        sc.add(Icon("fruit", (780, 880), tr + 0.6, ts, size=360, label="IL FORNITORE"), "pop")
        sc.add(Text("Scommesse\n*di nascosto*", (540, 300), ts, tg, size=104, anchor="ma", align="m"))
        sc.add(Icon("slip", (540, 920), ts, tg, size=560), "pop")
        sc.add(Text("Pagano per\n*truccarle*", (540, 300), tg, size=110, anchor="ma", align="m"))
        sc.add(Icon("money", (360, 900), tg, size=340), "pop")
        sc.add(Icon("ball", (740, 920), tg + 0.3, size=300), "pop")
        sc.add(Pill("SECONDO IL LORO RACCONTO", (540, 1290), tg, size=50, accent=True))
        sc.footer = "Fonti: Il Post (2012, 2020) · Panorama · Wikipedia · Linkiesta · TMW"
    elif i == 2:
        td = T("debiti") - 0.3; tn = T("novecentocinquanta") - 0.3; tp = T("primo") - 0.3
        sc.add(Text("I risultati\n*non tornano*", (540, 300), a, td, size=110, anchor="ma", align="m"))
        sc.add(Tabellone((60, 640, 1020, 1300), [("LAZIO", "AVELLINO", "1", "X"), ("BOLOGNA", "AVELLINO", "X", "1")], a, td, title="DUE PARTITE · schema", gap=0.3))
        sc.add(Text("Debiti con gli\n*allibratori*", (540, 300), td, tp, size=104, anchor="ma", align="m"))
        sc.add(Icon("betbook", (540, 860), td, tn, size=500), "pop")
        sc.add(Big("950 milioni", (540, 880), tn, tp, size=150, color=GOLD, sub="di lire · debiti dichiarati"))
        sc.add(Text("*1° marzo 1980*\nla denuncia", (540, 300), tp, size=104, anchor="ma", align="m"))
        sc.add(Img(doc_typed(820, 600, "ESPOSTO · SCHEMA", ["alla Procura di Roma", "1 marzo 1980", "calciatori denunciati", "ricostruzione grafica"], seed=4), (540, 920), tp, anim="drop", rot=-2), "paper")
        sc.footer = "Fonti: Il Post (2012, 2020) · Gli Eroi del Calcio · Wikipedia · Panorama"
    elif i == 3:
        tt = T("tredici") - 0.3; tp = T("presidente") - 0.3; tm = T("dicembre") - 0.5; tf = T("fatto") - 0.3
        sc.add(Text("*13* calciatori\nin manette", (540, 300), a, tp, size=110, anchor="ma", align="m"))
        for j in range(13):
            sc.add(Icon("shirt", (180 + (j % 5) * 180, 760 + (j // 5) * 220), tt + 0.08 * j, tp, size=150), "pop")
        sc.add(Text("Più il presidente\ndel *Milan*", (540, 300), tp, tm, size=100, anchor="ma", align="m"))
        sc.add(Icon("policecar", (540, 920), tp, tm, size=520), "pop")
        sc.add(Text("Dicembre\nil *tribunale*", (540, 300), tm, tf, size=110, anchor="ma", align="m"))
        sc.add(Icon("court", (540, 900), tm, size=460), "pop")
        sc.add(Stamp("ASSOLTI", (540, 1240), tf - 0.4, size=110, rot=-8))
        sc.add(Pill("IL FATTO NON SUSSISTE", (540, 620), tf, size=54, accent=True))
        sc.footer = "Fonti: Il Post (2012, 2020) · Wikipedia · Il Fatto Quotidiano · Linkiesta · Gli Eroi del Calcio"
    elif i == 4:
        tm = T("Milan") - 0.6; tr = T("Paolo") - 0.3; td = T("squalificato") - 0.3
        sc.add(Text("La giustizia\n*sportiva*", (540, 300), a, tm, size=110, anchor="ma", align="m"))
        sc.add(Icon("gavel", (540, 900), a, tm, size=480), "pop")
        sc.add(Text("Milan e Lazio\nin *serie B*", (540, 300), tm, tr, size=104, anchor="ma", align="m"))
        sc.add(Big("SERIE B", (540, 880), tm + 0.2, tr, size=170, color=RED, sub="per la prima volta nella storia del Milan"))
        sc.add(Text("*Paolo Rossi*", (540, 300), tr, size=120, anchor="ma", align="m"))
        sc.add(Icon("nophoto", (540, 860), tr, td, size=420), "pop")
        sc.add(Pill("SI È SEMPRE DETTO INNOCENTE", (540, 1180), tr + 0.6, td, size=48))
        sc.add(Big("2 anni", (540, 860), td, size=190, color=GOLD, sub="di squalifica"))
        sc.add(Icon("hourglass", (540, 1250), td + 0.3, size=200), "pop")
        sc.footer = "Fonti: Il Post (2012, 2016, 2020) · Wikipedia · Gli Eroi del Calcio · Avvenire"
    elif i == 5:
        tp = T("vince") - 0.3; ts = T("storia") - 0.2
        sc.add(Text("Torna in campo\nnel *1982*", (540, 300), a, tp, size=104, anchor="ma", align="m"))
        sc.add(Icon("shirt", (540, 900), a, tp, size=460), "pop")
        sc.add(Icon("ball", (820, 1200), a + 0.4, tp, size=180), "pop")
        sc.add(Text("Campioni\ndel *mondo*", (540, 300), tp, ts, size=120, anchor="ma", align="m"))
        sc.add(Icon("trophy", (540, 900), tp, ts, size=500), "pop")
        sc.add(Pill("SPAGNA · 1982", (540, 1290), tp + 0.3, ts, size=56, accent=True))
        sc.add(Icon("trophy", (540, 860), ts, size=320), "pop")
        sc.add(Text("Storia completa su YouTube", (540, 1185), ts, size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(90), (540, 1345), T("Fascicolo"), anim="pop", shadow=False), "hit")
        sc.footer = "Fonti: Il Post (2012, 2016, 2020) · Avvenire · Wikipedia"
    return sc
