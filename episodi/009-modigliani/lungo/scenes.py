import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from mod import *

W, H = 1920, 1080
FY = 870
CB = (200, 160, 1720, 880)      # scenografia: il Fosso Reale
GB = (260, 160, 1660, 880)      # sala della mostra
F_LEG = "Fonti: Il Fatto Quotidiano · Artribune · The Local · Geopop"
F_MOSTRA = "Fonti: Il Fatto Quotidiano · Geopop · Artribune · modigliani1909.com"
F_FOSSO = "Fonti: Il Fatto Quotidiano · Geopop · Libreriamo · The Local"
F_ESP = "Fonti: Artribune · modigliani1909.com · Il Fatto Quotidiano · The Local"
F_STUD = "Fonti: Geopop · Il Fatto Quotidiano · Artribune · Libreriamo · hoaxes.org"
F_FRO = "Fonti: Artribune · Geopop · modigliani1909.com · Wikipedia (A. Froglia)"
HEADS = [(2, STONE), (5, STONE), (3, GRANITE)]

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
        tu = T("Una") - 0.3; ta = T("All'improvviso") - 0.3; tp = T("Poi") - 0.3; te = T("E") - 0.3
        sc.add(MapEl((160, 160, 1760, 880), [(a, (11.0, 43.0), 160), (tu, (10.31, 43.55), 700)], a, tu + 0.4,
                     pins=[dict(at="Livorno", label="LIVORNO", t=a + 0.3, side="r", color=RED)], title="mappa: Natural Earth · schema non in scala"))
        sc.add(Calendar((330, 420), 220, [(a + 0.8, "ESTATE", "1984")], a + 0.8, tu + 0.4), "paper")
        sc.add(Canal(CB, tu, None, digs=[tu + 0.3, ta - 2.0], finds=[(ta, 2, STONE), (tp + 0.1, 5, STONE), (te + 0.2, 3, GRANITE)], crowd=T("davanti") - 0.2))
        sc.add(Pill("UNA TESTA DI PIETRA", (960, 220), ta + 0.6, tp, size=46, accent=True))
        sc.add(Pill("POI UN'ALTRA. E UN'ALTRA ANCORA", (960, 220), tp + 0.2, size=46, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (ta, 960, 540, 1.0), (ta + 1.0, 820, 540, 1.15), (te, 820, 540, 1.15), (te + 1.0, 960, 540, 1.0))
        sc.footer = F_FOSSO + " · schema non in scala"
    elif i == 1:
        ts = T("sono") - 0.3; tq = T("Qualche") - 0.3; tu = T("una") - 0.3; tc = T("Questo") - 0.3; tv = T("Vedremo") - 0.3
        for k in range(3):
            sc.add(Figure([(0, 560 + k * 400, FY)], a + 0.3 * k, tq, kind="expert", s=0.85), "pop" if k == 0 else None)
        sc.add(Icon("critic", (960, 330), ts, tq, size=260), "stamp")
        sc.add(Pill("\"SONO DI MODIGLIANI\"", (960, 200), ts + 0.2, tq, size=46, accent=True))
        sc.add(Icon("magazine", (560, 460), tq, tc, size=340), "paper")
        sc.add(Bubble((1200, 380), 140, tu, tc, inner="head", text="FATTA DA NOI"), "pop")
        sc.add(Icon("drill", (1500, 640), T("trapano") - 0.3, tc, size=240), "hit")
        sc.add(Img(cover_folder(), (960, 500), tc + 0.1, tv, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 009", (1150, 300), T("fascicolo") + 0.2, tv, size=70, rot=-12))
        sc.add(Icon("book", (360, 470), tv + 0.1, size=200, label="LA LEGGENDA"), "pop")
        sc.add(Icon("critic", (760, 470), T("esperti") - 0.3, size=200, label="GLI ESPERTI"), "pop")
        sc.add(Icon("head_g", (1160, 470), T("chi") - 0.3, size=200, label="LE ALTRE DUE"), "pop")
        sc.add(Icon("question", (1560, 470), T("altre") - 0.2, size=180, label="CHI C'ERA DIETRO?"), "pop")
        sc.footer = "Fonti: Il Fatto Quotidiano · Geopop · Artribune"
    elif i == 2:
        tc = T("Amedeo") - 0.6; to = T("Oggi") - 0.3; tm = T("Ma") - 0.3
        sc.add(Chapter("01", "La *leggenda*", a, tc))
        sc.add(Img(label_card(["Amedeo Modigliani", "Livorno, 1884", "pittore e scultore"], 560, title="SCHEDA"), (560, 500), tc, to, anim="drop", rot=-2), "paper")
        sc.add(MapEl((1000, 200, 1760, 860), [(tc, (10.31, 43.55), 900), (to, (10.31, 43.55), 900)], tc, to,
                     pins=[dict(at="Livorno", label="LIVORNO · 1884", t=tc + 0.4, side="r", color=RED)], title="Natural Earth"))
        sc.add(Icon("easel", (560, 470), to, tm, size=320, label="RITRATTI"), "pop")
        sc.add(Text("colli lunghi · occhi a mandorla", (1300, 470), T("con") - 0.2, tm, size=46, fnt=SERIF, color=GOLD, anchor="mm"))
        sc.add(Icon("chisel", (700, 470), tm, size=300, label="SCULTORE"), "pop")
        sc.add(Icon("head", (1250, 470), tm + 0.5, size=340), "pop")
        sc.add(Text("sagoma stilizzata, non un'opera", (1250, 760), tm + 0.5, size=26, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: The Local · modigliani1909.com · Il Fatto Quotidiano"
    elif i == 3:
        ts = T("Secondo") - 0.3; tv = T("Volti") - 0.3; to = T("Oggi") - 0.3
        sc.add(Pill("LE SUE TESTE DI PIETRA SONO POCHE", (960, 220), a + 0.1, ts, size=46, accent=True))
        sc.add(Icon("head", (960, 520), a + 0.3, ts, size=320), "pop")
        for k in range(26):
            x = 330 + (k % 13) * 105; y = 400 if k < 13 else 600
            sc.add(Icon("head", (x, y), ts + 0.3 + k * 0.06, tv, size=110), "pop" if k == 0 else None)
        sc.add(Big("26", (960, 790), ts + 0.6, tv, size=110, color=GOLD, fnt=OSW, count=(1, 26, lambda z: f"circa {z:.0f}", 1.2)), "hit")
        sc.add(Img(stone_head(300, 412, 2), (960, 520), tv, to, anim="drop", shadow=True))
        sc.add(Pill("VOLTO ALLUNGATO", (1400, 380), tv + 0.2, to, size=40))
        sc.add(Pill("NASO SOTTILE", (520, 520), T("nasi") - 0.2, to, size=40))
        sc.add(Pill("FORME SEMPLICI", (1400, 660), T("forme") - 0.2, to, size=40))
        sc.add(Icon("money", (660, 470), to, size=280, label="CIFRE ENORMI"), "pop")
        sc.add(Icon("toplist", (1260, 470), T("pezzo") - 0.3, size=300, label="SCOPERTA MONDIALE"), "pop")
        sc.footer = "Fonti: Geopop · Il Fatto Quotidiano · teste stilizzate, non opere"
    elif i == 4:
        tn = T("Nel") - 0.3; tp = T("prima") - 0.3; ts = T("Si") - 0.3; te = T("E") - 0.3
        sc.add(Pill("LA LEGGENDA", (960, 220), a + 0.1, tn, size=50, accent=True))
        sc.add(Icon("book", (960, 480), a + 0.2, tn, size=300), "paper")
        sc.add(MapEl((160, 160, 1760, 880), [(tn, (6.4, 46.3), 95), (ts, (6.4, 46.3), 97)], tn, ts,
                     pins=[dict(at="Livorno", label="LIVORNO · 1909", t=tn + 0.3, side="r", color=RED), dict(at="Parigi", label="PARIGI", t=tp, side="r", color=GOLD)],
                     routes=[dict(pts=["Livorno", "Parigi"], t=tp + 0.2, d=2.0, icon="train", color=GOLD)], title="mappa: Natural Earth · schema non in scala"))
        sc.add(Crowd((300, 640, 1000, 880), 6, ts, te, s=0.45, kinds=("man", "suit", "expert")))
        for k in range(3): sc.add(Bubble((420 + k * 220, 400), 70, ts + 0.4 + 0.2 * k, te, text="AH AH"), "pop" if k == 0 else None)
        sc.add(Icon("head", (1400, 470), ts + 0.3, te, size=260, label="LE SUE SCULTURE"), "pop")
        sc.add(Canal(CB, te, None, drop=[(T("canale") - 0.3, 2), (T("canale") + 0.5, 5)], ruspa=False))
        sc.add(Pill("NEL FOSSO REALE?", (960, 220), T("Fosso") - 0.2, size=46, accent=True))
        sc.footer = F_LEG + " · racconto tramandato, non verificato"
    elif i == 5:
        tu = T("Una") - 0.3; tn = T("Nessuno") - 0.3; tf = T("Fino") - 0.3
        sc.add(Calendar((560, 450), 260, [(a, "LEGGENDA", "1909"), (a + 0.8, "ANNI", "1930"), (a + 1.4, "ANNI", "1950"), (a + 2.0, "ANNI", "1970")], a, tu), "paper")
        sc.add(Bubble((1260, 420), 150, a + 0.3, tu, text="SI RACCONTA..."), "pop")
        sc.add(Stamp("NESSUNA\nPROVA", (960, 450), T("senza") - 0.1, tn, size=100, rot=-8))
        sc.add(Canal(CB, tn, None, ruspa=False, dim=0.1))
        sc.add(Icon("question", (1100, 760), tn + 0.4, tf, size=180), "pop")
        sc.add(Calendar((960, 460), 300, [(tf, "ESTATE", "1984")], tf), "paper")
        sc.footer = F_LEG
    elif i == 6:
        tl_ = T("Livorno") - 0.3; to = T("e") - 0.3
        sc.add(Chapter("02", "La *mostra*", a, tl_))
        sc.add(Icon("centenary", (620, 470), tl_, size=380, label="CENTENARIO DELLA NASCITA"), "pop")
        sc.add(Icon("museum", (1320, 470), T("mostra") - 0.3, size=320, label="VILLA MARIA · LIVORNO"), "pop")
        sc.add(Arrow((840, 470), (1130, 470), T("mostra"), color=GOLD))
        sc.add(Pill("MUSEO D'ARTE MODERNA DELLA CITTÀ", (960, 220), T("sede") - 0.2, size=42, accent=True))
        sc.footer = F_MOSTRA
    elif i == 7:
        ta = T("Al") - 0.3; td = T("Due") - 0.3
        sc.board({"v": dict(xy=(640, 500), name="VERA DURBÈ", role="direttrice del museo", t=a + 0.2, rot=-3),
                  "d": dict(xy=(1280, 500), name="DARIO DURBÈ", role="Galleria naz. d'arte moderna", t=ta + 0.2, rot=2)},
                 [("v", "d", ta + 0.8)], a, None)
        sc.add(Pill("CURATRICE DELLA MOSTRA", (640, 200), a + 0.6, ta, size=40, accent=True))
        sc.add(Pill("FRATELLO · ROMA", (1280, 200), T("fratello") - 0.1, td, size=40, accent=True))
        sc.add(Icon("museum", (960, 760), T("Galleria") - 0.3, td, size=150), "pop")
        sc.add(Stamp("NOMI\nIMPORTANTI", (960, 300), td + 0.1, size=60, rot=-8))
        sc.add(Text("sagome · nessuna foto reale", (960, 860), a + 0.5, size=26, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = F_MOSTRA
    elif i == 8:
        td = T("Delle") - 0.3; tp = T("Per") - 0.3; te = T("E") - 0.3; ts = T("Se") - 0.3
        sc.add(Pill("C'È UN PROBLEMA", (960, 200), a + 0.1, td, size=50, accent=True))
        sc.add(Gallery((160, 250, 1360, 880), td, te, heads=[(T("quattro") - 0.4 + 0.25 * k, 2 + k, STONE) for k in range(4)]))
        sc.add(Big("4", (1640, 450), T("quattro") - 0.2, te, size=150, color=RED, fnt=OSW, sub="sculture in mostra"), "hit")
        sc.add(Stamp("POCHE", (520, 330), tp + 0.2, te, size=70, rot=-10))
        sc.add(Figure([(0, 600, FY)], te, kind="suit", s=0.85, label="LA CURATRICE"), "pop")
        sc.add(Bubble((900, 380), 140, T("leggenda") - 0.3, inner="book"), "pop")
        sc.add(Canal((1060, 300, 1760, 700), ts, None, ruspa=False, label=""))
        sc.add(Icon("question", (1410, 760), T("perché") - 0.2, size=160), "pop")
        sc.footer = F_MOSTRA
    elif i == 9:
        ts = T("Si") - 0.3; tu = T("Un'idea") - 0.3
        sc.add(Icon("house", (560, 450), a, ts, size=300, label="IL COMUNE"), "pop")
        sc.add(Stamp("VIA LIBERA", (1200, 450), a + 0.6, ts, size=90, rot=-8))
        sc.add(Icon("excavator", (560, 470), ts, tu, size=340), "pop")
        sc.add(Icon("mud", (1260, 470), T("cioè") - 0.2, tu, size=300, label="SCAVARE IL FONDO"), "pop")
        sc.add(Arrow((760, 470), (1080, 470), T("cioè"), tu, color=GOLD))
        sc.add(Icon("clapper", (560, 470), tu, size=260, label="COME IN UN FILM"), "pop")
        sc.add(Figure(walk([(1950, FY), (1250, FY)], T("giornalisti") - 0.3, 360), T("giornalisti") - 0.3, kind="man", s=0.8, flip=-1), "pop")
        sc.add(Icon("tvcam", (1560, 420), T("telecamere") - 0.2, size=220), "pop")
        sc.footer = F_FOSSO
    elif i == 10:
        ts = T("Sul") - 0.3; ti = T("Il") - 0.3; tl_ = T("Lungo") - 0.3
        sc.add(Chapter("03", "Il *fosso*", a, ts))
        sc.add(Canal(CB, ts, None, digs=[ti, ti + 2.8, ti + 5.6], crowd=tl_))
        sc.add(Calendar((330, 300), 170, [(ts, "LUGLIO", "1984")], ts, ti + 1), "paper")
        sc.add(Pill("ARRIVA LA RUSPA", (960, 220), ts + 0.3, ti, size=46, accent=True))
        sc.add(Pill("SU E GIÙ: SOLO FANGO", (960, 220), T("risale") - 0.2, tl_, size=46, accent=True))
        sc.add(Pill("TURISTI · CURIOSI · FOTOGRAFI", (960, 220), T("Turisti") - 0.2, size=46))
        scene_cam(sc, (0, 960, 540, 1.0), (ti, 960, 540, 1.0), (ti + 1.0, 760, 540, 1.15), (tl_, 760, 540, 1.15), (tl_ + 1.0, 1100, 540, 1.12))
        sc.footer = F_FOSSO + " · schema non in scala"
    elif i == 11:
        ts = T("Il", 1) - 0.3; td = T("Dal") - 0.3; tp = T("Passa") - 0.3; tq = T("qualcuno") - 0.3
        sc.add(Calendar((400, 380), 220, [(a, "GIORNO", "1"), (ts, "GIORNO", "2"), (td + 0.5, "GIORNO", "3"), (tp, "GIORNO", "5"), (tp + 0.8, "GIORNO", "7")], a), "paper")
        sc.add(Icon("mud", (960, 450), a + 0.2, tq, size=300), "pop")
        sc.add(Stamp("NIENTE", (1400, 380), a + 0.6, ts, size=70, rot=-8))
        sc.add(Stamp("NIENTE", (1400, 520), ts + 0.3, td, size=70, rot=6))
        sc.add(Pill("SOLO FANGO", (960, 760), td + 0.2, tp, size=46, accent=True))
        sc.add(ClockFace((1440, 460), 130, tp, tq, start=8.0, speed=3.0, label="UNA SETTIMANA"))
        sc.add(Figure([(0, 1200, FY)], tq, kind="man", s=0.85, arms=[(tq + 0.5, "up")]), "pop")
        sc.add(Bubble((1360, 360), 150, tq + 0.4, text="LEGGENDA?"), "pop")
        sc.footer = F_FOSSO
    elif i == 12:
        tl_ = T("La") - 0.3; th = T("Ha") - 0.3; tlc = T("Lungo") - 0.3
        sc.add(Calendar((960, 460), 300, [(a, "LUGLIO 1984", "24")], a, tl_ + 0.2), "paper")
        sc.add(Canal(CB, tl_, None, digs=[tl_ - 1.0], finds=[(tl_ + 0.6, 2, STONE)], crowd=tl_))
        sc.add(Img(stone_head(300, 412, 2, STONE, mud=0.6), (1500, 470), th, tlc, anim="drop"))
        sc.add(Pill("VOLTO LUNGO · NASO SOTTILE", (1500, 760), T("un", 1) - 0.2, tlc, size=36, accent=True))
        sc.add(Flash(tlc))
        sc.add(Pill("ENTUSIASMO SUL CANALE", (960, 220), tlc + 0.2, size=48, accent=True))
        sc.footer = F_FOSSO + " · teste stilizzate · schema non in scala"
    elif i == 13:
        tp = T("Poco") - 0.3; te = T("E", 1) - 0.3; ts = T("Sulla") - 0.3; ti = T("I") - 0.3
        sc.add(Canal(CB, a, ti + 0.3, digs=[a + 0.2], finds=[(a - 5, 2, STONE), (tp + 0.4, 5, STONE), (te + 0.4, 3, GRANITE)], crowd=a))
        sc.add(Pill("UNA SECONDA TESTA", (960, 220), tp + 0.4, te, size=48, accent=True))
        sc.add(Pill("E UNA TERZA", (960, 220), te + 0.4, ts, size=48, accent=True))
        sc.add(Pill("DATE: LE VERSIONI NON COINCIDONO", (960, 220), ts, ti, size=40))
        sc.add(Icon("tv", (560, 470), ti + 0.2, size=300, label="TELEGIORNALI"), "pop")
        sc.add(Img(newspaper(520, 560, "CRONACA", "luglio 1984", "Ritrovati\ni *Modigliani*", "nel Fosso Reale"), (1300, 500), T("ritrovate") - 0.3, anim="drop", rot=3), "paper")
        sc.footer = F_FOSSO + " · giornale ricostruito (testata di fantasia)"
    elif i == 14:
        ti = T("I") - 0.3; tl_ = T("La") - 0.3
        sc.add(Chapter("04", "Gli *esperti*", a, a + 2.2))
        sc.add(Gallery(GB, a + 2.2, None, heads=[(a + 2.4 + 0.4 * k, s_, tn) for k, (s_, tn) in enumerate(HEADS)], labels=["N. 1", "N. 2", "N. 3"]))
        sc.add(Crowd((380, 700, 1540, 870), 12, ti, None, s=0.32, walk=40))
        sc.add(Pill("ESPOSTE A VILLA MARIA", (960, 200), a + 2.6, ti, size=44, accent=True))
        sc.add(Pill("DA 4 SCULTURE A UN \"TESORO\"", (960, 200), tl_ + 0.3, size=44, accent=True))
        sc.footer = F_ESP + " · teste stilizzate"
    elif i == 15:
        tg = T("Giulio") - 0.3; tl_ = T("le") - 0.3; ts = T("Secondo") - 0.3
        sc.board({"a": dict(xy=(960, 470), name="G. C. ARGAN", role="critico d'arte", t=tg, rot=-2, stamp=("AUTENTICHE", tl_ + 0.2, (40, 120, 60))),
                  "b": dict(xy=(480, 470), name="C. BRANDI", role="storico dell'arte", t=T("Cesare") - 0.2, rot=3),
                  "c": dict(xy=(1440, 470), name="C. L. RAGGHIANTI", role="storico dell'arte", t=T("Ragghianti") - 0.4, rot=-3)},
                 [("b", "a", T("Ragghianti")), ("a", "c", T("Ragghianti") + 0.3)], a, None, cw=290)
        sc.add(Pill("E GLI ESPERTI?", (960, 200), a + 0.1, tg, size=50, accent=True))
        sc.add(Pill("NON LE RICONOSCONO COME FALSE", (960, 200), T("non") - 0.2, size=44, accent=True))
        sc.add(Text("sagome · nessuna foto reale", (960, 860), tg + 0.5, size=26, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = F_ESP
    elif i == 16:
        tl_ = T("Lo") - 0.3; ta = T("Anche") - 0.3; tm = T("Ma") - 0.3
        sc.add(Icon("question", (960, 450), a, tl_, size=260, label="NON TUTTI CONVINTI"), "pop")
        sc.add(Figure([(0, 560, FY)], tl_, tm, kind="expert", s=0.85, carry=[(tl_ + 0.4, "magnifier")], label="FEDERICO ZERI"), "pop")
        sc.add(Icon("head", (1200, 460), tl_ + 0.4, tm, size=300), "pop")
        sc.add(Stamp("SCARSA\nQUALITÀ", (1200, 380), T("scarsa") - 0.1, tm, size=64, rot=-8))
        sc.add(Figure([(0, 1560, FY)], ta, tm, kind="painter", s=0.8, label="ALCUNI SCULTORI", flip=-1), "pop")
        sc.add(Gallery(GB, tm, None, heads=[(tm, s_, tn) for s_, tn in HEADS], labels=["MODIGLIANI?", "MODIGLIANI?", "MODIGLIANI?"]))
        sc.add(Pill("PER GRAN PARTE DEL MONDO DELL'ARTE: AUTENTICHE", (960, 200), tm + 0.4, size=40, accent=True))
        sc.footer = "Fonti: The Local · modigliani1909.com · Il Fatto Quotidiano"
    elif i == 17:
        tp = T("Poi") - 0.3; tpa = T("Parlano") - 0.3; ts = T("Si") - 0.3
        sc.add(Chapter("05", "Il *trapano*", a, tp))
        sc.add(Icon("magazine", (960, 470), tp, tpa, size=420, label="SETTIMANALE PANORAMA"), "paper")
        sc.add(Icon("quake", (1500, 470), T("tremare") - 0.2, tpa, size=200, anim="shake"), "hit")
        for k, (nm, w_) in enumerate((("PIETRO LURIDIANA", "Pietro"), ("PIERFRANCESCO FERRUCCI", "Pierfrancesco"), ("MICHELE GHELARDUCCI", "Michele"))):
            x = 480 + k * 480
            sc.add(Figure([(0, x, FY)], tpa + 0.2 * k, kind="man" if k != 1 else "worker", s=0.85), "pop" if k == 0 else None)
            sc.add(Pill(nm, (x, 360), T(w_) - 0.2, size=34, accent=(k == 0)))
        sc.add(Pill("TRE STUDENTI DI LIVORNO", (960, 200), tpa + 0.4, size=46, accent=True))
        sc.footer = F_STUD
    elif i == 18:
        tu = T("Una") - 0.3; tl_ = T("l'hanno") - 0.3; tc = T("Con") - 0.3
        sc.add(Pill("LA LORO VERSIONE", (960, 200), a + 0.1, tu, size=48, accent=True))
        sc.add(Gallery(GB, tu, tc, heads=[(tu, s_, tn) for s_, tn in HEADS], labels=["N. 1", "N. 2", "N. 3"]))
        sc.add(Stamp("FATTA DA NOI", (960, 400), tl_ + 0.1, tc, size=60, rot=-8))
        sc.add(Pill("ATTREZZI DA BRICOLAGE", (960, 200), tc, size=46, accent=True))
        sc.add(Icon("drill", (960, 480), tc + 0.2, T("martello") - 0.3, size=320), "pop")
        sc.add(Icon("hammer", (480, 480), T("martello") - 0.2, size=240, label="MARTELLO"), "pop")
        sc.add(Icon("chisel", (960, 480), T("cacciavite") - 0.2, size=240, label="CACCIAVITE"), "pop")
        sc.add(Icon("drill", (1440, 480), T("trapano") - 0.2, size=260, label="TRAPANO ELETTRICO"), "hit")
        sc.footer = F_STUD + " · attrezzi generici, nessun marchio"
    elif i == 19:
        tv = T("Volevano") - 0.3; th = T("Hanno") - 0.3; te = T("E") - 0.3
        for k in range(3):
            sc.add(Figure([(0, 560 + k * 400, FY)], a + 0.2 * k, th, kind="man", s=0.85), "pop" if k == 0 else None)
        sc.add(Bubble((960, 380), 140, a + 0.4, tv, text="UNO SCHERZO"), "pop")
        sc.add(Bubble((960, 380), 140, tv, th, inner="question", text="COSA SUCCEDE?"), "pop")
        sc.add(Canal(CB, th, te + 0.4, drop=[(th + 0.4, 5)], digs=[th + 1.6], crowd=th))
        sc.add(Gallery(GB, te, None, heads=[(te, s_, tn) for s_, tn in HEADS], labels=["", "CAPOLAVORO", ""]))
        sc.add(Pill("E GLI ESPERTI LA CHIAMANO \"CAPOLAVORO\"", (960, 200), T("gli") - 0.2, size=42, accent=True))
        sc.footer = F_STUD + " · schema non in scala"
    elif i == 20:
        tc = T("Come") - 0.3; tm = T("Ma") - 0.3
        sc.add(Crowd((300, 640, 1620, 880), 10, a, tm, s=0.4, kinds=("expert", "suit", "man")))
        for k in range(3): sc.add(Bubble((560 + k * 400, 400), 90, a + 0.3 + 0.25 * k, tm, text="IMPOSSIBILE"), "pop" if k == 0 else None)
        sc.add(Pill("TRE STUDENTI CONTRO I GRANDI CRITICI?", (960, 200), tc, tm, size=44, accent=True))
        sc.add(Icon("photos", (960, 470), tm, size=440, label="LE IMMAGINI DEL LAVORO"), "paper")
        sc.add(Stamp("LE PROVE", (1450, 330), T("prove") - 0.1, size=70, rot=-8))
        sc.footer = F_STUD
    elif i == 21:
        ti = T("I") - 0.3; td = T("Davanti") - 0.3; ts = T("Secondo") - 0.3
        sc.add(Pill("LA PROVA DAVANTI A TUTTI", (960, 200), a + 0.1, ti, size=48, accent=True))
        sc.add(Icon("tvlive", (960, 470), ti, ts, size=440), "pop")
        sc.add(Icon("tvcam", (1500, 520), td, ts, size=240), "pop")
        sc.add(Icon("drill", (440, 560), T("scolpiscono") - 0.2, ts, size=220), "hit")
        sc.add(Big("10 milioni", (960, 420), ts, size=150, color=GOLD, fnt=OSW, count=(0, 10, lambda z: f"{z:.0f} milioni", 1.4), sub="di telespettatori (stima)"), "hit")
        sc.add(Crowd((300, 680, 1620, 880), 16, ts + 0.3, None, s=0.3))
        sc.footer = F_STUD
    elif i == 22:
        te = T("E") - 0.3; tc = T("Chi") - 0.3
        sc.add(Chapter("06", "Il terzo *uomo*", a, te))
        sc.add(Gallery(GB, te, None, heads=[(te, s_, tn) for s_, tn in HEADS], fakes=[(te + 0.2, 1)], labels=["N. 1  ?", "STUDENTI", "N. 3  ?"]))
        sc.add(Icon("question", (520, 300), T("prima") - 0.3, size=150), "pop")
        sc.add(Icon("question", (1400, 300), T("terza") - 0.3, size=150), "pop")
        sc.add(Pill("24 LUGLIO", (520, 200), T("24") - 0.2, size=40, accent=True))
        sc.footer = F_FRO + " · teste stilizzate"
    elif i == 23:
        te = T("È") - 0.3; ta = T("Ammette") - 0.3
        sc.add(Pill("LA RISPOSTA ARRIVA POCO DOPO", (960, 200), a + 0.1, te, size=46, accent=True))
        sc.add(Img(person_card("ANGELO FROGLIA", "Livorno · 29 anni", 300), (560, 500), te, anim="drop", rot=-3), "paper")
        sc.add(Icon("ship", (1100, 380), T("lavoratore") - 0.3, size=220, label="PORTO"), "pop")
        sc.add(Icon("easel", (1500, 380), T("artista") - 0.3, size=220, label="ARTISTA"), "pop")
        sc.add(Icon("head", (1100, 680), ta + 0.2, size=200), "pop")
        sc.add(Icon("head_g", (1400, 680), ta + 0.5, size=200), "pop")
        sc.add(Stamp("LE ALTRE DUE", (1250, 820), T("altre") - 0.1, size=50, rot=-6))
        sc.footer = F_FRO + " · sagoma, nessuna foto reale"
    elif i == 24:
        tf = T("Froglia") - 0.3; tv = T("Voleva") - 0.3; tu = T("Una") - 0.3
        sc.add(Stamp("NON UNO\nSCHERZO", (960, 450), a + 0.2, tf, size=90, rot=-6))
        sc.add(Icon("easel", (960, 470), tf, T("televisione") - 0.3, size=360, label="OPERAZIONE ARTISTICA"), "pop")
        sc.add(Icon("tv", (480, 400), T("televisione") - 0.3, tu, size=220, label="TV"), "pop")
        sc.add(Icon("newspaper", (960, 400), T("giornali") - 0.3, tu, size=220, label="GIORNALI"), "pop")
        sc.add(Icon("critic", (1440, 400), T("esperti") - 0.3, tu, size=220, label="ESPERTI"), "pop")
        sc.add(Crowd((380, 690, 1540, 880), 14, T("possano") - 0.2, tu, s=0.3))
        sc.add(Icon("magnifier", (960, 470), tu, size=300, label="ESPERIMENTO SULLA PERSUASIONE"), "pop")
        sc.footer = F_FRO
    elif i == 25:
        tl_ = T("Le") - 0.3; ts = T("Sono") - 0.3; te = T("E") - 0.3
        sc.add(Chapter("07", "Dopo la *beffa*", a, tl_))
        sc.add(Gallery(GB, tl_, te, heads=[(tl_, s_, tn) for s_, tn in HEADS], fakes=[(tl_ + 0.4 + 0.3 * k, k) for k in range(3)], labels=["FROGLIA", "STUDENTI", "FROGLIA"]))
        sc.add(Pill("TRE STUDENTI E UN PORTUALE", (960, 200), ts, te, size=46, accent=True))
        sc.add(Img(newspaper(460, 520, "NOTIZIE", "1984", "La *beffa*\ndi Livorno", "le teste erano false"), (700, 520), te, anim="drop", rot=-3), "paper")
        sc.add(Img(newspaper(460, 520, "CRONACA", "1984", "Falsi\ni *Modigliani*", "il caso fa il giro del mondo"), (1220, 520), te + 0.8, anim="drop", rot=3), "paper")
        sc.footer = F_FRO + " · giornali ricostruiti (testate di fantasia)"
    elif i == 26:
        tl_ = T("Le") - 0.3; td = T("Da") - 0.3
        sc.add(Figure([(0, 960, FY)], a, td, kind="expert", s=0.9, arms=[(a + 0.6, "up")]), "pop")
        sc.add(Stamp("COLPO\nDURISSIMO", (960, 330), T("è") - 0.1, tl_, size=70, rot=-8))
        for k in range(4): sc.add(Bubble((420 + k * 360, 380), 90, tl_ + 0.25 * k, td, text="POLEMICA"), "pop" if k == 0 else None)
        sc.add(Icon("toplist", (960, 470), td, size=380, label="TRA LE PIÙ GRANDI BEFFE DELL'ARTE"), "pop")
        sc.footer = "Fonti: The Local · Geopop · Il Fatto Quotidiano"
    elif i == 27:
        tp = T("Per") - 0.3; tm = T("Ma") - 0.3
        sc.add(Calendar((560, 450), 260, [(a, "LIVORNO", "1997")], a, tp + 0.4), "paper")
        sc.add(Img(person_card("ANGELO FROGLIA", "1955 - 1997", 300), (1300, 500), a + 0.3, tp + 0.4, anim="drop", rot=3), "paper")
        sc.add(Icon("head", (700, 470), tp + 0.4, tm, size=280), "pop")
        sc.add(Pill("\"L'UOMO DELLE TESTE FALSE\"", (1250, 470), tp + 0.6, tm, size=44, accent=True))
        sc.add(Stamp("BURLA?", (700, 470), tm, T("per", 1) - 0.2, size=90, rot=-8))
        sc.add(Icon("easel", (960, 470), T("per", 1) - 0.2, size=360, label="UNA PERFORMANCE ARTISTICA"), "pop")
        sc.footer = "Fonti: Artribune · Wikipedia (A. Froglia) · sagoma, nessuna foto reale"
    elif i == 28:
        tl_ = T("Livorno") - 0.3; ta = T("Annuncia") - 0.3; ti = T("I") - 0.3
        sc.add(Calendar((960, 460), 300, [(a, "TRENT'ANNI DOPO", "2014")], a, tl_ + 0.4), "paper")
        sc.add(Icon("fortress", (560, 470), ta, size=360, label="FORTEZZA VECCHIA"), "pop")
        sc.add(Gallery((960, 220, 1700, 760), T("esporre") - 0.3, None, heads=[(T("esporre") + 0.2 * k, s_, tn) for k, (s_, tn) in enumerate(HEADS)], label="", labels=["FALSO", "FALSO", "FALSO"]))
        sc.add(Icon("newspaper", (1330, 820), T("giornali") - 0.3, size=130), "pop")
        sc.add(Pill("I FALSI DIVENTANO STORIA DELLA CITTÀ", (960, 200), ti, size=44, accent=True))
        sc.footer = "Fonti: Artribune (2014) · The Local (2014)"
    elif i == 29:
        tu = T("Una") - 0.3
        sc.add(Chapter("", "Il *verdetto*", a, tu))
        items = [("book", "LEGGENDA", T("Una")), ("centenary", "CENTENARIO", T("Un")), ("excavator", "LA RUSPA", T("ruspa") - 0.3),
                 ("head", "TRE TESTE", T("Tre")), ("critic", "\"AUTENTICHE\"", T("dichiarate")), ("drill", "TRE STUDENTI", T("tre", 1)),
                 ("easel", "UN ARTISTA", T("artista"))]
        for k, (ic, lab, tt) in enumerate(items):
            x = 220 + (k % 4) * 493; y = 330 if k < 4 else 650
            if k >= 4: x = 466 + (k - 4) * 493
            sc.add(Icon(ic, (x, y), tt - 0.2, T("Nessun") - 0.2, size=200, label=lab), "pop")
        sc.add(Stamp("NESSUN\nMODIGLIANI", (960, 500), T("Nessun") - 0.1, size=110, rot=-6))
        sc.footer = "Ricostruzione divulgativa · fonti nella descrizione"
    elif i == 30:
        ts = T("Iscriviti") - 0.3; te = T("E") - 0.3
        sc.add(Gallery(GB, a, T("Scrivilo") - 0.2, heads=[(a, s_, tn) for s_, tn in HEADS], dim=0.35, label=""))
        sc.add(Pill("CONTA IL NOME O L'OPERA?", (960, 200), a + 0.3, te, size=52, accent=True))
        sc.add(Pill("AVRESTI CREDUTO A QUELLE TESTE?", (960, 200), te, T("Scrivilo") - 0.2, size=48, accent=True))
        sc.add(Bubble((960, 470), 170, T("Scrivilo") - 0.1, ts, text="COMMENTI"), "pop")
        sc.add(Text("Fonti nella descrizione", (960, 760), T("fonti") - 0.2, ts, size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(110), (960, 520), ts + 0.35, anim="pop", shadow=False), "hit")
        sc.add(Text("ogni giorno un nuovo caso", (960, 700), T("ogni") - 0.2, size=54, fnt=PS, color=GOLD, anchor="ma"))
        sc.footer = "Ricostruzione divulgativa · voce generata con sintesi vocale"
    return sc


def thumbnail(path="thumbnail.jpg"):
    W_, H_ = 1920, 1080
    im = make_bg(8).convert("RGBA")
    lay = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    # tre teste di pietra su piedistalli a destra
    for k, (s_, tn) in enumerate(HEADS):
        x = 1260 + k * 215; hd = stone_head(190, 262, s_, tn, mud=0.3)
        ImageDraw.Draw(lay).rectangle([x - 5, 680, x + 195, 1000], fill=(226, 222, 212, 255))
        lay.alpha_composite(hd, (x, 420))
    im.alpha_composite(lay)
    ic = fx.icon("drill", 300); im.alpha_composite(ic, (1500, 40))
    st0 = stamp_img("FALSE", RED, 110, -12); im.alpha_composite(st0, (1330, 760))
    t = rich_img("3 TESTE\n*FALSE*\nNEL FOSSO", SERIF, 140, WHITE, RED, lh=1.0)
    im.alpha_composite(t, (90, 140))
    st = stamp_img("CASO 009", RED, 64, -10); im.alpha_composite(st, (760, 40))
    st2 = stamp_img("LIVORNO 1984", (200, 160, 60), 54, 6); im.alpha_composite(st2, (110, 640))
    d = ImageDraw.Draw(im)
    d.text((100, 800), "GLI ESPERTI DISSERO: \"SONO DI MODIGLIANI\"", font=font(OSW, 54, 600), fill=GOLD + (255,))
    d.text((100, 870), "ERANO DI TRE STUDENTI E UN PORTUALE", font=font(OSW, 54, 600), fill=GOLD + (255,))
    wm = wordmark(60, sub=False); im.alpha_composite(wm, (100, 975))
    im.convert("RGB").save(path, quality=92)
