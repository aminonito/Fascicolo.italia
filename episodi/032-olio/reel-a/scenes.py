import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "031-luttazzi"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "030-saliera"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "029-collana"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "027-dossena"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "028-smemorato"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "engine"))
from fi import *
from fx import *
from olio import *
import fx
W, H = 1080, 1920
FY = 1300
SB = (40, 640, 1040, 1300)
MT = "mappa: Natural Earth · schema non in scala"
FT = "Fonti: TIME (1965) · Wikipedia (Salad oil scandal; T. De Angelis) · Benzinga · TodayIFoundOut · AgWeb · Fortune (2024) · MoneyWeek"

V = {
 0: [("New", "New Jersey\n*1963*", "map1"), ("prestiti", "Prestiti\n*milionari*", "i:dollar_bag|PRESTITI IN DOLLARI"), ("garanzia", "In *garanzia*", "i:tank_full|L'OLIO DEI SERBATOI"),
     ("acqua", "Soprattutto\n*acqua*", "i:tank_x|SCHEMA · NON IN SCALA")],
 1: [("È", "Tino\n*De Angelis*", "i:nophoto|SAGOMA · NESSUNA FOTO"), ("immigrati", "Figlio di\n*immigrati italiani*", "i:family|GENITORI DALL'ITALIA"), ("macelleria", "Garzone di\n*macelleria*", "i:pig|IL BRONX")],
 2: [("ispettori", "Gli *ispettori*", "i:inspector|IL CONTROLLO"), ("alto", "Dall'*alto*", "i:dipstick|SI VEDE L'OLIO"), ("Sotto", "Sotto?\n*Acqua*", "i:tank_x|SECONDO LE RICOSTRUZIONI"),
     ("tubi", "I *tubi*", "i:pipes|L'OLIO SI SPOSTA")],
 3: [("Sulla", "Sulla\n*carta*", "i:wreceipt|OLTRE 800.000 TONNELLATE"), ("serbatoi", "Nei *serbatoi*", "big:<1/10|meno di un decimo"), ("decimo", "", "stamp:NON C'È")],
 4: [("Novembre", "Novembre\n*1963*", "i:price_down|CROLLA TUTTO"), ("Cinquantuno", "*51*\ncreditori", "i:bank|ANCHE GRANDI BANCHE"), ("oltre", "Oltre\n*150 milioni*", "big:$150 mln|di dollari · e oltre"),
     ("c'era", "", "stamp:OLIO FANTASMA")],
 5: [("De", "Si dichiara\n*colpevole*", "i:gavel|LA CONDANNA"), ("Esce", "Circa\n*7 anni*", "i:pen_gate|IN CARCERE"), ("storia", "La storia\n*completa*", "logo")],
}

def stage(sc, cmd, t0, t1, i):
    k, _, arg = cmd.partition(":"); p = arg.split("|") if arg else []
    if k == "i":
        sc.add(Icon(p[0], (540, 930), t0, t1, size=560, label=(p[1] if len(p) > 1 and p[1] else None)), "pop")
    elif k == "cal":
        sc.add(Calendar((540, 920), 420, [(t0, p[0], p[1])], t0, t1), "paper")
    elif k == "big":
        sc.add(Big(p[0], (540, 900), t0, t1, size=(420 if len(p[0]) <= 3 else (170 if len(p[0]) < 9 else 130)), color=GOLD, sub=p[1]))
    elif k == "rete":
        sc.add(Rete(SB, t0, t1, n=int(p[1]), mode=p[0], center="BAYONNE"))
    elif k == "stamp":
        sc.add(Stamp(arg, (540, 1250), t0, t1, size=110, rot=-8))
    elif k == "fig":
        sc.add(Figure([(t0, 380, 1250), (t0 + 1.5, 560, 1250)], t0, t1, kind="suit", s=1.4), "pop")
        sc.add(Icon("phone", (800, 1000), t0 + 0.3, t1, size=300), "pop")
    elif k in ("map1", "map2"):
        pts = ["New York", "Washington"]; cen, z = (-75.5, 40.2), 160.0; routes = []
        sc.add(WorldMap(SB, [(t0, cen, z * 0.9), (t1 or t0 + 6, cen, z)], t0, t1,
                        pins=[dict(at=q, label=q.upper(), t=t0 + 0.2 + 0.4 * j, side=("r" if j else "l"), color=(GOLD if j == 0 else RED)) for j, q in enumerate(pts)],
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
