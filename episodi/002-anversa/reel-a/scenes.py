import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from anv import *
W, H = 1080, 1920
FY = 1300

def build(i, dur, a, words):
    T = Clock(words, a); sc = Scene(dur)
    if i == 0:
        sc.add(Text("Il colpo\ndel *secolo*", (540, 400), a, size=110, anchor="ma", align="m"))
        sc.add(AIcon("sandwich", (540, 1000), T("panino") - 0.2, size=560), "hit")
        sc.add(Stamp("CASO 002", (820, 1280), T("salame"), size=64, rot=-10))
        scene_cam(sc, (0, 540, 960, 1.0), (T("panino"), 540, 960, 1.0), (dur, 540, 980, 1.08))
        sc.footer = "Ricostruzione · fonti: Wikipedia, NatGeo, Money.it"
    elif i == 1:
        ts = T("Sotto") - 0.3
        sc.add(Calendar((540, 760), 300, [(a, "ANVERSA · FEBBRAIO", "2003")], a, ts), "paper")
        tw = T("In") - 0.3
        sc.add(Cutaway((90, 560, 990, 1300), ts, tw, hl=[(T("caveau"), "vault")]))
        sc.add(Pill("10 LIVELLI DI SICUREZZA", (540, 420), T("dieci"), size=46, accent=True))
        sc.add(Boxes((110, 560, 970, 1220), 7, 8, tw + 0.1, open_t=T("svuotano"), n_open=40, rate=20, counter=(540, 1320)))
        sc.footer = "Ricostruzione · schema non in scala"
    elif i == 2:
        tp = T("inganna") - 0.3
        sc.add(Pill("SECONDO LE RICOSTRUZIONI", (540, 400), a, size=36, accent=True))
        sc.add(Sensor("sensor", (740, 700), a + 0.1, tp, size=280, off_t=T("lacca") + 0.6), "pop")
        sc.add(AIcon("spray", (300, 960), T("lacca") - 0.4, tp, size=240), "pop")
        sc.add(Spray((360, 880), (700, 720), T("lacca") - 0.2, dur=1.2))
        sc.add(Pill("LACCA PER CAPELLI", (300, 1140), T("lacca"), tp, size=40))
        sc.add(VaultDoor((440, 900), 260, tp, plates_t=tp + 0.1, foil_t=T("alluminio")))
        sc.add(AIcon("foil", (870, 760), T("alluminio") - 0.2, size=190), "pop")
        sc.add(AIcon("tape", (870, 1050), T("nastro"), size=170), "pop")
        sc.footer = "Fonti: Wikipedia · Money.it · Forbes Italia"
    elif i == 3:
        tm = T("Poi") - 0.3
        sc.add(Big("~100 mln $", (540, 640), a, tm, size=170, color=GOLD, fnt=OSW, count=(0, 100, lambda z: f"~{z:.0f} mln $", 1.2), sub="bottino stimato · cifra più citata"))
        for k in range(5):
            sc.add(AIcon("diamond", (180 + 180 * k, 1000), a + 0.3 + 0.1 * k, tm, size=150), "pop" if k % 2 == 0 else None)
        for k in range(4): sc.add(AIcon("tree", (140 + k * 270, 1080), tm + 0.08 * k, size=330))
        sc.add(AIcon("trashbag", (540, 1200), T("prove") - 0.2, size=260), "pop")
        sc.add(Pill("UN BOSCO LUNGO L'AUTOSTRADA E19", (540, 520), T("bosco"), size=36))
        sc.footer = "Fonti: Wikipedia · Money.it · NatGeo"
    elif i == 4:
        td = T("Dentro") - 0.3
        sc.add(Figure([(0, 320, FY)], a, td, kind="man", label="IL PROPRIETARIO"))
        sc.add(Figure([(0, 800, FY)], T("polizia") - 0.2, td, kind="police", flip=-1), "pop")
        for k in range(3): sc.add(AIcon("trashbag", (440 + k * 150, 1220), a + 0.2 + 0.1 * k, td, size=150))
        fat = doc_typed(560, 330, "FATTURA", ["intestata a:", "*L. Notarbartolo*"], footer=None, seed=32, size=40)
        sc.add(AIcon("trashbag", (540, 820), td + 0.1, T("fattura") + 0.3, size=420), "pop")
        sc.add(Pill("NEI SACCHI:", (540, 480), td + 0.2, size=44, accent=True))
        sc.add(Img(fat, (540, 740), T("fattura"), anim="drop", rot=-3), "paper")
        sc.add(AIcon("sandwich", (540, 1060), T("panino") - 0.1, size=420), "pop")
        sc.add(Pill("MANGIATO A METÀ", (540, 1300), T("metà") - 0.2, size=44, accent=True))
        sc.footer = "Fonti: Money.it · Forbes Italia · La Capital · documento ricostruito"
    elif i == 5:
        tm = T("Ma") - 0.3
        sc.add(Icon("gavel", (540, 700), a, tm, size=300, anim="shake"), "stamp")
        sc.add(Big("10 ANNI", (540, 1020), T("dieci"), tm, size=180, color=WHITE, fnt=OSW))
        for k in range(6):
            x0 = 240 + (k % 3) * 300; y0 = 700 + (k // 3) * 300
            sc.add(AIcon("diamond", (x0, y0), tm + 0.05 * k, None, size=180, move=(T("mai") + 0.08 * k, 1.0, (x0, -300), 0)), "pop" if k % 2 == 0 else None)
        sc.add(Stamp("MAI\nRITROVATI", (540, 1000), T("ritrovati") - 0.2, size=100, rot=-8))
        sc.footer = "Fonti: Wikipedia · Money.it"
    elif i == 6:
        sc.add(Text("Dove sono\n*finiti*?", (540, 470), a, size=110, anchor="ma", align="m"))
        sc.add(AIcon("diamond", (540, 880), a + 0.2, size=260), "pop")
        sc.add(Text("Storia completa su YouTube", (540, 1100), T("storia"), size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(90), (540, 1260), T("Fascicolo"), anim="pop", shadow=False), "hit")
        sc.footer = "Ricostruzione a scopo divulgativo"
    return sc
