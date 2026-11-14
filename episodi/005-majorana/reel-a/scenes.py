import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from maj import *
W, H = 1080, 1920
FY = 1300
SEAB = (40, 640, 1040, 1300)
VE = (-66.0, 10.16); IT = (12.5, 41.9)

def build(i, dur, a, words):
    T = Clock(words, a); sc = Scene(dur)
    if i == 0:
        tp = T("prende") - 0.2; ts = T("e", 1) - 0.2
        sc.add(Text("Un *genio*\ndella fisica", (540, 400), a, size=96, anchor="ma", align="m"))
        sc.add(Icon("money", (330, 860), T("ritira") - 0.2, size=260), "pop")
        sc.add(Icon("passport", (750, 860), tp, size=260), "pop")
        sc.add(Figure([(0, 540, FY)], a + 0.2, ts, kind="suit", s=1.0), "pop")
        sc.add(Figure([(0, 540, FY)], ts, ts + 0.9, kind="suit", s=1.0))
        sc.add(Icon("question", (540, 1110), ts + 0.4, size=260), "pop")
        sc.add(Stamp("SPARITO", (540, 860), T("nulla") - 0.2, size=120, rot=-10))
        sc.footer = "Fonti: Focus · Electra (Fundação EDP)"
    elif i == 1:
        tp = T("Per") - 0.2
        sc.add(Img(person_card("ETTORE MAJORANA", "fisico · 1906", 380), (540, 820), a, anim="drop", rot=-3), "paper")
        sc.add(Text("sagoma · nessuna foto reale", (540, 1130), a + 0.2, T("Galileo") - 0.3, size=30, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Pill("PER ENRICO FERMI: UN GENIO", (540, 420), tp, size=52, accent=True))
        sc.add(Text("come *Galileo*\ne *Newton*", (540, 1140), T("Galileo") - 0.2, size=72, anchor="ma", align="m"))
        sc.add(Stamp("CASO 005", (830, 600), a + 0.6, size=60, rot=-10))
        sc.footer = "Fonti: E. Recami (arXiv) · ANSA"
    elif i == 2:
        tn = T("Prende") - 0.3; tr = T("Scrive") - 0.2; tq = T("Poi") - 0.2
        sc.add(Calendar((540, 760), 320, [(a, "NAPOLI · MARZO", "1938")], a, tn), "paper")
        sc.add(MapEl((60, 400, 1020, 1300), [(0, (13.9, 39.5), 200), (dur, (13.9, 39.5), 210)], tn, tr,
                     routes=[dict(pts=["Napoli", "Palermo"], t=tn + 0.2, d=1.6, icon="ship")],
                     pins=[dict(at="Napoli", label="NAPOLI", t=tn, side="r"), dict(at="Palermo", label="PALERMO", t=tn + 0.8, side="r")], title="mappa: Natural Earth"))
        sc.add(Icon("telegram", (540, 470), tr, tq, size=170, label="«TORNERÒ»"), "pop")
        sc.add(Sea(SEAB, tr + 0.3, None, ship=[(tr + 0.3, .8), (tq + 0.3, .45)], flip=-1, ghost=tq + 0.2, sw=0.6))
        sc.add(Stamp("NESSUNA\nNOTIZIA CERTA", (540, 760), T("notizia") - 0.2, size=90, rot=-8))
        sc.footer = "Fonti: Electra (Fundação EDP) · Il Post · Focus"
    elif i == 3:
        sc.add(Text("Per *decenni*...", (540, 420), a, size=90, anchor="ma"))
        sc.add(Icon("ship", (540, 700), T("mare") - 0.2, size=260, label="IL MARE?"), "pop")
        sc.add(Icon("convent", (300, 1080), T("convento") - 0.2, size=250, label="UN CONVENTO?"), "pop")
        sc.add(Icon("flagless_globe", (780, 1080), T("l'Arg") - 0.2, size=250, label="L'ARGENTINA?"), "pop")
        sc.footer = "Fonti: Il Post · Focus · Discovery UK"
    elif i == 4:
        tc = T("altro") - 0.6; tf = T("c'è") - 0.4
        sc.add(Calendar((540, 520), 240, [(a, "SEGNALAZIONE", "2008")], a, tc - 0.3), "paper")
        sc.add(WorldMap((40, 700, 1040, 1300), a + 0.3, tc, view=(-80, 30, -10, 58), hl=("Italy", "Venezuela"),
                        routes=[dict(a=IT, b=VE, t=T("Venezuela") - 0.6, d=1.4, bend=0.15, icon="ship")],
                        pins=[dict(at=VE, label="VENEZUELA", t=T("Venezuela"), side="b")]))
        sc.add(Figure([(0, 540, FY)], tc, tf, kind="suit", s=1.0, label="«SIGNOR BINI»"), "pop")
        sc.add(Pill("UN ALTRO NOME", (540, 520), tc + 0.2, tf, size=56, accent=True))
        sc.add(Img(photo1955(520), (540, 880), tf, anim="drop", rot=-3), "paper")
        sc.add(Pill("VALENCIA · 1955", (540, 460), T("1955") - 0.3, size=56, accent=True))
        sc.footer = "Fonti: Avvenire · AGI · Il Fatto Quotidiano"
    elif i == 5:
        tv = T("era") - 0.2; tm = T("Ma") - 0.2
        sc.add(Calendar((540, 520), 240, [(a, "PROCURA DI ROMA", "2015")], a, tm), "paper")
        sc.add(Img(doc_typed(820, 520, "PROCURA DI ROMA · CONCLUSIONI (sintesi)", ["Vivo, almeno 1955-1959,", "a Valencia (Venezuela).", "", "Trasferimento *volontario*."], size=36), (540, 960), a + 0.4, tm, anim="drop", rot=-1), "paper")
        sc.add(Stamp("VIVO", (780, 820), tv, tm, size=110, color=(60, 150, 80), rot=-10))
        sc.add(Stamp("VOLONTARIO", (540, 1140), T("volontà") - 0.2, tm, size=90, rot=-8))
        sc.add(Icon("question", (540, 860), tm + 0.1, size=380), "pop")
        sc.add(Text("Ma *perché*?", (540, 450), tm + 0.1, size=110, anchor="ma"))
        sc.footer = "Fonti: Il Fatto Quotidiano · Avvenire · AGI · ANSA"
    elif i == 6:
        sc.add(Text("Storia completa su YouTube", (540, 700), a, size=54, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(96), (540, 900), T("Fascicolo") - 0.3, anim="pop", shadow=False), "hit")
        sc.add(Stamp("CASO 005", (540, 1180), T("Fascicolo"), size=70, rot=-8))
        sc.footer = "Ricostruzione divulgativa · voce sintetica"
    return sc
