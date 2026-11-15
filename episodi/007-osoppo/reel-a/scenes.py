import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from osp import *
W, H = 1080, 1920
FY = 1300

def build(i, dur, a, words):
    T0 = Clock(words, a)
    def T(p, n=0):
        try: return T0(p, n)
        except KeyError: return a + 0.5
    sc = Scene(dur)
    if i == 0:
        sc.add(Text("7 uomini,\n*pochi minuti*", (540, 330), a, size=104, anchor="ma", align="m"))
        sc.add(Big("100+ milioni", (540, 760), T("e") - 0.1, size=130, color=GOLD, fnt=OSW, count=(0, 100, lambda z: f"{z:.0f}+ milioni", 1.0), sub="di lire"), "hit")
        sc.add(Icon("moneybag", (540, 1010), T("cento") - 0.2, size=260), "pop")
        sc.add(Stamp("SENZA SPARARE\nUN COLPO", (540, 1290 - 20), T("Senza") - 0.1, size=66, rot=-8, color=(60, 150, 80)))
        sc.footer = "Fonti: Il Post · Geopop · MilanoFree"
    elif i == 1:
        tg = T("Giorno") - 0.3; tu = T("Un") - 0.3
        sc.add(Calendar((540, 560), 300, [(a, "MILANO · FEBBRAIO", "27"), (a + 0.8, "FEBBRAIO", "1958")], a, tu), "paper")
        sc.add(Icon("payenv", (540, 1000), tg, tu, size=320, label="GIORNO DI PAGA"), "pop")
        sc.add(Crossing((40, 420, 1040, 1320), tu, None, cars=[dict(kind="van", keys=[(tu, -.1, .63, 0), (tu + 2.0, .36, .63, 0)], label="PORTAVALORI", L=.13),
                                                        dict(kind="truck", keys=[(tu, 1.1, .63, 180), (tu + 2.0, .50, .63, 180)], L=.13)],
                        marks=[dict(t=tu + 2.0, x=.43, y=.63, text="BAM!", d=3)]))
        sc.add(Pill("VIA OSOPPO", (540, 360), T("Osoppo") - 0.4, size=50, accent=True))
        sc.footer = "Fonti: Il Post · Varesenews · Il Giornale · schema non in scala"
    elif i == 2:
        tc = T("caricano") - 0.3
        sc.add(Icon("van", (540, 760), a, size=520), None)
        for k in range(3): sc.add(Figure([(0, 220 + k * 320, FY)], a + 0.1 * k, kind="worker", s=1.0), "pop" if k == 0 else None)
        sc.add(Icon("overalls", (300, 420), a + 0.2, tc, size=220), "pop"); sc.add(Icon("balaclava", (780, 420), T("passamontagna") - 0.2, tc, size=220), "pop")
        sc.add(Pill("AGENTE DISARMATO", (540, 1020), T("disarmano") - 0.1, tc, size=46, accent=True))
        for k in range(4): sc.add(Icon("moneybag", (540, 760), tc + 0.25 * k, None, size=150, move=(tc + 0.1 + 0.25 * k, 0.8, (1200, 600 + 80 * k), 0)))
        sc.add(Stamp("SPARITI", (540, 1080), T("spariscono") - 0.1, size=90, rot=-8))
        sc.footer = "Fonti: Il Post · Geopop · Varesenews · ricostruzione grafica"
    elif i == 3:
        to = T("Oggi") - 0.3
        sc.add(Big("114 mln lire", (540, 640), a + 0.1, to, size=130, color=GOLD, fnt=OSW, count=(0, 114, lambda z: f"{z:.0f} mln lire", 1.2), sub="in contanti"), "hit")
        for k in range(4): sc.add(Icon("moneybag", (210 + k * 220, 1000), a + 0.3 + 0.1 * k, to, size=180), "pop" if k == 0 else None)
        sc.add(Big("≈ 1,8 mln €", (540, 640), to, size=140, color=WHITE, fnt=OSW), "hit")
        sc.add(Text("coefficienti ISTAT\n1958-2024", (540, 900), to + 0.3, size=44, fnt=COURR, color=GREY, anchor="ma", align="m"))
        sc.footer = "Fonti: Geopop · MilanoFree · ISTAT"
    elif i == 4:
        te = T("E") - 0.3
        sc.add(Icon("overalls", (540, 560), a, T("fiume") - 0.1, size=320), "pop")
        sc.add(Icon("river", (540, 1000), T("fiume") - 0.3, size=620, label="FIUME OLONA"), None)
        sc.add(Icon("overalls", (540, 600), T("fiume") - 0.1, None, size=200, move=(T("fiume"), 0.8, (540, 960), 0)))
        sc.add(Stamp("IN SECCA!", (700, 820), T("secca") - 0.2, size=90, rot=-8))
        sc.footer = "Fonti: Il Post · Geopop · Wikipedia"
    elif i == 5:
        ti = T("In") - 0.3
        sc.add(Icon("tag", (540, 640), a, ti, size=420), "hit")
        sc.add(Figure([(0, 300, FY)], a + 0.4, ti, kind="police", s=1.0, carry=[(a + 0.6, "magnifier")]), "pop")
        for k in range(5): sc.add(Icon("handcuffs", (180 + k * 180, 700), ti + 0.2 * k, size=150), "pop" if k == 0 else None)
        sc.add(Icon("gavel", (540, 1050), T("condannata") - 0.3, size=300), "stamp")
        sc.add(Stamp("CONDANNATI", (540, 1300), T("condannata"), size=80, rot=-6))
        sc.footer = "Fonti: Il Post · Milano Città Stato · Varesenews"
    elif i == 6:
        sc.add(Text("Perché Milano\n*simpatizzava*\ncon loro?", (540, 330), a, size=92, anchor="ma", align="m"))
        sc.add(Icon("van", (540, 820), a + 0.2, size=300), "pop")
        sc.add(Text("Storia completa su YouTube", (540, 1060), T("storia"), size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(90), (540, 1220), T("Fascicolo"), anim="pop", shadow=False), "hit")
        sc.footer = "Ricostruzione a scopo divulgativo"
    return sc
