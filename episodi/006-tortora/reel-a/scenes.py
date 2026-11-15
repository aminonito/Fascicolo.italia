import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from tor import *
W, H = 1080, 1920
FY = 1300
STB = (40, 560, 1040, 1300)

def build(i, dur, a, words):
    T = Clock(words, a); sc = Scene(dur)
    if i == 0:
        tp = T("prova") - 0.6; tn = T("che") - 0.3
        sc.add(Studio((40, 640, 1040, 1300), a, tp, parrot=True, sign="STUDIO TV", label=None))
        sc.add(Figure([(0, 600, FY)], a, tp, kind="suit", s=1.0), "pop")
        sc.add(Text("Il volto più *amato*\ndella TV", (540, 370), a, tp, size=84, anchor="ma", align="m"))
        sc.add(Icon("handcuffs", (600, 1080), T("manette") - 0.3, tp, size=200), "pop")
        sc.add(Flash(T("manette") - 0.1))
        sc.add(Icon("addressbook", (540, 800), tp, tn, size=420, label="LA PROVA SCRITTA"), "pop")
        sc.add(Img(lettere(900, 200, "TORTONA", 5, color=GOLD), (540, 760), tn, anim="pop", shadow=False), "hit")
        sc.add(Stamp("NON ERA\nIL SUO NOME", (540, 1050), T("suo") - 0.3, size=90, rot=-8))
        sc.footer = "Fonti: Il Post · Focus · AGI"
    elif i == 1:
        tr = T("Roma") - 0.3; ta = T("Accusa") - 0.3
        sc.add(Img(person_card("ENZO TORTORA", "conduttore di Portobello", 380), (540, 820), a, tr, anim="drop", rot=-3), "paper")
        sc.add(Text("sagoma · nessuna foto reale", (540, 1130), a + 0.2, tr, size=30, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Calendar((300, 560), 280, [(tr, "GIUGNO", "17"), (tr + 1.0, "GIUGNO", "1983")], tr, ta), "paper")
        sc.add(Icon("moon", (780, 520), tr + 0.3, ta, size=160), "pop")
        sc.add(Figure([(0, 380, FY)], tr + 0.5, kind="police", s=1.0, label="CARABINIERI"), "pop")
        sc.add(Figure([(0, 720, FY)], tr + 0.5, ta + 0.4, kind="suit", s=1.0, arms=[(tr + 0.5, "hold")]), "pop")
        sc.add(Icon("handcuffs", (720, 1110), tr + 0.8, ta + 0.4, size=120), "pop")
        sc.add(Pill("ACCUSA: CAMORRA", (540, 620), ta, size=64, accent=True))
        sc.add(Pill("E DROGA", (540, 760), T("droga") - 0.2, size=64, accent=True))
        sc.footer = "Fonti: Il Post · AGI · Sky TG24"
    elif i == 2:
        te = T("nell") - 0.3; tt = T("Tortona") - 0.3; tn = T("Il") - 0.3
        sc.add(Big("19", (540, 620), a, te, size=300, color=GOLD, fnt=OSW, sub="ACCUSATORI"), "hit")
        sc.add(Crowd((80, 1000, 1000, 1290), 19, a + 0.2, te, s=0.34, stagger=0.06))
        sc.add(Img(agenda_img(900, 580), (540, 820), te, tt, anim="drop", rot=-1), "paper")
        sc.add(Img(lettere(900, 200, "TORTORA", 5), (540, 560), tt, anim="pop", shadow=False))
        sc.add(Line((140, 560), (940, 560), tt + 0.4, color=RED, width=10))
        sc.add(Img(lettere(900, 200, "TORTONA", 5, color=GOLD), (540, 800), tt + 0.3, anim="pop", shadow=False), "hit")
        sc.add(Pill("CON LA ENNE", (540, 960), T("enne") - 0.3, size=56, accent=True))
        sc.add(Icon("phone", (540, 1180), tn, size=150), "pop")
        sc.add(Stamp("NON È IL SUO", (540, 1180), T("suo") - 0.2, size=80, rot=-8))
        sc.footer = "Fonti: Focus · AGI · Il Post · Geopop"
    elif i == 3:
        tc = T("Centrini") - 0.3; ts = T("spediti") - 0.3; tm = T("mai") - 0.3
        sc.add(Text("Il *movente*?", (540, 420), a, size=96, anchor="ma"))
        sc.add(Icon("question", (540, 800), a + 0.2, tc, size=300), "pop")
        sc.add(Icon("doily", (540, 820), tc, ts, size=420), "pop")
        sc.add(Icon("crochet", (820, 1060), tc + 0.3, ts, size=160), "pop")
        sc.add(Icon("prison", (260, 760), ts, size=240, label="UN DETENUTO"), "pop")
        sc.add(Icon("doily", (300, 800), ts + 0.2, size=160, move=(ts + 0.5, 1.2, (760, 760), 160)), "whoosh")
        sc.add(Icon("tv", (800, 760), ts + 0.2, size=260, label="PORTOBELLO"), "pop")
        sc.add(Stamp("MAI IN ONDA", (540, 1120), tm, size=90, rot=-8))
        sc.add(Text("secondo le ricostruzioni", (540, 1260), tm + 0.3, size=32, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: Il Post · AGI"
    elif i == 4:
        t2 = T("Nel", 1) - 0.3
        sc.add(Aula((40, 460, 1040, 1300), a, None, judges_t=a + 0.2, cage_t=a + 0.2, who=True, label=None, motto=False))
        sc.add(Calendar((830, 560), 220, [(a, "SETTEMBRE", "1985"), (t2, "SETTEMBRE", "1986")], a), "paper")
        sc.add(Big("10 ANNI", (540, 860), T("condannato") - 0.2, t2, size=200, color=WHITE, fnt=OSW), "hit")
        sc.add(Stamp("CONDANNATO", (540, 1060), T("dieci") - 0.2, t2, size=80, rot=-8))
        sc.add(Stamp("ASSOLTO", (540, 860), T("assolve") - 0.2, size=130, rot=-8, color=(60, 150, 80)))
        sc.add(Pill("FORMULA PIENA", (540, 1080), T("formula") - 0.2, size=64, accent=True))
        sc.footer = "Fonti: Il Post · Focus · AGI · Geopop"
    elif i == 5:
        td = T("Dunque") - 0.2
        sc.add(Studio((40, 720, 1040, 1300), a, None, parrot=True, sign=None, label=None))
        sc.add(Figure([(0, 600, FY)], a, kind="suit", s=1.0), "pop")
        sc.add(Calendar((540, 540), 240, [(a, "FEBBRAIO", "1987")], a, td), "paper")
        sc.add(Text("«Dunque,\ndove eravamo\n*rimasti*?»", (540, 360), td, size=90, anchor="ma", align="m"))
        sc.footer = "Fonti: Il Post · Focus · Geopop"
    elif i == 6:
        sc.add(Text("Storia completa su YouTube", (540, 700), a, size=54, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(96), (540, 900), T("Fascicolo") - 0.3, anim="pop", shadow=False), "hit")
        sc.add(Stamp("CASO 006", (540, 1180), T("Fascicolo"), size=70, rot=-8))
        sc.footer = "Ricostruzione divulgativa · voce sintetica"
    return sc
