import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from brk import *
import fx
W, H = 1080, 1920
FY = 1300
SB = (40, 640, 1040, 1300)
MT = "mappa: Natural Earth · schema non in scala"
FT = "Fonti: FBI (Famous Cases; 2007) · Wikipedia · History.com · Smithsonian (2025) · WGBH (2016) · EBSCO"

# (parola, titolo in alto, comando grafico)
V = {
 0: [("Avevano", "Le *chiavi*\ndi ogni porta", "dep:0|0|1|1|work|0"), ("smontavano", "Smontano\nla *serratura*", "i:lockcyl|IL CILINDRO DELLA SERRATURA"),
     ("chiave", "Una chiave\n*copiata*", "i:key|"), ("rimettevano", "E la rimettono\n*a posto*", "dep:5|0|1|1|work|1")],
 1: [("Boston", "*Boston*", "map:Boston"), ("gennaio", "*17 gennaio 1950*", "cal:BOSTON|17 GEN 1950"),
     ("deposito", "Il deposito\ndella *Brink's*", "str:none|0"), ("portavalori", "Furgoni\n*portavalori*", "i:armored|")],
 2: [("mente", "Chi è\nla *mente*?", "i:question|"), ("Italia", "Un ladro\nnato in *Italia*", "map:Italia"), ("Anthony", "Anthony *Pino*", "i:nophoto|LA MENTE · SECONDO QUASI TUTTE LE FONTI")],
 3: [("Sette", "*Sette* uomini", "str:parked|1"), ("maschere", "Maschere\n*di gomma*", "i:mask|MASCHERA GENERICA · SCHEMA"),
     ("cappotti", "Cappotti\nda *marinaio*", "i:peacoat|"), ("Legano", "Cinque\n*dipendenti*", "dep:5|7|0|1|tied|1")],
 4: [("In", "Una ventina\ndi *minuti*", "clock:19|LE 19 DI SERA"), ("oltre", "*1,2 milioni $*\nin contanti", "big:1,2 mln $|in contanti · più assegni e titoli"),
     ("assegni", "Assegni\ne *titoli*", "dep:5|7|1|0.2|tied|2")],
 5: [("Per", "*Sei anni*\nsenza prove", "i:hourglass|"), ("Poi", "Joseph\n*O'Keefe*", "i:nophoto|UNO DELLA BANDA"),
     ("tradito", "Si sente\n*tradito*", "i:mic|DECIDE DI PARLARE"), ("prescrizione", "Pochi giorni alla\n*prescrizione*", "cal:LA CONFESSIONE|GEN 1956")],
 6: [("Otto", "*Otto*\nergastoli", "i:gavel|"), ("ergastolo", "", "stamp:ERGASTOLO"), ("contanti", "Recuperati meno di\n*60.000 $*", "big:< 60.000 $|dei contanti rubati"),
     ("storia", "La storia\n*completa*", "logo")],
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
        if p[0] == "Italia":
            pins = ["Italia", "Boston"]; cen = (-29.0, 42.0); z = (9, 11)
            routes = [dict(pts=pins, t=t0 + 0.5, d=1.4, icon="person", color=RED)]
        else:
            pins = ["Boston"]; cen = "Boston"; z = (40, 70); routes = []
        sc.add(WorldMap((40, 640, 1040, 1320), [(t0, cen, z[0]), (t1 or t0 + 3, cen, z[1])], t0, t1,
                        pins=[dict(at=q, label=q.upper(), t=t0 + 0.2 + 0.2 * j, side="r", color=(RED if j else GOLD)) for j, q in enumerate(pins)], routes=routes, title=MT))
    elif k == "dep":
        d0, rb, pr, bg, staff, mode = p
        kw = dict(doors=int(d0), robbers=int(rb), staff=staff, night=True, dur=2.5)
        if mode == "1": kw.update(prog=0.0, prog_to=1.0)
        if mode == "2": kw.update(prog=1.0, bags=1.0, bags_to=0.15)
        sc.add(Deposito(SB, t0, t1, **kw, title="SCHEMA · NON IN SCALA"))
    elif k == "str":
        sc.add(Strada(SB, t0, t1, truck=p[0], lookout=(p[1] == "1"), title="PRINCE STREET · SCHEMA"))
    elif k == "clock":
        sc.add(ClockFace((540, 880), 300, t0, t1, start=int(p[0]) - 0.1, speed=0.12, label=p[1]), "pop")
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
            nm = [b[0] for b in main if b[0] > t]
            stage(sc, cmd, t, (nm[0] - 0.05 if nm else None), i)
        else:
            nm = [b[0] for b in main if b[0] > t]
            stage(sc, cmd, t, (nm[0] - 0.05 if nm else None), i)
    sc.footer = FT
    return sc
