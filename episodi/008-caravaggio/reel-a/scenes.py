import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from car import *
W, H = 1080, 1920
FY = 1300
OB = (40, 570, 1040, 1350)

def build(i, dur, a, words):
    T0 = Clock(words, a)
    def T(p, n=0):
        try: return T0(p, n)
        except KeyError: return a + 0.5
    sc = Scene(dur)
    if i == 0:
        tt = T("tagliato") - 0.3; te = T("E") - 0.3
        sc.add(Text("Un *Caravaggio*\nalto quasi 3 metri", (540, 330), a, size=80, anchor="ma", align="m"))
        sc.add(Oratory(OB, a + 0.2, None, cut_t=tt + 0.2, gone_t=te))
        sc.add(Stamp("MAI PIÙ\nRITROVATO", (540, 900), te + 0.1, size=80, rot=-8))
        scene_cam(sc, (0, 540, 960, 1.0), (tt, 540, 960, 1.0), (tt + 0.8, 540, 830, 1.35), (dur, 540, 830, 1.4))
        sc.footer = "Fonti: Il Post · Finestre sull'Arte · artnet · sagoma, non l'opera"
    elif i == 1:
        to = T("Oratorio") - 0.3; tn = T("nessun") - 0.3
        sc.add(MapEl((40, 420, 1040, 1320), [(a, (13.0, 40.0), 160), (to, (13.36, 38.12), 700)], a, to + 0.3,
                     pins=[dict(at="Palermo", label="PALERMO", t=a + 0.2, side="t", color=RED)], title="mappa: Natural Earth"))
        sc.add(Calendar((880, 560), 180, [(a, "OTTOBRE", "1969")], a), "paper")
        sc.add(Icon("oratory", (540, 760), to, tn, size=460, label="ORATORIO DI SAN LORENZO"), "pop")
        sc.add(Icon("alarm_off", (300, 900), tn, size=300, label="NESSUN ALLARME"), "pop")
        sc.add(Figure([(0, 780, FY - 100)], T("guardia") - 0.3, kind="guard", s=0.9, label="NESSUNA GUARDIA"), "pop")
        sc.add(Stamp("NO", (780, 1000), T("guardia"), size=100, rot=-10))
        sc.footer = "Fonti: Il Post · Finestre sull'Arte · AGI"
    elif i == 2:
        tl_ = T("arrotolano") - 0.3; te = T("e") - 0.3; tr = T("Resta") - 0.3
        sc.add(Oratory(OB, a, None, night=True, torch=a, cut_t=a + 0.3, gone_t=tl_ + 0.3))
        for k in range(2): sc.add(Figure([(0, 300 + k * 480, FY - 40)], a + 0.1 * k, te, kind="worker", s=0.9), "pop" if k == 0 else None)
        sc.add(Icon("roll", (540, 1220), tl_, None, size=260, move=(te, 1.0, (1250, 1220), 60)), "pop")
        sc.add(Pill("TAGLIATA LUNGO I BORDI", (540, 480), a + 0.3, tl_, size=52, accent=True))
        sc.add(Pill("SOLO IL TELAIO VUOTO", (540, 480), tr, size=52, accent=True))
        sc.footer = "Fonti: Il Post · artnet · Artribune · ricostruzione grafica"
    elif i == 3:
        tm = T("Mostrato") - 0.3; tr = T("Rosicchiato") - 0.3; tb = T("Bruciato") - 0.3
        sc.add(Bubble((540, 600), 200, a + 0.1, tm, text="LE VOCI"), "pop")
        sc.add(Text("collaboratori di giustizia\nversioni mai confermate", (540, 360), a + 0.3, size=44, fnt=COURR, color=GREY, anchor="ma", align="m"))
        sc.add(Icon("meeting", (540, 700), tm, tr, size=480, label="RIUNIONI DEI BOSS?"), "pop")
        sc.add(Icon("stable", (540, 700), tr, tb, size=420, label="UNA STALLA?"), "pop")
        sc.add(Icon("rat", (300, 1060), T("topi") - 0.2, tb, size=220), "pop")
        sc.add(Icon("pig", (780, 1060), T("topi") + 0.1, tb, size=220), "pop")
        sc.add(Icon("fire", (540, 760), tb, size=420), "hit")
        sc.add(Stamp("NON\nVERIFICATO", (540, 1250), tb + 0.4, size=80, rot=-8))
        sc.footer = "Fonti: Il Post · Il Foglio · artnet · testimonianze non verificate"
    elif i == 4:
        tu = T("mercante") - 0.4
        sc.add(Calendar((540, 450), 220, [(a, "GIUGNO", "2018")], a, tu), "paper")
        sc.add(Icon("commission", (540, 800), a + 0.4, tu, size=420, label="COMMISSIONE ANTIMAFIA"), "pop")
        sc.add(MapEl((40, 420, 1040, 1320), [(tu, (11.8, 42.2), 100), (dur, (11.7, 42.3), 102)], tu,
                     pins=[dict(at="Palermo", label="PALERMO", t=tu, side="r", color=RED), dict(at="Lugano", label="SVIZZERA", t=tu + 1.4, side="r", color=GOLD)],
                     routes=[dict(pts=["Palermo", "Roma", "Milano", "Lugano"], t=tu + 0.2, d=1.8, icon="painting", color=GOLD)], title="percorso indicativo · Natural Earth"))
        sc.add(Pill("UN MERCANTE D'ARTE?", (560, 900), T("mercante") - 0.2, size=52, accent=True))
        sc.footer = "Fonti: Finestre sull'Arte (2018) · artnet · Il Post"
    elif i == 5:
        tl_ = T("L'originale") - 0.3
        sc.add(Oratory(OB, a, None, empty=True, copy_t=a + 0.6))
        sc.add(Calendar((540, 440), 190, [(a, "DICEMBRE", "2015")], a, tl_), "paper")
        sc.add(Stamp("COPIA", (760, 640), a + 0.8, tl_, size=90, rot=-8))
        sc.add(Big("50+ anni", (540, 400), tl_, size=150, color=GOLD, fnt=OSW, count=(0, 50, lambda z: f"{z:.0f}+ anni", 1.0), sub="senza l'originale"), "hit")
        sc.footer = "Fonti: Il Post · Il Foglio · Finestre sull'Arte"
    elif i == 6:
        sc.add(Text("Esiste\n*ancora?*", (540, 330), a, size=110, anchor="ma", align="m"))
        sc.add(Icon("emptyframe", (540, 820), a + 0.2, size=400), "pop")
        sc.add(Text("Storia completa su YouTube", (540, 1100), T("storia"), size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(90), (540, 1250), T("Fascicolo"), anim="pop", shadow=False), "hit")
        sc.footer = "Ricostruzione a scopo divulgativo"
    return sc
