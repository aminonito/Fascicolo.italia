import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from maj import *

W, H = 1920, 1080
FY = 870
SEAB = (160, 200, 1760, 860)   # scenografia: il mare di notte con il piroscafo
VE = (-66.0, 10.16)     # Valencia (Venezuela)
IT = (12.5, 41.9)       # Roma
BA = (-58.38, -34.6)    # Buenos Aires
GE = (10.4, 51.1)       # Germania
F_38 = "Fonti: Electra (Fundação EDP) · Focus · Il Post · E. Recami (arXiv)"
F_BINI = "Fonti: Avvenire · AGI · Il Fatto Quotidiano · ANSA"

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

def build(i, dur, a, words):
    T = Clock(words, a); sc = Scene(dur)
    if i == 0:
        ts = T("Un") - 0.3; tr = T("Ritira") - 0.2; tn = T("Poi") - 0.2
        sc.add(Calendar((960, 470), 300, [(a, "NAPOLI · MARZO 1938", "25")], a, ts), "paper")
        sc.add(Text("VENERDÌ", (960, 700), a + 0.2, ts, size=40, fnt=TYPE, color=GOLD, anchor="ma"))
        sc.add(Figure(walk([(-100, FY), (560, FY)], ts, 380), ts, tn, kind="suit", s=0.95, label="IL PROFESSORE"))
        sc.add(Figure([(0, 1300, FY)], T("studentessa") - 0.4, tr, kind="expert", s=0.85, label="STUDENTESSA"), "pop")
        sc.add(Icon("folder", (700, 560), T("cartellina") - 0.3, tr, size=170, move=(T("cartellina") + 0.2, 1.0, (1180, 560), 120)), "whoosh")
        sc.add(Pill("UNA CARTELLINA DI APPUNTI", (960, 220), T("cartellina") - 0.1, tr, size=40))
        for k in range(4):
            sc.add(Icon("money", (820 + k * 130, 520 + (k % 2) * 40), tr + 0.15 * k, tn, size=150), "pop")
        sc.add(Pill("MESI DI STIPENDIO MAI RISCOSSI", (960, 220), tr + 0.1, tn, size=40, accent=True))
        sc.add(Sea(SEAB, tn, T("trentun") - 0.3, ship=[(tn, .75), (T("trentun"), .45)], flip=-1, label="ricostruzione · schema"))
        sc.add(Pill("UNA NAVE PER PALERMO", (960, 230), T("nave") - 0.2, T("trentun") - 0.3, size=44))
        sc.add(Big("31 ANNI", (960, 480), T("trentun") - 0.2, T("nessuno") - 0.3, size=220, color=GOLD, fnt=OSW), "hit")
        tq = T("nessuno") - 0.3
        sc.add(Sea(SEAB, tq, None, ship=[(tq, .45), (dur, .1)], flip=-1, ghost=tq + 0.4))
        sc.add(Stamp("MAI PIÙ RIVISTO\nCON CERTEZZA", (960, 420), T("certezza") - 0.3, size=80, rot=-8))
        sc.footer = F_38
    elif i == 1:
        tq = T("Questo") - 0.3; tv = T("Vedremo") - 0.3
        sc.add(Img(person_card("ETTORE MAJORANA", "fisico · 1906", 300), (480, 520), a, tq, anim="drop", rot=-3), "paper")
        sc.add(Text("sagoma · nessuna foto reale", (480, 780), a + 0.2, tq, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Pill("PER ENRICO FERMI: UN GENIO", (1260, 300), T("Enrico") - 0.1, tq, size=44))
        sc.add(Text("come *Galileo* e *Newton*", (1260, 400), T("Galileo") - 0.2, tq, size=72, anchor="ma"))
        sc.add(Icon("question", (1260, 640), T("scomparsa") - 0.2, tq, size=170, label="UNO DEI GRANDI MISTERI D'ITALIA"), "pop")
        sc.add(Img(cover_folder(), (960, 520), tq + 0.1, tv, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 005", (1150, 300), T("fascicolo") + 0.2, tv, size=70, rot=-12))
        sc.add(Icon("envelope", (420, 480), tv + 0.1, size=210, label="GLI ULTIMI GIORNI"), "pop")
        sc.add(Icon("magnifier", (960, 480), T("ipotesi") - 0.2, size=210, label="LE IPOTESI"), "pop")
        sc.add(Icon("camera", (1500, 480), T("fotografia") - 0.3, size=210, label="LA FOTO · PROCURA 2015"), "pop")
        sc.footer = "Fonti: E. Recami (arXiv) · ANSA · Il Fatto Quotidiano · Avvenire"
    elif i == 2:
        tc = T("Ettore") - 0.35
        sc.add(Chapter("01", "Il *genio*", a, tc))
        tf = T("In") - 0.2; tr = T("Ettore", 1) - 0.3
        sc.add(MapEl((980, 170, 1820, 860), [(0, (14.0, 39.7), 112), (tr, (14.0, 39.7), 112), (dur, (13.6, 40.2), 104)], tc + 0.1,
                     routes=[dict(pts=["Catania", "Roma"], t=T("Roma") - 0.3, d=1.4, icon="person")],
                     pins=[dict(at="Catania", label="CATANIA", t=T("Catania") - 0.2, side="l"), dict(at="Roma", label="ROMA", t=T("Roma") - 0.1, side="l")],
                     title="mappa: Natural Earth"))
        sc.add(Calendar((300, 360), 220, [(tc, "5 AGOSTO", "1906")], tc + 0.2, tf), "paper")
        sc.add(Icon("atom", (300, 330), tf, T("Tra") - 0.2, size=170, label="SCIENZIATI"), "pop")
        sc.add(Icon("house", (620, 330), T("politici") - 0.3, T("Tra") - 0.2, size=170, label="POLITICI"), "pop")
        sc.add(Img(person_card("QUIRINO", "lo zio fisico", 220), (460, 470), T("Tra") - 0.1, tr, anim="drop", rot=3), "paper")
        sc.add(Pill("TENIAMO A MENTE QUESTO NOME", (460, 790), T("Teniamo") - 0.1, tr, size=36, accent=True))
        sc.add(Pill("INGEGNERIA", (460, 360), T("Ingegneria") - 0.3, size=56))
        sc.add(Line((300, 360), (620, 360), T("1928") + 0.2, color=RED, width=10))
        sc.add(Pill("FISICA · 1928", (460, 560), T("Fisica") - 0.2, size=60, accent=True))
        sc.footer = "Fonti: Il Post · Focus · Discovery UK · Avvenire"
    elif i == 3:
        tg = T("Intorno") - 0.3; tm = T("entra") - 0.6
        sc.add(Facade((420, 260, 1500, 760), a, None, label="ISTITUTO DI FISICA · VIA PANISPERNA, ROMA"))
        sc.add(Figure(walk([(-100, FY), (760, FY)], a + 0.4, 360), a + 0.4, kind="suit", s=0.95, label="ENRICO FERMI"))
        sc.add(Crowd((900, 780, 1480, 890), 4, tg, None, s=0.42, kinds=("expert", "suit", "man", "expert")))
        sc.add(Pill("I RAGAZZI DI VIA PANISPERNA", (960, 190), T("ragazzi") - 0.3, size=48, accent=True))
        sc.add(Figure(walk([(2020, FY), (1640, FY)], tm, 300), tm, kind="man", s=0.95, label="MAJORANA"))
        sc.add(Stamp("SI FA NOTARE", (1260, 560), T("notare") - 0.2, size=70, rot=-8))
        scene_cam(sc, (0, 960, 540, 1.0), (tm, 960, 540, 1.0), (dur, 1220, 560, 1.18))
        sc.footer = "Fonti: Il Post · Focus · Discovery UK"
    elif i == 4:
        tb = T("Poi") - 0.3
        sc.add(MapEl((120, 160, 1100, 890), [(0, (10.0, 46.6), 68), (dur, (10.2, 46.6), 70)], a,
                     routes=[dict(pts=["Roma", "Lipsia"], t=a + 0.4, d=1.8, icon="train")],
                     pins=[dict(at="Roma", label="ROMA", t=a, side="r"), dict(at="Lipsia", label="LIPSIA · 1933", t=T("Lipsia") - 0.2, side="r", color=RED)],
                     title="mappa: Natural Earth"))
        sc.add(Calendar((1450, 330), 220, [(a, "GERMANIA", "1933")], a + 0.2, T("Heisenberg") - 0.3), "paper")
        sc.add(Img(person_card("W. HEISENBERG", "fisica quantistica", 230), (1450, 420), T("Heisenberg") - 0.2, tb, anim="drop", rot=2), "paper")
        sc.add(Img(person_card("NIELS BOHR", "Copenaghen", 230), (1450, 420), tb, T("grandi") - 0.6, anim="drop", rot=-2), "paper")
        sc.add(Pill("COPENAGHEN", (1450, 760), tb + 0.3, T("grandi") - 0.6, size=40))
        tI = T("grandi") - 0.5
        sc.add(Crowd((1240, 720, 1700, 880), 4, tI, None, s=0.45, kinds=("expert", "suit", "expert", "man")))
        sc.add(Bubble((1470, 470), 130, tI + 0.2, inner="atom", text="MAJORANA"), "pop")
        sc.footer = "Fonti: Focus · Electra (Fundação EDP) · Discovery UK"
    elif i == 5:
        tg = T("Ma") - 0.3; te = T("Ebbene") - 0.2
        sc.add(Figure(walk([(-100, FY), (360, FY)], a, 360), a, kind="suit", s=1.0, arms=[(tg, "point")], label="ENRICO FERMI"))
        sc.add(Figure([(0, 1580, FY)], a + 0.4, kind="expert", s=0.9, label="UN COLLEGA", flip=-1), "pop")
        sc.add(Text("Scienziati di *vari livelli*...", (960, 300), T("Ci") - 0.2, tg, size=66, anchor="ma"))
        for k in range(3): sc.add(Bar(620, 440 + k * 90, 680, 50, [(T("livelli") - 0.3 + k * 0.2, 0.3 + 0.25 * k)], T("livelli") - 0.3, tg, color=GOLD))
        sc.add(Text("«Ma poi ci sono i *geni*,\ncome Galileo e Newton»", (960, 260), tg + 0.1, size=74, anchor="ma", align="m"))
        sc.add(Text("«Ebbene, Ettore era uno di quelli»", (960, 560), te, size=64, color=GOLD, anchor="ma"))
        sc.add(Stamp("GENIO", (960, 760), T("quelli") - 0.1, size=100, rot=-8))
        sc.footer = "Citazione riportata da G. Cocconi (1965) · Fonti: E. Recami (arXiv) · ANSA"
    elif i == 6:
        tc = T("Nel") - 0.35
        sc.add(Chapter("02", "La *cattedra*", a, tc))
        tn = T("i") - 0.3; tl_ = T("lavoro") - 0.6; te = T("nello") - 0.4
        sc.add(Img(doc_typed(620, 720, "IL NUOVO CIMENTO · 1937", ["Teoria simmetrica", "dell'elettrone", "e del positrone", "", "E. Majorana", "", "*neutrini e antineutrini*"]), (520, 520), tc + 0.1, te, anim="drop", rot=-2), "paper")
        sc.add(Icon("neutrino", (1300, 440), tn, te, size=240, label="NEUTRINI"), "pop")
        sc.add(Crowd((1000, 720, 1620, 880), 5, tl_, te, s=0.42, kinds=("expert", "suit", "man", "expert", "poet")))
        sc.add(Pill("STUDIATO ANCORA OGGI", (1300, 210), tl_ + 0.2, te, size=44, accent=True))
        sc.add(Text("Un riconoscimento *rarissimo*", (960, 440), te + 0.1, size=84, anchor="ma"))
        sc.footer = "Fonti: E. Recami (arXiv) · Electra (Fundação EDP)"
    elif i == 7:
        tl_ = T("grazie") - 0.3; tm = T("La") - 0.3
        sc.add(Facade((300, 240, 1000, 760), a, None, label="UNIVERSITÀ DI NAPOLI"))
        sc.add(Figure(walk([(-100, FY), (650, FY)], a + 0.2, 380), a + 0.2, kind="suit", s=0.95, label="PROF. MAJORANA"))
        sc.add(Pill("FISICA TEORICA", (650, 200), T("fisica") - 0.2, size=44))
        sc.add(Img(doc_typed(560, 600, "NOMINA · AUTUNNO 1937", ["Professore ordinario", "di Fisica teorica", "", "*fuori concorso*"]), (1430, 500), T("senza") - 0.3, anim="drop", rot=2), "paper")
        sc.add(Stamp("MERITI\nECCEZIONALI", (1430, 640), tl_ + 0.2, size=70, rot=-10))
        sc.add(Pill("COME GUGLIELMO MARCONI", (1430, 190), T("Marconi") - 0.5, size=44, accent=True))
        sc.footer = "Fonti: E. Recami (arXiv) · Electra (Fundação EDP)"
    elif i == 8:
        tv = T("e") - 0.2; tg = T("È") - 0.3; tp = T("Poi") - 0.3
        sc.add(Calendar((1600, 330), 220, [(a, "NAPOLI", "1938"), (tp + 0.6, "FEBBRAIO", "1938"), (tp + 1.3, "MARZO", "1938")], a), "paper")
        sc.add(Icon("hotel", (420, 520), tv, size=260, label="ALBERGO"), "pop")
        sc.add(Icon("museum", (1100, 540), a + 0.3, size=280, label="UNIVERSITÀ"), "pop")
        sc.add(Figure([(tv, 520, FY), (tv + 2.5, 960, FY), (tv + 3.5, 960, FY), (tv + 6, 540, FY), (tv + 7, 540, FY), (tv + 9.5, 960, FY)], tv, kind="suit", s=0.85))
        sc.add(Pill("GIOVANE · STIMATO · UNA CARRIERA DAVANTI", (760, 200), tg, tp, size=40))
        sc.add(ClockFace((1600, 700), 110, tp, start=8, speed=6))
        sc.add(Stamp("?", (760, 330), T("succede") - 0.1, size=120, rot=-8))
        sc.footer = "Fonti: Electra (Fundação EDP) · Focus · Discovery UK"
    elif i == 9:
        tc = T("Masacra") if False else T("passa") - 0.6
        sc.add(Chapter("03", "Il *25 marzo*", a, tc))
        tco = T("Consegna") - 0.3; ts = T("Secondo") - 0.3
        sc.add(Calendar((1640, 330), 220, [(tc, "VENERDÌ", "25"), (tc + 0.01, "MARZO 1938", "25")], tc), "paper")
        sc.add(Icon("museum", (900, 470), tc + 0.1, size=300, label="ISTITUTO DI FISICA · NAPOLI"), "pop")
        sc.add(Figure(walk([(-100, FY), (560, FY)], tc + 0.1, 380), tc + 0.1, kind="suit", s=0.95, arms=[(tco + 0.6, "hold")], label="MAJORANA"))
        sc.add(Figure([(0, 1260, FY)], tco, kind="expert", s=0.85, label="GILDA SENATORE", flip=-1), "pop")
        sc.add(Icon("folder", (700, 640), tco + 0.4, size=150, move=(T("cartellina") + 0.1, 1.0, (1150, 640), 100)), "whoosh")
        sc.add(Pill("CARTE SCIENTIFICHE", (920, 200), T("carte") - 0.2, ts, size=44))
        sc.add(Bubble((1580, 640), 110, ts + 0.2, text="NE PARLIAMO POI"), "pop")
        sc.add(Text("secondo il racconto della studentessa", (920, 200), ts, size=34, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = F_38
    elif i == 10:
        tp = T("E") - 0.3; td = T("Due") - 0.3
        sc.add(Img(doc_typed(560, 600, "UNIVERSITÀ DI NAPOLI", ["Stipendi arretrati", "", "gennaio · febbraio · marzo", "", "*mai riscossi fino al 25-3-1938*"]), (520, 500), a, td, anim="drop", rot=-2), "paper")
        for k in range(4): sc.add(Icon("money", (1100 + k * 140, 400 + (k % 2) * 50), a + 0.4 + 0.2 * k, td, size=150), "pop")
        sc.add(Pill("DIVERSI MESI DI STIPENDIO", (1310, 220), T("stipendio") - 0.2, td, size=42))
        sc.add(Icon("passport", (1300, 680), T("passaporto") - 0.4, td, size=220), "pop")
        sc.add(Text("secondo le ricostruzioni", (1300, 830), tp + 0.4, td, size=28, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Clues((360, 200, 1560, 860), [((700, 600), "money", "LO STIPENDIO", td + 0.1, -3), ((1220, 600), "passport", "IL PASSAPORTO", td + 0.5, 3)], td))
        sc.add(Pill("PESERANNO MOLTISSIMO", (960, 260), T("peseranno") - 0.2, size=44, accent=True))
        sc.footer = "Fonti: Focus · Electra (Fundação EDP)"
    elif i == 11:
        tf = T("Una") - 0.2; tc = T("E", 0) - 0.2; tq = T("Nella") - 0.3
        sc.add(Icon("envelope", (600, 480), tf, tq, size=240, label="ALLA FAMIGLIA"), "pop")
        sc.add(Icon("envelope", (1320, 480), tc, tq, size=240, label="AD ANTONIO CARRELLI"), "pop")
        sc.add(Figure([(0, 1620, FY)], tc + 0.2, tq, kind="suit", s=0.85, label="IL DIRETTORE"), "pop")
        sc.add(Text("Due *lettere*", (960, 220), a, tq, size=80, anchor="ma"))
        sc.add(Img(letter(760, 640, "Napoli, 25 marzo 1938", "Caro Carrelli,", "Ho preso una\n*decisione* che era\normai *inevitabile*."), (960, 520), tq, anim="drop", rot=-1), "paper")
        scene_cam(sc, (0, 960, 540, 1.0), (T("ho") - 0.2, 960, 540, 1.0), (dur, 940, 470, 1.25))
        sc.footer = "Fonti: E. Recami (arXiv) · Electra (Fundação EDP) · Discovery UK"
    elif i == 12:
        tq = T("Quella") - 0.3; tn = T("Una") - 0.3
        sc.add(Text("Parole che fanno\n*temere il peggio*", (960, 380), a, tq, size=90, anchor="ma", align="m"))
        sc.add(MapEl((220, 170, 1700, 870), [(0, (14.0, 39.6), 180), (dur, (13.9, 39.5), 190)], tq,
                     routes=[dict(pts=["Napoli", "Palermo"], t=T("Palermo") - 0.6, d=3.0, icon="ship")],
                     pins=[dict(at="Napoli", label="NAPOLI · 25 MARZO", t=tq + 0.2, side="r"), dict(at="Palermo", label="PALERMO", t=T("Palermo") - 0.1, side="l")],
                     title="mappa: Natural Earth · rotta schematica"))
        sc.add(Pill("UNA NOTTE NEL MAR TIRRENO", (1350, 560), tn, size=44, accent=True))
        sc.add(Icon("moon", (1560, 330), tn + 0.2, size=130), "pop")
        sc.footer = F_38
    elif i == 13:
        tc = T("Sabato") - 0.35
        sc.add(Chapter("04", "Il *piroscafo*", a, tc))
        tt = T("Non") - 0.3; ts = T("Poi") - 0.3
        sc.add(Calendar((300, 330), 200, [(tc, "SABATO · MARZO", "26")], tc + 0.1), "paper")
        sc.add(Img(telegram_img(820, 440, ["NON ALLARMARTI.", "SEGUE LETTERA."]), (960, 520), tc + 0.3, ts, anim="drop", rot=-1), "paper")
        sc.add(Pill("DA PALERMO", (960, 230), tt, ts, size=40))
        sc.add(Img(letter(640, 560, "Palermo, 26 marzo 1938", "Caro Carrelli,", "*tornerò* a Napoli.", seed=44), (760, 520), ts + 0.1, anim="drop", rot=2), "paper")
        sc.add(Stamp("HA CAMBIATO\nIDEA", (1420, 440), T("cambiato") - 0.2, size=80, rot=-8))
        sc.add(Text("lettera ricostruita · riassunto del contenuto", (760, 830), ts + 0.4, size=26, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: Electra (Fundação EDP) · Focus · Discovery UK"
    elif i == 14:
        tv = T("Il") - 0.2; tm = T("mattina") - 0.5
        sc.add(Sea(SEAB, a, None, ship=[(a, .82), (dur, .22)], flip=-1, dawn=tm + 0.3, label="ricostruzione · schema"))
        sc.add(Pill("TIRRENIA · DA PALERMO A NAPOLI · 26 MARZO", (960, 240), a + 0.3, tv, size=42))
        sc.add(ClockFace((1560, 380), 90, tv, tm, start=20, speed=2.2, label="TUTTA LA NOTTE"))
        sc.add(Calendar((330, 380), 180, [(tv, "MARZO", "26"), (tm, "DOMENICA", "27")], tv), "paper")
        sc.add(Pill("ARRIVO A NAPOLI · LA MATTINA DOPO", (960, 240), tm + 0.2, size=42, accent=True))
        sc.footer = "Fonti: Il Post · Focus · AGI"
    elif i == 15:
        tq = T("sceso") - 0.7; tn = T("Non") - 0.3; td = T("Da") - 0.3
        sc.add(Sea(SEAB, a, None, ship=[(a, .45), (dur, .42)], flip=-1, port="NAPOLI", deck=(a + 0.4, tq + 1.4), ghost=td))
        sc.add(Pill("È SCESO DALLA NAVE?", (720, 240), tq, size=40))
        sc.add(Pill("QUALCUNO L'HA VISTO?", (1240, 240), T("Qualcuno") - 0.2, size=40))
        sc.add(Icon("question", (1560, 560), T("Qualcuno") + 0.6, size=140), "pop")
        sc.add(Stamp("MAI CHIARITO", (960, 470), tn, size=90, rot=-8))
        sc.add(Pill("NESSUNA NOTIZIA CERTA", (960, 760), td + 0.3, size=48, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (tq, 960, 540, 1.0), (tq + 2.0, 900, 560, 1.2), (dur, 900, 560, 1.22))
        sc.footer = "Fonti: Electra (Fundação EDP) · Il Post · Discovery UK"
    elif i == 16:
        t1 = T("Uno") - 0.2; t2 = T("Due") - 0.2; t3 = T("Tre") - 0.2; tm = T("Messi") - 0.2
        sc.add(Text("Cosa sappiamo *davvero*?", (960, 165), a, size=72, anchor="ma"))
        sc.add(Clues((200, 270, 1720, 880), [((470, 600), "envelope", "DECISIONE\nINEVITABILE", t1, -3), ((900, 600), "telegram", "TORNERÒ\nA NAPOLI", t2, 2),
                                             ((1250, 620), "money", "STIPENDIO", t3, -2), ((1520, 600), "passport", "PASSAPORTO", t3 + 0.5, 3)],
                     a + 0.2, links=[(0, 1, tm), (1, 2, tm + 0.4), (2, 3, tm + 0.8)]))
        sc.add(Stamp("NON TORNA", (960, 800), T("stessa") - 0.2, size=80, rot=-6))
        sc.footer = "Fonti: Electra (Fundação EDP) · Focus · E. Recami (arXiv)"
    elif i == 17:
        tc = T("Passano") - 0.35
        sc.add(Chapter("05", "Le *ricerche*", a, tc))
        tf = T("La") - 0.3; tp = T("La", 1) - 0.3; tm = T("mare") - 0.5
        sc.add(Icon("bell" if False else "telegram", (960, 470), tc + 0.1, tf, size=260, label="ALLARME"), "pop")
        sc.add(Crowd((380, 760, 900, 890), 4, tf, tm, s=0.45, kinds=("man", "suit", "poet", "man")))
        sc.add(Pill("LA FAMIGLIA", (640, 640), tf + 0.2, tp, size=40))
        sc.add(MapEl((1000, 180, 1800, 840), [(0, (14.0, 39.6), 160), (dur, (14.0, 39.6), 166)], tp, tm,
                     pins=[dict(at="Napoli", label="NAPOLI", t=tp + 0.2, side="r"), dict(at="Palermo", label="PALERMO", t=tp + 0.5, side="l")], title="mappa: Natural Earth"))
        sc.add(Figure(walk([(-100, FY), (700, FY)], tp, 340), tp, tm, kind="police", s=0.95, carry=[(tp, "magnifier")], label="POLIZIA"))
        sc.add(Sea(SEAB, tm, None, ship=[(tm, .5), (dur, .5)], sw=0.18))
        sc.add(Stamp("NULLA", (960, 460), T("nulla") - 0.1, size=120, rot=-10))
        sc.footer = "Fonti: Focus · Discovery UK"
    elif i == 18:
        tn = T("Nell") - 0.3; tt = T("Tra") - 0.3
        sc.add(Crowd((560, 740, 1360, 890), 6, a, tn, s=0.42, kinds=("expert", "suit", "man", "expert", "poet", "suit")))
        sc.add(Pill("I COLLEGHI", (960, 300), a + 0.2, tn, size=48))
        sc.add(Figure([(0, 380, FY)], tn, kind="suit", s=0.95, arms=[(tn, "hold")], label="ENRICO FERMI"), "pop")
        sc.add(Icon("envelope", (560, 560), tn + 0.4, size=150, move=(T("Mussolini") - 0.2, 1.2, (1500, 400), 160)), "whoosh")
        sc.add(Pill("ESTATE 1938 · LETTERA A MUSSOLINI", (1100, 200), T("Mussolini") - 0.2, tt, size=40))
        sc.add(Pill("INTENSIFICARE LE RICERCHE", (1100, 280), T("intensificare") - 0.2, tt, size=40, accent=True))
        sc.add(Img(doc_typed(820, 520, "LETTERA DI E. FERMI · 1938 (estratto)", ["...fra tutti gli studiosi", "che ho conosciuto,", "quello che per *profondità*", "*d'ingegno* mi ha", "maggiormente colpito..."]), (1180, 520), tt, anim="drop", rot=-1), "paper")
        sc.footer = "Fonti: E. Recami (arXiv) · Focus"
    elif i == 19:
        tn = T("Nessuna") - 0.2; tp = T("Il") - 0.3
        sc.add(CardGrid((260, 200, 1660, 760), a, tp, cols=16, rows=7, scan=3.2))
        sc.add(Stamp("NESSUNA TRACCIA", (960, 470), tn, tp, size=90, rot=-8))
        sc.add(Pill("NESSUN TESTIMONE SICURO", (960, 820), T("testimone") - 0.3, tp, size=44))
        sc.add(Figure([(0, 960, FY)], tp, kind="man", s=1.05, label="?"), "pop")
        sc.add(Text("Scomparso *nel nulla*", (960, 220), tp + 0.2, size=80, anchor="ma"))
        sc.footer = "Fonti: Focus · Discovery UK · Il Post"
    elif i == 20:
        tc = T("Per") - 0.35
        sc.add(Chapter("06", "Le *ipotesi*", a, tc))
        tl1 = T("La") - 0.3; tm = T("telegramma") - 0.6; tp = T("E", 1) - 0.3
        sc.add(Sea(SEAB, tl1, tm, ship=[(tl1, .7), (tm, .4)], flip=-1))
        sc.add(Pill("IPOTESI 1 · IL MARE", (960, 240), tl1 + 0.1, size=48, accent=True))
        sc.add(Icon("telegram", (640, 520), tm, tp, size=230, label="TELEGRAMMA"), "pop")
        sc.add(Icon("envelope", (1280, 520), tm + 0.6, tp, size=230, label="«TORNERÒ»"), "pop")
        sc.add(Icon("money", (640, 520), tp, size=200), "pop")
        sc.add(Icon("passport", (1280, 520), tp + 0.4, size=200), "pop")
        sc.add(Stamp("PERCHÉ?", (960, 700), T("passaporto") - 0.1, size=100, rot=-8))
        sc.footer = "Fonti: Il Post · Focus · Discovery UK"
    elif i == 21:
        tn = T("Nel") - 0.3; ti = T("E") - 0.3; tf = T("forse") - 0.3
        sc.add(Pill("IPOTESI 2 · UN CONVENTO", (960, 220), a, size=48, accent=True))
        sc.add(Icon("convent", (960, 520), a + 0.2, tn, size=320), "pop")
        sc.add(Img(book_cover(360), (520, 540), tn, anim="drop", rot=-3), "paper")
        sc.add(Figure(walk([(1100, FY), (1500, FY)], ti, 120), ti, tf, kind="man", s=0.95, label="RITIRARSI DAL MONDO?"))
        sc.add(Icon("atom", (1450, 520), tf, size=240, label="LA PAURA DELL'ATOMO?"), "pop")
        sc.footer = "Fonti: Il Post · ANSA · Focus"
    elif i == 22:
        tc = T("C'è") - 0.3; tn = T("Ma") - 0.3
        sc.add(Pill("IPOTESI 3 · IL SUD AMERICA", (960, 200), a, size=48, accent=True))
        sc.add(WorldMap((160, 250, 1760, 880), a + 0.2, view=(-80, 40, -45, 62), hl=("Italy", "Argentina", "Germany"),
                        routes=[dict(a=IT, b=BA, t=T("dall'Arg") - 0.4, d=2.0, bend=0.18, icon="question")],
                        pins=[dict(at=BA, label="BUENOS AIRES?", t=T("Buenos") - 0.2, side="r"), dict(at=GE, label="GERMANIA?", t=tc + 0.2, side="t", color=REDL)]))
        sc.add(Stamp("MAI CONFERMATE", (960, 560), tn + 0.4, size=100, rot=-8))
        sc.footer = "Fonti: Il Post · Focus · Discovery UK"
    elif i == 23:
        tl_ = T("teorie") - 0.6; to = T("oggi") - 0.4
        sc.add(Icon("chalk", (960, 480), a, to, size=420), "pop")
        sc.add(Crowd((520, 760, 1400, 890), 6, a + 0.3, to, s=0.42, kinds=("expert", "man", "suit", "poet", "expert", "man")))
        sc.add(Pill("UNA LEGGENDA NELLE AULE DI FISICA", (960, 200), T("leggenda") - 0.4, tl_, size=44))
        sc.add(Pill("TEORIE RISCOPERTE", (960, 200), tl_ + 0.1, to, size=44, accent=True))
        sc.add(Icon("atom", (560, 500), to + 0.1, size=240), "pop")
        sc.add(Icon("neutrino", (1360, 500), to + 0.4, size=240), "pop")
        sc.add(Text("fermioni di *Majorana*", (960, 700), T("fermioni") - 0.2, size=90, anchor="ma"))
        sc.footer = "Fonti: E. Recami (arXiv) · Electra (Fundação EDP)"
    elif i == 24:
        tc = T("Alla") - 0.6
        sc.add(Chapter("07", "Il signor *Bini*", a, tc))
        tt = T("Un") - 0.3; tr = T("racconta") - 0.3
        sc.add(Calendar((300, 330), 200, [(tc, "SEGNALAZIONE", "2008")], tc + 0.1), "paper")
        sc.add(Icon("tv", (960, 480), tc + 0.1, tr, size=300, label="CHI L'HA VISTO? · RAI 3"), "pop")
        sc.add(Icon("phone", (1440, 420), tc + 0.6, tr, size=160), "pop")
        sc.add(Figure([(0, 300, FY)], tt, T("meccanico") - 0.3, kind="worker", s=0.9, label="FRANCESCO FASANI"), "pop")
        sc.add(Figure([(0, 300, FY)], T("meccanico") - 0.3, kind="worker", s=0.9, label="FASANI · MECCANICO"))
        sc.add(WorldMap((560, 180, 1820, 860), tr, view=(-80, 40, -15, 55), hl=("Italy", "Venezuela"),
                        routes=[dict(a=IT, b=VE, t=T("Venezuela") - 0.3, d=2.0, bend=0.15, icon="ship")],
                        pins=[dict(at=VE, label="VENEZUELA · ANNI '50", t=T("Venezuela") + 1.5, side="r")]))
        sc.add(Pill("«HO CONOSCIUTO MAJORANA»", (1190, 230), T("conosciuto") - 0.3, size=44, accent=True))
        sc.footer = F_BINI
    elif i == 25:
        tf = T("Fasani") - 0.3; tu = T("mezza") - 0.6; tg = T("Guida") - 0.3
        sc.add(WorldMap((160, 180, 1760, 880), a, tf, view=(-78, -55, 4, 14), hl=("Venezuela",), title="mappa: Natural Earth",
                        pins=[dict(at=VE, label="VALENCIA · VENEZUELA", t=a + 0.4, side="r")]))
        sc.add(Calendar((1600, 330), 200, [(a, "VALENCIA", "1955")], a + 0.3, tf), "paper")
        sc.add(Figure(walk([(2020, FY), (1250, FY)], tf, 340), tf, kind="suit", s=0.95, label="«SIGNOR BINI»"))
        sc.add(Figure([(0, 420, FY)], tf + 0.3, kind="worker", s=0.9, arms=[(T("tiene"), "up")], label="FASANI"), "pop")
        sc.add(Pill("RISERVATO · EVITA GLI ALTRI ITALIANI", (960, 220), tu, tg, size=40))
        sc.add(Icon("car", (830, 600), tg, size=340, label="STUDEBAKER GIALLA"), "pop")
        sc.footer = F_BINI
    elif i == 26:
        ts = T("Secondo") - 0.3; tq = T("Quell") - 0.3
        sc.add(Text("Chi è davvero il *signor Bini*?", (960, 190), a, ts, size=72, anchor="ma"))
        sc.board({"fas": dict(xy=(430, 560), name="F. FASANI", role="testimone", t=a + 0.2, rot=-3),
                  "car": dict(xy=(960, 560), name="«SIGNOR CARLO»", role="mai identificato", t=T("Carlo") - 0.3, rot=2, stamp=("MAI TROVATO", T("identificare") - 0.4)),
                  "bin": dict(xy=(1490, 560), name="«SIGNOR BINI»", role="Valencia · 1955", t=a + 0.6, rot=-2)},
                 [("fas", "car", T("Carlo")), ("car", "bin", tq + 0.4)], a)
        sc.add(Pill("= ETTORE MAJORANA?", (1490, 250), T("fisico") - 0.2, size=48, accent=True))
        sc.footer = F_BINI
    elif i == 27:
        tt = T("Tranne") - 0.2; th = T("Ha") - 0.3; ti = T("In") - 0.2; td = T("È") - 0.3
        sc.add(Icon("nophoto", (960, 480), a, tt, size=280), "pop")
        sc.add(Big("1 VOLTA", (960, 480), tt, th, size=200, color=GOLD, fnt=OSW), "hit")
        sc.add(Figure([(0, 420, FY)], th, kind="worker", s=0.9, label="FASANI"), "pop")
        sc.add(Figure([(0, 1500, FY)], th, kind="suit", s=0.9, label="BINI", flip=-1), "pop")
        sc.add(Icon("money", (560, 560), T("prestito") - 0.3, ti, size=150, move=(T("prestito"), 1.0, (1360, 560), 120)), "whoosh")
        sc.add(Pill("UN PRESTITO", (960, 220), T("prestito") - 0.2, ti, size=44))
        sc.add(Img(photo1955(440), (960, 500), ti, anim="drop", rot=-3), "paper")
        sc.add(Pill("12 GIUGNO 1955 · VALENCIA", (960, 190), td, size=44, accent=True))
        sc.footer = F_BINI + " · Focus"
    elif i == 28:
        tn = T("Nell") - 0.3; te = T("È") - 0.3; tp = T("Parla") - 0.3
        sc.add(Icon("car", (960, 520), a, tn + 1.5, size=380, label="L'AUTO DI BINI"), "pop")
        sc.add(Img(postcard(820), (960, 520), tn + 1.2, anim="drop", rot=-2), "paper")
        sc.add(Pill("CARTOLINA DEL 1920", (960, 210), T("cartolina") - 0.2, te, size=44))
        sc.add(Pill("FIRMA: QUIRINO MAJORANA · LO ZIO", (960, 210), te, size=44, accent=True))
        sc.add(Pill("A W. G. CONKLIN · USA", (960, 840), T("indirizzata") - 0.2, size=40))
        sc.add(Stamp("GRAVITÀ", (1500, 760), tp + 0.3, size=80, rot=-10))
        sc.footer = "Fonti: Avvenire · AGI · Focus"
    elif i == 29:
        tc = T("Dopo") - 0.35
        sc.add(Chapter("08", "La *procura*", a, tc))
        tr = T("carabinieri") - 0.4
        sc.add(Icon("gavel", (960, 470), tc + 0.1, tr, size=240, label="PROCURA DI ROMA"), "stamp")
        sc.add(Figure([(0, 220, FY)], tr, kind="police", s=0.85, carry=[(tr, "magnifier")], label="RIS"), "pop")
        sc.add(FaceCompare((420, 170, 1760, 880), tr + 0.2, feats=[(T("Fronte") - 0.1, "FRONTE"), (T("naso") - 0.1, "NASO"), (T("zigomi") - 0.1, "ZIGOMI"), (T("mento") - 0.1, "MENTO"), (T("orecchie") - 0.1, "ORECCHIE")],
                               overlay=T("risultato") - 0.2, right="FABIO MAJORANA · 50 ANNI"))
        sc.add(Stamp("PERFETTA\nSOVRAPPONIBILITÀ", (1090, 520), T("perfetta") - 0.1, size=74, rot=-8))
        sc.footer = F_BINI
    elif i == 30:
        tv = T("Ettore") - 0.3; ts = T("Si") - 0.3
        sc.add(Calendar((300, 330), 200, [(a, "FEBBRAIO", "2015")], a), "paper")
        sc.add(Figure([(0, 300, FY)], a + 0.3, kind="judge", s=0.85, label="P. LAVIANI"), "pop")
        sc.add(Img(doc_typed(900, 700, "PROCURA DI ROMA · CONCLUSIONI (sintesi)", ["Ettore Majorana era vivo", "almeno tra il *1955* e il *1959*,", "a Valencia (Venezuela).", "", "Trasferimento all'estero", "*volontario*.", "", "Nessun reato."]), (1160, 520), T("mette") - 0.2, anim="drop", rot=-1), "paper")
        sc.add(Stamp("VIVO", (1380, 330), tv + 0.4, size=90, color=(60, 150, 80), rot=-10))
        sc.add(Stamp("VOLONTARIO", (1380, 700), ts + 0.4, size=80, rot=-8))
        sc.add(Stamp("NESSUN REATO", (760, 760), T("Nessun") - 0.1, size=70, rot=6))
        sc.footer = F_BINI
    elif i == 31:
        tc = T("Cosa") - 0.3; tl_ = T("Le") - 0.3; tf = T("fine") - 0.5
        sc.add(Text("Restano *molte domande*", (960, 200), a, tc, size=80, anchor="ma"))
        sc.add(Timeline(260, 1660, 520, [dict(top="1938", bottom="scompare", t=tc, hl=True), dict(top="?", bottom="17 anni\nsenza tracce", t=tc + 0.6),
                                          dict(top="1955-1959", bottom="Valencia\n«signor Bini»", t=tc + 1.2), dict(top="?", bottom="dopo il 1959", t=T("dopo") - 0.2, hl=True)], tc, tl_))
        sc.add(Icon("envelope", (500, 520), tl_, size=170, move=(tl_ + 0.4, 1.4, (1420, 520), 140)), "whoosh")
        sc.add(Icon("question", (1560, 520), tl_ + 1.8, tf, size=150), "pop")
        sc.add(Pill("NESSUNA RISPOSTA DAL VENEZUELA", (960, 260), T("senza") - 0.4, tf, size=44))
        sc.add(Stamp("FINE\nSCONOSCIUTA", (960, 520), tf + 0.2, size=100, rot=-8))
        sc.footer = "Fonti: Il Fatto Quotidiano · Avvenire · AGI · ANSA"
    elif i == 32:
        tr = T("Un") - 0.3
        sc.add(Text("Ricapitolando", (960, 190), a, size=72, anchor="ma"))
        sc.add(Icon("money", (300, 500), tr + 0.6, size=200, label="LO STIPENDIO"), "pop")
        sc.add(Icon("passport", (640, 500), T("passaporto") - 0.2, size=200, label="IL PASSAPORTO"), "pop")
        sc.add(Icon("ship", (980, 500), T("nave") - 0.2, size=220, label="LA NAVE"), "pop")
        sc.add(Icon("envelope", (1310, 500), T("Due") - 0.2, size=200, label="DUE LETTERE"), "pop")
        sc.add(Icon("camera", (1640, 500), T("foto") - 0.3, size=200, label="LA FOTO DEL 1955"), "pop")
        sc.add(Pill("DECENNI DI IPOTESI", (960, 780), T("Decenni") - 0.2, size=44, accent=True))
        sc.footer = "Ricostruzione divulgativa · fonti nella descrizione"
    elif i == 33:
        ts = T("Iscriviti") - 0.3
        sc.add(Sea(SEAB, a, T("Scrivilo") - 0.2, ship=[(a, .6), (dur, .3)], flip=-1, ghost=a))
        sc.add(Pill("PERCHÉ HA SCELTO DI SPARIRE?", (960, 240), T("Secondo") - 0.1, T("Scrivilo") - 0.2, size=48, accent=True))
        sc.add(Bubble((960, 470), 170, T("Scrivilo") - 0.1, ts, text="COMMENTI"), "pop")
        sc.add(Text("Fonti nella descrizione", (960, 760), T("fonti") - 0.2, ts, size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(110), (960, 520), ts, anim="pop", shadow=False), "hit")
        sc.add(Text("ogni giorno un nuovo caso", (960, 700), T("ogni") - 0.2, size=54, fnt=PS, color=GOLD, anchor="ma"))
        sc.footer = "Ricostruzione divulgativa · voce generata con sintesi vocale"
    return sc


def thumbnail(path="thumbnail.jpg"):
    im = make_bg(7).convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    Sea((1000, 120, 1860, 960), -5, None, ship=((0, .55),), flip=-1, ghost=None, sw=0.62).draw(lay, 0.0, 1.0)
    im.alpha_composite(lay)
    q = mpic("question", 230); im.alpha_composite(q, (1600, 170))
    t = rich_img("IL GENIO\nCHE SCELSE\nDI *SPARIRE*", SERIF, 140, WHITE, RED, lh=1.0)
    im.alpha_composite(t, (90, 150))
    st = stamp_img("CASO 005", RED, 70, -10); im.alpha_composite(st, (700, 60))
    d = ImageDraw.Draw(im)
    d.text((100, 800), "ETTORE MAJORANA · NAPOLI 1938", font=font(OSW, 58, 600), fill=GOLD + (255,))
    wm = wordmark(60, sub=False); im.alpha_composite(wm, (100, 960))
    im.convert("RGB").save(path, quality=92)
