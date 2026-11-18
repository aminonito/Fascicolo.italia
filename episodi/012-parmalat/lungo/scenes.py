import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from par import *
import fx, pon

W, H = 1920, 1080
FY = 870
LB = (330, 255, 1590, 895)      # scenografia ricorrente: il bilancio
LBR = (900, 255, 1780, 895)     # il bilancio a destra
MAPB = (160, 160, 1760, 880)
MT = "mappa: Natural Earth · percorsi indicativi · schema non in scala"
F_STORIA = "Fonti: AGI · Il Post · Money.it · Wikipedia (Parmalat)"
F_CONTI = "Fonti: Il Post · AGI · SEC (lit. rel. 18527) · Wikipedia"
F_BONLAT = "Fonti: SEC (lit. rel. 18527) · Wikipedia · AGI · imgpress"
F_FALSO = "Fonti: WSWS · imgpress · SEC · Wikipedia (timeline)"
F_DIC = "Fonti: AGI · imgpress · Wikipedia (timeline) · Blitz quotidiano"
F_RISP = "Fonti: AGI · imgpress · Blitz quotidiano · Wikipedia"
F_PROC = "Fonti: MF Milano Finanza · Blitz quotidiano · Money.it · imgpress · Il Post"
EURO = lambda s: pon.pic("euro", s)

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

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
        tu = T("Una") - 0.3; td = T("dichiara") - 0.2; tp = T("Poi") - 0.3; te = T("esiste") - 0.1
        sc.add(Calendar((960, 470), 300, [(a, "DICEMBRE", "2003")], a, tu + 0.3), "paper")
        sc.add(Icon("milk", (520, 470), tu, td, size=300, label="UN COLOSSO DEL LATTE"), "pop")
        sc.add(Icon("factory", (1000, 470), tu + 0.3, td, size=300), "pop")
        sc.add(WorldMap(MAPB, [(td, (-30, 35), 9), (tp, (-35, 38), 10)], td, tp + 0.3,
                        pins=[dict(at="Parma", label="PARMA", t=td + 0.2, side="r", color=GOLD),
                              dict(at="New York", label="NEW YORK", t=td + 0.9, side="l", color=RED)],
                        routes=[dict(pts=["Parma", "New York"], t=td + 0.3, d=1.4, icon="money", color=RED)], title=MT))
        sc.add(Pill("UN CONTO DA QUASI 4 MILIARDI €", (960, 215), T("quattro") - 0.2, tp, size=46, accent=True))
        sc.add(Img(confirm_letter(420), (640, 520), tp, anim="drop", rot=-3), "paper")
        sc.add(Figure(walk([(1900, FY), (1280, FY)], tp, 380), tp, kind="expert", s=1.0, flip=-1, carry=[(tp + 0.6, "magnifier")], label="LA BANCA"), "pop")
        sc.add(Stamp("NON\nESISTE", (640, 560), te, size=110, rot=-10))
        scene_cam(sc, (0, 960, 540, 1.0), (te - 0.2, 960, 540, 1.0), (dur, 760, 540, 1.12))
        sc.footer = F_BONLAT + " · documento ricostruito"
    elif i == 1:
        tsc = T("scanner") - 0.3; tf = T("fotocopiatrice") - 0.3; td = T("Dietro") - 0.3; tp = T("più") - 0.6
        sc.add(Img(confirm_letter(440, fake=True), (520, 520), a, td + 0.2, anim="drop", rot=-3), "paper")
        sc.add(Text("secondo le ricostruzioni", (1300, 230), T("secondo") - 0.2, td, size=30, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Icon("scanner", (1100, 520), tsc, td, size=260, label="SCANNER"), "pop")
        sc.add(Icon("fax", (1520, 520), tf, td, size=260, label="FOTOCOPIATRICE"), "pop")
        sc.add(Ledger(LB, td, None, cash_t=td - 5, gold_t=td - 5, fake_t=td + 0.2, hidden=[(td + 0.5, 1.0)], reveal_t=T("14") - 0.1, reveal_text="14 MLD €"))
        sc.add(Pill("IL PIÙ GRANDE CRAC PRIVATO IN EUROPA", (960, 215), tp, size=46, accent=True))
        sc.footer = F_FALSO + " · schema semplificato"
    elif i == 2:
        tq = T("Questo") - 0.3; tv = T("Vedremo") - 0.3
        sc.add(Img(cover_folder(), (960, 500), a, tv, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 012", (1150, 300), T("fascicolo") + 0.2, tv, size=70, rot=-12))
        sc.add(Icon("milk", (360, 470), tv + 0.1, size=200, label="DA LATTERIA A COLOSSO"), "pop")
        sc.add(Icon("island", (760, 470), T("dove") - 0.3, size=200, label="I DEBITI NASCOSTI"), "pop")
        sc.add(Icon("calendar_x", (1160, 470), T("settimana") - 0.3, size=200, label="LA SETTIMANA DEL CROLLO"), "pop")
        sc.add(Icon("family", (1560, 470), T("risparmiatori") - 0.4, size=200, label="I RISPARMIATORI"), "pop")
        sc.footer = "Fonti: AGI · Il Post · imgpress · SEC"
    elif i == 3:
        tc = T("Calisto") - 0.4; tn = T("nato") - 0.3; td = T("dove") - 0.3; tl_ = T("Lui") - 0.3
        sc.add(Chapter("01", "Il re del *latte*", a, tc))
        sc.add(Calendar((360, 420), 220, [(T("1961") - 0.3, "ANNO", "1961")], T("1961") - 0.3, tc + 0.2), "paper")
        sc.add(Img(label_card(["Calisto Tanzi", "nato a Collecchio", "vicino a Parma", "22 anni nel 1961"], 480, title="SCHEDA"), (380, 470), tc, td + 0.2, anim="drop", rot=-2), "paper")
        sc.add(Figure([(0, 900, FY)], tc + 0.2, tl_, kind="suit", s=1.0, label="SAGOMA · NESSUNA FOTO"), "pop")
        sc.add(MapEl((1180, 170, 1760, 870), [(tn, (10.3, 44.6), 120), (td + 0.6, "Collecchio", 260)], tn, None,
                     pins=[dict(at="Collecchio", label="COLLECCHIO", t=tn + 0.3, side="l", color=RED),
                           dict(at="Parma", label="PARMA", t=tn + 0.6, side="r", color=GOLD)], title="mappa: Natural Earth"))
        sc.add(Icon("shop", (480, 480), td + 0.2, tl_, size=260, label="ATTIVITÀ DI FAMIGLIA"), "pop")
        sc.add(Icon("milk", (600, 480), tl_, size=340), "hit")
        sc.add(Pill("PUNTA SUL LATTE", (600, 760), tl_ + 0.3, size=46, accent=True))
        sc.footer = F_STORIA
    elif i == 4:
        tn = T("Nasce") - 0.3; ti = T("All'inizio") - 0.3; tc = T("campagna") - 0.3
        sc.add(Icon("pasteur", (620, 480), a + 0.1, ti, size=360, label="IMPIANTO PER PASTORIZZARE"), "pop")
        sc.add(Icon("milk", (1180, 480), a + 0.9, ti, size=200), "pop")
        sc.add(Arrow((840, 480), (1060, 480), a + 0.6, ti, color=GOLD))
        sc.add(Stamp("1961 · NASCE\nLA PARMALAT", (1300, 760), tn, ti, size=60, rot=-6))
        sc.add(Icon("house", (700, 600), ti, size=260, label="AZIENDA LOCALE"), "pop")
        for k in range(3):
            sc.add(Icon("cow", (1060 + k * 240, 640 - (k % 2) * 40), tc + 0.2 * k, size=200), "pop" if k == 0 else None)
        sc.add(Pill("CAMPAGNA DI PARMA", (960, 215), tc, size=46, accent=True))
        sc.footer = F_STORIA + " · disegni generici"
    elif i == 5:
        tt = T("Trattato") - 0.3; tc = T("cartone") - 0.3; td = T("dura") - 0.3; ts = T("Si") - 0.3
        sc.add(Text("Lunga\n*conservazione*", (960, 380), a, tt, size=110, anchor="ma", align="m"))
        sc.add(Icon("thermo", (480, 480), tt, ts, size=320, label="ALTISSIMA TEMPERATURA"), "pop")
        sc.add(Icon("milk", (960, 480), tc, ts, size=320, label="IN CARTONE"), "pop")
        sc.add(Icon("nofridge", (1440, 480), td, ts, size=300, label="SENZA FRIGO"), "pop")
        sc.add(Calendar((1440, 260), 120, [(td, "MESE", "1"), (td + 0.4, "MESE", "2"), (td + 0.8, "MESE", "3")], td, ts), "paper")
        sc.add(WorldMap(MAPB, [(ts, (-25, 25), 8), (dur, (-25, 28), 8.6)], ts, None,
                        pins=[dict(at="Parma", label="PARMA", t=ts + 0.2, side="r", color=RED)],
                        routes=[dict(pts=["Parma", "New York"], t=ts + 0.3, d=1.0, color=GOLD),
                                dict(pts=["Parma", "Rio"], t=ts + 0.5, d=1.0, color=GOLD),
                                dict(pts=["Parma", "Atlanta"], t=ts + 0.7, d=1.0, color=GOLD),
                                dict(pts=["Parma", "Montreal"], t=ts + 0.9, d=1.0, color=GOLD)], title=MT))
        sc.add(Pill("SI SPEDISCE OVUNQUE", (960, 215), ts + 0.3, size=46, accent=True))
        sc.footer = "Fonti: Il Post · Wikipedia (Parmalat) · " + MT
    elif i == 6:
        ta = T("Arriva") - 0.3; tn = T("Nel") - 0.3
        sc.add(Text("Cresce\nin *fretta*", (960, 380), a, ta, size=120, anchor="ma", align="m"))
        for k in range(12):
            x = 330 + (k % 6) * 250; y = 380 + (k // 6) * 250
            sc.add(Icon("factory", (x, y), ta + 0.12 * k, tn, size=170), "pop" if k % 4 == 0 else None)
        sc.add(Big("130", (960, 300), T("130"), tn, size=150, color=GOLD, fnt=OSW, count=(0, 130, lambda v: "%d+" % v, 1.2), sub="stabilimenti"), "hit")
        sc.add(Pill("IN DIVERSI CONTINENTI", (960, 840), T("continenti") - 0.3, tn, size=44, accent=True))
        sc.add(Calendar((520, 480), 260, [(tn, "ANNO", "1990")], tn), "paper")
        sc.add(Icon("chart", (1200, 470), T("Borsa") - 0.3, size=320, label="QUOTATA IN BORSA"), "pop")
        sc.add(Pill("BORSA DI MILANO", (1200, 215), T("Milano") - 0.3, size=46, accent=True))
        sc.footer = "Fonti: AGI · Money.it · Wikipedia (Parmalat)"
    elif i == 7:
        tl_ = T("La") - 0.3; tco = T("comprese") - 0.3; tm = T("Il") - 0.3
        sc.add(Icon("ball", (960, 470), a + 0.2, tl_, size=320, label="IL PARMA CALCIO"), "pop")
        sc.add(Text("inizio anni Novanta", (960, 230), a + 0.4, tl_, size=34, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Pill("VINCE IN ITALIA E IN EUROPA", (960, 215), tl_, tm, size=46, accent=True))
        sc.add(Icon("trophy", (760, 500), tco, tm, size=300), "hit")
        sc.add(Icon("trophy", (1160, 500), tco + 0.3, tm, size=300), "pop")
        sc.add(Pill("2 COPPE UEFA", (960, 760), tco + 0.4, tm, size=50, accent=True))
        sc.add(Crowd((200, 520, 1720, 860), 22, T("tavoli") - 0.6, s=0.42, kinds=("man", "suit", "expert"), stagger=0.03))
        sc.add(Icon("milk", (960, 400), tm, size=260, label="UN MARCHIO FAMOSISSIMO"), "pop")
        sc.footer = "Fonti: AGI · Il Post · schema non in scala"
    elif i == 8:
        tu = T("Un") - 0.3; tm = T("Ma") - 0.3
        sc.add(Icon("factory", (960, 470), a, tm, size=380), "pop")
        sc.add(Pill("UN ORGOGLIO ITALIANO", (960, 215), a + 0.4, tu, size=46, accent=True))
        sc.add(Pill("«UN MODELLO»", (960, 215), tu, tm, size=50, accent=True))
        sc.add(Icon("book", (1440, 520), tu + 0.2, tm, size=220, label="DA STUDIARE"), "pop")
        sc.add(Ledger(LB, tm, None, cash_t=tm, hidden=[(T("torna") - 0.2, 0.25)]))
        sc.add(Icon("magnifier", (1500, 640), T("conti") - 0.1, size=220), "pop")
        sc.add(Icon("question", (1500, 400), T("torna"), size=160), "pop")
        sc.footer = "Fonti: AGI · Il Post · Il Fatto Quotidiano (2011) · schema semplificato"
    elif i == 9:
        tc = T("Compra") - 0.4; tp = T("Per") - 0.3
        sc.add(Chapter("02", "I debiti *nascosti*", a, tc))
        sc.add(Icon("milk", (960, 400), tc, T("televisione") - 0.3, size=240, label="NON SOLO LATTE"), "pop")
        sc.add(Icon("tv", (480, 470), T("televisione") - 0.3, tp, size=260, label="TELEVISIONE"), "pop")
        sc.add(Icon("plane", (960, 470), T("turismo") - 0.3, tp, size=260, label="TURISMO"), "pop")
        sc.add(Icon("water", (1440, 470), T("acque") - 0.3, tp, size=260, label="ACQUE MINERALI"), "pop")
        sc.add(Text("DEBITI", (300, 700), tp + 0.2, size=60, fnt=OSW, color=RED, anchor="lm"))
        sc.add(Bar(520, 670, 1180, 70, [(tp + 0.3, 0.2), (T("debiti") , 0.85)], tp + 0.2, color=RED))
        sc.add(Icon("money", (960, 460), tp, size=260), "pop")
        sc.add(Pill("SERVONO SOLDI", (960, 215), tp + 0.2, size=46, accent=True))
        sc.footer = "Fonti: Il Post · AGI · schema non in scala"
    elif i == 10:
        tu = T("Un'obbligazione") - 0.3; tt = T("tu") - 0.3; tl_ = T("lei") - 0.3; tc = T("con") - 0.3; tpf = T("Per", 1) - 0.3
        sc.add(Img(bond_doc(560), (960, 470), a + 0.2, tt, anim="drop", rot=-2), "paper")
        sc.add(Pill("OBBLIGAZIONE = UN PRESTITO", (960, 215), tu, tpf, size=46, accent=True))
        sc.add(Figure(walk([(200, FY), (620, FY)], tt, 300), tt, tpf, kind="man", s=1.0, carry=[(tt + 0.2, "money")], label="CHI PRESTA"), "pop")
        sc.add(Icon("factory", (1400, 600), tt + 0.2, tpf, size=320, label="L'AZIENDA"), "pop")
        sc.add(Arrow((720, 560), (1200, 560), tt + 0.6, tl_, color=GOLD))
        sc.add(Calendar((960, 430), 200, [(tl_, "SCADENZA", "DATA")], tl_, tpf), "paper")
        sc.add(Arrow((1200, 700), (720, 700), tl_ + 0.4, tpf, color=GREEN))
        sc.add(Pill("+ INTERESSI", (960, 760), tc, tpf, size=46, accent=True))
        sc.add(Ledger(LB, tpf, None, cash_t=tpf))
        sc.add(Figure([(0, 220, FY)], tpf + 0.2, kind="expert", s=0.9, carry=[(tpf + 0.4, "magnifier")]), "pop")
        sc.footer = "Fonti: AGI · Blitz quotidiano · spiegazione semplificata"
    elif i == 11:
        tt = T("Tanta") - 0.3; tm = T("Ma") - 0.3; tp = T("per") - 0.3
        led = Ledger(LB, a, None, cash_t=tt, gold_t=tt + 0.5, hidden=[(tp, 0.55)])
        sc.add(led)
        sc.add(Pill("SULLA CARTA: SPLENDIDI", (960, 215), a + 0.3, tm, size=46, accent=True))
        sc.add(Pill("SECONDO QUANTO EMERSO NEI PROCESSI", (960, 215), tm, tp + 0.5, size=40))
        sc.add(Stamp("BILANCI\nTRUCCATI", (960, 520), T("truccati") - 0.1, size=100, rot=-8))
        sc.add(Pill("OPERAZIONI FINANZIARIE FITTIZIE", (960, 215), T("operazioni") - 0.3, size=44, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (tp, 960, 540, 1.0), (dur, 1200, 560, 1.15))
        sc.footer = "Fonti: Il Post · imgpress (C. d'Appello Bologna) · schema semplificato"
    elif i == 12:
        ts = T("soprattutto") - 0.3; ti = T("I") - 0.3; te = T("e") - 0.3
        sc.add(WorldMap(MAPB, [(a, (-35, 32), 9), (ts + 1.2, (-81, 20), 40)], a, ti + 0.2,
                        pins=[dict(at="Parma", label="PARMA", t=a + 0.3, side="r", color=GOLD),
                              dict(at="Cayman", label="CARAIBI", t=ts + 0.4, side="r", color=RED)],
                        routes=[dict(pts=["Parma", "Cayman"], t=a + 0.6, d=1.6, icon="envelope", color=RED)], title=MT))
        sc.add(Pill("SOCIETÀ ALL'ESTERO", (960, 215), a + 0.3, ts, size=46, accent=True))
        sc.add(Pill("PARADISI FISCALI", (960, 215), ts, ti, size=46, accent=True))
        for k in range(3):
            sc.add(Icon("box_empty", (520 + k * 440, 560), ti + 0.15 * k, size=260, label="SCATOLA VUOTA" if k == 1 else None), "pop" if k == 0 else None)
            sc.add(Text("DEBITI", (520 + k * 440, 300), ti + 0.15 * k, te, size=44, fnt=OSW, color=RED, anchor="mm"))
            sc.add(Arrow((520 + k * 440, 330), (520 + k * 440, 430), ti + 0.3 + 0.15 * k, te, color=RED))
        for k in range(3):
            sc.add(Icon("money", (520 + k * 440, 330), te + 0.2 * k, size=150), "pop" if k == 0 else None)
            sc.add(Icon("question", (600 + k * 440, 260), te + 0.5 + 0.2 * k, size=90))
        sc.add(Pill("SOLDI CHE NON CI SONO", (960, 215), te + 0.3, size=46, accent=True))
        sc.footer = "Fonti: Il Post · SEC · Wikipedia · " + MT
    elif i == 13:
        th = T("Ha") - 0.3; te = T("È") - 0.3; tt = T("tesoro") - 0.4
        sc.add(Icon("island", (960, 470), a + 0.2, th, size=420), "pop")
        sc.add(Pill("BONLAT", (960, 760), T("Bonlat") - 0.2, th, size=60, accent=True))
        sc.add(WorldMap((160, 160, 1100, 880), [(th, (-78, 22), 30), (te + 1, "Cayman", 60)], th, None,
                        pins=[dict(at="Cayman", label="ISOLE CAYMAN", t=th + 0.4, side="r", color=RED)], title="mappa: Natural Earth"))
        sc.add(Img(label_card(["Bonlat Financing", "società del gruppo", "sede: isole Cayman"], 560, title="SCHEDA"), (1430, 480), th + 0.4, te, anim="drop", rot=2), "paper")
        sc.add(Ledger((1140, 255, 1780, 895), te, None, cash_t=te - 5, gold_t=tt, hl_gold=tt + 0.5, title="schema semplificato"))
        sc.add(Pill("SULLA CARTA", (1460, 215), T("sulla") - 0.2, size=40, accent=True))
        sc.footer = F_BONLAT
    elif i == 14:
        tb = T("Bonlat") - 0.3; tt = T("tra") - 0.3; ts = T("su") - 0.3
        sc.add(Chapter("03", "Il conto alle *Cayman*", a, tb - 0.3))
        sc.add(Calendar((330, 420), 220, [(tb, "BILANCIO", "2002")], tb, ts), "paper")
        sc.add(Ledger(LBR, tb, None, cash_t=tb - 5, gold_t=tb + 0.3, hl_gold=T("3,95"), title="schema semplificato"))
        sc.add(Big("3,95 MLD €", (480, 700), T("3,95") - 0.1, ts, size=110, color=GOLD, fnt=OSW, sub="contanti e titoli"), "hit")
        sc.add(WorldMap((160, 160, 880, 880), [(ts, (-80, 30), 26), (dur, (-76, 36), 30)], ts, None,
                        pins=[dict(at="Cayman", label="CAYMAN", t=ts + 0.2, side="r", color=GOLD),
                              dict(at="New York", label="NEW YORK", t=ts + 0.8, side="r", color=RED)],
                        routes=[dict(pts=["Cayman", "New York"], t=ts + 0.4, d=1.0, icon="money", color=RED)], title="mappa: Natural Earth"))
        sc.add(Icon("bank", (520, 660), T("New") - 0.2, size=180, label="BANK OF AMERICA"), "pop")
        sc.footer = F_BONLAT + " · schema semplificato"
    elif i == 15:
        ti = T("In") - 0.3; tf = T("fanno") - 0.3; tu = T("Una") - 0.3; te = T("E") - 0.3
        sc.add(Icon("calc", (960, 470), a + 0.2, ti, size=340, label="UN CALCOLO"), "pop")
        sc.add(Text("3.950.000.000 €", (960, 300), ti, te, size=90, fnt=OSW, color=GOLD, anchor="mm"))
        sc.add(Text("÷ 500 €", (960, 420), ti + 0.6, te, size=80, fnt=OSW, color=WHITE, anchor="mm"))
        sc.add(Big("7,9 MLN", (960, 600), tf, te, size=160, color=RED, fnt=OSW, sub="banconote da 500 €"), "hit")
        for k in range(10):
            sc.add(Icon("money", (300 + (k % 5) * 90, 820 - (k // 5) * 60), tu + 0.08 * k, te, size=140), None)
            sc.add(Icon("money", (1260 + (k % 5) * 90, 820 - (k // 5) * 60), tu + 0.08 * k, te, size=140), None)
        sc.add(Img(confirm_letter(440), (960, 520), te, anim="drop", rot=-3), "paper")
        sc.add(Pill("BASTA UN FOGLIO", (960, 215), te + 0.2, size=46, accent=True))
        sc.add(Text("calcolo: 3,95 miliardi ÷ 500 € · documento ricostruito", (960, 870), a + 0.4, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: SEC (lit. rel. 18527) · Wikipedia · calcolo nostro"
    elif i == 16:
        te = T("E") - 0.3; ts = T("Secondo") - 0.3; tu = T("un'intestazione") - 0.3; tm = T("montata") - 0.3
        sc.add(Ledger(LB, a, te + 0.2, cash_t=a - 5, gold_t=a - 5, fake_t=T("esiste") - 0.1))
        sc.add(Img(confirm_letter(420), (960, 520), te, ts, anim="drop", rot=-3), "paper")
        sc.add(Stamp("FALSA", (960, 520), T("falsa") - 0.1, ts, size=120, rot=-12))
        sc.add(Pill("FABBRICATA IN CASA · SECONDO LE RICOSTRUZIONI", (960, 215), ts, size=40, accent=True))
        sc.add(Icon("letter_bank", (380, 520), ts + 0.3, tm + 0.6, size=260, move=(tu + 0.3, 1.0, (860, 520), 60)), "pop")
        sc.add(Icon("scanner", (860, 560), tu - 0.2, tm + 0.6, size=280, label="SCANNER"), "pop")
        sc.add(Arrow((1060, 520), (1280, 520), tm, color=GOLD))
        sc.add(Img(confirm_letter(380, fake=True), (1500, 540), tm + 0.2, anim="drop", rot=3), "paper")
        sc.footer = F_FALSO + " · documento ricostruito, non l'originale"
    elif i == 17:
        tpo = T("poi") - 0.3; tu = T("Un") - 0.3; ts = T("stampata") - 0.3
        sc.add(Img(confirm_letter(340), (300, 500), a, ts, anim="drop", rot=-3), "paper")
        sc.add(Arrow((480, 500), (700, 500), a + 0.6, ts, color=GOLD))
        sc.add(Ledger((720, 270, 1180, 860), a + 0.6, ts, cash_t=a - 5, gold_t=T("inesistenti"), title="BONLAT"))
        sc.add(Arrow((1200, 500), (1380, 500), tpo, ts, color=GOLD))
        sc.add(Ledger((1400, 270, 1860, 860), tpo, ts, cash_t=tpo, gold_t=tpo + 0.5, title="GRUPPO PARMALAT"))
        sc.add(Pill("UN FOGLIO FALSO DIVENTA UNA CIFRA UFFICIALE", (960, 215), tu, ts, size=44, accent=True))
        sc.add(Icon("newspaper", (560, 470), ts, size=260, label="CONTI PUBBLICATI"), "pop")
        sc.add(Crowd((900, 560, 1760, 860), 14, ts + 0.3, s=0.5, kinds=("suit", "expert"), stagger=0.05))
        sc.add(Pill("GLI INVESTITORI LEGGONO", (1330, 400), ts + 0.6, size=44, accent=True))
        sc.footer = "Fonti: SEC (lit. rel. 18527) · Wikipedia · schema semplificato"
    elif i == 18:
        ti = T("I") - 0.3; tp = T("Prima") - 0.3; tc = T("con") - 0.3
        sc.add(Text("Il *limite*", (960, 400), a, ti, size=130, anchor="ma", align="m"))
        sc.add(Icon("money", (700, 470), ti, tp, size=320, color=(130, 130, 130)), "pop")
        sc.add(Stamp("NON SI\nSPENDONO", (1200, 480), T("spendere") - 0.2, tp, size=90, rot=-8))
        sc.add(Icon("hourglass", (600, 470), tp, size=280), "pop")
        sc.add(Calendar((1000, 470), 240, [(tp + 0.2, "SCADENZA", "?"), (tp + 0.8, "SCADENZA", "!!")], tp), "paper")
        sc.add(Icon("money", (1400, 470), tc, size=320), "hit")
        sc.add(Pill("SOLDI VERI", (1400, 720), tc + 0.2, size=50, accent=True))
        sc.footer = F_CONTI
    elif i == 19:
        tc = T("8") - 0.4; ts = T("Scade") - 0.3; tu = T("Una") - 0.3; tm = T("Ma") - 0.3
        sc.add(Chapter("04", "Dicembre *2003*", a, tc))
        sc.add(Calendar((360, 450), 260, [(tc, "DICEMBRE 2003", "8")], tc), "paper")
        sc.add(Img(bond_doc(520), (1100, 430), ts, tu, anim="drop", rot=-2), "paper")
        sc.add(Pill("150 MILIONI € DA RIMBORSARE", (1100, 720), ts + 0.4, tu, size=44, accent=True))
        sc.add(Text("150 MLN", (700, 380), tu, size=44, fnt=OSW, color=WHITE, anchor="lm"))
        sc.add(Bar(700, 410, 1000, 60, [(tu + 0.2, 0.038)], tu, color=RED))
        sc.add(Text("3.950 MLN dichiarati in cassa", (700, 540), tu + 0.4, size=44, fnt=OSW, color=GOLD, anchor="lm"))
        sc.add(Bar(700, 570, 1000, 60, [(tu + 0.6, 1.0)], tu + 0.4, color=GOLD))
        sc.add(Stamp("NON PAGATA", (1200, 760), tm + 0.4, size=96, rot=-8))
        sc.footer = "Fonti: Blitz quotidiano · imgpress · Wikipedia · schema in scala"
    elif i == 20:
        ti = T("In") - 0.3; ta = T("Al") - 0.3; tu = T("un") - 0.3
        sc.add(Icon("warning", (960, 470), a, ti, size=360, anim="shake"), "hit")
        sc.add(Pill("SEGNALE D'ALLARME", (960, 760), a + 0.3, ti, size=50, accent=True))
        sc.add(Icon("factory", (1460, 600), ti, size=320), "pop")
        sc.add(Figure(walk([(1300, FY), (-100, FY)], T("lascia") - 0.2, 300), ti, kind="suit", s=1.0, flip=-1, label="TANZI · SAGOMA"), "pop")
        sc.add(Figure(walk([(-100, FY), (900, FY)], ta, 360), ta, kind="expert", s=1.0, carry=[(tu, "magnifier")], label="ENRICO BONDI · SAGOMA"), "pop")
        sc.add(Pill("LASCIA LA GUIDA DELL'AZIENDA", (960, 215), ti + 0.3, ta, size=44, accent=True))
        sc.add(Pill("COSA C'È DAVVERO NEI CONTI?", (960, 215), tu, size=44, accent=True))
        sc.footer = "Fonti: AGI · Wikipedia · imgpress · sagome, nessuna foto"
    elif i == 21:
        tl_ = T("La") - 0.3; te = T("esiste") - 0.1; td = T("Il", 1) - 0.3
        sc.add(Calendar((330, 420), 220, [(a, "DICEMBRE 2003", "19")], a, tl_), "paper")
        sc.add(WorldMap((560, 160, 1760, 880), [(a, (-35, 38), 10), (tl_, (-35, 40), 10.5)], a, tl_ + 0.2,
                        pins=[dict(at="New York", label="NEW YORK", t=a + 0.2, side="r", color=RED),
                              dict(at="Parma", label="PARMA", t=a + 0.3, side="l", color=GOLD)],
                        routes=[dict(pts=["New York", "Parma"], t=a + 0.4, d=1.4, icon="envelope", color=RED)], title=MT))
        sc.add(Ledger(LB, tl_, td, cash_t=a - 5, gold_t=a - 5, fake_t=te, hl_gold=tl_ + 0.3))
        sc.add(Img(confirm_letter(420), (960, 520), td, anim="drop", rot=-3), "paper")
        sc.add(Icon("scales", (1500, 470), T("avvocati") - 0.3, size=220, label="AVVOCATI DELLA BANCA"), "pop")
        sc.add(Stamp("FALSO", (960, 520), T("falso") - 0.1, size=130, rot=-12))
        sc.footer = "Fonti: SEC · Wikipedia (timeline) · AGI · imgpress · documento ricostruito"
    elif i == 22:
        tv = T("Il", 1) - 0.3; tl_ = T("la", 1) - 0.3; tb = T("Bondi") - 0.3; tc = T("Il", 2) - 0.3
        sc.add(Icon("crash", (960, 470), a, tv, size=380, label="IL TITOLO CROLLA"), "hit")
        sc.add(Calendar((420, 450), 260, [(tv, "DICEMBRE 2003", "24")], tv, tb), "paper")
        sc.add(Text("la vigilia di Natale", (420, 680), T("vigilia") - 0.2, tb, size=34, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Icon("factory", (1200, 470), tl_ - 0.3, size=380), "pop")
        sc.add(Stamp("INSOLVENTE", (1200, 520), T("insolvente") - 0.1, tb, size=96, rot=-8))
        sc.add(Figure(walk([(-100, FY), (560, FY)], tb, 380), tb, kind="expert", s=1.0, label="COMMISSARIO STRAORDINARIO"), "pop")
        sc.add(Pill("SALVARE IL SALVABILE", (960, 215), tc, size=50, accent=True))
        sc.footer = F_DIC
    elif i == 23:
        tc = T("Calisto") - 0.3; ta = T("e") - 0.3; tn = T("Nelle") - 0.3
        sc.add(Calendar((960, 450), 260, [(a, "DICEMBRE 2003", "27")], a, tc), "paper")
        sc.add(Icon("plane", (300, 380), tc, tn, size=240, move=(tc + 0.2, 1.6, (1300, 460), 80)), "whoosh")
        sc.add(Text("rientro dall'estero", (960, 230), tc + 0.2, ta, size=36, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Figure([(0, 1300, FY)], ta, tn, kind="suit", s=1.0, label="TANZI · SAGOMA"), "pop")
        sc.add(Figure(walk([(1900, FY), (1520, FY)], ta, 380), ta, tn, kind="police", s=1.0, flip=-1), "pop")
        sc.add(Icon("handcuffs", (1400, 460), T("arrestato") - 0.1, tn, size=200), "hit")
        sc.add(Stamp("ARRESTATO", (700, 600), T("arrestato"), tn, size=90, rot=-8))
        sc.add(Ledger(LB, tn, None, cash_t=a - 5, gold_t=a - 5, fake_t=a - 5, hidden=[(tn + 0.3, 1.0)], reveal_t=T("14") - 0.1, reveal_text="14 MLD €"))
        sc.footer = F_DIC + " · schema semplificato"
    elif i == 24:
        tl_ = T("Le") - 0.4; tp = T("Pensionati") - 0.3; tpe = T("persone") - 0.3
        sc.add(Chapter("05", "I *risparmiatori*", a, tl_))
        sc.add(Savers((200, 400, 1720, FY), 9, tl_, s=0.85))
        sc.add(Pill("OBBLIGAZIONI NELLE FAMIGLIE", (960, 215), tl_ + 0.2, tp, size=46, accent=True))
        sc.add(Pill("PENSIONATI", (960, 215), tp, T("piccoli") - 0.2, size=50, accent=True))
        sc.add(Pill("PICCOLI RISPARMIATORI", (960, 215), T("piccoli") - 0.2, tpe, size=50, accent=True))
        sc.add(Icon("piggy", (960, 330), tpe, size=200), "pop")
        sc.add(Pill("«UN INVESTIMENTO TRANQUILLO»", (960, 215), tpe + 0.2, size=46, accent=True))
        sc.footer = "Fonti: imgpress · Money.it · AGI · disegni generici"
    elif i == 25:
        tl_ = T("Le") - 0.3; ts = T("si") - 0.3; tsec = T("secondo") - 0.3; td = T("Dall'oggi") - 0.3
        sc.add(Text("Quanti\n*erano?*", (960, 380), a, tl_, size=130, anchor="ma", align="m"))
        sc.add(Pill("LE STIME NON COINCIDONO", (960, 215), tl_, td, size=46, accent=True))
        sc.add(Crowd((160, 380, 1760, 870), 60, ts, td, s=0.32, stagger=0.02))
        sc.add(Pill("DECINE DI MIGLIAIA", (560, 305), T("decine") - 0.2, td, size=44))
        sc.add(Pill("PER ALCUNE FONTI: OLTRE 100.000", (1300, 305), tsec, td, size=44))
        sc.add(Savers((200, 400, 1720, FY), 9, td, s=0.85, drop_t=T("valgono") - 0.2))
        sc.add(Stamp("QUASI ZERO", (960, 330), T("niente") - 0.1, size=90, rot=-6))
        sc.footer = "Fonti: AGI · Blitz quotidiano · imgpress · Wikipedia · stime non concordi"
    elif i == 26:
        t14 = T("14") - 0.3; td = T("divisi") - 0.3; tf = T("fanno") - 0.3; tn = T("Neonati") - 0.3
        sc.add(Icon("calc", (960, 470), a, t14, size=340, label="UN ALTRO CALCOLO"), "pop")
        sc.add(Text("14.000.000.000 €", (960, 300), t14, size=96, fnt=OSW, color=RED, anchor="mm"))
        sc.add(Text("÷ 59 milioni di abitanti", (960, 420), td, size=70, fnt=OSW, color=WHITE, anchor="mm"))
        sc.add(Big("230+ €", (960, 590), tf, size=170, color=GOLD, fnt=OSW, sub="a testa"), "hit")
        sc.add(Crowd((200, 810, 1720, 890), 30, td + 0.3, s=0.24, stagger=0.02))
        sc.add(Pill("NEONATI COMPRESI", (1500, 215), tn, size=46, accent=True))
        sc.add(Text("popolazione: ISTAT (circa 59 milioni) · calcolo nostro", (960, 215), a + 0.4, tn, size=26, fnt=COURR, color=GREY, anchor="mm"))
        sc.footer = "Fonti: AGI · Il Post · ISTAT · calcolo nostro"
    elif i == 27:
        tl_ = T("Le") - 0.3; tb = T("Bondi") - 0.3; te = T("e", 1) - 0.3; tn = T("Nel") - 0.3
        sc.add(Text("L'azienda\nnon *chiude*", (960, 380), a, tl_, size=110, anchor="ma", align="m"))
        sc.add(Icon("factory", (640, 470), tl_, tb, size=340, label="FABBRICHE SANE"), "pop")
        sc.add(Icon("milk", (1280, 470), T("problema") - 0.2, tb, size=300), "pop")
        sc.add(Pill("IL PROBLEMA È NEI CONTI", (960, 215), T("problema") - 0.2, tb, size=46, accent=True))
        sc.add(Icon("court", (480, 470), tb, tn, size=300, label="CAUSE ALLE BANCHE"), "pop")
        for k in range(3): sc.add(Icon("bank", (1100 + k * 230, 400), tb + 0.4 + 0.15 * k, tn, size=170), "pop" if k == 0 else None)
        sc.add(Arrow((1300, 560), (700, 640), te, tn, color=GREEN, bend=0.2))
        sc.add(Big("+1 MLD €", (1330, 700), te + 0.2, tn, size=110, color=GREEN, fnt=OSW, sub="recuperati (oltre)"), "hit")
        sc.add(Calendar((640, 470), 240, [(tn, "ANNO", "2011")], tn), "paper")
        sc.add(Icon("factory", (1240, 470), tn + 0.3, size=300), "pop")
        sc.add(Pill("COMPRATA DA LACTALIS (FRANCIA)", (1240, 760), T("Lactalis") - 0.2, size=44, accent=True))
        sc.footer = "Fonti: AGI · Blitz quotidiano · Wikipedia (Parmalat; timeline)"
    elif i == 28:
        ts = T("Sono") - 0.4; tm = T("Milano") - 0.3; tp = T("Parma") - 0.3
        sc.add(Chapter("06", "I *processi*", a, ts))
        sc.add(MapEl((160, 160, 900, 880), [(ts, (10.0, 45.0), 260), (dur, (9.9, 45.1), 280)], ts, None,
                     pins=[dict(at="Milano", label="MILANO", t=tm, side="r", color=RED),
                           dict(at="Parma", label="PARMA", t=tp, side="r", color=GOLD)], title="mappa: Natural Earth"))
        sc.add(Pill("DUE FILONI", (1330, 215), ts + 0.2, size=46, accent=True))
        sc.add(Icon("court", (1150, 420), tm, size=220, label="MILANO"), "pop")
        sc.add(Text("AGGIOTAGGIO", (1150, 640), T("aggiotaggio") - 0.2, size=48, fnt=OSW, color=RED, anchor="mm"))
        sc.add(Text("notizie false\nal mercato", (1150, 690), T("diffuso") - 0.2, size=32, fnt=PS, color=GREY, anchor="ma", align="m"))
        sc.add(Icon("court", (1560, 420), tp, size=220, label="PARMA"), "pop")
        sc.add(Text("BANCAROTTA\nFRAUDOLENTA", (1560, 640), T("bancarotta") - 0.2, size=44, fnt=OSW, color=GOLD, anchor="ma", align="m"))
        sc.footer = F_PROC
    elif i == 29:
        tt = T("Tanzi") - 0.3; ti = T("Il") - 0.3; tm = T("ma") - 0.3; tl_ = T("pena") - 0.5; tn = T("Nello") - 0.3
        sc.add(Calendar((330, 420), 220, [(a, "MILANO", "2008"), (ti, "4 MAGGIO", "2011")], a), "paper")
        sc.add(Icon("gavel", (960, 470), a + 0.2, ti, size=300), "hit")
        sc.add(Big("10 anni", (1450, 470), tt + 0.3, ti, size=150, color=WHITE, fnt=OSW, sub="primo grado · aggiotaggio"), "hit")
        sc.add(Icon("court", (960, 430), ti, tm, size=280, label="CASSAZIONE"), "pop")
        sc.add(Icon("hourglass", (960, 430), tm, tl_, size=260, label="PRESCRIZIONE PER ALCUNI FATTI"), "pop")
        sc.add(Img(sentence_card(["Calisto Tanzi", "aggiotaggio", "8 anni e 1 mese"]), (1100, 480), tl_, anim="drop", rot=-2), "paper")
        sc.add(Stamp("DEFINITIVA", (1300, 700), tl_ + 0.6, size=70, rot=-8))
        sc.add(Pill("LE BANCHE A PROCESSO: ASSOLTE", (960, 215), tn, size=46, accent=True))
        sc.footer = "Fonti: MF Milano Finanza · Blitz quotidiano · Money.it · AGI"
    elif i == 30:
        tp = T("Per") - 0.3; ti = T("Il") - 0.3; t17 = T("17") - 0.3
        sc.add(Calendar((330, 420), 220, [(a, "PARMA", "2010"), (ti, "7 MARZO", "2014")], a), "paper")
        sc.add(Icon("gavel", (960, 470), a + 0.2, ti, size=300), "hit")
        sc.add(Big("18 anni", (1450, 470), T("18") - 0.1, ti, size=150, color=WHITE, fnt=OSW, sub="primo grado · bancarotta"), "hit")
        sc.add(Icon("court", (960, 430), ti, t17, size=280, label="CASSAZIONE"), "pop")
        sc.add(Img(sentence_card(["Calisto Tanzi", "bancarotta fraudolenta", "17 anni e 5 mesi"]), (1100, 480), t17, anim="drop", rot=-2), "paper")
        sc.add(Stamp("DEFINITIVA", (1300, 700), t17 + 0.6, size=70, rot=-8))
        sc.footer = "Fonti: Blitz quotidiano · imgpress · Money.it · Il Post · MF Milano Finanza"
    elif i == 31:
        tm = T("Muore") - 0.3; tl_ = T("La") - 0.3
        sc.add(Icon("house", (700, 470), a, tm, size=340), "pop")
        sc.add(Pill("ARRESTI DOMICILIARI", (700, 740), a + 0.4, tm, size=46, accent=True))
        sc.add(Figure([(0, 1200, FY)], a + 0.3, tm, kind="suit", s=1.0, label="SAGOMA · NESSUNA FOTO"), "pop")
        sc.add(Calendar((960, 450), 280, [(tm, "1 GENNAIO", "2022")], tm, tl_), "paper")
        sc.add(Text("83 anni", (960, 720), T("83") - 0.2, tl_, size=60, fnt=OSW, color=GOLD, anchor="mm"))
        sc.add(Icon("milk", (760, 470), tl_, size=320), "pop")
        sc.add(Icon("factory", (1200, 470), tl_ + 0.3, size=320), "pop")
        sc.add(Pill("ESISTE ANCORA", (960, 215), T("esiste") - 0.2, size=50, accent=True))
        sc.footer = "Fonti: Il Post (2022) · Money.it · AGI"
    elif i == 32:
        tu = T("Una") - 0.3; tp = T("e", 2) - 0.2
        sc.add(Chapter("", "Il *verdetto*", a, tu))
        items = [("milk", "LA LATTERIA", T("Una")), ("factory", "IL COLOSSO", T("colosso")), ("crash", "DEBITI", T("debiti")),
                 ("box_empty", "NASCOSTI", T("nascosti")), ("island", "IL CONTO", T("conto")), ("letter_bank", "FOGLIO FALSO", T("falso")),
                 ("calendar_x", "150 MLN NON PAGATI", T("Poi")), ("warning", "IL CROLLO", T("crolla"))]
        for k, (ic, lab, tt) in enumerate(items):
            x = 330 + (k % 4) * 420; y = 330 if k < 4 else 640
            sc.add(Icon(ic, (x, y), tt - 0.2, size=180, label=lab), "pop" if k % 3 == 0 else None)
        sc.add(Stamp("IN DUE SETTIMANE", (960, 830), T("settimane") - 0.2, size=80, rot=-5))
        sc.footer = "Ricostruzione divulgativa · fonti nella descrizione"
    elif i == 33:
        ts = T("Iscriviti") - 0.3; tsc = T("Scrivilo") - 0.2
        sc.add(Img(confirm_letter(380, fake=True), (620, 520), a, tsc, anim="drop", rot=-3), "paper")
        sc.add(Icon("scanner", (1300, 520), a + 0.3, tsc, size=300), "pop")
        sc.add(Pill("UN FOGLIO HA INGANNATO IL MERCATO?", (960, 215), a + 0.3, tsc, size=46, accent=True))
        sc.add(Bubble((960, 470), 170, tsc + 0.1, ts, text="COMMENTI"), "pop")
        sc.add(Text("Fonti nella descrizione", (960, 760), T("fonti") - 0.2, ts, size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(110), (960, 520), ts, anim="pop", shadow=False), "hit")
        sc.add(Text("ogni giorno un nuovo caso", (960, 700), T("ogni") - 0.2, size=54, fnt=PS, color=GOLD, anchor="ma"))
        sc.footer = "Ricostruzione divulgativa · voce generata con sintesi vocale"
    return sc


def thumbnail(path="thumbnail.jpg"):
    im = make_bg(8).convert("RGBA")
    let = confirm_letter(470, fake=True).rotate(4, expand=True, resample=Image.BICUBIC)
    im.alpha_composite(let, (1290, 90))
    st = stamp_img("NON ESISTE", RED, 90, -12); im.alpha_composite(st, (1260, 420))
    mk = fx.icon("milk", 300); im.alpha_composite(mk, (1050, 600))
    t = rich_img("IL CONTO\nCHE NON\n*ESISTEVA*", SERIF, 150, WHITE, RED, lh=1.0)
    im.alpha_composite(t, (90, 100))
    st2 = stamp_img("CASO 012", RED, 64, -10); im.alpha_composite(st2, (800, 40))
    d = ImageDraw.Draw(im)
    d.text((100, 800), "PARMALAT 2003: UN FOGLIO FALSO", font=font(OSW, 56, 600), fill=GOLD + (255,))
    d.text((100, 870), "E UN BUCO DA 14 MILIARDI", font=font(OSW, 56, 600), fill=GOLD + (255,))
    wm = wordmark(60, sub=False); im.alpha_composite(wm, (100, 975))
    im.convert("RGB").save(path, quality=92)
