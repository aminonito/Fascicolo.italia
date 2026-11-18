import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from vg import *
W, H = 1080, 1920
FY = 1300
BB = (40, 640, 1040, 1300)
MT = "mappa: Natural Earth · schema non in scala"
GY = 640 + int(660 * .88)
ROOF = 640 + int(660 * .48)

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
        sc.add(Text("Due *Van Gogh*\nrubati", (540, 330), a, te, size=110, anchor="ma", align="m"))
        sc.add(Sala(BB, a, te + 0.4, gone={0: a + 0.8, 1: a + 1.3}, night=True, torch=a, captions=False, label=""))
        sc.add(Pill("IN POCHI MINUTI", (540, 1290), a + 0.6, te, size=56, accent=True))
        sc.add(Text("Ritrovati\nin un'inchiesta\nsulla *camorra*", (540, 330), te, size=92, anchor="ma", align="m"))
        sc.add(Icon("bundle", (540, 960), te + 0.2, size=520), "hit")
        sc.add(Pill("QUASI 14 ANNI DOPO", (540, 1290), T("anni") - 0.2, size=56, accent=True))
        sc.footer = "Fonti: NOS · Il Post · Sky TG24 · sagome stilizzate"
    elif i == 1:
        td = T("Due") - 0.3; ts = T("salgono") - 0.3; tf = T("sfondano") - 0.3; tp = T("e") - 0.3
        sc.add(MapEl(BB, [(a, (5.0, 51.5), 200), (td, "Amsterdam", 500)], a, td + 0.2,
                     pins=[dict(at="Amsterdam", label="AMSTERDAM", t=a + 0.3, side="r", color=RED)], title=""))
        sc.add(Calendar((880, 450), 170, [(a, "DICEMBRE", "2002")], a, td), "paper")
        sc.add(Museo(BB, td, tp + 0.3, ladder_t=T("scala") - 0.2, window_t=tf + 0.4, label=""))
        sc.add(Figure([(td, 120, GY), (ts, 180, GY), (ts + 1.0, 190, ROOF), (tf, 380, ROOF)], td, tp + 0.3, kind="man", s=0.45))
        sc.add(Pill("UNA SCALA", (540, 570), T("scala") - 0.2, ts, size=56, accent=True))
        sc.add(Pill("IL TETTO", (540, 570), ts, tf, size=56, accent=True))
        sc.add(Icon("sledge", (800, 900), tf, tp + 0.3, size=260), "hit")
        sc.add(Text("Museo *Van Gogh*", (540, 380), td, size=90, anchor="ma", align="m"))
        sc.add(Sala(BB, tp, None, gone={0: tp + 0.6, 1: tp + 1.0}, window_t=tp, captions=False, label=""))
        sc.footer = "Fonti: NOS · The Week · Smithsonian · schema non in scala"
    elif i == 2:
        tm = T("Ma") - 0.3; tc = T("con", 1) - 0.3; tn = T("Nel") - 0.3
        sc.add(Museo(BB, a, tm + 0.3, ladder_t=a, window_t=a, rope_t=a + 0.2, label=""))
        sc.add(Figure([(a + 0.4, 960, 900), (tm, 960, GY)], a + 0.3, tm + 0.3, kind="man", s=0.45))
        sc.add(Text("La *fuga*", (540, 330), a, tm, size=110, anchor="ma", align="m"))
        sc.add(Text("Un *berretto*", (540, 330), tm, tn, size=110, anchor="ma", align="m"))
        sc.add(Icon("cap", (540, 900), tm, tn + 0.1, size=440), "hit")
        sc.add(Icon("dna", (820, 1200), tc, tn + 0.1, size=260), "pop")
        sc.add(Icon("gavel", (540, 940), tn + 0.3, size=460), "hit")
        sc.add(Stamp("CONDANNATI\n2004", (540, 1280), tn + 0.4, size=80, rot=-8))
        sc.footer = "Fonti: NOS · Smithsonian · NZ Herald · The Week"
    elif i == 3:
        ta = T("Anni") - 0.3
        sc.add(Text("E i *quadri?*", (540, 330), a, ta, size=110, anchor="ma", align="m"))
        sc.add(Sala(BB, a, ta + 0.3, gone={0: a, 1: a}, captions=False, label=""))
        sc.add(Icon("question", (540, 1400), a + 0.4, ta, size=220), "pop")
        sc.add(Text("Venduti\nin *Italia*", (540, 330), ta, size=110, anchor="ma", align="m"))
        sc.add(MapEl((140, 640, 940, 1300), [(ta, (9.5, 46.6), 56)], ta, None,
                     pins=[dict(at="Amsterdam", label="AMSTERDAM", t=ta + 0.2, side="r", color=GOLD),
                           dict(at="Napoli", label="ITALIA", t=ta + 1.6, side="r", color=RED)],
                     routes=[dict(pts=["Amsterdam", "Milano", "Napoli"], t=ta + 0.3, d=1.4, icon="painting", color=RED)], title=""))
        sc.add(Text("secondo il racconto del ladro (2017)", (540, 590), ta + 0.4, size=32, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: NL Times · Malay Mail · NZ Herald · Natural Earth"
    elif i == 4:
        tl_ = T("La") - 0.3; ta = T("A") - 0.3; ts = T("Sono") - 0.3
        sc.add(Calendar((540, 520), 240, [(a, "2016", "SET")], a, tl_), "paper")
        sc.add(Icon("gdf", (540, 950), tl_, ta, size=440, label="GUARDIA DI FINANZA"), "pop")
        sc.add(Text("Un'inchiesta\nsulla *camorra*", (540, 330), tl_, ta, size=96, anchor="ma", align="m"))
        sc.add(MapEl(BB, [(ta, "Castellammare", 1300)], ta, ts,
                     pins=[dict(at="Castellammare", label="CASTELLAMMARE", t=ta + 0.2, side="l", color=RED)], title=""))
        sc.add(Text("*Castellammare*\ndi Stabia", (540, 330), ta, ts, size=96, anchor="ma", align="m"))
        sc.add(Icon("bundle", (540, 900), T("due", 1) - 0.2, ts + 0.3, size=440), "hit")
        sc.add(Img(framed("sea", 300, frame=False, torn=True), (540, 830), ts, anim="drop"), "paper")
        sc.add(Img(framed("church", 340, frame=False), (540, 1180), ts + 0.3, anim="drop"))
        sc.add(Stamp("SONO LORO", (540, 470), ts + 0.4, size=100, rot=-8))
        sc.footer = "Fonti: Sky TG24 · Smithsonian · Il Post · Natural Earth"
    elif i == 5:
        sc.add(Text("Perché tenere\nnascosti quadri\n*invendibili?*", (540, 300), a, size=86, anchor="ma", align="m"))
        sc.add(Sala((90, 640, 990, 1110), a + 0.2, None, captions=False, label=""))
        sc.add(Text("Storia completa su YouTube", (540, 1185), T("storia"), size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(90), (540, 1345), T("Fascicolo"), anim="pop", shadow=False), "hit")
        sc.footer = "Ricostruzione a scopo divulgativo · voce generata con sintesi vocale"
    return sc
