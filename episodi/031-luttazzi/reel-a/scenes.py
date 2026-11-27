import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "030-saliera"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "029-collana"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "027-dossena"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "028-smemorato"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "engine"))
from fi import *
from fx import *
from ltz import *
import fx
W, H = 1080, 1920
FY = 1300
SB = (40, 640, 1040, 1300)
MT = "mappa: Natural Earth · schema non in scala"
FT = "Fonti: Il Tempo · Quotidiano Nazionale · Sky TG24/ANSA · La Voce di New York · La Nazione · storiaradiotv · Wikipedia"

V = {
 0: [("Roma", "Roma\n*1970*", "map1"), ("volti", "Un volto\n*famoso*", "i:tvstage|RADIO E TELEVISIONE"), ("carcere", "In *carcere*", "i:prison|REGINA COELI"),
     ("telefonata", "Per una\n*telefonata*", "i:phonecall|")],
 1: [("È", "Lelio\n*Luttazzi*", "i:piano|MUSICISTA E PIANISTA"), ("pianista", "In *smoking*", "i:tuxedo|SAGOMA · NESSUNA FOTO"), ("Hit", "La *Hit Parade*", "i:hitparade|ALLA RADIO")],
 2: [("Un", "Un *amico*", "i:clapper|L'ATTORE WALTER CHIARI"), ("chiamare", "«Chiamalo\n*tu*»", "i:phonecall|UN CONOSCENTE"), ("Luttazzi", "Luttazzi\n*chiama*", "fig"),
     ("intercettato", "*Intercettato*", "i:taperec|IL TELEFONO SOTTO CONTROLLO"), ("spacciatore", "", "stamp:SPACCIATORE")],
 3: [("Arriva", "Guardia\ndi *Finanza*", "i:gdf|"), ("niente", "*Niente*\nin casa", "i:magnifier|NESSUNA DROGA TROVATA"), ("arrestato", "*Arrestato*", "i:handcuffs|ACCUSA: SPACCIO")],
 4: [("Ventisette", "*27 giorni*", "big:27|giorni in carcere"), ("isolamento", "In *isolamento*", "i:isolation|REGINA COELI"), ("scarcerato", "*Prosciolto*", "i:certificate|DEL TUTTO ESTRANEO"),
     ("estraneo", "", "stamp:INNOCENTE")],
 5: [("Ma", "La *carriera*", "i:radio|NON PIÙ COME PRIMA"), ("storia", "La storia\n*completa*", "logo")],
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
        sc.add(Rete(SB, t0, t1, n=int(p[1]), mode=p[0], center="ROMA"))
    elif k == "stamp":
        sc.add(Stamp(arg, (540, 1250), t0, t1, size=110, rot=-8))
    elif k == "fig":
        sc.add(Figure([(t0, 380, 1250), (t0 + 1.5, 560, 1250)], t0, t1, kind="suit", s=1.4), "pop")
        sc.add(Icon("phone", (800, 1000), t0 + 0.3, t1, size=300), "pop")
    elif k in ("map1", "map2"):
        pts = ["Roma", "Bologna", "Trieste"]; cen, z = (12.5, 43.8), 90.0; routes = []
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
