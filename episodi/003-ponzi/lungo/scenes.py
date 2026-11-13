import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
import fi
from pon import *

W, H = 1920, 1080
FY = 870
F_BASE = "Fonti: Il Post · ABA Journal · History Hit · New England Historical Society"

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

def quote_card(text, who, w=760):
    im = paper(w, 300, (232, 222, 200), 6, 0.5); d = ImageDraw.Draw(im)
    t = rich_img(text, SERIF, 52, INK, RED, lh=1.05, align="m")
    if t.width > w - 60: t = t.resize((w - 60, int(t.height * (w - 60) / t.width)), Image.LANCZOS)
    im.alpha_composite(t, (int((w - t.width) / 2), 50))
    d.text((w / 2, 250), who, font=font(COURR, 24), fill=(90, 80, 70, 255), anchor="mm")
    return im

def build(i, dur, a, words):
    T = Clock(words, a); sc = Scene(dur)
    if i == 0:
        td = T("Davanti") - 0.3
        sc.add(WorldMap((560, 170, 1860, 860), [(0, (-35, 40), 7), (td - 0.2, "Boston", 40)], a, td,
                        pins=[dict(at="Boston", label="Boston", t=a + 0.4)]), "whoosh")
        sc.add(Calendar((300, 470), 250, [(a, "BOSTON · ESTATE", "1920")], a, td), "paper")
        off = sc.add(Office((140, 300, 640, FY), td, queue=[(td + 0.2, 4), (T("fila"), 18), (T("strada"), 30)], cash=[(T("soldi"), 0.3)]))
        sc.add(Pill("UNA FILA FINO IN STRADA", (1250, 230), T("fila"), T("Tutti", 1) - 0.2, size=40))
        sc.add(Pill("TUTTI CON I SOLDI IN MANO", (1250, 230), T("soldi") - 0.2, T("Nei") - 0.3, size=40, accent=True))
        sc.add(Figure([(0, 390, FY)], T("stesso") - 0.3, kind="suit", label="LO STESSO UOMO"), "pop")
        scene_cam(sc, (0, 960, 540, 1.0), (td, 960, 540, 1.0), (T("strada"), 960, 540, 1.0), (T("stesso"), 620, 560, 1.18), (T("Nei") - 0.2, 620, 560, 1.18), (T("Nei") + 0.4, 960, 540, 1.0), (dur, 960, 540, 1.0))
        sc.add(Big("$ 250.000", (1250, 470), T("duecentocinquantamila") - 0.2, size=170, color=GOLD, fnt=OSW,
                   count=(0, 250, lambda z: f"$ {int(z):,}.000".replace(",", "."), 1.4), sub="AL GIORNO · nei giorni migliori"), "hit")
        for k in range(5):
            sc.add(PIcon("dollar", (1250, 720), T("dollari") + 0.08 * k, size=110, move=(T("dollari") + 0.08 * k, 0.9, (900 + 150 * k, 760), 60)), "pop" if k % 2 == 0 else None)
        sc.footer = "Fonti: ABA Journal · History Hit · New England Historical Society · mappa Natural Earth"
    elif i == 1:
        ts = T("Il", 1) - 0.3
        sc.add(Big("+50%", (560, 430), T("cinquanta"), T("Quell") - 0.3, size=260, color=GOLD, fnt=OSW, count=(0, 50, lambda z: f"+{z:.0f}%", 1.0), sub="in 45 giorni · la promessa"), "hit")
        sc.add(ClockFace((1300, 430), 150, T("quarantacinque"), T("Quell") - 0.3, start=9, speed=6, label="45 GIORNI"), "pop")
        sc.add(Img(coupon_doc(560), (1300, 470), T("buono") - 0.2, T("Quell") - 0.3, anim="drop", rot=4), "paper")
        sc.add(Pill("IL SEGRETO?", (1300, 220), T("segreto"), T("Quell") - 0.3, size=44, accent=True))
        tq = T("Quell") - 0.3; tv = T("Vedremo") - 0.3
        sc.add(Img(person_card("CARLO PONZI", "nato in Italia", 300, 4), (420, 500), tq + 0.2, T("Questo") - 0.3, anim="drop", rot=-3), "paper")
        sc.add(Text("il suo cognome\n= il nome di una *truffa*", (960, 330), T("cognome"), T("Questo") - 0.3, size=72, maxw=900))
        sc.add(Stamp("SCHEMA\nPONZI", (1260, 640), T("truffa") - 0.1, T("Questo") - 0.3, size=90, rot=-8))
        cover = paper(520, 640, (196, 160, 104), 9, 0.7); d = ImageDraw.Draw(cover)
        d.rectangle([50, 110, 470, 310], fill=(232, 222, 200, 255), outline=INK + (255,), width=3)
        d.text((260, 145), "FASCICOLO N. 003", font=font(COUR, 32), fill=INK + (255,), anchor="ma")
        d.text((260, 200), "LO SCHEMA", font=font(TYPE, 40), fill=INK + (255,), anchor="ma")
        d.text((260, 248), "PONZI", font=font(TYPE, 56), fill=RED + (255,), anchor="ma")
        d.text((260, 360), "Boston · 1920", font=font(COURR, 26), fill=INK + (255,), anchor="ma")
        sc.add(Img(cover, (960, 520), T("Questo"), tv, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 003", (1130, 300), T("schema") + 0.2, tv, size=70, rot=-12))
        sc.add(PIcon("coin", (420, 470), T("funzionava") - 0.3, size=200, label="COME FUNZIONAVA"), "pop")
        sc.add(Icon("newspaper", (960, 470), T("smascherato") - 0.3, size=200, label="CHI LO HA SMASCHERATO"), "pop")
        sc.add(PIcon("warning", (1500, 470), T("riconoscerne") - 0.3, size=200, label="COME RICONOSCERNE UNO OGGI"), "pop")
        sc.footer = "Fonti: Il Post · History Hit · Biography · documenti: ricostruzione grafica"
    elif i == 2:
        tc = T("A") - 0.3
        sc.add(Chapter("01", "L'*emigrante*", a, tc))
        sc.add(WorldMap((760, 180, 1840, 860), [(0, (11.0, 44.0), 90), (dur, (11.2, 44.4), 110)], tc,
                        pins=[dict(at="Lugo", label="Lugo", t=T("Lugo")), dict(at="Parma", label="Parma", t=T("Parma"), side="l", color=GOLD)]), "whoosh")
        sc.add(Calendar((330, 400), 240, [(tc, "NASCITA", "1882")], tc), "paper")
        sc.add(Pill("SECONDO MOLTE RICOSTRUZIONI: LUGO", (420, 640), T("Lugo"), T("Parma"), size=30))
        sc.add(Pill("SECONDO ALTRE: PARMA", (420, 640), T("Parma"), T("Della") - 0.2, size=30, accent=True))
        sc.add(PIcon("question", (420, 680), T("Della"), size=170, label="RACCONTI NON VERIFICABILI"), "pop")
        sc.footer = "Fonti: Il Post · ABA Journal · Biography · IBTimes · mappa Natural Earth"
    elif i == 3:
        tb = T("Anni") - 0.3
        sc.add(Calendar((300, 420), 240, [(a, "NOVEMBRE", "1903")], a, tb), "paper")
        sc.add(WorldMap((560, 180, 1840, 860), [(0, (-30, 42), 9), (dur, (-30, 42), 9.5)], a, tb,
                        routes=[dict(pts=["Lugo", "Boston"], t=a + 0.3, d=2.2, icon="ship")],
                        pins=[dict(at="Lugo", label="Italia", t=a + 0.2, side="b"), dict(at="Boston", label="Boston", t=T("Boston"))]), "whoosh")
        sc.add(Big("$ 2,50", (960, 430), T("dollari") - 0.2, T("Non") - 0.2, size=230, color=GOLD, fnt=OSW, sub="in tasca · secondo il suo racconto"), "hit")
        sc.add(Figure(walk([(-100, FY), (700, FY)], tb, 300), tb, kind="man", label="CARLO PONZI"))
        sc.add(Bubble((900, 470), 110, T("inglese") - 0.2, T("Fa") - 0.1, text="INGLESE?"), "pop")
        for k, nm in enumerate(["glass", "money", "envelope", "bench"]):
            sc.add(Icon(nm, (1000 + k * 230, 470), T("lavori") + 0.35 * k, size=150), "pop")
        sc.add(Pill("LAVORI DI OGNI TIPO", (1350, 680), T("tipo"), size=40, accent=True))
        sc.footer = "Fonti: Il Post · ABA Journal · Biography · mappa Natural Earth"
    elif i == 4:
        tl_ = T("Lavora") - 0.3
        sc.add(WorldMap((120, 180, 1000, 860), [(0, "Boston", 40), (tl_ - 0.2, "Boston", 40), (tl_ + 0.6, (-72.5, 44), 60), (dur, (-72.5, 44), 62)], a,
                        routes=[dict(pts=["Boston", "Montreal"], t=a + 0.3, d=1.4, icon="train")],
                        pins=[dict(at="Boston", label="Boston", t=a + 0.1, side="r"), dict(at="Montreal", label="Montréal", t=T("Montr"), side="l")]), "whoosh")
        sc.add(PIcon("bank", (1430, 430), T("banca") - 0.2, size=300, anim="pop" if False else "pop"), "pop")
        sc.add(Pill("BANCO ZAROSSI", (1430, 640), T("Zarossi") - 0.2, size=40))
        sc.add(Pill("INTERESSI AI CLIENTI", (1250, 220), T("interessi"), T("rosso") - 0.2, size=34))
        sc.add(Pill("CONTI IN ROSSO", (1250, 220), T("rosso") - 0.2, size=34, accent=True))
        tc = T("crolla")
        sc.add(Icon(pic("bank", 300), (1430, 430), tc - 0.3, size=300, anim="shake"))
        sc.add(Stamp("CROLLA", (1430, 470), tc, size=96, rot=-10))
        sc.footer = "Fonti: Il Post · ABA Journal · History Hit · mappa Natural Earth"
    elif i == 5:
        t2 = T("Tornato") - 0.3
        sc.add(PIcon("check", (520, 420), T("assegno") - 0.5, t2, size=360), "paper")
        sc.add(Pill("ASSEGNO FALSIFICATO", (520, 630), T("falsificato") - 0.3, t2, size=40, accent=True))
        sc.add(Icon("bars", (1300, 470), T("carcere") - 0.2, t2, size=300, label="CARCERE IN CANADA"), "stamp")
        sc.add(Figure([(0, 1300, FY)], T("arrestato") - 0.2, t2, kind="police", flip=-1), "pop")
        sc.add(WorldMap((120, 180, 1100, 860), [(0, (-78, 39), 22), (dur, (-78, 39), 23)], t2,
                        routes=[dict(pts=["Montreal", "Atlanta"], t=t2 + 0.3, d=1.8, icon="train")],
                        pins=[dict(at="Montreal", label="Montréal", t=t2 + 0.2, side="r"), dict(at="Atlanta", label="Atlanta", t=T("Atlanta"), side="r")]), "whoosh")
        sc.add(Pill("CONDANNATO DI NUOVO", (1480, 260), T("condannato"), size=40, accent=True))
        sc.add(Crowd((1240, 380, 1740, 640), 8, T("emigranti") - 0.3, T("Altro") - 0.2, s=0.32, stagger=0.06))
        sc.add(Pill("EMIGRANTI FATTI ENTRARE ILLEGALMENTE", (1480, 720), T("illegalmente") - 0.3, T("Altro") - 0.2, size=30))
        sc.add(Icon("bars", (1480, 560), T("Altro"), size=260, label="CARCERE AD ATLANTA"), "stamp")
        sc.footer = "Fonti: ABA Journal · History Hit · Biography · New England Historical Society"
    elif i == 6:
        tn = T("Nel") - 0.3; th = T("Ha") - 0.3; tf = T("Finché") - 0.3
        sc.add(WorldMap((560, 180, 1840, 860), [(0, "Boston", 30), (tn, "Boston", 60)], a, tn, pins=[dict(at="Boston", label="Boston", t=a + 0.3)]), "whoosh")
        sc.add(Calendar((300, 420), 240, [(a, "DI NUOVO A", "BOSTON"), (tn + 0.2, "MATRIMONIO", "1918")], a, th), "paper")
        sc.add(Figure([(0, 760, FY)], tn + 0.2, th, kind="suit", label="CARLO PONZI"), "pop")
        sc.add(Figure([(0, 1260, FY)], tn + 0.4, th, kind="poet", flip=-1, label="ROSE MARIA GNECCO"), "pop")
        sc.add(Office((200, 360, 700, FY), th, tf, sign="UFFICIO · BOSTON"))
        sc.add(Bubble((1050, 400), 110, T("idee") - 0.2, tf, inner="magnifier"), "pop")
        sc.add(PIcon("coin", (1400, 450), T("soldo") - 0.4, tf, size=170), "pop")
        sc.add(Line((1300, 450), (1500, 450), T("soldo"), tf, RED, 14, 0.3))
        sc.add(PIcon("coupon", (1250, 500), T("tagliando") - 0.2, size=300), "hit")
        scene_cam(sc, (0, 960, 540, 1.0), (T("tagliando"), 960, 540, 1.0), (T("tagliando") + 0.9, 1200, 500, 1.4), (dur, 1220, 500, 1.45))
        sc.footer = "Fonti: Il Post · History Hit · ABA Journal · mappa Natural Earth"
    elif i == 7:
        tc = T("È") - 0.3
        sc.add(Chapter("02", "Il buono *postale*", a, tc))
        sc.add(Img(coupon_doc(620), (520, 480), tc + 0.1, anim="drop", rot=-3), "paper")
        sc.add(PIcon("bank", (1100, 330), T("compra") - 0.3, size=190, label="PAESE A"), "pop")
        sc.add(Arrow((1220, 330), (1540, 330), T("cambia") - 0.3, color=GOLD, width=8, bend=-0.15))
        sc.add(PIcon("bank", (1660, 330), T("cambia") - 0.1, size=190, label="PAESE B"), "pop")
        for k in range(3):
            sc.add(PIcon("stamp", (1560 + k * 100, 600), T("francobolli") + 0.12 * k, size=120), "pop")
        sc.add(Icon("envelope", (1300, 640), T("Serve") - 0.2, size=170, move=(T("scrive"), 1.2, (1660, 560), 120)), "whoosh")
        sc.add(Pill("CHI RISPONDE NON PAGA IL FRANCOBOLLO", (1380, 790), T("risponde") - 0.2, size=32, accent=True))
        sc.footer = "Fonti: Biography · New England Historical Society · IBTimes · schema semplificato"
    elif i == 8:
        te = T("alcuni") - 0.5; tc = T("Così") - 0.3
        sc.add(Text("Dopo la *guerra*", (110, 200), a, te, size=60))
        sc.add(Growth((200, 330, 900, 800), [100, 80, 62, 45, 34], a + 0.3, te, dur=2.0, labels={0: "1914", 4: "1920"}, color=RED))
        sc.add(Pill("VALORE DELLE MONETE EUROPEE · ANDAMENTO INDICATIVO", (560, 860 - 10), T("perso"), te, size=24))
        sc.add(WorldMap((980, 180, 1840, 860), [(0, (-30, 40), 8), (dur, (-30, 40), 8.4)], a + 0.2,
                        pins=[dict(at="Spagna", label="Europa", t=T("Europa"), side="b"), dict(at="Boston", label="Stati Uniti", t=T("Stati"), side="b")],
                        routes=[dict(pts=["Spagna", "Boston"], t=T("negli", 1) - 0.3, d=1.6, icon="envelope")]), "whoosh")
        sc.add(PIcon("coupon", (560, 450), te + 0.1, size=230, label="IN ALCUNI PAESI: COSTA MENO"), "pop")
        sc.add(Big("pochi centesimi", (560, 720), T("pochi"), size=70, color=WHITE, fnt=SERIF))
        sc.add(PIcon("stamp", (1500, 300), T("francobolli") - 0.1, size=160, label="VALGONO DI PIÙ"), "hit")
        sc.footer = "Fonti: Il Post · Biography · New England Historical Society · andamento indicativo"
    elif i == 9:
        sc.add(Figure([(0, 300, FY)], a, kind="suit", arms=[(T("affare"), "point")], label="PONZI"), "pop")
        sc.add(Bubble((460, 380), 100, T("conti") - 0.2, T("Comprare") - 0.2, text="+ $"), "pop")
        steps = [("coupon", "1 · COMPRA", T("Comprare")), ("stamp", "2 · CAMBIA", T("cambiarli")), ("dollar", "3 · DIFFERENZA", T("intascare"))]
        for k, (nm, lab, tt) in enumerate(steps):
            sc.add(PIcon(nm, (820 + k * 400, 430), tt - 0.2, size=220, label=lab), "pop")
            if k: sc.add(Arrow((620 + k * 400, 430), (700 + k * 400, 430), tt - 0.2, color=GOLD, width=8))
        sc.add(Stamp("SU CARTA", (1220, 720), T("carta"), size=80, rot=-8, color=GOLD))
        sc.footer = "Fonti: Il Post · Biography · IBTimes · schema semplificato"
    elif i == 10:
        sc.add(Text("Il *problema*", (960, 180), a, size=64, anchor="ma"))
        sc.add(PIcon("coupon", (420, 460), T("buoni") - 0.2, size=240), "pop")
        sc.add(Arrow((560, 440), (760, 440), T("solo") - 0.4, color=GOLD))
        sc.add(PIcon("dollar", (900, 380), T("denaro") - 0.2, size=170), "pop")
        sc.add(Line((800, 300), (1000, 460), T("denaro") + 0.3, None, RED, 16, 0.3))
        for k in range(6):
            sc.add(PIcon("stamp", (860 + (k % 3) * 90, 560 + (k // 3) * 100), T("francobolli") + 0.08 * k, size=100), "pop" if k % 2 == 0 else None)
        sc.add(PIcon("hourglass", (1300, 420), T("tempo") - 0.1, size=170, label="TEMPO"), "pop")
        mod = doc_typed(300, 340, "MODULI", ["richiesta", "timbro", "firma", "permesso"], footer=None, seed=21, size=26)
        sc.add(Img(mod, (1560, 440), T("carte") - 0.1, anim="drop", rot=4), "paper")
        sc.add(Pill("I COSTI SI MANGIANO IL GUADAGNO", (1420, 690), T("costi"), size=34))
        sc.add(Stamp("NON FUNZIONA", (960, 600), T("funziona") - 0.3, size=110, rot=-8))
        sc.footer = "Fonti: New England Historical Society · Biography · documento: ricostruzione grafica"
    elif i == 11:
        tc = T("Nel") - 0.3
        sc.add(Chapter("03", "La *promessa*", a, tc))
        off = sc.add(Office((120, 300, 720, FY), tc, sign="SECURITIES EXCHANGE CO."))
        sc.add(Calendar((1000, 300), 200, [(tc + 0.1, "GENNAIO", "1920")], tc + 0.1), "paper")
        sc.add(Pill("LA SOCIETÀ DI PONZI", (420, 240), T("Securities") - 0.2, size=34, accent=True))
        rec = doc_typed(560, 440, "LA PROMESSA", ["+50%", "in 45 giorni", "", "oppure", "x2 in 90 giorni"], footer="contenuto indicativo", seed=31, size=44)
        sc.add(Img(rec, (1420, 520), T("promessa") - 0.1, anim="drop", rot=-3), "paper")
        sc.add(Crowd((780, 600, 1100, FY), 5, T("risparmiatori") - 0.2, s=0.42, stagger=0.1))
        sc.add(Stamp("x2", (1600, 720), T("doppio"), size=90, rot=-10, color=GOLD))
        sc.footer = "Fonti: Il Post · History Hit · Biography · NEHS · documento: ricostruzione grafica"
    elif i == 12:
        vals = [100 * 1.5 ** k for k in range(9)] + [2680]
        tg = T("Cento") - 0.2
        sc.add(Pill("FACCIAMO UN CONTO", (960, 190), a, size=46, accent=True))
        sc.add(Growth((160, 280, 1160, 800), vals, tg, dur=T("anno") + 0.8 - tg, labels={0: "oggi", 4: "6 mesi", 9: "1 anno"}, fmt=lambda v: f"${v:,.0f}".replace(",", ".")))
        sc.add(Big("≈ $ 2.680", (1560, 360), T("duemilaseicento") - 0.2, size=120, color=GOLD, fnt=OSW, sub="da 100 dollari\n+50% ogni 45 giorni", subsize=34), "hit")
        sc.add(Text("calcolo: 100 × 1,5^(365/45)", (1560, 560), T("duemilaseicento"), size=30, fnt=COURR, color=GREY, anchor="ma"))
        sc.add(Stamp("NESSUNA ATTIVITÀ\nONESTA", (1560, 720), T("Nessuna"), size=56, rot=-8))
        sc.footer = "Calcolo Fascicolo Italia sulla promessa riportata da Il Post · History Hit · Biography"
    elif i == 13:
        sc.add(PIcon("coupon", (300, 420), a, T("Quando") - 0.3, size=260), "pop")
        sc.add(Line((180, 300), (420, 540), T("buoni") , T("Quando") - 0.3, RED, 16, 0.3))
        py = sc.add(Pyramid((560, 170, 1760, 880), [T("primi"), T("dopo") - 0.3, T("dopo") + 0.3], T("Quando") - 0.3, labels={0: "I PRIMI", 1: "CHI ARRIVA DOPO"}))
        sc.add(Pill("PAGATI DAVVERO", (300, 420), T("paga") - 0.2, T("Ma") - 0.2, size=40))
        sc.add(Pill("CON I SOLDI DEI NUOVI", (300, 420), T("denaro"), T("cuore") - 0.4, size=40, accent=True))
        sc.add(Text("i nuovi\npagano\ni *vecchi*", (300, 360), T("nuovi", 0) - 0.2, size=78, anchor="ma", align="m"))
        sc.footer = "Fonti: Il Post · ABA Journal · Poynter · schema semplificato"
    elif i == 14:
        tq = T("Ponzi") - 0.3; tm = T("Ma") - 0.3
        sc.add(Pyramid((560, 170, 1760, 880), [a, a, T("nuovi") - 0.2, T("soldi") - 0.2], a, tq, labels={0: "I PRIMI", 3: "I NUOVI"}))
        for k in range(3):
            sc.add(Figure(walk([(-80 - k * 90, FY), (300 - k * 90, FY)], a + 0.3 * k, 300), a, tq, kind=("man", "poet", "worker")[k]))
        sc.add(Bubble((300, 400), 100, a + 0.4, tq, inner="money"), "pop")
        sc.add(Img(quote_card("«Derubare Pietro\nper pagare *Paolo*»", "Carlo Ponzi, anni dopo · citazione riportata"), (960, 480), tq, tm, anim="drop", rot=-2), "paper")
        sc.add(Text("per pagare tutti servono\nsempre più *persone*", (960, 200), T("pagare", 1), size=56, anchor="ma", align="m"))
        for k, n in enumerate([2, 4, 8, 16, 32, 64]):
            sc.add(Big(str(n), (300 + k * 260, 520), T("servono") + 0.25 * k, size=90 + 14 * k, color=GOLD if k < 5 else RED, fnt=OSW), "pop" if k % 2 == 0 else None)
        sc.add(Pill("OGNI LIVELLO DEVE ESSERE PIÙ GRANDE DEL PRECEDENTE", (960, 760), T("persone") , size=30))
        sc.footer = "Fonti: Poynter · Il Post · schema semplificato"
    elif i == 15:
        tc = T("Davanti") - 0.3
        sc.add(Chapter("04", "La *febbre*", a, tc))
        sc.add(Office((80, 300, 560, FY), tc, queue=[(tc, 6), (T("traffico") - 0.2, 26)], cash=[(tc, 0.4)]))
        sc.add(Pill("FILE CHE BLOCCANO IL TRAFFICO", (1200, 230), T("traffico") - 0.3, size=40))
        sc.add(Figure(walk([(2100, FY - 40), (1500, FY - 40)], T("polizia") - 0.8, 500), T("polizia") - 0.8, kind="police", flip=-1, arms=[(T("l'ordine"), "up")]))
        sc.add(Figure(walk([(2200, FY - 40), (1700, FY - 40)], T("polizia") - 0.5, 500), T("polizia") - 0.5, kind="police", flip=-1))
        sc.add(PIcon("hourglass", (1200, 450), T("tardi") - 0.6, size=200, label="PRIMA CHE SIA TROPPO TARDI"), "pop")
        sc.footer = "Fonti: New England Historical Society · ABA Journal"
    elif i == 16:
        tr = T("I", 0) - 0.3; ts = T("Secondo") - 0.3
        sc.add(Big("$ 250.000", (960, 380), a + 0.2, tr, size=200, color=GOLD, fnt=OSW, count=(0, 250, lambda z: f"$ {int(z):,}.000".replace(",", "."), 1.6), sub="AL GIORNO · nei giorni di punta"), "hit")
        sc.add(Crowd((200, 300, 1720, FY), 64, tr, ts, s=0.26, stagger=0.02))
        sc.add(Pill("DECINE DI MIGLIAIA DI RISPARMIATORI", (960, 220), T("decine"), ts, size=44, accent=True))
        sc.add(Big("~ 15 milioni $", (960, 420), ts + 0.2, size=170, color=GOLD, fnt=OSW, count=(0, 15, lambda z: f"~ {z:.0f} milioni $", 1.4), sub="raccolti in pochi mesi · stima più citata"), "hit")
        sc.add(Pill("OGGI ≈ 200 MILIONI DI DOLLARI (STIME DELLE FONTI)", (960, 720), T("Oggi"), size=34))
        for k in range(8):
            sc.add(PIcon("dollar", (220 + k * 210, 820), ts + 0.4 + 0.1 * k, size=110), "pop" if k % 3 == 0 else None)
        sc.footer = "Fonti: ABA Journal · History Hit · IBTimes · Il Post · NEHS · hoaxes.org"
    elif i == 17:
        tv = T("Compra") - 0.3
        sc.add(Figure([(0, 300, FY)], a, kind="suit", arms=[(a + 0.3, "up")], label="PONZI MILIONARIO"), "pop")
        sc.add(PIcon("villa", (900, 470), T("villa") - 0.2, size=380), "hit")
        sc.add(Pill("VILLA A LEXINGTON", (900, 260), T("Lexington") - 0.2, size=36))
        sc.add(Pill("PISCINA RISCALDATA", (900, 720), T("piscina") - 0.2, size=34, accent=True))
        sc.add(PIcon("car", (1500, 520), T("un'auto") - 0.3, size=340, move=(T("un'auto") - 0.3, 1.2, (1460, 520), 0)), "whoosh")
        sc.add(Pill("AUTO DI LUSSO", (1480, 720), T("lusso") - 0.2, size=34))
        sc.add(Text("«ce l'ha *fatta*»", (1500, 230), T("Per"), size=56, anchor="ma"))
        sc.footer = "Fonti: Il Post · New England Historical Society · Biography"
    elif i == 18:
        sc.add(Office((80, 300, 560, FY), a, queue=[(a, 10), (T("allunga"), 30)], cash=[(a, 0.6), (T("allunga"), 0.9)]))
        sc.add(Text("i conti\nnon *tornano*", (1250, 170), a, size=60, anchor="ma", align="m"))
        sc.add(Text("ENTRATO", (760, 385), T("Ogni") - 0.2, size=36, fnt=OSW, color=WHITE))
        sc.add(Bar(760, 450, 1000, 60, [(T("Ogni") - 0.2, 0.4), (T("allunga"), 0.7)], T("Ogni") - 0.2, color=(110, 160, 100)))
        sc.add(Text("DA RESTITUIRE (+50%)", (760, 525), T("debito") - 0.2, size=36, fnt=OSW, color=WHITE))
        sc.add(Bar(760, 590, 1000, 60, [(T("debito") - 0.2, 0.6), (T("allunga"), 1.0)], T("debito") - 0.2, color=RED))
        sc.add(Pill("IL BUCO", (1500, 720), T("buco") - 0.3, size=50, accent=True))
        sc.add(Arrow((1460, 690), (1420, 640), T("buco"), color=RED))
        sc.footer = "Schema semplificato · fonti: Il Post · History Hit · Biography"
    elif i == 19:
        tc = T("È") - 0.3; tg = T("manda") - 0.6
        sc.add(Chapter("05", "Il *giornale*", a, tc))
        news = newspaper(620, 760, "BOSTON POST", "Boston · luglio 1920", "Domande\nsu *Ponzi*", "ricostruzione · titolo indicativo", seed=7)
        sc.add(Img(news, (480, 530), tc + 0.1, anim="drop", rot=-3), "paper")
        sc.add(Calendar((1000, 320), 200, [(tc, "FINE LUGLIO", "1920")], tc), "paper")
        sc.add(Figure(walk([(2100, FY), (1150, FY)], tg, 420), tg, kind="expert", carry=[(tg, "magnifier")], flip=-1, label="I CRONISTI"))
        sc.add(Figure(walk([(2200, FY), (1330, FY)], tg + 0.2, 420), tg + 0.2, kind="suit", flip=-1))
        sc.add(Img(person_card("CLARENCE BARRON", "esperto di finanza", 260, 8), (1640, 420), T("Clarence") - 0.3, anim="drop", rot=3), "paper")
        sc.footer = "Fonti: Poynter · New England Historical Society · History Hit · giornale: ricostruzione grafica"
    elif i == 20:
        tg = T("conti") - 0.6
        sc.add(Img(quote_card("«Nessuno con esperienza\nlo prenderebbe sul *serio*»", "Clarence Barron, sintesi del suo giudizio"), (960, 420), a + 0.2, tg, anim="drop", rot=-2), "paper")
        sc.add(Text("Quanti buoni servirebbero?", (960, 180), tg, size=56, anchor="ma"))
        sc.add(Text("SERVIREBBERO", (200, 295), T("servirebbero") - 0.2, size=40, fnt=OSW, color=WHITE))
        sc.add(Bar(200, 360, 1500, 90, [(T("servirebbero") - 0.2, 1.0)], T("servirebbero") - 0.2, color=GOLD))
        sc.add(Big("150.000.000+", (950, 405), T("centocinquanta") , size=70, color=INK, fnt=OSW))
        sc.add(Text("IN CIRCOLAZIONE", (200, 505), T("circolazione") - 0.2, size=40, fnt=OSW, color=WHITE))
        sc.add(Bar(200, 570, 1500, 90, [(T("circolazione") - 0.2, 0.004)], T("circolazione") - 0.2, color=RED))
        sc.add(Text("poche decine di migliaia", (240, 615), T("poche"), size=46, fnt=OSW, color=REDL, anchor="lm"))
        for k in range(5): sc.add(PIcon("coupon", (1500 + (k % 3) * 120, 760 + (k // 3) * 60), T("poche") + 0.1 * k, size=90), "pop" if k % 2 == 0 else None)
        sc.footer = "Fonti: Poynter · New England Historical Society · Il Post · cifre riportate dal Boston Post"
    elif i == 21:
        tr = T("Davanti") - 0.3
        news = newspaper(420, 520, "BOSTON POST", "Boston · 1920", "Inchiesta\nsu *Ponzi*", "ricostruzione", seed=9)
        sc.add(Img(news, (960, 500), a + 0.1, tr, anim="drop", rot=2), "paper")
        sc.add(Crowd((200, 760, 1700, FY), 14, a + 0.4, tr, s=0.4, stagger=0.05))
        sc.add(Office((80, 300, 560, FY), tr, queue=[(tr, 26)], cash=[(tr, 0.9), (T("dimostrare"), 0.3)], run_t=T("riavere") - 0.3))
        sc.add(Pill("LA CORSA A RIAVERE I SOLDI", (1250, 230), T("riavere") - 0.3, size=40, accent=True))
        sc.add(Figure([(0, 560, FY)], T("Ponzi") - 0.2, kind="suit", arms=[(T("paga"), "hold")], label="PONZI PAGA"), "pop")
        for k in range(6):
            sc.add(PIcon("dollar", (560, 640), T("paga") + 0.25 * k, size=90, move=(T("paga") + 0.25 * k, 0.9, (700 + 180 * k, 560), 100)))
        sc.add(Pill("PER GIORNI", (1250, 330), T("giorni"), size=34))
        sc.footer = "Fonti: New England Historical Society · Biography · giornale: ricostruzione grafica"
    elif i == 22:
        ts = T("Boston") - 0.4; tf = T("fiducia") - 0.5; tg = T("Ad") - 0.3
        sc.add(Text("Il colpo *finale*", (960, 180), a, ts, size=64, anchor="ma"))
        news = newspaper(520, 640, "BOSTON POST", "Boston · agosto 1920", "Il passato\ndi *Ponzi*", "ricostruzione · titolo indicativo", seed=11)
        sc.add(Img(news, (440, 520), ts, tf, anim="drop", rot=-3), "paper")
        sc.add(WorldMap((800, 200, 1820, 760), [(0, (-73, 44), 50), (dur, (-73.3, 44.5), 54)], T("canadese") - 0.3, tf,
                        pins=[dict(at="Montreal", label="Montréal", t=T("canadese")), dict(at="Boston", label="Boston", t=T("canadese") + 0.2, side="l", color=GOLD)]), "whoosh")
        sc.add(PIcon("check", (1100, 640), T("l'assegno") - 0.2, tf, size=200), "pop")
        sc.add(Icon("bars", (1500, 640), T("carcere") - 0.2, tf, size=200), "pop")
        sc.add(Office((640, 300, 1120, FY), tf, closed_t=T("consegna")))
        sc.add(Stamp("FIDUCIA\nCROLLATA", (1450, 400), T("crolla") - 0.1, tg, size=80, rot=-8))
        sc.add(Calendar((1450, 420), 220, [(tg, "AGOSTO", "1920")], tg), "paper")
        sc.add(Figure(walk([(2100, FY), (1500, FY)], tg + 0.3, 500), tg + 0.3, kind="police", flip=-1))
        sc.add(Pill("SI CONSEGNA ALLE AUTORITÀ", (1450, 700 - 40), T("consegna"), size=32, accent=True))
        sc.footer = "Fonti: Poynter · History Hit · Il Post · Biography · NEHS · giornale: ricostruzione grafica"
    elif i == 23:
        ti = T("risparmiatori") - 0.3
        sc.add(Stamp("PREMIO\nPULITZER 1921", (600, 420), T("Pulitzer") - 0.4, T("piccoli") - 0.4, size=80, rot=-6, color=GOLD))
        sc.add(Icon("newspaper", (1250, 430), a + 0.2, ti, size=280, label="BOSTON POST · SERVIZIO PUBBLICO"), "pop")
        sc.add(Crowd((200, 560, 1720, FY), 22, ti, s=0.36, stagger=0.04))
        for k in range(6):
            sc.add(PIcon("dollar", (400 + k * 240, 300), ti + 0.15 * k, size=110, move=(ti + 0.3 + 0.15 * k, 1.2, (400 + k * 240, 1200), -60)))
        sc.add(Pill("MILIONI DI DOLLARI PERSI", (960, 220), T("milioni") - 0.2, size=44, accent=True))
        sc.add(Pill("TANTI PICCOLI RISPARMIATORI", (960, 480), T("piccoli") - 0.2, size=36))
        sc.footer = "Fonti: Pulitzer 1921 (Wikipedia) · Poynter · History Hit · NEHS · Biography"
    elif i == 24:
        tc = T("Viene") - 0.3
        sc.add(Chapter("06", "Il *conto*", a, tc))
        sc.add(Icon("gavel", (520, 480), tc, size=300, anim="shake"), "stamp")
        sc.add(Calendar((1000, 340), 200, [(tc, "NOVEMBRE", "1920")], tc), "paper")
        sc.add(Big("5 ANNI", (1450, 420), T("cinque") - 0.1, size=200, color=WHITE, fnt=OSW, sub="frode postale · giustizia federale"), "stamp")
        sc.add(Icon("bars", (1450, 720), T("cinque") + 0.3, size=180), "pop")
        sc.add(Pill("NE SCONTA CIRCA 3 E MEZZO", (960, 760), T("sconta"), size=40, accent=True))
        sc.footer = "Fonti: ABA Journal · History Hit · Il Post · hoaxes.org"
    elif i == 25:
        tm = T("In") - 0.3; tf = T("viene") - 0.3
        sc.add(Text("i conti con\nla *giustizia*", (420, 220), a, T("Stato") - 0.3, size=64, anchor="ma", align="m"))
        sc.add(Icon("gavel", (420, 420), T("Stato") - 0.2, tm, size=260, anim="shake", label="MASSACHUSETTS"), "stamp")
        sc.add(Pill("PROCESSO PER FURTO", (420, 680), T("furto") - 0.2, tm, size=36))
        sc.add(Stamp("CONDANNA", (1200, 430), T("condanna") - 0.1, tm, size=90, rot=-8))
        sc.add(WorldMap((760, 180, 1840, 860), [(0, (-76, 37), 18), (dur, (-78, 33), 22)], tm,
                        routes=[dict(pts=["Boston", "Florida"], t=tm + 0.3, d=1.6, icon="train")],
                        pins=[dict(at="Boston", label="Boston", t=tm + 0.2), dict(at="Florida", label="Florida", t=T("Florida"))]), "whoosh")
        sc.add(Pill("LIBERO IN ATTESA DELL'APPELLO", (420, 300), T("libero"), tf, size=32))
        sc.add(PIcon("palm", (420, 560), T("terreni") - 0.4, size=260, label="TERRENI IN FLORIDA"), "pop")
        sc.add(Stamp("DI NUOVO\nCONDANNATO", (1300, 520), T("condannato"), size=80, rot=-8))
        sc.footer = "Fonti: ABA Journal · History Hit · IBTimes · NEHS · mappa Natural Earth"
    elif i == 26:
        tb = T("Qualche") - 0.3; tm = T("Muore") - 0.3
        sc.add(WorldMap((560, 180, 1840, 860), [(0, (-30, 35), 8), (tb, (-30, 35), 8), (tb + 1.5, (-25, 10), 6), (dur, (-30, 5), 6.2)], a,
                        routes=[dict(pts=["Boston", "Napoli"], t=T("espulso") - 0.2, d=2.0, icon="ship"), dict(pts=["Roma", "Rio"], t=tb + 0.3, d=2.2, icon="ship", color=GOLD, bend=-0.2)],
                        pins=[dict(at="Boston", label="Stati Uniti", t=a + 0.2, side="l"), dict(at="Roma", label="Italia", t=T("Italia"), side="r"),
                              dict(at="Rio", label="Rio de Janeiro", t=T("Brasile"), side="r")]), "whoosh")
        sc.add(Calendar((300, 420), 220, [(a, "ESPULSO", "1934"), (tm, "GENNAIO", "1949")], a), "paper")
        sc.add(Pill("VIVE IN POVERTÀ", (300, 660), T("povertà") - 0.2, tm, size=36, accent=True))
        sc.add(PIcon("hospital", (300, 700), tm + 0.3, size=180, label="OSPEDALE DI BENEFICENZA"), "pop")
        sc.footer = "Fonti: History Hit · IBTimes · NEHS · Biography · hoaxes.org · mappa Natural Earth"
    elif i == 27:
        tc = T("E", 0) - 0.3
        sc.add(Chapter("07", "Come riconoscerlo *oggi*", a, tc))
        sc.add(PIcon("coupon", (400, 420), tc, T("criptovalute") + 0.2, size=220, label="1920"), "pop")
        sc.add(Arrow((560, 420), (760, 420), T("cambiano"), color=GOLD))
        for k, (nm, lab, tt) in enumerate([("euro", "CRIPTOVALUTE", T("criptovalute")), ("phone", "TRADING ONLINE", T("trading")), (None, "AFFARI TRA AMICI", T("affari"))]):
            if nm: sc.add(PIcon(nm, (950 + k * 330, 420), tt - 0.2, size=200, label=lab), "pop")
            else:
                sc.add(Figure([(0, 1580, 560)], tt - 0.2, kind="man", s=0.5), "pop"); sc.add(Figure([(0, 1700, 560)], tt - 0.1, kind="suit", s=0.5, flip=-1))
                sc.add(Pill(lab, (1640, 620), tt, size=30))
        sc.add(Pill("IL MECCANISMO È SEMPRE QUELLO", (960, 780), T("meccanismo"), size=44, accent=True))
        sc.footer = "Fonti: Money.it · QuiFinanza · Biography"
    elif i == 28:
        sc.add(Text("I segnali d'*allarme*", (110, 180), a, size=64))
        sc.add(Check([(T("Primo"), "1 · Rendimenti alti, costanti, \"sicuri\""), (T("Secondo"), "2 · Guadagno vago o incomprensibile")], (110, 380), a, size=44, width=1050))
        sc.add(PIcon("chart", (1550, 420), T("rendimenti") - 0.2, T("Secondo") - 0.2, size=300), "pop")
        sc.add(Pill("NESSUN INVESTIMENTO È SENZA RISCHIO", (1550, 680), T("Nessun"), T("Secondo") - 0.2, size=30, accent=True))
        sc.add(PIcon("question", (1550, 450), T("Secondo"), size=280), "pop")
        sc.add(Pill("PAROLE TECNICHE, NESSUNA SPIEGAZIONE", (1550, 700), T("tecniche") - 0.3, size=28))
        sc.footer = "Fonti: Money.it · QuiFinanza"
    elif i == 29:
        sc.add(Text("I segnali d'*allarme*", (110, 180), a, size=64))
        sc.add(Check([(T("Terzo"), "3 · Si guadagna portando altre persone"), (T("Quarto"), "4 · Fretta: \"posti limitati\""), (T("Quinto"), "5 · La proposta arriva da un amico")], (110, 360), a, size=40, width=1000))
        sc.add(Crowd((1300, 300, 1800, 560), 7, T("portando") - 0.2, T("Quarto") - 0.2, s=0.34, stagger=0.08))
        sc.add(PIcon("hourglass", (1550, 450), T("fretta") - 0.2, T("Quinto") - 0.2, size=280, label="OFFERTA CHE SCADE"), "pop")
        sc.add(Figure([(0, 1450, 760)], T("amico") - 0.3, kind="man", s=0.62), "pop")
        sc.add(Figure([(0, 1660, 760)], T("amico") - 0.1, kind="poet", s=0.62, flip=-1, arms=[(T("amico") + 0.2, "point")]))
        sc.add(Bubble((1660, 380), 90, T("amico"), inner="money"), "pop")
        sc.add(Pill("SPESSO È UNA VITTIMA ANCHE LUI", (1550, 830 - 20), T("vittima") - 0.3, size=28, accent=True))
        sc.footer = "Fonti: Money.it · QuiFinanza"
    elif i == 30:
        tp = T("Prima") - 0.3; tch = T("Chiedere") - 0.3
        sc.add(Text("Cosa *fare*", (110, 180), a, size=64))
        sc.add(PIcon("shield_ok", (420, 520), tp, size=320), "pop")
        reg = doc_typed(520, 420, "VERIFICA", ["Società autorizzata?", "Elenchi Consob", "Elenchi Banca d'Italia", "Da dove arriva", "il guadagno?"], footer=None, seed=41, size=34)
        sc.add(Img(reg, (1000, 520), T("controllare") - 0.2, anim="drop", rot=-2), "paper")
        sc.add(Check([(T("non", 1), "Non versare altro"), (T("conservare"), "Conservare le prove"), (T("denunciare"), "Denunciare")], (1340, 380), T("sospetta") - 0.3, size=38, width=520, icon_name="shield_ok"))
        sc.add(Pill("SE SI SOSPETTA UNA TRUFFA", (1600, 250), T("sospetta") - 0.3, size=30, accent=True))
        sc.footer = "Fonti: Money.it · QuiFinanza · documento: ricostruzione grafica"
    elif i == 31:
        tc = T("Un", 0) - 0.3
        sc.add(Chapter(None, "Il *verdetto*", a, tc))
        items = [("ship", "$ 2,50 IN TASCA", T("emigrante")), ("coupon", "UN BUONO DA POCHI CENTESIMI", T("buono")),
                 ("hourglass", "+50% IN 45 GIORNI", T("promessa")), ("coin", "I NUOVI PAGANO I VECCHI", T("sistema"))]
        for k, (nm, lab, tt) in enumerate(items):
            sc.add(PIcon(nm, (330 + k * 420, 420), tt - 0.2, T("Bastano") - 0.2, size=210, label=lab), "pop")
        sc.add(Big("MILIONI IN POCHI MESI", (960, 380), T("Bastano"), size=110, color=GOLD, fnt=OSW))
        sc.add(Icon("newspaper", (760, 640), T("articoli") - 0.2, size=170), "pop")
        sc.add(Stamp("CROLLO", (1200, 640), T("crollare"), size=90, rot=-8))
        sc.footer = F_BASE
    elif i == 32:
        sc.add(Text("E *tu*?", (960, 170), a, size=80, anchor="ma"))
        sc.add(Figure([(0, 520, FY)], a + 0.2, kind="man", s=0.9), "pop")
        sc.add(Bubble((760, 400), 120, T("proposta") - 0.2, inner="money"), "pop")
        sc.add(Text("Troppo bella\nper essere *vera*?", (1300, 330), T("troppo"), size=72, anchor="ma", align="m"))
        sc.add(Pill("SCRIVILO NEI COMMENTI", (1300, 620), T("Raccontalo") - 0.2, size=40, accent=True))
        sc.add(Pill("FONTI IN DESCRIZIONE", (1300, 720), T("fonti") - 0.2, size=34))
        sc.add(Img(wordmark(80), (1300, 820), T("Iscriviti"), anim="pop", shadow=False), "hit")
        sc.footer = "Ricostruzione a scopo divulgativo · voce generata con intelligenza artificiale"
    return sc

def thumbnail(path="thumbnail.jpg"):
    im = make_bg(7).convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    Pyramid((1080, 160, 1880, 900), [-5, -5, -5, -5], -5, top_label="PONZI").draw(lay, 0.8, 1.0)
    im.alpha_composite(lay)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    place(lay, pic("coupon", 260).rotate(-12, expand=True, resample=Image.BICUBIC), (1180, 330), "mm", 1.0)
    im.alpha_composite(lay)
    t = rich_img("IL SUO NOME\nÈ DIVENTATO\nUNA *TRUFFA*", SERIF, 136, WHITE, RED, lh=1.0)
    im.alpha_composite(t, (90, 150))
    st = stamp_img("CASO 003", RED, 70, -10); im.alpha_composite(st, (760, 70))
    d = ImageDraw.Draw(im)
    d.text((100, 830), "+50% IN 45 GIORNI. MA ERA IMPOSSIBILE.", font=font(OSW, 54, 600), fill=GOLD + (255,))
    wm = wordmark(60, sub=False); im.alpha_composite(wm, (100, 960))
    im.convert("RGB").save(path, quality=92)
