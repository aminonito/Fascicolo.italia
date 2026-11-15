import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from osp import *

W, H = 1920, 1080
FY = 870
XB = (160, 170, 1760, 870)      # scenografia: l'incrocio
F_COLPO = "Fonti: Il Post · Varesenews · Milano Città Stato · Il Giornale"
F_BAND = "Fonti: Il Post · Geopop · MilanoFree · Varesenews"
F_IND = "Fonti: Il Post · Geopop · Wikipedia · Milano Città Stato · Il Giornale"

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

def build(i, dur, a, words):
    T0 = Clock(words, a)
    def T(p, n=0):
        try: return T0(p, n)
        except KeyError: return a + 0.5
    sc = Scene(dur)
    if i == 0:
        tc = T("un") - 0.3; ts = T("Sette") - 0.3; tp = T("Pochi") - 0.3
        sc.add(Calendar((330, 400), 240, [(a, "MILANO · FEBBRAIO", "27"), (a + 1.3, "FEBBRAIO", "1958")], a, T("Poco")), "paper")
        sc.add(ClockFace((960, 400), 150, a + 0.4, T("un"), start=9.0, speed=0.08, label="POCO DOPO LE 9"))
        sc.add(Icon("factory", (1560, 420), T("periferia") - 0.3, tc, size=260, label="PERIFERIA OVEST"), "pop")
        sc.add(Crossing(XB, tc, ts, cars=[dict(kind="van", keys=[(tc, -.08, .63, 0), (tc + 2.2, .40, .63, 0)], label="PORTAVALORI"),
                                       dict(kind="truck", keys=[(tc, 1.1, .63, 180), (tc + 2.2, .52, .63, 180)])],
                        marks=[dict(t=tc + 2.2, x=.46, y=.63, text="BAM!")]))
        sc.add(Pill("UN CAMION SPERONA IL FURGONE", (960, 230), T("speronato") - 0.2, ts, size=46, accent=True))
        for k in range(7):
            sc.add(Figure([(0, 330 + k * 210, FY)], ts + 0.12 * k, tp, kind="worker", s=0.8), "pop" if k % 3 == 0 else None)
        sc.add(Icon("overalls", (700, 360), T("tuta") - 0.2, tp, size=200, label="TUTE DA OPERAIO"), "pop")
        sc.add(Icon("balaclava", (1220, 360), T("passamontagna") - 0.2, tp, size=200, label="PASSAMONTAGNA"), "pop")
        sc.add(Big("100+ milioni", (960, 470), T("con") - 0.1, size=180, color=GOLD, fnt=OSW, count=(0, 100, lambda z: f"{z:.0f}+ milioni", 1.2), sub="di lire in contanti"), "hit")
        for k in range(4): sc.add(Icon("moneybag", (420 + k * 360, 790), tp + 0.3 + 0.12 * k, size=170), "pop" if k == 0 else None)
        sc.footer = F_COLPO
    elif i == 1:
        tg = T("I") - 0.3; tq = T("Questo") - 0.3; tv = T("Vedremo") - 0.3
        sc.add(Stamp("NESSUN COLPO\nSPARATO", (620, 450), a + 0.1, tg, size=80, rot=-8))
        sc.add(Stamp("NESSUN\nFERITO", (1300, 470), T("ferito") - 0.2, tg, size=80, rot=6, color=(60, 150, 80)))
        sc.add(Img(newspaper(620, 640, "CRONACA", "28 febbraio 1958", "La rapina\n*del secolo*", "sette banditi in tuta"), (960, 520), tg, tq + 0.2, anim="drop", rot=-3), "paper")
        sc.add(Icon("camera", (1480, 330), tg + 0.4, tq, size=150), "pop")
        sc.add(Img(cover_folder(), (960, 520), tq + 0.1, tv, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 007", (1150, 300), T("fascicolo") + 0.2, tv, size=70, rot=-12))
        sc.add(Icon("van", (330, 470), tv + 0.1, size=200, label="IL PIANO"), "pop")
        sc.add(Icon("question", (750, 470), T("come", 1) - 0.2, size=190, label="LA FUGA"), "pop")
        sc.add(Icon("handcuffs", (1170, 470), T("quale") - 0.2, size=190, label="L'ERRORE"), "pop")
        sc.add(Icon("river", (1590, 470), T("sacco") - 0.3, size=210, label="IL FIUME"), "pop")
        sc.footer = "Fonti: Il Post · Geopop · MilanoFree · giornale ricostruito"
    elif i == 2:
        tc = T("È") - 0.3; tf = T("Le") - 0.3; to = T("e") - 0.3; ts = T("Uno") - 0.3
        sc.add(Chapter("01", "Il giorno di *paga*", a, tc))
        sc.add(Calendar((330, 380), 220, [(tc, "MILANO, FINE", "'50")], tc, ts), "paper")
        sc.add(Pill("IL BOOM ECONOMICO", (960, 230), tc + 0.2, ts, size=50, accent=True))
        for k in range(3): sc.add(Icon("factory", (760 + k * 380, 450), tf + 0.2 * k, ts, size=280), "pop" if k == 0 else None)
        sc.add(Crowd((300, 640, 1640, 890), 18, to, None, s=0.36, kinds=("worker", "man", "worker"), stagger=0.05))
        sc.add(Icon("payenv", (960, 400), ts, size=300, label="IN CONTANTI"), "hit")
        for k in range(2): sc.add(Icon("money", (640 + k * 640, 400), ts + 0.3 + 0.2 * k, size=170), "pop")
        sc.footer = "Fonti: Il Giornale · MilanoFree · Il Post"
    elif i == 3:
        tv = T("E") - 0.3; tg = T("Il") - 0.3; tp = T("i", 3) - 0.3
        sc.add(Icon("museum", (380, 470), a + 0.1, size=300, label="BANCA"), "pop")
        sc.add(Icon("factory", (1540, 470), a + 0.4, size=300, label="AZIENDE"), "pop")
        sc.add(Arrow((560, 470), (1360, 470), a + 0.8, color=GOLD, bend=-0.15, dashed=True))
        sc.add(Icon("van", (380, 780), tv, None, size=230, move=(tv + 0.3, 2.6, (1540, 780), 0)), "pop")
        sc.add(Calendar((960, 330), 220, [(tg, "OGNI MESE", "27")], tg), "paper")
        sc.add(Pill("GIORNO DI PAGA", (960, 560), T("giorno") - 0.1, size=46, accent=True))
        for k in range(5): sc.add(Icon("moneybag", (720 + k * 120, 690), T("pieni") - 0.2 + 0.08 * k, size=120), "pop" if k == 0 else None)
        sc.footer = "Fonti: Il Giornale · MilanoFree"
    elif i == 4:
        tb = T("A") - 0.3; ts = T("La") - 0.3
        sc.add(Icon("van", (960, 400), a, ts, size=440), "pop")
        sc.add(Pill("BANCA POPOLARE DI MILANO", (960, 220), a + 0.4, ts, size=44, accent=True))
        sc.add(Figure([(0, 420, FY)], T("l'autista") - 0.2, ts, kind="man", s=0.8, label="AUTISTA"), "pop")
        sc.add(Figure([(0, 960, FY)], T("impiegato") - 0.2, ts, kind="suit", s=0.8, label="IMPIEGATO"), "pop")
        sc.add(Figure([(0, 1500, FY)], T("agente") - 0.2, ts, kind="police", s=0.8, label="AGENTE ARMATO"), "pop")
        sc.add(MapEl((360, 170, 1560, 870), [(ts, (10.5, 45.0), 160), (dur, (9.6, 45.3), 260)], ts,
                     pins=[dict(at="Milano", label="MILANO · PERIFERIA OVEST: VIA OSOPPO", t=T("periferia") - 0.2, side="r", color=RED), dict(at="Torino", label="TORINO", t=ts + 0.3, side="l")],
                     title="mappa: Natural Earth · schema non in scala"))
        sc.footer = "Fonti: Il Post · MilanoFree · Il Giornale"
    elif i == 5:
        tl_ = T("Una") - 0.3; tp = T("Proprio") - 0.3; to = T("Non") - 0.3; tr = T("Ricordatevi") - 0.3
        sc.add(Crossing(XB, a, None, olona=True))
        scene_cam(sc, (0, 960, 540, 1.0), (to, 960, 540, 1.0), (to + 1.2, 700, 380, 1.3), (tr + 0.8, 700, 380, 1.3), (tr + 2.0, 960, 540, 1.0), (dur, 960, 540, 1.0))
        sc.add(Pill("STRADA LARGA", (520, 280), tl_, to, size=44, accent=True))
        for p, q in [((1088, 580), (1088, 200)), ((1088, 650), (1088, 860)), ((1200, 600), (1700, 600)), ((900, 600), (220, 600))]:
            sc.add(Arrow(p, q, T("vie") + 0.1, to, color=GOLD, dashed=True))
        sc.add(Pill("PIÙ VIE DI FUGA", (1400, 300), T("vie"), to, size=44))
        sc.add(Stamp("LUOGO\nSCELTO", (480, 780), tp + 0.6, to, size=60, rot=-8))
        sc.add(Icon("river", (560, 250), T("Olona") - 0.2, tr + 2.0, size=200), "pop")
        sc.add(Stamp("RICORDATE\nIL FIUME", (1400, 400), tr + 2.0, size=66, rot=-8))
        sc.footer = "Fonti: Il Post · Varesenews · Milano Città Stato · schema non in scala"
    elif i == 6:
        tc = T("Sette") - 0.3; tm = T("Molti") - 0.3; tca = T("Il", 0) - 0.3; ti = T("In") - 0.3
        sc.add(Chapter("02", "La *banda*", a, tc))
        for k in range(7): sc.add(Figure([(0, 330 + k * 210, FY)], tc + 0.1 * k, tca, kind="man", s=0.75), "pop" if k == 0 else None)
        sc.add(Pill("CIRCA 30 ANNI", (960, 280), T("quasi") - 0.2, tca, size=48, accent=True))
        sc.add(Icon("prison", (960, 470), tm, tca, size=260, label="PRECEDENTI"), "pop")
        sc.add(Img(person_card("UGO CIAPPINA", "ex partigiano", 280), (620, 500), tca + 0.3, anim="drop", rot=-3), "paper")
        sc.add(Pill("IL CAPO · SECONDO LE PIÙ CITATE RICOSTRUZIONI", (960, 220), tca + 0.4, ti, size=36))
        sc.add(Img(person_card("ENRICO CESARONI", "\"la mente\"?", 280), (1300, 500), ti + 0.2, anim="drop", rot=3), "paper")
        sc.add(Pill("SECONDO ALTRE RICOSTRUZIONI", (960, 220), ti + 0.2, size=36, accent=True))
        sc.add(Text("sagome · nessuna foto reale", (960, 840), tca + 0.5, size=26, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = F_BAND
    elif i == 7:
        names = [("LUCIANO DE MARIA", "Luciano"), ("ARNALDO GESMUNDO", "Gesmundo"), ("FERDINANDO RUSSO", "Ferdinando"),
                 ("ARNALDO BOLOGNINI", "Bolognini"), ("EROS CASTIGLIONI", "Eros")]
        nick = {1: "\"Jess il bandito\"", 2: "\"Nando\""}
        sc.add(Pill("DALLE SENTENZE", (960, 220), a + 0.2, size=44, accent=True))
        for k, (n, w_) in enumerate(names):
            sc.add(Img(person_card(n, nick.get(k, "condannato"), 230, seed=k + 3), (300 + k * 330, 520), T(w_) - 0.3, anim="drop", rot=(-3 + 2 * k) % 7 - 3), "paper")
        sc.add(Img(person_card("UGO CIAPPINA", "ex partigiano", 150, seed=9), (300, 790), T("Sette") - 0.3, anim="drop"), "paper")
        sc.add(Img(person_card("ENRICO CESARONI", "", 150, seed=10), (520, 790), T("Sette") - 0.1, anim="drop"), "paper")
        sc.add(Big("7", (1400, 790), T("Sette") + 0.1, size=150, color=GOLD, fnt=OSW))
        sc.add(Icon("question", (1600, 790), T("nessuno") - 0.2, size=130), "pop")
        sc.footer = "Fonti: Il Post · MilanoFree · Varesenews · Il Giornale · sagome, non foto"
    elif i == 8:
        tv = T("Vuole") - 0.3; to = T("Ognuno") - 0.3; tm = T("e") - 0.3; tob = T("L'obiettivo") - 0.3
        sc.add(Icon("clapper", (960, 470), tv, to, size=340, label="COME IN UN FILM"), "pop")
        sc.add(ClockFace((1480, 430), 140, tv + 0.4, to, start=9.2, speed=0.2))
        for k, (kn, lab) in enumerate((("worker", "AUTO"), ("worker", "CAMION"), ("worker", "CARICO"), ("worker", "FUGA"))):
            sc.add(Figure([(0, 420 + k * 360, FY)], to + 0.2 * k, tob, kind=kn, s=0.75, label=lab), "pop" if k == 0 else None)
        sc.add(Icon("fiat", (560, 380), tm, tob, size=230), "pop"); sc.add(Icon("truck", (960, 380), tm + 0.2, tob, size=230), "pop"); sc.add(Icon("sportcar", (1360, 380), tm + 0.4, tob, size=230), "pop")
        sc.add(Stamp("RUBATI\nTARGHE FALSE", (960, 260), T("rubati") - 0.1, tob, size=60, rot=-6))
        sc.add(Pill("OBIETTIVO", (960, 300), tob, size=44, accent=True))
        sc.add(Icon("moneybag", (760, 520), tob + 0.3, size=240), "pop")
        sc.add(Stamp("SENZA\nSANGUE", (1200, 520), T("senza") - 0.1, size=70, rot=-8, color=(60, 150, 80)))
        sc.footer = "Fonti: Il Post · MilanoFree · Varesenews"
    elif i == 9:
        tc = T("Secondo") - 0.3; tq = T("Qualcosa") - 0.3; ts = T("Si") - 0.3
        sc.add(Chapter("03", "Le prove *generali*", a, tc))
        sc.add(Calendar((360, 420), 240, [(tc, "SETTIMANE", "PRIMA"), (tc + 1.0, "TENTATIVO", "1"), (tc + 2.0, "TENTATIVO", "2")], tc), "paper")
        sc.add(Icon("van", (960, 470), tc + 0.3, ts, size=380), "pop")
        sc.add(Stamp("FALLITO", (900, 420), tq, ts, size=70, rot=-10)); sc.add(Stamp("FALLITO", (1050, 560), tq + 0.8, ts, size=70, rot=6))
        sc.add(Icon("van", (820, 520), ts + 0.2, None, size=260, move=(ts + 0.6, 3.0, (1500, 520), 0)), "pop")
        sc.add(Icon("question", (1420, 360), T("sbagliato") - 0.4, size=170), "pop")
        sc.add(Pill("SI RACCONTA", (960, 260), ts + 0.2, size=44, accent=True))
        sc.footer = "Fonti: Geopop · MilanoFree · Il Giornale"
    elif i == 10:
        tl_ = T("La") - 0.3; te = T("E") - 0.3; tg = T("Il", 1) - 0.3
        sc.add(Crossing(XB, a, te, cars=[dict(kind="van", keys=[(a, -.1, .63, 0), (a + 3.0, 1.1, .63, 0)], label="PORTAVALORI"),
                                        dict(kind="van", keys=[(a + 4.0, -.1, .63, 0), (a + 7.0, 1.1, .63, 0)])]))
        sc.add(Figure([(0, 1500, FY)], tl_, te, kind="expert", s=0.8, carry=[(tl_, "magnifier")], label="OSSERVA"), "pop")
        sc.add(ClockFace((420, 330), 110, T("orari") - 0.3, te, start=9.0, speed=0.3), "pop")
        sc.add(Pill("ORARI · PERCORSO · ABITUDINI", (960, 230), T("orari"), te, size=42, accent=True))
        sc.add(Calendar((960, 470), 300, [(te, "FEBBRAIO", "20"), (te + 0.6, "FEBBRAIO", "24"), (tg, "GIOVEDÌ", "27")], te), "paper")
        sc.add(Stamp("IL GIORNO\nGIUSTO", (1350, 400), T("febbraio") + 0.2, size=60, rot=-8))
        sc.footer = "Fonti: MilanoFree · Il Giornale · schema non in scala"
    elif i == 11:
        tc = T("Il") - 0.3; td = T("Davanti") - 0.3; tf = T("È", 1) - 0.3; tm = T("Finisce") - 0.3
        sc.add(Chapter("04", "Pochi *minuti*", a, tc))
        sc.add(Crossing(XB, tc, None, cars=[dict(kind="van", keys=[(tc, -.1, .63, 0), (td, .18, .63, 0), (tm + 0.6, .32, .63, 0)], label="PORTAVALORI"),
                                         dict(kind="fiat", keys=[(tc, .12, .63, 0), (td, .40, .63, 0), (td + 0.7, .46, .58, -12), (td + 1.4, .52, .66, 14), (td + 2.1, .58, .60, -10), (tm, .66, .66, 10), (tm + 0.5, .72, .78, 40)], label="FIAT 1400")],
                        marks=[dict(t=tm + 0.5, x=.74, y=.82, text="CRASH")]))
        sc.add(Pill("RALLENTA E SBANDA", (960, 230), td + 0.6, tf, size=44, accent=True))
        sc.add(Pill("ALLA GUIDA: UNO DELLA BANDA", (960, 230), tf, size=44))
        sc.footer = F_COLPO + " · schema non in scala"
    elif i == 12:
        tl_ = T("un") - 0.3; tb = T("Lo") - 0.3; ts = T("Il", 1) - 0.3
        sc.add(Crossing(XB, a, None, cars=[dict(kind="van", keys=[(a, .32, .63, 0), (a + 0.8, .40, .63, 0)], label="PORTAVALORI"),
                                        dict(kind="fiat", keys=[(a, .72, .78, 40)]),
                                        dict(kind="truck", keys=[(tl_, 1.12, .63, 180), (ts + 0.3, .56, .63, 180), (ts + 0.6, .52, .64, 172)], label="CAMIONCINO")],
                        marks=[dict(t=ts + 0.6, x=.47, y=.63, text="BAM!", d=2.5)]))
        sc.add(Icon("truck", (1500, 330), tl_, tb + 0.4, size=240, label="OM LEONCINO"), "pop")
        sc.add(Pill("ALLA GUIDA: ARNALDO BOLOGNINI", (960, 230), tb, size=40))
        sc.add(Stamp("BLOCCATO", (960, 760), T("blocca") - 0.1, size=80, rot=-8))
        sc.footer = F_COLPO + " · schema non in scala"
    elif i == 13:
        tg = T("Gli") - 0.3; tf = T("Un") - 0.3; ta = T("e") - 0.3; tl_ = T("L'autista") - 0.3
        sc.add(Icon("van", (960, 560), a, size=600), None)
        sc.add(ClockFace((1700, 260), 90, a, start=9.3, speed=0.02, label="SECONDI"))
        for k in range(3): sc.add(Figure(walk([(-100 - 150 * k, FY), (300 + 170 * k, FY)], tg + 0.1 * k, 500), tg + 0.1 * k, kind="worker", s=0.85), "pop" if k == 0 else None)
        sc.add(Icon("balaclava", (330, 300), tg + 0.4, tf, size=170, label="PASSAMONTAGNA"), "pop")
        sc.add(Icon("hammer", (900, 330), tf, ta + 0.6, size=200), "hit")
        sc.add(Flash(T("frantumi") - 0.1))
        sc.add(Figure([(0, 1450, FY)], ta, kind="police", s=0.8, arms=[(T("disarmato"), "up")], label="AGENTE DISARMATO"), "pop")
        sc.add(Figure([(0, 1250, FY)], tl_ + 0.2, kind="man", s=0.75, arms=[(tl_ + 0.4, "up")]), "pop")
        sc.add(Figure([(0, 1650, FY)], tl_ + 0.4, kind="suit", s=0.75, arms=[(tl_ + 0.6, "up")]), "pop")
        sc.add(Pill("MANI IN ALTO", (1450, 240), T("mani") - 0.1, size=46, accent=True))
        sc.footer = F_COLPO + " · ricostruzione grafica"
    elif i == 14:
        ti = T("Intanto") - 0.3; ts = T("Secondo") - 0.3; tn = T("Nessuno") - 0.3
        sc.add(Icon("van", (360, 560), a, size=380), None)
        sc.add(Icon("truck", (1560, 560), a + 0.2, size=380, label="ALTRO MEZZO"), "pop")
        for k in range(5):
            sc.add(Icon("moneybag" if k % 2 == 0 else "suitcase", (480, 560), a + 0.3 + 0.45 * k, None, size=130, move=(a + 0.4 + 0.45 * k, 0.8, (1450, 560 + (k % 3 - 1) * 40), 0)))
        sc.add(Facade((640, 170, 1280, 520), ti, tn + 1.5, label=None))
        sc.add(Crowd((680, 330, 1240, 500), 6, ti + 0.3, tn + 1.5, s=0.3))
        sc.add(Bubble((960, 640), 130, T("raffica") - 0.3, tn, text="TA-TA-TA!"), "pop")
        sc.add(Pill("SOLO CON LA BOCCA", (960, 830), T("raffica"), tn, size=40, accent=True))
        sc.add(Stamp("NESSUNO\nSPARA", (960, 620), tn + 0.1, size=90, rot=-8, color=(60, 150, 80)))
        sc.footer = "Fonti: Il Post · Milano Città Stato · Il Giornale · ricostruzione grafica"
    elif i == 15:
        tf = T("Fuggono") - 0.3; tin = T("In") - 0.3
        sc.add(Crossing(XB, a, None, cars=[dict(kind="van", keys=[(a, .40, .63, 0)], label="FURGONE"),
                                        dict(kind="fiat", keys=[(a, .72, .78, 40)]),
                                        dict(kind="truck", keys=[(a, .52, .64, 172)]),
                                        dict(kind="car", keys=[(a, .58, .52, -90), (tf + 0.2, .58, .52, -90), (tf + 2.2, .58, -.2, -90)], label="LA BANDA")]))
        sc.add(ClockFace((1600, 300), 110, a, tin, start=9.3, speed=0.05, label="POCHI MINUTI"))
        sc.add(Pill("VERSO NORD", (1000, 230), tf, tin, size=44, accent=True))
        sc.add(Icon("sportcar", (360, 330), T("cambiano") - 0.2, tin, size=220, label="CAMBIO AUTO"), "pop")
        sc.add(Pill("FURGONE AMMACCATO", (640, 760), T("furgone") - 0.2, size=36))
        sc.add(Pill("FIAT CONTRO IL MURO", (1420, 830), T("una") - 0.2, size=36))
        sc.add(Stamp("NESSUN\nFERITO", (1000, 420), T("feriti") - 0.4, size=70, rot=-6, color=(60, 150, 80)))
        sc.footer = F_COLPO + " · schema non in scala"
    elif i == 16:
        tn = T("Nel") - 0.3; tm = T("Ma") - 0.3; ti = T("soli") - 0.5
        sc.add(Big("114 milioni", (960, 380), a + 0.2, tn + 0.2, size=200, color=GOLD, fnt=OSW, count=(0, 114, lambda z: f"{z:.0f} milioni", 1.6), sub="di lire in contanti"), "hit")
        for k in range(6): sc.add(Icon("moneybag", (360 + k * 240, 750), a + 0.5 + 0.1 * k, tn + 0.2, size=160), "pop" if k == 0 else None)
        for k in range(5): sc.add(Icon("cheque", (420 + k * 270, 470 + (k % 2) * 160), tn + 0.1 * k, ti, size=230), "paper" if k == 0 else None)
        sc.add(Pill("+ ASSEGNI E TITOLI", (960, 260), T("assegni"), ti, size=48, accent=True))
        sc.add(Stamp("LE CIFRE TOTALI\nNON COINCIDONO", (960, 770), tm + 0.3, ti, size=60, rot=-6))
        sc.add(Big("≈ 1,8 mln €", (960, 380), ti + 0.2, size=200, color=WHITE, fnt=OSW), "hit")
        sc.add(Text("114 mln di lire 1958 × coeff. ISTAT 31,47 ÷ 1936,27 = circa 1,85 mln di euro (2024)", (960, 640), ti + 0.6, size=30, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Pill("SOLO I CONTANTI · VALORE DI OGGI", (960, 760), ti + 0.9, size=40))
        sc.footer = "Fonti: Geopop · MilanoFree · Wikipedia · Il Post · ISTAT, Il valore della moneta in Italia"
    elif i == 17:
        tc = T("Sui") - 0.3; tp = T("La") - 0.3; tci = T("La", 1) - 0.3
        sc.add(Chapter("05", "La *caccia*", a, tc))
        sc.add(Img(newspaper(600, 640, "CRONACA", "1 marzo 1958", "Il colpo\n*più clamoroso*", "la caccia ai sette banditi"), (520, 520), tc, tci, anim="drop", rot=-3), "paper")
        sc.add(Crowd((960, 560, 1760, 890), 14, tp, None, s=0.42, kinds=("police",), stagger=0.06))
        sc.add(Pill("MIGLIAIA DI AGENTI E CARABINIERI", (1360, 260), T("migliaia") - 0.1, tci, size=40, accent=True))
        sc.add(Icon("magnifier", (520, 400), tci, size=220, label="QUARTIERE PER QUARTIERE"), "pop")
        for k in range(4): sc.add(Icon("house", (1080 + k * 190, 330), tci + 0.2 + 0.15 * k, size=140), "pop" if k == 0 else None)
        sc.footer = "Fonti: Il Post · Milano Città Stato · giornale ricostruito"
    elif i == 18:
        ti = T("I") - 0.3; ts = T("Si") - 0.3
        sc.add(Pill("GIAMBELLINO", (620, 230), a + 0.6, ti, size=44)); sc.add(Pill("LORENTEGGIO", (1300, 230), T("Lorenteggio") - 0.2, ti, size=44))
        for k in range(3): sc.add(Icon("suitcase", (560 + k * 400, 470), T("valigie") - 0.2 + 0.15 * k, ti, size=250), "pop" if k == 0 else None)
        for k in range(6): sc.add(Icon("cheque", (500 + k * 190, 700 + (k % 2) * 60), T("assegni") - 0.2 + 0.1 * k, ts, size=190, rot=(k * 7) % 20 - 10))
        sc.add(Stamp("BUTTATI VIA", (960, 470), ti + 0.2, ts, size=80, rot=-6))
        sc.add(Pill("TROPPO FACILI DA RINTRACCIARE", (960, 300), T("troppo") - 0.1, ts, size=42, accent=True))
        sc.add(Icon("moneybag", (960, 520), ts, size=340, label="SOLO CONTANTI"), "hit")
        sc.footer = "Fonti: Il Giornale · Milano Città Stato"
    elif i == 19:
        tu = T("Un") - 0.3; td = T("Dalla") - 0.3; tm = T("Ma") - 0.3
        sc.add(Figure(walk([(-100, FY), (560, FY)], a, 400), a, td, kind="police", s=0.8, label="INVESTIGATORI"))
        sc.add(Icon("shop", (1240, 520), tu, td, size=420), "pop")
        sc.add(Figure([(0, 1500, FY)], tu + 0.3, td, kind="man", s=0.8, flip=-1, label="IL SALUMIERE"), "pop")
        sc.add(Bubble((1000, 300), 110, T("ricorda") - 0.1, td, inner="overalls"), "pop")
        sc.add(Icon("identikit", (700, 480), td, size=360), "paper")
        sc.add(Img(newspaper(520, 560, "CRONACA", "2 marzo 1958", "Ecco\n*l'identikit*", "chi lo ha visto?"), (1300, 520), T("pubblicato") - 0.2, anim="drop", rot=3), "paper")
        sc.add(Stamp("NON BASTA", (960, 760), tm + 0.4, size=70, rot=-8))
        sc.footer = "Fonti: Il Post · Il Giornale · giornale ricostruito"
    elif i == 20:
        tu = T("Una") - 0.3; tn = T("Nessuno") - 0.3; tg = T("giornali") - 0.4
        sc.add(Crowd((200, 560, 1720, 890), 24, a + 0.3, None, s=0.4, stagger=0.03))
        sc.add(Pill("UNA PARTE DELLA CITTÀ SIMPATIZZA", (960, 230), tu + 0.3, tn, size=46, accent=True))
        sc.add(Bubble((600, 380), 140, tn, tg, text="NESSUN FERITO"), "pop")
        sc.add(Bubble((1320, 380), 140, T("soldi") - 0.2, tg, text="SOLDI DI BANCA"), "pop")
        sc.add(Img(newspaper(600, 520, "CRONACA", "marzo 1958", "I *gangster*\ndi via Osoppo", "secondo le cronache dell'epoca"), (960, 380), tg, anim="drop", rot=-2), "paper")
        sc.add(Text("titolo ricostruito · non originale", (960, 690), tg + 0.4, size=26, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: Il Post · Varesenews · giornale ricostruito"
    elif i == 21:
        tc = T("Circa") - 0.3; td = T("Dentro") - 0.3; tb = T("banditi") - 0.3
        sc.add(Chapter("06", "Le tute nel *fiume*", a, tc))
        sc.add(Calendar((330, 380), 220, [(tc, "CIRCA", "+7 gg")], tc), "paper")
        sc.add(Icon("river", (960, 600), tc + 0.2, size=700), None)
        sc.add(Pill("OLONA · IN SECCA", (960, 800), tc + 0.4, size=40))
        sc.add(Figure(walk([(1900, FY), (1450, FY)], tc + 0.4, 300), tc + 0.4, kind="worker", s=0.8, label="OPERAI"))
        sc.add(Icon("overalls", (860, 520), td, size=230), "pop")
        sc.add(Icon("balaclava", (1100, 520), T("passamontagna") - 0.2, size=200), "pop")
        sc.add(Pill("UN SACCO NEL LETTO DEL FIUME", (960, 250), T("sacco") - 0.3, size=44, accent=True))
        sc.add(Arrow((960, 300), (960, 430), td - 0.6, color=GOLD))
        sc.add(Pill("\"L'ACQUA LE PORTERÀ VIA\"", (1450, 380), T("convinti") - 0.2, size=40))
        sc.footer = "Fonti: Il Post · Geopop · Wikipedia · Il Giornale"
    elif i == 22:
        te = T("E") - 0.3; ts = T("Secondo") - 0.3; tf = T("È") - 0.3
        sc.add(Icon("river", (960, 520), a, te, size=600), None)
        sc.add(Stamp("SVUOTATO", (960, 520), a + 0.4, te, size=90, rot=-8))
        sc.add(Icon("overalls", (600, 520), te, ts, size=360), "pop")
        sc.add(Icon("tag", (1200, 520), T("un'etichetta") - 0.2, ts + 0.3, size=360), "hit")
        sc.add(MapEl((360, 170, 1560, 870), [(ts, (10.0, 45.0), 260), (dur, (10.0, 45.0), 280)], ts,
                     routes=[dict(pts=["Milano", "Modena"], t=T("Modena") - 0.2, d=1.4, color=GOLD, dashed=True)],
                     pins=[dict(at="Milano", label="MILANO", t=ts + 0.2, side="l"), dict(at="Modena", label="MODENA", t=T("Modena") - 0.2, side="r", color=RED)],
                     title="mappa: Natural Earth · schema non in scala"))
        sc.add(Figure([(0, 1500, FY)], T("investigatori") - 0.2, kind="police", s=0.7, carry=[(T("investigatori"), "magnifier")]), "pop")
        sc.add(Pill("IL FILO DELL'INDAGINE", (960, 230), tf, size=46, accent=True))
        sc.footer = "Fonti: Il Post · Milano Città Stato · Wikipedia"
    elif i == 23:
        ta = T("Alcuni") - 0.3; ts = T("Secondo") - 0.3; tp = T("Per") - 0.3
        sc.add(Icon("moneybag", (960, 470), a, ta, size=360), "pop")
        for k in range(3): sc.add(Figure(walk([(-100 - 200 * k, FY), (500 + 260 * k, FY)], ta + 0.2 * k, 400), ta + 0.2 * k, kind="suit", s=0.8))
        sc.add(Icon("sportcar", (1450, 440), T("farsi") - 0.2, size=240), "pop")
        sc.add(Icon("glass", (560, 360), ts, size=170), "pop"); sc.add(Icon("money", (900, 330), ts + 0.3, size=170), "pop")
        sc.add(Pill("SPESE APPARISCENTI", (960, 220), ts + 0.2, size=46, accent=True))
        sc.add(Figure([(0, 1700, FY)], tp - 0.2, kind="police", s=0.8, flip=-1, carry=[(tp, "magnifier")]), "pop")
        sc.add(Stamp("SEGNALE\nCHIARO", (1420, 640), T("segnale") - 0.1, size=60, rot=-6))
        sc.footer = "Fonti: MilanoFree · Il Giornale · Il Post"
    elif i == 24:
        tc = T("Cinque") - 0.3; tu = T("Una") - 0.3; tal = T("Un'altra") - 0.3
        sc.add(Calendar((330, 380), 220, [(a + 0.1, "FINE", "MARZO"), (a + 1.6, "INIZIO", "APRILE")], a, tc + 0.6), "paper")
        sc.add(Pill("LA RETATA · 1958", (960, 230), a + 0.4, tu, size=48, accent=True))
        for k in range(7):
            sc.add(Figure([(0, 330 + k * 210, FY)], a + 0.2 + 0.08 * k, tu, kind="man", s=0.75), None)
            if k < 5: sc.add(Icon("handcuffs", (330 + k * 210, 520), tc + 0.25 * k, tu, size=120), "pop")
        sc.add(Big("5 su 7", (1300, 380), tc + 0.3, tu, size=140, color=WHITE, fnt=OSW))
        for k in range(3): sc.add(Icon("house", (560 + k * 400, 480), tu + 0.15 * k, tal, size=220), "pop" if k == 0 else None)
        for k in range(3): sc.add(Icon("moneybag", (560 + k * 400, 700), T("nascosta") - 0.2 + 0.15 * k, tal, size=150), "pop" if k == 0 else None)
        sc.add(Icon("money", (960, 520), tal, size=300, label="GIÀ SPESA"), "pop")
        sc.footer = "Fonti: Il Post · Milano Città Stato · Il Giornale"
    elif i == 25:
        te = T("Enrico") - 0.3; tv = T("Viene") - 0.3; tea = T("Eros") - 0.3
        sc.add(Pill("MANCANO DUE NOMI", (960, 230), a + 0.1, te, size=50, accent=True))
        sc.add(Img(person_card("ENRICO CESARONI", "latitante", 240, seed=10), (700, 520), a + 0.3, te, anim="drop"), "paper")
        sc.add(Img(person_card("EROS CASTIGLIONI", "latitante", 240, seed=7), (1220, 520), a + 0.5, te, anim="drop"), "paper")
        sc.add(WorldMap((160, 170, 1760, 870), te, tea, view=(-85, 25, -5, 60), hl=("Italy", "Venezuela"),
                        routes=[dict(a=(9.19, 45.46), b=(-66.9, 10.5), t=T("Venezuela") - 0.4, d=1.8, bend=0.2, icon="passport")],
                        pins=[dict(at=(9.19, 45.46), label="MILANO", t=te + 0.2, side="l"), dict(at=(-66.9, 10.5), label="VENEZUELA", t=T("Venezuela") + 1.0, side="r", color=RED)]))
        sc.add(Icon("handcuffs", (1200, 400), tv, tea, size=180, label="ALCUNI MESI DOPO"), "pop")
        sc.add(Figure(walk([(-100, FY), (700, FY)], tea, 380), tea, kind="man", s=0.8, label="CASTIGLIONI"))
        sc.add(Icon("passport", (1100, 520), T("scappa") - 0.2, size=200, label="ALL'ESTERO"), "pop")
        sc.add(Calendar((1500, 470), 240, [(T("latitante") - 0.2, "LATITANTE", "~2"), (T("latitante") + 0.6, "CIRCA", "2 ANNI")], T("latitante") - 0.2), "paper")
        sc.add(Icon("handcuffs", (1100, 300), T("fermato") - 0.3, size=150), "pop")
        sc.footer = "Fonti: Il Post · Il Giornale · mappa: Natural Earth"
    elif i == 26:
        tc = T("La") - 0.3; tco = T("Le") - 0.3
        sc.add(Chapter("07", "Il processo e il *mito*", a, tc))
        sc.add(Calendar((960, 300), 200, [(tc, "NOVEMBRE", "1958")], tc, tco), "paper")
        sc.add(Icon("gavel", (960, 520), tc + 0.3, tco, size=220), "stamp")
        sc.add(Pill("POCHI MESI DOPO IL COLPO", (960, 650), T("pochi") - 0.1, tco, size=44, accent=True))
        sc.add(Bar(360, 440, 1200, 70, [(T("9") , 0.0), (T("9") + 0.6, 0.47)], T("9") - 0.2, color=GOLD))
        sc.add(Text("F. RUSSO · 9 ANNI E 8 MESI", (360, 380), T("9") - 0.2, size=40, fnt=OSW, color=WHITE))
        sc.add(Bar(360, 660, 1200, 70, [(T("20") , 0.0), (T("20") + 0.8, 1.0)], T("20") - 0.2, color=RED))
        sc.add(Text("L. DE MARIA · 20 ANNI E 8 MESI", (360, 600), T("20") - 0.2, size=40, fnt=OSW, color=WHITE))
        sc.add(Text("dalla pena più bassa alla più alta", (960, 240), tco + 0.3, size=34, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: Il Post · Varesenews · Il Giornale"
    elif i == 27:
        tg = T("Gli") - 0.3; ti = T("Il") - 0.3
        sc.add(Icon("scales", (960, 470), a, tg, size=360), "pop")
        sc.add(Stamp("ZERO\nFERITI", (600, 400), a + 0.4, tg, size=60, rot=-8, color=(60, 150, 80)))
        sc.add(Img(sentence_card([("F. Russo", "9 a 8 m"), ("altri cinque", "tra 11 e 18 a"), ("L. De Maria", "20 a 8 m")], 700), (960, 500), tg, ti + 0.4, anim="drop", rot=-2), "paper")
        sc.add(Icon("prison", (960, 470), ti + 0.2, size=360), "pop")
        sc.add(Stamp("FINE DEL\nCOLPO PERFETTO", (1350, 360), T("tribunale") - 0.3, size=60, rot=-8))
        sc.footer = "Fonti: Il Post · Varesenews · Il Giornale"
    elif i == 28:
        te = T("Entra") - 0.3; ti = T("Ispira") - 0.3; tn = T("Negli") - 0.3
        sc.add(Crowd((300, 560, 1620, 880), 16, a + 0.2, ti, s=0.4))
        sc.add(Pill("CULTURA POPOLARE", (960, 300), te, ti, size=50, accent=True))
        sc.add(Icon("clapper", (620, 470), ti, tn, size=300), "pop")
        sc.add(Img(doc_typed(560, 300, "AL CINEMA", ["*L'audace colpo*", "*dei soliti ignoti*", "storia di fantasia"], seed=12, size=36), (1240, 470), T("L'audace") - 0.2, tn, anim="drop", rot=2), "paper")
        sc.add(Pill("LA VECCHIA MALA MILANESE", (960, 760), T("simbolo") - 0.2, tn, size=44))
        sc.add(Bubble((960, 300), 100, T("quella") - 0.2, tn, text="\"NON SPARAVA\""), "pop")
        for k in range(3): sc.add(Icon("book", (620 + k * 340, 520), tn + 0.2 * k, size=230), "pop" if k == 0 else None)
        sc.add(Pill("MEMORIE DEI PROTAGONISTI", (960, 760), tn + 0.6, size=44, accent=True))
        sc.footer = "Fonti: Varesenews · Il Post · Milano Città Stato"
    elif i == 29:
        ts = T("Sette") - 0.3
        sc.add(Chapter("", "Il *verdetto*", a, ts))
        items = [("overalls", "7 IN TUTA", ts), ("payenv", "GIORNO DI PAGA", T("Un")), ("van", "POCHI MINUTI", T("Pochi")),
                 ("moneybag", "100+ MILIONI", T("e", 1)), ("river", "L'ERRORE", T("un", 1))]
        for k, (ic, lab, tt) in enumerate(items):
            sc.add(Icon(ic, (290 + k * 335, 470), tt - 0.2, size=220, label=lab), "pop")
        sc.add(Stamp("UN SOLO\nERRORE", (960, 760), T("solo") - 0.1, size=64, rot=-6))
        sc.footer = "Ricostruzione divulgativa · fonti nella descrizione"
    elif i == 30:
        ts = T("Iscriviti") - 0.3
        sc.add(Crossing(XB, a, T("Scrivilo") - 0.2, dim=0.35, cars=[dict(kind="van", keys=[(a, .40, .63, 0)])]))
        sc.add(Pill("PERCHÉ MILANO HA SIMPATIZZATO?", (960, 330), a + 0.3, T("Scrivilo") - 0.2, size=52, accent=True))
        sc.add(Bubble((960, 470), 170, T("Scrivilo") - 0.1, ts, text="COMMENTI"), "pop")
        sc.add(Text("Fonti nella descrizione", (960, 760), T("fonti") - 0.2, ts, size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(110), (960, 520), ts, anim="pop", shadow=False), "hit")
        sc.add(Text("ogni giorno un nuovo caso", (960, 700), T("ogni") - 0.2, size=54, fnt=PS, color=GOLD, anchor="ma"))
        sc.footer = "Ricostruzione divulgativa · voce generata con sintesi vocale"
    return sc


def thumbnail(path="thumbnail.jpg"):
    im = make_bg(7).convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    Crossing((1000, 140, 1860, 940), -5, None, label=None,
             cars=[dict(kind="van", keys=[(0, .38, .63, 0)], L=.24), dict(kind="truck", keys=[(0, .62, .64, 172)], L=.24), dict(kind="fiat", keys=[(0, .80, .80, 40)], L=.22)],
             marks=[dict(t=0, x=.50, y=.60, text="BAM!", d=99)]).draw(lay, 1.0, 1.0)
    im.alpha_composite(lay)
    ic = fx.icon("overalls", 230); im.alpha_composite(ic, (1080, 180))
    ic = fx.icon("moneybag", 200); im.alpha_composite(ic, (1600, 170))
    t = rich_img("7 UOMINI\nIN *TUTA BLU*", SERIF, 140, WHITE, RED, lh=1.0)
    im.alpha_composite(t, (90, 190))
    st = stamp_img("CASO 007", RED, 64, -10); im.alpha_composite(st, (620, 50))
    st2 = stamp_img("MILANO 1958", (200, 160, 60), 54, 6); im.alpha_composite(st2, (110, 560))
    d = ImageDraw.Draw(im)
    d.text((100, 770), "114 MILIONI DI LIRE IN POCHI MINUTI", font=font(OSW, 56, 600), fill=GOLD + (255,))
    d.text((100, 845), "SENZA SPARARE UN COLPO", font=font(OSW, 56, 600), fill=GOLD + (255,))
    wm = wordmark(60, sub=False); im.alpha_composite(wm, (100, 960))
    im.convert("RGB").save(path, quality=92)
