import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from fan import *
import fx
W, H = 1080, 1920
FY = 1300
SB = (40, 640, 1040, 1300)
MT = "mappa: Natural Earth · schema non in scala"
FT = "Fonti: Corte di cassazione n. 22/2019 · CEDU 2/5/2024 · Il Post (2024) · Finestre sull'Arte · Univ. di Ginevra (ArThemis) · Wikipedia"

# (parola, titolo in alto, comando grafico)
V = {
 0: [("Estate", "Estate\n*1964*", "cal:ESTATE|1964"), ("peschereccio", "Un *peschereccio*\ndi Fano", "mare:fondo"),
     ("rete", "Tirano su\nla *rete*", "mare:rete"), ("statua", "Una statua\ndi *bronzo*", "i:statue_crust|SAGOMA STILIZZATA · NON È L'OPERA"),
     ("duemila", "Oltre\n*2.000 anni*", "big:2.000+|anni di età")],
 1: [("Nessuno", "Nessuno\nla *denuncia*", "mare:rotta"), ("campo", "Un campo\ndi *cavoli*", "i:cabbage|CARRARA DI FANO"),
     ("Gubbio", "Poi a\n*Gubbio*", "map:Fano,Gubbio|Fano>Gubbio|60"), ("sacerdote", "Nella casa\ndi un *sacerdote*", "i:priest|")],
 2: [("Tre", "*3,5 milioni*\ndi lire", "big:3,5 mln|di lire · 1964"), ("Processati", "Il *processo*", "i:gavel|PERUGIA · FINO AL 1970"),
     ("assolti", "", "stamp:ASSOLTI"), ("prova", "*Dove* era\nstata trovata?", "map:Fano,Pedaso,Croazia||60")],
 3: [("Monaco", "Ricompare\na *Monaco*", "map:Gubbio,Monaco di Baviera|Gubbio>Monaco di Baviera|14"), ("1977", "*1977*", "cal:CALIFORNIA|1977"),
     ("California", "Il museo\nin *California*", "map:Monaco di Baviera,Malibu|Monaco di Baviera>Malibu|7"),
     ("quattro", "*3,95 milioni $*", "big:3,95 mln $|pagati nel 1977")],
 4: [("2018", "La *Cassazione*", "i:court|NOVEMBRE 2018"), ("Stato", "", "stamp:CONFISCA"),
     ("2024", "La Corte di\n*Strasburgo*", "i:strasbourg|2 MAGGIO 2024"), ("ragione", "Ragione\nall'*Italia*", "i:scales|ALL'UNANIMITÀ")],
 5: [("Ma", "Ancora in\n*California*", "sala:statua"), ("storia", "La storia\n*completa*", "logo")],
}

def stage(sc, cmd, t0, t1, i):
    k, _, arg = cmd.partition(":"); p = arg.split("|") if arg else []
    if k == "i":
        sc.add(Icon(p[0], (540, 930), t0, t1, size=560, label=(p[1] if len(p) > 1 and p[1] else None)), "pop")
    elif k == "cal":
        sc.add(Calendar((540, 920), 420, [(t0, p[0], p[1])], t0, t1), "paper")
    elif k == "big":
        sc.add(Big(p[0], (540, 900), t0, t1, size=170 if len(p[0]) < 9 else 130, color=GOLD, sub=p[1]))
    elif k == "mare":
        sc.add(Mare(SB, t0, t1, mode=p[0], dur=2.5, title="SCHEMA · NON IN SCALA"))
    elif k == "sala":
        sc.add(Sala(SB, t0, t1, mode=p[0], sign="MALIBU · SCHEMA", visitors=2, title="SCHEMA · NON IN SCALA"))
    elif k == "map":
        pins = p[0].split(","); ll = [WPL[q] for q in pins]
        cen = (sum(x for x, y in ll) / len(ll), sum(y for x, y in ll) / len(ll)); z = float(p[2])
        routes = []
        if p[1]:
            pts = p[1].split(">"); routes = [dict(pts=pts, t=t0 + 0.5, d=1.4, icon="person", color=RED)]
        sc.add(WorldMap((40, 640, 1040, 1320), [(t0, cen, z * 0.8), (t1 or t0 + 3, cen, z)], t0, t1,
                        pins=[dict(at=q, label=q.upper(), t=t0 + 0.2 + 0.2 * j, side=("l" if (j == 0 and len(pins) > 1) else "r"), color=(GOLD if j else RED)) for j, q in enumerate(pins)], routes=routes, title=MT))
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
