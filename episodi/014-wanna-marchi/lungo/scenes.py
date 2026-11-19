import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from wm import *

W, H = 1920, 1080
FY = 870
STB = (260, 170, 1660, 870)     # scenografia ricorrente: lo studio delle televendite
SAL = (260, 170, 1660, 870)     # la casa della telespettatrice (la trappola)
MAPB = (160, 160, 1760, 880)
MT = "mappa: Natural Earth · schema non in scala"
F_TV = "Fonti: Il Post · Fanpage · QuiFinanza"
F_ASC = "Fonti: Il Post · Fanpage · QuiFinanza · il Giornale (2005)"
F_TRAP = "Fonti: Il Post · il Giornale (2005) · Fanpage · QuiFinanza"
F_ARR = "Fonti: Il Post · Fanpage · QuiFinanza"
F_SENT = "Fonti: VareseNews (2009) · Blitz quotidiano (2009) · Il Post · Fanpage"
F_IST = "Fonti: ISTAT, valore della moneta · calcolo Fascicolo Italia"
WHO = (560, 840)                # posizione della telespettatrice nel salotto

def build(i, dur, a, words):
    T0 = Clock(words, a)
    def T(p, n=0):
        try: return T0(p, n)
        except KeyError: return a + 0.5
    sc = Scene(dur)
    if i == 0:
        tf = T("foglio") - 0.3; tt = T("telefonata") - 0.3; ts = T("sciolto") - 0.3; tm = T("malocchio") - 0.3
        tr = T("Per") - 0.3; tq = T("milioni") - 0.8
        sc.add(Icon("salt", (620, 480), a, tt, size=340), "pop")
        sc.add(Pill("SALE DA CUCINA", (620, 740), a + 0.4, tt, size=44))
        sc.add(Icon("lotto", (1300, 480), tf, tt, size=320), "pop")
        sc.add(Pill("4 NUMERI DEL LOTTO", (1300, 740), tf + 0.3, tt, size=44))
        sc.add(Salotto(SAL, tt, tm + 0.2, ring=(tt, tm)), "whoosh")
        sc.add(Figure([(tt, *WHO)], tt, tm + 0.2, kind="expert", s=0.8), None)
        sc.add(Icon("glass_salt", (1300, 420), ts, tm + 0.2, size=240, label="NON SI È SCIOLTO"), "pop")
        sc.add(Icon("eye", (960, 470), tm, tr + 0.2, size=520), "hit")
        sc.add(Pill("IL «MALOCCHIO»", (960, 780), tm + 0.3, tr + 0.2, size=52, accent=True))
        sc.add(Icon("amulet", (620, 470), tr, size=300, label="IL RITO"), "pop")
        sc.add(Icon("lire", (1300, 450), tq, size=380), "hit")
        sc.add(Pill("4 MILIONI DI LIRE", (1300, 700), tq + 0.3, size=56, accent=True))
        sc.footer = F_TRAP + " · ricostruzione"
    elif i == 1:
        tc = T("C'è") - 0.3; tw = T("Wanna") - 0.3; tsn = T("Stefania") - 0.3; tm = T("questa") - 0.5
        sc.add(Icon("phone", (960, 470), a, tc, size=300), "pop")
        sc.add(Icon("question", (1260, 330), a + 0.6, tc, size=160), "pop")
        sc.add(Pill("NON UN MAGO QUALSIASI", (960, 760), a + 0.8, tc, size=46))
        sc.add(Tele((160, 170, 1000, 870), tc, tm + 0.2, items=[(tc + 0.3, "jar"), (tc + 0.6, "salt"), (tc + 0.9, "lotto")], calls=(tc, tm)), "whoosh")
        sc.add(Board({"w": dict(xy=(1250, 560), name="WANNA MARCHI", role="televenditrice", t=tw, rot=-3),
                      "s": dict(xy=(1580, 560), name="STEFANIA NOBILE", role="la figlia", t=tsn, rot=3)},
                     [("w", "s", tsn + 0.5)], tw, tm + 0.2, cw=260))
        sc.add(Pill("LA REGINA DELLE TELEVENDITE", (1410, 215), T("regina") - 0.2, tm + 0.2, size=42, accent=True))
        sc.add(Salotto(SAL, tm, None, cams=[(tm + 1.4, (.46, .22))]), "whoosh")
        sc.add(Figure([(tm, *WHO)], tm, None, kind="expert", s=0.8))
        sc.add(Pill("UNA TELECAMERA NASCOSTA", (960, 215), T("telecamera") - 0.2, size=48, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (T("telecamera"), 960, 540, 1.0), (dur, 904, 400, 1.35))
        sc.footer = F_TRAP + " · silhouette, nessuna foto reale"
    elif i == 2:
        tv = T("Vedremo") - 0.3
        sc.add(Img(cover_folder(), (960, 500), a, tv, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 014", (1150, 300), T("fascicolo") + 0.2, tv, size=70, rot=-12))
        items = [("studio_tv", "LE TELEVENDITE", "regina"), ("amulet", "IL MAESTRO DI VITA", "maestro"), ("salt", "SALE ED EDERA", "sale"),
                 ("hiddencam", "LA TRAPPOLA", "trappola"), ("gavel", "LE CONDANNE", "condanne")]
        for k, (ic, lab, w_) in enumerate(items):
            n = 1 if w_ == "sale" else 0
            sc.add(Icon(ic, (280 + k * 340, 470), T(w_, n) - 0.3, size=190, label=lab), "pop")
        sc.footer = F_TV
    elif i == 3:
        tc = T("Wanna") - 0.4; te = T("giovane") - 0.6; tp = T("Poi") - 0.3
        sc.add(Chapter("01", "La regina delle *televendite*", a, tc))
        sc.add(Img(person_card("WANNA MARCHI", "televenditrice", 300, seed=4), (520, 500), tc, anim="drop", rot=-3), "paper")
        sc.add(Text("silhouette · nessuna foto reale", (520, 730), tc + 0.3, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Calendar((1250, 470), 260, [(tc + 0.2, "NASCE NEL", "1942")], tc, te), "paper")
        sc.add(Figure([(te, 1150, FY)], te, None, kind="host", s=0.8, label="ESTETISTA"), "pop")
        sc.add(Icon("jar", (1450, 520), te + 0.3, tp, size=200), "pop")
        sc.add(Icon("studio_tv", (1450, 480), tp, size=300, label="LA TELEVISIONE"), "pop")
        sc.footer = F_TV
    elif i == 4:
        tg = T("Uno") - 0.3; tw = T("Wanna") - 0.3
        for k in range(3):
            sc.add(Icon("studio_tv", (480 + k * 480, 450), a + k * 0.4, tg, size=260), "pop")
        sc.add(Pill("LE TV PRIVATE", (960, 720), a + 0.5, T("E") - 0.2, size=48))
        sc.add(Pill("LA TELEVENDITA", (960, 720), T("televendita.") - 0.3, tg, size=48, accent=True))
        sc.add(Img(label_card(["GRAN BAZAR", "programma dedicato", "alle televendite"], 520, title="SCHEDA"), (620, 480), tg, tw, anim="drop", rot=-2), "paper")
        sc.add(Icon("phone", (1350, 470), tg + 0.4, tw, size=260), "pop")
        sc.add(Tele((160, 170, 1000, 870), tw, None, items=[(T("bellezza") - 0.2, "jar"), (T("dimagrire") - 0.2, "jar"), (T("alghe") - 0.2, "algae")]), "whoosh")
        sc.add(MapEl((1040, 170, 1760, 870), [(tw, "Bologna", 900)], tw, None,
                     pins=[dict(at="Bologna", label="BOLOGNA", t=tw + 0.4, side="r", color=RED)], title=MT))
        sc.add(Pill("UNA RETE LOCALE", (1400, 800), T("rete") - 0.2, size=40, accent=True))
        sc.footer = F_TV + " · " + MT
    elif i == 5:
        ts = T("scioglipancia") - 0.3; tt = T("Tre") - 0.3; tse = T("Secondo") - 0.3
        sc.add(Tele(STB, a, None, sign="", items=[(a + 0.4, "algae"), (ts, "jar"), (tt + 0.3, "jar"), (tt + 0.6, "jar")], calls=(tse, dur)))
        sc.add(Pill("LO «SCIOGLIPANCIA»", (960, 215), ts, tt, size=50, accent=True))
        sc.add(Pill("3 CONFEZIONI = 100.000 LIRE", (960, 215), tt, tse, size=50, accent=True))
        sc.add(Icon("lire", (1300, 330), tt + 0.4, tse, size=220), "pop")
        sc.add(Pill("FINO A 300 MILIONI DI LIRE AL GIORNO", (960, 215), T("trecento") - 0.2, size=46, accent=True))
        sc.add(Text("secondo i racconti della famiglia", (960, 280), tse + 0.2, size=28, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Icon("money", (1300, 380), T("trecento"), size=200), "pop")
        sc.footer = F_TV + " · ricostruzione · schema"
    elif i == 6:
        tb = T("Diventa") - 0.3; tm = T("Ma") - 0.3; tar = T("Arriva") - 0.3; tsu = T("Sulla") - 0.3
        sc.add(Calendar((330, 420), 220, [(a, "DAL", "1983")], a, tm), "paper")
        sc.add(Board({"w": dict(xy=(880, 560), name="WANNA MARCHI", role="la madre", t=a + 0.3, rot=-3),
                      "s": dict(xy=(1300, 560), name="STEFANIA NOBILE", role="la figlia", t=a + 0.8, rot=3)},
                     [("w", "s", tb)], a, tm + 0.2, cw=260))
        sc.add(Pill("IL BRACCIO DESTRO", (1090, 215), tb, tm + 0.2, size=46, accent=True))
        sc.add(Calendar((330, 420), 220, [(tm, "ANNO", "1990")], tm, None), "paper")
        sc.add(Img(doc_typed(520, 460, "SOCIETÀ DI TELEVENDITE", ["stato:", "", "FALLIMENTO"], size=34), (900, 480), tm + 0.2, anim="drop", rot=-2), "paper")
        sc.add(Stamp("FALLITA", (900, 560), T("fallisce") + 0.2, size=70, rot=-10))
        sc.add(Icon("gavel", (1450, 450), tar, size=280), "hit")
        sc.add(Pill("BANCAROTTA FRAUDOLENTA", (1450, 680), T("bancarotta") - 0.2, size=42, accent=True))
        sc.add(Text("durata della pena: fonti non concordi", (1450, 750), tsu, size=28, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = F_TV + " · documento: ricostruzione grafica"
    elif i == 7:
        tc = T("televisione") + 0.3; tb = T("attraverso") - 0.3; ts = T("Si") - 0.3
        sc.add(Chapter("02", "Il maestro di *vita*", a, tc))
        sc.add(Tele(STB, tc, ts + 0.2, sign="", items=[(tc + 0.3, "jar")]), "whoosh")
        sc.add(Pill("DI NUOVO IN TV", (960, 215), tc + 0.3, tb, size=46, accent=True))
        sc.add(WorldMap(MAPB, [(tb, (-15, 15), 9), (ts, (-20, 12), 9.5)], tb, ts + 0.3,
                        pins=[dict(at="Brasile", label="BRASILE", t=tb + 0.6, side="r", color=RED),
                              dict(at="Milano", label="ITALIA", t=tb + 0.3, side="r", color=GOLD)], title=MT))
        sc.add(Pill("UN UOMO BRASILIANO", (1300, 800), tb + 0.4, ts, size=46, accent=True))
        sc.add(Tele(STB, ts, None, mood="luck", sign="", items=[]), "whoosh")
        sc.add(Figure([(ts, 960, 800)], ts, None, kind="mage", s=0.8, label="«MAESTRO DI VITA»"), "pop")
        sc.add(Icon("amulet", (1250, 420), T("arti") - 0.2, size=200), "pop")
        sc.add(Icon("balls", (660, 420), T("arti") + 0.2, size=220), "pop")
        sc.add(Text("è così che si presenta", (960, 215), ts + 0.4, size=32, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = F_ASC + " · " + MT
    elif i == 8:
        tc = T("cambiano") - 0.6; tn = T("Non") - 0.3; tf = T("fortuna") - 0.4
        sc.add(Img(label_card(["ASCIÈ", "nuova società", "di televendite"], 520, title="LA SOCIETÀ", seed=9), (960, 480), a, tc, anim="drop", rot=-2), "paper")
        sc.add(Tele(STB, tc, tf + 0.2, items=[(tc + 0.2, "jar"), (tc + 0.4, "algae")]), "whoosh")
        sc.add(Stamp("BASTA CREME", (848, 640), tn + 0.4, tf + 0.2, size=80, rot=-8))
        sc.add(Tele(STB, tf, None, mood="luck", sign="FORTUNA", items=[(tf + 0.2, "balls"), (T("sfortuna") - 0.2, "amulet"), (T("malocchio") - 0.2, "eye")], calls=(T("malocchio"), dur)), "whoosh")
        sc.add(Pill("FORTUNA · SFORTUNA · MALOCCHIO", (960, 760), T("malocchio") - 0.2, size=44, accent=True))
        sc.footer = F_ASC + " · ricostruzione · schema"
    elif i == 9:
        tn = T("Numeri") - 0.3; tta = T("talismani") - 0.3; tb = T("Bustine") - 0.3; tr = T("Rametti") - 0.3; tt = T("Tutto") - 0.3
        sc.add(Tele(STB, a, None, mood="luck", sign="", items=[(tn, "lotto"), (tta, "amulet"), (tb, "salt"), (tr, "ivy")], calls=(tt, dur)))
        sc.add(Pill("NUMERI DEL LOTTO", (960, 330), tn, tta, size=48, accent=True))
        sc.add(Pill("TALISMANI E AMULETI", (960, 330), tta, tb, size=48, accent=True))
        sc.add(Pill("SALE DA CUCINA", (960, 330), tb, tr, size=48, accent=True))
        sc.add(Pill("RAMETTI DI EDERA", (960, 330), tr, tt, size=48, accent=True))
        sc.add(Pill("«PROTEZIONE CONTRO LA SFORTUNA»", (960, 330), tt, size=48, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (tn - 0.2, 960, 540, 1.0), (tn + 0.8, 848, 560, 1.25), (tt, 848, 560, 1.25), (tt + 1.0, 960, 540, 1.0), (dur, 960, 540, 1.0))
        sc.footer = F_ASC + " · oggetti generici · ricostruzione"
    elif i == 10:
        ti = T("nomi") - 0.6; tsr = T("sono") - 0.3; te = T("quell'") - 0.6; tp = T("parte") - 0.3
        sc.add(Text("Un dettaglio *importante*", (960, 400), a, ti, size=90, anchor="ma", align="m"))
        sc.add(CardGrid((260, 200, 1660, 820), ti, te + 0.3, cols=16, rows=7, scan=3.0))
        sc.add(Icon("jar", (1500, 300), T("prodotti") - 0.2, te + 0.3, size=160), "pop")
        sc.add(Pill("L'ELENCO DEI VECCHI CLIENTI", (960, 860), tsr, te + 0.3, size=44, accent=True))
        sc.add(Icon("drawer", (600, 470), te, size=280), "pop")
        sc.add(Arrow((780, 470), (1150, 470), te + 0.6, color=RED))
        sc.add(Icon("phone", (1340, 470), tp, size=300), "shake")
        sc.add(Pill("UNA TELEFONATA", (1340, 720), tp + 0.3, size=46, accent=True))
        sc.footer = F_ASC
    elif i == 11:
        tc = T("Dall") - 0.4; tan = T("Anni") - 0.3; to = T("Ora") - 0.3
        sc.add(Chapter("03", "Il *sale*", a, tc))
        sc.add(Salotto(SAL, tc, None, ring=(tc, tan)), "whoosh")
        sc.add(Calendar((1500, 330), 180, [(tc, "ANNO", "2001")], tc, tan), "paper")
        sc.add(Figure([(tc, *WHO)], tc, None, kind="expert", s=0.8, label="UNA TELESPETTATRICE"), "pop")
        sc.add(Icon("jar", (1250, 380), tan, to, size=200, label="EX CLIENTE"), "pop")
        sc.add(Icon("lotto", (1250, 400), to, size=260), "pop")
        sc.add(Pill("I «NUMERI VINCENTI» DEL LOTTO", (960, 215), T("numeri") - 0.2, size=46, accent=True))
        sc.footer = F_TRAP + " · ricostruzione · schema"
    elif i == 12:
        tr = T("rifiuta") - 0.2; tm = T("Ma") - 0.3; tav = T("Avvisa") - 0.3
        sc.add(Salotto(SAL, a, None))
        sc.add(Figure([(a, *WHO)], a, None, kind="expert", s=0.8))
        sc.add(Icon("lire", (1300, 400), a, tav, size=300), "pop")
        sc.add(Pill("300.000 LIRE", (1300, 600), a + 0.3, tav, size=52, accent=True))
        sc.add(Stamp("NO", (1300, 400), tr, tav, size=120, rot=-10))
        sc.add(Icon("studio_tv", (1300, 420), tav, size=300, label="PROGRAMMA SATIRICO"), "pop")
        sc.add(Arrow((700, 600), (1110, 450), tav + 0.3, color=GOLD))
        sc.add(Pill("STRISCIA LA NOTIZIA", (960, 215), T("Striscia") - 0.2, size=50, accent=True))
        sc.footer = F_TRAP + " · ricostruzione · schema"
    elif i == 13:
        tf = T("Fingere") - 0.3; tpa = T("Pagare") - 0.3; tas = T("aspettare") - 0.3; tv = T("vedere") - 0.3
        tac = T("accetta.") - 0.3; tpp = T("paga.") - 0.3
        sc.add(Icon("studio_tv", (1350, 420), a, size=300, label="IL PROGRAMMA"), "pop")
        sc.add(Text("Il *piano*", (560, 210), a + 0.2, size=80, anchor="ma", align="m"))
        sc.add(Pill("1 · FINGERE DI ACCETTARE", (560, 360), tf, size=44, accent=True))
        sc.add(Pill("2 · PAGARE", (560, 470), tpa, size=44))
        sc.add(Pill("3 · ASPETTARE", (560, 580), tas, size=44))
        sc.add(Pill("4 · VEDERE COSA SUCCEDE", (560, 690), tv, size=44))
        sc.add(Figure([(tac, 1100, FY)], tac, None, kind="expert", s=0.75, label="ACCETTA"), "pop")
        sc.add(Icon("lire", (1150, 600), tpp, size=160, move=(tpp + 0.3, 1.0, (1600, 760), 120)), "pop")
        sc.add(Icon("hiddencam", (1700, 260), tpp + 0.4, size=110), "pop")
        sc.footer = F_TRAP
    elif i == 14:
        td = T("Dentro") - 0.3; tl_ = T("Le") - 0.3; ts = T("sciogliere") - 0.3; tn = T("non") - 0.3
        sc.add(Icon("parcel", (960, 470), a, td + 0.2, size=360), "hit")
        sc.add(Pill("UN PACCO", (960, 740), a + 0.3, td, size=48, accent=True))
        sc.add(Icon("lotto", (700, 470), td, tl_ + 0.2, size=280), "pop")
        sc.add(Icon("salt", (1220, 470), td + 0.6, tl_ + 0.2, size=280), "pop")
        sc.add(Img(phone_note(["sciogliere il sale", "nell'acqua"], 520, title="LE ISTRUZIONI"), (560, 470), tl_, anim="drop", rot=-2), "paper")
        sc.add(Text("ricostruzione grafica", (560, 650), tl_ + 0.3, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Icon("glass_salt", (1300, 460), ts, size=380), "pop")
        sc.add(Pill("NON SI SCIOGLIE DEL TUTTO", (1300, 760), tn, size=46, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (tn - 0.3, 960, 540, 1.0), (dur, 1300, 560, 1.3))
        sc.footer = F_TRAP + " · ricostruzione"
    elif i == 15:
        tu = T("Una") - 0.3; tm = T("malocchio") - 0.3; tp = T("Per") - 0.3; tc = T("Costo") - 0.3
        sc.add(Text("La *svolta*", (960, 420), a, tu, size=120, anchor="ma", align="m"))
        sc.add(Salotto(SAL, tu, tm + 0.3, ring=(tu, tm)), "whoosh")
        sc.add(Figure([(tu, *WHO)], tu, tm + 0.3, kind="expert", s=0.8))
        sc.add(Icon("glass_salt", (1300, 420), T("Il") - 0.2, tm + 0.3, size=240, label="«UN SEGNALE»"), "pop")
        sc.add(Icon("eye", (960, 450), tm, tp, size=520), "hit")
        sc.add(Pill("«LEI HA IL MALOCCHIO»", (960, 770), tm + 0.3, tp, size=52, accent=True))
        sc.add(Tele(STB, tp, None, mood="luck", sign="IL RITO", items=[]), "whoosh")
        sc.add(Figure([(tp, 700, 800)], tp, None, kind="mage", s=0.8, label="«MAESTRO DI VITA»"), "pop")
        sc.add(Icon("moon", (1450, 320), tp + 0.4, size=160), "pop")
        sc.add(Icon("lire", (1250, 520), tc, size=320), "hit")
        sc.add(Pill("4 MILIONI DI LIRE", (1250, 740), tc + 0.3, size=56, accent=True))
        sc.footer = F_TRAP + " · ricostruzione · schema"
    elif i == 16:
        tc = T("Con") - 0.3; tq = T("quattro") - 0.6; tt = T("Tutto") - 0.3
        sc.add(Icon("calc", (330, 470), a, size=300, label="UN CALCOLO"), "pop")
        sc.add(Text("300.000 lire (2001)", (640, 300), tc, size=46, fnt=PS, color=WHITE))
        sc.add(Bar(640, 360, 1100, 70, [(tc + 0.6, 240 / 3160)], tc, None, color=GOLD))
        sc.add(Text("≈ 240 € di oggi", (760, 395), T("duecentoquaranta") - 0.2, size=44, fnt=OSW, color=GOLD, anchor="lm"))
        sc.add(Text("4.000.000 lire (2001)", (640, 500), tq, size=46, fnt=PS, color=WHITE))
        sc.add(Bar(640, 560, 1100, 70, [(tq + 0.4, 1.0)], tq, None, color=RED))
        sc.add(Text("più di 3.000 € di oggi", (1720, 645), T("tremila") - 0.2, size=44, fnt=OSW, color=RED, anchor="ra"))
        sc.add(Text("coefficienti ISTAT · valore della moneta · cambio 1.936,27 lire per euro", (960, 730), tc + 0.5, size=26, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Icon("glass_salt", (1040, 820), tt, size=120), "pop")
        sc.add(Pill("TUTTO DA UN PO' DI SALE NELL'ACQUA", (1420, 820), tt + 0.2, size=36, accent=True))
        sc.footer = F_IST + " · Il Post · il Giornale"
    elif i == 17:
        tp = T("Prima") - 0.3; tpo = T("Poi") - 0.3; ti = T("Infine") - 0.3; ts = T("È") - 0.3; tr = T("Riconoscerla") - 0.3
        sc.add(Text("Lo *schema*", (600, 160), a, size=80, anchor="ma", align="m"))
        sc.add(Icon("stairs", (760, 560), a + 0.3, size=600), "pop")
        X = lambda k: 568 + 96 * k; Y = lambda k: 740 - 96 * k
        sc.add(Figure([(tp, X(0), Y(0)), (tpo, X(0), Y(0)), (tpo + 0.8, X(2), Y(2)), (ti, X(2), Y(2)), (ti + 0.8, X(4), Y(4))], tp, None, kind="expert", s=0.5), "pop")
        sc.add(Pill("1 · UNA CIFRA PICCOLA: I NUMERI", (1440, 720), tp, size=36, accent=False))
        sc.add(Pill("2 · UN PROBLEMA: IL «MALOCCHIO»", (1440, 560), tpo, size=36))
        sc.add(Pill("3 · UNA CIFRA GRANDE: IL RITO", (1440, 400), ti, size=36, accent=True))
        sc.add(Arrow((1150, 820), (1150, 330), ts, color=RED))
        sc.add(Text("ogni gradino costa di più", (1440, 300), ts + 0.3, size=30, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Stamp("RICONOSCILA", (760, 420), tr + 0.3, size=80, rot=-8))
        sc.footer = "Analisi Fascicolo Italia sui fatti riportati da Il Post e il Giornale (2005)"
    elif i == 18:
        tc = T("Nella") - 0.4; tcam = T("telecamere") - 0.3; to = T("Ogni") - 0.3; tr = T("registrata") - 0.3
        sc.add(Chapter("04", "La *trappola*", a, tc))
        sc.add(Salotto(SAL, tc, None, cams=[(tcam, (.46, .22)), (tcam + 0.5, (.15, .30)), (tcam + 1.0, (.62, .56))], ring=(to, to + 1.2)), "whoosh")
        sc.add(Figure([(tc, *WHO)], tc, None, kind="expert", s=0.8))
        sc.add(Pill("TELECAMERE NASCOSTE", (960, 215), tcam, to, size=48, accent=True))
        sc.add(Pill("OGNI TELEFONATA", (960, 215), to, T("visita") - 0.3, size=48, accent=True))
        sc.add(Pill("OGNI VISITA", (960, 215), T("visita") - 0.3, T("parola") - 0.3, size=48, accent=True))
        sc.add(Pill("OGNI PAROLA", (960, 215), T("parola") - 0.3, tr, size=48, accent=True))
        sc.add(Stamp("REC", (1480, 300), tr, size=90, rot=-6))
        scene_cam(sc, (0, 960, 540, 1.0), (tcam, 960, 540, 1.0), (tcam + 0.8, 904, 330, 1.5), (to, 904, 330, 1.5), (to + 0.8, 960, 540, 1.0), (dur, 960, 540, 1.0))
        sc.footer = F_TRAP + " · ricostruzione · schema"
    elif i == 19:
        tm = T("Ma") - 0.3; tti = T("tira") - 0.4; td = T("Dall") - 0.3; tal = T("Al") - 0.3; tle = T("Le") - 0.3
        sc.add(Salotto(SAL, a, None, cams=[(a, (.46, .22)), (a, (.62, .56))], ring=(tal, tle)))
        sc.add(Figure([(a, *WHO)], a, None, kind="expert", s=0.8))
        sc.add(Icon("lire", (1300, 400), a, td, size=280), "pop")
        sc.add(Pill("I SOLDI CI SONO", (1300, 260), a + 0.3, tm, size=46))
        sc.add(Stamp("SI TIRA\nINDIETRO", (1300, 420), tti, td, size=70, rot=-10))
        sc.add(Icon("warn", (1300, 400), td, size=240), "hit")
        sc.add(Pill("LA REAZIONE È DURA", (960, 215), td + 0.3, tal, size=44, accent=True))
        sc.add(Pill("AL TELEFONO: MINACCE", (960, 215), tal, tle, size=44, accent=True))
        sc.add(Pill("LA SIGNORA NON PAGA", (960, 215), T("non") - 0.2, size=48, accent=True))
        sc.footer = F_TRAP + " · ricostruzione · schema"
    elif i == 20:
        ts = T("servizio") - 0.6; tdv = T("Davanti") - 0.3; te = T("È") - 0.3
        sc.add(Icon("hiddencam", (960, 450), a, ts, size=360), "pop")
        sc.add(Stamp("REGISTRATO", (960, 700), a + 0.4, ts, size=80, rot=-6))
        sc.add(Calendar((360, 420), 220, [(ts, "ANNO", "2001")], ts, None), "paper")
        sc.add(Icon("studio_tv", (1000, 420), ts + 0.2, size=420, label="IL SERVIZIO VA IN ONDA"), "hit")
        sc.add(Crowd((260, 720, 1660, 890), 22, tdv, None, s=0.3, stagger=0.03))
        sc.add(Text("L'inizio *della fine*", (960, 160), te, size=70, anchor="ma", align="m"))
        sc.footer = F_TRAP
    elif i == 21:
        tg = T("Gli") - 0.3; tr = T("raccolgono") - 0.3; tq = T("quadro") - 0.6
        sc.add(Icon("gdf", (480, 450), a, size=320, label="GUARDIA DI FINANZA"), "pop")
        sc.add(Figure(([(tg, 900, FY), (tg + 2.0, 1100, FY)]), tg, None, kind="expert", s=0.75, carry=[(tg, "magnifier")]), "pop")
        sc.add(Img(doc_typed(420, 380, "SOCIETÀ ASCIÈ", ["affari", "clienti", "incassi"], size=32), (1450, 420), tg + 0.4, tr, anim="drop", rot=2), "paper")
        for k in range(8):
            sc.add(Icon("envelope", (1300 + (k % 4) * 110, 340 + (k // 4) * 120), tr + k * 0.15, size=110), "pop" if k == 0 else None)
        sc.add(Pill("LE DENUNCE DEI CLIENTI", (1460, 620), tr + 0.3, size=40, accent=True))
        sc.add(Pill("MOLTO PIÙ DI UNA TELEFONATA", (960, 215), tq, size=48, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (tq, 960, 540, 1.0), (dur, 1100, 480, 1.15))
        sc.footer = F_ARR + " · documento: ricostruzione grafica"
    elif i == 22:
        tc = T("La") - 0.4; tal = T("altre") - 0.3; to = T("L'operazione") - 0.3
        sc.add(Chapter("05", "L'*operazione*", a, tc))
        sc.add(Calendar((330, 420), 220, [(tc, "GENNAIO 2002", "24")], tc, None), "paper")
        sc.add(Icon("gdf", (330, 740), tc + 0.3, size=180), "pop")
        sc.add(Board({"w": dict(xy=(900, 560), name="WANNA MARCHI", role="arrestata", t=T("Wanna") - 0.2, rot=-3),
                      "s": dict(xy=(1250, 560), name="STEFANIA NOBILE", role="arrestata", t=T("Stefania") - 0.2, rot=3)},
                     [("w", "s", T("Stefania") + 0.3)], tc, None, cw=250))
        sc.add(Icon("handcuffs", (1075, 280), T("arresta") - 0.2, size=160), "pop")
        sc.add(Pill("+ ALTRE 5 PERSONE", (1580, 560), tal, size=44, accent=True))
        sc.add(Pill("OPERAZIONE «TAPIRO SALATO»", (1075, 830), to + 1.0, size=48, accent=True))
        sc.footer = F_ARR + " · silhouette, nessuna foto reale"
    elif i == 23:
        tb = T("È") - 0.3; tp = T("Più") - 0.3; tm = T("tornerà") - 1.4
        sc.add(Text("Manca *qualcuno*", (960, 200), a, tb, size=90, anchor="ma", align="m"))
        sc.add(Figure([(a, 960, FY)], a, tb, kind="mage", s=0.8, label="«MAESTRO DI VITA»"), "pop")
        sc.add(Icon("question", (1250, 500), a + 0.6, tb, size=180), "pop")
        sc.add(WorldMap(MAPB, [(tb, (-15, 18), 8), (tp, (-20, 12), 8.5)], tb, tp + 0.3,
                        pins=[dict(at="Milano", label="ITALIA", t=tb + 0.2, side="r", color=GOLD),
                              dict(at="Brasile", label="BRASILE", t=tb + 1.6, side="r", color=RED)],
                        routes=[dict(pts=["Milano", "Brasile"], t=tb + 0.3, d=1.4, icon="person", color=RED)], title=MT))
        sc.add(Img(sentence_card(["il «maestro di vita»", "rito abbreviato", "4 anni"], title="CONDANNA"), (620, 480), tp, anim="drop", rot=-2), "paper")
        sc.add(Icon("gavel", (1000, 330), tp + 0.3, size=180), "pop")
        sc.add(Icon("plane", (1350, 470), tm, size=240), "pop")
        sc.add(Stamp("MAI TORNATO\nIN ITALIA", (1350, 680), tm + 0.4, size=64, rot=-8))
        sc.footer = F_ARR + " · " + MT
    elif i == 24:
        ts = T("Secondo") - 0.3; tal = T("Al") - 0.3; tc = T("Con") - 0.3
        sc.add(Icon("question", (760, 470), a, ts, size=220), "pop")
        sc.add(Icon("money", (1160, 470), a + 0.3, ts, size=240), "pop")
        sc.add(Icon("gdf", (330, 420), ts, size=220, label="STIMA GDF"), "pop")
        sc.add(Big("60 miliardi", (1060, 360), T("oltre") - 0.2, size=150, sub="di lire", subsize=44))
        sc.add(Icon("calc", (330, 760), tal, size=170), "pop")
        sc.add(Pill("AL CAMBIO: CIRCA 31 MILIONI DI EURO", (1060, 640), tal, size=44))
        sc.add(Pill("CON I COEFFICIENTI ISTAT: OLTRE 45 MILIONI DI EURO DI OGGI", (1060, 760), tc, size=40, accent=True))
        sc.footer = "Fonti: Il Post · Fanpage (stima della Guardia di Finanza) · " + F_IST[7:]
    elif i == 25:
        tse = T("Se") - 0.3; tn = T("ne") - 0.3; tsti = T("È") - 0.3
        sc.add(Text("Proviamo a *immaginarlo*", (960, 200), a, tse, size=80, anchor="ma", align="m"))
        sc.add(Icon("lotto", (960, 480), a + 0.3, tse, size=300), "pop")
        sc.add(Text("60.000.000.000 ÷ 300.000 =", (960, 220), tse, size=60, fnt=OSW, color=WHITE, anchor="ma"))
        for k in range(24):
            sc.add(Icon("envelope", (300 + (k % 12) * 120, 420 + (k // 12) * 130), tse + 0.6 + k * 0.08, size=100), "pop" if k == 0 else None)
        sc.add(Big("200.000", (960, 720), tn, size=150, color=GOLD, count=(0, 200000, lambda v: f"{int(v):,}".replace(",", "."), 1.2)))
        sc.add(Pill("STIMA PER L'ORDINE DI GRANDEZZA · NON IL NUMERO DELLE VITTIME", (960, 860), tsti, size=34, accent=True))
        sc.footer = "Calcolo Fascicolo Italia sulla stima riportata da Il Post e Fanpage"
    elif i == 26:
        tl_ = T("Le") - 0.3; tal = T("Al") - 0.3; tm = T("Ma") - 0.3
        sc.add(Text("E le *vittime?*", (960, 400), a, tl_, size=110, anchor="ma", align="m"))
        sc.add(Big("132", (560, 420), tl_, tm, size=200, color=GOLD, sub="denunce formali"))
        for k in range(6):
            sc.add(Icon("envelope", (1050 + (k % 3) * 160, 360 + (k // 3) * 150), tl_ + 0.3 + k * 0.12, tal, size=130), "pop" if k == 0 else None)
        sc.add(Aula((960, 170, 1760, 870), tal, tm + 0.2, judges_t=tal + 0.3, cage_t=None, motto=False))
        sc.add(Crowd((1000, 720, 1720, 870), 12, tal + 0.4, tm + 0.2, s=0.28, stagger=0.04))
        sc.add(Pill("UNA SESSANTINA DI PARTI CIVILI", (1360, 215), tal + 0.3, tm + 0.2, size=40, accent=True))
        sc.add(Crowd((160, 520, 1760, 880), 70, tm, None, s=0.3, stagger=0.015))
        sc.add(Pill("MIGLIAIA DI TELESPETTATORI", (960, 300), T("migliaia") - 0.2, size=52, accent=True))
        sc.add(Text("secondo le cronache", (960, 370), T("migliaia"), size=28, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: Il Post · QuiFinanza · il Giornale (2005)"
    elif i == 27:
        tc = T("Sul") - 0.4; ti = T("In") - 0.3; td = T("dieci") - 0.3
        sc.add(Chapter("06", "Le *condanne*", a, tc))
        sc.add(Aula((260, 170, 1660, 870), tc, None, judges_t=ti, cage_t=None, motto=False))
        sc.add(Pill("MADRE E FIGLIA IMPUTATE", (960, 215), tc + 0.3, ti, size=46, accent=True))
        sc.add(Img(sentence_card(["Wanna Marchi", "Stefania Nobile", "10 anni a testa"], title="PRIMO GRADO"), (1400, 470), td, anim="drop", rot=2), "paper")
        sc.add(Pill("ASSOCIAZIONE PER DELINQUERE FINALIZZATA ALLA TRUFFA", (960, 820), T("associazione") - 0.2, size=36, accent=True))
        sc.footer = "Fonti: Il Post · Fanpage · documento: ricostruzione grafica"
    elif i == 28:
        tl_ = T("La") - 0.3; tn = T("Nove") - 0.3; tn2 = T("Nove", 1) - 0.3
        sc.add(Calendar((330, 420), 220, [(a, "MARZO", "2008")], a, None), "paper")
        sc.add(Icon("court", (760, 450), tl_, size=300, label="CORTE D'APPELLO DI MILANO"), "pop")
        sc.add(Img(sentence_card(["Wanna Marchi", "9 anni e 6 mesi"], title="APPELLO", seed=43), (1350, 330), tn, anim="drop", rot=-2), "paper")
        sc.add(Img(sentence_card(["Stefania Nobile", "9 anni e 4 mesi"], title="APPELLO", seed=44), (1350, 660), tn2, anim="drop", rot=2), "paper")
        sc.add(Pill("PENE RIDOTTE", (760, 760), tl_ + 1.0, size=44, accent=True))
        sc.footer = F_SENT + " · documenti: ricostruzione grafica"
    elif i == 29:
        tl_ = T("Le") - 0.3; tm = T("Madre") - 0.3; tt = T("Torneranno") - 0.3
        sc.add(Calendar((330, 420), 220, [(a, "MARZO", "2009"), (tt, "ANNO", "2015")], a, None), "paper")
        sc.add(Icon("court", (800, 450), a + 0.3, tm, size=300, label="CORTE DI CASSAZIONE"), "pop")
        sc.add(Stamp("DEFINITIVE", (800, 700), tl_ + 0.3, tm, size=90, rot=-8))
        sc.add(Icon("bars", (1100, 470), tm, tt, size=360), "pop")
        sc.add(Pill("DI NUOVO IN CARCERE", (1100, 760), tm + 0.3, tt, size=46, accent=True))
        sc.add(Door((1100, 520), 220, 400, tt, None, open_t=tt + 0.6), "pop")
        sc.add(Pill("LIBERE DAL 2015", (1100, 800), tt + 0.4, size=46, accent=True))
        sc.footer = F_SENT
    elif i == 30:
        tc = T("Ricapitolando.") - 0.2; tu2 = T("Una", 1) - 0.3; tf = T("condanne") - 0.3
        sc.add(Chapter("", "Il *verdetto*", a, T("Una") - 0.1))
        icons = [("studio_tv", "regina", "TELEVENDITE"), ("amulet", "maestro", "MAESTRO DI VITA"), ("salt", "bustine", "SALE"),
                 ("ivy", "rametti", "EDERA"), ("hiddencam", "telecamera", "TRAPPOLA"), ("gavel", "condanne", "CONDANNE")]
        for k, (ic, w_, lab) in enumerate(icons):
            sc.add(Icon(ic, (310 + k * 260, 360), T(w_) - 0.2, size=160, label=lab), "pop")
        sc.add(Timeline(260, 1660, 720, [dict(top="2001", bottom="la trappola", t=tu2, hl=True),
                                         dict(top="GEN 2002", bottom="gli arresti", t=tu2 + 0.6),
                                         dict(top="MAR 2008", bottom="l'appello", t=tu2 + 1.2),
                                         dict(top="MAR 2009", bottom="condanne definitive", t=tf, hl=True),
                                         dict(top="2015", bottom="di nuovo libere", t=tf + 0.6)], tu2, None))
        sc.footer = "Fonti: Il Post · Fanpage · QuiFinanza · il Giornale · VareseNews · Blitz quotidiano"
    elif i == 31:
        tl_ = T("Le") - 0.3; tq = T("Qualcuno") - 0.3; tpr = T("promette") - 0.3; tri = T("rivela") - 0.3; tch = T("chiede") - 0.3; te = T("È") - 0.3
        sc.add(Text("E *oggi?*", (960, 200), a, size=90, anchor="ma", align="m"))
        sc.add(Icon("studio_tv", (960, 480), a + 0.3, tq, size=320), "pop")
        sc.add(Pill("LO SCHEMA SI RICONOSCE ANCORA", (960, 760), tl_ + 0.6, tq, size=44, accent=True))
        steps = [("phone", tq, "TI CONTATTA PER PRIMO"), ("balls", tpr, "TI PROMETTE FORTUNA"), ("eye", tri, "UN PROBLEMA «INVISIBILE»"), ("lire", tch, "CHIEDE SOLDI")]
        for k, (ic, tt, lab) in enumerate(steps):
            sc.add(Icon(ic, (330 + k * 420, 480), tt, size=200, label=lab), "pop")
            if k: sc.add(Arrow((330 + (k - 1) * 420 + 120, 480), (330 + k * 420 - 120, 480), tt, color=GOLD))
        sc.add(Stamp("RIATTACCA", (960, 760), te + 0.3, size=90, rot=-6))
        sc.footer = "Consiglio generale di prudenza · analisi Fascicolo Italia"
    elif i == 32:
        ts = T("Scrivilo") - 0.3; ti = T("Iscriviti") - 0.3
        sc.add(Text("Perché tante persone hanno creduto\na un pugno di *sale?*", (960, 220), a, ti, size=76, anchor="ma", align="m"))
        sc.add(Icon("salt_pile", (960, 560), a + 0.3, ti, size=300), "pop")
        sc.add(Icon("question", (1260, 520), a + 0.8, ti, size=160), "pop")
        sc.add(Pill("SCRIVILO NEI COMMENTI", (960, 820), ts, ti, size=44, accent=True))
        sc.add(Img(wordmark(150), (960, 480), ti, anim="pop", shadow=False), "hit")
        sc.add(Text("ogni giorno un nuovo caso", (960, 640), ti + 0.4, size=48, fnt=PS, color=GREY, anchor="ma"))
        sc.footer = "Ricostruzione a scopo divulgativo · voce generata con sintesi vocale"
    return sc

def thumbnail(path="thumbnail.jpg"):
    im = make_bg(9); d = ImageDraw.Draw(im)
    t = rich_img("IL SALE\nCONTRO IL\n*MALOCCHIO*", SERIF, 128, WHITE, RED, lh=1.0)
    im.alpha_composite(t, (90, 140))
    tv = fx.icon("studio_tv", 380); im.alpha_composite(tv, (1180, 120))
    s = fx.icon("salt", 300).rotate(-8, expand=True, resample=Image.BICUBIC); im.alpha_composite(s, (1160, 520))
    e = fx.icon("eye", 300); im.alpha_composite(e, (1500, 470))
    cam = fx.icon("hiddencam", 170); im.alpha_composite(cam, (1580, 190))
    st = stamp_img("CASO 014", RED, 70, -10); im.alpha_composite(st, (1520, 40))
    d.text((100, 840), "LA TRAPPOLA CON LE TELECAMERE NASCOSTE", font=font(OSW, 54, 600), fill=GOLD + (255,))
    d.text((1880, 1060), "ricostruzione grafica · oggetti generici", font=font(COURR, 22), fill=(200, 190, 170, 255), anchor="rs")
    wm_ = wordmark(60, sub=False); im.alpha_composite(wm_, (100, 960))
    im.convert("RGB").save(path, quality=92)
