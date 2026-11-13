import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from klm import *
W, H = 1080, 1920
FY = 1300
GB = (60, 640, 1020, 1240)

def build(i, dur, a, words):
    T = Clock(words, a); sc = Scene(dur)
    if i == 0:
        te = T("E") - 0.2
        sc.add(Img(lady_pic(330, 412), (540, 820), a, te, anim="drop", rot=-3), "paper")
        sc.add(Text("Un *Klimt* sparito", (540, 400), a, te, size=96, anchor="ma", align="m"))
        sc.add(Big("22 ANNI", (540, 1180), T("ventidue") - 0.2, te, size=150, color=GOLD, fnt=OSW, count=(0, 22, lambda z: f"{z:.0f} ANNI", 0.8)), "hit")
        sc.add(Niche((60, 520, 1020, 1320), te, None, clear=te, door=te + 0.3, open_=T("muro") - 0.3, sack=T("muro"), canvas=T("rubato") - 0.3))
        sc.add(Text("...nel *muro* del museo", (540, 400), te, size=84, anchor="ma", align="m"))
        sc.add(Stamp("CASO 004", (260, 1250), T("rubato"), size=60, rot=-10))
        sc.footer = "Fonti: Il Post · Finestre sull'Arte · Live Science"
    elif i == 1:
        tg = T("Dalla") - 0.2; tt = T("Sul") - 0.2
        sc.add(Calendar((540, 760), 320, [(a, "PIACENZA · FEBBRAIO", "1997")], a, tg), "paper")
        sc.add(Gallery(GB, tg, hl=tg, gone=T("sparisce") - 0.1, roof_frame=T("cornice") - 0.2, title=None))
        sc.add(Pill("RITRATTO DI SIGNORA", (540, 470), T("Ritratto") - 0.2, tt, size=50))
        sc.add(Pill("LA CORNICE SUL TETTO", (540, 470), T("cornice") - 0.1, size=50, accent=True))
        sc.add(Stamp("VUOTA", (760, 600), T("Vuota") - 0.1, size=110, rot=-8))
        scene_cam(sc, (0, 540, 960, 1.0), (tt, 540, 960, 1.0), (tt + 1.0, 480, 880, 1.15), (dur, 480, 880, 1.17))
        sc.footer = "Fonti: AGI · Smithsonian · Reuters (Dawn)"
    elif i == 2:
        tu = T("L'unico") - 0.3
        sc.add(Figure([(a, 230, 1150)], a + 0.1, tu, kind="expert", s=0.85, label="STUDENTESSA"), "pop")
        sc.add(KIcon("book", (230, 600), a + 0.3, tu, size=200), "pop")
        sc.add(XRay((690, 820), 400, 500, T("sotto") - 0.4, tu, scan=T("sotto") - 0.1, dur=1.6, label=False))
        sc.add(Pill("UN ALTRO RITRATTO SOTTO", (540, 420), T("altro") - 0.2, tu, size=50))
        sc.add(Stamp("UNICO DOPPIO\nRITRATTO", (540, 820), tu + 0.1, size=100, rot=-7))
        sc.add(Text("raggi X · ricostruzione grafica", (540, 1200), tu + 0.2, size=34, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: Smithsonian · artnet · Reuters (Dawn)"
    elif i == 3:
        sc.add(Img(lady_pic(300, 375), (540, 700), a, T("indagini") - 0.2, anim="pop"), "pop")
        sc.add(Stamp("FALSO", (540, 700), a + 0.5, T("indagini") - 0.2, size=120, rot=-12))
        sc.add(Stamp("ARCHIVIATO", (540, 760), T("indagini") - 0.1, T("anni") - 0.2, size=110, rot=-8))
        sc.add(Calendar((540, 800), 360, [(T("anni") - 0.2, "1997", "?"), (T("anni") + 0.4, "2005", "?"), (T("silenzio") - 0.1, "2015", "?")], T("anni") - 0.2), "paper")
        sc.add(Pill("NESSUNA TRACCIA", (540, 1180), T("silenzio") - 0.2, size=50, accent=True))
        sc.footer = "Fonti: Smithsonian · artnet · Il Post"
    elif i == 4:
        td = T("Dietro") - 0.3
        sc.add(Calendar((540, 760), 300, [(a, "DICEMBRE", "2019")], a, T("Alcuni") - 0.2), "paper")
        sc.add(Figure(walk([(-100, FY), (330, FY)], T("Alcuni") - 0.3, 420) if False else [(T("Alcuni") - 0.3, -100, FY), (T("Alcuni") + 0.8, 300, FY)],
                      T("Alcuni") - 0.3, td, kind="worker", s=1.0, arms=[(T("l'edera"), "up")], label="GIARDINIERI"))
        sc.add(KIcon("leaf", (760, 760), T("l'edera") - 0.2, td, size=240), "pop")
        sc.add(Niche((60, 500, 1020, 1320), td, None, clear=td, door=td + 0.2, open_=td + 0.6, sack=T("sacco") - 0.2, canvas=T("quadro") - 0.2))
        sc.add(Pill("UN SACCO NERO", (540, 420), T("sacco") - 0.1, T("Dentro") - 0.1, size=52))
        sc.add(Pill("DENTRO, IL QUADRO", (540, 420), T("Dentro") - 0.1, size=56, accent=True))
        scene_cam(sc, (0, 540, 960, 1.0), (td + 0.4, 540, 960, 1.0), (dur, 600, 900, 1.2))
        sc.footer = "Fonti: Finestre sull'Arte · Live Science · Il Post"
    elif i == 5:
        tm = T("Ma") - 0.2
        sc.add(Img(lady_pic(340, 425), (540, 800), a, tm, anim="pop"), "pop")
        sc.add(Text("La *perizia*", (540, 400), a, tm, size=96, anchor="ma"))
        sc.add(Stamp("AUTENTICO", (540, 860), T("autentico") - 0.1, tm, size=120, color=(60, 150, 80), rot=-10))
        sc.add(Figure([(0, 540, 1250)], tm, kind="man", s=1.1, label="IL LADRO?"), "pop")
        sc.add(Text("Chi l'ha *rubato*?", (540, 400), tm, size=96, anchor="ma"))
        sc.add(Pill("ANCORA OGGI NON SI SA", (540, 560), T("ancora") - 0.2, size=52, accent=True))
        sc.footer = "Fonti: artnet · AGI · Live Science"
    elif i == 6:
        sc.add(Text("Storia completa su YouTube", (540, 700), a, size=54, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(96), (540, 900), T("Fascicolo") - 0.3, anim="pop", shadow=False), "hit")
        sc.add(Stamp("CASO 004", (540, 1180), T("Fascicolo"), size=70, rot=-8))
        sc.footer = "Ricostruzione divulgativa · voce sintetica"
    return sc
