import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from dos import *
import fx
W, H = 1080, 1920
FY = 1300
SB = (40, 640, 1040, 1300)
MT = "mappa: Natural Earth · schema non in scala"
FT = "Fonti: Museum of Fine Arts Boston (scheda 24.150) · Finestre sull'Arte (2021) · il Giornale (2026) · Wikipedia · TIME (1928) · Avvenire (2021) · J. Keats, Forged"

V = {
 0: [("tomba", "Una tomba\ndel *1430*", "i:sarcoph|«DEL 1430»"), ("centomila", "Oltre *100.000 $*", "big:100.135 $|pagati dal museo di Boston"),
     ("scolpita", "Scolpita\nnel *1920*", "i:workshop|INTORNO AL 1920"), ("1920", "", "stamp:FALSO")],
 1: [("L'autore", "Alceo\n*Dossena*", "i:chisel|CREMONA 1878 · ROMA 1937"), ("Madonne", "*Madonne*\ne angeli", "i:madonna|IN STILE ANTICO"),
     ("greche", "Statue\n*greche*", "i:kore|STILE ARCAICO"), ("maestri", "I grandi\n*maestri*", "i:museum|DONATELLO · MINO · SIMONE MARTINI")],
 2: [("Due", "Due *mercanti*", "i:handshake|ROMA"), ("antiche", "Vendute\ncome *antiche*", "i:price|«ANTICO»"), ("musei", "Verso\nl'*America*", "map")],
 3: [("Un'Annunciazione", "Un'*Annunciazione*", "i:annunc|«SIMONE MARTINI»"), ("almeno", "Almeno\n*150.000 $*", "big:≥ 150.000 $|nel 1924 · fonti non concordi sul prezzo esatto")],
 4: [("Nel", "*1928*", "cal:LO SCANDALO|1928"), ("assolto", "*Assolto*", "i:court|INSUFFICIENZA DI PROVE"), ("dice", "Non *sapeva*", "i:question|LA SUA DIFESA")],
 5: [("Nel", "*1933*", "i:auction|ASTA · 39 OPERE"), ("novemila", "*≈ 9.000 $*\nin tutto", "big:≈ 9.000 $|39 opere · vendute come sue"), ("storia", "La storia\n*completa*", "logo")],
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
        sc.add(Rete(SB, t0, t1, n=int(p[1]), mode=p[0], center="ROMA"))
    elif k == "stamp":
        sc.add(Stamp(arg, (540, 1250), t0, t1, size=110, rot=-8))
    elif k == "map":
        pts = ["Roma", "Boston", "New York", "Cleveland"]
        routes = [dict(pts=["Roma", q], t=t0 + 0.4 + 0.5 * j, d=0.9, icon="statue", color=RED) for j, q in enumerate(pts[1:])]
        sc.add(WorldMap(SB, [(t0, (-28.0, 42.0), 8.0), (t1 or t0 + 6, (-30.0, 42.0), 8.6)], t0, t1,
                        pins=[dict(at=q, label=q.upper(), t=t0 + 0.2 + 0.4 * j, side=("r" if q == "Boston" else "l"), color=(GOLD if q == "Roma" else RED)) for j, q in enumerate(pts)],
                        routes=routes, title=MT))
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
