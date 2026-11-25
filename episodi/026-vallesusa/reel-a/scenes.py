import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from vfs import *
import fx
W, H = 1080, 1920
FY = 1300
SB = (40, 640, 1040, 1300)
MT = "mappa: Natural Earth · schema non in scala"
FT = "Fonti: La Nazione (2017) · Remocontro (2014) · Magliarossonera (con Repubblica 1984 e Corriere 2017) · R. Bruni (2020) · Wikipedia · Sempione News"

V = {
 0: [("Ottomila", "*8.000*\noperai", "big:8.000|senza lavoro"), ("padrone", "Il *padrone*", "i:factory_x|IL CRAC"),
     ("trent'anni", "*30* anni", "big:30|anni"), ("Milan", "Presidente\ndel *Milan*", "i:trophy|1963-1965")],
 1: [("Felice", "Felice *Riva*", "i:spool|L'EREDE DEL COTONE"), ("trentina", "Una *trentina*\ndi fabbriche", "rete:rete|10"),
     ("quindicimila", "*15.000*\ndipendenti", "big:15.000|dipendenti · intorno al 1960")],
 2: [("Nel", "Ottobre\n*1965*", "cal:FALLIMENTO|OTT 1965"), ("fallisce", "", "rete:stop|10"),
     ("quarantasei", "*46 miliardi*\ndi debiti", "big:46 MLD|di lire di debiti"), ("cinquecentosettanta", "*570 mln €*\ndi oggi", "big:≈ 570 MLN €|coefficienti ISTAT · stima")],
 3: [("Nel", "*1969*", "cal:L'ARRESTO|1969"), ("cinema", "All'uscita\ndi un *cinema*", "i:cinema|MILANO"),
     ("giorni", "Pochi *giorni*", "i:prison|SAN VITTORE"), ("vizio", "Vizio\ndi *forma*", "stamp:ANNULLATO")],
 4: [("E", "Con il *passaporto*\nverso *Beirut*", "map")],
 5: [("Tredici", "*13* anni\nin Libano", "i:skyline|BEIRUT · 1969-1982"), ("amnistie", "Amnistie\ne *cittadinanza*", "i:amnesty|AMNISTIE"),
     ("sconterà", "Pena\n*mai scontata*", "stamp:MAI SCONTATA"), ("storia", "La storia\n*completa*", "logo")],
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
        sc.add(Rete(SB, t0, t1, n=int(p[1]), mode=p[0], center="VALLESUSA"))
    elif k == "stamp":
        sc.add(Stamp(arg, (540, 1250), t0, t1, size=110, rot=-8))
    elif k == "map":
        pts = ["Milano", "Nizza", "Parigi", "Atene", "Beirut"]
        routes = [dict(pts=[pts[j], pts[j + 1]], t=t0 + 0.4 + 0.6 * j, d=0.6, icon="passport", color=RED) for j in range(4)]
        sc.add(WorldMap(SB, [(t0, (17.0, 42.0), 22), (t1 or t0 + 6, (20.5, 41.0), 25)], t0, t1,
                        pins=[dict(at=q, label=q.upper(), t=t0 + 0.2 + 0.6 * j, side=("l" if (j % 2 or q == "Beirut") else "r"), color=(RED if q == "Beirut" else GOLD)) for j, q in enumerate(pts)],
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
