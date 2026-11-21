import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from met import *
import fx
W, H = 1080, 1920
FY = 1300
BB = (40, 640, 1040, 1320)
MT = "mappa: Natural Earth · schema non in scala"

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
        tb = T("bicchiere") - 0.3; to = T("ospedale") - 0.3; tv = T("23") - 0.3
        sc.add(Text("Italia\n*1986*", (540, 300), a, tb, size=120, anchor="ma", align="m"))
        sc.add(Icon("bottle", (540, 920), a, tb, size=560), "pop")
        sc.add(Text("Vino *da tavola*", (540, 330), tb, to, size=100, anchor="ma", align="m"))
        sc.add(Icon("wglass", (540, 920), tb, to, size=520), "pop")
        sc.add(Text("Decine\nin *ospedale*", (540, 300), to, tv, size=104, anchor="ma", align="m"))
        sc.add(Icon("hospital2", (540, 900), to, tv, size=480), "pop")
        sc.add(Crowd((120, 1080, 960, 1300), 10, to + 0.3, tv, s=0.5, seed=4))
        sc.add(Big("23", (540, 820), tv, size=420, color=RED, sub="vittime"))
        sc.footer = "Fonti: Wikipedia · Linkiesta · GreenMe · La Nazione · Il Giorno"
    elif i == 1:
        tu = T("un") - 0.3; to = T("oltre") - 0.2; ta = T("In") - 0.3
        sc.add(Text("Dentro:\n*metanolo*", (540, 300), a, tu, size=110, anchor="ma", align="m"))
        sc.add(Icon("flask", (540, 920), a, ta, size=520), "pop")
        sc.add(Text("Esiste anche\n*in natura*", (540, 300), tu, to, size=100, anchor="ma", align="m"))
        sc.add(Icon("grapes", (300, 1300), tu + 0.2, ta, size=220), "pop")
        sc.add(Text("Oltre i limiti\nè *tossico*", (540, 300), to, ta, size=100, anchor="ma", align="m"))
        sc.add(Icon("warn", (800, 1300), to + 0.2, ta, size=220), "pop")
        sc.add(Text("*Molte volte*\noltre il limite", (540, 300), ta, size=100, anchor="ma", align="m"))
        sc.add(Gauge((60, 700, 1020, 1200), [(ta + 0.3, 0.2), (ta + 1.2, 5.0)], ta, vmax=6.0, title="METANOLO · schema semplificato",
                     labels={0.3: "", 5.0: "in alcuni campioni"}))
        sc.footer = "Fonti: TIME (1986) · Il Giorno · Wikipedia · GreenMe · ACU"
    elif i == 2:
        tm = T("metanolo") - 0.3; te = T("E") - 0.3; tz = T("costava") - 0.3
        sc.add(Text("*Perché?*", (540, 330), a, tm, size=150, anchor="ma", align="m"))
        sc.add(Icon("magnifier", (540, 900), a, tm, size=460), "pop")
        sc.add(Text("Più *gradi*\nvino più caro", (540, 300), tm, te, size=100, anchor="ma", align="m"))
        sc.add(Icon("bottle", (540, 920), tm, te, size=500), "pop")
        sc.add(Text("Dal *1984*\nniente imposta", (540, 300), te, tz, size=100, anchor="ma", align="m"))
        sc.add(Icon("notax", (540, 920), te, tz, size=500), "pop")
        sc.add(Text("Costava meno\ndello *zucchero*", (540, 300), tz, size=100, anchor="ma", align="m"))
        sc.add(Icon("flask", (320, 920), tz, size=360), "pop")
        sc.add(Icon("sugar", (760, 920), tz + 0.3, size=360), "pop")
        sc.add(Text("<", (540, 920), tz + 0.5, size=200, anchor="mm"))
        sc.footer = "Fonti: Wikipedia · Linkiesta · Dissapore · GreenMe · La Nazione"
    elif i == 3:
        tf = T("fino") - 0.3
        sc.add(Text("La procura\ndi *Milano*", (540, 300), a, tf, size=110, anchor="ma", align="m"))
        sc.add(Filiera((30, 760, 1050, 1160), a + 0.2, tf, upto=5, bad=0, flow_t=a + 1.0, title="LA FILIERA · schema semplificato"))
        sc.add(Text("Narzole\n(Cuneo)", (540, 300), tf, size=110, anchor="ma", align="m"))
        sc.add(WorldMap(BB, [(tf, "Milano", 300), (dur + a, "Narzole", 520)], tf,
                        pins=[dict(at="Milano", label="MILANO", t=tf + 0.2, side="r", color=GOLD),
                              dict(at="Narzole", label="NARZOLE", t=tf + 0.6, side="r", color=RED)],
                        routes=[dict(pts=["Milano", "Narzole"], t=tf + 0.4, d=1.2, icon="magnifier", color=RED)], title=MT))
        sc.footer = "Fonti: Wikipedia · Linkiesta · TIME (1986) · ACU · GreenMe"
    elif i == 4:
        tn = T("Nel") - 0.3; tq = T("14") - 0.4
        sc.add(Text("Export\nin *crollo*", (540, 300), a, tn, size=110, anchor="ma", align="m"))
        sc.add(Icon("ship", (540, 820), a, tn, size=380), "pop")
        sc.add(Icon("certificate", (540, 1200), a + 1.0, tn, size=280, label="NUOVI CONTROLLI"), "pop")
        sc.add(Calendar((540, 820), 360, [(tn, "MILANO", "1992")], tn, tq), "paper")
        sc.add(Text("Primo *grado*", (540, 300), tn, size=110, anchor="ma", align="m"))
        sc.add(Img(sentence18(["Giovanni Ciravegna: 14 anni", "Daniele Ciravegna: 4 anni", "Corte d'assise di Milano"], w=900), (540, 900), tq, anim="drop", rot=-2), "paper")
        sc.add(Icon("gavel", (860, 1250), tq + 0.4, size=220), "pop")
        sc.footer = "Fonti: Wikipedia · Linkiesta · ACU · GreenMe · Il Sole 24 Ore"
    elif i == 5:
        ts = T("storia") - 0.2
        sc.add(Text("Nessun\n*risarcimento*", (540, 320), a, ts, size=110, anchor="ma", align="m"))
        sc.add(Icon("box_empty", (540, 900), a + 0.2, ts, size=440), "pop")
        sc.add(Stamp("MAI PAGATO", (540, 1000), a + 0.6, ts, size=110, rot=-8))
        sc.add(Text("Storia completa su YouTube", (540, 1185), ts, size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(90), (540, 1345), T("Fascicolo"), anim="pop", shadow=False), "hit")
        sc.footer = "Fonti: Il Giorno · Linkiesta · GreenMe · Dissapore"
    return sc
