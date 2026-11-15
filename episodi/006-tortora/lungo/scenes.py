import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from tor import *

W, H = 1920, 1080
FY = 870
STB = (160, 170, 1760, 870)     # scenografia: lo studio TV
AUB = (160, 170, 1760, 870)     # aula
F_ARR = "Fonti: Il Post · AGI · Sky TG24 · Geopop"
F_ACC = "Fonti: Il Post · AGI · Wikipedia · Focus"
F_SENT = "Fonti: Il Post · Focus · AGI · Geopop · Wikipedia"

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

def build(i, dur, a, words):
    T = Clock(words, a); sc = Scene(dur)
    if i == 0:
        tc = T("I") - 0.3; tf = T("Poche") - 0.3; ta = T("L'accusa") - 0.3
        sc.add(Calendar((420, 420), 260, [(a, "ROMA · GIUGNO", "17"), (a + 1.2, "GIUGNO", "1983")], a, tc + 0.4), "paper")
        sc.add(ClockFace((1420, 420), 150, a + 0.3, tc + 0.4, start=3.9, speed=0.02, label="ORE 4 DEL MATTINO"))
        sc.add(Icon("moon", (920, 300), a + 0.5, tc + 0.4, size=150), "pop")
        sc.add(Door((1300, FY), 220, 420, tc, tf, open_t=T("famosi") - 0.3))
        sc.add(Figure(walk([(-120, FY), (820, FY)], tc, 420), tc, tf, kind="police", s=0.95, label="CARABINIERI"))
        sc.add(Figure(walk([(-260, FY), (640, FY)], tc, 420), tc, tf, kind="police", s=0.95))
        sc.add(Pill("UN VOLTO FAMOSISSIMO DELLA TV", (960, 220), T("famosi") - 0.3, tf, size=42, accent=True))
        sc.add(Img(newspaper(640, 680, "IL QUOTIDIANO", "18 giugno 1983", "Arrestato\n*il presentatore*", "blitz contro la camorra"), (600, 520), tf, ta + 0.3, anim="drop", rot=-3), "paper")
        sc.add(Icon("handcuffs", (1300, 470), T("manette") - 0.3, ta + 0.3, size=260), "pop")
        sc.add(Icon("camera", (1560, 300), T("giornali") - 0.4, ta + 0.3, size=150), "pop")
        sc.add(Flash(T("giornali") - 0.2))
        sc.add(Pill("ACCUSA: CAMORRA", (640, 340), ta, size=54, accent=True))
        sc.add(Pill("E TRAFFICO DI DROGA", (1280, 340), T("trafficare") - 0.2, size=54, accent=True))
        sc.add(Icon("gavel", (960, 620), ta + 0.3, size=260), "stamp")
        sc.footer = F_ARR
    elif i == 1:
        to = T("Ogni") - 0.3; tp = T("prova") - 0.6; tq = T("Questo") - 0.3; tv = T("Vedremo") - 0.3
        sc.add(Img(person_card("ENZO TORTORA", "giornalista e conduttore", 300), (480, 520), a, to + 2.6, anim="drop", rot=-3), "paper")
        sc.add(Text("sagoma · nessuna foto reale", (480, 780), a + 0.2, to + 2.6, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Icon("tv", (1300, 420), to, tp, size=280, label="OGNI VENERDÌ"), "pop")
        sc.add(Crowd((1020, 700, 1600, 880), 6, to + 0.4, tp, s=0.42))
        sc.add(Icon("addressbook", (1300, 460), tp, tq - 0.2, size=300, label="LA PROVA: UN'AGENDINA"), "pop")
        sc.add(Stamp("NON ERA\nIL SUO NOME", (960, 470), T("nemmeno") - 0.3, tq, size=80, rot=-8))
        sc.add(Img(cover_folder(), (960, 520), tq + 0.1, tv, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 006", (1150, 300), T("fascicolo") + 0.2, tv, size=70, rot=-12))
        sc.add(Icon("handcuffs", (330, 470), tv + 0.1, size=190, label="L'ARRESTO"), "pop")
        sc.add(Icon("question", (750, 470), T("gli") - 0.2, size=190, label="GLI ACCUSATORI"), "pop")
        sc.add(Icon("doily", (1170, 470), T("centrini") - 0.5, size=190, label="I CENTRINI"), "pop")
        sc.add(Icon("scales", (1590, 470), T("errori") - 0.6, size=190, label="L'ERRORE GIUDIZIARIO"), "pop")
        sc.footer = "Fonti: Il Post · Focus · Geopop"
    elif i == 2:
        tc = T("Enzo") - 0.3
        sc.add(Chapter("01", "*Portobello*", a, tc))
        ti = T("Alla") - 0.3; tpo = T("Portobello") - 0.3
        sc.add(Figure(walk([(-100, FY), (520, FY)], tc, 380), tc, kind="suit", s=1.0, label="ENZO TORTORA"))
        sc.add(Icon("mic", (760, 560), T("giornalista") - 0.2, ti, size=170), "pop")
        sc.add(Icon("tvcam", (1450, 520), T("conduttore") - 0.2, ti, size=300, label="RAI"), "pop")
        sc.add(Calendar((1450, 380), 220, [(ti, "FINE ANNI", "'70")], ti, tpo), "paper")
        sc.add(Icon("question", (1150, 420), T("diverso") - 0.3, tpo, size=150), "pop")
        sc.add(Studio((760, 200, 1820, 860), tpo, None, parrot=True, sign="PORTOBELLO"))
        sc.footer = "Fonti: Geopop · Wikipedia · Focus"
    elif i == 3:
        tm = T("È") - 0.3; tc = T("E") - 0.3; tz = T("centralini") - 0.3
        sc.add(Studio(STB, a, None, ring=(tc + 0.5, dur), sign="PORTOBELLO · VENERDÌ SERA"))
        sc.add(Calendar((1600, 380), 180, [(a, "OGNI", "VEN")], a + 0.3, tm), "paper")
        sc.add(Pill("IL MERCATINO IN DIRETTA", (960, 430), tm, tz, size=48, accent=True))
        for k, nm in enumerate(("easel", "glass", "frame_empty")):
            sc.add(Icon(nm, (560 + k * 260, 640), T("oggetti") - 0.3 + k * 0.25, tc, size=150), "pop")
        sc.add(Figure(walk([(-100, FY), (760, FY)], tm, 340), tm, tc, kind="man", s=0.9, label="CHI PORTA UN OGGETTO"))
        sc.add(Icon("house", (560, 560), tc, size=200, label="DA CASA"), "pop")
        sc.add(Arrow((680, 540), (1320, 680), tc + 0.4, color=GOLD, bend=-0.12, dashed=True))
        sc.add(Pill("CENTRALINI SENZA SOSTA", (1300, 430), tz, size=48))
        sc.footer = "Fonti: Geopop · Wikipedia"
    elif i == 4:
        tsc = T("Se") - 0.3; tp = T("Per") - 0.3; tu = T("Ci") - 0.3
        sc.add(Studio(STB, a, None, parrot=True))
        scene_cam(sc, (0, 960, 540, 1.0), (a + 0.3, 960, 540, 1.0), (a + 1.8, 520, 437, 1.5), (tu, 520, 437, 1.5), (tu + 1.0, 960, 540, 1.0), (dur, 960, 540, 1.0))
        sc.add(Bubble((820, 420), 70, tsc, tp, text="PORTOBELLO?"), "pop")
        sc.add(Icon("money", (900, 640), tsc + 0.6, tp, size=120), "pop")
        sc.add(Text("...", (820, 360), tp, tu, size=90, color=GREY, anchor="ma"))
        sc.add(Calendar((1200, 470), 260, [(tu, "UNA SOLA VOLTA", "1982")], tu + 0.6), "paper")
        sc.add(Text("si racconta", (1200, 680), tu + 1.0, size=34, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: Geopop · Focus · Wikipedia"
    elif i == 5:
        te = T("Elegante") - 0.3; tv = T("Un") - 0.3; tq = T("Ed") - 0.3
        sc.add(Figure([(0, 960, FY)], a, kind="suit", s=1.05, arms=[(te, "up")], label="ENZO TORTORA"), "pop")
        sc.add(Big("ALL'APICE", (960, 330), a + 0.2, te, size=130, color=GOLD, fnt=OSW), "hit")
        for k, w_ in enumerate(("ELEGANTE", "IRONICO", "AMATISSIMO")):
            sc.add(Pill(w_, (480 + k * 480, 260), te + k * 0.4, tv, size=44, accent=(k == 2)))
        sc.add(Crowd((220, 640, 700, 880), 5, tv, None, s=0.42)); sc.add(Crowd((1220, 640, 1700, 880), 5, tv + 0.2, None, s=0.42, seed=7))
        for k in range(6): sc.add(Icon("house", (300 + k * 264, 330), tv + 0.15 * k, tq, size=110), "pop")
        sc.add(Icon("handcuffs", (960, 300), tq + 1.2, size=180), "pop")
        sc.add(Pill("NEL GIRO DI UNA NOTTE", (960, 450), tq + 0.6, size=42, accent=True))
        sc.footer = "Fonti: Il Post · Geopop"
    elif i == 6:
        tc = T("Il") - 0.3
        sc.add(Chapter("02", "L'alba del *17 giugno*", a, tc))
        tcu = T("il", 1) - 0.3; tb = T("È") - 0.3
        sc.add(Calendar((300, 330), 200, [(tc, "GIUGNO", "17"), (tc + 0.8, "GIUGNO", "1983")], tc), "paper")
        sc.add(Pill("OPERAZIONE CONTRO LA NUOVA CAMORRA ORGANIZZATA", (1000, 220), T("grande") - 0.2, tb, size=40))
        sc.add(Img(person_card("RAFFAELE CUTOLO", "capo della NCO", 240), (1000, 500), tcu, tb, anim="drop", rot=2), "paper")
        sc.add(MapEl((560, 170, 1760, 880), [(0, (11.8, 42.6), 100), (dur, (11.8, 42.6), 104)], tb,
                     pins=[dict(at="Napoli", label="NAPOLI", t=tb + 0.2, side="r"), dict(at="Roma", label="ROMA", t=tb + 0.4, side="l"),
                           dict(at="Milano", label="MILANO", t=tb + 0.6, side="r"), dict(at="Torino", label="TORINO", t=tb + 0.8, side="l")],
                     title="mappa: Natural Earth"))
        sc.add(Pill("BLITZ IN TUTTA ITALIA", (1160, 820), tb + 0.4, size=44, accent=True))
        sc.footer = F_ARR
    elif i == 7:
        tn = T("Un") - 0.3; to = T("fretta") - 0.6
        sc.add(Big("856", (960, 380), a + 0.2, to, size=260, color=GOLD, fnt=OSW, count=(0, 856, lambda v: f"{int(v)}", 2.2), sub="ARRESTATI IN UN GIORNO"), "hit")
        sc.add(Crowd((200, 640, 1720, 890), 40, a + 0.4, to, s=0.3, stagger=0.03))
        sc.add(Stamp("UN NUMERO\nENORME", (1500, 300), tn, to, size=60, rot=-8))
        sc.add(Img(card_box(["Mario Rossi", "*Mario Rossi*"], 520, 220, "STESSO NOME"), (560, 470), to + 0.4, anim="drop", rot=-2), "paper")
        sc.add(Arrow((840, 470), (1150, 470), to + 1.2, color=REDL))
        sc.add(Figure([(0, 1380, FY)], T("persone", 1) - 0.4, kind="man", s=0.9, label="L'OMONIMO"), "pop")
        sc.add(Text("secondo le ricostruzioni · nomi di esempio", (960, 230), to + 0.2, size=30, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: Il Post · AGI · Sky TG24"
    elif i == 8:
        tv = T("Verso") - 0.3; tm = T("Il") - 0.3; tl_ = T("Le") - 0.3
        sc.add(MapEl((160, 170, 1000, 880), [(0, (12.6, 41.6), 160), (dur, (12.9, 41.4), 170)], a,
                     routes=[dict(pts=["Napoli", "Roma"], t=tm + 0.2, d=1.4, icon="envelope")],
                     pins=[dict(at="Roma", label="ROMA", t=a + 0.2, side="l"), dict(at="Napoli", label="NAPOLI", t=tm, side="b", color=RED)],
                     title="mappa: Natural Earth"))
        sc.add(ClockFace((1400, 330), 120, tv, tl_, start=3.85, speed=0.02, label="ORE 4"))
        sc.add(Figure(walk([(2020, FY), (1500, FY)], tv, 380), tv, tl_, kind="police", s=0.9, label="CARABINIERI"))
        sc.add(Figure(walk([(2160, FY), (1700, FY)], tv, 380), tv, tl_, kind="police", s=0.9))
        sc.add(Img(doc_typed(600, 500, "PROCURA DI NAPOLI · 1983", ["Ordine di cattura", "", "ENZO TORTORA", "", "*associazione camorristica*", "*traffico di droga*"]), (1380, 430), tl_, anim="drop", rot=2), "paper")
        sc.footer = F_ARR
    elif i == 9:
        tm = T("viene") - 0.6; tg = T("giorno") - 0.6; tp = T("Per") - 0.3
        sc.add(Text("Il momento che *nessuno*\ndimenticherà", (960, 330), a, tm, size=80, anchor="ma", align="m"))
        sc.add(Figure(walk([(700, FY), (1240, FY)], tm, 110), tm, tg + 0.3, kind="suit", s=1.0, arms=[(tm, "hold")], label="TORTORA"))
        sc.add(Figure(walk([(560, FY), (1100, FY)], tm, 110), tm, tg + 0.3, kind="police", s=0.95))
        sc.add(Icon("handcuffs", (900, 700), T("manette") - 0.2, tg + 0.3, size=120), "pop")
        for k in range(4):
            sc.add(Icon("camera", (330 + k * 420, 300 + (k % 2) * 70), T("fotografi") - 0.3 + k * 0.15, tg + 0.3, size=130), "pop")
            sc.add(Flash(T("fotografi") + k * 0.5, 0.25))
        sc.add(Icon("tvcam", (1700, 560), T("telecamere") - 0.3, tg + 0.3, size=200), "pop")
        for k in range(3):
            sc.add(Img(newspaper(440, 500, "IL QUOTIDIANO" if k != 1 else "CRONACA", "18-6-1983", "*Tortora*\nin manette", "ricostruzione", seed=k + 3), (440 + k * 520, 520), tg + k * 0.3, tp + 0.4, anim="drop", rot=(-4, 2, -2)[k]), "paper")
        sc.add(Crowd((300, 700, 1620, 890), 12, tp, None, s=0.38))
        sc.add(Stamp("COLPEVOLE?", (960, 400), T("già") - 0.2, size=110, rot=-8))
        sc.footer = "Fonti: AGI · Geopop · Il Post"
    elif i == 10:
        tc = T("Le") - 0.3
        sc.add(Chapter("03", "Gli *accusatori*", a, tc))
        tp = T("le", 1) - 0.3; td = T("detenuti") - 0.3
        sc.add(Icon("question", (960, 470), tc, tp, size=240, label="SU COSA SI BASANO LE ACCUSE?"), "pop")
        sc.add(Icon("prison", (480, 520), tp, size=300, label="CARCERE"), "pop")
        sc.add(Figure([(0, 1100, FY)], tp + 0.2, kind="man", s=0.85, label="PENTITO"), "pop")
        sc.add(Figure([(0, 1400, FY)], tp + 0.4, kind="man", s=0.85, label="PENTITO"), "pop")
        sc.add(Figure([(0, 1700, FY)], tp + 0.6, kind="man", s=0.85, label="PENTITO"), "pop")
        sc.add(Bubble((1400, 330), 110, td, text="COLLABORO"), "pop")
        sc.add(Pill("COLLABORATORI DI GIUSTIZIA", (960, 210), td + 0.2, size=44, accent=True))
        sc.footer = F_ACC
    elif i == 11:
        tb = T("Poi") - 0.3; tm = T("E") - 0.3
        sc.board({"pan": dict(xy=(420, 560), name="G. PANDICO", role="il primo nome", t=a + 0.2, rot=-3),
                  "bar": dict(xy=(960, 560), name="P. BARRA", role="«i locali di Milano»", t=tb, rot=2),
                  "mel": dict(xy=(1500, 560), name="G. MELLUSO", role="«consegne di droga»", t=tm, rot=-2)},
                 [("pan", "bar", tb + 0.3), ("bar", "mel", tm + 0.3)], a)
        sc.add(Pill("ACCUSATORI · PENTITI DELLA CAMORRA", (960, 210), a + 0.3, size=40))
        sc.add(Icon("moon", (960, 300), T("notturni") - 0.4, tm, size=90), "pop")
        sc.add(Text("dichiarazioni poi ritenute non credibili in appello", (960, 860), tm + 1.0, size=28, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = F_ACC
    elif i == 12:
        tn = T("Alla") - 0.3; tv = T("Diciannove") - 0.3; tmo = T("Sembra") - 0.3; tpa = T("Ma") - 0.3
        sc.add(Crowd((260, 600, 1660, 880), 19, a + 0.3, tmo, s=0.4, stagger=0.12))
        sc.add(Big("19", (960, 360), tn + 0.5, tmo, size=240, color=GOLD, fnt=OSW, sub="PERSONE FANNO IL SUO NOME"), "hit")
        sc.add(Figure([(0, 1760, FY)], tv, tmo, kind="suit", s=0.8, label="1"), "pop")
        sc.add(Pill("19 CONTRO 1", (1480, 220), tv + 0.3, tmo, size=48, accent=True))
        for k in range(19):
            sc.add(Icon(rich_cached("«...»", fnt=SERIF, size=56, color=WHITE), (960 + (k % 5 - 2) * 140, 820 - (k // 5) * 110), tmo + k * 0.06, size=60), None)
        sc.add(Text("solo *parole*", (960, 200), tpa + 0.3, size=100, anchor="ma"))
        sc.footer = F_ACC
    elif i == 13:
        tn = T("E") - 0.3; tp = T("Passa") - 0.3; tg = T("Il") - 0.3
        sc.add(MapEl((160, 170, 1000, 880), [(0, (11.0, 43.6), 110), (dur, (10.8, 43.8), 114)], a,
                     routes=[dict(pts=["Roma", "Bergamo"], t=a + 0.5, d=1.8, icon="person")],
                     pins=[dict(at="Roma", label="ROMA", t=a + 0.2, side="r"), dict(at="Bergamo", label="CARCERE DI BERGAMO", t=T("Bergamo") - 0.2, side="r", color=RED)],
                     title="mappa: Natural Earth"))
        sc.add(Icon("bars", (1400, 450), T("carcere") - 0.2, tg, size=320), "pop")
        sc.add(Bubble((1680, 300), 100, tn, tp, text="INNOCENTE"), "pop")
        sc.add(Calendar((1400, 480), 260, [(tp, "IN CELLA", "7 mesi"), (tg, "17 GENNAIO", "1984")], tp), "paper")
        sc.add(Icon("house", (1400, 780), T("arresti") - 0.2, size=140, label="ARRESTI DOMICILIARI"), "pop")
        sc.footer = "Fonti: Il Post · Wikipedia · Focus"
    elif i == 14:
        tc = T("Durante") - 0.3
        sc.add(Chapter("04", "L'*agendina*", a, tc))
        ta = T("un'agendina") - 0.4; tt = T("Alla") - 0.3
        sc.add(Icon("house", (420, 520), tc, ta + 0.5, size=260, label="PERQUISIZIONE"), "pop")
        sc.add(Figure(walk([(-100, FY), (700, FY)], tc, 380), tc, ta + 0.5, kind="police", s=0.9, carry=[(tc, "magnifier")]))
        sc.add(Icon("addressbook", (1300, 500), ta, tt + 0.4, size=360), "pop")
        sc.add(Img(agenda_img(900, 520), (960, 500), tt + 0.2, anim="drop", rot=-1), "paper")
        scene_cam(sc, (0, 960, 540, 1.0), (tt + 0.8, 960, 540, 1.0), (dur, 820, 500, 1.35))
        sc.footer = "Fonti: Focus · Il Post · AGI · Geopop"
    elif i == 15:
        tr = T("Quel") - 0.3; tn = T("È") - 0.3; tpz = T("Lo") - 0.3; tnu = T("numero") - 0.5
        sc.add(Img(lettere(900, 220, "TORTORA", 5), (960, 340), tr, anim="pop", shadow=False))
        sc.add(Line((520, 340), (1400, 340), tn - 0.1, color=RED, width=10))
        sc.add(Img(lettere(900, 220, "TORTONA", 5, color=GOLD), (960, 600), tn, anim="pop", shadow=False), "hit")
        sc.add(Pill("CON LA ERRE", (300, 340), tr + 0.4, size=40))
        sc.add(Pill("CON LA ENNE", (300, 600), tn + 0.3, size=40, accent=True))
        sc.add(Figure([(0, 1700, FY)], tpz, kind="expert", s=0.85, carry=[(tpz, "magnifier")], label="PERITO"), "pop")
        sc.add(Stamp("PERIZIA\nCALLIGRAFICA", (1640, 300), tpz + 0.6, size=50, rot=-10))
        sc.add(Icon("phone", (960, 790), tnu, size=120), "pop")
        sc.add(Stamp("NON È IL SUO", (1300, 790), T("presentatore") - 0.2, size=56, rot=-6))
        sc.footer = "Fonti: Focus · AGI · Il Post · Geopop"
    elif i == 16:
        ts = T("Secondo") - 0.3; tu = T("Una") - 0.3; tf = T("E") - 0.3
        sc.add(Text("Il dettaglio più *incredibile*", (960, 220), a, ts, size=76, anchor="ma"))
        sc.add(Img(agenda_img(700, 460, seed=11), (600, 560), a + 0.3, tu, anim="drop", rot=-2), "paper")
        sc.add(Icon("phone", (1350, 520), ts, size=260), "pop")
        sc.add(Stamp("NESSUNO\nCHIAMA", (1350, 520), T("compone") - 0.2, tu, size=70, rot=-10))
        sc.add(Big("1 TELEFONATA", (960, 330), tu, tf, size=130, color=GOLD, fnt=OSW), "hit")
        sc.add(ClockFace((600, 560), 140, tf, start=4.5, speed=0.6, label="IL PRIMO GIORNO"))
        sc.add(Pill("E FORSE SAREBBE FINITA QUI", (960, 220), tf + 0.3, size=48, accent=True))
        sc.footer = "Fonti: Il Post · Sky TG24 · Focus"
    elif i == 17:
        tc = T("Perché") - 0.3
        sc.add(Chapter("05", "I *centrini*", a, tc))
        tr = T("La") - 0.3
        sc.add(Icon("prison", (480, 500), tc, size=260, label="UN DETENUTO"), "pop")
        sc.add(Arrow((660, 480), (1200, 480), tc + 0.8, color=REDL, bend=-0.1))
        sc.add(Figure([(0, 1400, FY)], tc + 0.6, tr, kind="suit", s=0.95, label="TORTORA"), "pop")
        sc.add(Icon("question", (1400, 330), tc + 1.0, tr, size=140), "pop")
        sc.add(Icon("envelope", (1400, 470), tr, size=260, label="UN PACCO"), "pop")
        sc.add(Icon("doily", (1400, 470), T("centrini") - 0.2, size=220), "pop")
        sc.footer = "Fonti: Il Post · AGI · Sky TG24"
    elif i == 18:
        tm = T("perché") - 0.3; tn = T("non") - 0.3; tpe = T("E") - 0.3; tsc = T("E", 1) - 0.3
        sc.add(Icon("prison", (330, 470), a, size=240, label="IL CARCERE"), "pop")
        sc.add(Icon("crochet", (330, 760), a + 0.4, size=120), "pop")
        sc.add(Studio((1000, 230, 1800, 860), a + 0.6, None, parrot=False, sign="PORTOBELLO"))
        for k in range(3): sc.add(Icon("doily", (560 + k * 60, 520 + k * 30), T("centrini") - 0.3 + k * 0.2, size=150, move=(T("all'uncinetto") + k * 0.15, 1.6, (1220 + k * 110, 700), 160)), "whoosh")
        sc.add(Pill("PER ESSERE MOSTRATI IN TV", (960, 200), tm, tn, size=44))
        sc.add(Stamp("MAI IN ONDA", (1400, 480), tn + 0.2, size=70, rot=-8))
        sc.add(Stamp("PERSI", (1400, 590), tpe + 0.2, size=70, rot=6))
        sc.add(Icon("envelope", (360, 470), tsc, size=180, move=(tsc + 0.3, 1.2, (900, 330), 100)), "whoosh")
        sc.add(Pill("LETTERE DI PROTESTA", (900, 200), tsc + 0.5, size=44, accent=True))
        sc.footer = "Fonti: Il Post · AGI"
    elif i == 19:
        tl_ = T("la") - 0.3; tma = T("Ma") - 0.3; te = T("Erano") - 0.3; tp = T("Pandico", 1) - 0.4
        sc.add(Text("Per l'accusa:", (960, 190), a, tma, size=56, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Icon("doily", (720, 500), a + 0.2, tp, size=260), "pop")
        sc.add(Arrow((880, 500), (1080, 500), tl_, te, color=REDL))
        sc.add(Pill("= UN CODICE PER LA DROGA?", (1340, 500), tl_ + 0.2, tma, size=44, accent=True))
        sc.add(Figure([(0, 1500, FY)], tma, kind="man", s=0.9, label="EX COMPAGNO DI CELLA"), "pop")
        sc.add(Bubble((1180, 330), 110, tma + 0.6, te, text="UN'ALTRA STORIA"), "pop")
        sc.add(Stamp("DAVVERO\nCENTRINI", (720, 500), te + 0.2, tp, size=80, rot=-8))
        sc.add(Img(person_card("G. PANDICO", "«ignorato»", 260), (720, 500), tp, anim="drop", rot=3), "paper")
        sc.add(Text("secondo la testimonianza riportata dalle cronache", (960, 860), tp + 0.5, size=26, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: Il Post · AGI"
    elif i == 20:
        tc = T("Nel") - 0.3
        sc.add(Chapter("06", "La *condanna*", a, tc))
        tel = T("eletto") - 0.6; to = T("Ora") - 0.3
        sc.add(Icon("house", (360, 520), tc, to, size=220, label="AI DOMICILIARI"), "pop")
        sc.add(Calendar((960, 420), 240, [(tc + 0.4, "GIUGNO", "1984")], tc + 0.4, to), "paper")
        sc.add(Icon("ballot", (1500, 470), T("elezioni") - 0.3, to, size=280, label="ELEZIONI EUROPEE"), "pop")
        sc.add(Stamp("ELETTO", (1500, 470), tel + 0.2, to, size=90, rot=-8, color=(60, 150, 80)))
        sc.add(MapEl((160, 170, 1000, 880), [(0, (9.0, 46.0), 60), (dur, (9.0, 46.2), 62)], to,
                     routes=[dict(pts=["Milano", "Strasburgo"], t=to + 0.3, d=1.4, icon="person")],
                     pins=[dict(at="Strasburgo", label="STRASBURGO", t=to + 0.4, side="r")], title="mappa: Natural Earth"))
        sc.add(Icon("parliament", (1380, 500), to + 0.4, size=360), "pop")
        sc.footer = "Fonti: Il Post · Wikipedia · Focus"
    elif i == 21:
        tg = T("Al") - 0.3; ta = T("Gli") - 0.3; tc_ = T("E") - 0.3
        sc.add(Aula(AUB, a, None, judges_t=a + 0.4, cage_t=tg, who=None))
        sc.add(Pill("TRIBUNALE DI NAPOLI", (420, 230), a + 0.3, tg, size=44))
        sc.add(Pill("LA GABBIA DEGLI IMPUTATI", (420, 230), tg + 0.2, ta, size=40, accent=True))
        sc.add(Crowd((620, 760, 1100, 890), 4, ta, None, s=0.42, kinds=("man",)))
        sc.add(Bubble((860, 560), 90, ta + 0.3, tc_ + 0.4, text="ACCUSE"), "pop")
        sc.add(Figure(walk([(2020, FY), (1500, FY)], tc_ - 0.6, 420), tc_ - 0.6, kind="suit", s=0.95, arms=[(tc_ + 0.4, "point")], flip=-1, label="TORTORA"))
        sc.add(Bubble((1150, 600), 110, T("contesta") - 0.2, text="NON È VERO"), "pop")
        sc.footer = "Fonti: Il Post · Wikipedia"
    elif i == 22:
        ts = T("La") - 0.3; tc = T("Enzo") - 0.3; tm = T("multa") - 0.6
        sc.add(Calendar((300, 330), 220, [(a, "SETTEMBRE", "17"), (a + 0.9, "SETTEMBRE", "1985")], a), "paper")
        sc.add(Aula((560, 170, 1760, 870), a, None, judges_t=a + 0.2, cage_t=a + 0.2, who=True))
        sc.add(Icon("gavel", (1660, 330), ts, size=140), "stamp")
        sc.add(Big("10 ANNI", (1160, 520), tc + 0.3, size=200, color=WHITE, fnt=OSW), "hit")
        sc.add(Stamp("CONDANNATO", (1160, 700), tc + 0.6, size=80, rot=-8))
        sc.add(Img(card_box(["multa", "*50 milioni di lire*"], 460, 200), (360, 700), tm, anim="drop", rot=-2), "paper")
        sc.footer = "Fonti: Il Post · Focus · Wikipedia · Geopop"
    elif i == 23:
        tdm = T("Si") - 0.3; ti = T("rinuncia") - 0.3; tt = T("torna") - 0.5
        sc.add(Figure([(0, 520, FY)], a, kind="suit", s=1.0, label="TORTORA"), "pop")
        sc.add(Text("Una *scelta*", (960, 210), a, tdm, size=80, anchor="ma"))
        sc.add(Icon("parliament", (1300, 470), tdm - 0.2, tt, size=320), "pop")
        sc.add(Img(doc_typed(520, 420, "LETTERA DI DIMISSIONI", ["dal Parlamento", "europeo", "", "*rinuncia all'immunità*"]), (1300, 500), tdm + 0.4, tt, anim="drop", rot=2), "paper")
        sc.add(Stamp("SENZA IMMUNITÀ", (1300, 760), ti + 0.4, tt, size=60, rot=-6))
        sc.add(Icon("house", (1300, 480), tt, size=300, label="DI NUOVO AI DOMICILIARI"), "pop")
        sc.footer = "Fonti: Il Post · Sky TG24"
    elif i == 24:
        tc = T("Si") - 0.3
        sc.add(Chapter("07", "L'*assoluzione*", a, tc))
        tg = T("giudici") - 0.4; te = T("E") - 0.3
        sc.add(Calendar((300, 330), 200, [(tc, "MAGGIO", "1986")], tc), "paper")
        sc.add(Aula((560, 170, 1760, 870), tc, None, judges_t=tc + 0.3, cage_t=None, motto=False))
        sc.add(Pill("CORTE D'APPELLO DI NAPOLI", (1160, 210), tc + 0.3, size=40))
        for k in range(5):
            sc.add(Img(doc_typed(220, 260, f"VERBALE {k + 1}", ["...", "...", "..."], size=26), (700 + k * 240, 700), tg + k * 0.25, anim="drop", rot=(-3, 2, -1, 3, -2)[k]), "paper")
        sc.add(Arrow((700, 560), (1660, 560), te + 0.2, color=GOLD, bend=0.06, dashed=True))
        sc.add(Icon("magnifier", (1180, 460), te, size=160), "pop")
        sc.footer = "Fonti: Il Post · Geopop"
    elif i == 25:
        tas = T("La") - 0.3; t1 = T("Per") - 0.3; t2 = T("Per", 1) - 0.3; tf = T("Formula") - 0.3
        sc.add(Calendar((300, 330), 220, [(a, "SETTEMBRE", "15"), (a + 0.9, "SETTEMBRE", "1986")], a), "paper")
        sc.add(Aula((560, 170, 1760, 870), a, tf, judges_t=a, cage_t=None))
        sc.add(Icon("gavel", (1660, 330), tas + 0.3, tf, size=140), "stamp")
        sc.add(Stamp("ASSOLTO", (1160, 470), tas + 1.0, tf, size=110, rot=-8, color=(60, 150, 80)))
        sc.add(Pill("CAMORRA: NON HA COMMESSO IL FATTO", (1160, 640), t1, tf, size=40))
        sc.add(Pill("DROGA: IL FATTO NON SUSSISTE", (1160, 740), t2, tf, size=40))
        sc.add(Big("FORMULA PIENA", (960, 470), tf + 0.1, size=170, color=GOLD, fnt=OSW), "hit")
        sc.add(Figure([(0, 960, FY)], tf + 0.3, kind="suit", s=0.8, arms=[(tf + 0.6, "up")]), "pop")
        sc.footer = "Fonti: Il Post · Focus · AGI · Sky TG24"
    elif i == 26:
        tn = T("Nel") - 0.3; tl_ = T("L'assoluzione") - 0.3; td = T("Dopo") - 0.3
        sc.add(Crowd((300, 640, 1000, 880), 6, a, tn, s=0.42, kinds=("man",)))
        sc.add(Stamp("NON CREDIBILI", (650, 420), a + 1.0, tn, size=80, rot=-8))
        sc.add(Calendar((1400, 400), 240, [(tn, "GIUGNO", "1987")], tn, td), "paper")
        sc.add(Icon("scales", (1400, 680), tn + 0.4, td, size=180, label="CORTE DI CASSAZIONE"), "pop")
        sc.add(Img(doc_typed(760, 520, "CORTE DI CASSAZIONE · 1987 (sintesi)", ["Confermata l'assoluzione", "di Enzo Tortora.", "", "*sentenza definitiva*"]), (800, 500), tl_, td, anim="drop", rot=-1), "paper")
        sc.add(Stamp("DEFINITIVA", (1080, 700), T("definitiva") - 0.1, td, size=70, rot=-8))
        sc.add(Big("4 ANNI", (960, 600), td + 1.6, size=170, color=GOLD, fnt=OSW, sub="DALL'ARRESTO ALLA SENTENZA DEFINITIVA"), "hit")
        sc.add(Timeline(280, 1640, 330, [dict(top="1983", bottom="arresto", t=td), dict(top="1985", bottom="condanna", t=td + 0.4),
                                         dict(top="1986", bottom="assolto", t=td + 0.8), dict(top="1987", bottom="definitivo", t=td + 1.2, hl=True)], td))
        sc.footer = F_SENT
    elif i == 27:
        tch = T("il") - 0.1; tc = T("Tortora") - 0.3
        sc.add(Chapter("08", "Dove eravamo *rimasti*", a, tch))
        tp = T("Torna", 1) - 0.3; ts = T("Lo") - 0.3
        sc.add(Calendar((960, 470), 300, [(tch, "FEBBRAIO", "20"), (T("1987") - 0.2, "FEBBRAIO", "1987")], tch, tc), "paper")
        sc.add(Crowd((300, 680, 1620, 890), 10, T("molti") - 0.3, tc, s=0.4))
        sc.add(Icon("tv", (960, 480), tc, tp, size=320, label="DI NUOVO IN TV"), "pop")
        sc.add(Studio(STB, tp, None, parrot=True, sign="PORTOBELLO"))
        sc.add(Figure(walk([(2020, FY), (1000, FY)], tp + 0.3, 340), tp + 0.3, kind="suit", s=1.0, label="ENZO TORTORA"))
        sc.add(Pill("LO STESSO VENERDÌ SERA", (1450, 560), ts, size=44, accent=True))
        sc.footer = "Fonti: Il Post · Focus · Geopop · Wikipedia"
    elif i == 28:
        tf = T("dice") - 0.4; td = T("Dunque") - 0.2; tp = T("Poi") - 0.3
        sc.add(Studio(STB, a, None, parrot=True, sign=None))
        sc.add(Figure([(0, 1000, FY)], a, kind="suit", s=1.0), "pop")
        sc.add(Icon("mic", (1140, 650), a + 0.3, size=130), "pop")
        sc.add(Pill("EMOZIONATO", (960, 330), a + 0.4, td - 0.2, size=48))
        sc.add(Text("«Dunque,\ndove eravamo *rimasti*?»", (960, 300), td, size=84, anchor="ma", align="m"))
        sc.add(Pill("ANCHE PER CHI NON PUÒ PARLARE", (1420, 580), tp + 0.4, size=40, accent=True))
        sc.footer = "Fonti: Il Post · Focus · Geopop · Wikipedia · Sky TG24"
    elif i == 29:
        tr = T("Il") - 0.3; tv = T("Vince") - 0.3; tl_ = T("Nel") - 0.3; tc = T("chi") - 0.3
        sc.add(Text("Cambiano le *regole*", (960, 200), a, tr, size=80, anchor="ma"))
        sc.add(Calendar((360, 420), 240, [(tr, "NOVEMBRE", "8"), (tr + 0.9, "NOVEMBRE", "1987")], tr, tl_), "paper")
        sc.add(Icon("ballot", (960, 470), tr + 0.3, tl_, size=300, label="REFERENDUM · RESPONSABILITÀ CIVILE"), "pop")
        sc.add(Bar(1260, 420, 420, 60, [(tv + 0.2, 0.80)], tv, tl_, color=(60, 150, 80)))
        sc.add(Big("SÌ ~80%", (1470, 330), tv + 0.2, tl_, size=90, color=GOLD, fnt=OSW), "hit")
        sc.add(Img(doc_typed(780, 560, "LEGGE 117 / 1988 · «VASSALLI» (sintesi)", ["Danno da *dolo* o *colpa grave*", "di un magistrato:", "", "risarcimento chiesto", "*allo Stato*"]), (960, 520), tl_, anim="drop", rot=-1), "paper")
        sc.add(Icon("scales", (1560, 520), tc, size=200), "pop")
        sc.add(Icon("money", (360, 520), T("risarcimento") - 0.3, size=180), "pop")
        sc.footer = "Fonti: Pagella Politica · Sky TG24 · Il Post"
    elif i == 30:
        ts = T("Si") - 0.3; tm = T("Meno") - 0.3; ta = T("Aveva") - 0.3
        sc.add(Studio(STB, a, None, dark=a + 0.8, parrot=True, sign=None))
        sc.add(Calendar((960, 500), 260, [(ts, "MILANO · MAGGIO", "1988")], ts, ta), "paper")
        sc.add(Pill("MENO DI UN ANNO DOPO L'ASSOLUZIONE DEFINITIVA", (960, 230), tm, ta, size=40))
        sc.add(Big("1928 – 1988", (960, 470), ta, size=150, color=WHITE, fnt=OSW), "hit")
        sc.add(Text("Enzo Tortora", (960, 640), ta + 0.3, size=70, color=GOLD, anchor="ma"))
        sc.footer = "Fonti: Il Post · Wikipedia · Geopop"
    elif i == 31:
        tr = T("Un") - 0.3
        sc.add(Text("Ricapitolando", (960, 190), a, size=72, anchor="ma"))
        sc.add(Icon("handcuffs", (300, 470), tr + 0.3, size=190, label="856 ARRESTI"), "pop")
        sc.add(Icon("question", (640, 470), T("Diciannove") - 0.2, size=190, label="19 ACCUSATORI"), "pop")
        sc.add(Icon("addressbook", (980, 470), T("nome") - 0.3, size=190, label="TORTONA"), "pop")
        sc.add(Icon("doily", (1310, 470), T("centrini") - 0.3, size=190, label="I CENTRINI"), "pop")
        sc.add(Icon("scales", (1640, 470), T("condanna") - 0.3, size=190, label="10 ANNI, POI ASSOLTO"), "pop")
        sc.add(Stamp("FORMULA PIENA", (960, 760), T("l'assoluzione") - 0.1, size=70, rot=-6, color=(60, 150, 80)))
        sc.footer = "Ricostruzione divulgativa · fonti nella descrizione"
    elif i == 32:
        ts = T("Iscriviti") - 0.3
        sc.add(Studio(STB, a, T("Scrivilo") - 0.2, parrot=True, sign=None))
        sc.add(Pill("COME È STATO POSSIBILE?", (960, 330), T("Secondo") - 0.1, T("Scrivilo") - 0.2, size=56, accent=True))
        sc.add(Bubble((960, 470), 170, T("Scrivilo") - 0.1, ts, text="COMMENTI"), "pop")
        sc.add(Text("Fonti nella descrizione", (960, 760), T("fonti") - 0.2, ts, size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(110), (960, 520), ts, anim="pop", shadow=False), "hit")
        sc.add(Text("ogni giorno un nuovo caso", (960, 700), T("ogni") - 0.2, size=54, fnt=PS, color=GOLD, anchor="ma"))
        sc.footer = "Ricostruzione divulgativa · voce generata con sintesi vocale"
    return sc


def thumbnail(path="thumbnail.jpg"):
    im = make_bg(7).convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    Studio((1020, 130, 1860, 940), -5, None, parrot=True, sign="STUDIO TV", label=None).draw(lay, 0.0, 1.0)
    draw_person(lay, 1440, 900, 1.6, "suit")
    im.alpha_composite(lay)
    hc = fx.icon("handcuffs", 200); im.alpha_composite(hc, (1340, 650))
    t = rich_img("INNOCENTE\nIN *MANETTE*", SERIF, 150, WHITE, RED, lh=1.0)
    im.alpha_composite(t, (90, 190))
    st = stamp_img("CASO 006", RED, 64, -10); im.alpha_composite(st, (600, 50))
    st2 = stamp_img("ASSOLTO", (60, 150, 80), 60, 8); im.alpha_composite(st2, (110, 560))
    d = ImageDraw.Draw(im)
    d.text((100, 770), "IL NOME NELL'AGENDINA", font=font(OSW, 56, 600), fill=GOLD + (255,))
    d.text((100, 845), "NON ERA NEMMENO IL SUO", font=font(OSW, 56, 600), fill=GOLD + (255,))
    wm = wordmark(60, sub=False); im.alpha_composite(wm, (100, 960))
    im.convert("RGB").save(path, quality=92)
