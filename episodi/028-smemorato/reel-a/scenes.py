import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "027-dossena"))
from fi import *
from fx import *
from smem import *
import fx
W, H = 1080, 1920
FY = 1300
SB = (40, 640, 1040, 1300)
MT = "mappa: Natural Earth · schema non in scala"
FT = "Fonti: Il Post (2026) · Wikipedia · L. Roscioni, Einaudi (estratto) · Doppiozero (2021) · Blitz quotidiano (2014) · Cabinet (2011) · l'Unità (2009)"

V = {
 0: [("Nel", "*1927*", "cal:LA FOTO SUL GIORNALE|1927"), ("due", "Due *donne*", "i:two_claim|"), ("foto", "Lo stesso\n*uomo*", "i:beard|SENZA MEMORIA"),
     ("dicono", "«È mio\n*marito*»", "i:rings|DUE MOGLI")],
 1: [("Un", "*Torino*\n1926", "map1"), ("ruba", "Un *vaso*", "i:vase|CIMITERO EBRAICO"), ("Non", "Chi *è*?", "i:question|NESSUN DOCUMENTO"),
     ("finisce", "*Collegno*", "i:asylum|IL MANICOMIO"), ("Collegno", "N. *44170*", "i:beard_n|IL SUO NUMERO")],
 2: [("Per", "Giulia\n*Canella*", "i:woman|VERONA"), ("Giulio", "Il professor\n*Canella*", "i:book|FILOSOFIA"), ("disperso", "Disperso\nnel *1916*", "i:helmet|MACEDONIA · 1916")],
 3: [("Ma", "Una lettera\n*anonima*", "i:anon|"), ("Mario", "Mario\n*Bruneri*", "i:press|TIPOGRAFO · TORINO"), ("ricercato", "*Ricercato*", "i:handcuffs|PER TRUFFA"),
     ("Sua", "Un'altra\n*moglie*", "i:witness|"), ("impronte", "Le *impronte*", "i:finger2|COINCIDONO")],
 4: [("Nel", "*1931*", "i:court|TORINO · FIRENZE · ROMA"), ("quattro", "*4 anni*\ndi cause", "i:hourglass|1927-1931"), ("sentenza", "«È *Bruneri*»", "i:gavel|LA SENTENZA"), ("Ma", "Giulia\nnon ci *crede*", "i:question|"),
     ("Brasile", "Verso il\n*Brasile*", "map2")],
 5: [("Muore", "Rio\n*1941*", "i:rio|RIO DE JANEIRO"), ("nome", "Il nome:\n*Giulio Canella*", "i:grave|"), ("storia", "La storia\n*completa*", "logo")],
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
    elif k == "fig":
        sc.add(Figure([(t0, 540, 1250)], t0, t1, kind="man", s=2.0), "pop")
        sc.add(Icon("beard", (540, 760), t0 + 0.3, t1, size=300), "pop")
    elif k in ("map1", "map2"):
        if k == "map1":
            pts = ["Torino"]; cen, z = (10.5, 43.5), 40.0; routes = []
        else:
            pts = ["Torino", "Rio de Janeiro"]; cen, z = (-18.0, 12.0), 7.0; routes = [dict(pts=["Torino", "Rio de Janeiro"], t=t0 + 0.6, d=1.4, icon="person", color=RED)]
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
