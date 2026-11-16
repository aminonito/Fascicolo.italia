import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from car import *

W, H = 1920, 1080
FY = 870
OB = (260, 160, 1660, 880)      # scenografia: l'oratorio
F_OPERA = "Fonti: Finestre sull'Arte · Il Post · Artribune · artnet"
F_FURTO = "Fonti: Il Post · Finestre sull'Arte · artnet · AGI · Il Foglio"
F_VOCI = "Fonti: Il Post · Il Foglio · artnet · Artribune · testimonianze non verificate"
F_2018 = "Fonti: Finestre sull'Arte (2018) · Il Post · artnet · Artribune"

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
        ti = T("In") - 0.3; te = T("È") - 0.3; tu = T("Una") - 0.3; tt = T("La", 1) - 0.3
        sc.add(MapEl((160, 160, 1760, 880), [(a, (12.0, 41.5), 140), (ti, (13.36, 38.4), 320)], a, ti + 0.4,
                     pins=[dict(at="Palermo", label="PALERMO", t=a + 0.3, side="r", color=RED)], title="mappa: Natural Earth · schema non in scala"))
        sc.add(Calendar((330, 420), 220, [(a + 0.8, "PALERMO", "OTT"), (a + 1.6, "OTTOBRE", "1969")], a + 0.8, ti + 0.4), "paper")
        sc.add(Oratory(OB, ti, None, cut_t=tu + 0.4, gone_t=tu + 1.4))
        fxp = (960, 452)
        sc.add(Pill("ALTO QUASI 3 METRI", (960, 220), T("quasi") - 0.2, te, size=46, accent=True))
        sc.add(Stamp("CARAVAGGIO", (1420, 420), te + 0.1, tu, size=70, rot=-8))
        sc.add(Pill("RESTA SOLO IL TELAIO", (960, 220), tu + 1.4, tt, size=46, accent=True))
        sc.add(Icon("roll", (1300, 600), T("portata") - 0.2, None, size=160, move=(T("portata"), 1.2, (1700, 560), 60)))
        sc.footer = F_FURTO + " · schema non in scala"
    elif i == 1:
        tn = T("Nessuno") - 0.3; tq = T("Questo") - 0.3; tv = T("Vedremo") - 0.3
        sc.add(Calendar((560, 450), 280, [(a, "OTTOBRE", "1969"), (a + 0.8, "ANNI '80", "1985"), (a + 1.4, "ANNI 2000", "2005"), (a + 2.0, "OGGI", "2026")], a, tq), "paper")
        sc.add(Big("50+ anni", (1260, 420), a + 0.4, tq, size=170, color=GOLD, fnt=OSW, count=(0, 50, lambda z: f"{z:.0f}+ anni", 1.4)), "hit")
        sc.add(Icon("question", (1260, 680), tn, tq, size=190, label="MAI PIÙ VISTA"), "pop")
        sc.add(Img(cover_folder(), (960, 520), tq + 0.1, tv, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 008", (1150, 300), T("fascicolo") + 0.2, tv, size=70, rot=-12))
        sc.add(Icon("moon", (360, 470), tv + 0.1, size=190, label="UNA NOTTE"), "pop")
        sc.add(Icon("rat", (760, 470), T("voci") - 0.3, size=200, label="LE VOCI"), "pop")
        sc.add(Icon("question", (1160, 470), T("perché") - 0.2, size=180, label="IL MISTERO"), "pop")
        sc.add(Icon("swiss", (1560, 470), T("Svizzera") - 0.4, size=210, label="LA SVIZZERA"), "pop")
        sc.footer = "Fonti: Il Post · Finestre sull'Arte · artnet"
    elif i == 2:
        tc = T("nome") - 0.6; ta = T("Al") - 0.3; to = T("È") - 0.3
        sc.add(Chapter("01", "Il *quadro*", a, tc))
        sc.add(Img(label_card(["Natività con i santi", "Lorenzo e Francesco", "Caravaggio", "olio su tela"], 560, title="SCHEDA DELL'OPERA"), (560, 500), tc, to, anim="drop", rot=-2), "paper")
        sc.add(Icon("nativity", (1320, 480), tc + 0.3, to, size=480), "pop")
        sc.add(Pill("MADONNA E BAMBINO", (1320, 200), ta + 0.2, to, size=40, accent=True))
        sc.add(Pill("SAN FRANCESCO · SAN LORENZO", (1320, 780), T("intorno") - 0.1, to, size=40))
        ph = 470; pw = int(ph * 197 / 268)
        sc.add(Img(nativity_sketch(pw, ph), (1080, FY - ph / 2 - 6), to, anim="drop", shadow=True))
        sc.add(Figure([(0, 1420, FY)], to + 0.3, kind="man", s=0.85), "pop")
        sc.add(Pill("1,75 m", (1420, 520), to + 0.5, size=34))
        sc.add(Pill("2,68 m", (1080, 360), to + 0.7, size=34, accent=True))
        sc.add(Big("268 × 197 cm", (540, 470), T("268") - 0.3, size=130, color=GOLD, fnt=OSW, sub="olio su tela"), "hit")
        sc.add(Text("proporzioni indicative", (1250, 220), to + 0.5, size=28, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = F_OPERA + " · sagoma stilizzata, non l'opera"
    elif i == 3:
        tq = T("Qui") - 0.3; tp = T("Per") - 0.3; ts = T("recenti") - 0.6; td = T("da") - 0.3
        sc.add(Icon("question", (960, 420), a, tq + 0.4, size=260), "pop")
        sc.add(Pill("GLI STUDIOSI NON SONO D'ACCORDO", (960, 230), tq, tp, size=46, accent=True))
        sc.add(MapEl((160, 160, 1760, 880), [(tp, (12.4, 40.1), 140), (dur, (12.4, 40.1), 145)], tp,
                     pins=[dict(at="Palermo", label="SICILIA · 1609?", t=tp + 0.4, side="r", color=GOLD),
                           dict(at="Roma", label="ROMA · 1600?", t=ts + 0.3, side="r", color=RED)],
                     routes=[dict(pts=["Roma", (12.6, 39.5), "Palermo"], t=td, d=2.0, icon="painting", color=GOLD)],
                     title="mappa: Natural Earth · schema non in scala"))
        sc.add(Calendar((330, 420), 200, [(tp + 0.3, "IPOTESI A", "1609"), (ts + 0.2, "IPOTESI B", "1600")], tp + 0.3), "paper")
        sc.footer = "Fonti: Finestre sull'Arte · Artribune · artnet · Il Foglio · mappa: Natural Earth"
    elif i == 4:
        tg = T("Generazioni") - 0.3; tu = T("Un") - 0.3
        sc.add(Oratory(OB, a, None))
        sc.add(Calendar((330, 330), 200, [(a + 0.2, "SECOLO", "1600"), (a + 1.2, "SECOLO", "1700"), (a + 2.0, "SECOLO", "1800"), (a + 2.8, "SECOLO", "1900"), (a + 3.6, "OTTOBRE", "1969")], a + 0.2), "paper")
        sc.add(Pill("PIÙ DI TRE SECOLI E MEZZO", (960, 220), T("per") - 0.2, tg, size=46, accent=True))
        sc.add(Crowd((420, 700, 1500, 870), 9, tg, tu + 0.4, s=0.32, walk=40))
        sc.add(Icon("oratory", (560, 470), tu, size=220, label="PICCOLO ORATORIO"), "pop")
        sc.add(Icon("museum", (1360, 470), T("lontano") - 0.2, size=200, label="GRANDI MUSEI"), "pop")
        sc.add(Arrow((700, 470), (1220, 470), T("lontano"), color=GOLD, dashed=True))
        sc.footer = "Fonti: Il Post · Artribune · artnet · schema non in scala"
    elif i == 5:
        tn = T("Nessun") - 0.3; ta = T("occuparsi") - 0.4; tp = T("Per") - 0.3
        sc.add(Oratory(OB, a, None, night=True))
        sc.add(Pill("IL PRIMO PROBLEMA", (960, 220), a + 0.2, tn, size=46, accent=True))
        sc.add(Icon("alarm_off", (560, 480), T("sicurezza") - 0.3, ta, size=230, label="NESSUN ALLARME"), "pop")
        sc.add(Figure([(0, 1360, FY)], T("nessuna") - 0.2, ta, kind="guard", s=0.8, label="NESSUNA GUARDIA"), "pop")
        sc.add(Stamp("NO", (1360, 560), T("nessuna") + 0.2, ta, size=90, rot=-10))
        sc.add(Figure(walk([(-80, FY), (520, FY)], ta, 420), ta, tp + 0.6, kind="man", s=0.8, label="UNA CUSTODE"))
        sc.add(Icon("toplist", (1300, 470), tp, size=300, label="FBI · TOP TEN"), "pop")
        sc.footer = "Fonti: Il Post · AGI · artnet · Daily Beast · schema non in scala"
    elif i == 6:
        tc = T("Secondo") - 0.3; ta = T("Alcune") - 0.3; ts = T("Sappiamo") - 0.3
        sc.add(Chapter("02", "La *notte*", a, tc))
        sc.add(Calendar((560, 460), 300, [(tc, "OTTOBRE 1969", "17"), (tc + 1.6, "OTTOBRE 1969", "18")], tc, ts + 0.2), "paper")
        sc.add(Icon("moon", (1100, 380), tc + 0.3, ts + 0.2, size=220), "pop")
        sc.add(ClockFace((1440, 460), 130, tc + 0.5, ts + 0.2, start=23.0, speed=0.6, label="NOTTE"))
        sc.add(Pill("ALTRE FONTI: DATE DIVERSE", (960, 760), ta, ts + 0.2, size=44, accent=True))
        sc.add(Icon("emptyframe", (960, 470), ts + 0.2, size=440, label="IL TELAIO VUOTO"), "pop")
        sc.footer = "Fonti: Il Post · Finestre sull'Arte · artnet · AGI · Artribune"
    elif i == 7:
        ti = T("Il") - 0.3; tc = T("Così") - 0.3; tr = T("Restano") - 0.3; tfig = tc + 0.6
        o = sc.add(Oratory(OB, a, None, night=True, torch=a, cut_t=T("tagliata") - 0.2, gone_t=tr))
        for k in range(2):
            sc.add(Figure(walk([(-100 - 140 * k, FY), (620 + 140 * k, FY)], a + 0.2 * k, 300), a + 0.2 * k, tfig, kind="worker", s=0.8), "pop" if k == 0 else None)
        sc.add(Pill("TROPPO GRANDE CON LA CORNICE", (960, 220), ti + 0.3, tc, size=44, accent=True))
        sc.add(Pill("TAGLIATA LUNGO I BORDI", (960, 220), tc + 0.3, tr, size=44, accent=True))
        sc.add(Icon("cutter", (1500, 330), T("tagliata") - 0.2, tr, size=120), "pop")
        sc.add(Pill("RESTANO SOLO FRAMMENTI", (960, 220), tr, size=44))
        sc.footer = F_FURTO + " · ricostruzione grafica"
    elif i == 8:
        tq = T("Quella") - 0.3; ts = T("Secondo") - 0.3; tm = T("Ma") - 0.3
        sc.add(Icon("roll", (960, 470), a, tm, size=360, label="LA TELA ARROTOLATA"), "pop")
        sc.add(Icon("carpet", (960, 470), tq + 0.2, None, size=360, move=(ts + 0.2, 1.0, (960, 470), 0)), "pop")
        sc.add(Pill("SPARISCE ANCHE UN TAPPETO", (960, 220), tq + 0.2, tm, size=46, accent=True))
        sc.add(Arrow((960, 680), (960, 560), ts + 0.4, tm, color=GOLD))
        sc.add(Pill("PER AVVOLGERE IL QUADRO?", (960, 760), ts + 0.4, tm, size=40))
        sc.add(Icon("nativity", (960, 480), tm, size=380), "pop")
        sc.add(Icon("magnifier", (1160, 420), tm + 0.4, size=200), "pop")
        sc.add(Stamp("CREPE", (720, 360), T("crepe") - 0.1, size=70, rot=-10))
        sc.add(Stamp("COLORE CHE\nSI STACCA", (1260, 640), T("colore") - 0.1, size=56, rot=6))
        sc.footer = "Fonti: artnet · AGI · Il Post · ricostruzione grafica"
    elif i == 9:
        ta = T("A") - 0.3; tn = T("Non") - 0.3; tt = T("Tutto") - 0.3
        sc.add(Icon("question", (960, 450), a, ta + 0.4, size=280, label="CHI?"), "pop")
        ti_ = T("indagini") - 0.5
        sc.add(Icon("gavel", (560, 450), ta + 0.2, ti_, size=240), "stamp")
        sc.add(Stamp("NESSUN\nPROCESSO", (560, 700), tn, ti_, size=60, rot=-8))
        sc.add(Icon("handcuffs", (1360, 450), T("nessuno") - 0.4, ti_, size=240), "pop")
        sc.add(Stamp("NESSUN\nCONDANNATO", (1360, 700), T("nessuno"), ti_, size=60, rot=6))
        sc.add(Pill("DOPO QUELLA NOTTE: SOLO", (960, 230), tt, size=46, accent=True))
        sc.add(Icon("magnifier", (440, 470), T("indagini") - 0.3, size=220, label="INDAGINI"), "pop")
        sc.add(Icon("mic", (960, 470), T("testimonianze") - 0.3, size=220, label="TESTIMONIANZE"), "pop")
        sc.add(Bubble((1480, 450), 130, T("voci") - 0.3, text="VOCI"), "pop")
        sc.footer = "Fonti: Il Post · Finestre sull'Arte · Daily Beast"
    elif i == 10:
        tc = T("È") - 0.3; tu = T("Una") - 0.3; tv = T("e", 2) - 0.3
        sc.add(Chapter("03", "Il telaio *vuoto*", a, tc))
        sc.add(Oratory(OB, tc, None, empty=True))
        sc.add(Calendar((420, 330), 180, [(tc, "OTTOBRE", "18")], tc, tu + 0.6), "paper")
        sc.add(ClockFace((1500, 330), 100, tc + 0.3, tu + 0.6, start=15.0, speed=0.05, label="POMERIGGIO"))
        sc.add(Figure(walk([(-80, FY), (760, FY)], tu, 320), tu, kind="man", s=0.85, label="LA CUSTODE", arms=[(T("vede"), "up")]))
        sc.add(Stamp("VUOTO!", (1300, 470), T("vuoto") - 0.1, size=90, rot=-8))
        sc.footer = "Fonti: Il Post · Il Foglio · AGI · schema non in scala"
    elif i == 11:
        tm = T("Ma") - 0.3; tl_ = T("indagini") - 0.3; tn = T("La") - 0.3
        sc.add(Figure(walk([(-100, FY), (700, FY)], a, 360), a, tm, kind="police", s=0.85, carry=[(a + 0.5, "magnifier")]), "pop")
        sc.add(Figure(walk([(-260, FY), (520, FY)], a + 0.3, 360), a + 0.3, tm, kind="police", s=0.85), None)
        sc.add(Icon("emptyframe", (1300, 450), a + 0.4, tm, size=360), "pop")
        sc.add(ClockFace((960, 430), 160, tm, tl_ + 0.2, start=0.0, speed=4.0, label="UNA NOTTE DI VANTAGGIO"))
        sc.add(Stamp("NESSUN\nCOLPEVOLE", (960, 500), T("nessun") - 0.1, tn, size=80, rot=-8))
        sc.add(Img(newspaper(560, 600, "CRONACA", "ottobre 1969", "Rubato\nun *Caravaggio*", "a Palermo"), (700, 520), tn, anim="drop", rot=-3), "paper")
        sc.add(Img(newspaper(560, 600, "NOTIZIE", "ottobre 1969", "Sparita\nla *Natività*", "il telaio vuoto"), (1240, 520), tn + 0.8, anim="drop", rot=3), "paper")
        sc.footer = "Fonti: Il Post · Il Foglio · giornali ricostruiti (testate di fantasia)"
    elif i == 12:
        ta = T("lista") - 1.2; tm = T("Ma") - 0.3; te = T("vuoto") - 0.8
        sc.add(Crowd((300, 640, 1620, 880), 10, a, ta, s=0.4, kinds=("police", "expert", "suit")))
        sc.add(Pill("INVESTIGATORI ITALIANI E STRANIERI", (960, 300), a + 0.3, ta, size=46, accent=True))
        sc.add(Icon("toplist", (960, 470), ta, tm, size=380, label="FBI · DIECI CRIMINI D'ARTE"), "pop")
        sc.add(Icon("emptyframe", (960, 470), tm, te, size=380, label="NON SI TROVA"), "pop")
        for k, (x, y) in enumerate(((560, 380), (1360, 380), (760, 640), (1160, 640))):
            sc.add(Bubble((x, y), 90, te + 0.4 + 0.3 * k, text="VOCI" if k == 0 else "?"), "pop" if k == 0 else None)
        sc.footer = "Fonti: Il Post · Finestre sull'Arte · artnet · Daily Beast"
    elif i == 13:
        tc = T("Cosa") - 0.3; tl_ = T("L'ipotesi") - 0.3; tm = T("attenzione") - 0.6
        sc.add(Chapter("04", "Le *voci*", a, tc))
        sc.add(Icon("magnifier", (560, 470), tc, tm, size=240), "pop")
        sc.add(Icon("meeting", (1300, 470), tc + 0.3, tm, size=320, label="COSA NOSTRA?"), "pop")
        sc.add(Pill("IPOTESI: LA MAFIA HA RUBATO O PRESO IL QUADRO", (960, 230), tl_, tm, size=40, accent=True))
        sc.add(Stamp("IPOTESI,\nNON SENTENZE", (960, 500), T("ipotesi", 1) - 0.1, size=90, rot=-6))
        sc.footer = "Fonti: Finestre sull'Arte · Il Foglio · Daily Beast"
    elif i == 14:
        te = T("E") - 0.3; tu = T("Uno") - 0.3; ta = T("Un'altra") - 0.3
        sc.board({"a": dict(xy=(480, 520), name="COLLABORATORE", role="testimonianza", t=a + 0.2, rot=-3),
                  "b": dict(xy=(960, 520), name="COLLABORATORE", role="testimonianza", t=a + 0.5, rot=2),
                  "c": dict(xy=(1440, 520), name="COLLABORATORE", role="testimonianza", t=a + 0.8, rot=-2)},
                 [("a", "b", te), ("b", "c", te + 0.3)], a, tu)
        sc.add(Stamp("VERSIONI\nDIVERSE", (960, 300), te + 0.4, tu, size=60, rot=-8))
        sc.add(Icon("meeting", (760, 470), tu, ta, size=360), "pop")
        sc.add(Icon("nativity", (1260, 470), tu + 0.5, ta, size=300, label="SIMBOLO DI POTERE?"), "pop")
        sc.add(Icon("carpet", (960, 480), ta, size=420, label="USATO COME TAPPETO?"), "pop")
        sc.add(Text("sagome · nessuna foto reale", (960, 860), a + 0.5, tu, size=26, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = F_VOCI
    elif i == 15:
        tr = T("Racconta") - 0.3; tc = T("e") - 0.3; ta = T("Anche") - 0.3
        sc.add(Figure([(0, 480, FY)], a, kind="man", s=0.85, label="COLLABORATORE"), "pop")
        sc.add(Bubble((520, 330), 110, a + 0.4, inner="roll"), "pop")
        sc.add(Icon("roll", (1160, 470), tr, T("colore") - 0.2, size=360), "pop")
        sc.add(Icon("nativity", (1160, 470), T("colore") - 0.2, size=380), "pop")
        sc.add(Stamp("ROVINATO", (1160, 360), T("rovinato") - 0.1, ta, size=70, rot=-10))
        sc.add(Pill("L'AFFARE SALTA", (1160, 760), T("saltò") - 0.2, ta, size=44, accent=True))
        sc.add(Stamp("MAI\nCONFERMATA", (1160, 770), ta + 0.2, size=70, rot=-6))
        sc.footer = "Fonti: AGI · artnet · testimonianza non verificata"
    elif i == 16:
        ts = T("Secondo") - 0.3; te = T("E", 1) - 0.3; tu = T("Un") - 0.3; ta = T("Anche") - 0.3
        sc.add(Pill("LA VOCE PIÙ TRISTE", (960, 220), a + 0.1, ts, size=48, accent=True))
        sc.add(Icon("stable", (960, 480), ts + 0.4, ta, size=380, label="UNA STALLA FUORI PALERMO"), "pop")
        sc.add(Icon("rat", (500, 700), T("topi") - 0.2, ta, size=180), "pop")
        sc.add(Icon("pig", (1420, 700), T("maiali") - 0.2, ta, size=200), "pop")
        sc.add(Icon("fire", (960, 300), T("bruciato") - 0.2, ta, size=200), "hit")
        sc.add(Stamp("SOLO UNA\nTESTIMONIANZA", (960, 500), ta + 0.1, size=90, rot=-6))
        sc.footer = "Fonti: Il Post · Il Foglio · artnet · testimonianza non verificata"
    elif i == 17:
        tl_ = T("La") - 0.3; tn = T("nel") - 0.3; tw = T("Watson", 1) - 0.3
        sc.add(Chapter("05", "L'appuntamento *mancato*", a, tl_))
        sc.add(Figure([(0, 520, FY)], tl_, kind="expert", s=0.85, carry=[(tl_ + 0.4, "magnifier")], label="GIORNALISTA"), "pop")
        sc.add(Icon("book", (1100, 450), tn, tw, size=300), "pop")
        sc.add(Pill("\"THE CARAVAGGIO CONSPIRACY\" · 1984", (1100, 700), tn + 0.4, tw, size=40, accent=True))
        sc.add(Figure([(0, 1460, FY)], tw + 0.4, kind="suit", s=0.85, label="MERCANTE D'ARTE", flip=-1), "pop")
        sc.add(Bubble((1060, 420), 130, T("offre") - 0.2, inner="nativity", text="IN VENDITA"), "pop")
        sc.footer = "Fonti: Il Post · Il Foglio"
    elif i == 18:
        tp = T("per") - 0.3; tm = T("Ma") - 0.3; te = T("È") - 0.3
        sc.add(MapEl((160, 160, 1760, 880), [(a, (14.5, 40.6), 300), (tp, (15.3, 40.8), 700)], a, tm,
                     pins=[dict(at="Laviano", label="APPUNTAMENTO · CAMPANIA", t=a + 0.6, side="r", color=RED), dict(at="Napoli", label="NAPOLI", t=a + 0.3, side="l")],
                     title="mappa: Natural Earth · schema non in scala"))
        sc.add(Calendar((330, 400), 220, [(tp, "NOVEMBRE", "23"), (tp + 0.9, "NOVEMBRE", "1980")], tp, tm), "paper")
        sc.add(Icon("earth", (960, 470), tm + 0.2, size=420, anim="shake"), "hit")
        sc.add(Flash(T("trema") - 0.1))
        sc.add(Pill("TERREMOTO DELL'IRPINIA", (960, 230), te, size=50, accent=True))
        sc.add(Icon("quake", (560, 520), te + 0.4, size=220, anim="shake"), None)
        sc.add(Icon("quake", (1360, 520), te + 0.6, size=220, anim="shake"), None)
        sc.footer = "Fonti: Il Post · Il Foglio · mappa: Natural Earth"
    elif i == 19:
        ti = T("I") - 0.3; te = T("E") - 0.3; td = T("nasce") - 0.6
        sc.add(Stamp("APPUNTAMENTO\nSALTATO", (960, 450), a + 0.1, ti + 0.6, size=90, rot=-6))
        sc.add(Icon("phone", (960, 470), ti + 0.6, te, size=280, label="CONTATTI PERSI"), "pop")
        sc.add(Icon("nativity", (640, 470), te, td, size=320, label="ORIGINALE?"), "pop")
        sc.add(Icon("question", (1280, 470), T("o") - 0.3, td, size=260, label="UN'ESCA?"), "pop")
        sc.add(Icon("quake", (960, 470), td + 0.2, size=320, anim="shake"), "hit")
        sc.add(Pill("UN'ALTRA VOCE: DISTRUTTO NEL TERREMOTO", (960, 760), T("che") - 0.2, size=44, accent=True))
        sc.footer = "Fonti: Il Post · Il Foglio · artnet · Artribune"
    elif i == 20:
        tl_ = T("La") - 0.3; te = T("e") - 0.3; ti = T("Il") - 0.3
        sc.add(Calendar((960, 460), 300, [(a + 0.1, "ANNI '80", "1985"), (a + 0.7, "ANNI '90", "1995"), (a + 1.3, "GIUGNO", "2018")], a + 0.1, tl_ + 0.2), "paper")
        sc.add(Chapter("06", "La pista *svizzera*", tl_ + 0.2, ti + 0.2))
        sc.add(Icon("commission", (560, 460), ti + 0.2, size=300, label="COMMISSIONE ANTIMAFIA"), "pop")
        sc.add(Icon("folder", (1360, 460), ti + 0.4, size=260, label="NUOVA TESTIMONIANZA"), "pop")
        sc.footer = "Fonti: Finestre sull'Arte (2018) · artnet · Il Post"
    elif i == 21:
        tl_ = T("Lo") - 0.3; ts = T("Solo") - 0.3; tc = T("che") - 0.3
        sc.add(Pill("SECONDO QUESTA VERSIONE", (960, 220), a + 0.1, size=44, accent=True))
        sc.add(Figure(walk([(-100, FY), (560, FY)], a + 0.2, 300), a + 0.2, kind="worker", s=0.85, label="LADRI COMUNI"), "pop")
        sc.add(Stamp("NON LA MAFIA?", (560, 330), tl_, ts, size=56, rot=-6))
        sc.add(Icon("roll", (700, 760), tl_ + 0.6, None, size=180, move=(ts + 0.2, 1.4, (1220, 760), 80)))
        sc.add(Figure([(0, 1400, FY)], ts, kind="suit", s=0.85, label="UN BOSS (SAGOMA)", flip=-1), "pop")
        sc.add(Icon("money", (1400, 330), tc, size=220), "pop")
        sc.add(Pill("NE CAPISCE IL VALORE ECONOMICO", (960, 220), tc + 0.2, size=44))
        sc.footer = F_2018
    elif i == 22:
        ti = T("Il") - 0.3; ts = T("versione") - 0.6
        sc.add(MapEl((560, 160, 1360, 880), [(a, (11.9, 42.1), 80), (ti + 1.5, (11.9, 42.1), 80)], a, ts,
                     pins=[dict(at="Palermo", label="PALERMO", t=a + 0.2, side="r", color=RED), dict(at="Lugano", label="SVIZZERA", t=ti + 1.2, side="r", color=GOLD)],
                     routes=[dict(pts=["Palermo", "Roma", "Milano", "Lugano"], t=ti, d=2.4, icon="painting", color=GOLD)],
                     title="Natural Earth"))
        sc.add(Pill("UN MERCANTE SVIZZERO", (1630, 520), T("mercante") - 0.3, ts, size=40, accent=True))
        sc.add(Icon("swiss", (560, 470), ts, size=260), "pop")
        sc.add(Icon("pieces", (1300, 470), T("tagliata") - 0.3, size=360, label="IN PIÙ PEZZI?"), "pop")
        sc.footer = F_2018 + " · mappa: Natural Earth"
    elif i == 23:
        tl_ = T("La") - 0.3; ti = T("Intanto") - 0.3; ta = T("Ancora") - 0.3
        sc.add(Icon("pieces", (960, 470), a, ti, size=380), "pop")
        sc.add(Stamp("POCO\nATTENDIBILE", (1400, 420), tl_ + 0.3, ti, size=70, rot=-8))
        sc.add(Pill("UN QUADRO A PEZZI È DIFFICILISSIMO DA VENDERE", (960, 780), T("un") - 0.2, ti, size=40, accent=True))
        sc.add(Calendar((520, 450), 240, [(ti, "PALERMO", "2018")], ti), "paper")
        sc.add(Icon("folder", (1000, 450), ti + 0.4, size=260, label="PROCURA DI PALERMO"), "pop")
        sc.add(Stamp("CONTRO\nIGNOTI", (1440, 450), T("contro") - 0.1, size=80, rot=-8))
        sc.footer = "Fonti: Il Post · Finestre sull'Arte (2018) · Artribune"
    elif i == 24:
        tf = T("Fino") - 0.3; tq = T("Quel") - 0.3; tl_ = T("L'ha") - 0.3
        sc.add(Chapter("07", "La *copia*", a, tf))
        sc.add(Oratory(OB, tf, None, empty=True, copy_t=T("copia") - 0.2))
        sc.add(Calendar((420, 330), 200, [(tf + 0.2, "DICEMBRE", "12"), (tf + 1.0, "DICEMBRE", "2015")], tf + 0.2, tl_), "paper")
        sc.add(Pill("UNA COPIA AL POSTO DELL'ORIGINALE", (960, 220), T("copia") - 0.1, tl_, size=44, accent=True))
        sc.add(Pill("COMMISSIONATA DA SKY · REALIZZATA DA FACTUM ARTE (MADRID)", (960, 220), tl_, size=36))
        sc.add(Icon("scanner", (1560, 560), T("Madrid") - 0.4, size=220), "pop")
        sc.footer = "Fonti: Il Post · Il Foglio · Finestre sull'Arte · artnet"
    elif i == 25:
        to = T("Oggi") - 0.3; tm = T("Ma") - 0.3
        sc.add(Icon("scanner", (960, 470), a, to, size=420, label="RICOSTRUZIONE DIGITALE"), "pop")
        sc.add(Oratory(OB, to, None, empty=True, copy_t=to))
        sc.add(Crowd((420, 700, 1500, 870), 8, to + 0.3, None, s=0.32))
        sc.add(Stamp("RIPRODUZIONE", (1300, 330), tm + 0.1, size=60, rot=-8))
        sc.add(Pill("L'ORIGINALE MANCA ANCORA", (960, 220), T("l'originale") - 0.1, size=46, accent=True))
        sc.footer = "Fonti: Il Foglio · Finestre sull'Arte · schema non in scala"
    elif i == 26:
        tl_ = T("Leonardo") - 0.3; te = T("diventato") - 0.8
        sc.add(Icon("book", (960, 450), tl_, te, size=320, label="\"UNA STORIA SEMPLICE\""), "pop")
        sc.add(Pill("LEONARDO SCIASCIA", (960, 230), tl_ + 0.3, te, size=48, accent=True))
        sc.add(Icon("newspaper", (500, 450), a + 0.1, tl_, size=240), "pop")
        for k in range(5):
            sc.add(Icon("emptyframe", (300 + k * 330, 470), te + 0.25 * k, size=240), "pop" if k == 0 else None)
        sc.add(Pill("OPERE RUBATE E MAI RITROVATE", (960, 760), T("simbolo") - 0.2, size=44, accent=True))
        sc.footer = "Fonti: Il Post · Il Foglio"
    elif i == 27:
        tu = T("Un") - 0.3
        sc.add(Chapter("", "Il *verdetto*", a, tu))
        items = [("nativity", "QUASI 3 METRI", T("Un")), ("alarm_off", "NESSUN ALLARME", T("oratorio")), ("roll", "OTTOBRE 1969", T("Una")),
                 ("meeting", "RIUNIONI?", T("riunioni")), ("stable", "UNA STALLA?", T("stalla")), ("earth", "UN TERREMOTO?", T("terremoto")),
                 ("swiss", "LA SVIZZERA?", T("mercante"))]
        for k, (ic, lab, tt) in enumerate(items):
            x = 220 + (k % 4) * 493; y = 330 if k < 4 else 650
            if k >= 4: x = 466 + (k - 4) * 493
            sc.add(Icon(ic, (x, y), tt - 0.2, T("nessuna") - 0.2, size=200, label=lab), "pop")
        sc.add(Stamp("NESSUNA PROVA\nDEFINITIVA", (960, 500), T("nessuna") - 0.1, size=100, rot=-6))
        sc.footer = "Ricostruzione divulgativa · fonti nella descrizione"
    elif i == 28:
        ts = T("Iscriviti") - 0.3
        sc.add(Oratory(OB, a, T("Scrivilo") - 0.2, empty=True, dim=0.35))
        sc.add(Pill("ESISTE ANCORA O È PERDUTA?", (960, 230), a + 0.3, T("Scrivilo") - 0.2, size=52, accent=True))
        sc.add(Bubble((960, 470), 170, T("Scrivilo") - 0.1, ts, text="COMMENTI"), "pop")
        sc.add(Text("Fonti nella descrizione", (960, 760), T("fonti") - 0.2, ts, size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(110), (960, 520), ts, anim="pop", shadow=False), "hit")
        sc.add(Text("ogni giorno un nuovo caso", (960, 700), T("ogni") - 0.2, size=54, fnt=PS, color=GOLD, anchor="ma"))
        sc.footer = "Ricostruzione divulgativa · voce generata con sintesi vocale"
    return sc


def thumbnail(path="thumbnail.jpg"):
    W_, H_ = 1920, 1080
    im = make_bg(8).convert("RGBA")
    lay = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    # telaio vuoto a destra, con la sagoma della tela arrotolata
    fr = ragged_frame(470, 640, seed=5)
    lay.alpha_composite(fr, (1290, 150))
    ghost = set_alpha(nativity_sketch(400, 560), 0.25); lay.alpha_composite(ghost, (1325, 190))
    im.alpha_composite(lay)
    ic = fx.icon("roll", 300); im.alpha_composite(ic, (1080, 700))
    ic = fx.icon("question", 170); im.alpha_composite(ic, (1700, 60))
    t = rich_img("IL CARAVAGGIO\n*SPARITO*\nNEL NULLA", SERIF, 130, WHITE, RED, lh=1.0)
    im.alpha_composite(t, (90, 150))
    st = stamp_img("CASO 008", RED, 64, -10); im.alpha_composite(st, (760, 40))
    st2 = stamp_img("PALERMO 1969", (200, 160, 60), 54, 6); im.alpha_composite(st2, (110, 620))
    d = ImageDraw.Draw(im)
    d.text((100, 800), "TAGLIATO DALLA CORNICE IN UNA NOTTE", font=font(OSW, 54, 600), fill=GOLD + (255,))
    d.text((100, 870), "E MAI PIÙ RITROVATO", font=font(OSW, 54, 600), fill=GOLD + (255,))
    wm = wordmark(60, sub=False); im.alpha_composite(wm, (100, 975))
    im.convert("RGB").save(path, quality=92)
