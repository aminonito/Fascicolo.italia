import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from pon import *
W, H = 1080, 1920
FY = 1300

def build(i, dur, a, words):
    T = Clock(words, a); sc = Scene(dur)
    if i == 0:
        te = T("Ed") - 0.2
        sc.add(Text("Il suo *cognome*", (540, 400), a, size=96, anchor="ma", align="m"))
        sc.add(Img(person_card("CARLO PONZI", "1882 - 1949", 340, 4), (540, 820), a + 0.1, te, anim="drop", rot=-3), "paper")
        sc.add(Stamp("SCHEMA\nPONZI", (540, 1120), T("truffa") - 0.2, te, size=110, rot=-9))
        sc.add(WorldMap((90, 600, 990, 1320), [(0, (11.5, 43.5), 70), (dur, (11.5, 43.5), 76)], te,
                        pins=[dict(at="Lugo", label="ITALIA", t=te + 0.3, side="r")], title="mappa: Natural Earth"), "whoosh")
        sc.add(Stamp("CASO 003", (800, 1240), T("italiano"), size=60, rot=-10))
        sc.footer = "Fonti: Il Post · ABA Journal · History Hit"
    elif i == 1:
        tc = T("Carlo") - 0.2; tb = T("grazie") - 0.2
        sc.add(Calendar((540, 760), 320, [(a, "BOSTON", "1920")], a, tc), "paper")
        sc.add(Img(person_card("CARLO PONZI", "Boston, 1920", 340, 4), (540, 800), tc, T("cinquanta") - 0.2, anim="drop", rot=3), "paper")
        sc.add(Big("+50%", (540, 640), T("cinquanta") - 0.1, tb, size=220, color=GOLD, fnt=OSW, count=(0, 50, lambda z: f"+{z:.0f}%", 1.0), sub="la promessa"), "hit")
        sc.add(ClockFace((540, 1040), 150, T("quarantacinque") - 0.2, tb, start=9, speed=6, label="IN 45 GIORNI"), "pop")
        sc.add(Img(coupon_doc(760), (540, 860), tb, anim="drop", rot=-4), "paper")
        sc.add(Pill("UN BUONO DELLE POSTE", (540, 1200), T("buono"), size=46, accent=True))
        sc.footer = "Fonti: Il Post · History Hit · Biography"
    elif i == 2:
        tn = T("Nei") - 0.3
        sc.add(Office((60, 820, 520, FY), a, queue=[(a, 6), (T("strada") - 0.3, 16)], cash=[(a, 0.3), (tn, 0.8)], s=0.40))
        sc.add(Pill("FILE FINO IN STRADA", (540, 440), T("file") - 0.2, tn, size=50))
        sc.add(Big("$ 250.000", (540, 600), tn + 0.1, size=150, color=GOLD, fnt=OSW, count=(0, 250, lambda z: f"$ {int(z):,}.000".replace(",", "."), 1.4), sub="AL GIORNO\nnei giorni migliori", subsize=44), "hit")
        scene_cam(sc, (0, 540, 960, 1.0), (dur, 540, 960, 1.06))
        sc.footer = "Fonti: ABA Journal · History Hit · NEHS"
    elif i == 3:
        tp = T("primi") - 0.3
        sc.add(Stamp("IL GUADAGNO\nNON ESISTE", (540, 620), a, tp, size=100, rot=-8))
        sc.add(Pyramid((60, 420, 1020, 1300), [tp + 0.1, T("dopo") - 0.4, T("dopo")], tp, labels={0: "I PRIMI", 2: "I NUOVI"}))
        sc.add(Pill("I NUOVI PAGANO I VECCHI", (540, 400), T("soldi") - 0.2, size=48, accent=True))
        sc.footer = "Fonti: Il Post · Poynter · schema semplificato"
    elif i == 4:
        tn = T("servirebbero") - 0.3
        news = newspaper(620, 760, "BOSTON POST", "Boston · 1920", "I conti\ndi *Ponzi*", "ricostruzione · titolo indicativo", seed=7)
        sc.add(Img(news, (540, 860), a, tn, anim="drop", rot=-3), "paper")
        sc.add(Text("SERVIREBBERO", (100, 560), tn, size=50, fnt=OSW))
        sc.add(Bar(100, 630, 880, 120, [(tn, 1.0)], tn, color=GOLD))
        sc.add(Big("150.000.000+", (540, 690), T("centocinquanta") - 0.2, size=84, color=INK, fnt=OSW))
        sc.add(Pill("BUONI", (540, 820), T("buoni"), size=40))
        sc.add(Text("IN CIRCOLAZIONE", (100, 915), T("circolano") - 0.2, size=50, fnt=OSW))
        sc.add(Bar(100, 1000, 880, 120, [(T("circolano") - 0.2, 0.005)], T("circolano") - 0.2, color=RED))
        sc.add(Text("poche decine di migliaia", (130, 1060), T("poche"), size=56, fnt=OSW, color=REDL, anchor="lm"))
        sc.footer = "Fonti: Poynter · NEHS · Il Post · ricostruzione"
    elif i == 5:
        tp = T("Ponzi") - 0.2; tm = T("muore") - 0.2
        sc.add(Office((290, 700, 790, 1200), a, tp, closed_t=a + 0.2))
        sc.add(Stamp("CROLLA", (540, 560), T("crolla") - 0.2, tp, size=110, rot=-8))
        sc.add(Icon("bars", (540, 860), tp, tm, size=440, label="CARCERE"), "stamp")
        sc.add(WorldMap((90, 560, 990, 1320), [(0, (-43.2, -22.9), 16), (dur, (-43.2, -22.9), 18)], tm,
                        pins=[dict(at="Rio", label="Rio de Janeiro", t=tm + 0.3, side="b")], title="mappa: Natural Earth"), "whoosh")
        sc.add(Pill("MUORE POVERO · 1949", (540, 480), T("povero") - 0.2, size=48, accent=True))
        sc.footer = "Fonti: History Hit · IBTimes · NEHS · ABA Journal"
    elif i == 6:
        ts = T("La") - 0.3
        sc.add(PIcon("warning", (540, 760), a, ts, size=380), "pop")
        sc.add(Text("Rendimenti\nalti e *sicuri*?", (540, 400), a, ts, size=92, anchor="ma", align="m"))
        sc.add(Pill("PRIMO SEGNALE D'ALLARME", (540, 1060), T("primo") - 0.1, ts, size=52, accent=True))
        sc.add(Text("Storia completa su YouTube", (540, 760), ts, size=54, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(96), (540, 940), T("Fascicolo"), anim="pop", shadow=False), "hit")
        sc.footer = "Ricostruzione divulgativa · Money.it · QuiFinanza"
    return sc
