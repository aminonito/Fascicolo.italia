import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from par import *
import fx
W, H = 1080, 1920
FY = 1300
BB = (40, 640, 1040, 1320)
MT = "mappa: Natural Earth · schema non in scala"

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

def build(i, dur, a, words):
    T0 = Clock(words, a)
    def T(p, n=0):
        nrm = lambda s: re.sub(r"[^\w']", "", s.lower())
        cs = lambda s: re.sub(r"[^\w']", "", s)
        hits = [w for w in words if cs(w[0]) == cs(p)] or [w for w in words if nrm(w[0]) == nrm(p)]
        if hits: return a + hits[min(n, len(hits) - 1)][1]
        try: return T0(p, n)
        except KeyError: return a + 0.5
    sc = Scene(dur)
    if i == 0:
        tm = T("Ma") - 0.3
        sc.add(Text("Quasi *4 miliardi*\na New York", (540, 330), a, tm, size=96, anchor="ma", align="m"))
        sc.add(Ledger(BB, a, None, cash_t=a, gold_t=a + 0.6, fake_t=T("esisteva") - 0.1, title="schema semplificato"))
        sc.add(Text("Il conto\n*non esisteva*", (540, 330), tm, size=110, anchor="ma", align="m"))
        sc.add(Stamp("FALSO", (540, 1000), T("esisteva"), size=130, rot=-8))
        sc.footer = "Fonti: SEC · Wikipedia · AGI · schema semplificato"
    elif i == 1:
        tl_ = T("La") - 0.3; tn = T("non") - 0.3
        sc.add(Calendar((540, 900), 360, [(a, "DICEMBRE", "2003")], a, tl_ + 0.2), "paper")
        sc.add(Icon("milk", (330, 920), tl_, tn, size=380), "pop")
        sc.add(Icon("factory", (760, 920), tl_ + 0.3, tn, size=380, label="UN COLOSSO DEL LATTE"), "pop")
        sc.add(Img(bond_doc(860), (540, 900), tn, anim="drop", rot=-2), "paper")
        sc.add(Pill("150 MILIONI DA RIMBORSARE", (540, 1240), T("150") - 0.2, size=56, accent=True))
        sc.add(Stamp("NON PAGATA", (540, 950), T("milioni") + 0.3, size=110, rot=-8))
        sc.add(Text("Dicembre\n*2003*", (540, 330), a, size=110, anchor="ma", align="m"))
        sc.footer = "Fonti: Blitz quotidiano · imgpress · Wikipedia"
    elif i == 2:
        ts = T("su") - 0.3
        sc.add(Text("Eppure\nin cassa…", (540, 330), a, size=110, anchor="ma", align="m"))
        sc.add(Ledger(BB, a, ts, cash_t=a, gold_t=T("3,95") - 0.2, hl_gold=T("3,95") + 0.4, title="schema semplificato"))
        sc.add(WorldMap(BB, [(ts, (-79, 30.5), 26), (dur, (-79, 30.5), 27)], ts, None,
                        pins=[dict(at="Cayman", label="ISOLE CAYMAN", t=ts + 0.3, side="r", color=GOLD),
                              dict(at="New York", label="BANK OF AMERICA · NY", t=ts + 0.3, side="r", color=RED)],
                        routes=[dict(pts=["Cayman", "New York"], t=ts + 0.5, d=1.0, icon="money", color=RED)], title=MT))
        sc.footer = "Fonti: SEC · Wikipedia · AGI · " + MT
    elif i == 3:
        ts = T("Secondo") - 0.3
        sc.add(Calendar((540, 900), 360, [(a, "DICEMBRE 2003", "19")], a, T("risponde") - 0.1), "paper")
        sc.add(Img(confirm_letter(640), (540, 960), T("risponde") - 0.1, ts + 0.2, anim="drop", rot=-3), "paper")
        sc.add(Stamp("NON ESISTE", (540, 980), T("esiste") - 0.1, ts + 0.2, size=110, rot=-10))
        sc.add(Icon("scanner", (540, 900), ts + 0.2, size=480), "pop")
        sc.add(Pill("SECONDO LE RICOSTRUZIONI", (540, 1240), ts + 0.3, size=52, accent=True))
        sc.add(Text("La *conferma*\nera falsa", (540, 330), a, size=104, anchor="ma", align="m"))
        sc.footer = "Fonti: Wikipedia (timeline) · AGI · WSWS · imgpress"
    elif i == 4:
        td = T("Decine") - 0.3; tc = T("Calisto") - 0.3
        sc.add(Ledger(BB, a, td, cash_t=a - 5, gold_t=a - 5, fake_t=a - 5, hidden=[(a + 0.2, 1.0)], reveal_t=T("14") - 0.1, reveal_text="14 MLD €", title="schema semplificato"))
        sc.add(Text("Un buco\nda *14 miliardi*", (540, 330), a, tc, size=104, anchor="ma", align="m"))
        sc.add(Savers((80, 900, 1000, 1250), 4, td, tc, drop_t=T("senza") - 0.2, s=1.3))
        sc.add(Img(sentence_card(["Calisto Tanzi", "bancarotta fraudolenta", "17 anni e 5 mesi"], w=820), (540, 960), tc, anim="drop", rot=-2), "paper")
        sc.add(Stamp("DEFINITIVA", (540, 1180), T("17") + 0.3, size=100, rot=-8))
        sc.add(Text("La *condanna*", (540, 330), tc, size=110, anchor="ma", align="m"))
        sc.footer = "Fonti: AGI · imgpress · Blitz quotidiano · Il Post"
    elif i == 5:
        sc.add(Text("Un foglio falso\nha ingannato\nil *mercato?*", (540, 300), a, size=88, anchor="ma", align="m"))
        sc.add(Img(confirm_letter(480, fake=True), (540, 960), a + 0.2, T("storia") - 0.2, anim="drop", rot=-3), "paper")
        sc.add(Text("Storia completa su YouTube", (540, 1185), T("storia"), size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(90), (540, 1345), T("Fascicolo"), anim="pop", shadow=False), "hit")
        sc.footer = "Ricostruzione a scopo divulgativo · voce generata con sintesi vocale"
    return sc
