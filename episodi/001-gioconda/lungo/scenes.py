from fi import *
from fx import *

W, H = 1920, 1080
FY = 870  # pavimento (piedi degli omini)
F_BASE = "Fonti: Focus · Finestre sull'Arte · History.com · Smithsonian Magazine"

PBOX = (260, 180, 1660, 860)
R_ENT = (0.02, 0.64, 0.26, 0.97, "Ingresso\noperai")
R_SALON = (0.04, 0.04, 0.42, 0.46, "Salon Carré", True, 34)
R_SCALA = (0.50, 0.04, 0.70, 0.66, "Scala di\nservizio")
R_PORTA = (0.735, 0.47, 0.815, 0.63, "")
R_EXIT = (0.85, 0.24, 0.995, 0.97, "Cortile,\npoi la\nstrada")
ROOMS = [R_ENT, R_SALON, R_SCALA, R_PORTA, R_EXIT]
def PP(p): return (PBOX[0] + (PBOX[2] - PBOX[0]) * p[0], PBOX[1] + (PBOX[3] - PBOX[1]) * p[1])

def walk(pts, t0, speed=260):
    """pts schermo -> chiavi (t, x, y) a velocità costante"""
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

def left(sc, text, y, t0, t1=None, size=64, color=WHITE, fnt=SERIF, x=110, maxw=700):
    return sc.add(Text(text, (x, y), t0, t1, size=size, fnt=fnt, color=color, maxw=maxw))

def build(i, dur, a, words):
    T = Clock(words, a); sc = Scene(dur)
    if i == 0:
        tin = T("Dentro") - 0.3
        sc.add(Calendar((230, 380), 230, [(a, "AGOSTO 1911", "21")], a, tin), "paper")
        sc.add(Text("PARIGI · LUNEDÌ", (230, 560), a + 0.2, tin, size=36, fnt=TYPE, color=GOLD, anchor="ma"))
        sc.add(Facade((560, 330, 1780, 780), T("museo") - 0.3, tin, label="LOUVRE", closed_t=T("chiuso")))
        scene_cam(sc, (0, 960, 540, 1.0), (tin - 0.2, 960, 540, 1.04), (tin + 0.3, 960, 540, 1.0), (T("esce"), 960, 560, 1.08), (T("Nessuno") - 0.3, 960, 540, 1.0), (dur, 960, 540, 1.04))
        wall = sc.add(Wall((60, 170, 1860, 830), tin, T("Nessuno") - 0.3, gone_t=T("stacca") + 0.5))
        gx, gy, gw, gh, _ = wall.frames[2]
        sc.add(Figure(walk([(-120, FY), (gx + gw / 2 - 60, FY)], tin, 380) + [(T("esce") - 0.1, gx + gw / 2 - 60, FY)] + walk([(gx + gw / 2 - 60, FY), (2100, FY)], T("esce"), 420)[1:],
                      tin, T("Nessuno") - 0.3, carry=[(T("stacca") + 0.5, "painting"), (T("nasconde"), "hidden")]))
        sc.add(ClockFace((960, 470), 210, T("Nessuno") - 0.1, None, start=7, speed=9, label="24+ ORE"), "hit")
        sc.footer = F_BASE
    elif i == 1:
        t1 = T("quell'uomo") - 0.3
        sc.add(Img(painting_icon(240), (960, 470), a, t1, anim="pop", shadow=True))
        sc.add(Pill("LA GIOCONDA · LEONARDO DA VINCI", (960, 760), T("Gioconda"), t1, size=40))
        t2 = T("Questo") - 0.3
        sc.add(Figure([(t1, 620, FY)], t1, t2, kind="worker", s=1.15), "pop")
        sc.add(Text("GENIO DEL CRIMINE", (1300, 300), T("genio") - 0.2, t2, size=60, fnt=OSW, color=GREY, anchor="ma"))
        sc.add(Line((1020, 335), (1580, 335), T("crimine") + 0.3, t2, RED, 10, 0.3))
        sc.add(Pill("DECORATORE ITALIANO", (1300, 480), T("decoratore"), t2, size=42))
        sc.add(Pill("29 ANNI", (1300, 590), T("29"), t2, size=42))
        sc.add(Pill("AL LOUVRE CI AVEVA LAVORATO", (1300, 700), T("lavorato") - 0.2, t2, size=42, accent=True))
        t3 = T("Vedremo") - 0.3
        cover = paper(520, 640, (196, 160, 104), 9, 0.7); d = ImageDraw.Draw(cover)
        d.rectangle([50, 110, 470, 310], fill=(232, 222, 200, 255), outline=INK + (255,), width=3)
        d.text((260, 145), "FASCICOLO N. 001", font=font(COUR, 32), fill=INK + (255,), anchor="ma")
        d.text((260, 200), "IL FURTO DELLA", font=font(TYPE, 38), fill=INK + (255,), anchor="ma")
        d.text((260, 248), "GIOCONDA", font=font(TYPE, 50), fill=RED + (255,), anchor="ma")
        d.text((260, 360), "Parigi · Firenze · 1911-1914", font=font(COURR, 26), fill=INK + (255,), anchor="ma")
        sc.add(Img(cover, (960, 520), t2 + 0.2, t3, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 001", (1130, 300), T("fascicolo") + 0.2, t3, size=70, rot=-12))
        sc.add(Icon("corridor", (420, 470), T("uscito") - 0.3, size=230, label="COME È USCITO"), "pop")
        sc.add(Icon("magnifier", (960, 470), T("polizia"), size=230, label="PERCHÉ NON L'HANNO TROVATO"), "pop")
        sc.add(Icon("museum", (1500, 470), T("Firenze") - 0.5, size=230, label="COME È FINITO A FIRENZE"), "pop")
        sc.footer = F_BASE
    elif i == 2:
        tc = T("nato") - 0.35
        sc.add(Chapter("01", "Il *ladro*", a, tc))
        sc.add(Text("Vincenzo *Peruggia*", (110, 190), tc + 0.1, size=84, maxw=760))
        sc.add(Calendar((250, 470), 200, [(T("1881"), "NATO NEL", "1881")], T("1881") - 0.1), "paper")
        sc.add(Figure([(tc, 560, 800)], T("Dumenza"), kind="worker", s=0.95, label="DUMENZA (VA)"), "pop")
        sc.add(Pill("DECORATORE E VETRAIO", (420, 870), T("decoratore"), size=40, accent=True))
        sc.add(MapEl((880, 190, 1820, 860), [(0, (5.6, 47.4), 92), (dur, (5.6, 47.4), 104)], tc + 0.1,
                     routes=[dict(pts=["Dumenza", "Parigi"], t=T("emigrato") - 0.2, d=2.2, icon="person")],
                     pins=[dict(at="Dumenza", label="Dumenza", t=T("Dumenza"), side="r"), dict(at="Parigi", label="Parigi", t=T("Francia"), side="l")],
                     title="mappa: Natural Earth"))
        sc.footer = "Fonti: Focus · VareseNews · Quotidiano.net"
    elif i == 3:
        tk = T("Conosce") - 0.3
        sc.add(Pill("AL LOUVRE: VETRAIO", (480, 220), a, tk, size=46))
        sc.add(Frame((1380, 480), 260, 378, a + 0.1, tk))
        sc.add(Figure(walk([(-120, FY), (1080, FY)], a + 0.2, 330), a + 0.2, tk, carry=[(0, "glass"), (T("teche"), None)]))
        sc.add(Icon("glass", (1380, 480), T("teche"), tk, size=430, anim="pop"), "pop")
        sc.add(Pill("TECA DI VETRO", (1380, 720), T("teche") + 0.3, tk, size=36))
        sc.add(Text("compresa, secondo le ricostruzioni,\nquella della *Gioconda*", (110, 320), T("compresa"), tk, size=44, fnt=PS, color=WHITE))
        sc.add(Text("Conosce:", (960, 220), tk + 0.1, size=56, fnt=SERIF, anchor="ma"))
        sc.add(Icon("corridor", (480, 520), T("corridoi"), size=250, label="I CORRIDOI"), "pop")
        sc.add(Icon("stairs", (960, 520), T("scale"), size=250, label="LE SCALE DI SERVIZIO"), "pop")
        sc.add(Icon("smock", (1440, 520), T("camice"), size=250, label="IL CAMICE BIANCO"), "pop")
        sc.footer = "Fonti: History.com · Cracked · Nation (ricostruzioni sulla teca)"
    elif i == 4:
        tc = T("impronte") - 0.2
        sc.add(Text("Un dettaglio che *conterà*", (960, 190), a, tc, size=64, anchor="ma"))
        sc.add(Calendar((260, 470), 220, [(T("1909"), "PARIGI", "1909")], T("1909") - 0.1, tc), "paper")
        sc.add(Figure([(a, 900, FY)], a + 0.2, tc, kind="worker", label="PERUGGIA"))
        sc.add(Figure(walk([(2100, FY), (1250, FY)], T("fermato") - 0.8, 600), T("fermato") - 0.8, tc, kind="police", arms=[(T("fermato"), "point")], flip=-1))
        sc.add(Icon("handcuffs", (1080, 640), T("fermato"), tc, size=130), "pop")
        sc.add(Icon("camera", (620, 460), T("foto") - 0.3, tc, size=200), "pop")
        sc.add(Flash(T("foto") + 0.3))
        card = id_card(780, 640, [("NOME", "Vincenzo Peruggia"), ("ANNO", "1909"), ("CITTÀ", "Parigi"), ("NOTE", "foto e impronte")])
        sc.add(Img(card, (960, 520), tc, anim="drop", rot=-2), "paper")
        sc.add(Stamp("SCHEDATO", (1180, 300), tc + 0.5, size=62, rot=10))
        sc.footer = "Fonti: Wikipedia (foto segnaletica 1909) · CrimeReads · Advance.hr"
    elif i == 5:
        wall = sc.add(Wall((60, 170, 1860, 830), a, hl_t=T("Salon")))
        gx, gy, gw, gh, _ = wall.frames[2]; gc = (gx + gw / 2, gy + gh / 2)
        sc.add(Pill("SALON CARRÉ · MUSEO DEL LOUVRE", (960, 120 + 110), T("Salon"), T("piccolo") - 0.3, size=40))
        scene_cam(sc, (0, 960, 540, 1.0), (T("piccolo") - 0.2, 960, 540, 1.0), (T("piccolo") + 0.8, gc[0], gc[1] + 40, 2.0),
                  (T("famosa") - 0.2, gc[0], gc[1] + 40, 2.0), (T("famosa") + 0.8, 960, 540, 1.0), (dur, 960, 540, 1.03))
        sc.add(Text("77 × 53 cm", (gc[0], gy + gh + 22), T("77"), T("famosa") - 0.2, size=34, fnt=OSW, color=GOLD, anchor="ma"))
        sc.add(Crowd((520, 680, 1400, 870), 5, T("famosa"), None, s=0.62, kinds=("expert", "suit", "poet")))
        sc.add(Pill("FAMOSA TRA GLI ESPERTI", (960, 230), T("famosa") + 0.2, T("ancora") - 0.2, size=40))
        sc.add(Pill("MA NON ANCORA UN'ICONA MONDIALE", (960, 230), T("ancora"), size=40, accent=True))
        sc.footer = "Fonti: Smithsonian Magazine · CrimeReads · Louvre (dimensioni)"
    elif i == 6:
        tc = T("Il") - 0.3
        sc.add(Chapter("02", "Lunedì *mattina*", a, tc))
        P_IN = [PP(p) for p in [(0.06, 0.92), (0.06, 0.55), (0.18, 0.55), (0.18, 0.36)]]
        sc.add(Plan(PBOX, ROOMS, tc + 0.1, None, [(P_IN, T("entra"), 2.6)], [], title="SCHEMA SEMPLIFICATO · NON IN SCALA"))
        sc.add(Figure([(0, *PP((0.32, 0.30)))], T("custodi"), kind="guard", s=0.3), "pop")
        sc.add(Figure([(0, *PP((0.60, 0.50)))], T("operai") - 0.1, kind="worker", s=0.3), "pop")
        sc.add(Figure([(0, *PP((0.92, 0.80)))], T("pulizie") - 0.2, kind="man", s=0.3), "pop")
        sc.add(ClockFace((1760, 300), 90, T("sette") - 0.4, None, start=6.9, speed=0.05, label="ORE 7"), "pop")
        sc.add(Figure(walk(P_IN, T("entra"), 160), T("entra"), kind="worker", s=0.32, label="PERUGGIA"), "pop")
        sc.add(Pill("MUSEO CHIUSO AL PUBBLICO", (960, 905 - 30), T("Il"), T("entra") - 0.3, size=34))
        scene_cam(sc, (0, 960, 540, 1.0), (T("entra"), 960, 540, 1.0), (T("entra") + 1.2, 800, 600, 1.15), (dur, 800, 600, 1.18))
        sc.footer = "Fonti: History Hit · Mona Lisa Missing · Auralcrave"
    elif i == 7:
        sc.add(Text("Le versioni *non coincidono*", (960, 170), a, size=66, anchor="ma"))
        d0 = T("Secondo") - 0.2; d1 = T("Lui") - 0.2
        sc.add(Pill("A · ALCUNE RICOSTRUZIONI", (500, 300), d0, size=36))
        sc.add(Icon("moon", (300, 450), d0 + 0.2, size=140), "pop")
        sc.add(Door((560, 840), 240, 420, d0 + 0.1))
        sc.add(Figure([(0, 560, 840)], T("ripostiglio") - 0.5, kind="worker", s=0.95), "pop")
        sc.add(Pill("LA NOTTE NASCOSTO IN UN RIPOSTIGLIO", (500, 900), T("ripostiglio"), size=30))
        sc.add(Line((960, 280), (960, 880), d1 - 0.3, None, DIM, 3, 0.3))
        sc.add(Pill("B · LA VERSIONE DI PERUGGIA", (1420, 300), d1, size=36, accent=True))
        sc.add(Icon("sun", (1240, 450), d1 + 0.2, size=140), "pop")
        sc.add(Door((1600, 840), 240, 420, d1 + 0.1, open_t=d1 + 0.4))
        sc.add(Figure(walk([(1100, 840), (1560, 840)], T("mattina") - 0.3, 300), T("mattina") - 0.3, kind="worker", s=0.95))
        sc.add(Pill("ALLE 7, DALLA PORTA DEGLI OPERAI", (1420, 900), T("porta"), size=30))
        sc.footer = "Fonti: The Week · TheCollector · Mona Lisa Missing · Wikipedia"
    elif i == 8:
        wall = sc.add(Wall((-300, 170, 1500, 830), a, gone_t=T("stacca") + 0.6))
        gx, gy, gw, gh, _ = wall.frames[2]; px = gx + gw / 2
        sc.add(Pill("1 · SALON CARRÉ: NESSUNO", (420, 230), a, T("porta") - 0.2, size=36))
        sc.add(Figure([(a, px - 140, FY), (T("stacca") - 0.3, px, FY), (T("porta"), px, FY)] + walk([(px, FY), (1520, FY)], T("porta"), 300)[1:],
                      a, None, carry=[(T("stacca") + 0.6, "painting"), (T("toglie") + 0.6, "hidden")]))
        sc.add(Text("4 ganci", (px, gy + gh + 30), T("quattro"), T("porta"), size=40, fnt=OSW, color=GOLD, anchor="ma"))
        sc.add(Icon("stairs", (1680, 640), T("scala") - 0.6, size=420), "pop")
        sc.add(Pill("2 · SCALA DI SERVIZIO", (1680, 360), T("scala"), size=36))
        sc.add(Icon("frame_empty", (1560, 760), T("toglie") + 0.3, size=150, move=(T("toglie") + 0.3, 0.6, (1460, 800), 80)), "pop")
        sc.add(Icon("glass", (1600, 760), T("teca") + 0.1, size=140, move=(T("teca") + 0.1, 0.6, (1760, 810), 80)), "pop")
        sc.add(Pill("CORNICE E VETRO RESTANO QUI", (1520, 940 - 70), T("lascia"), size=30, accent=True))
        scene_cam(sc, (0, 900, 540, 1.15), (T("porta"), 900, 540, 1.15), (T("porta") + 2.0, 1400, 560, 1.15), (dur, 1450, 560, 1.2))
        sc.footer = "Fonti: History.com · Advance.hr · Wikipedia"
    elif i == 9:
        sc.add(Icon("stairs", (360, 600), a, size=480))
        sc.add(Figure(walk([(250, 470), (560, FY), (1060, FY)], a + 0.1, 260), a, kind="worker", carry=[(0, "hidden")], arms=[(T("Prova"), "point")]))
        sc.add(Door((1300, FY), 220, 400, a + 0.1, lock_t=T("chiusa"), knob_off=T("smontare") + 0.4))
        sc.add(Pill("3 · LA PORTA È CHIUSA A CHIAVE", (1300, 330 - 40), T("chiusa"), size=36))
        sc.add(Icon("knob", (1210, 680), T("smontare") + 0.4, size=60, move=(T("smontare") + 0.4, 0.5, (1120, 740), 40)), "pop")
        sc.add(Text("senza riuscirci", (960, 200), T("senza"), T("arriva"), size=44, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Figure(walk([(2100, FY), (1600, FY)], T("arriva"), 380), T("arriva"), kind="plumber", label="SAUVET · IDRAULICO", flip=-1))
        scene_cam(sc, (0, 700, 560, 1.12), (T("chiusa") - 0.2, 1100, 600, 1.25), (T("arriva"), 1150, 580, 1.2), (dur, 1250, 560, 1.1))
        sc.footer = "Fonti: History.com · History Hit · The Week · CrimeReads"
    elif i == 10:
        to = T("apre")
        sc.add(Door((1300, FY), 220, 400, a, lock_t=a - 5, unlock_t=to + 0.2, open_t=to + 0.2, knob_off=a - 5))
        sc.add(Figure([(a, 1060, FY), (to + 0.6, 1060, FY)] + walk([(1060, FY), (1300, FY)], to + 0.6, 300)[1:], a, to + 1.6, kind="worker", carry=[(0, "hidden")]))
        sc.add(Figure([(a, 1600, FY), (T("Prende"), 1600, FY), (to - 0.1, 1420, FY), (T("Il"), 1420, FY)], a, None, kind="plumber", carry=[(T("Prende"), "pliers")], flip=-1, label="SAUVET"))
        sc.add(Pill("NON SOSPETTA NIENTE", (1500, 300), T("sospetta"), T("Prende"), size=36))
        sc.add(Pill("4 · ESCE DAL LOUVRE", (1300, 300), T("uscire"), T("Più") - 0.3, size=36, accent=True))
        sc.add(Pill("AIUTATO DA UN DIPENDENTE DEL MUSEO", (960, 200), T("grazie"), T("Più") - 0.3, size=40))
        tp = T("Più") - 0.2
        sc.add(Figure([(tp, 560, FY)], tp, kind="man", label="UN PASSANTE"), "pop")
        sc.add(Icon("knob", (300, 560), T("gettare"), size=70, move=(T("gettare"), 1.0, (160, 860), 220)), "pop")
        sc.add(Pill("UNA MANIGLIA GETTATA IN UN FOSSO", (560, 230), T("maniglia", 1), size=36, accent=True))
        scene_cam(sc, (0, 1250, 600, 1.25), (to + 1.5, 1250, 600, 1.25), (tp - 0.1, 1100, 560, 1.0), (dur, 900, 560, 1.05))
        sc.footer = "Fonti: The American · CrimeReads · History.com"
    elif i == 11:
        tn = T("Nasconde") - 0.3
        sc.add(Icon("house", (1450, 600), a, tn, size=420, label="RUE DE L'HÔPITAL SAINT-LOUIS"))
        sc.add(Figure(walk([(-120, FY), (1300, FY)], a, 420), a, tn, kind="worker", carry=[(0, "hidden")]))
        sc.add(Icon("bed", (560, 720), tn + 0.1, size=420), "paper")
        sc.add(Trunk((1300, 730), 380, tn + 0.1), "paper")
        sc.add(Img(painting_icon(110), (900, 560), tn + 0.1, T("Nasconde") + 1.5, anim="pop", shadow=False))
        sc.add(ClockFace((960, 300), 110, T("aspetta") - 0.2, None, start=9, speed=12), "pop")
        sc.footer = "Fonti: Quotidiano.net · Ecoseven · Finestre sull'Arte"
    elif i == 12:
        tc = T("Il") - 0.3
        sc.add(Chapter("03", "Il muro *vuoto*", a, tc))
        wall = sc.add(Wall((60, 170, 1860, 830), tc + 0.1, gone_t=-9))
        gx, gy, gw, gh, _ = wall.frames[2]; gc = (gx + gw / 2, gy + gh / 2)
        sc.add(Calendar((1620, 330), 200, [(tc, "AGOSTO 1911", "22")], tc + 0.2), "paper")
        sc.add(Figure(walk([(2100, FY), (gc[0] + 260, FY)], T("pittore") - 0.3, 330), T("pittore") - 0.3, kind="painter", carry=[(0, "easel")], label="LOUIS BÉROUD · PITTORE", flip=-1, t1=T("trova") - 0.1))
        sc.add(Pill("4 GANCI DI FERRO", (gc[0], gy + gh + 50), T("quattro"), size=28, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (T("trova") - 0.2, 960, 540, 1.0), (T("trova") + 1.0, gc[0], gc[1] + 30, 2.1), (dur, gc[0], gc[1] + 30, 2.2))
        sc.footer = "Fonti: Quotidiano.net · Slate · Smithsonian Magazine"
    elif i == 13:
        sc.add(Wall((60, 170, 1860, 830), a, gone_t=-9))
        sc.add(Figure([(a, 640, FY)], a, kind="guard"))
        sc.add(Figure([(a, 860, FY)], a + 0.15, kind="guard"))
        sc.add(Bubble((1040, 330), 120, T("pensano"), T("Solo"), inner="camera", text="DAI FOTOGRAFI?"))
        sc.add(ClockFace((1460, 420), 120, T("Solo"), None, start=10, speed=3, label="ORE DI RICERCHE"), "pop")
        sc.add(Stamp("RUBATA", (960, 560), T("rubata"), size=130, rot=-12))
        scene_cam(sc, (0, 960, 540, 1.0), (T("rubata") - 0.1, 960, 540, 1.0), (T("rubata") + 0.3, 960, 560, 1.12), (dur, 960, 560, 1.14))
        sc.footer = "Fonti: Slate · Advance.hr · My Modern Met"
    elif i == 14:
        tchiuso = T("Il") - 0.3; triapre = T("Quando") - 0.3
        np_ = newspaper(600, 640, "PARIGI · 23 AGOSTO 1911", "titolo tradotto", "LA GIOCONDA\nÈ *SCOMPARSA*\nDAL LOUVRE", "titolo ricostruito")
        sc.add(Img(np_, (960, 520), a, tchiuso, anim="drop", rot=-3), "paper")
        spots = [(300, 320), (1620, 330), (260, 760), (1660, 760), (620, 220), (1300, 220)]
        for k, (x, y) in enumerate(spots):
            sc.add(Icon("newspaper", (960, 520), T("giro") + 0.08 * k, tchiuso, size=150, move=(T("giro") + 0.08 * k, 0.7, (x, y), 60), rot=(-12 + 5 * k)), "paper" if k % 2 == 0 else None)
        sc.add(Facade((300, 330, 1500, 770), tchiuso + 0.1, triapre, label="LOUVRE", closed_t=tchiuso + 0.4))
        pages = [(tchiuso + 0.3 + 0.18 * k, "AGOSTO 1911", str(22 + k)) for k in range(8)]
        sc.add(Calendar((1700, 470), 220, pages, tchiuso + 0.2, triapre), "paper")
        sc.add(Wall((60, 170, 1860, 760), triapre + 0.1, gone_t=-9))
        sc.add(Crowd((-500, 760, 700, 900), 16, triapre + 0.2, None, s=0.42, walk=55, stagger=0.06))
        sc.add(Crowd((500, 780, 1500, 900), 14, T("Migliaia"), None, s=0.45, stagger=0.05, seed=9))
        sc.add(Pill("TRA LORO, SECONDO LE CRONACHE: FRANZ KAFKA", (960, 200), T("Kafka") - 0.5, size=36, accent=True))
        sc.footer = "Fonti: Focus · TheCollector · Smithsonian Magazine · Slate"
    elif i == 15:
        tc = T("sulla", 1) - 0.5
        sc.add(Chapter("04", "L'*indagine*", a, tc))
        sc.add(Icon("stairs", (420, 600), tc + 0.1, size=440))
        sc.add(Icon("frame_empty", (430, 600), tc + 0.2, size=170, rot=8), "pop")
        sc.add(Icon("glass", (560, 620), tc + 0.3, size=150, rot=-6), "pop")
        sc.add(Arrow((560, 560), (1150, 480), T("un'impronta"), None, GOLD, 6, 0.5, bend=-0.15, dashed=True))
        sc.add(Fingerprint((1350, 470), 340, T("un'impronta") + 0.3, None, (220, 210, 196)))
        sc.add(Pill("UN'IMPRONTA DEL POLLICE", (1350, 760), T("pollice"), size=36, accent=True))
        sc.add(Figure(walk([(2100, FY), (1750, FY)], T("occuparsene") - 0.3, 420), T("occuparsene") - 0.3, kind="suit", label="A. BERTILLON", flip=-1))
        sc.add(Pill("PIONIERE DELLE SCHEDE SEGNALETICHE", (960, 200), T("pioniere"), size=34))
        sc.footer = "Fonti: Mail & Guardian · NZ Herald · Rallypoint"
    elif i == 16:
        tg = T("Ma") - 0.2
        card = id_card(700, 620, [("NOME", "V. Peruggia"), ("ANNO", "1909"), ("CITTÀ", "Parigi"), ("NOTE", "impronte")])
        sc.add(Img(card, (960, 520), a + 0.1, tg, anim="drop", rot=-2), "paper")
        sc.add(Pill("LE SUE IMPRONTE: GIÀ IN ARCHIVIO", (960, 200), T("archivi") - 0.3, tg, size=38, accent=True))
        sc.add(CardGrid((640, 190, 1820, 820), tg, None, 18, 9, scan=T("Così") - tg))
        sc.add(Pill("ARCHIVIO ORDINATO PER MISURE, NON PER IMPRONTE", (1230, 880 - 20), T("sistema"), T("Così") - 0.2, size=30))
        sc.add(Figure([(tg, 380, FY)], tg + 0.2, kind="suit", carry=[(T("Confrontare"), "magnifier")], arms=[(T("Confrontare"), "point")]))
        sc.add(Text("migliaia di schede,\n*a mano*", (110, 220), T("Confrontare"), size=50, fnt=SERIF))
        sc.add(Stamp("NESSUNA\nCORRISPONDENZA", (1230, 500), T("Così"), size=76, rot=-8))
        sc.footer = "Fonti: CrimeReads · Advance.hr · Rallypoint"
    elif i == 17:
        tp = T("Passano") - 0.3
        sc.add(Figure([(a, 260, FY)], a, tp, kind="police", label="INVESTIGATORI"))
        sc.add(Crowd((600, 700, 1800, 880), 8, a + 0.2, tp, s=0.8, kinds=("worker",), stagger=0.08))
        sc.add(Icon("bed", (1000, 720), tp + 0.1, size=360), "paper")
        sc.add(Trunk((1450, 730), 340, tp + 0.1))
        sc.add(Figure(walk([(-150, FY), (420, FY)], tp, 420), tp, kind="police"))
        sc.add(Figure(walk([(-300, FY), (640, FY)], tp, 480), tp, kind="police"))
        sc.add(Arrow((760, 560), (1330, 600), T("pochi") - 0.2, None, GOLD, 6, 0.5, bend=-0.2, dashed=True))
        sc.add(Pill("A POCHI METRI", (1050, 430), T("pochi"), size=40, accent=True))
        sc.add(Stamp("NON TROVATA", (1450, 700), T("trovano"), size=74, rot=-10))
        scene_cam(sc, (0, 960, 540, 1.0), (T("trovano") - 0.2, 960, 540, 1.0), (T("trovano") + 0.5, 1300, 640, 1.25), (dur, 1320, 640, 1.28))
        sc.footer = "Fonti: Auralcrave · Nation · Smithsonian Magazine · Spokesman-Review"
    elif i == 18:
        nodes = {"g": dict(xy=(1560, 600), name="G. PIERET", role="ladro di statuette", t=T("amico"), rot=2),
                 "a": dict(xy=(960, 600), name="APOLLINAIRE", role="poeta", t=T("arrestato") - 0.2, rot=-2),
                 "c": dict(xy=(360, 600), name="PICASSO", role="pittore", t=T("Picasso") - 0.3, rot=3)}
        sc.board(nodes, [("a", "g", T("amico") + 0.2), ("c", "a", T("Picasso"))], a, cw=240)
        sc.add(Text("I sospetti cadono *su altri*", (960, 170), a, size=64, anchor="ma"))
        sc.add(Icon("handcuffs", (1130, 380), T("arrestato"), T("Entrambi"), size=130), "pop")
        sc.add(Icon("bars", (960, 590), T("carcere"), T("Entrambi"), size=330, anim="fade"), "stamp")
        sc.add(Pill("IN CARCERE ALCUNI GIORNI", (960, 840), T("carcere") + 0.2, T("Entrambi"), size=34))
        sc.add(Icon("magnifier", (560, 380), T("Picasso"), T("Entrambi"), size=110), "pop")
        sc.add(Stamp("ESTRANEI AL FURTO", (960, 840), T("Entrambi"), size=70, rot=-5, color=GOLD))
        sc.footer = "Fonti: Nation · CrimeReads · Rallypoint · History Today · History.com"
    elif i == 19:
        tc = T("Il") - 0.3
        sc.add(Chapter("05", "La *lettera*", a, tc))
        months = ["AGO", "SET", "OTT", "NOV", "DIC", "GEN", "FEB", "MAR", "APR", "MAG", "GIU", "LUG"]
        pages = []
        for k in range(28):
            mi = (7 + k) % 12; yr = 1911 + (7 + k) // 12
            pages.append((tc + 0.2 + k * 0.09, months[mi - 0] if False else months[(k) % 12], str(yr)))
        pages = [(tc + 0.2 + k * 0.09, ["AGO", "SET", "OTT", "NOV", "DIC", "GEN", "FEB", "MAR", "APR", "MAG", "GIU", "LUG"][k % 12], str(1911 + (k + 7) // 12)) for k in range(28)]
        pages.append((T("novembre") - 0.1, "NOVEMBRE", "1913"))
        sc.add(Calendar((470, 470), 300, pages, tc + 0.1), "paper")
        sc.add(Big("28 mesi", (470, 760), tc + 0.3, size=90, fnt=OSW, color=GOLD, count=(0, 28, lambda z: f"{z:.0f} mesi", 2.4)))
        sc.add(Trunk((1350, 690), 440, T("baule") - 0.3, open_t=T("doppio") - 0.2, reveal=T("doppio") + 0.3), "paper")
        sc.add(Icon("envelope", (870, 330), T("mossa") - 0.3, size=170), "pop")
        sc.footer = "Fonti: Finestre sull'Arte · TheCollector · The American"
    elif i == 20:
        sc.add(MapEl((900, 180, 1820, 860), [(0, (7.6, 46.3), 76), (dur, (7.6, 46.3), 84)], a,
                     routes=[dict(pts=["Parigi", "Firenze"], t=T("Scrive") + 0.2, d=2.4, icon="envelope")],
                     pins=[dict(at="Parigi", label="Parigi", t=a + 0.2, side="r"), dict(at="Firenze", label="Alfredo Geri, Firenze", t=T("Geri"), side="l")],
                     title="mappa: Natural Earth"))
        let = doc_typed(640, 520, "LETTERA AD ALFREDO GERI · 24.11.1913",
                        ["Ho la Gioconda.", "Voglio riportarla in Italia,", "meglio agli *Uffizi*.", "", "firmato: «Leonardo V.»"], footer="contenuto riassunto", seed=10, size=32)
        sc.add(Img(let, (460, 520), T("firma") - 0.2, anim="drop", rot=-2), "paper")
        sc.add(Stamp("500.000 LIRE", (500, 760), T("500"), size=70, rot=-7))
        sc.footer = "Fonti: Finestre sull'Arte · History.com · History Hit · The Art Newspaper"
    elif i == 21:
        sc.add(Text("Quanto sono, *oggi*?", (960, 170), a, size=70, anchor="ma"))
        sc.add(Calendar((960, 560), 240, [(a + 0.2, "ANNO", "1913"), (T("ISTAT"), "ANNO", "2023")], a + 0.1, T("500") - 0.2), "paper")
        sc.add(Pill("COEFFICIENTI ISTAT · VALORE DELLA MONETA", (960, 300), T("ISTAT"), size=32))
        for k in range(2):
            sc.add(Icon("money", (430 + k * 170, 560), T("500") + 0.1 * k, size=170), "pop")
        sc.add(Text("500.000 lire · 1913", (515, 690), T("500"), size=48, fnt=OSW, color=WHITE, anchor="ma"))
        sc.add(Arrow((760, 560), (1000, 560), T("valgono"), None, GREY, 8, 0.4))
        for k in range(8):
            sc.add(Icon("money", (1120 + (k % 4) * 150, 480 + (k // 4) * 150), T("2,3") + 0.08 * k, size=150, color=None), "pop" if k % 2 == 0 else None)
        sc.add(Big("2,3 milioni €", (1345, 820), T("2,3"), size=90, color=GOLD, fnt=OSW, count=(0.0, 2.34, lambda z: f"{z:.1f} milioni €".replace(".", ","), 1.0)), "hit")
        sc.footer = "Calcolo: ISTAT, Il valore della moneta in Italia · coeff. 1913-2023 = 9.079,84 · 1 € = 1.936,27 lire · stima indicativa"
    elif i == 22:
        sc.add(Figure([(a, 260, FY)], a, kind="suit", label="A. GERI"))
        sc.add(Figure([(a, 560, FY)], T("Poggi") - 0.3, kind="expert", label="G. POGGI · UFFIZI"), "pop")
        sc.add(Calendar((410, 330), 190, [(T("appuntamento"), "DICEMBRE 1913", "?"), (T("10") - 0.1, "DICEMBRE 1913", "10")], T("appuntamento") - 0.1), "paper")
        sc.add(MapEl((800, 180, 1820, 860), [(0, (7.6, 46.3), 76), (dur, (7.6, 46.3), 84)], a,
                     routes=[dict(pts=["Parigi", "Milano", "Firenze"], t=T("10") + 0.1, d=3.2, icon="train")],
                     pins=[dict(at="Parigi", label="Parigi", t=a + 0.3, side="r"), dict(at="Firenze", label="Hotel Tripoli · Firenze", t=T("all'Hotel"), side="l")],
                     title="mappa: Natural Earth · percorso indicativo"), "whoosh")
        sc.footer = "Fonti: RSI · Michelangelo Buonarroti è tornato · Robert Edsel · Finestre sull'Arte"
    elif i == 23:
        sc.add(Pill("11 DICEMBRE 1913 · HOTEL TRIPOLI, FIRENZE", (960, 180), a, size=36))
        sc.add(Figure([(a, 360, FY)], a, kind="man", label="PERUGGIA"))
        sc.add(Trunk((900, 700), 420, a + 0.1, open_t=T("apre"), reveal=T("Sotto")), "paper")
        sc.add(Figure(walk([(2100, FY), (1350, FY)], T("Poggi") - 0.8, 500), T("Poggi") - 0.8, kind="expert", carry=[(T("esamina"), "magnifier")], arms=[(T("esamina"), "point")], label="POGGI", flip=-1))
        sc.add(Stamp("ORIGINALE", (1180, 290), T("l'originale"), size=64, rot=8, color=GOLD))
        sc.add(Icon("museum", (1700, 380), T("Uffizi") - 0.4, size=220, label="UFFIZI"), "pop")
        sc.add(Img(painting_icon(110), (900, 470), T("scusa") - 0.1, T("Poco") - 0.3, anim="pop", shadow=False))
        sc.add(Figure(walk([(-150, FY), (180, FY)], T("Poco") - 0.6, 450), T("Poco") - 0.6, kind="police"))
        sc.add(Icon("handcuffs", (440, 650), T("arrestato") - 0.2, size=120), "pop")
        sc.add(Stamp("ARRESTATO", (360, 380), T("arrestato") + 0.2, size=84, rot=-8))
        sc.footer = "Fonti: History.com · Robert Edsel · TheCollector · My Modern Met"
    elif i == 24:
        tc = T("Peruggia") - 0.3; tf = T("Fu") - 0.2
        sc.add(Chapter("06", "Il *processo*", a, tc))
        sc.add(Figure([(tc, 380, FY)], tc + 0.1, tf, kind="man", label="PERUGGIA"))
        sc.add(Pill("«L'HO RUBATA PER L'ITALIA»", (960, 200), T("rubata") - 0.2, tf, size=40))
        sc.add(Bubble((800, 430), 150, T("Napoleone") - 0.6, tf, inner="bicorne", text="PORTATA VIA DA NAPOLEONE?"))
        sc.add(Stamp("FALSO", (800, 430), T("così"), tf, size=110, rot=-14))
        sc.add(MapEl((300, 180, 1620, 860), [(0, (7.2, 46.0), 80), (dur, (7.2, 46.0), 86)], tf,
                     routes=[dict(pts=["Firenze", "Milano", "Parigi"], t=T("Leonardo") , d=2.2, icon="painting", color=GOLD)],
                     pins=[dict(at="Firenze", label="Italia", t=tf + 0.2, side="r"), dict(at="Parigi", label="Francia", t=T("Francia"), side="r")],
                     title="percorso indicativo · mappa: Natural Earth"))
        sc.add(Pill("LEONARDO LA PORTA IN FRANCIA", (960, 230), T("Leonardo"), T("passò") - 0.2, size=36))
        sc.add(Icon("crown", (1500, 330), T("Francesco"), size=130, label="RE FRANCESCO I · LEGALMENTE"), "pop")
        sc.footer = "Fonti: Focus · History.com · The American · History Hit"
    elif i == 25:
        sc.add(Pill("TRIBUNALE DI FIRENZE · 4-5 GIUGNO 1914", (960, 180), a, size=36))
        sc.add(Figure([(a, 640, 640)], a, kind="judge", s=0.9))
        sc.add(Icon("bench", (640, 700), a, size=380, anim="fade"))
        sc.add(Figure([(a, 200, FY)], a + 0.2, kind="man", label="PERUGGIA"))
        sc.add(Icon("gavel", (880, 470), T("condannato"), size=150, anim="shake"), "stamp")
        sc.add(Text("1 anno e 15 giorni", (1150, 300), T("anno"), size=50, fnt=OSW, color=WHITE))
        sc.add(Bar(1150, 380, 640, 54, [(T("anno"), 1.0), (T("sette"), 218 / 380)], T("anno")))
        sc.add(Text("in appello (29 luglio): *7 mesi e 8 giorni*", (1150, 470), T("sette") - 0.2, size=40, fnt=PS, color=WHITE, maxw=700))
        sc.add(Crowd((1150, 620, 1800, 880), 10, T("Gran"), None, s=0.42, stagger=0.05))
        sc.add(Pill("OPINIONE PUBBLICA: DALLA SUA PARTE", (1470, 580), T("Gran") + 0.3, size=30, accent=True))
        sc.footer = "Fonti: Focus · Studio Cataldi (sentenze) · Quotidiano.net · Michelangelo Buonarroti è tornato"
    elif i == 26:
        tc = T("Prima") - 0.3
        sc.add(Chapter("07", "Come *finì*", a, tc))
        sc.add(MapEl((760, 180, 1820, 860), [(0, (11.2, 43.6), 95), (T("torna", 1) - 0.4, (11.2, 43.6), 95), (T("torna", 1) + 1.6, (7.2, 46.6), 64), (dur, (7.2, 46.6), 64)], tc + 0.1,
                     routes=[dict(pts=["Firenze", "Roma"], t=T("Roma"), d=0.9, icon="painting"), dict(pts=["Roma", "Milano"], t=T("Milano"), d=1.0, icon="painting"),
                             dict(pts=["Milano", "Parigi"], t=T("torna", 1) + 0.4, d=1.6, color=GOLD, icon="painting")],
                     pins=[dict(at="Firenze", label="Uffizi", t=T("Uffizi"), side="r"), dict(at="Roma", label="Roma", t=T("Roma"), side="r"),
                           dict(at="Milano", label="Milano", t=T("Milano"), side="l"), dict(at="Parigi", label="Louvre", t=T("Louvre"), side="r")],
                     title="mappa: Natural Earth · percorso indicativo"))
        sc.add(Crowd((80, 400, 700, 880), 12, T("folle"), T("4") - 0.2, s=0.45, stagger=0.05))
        sc.add(Calendar((400, 430), 220, [(T("4"), "GENNAIO 1914", "4")], T("4") - 0.1, T("Nei") - 0.2), "paper")
        sc.add(Crowd((80, 380, 700, 880), 30, T("Nei"), None, s=0.36, stagger=0.03, seed=11))
        sc.add(Pill("100.000+ IN 2 GIORNI", (390, 300), T("centomila"), size=44, accent=True), "hit")
        sc.footer = "Fonti: Quotidiano.net · Smithsonian Magazine · History.com · History Hit"
    elif i == 27:
        tl_ = T("Gioconda") - 0.3
        sc.add(Figure([(a, 760, FY)], a, tl_, kind="man", label="V. PERUGGIA"))
        sc.add(Calendar((1180, 470), 220, [(T("1925"), "MUORE NEL", "1925")], T("1925") - 0.1, tl_), "paper")
        sc.add(Pill("44 ANNI · IN FRANCIA", (1180, 700), T("44"), tl_, size=36))
        sc.add(Img(painting_icon(220), (960, 500), tl_ + 0.1, anim="pop", shadow=True))
        spots = [(420, 280), (1500, 280), (330, 640), (1590, 640), (640, 820), (1280, 820), (960, 190)]
        for k, (x, y) in enumerate(spots):
            sc.add(Icon("newspaper", (x + (960 - x) * 0.3, y + (500 - y) * 0.3), T("giornali") + 0.1 * k, size=140, rot=-15 + 5 * k), "paper" if k % 2 else None)
        sc.add(Pill("IL QUADRO PIÙ FAMOSO DEL PIANETA", (960, 840), T("Ed"), size=40, accent=True), "hit")
        scene_cam(sc, (0, 960, 540, 1.0), (tl_, 960, 540, 1.0), (dur, 960, 520, 1.12))
        sc.footer = "Fonti: Focus · The Walk of Fame · Smithsonian Magazine"
    elif i == 28:
        sc.add(Chapter("", "Il *verdetto*", a, T("Un") - 0.3))
        rows = [("Armi e violenza", "nessuna", T("Un"), "smock"), ("Per uscire", "un idraulico gentile", T("camice"), "pliers"),
                ("L'impronta", "mai collegata", T("Un'impronta"), "magnifier"), ("L'errore", "vendere il quadro", T("errore"), "envelope")]
        sc.add(Rows([dict(label=l, value=v, t=t, color=(REDL if k == 3 else GOLD)) for k, (l, v, t, _) in enumerate(rows)], T("Un") - 0.2, x0=420, x1=1700, y=320, gap=140, size=48))
        for k, (l, v, t, ic) in enumerate(rows):
            sc.add(Icon(ic, (300, 320 + k * 140), t, size=100), "pop")
        sc.footer = F_BASE
    elif i == 29:
        sc.add(Text("Ladro o *patriota*?", (960, 200), T("Vincenzo"), size=110, anchor="ma"))
        sc.add(Icon("handcuffs", (620, 520), T("ladro"), size=200, label="LADRO"), "pop")
        sc.add(Icon("crown", (1300, 520), T("patriota"), size=200, label="PATRIOTA"), "pop")
        sc.add(Text("Scrivilo nei commenti", (960, 700), T("Scrivilo"), size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(100), (960, 830), T("Iscriviti"), anim="pop", shadow=False), "hit")
        sc.footer = "Tutte le fonti nella descrizione · ricostruzione a scopo divulgativo"
    return sc

def thumbnail(path="thumbnail.jpg"):
    im = make_bg(7); d = ImageDraw.Draw(im)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    Frame((1500, 470), 330, 480, -10, None, vanish=-10).draw(lay, 0, 1.0)
    draw_person(lay, 1250, 1000, 1.25, "worker", 0.8, True, "hidden")
    im.alpha_composite(lay)
    t = rich_img("L'ITALIANO\nCHE RUBÒ\nLA *GIOCONDA*", SERIF, 150, WHITE, RED, lh=1.0)
    im.alpha_composite(t, (90, 150))
    st = stamp_img("CASO 001", RED, 70, -10); im.alpha_composite(st, (1520, 90))
    d.text((100, 840), "USCITO DAL LOUVRE CON UN AIUTO INSOSPETTABILE", font=font(OSW, 48, 600), fill=GOLD + (255,))
    wm = wordmark(60, sub=False); im.alpha_composite(wm, (100, 960))
    im.convert("RGB").save(path, quality=92)
