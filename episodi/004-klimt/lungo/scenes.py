import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from klm import *

W, H = 1920, 1080
FY = 870
GB = (180, 230, 1740, 830)   # scenografia: sezione della galleria
F1 = "Fonti: Finestre sull'Arte · Live Science · Il Post · Reuters (Dawn)"

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

def canvas_back(w, h):
    im = paper(w, h, (214, 196, 160), 4, 0.4); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=(120, 90, 50, 255), width=18)
    d.line([(18, h / 2), (w - 18, h / 2)], fill=(120, 90, 50, 255), width=12)
    for x, y in ((w * .3, h * .25), (w * .7, h * .72)):
        d.ellipse([x - 34, y - 34, x + 34, y + 34], fill=(170, 30, 30, 255))
        d.ellipse([x - 20, y - 20, x + 20, y + 20], outline=(120, 16, 16, 255), width=4)
    d.rectangle([w * .48, h * .18, w * .86, h * .34], fill=(240, 234, 220, 255), outline=INK + (255,), width=2)
    d.text((w * .67, h * .26), "ETICHETTA", font=font(COURR, 22), fill=INK + (255,), anchor="mm")
    d.rectangle([w * .14, h * .62, w * .46, h * .80], outline=(60, 60, 120, 255), width=4)
    d.text((w * .30, h * .71), "TIMBRO", font=font(COUR, 24), fill=(60, 60, 120, 255), anchor="mm")
    recon_label(d, w, h)
    return im

def cover(t0):
    c = paper(520, 640, (196, 160, 104), 9, 0.7); d = ImageDraw.Draw(c)
    d.rectangle([50, 110, 470, 330], fill=(232, 222, 200, 255), outline=INK + (255,), width=3)
    d.text((260, 145), "FASCICOLO N. 004", font=font(COUR, 32), fill=INK + (255,), anchor="ma")
    d.text((260, 200), "IL KLIMT DI", font=font(TYPE, 40), fill=INK + (255,), anchor="ma")
    d.text((260, 252), "PIACENZA", font=font(TYPE, 52), fill=RED + (255,), anchor="ma")
    d.text((260, 380), "Piacenza · 1997-2019", font=font(COURR, 26), fill=INK + (255,), anchor="ma")
    return c

def build(i, dur, a, words):
    T = Clock(words, a); sc = Scene(dur)
    if i == 0:
        tc = T("Nel") - 0.3
        sc.add(Calendar((960, 470), 300, [(a, "DICEMBRE 2019", "10")], a, tc), "paper")
        sc.add(Text("PIACENZA · MARTEDÌ", (960, 700), a + 0.2, tc, size=40, fnt=TYPE, color=GOLD, anchor="ma"))
        sc.add(Niche((260, 170, 1660, 880), tc, None, clear=T("togliendo") - 0.2, door=T("Sotto") + 0.3, open_=T("aprono") - 0.1,
                     sack=T("sacco") - 0.2, canvas=T("quadro") - 0.2))
        sc.add(Figure(walk([(-100, FY), (330, FY)], tc, 360), tc, T("Sotto") + 0.3, kind="worker", s=0.9, arms=[(T("l'edera"), "up")], label="GIARDINIERE"))
        sc.add(Pill("UNO SPORTELLO DI METALLO", (960, 210), T("sportello") - 0.1, T("Lo") - 0.1, size=40))
        sc.add(Pill("UN SACCO NERO", (960, 210), T("sacco"), T("E", 1) - 0.1, size=40))
        sc.add(Pill("DENTRO, UN QUADRO", (960, 210), T("quadro") - 0.1, size=44, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (tc, 960, 540, 1.0), (T("sportello"), 960, 540, 1.12), (T("sacco"), 960, 540, 1.22), (dur, 1040, 520, 1.25))
        sc.footer = F1
    elif i == 1:
        t2 = T("Questo") - 0.3
        sc.add(Img(lady_pic(300, 375), (420, 500), a, t2, anim="drop", rot=-2), "paper")
        sc.add(Text("sagoma stilizzata · non l'opera", (420, 730), a + 0.2, t2, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Pill("RITRATTO DI SIGNORA · GUSTAV KLIMT", (1240, 280), T("Ritratto") - 0.1, t2, size=40))
        sc.add(Big("22 ANNI", (1240, 420), T("ventidue") - 0.2, t2, size=150, color=GOLD, fnt=OSW, sub="sparito dalla stessa galleria", subsize=40), "hit")
        sc.add(Stamp("TRA I PIÙ\nRICERCATI", (1240, 720), T("ricercate") - 0.3, t2, size=70, rot=-8))
        t3 = T("Vedremo") - 0.3
        sc.add(Img(cover(t2), (960, 520), t2 + 0.1, t3, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 004", (1140, 300), T("fascicolo") + 0.2, t3, size=70, rot=-12))
        sc.add(KIcon("fishing", (420, 470), t3 + 0.1, size=230, label="COME È SPARITO"), "pop")
        sc.add(Icon("gavel", (960, 470), T("perché") - 0.1, size=230, label="NESSUN CONDANNATO"), "pop")
        sc.add(KIcon("sack", (1500, 470), T("riapparso") - 0.4, size=230, label="COME È RIAPPARSO"), "pop")
        sc.footer = "Fonti: Il Post · Finestre sull'Arte · Smithsonian · Live Science"
    elif i == 2:
        tc = T("Klimt") - 0.3
        sc.add(Chapter("01", "La *signora*", a, tc))
        tm = T("Ritratto") - 0.3
        sc.add(MapEl((880, 170, 1820, 860), [(0, (14.0, 47.6), 120), (dur, (14.4, 47.8), 132)], tc + 0.1, T("ritratti", 1) - 0.3,
                     pins=[dict(at="Vienna", label="Vienna", t=T("Vienna") - 0.2, side="r")], title="mappa: Natural Earth"))
        sc.add(Text("Gustav *Klimt*", (110, 190), tc + 0.1, T("ritratti", 1) - 0.3, size=84, maxw=740))
        sc.add(Pill("IL BACIO · I RITRATTI DORATI", (440, 360), T("Bacio") - 0.2, tm, size=38))
        sc.add(Calendar((300, 600), 220, [(T("1918") - 0.1, "MUORE NEL", "1918")], T("Muore") - 0.1, tm), "paper")
        sc.add(Img(lady_pic(240, 300), (620, 600), tm + 0.2, T("ritratti", 1) - 0.3, anim="drop", rot=2), "paper")
        sc.add(Pill("1916 - 1917", (620, 800), T("1916") - 0.1, T("ritratti", 1) - 0.3, size=40, accent=True))
        ti = T("ritratti", 1) - 0.2
        for k in range(5):
            sc.add(KIcon("dollar", (560 + k * 200, 520 + (k % 2) * 60), T("venduti") - 0.3 + 0.15 * k, size=150), "pop")
        sc.add(Text("I suoi *ritratti*, oggi", (960, 170), ti, size=72, anchor="ma"))
        sc.add(Icon("gavel", (960, 760), T("all'asta") - 0.2, size=150), "stamp")
        sc.add(Pill("DECINE DI MILIONI ALL'ASTA", (960, 330 + 40), T("decine") - 0.1, size=44, accent=True))
        sc.footer = "Fonti: Finestre sull'Arte · AGI · Live Science · artnet"
    elif i == 3:
        tg = T("La") - 0.3
        sc.add(Calendar((1650, 330), 220, [(a, "PIACENZA", "1925")], a, tg), "paper")
        sc.add(Figure(walk([(-100, FY), (720, FY)], a + 0.3, 340), a + 0.3, tg, kind="suit", s=1.0, label="GIUSEPPE RICCI ODDI"))
        sc.add(Img(lady_pic(220, 275), (1150, 520), T("compra") - 0.3, tg, anim="pop"), "pop")
        sc.add(Pill("COLLEZIONISTA", (1150, 760), T("collezionista") - 0.2, tg, size=40))
        sc.add(Arrow((800, 640), (1020, 560), T("compra"), tg, color=GOLD))
        sc.add(Facade((420, 320, 1500, 760), tg + 0.1, T("Ed") - 0.3, label="GALLERIA RICCI ODDI"))
        sc.add(Pill("GALLERIA D'ARTE MODERNA · PIACENZA", (960, 860), T("Galleria") - 0.2, T("Ed") - 0.3, size=40, accent=True))
        te = T("Ed") - 0.3
        sc.add(Gallery(GB, te, hl=T("appeso") - 0.3))
        sc.add(Pill("PER DECENNI", (960, 170), T("decenni") - 0.3, size=40))
        scene_cam(sc, (0, 960, 540, 1.0), (te + 0.3, 960, 540, 1.0), (dur, 860, 560, 1.25))
        sc.footer = "Fonti: artnet · Artribune · Finestre sull'Arte"
    elif i == 4:
        tp = T("uno") - 0.4
        sc.add(Text("Un quadro *raro*", (110, 200), a, size=80))
        sc.add(Big("3", (380, 400), T("tre") - 0.3, size=300, color=GOLD, fnt=OSW, sub="dipinti di Klimt\nnei musei italiani", subsize=40), "hit")
        sc.add(MapEl((820, 160, 1820, 880), [(0, (11.6, 43.2), 120), (dur, (11.6, 43.2), 132)], a + 0.2,
                     pins=[dict(at="Venezia", label="Venezia", t=T("Venezia") - 0.1, side="r"), dict(at="Roma", label="Roma", t=T("Roma") - 0.1, side="r"),
                           dict(at="Piacenza", label="PIACENZA", t=T("Piacenza") - 0.1, side="l", color=RED)], title="mappa: Natural Earth"))
        sc.add(Crowd((160, 780, 660, 890), 3, T("Ma") - 0.1, None, s=0.42, kinds=("expert", "suit", "man")))
        sc.add(Pill("FUORI CITTÀ, LA CONOSCONO IN POCHI", (410, 735), T("pochi") - 0.4, size=30, accent=True))
        sc.footer = "Fonti: Finestre sull'Arte · artnet"
    elif i == 5:
        tc = T("Una") - 0.35
        sc.add(Chapter("02", "Il *doppio* ritratto", a, tc))
        sc.add(Figure([(tc, 380, FY)], tc + 0.1, kind="expert", s=0.95, label="CLAUDIA MAGA · 18 ANNI"), "pop")
        sc.add(KIcon("book", (640, 640), T("libro") - 0.3, size=170), "pop")
        sc.add(Compare((1240, 500), 280, 350, T("nota") - 0.2, b_t=T("altro") - 0.1))
        sc.add(Pill("UNA SOMIGLIANZA", (1240, 200), T("somiglianza") - 0.2, T("Il") - 0.2, size=40))
        sc.add(Calendar((1700, 250), 170, [(T("1912") - 0.1, "MAI PIÙ VISTO DAL", "1912")], T("1912") - 0.2), "paper")
        scene_cam(sc, (0, 960, 540, 1.0), (T("altro"), 960, 540, 1.0), (dur, 990, 530, 1.04))
        sc.footer = "Fonti: Smithsonian · artnet · Reuters (Dawn)"
    elif i == 6:
        tx = T("L'intuizione") - 0.3
        sc.add(Compare((960, 500), 280, 350, a, tx, b_t=a, merge=T("perduto") - 0.4))
        sc.add(Stamp("PERDUTO?", (960, 180), T("perduto") - 0.1, tx, size=70, rot=-6))
        sc.add(Text("E se non fosse *mai sparito*?", (960, 820), T("se") - 0.2, tx, size=54, anchor="ma"))
        sc.add(XRay((700, 500), 300, 375, tx + 0.1, scan=T("raggi") - 0.1, dur=2.4))
        sc.add(KIcon("xray", (1300, 330), T("raggi") - 0.2, size=170), "pop")
        sc.add(Pill("UN ALTRO VOLTO", (1300, 520), T("volto") - 0.3, size=44, accent=True))
        sc.add(Pill("IL RITRATTO PERDUTO", (1300, 620), T("perduto", 1) - 0.2, size=40))
        sc.add(Text("Klimt lo aveva *ridipinto*", (1300, 720), T("ridipinto") - 0.4, size=44, anchor="ma"))
        sc.footer = "Fonti: Smithsonian · artnet · Reuters (Dawn) · ricostruzione grafica"
    elif i == 7:
        tn = T("La") - 0.3
        sc.add(XRay((480, 480), 260, 325, a, tn, scan=a + 0.2, dur=0.8, label=False))
        sc.add(Stamp("UNICO DOPPIO\nRITRATTO DI KLIMT", (1240, 460), T("l'unico") - 0.1, tn, size=72, rot=-7))
        news = newspaper(620, 700, "QUOTIDIANO", "Piacenza · 1996", "Il Klimt\n*nascosto*", "ricostruzione · titolo indicativo", seed=4)
        sc.add(Img(news, (480, 540), tn, T("diventare") - 0.8, anim="drop", rot=-3), "paper")
        tp = T("Palazzo") - 0.4
        sc.add(Facade((900, 330, 1800, 780), tp, None, label="PALAZZO GOTICO"))
        sc.add(Pill("MOSTRA IN PREPARAZIONE", (1350, 860), T("mostra") - 0.2, size=40))
        ts = T("diventare") - 0.8
        sc.add(Icon("crown", (480, 480), ts, T("Ma") - 0.2, size=260), "pop")
        sc.add(Stamp("NON ARRIVERÀ\nMAI", (480, 520), T("Ma") - 0.05, size=76, rot=-10))
        sc.footer = "Fonti: Smithsonian · Open · AGI"
    elif i == 8:
        tc = T("Nella") - 0.35
        sc.add(Chapter("03", "Il *furto*", a, tc))
        sc.add(Calendar((1760, 300), 150, [(tc, "FEBBRAIO", "1997")], tc), "paper")
        sc.add(Gallery(GB, tc + 0.1, boxes=T("Casse") - 0.3, hl=T("preparate") - 0.2))
        sc.add(Figure(walk([(300, 808), (1100, 808)], T("movimento") - 0.2, 260), T("movimento") - 0.2, kind="worker", s=0.38, carry=[(0, "painting")]))
        sc.add(Figure(walk([(1250, 808), (420, 808)], T("trasferite") - 0.3, 240), T("trasferite") - 0.3, kind="worker", s=0.38, flip=-1))
        sc.add(Pill("VERSO IL PALAZZO GOTICO", (960, 170), T("Palazzo") - 0.2, T("Casse") - 0.2, size=38))
        sc.add(Pill("CASSE, IMBALLAGGI", (960, 170), T("Casse") - 0.1, size=38, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (T("Casse") - 0.3, 960, 540, 1.0), (dur, 900, 560, 1.08))
        sc.footer = "Fonti: Open · AGI · Smithsonian · schema semplificato"
    elif i == 9:
        sc.add(Calendar((1760, 300), 150, [(a, "SABATO", "22"), (T("febbraio") - 0.2, "FEBBRAIO 1997", "22")], a), "paper")
        sc.add(Gallery(GB, a, hl=a, gone=T("non") - 0.1, boxes=a))
        sc.add(Figure(walk([(300, 808), (640, 808)], a + 0.3, 260), a + 0.3, kind="guard", s=0.4, arms=[(T("accorge") - 0.2, "point")]))
        sc.add(Pill("NON È PIÙ AL SUO POSTO", (960, 170), T("non") - 0.1, T("furto") - 0.5, size=40, accent=True))
        sc.add(ClockFace((1760, 610), 110, T("furto") - 0.4, None, start=3, speed=-14, label="NEI GIORNI PRIMA"), "pop")
        sc.add(Pill("IL MOMENTO ESATTO: MAI CHIARITO", (960, 170), T("Ma") - 0.1, size=40))
        scene_cam(sc, (0, 960, 540, 1.0), (T("non") - 0.3, 960, 540, 1.0), (T("non") + 1.0, 760, 480, 1.2), (T("furto") - 0.4, 760, 480, 1.2), (T("furto") + 0.6, 960, 540, 1.0))
        sc.footer = "Fonti: AGI · Live Science · Finestre sull'Arte · Smithsonian"
    elif i == 10:
        tr = T("tetto") - 0.2
        sc.add(Gallery(GB, a, gone=a, roof_frame=tr + 0.2, boxes=a))
        sc.add(Text("Il primo *indizio*", (960, 160), a, tr, size=60, anchor="ma"))
        sc.add(Icon("magnifier", (1120, 230), T("cornice") - 0.2, T("tela") - 0.3, size=130, move=(T("cornice"), 1.0, (1000, 260), 20)), "pop")
        sc.add(Stamp("VUOTA", (1000, 160), T("Vuota") - 0.1, size=80, rot=-8))
        sc.add(Pill("LA TELA È SPARITA", (960, 900 - 30), T("tela") - 0.2, size=40, accent=True))
        sc.add(Figure([(0, 1550, 808)], T("chi") - 0.2, kind="man", s=0.4, label="?"), "pop")
        scene_cam(sc, (0, 960, 540, 1.0), (tr, 960, 540, 1.0), (tr + 1.0, 960, 330, 1.5), (T("tela") - 0.3, 960, 330, 1.5), (T("tela") + 0.6, 960, 540, 1.0))
        sc.footer = "Fonti: Smithsonian · Reuters (Dawn) · artnet · schema semplificato"
    elif i == 11:
        tc = T("Il") - 0.35
        sc.add(Chapter("04", "Il *lucernario*", a, tc))
        g = sc.add(Gallery(GB, tc + 0.1, lift=T("agganciato") - 0.9, boxes=tc))
        sc.add(Figure(walk([(1200, g.roof_y), (g.sky_x + 90, g.roof_y)], T("salito") - 0.2, 300), T("salito") - 0.3, kind="man", s=0.4, flip=-1, arms=[(T("calato"), "hold")], label="IPOTESI"))
        sc.add(Pill("LA PRIMA IPOTESI", (960, 170), tc + 0.2, T("calato") - 0.2, size=38))
        sc.add(KIcon("fishing", (1160, 250), T("lenza") - 0.2, size=130, label="UNA LENZA?"), "pop")
        sc.add(Pill("ATTRAVERSO UN LUCERNARIO APERTO", (960, 170), T("lucernario") - 0.3, size=38, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (T("calato"), 960, 540, 1.0), (T("tirato") - 0.2, 860, 450, 1.15), (dur, 860, 450, 1.17))
        sc.footer = "Fonti: Reuters (Dawn) · Smithsonian · The Art Newspaper · ipotesi, schema semplificato"
    elif i == 12:
        tq = T("Ma") - 0.3
        g = sc.add(Gallery(GB, a, tq, gone=a, roof_frame=T("lasciando") - 0.1, boxes=a))
        sc.add(Figure(walk([(g.sky_x + 90, g.roof_y)], a)[:1] + walk([(g.sky_x + 90, g.roof_y), (2050, g.roof_y)], T("sparito") - 0.4, 420)[1:], a, tq, kind="man", s=0.4, carry=[(0, "painting")]))
        sc.add(Pill("TELA SENZA CORNICE", (960, 170), T("tolto") - 0.2, tq, size=38))
        sc.add(Stamp("QUALCOSA\nNON TORNA", (960, 330), tq + 0.1, T("Secondo") - 0.3, size=86, rot=-7))
        ts = T("Secondo") - 0.3
        sc.add(Img(lady_pic(330, 412), (720, 560), ts, anim="pop"), "pop")
        sc.add(Line((1080, 470), (1380, 470), ts + 0.2, None, (170, 210, 230), 10, 0.3))
        sc.add(Text("LUCERNARIO", (1230, 410), ts + 0.2, size=34, fnt=OSW, color=(170, 210, 230), anchor="ma"))
        sc.add(Arrow((900, 560), (1180, 480), T("passata") - 0.4, None, color=RED))
        sc.add(Stamp("NON PASSA?", (1230, 620), T("passata") - 0.1, size=60, rot=-6))
        sc.add(Text("secondo alcune ricostruzioni", (960, 830), ts + 0.3, size=30, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: Smithsonian · Reuters (Dawn) · schema semplificato"
    elif i == 13:
        sc.add(Text("Un'altra *ipotesi*", (960, 160), a, size=66, anchor="ma"))
        sc.add(Pill("A · DAL LUCERNARIO", (500, 280), a + 0.3, size=38))
        sc.add(KIcon("fishing", (500, 520), a + 0.4, size=260), "pop")
        sc.add(Line((960, 260), (960, 860), T("Che") - 0.3, None, DIM, 3, 0.3))
        sc.add(Pill("B · SPARITO PRIMA", (1420, 280), T("Che") - 0.2, size=38, accent=True))
        sc.add(KIcon("crate", (1300, 540), T("confusione") - 0.2, size=200), "pop")
        sc.add(ClockFace((1560, 520), 100, T("prima") - 0.2, None, start=6, speed=-10), "pop")
        sc.add(Stamp("MESSA IN\nSCENA?", (500, 520), T("messa") - 0.1, T("versioni") - 0.2, size=70, rot=-8))
        sc.add(Pill("LE VERSIONI NON COINCIDONO", (960, 790), T("versioni") - 0.2, size=40))
        sc.add(Stamp("MAI DIMOSTRATA", (960, 470), T("nessuna") - 0.1, size=74, rot=-6))
        sc.footer = "Fonti: Open · AGI · artnet · Smithsonian"
    elif i == 14:
        sc.add(Text("Mettiamo in fila gli *indizi*", (960, 160), a, size=66, anchor="ma"))
        sc.add(Icon("frame_empty", (420, 470), T("Uno") - 0.2, size=230, label="1 · CORNICE SUL TETTO"), "pop")
        sc.add(Calendar((960, 470), 220, [(T("Due") - 0.2, "QUANTI GIORNI?", "?")], T("Due") - 0.2), "paper")
        sc.add(Pill("2 · FURTO SCOPERTO IN RITARDO", (960, 690), T("Due"), size=32))
        sc.add(KIcon("crate", (1500, 470), T("Tre") - 0.2, size=230, label="3 · CASSE E PERSONE"), "pop")
        sc.add(Text("Tre indizi, *tre storie diverse*", (960, 800), T("Ognuno") - 0.2, size=54, anchor="ma"))
        sc.footer = "Fonti: Smithsonian · AGI · Open · ricostruzione divulgativa"
    elif i == 15:
        tc = T("Viene") - 0.35
        sc.add(Chapter("05", "Le *piste*", a, tc))
        sc.add(Calendar((260, 420), 200, [(tc, "APRILE", "1997")], tc), "paper")
        sc.add(Icon("envelope", (-100, 520), tc + 0.1, T("Gli") - 0.2, size=200, move=(tc + 0.1, 1.2, (900, 520), 120)))
        sc.add(Pill("UN PACCO INTERCETTATO", (900, 300), T("pacco") - 0.2, T("Gli") - 0.2, size=40))
        sc.add(Figure(walk([(2050, FY), (1450, FY)], T("Gli") - 0.6, 500), T("Gli") - 0.6, kind="police", s=1.0, flip=-1, carry=[(0, "magnifier")]))
        tf = T("falso") - 0.2
        sc.add(Img(lady_pic(260, 325), (900, 520), T("Gli") - 0.2, anim="pop"), "pop")
        sc.add(Stamp("FALSO", (900, 520), tf, size=110, rot=-12))
        sc.add(Pill("UNA COPIA", (900, 760), T("copia") - 0.2, size=44, accent=True))
        sc.footer = "Fonti: Smithsonian · artnet · Reuters (Dawn)"
    elif i == 16:
        sc.add(Crowd((260, 560, 1100, 870), 4, a, None, s=0.5, kinds=("guard", "worker", "guard", "man")))
        sc.add(Pill("CHI LAVORAVA NELLA GALLERIA", (680, 300), a + 0.3, size=40))
        sc.add(Icon("magnifier", (1450, 420), T("puntano") - 0.2, size=200, move=(T("puntano"), 1.6, (700, 420), 40)), "pop")
        sc.add(Pill("NESSUNA PROVA", (1450, 300), T("non") - 0.1, size=44, accent=True))
        sc.add(Stamp("ARCHIVIATO", (1400, 560), T("archiviato") - 0.2, size=96, rot=-8))
        sc.add(Pill("NESSUN COLPEVOLE", (1400, 760), T("Nessun") - 0.1, size=40))
        sc.add(Pill("NESSUN QUADRO", (1400, 840), T("nessun", 1) - 0.1, size=40))
        sc.footer = "Fonti: Smithsonian · Il Post"
    elif i == 17:
        sc.add(Calendar((300, 430), 220, [(a, "IL CASO", "?"), (T("chiuso") - 0.1, "CHIUSO", "X"), (T("riaperto") - 0.1, "RIAPERTO", "!")], a), "paper")
        news = newspaper(560, 640, "QUOTIDIANO", "anni 2010", "«So dov'è\nil *Klimt*»?", "ricostruzione · titolo indicativo", seed=9)
        sc.add(Img(news, (900, 520), T("Ai") - 0.2, anim="drop", rot=-3), "paper")
        sc.add(Bubble((1450, 330), 120, T("promette") - 0.2, inner=None, text="TORNERÀ"), "pop")
        sc.add(Calendar((1450, 640), 200, [(T("2017") - 0.2, "20° ANNIVERSARIO", "2017")], T("ventesimo") - 0.2), "paper")
        sc.add(Stamp("NON TORNA", (1450, 640), T("Non") - 0.05, size=80, rot=-10))
        sc.add(Stamp("NESSUNA\nCONFERMA", (900, 520), T("conferma") - 0.3, size=86, rot=-8))
        sc.footer = "Fonti: Smithsonian · artnet · racconto mai confermato"
    elif i == 18:
        sc.add(Pill("TRA LE OPERE PIÙ RICERCATE AL MONDO", (960, 200), a + 0.3, size=44))
        sc.add(CardGrid((260, 280, 1660, 520), a + 0.2, T("valore") - 0.3, cols=14, rows=4, scan=2.0))
        sc.add(Big("$ 66 MLN", (960, 470), T("sessantasei") - 0.3, T("A") - 0.3, size=200, color=GOLD, fnt=OSW,
                   count=(0, 66, lambda z: f"$ {z:.0f} MLN", 1.2), sub="stime riportate dalla stampa internazionale", subsize=36), "hit")
        sc.add(KIcon("dollar", (420, 470), T("valore") - 0.1, T("A") - 0.3, size=170), "pop")
        sc.add(Frame((960, 560), 230, 290, T("A") - 0.2, None, vanish=T("vuoto") - 0.6, label="PIACENZA"))
        sc.footer = "Fonti: Smithsonian · Bloomberg · Il Post · Finestre sull'Arte"
    elif i == 19:
        tc = T("Martedì") - 0.35
        sc.add(Chapter("06", "L'*edera*", a, tc))
        sc.add(Pill("22 ANNI DOPO", (960, 760), T("ventidue") - 0.2, tc, size=48, accent=True), "hit")
        sc.add(Calendar((1760, 330), 150, [(tc, "1997", "..."), (T("10") - 0.1, "DICEMBRE 2019", "10")], tc, T("Stanno") - 0.1), "paper")
        g = sc.add(Gallery(GB, tc + 0.2, hl=None, gone=tc))
        sc.add(Figure(walk([(1950, 808), (1500, 808)], T("giardinieri") - 0.5, 320), T("giardinieri") - 0.5, kind="worker", s=0.4, flip=-1, arms=[(T("togliendo"), "up")]))
        sc.add(Figure(walk([(2050, 808), (1650, 808)], T("giardinieri") - 0.3, 320), T("giardinieri") - 0.3, kind="worker", s=0.4, flip=-1, arms=[(T("togliendo") + 0.3, "up")]))
        sc.add(Pill("MANUTENZIONE NEL CORTILE", (960, 170), T("manutenzione") - 0.3, T("Stanno") - 0.1, size=38))
        sc.add(KIcon("leaf", (1280, 600), T("l'edera") - 0.2, size=110), "pop")
        scene_cam(sc, (0, 960, 540, 1.0), (T("giardinieri") - 0.4, 960, 540, 1.0), (T("Stanno"), 1400, 600, 1.35), (dur, 1400, 600, 1.38))
        sc.footer = "Fonti: Finestre sull'Arte · Live Science · artnet · schema semplificato"
    elif i == 20:
        sc.add(Niche((260, 170, 1660, 880), a, None, clear=a, door=a + 0.2, open_=T("aprono") - 0.1, sack=T("sacco") - 0.6, canvas=T("tela") - 0.2))
        sc.add(Pill("SPORTELLO DI METALLO", (960, 200), a + 0.3, T("Lo") - 0.1, size=40))
        sc.add(Pill("UNA CAVITÀ NEL MURO", (960, 200), T("cavità") - 0.2, T("sacco") - 0.2, size=40))
        sc.add(Pill("SACCO NERO DI PLASTICA", (960, 200), T("sacco") - 0.1, T("tela") - 0.2, size=40, accent=True))
        sc.add(Pill("UNA TELA", (960, 200), T("tela") - 0.1, size=44, accent=True))
        scene_cam(sc, (0, 960, 540, 1.05), (T("aprono"), 960, 540, 1.15), (T("sacco"), 960, 540, 1.3), (dur, 1060, 520, 1.3))
        sc.footer = "Fonti: Il Post · Reuters (Dawn) · The Art Newspaper · Finestre sull'Arte"
    elif i == 21:
        g = sc.add(Gallery(GB, a, gone=a, niche=a))
        sc.add(Text("Pensiamo a cosa *vuol dire*", (960, 160), a, T("Per") - 0.2, size=60, anchor="ma"))
        sc.add(Figure([(0, 360, 808)], T("polizia") - 0.2, kind="police", s=0.4), "pop")
        sc.add(Icon("newspaper", (560, 600), T("giornalisti") - 0.2, size=120), "pop")
        sc.add(Figure([(0, 760, 808)], T("collezionisti") - 0.3, kind="suit", s=0.4), "pop")
        sc.add(Pill("22 ANNI DI RICERCHE", (960, 170), T("Per") - 0.1, T("Dietro") - 0.3, size=38))
        sc.add(Arrow((g.nc[0], g.nc[1] - 40), (g.pc[0] + 60, g.pc[1]), T("passi") - 0.4, None, color=GOLD, bend=0.25, dashed=True))
        sc.add(Pill("A POCHI PASSI DALLA SALA", (960, 170), T("passi") - 0.2, size=40, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (T("Dietro") - 0.3, 960, 540, 1.0), (T("Dietro") + 0.8, 1300, 560, 1.25), (T("passi") - 0.3, 1300, 560, 1.25), (T("passi") + 0.6, 1100, 540, 1.08))
        sc.footer = "Fonti: Il Post · Live Science · The Art Newspaper · schema semplificato"
    elif i == 22:
        sc.add(Figure(walk([(-100, FY), (380, FY)], a, 380), a, kind="police", s=1.0, carry=[(0, "painting")], label="POLIZIA"))
        tb = T("Sul") - 0.3
        sc.add(Img(canvas_back(560, 680), (1000, 520), tb, anim="drop", rot=2), "paper")
        sc.add(Pill("IL RETRO DELLA TELA", (1000, 170), tb + 0.1, T("Ma") - 0.3, size=38))
        sc.add(Pill("TIMBRI E CERALACCA", (1500, 360), T("ceralacca") - 0.3, size=36, accent=True))
        sc.add(Bubble((1550, 560), 110, T("falso") - 0.6, inner="magnifier", text="FALSO?"), "pop")
        sc.add(Stamp("SERVE UNA\nPERIZIA", (1000, 520), T("perizia") - 0.2, size=90, rot=-9))
        sc.footer = "Fonti: Il Post · Smithsonian · Reuters (Dawn) · ricostruzione grafica"
    elif i == 23:
        tc = T("Controllano") - 0.35
        sc.add(Chapter("07", "La *perizia*", a, tc))
        for k, x in enumerate((240, 420, 600)):
            sc.add(Figure([(0, x, FY)], tc + 0.1 + 0.15 * k, kind="expert", s=0.85, carry=[(0, "magnifier")] if k == 1 else None), "pop")
        sc.add(Text("3 esperti nominati dalla procura", (420, 230), tc + 0.2, size=40, fnt=OSW, anchor="ma"))
        rows = [dict(label="Telaio", value="OK", t=T("telaio") - 0.1), dict(label="Timbri", value="OK", t=T("timbri") - 0.1),
                dict(label="Sigilli", value="OK", t=T("sigilli") - 0.1), dict(label="Etichette", value="OK", t=T("etichette") - 0.1)]
        sc.add(Rows(rows, tc + 0.1, T("Poi") - 0.3, x0=900, x1=1680, y=300, gap=100, size=46))
        sc.add(Calendar((1290, 520), 200, [(T("1996") - 0.2, "ANALISI DEL", "1996")], T("confrontano") - 0.2, T("Poi") - 0.3), "paper")
        sc.add(Pill("CONFRONTO CON LE ANALISI PRIMA DEL FURTO", (1290, 760), T("confrontano"), T("Poi") - 0.3, size=32))
        sc.add(KIcon("xray", (1290, 520), T("Poi") - 0.1, size=240, label="LA PROVA PIÙ DIFFICILE DA FALSIFICARE"), "pop")
        sc.footer = "Fonti: Open · AGI · Finestre sull'Arte"
    elif i == 24:
        tv = T("Venerdì") - 0.3
        sc.add(XRay((960, 500), 340, 425, a, tv, scan=T("raggi") - 0.1, dur=2.6))
        sc.add(Pill("IL RITRATTO NASCOSTO", (960, 170), a + 0.2, tv, size=40))
        sc.add(Pill("È LÌ", (1420, 500), T("lì") - 0.2, tv, size=56, accent=True))
        sc.add(Calendar((480, 470), 230, [(tv, "VENERDÌ", "17"), (T("gennaio") - 0.1, "GENNAIO 2020", "17")], tv), "paper")
        sc.add(Icon("camera", (1440, 380), T("conferenza") - 0.3, size=170, label="CONFERENZA STAMPA"), "pop")
        sc.add(Flash(T("conferenza") + 0.2))
        sc.add(Img(lady_pic(300, 375), (960, 520), T("autentico") - 0.5, anim="pop"), "pop")
        sc.add(Stamp("AUTENTICO", (960, 560), T("autentico") - 0.1, size=110, color=(60, 150, 80), rot=-10))
        sc.footer = "Fonti: artnet · AGI · Finestre sull'Arte · Open"
    elif i == 25:
        sc.add(Img(lady_pic(380, 475), (760, 520), a, anim="drop"), "paper")
        sc.add(Pill("OTTIME CONDIZIONI", (1380, 300), a + 0.3, size=48, accent=True))
        sc.add(Line((930, 640), (950, 690), T("segno") - 0.1, None, (240, 240, 240), 5, 0.3))
        sc.add(Icon("magnifier", (1000, 690), T("segno") - 0.3, size=170), "pop")
        sc.add(Pill("UN PICCOLO SEGNO SUL BORDO", (1380, 450), T("segno"), size=38))
        sc.add(Text("tolta in fretta\ndalla cornice?", (1380, 560), T("tolta") - 0.2, size=48, anchor="ma", align="m"))
        sc.add(Bubble((1380, 790 - 40), 80, T("domanda") - 0.4, text="?"), "pop")
        scene_cam(sc, (0, 960, 540, 1.0), (T("segno") - 0.3, 960, 540, 1.0), (T("segno") + 0.6, 900, 600, 1.3), (T("Ma") - 0.3, 900, 600, 1.3), (T("Ma") + 0.4, 960, 540, 1.0))
        sc.footer = "Fonti: Live Science · artnet · Smithsonian · Reuters (Dawn)"
    elif i == 26:
        g = sc.add(Gallery(GB, a, T("Le") - 0.3, gone=a, niche=a, question=T("davvero") - 0.2))
        sc.add(Pill("22 ANNI NEL MURO?", (700, 170), T("davvero") - 0.1, T("Le") - 0.3, size=40))
        sc.add(Pill("O RIMESSO LÌ DOPO?", (1300, 170), T("Oppure") - 0.1, T("Le") - 0.3, size=40, accent=True))
        tl_ = T("Le") - 0.3
        sc.add(Text("Le versioni *non coincidono*", (960, 300), tl_, size=66, anchor="ma"))
        sc.add(Figure([(0, 960, FY)], T("chi") - 0.3, kind="man", s=1.0, label="?"), "pop")
        sc.add(Stamp("NESSUN\nCOLPEVOLE", (1440, 600), T("colpevole") - 0.2, size=86, rot=-8))
        sc.add(Icon("gavel", (480, 600), T("furto") - 0.3, size=200), "stamp")
        sc.footer = "Fonti: Open · Smithsonian · Live Science · The Art Newspaper"
    elif i == 27:
        tr = T("Ricapitolando") - 0.3
        sc.add(Calendar((1760, 300), 150, [(a, "NOVEMBRE 2020", "28")], a, tr), "paper")
        sc.add(Gallery(GB, a, tr, gone=a - 1, back=T("torna") - 0.1))
        sc.add(Pill("DI NUOVO IN GALLERIA, IN UNA TECA", (960, 170), T("teca") - 0.4, tr, size=40, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (tr - 0.3, 960, 540, 1.05))
        sc.add(Text("Ricapitolando", (960, 190), tr + 0.1, size=66, anchor="ma"))
        sc.add(KIcon("xray", (360, 520), T("quadro") - 0.2, size=210, label="DOPPIO RITRATTO"), "pop")
        sc.add(Icon("frame_empty", (760, 520), T("cornice") - 0.2, size=210, label="CORNICE SUL TETTO"), "pop")
        sc.add(Icon("envelope", (1160, 520), T("falso") - 0.3, size=210, label="IL FALSO"), "pop")
        sc.add(KIcon("sack", (1560, 520), T("tela") - 0.3, size=210, label="NEL MURO, 22 ANNI DOPO"), "pop")
        sc.footer = "Fonti: Artribune · The Art Newspaper · ricostruzione divulgativa"
    elif i == 28:
        ts = T("Iscriviti") - 0.3
        sc.add(Gallery(GB, a, T("Scrivilo") - 0.2, gone=a, niche=a, question=a))
        sc.add(Pill("NEL MURO PER 22 ANNI?", (700, 170), T("Secondo") - 0.1, T("Scrivilo") - 0.2, size=40))
        sc.add(Pill("O RIPORTATO DOPO?", (1260, 170), T("riportato") - 0.3, T("Scrivilo") - 0.2, size=40, accent=True))
        sc.add(Bubble((960, 470), 170, T("Scrivilo") - 0.1, ts, text="COMMENTI"), "pop")
        sc.add(Text("Fonti nella descrizione", (960, 760), T("fonti") - 0.2, ts, size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(110), (960, 520), ts, anim="pop", shadow=False), "hit")
        sc.add(Text("ogni giorno un nuovo caso", (960, 700), T("ogni") - 0.2, size=54, fnt=PS, color=GOLD, anchor="ma"))
        sc.footer = "Ricostruzione divulgativa · voce generata con sintesi vocale"
    return sc


def thumbnail(path="thumbnail.jpg"):
    im = make_bg(7).convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    Niche((1060, 120, 1860, 960), -5, None, clear=-1.2, door=-5, open_=-5, sack=-5).draw(lay, 0.6, 1.0)
    im.alpha_composite(lay)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    place(lay, lady_pic(300, 375).rotate(-8, expand=True, resample=Image.BICUBIC), (1560, 440), "mm", 1.0)
    im.alpha_composite(lay)
    t = rich_img("RUBATO.\nRITROVATO\nNEL *MURO*", SERIF, 140, WHITE, RED, lh=1.0)
    im.alpha_composite(t, (90, 150))
    st = stamp_img("CASO 004", RED, 70, -10); im.alpha_composite(st, (720, 70))
    d = ImageDraw.Draw(im)
    d.text((100, 800), "UN KLIMT SPARITO PER 22 ANNI.", font=font(OSW, 58, 600), fill=GOLD + (255,))
    wm = wordmark(60, sub=False); im.alpha_composite(wm, (100, 960))
    im.convert("RGB").save(path, quality=92)
