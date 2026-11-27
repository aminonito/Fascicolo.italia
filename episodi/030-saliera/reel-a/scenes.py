import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "029-collana"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "027-dossena"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "028-smemorato"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "engine"))
from fi import *
from fx import *
from sal import *
import fx
W, H = 1080, 1920
FY = 1300
SB = (40, 640, 1040, 1300)
MT = "mappa: Natural Earth · schema non in scala"
FT = "Fonti: Tiroler Tageszeitung · AP · New York Times · La Libre/AFP · Vorarlberg Online · Wikipedia · Kunsthistorisches Museum"

V = {
 0: [("Vienna", "Vienna\n*maggio 2003*", "map1"), ("notte", "Di *notte*", "i:scaffold_man|SALE SULL'IMPALCATURA"), ("museo", "Entra nel\n*museo*", "i:facade_win|LA FINESTRA ROTTA"),
     ("capolavoro", "Un capolavoro\n*d'oro*", "i:saliera|"), ("cinquanta", "≈ *50 mln €*", "big:50 MLN €|il valore stimato")],
 1: [("È", "La *Saliera*", "i:saliera|SCHEMA · NON L'ORIGINALE"), ("Cellini", "Benvenuto\n*Cellini*", "i:goldsmith|ORAFO · FIRENZE 1500"), ("Parigi", "Per il re\ndi *Francia*", "i:fleur|PARIGI · 1540-1543"),
     ("cinque", "Quasi *5 secoli*", "big:≈ 460|anni prima")],
 2: [("Scatta", "*Allarme*!", "i:alarm|3:55"), ("guardiani", "«Falso\n*allarme*»", "i:alarm_off|SPENTO"), ("spengono", "Nessuno\n*controlla*", "fig"),
     ("furto", "La vetrina\n*vuota*", "i:vitrine_broken|LA MATTINA DOPO")],
 3: [("Nel", "*2005*", "i:letter|IL RICATTO"), ("dieci", "*10 mln €*", "big:10 MLN €|di riscatto"), ("prova", "La *prova*", "i:trident|IL TRIDENTE DI NETTUNO")],
 4: [("Lo", "Una\n*telecamera*", "i:cctv|IL NEGOZIO DI TELEFONI"), ("telefono", "Il telefono\ndel *ricatto*", "i:sms|"), ("esperto", "Un esperto\ndi *allarmi*", "i:sensor|IL LADRO"),
     ("d'allarme", "", "stamp:IL PARADOSSO")],
 5: [("Porta", "Un *bosco*", "i:forest_box|VICINO A ZWETTL"), ("sepolta", "*Ritrovata*", "i:box_open|21 GENNAIO 2006"), ("storia", "La storia\n*completa*", "logo")],
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
        for j, x in enumerate((300, 540, 780)):
            sc.add(Figure([(t0, x, 1250)], t0 + 0.2 * j, t1, kind="guard", s=1.3), "pop")
        sc.add(Icon("alarm_off", (540, 700), t0 + 0.3, t1, size=300), "pop")
    elif k in ("map1", "map2"):
        pts = ["Vienna", "Parigi", "Firenze"]; cen, z = (9.0, 46.5), 60.0; routes = []
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
