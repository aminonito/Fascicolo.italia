import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from urb import *

W, H = 1920, 1080
FY = 870
PB = (260, 160, 1660, 880)      # scenografia esterna: il palazzo
SB = (200, 165, 1720, 875)      # scenografia interna: la sala con i tre dipinti
MAPB = (160, 160, 1760, 880)
MT = "mappa: Natural Earth · schema non in scala"
F_OPERE = "Fonti: Wikipedia (La Muta) · Finestre sull'Arte · ANSA · Il Giornale dell'Arte"
F_NOTTE = "Fonti: ANSA · Il Giornale dell'Arte · San Marino RTV · Prima Bergamo · Affaritaliani"
F_TEL = "Fonti: ANSA · Prima Bergamo · Il Giornale dell'Arte · San Marino RTV"
F_VEL = "Fonti: San Marino RTV · Affaritaliani · archeosardegna"
F_TRAT = "Fonti: San Marino RTV · archeosardegna · Affaritaliani · Rotary Rimini"
F_LOC = "Fonti: ANSA · Prima Bergamo · Il Giornale dell'Arte · San Marino RTV · Wikipedia (La Muta)"

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

def build(i, dur, a, words):
    T0 = Clock(words, a)
    def T(p, n=0):
        try: return T0(p, n)
        except KeyError: return a + 0.5
    sc = Scene(dur)
    if i == 0:
        tn = T("C'è") - 0.3; ti = T("Il") - 0.3; tp = T("In") - 0.3; td = T("due") - 0.2; tr = T("e", 2) - 0.1
        sc.add(MapEl(MAPB, [(a, (12.0, 42.5), 160), (tn - 0.4, "Urbino", 380)], a, tn + 0.2,
                     pins=[dict(at="Urbino", label="URBINO", t=a + 0.4, side="r", color=RED)], title=MT))
        sc.add(Calendar((360, 420), 220, [(a + 0.9, "URBINO", "FEB"), (a + 1.6, "FEBBRAIO", "1975")], a + 0.9, tn + 0.2), "paper")
        sc.add(Palazzo(PB, tn, tp + 0.2, night=True, fog=True, scaf_t=T("impalcature") - 0.4), "whoosh")
        sc.add(Pill("C'È LA NEBBIA", (960, 210), tn + 0.2, ti, size=46, accent=True))
        sc.add(Pill("LAVORI IN CORSO: IMPALCATURE", (960, 210), T("impalcature") - 0.3, tp, size=46, accent=True))
        sc.add(Sala(SB, tp, None, gone={0: tp + 0.6, 1: tp + 1.0, 2: tp + 1.4}, night=True, torch=tp), "whoosh")
        sc.add(Pill("2 × PIERO DELLA FRANCESCA", (700, 230), td, size=40, accent=True))
        sc.add(Pill("1 × RAFFAELLO", (1300, 230), tr, size=40, accent=True))
        sc.footer = F_NOTTE + " · schema non in scala"
    elif i == 1:
        tl_ = T("le") - 0.3; tg = T("perfino") - 0.3; te = T("Eppure") - 0.3
        sc.add(Icon("art_flag", (600, 470), a, te, size=360), "pop")
        sc.add(Text("Flagellazione · Piero della Francesca", (600, 700), a + 0.3, te, size=30, fnt=OSW, color=GOLD, anchor="ma"))
        sc.add(Icon("nuke", (1320, 470), tl_, te, size=320, label="30 OPERE DA SALVARE"), "pop")
        sc.add(Arrow((850, 470), (1140, 470), tl_ + 0.3, te, color=GOLD))
        sc.add(Pill("ANCHE IN CASO DI GUERRA NUCLEARE", (960, 220), tg, te, size=46, accent=True))
        sc.add(Icon("museum", (700, 470), te, size=300, label="IL MUSEO"), "pop")
        sc.add(Icon("alarm_off", (1240, 470), te + 0.5, size=300), "pop")
        sc.add(Stamp("NESSUN\nALLARME", (1240, 720), T("allarme") - 0.1, size=72, rot=-8))
        sc.footer = "Fonti: ANSA · Prima Bergamo · schema non in scala"
    elif i == 2:
        tq = T("Questo") - 0.3; tv = T("Vedremo") - 0.3
        sc.add(Img(newspaper(640, 500, "CRONACA", "7 febbraio 1975", "IL FURTO DEL SECOLO", "Tre capolavori spariti da Urbino"), (960, 520), a, tq, anim="drop", rot=-3), "paper")
        sc.add(Text("giornale ricostruito · testata generica", (960, 820), a + 0.3, tq, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Img(cover_folder(), (960, 500), tq + 0.1, tv, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 011", (1150, 300), T("fascicolo") + 0.2, tv, size=70, rot=-12))
        sc.add(Icon("scaffold", (360, 470), tv + 0.1, size=200, label="COME SONO ENTRATI"), "pop")
        sc.add(Icon("ear", (760, 470), T("telefonate") - 0.3, size=200, label="LE TELEFONATE"), "pop")
        sc.add(Icon("velvet", (1160, 470), T("velluto") - 0.3, size=200, label="IL VELLUTO"), "pop")
        sc.add(Icon("hotel", (1560, 470), T("camera") - 0.3, size=200, label="UN ALBERGO IN SVIZZERA"), "pop")
        sc.footer = "Fonti: ANSA · Il Giornale dell'Arte · Prima Bergamo · archeosardegna"
    elif i == 3:
        tc = T("Sono") - 0.6; td = T("dentro") - 0.3; tr = T("la", 1) - 0.3
        sc.add(Chapter("01", "I tre *capolavori*", a, tc))
        sc.add(MapEl(MAPB, [(tc, (12.2, 42.6), 170), (td, "Urbino", 300)], tc, td + 0.3,
                     pins=[dict(at="Urbino", label="URBINO", t=tc + 0.3, side="r", color=RED)], title=MT))
        sc.add(Icon("museum", (600, 400), tc + 0.6, td + 0.3, size=240, label="GALLERIA NAZIONALE DELLE MARCHE"), "pop")
        sc.add(Palazzo(PB, td, None), "whoosh")
        sc.add(Pill("IL PALAZZO DUCALE", (960, 220), td + 0.3, tr, size=46, accent=True))
        sc.add(Pill("RINASCIMENTO · FEDERICO DA MONTEFELTRO", (960, 220), tr, size=44, accent=True))
        sc.footer = "Fonti: ANSA · Affaritaliani · Il Giornale dell'Arte · schema non in scala"
    elif i == 4:
        tu = T("Una") - 0.3; tm = T("e", 1) - 0.3
        sc.add(Img(framed("flag", 380), (620, 470), a, anim="drop"), "paper")
        sc.add(Text("sagoma stilizzata, non l'opera", (620, 720), a + 0.3, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Img(label_card(["Piero della Francesca", "Flagellazione di Cristo", "tempera su tavola"], 560, title="SCHEDA DELL'OPERA"), (1340, 400), a + 0.4, tm, anim="drop", rot=2), "paper")
        sc.add(Pill("PICCOLA TAVOLA", (1340, 660), tu, tm, size=44, accent=True))
        for k in range(4):
            sc.add(Arrow((1040, 300 + k * 60), (700, 520), T("prospettiva") + 0.12 * k, tm, color=GOLD, width=5, dashed=True))
        sc.add(Pill("PROSPETTIVA", (960, 220), T("prospettiva") - 0.2, tm, size=46, accent=True))
        sc.add(Icon("magnifier", (1340, 450), tm, size=240), "pop")
        sc.add(Icon("question", (1500, 380), tm + 0.4, size=150), "pop")
        sc.add(Pill("MISTERI ANCORA DISCUSSI", (1380, 660), tm + 0.3, size=44, accent=True))
        sc.footer = F_OPERE
    elif i == 5:
        tt = T("La", 1) - 0.3; tr = T("Raffaello", 1) - 0.4
        sc.add(Img(framed("madonna", 400), (560, 470), a, anim="drop"), "paper")
        sc.add(Pill("PIERO · MADONNA DI SENIGALLIA", (560, 760), a + 0.4, size=38, accent=True))
        sc.add(Img(framed("muta", 400), (1360, 470), tt, anim="drop"), "paper")
        sc.add(Pill("RAFFAELLO · LA MUTA", (1360, 760), tt + 0.3, size=38, accent=True))
        sc.add(Text("sagome stilizzate, non le opere", (960, 830), a + 0.3, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Icon("house", (960, 420), tr, size=200, label="NATO A URBINO"), "pop")
        sc.footer = F_OPERE
    elif i == 6:
        tp = T("Piccoli") - 0.3; tpb = T("Per") - 0.3
        xs = (480, 960, 1440)
        for k, (kind, wcm, hcm, lab) in enumerate(ART):
            ph = int(300 * hcm / 64); fr = framed(kind, ph)
            sc.add(Img(fr, (xs[k], FY - fr.height / 2 - 40), a + 0.3 * k, anim="drop", shadow=True), "paper" if k == 0 else None)
        sc.add(Figure([(0, 1700, FY - 40)], a + 0.6, kind="man", s=0.75), "pop")
        sc.add(Pill("1,75 m", (1700, 400), a + 0.8, size=30))
        sc.add(Pill("NESSUNO SUPERA IL METRO", (960, 220), T("nessuno") - 0.2, tp, size=46, accent=True))
        sc.add(Pill("PICCOLI", (480, 220), tp, tpb, size=46))
        sc.add(Pill("LEGGERI", (960, 220), T("leggeri") - 0.2, tpb, size=46))
        sc.add(Pill("VALORE INESTIMABILE", (1440, 220), T("valore") - 0.2, tpb, size=46, accent=True))
        sc.add(Stamp("IL BOTTINO\nPERFETTO", (960, 380), T("bottino") - 0.2, size=76, rot=-7))
        sc.add(Text("proporzioni indicative · sagome stilizzate", (960, 290), a + 0.5, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = F_OPERE + " · schema non in scala"
    elif i == 7:
        ttr = T("Trent'anni") - 0.3; tps = T("il") - 0.3; tn = T("nascondendole") - 0.3; tl_ = T("Le") - 0.3
        sc.add(Text("Un dettaglio\nquasi *ironico*", (960, 400), a, ttr, size=100, anchor="ma", align="m"))
        sc.add(Calendar((330, 420), 200, [(ttr, "GUERRA", "1940-45")], ttr, tl_), "paper")
        sc.add(Img(person_card("PASQUALE ROTONDI", "soprintendente"), (330, 470), tps, tn, anim="drop"), "paper")
        sc.add(MapEl((560, 170, 1760, 870), [(tps, (12.6, 43.75), 1500), (dur, (12.6, 43.75), 1600)], tps,
                     pins=[dict(at="Urbino", label="URBINO", t=tps + 0.2, side="r", color=GOLD),
                           dict(at="Sassocorvaro", label="SASSOCORVARO", t=tn, side="l", color=RED)],
                     routes=[dict(pts=["Urbino", "Sassocorvaro"], t=tn + 0.2, d=1.4, icon="painting", color=GOLD)], title=MT))
        sc.add(Icon("rocca", (1460, 330), tn + 0.4, tl_, size=170, label="LA ROCCA"), "pop")
        sc.add(Stamp("SALVATE\nDALLA GUERRA", (1160, 640), tl_, size=74, rot=-6))
        sc.footer = "Fonti: ANSA · Finestre sull'Arte · Ministero della Cultura · " + MT
    elif i == 8:
        tc = T("Sul") - 0.6; tu = T("Una") - 0.3
        sc.add(Chapter("02", "La notte della *nebbia*", a, tc))
        sc.add(Calendar((330, 420), 220, [(tc, "FEBBRAIO 1975", "5"), (tc + 0.8, "FEBBRAIO 1975", "6")], tc, None), "paper")
        sc.add(Palazzo((560, 170, 1760, 870), tc, None, night=True, fog=True, scaf_t=T("un'impalcatura") - 0.3), "whoosh")
        sc.add(Pill("LAVORI IN CORSO", (1160, 220), T("lavori") - 0.2, T("un'impalcatura") - 0.2, size=44, accent=True))
        sc.add(Pill("IMPALCATURA DI TUBI", (1160, 220), T("un'impalcatura") - 0.2, size=44, accent=True))
        sc.add(Arrow((900, 820), (900, 420), T("sale") - 0.2, color=GOLD, width=10))
        sc.footer = F_NOTTE + " · schema non in scala"
    elif i == 9:
        tm = T("Ma") - 0.3; tg = T("Di", 1) - 0.3; tn = T("E", 1) - 0.3
        sc.add(Icon("fortress", (960, 440), a, tm, size=320), "pop")
        sc.add(Pill("«UNA FORTEZZA INESPUGNABILE»", (960, 720), T("fortezza") - 0.3, tm, size=50, accent=True))
        sc.add(Icon("moon", (520, 360), tm, tn, size=150), "pop")
        sc.add(Big("2", (520, 560), T("soltanto") - 0.3, tn, size=200, color=GOLD, fnt=OSW, sub="guardiani di notte"), "hit")
        sc.add(Icon("sun", (1400, 360), tg, tn, size=150), "pop")
        sc.add(Big("22", (1400, 560), tg + 0.2, tn, size=200, color=WHITE, fnt=OSW, sub="di giorno"), "hit")
        sc.add(Text("secondo le ricostruzioni", (960, 820), tm + 0.4, tn, size=28, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Icon("alarm_off", (960, 450), tn, size=300), "pop")
        sc.add(Stamp("NESSUN\nALLARME", (960, 720), tn + 0.4, size=80, rot=-8))
        sc.footer = "Fonti: Il Giornale dell'Arte · archeosardegna · ANSA · Prima Bergamo"
    elif i == 10:
        tc = T("C'è") ; ti = T("guardiani") - 0.5; td = T("Due") - 0.3
        s_ = Sala(SB, a, td, night=True, torch=T("torce") - 0.4)
        sc.add(s_, "whoosh")
        sc.add(Pill("ELETTRICITÀ SPENTA NELLE SALE", (960, 220), T("l'elettricità") - 0.4, ti, size=44, accent=True))
        sc.add(Text("secondo le ricostruzioni", (960, 290), T("l'elettricità") - 0.2, ti, size=28, fnt=COURR, color=GREY, anchor="ma"))
        fy = s_.floor_y()
        sc.add(Figure(walk([(-80, fy), (1900, fy)], T("torce") - 0.4, 260), T("torce") - 0.4, td, kind="guard", s=0.7), "pop")
        sc.add(Pill("UN GIRO OGNI DUE ORE", (960, 220), ti, td, size=46, accent=True))
        sc.add(ClockFace((1560, 330), 110, ti, td, start=0.0, speed=0.6, label="GIRO"))
        sc.add(ClockFace((700, 470), 170, td, start=0.5, speed=0.5, label="BUIO"))
        sc.add(Big("2 ore", (1260, 420), td + 0.2, size=180, color=GOLD, fnt=OSW, sub="tra un passaggio e l'altro"), "hit")
        sc.footer = "Fonti: archeosardegna · Rotary Rimini (N. Monaco) · schema non in scala"
    elif i == 11:
        tu = T("Usano") - 0.3; ts = T("Salgono") - 0.3; te = T("e", 0) - 0.3
        PB2 = (380, 200, 1540, 820)
        p = sc.add(Palazzo(PB2, a, None, night=True, fog=True, scaf_t=a - 5, lights=[(ts + 1.4, (.30, .33))]))
        x0 = PB2[0]; gy = PB2[1] + (PB2[3] - PB2[1]) * .88
        for k in range(2):
            pts = [(x0 + 30 - 60 * k, gy), (x0 + 210 - 34 * k, gy), (x0 + 240 - 34 * k, PB2[1] + 270), (x0 + 350 - 34 * k, PB2[1] + 250)]
            sc.add(Figure(walk(pts, tu + 0.2 * k, 150), a + 0.2 * k, kind="worker", s=0.55), "pop" if k == 0 else None)
        sc.add(Pill("ALMENO DUE", (960, 210), a + 0.3, tu, size=46, accent=True))
        sc.add(Pill("L'IMPALCATURA COME SCALA", (960, 210), tu, ts, size=46, accent=True))
        sc.add(Pill("FINO AL GIARDINO PENSILE", (960, 210), ts, te + 0.6, size=46, accent=True))
        sc.add(Pill("POI LE SALE DEI QUADRI", (960, 210), T("raggiungono") - 0.2, size=46, accent=True))
        scene_cam(sc, (a, 960, 520, 1.0), (ts, 860, 520, 1.1), (dur, 820, 520, 1.12))
        sc.footer = F_NOTTE + " · schema non in scala"
    elif i == 12:
        ti = T("I") - 0.3; tp = T("Poi") - 0.3
        s_ = Sala(SB, a, None, gone={2: T("uno") - 0.1, 1: T("dopo") - 0.1, 0: T("dopo") + 0.5}, night=True, torch=a, window_t=a)
        sc.add(s_, "whoosh")
        sc.add(ClockFace((1560, 300), 110, a + 0.3, ti + 0.3, start=0.5, speed=0.5, label="NOTTE"))
        sc.add(Pill("TRA 00:30 E 02:30", (960, 220), T("mezzanotte") - 0.2, ti, size=46, accent=True))
        sc.add(Text("secondo diverse ricostruzioni", (960, 290), T("mezzanotte"), ti, size=28, fnt=COURR, color=GREY, anchor="ma"))
        fy = s_.floor_y()
        for k in range(2):
            sc.add(Figure(walk([(1800 - 60 * k, fy), (1300 - 100 * k, fy)], a + 0.4 * k, 240) +
                          [(tp + 0.3, 1300 - 100 * k, fy), (tp + 3.5, 1850, fy)], a + 0.2, kind="worker", s=0.7,
                          carry=[(ti + 1.2, "painting")], flip=-1), "pop" if k == 0 else None)
        sc.add(Pill("STACCATI UNO DOPO L'ALTRO", (960, 220), ti, tp, size=46, accent=True))
        sc.add(Pill("SPARITI NELLA NEBBIA", (960, 220), tp, size=46, accent=True))
        sc.footer = F_NOTTE + " · ricostruzione grafica"
    elif i == 13:
        tl_ = T("La") - 0.3; tm = T("Il") - 0.3; tmi = T("Nei") - 0.3
        sc.add(Sala(SB, a, tl_ + 0.2, gone={0: a - 5, 1: a - 5, 2: a - 5}, hl=(1, a + 0.6)))
        sc.add(Pill("TRE SPAZI VUOTI", (960, 220), a + 0.3, tl_, size=46, accent=True))
        sc.add(Icon("newspaper", (500, 450), tl_, tm, size=240), "pop")
        sc.add(Icon("flagless_globe", (960, 450), T("mondo") - 0.3, tm, size=240, label="IL MONDO"), "pop")
        sc.add(Icon("ministry", (700, 450), tm, size=260, label="BENI CULTURALI"), "pop")
        sc.add(Pill("MINISTERO NATO DA POCHE SETTIMANE", (960, 220), tm + 0.4, size=46, accent=True))
        sc.add(Figure(walk([(1900, FY), (1300, FY)], tmi, 300), tmi, kind="suit", s=0.85, label="IL MINISTRO SPADOLINI", flip=-1))
        sc.footer = "Fonti: ANSA · Prima Bergamo · schema non in scala"
    elif i == 14:
        tt = T("trattate") - 0.3; tn = T("Non") - 0.3; tr = T("Ricordiamoci") - 0.3
        sc.add(Icon("megaphone", (480, 470), a, tr, size=260, label="APPELLO AI LADRI"), "pop")
        sc.add(Pill("TRATTATE LE OPERE CON DELICATEZZA", (1160, 330), tt, tr, size=42, accent=True))
        sc.add(Pill("NON TOCCATELE CON LE MANI", (1160, 450), tn, tr, size=42))
        sc.add(Pill("AVVOLGETELE NEL VELLUTO", (1160, 570), T("avvolgetele") - 0.2, tr, size=42, accent=True))
        sc.add(Icon("velvet", (960, 430), tr, size=340), "pop")
        sc.add(Text("VELLUTO", (960, 660), T("velluto", 1) - 0.2, size=110, fnt=OSW, color=GOLD, anchor="ma"))
        scene_cam(sc, (tr, 960, 520, 1.0), (dur, 960, 500, 1.15))
        sc.footer = "Fonti: San Marino RTV · Affaritaliani · Il Giornale dell'Arte"
    elif i == 15:
        tc = T("il") - 0.6; ta = T("Arrivano") - 0.3; tm = T("Molte") - 0.3
        sc.add(Chapter("03", "Le *telefonate*", a, tc))
        sc.add(Icon("ear", (960, 440), tc, ta + 0.3, size=320), "pop")
        for k in range(8):
            x = 300 + (k % 4) * 440; y = 340 if k < 4 else 600
            sc.add(Icon("ear", (x, y), ta + 0.15 * k, tm + 0.6, size=150), "pop" if k == 0 else None)
        sc.add(Pill("DECINE DI RIVENDICAZIONI", (960, 220), ta + 0.2, size=46, accent=True))
        sc.add(Stamp("MITOMANI", (620, 470), T("mitomani") - 0.1, size=80, rot=-8))
        sc.add(Stamp("TRUFFATORI", (1300, 470), T("truffatori") - 0.1, size=80, rot=6))
        sc.add(Text("quadri mai visti", (960, 720), T("quadri") - 0.2, size=60, fnt=SERIF, color=GOLD, anchor="ma"))
        sc.footer = F_TEL
    elif i == 16:
        tl_ = T("La") - 0.3; tt = T("Tre") - 0.3
        sc.add(Icon("ear", (400, 450), a, tt, size=220, label="TELEFONATA ANONIMA"), "pop")
        sc.add(Icon("museum", (900, 450), a + 0.6, tt, size=240, label="ACCADEMIA DI BELLE ARTI"), "pop")
        sc.add(Arrow((540, 450), (760, 450), a + 0.5, tt, color=GOLD, dashed=True))
        sc.add(Big("1 miliardo", (1430, 430), T("un") - 0.2, tt, size=120, color=GOLD, fnt=OSW, sub="di lire per ogni quadro"), "hit")
        for k, (kind, _, _, _) in enumerate(ART):
            x = 480 + k * 480
            sc.add(Icon("art_" + kind, (x, 420), tt + 0.25 * k, T("Con") - 0.3, size=230), "pop")
            sc.add(Pill("1 MILIARDO", (x, 620), tt + 0.25 * k + 0.2, T("Con") - 0.3, size=36))
        tco = T("Con") - 0.3
        sc.add(Big("= 3 miliardi", (960, 780), T("tre", 1) - 0.2, tco, size=90, color=RED, fnt=OSW), "hit")
        sc.add(Big("> 6 mln €", (960, 470), tco + 0.2, size=200, color=GOLD, fnt=OSW, sub="oggi, per ogni quadro · stima"), "hit")
        sc.add(Text("coefficienti ISTAT · valore della moneta 1975-2024\n1 mld × 12,28 / 1936,27 ≈ 6,3 mln €", (960, 700), tco + 0.5, size=28, fnt=COURR, color=GREY, anchor="ma", align="m"))
        sc.footer = F_TEL + " · ISTAT"
    elif i == 17:
        tq = T("Questa") - 0.3; tb = T("in") - 0.3; tm = T("Ma") - 0.3
        sc.add(Figure([(0, 420, FY)], a, tm, kind="suit", s=0.9, label="IL SINDACO DI URBINO"), "pop")
        sc.add(Icon("ear", (820, 420), a + 0.3, tm, size=180), "pop")
        sc.add(Big("100 milioni", (1300, 400), T("cento") - 0.2, tm, size=130, color=GOLD, fnt=OSW, sub="di lire",
                   count=(0, 100, lambda z: f"{z:.0f} milioni", 1.2)), "hit")
        sc.add(Icon("lire", (1300, 640), tb, tm, size=200), "pop")
        sc.add(Pill("BANCONOTE DA 10.000 · USATE", (1300, 790), tb + 0.2, tm, size=40, accent=True))
        sc.add(Icon("ear", (960, 450), tm, size=240), "pop")
        sc.add(Stamp("NESSUNA PISTA", (960, 650), tm + 0.6, size=80, rot=-8))
        sc.footer = F_TEL
    elif i == 18:
        te = T("E") - 0.3; tr = T("un") - 0.3
        sc.add(Img(person_card("RODOLFO SIVIERO", "recupero opere d'arte"), (560, 480), a, te + 0.5, anim="drop"), "paper")
        sc.add(Pill("INCARICATO DAL GOVERNO", (1200, 360), T("l'uomo") - 0.2, te + 0.5, size=44, accent=True))
        sc.add(Icon("art_muta", (1200, 560), T("recuperare") - 0.3, te + 0.5, size=200), "pop")
        sc.add(Arrow((1050, 560), (900, 560), T("recuperare"), te + 0.5, color=GOLD))
        for k in range(3):
            sc.add(Figure(walk([(-100 - 120 * k, FY), (620 + 160 * k, FY)], te + 0.2 * k, 380), te + 0.2 * k, kind="police", s=0.85), "pop" if k == 0 else None)
        sc.add(Icon("shield_ok", (1360, 450), te + 0.6, size=240, label="NUCLEO TUTELA PATRIMONIO ARTISTICO"), "pop")
        sc.add(Pill("UN REPARTO NATO DA POCHI ANNI", (960, 220), tr, size=46, accent=True))
        sc.footer = "Fonti: Il Giornale dell'Arte · archeosardegna · San Marino RTV"
    elif i == 19:
        tc = T("Arriva") - 0.6; tp = T("Poche") - 0.3; tr = T("una") - 0.3
        sc.add(Chapter("04", "Il *velluto*", a, tc))
        sc.add(Icon("ear", (560, 450), tc, tp, size=240), "pop")
        sc.add(Stamp("NO", (560, 450), tc + 0.3, tp, size=100, rot=-10))
        sc.add(Icon("shop", (1300, 450), T("negozio") - 0.3, size=300, label="NEGOZIO DI STOFFE"), "pop")
        sc.add(Pill("POCHE ORE DOPO IL FURTO · PESARO", (960, 220), tp, size=46, accent=True))
        sc.add(Icon("velvet", (560, 470), tr, size=280, label="TANTO VELLUTO"), "pop")
        sc.add(Arrow((1120, 470), (740, 470), tr + 0.3, color=GOLD))
        sc.footer = F_VEL
    elif i == 20:
        tm = T("Ma") - 0.3; ti = T("In") - 0.3
        sc.add(Icon("velvet", (520, 450), a, size=260), "pop")
        sc.add(Pill("PER IL FIDANZATO", (520, 680), a + 0.3, size=40, accent=True))
        sc.add(Icon("question", (960, 450), tm, size=180), "pop")
        sc.add(Icon("megaphone", (1400, 450), ti, size=240), "pop")
        sc.add(Pill("«AVVOLGETELI NEL VELLUTO»", (1400, 680), T("avvolgete") - 0.2, size=40, accent=True))
        sc.add(Text("=", (960, 600), T("avvolgete"), size=120, fnt=OSW, color=RED, anchor="ma"))
        sc.footer = F_VEL
    elif i == 21:
        te = T("E") - 0.3; tl_ = T("È") - 0.3; tp = T("Per") - 0.3
        sc.add(Figure([(0, 300, FY)], a, kind="man", s=0.8, label="LA RAGAZZA"), "pop")
        sc.add(Figure([(0, 620, FY)], T("madre") - 0.3, kind="man", s=0.8, label="LA MADRE"), "pop")
        sc.add(Arrow((360, 600), (560, 600), T("madre") - 0.1, color=GOLD))
        sc.add(Figure([(0, 1000, FY)], T("un") - 0.2, kind="police", s=0.8, label="EX MARESCIALLO"), "pop")
        sc.add(Arrow((680, 600), (940, 600), T("amico") - 0.2, color=GOLD))
        for k in range(3):
            sc.add(Figure([(0, 1380 + k * 140, FY)], tl_ + 0.2 * k, kind="police", s=0.8), "pop" if k == 0 else None)
        sc.add(Arrow((1060, 600), (1320, 600), tl_ + 0.2, color=GOLD))
        sc.add(Pill("I CARABINIERI", (1520, 300), tl_ + 0.5, size=40))
        sc.add(Stamp("LA PISTA\nGIUSTA", (960, 330), tp, size=80, rot=-7))
        sc.footer = F_VEL + " · ricostruzione grafica"
    elif i == 22:
        tc = T("Quei") - 0.6; to = T("Ogni") - 0.3; tr = T("Rubarli") - 0.3
        sc.add(Chapter("05", "La *trattativa*", a, tc))
        for k, (kind, _, _, _) in enumerate(ART):
            sc.add(Icon("art_" + kind, (560 + k * 400, 400), tc + 0.2 * k, tr, size=240), "pop" if k == 0 else None)
        sc.add(Pill("TROPPO FAMOSI", (960, 220), tc + 0.5, tr, size=48, accent=True))
        sc.add(Crowd((300, 600, 1620, 870), 12, to, tr, s=0.32, kinds=("suit", "expert", "police", "man")))
        sc.add(Icon("scaffold", (600, 450), tr, size=220, label="RUBARLI: FACILE"), "pop")
        sc.add(Icon("crash", (1320, 450), T("Venderli") - 0.2, size=220, label="VENDERLI"), "pop")
        sc.add(Stamp("IMPOSSIBILE", (1320, 700), T("impossibile") - 0.1, size=80, rot=-8))
        sc.footer = F_TRAT
    elif i == 23:
        tl_ = T("La") - 0.3; tc = T("Con") - 0.3
        sc.add(Text("secondo le ricostruzioni", (960, 200), a, tl_, size=34, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Icon("ear", (960, 450), a + 0.2, tl_, size=260, label="IL RISCATTO"), "pop")
        sc.add(Big("250 milioni", (620, 430), tl_ + 0.3, size=130, color=GOLD, fnt=OSW, sub="di lire · 1976",
                   count=(0, 250, lambda z: f"{z:.0f} milioni", 1.4)), "hit")
        sc.add(Icon("lire", (620, 700), tl_ + 0.6, size=160), "pop")
        sc.add(Arrow((960, 450), (1180, 450), tc + 0.3, color=GOLD))
        sc.add(Big("≈ 1,4 mln €", (1430, 430), T("oggi") - 0.2, size=120, color=WHITE, fnt=OSW, sub="euro di oggi · stima"), "hit")
        sc.add(Text("coefficienti ISTAT · valore della moneta\n1976-2024 · calcolo: 250 mln × 10,53 / 1936,27",
                    (1430, 640), tc + 0.4, size=26, fnt=COURR, color=GREY, anchor="ma", align="m"))
        sc.footer = "Fonti: San Marino RTV · archeosardegna · ISTAT (Il valore della moneta in Italia 1861-2024)"
    elif i == 24:
        ts = T("Si") - 0.3; tn = T("Nella") - 0.3; tt = T("Le") - 0.3
        sc.add(Pill("STARE AL GIOCO", (960, 220), a + 0.2, ts, size=48, accent=True))
        for k in range(2):
            sc.add(Figure(walk([(-100 - 140 * k, FY), (420 + 160 * k, FY)], a + 0.2 * k, 340), a + 0.2 * k, kind="suit", s=0.85,
                          label="FINTI ACQUIRENTI" if k == 1 else None), "pop" if k == 0 else None)
        sc.add(Icon("money", (860, 460), ts, size=200), "pop")
        sc.add(Icon("antique", (1340, 450), tn, size=260, label="UN ANTIQUARIO"), "pop")
        sc.add(Pill("INTERMEDIARIO · COLLABORA CON GLI INVESTIGATORI", (960, 220), T("che") - 0.2, tt, size=40, accent=True))
        sc.add(Icon("hourglass", (1340, 450), tt, size=240), "pop")
        sc.add(Pill("CIRCA DUE MESI DI TRATTATIVE", (960, 220), tt + 0.2, size=46, accent=True))
        sc.footer = F_TRAT
    elif i == 25:
        tp = T("tra") - 0.2; te = T("E") - 0.3; ts = T("Sono") - 0.3
        sc.add(MapEl(MAPB, [(a, (12.2, 44.15), 420), (te + 0.2, (12.2, 44.15), 420), (ts, (10.6, 45.3), 270)], a,
                     pins=[dict(at="Pesaro", label="PESARO", t=T("Pesaro") - 0.2, side="r", color=GOLD),
                           dict(at="Urbino", label="URBINO", t=T("Urbino") - 0.2, side="b", color=GOLD),
                           dict(at="Rimini", label="RIMINI", t=T("Rimini") - 0.2, side="t", color=GOLD),
                           dict(at="Bologna", label="BOLOGNA", t=T("Bologna") - 0.2, side="l", color=GOLD),
                           dict(at="Locarno", label="LOCARNO · CANTON TICINO", t=ts + 0.4, side="r", color=RED)],
                     routes=[dict(pts=["Pesaro", "Rimini", "Bologna"], t=a + 0.4, d=2.6, icon="person", color=GOLD, dashed=True),
                             dict(pts=["Bologna", (9.2, 45.5), "Locarno"], t=te + 0.6, d=2.2, icon="painting", color=RED)], title=MT))
        sc.add(Pill("I QUADRI HANNO LASCIATO L'ITALIA", (960, 220), te + 0.4, ts, size=44, accent=True))
        sc.add(Icon("swiss", (1560, 340), ts, size=170, label="SVIZZERA"), "pop")
        sc.footer = F_TRAT + " · Il Giornale dell'Arte · " + MT
    elif i == 26:
        tc = T("Più") - 0.6; tb = T("Il") - 0.3; tc2 = T("I", 1) - 0.3
        sc.add(Chapter("06", "*Locarno*", a, tc))
        sc.add(Calendar((400, 440), 260, [(tc, "MARZO 1976", "23")], tc), "paper")
        sc.add(Pill("PIÙ DI UN ANNO DOPO IL FURTO", (960, 220), tc + 0.2, tb, size=46, accent=True))
        sc.add(Icon("hotel", (900, 460), tb, size=320, label="UN ALBERGO DI LOCARNO"), "pop")
        sc.add(Figure([(0, 1320, FY)], tc2, kind="police", s=0.85, label="CARABINIERI"), "pop")
        sc.add(Figure([(0, 1660, FY)], tc2 + 0.4, kind="police", s=0.85, label="POLIZIA SVIZZERA"), "pop")
        sc.footer = F_LOC
    elif i == 27:
        tm = T("Ma") - 0.3; tf = T("La") - 0.3; ts = T("Secondo") - 0.3
        sc.add(Icon("hotel", (960, 440), a, tm, size=300), "pop")
        sc.add(Pill("VERSIONI NON CONCORDI SUI DETTAGLI", (960, 720), a + 0.4, tm, size=42))
        sc.add(Flash(tm))
        for k, (kind, _, _, lab) in enumerate(ART):
            sc.add(Icon("art_" + kind, (480 + k * 480, 440), T(["Flagellazione", "Madonna", "Muta"][k]) - 0.6, ts, size=270), "pop")
        sc.add(Pill("TUTTI E TRE", (960, 220), T("tutti") - 0.2, ts, size=46, accent=True))
        sc.add(Stamp("RITROVATI", (960, 720), T("Muta") + 0.3, ts, size=90, rot=-7))
        sc.add(Icon("fire", (760, 450), ts, size=240), "pop")
        sc.add(Stamp("PRONTI A\nDISTRUGGERLI?", (1240, 450), T("distruggerli") - 0.2, size=70, rot=6))
        sc.add(Text("secondo le cronache", (960, 760), ts + 0.3, size=30, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = F_LOC
    elif i == 28:
        tl_ = T("Le") - 0.3; tu = T("Uno") - 0.3; ts = T("Sugli") - 0.3
        sc.add(Icon("handcuffs", (600, 440), a, tl_, size=280), "pop")
        sc.add(Big("5", (1250, 400), a + 0.3, tl_, size=240, color=GOLD, fnt=OSW, sub="persone arrestate"), "hit")
        sc.add(Img(doc_typed(760, 360, "CAPI D'ACCUSA", ["concorso in furto aggravato", "ricettazione", "(a vario titolo)"]), (960, 500), tl_, ts, anim="drop", rot=-2), "paper")
        sc.add(Pill("UNO DEGLI ARRESTATI CONFESSA", (960, 220), tu, ts, size=44, accent=True))
        sc.add(Icon("gavel", (620, 460), ts, size=240), "pop")
        sc.add(Img(note_card(["Esiti dei processi:", "fonti non concordi", "quindi: nessun nome"], 560, title="NOTA DELLA REDAZIONE"), (1260, 460), ts + 0.3, anim="drop", rot=2), "paper")
        sc.footer = "Fonti: ANSA · Prima Bergamo · archeosardegna"
    elif i == 29:
        tv = T("Viaggiano") - 0.3; ta = T("A", 1) - 0.3; to = T("Oggi") - 0.3
        sc.add(MapEl(MAPB, [(a, (10.8, 45.0), 330)], a, ta,
                     pins=[dict(at="Locarno", label="LOCARNO", t=a + 0.2, side="r", color=GOLD),
                           dict(at="Urbino", label="URBINO", t=a + 0.4, side="r", color=RED)],
                     routes=[dict(pts=["Locarno", "Bologna", "Urbino"], t=tv, d=2.6, icon="painting", color=GOLD)], title=MT))
        sc.add(Icon("armored", (520, 300), tv, ta, size=200, label="FURGONE BLINDATO"), "pop")
        sc.add(Palazzo(PB, ta, to + 0.2), "whoosh")
        sc.add(Crowd((420, 700, 1500, 870), 14, ta + 0.2, to + 0.2, s=0.34))
        sc.add(Pill("LA GENTE APPLAUDE", (960, 210), T("applaude") - 0.3, T("Sulla") - 0.3, size=46, accent=True))
        sc.add(Pill("29 O 31 MARZO? FONTI NON CONCORDI", (960, 210), T("Sulla") - 0.3, to, size=42))
        sc.add(Sala(SB, to, None, gone={0: a - 5, 1: a - 5, 2: a - 5}, back=to + 0.4))
        sc.add(Pill("GALLERIA NAZIONALE DELLE MARCHE", (960, 220), T("nella") - 0.2, size=44, accent=True))
        sc.footer = F_LOC + " · schema non in scala"
    elif i == 30:
        tn = T("Nevio") - 0.3; tg = T("Il", 1) - 0.3; tf = T("Il", 2) - 0.3
        sc.add(Icon("emptyfolder", (960, 450), a, tn, size=280, label="SOLO ARCHIVI?"), "pop")
        sc.add(Icon("book", (560, 430), tn, size=280), "pop")
        sc.add(Pill("«IL CARABINIERE E L'ANTIQUARIO»", (560, 650), T("Il") - 0.2, size=36, accent=True))
        sc.add(Text("Nevio Monaco · ex capitano dei carabinieri", (560, 720), tn + 0.4, size=28, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Icon("book", (1360, 430), tg, size=280), "pop")
        sc.add(Pill("UN GIALLO · V. OLIVERI", (1360, 650), tg + 0.2, size=36, accent=True))
        sc.add(Text("personaggi di fantasia", (1360, 720), T("personaggi") - 0.2, size=28, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Stamp("IL FURTO DEL SECOLO", (960, 240), tf, size=70, rot=-5))
        sc.footer = "Fonti: Rotary Rimini · il Resto del Carlino · ANSA · Prima Bergamo"
    elif i == 31:
        tu = T("Una") - 0.3; ti = T("quadri") - 0.4
        sc.add(Chapter("", "Il *verdetto*", a, tu))
        items = [("fog", "NEBBIA", T("Una")), ("scaffold", "IMPALCATURA", T("un'impalcatura")), ("alarm_off", "NESSUN ALLARME", T("museo")),
                 ("art_flag", "3 CAPOLAVORI", T("Tre")), ("ear", "TELEFONATE", T("telefonate")), ("lire", "RISCATTI", T("riscatti")),
                 ("velvet", "VELLUTO", T("acquisto")), ("antique", "TRATTATIVA FINTA", T("trattativa")), ("hotel", "LOCARNO", T("fino"))]
        for k, (ic, lab, tt) in enumerate(items):
            x = 300 + (k % 5) * 330; y = 330 if k < 5 else 640
            if k >= 5: x = 465 + (k - 5) * 330
            sc.add(Icon(ic, (x, y), tt - 0.2, ti, size=170, label=lab), "pop" if k % 3 == 0 else None)
        sc.add(Sala(SB, ti, None, back=ti))
        sc.add(Stamp("I QUADRI SONO SALVI", (960, 790), ti + 0.4, size=80, rot=-4))
        sc.footer = "Ricostruzione divulgativa · fonti nella descrizione"
    elif i == 32:
        ts = T("Iscriviti") - 0.3
        sc.add(Sala(SB, a, T("Scrivilo") - 0.2, dim=0) if False else Sala(SB, a, T("Scrivilo") - 0.2))
        sc.add(Pill("PERCHÉ RUBARE QUADRI INVENDIBILI?", (960, 230), a + 0.3, T("Scrivilo") - 0.2, size=50, accent=True))
        sc.add(Bubble((960, 470), 170, T("Scrivilo") - 0.1, ts, text="COMMENTI"), "pop")
        sc.add(Text("Fonti nella descrizione", (960, 760), T("fonti") - 0.2, ts, size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(110), (960, 520), ts, anim="pop", shadow=False), "hit")
        sc.add(Text("ogni giorno un nuovo caso", (960, 700), T("ogni") - 0.2, size=54, fnt=PS, color=GOLD, anchor="ma"))
        sc.footer = "Ricostruzione divulgativa · voce generata con sintesi vocale"
    return sc


def thumbnail(path="thumbnail.jpg"):
    W_, H_ = 1920, 1080
    im = make_bg(8).convert("RGBA")
    # a destra: tre cornici, due vuote e una con la sagoma stilizzata
    for k, (kind, rot, xy) in enumerate([("flag", -5, (1130, 170)), ("madonna", 4, (1500, 120)), ("muta", -3, (1420, 520))]):
        fr = framed(kind, 300)
        if k < 2:
            e = Image.new("RGBA", fr.size, (0, 0, 0, 0)); de = ImageDraw.Draw(e)
            b = max(8, 300 // 12)
            de.rectangle([0, 0, fr.width - 1, fr.height - 1], fill=(176, 136, 70, 255), outline=(110, 80, 36, 255), width=3)
            de.rectangle([b, b, fr.width - b, fr.height - b], fill=(30, 28, 34, 255))
            de.text((fr.width / 2, fr.height / 2), "?", font=font(SERIF, 160), fill=(200, 52, 42, 255), anchor="mm")
            fr = e
        fr = fr.rotate(rot, expand=True, resample=Image.BICUBIC); im.alpha_composite(fr, xy)
    import fx as _fx
    sc_ = _fx.icon("scaffold", 220); im.alpha_composite(sc_, (1170, 560))
    t = rich_img("IL FURTO\nDEL *SECOLO*\nA URBINO", SERIF, 140, WHITE, RED, lh=1.0)
    im.alpha_composite(t, (90, 110))
    st = stamp_img("CASO 011", RED, 64, -10); im.alpha_composite(st, (760, 40))
    st2 = stamp_img("URBINO 1975", (200, 160, 60), 54, 6); im.alpha_composite(st2, (110, 640))
    d = ImageDraw.Draw(im)
    d.text((100, 800), "UN MUSEO SENZA ALLARME, TRE CAPOLAVORI SPARITI", font=font(OSW, 52, 600), fill=GOLD + (255,))
    d.text((100, 868), "E UN ALBERGO IN SVIZZERA", font=font(OSW, 52, 600), fill=GOLD + (255,))
    wm = wordmark(60, sub=False); im.alpha_composite(wm, (100, 975))
    im.convert("RGB").save(path, quality=92)
