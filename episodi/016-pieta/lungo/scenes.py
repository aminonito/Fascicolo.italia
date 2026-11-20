import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from pt import *

W, H = 1920, 1080
FY = 870
CB = (260, 170, 1660, 870)      # scenografia: la cappella della Pietà
CL = (160, 200, 1060, 860)      # cappella ridotta a sinistra
CS = (460, 250, 1460, 770)      # cappella ridotta al centro (per gli zoom)
MAPB = (160, 160, 1760, 880)
MT = "mappa: Natural Earth · schema non in scala"
WT = "mappa: Natural Earth · percorso indicativo"
F_OP = "Fonti: Musei Vaticani · Libreriamo · Finestre sull'Arte · Geopop"
F_ATT = "Fonti: Il Post · Finestre sull'Arte · Geopop · Wanted in Rome · Wikipedia"
F_TOTH = "Fonti: Il Post · Finestre sull'Arte · Wikipedia · Wanted in Rome"
F_RES = "Fonti: Reuters (2013) · Wanted in Rome · Finestre sull'Arte · Geopop · Wikipedia"
SAG = "sagoma stilizzata, non l'opera"

def TLE(evs):
    return [dict(t=t, top=top, bottom=b, hl=(k == len(evs) - 1)) for k, (t, top, b) in enumerate(evs)]

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
        tb = T("Basilica") - 0.3; td = T("Domenica") - 0.3; tf = T("festa") - 0.2; ts = T("Sono") - 0.3; tdv = T("Davanti") - 0.3
        sc.add(MapEl(MAPB, [(a, (12.5, 42.5), 90), (tb, "Roma", 420)], a, td + 0.2,
                     pins=[dict(at="Roma", label="ROMA", t=a + 0.4, side="r", color=RED)], title=MT))
        sc.add(Icon("basilica", (1400, 560), tb, td + 0.2, size=360), "pop")
        sc.add(Pill("BASILICA DI SAN PIETRO", (960, 215), tb + 0.2, td + 0.2, size=48, accent=True))
        sc.add(Calendar((560, 500), 280, [(td, "DOMENICA", "21"), (td + 1.0, "MAGGIO 1972", "21")], td, ts), "paper")
        sc.add(Icon("dove", (1360, 470), tf, ts, size=300), "pop")
        sc.add(Pill("PENTECOSTE", (1360, 700), tf + 0.2, ts, size=52, accent=True))
        sc.add(ClockFace((960, 500), 220, ts, tdv, start=11.4, speed=0.01, label="11:30 CIRCA"))
        sc.add(Cappella(CB, tdv, None), "whoosh")
        sc.add(Crowd((420, 760, 1500, 860), 12, tdv + 0.4, None, s=0.36, seed=4))
        sc.add(Pill("LA PIETÀ DI MICHELANGELO", (960, 215), tdv + 0.3, size=48, accent=True))
        sc.footer = "Fonti: Il Post · Finestre sull'Arte · Geopop · " + SAG + " · " + MT
    elif i == 1:
        ti = T("All'improvviso") - 0.2; tm = T("In") - 0.3; tc = T("Colpisce") - 0.2; tb = T("Il") - 0.2; tn = T("naso") - 0.2; tal = T("Alla") - 0.3
        hits = [tc + 0.3 + k * 0.32 for k in range(8)]
        sc.add(Cappella(CS, a, tal, pk=dict(hits=hits, arm_t=tb + 0.4, nose_t=tn + 0.1), frags=(tb, 50), label=""))
        sc.add(Figure([(ti, 560, 760), (ti + 1.2, 790, 680)], ti, tal, kind="man", s=0.42, arms=[(tm, "up")]))
        sc.add(Swing((840, 440), 110, tm, tal, hits=hits))
        sc.add(Pill("MARTELLO DA GEOLOGO", (960, 215), tm + 0.2, tc, size=48, accent=True))
        sc.add(Pill("UNA QUINDICINA DI COLPI", (960, 215), tc, tb, size=48, accent=True))
        sc.add(Pill("IL BRACCIO SINISTRO", (960, 215), tb, tn - 0.35, size=48, accent=True))
        sc.add(Pill("IL NASO", (960, 215), tn, tal, size=48, accent=True))
        scene_cam(sc, (tc, 960, 540, 1.0), (tc + 1.0, 960, 500, 1.2), (tb + 1.0, 960, 500, 1.2), (tal - 0.3, 960, 540, 1.0))
        sc.add(Frags((260, 230, 1660, 880), tal, None, n=100))
        sc.add(Big("100", (960, 520), tal + 0.3, size=260, color=RED, sub="frammenti circa", subsize=50))
        sc.footer = F_ATT + " · " + SAG
    elif i == 2:
        sc.add(Img(cover_folder(560), (540, 520), a, anim="drop", rot=-3), "paper")
        items = [("IL CAPOLAVORO", "capolavoro"), ("L'UOMO CON IL MARTELLO", "chi"), ("LA DOMENICA DI PENTECOSTE", "quella"),
                 ("CHE FINE FA L'AGGRESSORE", "che"), ("LA CACCIA AI FRAMMENTI", "la"), ("IL RESTAURO INVISIBILE", "restauro")]
        for k, (lab, w_) in enumerate(items):
            sc.add(Pill(lab, (1340, 250 + k * 100), T(w_) - 0.2, size=42, accent=(k % 2 == 1)))
        sc.footer = "Ricostruzione a scopo divulgativo · fascicolo ricostruito"
    elif i == 3:
        tf = T("Fine") - 0.3; tu = T("Un") - 0.3; tam = T("ambasciatore") - 0.2; tfi = T("firma") - 0.2; tl = T("Lo") - 0.3; ts = T("Si") - 0.3
        sc.add(Text("Partiamo\ndall'*opera*", (960, 330), a, tf, size=110, anchor="ma", align="m"))
        sc.add(Calendar((960, 480), 300, [(tf, "AGOSTO", "27"), (tf + 1.0, "1498", "26/27")], tf, tu), "paper")
        sc.add(Img(person_card("Jean de Bilhères", "cardinale francese", 300, seed=2), (520, 480), tu, anim="drop", rot=-2), "paper")
        sc.add(Icon("crown", (520, 760), tam, size=120, label="AMBASCIATORE DEL RE DI FRANCIA"), "pop")
        sc.add(Img(contract_img(480), (1000, 520), tfi, anim="drop", rot=1), "paper")
        sc.add(Img(person_card("Michelangelo Buonarroti", "scultore fiorentino", 300, seed=5), (1480, 480), tl, anim="drop", rot=2), "paper")
        sc.add(Stamp("23 ANNI", (1480, 760), tl + 0.3, size=70, rot=-8))
        sc.footer = F_OP + " · Fordham University · contratto: ricostruzione grafica, data 26 o 27 agosto secondo le fonti"
    elif i == 4:
        tn = T("nella") - 0.2; ta = T("accanto") - 0.2; tm = T("Michelangelo") - 0.3; ts = T("a") - 0.2; tu = T("Un", 1) - 0.3
        sc.add(Icon("basilica", (560, 500), a, tm, size=380), "pop")
        sc.add(Pill("UN MONUMENTO PER LA TOMBA", (960, 215), a + 0.2, tn, size=48, accent=True))
        sc.add(Pill("CAPPELLA DI SANTA PETRONILLA", (960, 215), tn, tm, size=48, accent=True))
        sc.add(Text("accanto alla\n*vecchia* basilica", (1350, 420), ta, tm, size=72, anchor="ma", align="m"))
        sc.add(MapEl(MAPB, [(tm, (11.0, 43.2), 140), (ts + 0.8, "Carrara", 320)], tm, None,
                     pins=[dict(at="Roma", label="ROMA", t=tm + 0.2, side="r", color=GOLD),
                           dict(at="Carrara", label="CARRARA", t=tm + 0.4, side="r", color=RED)],
                     routes=[dict(pts=["Roma", "Carrara"], t=tm + 0.4, d=1.6, icon="person", color=RED)], title=MT))
        sc.add(Icon("mountain", (1450, 520), ts + 0.4, size=240, label="CAVE DI MARMO"), "pop")
        sc.add(Pill("MARMO BIANCO · LA MIGLIOR QUALITÀ", (960, 215), tu, size=48, accent=True))
        sc.footer = "Fonti: Musei Vaticani (schede 2013 e 2023) · Libreriamo · Fordham University · " + MT
    elif i == 5:
        tl = T("la", 1) - 0.2; tla = T("La", 2) - 0.3; tlr = T("e", 1) - 0.2; tmc = T("Michelangelo") - 0.3
        sc.add(Text("La *Pietà*", (960, 190), a, tla, size=90, anchor="ma", align="m"))
        sc.add(Pieta((960, 860), 600, a + 0.3, None, label=SAG), "whoosh")
        sc.add(Arrow((1320, 380), (1080, 500), tl, tla, color=GOLD))
        sc.add(Pill("LA MADONNA", (1450, 360), tl, tla, size=42))
        sc.add(Arrow((560, 700), (790, 610), tl + 1.0, tla, color=GOLD))
        sc.add(Pill("IL CRISTO SULLE GINOCCHIA", (460, 740), tl + 1.0, tla, size=40))
        sc.add(Line((1340, 860), (1340, 260), tla, tmc, color=RED, width=6))
        sc.add(Text("circa\n*174 cm*", (1480, 520), tla + 0.3, tmc, size=64, anchor="ma", align="m"))
        sc.add(Line((660, 900), (1260, 900), tlr, tmc, color=RED, width=6))
        sc.add(Pill("LARGA CIRCA 195 CM", (960, 215), tlr + 0.2, tmc, size=46, accent=True))
        sc.add(Pill("COMPLETATA INTORNO AL 1500", (960, 215), tmc, size=46, accent=True))
        sc.add(Icon("chisel_s", (1500, 520), tmc + 0.3, size=200), "pop")
        sc.footer = "Fonti: Finestre sull'Arte · Geopop · Musei Vaticani · misure 174 x 195 x 69 cm · " + SAG
    elif i == 6:
        ts = T("Sulla") - 0.3; tm = T("Michelangelo") - 0.3; te = T("È") - 0.3; tsc = T("Secondo") - 0.3; tlo = T("lo") - 0.2
        sc.add(Text("Un dettaglio\n*unico*", (960, 330), a, ts, size=110, anchor="ma", align="m"))
        sc.add(Pieta((560, 860), 560, ts, None, label=SAG))
        sc.add(Bubble((1300, 420), 220, ts + 0.3, tm, inner="magnifier"))
        sc.add(Img(signature_img(820), (1300, 470), tm, tsc, anim="drop"), "paper")
        sc.add(Stamp("L'UNICA OPERA FIRMATA", (1300, 720), te, tsc, size=62, rot=-6))
        sc.add(Crowd((1000, 640, 1700, 860), 5, tsc, None, s=0.42, seed=8))
        sc.add(Bubble((1350, 330), 180, tlo, None, text="DI CHI È?"))
        sc.footer = "Fonti: Musei Vaticani (scheda 2013 e 2023) · Libreriamo · Mental Floss · firma: ricostruzione grafica"
    elif i == 7:
        tdc = T("Dal") - 0.3; tp = T("passano") - 0.2; td = T("Dal", 1) - 0.3; tap = T("appena") - 0.2; te = T("È") - 0.3
        sc.add(Text("Facciamo\nun *conto*", (960, 330), a, tdc, size=110, anchor="ma", align="m"))
        sc.add(Timeline(260, 1660, 480, TLE([(tdc, "1498", "contratto"), (tdc + 1.2, "1749", "nella cappella di oggi"), (T("a") - 0.2, "1972", "la domenica dei colpi")]), tdc, td))
        sc.add(Big("474", (960, 680), tp, td, size=170, color=RED, sub="anni", subsize=48))
        sc.add(Text("1972 − 1498 = 474", (960, 860), tp + 0.5, td, size=34, fnt=COURR, color=GOLD, anchor="ma"))
        sc.add(Cappella(CB, td, None), "whoosh")
        sc.add(Pill("PRIMA CAPPELLA A DESTRA · DAL 1749", (960, 215), td + 0.2, te, size=46, accent=True))
        sc.add(Crowd((420, 760, 1500, 860), 14, tap, None, s=0.36, seed=6))
        sc.add(Pill("UNA DELLE OPERE PIÙ AMMIRATE AL MONDO", (960, 215), te, size=44, accent=True))
        sc.footer = "Fonti: Musei Vaticani (scheda 2013) · Mental Floss · calcolo nostro · " + SAG
    elif i == 8:
        ts = T("Si") - 0.3; te = T("È") - 0.3; tg = T("e") - 0.2; tn = T("Nel", 1) - 0.3
        sc.add(Text("L'uomo con\nil *martello*", (960, 330), a, ts, size=110, anchor="ma", align="m"))
        sc.add(Img(label_card(["László Tóth", "nato nel 1938, Ungheria", "studi di geologia", "33 anni nel 1972"], 560, title="SCHEDA"), (620, 520), ts, anim="drop", rot=-2), "paper")
        sc.add(Icon("nophoto", (620, 820), ts + 0.4, size=90), "pop")
        sc.add(MapEl((1080, 220, 1760, 820), [(te, (19.0, 47.5), 140)], te, tg,
                     pins=[dict(at=(19.0, 47.6), label="UNGHERIA", t=te + 0.3, side="r", color=RED)], title=""))
        sc.add(Icon("geo", (1420, 480), tg, tn, size=280), "pop")
        sc.add(Pill("GEOLOGO", (1420, 720), tg + 0.2, tn, size=48, accent=True))
        sc.add(Big("33", (1420, 480), tn, size=200, color=RED, sub="anni nel 1972", subsize=40))
        sc.footer = F_TOTH + " · nessuna foto: scheda ricostruita"
    elif i == 9:
        tl = T("Lì,") - 0.3; tn = T("Nel", 1) - 0.3; tg = T("Guardiamo") - 0.3
        sc.add(WorldMap(MAPB, [(a, (80, 8), 7.8), (tn, (78, 8), 7.6)], a, None,
                        routes=[dict(pts=["Ungheria", "Sydney"], t=a + 0.3, d=2.0, icon="plane", color=GOLD, bend=-0.12),
                                dict(pts=["Sydney", "Roma"], t=tn + 0.2, d=2.0, icon="plane", color=RED, bend=0.12)],
                        pins=[dict(at="Ungheria", label="UNGHERIA", t=a + 0.1, side="r"),
                              dict(at="Sydney", label="AUSTRALIA · 1965", t=a + 1.6, side="l", color=GOLD),
                              dict(at="Roma", label="ROMA · 1971", t=tn + 1.6, side="b")], title=WT))
        sc.add(Icon("soap", (1500, 330), tl, tn, size=200, label="FABBRICA DI SAPONE"), "pop")
        sc.add(Pill("DALL'EUROPA ALL'AUSTRALIA · E RITORNO", (960, 820), tg, size=46, accent=True))
        sc.footer = F_TOTH + " · " + WT
    elif i == 10:
        tt = T("Tóth") - 0.2; tc = T("Chiede") - 0.3; tn = T("Non") - 0.3; ts = T("Secondo") - 0.3
        sc.add(Icon("basilica", (500, 480), a, size=320), "pop")
        sc.add(Figure([(a + 0.2, 120, FY), (a + 2.2, 420, FY)], a + 0.2, None, kind="man", s=0.55, label="TÓTH"))
        sc.add(Img(letter_img(440), (1000, 470), tt, anim="drop", rot=-3), "paper")
        sc.add(Icon("envelope", (1400, 360), tt + 0.6, size=150, move=(tt + 0.6, 1.0, (1450, 520), 80)), "whoosh")
        sc.add(Icon("envelope", (1450, 520), tc, size=150), "pop")
        sc.add(Pill("PAPA PAOLO VI", (1450, 700), tt + 0.4, size=46, accent=True))
        sc.add(Stamp("NESSUN INCONTRO", (1000, 700), tn, size=70, rot=-8))
        sc.add(Bubble((1560, 330), 160, ts, None, text="«CRISTO»"))
        sc.footer = F_TOTH + " · lettera: ricostruzione grafica, testo non originale"
    elif i == 11:
        ti = T("In") - 0.3; tl = T("La") - 0.3; ts = T("sopra") - 0.2; tt = T("Tra") - 0.3; tc = T("c'è") - 0.2
        sc.add(Calendar((960, 480), 320, [(a, "DOMENICA", "21"), (a + 1.0, "MAGGIO 1972", "21")], a, ti), "paper")
        sc.add(Icon("dove", (960, 480), ti, tl, size=360), "pop")
        sc.add(Pill("PENTECOSTE IN SAN PIETRO", (960, 215), ti + 0.2, tl, size=48, accent=True))
        sc.add(Cappella(CB, tl, None, rail=False), "whoosh")
        sc.add(Pill("IL BASAMENTO", (960, 215), ts, tt, size=48, accent=True))
        sc.add(Cappella(CB, tc, None, rail=True))
        sc.add(Crowd((420, 780, 1500, 870), 12, tc + 0.3, None, s=0.34, seed=2))
        sc.add(Pill("SOLO UNA BALAUSTRA · NESSUN VETRO", (960, 215), tc, size=46, accent=True))
        sc.footer = F_ATT + " · " + SAG
    elif i == 12:
        tt = T("Tóth") - 0.3; tsc = T("scavalca") - 0.2; te = T("e") - 0.2; tm = T("Mentre") - 0.3; tg = T("«Sono") - 0.3
        hits = [te + 0.6 + k * 0.4 for k in range(7)]
        sc.add(Cappella(CS, a, None, pk=dict(hits=hits), label=""))
        sc.add(ClockFace((1650, 330), 90, a, tsc, start=11.45, speed=0.01, label="11:30"))
        sc.add(Figure([(tt, 520, 760), (tsc + 0.8, 790, 680)], tt, None, kind="man", s=0.42, arms=[(te, "up")]))
        sc.add(Swing((840, 440), 110, te, None, hits=hits))
        sc.add(Pill("SCAVALCA LA BALAUSTRA", (960, 200), tsc, te, size=48, accent=True))
        sc.add(Pill("COLPISCE LA STATUA", (960, 200), te, tm, size=48, accent=True))
        sc.add(Bubble((400, 430), 150, tg, None, text="«CRISTO!»"))
        scene_cam(sc, (te, 960, 540, 1.0), (te + 1.0, 940, 500, 1.2))
        sc.footer = F_ATT + " · " + SAG
    elif i == 13:
        tp = T("Per") - 0.3; tu = T("una") - 0.2; ts = T("Secondo") - 0.3; td = T("dodici.") - 0.2; tq = T("Quasi") - 0.3
        sc.add(Icon("question", (960, 480), a, tp, size=300), "pop")
        sc.add(Big("15", (620, 470), tu, tq, size=230, color=RED, sub="circa · quasi tutte le fonti", subsize=34))
        sc.add(Big("12", (1300, 470), td, tq, size=230, color=GOLD, sub="altre ricostruzioni", subsize=34))
        sc.add(Pill("LE FONTI NON COINCIDONO", (960, 215), ts, tq, size=48, accent=True))
        sc.add(Pieta((960, 870), 560, tq, None, label=SAG))
        for k, (w_, lab, tgt, ly) in enumerate([("volto,", "VOLTO", (985, 425), 330), ("velo,", "VELO", (1010, 360), 230), ("braccio", "BRACCIO SINISTRO", (1110, 560), 520)]):
            tw = T(w_) - 0.1
            sc.add(Arrow((1400, ly), tgt, tw, color=RED))
            sc.add(Pill(lab, (1560, ly), tw, size=40))
        sc.footer = F_ATT + " (15) · Reuters 2013 · Finestre sull'Arte (12) · " + SAG
    elif i == 14:
        te = T("Ecco") - 0.3; tb = T("Il") - 0.3; tn = T("naso") - 0.2; tp = T("Una") - 0.3; ts = T("Sul") - 0.3
        sc.add(Text("Il bilancio\ndei *danni*", (960, 330), a, tb, size=110, anchor="ma", align="m"))
        sc.add(Pieta((700, 880), 620, tb, None, arm_t=tb + 0.4, nose_t=tn + 0.2, eye_t=tp + 0.3, label=SAG))
        sc.add(Pill("BRACCIO SINISTRO · STACCATO AL GOMITO", (1360, 330), tb + 0.2, size=38, accent=True))
        sc.add(Pill("NASO · IN PEZZI", (1360, 440), tn, size=38, accent=True))
        sc.add(Pill("UNA PALPEBRA · SCHEGGIATA", (1360, 550), tp, size=38, accent=True))
        sc.add(Frags((1060, 600, 1700, 880), ts, None, n=100, counter=False))
        sc.add(Big("100", (1380, 720), ts + 0.4, size=150, color=RED, sub="frammenti circa", subsize=36))
        sc.footer = F_ATT + " · Reuters 2013 · " + SAG
    elif i == 15:
        tt = T("Tra") - 0.3; tb = T("Bob") - 0.2; tg = T("e") - 0.2; tm = T("Marco") - 0.2; tp = T("Poco") - 0.3
        sc.add(Cappella(CB, a, None, pk=dict(broken=True), frags=(a, 50)))
        sc.add(Figure([(a, 760, 760)], a, None, kind="man", s=0.55))
        sc.add(Crowd((300, 780, 1600, 870), 10, a + 0.3, None, s=0.36, seed=12))
        sc.add(Figure([(tt, 300, 860), (tt + 1.0, 640, 780)], tt, None, kind="painter", s=0.55, label="SCULTORE AMERICANO"))
        sc.add(Icon("chisel_s", (300, 330), tb, tp, size=150, label="BOB CASSILLY"), "pop")
        sc.add(Figure([(tg, 1660, 860), (tg + 1.0, 880, 780)], tg, None, kind="plumber", s=0.55, label="VIGILE DEL FUOCO"))
        sc.add(Icon("fire", (1620, 330), tm, tp, size=150, label="MARCO OTTAGGIO"), "pop")
        sc.add(Figure([(tp, 1700, 860), (tp + 1.2, 980, 790)], tp, None, kind="police", s=0.55))
        sc.add(Icon("handcuffs", (960, 300), tp + 0.6, size=180), "hit")
        sc.add(Pill("ARRESTATO", (960, 215), tp + 0.8, size=52, accent=True))
        sc.footer = "Fonti: Wikipedia · Finestre sull'Arte · Geopop · Wanted in Rome · " + SAG
    elif i == 16:
        tal = T("Almeno") - 0.3; te = T("e") - 0.2; tm = T("Mesi") - 0.3; ts = T("spedito") - 0.2; td = T("dagli") - 0.2
        sc.add(Text("Una cosa\n*incredibile*", (960, 330), a, tal, size=110, anchor="ma", align="m"))
        sc.add(Cappella(CL, tal, tm + 0.3, pk=dict(broken=True), frags=(tal, 50), label=""))
        sc.add(Figure([(tal + 0.2, 900, 840), (te + 0.3, 900, 840), (te + 2.0, 1500, 860)], tal + 0.2, tm, kind="suit", s=0.5, arms=[(tal + 1.0, "hold")]))
        sc.add(Icon("pieces", (1500, 420), te, tm, size=200, label="UN FRAMMENTO PORTATO VIA"), "pop")
        sc.add(WorldMap(MAPB, [(tm, (-25, 42), 14)], tm, None,
                        routes=[dict(pts=["NewYork", "Roma"], t=ts, d=2.2, icon="envelope", color=GOLD, bend=-0.15)],
                        pins=[dict(at="NewYork", label="STATI UNITI", t=ts - 0.1, side="r", color=GOLD),
                              dict(at="Roma", label="ROMA", t=ts, side="l")], title=WT))
        sc.add(Pill("MESI DOPO · SPEDITO IN FORMA ANONIMA", (960, 215), ts, size=46, accent=True))
        sc.footer = "Fonti: Wikipedia · Wanted in Rome · Reuters (2013) · " + WT
    elif i == 17:
        tl = T("La", 1) - 0.3; ti = T("Il", 1) - 0.3; to = T("ora") - 0.2
        sc.add(Cappella(CB, a, tl - 0.3, pk=dict(broken=True)))
        sc.add(Figure([(a + 0.2, 1700, 860), (a + 2.4, 1150, 820)], a + 0.2, tl - 0.3, kind="suit", s=0.55, label="PAOLO VI"))
        sc.add(Pill("LO STESSO GIORNO", (960, 215), a + 0.3, tl, size=48, accent=True))
        sc.add(Img(newspaper(760, 500, "CRONACA", "LUNEDÌ 22 MAGGIO 1972", "Colpi di martello\nalla Pietà", "Danneggiata la statua\ndi Michelangelo in San Pietro", seed=8),
                   (680, 520), tl, anim="drop", rot=-3), "paper")
        sc.add(Icon("flagless_globe", (1460, 460), tl + 0.4, to, size=280), "pop")
        sc.add(Text("quasi *5 secoli*", (1460, 700), ti, size=64, anchor="ma"))
        sc.add(Icon("pieta_b", (1460, 460), to, size=300), "hit")
        sc.footer = "Fonti: Il Post · Finestre sull'Arte · giornale: ricostruzione grafica, testata generica"
    elif i == 18:
        tn = T("Non") - 0.3; tv = T("Viene") - 0.3; tal = T("Alla") - 0.3; ti = T("in") - 0.2; tp = T("per") - 0.2
        sc.add(Text("E l'uomo\ncon il *martello*?", (960, 330), a, tn, size=100, anchor="ma", align="m"))
        sc.add(Icon("court", (560, 480), tn, size=300), "pop")
        sc.add(Stamp("MAI PROCESSATO", (560, 720), tn + 0.4, size=70, rot=-8))
        sc.add(Img(label_card(["giudicato", "infermo di mente"], 520, title="PERIZIA"), (1340, 470), tv, tal, anim="drop", rot=2), "paper")
        sc.add(Calendar((1340, 470), 260, [(tal, "GENNAIO", "28"), (tal + 1.0, "1973", "28/29")], tal, ti), "paper")
        sc.add(Img(order_img(460), (1340, 520), ti, anim="drop", rot=-2), "paper")
        sc.add(Icon("hospital", (1700, 300), ti + 0.3, size=150), "pop")
        sc.add(Pill("ALMENO 2 ANNI", (1340, 830), tp, size=50, accent=True))
        sc.footer = "Fonti: Wikipedia (NYT 30/1/1973) · Il Post · Finestre sull'Arte · Mental Floss · documento: ricostruzione grafica"
    elif i == 19:
        te = T("e") - 0.2; tl = T("Lì") - 0.3; td = T("Di") - 0.3; tm = T("Muore") - 0.3
        sc.add(WorldMap(MAPB, [(a, (40, 30), 14), (te + 0.3, (78, 8), 7.6)], a, td,
                        routes=[dict(pts=["Roma", "Sydney"], t=te, d=2.2, icon="plane", color=GOLD, bend=0.12)],
                        pins=[dict(at="Roma", label="ROMA · 1975", t=a + 0.2, side="l"),
                              dict(at="Sydney", label="AUSTRALIA", t=te + 2.0, side="l", color=GOLD)], title=WT))
        sc.add(Pill("DIMESSO ALL'INIZIO DEL 1975", (960, 215), a + 0.3, tl, size=46, accent=True))
        sc.add(Pill("IN AUSTRALIA NON VIENE ARRESTATO", (960, 215), tl, td, size=46, accent=True))
        sc.add(Icon("question", (960, 500), td, tm, size=260), "pop")
        sc.add(Timeline(360, 1560, 540, TLE([(tm - 1.0, "1972", "i colpi"), (tm - 0.6, "1973", "ricovero"), (tm - 0.3, "1975", "in Australia"), (tm + 0.4, "2012", "muore")]), tm - 1.0, None))
        sc.footer = F_TOTH + " · Geopop · " + WT
    elif i == 20:
        tc = T("Che") - 0.3; tl = T("Lasciare") - 0.3; to = T("Oppure") - 0.3
        sc.add(Text("Un *dibattito*", (960, 200), a, None, size=90, anchor="ma", align="m"))
        sc.add(Icon("debate", (960, 500), a + 0.3, tl, size=320), "pop")
        sc.add(Pieta((560, 860), 480, tl, None, broken=True, label=SAG))
        sc.add(Pill("A · LASCIARE I SEGNI", (560, 330), tl + 0.2, size=44, accent=True))
        sc.add(Pieta((1360, 860), 480, to, None, label=SAG))
        sc.add(Pill("B · RESTAURO INVISIBILE", (1360, 330), to + 0.2, size=44))
        sc.footer = "Fonti: Reuters (2013) · Mental Floss · " + SAG
    elif i == 21:
        ti = T("invisibile") - 0.2; tl = T("Lo") - 0.3; td = T("Deoclecio") - 0.2; tla = T("La", 2) - 0.3; til = T("il", 1) - 0.2
        sc.add(Stamp("B", (960, 330), a, tl, size=140, rot=-6))
        sc.add(Pill("RESTAURO INTEGRALE", (960, 520), a + 0.4, tl, size=56, accent=True))
        sc.add(Icon("eye", (960, 700), ti, tl, size=200, label="INVISIBILE A OCCHIO NUDO"), "pop")
        sc.add(Icon("museum", (560, 480), tl, tla, size=280), "pop")
        sc.add(Img(person_card("Deoclecio Redig de Campos", "dir. Musei Vaticani", 320, seed=11), (1300, 480), td, tla, anim="drop", rot=2), "paper")
        sc.add(Cappella(CB, tla, None, screen_t=til + 0.3), "whoosh")
        sc.add(Pill("LA STATUA RESTA NELLA CAPPELLA", (960, 215), tla + 0.2, til, size=46, accent=True))
        sc.add(Pill("UN LABORATORIO INTORNO A LEI", (960, 215), til, size=46, accent=True))
        sc.add(Icon("lab", (1500, 420), til + 0.8, size=180), "pop")
        sc.footer = F_RES + " · " + SAG
    elif i == 22:
        tp = T("Per") - 0.3; ti = T("i", 1) - 0.2; to = T("Ognuno") - 0.3; tc = T("come") - 0.2
        sc.add(Text("Prima di tutto,\ni *frammenti*", (960, 200), a, tp, size=80, anchor="ma", align="m"))
        sc.add(Frags((260, 300, 1660, 860), a + 0.3, to, n=100, sort_t=ti, sort_d=3.5))
        sc.add(Calendar((1700, 300), 160, [(tp, "5 MESI", "+"), (tp + 0.8, "OLTRE", "5")], tp, to), "paper")
        sc.add(Pieta((560, 860), 520, to, None, broken=True, label=SAG))
        sc.add(Icon("pieces", (1300, 520), to + 0.4, size=260), "pop")
        sc.add(Arrow((1150, 520), (760, 400), to + 0.8, color=GOLD))
        sc.add(Icon("puzzle", (1500, 330), tc, size=180), "pop")
        sc.add(Pill("UN PUZZLE IN 3D", (1300, 760), tc + 0.2, size=48, accent=True))
        sc.footer = F_RES + " · " + SAG
    elif i == 23:
        tc = T("Circa") - 0.3; ti = T("in") - 0.2; tm = T("in") - 0.2; tm = T("media,") - 0.2; tu = T("Un", 1) - 0.3
        sc.add(Text("Un altro\n*conto*", (960, 330), a, tc, size=110, anchor="ma", align="m"))
        sc.add(Big("100", (560, 450), tc, tu, size=180, color=WHITE, sub="frammenti circa", subsize=40))
        sc.add(Text("÷", (960, 430), ti, tu, size=120, anchor="ma"))
        sc.add(Big("150", (1360, 450), ti + 0.2, tu, size=180, color=GOLD, sub="giorni circa (5 mesi)", subsize=40))
        sc.add(Pill("= 1 FRAMMENTO OGNI GIORNO E MEZZO", (960, 760), tm, tu, size=52, accent=True))
        sc.add(Icon("hourglass", (560, 520), tu, size=300), "pop")
        sc.add(Text("Lento.\nE la fretta è\nil *nemico*.", (1240, 380), tu + 0.3, size=72, anchor="ma", align="m"))
        sc.footer = "Calcolo nostro su dati di Reuters (2013), Wanted in Rome, Wikipedia · 150 ÷ 100 = 1,5 giorni"
    elif i == 24:
        tc = T("C'è") - 0.3; tu = T("una") - 0.2; tr = T("realizzata") - 0.2; td = T("Dai") - 0.3
        sc.add(Icon("question", (960, 480), a, tc, size=280), "pop")
        sc.add(Pieta((560, 860), 480, tu, None, label="COPIA (sagoma stilizzata)"))
        sc.add(Stamp("PRIMA DEL DANNO", (560, 330), tr, size=60, rot=-6))
        sc.add(Icon("mould", (1000, 520), td, size=220, label="CALCO"), "pop")
        sc.add(Arrow((660, 520), (880, 520), td + 0.2, color=GOLD))
        sc.add(Pieta((1460, 860), 480, td + 0.6, None, broken=True, label=SAG))
        sc.add(Arrow((1110, 520), (1330, 420), td + 0.9, color=GOLD))
        sc.add(Pill("LE FORME DELLE PARTI MANCANTI", (960, 215), td + 0.8, size=46, accent=True))
        sc.footer = "Fonti: Reuters (2013) · Mental Floss · Musei Vaticani (copia del 1930) · Finestre sull'Arte · " + SAG
    elif i == 25:
        tm = T("mescolata") - 0.2; tc = T("Così") - 0.3; tq = T("quasi") - 0.2; tn = T("Il") - 0.3; tb = T("e") - 0.2
        sc.add(Icon("glue", (560, 480), a, size=300, label="COLLA SPECIALE"), "pop")
        sc.add(Pill("+ POLVERE DI MARMO DI CARRARA", (960, 760), tm, tc, size=48, accent=True))
        sc.add(Pieta((1300, 870), 600, tc, None, broken=True, fix_t=tq + 0.2, label=SAG))
        sc.add(Pill("NASO RICOMPOSTO", (960, 215), tn, tb, size=48, accent=True))
        sc.add(Pill("BRACCIO AL SUO POSTO", (960, 215), tb, size=48, accent=True))
        sc.add(Stamp("RICOMPOSTA", (1680, 330), tb + 0.4, size=56, rot=-8, color=GOLD))
        sc.footer = "Fonti: Wikipedia · Wanted in Rome · Reuters (2013) · Finestre sull'Arte · Geopop · " + SAG
    elif i == 26:
        ts = T("arriva") - 0.2; tn = T("Nella") - 0.3; ti = T("i") - 0.2; tu = T("una", 1) - 0.2; tp = T("Per") - 0.3
        sc.add(Text("Una\n*sorpresa*", (960, 330), a, tn, size=110, anchor="ma", align="m"))
        sc.add(Pieta((700, 880), 600, tn, None, label=SAG))
        sc.add(Bubble((1360, 450), 230, ti, tu, inner="magnifier"))
        sc.add(Icon("letter_m", (1360, 450), tu, size=300), "hit")
        sc.add(Pill("UNA «M» NELLA MANO SINISTRA", (1360, 720), tu + 0.2, tp, size=44, accent=True))
        sc.add(Text("un'altra *firma*\nnascosta?", (1360, 640), tp, size=60, anchor="ma", align="m"))
        sc.footer = "Fonti: Wikipedia · Mental Floss · " + SAG
    elif i == 27:
        tc = T("Circa") - 0.3; tl = T("la") - 0.2; ta = T("A") - 0.3
        sc.add(Calendar((960, 480), 300, [(a, "MARZO", "25"), (a + 1.0, "1973", "25")], a, tc + 0.3), "paper")
        sc.add(Timeline(260, 1660, 300, TLE([(tc, "MAG 1972", "i colpi"), (tc + 0.8, "MAR 1973", "di nuovo visibile")]), tc, tl))
        sc.add(Pill("CIRCA 10 MESI", (960, 480), tc + 1.0, tl, size=56, accent=True))
        sc.add(Cappella(CB, tl, None, screen_t=a, screen_off=tl + 0.4), "whoosh")
        sc.add(Crowd((420, 780, 1500, 870), 14, tl + 0.8, None, s=0.34, seed=9))
        sc.add(Pill("I SEGNI NON SI VEDONO PIÙ", (960, 215), ta, size=48, accent=True))
        sc.footer = "Fonti: Il Post · Geopop · Finestre sull'Arte (25 marzo) · Wikipedia · " + SAG
    elif i == 28:
        td = T("Davanti") - 0.3; tda = T("Da") - 0.3; tn = T("Nel") - 0.3; tc = T("con") - 0.2
        sc.add(Text("Qualcosa\nè *cambiato*", (960, 330), a, td, size=110, anchor="ma", align="m"))
        sc.add(Cappella(CB, td, None, pk=dict(glass_t=td + 0.4)), "whoosh")
        sc.add(Pill("VETRO ANTIPROIETTILE", (960, 215), td + 0.5, tn, size=48, accent=True))
        sc.add(Crowd((420, 780, 1500, 870), 12, tda, None, s=0.34, seed=3))
        sc.add(Calendar((1720, 320), 180, [(tn, "VETRI NUOVI", "2024")], tn, None), "paper")
        sc.add(Pill("2024 · VETRI NUOVI, PIÙ TRASPARENTI", (960, 215), tn, size=46, accent=True))
        sc.add(Icon("shield", (300, 320), tc, size=170), "pop")
        sc.footer = "Fonti: Il Post · Wikipedia · Wanted in Rome · Reuters (2013) · Geopop (2024) · michelangelobuonarrotietornato (2024) · " + SAG
    elif i == 29:
        tv = T("vede") - 0.2; tm = T("Ma") - 0.3; tf = T("frammento") - 0.2; te = T("Ed") - 0.3
        sc.add(Crowd((260, 780, 1660, 870), 16, a, None, s=0.34, seed=5))
        sc.add(Pieta((960, 760), 560, a + 0.3, te, glass_t=a, label=SAG))
        sc.add(Pill("SEMBRA INTATTA", (960, 215), tv, tm, size=48, accent=True))
        sc.add(Frags((360, 260, 1560, 760), tm + 0.3, te, n=100, counter=False))
        sc.add(Pill("RICOMPOSTA · FRAMMENTO DOPO FRAMMENTO", (960, 215), tm + 0.3, te, size=46, accent=True))
        sc.add(Icon("shield", (960, 500), te, size=300), "hit")
        sc.add(Text("protetta come\npochissime *altre*", (960, 180), te + 0.4, size=64, anchor="ma", align="m"))
        sc.footer = "Fonti: Il Post · Wikipedia · Reuters (2013) · " + SAG
    elif i == 30:
        tu = T("Un") - 0.3; td = T("Una") - 0.3; tc = T("circa") - 0.2; tum = T("Un", 2) - 0.3; te = T("e") - 0.2
        sc.add(Text("*Ricapitolando*", (960, 200), a, None, size=80, anchor="ma"))
        sc.board({"op": dict(xy=(400, 470), t=tu, name="Michelangelo", role="23 anni · 1498"),
                  "pen": dict(xy=(960, 470), t=td, name="21 maggio 1972", role="Pentecoste"),
                  "fr": dict(xy=(1520, 470), t=tc, name="~100 frammenti", role="15 colpi circa"),
                  "to": dict(xy=(680, 730), t=tum, name="László Tóth", role="mai processato"),
                  "res": dict(xy=(1240, 730), t=te, name="marzo 1973", role="dietro il vetro")},
                 [("op", "pen", tum), ("pen", "fr", tum), ("pen", "to", te), ("fr", "res", te + 0.3)], tu, cw=220)
        sc.footer = "Fonti: Il Post · Finestre sull'Arte · Geopop · Wikipedia · Reuters · Musei Vaticani"
    elif i == 31:
        te = T("Era") - 0.3; to = T("o") - 0.2; tt = T("E") - 0.3; ti = T("Iscriviti") - 0.3
        sc.add(Text("Una domanda\nresta *aperta*", (960, 200), a, te, size=90, anchor="ma", align="m"))
        sc.add(Pieta((560, 860), 460, te, ti, label=SAG))
        sc.add(Pill("CANCELLARE OGNI TRACCIA?", (560, 290), te + 0.2, ti, size=42, accent=True))
        sc.add(Pieta((1360, 860), 460, to, ti, broken=True, label=SAG))
        sc.add(Pill("O LASCIARLE COME MEMORIA?", (1360, 290), to + 0.2, ti, size=42))
        sc.add(Icon("debate", (960, 560), tt, ti, size=200), "pop")
        sc.add(Img(cover_folder(520), (960, 520), ti, anim="drop"), "paper")
        sc.add(Pill("OGNI GIORNO UN NUOVO CASO", (960, 820), ti + 0.4, size=46, accent=True))
        sc.footer = "Iscriviti a Fascicolo Italia · le fonti sono nella descrizione"
    return sc

def thumbnail(path="thumbnail.jpg"):
    im = make_bg(7); d = ImageDraw.Draw(im)
    t = rich_img("LA PIETÀ\nE IL *MARTELLO*", SERIF, 124, WHITE, RED, lh=1.0)
    im.alpha_composite(t, (90, 190))
    lay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    Pieta((1440, 900), 700, 0, None, broken=True, label=None).draw(lay, 5.0, 1.0)
    im.alpha_composite(lay)
    fl = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    Frags((1080, 880, 1880, 1040), 0, None, n=60, counter=False).draw(fl, 1.0, 1.0)
    im.alpha_composite(fl)
    st = stamp_img("CASO 016", RED, 70, -10); im.alpha_composite(st, (90, 40))
    d.text((100, 640), "ROMA 1972: CIRCA 100 FRAMMENTI DA RICOMPORRE", font=font(OSW, 50, 600), fill=GOLD + (255,))
    d.text((1880, 1060), "sagoma stilizzata, non l'opera", font=font(COURR, 22), fill=(200, 190, 170, 255), anchor="rs")
    wm = wordmark(60, sub=False); im.alpha_composite(wm, (100, 960))
    im.convert("RGB").save(path, quality=92)
