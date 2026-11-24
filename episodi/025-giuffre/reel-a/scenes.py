import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from giu import *
import fx
W, H = 1080, 1920
FY = 1300
SB = (40, 640, 1040, 1300)
MT = "mappa: Natural Earth · schema non in scala"
FT = "Fonti: Camera dei deputati (sedute 25/9/1958, 22/1/1959) · Archivio storico del Senato · Il Resto del Carlino (2010) · Wikipedia · FILO Magazine"

V = {
 0: [("Anni", "Anni\n*Cinquanta*", "cal:ROMAGNA|1950"), ("ex", "Un ex impiegato\ndi *banca*", "i:bankold|EX IMPIEGATO DI BANCA"),
     ("settanta", "Interessi\ndel *70%*", "big:70%|all'anno"), ("cento", "Perfino\nil *100%*", "big:100%|all'anno")],
 1: [("soldi", "Parroci\ne *conventi*", "rete:su|6"), ("ricostruire", "Per ricostruire\nle *chiese*", "i:convent|LE CHIESE DA RICOSTRUIRE"),
     ("dono", "Un dono della\n*Provvidenza*", "i:moneybag|GLI INTERESSI")],
 2: [("Ma", "Il denaro\n*investito*?", "i:question|SECONDO LE RICOSTRUZIONI: NO"), ("nuovi", "I *nuovi* pagano\ni vecchi", "rete:ponzi|9"),
     ("Ponzi", "Uno schema\n*Ponzi*", "pyr")],
 3: [("agosto", "Agosto\n*1958*", "cal:LO SCANDALO|AGO 1958"), ("esplode", "", "stamp:SCANDALO"),
     ("banchiere", "Il banchiere\ndi *Dio*", "i:priest|IL SOPRANNOME")],
 4: [("Parlamento", "L'*inchiesta*", "i:report|COMMISSIONE D'INCHIESTA · 1958"), ("Camera", "Un solo\n*voto*", "i:urn|VOTO SEGRETO · CAMERA · 22 GENNAIO 1959"),
     ("279", "*279 a 278*", "big:279-278|la mozione passa")],
 5: [("fallito", "Dichiarato\n*fallito*", "i:court|TRIBUNALE DI BOLOGNA"), ("carcere", "Mai in\n*carcere*", "rete:stop|9"),
     ("storia", "La storia\n*completa*", "logo")],
}

def stage(sc, cmd, t0, t1, i):
    k, _, arg = cmd.partition(":"); p = arg.split("|") if arg else []
    if k == "i":
        sc.add(Icon(p[0], (540, 930), t0, t1, size=560, label=(p[1] if len(p) > 1 and p[1] else None)), "pop")
    elif k == "cal":
        sc.add(Calendar((540, 920), 420, [(t0, p[0], p[1])], t0, t1), "paper")
    elif k == "big":
        sc.add(Big(p[0], (540, 900), t0, t1, size=170 if len(p[0]) < 9 else 130, color=GOLD, sub=p[1]))
    elif k == "rete":
        sc.add(Rete(SB, t0, t1, n=int(p[1]), mode=p[0]))
    elif k == "pyr":
        sc.add(Pyramid((60, 660, 1020, 1300), [t0 + 0.2 + 0.5 * j for j in range(4)], t0, t1, top_label="IMOLA"))
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
        nx = [b[0] for b in beats if b[0] > t and b[1]]
        t1 = nx[0] - 0.05 if nx else None
        if tt: sc.add(Text(tt, (540, 300), t, t1, size=100 if len(tt) < 22 else 88, anchor="ma", align="m"))
        nm = [b[0] for b in main if b[0] > t]
        stage(sc, cmd, t, (nm[0] - 0.05 if nm else None), i)
    sc.footer = FT
    return sc
