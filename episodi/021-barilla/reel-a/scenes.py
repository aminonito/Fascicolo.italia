import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from bar import *
import fx
W, H = 1080, 1920
FY = 1300
SB = (40, 640, 1040, 1300)
MT = "mappa: Natural Earth · schema non in scala"
FT = "Fonti: Il Sole 24 Ore (2025) · Tgcom24 · Panorama · L'Eco di Bergamo (2003) · Il Giornale · Wikipedia · art643.org"

# (parola, titolo in alto, comando grafico)
V = {
 0: [("Sette", "*7 anni e mezzo*\nin carcere", "i:cell|"), ("innocente", "Da *innocente*", "stamp:INNOCENTE"),
     ("colpa", "Per colpa\ndi un'*auto*", "ii:tipo|LA SUA AUTO|tipo_b|UN'AUTO IDENTICA")],
 1: [("13", "*13 febbraio*\n1992", "cal:13 FEBBRAIO|1992"), ("Daniele", "*Daniele Barillà*", "i:nophoto|IMPRENDITORE BRIANZOLO"), ("va", "Va dalla\n*fidanzata*", "i:rose|LA VIGILIA DI SAN VALENTINO"),
     ("Fiat", "Una *Fiat Tipo*\nrossa", "i:tipo|SCHEMA · NESSUN MARCHIO")],
 2: [("carabinieri", "I *carabinieri*\nseguono…", "strada:follow"), ("trafficante", "…un *trafficante*\ndi cocaina", "strada:follow"),
     ("identica", "Auto *identica*,\ntarga simile", "i:plates2|DETTAGLI COPERTI"), ("Scambiano", "*Scambiato*\nper lui", "strada:swap")],
 3: [("Diciotto", "*18 anni*\nin primo grado", "big:18 anni|primo grado"), ("quindici", "*15* in appello", "big:15 anni|appello"),
     ("Condanna", "Condanna\n*definitiva*", "i:gavel|"), ("definitiva", "In *carcere*", "muro:1996")],
 4: [("Nel", "*1997*", "cal:ARRESTATO L'UFFICIALE|1997"), ("arrestato", "Arrestato per\naltre *vicende*", "i:scales|ACCUSATO · FATTI DIVERSI"),
     ("caso", "Il caso\nsi *riapre*", "i:folder|")],
 5: [("Luglio", "*Luglio 1999*", "i:court|REVISIONE · GENOVA"), ("esce", "Esce dal\n*carcere*", "muro:1999.53"),
     ("Poi", "*Assolto*", "cal:ASSOLUZIONE DEFINITIVA|2000"), ("non", "Non ha commesso\nil *fatto*", "stamp:ASSOLTO")],
 6: [("Stato", "Il *risarcimento*", "big:3-4 milioni|di euro · cifre non concordi"), ("storia", "La storia\n*completa*", "logo")],
}

def stage(sc, cmd, t0, t1, i):
    k, _, arg = cmd.partition(":"); p = arg.split("|") if arg else []
    if k == "i":
        sc.add(Icon(p[0], (540, 930), t0, t1, size=560, label=(p[1] if len(p) > 1 and p[1] else None)), "pop")
    elif k == "ii":
        sc.add(Icon(p[0], (300, 930), t0, t1, size=400, label=p[1]), "pop")
        sc.add(Icon(p[2], (780, 930), t0 + 0.4, t1, size=400, label=p[3]), "pop")
    elif k == "cal":
        sc.add(Calendar((540, 920), 420, [(t0, p[0], p[1])], t0, t1), "paper")
    elif k == "big":
        sc.add(Big(p[0], (540, 900), t0, t1, size=170 if len(p[0]) < 9 else 130, color=GOLD, sub=p[1]))
    elif k == "map":
        pins = p[1].split(",")
        sc.add(WorldMap((40, 640, 1040, 1320), [(t0, p[0], 3000), (t1 or t0 + 3, p[0], 3600)], t0, t1,
                        pins=[dict(at=q, label=q.upper(), t=t0 + 0.2 + 0.2 * j, side="r", color=(RED if j else GOLD)) for j, q in enumerate(pins)], title=MT))
    elif k == "strada":
        sc.add(Strada(SB, t0, t1, mode=arg, title="schema semplificato · dinamica esatta non documentata"))
    elif k == "muro":
        sc.add(Muro((60, 640, 1020, 1300), t0, t1, upto=float(arg), dur=2.5))
    elif k == "stamp":
        sc.add(Stamp(arg, (540, 1250), t0, t1, size=110, rot=-8))
    elif k == "logo":
        sc.add(Img(wordmark(110), (540, 900), t0, t1, anim="pop", shadow=False), "hit")
        sc.add(Pill("SU YOUTUBE · FASCICOLO ITALIA", (540, 1120), t0 + 0.3, t1, size=52, accent=True))

def build(i, dur, a, words):
    used = {}
    def T(p):
        cs = lambda s: re.sub(r"[^\w']", "", s.lower())
        hits = [w for w in words if cs(w[0]) == cs(p)] or [w for w in words if cs(w[0]).startswith(cs(p))]
        n = used.get(p, 0); used[p] = n + 1
        return a + hits[min(n, len(hits) - 1)][1] if hits else a + 0.5
    sc = Scene(dur)
    beats = sorted([(max(a, T(w) - 0.25), tt, cmd) for w, tt, cmd in V[i]])
    beats[0] = (a, beats[0][1], beats[0][2])
    main = [b for b in beats if not b[2].startswith("stamp")]
    for j, (t, tt, cmd) in enumerate(beats):
        nx = [b[0] for b in beats if b[0] > t]
        t1 = nx[0] - 0.05 if nx else None
        sc.add(Text(tt, (540, 300), t, t1, size=100 if len(tt) < 22 else 88, anchor="ma", align="m"))
        if cmd.startswith("stamp"):
            stage(sc, cmd, t, None, i)
        else:
            nm = [b[0] for b in main if b[0] > t]
            stage(sc, cmd, t, (nm[0] - 0.05 if nm else None), i)
    sc.footer = FT
    return sc
