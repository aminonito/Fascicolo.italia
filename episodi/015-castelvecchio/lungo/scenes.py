import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from cv import *

W, H = 1920, 1080
FY = 870
GB = (260, 170, 1660, 870)      # scenografia: la galleria con i 17 quadri
CB = (260, 170, 1660, 870)      # il castello visto da fuori
MAPB = (160, 160, 1760, 880)
GL = (180, 170, 1080, 860)      # galleria ridotta a sinistra
MT = "mappa: Natural Earth · schema non in scala"
F_MUS = "Fonti: Il Post · Finestre sull'Arte · MuseiOnline · sagome stilizzate"
F_SERA = "Fonti: Il Post · The Art Newspaper · AP · Finestre sull'Arte"
F_IND = "Fonti: Il Post · ANSA · The Art Newspaper · L'Adige · Kyiv Post · AP"
F_ARR = "Fonti: The Art Newspaper · L'Adige · Il Post · ANSA"
F_ISO = "Fonti: The Art Newspaper · Kyiv Post · AP · UNIAN"
F_RIT = "Fonti: AP · artnet · ANSA"
GY = 170 + int(700 * .88)       # suolo del castello

def build(i, dur, a, words):
    T0 = Clock(words, a)
    def T(p, n=0):
        cs = lambda s: re.sub(r"[^\w']", "", s.lower())
        hits = [w for w in words if cs(w[0]) == cs(p)]
        if hits: return a + hits[min(n, len(hits) - 1)][1]
        try: return T0(p, n)
        except KeyError: return a + 0.5
    sc = Scene(dur)
    E = a + dur
    if i == 0:
        td = T("Diciannove") - 0.3; ts = T("È") - 0.3; ti = T("In") - 0.3; tl = T("L'allarme") - 0.3
        sc.add(MapEl(MAPB, [(a, (12.5, 43.0), 120), (td, "Verona", 420)], a, ti + 0.3,
                     pins=[dict(at="Verona", label="VERONA", t=a + 0.5, side="r", color=RED)], title=MT))
        sc.add(Calendar((420, 420), 220, [(td, "NOVEMBRE", "19"), (td + 1.2, "2015", "19")], td, ti), "paper")
        sc.add(Icon("moon", (1500, 330), ts, ti, size=160), "pop")
        sc.add(Castello(CB, ti, None, night=True), "whoosh")
        sc.add(Pill("UN MUSEO IN UN CASTELLO", (960, 215), ti + 0.3, tl, size=46, accent=True))
        sc.add(Figure([(ti + 0.5, 790, GY), (tl, 300, GY)], ti + 0.5, tl, kind="man", s=0.5))
        sc.add(Figure([(ti + 0.9, 800, GY), (tl + 0.5, 240, GY)], ti + 0.9, tl + 0.5, kind="suit", s=0.5))
        sc.add(Icon("alarm_off", (1100, 470), tl, size=260), "hit")
        sc.add(Pill("ALLARME NOTTURNO NON ANCORA ACCESO", (960, 215), tl + 0.2, size=46, accent=True))
        scene_cam(sc, (ti, 960, 540, 1.0), (tl, 960, 540, 1.0), (tl + 1.0, 1100, 470, 1.25))
        sc.footer = F_SERA + " · " + MT
    elif i == 1:
        tt = T("Tintoretto") - 0.2; tv = T("Valore") - 0.3; ts = T("Sei") - 0.3; tsu = T("su") - 0.3
        sc.add(Galleria(GB, a, tv, gone=a + 0.6, step=0.09, night=True, torch=a))
        sc.add(Big("17", (1500, 330), a + 0.4, tt, size=200, color=RED))
        for k, (nm, w_) in enumerate([("TINTORETTO", "Tintoretto"), ("MANTEGNA", "Mantegna"), ("PISANELLO", "Pisanello"), ("RUBENS", "Rubens")]):
            sc.add(Pill(nm, (960, 260 + k * 110), T(w_) - 0.15, tv, size=56, accent=(k % 2 == 0)))
        sc.add(Text("circa\n*15 milioni*\ndi euro", (560, 330), tv, ts, size=100, anchor="ma", align="m"))
        sc.add(Icon("euro", (1340, 520), tv + 0.3, ts, size=360), "hit")
        sc.add(Text("valore stimato dal museo", (560, 760), tv + 0.5, ts, size=30, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(MapEl(MAPB, [(ts, (20.0, 46.0), 52), (tsu + 1.0, (27.0, 46.5), 110)], ts, None,
                     pins=[dict(at="Verona", label="VERONA", t=ts + 0.2, side="l", color=GOLD),
                           dict(at="Turunchuk", label="UCRAINA", t=tsu, side="r", color=RED)],
                     routes=[dict(pts=["Verona", "Turunchuk"], t=ts + 0.3, d=2.0, icon="painting", color=RED)], title=MT))
        sc.add(Pill("QUASI 1.500 KM · IN LINEA D'ARIA", (960, 215), ts + 0.6, size=44, accent=True))
        sc.add(Icon("island", (1500, 700), tsu + 0.3, size=200), "pop")
        sc.footer = "Fonti: Il Post · ANSA · The Art Newspaper · AP · calcolo nostro (Python) · " + MT
    elif i == 2:
        sc.add(Img(cover_folder(560), (540, 520), a, anim="drop", rot=-3), "paper")
        items = [("IL CASTELLO", "castello"), ("LA SERA DEL COLPO", "sera"), ("LE PRIME ORE", "prime"),
                 ("LA PISTA MOLDAVA", "pista"), ("L'ISOLA SUL DNESTR", "l'isola"), ("IL RITORNO", "viaggio")]
        for k, (lab, w_) in enumerate(items):
            sc.add(Pill(lab, (1340, 250 + k * 100), T(w_) - 0.2, size=44, accent=(k % 2 == 1)))
        sc.footer = "Ricostruzione a scopo divulgativo · fascicolo ricostruito"
    elif i == 3:
        tc = T("Castelvecchio") - 0.3; tco = T("La") - 0.3; th = T("Ha") - 0.3; tp = T("e", 1) - 0.2
        sc.add(Text("Partiamo\ndal *luogo*", (960, 330), a, tc, size=110, anchor="ma", align="m"))
        sc.add(Castello(CB, tc, None, night=False), "whoosh")
        sc.add(Pill("CASTELVECCHIO · VERONA", (960, 215), tc + 0.2, tco, size=48, accent=True))
        sc.add(Icon("river", (1520, 790), tc + 0.4, size=150, label="ADIGE"), "pop")
        sc.add(Pill("TRECENTO · GLI SCALIGERI", (960, 215), tco, th, size=48, accent=True))
        sc.add(Icon("crown", (520, 300), tco + 0.3, th, size=160), "pop")
        sc.add(Pill("MURA MERLATE · TORRI · PONTE", (960, 215), th, size=48, accent=True))
        scene_cam(sc, (th, 960, 540, 1.0), (th + 1.2, 1180, 300, 1.6), (tp, 1180, 300, 1.6), (tp + 1.2, 960, 540, 1.0))
        sc.footer = "Fonti: MuseiOnline · Italia.it · schema non in scala"
    elif i == 4:
        ts = T("Il") - 0.3; tc = T("Carlo") - 0.2; tn = T("Nelle") - 0.3; tsp = T("e", 1) - 0.2
        sc.add(Castello((260, 300, 1660, 870), a, ts, night=False))
        sc.add(Icon("museum", (960, 230), a + 0.3, ts, size=150), "pop")
        sc.add(Text("Il *museo civico*", (960, 200), ts, tn, size=84, anchor="ma", align="m"))
        sc.add(Galleria((900, 300, 1700, 800), ts + 0.2, tn, label=""))
        sc.add(Icon("studio", (600, 560), ts + 0.2, tc, size=300) if False else Icon("easel", (600, 560), ts + 0.2, tn, size=300), "pop")
        sc.add(Img(label_card(["Carlo Scarpa", "architetto", "(1906-1978)"], 520, title="L'ALLESTIMENTO") if False else label_card(["Carlo Scarpa", "architetto del Novecento"], 520, title="L'ALLESTIMENTO"), (1300, 560), tc, tn, anim="drop", rot=2), "paper")
        sc.add(Icon("head", (420, 520), T("sculture") - 0.1, size=200, label="SCULTURE"), "pop")
        sc.add(Icon("crown", (960, 520), T("armi") - 0.1, size=200, label="ARMI ANTICHE"), "pop")
        sc.add(Icon("easel", (1500, 520), tsp, size=200, label="PITTURA"), "hit")
        sc.add(Pill("DAL MEDIOEVO AL SETTECENTO", (960, 800), T("dal") - 0.2, size=46, accent=True))
        sc.footer = "Fonti: MuseiOnline · Italia.it · sagome stilizzate"
    elif i == 5:
        tm = T("La") - 0.3
        sc.add(Text("Quattro opere\nda *ricordare*", (960, 330), a, tm, size=100, anchor="ma", align="m"))
        names = [("Madonna della quaglia", "attrib. Pisanello", "Madonna"), ("Sacra Famiglia", "Andrea Mantegna", "Sacra"),
                 ("San Girolamo penitente", "Jacopo Bellini", "San"), ("Ritratto", "G. F. Caroto", "ritratto")]
        for k, (t1_, t2_, w_) in enumerate(names):
            x = 330 + k * 420; tk = T(w_) - 0.3
            sc.add(Img(pic(k * 3 + (1 if k == 3 else 0), 250, 320), (x, 470), tk, anim="drop"), "paper")
            sc.add(Text(t1_, (x, 680), tk + 0.2, size=34, fnt=OSW, color=WHITE, anchor="ma"))
            sc.add(Text(t2_, (x, 730), tk + 0.3, size=30, fnt=PS, color=GOLD, anchor="ma"))
        sc.add(Text("sagome stilizzate, non le opere", (960, 800), tm + 0.4, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: Il Post · Finestre sull'Arte · ANSA · sagome stilizzate"
    elif i == 6:
        to = T("Opere") - 0.3
        sc.add(Galleria(GB, a, to, hl=None))
        sc.add(Pill("JACOPO TINTORETTO", (960, 215), T("diverse") - 0.2, T("un") - 0.3, size=48, accent=True))
        sc.add(Pill("PIETER PAUL RUBENS", (960, 215), T("un") - 0.3, T("e") - 0.3, size=48, accent=True))
        sc.add(Pill("RITRATTI E PAESAGGI", (960, 215), T("e") - 0.3, to, size=48))
        sc.add(Text("Famose in\ntutto il *mondo*", (560, 330), to, size=90, anchor="ma", align="m"))
        sc.add(Icon("globe2", (560, 700), to + 0.3, size=200), "pop")
        sc.add(Icon("frame_empty", (1350, 480), T("impossibili") - 0.3, size=320), "hit")
        sc.add(Stamp("INVENDIBILI", (1350, 720), T("impossibili") + 0.2, size=80, rot=-8))
        sc.footer = "Fonti: Finestre sull'Arte · Il Post · ANSA · sagome stilizzate"
    elif i == 7:
        ta = T("Al") - 0.3; ti = T("Il") - 0.3; tr = T("Rimangono") - 0.3; tg = T("e", 0) - 0.2
        sc.add(Calendar((960, 470), 300, [(a, "GIOVEDÌ", "19"), (a + 1.0, "NOV 2015", "19")], a, ta), "paper")
        sc.add(Castello(CB, ta, None, night=True, door_t=ta), "whoosh")
        sc.add(ClockFace((1500, 330), 110, ta + 0.2, tr, start=7.35, speed=0.02))
        sc.add(Pill("ORARIO DI CHIUSURA", (960, 215), ta + 0.2, tr, size=48, accent=True))
        for k in range(4):
            sc.add(Figure([(ti + k * 0.4, 820, GY), (ti + k * 0.4 + 2.5, 200, GY)], ti + k * 0.4, ti + k * 0.4 + 2.6, kind=("man", "suit", "expert", "man")[k], s=0.5))
        sc.add(Figure([(tr, 700, GY)], tr, None, kind="man", s=0.55, label="CASSIERA"))
        sc.add(Figure([(tg, 1000, GY)], tg, None, kind="guard", s=0.55, label="GUARDIA GIURATA"))
        sc.add(Pill("UNICA VIGILANZA NOTTURNA", (960, 215), T("l'unica") - 0.2, size=48, accent=True))
        sc.footer = F_SERA
    elif i == 8:
        tl = T("L'allarme") - 0.3; ti = T("In") - 0.3; tm = T("ma", 0) - 0.2
        sc.add(Text("Un dettaglio\n*decisivo*", (960, 330), a, tl, size=110, anchor="ma", align="m"))
        sc.add(Icon("alarm_off", (560, 520), tl, size=320), "hit")
        sc.add(ClockFace((1340, 520), 170, tl + 0.3, start=7.4, speed=0.03, label="SOLO DOPO LA CHIUSURA"))
        sc.add(Door((960, 560), 300, 520, ti, None, open_t=ti + 0.2) if False else Pill("APERTO", (560, 760), ti + 0.2, size=60))
        sc.add(Pill("MA NON PROTETTO", (960, 215), tm, size=56, accent=True))
        sc.footer = "Fonti: Il Post · The Art Newspaper · AP"
    elif i == 9:
        tv = T("Verso") - 0.3; th = T("Hanno") - 0.3; tb = T("Bloccano") - 0.3; ta = T("Adesso") - 0.3
        sc.add(ClockFace((960, 480), 220, a, tv + 1.2, start=7.45, speed=0.02, label="19:30 CIRCA"))
        sc.add(Castello(CB, tv + 0.6, None, night=True, door_t=tv + 0.6))
        for k in range(3):
            sc.add(Figure([(tv + 0.8, 1640 - k * 80, GY), (th + 0.6, 900 - k * 60, GY)], tv + 0.8, tb + 0.2, kind="man", s=0.55))
        sc.add(Pill("TRE UOMINI", (960, 215), tv + 0.8, th, size=50, accent=True))
        sc.add(Icon("balaclava", (1450, 420), th, tb, size=220), "pop")
        sc.add(Pill("VOLTO COPERTO · ARMATI", (960, 215), th, tb, size=50, accent=True))
        sc.add(Figure([(tb, 700, GY)], tb, None, kind="man", s=0.55, label="CASSIERA"))
        sc.add(Figure([(tb, 1000, GY)], tb, None, kind="guard", s=0.55, label="GUARDIA"))
        sc.add(Icon("tape", (850, 420), tb + 0.3, size=220), "hit")
        sc.add(Pill("BLOCCATI", (960, 215), tb + 0.2, size=50, accent=True))
        sc.footer = F_SERA + " · sagome stilizzate"
    elif i == 10:
        tn = T("Non") - 0.3; ta = T("Alcune") - 0.3; tf = T("Alla") - 0.3
        sc.add(Galleria(GB, a, None, gone=tf, step=0.1, night=True, torch=a))
        sc.add(Pill("DI SALA IN SALA", (960, 215), a + 0.3, tn, size=48, accent=True))
        sc.add(Pill("SOLO ALCUNE OPERE", (960, 215), tn, ta, size=48, accent=True))
        sc.add(Icon("cutter", (560, 520), ta, tf, size=240), "pop")
        sc.add(Icon("roll", (1360, 520), T("arrotolate") - 0.2, tf, size=260), "pop")
        sc.add(Big("17", (960, 520), tf + 1.2, size=260, color=RED))
        sc.add(Pill("DIPINTI SPARITI", (960, 215), tf + 1.2, size=50, accent=True))
        sc.footer = "Fonti: Il Post · Finestre sull'Arte · The Art Newspaper · sagome stilizzate"
    elif i == 11:
        tu = T("usano") - 0.3; tc = T("Caricano") - 0.3; td = T("Dei") - 0.3
        sc.add(Castello(CB, a, td + 0.3, night=True, door_t=a))
        sc.add(Icon("car", (900, 760), tu, td + 0.3, size=280, move=(T("spariscono"), 1.6, (2100, 760), 0)), "whoosh")
        sc.add(Pill("L'AUTO DELLA GUARDIA GIURATA", (960, 215), tu, tc, size=48, accent=True))
        for k in range(3):
            sc.add(Icon("roll", (560 + k * 70, 780), tc + 0.2 + k * 0.25, T("spariscono"), size=110), "pop")
        sc.add(Text("Nessuna\n*traccia*", (960, 330), td, size=120, anchor="ma", align="m"))
        sc.add(Icon("question", (960, 700), td + 0.4, size=200), "pop")
        sc.footer = "Fonti: Il Post · The Art Newspaper · AP · schema non in scala"
    elif i == 12:
        tl = T("La", 1) - 0.3; tc = T("circa") - 0.3; ta = T("Altre") - 0.3; tp = T("Per") - 0.3
        sc.add(Img(newspaper(640, 480, "CRONACA", "20 novembre 2015", "RUBATI 17 QUADRI A VERONA", "Colpo al Museo di Castelvecchio"), (960, 500), a, tc, anim="drop", rot=-3), "paper")
        sc.add(Text("giornale ricostruito · testata generica", (960, 790), a + 0.3, tc, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Big("15", (620, 470), tc, tp, size=240, color=RED, sub="MILIONI DI EURO · STIMA DEL MUSEO"))
        sc.add(Big("16-17", (1360, 470), ta, tp, size=180, color=GOLD, sub="ALTRE STIME"))
        sc.add(Text("stime non concordi tra le fonti", (960, 800), ta + 0.3, tp, size=26, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Text("Uno dei furti d'arte\npiù *gravi* da decenni", (960, 260), tp, size=90, anchor="ma", align="m"))
        for k in range(3): sc.add(Icon("frame_empty", (600 + k * 360, 640), tp + 0.4 + k * 0.3, size=220), "pop")
        sc.footer = F_IND
    elif i == 13:
        tq = T("fanno") - 0.3; tm = T("Ma") - 0.3
        sc.add(Text("Facciamo\nun *calcolo*", (960, 330), a, T("Quindici") - 0.3, size=110, anchor="ma", align="m"))
        sc.add(Img(label_card(["15.000.000 € ÷ 17 quadri", "≈ 880.000 € a quadro", "(media, solo indicativa)"], 640, title="IL CALCOLO"), (960, 480), T("Quindici") - 0.3, tm, anim="drop", rot=-2), "paper")
        sc.add(Text("calcolo nostro sulla stima del museo (Python)", (960, 800), tq, tm, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Text("Il valore vero?\nOpere *uniche*", (960, 200), tm, size=80, anchor="ma", align="m"))
        sc.add(Icon("folder", (460, 580), T("schedate") - 0.2, size=220, label="SCHEDATE"), "pop")
        sc.add(Icon("camera", (960, 580), T("fotografate") - 0.2, size=220, label="FOTOGRAFATE"), "pop")
        sc.add(Icon("magnifier", (1460, 580), T("conosciute") - 0.2, size=220, label="CONOSCIUTE"), "pop")
        sc.footer = "Fonti: Il Post · ANSA · calcolo nostro"
    elif i == 14:
        tu = T("Un") - 0.3; tp = T("Per") - 0.3
        sc.add(Text("Il *paradosso*\ndei furti d'arte", (960, 330), a, tu, size=100, anchor="ma", align="m"))
        sc.add(Icon("gavel", (560, 500), tu, tp, size=300, label="ASTA"), "pop")
        sc.add(Icon("suit", (1360, 500), T("né") - 0.2, tp, size=300, label="COLLEZIONISTA") if False else Figure([(T("né") - 0.2, 1360, 700)], T("né") - 0.2, tp, kind="suit", s=0.9, label="COLLEZIONISTA ONESTO"))
        sc.add(Stamp("NO", (560, 500), tu + 1.2, tp, size=120, rot=-10))
        sc.add(Stamp("NO", (1360, 450), T("onesto"), tp, size=120, rot=-10))
        sc.add(Icon("sack", (960, 520), tp, size=360), "hit")
        sc.add(Pill("UN PESO DA NASCONDERE", (960, 215), tp + 0.3, size=50, accent=True))
        sc.footer = "Ricostruzione a scopo divulgativo"
    elif i == 15:
        tl = T("Le", 1) - 0.3; tg = T("Il") - 0.3
        sc.add(Text("Le *indagini*", (960, 330), a, tl, size=120, anchor="ma", align="m"))
        sc.add(Icon("court", (420, 480), T("Procura") - 0.2, tg, size=240, label="PROCURA DI VERONA"), "pop")
        sc.add(Figure([(T("Squadra") - 0.2, 960, 660)], T("Squadra") - 0.2, tg, kind="police", s=0.8, label="SQUADRA MOBILE"))
        sc.add(Icon("easel", (1500, 480), T("Carabinieri") - 0.2, tg, size=240, label="CARABINIERI TUTELA PATRIMONIO"), "pop")
        sc.add(Galleria(GL, tg, None, night=True))
        sc.add(Icon("magnifier", (1420, 480), tg + 0.3, size=300), "pop")
        sc.add(Text("Un aiuto\n*dall'interno?*", (1420, 700), T("Gli") - 0.2, size=60, anchor="ma", align="m"))
        sc.footer = "Fonti: L'Adige · The Art Newspaper · artnet · AP"
    elif i == 16:
        ti = T("Il") - 0.3; tt = T("tredici") - 0.3; tp = T("Polizia") - 0.3
        sc.add(Calendar((960, 470), 300, [(a, "NOV 2015", "19"), (a + 0.6, "GEN 2016", "1"), (a + 1.2, "MARZO 2016", "15")], a, tt), "paper")
        sc.add(Text("4 mesi dopo", (960, 760), a + 0.4, tt, size=50, fnt=OSW, color=GOLD, anchor="ma"))
        sc.add(MapEl(MAPB, [(tt, (20.0, 46.3), 58)], tt, None,
                     pins=[dict(at="Verona", label="VERONA", t=tt + 0.2, side="l", color=RED),
                           dict(at="Chisinau", label="MOLDAVIA", t=tt + 0.6, side="r", color=RED)],
                     routes=[dict(pts=["Verona", "Chisinau"], t=tt + 0.3, d=1.2, color=GOLD, dashed=True)], title=MT))
        sc.add(Big("13", (960, 340), tt + 0.2, size=200, color=RED, sub="ARRESTI"))
        sc.add(Icon("handcuffs", (960, 680), tt + 0.6, size=200), "hit")
        sc.footer = F_ARR + " · " + MT
    elif i == 17:
        tf = T("C'è") - 0.3; td = T("E", 0) - 0.3
        nodes = {"g": dict(xy=(480, 480), name="LA GUARDIA GIURATA", role="in servizio", t=a + 0.3, rot=-3),
                 "f": dict(xy=(960, 480), name="IL FRATELLO GEMELLO", role="arrestato", t=tf, rot=2),
                 "d": dict(xy=(1440, 480), name="UNA DONNA MOLDAVA", role="tramite (accusa)", t=td, rot=-2)}
        sc.add(Board(nodes, [("g", "f", tf + 0.3), ("f", "d", td + 0.4)], a, cw=300))
        sc.add(Text("schede ricostruite · nessuna foto · nessun nome", (960, 230), a + 0.4, size=26, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Stamp("ARRESTATI", (960, 790), T("faceva"), size=70, rot=-6))
        sc.footer = F_ARR
    elif i == 18:
        tv = T("A") - 0.3; tm = T("In", 0) - 0.3; tme = T("In", 1) - 0.3
        sc.add(Pill("LO SCHEMA SECONDO L'ACCUSA", (960, 215), a, size=48, accent=True))
        sc.add(Img(label_card(["VERONA", "chi conosceva il museo", "e i suoi orari"], 520, title="SECONDO L'ACCUSA"), (480, 500), tv, anim="drop", rot=-2), "paper")
        sc.add(Icon("museum", (480, 760), tv + 0.4, size=120), "pop")
        sc.add(Img(label_card(["MOLDAVIA", "chi avrebbe eseguito", "il colpo"], 520, title="SECONDO L'ACCUSA"), (1440, 500), tm, anim="drop", rot=2), "paper")
        sc.add(Icon("balaclava", (1440, 760), tm + 0.4, size=120), "pop")
        sc.add(Arrow((760, 500), (1180, 500), tme, color=GOLD, width=8, dashed=True))
        sc.add(Arrow((1180, 560), (760, 560), tme + 0.4, color=GOLD, width=8, dashed=True))
        sc.add(Icon("phone", (960, 420), tme + 0.2, size=120), "pop")
        sc.add(Text("schema semplificato", (960, 830), a + 0.3, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: L'Adige · The Art Newspaper · schema semplificato"
    elif i == 19:
        tg = T("Gli") - 0.3; ti = T("Il") - 0.3; tit = T("che") - 0.3
        sc.add(Text("E i *quadri?*", (960, 330), a, tg, size=120, anchor="ma", align="m"))
        sc.add(Galleria((560, 470, 1360, 870), a, tg, gone=a, step=0, label=""))
        sc.add(MapEl(MAPB, [(tg, (20.0, 46.5), 52)], tg, None,
                     pins=[dict(at="Roma", label="ITALIA", t=T("italiana") - 0.2, side="r", color=GOLD),
                           dict(at="Chisinau", label="MOLDAVIA", t=T("moldava") - 0.2, side="t", color=RED),
                           dict(at="Kyiv", label="UCRAINA", t=T("ucraina") - 0.2, side="r", color=GOLD)], title=MT))
        sc.add(Icon("question", (330, 360), tg + 0.4, size=180), "pop")
        sc.add(Pill("CACCIA INTERNAZIONALE", (960, 215), ti, size=48, accent=True))
        sc.footer = F_ARR + " · " + MT
    elif i == 20:
        tt = T("Tra") - 0.3; tv = T("Vicino") - 0.3; ts = T("Si") - 0.3
        sc.add(Text("Guardiamo\nla *mappa*", (960, 330), a, tt, size=110, anchor="ma", align="m"))
        sc.add(MapEl(MAPB, [(tt, (27.0, 47.0), 120), (tv, "Turunchuk", 420)], tt, None,
                     pins=[dict(at="Chisinau", label="MOLDAVIA", t=tt + 0.3, side="l", color=GOLD),
                           dict(at="Odessa", label="ODESSA · UCRAINA", t=tv + 0.3, side="r", color=GOLD),
                           dict(at="Turunchuk", label="TURUNCHUK", t=ts, side="b", color=RED)], title=MT))
        sc.add(Pill("IL FIUME DNESTR", (960, 215), T("il", 0) + 0.3, ts, size=48, accent=True))
        sc.add(Icon("river", (1560, 330), tt + 0.6, ts, size=170), "pop")
        sc.add(Icon("island", (1560, 330), ts, size=200), "pop")
        sc.footer = "Fonti: Kyiv Post · UNIAN · The Art Newspaper · " + MT
    elif i == 21:
        tf = T("fermano") - 0.3; ts = T("Su") - 0.3; td = T("Dentro") - 0.3
        sc.add(Calendar((420, 420), 220, [(a, "MAGGIO", "2016")], a, ts), "paper")
        for k in range(2):
            sc.add(Figure([(a + 0.4, 1700 - k * 90, FY), (tf + 1.0, 1250 - k * 90, FY)], a + 0.4, None, kind="police", s=0.6, label="GUARDIE DI FRONTIERA" if k == 0 else None))
        sc.add(Pill("CONTRABBANDO VERSO LA MOLDAVIA", (960, 215), tf, ts, size=46, accent=True))
        sc.add(Icon("island", (760, 520), ts, size=420), "pop")
        for k in range(3):
            sc.add(Icon("trashbag", (560 + k * 150, 790), T("sacchi") - 0.1 + k * 0.2, size=170), "pop")
        sc.add(Big("17", (960, 330), td + 0.3, size=180, color=RED, sub="DIPINTI"))
        sc.footer = F_ISO
    elif i == 22:
        ts = T("Sono") - 0.3; tt = T("Tutti") - 0.3; td = T("Dal") - 0.3; te = T("linea") - 1.2
        sc.add(Calendar((420, 420), 220, [(a, "MAGGIO 2016", "11")], a, ts), "paper")
        sc.add(Img(stamp_img("UFFICIALE", RED, 80, -8), (1300, 420), a + 0.4, ts, anim="pop", shadow=False), "stamp")
        sc.add(Galleria(GB, ts, td, gone=ts - 5, back=tt, step=0.08, label="sagome stilizzate"))
        sc.add(Pill("TUTTI E 17", (960, 215), tt, td, size=56, accent=True))
        sc.add(Text("quasi *6 mesi*\ndopo il furto", (960, 330), td, te, size=100, anchor="ma", align="m"))
        sc.add(MapEl(MAPB, [(te, (20.0, 46.0), 52)], te, None,
                     pins=[dict(at="Verona", label="VERONA", t=te + 0.2, side="l", color=GOLD),
                           dict(at="Turunchuk", label="L'ISOLA", t=te + 0.4, side="r", color=RED)],
                     routes=[dict(pts=["Verona", "Turunchuk"], t=te + 0.3, d=1.4, color=RED, dashed=True)], title=MT))
        sc.add(Pill("≈ 1.470 KM IN LINEA D'ARIA", (960, 215), te + 0.8, size=48, accent=True))
        sc.add(Text("calcolo nostro con le coordinate (Python)", (1400, 846), te + 1.0, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: The Art Newspaper · Kyiv Post · calcolo nostro · " + MT
    elif i == 23:
        tl = T("Le") - 0.3; td = T("Durante") - 0.3; tm = T("Ma") - 0.3
        sc.add(Text("Come stanno\nle *opere?*", (960, 330), a, tl, size=110, anchor="ma", align="m"))
        sc.add(Icon("frame_empty", (560, 500), tl, size=320, label="CORNICI ORIGINALI"), "pop")
        sc.add(Icon("cutter", (1360, 500), tl + 0.6, size=280), "hit")
        sc.add(Img(pic(4, 420, 330), (960, 500), td, anim="drop"), "paper")
        sc.add(Icon("magnifier", (1200, 560), td + 0.5, size=220), "pop")
        sc.add(Pill("GRAFFI", (960, 215), td + 0.3, tm, size=50, accent=True))
        sc.add(Stamp("NIENTE DI GRAVE", (960, 760), tm + 0.4, size=70, rot=-6))
        sc.add(Text("secondo il museo", (960, 860), tm + 0.6, size=26, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: AP · artnet · sagoma stilizzata"
    elif i == 24:
        tp = T("Poi") - 0.3; ti = T("Il") - 0.3
        sc.add(Figure([(a + 0.2, 560, FY)], a + 0.2, tp, kind="expert", s=0.9, label="ESPERTI ITALIANI"))
        sc.add(Img(pic(1, 380, 300), (1200, 470), a + 0.3, tp, anim="drop"), "paper")
        sc.add(Icon("magnifier", (1250, 500), a + 0.8, tp, size=200), "pop")
        sc.add(Img(doc_typed(560, 420, "VERBALE DI CONSEGNA", ["Italia - Ucraina", "17 dipinti", "procedure tra Stati"]), (960, 500), tp, ti, anim="drop", rot=-2), "paper")
        sc.add(Calendar((960, 500), 300, [(ti, "MAGGIO 2016", "·"), (ti + 0.8, "AGOSTO 2016", "·"), (ti + 1.6, "DICEMBRE 2016", "·")], ti, None), "paper")
        sc.add(Pill("ANCORA IN UCRAINA", (960, 215), ti + 0.3, size=50, accent=True))
        sc.footer = "Fonti: Kyiv Post · ANSA · AP · documento: ricostruzione grafica"
    elif i == 25:
        tc = T("c'è") - 0.3; tp = T("presidente") - 0.3; te = T("Entrambi") - 0.3
        sc.add(MapEl(MAPB, [(a, (30.5, 50.4), 200)], a, tc + 0.6,
                     pins=[dict(at="Kyiv", label="KIEV", t=a + 0.3, side="r", color=RED)], title=MT))
        sc.add(Calendar((420, 420), 220, [(a + 0.2, "DICEMBRE 2016", "21")], a + 0.2, tc + 0.6), "paper")
        sc.add(Text("La *cerimonia*", (960, 200), tc + 0.6, size=84, anchor="ma", align="m"))
        sc.add(Figure([(tp, 500, FY), (tp + 1.5, 540, FY)], tp, None, kind="suit", s=0.85, label="PRESIDENTE UCRAINO"))
        sc.add(Figure([(T("consegna") - 0.2, 1450, FY), (T("consegna") + 1.3, 1380, FY)], T("consegna") - 0.2, None, kind="suit", s=0.85, label="MINISTRO DELLA CULTURA", flip=-1))
        sc.add(Img(pic(2, 200, 150), (960, 600), T("opere") - 0.1, anim="drop"), "paper")
        sc.add(Pill("COLLABORAZIONE TRA LE POLIZIE", (960, 400), te, size=46, accent=True))
        sc.footer = "Fonti: AP · artnet · " + MT
    elif i == 26:
        ta = T("A") - 0.3; tp = T("Poi") - 0.3
        sc.add(MapEl(MAPB, [(a, (20.5, 47.5), 52)], a, ta + 0.3,
                     pins=[dict(at="Kyiv", label="KIEV", t=a + 0.2, side="r", color=GOLD),
                           dict(at="Verona", label="VERONA", t=a + 1.6, side="l", color=RED)],
                     routes=[dict(pts=["Kyiv", "Verona"], t=a + 0.3, d=1.6, icon="painting", color=RED)], title=MT))
        sc.add(Galleria(GB, ta, tp + 0.3, label="cornici provvisorie · sagome stilizzate"))
        sc.add(Pill("ESPOSTI PER CIRCA UN MESE", (960, 215), T("per") - 0.2, tp, size=48, accent=True))
        sc.add(Figure([(tp, 600, FY)], tp, None, kind="painter", s=0.9, label="RESTAURO"))
        sc.add(Img(pic(5, 300, 380), (1200, 520), tp + 0.2, anim="drop"), "paper")
        sc.add(Pill("DI NUOVO NELLE SALE", (960, 215), T("per", 1) - 0.2, size=48, accent=True))
        sc.footer = "Fonti: AP · artnet · " + MT
    elif i == 27:
        ti = T("Il") - 0.3; tl = T("La") - 0.3; tt = T("Tra") - 0.3; td = T("Due") - 0.3
        sc.add(Text("E i *processi?*", (960, 330), a, ti, size=120, anchor="ma", align="m"))
        sc.add(Calendar((420, 420), 220, [(ti, "DICEMBRE 2016", "5")], ti, td), "paper")
        sc.add(Icon("gavel", (1560, 380), ti + 0.2, td, size=220, label="TRIBUNALE DI VERONA"), "hit")
        sc.add(Big("10 anni e 8 mesi", (960, 600), tl, td, size=110, color=RED, sub="LA PENA PIÙ ALTA"))
        sc.add(Stamp("PRIMO GRADO", (960, 820), tl + 0.6, td, size=56, rot=-5))
        sc.add(Pill("CONDANNATA ANCHE LA GUARDIA GIURATA", (960, 215), tt, td, size=44, accent=True))
        sc.add(MapEl(MAPB, [(td, "Chisinau", 160)], td, None,
                     pins=[dict(at="Chisinau", label="PROCESSO IN MOLDAVIA", t=td + 0.3, side="r", color=RED)], title=MT))
        sc.add(Icon("court", (700, 520), td + 0.4, size=200), "pop")
        sc.footer = "Fonti: ANSA · artnet · AP · esiti successivi non confermati da due fonti"
    elif i == 28:
        tn = T("Nel") - 0.3; tc = T("che") - 0.3
        sc.add(Text("Una conseguenza\npiù *grande*", (960, 330), a, tn, size=100, anchor="ma", align="m"))
        sc.add(Icon("court", (500, 500), tn, size=280, label="PARLAMENTO"), "pop")
        sc.add(Img(doc_typed(600, 460, "LEGGE 9 MARZO 2022, N. 22", ["Reati contro", "il patrimonio culturale", "nel codice penale", "pene più severe"]), (1250, 500), tc, anim="drop", rot=2), "paper")
        sc.add(Icon("scales", (500, 500), T("con") - 0.2, size=0) if False else Pill("FURTO D'ARTE = REATO SPECIFICO", (960, 215), T("con") - 0.2, size=46, accent=True))
        sc.footer = "Fonti: Normattiva · Il Sole 24 Ore · AP · documento: ricostruzione grafica"
    elif i == 29:
        tr = T("Tre") - 0.3
        steps = [("TRE UOMINI", "balaclava", "Tre"), ("MUSEO IN CHIUSURA", "museum", "un"), ("ALLARME SPENTO", "alarm_off", "allarme"),
                 ("17 QUADRI", "frame_empty", "Diciassette"), ("L'AUTO DELLA GUARDIA", "car", "l'auto"),
                 ("13 ARRESTI", "handcuffs", "Tredici"), ("L'ISOLA", "island", "dei")]
        for k, (lab, ic, w_) in enumerate(steps):
            x = 220 + (k % 4) * 490; y = 380 if k < 4 else 690
            tk = T(w_) - 0.2
            sc.add(Icon(ic, (x, y - 40), tk, size=170), "pop")
            sc.add(Text(lab, (x, y + 70), tk + 0.1, size=34, fnt=OSW, color=GOLD, anchor="ma"))
        sc.add(Text("*Ricapitolando*", (960, 190), a, size=70, anchor="ma", align="m"))
        sc.footer = "Fonti: Il Post · The Art Newspaper · AP · ANSA · L'Adige"
    elif i == 30:
        te = T("E", 0) - 0.3; ti = T("Iscriviti") - 0.3
        sc.add(Text("A chi dovevano\n*arrivare?*", (960, 220), a, ti, size=90, anchor="ma", align="m"))
        sc.add(Galleria((460, 450, 1460, 860), a, ti, gone=a + 0.4, back=te, step=0.06, label=""))
        sc.add(Icon("question", (1600, 330), a + 0.6, ti, size=160), "pop")
        sc.add(Img(wordmark(110), (960, 500), ti, anim="pop", shadow=False), "hit")
        sc.add(Pill("OGNI GIORNO UN NUOVO CASO", (960, 680), ti + 0.4, size=50, accent=True))
        sc.footer = "Ricostruzione a scopo divulgativo · voce generata con sintesi vocale"
    return sc

def thumbnail(path="thumbnail.jpg"):
    im = make_bg(7); d = ImageDraw.Draw(im)
    t = rich_img("17 QUADRI\nSPARITI\nIN *UNA SERA*", SERIF, 118, WHITE, RED, lh=1.0)
    im.alpha_composite(t, (90, 150))
    lay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    Galleria((1080, 170, 1860, 640), 0, None, gone=0.0, step=0.0, label="").draw(lay, 5.0, 1.0)
    g2 = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    im.alpha_composite(lay)
    isl = fx.icon("island", 300); im.alpha_composite(isl, (1250, 660))
    bag = fx.icon("trashbag", 200); im.alpha_composite(bag, (1560, 760))
    st = stamp_img("CASO 015", RED, 70, -10); im.alpha_composite(st, (1560, 40))
    d.text((100, 840), "VERONA 2015: RITROVATI SU UN'ISOLA IN UCRAINA", font=font(OSW, 48, 600), fill=GOLD + (255,))
    d.text((1880, 1060), "sagome stilizzate, non le opere", font=font(COURR, 22), fill=(200, 190, 170, 255), anchor="rs")
    wm = wordmark(60, sub=False); im.alpha_composite(wm, (100, 960))
    im.convert("RGB").save(path, quality=92)
