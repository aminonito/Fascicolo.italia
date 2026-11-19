import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from cv import *
W, H = 1080, 1920
BB = (40, 640, 1040, 1300)
MT = "mappa: Natural Earth · schema non in scala"
GY = 1240

def build(i, dur, a, words):
    T0 = Clock(words, a)
    def T(p, n=0):
        cs = lambda s: re.sub(r"[^\w']", "", s.lower())
        hits = [w for w in words if cs(w[0]) == cs(p)]
        if hits: return a + hits[min(n, len(hits) - 1)][1]
        try: return T0(p, n)
        except KeyError: return a + 0.5
    sc = Scene(dur)
    if i == 0:
        te = T("E") - 0.3
        sc.add(Text("*17* quadri\nrubati", (540, 330), a, te, size=120, anchor="ma", align="m"))
        sc.add(Galleria(BB, a, te + 0.4, gone=a + 0.9, step=0.08, night=True, torch=a, label=""))
        sc.add(Pill("IN UNA SOLA SERA", (540, 1290), T("una") - 0.2, te, size=56, accent=True))
        sc.add(Text("Ritrovati\nsu un'*isola*", (540, 330), te, size=100, anchor="ma", align="m"))
        sc.add(Icon("island", (540, 960), te + 0.2, size=500), "hit")
        sc.add(Pill("IN UCRAINA · 6 MESI DOPO", (540, 1290), T("Ucraina") - 0.3, size=52, accent=True))
        sc.footer = "Fonti: Il Post · The Art Newspaper · AP · sagome stilizzate"
    elif i == 1:
        tu = T("2015") + 0.4; ti = T("Il") - 0.3; tl = T("e") - 0.3
        sc.add(MapEl(BB, [(a, (12.0, 43.5), 70), (a + 1.2, "Verona", 400)], a, ti + 0.2,
                     pins=[dict(at="Verona", label="VERONA", t=a + 0.8, side="r", color=RED)], title=""))
        sc.add(Calendar((540, 420), 220, [(a + 0.3, "NOVEMBRE", "19"), (tu, "2015", "19")], a, ti - 0.35), "paper")
        sc.add(Castello(BB, ti - 0.1, None, night=True, label=""), "whoosh")
        sc.add(Text("Museo di\n*Castelvecchio*", (540, 330), ti, tl, size=96, anchor="ma", align="m"))
        sc.add(ClockFace((900, 470), 110, ti + 0.2, tl, start=7.4, speed=0.05))
        sc.add(Pill("STA PER CHIUDERE", (540, 1290), ti + 0.4, tl, size=56, accent=True))
        sc.add(Icon("alarm_off", (540, 420), tl, size=300), "pop")
        sc.add(Pill("ALLARME NON ANCORA ACCESO", (540, 1290), tl + 0.1, size=50, accent=True))
        sc.footer = "Fonti: Il Post · The Art Newspaper · AP · " + MT
    elif i == 2:
        tb = T("Bloccano") - 0.3; tp = T("portano") - 0.3; tt = T("Tintoretto") - 0.2
        sc.add(Castello(BB, a, tp + 0.3, night=True, door_t=a + 0.3, label=""))
        for k in range(3):
            sc.add(Figure([(a + 0.2, 160 + k * 90, GY), (tb, 470 + k * 60, GY)], a + 0.2, tb + 0.3, kind="man", s=0.45))
        sc.add(Icon("balaclava", (540, 400), a + 0.3, tb, size=280), "pop")
        sc.add(Figure([(tb, 420, GY)], tb, tp + 0.3, kind="guard", s=0.5))
        sc.add(Figure([(tb, 660, GY)], tb, tp + 0.3, kind="man", s=0.45))
        sc.add(Icon("tape", (540, 400), tb + 0.2, tp, size=260), "hit")
        sc.add(Galleria(BB, tp, None, gone=tp + 0.6, step=0.1, label=""))
        sc.add(Big("17", (540, 420), tp, tt, size=220, color=RED))
        sc.add(Text("Tintoretto · Mantegna\nPisanello · *Rubens*", (540, 330), tt, size=70, anchor="ma", align="m"))
        sc.footer = "Fonti: Il Post · Finestre sull'Arte · The Art Newspaper · sagome stilizzate"
    elif i == 3:
        tv = T("Valore") - 0.3
        sc.add(Text("La *fuga*", (540, 330), a, tv - 0.35, size=120, anchor="ma", align="m"))
        sc.add(Castello(BB, a, tv, night=True, door_t=a, label=""))
        sc.add(Icon("car", (540, 1150), a + 0.2, tv, size=300, move=(a + 1.0, 1.4, (1150, 1150), 0)), "whoosh")
        sc.add(Pill("L'AUTO DELLA GUARDIA", (540, 1290), a + 0.4, tv, size=54, accent=True))
        sc.add(Text("circa\n*15 milioni*\ndi euro", (540, 300), tv, size=120, anchor="ma", align="m"))
        sc.add(Icon("euro", (540, 960), tv + 0.3, size=420), "hit")
        sc.add(Text("valore stimato", (540, 1250), tv + 0.6, size=36, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: Il Post · ANSA · The Art Newspaper · AP"
    elif i == 4:
        tt = T("tredici") - 0.2; tg = T("Tra", 1) - 0.3
        sc.add(Calendar((540, 520), 240, [(a, "MARZO", "2016")], a, tt), "paper")
        sc.add(MapEl(BB, [(tt, (20.0, 46.3), 46)], tt, tg + 0.3,
                     pins=[dict(at="Verona", label="VERONA", t=tt + 0.2, side="l", color=RED),
                           dict(at="Chisinau", label="MOLDAVIA", t=tt + 0.6, side="r", color=RED)],
                     routes=[dict(pts=["Verona", "Chisinau"], t=tt + 0.3, d=1.0, color=GOLD, dashed=True)], title=""))
        sc.add(Text("*13* arresti", (540, 330), tt, tg, size=120, anchor="ma", align="m"))
        sc.add(Icon("handcuffs", (540, 1180), tt + 0.4, tg, size=200), "hit")
        sc.add(Text("E tra loro\nla *guardia*", (540, 330), tg, size=110, anchor="ma", align="m"))
        sc.add(Figure([(tg, 540, 1200)], tg, None, kind="guard", s=0.9))
        sc.add(Stamp("ARRESTATA", (540, 1300), T("sera") - 0.2, size=84, rot=-8))
        sc.footer = "Fonti: L'Adige · The Art Newspaper · Il Post · " + MT
    elif i == 5:
        ts = T("un'isola") - 0.3; tav = T("avvolti") - 0.1
        sc.add(Text("Maggio *2016*", (540, 330), a, ts - 0.1, size=110, anchor="ma", align="m"))
        sc.add(MapEl(BB, [(a, (24.0, 47.0), 60), (ts, "Turunchuk", 320)], a, tav + 0.4,
                     pins=[dict(at="Chisinau", label="MOLDAVIA", t=a + 0.3, side="l", color=GOLD),
                           dict(at="Odessa", label="UCRAINA", t=a + 0.6, side="r", color=GOLD),
                           dict(at="Turunchuk", label="ISOLA SUL DNESTR", t=ts + 0.3, side="b", color=RED)], title=""))
        sc.add(Figure([(a + 0.6, 880, 1240)], a + 0.6, ts, kind="police", s=0.55, label="GUARDIE DI FRONTIERA"))
        sc.add(Text("Un'*isola*\nsul fiume", (540, 330), ts + 0.2, tav - 0.2, size=100, anchor="ma", align="m"))
        sc.add(Text("Avvolti nella\n*plastica*", (540, 330), tav + 0.1, size=100, anchor="ma", align="m"))
        sc.add(Icon("trashbag", (540, 950), tav + 0.45, size=480), "hit")
        sc.add(Stamp("RITROVATI", (540, 1300), tav + 0.6, size=90, rot=-8))
        sc.footer = "Fonti: The Art Newspaper · Kyiv Post · AP · " + MT
    elif i == 6:
        sc.add(Text("Dove dovevano\nfinire i *17*\nquadri?", (540, 300), a, size=86, anchor="ma", align="m"))
        sc.add(Galleria((90, 680, 990, 1110), a + 0.2, None, gone=a, back=a + 0.6, step=0.06, label=""))
        sc.add(Text("Storia completa su YouTube", (540, 1185), T("storia"), size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(90), (540, 1345), T("Fascicolo"), anim="pop", shadow=False), "hit")
        sc.footer = "Ricostruzione a scopo divulgativo · voce generata con sintesi vocale"
    return sc
