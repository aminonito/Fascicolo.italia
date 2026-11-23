import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from gir import *
import fx
W, H = 1080, 1920
FY = 1300
SB = (40, 640, 1040, 1300)
MT = "mappa: Natural Earth · schema non in scala"
FT = "Fonti: Il Post (2014) · AGI (2023) · Finestre sull'Arte (2026) · L'Espresso (2013, 2015) · ILAB · Doppiozero · Live Science"

# (parola, titolo in alto, comando grafico)
V = {
 0: [("Il", "Il *direttore*", "i:keys|CHI AVEVA LE CHIAVI"), ("biblioteche", "Una biblioteca\n*antichissima*", "sala:day|1|1|"),
     ("portava", "I libri\n*escono*", "sala:night|0.9|0.5|"), ("notte", "Anche\n*di notte*", "i:boxbooks|")],
 1: [("Napoli", "*Napoli*", "map:Napoli"), ("Girolamini", "Biblioteca\ndei *Girolamini*", "i:library|"), ("aperta", "Aperta dal *1586*", "cal:APERTA AL PUBBLICO|1586"),
     ("160.000", "*160.000*\nvolumi", "i:shelf|")],
 2: [("Giugno", "*Giugno 2011*", "cal:IL NUOVO DIRETTORE|2011"), ("commerciante", "Un *commerciante*\ndi libri antichi", "i:oldbook|"),
     ("Marino", "Marino Massimo\n*De Caro*", "i:nophoto|IL DIRETTORE")],
 3: [("In", "Migliaia\ndi libri *spariti*", "sala:mess|0.8|0.5|"), ("aprile", "*Aprile 2012*", "i:press|LA DENUNCIA SUI GIORNALI"),
     ("denuncia", "Poi il *sequestro*", "i:seal|")],
 4: [("Monaco", "*Monaco*\ndi Baviera", "map:Monaco di Baviera"), ("all'asta", "Centinaia di libri\n*all'asta*", "i:catalog|"),
     ("Fermati", "Fermati\nla sera *prima*", "i:lots|LOTTI RITIRATI"), ("prima", "", "stamp:FERMATA")],
 5: [("De", "La *confessione*", "i:mic|"), ("sette", "*7 anni*\ndefinitivi", "big:7 anni|per peculato"),
     ("falso", "Un falso\n*Galileo*", "i:moonbook|SCHEMA · NON L'ORIGINALE"), ("mezzo", "*500.000 $*\na New York", "big:500.000 $|venduto a New York · 2005")],
 6: [("biblioteca", "Riaperta\nnel *2026*", "sala:open|0.8|0.8|"), ("storia", "La storia\n*completa*", "logo")],
}
ALIAS = {"mic": "microphone"}

def stage(sc, cmd, t0, t1, i):
    k, _, arg = cmd.partition(":"); p = arg.split("|") if arg else []
    if k == "i":
        sc.add(Icon(ALIAS.get(p[0], p[0]), (540, 930), t0, t1, size=560, label=(p[1] if len(p) > 1 and p[1] else None)), "pop")
    elif k == "cal":
        sc.add(Calendar((540, 920), 420, [(t0, p[0], p[1])], t0, t1), "paper")
    elif k == "big":
        sc.add(Big(p[0], (540, 900), t0, t1, size=170 if len(p[0]) < 9 else 130, color=GOLD, sub=p[1]))
    elif k == "map":
        pins = ["Napoli"] if p[0] == "Napoli" else ["Napoli", p[0]]
        routes = [] if len(pins) == 1 else [dict(pts=pins, t=t0 + 0.5, d=1.2, icon="person", color=RED)]
        cen = "Napoli" if len(pins) == 1 else (12.9, 44.5)
        sc.add(WorldMap((40, 640, 1040, 1320), [(t0, cen, 60 if len(pins) == 1 else 50), (t1 or t0 + 3, cen, 90 if len(pins) == 1 else 60)], t0, t1,
                        pins=[dict(at=q, label=q.upper(), t=t0 + 0.2 + 0.2 * j, side="r", color=(RED if j else GOLD)) for j, q in enumerate(pins)], routes=routes, title=MT))
    elif k == "sala":
        sc.add(Sala(SB, t0, t1, mode=p[0], fill=float(p[1]), fill_to=float(p[2]), dur=2.5, title="LA SALA · schema · non in scala"))
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
        if cmd.startswith("stamp"):
            stage(sc, cmd, t, None, i)
        else:
            nm = [b[0] for b in main if b[0] > t]
            stage(sc, cmd, t, (nm[0] - 0.05 if nm else None), i)
    sc.footer = FT
    return sc
