import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from vg import *

W, H = 1920, 1080
FY = 870
MB = (260, 160, 1660, 880)      # scenografia esterna: il museo
SB = (200, 165, 1720, 875)      # scenografia interna: la sala con i due dipinti
MAPB = (160, 160, 1760, 880)
MT = "mappa: Natural Earth · schema non in scala"
F_OPERE = "Fonti: Il Post · Sky TG24 · Finestre sull'Arte · Al Jazeera"
F_NOTTE = "Fonti: NOS · The Week · Smithsonian · Malay Mail (AFP)"
F_IND = "Fonti: NOS · Smithsonian · NZ Herald · Al Jazeera"
F_DUR = "Fonti: NL Times · Malay Mail (AFP) · NZ Herald"
F_RIT = "Fonti: Sky TG24 · Smithsonian · Il Post · L'Adige · NOS"
F_RIT2 = "Fonti: Sky TG24 · Finestre sull'Arte · The Week · The Art Newspaper"
GY = 793                        # suolo della scenografia esterna
ROOF = 505                      # tetto del primo piano

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
        ts = T("Sette") - 0.3; tb = T("È") - 0.3; td = T("Due") - 0.3; tsa = T("Salgono") - 0.3; tp = T("e", 1) - 0.2
        sc.add(MapEl(MAPB, [(a, (6.0, 50.0), 150), (ts, "Amsterdam", 420)], a, tb + 0.3,
                     pins=[dict(at="Amsterdam", label="AMSTERDAM", t=a + 0.5, side="r", color=RED)], title=MT))
        sc.add(Calendar((360, 420), 220, [(ts, "DICEMBRE", "7"), (ts + 0.8, "DICEMBRE 2002", "7")], ts, tb + 0.3), "paper")
        sc.add(Museo(MB, tb, None, ladder_t=T("scala") - 0.2, window_t=T("rompono"), rope_t=None), "whoosh")
        sc.add(Pill("È ANCORA BUIO", (960, 210), tb + 0.2, td, size=46, accent=True))
        sc.add(Figure(walk([(200, GY), (400, GY)], td, 300), td, tsa + 0.2, kind="man", s=0.55), "pop")
        sc.add(Figure(walk([(150, GY), (350, GY)], td + 0.2, 300), td, tsa + 0.2, kind="man", s=0.55))
        sc.add(Figure([(tsa, 440, GY), (tsa + 1.0, 450, ROOF), (tsa + 2.0, 640, ROOF)], tsa, tp + 0.4, kind="man", s=0.55))
        sc.add(Icon("sledge", (1300, 330), T("rompono") - 0.2, tp, size=160), "hit")
        sc.add(Icon("vg_sea", (760, 330), tp, size=260), "pop")
        sc.add(Icon("vg_church", (1160, 330), tp + 0.4, size=260), "pop")
        sc.add(Pill("DUE QUADRI DI VINCENT VAN GOGH", (960, 520), T("Vincent") - 0.2, size=46, accent=True))
        sc.footer = F_NOTTE + " · schema non in scala"
    elif i == 1:
        tp = T("Poi") - 0.3; te = T("E") - 0.3; ts = T("Sono", 0) - 0.3; tav = T("avvolti") - 0.3
        sc.add(Icon("stopwatch", (960, 470), a, tp, size=360), "pop")
        sc.add(Big("3:40", (960, 760), a + 0.6, tp, size=110) if False else Pill("CIRCA 3 MINUTI E 40 SECONDI", (960, 760), a + 0.6, tp, size=48, accent=True))
        sc.add(Text("secondo il racconto di uno dei ladri", (960, 230), a + 0.2, tp, size=34, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Calendar((960, 470), 300, [(tp, "2002", "DIC"), (tp + 0.7, "2006", "…"), (tp + 1.3, "2011", "…"), (tp + 1.9, "2016", "SET")], tp, te), "paper")
        sc.add(Pill("QUASI 14 ANNI", (960, 780), tp + 0.4, te, size=48, accent=True))
        sc.add(MapEl((560, 160, 1360, 880), [(te, (9.5, 46.6), 56), (tav - 0.2, "Castellammare", 260)], te, None,
                     pins=[dict(at="Amsterdam", label="AMSTERDAM", t=te + 0.1, side="r", color=GOLD),
                           dict(at="Castellammare", label="CASTELLAMMARE", t=ts + 0.5, side="l", color=RED)],
                     routes=[dict(pts=["Amsterdam", "Milano", "Napoli", "Castellammare"], t=ts, d=1.6, icon="painting", color=RED)], title=MT))
        sc.add(Icon("bundle", (1620, 470), tav, size=240, label="AVVOLTI IN UN PANNO"), "hit")
        sc.footer = "Fonti: The Week · Malay Mail (AFP) · Sky TG24 · Smithsonian · " + MT
    elif i == 2:
        tv = T("Vedremo") - 0.3
        sc.add(Img(cover_folder(), (960, 500), a, tv, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 013", (1150, 300), T("fascicolo") + 0.2, tv, size=70, rot=-12))
        items = [("vg_sea", "I DUE QUADRI", "quadri"), ("ladder", "LA NOTTE DEL TETTO", "notte"), ("cap", "IL BERRETTO", "berretto"),
                 ("hourglass", "14 ANNI DI BUIO", "quattordici"), ("gdf", "L'INCHIESTA", "un'inchiesta")]
        for k, (ic, lab, w_) in enumerate(items):
            sc.add(Icon(ic, (280 + k * 340, 470), T(w_) - 0.3, size=190, label=lab), "pop")
        sc.add(Icon("museum", (960, 760), T("museo") - 0.3, size=150), "pop")
        sc.footer = "Fonti: Il Post · NOS · Sky TG24 · The Week"
    elif i == 3:
        tc = T("Non") - 0.6; ti = T("i", 1) - 0.3; ts = T("Sono") - 0.3; tm = T("il", 1) - 0.3
        sc.add(Chapter("01", "I due *quadri*", a, tc))
        sc.add(Figure([(tc, 500, FY)], tc, ti, kind="man", s=0.7, label="I LADRI?"), "pop")
        sc.add(Stamp("NO", (500, 400), T("Non") + 0.1, ti, size=80, rot=-8))
        sc.add(Icon("vg_sea", (1100, 470), ti, ts, size=300), "pop")
        sc.add(Icon("vg_church", (1460, 470), ti + 0.3, ts, size=300), "pop")
        sc.add(MapEl(MAPB, [(ts, (5.0, 52.0), 260), (tm, "Amsterdam", 700)], ts, None,
                     pins=[dict(at="Amsterdam", label="AMSTERDAM", t=ts + 0.3, side="r", color=RED)], title=MT))
        sc.add(Icon("museum", (1300, 420), ts + 0.6, size=240, label="MUSEO VAN GOGH"), "pop")
        sc.add(Pill("LA PIÙ GRANDE RACCOLTA DI VAN GOGH AL MONDO", (960, 220), tm, size=42, accent=True))
        sc.footer = "Fonti: Il Post · NOS · " + MT
    elif i == 4:
        tsch = T("la") - 0.3; td = T("dipinta") - 0.3; tm = T("Un") - 0.3
        sc.add(MapEl((160, 160, 900, 880), [(a, "Scheveningen", 900)], a, td,
                     pins=[dict(at="Scheveningen", label="SCHEVENINGEN", t=tsch, side="r", color=RED),
                           dict(at="Amsterdam", label="AMSTERDAM", t=a + 0.3, side="r", color=GOLD)], title=MT))
        sc.add(Img(framed("sea", 360), (1340, 460), a + 0.2, anim="drop"), "paper")
        sc.add(Text("sagoma stilizzata, non l'opera", (1340, 700), a + 0.4, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Calendar((530, 470), 260, [(td, "1882", "AGO")], td, None), "paper")
        sc.add(Pill("MARE GRIGIO E AGITATO", (1340, 790), tm, T("sotto") - 0.2, size=44))
        sc.add(Pill("CIELO DA TEMPESTA", (1340, 790), T("sotto") - 0.2, size=44, accent=True))
        sc.footer = F_OPERE + " · " + MT
    elif i == 5:
        tsi = T("Si") - 0.3; tch = T("dove") - 0.7; tq = T("e", 1) - 0.3
        sc.add(MapEl((160, 160, 900, 880), [(a, "Nuenen", 700)], a, tsi + 0.3,
                     pins=[dict(at="Nuenen", label="NUENEN", t=a + 0.3, side="r", color=RED),
                           dict(at="Amsterdam", label="AMSTERDAM", t=a + 0.5, side="r", color=GOLD)], title=MT))
        sc.add(Img(framed("church", 420), (1340, 470), a + 0.2, anim="drop"), "paper")
        sc.add(Text("sagoma stilizzata, non l'opera", (1340, 740), a + 0.4, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Img(label_card(["Vincent van Gogh", "Una congregazione lascia", "la chiesa riformata di Nuenen"], 600, title="SCHEDA DELL'OPERA"), (530, 470), tsi, tch, anim="drop", rot=-2), "paper")
        sc.add(Figure([(tch, 420, FY)], tch, None, kind="suit", s=0.7, label="IL PADRE: PASTORE"), "pop")
        sc.add(Icon("house", (700, 500), tq, size=200, label="PER I GENITORI"), "pop")
        sc.footer = F_OPERE + " · " + MT
    elif i == 6:
        tma = T("ma") - 0.3; te = T("E") - 0.3; tq = T("Quanto") - 0.3; tl_ = T("Le") - 0.3
        sc.add(Pill("OPERE GIOVANILI", (960, 220), a, te, size=46, accent=True))
        sc.add(Icon("easel", (700, 520), a + 0.2, te, size=320), "pop")
        sc.add(Figure([(tma, 1200, FY)], tma, te, kind="painter", s=0.8, label="IL PITTORE AGLI INIZI"), "pop")
        sc.add(Img(framed("sea", 200), (700, 560), te, tq, anim="drop"), "paper")
        sc.add(Img(framed("church", 240), (1000, 560), te + 0.3, tq, anim="drop"))
        sc.add(Figure([(te, 1350, FY)], te, tq, kind="man", s=0.8), "pop")
        sc.add(Pill("TELE PICCOLE", (960, 220), te, tq, size=46))
        sc.add(Text("proporzioni indicative · sagome stilizzate", (960, 290), te + 0.3, tq, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Icon("question", (960, 460), tq, tl_, size=260), "pop")
        sc.add(Icon("money", (700, 480), tl_, size=220), "pop")
        sc.add(Bar(1000, 440, 600, 70, [(tl_ + 0.3, 0.3), (T("fino") + 0.2, 1.0)], tl_, None, color=RED))
        sc.add(Text("LE STIME", (1000, 390), tl_, size=36, fnt=OSW, color=RED, anchor="lm"))
        sc.add(Pill("DA DECINE DI MILIONI A CIRCA 100 MILIONI", (960, 680), T("da") - 0.2, size=44, accent=True))
        sc.add(Text("stime non concordi tra le fonti", (960, 760), T("da"), size=26, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: Sky TG24 · L'Adige · Al Jazeera · Il Post"
    elif i == 7:
        tc = T("È") - 0.6; tm = T("chiuso") - 1.0; td = T("Dentro") - 0.3
        sc.add(Chapter("02", "La notte del *tetto*", a, tc))
        sc.add(Calendar((330, 420), 220, [(tc, "DICEMBRE 2002", "6"), (tc + 0.8, "DICEMBRE 2002", "7")], tc, None), "paper")
        sc.add(ClockFace((330, 720), 110, tc + 0.4, None, start=5.0, speed=0.4), None)
        sc.add(Museo((560, 170, 1760, 870), tm, td + 0.2, lights=[(tm + 0.5, (.5, .62))]), "whoosh")
        sc.add(Pill("MUSEO CHIUSO", (1160, 220), tm + 0.3, td, size=44, accent=True))
        sc.add(Sala((560, 170, 1760, 870), td, None, night=True, torch=td, label="schema semplificato · non in scala"), "whoosh")
        sc.add(Icon("camera", (760, 300), T("telecamere") - 0.2, size=130), "pop")
        sc.add(Icon("sensor", (1160, 300), T("i", 0) - 0.1, size=130), "pop")
        sc.add(Figure([(T("guardiani") - 0.2, 1500, 850), (dur, 1300, 850)], T("guardiani") - 0.2, None, kind="guard", s=0.55), "pop")
        sc.footer = F_NOTTE + " · schema non in scala"
    elif i == 8:
        ta = T("Arrivano") - 0.3; tl_ = T("La") - 0.3; ts = T("e", 0) - 0.3; ti = T("In") - 0.3
        sc.add(Museo(MB, a, None, ladder_t=tl_ + 0.3))
        sc.add(Pill("SECONDO LE RICOSTRUZIONI: DUE LADRI", (960, 210), a + 0.2, ta, size=44, accent=True))
        sc.add(Figure(walk([(120, GY), (400, GY)], ta, 200), ta, None, kind="man", s=0.55, label="LADRO 1"), "pop")
        sc.add(Figure(walk([(80, GY), (330, GY)], ta + 0.3, 200), ta, ts + 1.0, kind="man", s=0.55))
        sc.add(Icon("ladder", (960, 330), ta + 0.4, tl_, size=200, label="UNA SCALA"), "pop")
        sc.add(Figure([(ts, 330, GY), (ts + 1.2, 450, ROOF)], ts, None, kind="man", s=0.55))
        sc.add(Pill("IL TETTO DEL PRIMO PIANO", (960, 210), ts, ti, size=44, accent=True))
        sc.add(Icon("rope", (1150, 300), ti, size=160, label="CORDA"), "pop")
        sc.add(Icon("sledge", (1420, 300), T("mazza") - 0.2, size=160, label="MAZZA"), "pop")
        sc.footer = F_NOTTE + " · schema non in scala"
    elif i == 9:
        te = T("Entrano") - 0.3; tg = T("guardiano") - 0.5; tma = T("Ma,") - 0.3; tc = T("Chiama") - 0.3
        sc.add(Sala(SB, a, None, gone={0: T("staccano") + 0.3, 1: T("staccano") + 0.8}, window_t=a + 0.4))
        sc.add(Flash(a + 0.4))
        sc.add(Icon("sledge", (1580, 520), a, te, size=180), "hit")
        sc.add(Figure([(te, 1640, 830), (te + 1.4, 900, 830)], te, tg + 0.5, kind="man", s=0.6), "pop")
        sc.add(Figure([(tg, 300, 830), (tg + 1.0, 520, 830)], tg, None, kind="guard", s=0.6, label="GUARDIANO"), "pop")
        sc.add(Pill("NIENTE USO DELLA FORZA", (960, 210), tma, tc, size=44, accent=True))
        sc.add(Text("secondo le cronache", (960, 270), tma, tc, size=26, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Icon("phone", (960, 260), tc, size=160, label="CHIAMA LA POLIZIA"), "pop")
        sc.footer = F_NOTTE + " · schema non in scala"
    elif i == 10:
        ts_ = T("Si") - 0.3; tu = T("Uno") - 0.3; tn = T("Nell'urto,") - 0.3
        sc.add(Museo(MB, a, tn + 0.2, ladder_t=a, window_t=a, rope_t=ts_))
        sc.add(Stamp("NON DALLA SCALA", (560, 300), a + 0.4, ts_, size=56, rot=-6))
        sc.add(Figure([(ts_ + 0.8, 1520, 400), (tu + 0.6, 1520, GY)], ts_ + 0.6, tn + 0.2, kind="man", s=0.55))
        sc.add(Flash(tu + 0.6))
        sc.add(Icon("vg_sea", (1200, 600), T("cade") - 0.2, tn + 0.2, size=180), "pop")
        sc.add(Img(framed("sea", 360, torn=True), (960, 470), tn, anim="drop"), "hit")
        sc.add(Arrow((620, 760), (790, 620), tn + 0.6, color=RED))
        sc.add(Pill("ANGOLO IN BASSO A SINISTRA", (620, 800), tn + 0.6, size=40, accent=True))
        sc.add(Text("schema · sagoma stilizzata, non l'opera", (960, 220), tn + 0.2, size=26, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: The Week · Malay Mail (AFP) · Sky TG24 · Smithsonian · schema non in scala"
    elif i == 11:
        tn = T("Nessuno") - 0.3; ta = T("Anni") - 0.3
        sc.add(Museo(MB, a, ta, ladder_t=a, window_t=a, rope_t=a, police_t=a + 0.3))
        sc.add(Pill("I LADRI SONO GIÀ SPARITI", (960, 210), T("i") - 0.2, ta, size=46, accent=True))
        sc.add(Stamp("NESSUNO\nLI FERMA", (1160, 470), tn, ta, size=70, rot=-8))
        sc.add(Icon("stopwatch", (960, 470), ta, size=340), "pop")
        sc.add(Big("3' 40\"", (960, 770), T("circa") - 0.2, size=90) if False else Pill("CIRCA 3 MINUTI E 40", (960, 770), T("circa") - 0.2, size=52, accent=True))
        sc.add(Text("secondo il ladro, anni dopo", (960, 230), ta + 0.3, size=30, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: NOS · The Week · Malay Mail (AFP) · schema non in scala"
    elif i == 12:
        tt = T("Tre") - 0.3; tq = T("I") - 0.3; tc = T("Circa") - 0.3; tp = T("Per") - 0.3
        sc.add(Text("Fermiamoci\nun *attimo*", (960, 400), a, tt, size=100, anchor="ma", align="m"))
        sc.add(Img(label_card(["3 min 40 s", "= 3 × 60 + 40", "= 220 secondi"], 560, title="IL CALCOLO"), (560, 480), tt, tp, anim="drop", rot=-2), "paper")
        sc.add(Img(label_card(["dal 7/12/2002 al 26/9/2016", "= 5.042 giorni", "= circa 435 mln di secondi"], 640, title="L'ASSENZA"), (1340, 480), tq, tp, anim="drop", rot=2), "paper")
        sc.add(Pill("CIRCA 5.000 GIORNI", (1340, 760), tc, tp, size=44, accent=True))
        sc.add(Bar(260, 380, 1400, 80, [(tp + 0.2, 0.012)], tp, None, color=GOLD))
        sc.add(Text("IL FURTO: 220 SECONDI", (260, 330), tp, size=36, fnt=OSW, color=GOLD, anchor="lm"))
        sc.add(Bar(260, 560, 1400, 80, [(tp + 0.6, 1.0)], tp, None, color=RED))
        sc.add(Text("L'ASSENZA: CIRCA 435 MILIONI DI SECONDI", (260, 510), tp + 0.4, size=36, fnt=OSW, color=RED, anchor="lm"))
        sc.add(Pill("1 SECONDO DI FURTO = QUASI 2 MILIONI DI SECONDI DI ASSENZA", (960, 760), T("quasi") - 0.2, size=40, accent=True))
        sc.add(Text("calcolo nostro, dalla data del furto a quella del ritrovamento (Python)", (960, 830), tp + 0.3, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: NOS · The Week · Il Post · calcolo nostro"
    elif i == 13:
        tc = T("La") - 0.6; tm = T("Il") - 0.3; tma = T("Ma") - 0.3
        sc.add(Chapter("03", "Il *berretto*", a, tc))
        sc.add(Img(newspaper(620, 480, "CRONACA", "8 dicembre 2002", "RUBATI DUE VAN GOGH", "Colpo notturno al museo di Amsterdam"), (960, 500), tc, tm, anim="drop", rot=-3), "paper")
        sc.add(Text("giornale ricostruito · testata generica", (960, 790), tc + 0.3, tm, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Icon("reward", (760, 470), tm, size=320), "pop")
        sc.add(Pill("RICOMPENSA: 100.000 EURO", (1250, 400), T("centomila") - 0.2, size=46, accent=True))
        sc.add(Stamp("NESSUN\nRISULTATO", (1250, 600), tma + 0.3, size=70, rot=-8))
        sc.footer = "Fonti: NOS · Al Jazeera"
    elif i == 14:
        tn = T("Nella") - 0.3; tb = T("un") - 0.3; td = T("Dentro") - 0.3; te = T("È") - 0.3
        sc.add(Figure([(a, 400, FY)], a, None, kind="expert", s=0.75, carry=[(a, "magnifier")], label="INVESTIGATORI"), "pop")
        sc.add(Text("Un *indizio*", (1100, 300), a, tb, size=100, anchor="ma", align="m"))
        sc.add(Icon("cap", (1100, 520), tb, size=320), "hit")
        sc.add(Pill("UN BERRETTO PERSO NELLA FUGA", (1100, 780), tb + 0.3, td, size=42, accent=True))
        sc.add(Icon("dna", (1500, 470), td, size=260), "pop")
        sc.add(Arrow((1240, 520), (1380, 480), td + 0.2))
        sc.add(Pill("IL LORO DNA", (1500, 720), td + 0.3, size=44, accent=True))
        sc.add(Stamp("PROVA", (1100, 300), te + 0.5, size=80, rot=-8))
        sc.footer = F_IND
    elif i == 15:
        tc = T("Circa") - 0.3; tu = T("Uno") - 0.3; tl_ = T("L'altro") - 0.3; tt = T("Tutti") - 0.3
        sc.add(Calendar((360, 450), 240, [(a, "2003", "…"), (tc, "FINE 2003", "ARRESTI")], a, None), "paper")
        sc.add(Figure([(tc, 1000, FY)], tc, None, kind="police", s=0.75), "pop")
        sc.add(Board({"d": dict(xy=(1300, 460), name="OCTAVE DURHAM", role="olandese · arrestato", t=tu, rot=-3),
                      "c": dict(xy=(1640, 460), name="IL COMPLICE", role="olandese · arrestato", t=tl_, rot=3)},
                     [("d", "c", tl_ + 0.3)], tu, None))
        sc.add(Icon("handcuffs", (720, 420), tc + 0.5, size=180), "pop")
        sc.add(Pill("TUTTI E DUE NEGANO", (1460, 760), tt, size=46, accent=True))
        sc.add(Text("schede ricostruite · nessuna foto", (1460, 230), tu + 0.3, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: NOS · Smithsonian · NZ Herald · L'Adige"
    elif i == 16:
        ti = T("Il") - 0.3; ts = T("Sulla") - 0.3; td = T("Durham,") - 0.3
        sc.add(Icon("gavel", (700, 450), a, size=300), "hit")
        sc.add(Calendar((1300, 430), 240, [(a, "2004", "CONDANNA")], a, ti), "paper")
        sc.add(Stamp("CONDANNATI", (700, 720), a + 0.6, size=76, rot=-6))
        sc.add(Icon("cap", (1180, 420), ti, ts, size=200), "pop")
        sc.add(Icon("dna", (1460, 420), ti + 0.3, ts, size=200), "pop")
        sc.add(Pill("PROVA DEL DNA > SMENTITE", (1320, 640), ti + 0.4, ts, size=42, accent=True))
        sc.add(Img(label_card(["durate diverse nelle fonti", "Durham: poco più di 2 anni", "scontati in carcere"], 600, title="LE PENE"), (1320, 500), ts, anim="drop", rot=2), "paper")
        sc.add(Icon("bars", (1680, 760), td, size=160), "pop")
        sc.footer = "Fonti: NOS · Smithsonian · The Week · Malay Mail (AFP) · NZ Herald"
    elif i == 17:
        ti = T("I") - 0.3; tn = T("Nessuno") - 0.3; tso = T("venduti") - 0.8
        sc.add(Text("Un *problema*", (960, 400), a, ti, size=110, anchor="ma", align="m"))
        sc.add(Icon("bars", (600, 470), ti, tn, size=300, label="I LADRI: IN CARCERE"), "pop")
        sc.add(Icon("frame_empty", (1320, 470), T("quadri") - 0.2, tn, size=300, label="I QUADRI: ?"), "pop")
        sc.add(Text("Dove sono\n*finiti?*", (960, 300), tn, tso, size=100, anchor="ma", align="m"))
        sc.add(Icon("money", (500, 520), tso, size=220, label="VENDUTI?"), "pop")
        sc.add(Icon("drawer", (960, 520), T("Nascosti?") - 0.2, size=220, label="NASCOSTI?"), "pop")
        sc.add(Icon("fire", (1420, 520), T("Distrutti?") - 0.2, size=220, label="DISTRUTTI?"), "pop")
        sc.footer = "Fonti: NOS · L'Adige"
    elif i == 18:
        tc = T("Nel") - 0.6; tf = T("Il", 0) - 0.3
        sc.add(Chapter("04", "Quattordici anni\ndi *buio*", a, tc))
        sc.add(Calendar((330, 450), 240, [(tc + k * 0.5, str(2003 + k * 2), "…") for k in range(7)], tc, None), "paper")
        sc.add(Sala((560, 170, 1760, 870), tc, tf + 0.2, gone={0: tc, 1: tc}, label="schema semplificato · non in scala"), "whoosh")
        sc.add(Pill("RESTA UN VUOTO", (1160, 220), T("resta") - 0.2, tf, size=44, accent=True))
        sc.add(Img(label_card(["Amsterdam 2002", "due Van Gogh", "ancora da ritrovare"], 520, title="GRANDI MISTERI DELL'ARTE"), (1160, 470), tf, anim="drop", rot=-2), "paper")
        sc.add(Icon("question", (1500, 700), tf + 0.6, size=160), "pop")
        sc.footer = "Fonti: NOS · Il Post · Al Jazeera"
    elif i == 19:
        tu = T("Un") - 0.3; tn = T("Nessun") - 0.3; ta = T("Al") - 0.3
        sc.add(Text("Il motivo è\n*semplice*", (960, 400), a, tu, size=100, anchor="ma", align="m"))
        sc.add(Icon("vg_sea", (960, 470), tu, tn, size=320), "pop")
        sc.add(Stamp("INVENDIBILE", (960, 700), T("vendere") - 0.2, tn, size=80, rot=-8))
        sc.add(Icon("museum", (500, 470), tn, ta, size=220, label="MUSEI"), "pop")
        sc.add(Icon("gavel", (960, 470), T("nessuna") - 0.2, ta, size=220, label="CASE D'ASTE"), "pop")
        sc.add(Figure([(T("nessun", 1) - 0.2, 1420, FY - 120)], T("nessun", 1) - 0.2, ta, kind="suit", s=0.7, label="COLLEZIONISTI ONESTI"), "pop")
        sc.add(Bar(460, 400, 1000, 80, [(ta + 0.4, 1.0)], ta + 0.3, None, color=GOLD))
        sc.add(Text("VALORE DELL'OPERA", (460, 350), ta, size=36, fnt=OSW, color=GOLD, anchor="lm"))
        sc.add(Bar(460, 580, 1000, 80, [(ta + 0.8, 0.07)], ta, None, color=RED))
        sc.add(Text("VENDUTO DI NASCOSTO: UNA PICCOLA PARTE", (460, 530), ta + 0.6, size=36, fnt=OSW, color=RED, anchor="lm"))
        sc.add(Text("proporzioni indicative", (960, 760), ta + 0.4, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: NZ Herald · NL Times · schema indicativo"
    elif i == 20:
        ta = T("Ammette") - 0.3; te = T("E") - 0.3; tv = T("i") - 0.3
        sc.add(Calendar((330, 430), 220, [(a, "2017", "MAR")], a, ta + 0.3), "paper")
        sc.add(Img(newspaper(600, 460, "QUOTIDIANO", "marzo 2017", "IL LADRO PARLA", "«Così abbiamo rubato i Van Gogh»"), (1000, 480), a + 0.2, te, anim="drop", rot=-3), "paper")
        sc.add(Text("giornale ricostruito · testata generica", (1000, 760), a + 0.4, te, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Stamp("AMMETTE\nIL FURTO", (1450, 300), ta, te, size=64, rot=-8))
        sc.add(MapEl((760, 160, 1560, 880), [(te, (9.5, 46.6), 56)], te, None,
                     pins=[dict(at="Amsterdam", label="TENTATIVI FALLITI IN OLANDA", t=te + 0.3, side="r", color=GOLD),
                           dict(at="Napoli", label="ITALIA", t=tv + 0.6, side="r", color=RED)],
                     routes=[dict(pts=["Amsterdam", "Milano", "Napoli"], t=tv, d=1.6, icon="painting", color=RED)], title=MT))
        sc.add(Pill("VENDUTI IN ITALIA", (400, 600), tv + 0.2, size=46, accent=True))
        sc.footer = F_DUR + " · " + MT
    elif i == 21:
        tu = T("Una") - 0.3; ts = T("ipotesi") - 1.4; tm = T("restano") - 0.5
        sc.add(Text("Perché\n*comprarli?*", (960, 380), a, tu, size=110, anchor="ma", align="m"))
        sc.add(Icon("question", (960, 470), tu, ts, size=320), "pop")
        sc.add(Icon("vg_church", (500, 470), ts, size=220, label="GRANDE VALORE"), "pop")
        sc.add(Icon("bundle", (960, 470), T("piccolo,") - 0.2, size=220, label="PICCOLO"), "pop")
        sc.add(Icon("safe", (1420, 470), T("facile") - 0.2, size=220, label="DA NASCONDERE"), "pop")
        sc.add(Stamp("SOLO IPOTESI", (960, 760), tm, size=70, rot=-6))
        sc.footer = "Ipotesi generali, non accertate per questo caso"
    elif i == 22:
        tc = T("La") - 0.6; ti = T("indaga") - 0.3; ts = T("Secondo") - 0.3
        sc.add(Chapter("05", "*Castellammare*", a, tc))
        sc.add(Calendar((330, 430), 220, [(tc, "2016", "SET")], tc, None), "paper")
        sc.add(Icon("gdf", (760, 440), tc + 0.2, size=260, label="GUARDIA DI FINANZA"), "pop")
        sc.add(Icon("court", (1160, 440), T("coordinata") - 0.2, size=240, label="PROCURA DI NAPOLI"), "pop")
        sc.add(Pill("INDAGINE SU UN CLAN DELLA CAMORRA", (960, 760), ti, ts, size=44, accent=True))
        sc.add(Icon("ship", (1560, 440), ts, size=220, label="TRAFFICO INTERNAZIONALE"), "pop")
        sc.add(Pill("SECONDO L'ACCUSA", (960, 760), ts, size=44, accent=True))
        sc.footer = "Fonti: Sky TG24 · Il Post · Smithsonian · L'Adige"
    elif i == 23:
        te = T("E") - 0.3; ti = T("i") - 0.3; td = T("Due") - 0.3
        sc.add(Icon("moneybag", (960, 450), a, te, size=300), "pop")
        sc.add(Pill("BENI SEQUESTRATI: DECINE DI MILIONI", (960, 720), a + 0.4, te, size=44, accent=True))
        sc.add(MapEl(MAPB, [(te, "Napoli", 900), (te + 1.5, "Castellammare", 1500)], te, td,
                     pins=[dict(at="Napoli", label="NAPOLI", t=te + 0.2, side="l", color=GOLD),
                           dict(at="Castellammare", label="CASTELLAMMARE DI STABIA", t=te + 0.8, side="r", color=RED)], title=MT))
        sc.add(Icon("vesuvio", (1450, 330), te + 1.0, td, size=200), "pop")
        sc.add(Figure([(ti, 400, FY), (ti + 1.5, 700, FY)], ti, None, kind="police", s=0.7, carry=[(ti, "magnifier")]), "pop")
        sc.add(Icon("bundle", (1250, 520), td, size=420), "hit")
        sc.add(Pill("SENZA CORNICE", (1100, 220), T("senza") - 0.2, size=44))
        sc.add(Pill("AVVOLTE IN UN PANNO", (1100, 800), T("avvolte") - 0.2, size=44, accent=True))
        sc.footer = "Fonti: Sky TG24 · Smithsonian · Il Post · L'Adige · " + MT
    elif i == 24:
        ts = T("parla") - 0.5; td = T("certo") - 0.6
        sc.add(Text("Dove,\n*esattamente?*", (960, 380), a, ts, size=100, anchor="ma", align="m"))
        sc.add(Icon("house", (500, 470), ts, td, size=230, label="UNA PALAZZINA"), "pop")
        sc.add(Icon("stable", (960, 470), T("casolare,") - 0.2, td, size=230, label="UN CASOLARE"), "pop")
        sc.add(Icon("crate", (1420, 470), T("magazzino.") - 0.2, td, size=230, label="UN MAGAZZINO"), "pop")
        sc.add(Stamp("FONTI NON CONCORDI", (960, 760), ts + 1.0, td, size=60, rot=-5))
        sc.add(Icon("bundle", (960, 460), td, size=380), "pop")
        sc.add(Stamp("NON APPESE\nA UNA PARETE", (960, 760), T("nessuno") - 0.2, size=60, rot=-6))
        sc.footer = "Fonti: Sky TG24 · Finestre sull'Arte · Smithsonian · Il Post"
    elif i == 25:
        tl_ = T("guarda") - 0.5; te = T("conferma") - 0.5; ti = T("30") - 0.4
        sc.add(Figure(walk([(200, FY), (700, FY)], a, 300), a, None, kind="expert", s=0.75, label="ESPERTO DEL MUSEO"), "pop")
        sc.add(Icon("bundle", (1250, 500), a, tl_ + 0.5, size=300), "pop")
        sc.add(Img(framed("sea", 260, frame=False, torn=True), (1100, 480), tl_ + 0.5, anim="drop"), "paper")
        sc.add(Img(framed("church", 300, frame=False), (1500, 480), tl_ + 0.8, anim="drop"))
        sc.add(Icon("magnifier", (900, 380), tl_, ti, size=160), "pop")
        sc.add(Stamp("AUTENTICI", (1300, 760), te + 0.4, size=76, rot=-6))
        sc.add(Calendar((330, 400), 200, [(ti, "SETTEMBRE 2016", "30")], ti, None), "paper")
        sc.add(Icon("megaphone", (560, 300), ti + 0.4, size=150), "pop")
        sc.add(Text("tele senza cornice · sagome stilizzate", (1300, 230), tl_ + 0.6, size=24, fnt=COURR, color=GREY, anchor="ma"))
        sc.footer = "Fonti: Il Post · NOS · Al Jazeera"
    elif i == 26:
        ts = T("Sorprendentemente") - 0.3; tc = T("La") - 0.3; tm = T("La", 1) - 0.3
        sc.add(Text("In che\n*condizioni?*", (960, 380), a, ts, size=100, anchor="ma", align="m"))
        sc.add(Pill("SORPRENDENTEMENTE BUONE", (960, 220), ts, tc, size=46, accent=True))
        sc.add(Img(framed("church", 400), (620, 500), tc - 0.2, anim="drop"), "paper")
        sc.add(Pill("PICCOLI DANNI AI BORDI", (620, 820), tc + 0.3, size=38))
        sc.add(Img(framed("sea", 300, torn=True), (1340, 500), tm, anim="drop"), "paper")
        sc.add(Arrow((1080, 760), (1150, 640), tm + 0.6, color=RED))
        sc.add(Pill("COLORE MANCANTE IN BASSO A SINISTRA", (1340, 820), T("il") - 0.2, size=36, accent=True))
        sc.footer = "Fonti: Sky TG24 · Smithsonian · The Week · sagome stilizzate"
    elif i == 27:
        tc = T("Prima") - 0.6; td = T("Dal") - 0.3; tdv = T("Due") - 0.3
        sc.add(Chapter("06", "Il *ritorno*", a, tc))
        sc.add(MapEl(MAPB, [(tc, "Napoli", 1200)], tc, td + 0.3,
                     pins=[dict(at="Napoli", label="NAPOLI", t=tc + 0.3, side="r", color=RED)], title=MT))
        sc.add(Calendar((360, 420), 220, [(td, "FEBBRAIO 2017", "7"), (td + 1.2, "FEBBRAIO 2017", "26")], td, None), "paper")
        sc.add(Icon("museum", (960, 450), td + 0.3, size=280, label="MUSEO DI CAPODIMONTE"), "pop")
        sc.add(Crowd((700, 650, 1700, 880), 14, tdv, None, s=0.3))
        sc.add(Icon("vg_sea", (1350, 360), tdv + 0.2, size=170), "pop")
        sc.add(Icon("vg_church", (1580, 360), tdv + 0.4, size=170), "pop")
        sc.footer = "Fonti: Sky TG24 · Finestre sull'Arte · " + MT
    elif i == 28:
        tn = T("Napoli,") - 0.3; tp = T("Poche") - 0.3; tpi = T("Più") - 0.3
        sc.add(MapEl((560, 160, 1360, 880), [(a, "Napoli", 300), (tp, (9.5, 46.6), 56)], a, tp + 0.4,
                     pins=[dict(at="Napoli", label="NAPOLI", t=a + 0.3, side="r", color=GOLD),
                           dict(at="Amsterdam", label="AMSTERDAM", t=T("Amsterdam.") - 0.2, side="r", color=RED)],
                     routes=[dict(pts=["Napoli", "Roma", "Milano", "Amsterdam"], t=tn, d=2.4, icon="painting", color=RED)], title=MT))
        sc.add(Icon("armored", (1600, 470), T("Alpi,") - 0.2, tp, size=180), "pop")
        sc.add(Sala(SB, tp, None, gone={0: tp - 1, 1: tp - 1}, back=tp + 0.6))
        sc.add(Stamp("DI NUOVO A CASA", (960, 230), tp + 1.2, size=64, rot=-5))
        sc.add(Pill("PIÙ DI 14 ANNI DOPO IL FURTO", (960, 760), tpi, size=46, accent=True))
        sc.footer = "Fonti: Finestre sull'Arte · Malay Mail (AFP) · " + MT
    elif i == 29:
        tl_ = T("tele") - 0.6; tn = T("laboratorio") - 0.6; tg = T("esperti") - 0.6; t19 = T("2019") - 0.6
        sc.add(Text("Non è *finita*", (960, 400), a, tl_, size=110, anchor="ma", align="m"))
        sc.add(Icon("lab", (500, 470), tl_, t19, size=260, label="LABORATORIO DI RESTAURO"), "pop")
        sc.add(Figure([(tn, 860, FY)], tn, t19, kind="expert", s=0.75, carry=[(tn, "magnifier")]), "pop")
        sc.add(Img(framed("sea", 360, torn=True), (1350, 470), tn, t19, anim="drop"), "paper")
        sc.add(Arrow((1100, 760), (1190, 630), tg + 0.4, t19, color=RED))
        sc.add(Pill("L'ANGOLO DANNEGGIATO", (1350, 760), tg + 0.4, t19, size=40, accent=True))
        sc.add(Sala(SB, t19, None, back=t19))
        sc.add(Calendar((1580, 330), 180, [(t19, "2019", "APR")], t19, None), "paper")
        sc.add(Crowd((400, 680, 1500, 880), 10, t19 + 1.0, None, s=0.3))
        sc.footer = "Fonti: The Week · The Art Newspaper · Van Gogh Museum · sagome stilizzate"
    elif i == 30:
        tc = T("Ricapitolando.") - 0.2; tp = T("Pochi") - 0.3; tu = T("berretto") - 0.5; tpo = T("Poi") - 0.3
        sc.add(Chapter("", "Il *verdetto*", a, tc + 1.2))
        sc.add(Icon("ladder", (500, 450), T("scala,") - 0.2, size=200, label="SCALA"), "pop")
        sc.add(Icon("rope", (960, 450), T("corda,") - 0.2, size=200, label="CORDA"), "pop")
        sc.add(Icon("sledge", (1420, 450), T("mazza.") - 0.2, size=200, label="MAZZA"), "pop")
        sc.add(Timeline(260, 1660, 760, [dict(top="DIC 2002", bottom="il furto", t=tp, hl=True),
                                         dict(top="2004", bottom="condanne", t=tu + 0.4),
                                         dict(top="SET 2016", bottom="Castellammare", t=tpo + 0.3, hl=True),
                                         dict(top="2017", bottom="Capodimonte e ritorno", t=tpo + 1.5),
                                         dict(top="2019", bottom="restaurati", t=tpo + 2.2)], tp, None))
        sc.add(Icon("cap", (700, 300), tu, size=150), "pop")
        sc.add(Icon("bundle", (1240, 300), tpo + 0.6, size=180), "pop")
        sc.footer = "Fonti: NOS · Il Post · Sky TG24 · The Week · Finestre sull'Arte"
    elif i == 31:
        ts = T("Scrivilo") - 0.3; ti = T("Iscriviti") - 0.3
        sc.add(Text("Perché tenere nascosti\nquadri *invendibili?*", (960, 300), a, ti, size=86, anchor="ma", align="m"))
        sc.add(Icon("vg_sea", (720, 600), a + 0.3, ti, size=240), "pop")
        sc.add(Icon("vg_church", (1200, 600), a + 0.5, ti, size=240), "pop")
        sc.add(Icon("question", (960, 600), a + 0.8, ti, size=160), "pop")
        sc.add(Pill("SCRIVILO NEI COMMENTI", (960, 820), ts, ti, size=44, accent=True))
        sc.add(Img(wordmark(150), (960, 480), ti, anim="pop", shadow=False), "hit")
        sc.add(Text("ogni giorno un nuovo caso", (960, 640), ti + 0.4, size=48, fnt=PS, color=GREY, anchor="ma"))
        sc.footer = "Ricostruzione a scopo divulgativo · voce generata con sintesi vocale"
    return sc

def thumbnail(path="thumbnail.jpg"):
    im = make_bg(7); d = ImageDraw.Draw(im)
    t = rich_img("I VAN GOGH\nFINITI A\n*CASTELLAMMARE*", SERIF, 118, WHITE, RED, lh=1.0)
    im.alpha_composite(t, (90, 150))
    fr = framed("sea", 300, torn=True).rotate(-6, expand=True, resample=Image.BICUBIC); im.alpha_composite(fr, (1170, 200))
    fr2 = framed("church", 330).rotate(5, expand=True, resample=Image.BICUBIC); im.alpha_composite(fr2, (1500, 400))
    b = vpic("bundle", 280); im.alpha_composite(b, (1180, 640))
    st = stamp_img("CASO 013", RED, 70, -10); im.alpha_composite(st, (1520, 90))
    d.text((100, 840), "RUBATI AD AMSTERDAM, RITROVATI QUASI 14 ANNI DOPO", font=font(OSW, 48, 600), fill=GOLD + (255,))
    d.text((1880, 1060), "sagome stilizzate, non le opere", font=font(COURR, 22), fill=(200, 190, 170, 255), anchor="rs")
    wm = wordmark(60, sub=False); im.alpha_composite(wm, (100, 960))
    im.convert("RGB").save(path, quality=92)
