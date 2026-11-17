import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from rom import *

W, H = 1920, 1080
FY = 870
BB = (200, 240, 1720, 860)      # scenografia: la banca con la cassa
HB = (160, 160, 1760, 880)      # aula della Camera
F_BANK = "Fonti: Wikipedia (Banca Romana scandal) · IMF Working Paper 17/274 · moruzzi.it"
F_ISP = "Fonti: Filodiritto · Skuola.net · IMF WP 17/274 · moruzzi.it"
F_CAM = "Fonti: Wikipedia · Skuola.net · IMF WP 17/274 · Filodiritto"
F_BI = "Fonti: Banca d'Italia · IMF WP 17/274 · Wikipedia (Bank of Italy)"
F_PROC = "Fonti: Wikipedia · IMF WP 17/274 · Filodiritto · moruzzi.it"
BANKS = [("BANCA NAZIONALE\nNEL REGNO", "bankold"), ("BANCA NAZ.\nTOSCANA", "bankold"), ("BANCA TOSCANA\nDI CREDITO", "bankold"),
         ("BANCO DI\nNAPOLI", "bankold"), ("BANCO DI\nSICILIA", "bankold"), ("BANCA\nROMANA", "bankold")]

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

def six(sc, t0, t1, hl=None, hl_t=None, y=430, size=170, gone=None):
    for k, (lab, ic) in enumerate(BANKS):
        x = 260 + k * 280
        sc.add(Icon(ic, (x, y), t0 + 0.18 * k, t1, size=size), "pop" if k == 0 else None)
        sc.add(Text(lab.replace("\n", "\n"), (x, y + size / 2 + 20), t0 + 0.18 * k, t1, size=28, fnt=OSW, color=GOLD if k == 5 else WHITE, anchor="ma", align="m"))
    if hl_t is not None:
        sc.add(Line((260 + 5 * 280 - 120, y + size / 2 + 110), (260 + 5 * 280 + 120, y + size / 2 + 110), hl_t, t1, color=RED, width=10))

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
        tf = T("Fine") - 0.3; ti = T("In") - 0.3; tq = T("qualcuno") - 0.3; ts = T("Stesso") - 0.3; tn = T("E") - 0.3
        sc.add(MapEl((160, 160, 1760, 880), [(a, (12.5, 42.5), 140), (ti, (12.50, 41.90), 600)], a, ti + 0.4,
                     pins=[dict(at="Roma", label="ROMA", t=a + 0.3, side="r", color=RED)], title="mappa: Natural Earth · schema non in scala"))
        sc.add(Calendar((420, 420), 220, [(tf, "FINE", "'800")], tf, ti + 0.4), "paper")
        sc.add(Bank(BB, ti, tq + 0.2, level=[(0, 0.8)], limit=False, label=""))
        sc.add(Pill("PUÒ STAMPARE DENARO VERO", (960, 185), ti + 0.6, tq + 0.2, size=44, accent=True))
        sc.add(Figure(walk([(-60, FY), (520, FY)], tq - 0.6, 420), tq - 0.6, kind="expert", s=0.9, carry=[(tq + 0.3, "magnifier")]), "pop")
        sc.add(Twins((1100, 500), 520, tq + 0.2, hl_t=tn + 0.3, gap=40))
        sc.add(Pill("STESSO VALORE", (1100, 220), ts, T("Stessa") - 0.2, size=44))
        sc.add(Pill("STESSA FIRMA", (1100, 220), T("Stessa") - 0.1, tn, size=44))
        sc.add(Pill("STESSO NUMERO DI SERIE", (1100, 220), tn + 0.1, size=48, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (tn, 960, 540, 1.0), (tn + 1.0, 1100, 620, 1.18))
        sc.footer = F_BANK + " · banconote ricostruite"
    elif i == 1:
        te = T("È") - 0.3; tq = T("Questo") - 0.3; tv = T("Vedremo") - 0.3
        sc.add(Stamp("NON È UN\nFALSARIO", (960, 450), a + 0.2, te, size=96, rot=-8))
        six(sc, te, tq, hl_t=T("sei") + 0.4)
        sc.add(Pill("6 BANCHE AUTORIZZATE A STAMPARE BANCONOTE", (960, 210), T("sei") - 0.1, tq, size=44, accent=True))
        sc.add(Img(cover_folder(), (960, 500), tq + 0.1, tv, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 010", (1150, 300), T("fascicolo") + 0.2, tv, size=70, rot=-12))
        sc.add(Icon("report", (360, 470), tv + 0.1, size=200, label="L'ISPEZIONE"), "pop")
        sc.add(Icon("drawer", (760, 470), T("perché") - 0.3, size=200, label="LA RELAZIONE NASCOSTA"), "pop")
        sc.add(Icon("chamber", (1160, 470), T("come") - 0.3, size=200, label="LO SCANDALO"), "pop")
        sc.add(Icon("newbank", (1560, 470), T("Banca") - 0.3, size=200, label="LA BANCA D'ITALIA"), "pop")
        sc.footer = "Fonti: Wikipedia · IMF WP 17/274 · Banca d'Italia"
    elif i == 2:
        tn = T("Nell'Italia") - 0.4; tc = T("Ce") - 0.3; ts = T("Sono") - 0.3
        sc.add(Chapter("01", "Sei *banche*", a, tn))
        sc.add(MapEl((900, 160, 1760, 880), [(tn, (12.2, 42.2), 75), (ts + 1.5, (12.2, 42.2), 77)], tn, None,
                     pins=[dict(at="Torino", label="TORINO", t=tc + 0.2, side="r", color=GOLD), dict(at="Firenze", label="FIRENZE ×2", t=tc + 0.5, side="r", color=GOLD),
                           dict(at="Roma", label="ROMA", t=tc + 0.8, side="r", color=RED), dict(at="Napoli", label="NAPOLI", t=tc + 1.1, side="r", color=GOLD),
                           dict(at="Palermo", label="PALERMO", t=tc + 1.4, side="r", color=GOLD)], title="mappa: Natural Earth · sedi storiche · schema non in scala"))
        sc.add(Pill("NON UNA SOLA BANCA CHE STAMPA I SOLDI", (520, 260), T("non") - 0.2, tc, size=44, accent=True))
        sc.add(Big("6", (420, 520), tc, size=220, color=RED, fnt=OSW, sub="banche di emissione"), "hit")
        sc.add(Pill("EREDITÀ DEGLI STATI PRE-UNITARI", (520, 780), ts, size=44))
        sc.footer = "Fonti: IMF WP 17/274 · Wikipedia · Filodiritto"
    elif i == 3:
        tr = T("E") - 0.3; tch = T("che") - 0.3
        six(sc, a, None, size=180)
        sc.add(Pill("BANCA NAZIONALE NEL REGNO", (960, 210), a, T("due") - 0.2, size=40))
        sc.add(Pill("DUE BANCHE TOSCANE", (960, 210), T("due") - 0.1, T("il") - 0.2, size=40))
        sc.add(Pill("NAPOLI · SICILIA", (960, 210), T("il") - 0.1, tr, size=40))
        sc.add(Arrow((1660, 780), (1660, 650), tr + 0.3, color=RED))
        sc.add(Pill("A ROMA: LA BANCA ROMANA", (960, 210), tr, tch, size=46, accent=True))
        sc.add(Calendar((1500, 760), 150, [(tch, "PRIMA DEL", "1870")], tch), "paper")
        sc.add(Pill("EX BANCA DELLO STATO PONTIFICIO", (960, 210), tch + 0.2, size=44, accent=True))
        sc.footer = F_BANK
    elif i == 4:
        tl_ = T("La") - 0.3; te = T("E") - 0.3; tc = T("È") - 0.3
        sc.add(Bank(BB, a, None, level=[(a, 0.3), (a + 1.6, 0.8), (tl_ + 0.4, 1.0)], label="schema semplificato · non in scala"))
        sc.add(Pill("NON PUÒ STAMPARE QUANTO VUOLE", (960, 185), a + 0.3, tl_, size=42, accent=True))
        sc.add(Pill("LA LEGGE FISSA UN LIMITE", (960, 185), tl_, te, size=46, accent=True))
        sc.add(Img(banknote(560, serial="N. 048217", hl=True), (560, 540), te, tc + 1.0, anim="drop", rot=-3), "paper")
        sc.add(Icon("passport", (1300, 500), T("come") - 0.3, tc + 1.0, size=240, label="COME UNA CARTA D'IDENTITÀ"), "pop")
        sc.add(Pill("UN NUMERO, UN BIGLIETTO", (960, 185), te + 0.3, tc, size=44))
        sc.add(Icon("magnifier", (1500, 760), tc + 1.0, size=180, label="CONTROLLO"), "pop")
        sc.footer = "Fonti: Wikipedia · moruzzi.it · Banca d'Italia · schema non in scala"
    elif i == 5:
        ts = T("Sono") - 0.3; tr = T("Roma") - 0.3; te = T("e", 1) - 0.3
        sc.add(Img(label_card(["Bernardo Tanlongo", "governatore della", "Banca Romana dal 1881"], 560, title="SCHEDA"), (560, 500), a + 0.2, ts, anim="drop", rot=-2), "paper")
        sc.add(Figure([(0, 1300, FY)], a + 0.4, ts, kind="suit", s=1.0, label="SAGOMA · NESSUNA FOTO"), "pop")
        sc.add(Icon("crane", (480, 450), ts + 0.3, size=300, label="GRANDI CANTIERI"), "pop")
        sc.add(Pill("ROMA CAPITALE", (1200, 220), tr, size=46, accent=True))
        for k in range(5): sc.add(Icon("house", (900 + k * 180, 520 - (k % 2) * 60), T("quartieri") - 0.3 + 0.15 * k, size=150), "pop" if k == 0 else None)
        sc.add(Icon("notes", (1200, 760), te, size=200, label="PRESTITI A PIENE MANI"), "pop")
        sc.footer = "Fonti: Wikipedia · moruzzi.it · Filodiritto · Skuola.net"
    elif i == 6:
        tl_ = T("Le") - 0.3; te = T("E") - 0.3
        sc.add(Icon("crash", (560, 470), a + 0.2, size=360, label="CROLLA L'EDILIZIA"), "pop")
        sc.add(Icon("quake", (1320, 470), T("crolla") - 0.2, tl_, size=300, anim="shake"), "hit")
        for k in range(3):
            sc.add(Figure([(0, 1100 + k * 230, FY)], tl_ + 0.15 * k, te, kind="worker", s=0.8, arms=[(tl_ + 0.6, "up")]), "pop" if k == 0 else None)
        sc.add(Pill("PRESTITI NON RESTITUITI", (1330, 220), tl_ + 0.2, te, size=44, accent=True))
        sc.add(Bank(BB, te, None, level=[(te, 0.9)], hole_t=T("buchi") - 0.2, label=""))
        sc.add(Pill("BUCHI NEI CONTI", (960, 185), T("buchi") - 0.1, size=46, accent=True))
        sc.footer = "Fonti: Wikipedia · Filodiritto · Skuola.net"
    elif i == 7:
        ti = T("Il") - 0.4; tb = T("Bisogna") - 0.3
        sc.add(Chapter("02", "L'*ispezione*", a, ti))
        sc.add(Calendar((420, 440), 240, [(ti, "GIUGNO", "1889")], ti), "paper")
        sc.add(Img(label_card(["governo Crispi", "ordina un'ispezione", "nelle banche di emissione"], 640, title="1889"), (1200, 460), T("ordina") - 0.3, anim="drop", rot=2), "paper")
        sc.add(Icon("magnifier", (1500, 760), tb, size=200, label="CONTI IN ORDINE?"), "pop")
        sc.footer = "Fonti: Wikipedia · Filodiritto · Skuola.net"
    elif i == 8:
        tg = T("Giuseppe") - 0.3; tgb = T("Gustavo") - 0.3; ta = T("Aprono") - 0.3
        sc.add(Bank(BB, a, None, level=[(a, 1.2)], insp=[(a + 0.3, "suit"), (a + 0.6, "expert")]))
        sc.add(Pill("ARRIVANO DUE ISPETTORI", (960, 185), a + 0.2, tg, size=44, accent=True))
        sc.add(Pill("SEN. GIUSEPPE GIACOMO ALVISI", (960, 185), tg, tgb, size=42, accent=True))
        sc.add(Pill("GUSTAVO BIAGINI · MINISTERO DEL TESORO", (960, 185), tgb, ta, size=42, accent=True))
        sc.add(Pill("REGISTRI · BIGLIETTI · CASSA", (960, 185), ta, size=44))
        sc.add(Icon("book", (1450, 520), ta, T("contano") - 0.2, size=220), "pop")
        sc.add(Icon("notes", (1450, 520), T("contano") - 0.2, T("controllano") - 0.2, size=220), "pop")
        sc.add(Icon("safe", (1450, 520), T("controllano") - 0.2, size=220), "pop")
        sc.footer = F_ISP + " · sagome, nessuna foto reale"
    elif i == 9:
        tp = T("Primo") - 0.3; ts = T("Secondo") - 0.3
        sc.add(Bank((820, 240, 1760, 860), a, None, level=[(a, 0.8), (tp + 0.6, 1.4)], hole_t=T("mancano") - 0.2))
        sc.add(Stamp("1", (420, 330), tp, ts, size=80, rot=-6))
        sc.add(Big("+25 mln", (420, 520), T("25") - 0.3, ts, size=110, color=RED, fnt=OSW, sub="di lire oltre il limite"), "hit")
        sc.add(Stamp("2", (420, 330), ts, size=80, rot=-6))
        sc.add(Big("−9 mln", (420, 520), T("nove") - 0.3, size=120, color=RED, fnt=OSW, sub="mancano in cassa"), "hit")
        sc.footer = "Fonti: IMF WP 17/274 · moruzzi.it · Skuola.net · cifre approssimate · schema non in scala"
    elif i == 10:
        tg = T("Gli") - 0.3; td = T("Due") - 0.3; tf = T("Facciamo") - 0.3; tn = T("nei") - 0.3; tl_ = T("L'altro") - 0.3
        sc.add(Pill("IL DETTAGLIO PIÙ GRAVE", (960, 200), a + 0.1, tg, size=48, accent=True))
        sc.add(Icon("serial", (960, 470), tg, td, size=380, label="NUMERI DI SERIE DOPPI"), "pop")
        sc.add(Twins((960, 520), 560, td, tf, hl_t=T("lo") - 0.1))
        sc.add(Pill("ESEMPIO", (960, 200), tf, size=48, accent=True))
        sc.add(Img(banknote(420, serial="N. 000731", hl=True), (560, 430), tf + 0.4, anim="drop", rot=-2), "paper")
        sc.add(Img(banknote(420, serial="N. 000731", hl=True), (1360, 430), tf + 0.8, anim="drop", rot=2), "paper")
        sc.add(Img(label_card(["N. 000731 ......... 100 L.", "N. 000732 ......... 100 L."], 620, title="REGISTRO"), (960, 760), tn, anim="drop"), "paper")
        sc.add(Stamp("NON REGISTRATO", (1360, 430), tl_ + 0.2, size=50, rot=-10))
        sc.footer = "Fonti: Wikipedia · moruzzi.it · IMF WP 17/274 · esempio illustrativo, banconote ricostruite"
    elif i == 11:
        tn = T("Nero") - 0.3; tu = T("Una") - 0.3
        sc.add(Img(doc_typed(600, 640, "RELAZIONE D'ISPEZIONE",
                              ["Circolazione oltre il limite", "di legge: circa 25 milioni.", "", "Ammanco di cassa:", "circa 9 milioni.", "",
                               "Biglietti con numeri", "di serie duplicati."], footer="Banca Romana · 1889-1890"), (560, 510), a + 0.2, anim="drop", rot=-2), "paper")
        sc.add(Pill("ECCEDENZE", (1360, 330), T("eccedenze") - 0.2, size=44, accent=True))
        sc.add(Pill("AMMANCHI", (1360, 450), T("ammanchi") - 0.2, size=44, accent=True))
        sc.add(Pill("BIGLIETTI DUPLICATI", (1360, 570), T("biglietti") - 0.2, size=44, accent=True))
        sc.add(Icon("newspaper", (1360, 760), tu + 0.6, size=180, label="CASO NAZIONALE?"), "pop")
        sc.footer = F_ISP + " · documento ricostruito, non originale"
    elif i == 12:
        tl_ = T("La") - 0.3; tp = T("Passa") - 0.3
        sc.add(Chapter("03", "Il *cassetto*", a, a + 2.0))
        sc.add(Stamp("NON SUCCEDE\nNIENTE", (960, 460), a + 2.0, tl_, size=90, rot=-6))
        sc.add(Icon("report", (700, 470), tl_, tp, size=320), "pop")
        sc.add(Icon("drawer", (1250, 470), tl_ + 0.8, tp, size=320, label="NON RESA PUBBLICA"), "paper")
        sc.add(Calendar((960, 470), 300, [(tp, "ANNO", "1890"), (T("Passa", 1) - 0.2, "ANNO", "1891"), (T("Passa", 2) - 0.2, "ANNO", "1892")], tp), "paper")
        sc.add(ClockFace((1500, 440), 120, tp, start=8.0, speed=4.0, label="PASSANO GLI ANNI"))
        sc.footer = "Fonti: Wikipedia · moruzzi.it · Skuola.net"
    elif i == 13:
        tc = T("chiusa") - 0.3; tn = T("Nel") - 0.3; tt = T("Tanlongo") - 0.3
        sc.add(Icon("drawer", (960, 470), a + 0.1, tn, size=380), "pop")
        sc.add(Icon("report", (960, 470), a + 0.3, tc + 0.4, size=200, move=(tc, 0.8, (960, 560), 0)), None)
        sc.add(Pill("CHIUSA IN UN CASSETTO", (960, 200), tc, tn, size=46, accent=True))
        sc.add(Bank(BB, tn, None, level=[(tn, 1.2)]))
        sc.add(Crowd((260, 720, 1000, 870), 6, tn + 0.5, None, s=0.38, walk=60))
        sc.add(Pill("LA BANCA CONTINUA A LAVORARE", (960, 185), tn + 0.2, tt, size=44))
        sc.add(Pill("TANLONGO RESTA AL SUO POSTO", (960, 185), tt, size=44, accent=True))
        sc.footer = "Fonti: Wikipedia · moruzzi.it · Skuola.net · schema non in scala"
    elif i == 14:
        ti = T("Il") - 0.3; tm = T("Manca") - 0.3
        sc.add(Pill("A ROMA I SEGRETI DURANO POCO", (960, 200), a + 0.1, ti, size=46, accent=True))
        sc.add(Icon("report", (420, 480), a + 0.3, size=240), "pop")
        sc.add(Icon("chamber", (1500, 480), T("Camera") - 0.3, size=320, label="CAMERA DEI DEPUTATI"), "pop")
        sc.add(Arrow((560, 480), (1300, 480), ti + 0.4, color=GOLD, dashed=True, bend=-0.2))
        sc.add(Icon("envelope", (560, 480), ti + 0.4, size=120, move=(ti + 0.5, 1.8, (1300, 480), 120)), None)
        sc.add(Icon("mic", (960, 700), tm, size=200, label="CHI LO LEGGE AD ALTA VOCE?"), "pop")
        sc.footer = "Fonti: Wikipedia · moruzzi.it · Skuola.net"
    elif i == 15:
        tc = T("Camera") - 0.3; ts = T("Si") - 0.3; te = T("E") - 0.3
        sc.add(Chapter("04", "Il *discorso*", a, a + 2.2))
        sc.add(Calendar((960, 460), 300, [(a + 2.2, "DICEMBRE 1892", "20")], a + 2.2, tc + 0.3), "paper")
        sc.add(Hemicycle(HB, tc, None, speak_t=ts + 0.3))
        sc.add(Pill("CAMERA DEI DEPUTATI", (960, 200), tc + 0.2, ts, size=46, accent=True))
        sc.add(Pill("NAPOLEONE COLAJANNI, DEPUTATO", (960, 200), T("Napoleone") - 0.2, te, size=46, accent=True))
        sc.add(Text("sagoma · nessuna foto reale", (460, 900), ts + 0.5, size=24, fnt=COURR, color=GREY, anchor="ma"))
        scene_cam(sc, (0, 960, 540, 1.0), (te, 960, 540, 1.0), (te + 1.0, 640, 620, 1.25))
        sc.footer = F_CAM + " · schema non in scala"
    elif i == 16:
        tl_ = T("Le") - 0.3; tn = T("La") - 0.3; ti = T("Il") - 0.3
        sc.add(Hemicycle(HB, a, None, speak_t=a, stir_t=tn, dim=0.0))
        sc.add(Pill("LE CIFRE", (1350, 220), tl_, size=40, accent=True))
        sc.add(Pill("LE ECCEDENZE", (1350, 300), T("eccedenze") - 0.2, size=40, accent=True))
        sc.add(Pill("I BIGLIETTI DOPPI", (1350, 380), T("biglietti") - 0.2, size=40, accent=True))
        sc.add(Img(banknote(300, serial="N. 048217", hl=True), (1350, 520), T("biglietti"), anim="drop", rot=3), "paper")
        sc.add(Icon("newspaper", (960, 520), tn, ti, size=260, label="LA NOTIZIA FA IL GIRO DEL PAESE"), "pop")
        sc.add(Pill("IL SEGRETO ORA È DI TUTTI", (960, 560), ti, size=52, accent=True))
        sc.footer = F_CAM + " · schema non in scala"
    elif i == 17:
        tv = T("Viene") - 0.3; tg = T("guidata") - 0.3; tq = T("Questa") - 0.3
        sc.add(Icon("hourglass", (960, 470), a + 0.1, tv, size=300, label="NON SI PUÒ PIÙ ASPETTARE"), "pop")
        sc.add(Icon("meeting", (560, 470), tv, tq, size=320, label="NUOVA COMMISSIONE"), "pop")
        sc.add(Img(label_card(["Enrico Martuscelli", "presidente della", "Corte dei conti"], 560, title="SCHEDA"), (1300, 470), tg, tq, anim="drop", rot=2), "paper")
        sc.add(Calendar((700, 450), 240, [(tq, "DICEMBRE", "1892"), (tq + 1.0, "GENNAIO", "1893")], tq), "paper")
        sc.add(Pill("RISULTATI IN POCHE SETTIMANE", (1250, 450), T("risultati") - 0.2, size=46, accent=True))
        sc.footer = "Fonti: Filodiritto · Skuola.net · Wikipedia"
    elif i == 18:
        ts = T("Secondo") - 0.3; tq = T("quasi") - 0.3; tc = T("Sulle") - 0.3
        sc.add(Chapter("05", "Le banconote *gemelle*", a, ts))
        sc.add(Bar(260, 420, 1100, 90, [(ts + 0.6, 0.0), (ts + 1.6, 1.0)], ts + 0.4, None, color=RED, label="IN CIRCOLAZIONE · OLTRE 110 MLN (stime)"))
        sc.add(Bar(260, 640, 1100, 90, [(ts + 0.4, 0.0), (ts + 1.2, 0.55)], ts + 0.4, None, color=GOLD, label="LIMITE CONSENTITO"))
        sc.add(Text("IN CIRCOLAZIONE · OLTRE 110 MLN DI LIRE (stime)", (260, 340), ts + 0.4, size=40, fnt=OSW, color=WHITE))
        sc.add(Text("LIMITE CONSENTITO", (260, 560), ts + 0.4, size=40, fnt=OSW, color=GOLD))
        sc.add(Stamp("QUASI IL\nDOPPIO", (1540, 520), tq, size=80, rot=-8))
        sc.add(Pill("CIFRE ESATTE: LE VERSIONI NON COINCIDONO", (960, 820), tc, size=40))
        sc.footer = "Fonti: Filodiritto · Skuola.net · Wikipedia (cifre diverse) · schema non in scala"
    elif i == 19:
        tu = T("Una") - 0.3; tt = T("Tutte") - 0.3; ts = T("Se") - 0.3
        sc.add(Twins((960, 460), 520, a + 0.2, tu, hl_t=a + 1.0, serial="N. 112305", value="50"))
        sc.add(Icon("press", (520, 480), tu, tt, size=300, label="UNA SECONDA SERIE"), "pop")
        for k in range(6):
            sc.add(Icon("notes_dup", (1050 + (k % 3) * 220, 400 + (k // 3) * 200), tu + 0.6 + 0.2 * k, tt, size=170), "pop" if k == 0 else None)
        sc.add(Pill("STESSI NUMERI DI QUELLI GIÀ ESISTENTI", (960, 200), T("con") - 0.2, tt, size=42, accent=True))
        sc.add(Big("40 mln", (960, 450), tt, size=200, color=RED, fnt=OSW, count=(0, 40, lambda z: f"{z:.0f} mln", 1.2), sub="di lire · circa"), "hit")
        sc.add(Icon("question", (1550, 760), ts, size=160), "pop")
        sc.add(Pill("IN CIRCOLAZIONE? LE FONTI NON CONCORDANO", (960, 760), ts + 0.2, size=36))
        sc.footer = "Fonti: Wikipedia · IMF WP 17/274 · moruzzi.it · Filodiritto · Skuola.net"
    elif i == 20:
        tc = T("Con") - 0.3; ts = T("sono") - 0.3; te = T("È") - 0.3; tu = T("una", 1) - 0.3
        sc.add(Big("40.000.000 L.", (960, 420), a + 0.2, tc, size=150, color=GOLD, fnt=OSW, sub="lire del 1893"), "hit")
        sc.add(Icon("istat", (560, 480), tc, te, size=320, label="COEFFICIENTI ISTAT"), "pop")
        sc.add(Big("≈ 210 mln €", (1250, 450), T("sono", 1) - 0.3, te, size=130, color=RED, fnt=OSW, count=(0, 210, lambda z: f"≈ {z:.0f} mln €", 1.2), sub="euro di oggi (stima)"), "hit")
        sc.add(Text("40 mln di lire 1893 × coeff. ISTAT ≈ 10.164 ÷ 1.936,27 = circa 210 mln di euro (2024)", (960, 760), T("sono", 1) + 0.3, size=30, fnt=COURR, color=GREY, anchor="ma"))
        for k in range(10):
            sc.add(Icon("notes", (300 + (k % 5) * 330, 330 + (k // 5) * 230), te + 0.15 * k, size=190), "pop" if k == 0 else None)
        sc.add(Stamp("NON DOVEVA\nESISTERE", (960, 500), tu + 0.6, size=90, rot=-8))
        sc.footer = "Calcolo: ISTAT, Il valore della moneta in Italia 1861-2024 (indici, base 1913) · stima indicativa"
    elif i == 21:
        tb = T("Bernardo") - 0.3; tc = T("Con") - 0.3; ti = T("Il") - 0.3
        sc.add(Calendar((960, 460), 300, [(a, "GENNAIO", "1893")], a, tb + 0.4), "paper")
        sc.add(Figure([(0, 700, FY)], tb, kind="suit", s=1.0, label="B. TANLONGO"), "pop")
        sc.add(Figure(walk([(1950, FY), (980, FY)], tb, 500), tb, kind="police", s=1.0, flip=-1), "pop")
        sc.add(Icon("handcuffs", (840, 600), T("arrestato") - 0.2, size=180), "hit")
        sc.add(Pill("ARRESTATO", (960, 200), T("arrestato") - 0.1, tc, size=50, accent=True))
        sc.add(Pill("CON LUI ALTRI DIRIGENTI DELLA BANCA", (960, 200), tc, ti, size=44, accent=True))
        sc.add(Icon("bankold", (330, 330), ti, size=220, label="L'UFFICIO"), "pop")
        sc.add(Arrow((480, 330), (1380, 330), ti + 0.6, color=RED, bend=-0.15))
        sc.add(Icon("prison", (1560, 330), T("cella") - 0.4, size=240, label="LA CELLA"), "pop")
        sc.footer = F_PROC + " · sagome, nessuna foto reale"
    elif i == 22:
        ts = T("Secondo") - 0.3; tsu = T("Sono") - 0.3; tm = T("Ma") - 0.3
        sc.add(Icon("bars", (560, 470), a, size=360), "pop")
        sc.add(Figure([(0, 560, FY)], a + 0.2, kind="suit", s=0.9), None)
        sc.add(Bubble((1100, 380), 150, ts, tsu, inner="notes"), "pop")
        sc.add(Pill("DENARO A POLITICI E GIORNALISTI?", (1150, 640), ts + 0.3, tsu, size=40))
        sc.add(Pill("SECONDO LE RICOSTRUZIONI: SUE DICHIARAZIONI", (1250, 200), ts, size=36, accent=True))
        sc.add(Stamp("MAI DIMOSTRATE\nIN TRIBUNALE", (1250, 480), T("in") - 0.1, size=72, rot=-8))
        sc.add(Icon("quake", (1250, 760), tm, size=200, anim="shake", label="TREMANO I PALAZZI"), "hit")
        sc.footer = "Fonti: Filodiritto · Skuola.net · accuse mai provate in giudizio"
    elif i == 23:
        tl_ = T("La") - 0.3; t23 = T("23") - 0.3; tg = T("Il", 1) - 0.3
        sc.add(Chapter("06", "La *crisi*", a, tl_))
        sc.add(Hemicycle(HB, tl_, t23 + 1.0, fill_t=tl_))
        sc.add(Icon("meeting", (960, 420), tl_ + 0.5, t23, size=260, label="COMITATO DI DEPUTATI"), "pop")
        sc.add(Calendar((560, 460), 260, [(t23, "NOVEMBRE 1893", "23"), (tg, "NOVEMBRE 1893", "24")], t23), "paper")
        sc.add(Icon("report", (1300, 460), t23 + 0.6, tg, size=260, label="LA RELAZIONE IN AULA"), "pop")
        sc.add(Stamp("IL GOVERNO\nSI DIMETTE", (1300, 460), T("dimette") - 0.2, size=84, rot=-8))
        sc.footer = "Fonti: Wikipedia · IMF WP 17/274"
    elif i == 24:
        tc = T("Con") - 0.3; tl_ = T("la", 2) - 0.3; tp = T("Le") - 0.3
        sc.add(Pill("LO STATO CAMBIA LE REGOLE", (960, 200), a + 0.1, tc, size=48, accent=True))
        sc.add(Img(doc_typed(560, 700, "LEGGE 10 AGOSTO 1893, N. 449", ["Riordinamento degli", "istituti di emissione.", "", "Banca Romana:", "in liquidazione."], footer="testo riassunto, non originale"),
                   (560, 520), tc, anim="drop", rot=-2), "paper")
        sc.add(Bank((960, 250, 1800, 860), tl_, None, level=[(tl_, 1.2)], closed_t=tp + 0.2, label=""))
        sc.add(Pill("LE PORTE SI CHIUDONO", (1380, 185), T("si") - 0.2, size=44, accent=True))
        sc.footer = F_BI + " · documento ricostruito"
    elif i == 25:
        tla = T("La") - 0.3; tn = T("Nasce") - 0.3; ti = T("Il") - 0.3
        sc.add(Pill("UNA NUOVA BANCA", (960, 200), a + 0.1, tla, size=48, accent=True))
        for k, lab in enumerate(("BANCA NAZIONALE\nNEL REGNO", "BANCA NAZ.\nTOSCANA", "BANCA TOSCANA\nDI CREDITO")):
            x = 400 + k * 560
            sc.add(Icon("bankold", (x, 420), tla + 0.3 * k, tn, size=200, move=(tn - 0.9, 0.8, (960, 470), 0)), "pop" if k == 0 else None)
            sc.add(Text(lab, (x, 540), tla + 0.3 * k, tn - 0.9, size=30, fnt=OSW, anchor="ma", align="m"))
        sc.add(Icon("newbank", (960, 470), tn, size=380, label="BANCA D'ITALIA · 1893"), "pop")
        sc.add(Flash(tn))
        sc.add(Icon("bankold", (420, 720), ti, size=160, label="BANCO DI NAPOLI"), "pop")
        sc.add(Icon("bankold", (1500, 720), ti + 0.3, size=160, label="BANCO DI SICILIA"), "pop")
        sc.add(Pill("REGOLE PIÙ SEVERE", (960, 820), T("regole") - 0.2, size=40))
        sc.footer = F_BI
    elif i == 26:
        tn = T("Nel") - 0.3; tc = T("Ci") - 0.3; tl_ = T("Le") - 0.3
        sc.add(Chapter("07", "Il *processo*", a, tn))
        sc.add(Aula((160, 160, 1760, 880), tn, None, judges_t=tn + 0.3, cage_t=tn + 0.6, who=True))
        sc.add(Calendar((1640, 330), 150, [(tn, "ANNO", "1894")], tn, tc), "paper")
        sc.add(Icon("report", (1300, 640), tc, size=170, label="RELAZIONI"), "pop")
        sc.add(Icon("notes_dup", (1580, 640), T("Ci", 1) - 0.2, size=170, label="BIGLIETTI DOPPI"), "pop")
        sc.add(Pill("LE ACCUSE SONO PESANTI", (960, 200), tl_, size=46, accent=True))
        sc.footer = F_PROC + " · schema non in scala"
    elif i == 27:
        ta = T("arriva") - 0.3; tt = T("Tutti") - 0.3
        sc.add(Aula((160, 160, 1760, 880), a, None, judges_t=a, cage_t=a, who=True))
        sc.add(Calendar((1640, 330), 150, [(a + 0.2, "LUGLIO", "1894")], a + 0.2, tt), "paper")
        sc.add(Icon("gavel", (1500, 560), ta, size=200), "hit")
        sc.add(Stamp("ASSOLTI", (960, 460), tt + 0.2, color=(40, 120, 60), size=130, rot=-8))
        sc.add(Pill("TUTTI GLI IMPUTATI · TANLONGO COMPRESO", (960, 200), T("Tanlongo") - 0.2, size=44, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (tt, 960, 540, 1.0), (tt + 0.8, 960, 500, 1.12))
        sc.footer = F_PROC + " · schema non in scala"
    elif i == 28:
        tl_ = T("Le") - 0.3; tc = T("Carte") - 0.3; tp = T("Per") - 0.3
        sc.add(Icon("question", (960, 470), a, tl_, size=300), "pop")
        sc.add(Pill("PROVE INSUFFICIENTI", (560, 220), tl_, tp, size=44, accent=True))
        sc.add(Icon("emptyfolder", (560, 480), T("documenti") - 0.3, tp, size=340, label="DOCUMENTI SPARITI"), "pop")
        sc.add(Figure(walk([(1100, FY), (1960, FY)], tc + 0.4, 220), tc + 0.2, T("nessuno") + 1.5, kind="man", s=0.9, carry=[(tc + 0.2, "folder")]), "pop")
        sc.add(Bubble((1450, 380), 150, T("nessuno") - 0.2, tp, inner="question", text="CHI?"), "pop")
        sc.add(Stamp("CASO CHIUSO", (960, 460), tp + 0.3, size=100, rot=-6))
        sc.footer = "Fonti: Filodiritto · moruzzi.it · IMF WP 17/274"
    elif i == 29:
        tn = T("Nel") - 0.3; td = T("Da") - 0.3; tt = T("Tutto") - 0.3
        sc.add(Icon("newbank", (960, 470), a, tn, size=380, label="BANCA D'ITALIA"), "pop")
        sc.add(Calendar((560, 450), 260, [(tn, "ANNO", "1926")], tn, td), "paper")
        sc.add(Pill("UNICA BANCA AUTORIZZATA A STAMPARE", (1250, 450), tn + 0.4, td, size=44, accent=True))
        six(sc, td, tt, size=150)
        sc.add(Big("DA 6 A 1", (960, 780), td + 0.3, tt, size=110, color=GOLD, fnt=OSW), "hit")
        sc.add(Twins((960, 480), 520, tt, hl_t=T("stesso") - 0.1))
        sc.footer = "Fonti: Wikipedia (Bank of Italy) · Filodiritto · banconote ricostruite"
    elif i == 30:
        ts = T("Sei") - 0.3
        sc.add(Chapter("", "Il *verdetto*", a, ts))
        items = [("bankold", "SEI BANCHE", T("Sei")), ("magnifier", "ISPEZIONE 1889", T("Un'ispezione")), ("notes", "OLTRE IL LIMITE", T("Biglietti")),
                 ("safe", "BUCO IN CASSA", T("buco")), ("serial", "NUMERI DOPPI", T("numeri")), ("drawer", "3 ANNI NASCOSTA", T("Una", 1)),
                 ("chamber", "IL DISCORSO", T("discorso")), ("gavel", "ARRESTO E ASSOLUZIONE", T("governatore"))]
        for k, (ic, lab, tt) in enumerate(items):
            x = 280 + (k % 4) * 453; y = 330 if k < 4 else 650
            sc.add(Icon(ic, (x, y), tt - 0.2, T("alla") - 0.2, size=190, label=lab), "pop")
        sc.add(Icon("newbank", (960, 470), T("alla") - 0.1, size=400, label="LA BANCA D'ITALIA"), "hit")
        sc.footer = "Ricostruzione divulgativa · fonti nella descrizione"
    elif i == 31:
        ts = T("Iscriviti") - 0.3; te = T("E") - 0.3
        sc.add(Twins((960, 470), 480, a, T("Scrivilo") - 0.2, hl_t=a + 0.6))
        sc.add(Pill("QUANTO PUÒ DURARE UN SEGRETO?", (960, 200), a + 0.3, te, size=52, accent=True))
        sc.add(Pill("QUELLA SENTENZA TI CONVINCE?", (960, 200), te, T("Scrivilo") - 0.2, size=48, accent=True))
        sc.add(Bubble((960, 470), 170, T("Scrivilo") - 0.1, ts, text="COMMENTI"), "pop")
        sc.add(Text("Fonti nella descrizione", (960, 760), T("fonti") - 0.2, ts, size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(110), (960, 520), ts + 0.35, anim="pop", shadow=False), "hit")
        sc.add(Text("ogni giorno un nuovo caso", (960, 700), T("ogni") - 0.2, size=54, fnt=PS, color=GOLD, anchor="ma"))
        sc.footer = "Ricostruzione divulgativa · voce generata con sintesi vocale"
    return sc


def thumbnail(path="thumbnail.jpg"):
    W_, H_ = 1920, 1080
    im = make_bg(8).convert("RGBA")
    n1 = banknote(620, serial="N. 048217", hl=True).rotate(-6, expand=True, resample=Image.BICUBIC)
    n2 = banknote(620, serial="N. 048217", hl=True).rotate(5, expand=True, resample=Image.BICUBIC)
    im.alpha_composite(n1, (1180, 140)); im.alpha_composite(n2, (1220, 520))
    d0 = ImageDraw.Draw(im)
    d0.ellipse([1110, 450, 1230, 570], fill=RED + (255,)); d0.text((1170, 505), "=", font=font(OSW, 100, 700), fill=WHITE + (255,), anchor="mm")
    t = rich_img("STESSO\n*NUMERO*\nDI SERIE", SERIF, 150, WHITE, RED, lh=1.0)
    im.alpha_composite(t, (90, 120))
    st = stamp_img("CASO 010", RED, 64, -10); im.alpha_composite(st, (760, 40))
    st2 = stamp_img("ROMA 1893", (200, 160, 60), 54, 6); im.alpha_composite(st2, (110, 640))
    d = ImageDraw.Draw(im)
    d.text((100, 800), "LO SCANDALO DELLA BANCA ROMANA:", font=font(OSW, 54, 600), fill=GOLD + (255,))
    d.text((100, 870), "CIRCA 40 MILIONI IN BANCONOTE \"GEMELLE\"", font=font(OSW, 54, 600), fill=GOLD + (255,))
    wm = wordmark(60, sub=False); im.alpha_composite(wm, (100, 975))
    im.convert("RGB").save(path, quality=92)
