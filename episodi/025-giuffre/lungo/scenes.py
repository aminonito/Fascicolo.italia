import sys, os, re, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from giu import *
import fx, brk
from script import SCENES_H, CH

W, H = 1920, 1080
FY = 870
MAPB = (160, 250, 1760, 880)
RBOX = (260, 240, 1660, 860)
MT = "mappa: Natural Earth · schema non in scala"

FB = "Camera dei deputati (sedute 25/9/1958, 21-22/1/1959) · Archivio storico del Senato · Senato (8/4/1959) · Il Resto del Carlino (2010) · Wikipedia (Caso Giuffrè)"
CAM = "Camera dei deputati, sedute 25/9/1958 e 21-22/1/1959"
F = {0: "Fonti: " + FB,
     1: "Fonti: " + CAM + " · giulioandreotti.org (intervento 25/9/1958) · Wikipedia · FILO Magazine (2019) · ISTAT, valore della moneta",
     2: "Fonti: Archivio storico del Senato · Il Resto del Carlino (2010) · tuttosesto.net · Wikipedia · FILO Magazine · " + CAM,
     3: "Fonti: " + CAM + " · Archivio storico del Senato · Il Resto del Carlino (2010) · tuttosesto.net · Wikipedia · FILO Magazine",
     4: "Fonti: " + CAM + " · Senato (8/4/1959) · Il Resto del Carlino (2010) · Wikipedia · tuttosesto.net · Puntodivista (2011) · calcoli nostri",
     5: "Fonti: Archivio storico del Senato · Wikipedia · FILO Magazine · tuttosesto.net · Diritto Economia Impresa · " + CAM,
     6: "Fonti: " + CAM + " · Senato (8/4/1959) · giulioandreotti.org (relazione) · Wikipedia · Puntodivista (2011)",
     7: "Fonti: " + CAM + " · Senato (8/4/1959) · giulioandreotti.org · Il Resto del Carlino (2010) · tuttosesto.net · FILO Magazine",
     8: "Fonti: " + CAM + " · giulioandreotti.org (intervento 25/9/1958) · Archivio storico del Senato · L. 18/10/1958 n. 943",
     9: "Fonti: Archivio storico del Senato · giulioandreotti.org (relazione) · " + CAM + " · Senato (8/4/1959)",
     10: "Fonti: Senato (8/4/1959) · Il Resto del Carlino (2010) · FILO Magazine · tuttosesto.net · Diritto Economia Impresa · Wikipedia",
     11: "Fonti: Senato (8/4/1959) · " + CAM + " · Wikipedia · FILO Magazine · Il Resto del Carlino (2010)",
     12: "D.lgs. 385/1993 (Testo unico bancario, artt. 11 e 130) · Banca d'Italia · Consob · indicazioni generali, non consulenza finanziaria",
     13: "Fonti: tutte in descrizione · ricostruzione a scopo divulgativo"}

CHT = {1: "La Romagna,\n*anni '50*", 2: "I *protagonisti*", 3: "Il *commendatore*", 4: "Il *meccanismo*",
       5: "La *rete*", 6: "I primi\n*controlli*", 7: "Agosto\n*1958*", 8: "Il *Parlamento*", 9: "Il *voto*",
       10: "La *fine*", 11: "Le domande *aperte*", 12: "La *lezione*", 13: "Il *verdetto*"}
LASTCH = 13
FIRST = {}
for k, (h, _) in enumerate(SCENES_H):
    FIRST.setdefault(h, k)

BOARD = [("GIUFFRÈ", "ex impiegato di banca · Imola", "person"), ("I DEPOSITANTI", "parroci · conventi · famiglie", "person"),
         ("LA GUARDIA DI FINANZA", "perquisizione · marzo 1957", "card"), ("LUIGI PRETI", "ministro delle Finanze · 1958", "person"),
         ("GIULIO ANDREOTTI", "ministro del Tesoro · 1958", "person"), ("IL PARLAMENTO", "commissione d'inchiesta", "card")]
BXY = [(960, 450), (420, 450), (1500, 450), (420, 740), (960, 740), (1500, 740)]

def board_el(n, t0, t1):
    nodes = {}
    for j in range(n + 1):
        nm, role, kind = BOARD[j]
        nodes[f"n{j}"] = dict(xy=BXY[j], name=nm, role=role, t=t0 + (0.2 if j == n else -5), rot=(-3 + 2 * (j % 3)))
    pairs = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4), (0, 5)]
    links = [(f"n{p}", f"n{q}", t0 - 5 if max(p, q) < n else t0 + 0.6) for p, q in pairs if max(p, q) <= n]
    return Board(nodes, links, t0, t1, cw=220)

from data import SC
V = {i: b for i, (_, _, b) in enumerate(SC)}

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

ALIAS = {"crowd_icon": "family", "lab": "tubes", "suit": "nophoto", "critic": "meeting", "shield": "shield_ok", "hospital": "hospital2", "reward": "moneybag", "basilica": "convent", "calendar_x": "hourglass", "van": "truck", "warehouse": "boxbooks", "window": "window", "arrow_icon": "front", "scroll_icon": "letter", "note_icon": "music", "stars_icon": "stars", "map_icon": "globe2", "check": "shield_ok", "stop": "warn", "doc_icon": "letter", "mic": "microphone",
         "clock_icon": "hourglass", "fig_icon": "nophoto"}
def IC(n): return ALIAS.get(n, n)


def stage(sc, cmd, t0, t1, a, dur, i):
    k, _, arg = cmd.partition(":"); p = arg.split("|") if arg else []
    if k == "h":
        sc.add(Text(arg, (960, 430), t0, t1, size=104, anchor="ma", align="m"))
    elif k == "big":
        sc.add(Big(p[0], (960, 520), t0, t1, size=150 if len(p[0]) < 14 else 96, sub=(p[1] if len(p) > 1 and p[1] else None)))
    elif k == "i":
        sc.add(Icon(IC(p[0]), (960, 560), t0, t1, size=360, label=(p[1] if len(p) > 1 and p[1] else None)), "pop")
    elif k in ("ii", "iii"):
        n = len(p) // 2; xs = [660, 1260] if n == 2 else [520, 960, 1400]
        for j in range(n):
            sc.add(Icon(IC(p[2 * j]), (xs[j], 560), t0 + j * 0.35, t1, size=300 if n == 2 else 260, label=(p[2 * j + 1] or None)), "pop")
    elif k == "cal":
        sc.add(Calendar((960, 560), 320, [(t0, p[0], p[1])], t0, t1), "paper")
    elif k == "clock":
        hh = int(p[0])
        sc.add(ClockFace((960, 520), 220, t0, t1, start=hh - 0.4, speed=0.08, label=(p[1] if len(p) > 1 else "")), "pop")
    elif k == "card":
        sc.add(Img(label_card(p[1:], 860, title=p[0], seed=i), (960, 570), t0, t1, anim="drop", rot=-2 + (i % 3)), "paper")
    elif k == "doc":
        sc.add(Img(doc_typed(760, 540, p[0], p[1:], seed=i), (960, 570), t0, t1, anim="drop", rot=-2), "paper")
    elif k == "news":
        sc.add(Img(newspaper(720, 600, p[0], p[1], p[2], p[3], seed=i), (960, 580), t0, t1, anim="drop", rot=-3), "paper")
    elif k == "map":
        cen, ppd = p[0], min(200.0, float(p[1]) * 4); pins = p[2].split(",") if len(p) > 2 and p[2] else [cen]
        if len(pins) > 1:
            ll = [WPL[q] for q in pins]; lo0, lo1 = min(x for x, y in ll), max(x for x, y in ll); la0, la1 = min(y for x, y in ll), max(y for x, y in ll)
            cen = ((lo0 + lo1) / 2, (la0 + la1) / 2); ppd = min(ppd, 1100 / max(0.3, lo1 - lo0), 420 / max(0.3, la1 - la0))
        routes = []
        if len(p) > 3:
            pts = p[3].split(">")
            routes = [dict(pts=[pts[j], pts[j + 1]], t=t0 + 0.6 + 0.8 * j, d=1.0, icon="person", color=RED) for j in range(len(pts) - 1)]
        sc.add(WorldMap(MAPB, [(t0, cen, ppd * 0.8), (t1 or a + dur, cen, ppd)], t0, t1,
                        pins=[dict(at=q, label=q.upper(), t=t0 + 0.3 + 0.2 * j, side=("l" if j % 2 else "r"), color=(RED if j == 0 else GOLD)) for j, q in enumerate(pins)],
                        routes=routes, title=MT))
    elif k == "rete":
        sc.add(Rete(RBOX, t0, t1, n=int(p[1]), mode=p[0], label=(p[2] if len(p) > 2 and p[2] else None), grow=(int(p[3]) if len(p) > 3 else 0)))
    elif k == "pyr":
        sc.add(Pyramid((360, 240, 1560, 880), [t0 + 0.2 + 0.5 * j for j in range(5)], t0, t1, top_label="IMOLA", labels={0: "i primi", 4: "gli ultimi"}))
    elif k == "office":
        n = int(p[0])
        sc.add(Office((420, 260, 1500, 870), t0, t1, queue=[(t0, 1), (t0 + 1.5, n)], sign="IMOLA · SCHEMA", s=0.5))
    elif k == "growth":
        vals = [float(v) for v in p]
        sc.add(Growth((360, 300, 1560, 820), vals, t0, t1, dur=2.5, labels={0: "inizio", len(vals) - 1: "fine"}, fmt=lambda v: f"{v:g}"))
        sc.add(Text("schema semplificato · valori indicativi", (960, 870), t0, t1, size=24, fnt=COURR, color=GREY, anchor="mm"))
    elif k == "check":
        n = int(p[0]); items = ["Rendimento troppo alto", "Nessuna autorizzazione", "Interessi da dove?", "Fiducia di gruppo", "Documenti deboli"]
        sc.add(Check([(t0 - 5 if j < n - 1 else t0 + 0.2, f"{j + 1}. {items[j]}") for j in range(n)], (560, 300), t0, t1, size=40, width=800))
    elif k == "board":
        sc.add(board_el(int(p[0]), t0, t1))
    elif k == "crowd":
        sc.add(Crowd((200, 420, 1720, 860), 26, t0, t1, s=0.42, seed=i))
    elif k == "tl":
        evs = [e.split("|") for e in arg.split(";")]
        sc.add(Timeline(300, 1620, 600, [dict(top=e[0], bottom=e[1], t=t0 + 0.3 + 0.6 * j, hl=(j == len(evs) - 1)) for j, e in enumerate(evs)], t0, t1, size=46))
    elif k == "court":
        sc.add(Icon("court", (960, 470), t0, t1, size=380, label=arg), "pop")
        sc.add(Figure([(t0, 1420, FY)], t0 + 0.3, t1, kind="judge", s=0.9, flip=-1), "pop")
    elif k == "bars":
        vals = [(p[2 * j], float(p[2 * j + 1])) for j in range(len(p) // 2)]; mx = max(v for _, v in vals)
        gap = 150 if len(vals) <= 3 else 120
        for j, (lab, v) in enumerate(vals):
            y = 420 + j * gap
            sc.add(Text(lab, (300, y - 40), t0 + 0.2 * j, t1, size=40, fnt=OSW, color=GOLD))
            sc.add(Bar(300, y + 20, 1300, 60, [(t0 + 0.2 * j, 0.0), (t0 + 0.2 * j + 0.8, v / mx)], t0 + 0.2 * j, t1, color=(RED if j == len(vals) - 1 else (90, 110, 160))))
        sc.add(Text("schema semplificato · proporzioni indicative", (960, 860), t0, t1, size=24, fnt=COURR, color=GREY, anchor="mm"))
    elif k == "flow":
        a_, b_ = arg.split(">")
        sc.add(Pill(a_, (520, 560), t0, t1, size=44))
        sc.add(Arrow((880, 560), (1040, 560), t0 + 0.3, t1, color=RED))
        sc.add(Pill(b_, (1400, 560), t0 + 0.7, t1, size=44, accent=True))
    elif k == "cover":
        sc.add(Img(cover_folder25(620), (960, 560), t0, t1, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 025", (1180, 360), t0 + 0.6, t1, size=70, rot=-12))
    elif k == "subscribe":
        sc.add(Img(wordmark(120), (960, 470), t0, t1, anim="pop", shadow=False), "hit")
        sc.add(Pill("ISCRIVITI · OGNI GIORNO UN NUOVO CASO", (960, 700), t0 + 0.4, t1, size=50, accent=True))
    elif k == "fig":
        sc.add(Figure(walk([(60, FY), (380, FY)], t0, 520), t0, t1, kind=p[0], s=1.0, label=(p[1] if len(p) > 1 and p[1] else None)), "pop")
    else:
        raise ValueError(cmd)

def build(i, dur, a, words):
    used = {}
    def T(p, n=None):
        cs = lambda s: re.sub(r"[^\w']", "", s.lower())
        hits = [w for w in words if cs(w[0]) == cs(p)] or [w for w in words if cs(w[0]).startswith(cs(p))]
        if n is None:
            n = used.get(p, 0); used[p] = n + 1
        if hits: return a + hits[min(n, len(hits) - 1)][1]
        return None
    sc = Scene(dur)
    h = SCENES_H[i][0]
    start = a
    if FIRST.get(h) == i and h > 0:
        num = f"{h:02d}" if h < LASTCH else None
        sc.add(Chapter(num, CHT[h], a, a + 2.4)); start = a + 2.5
    beats = []
    for w, cmd in V.get(i, []):
        t = T(w); t = (a + 0.5 if t is None else t - 0.25)
        beats.append((max(start, t), cmd))
    beats.sort(key=lambda b: b[0])
    st = [b for b in beats if b[1].split(":")[0] not in ("t", "stamp", "fig")]
    for j, (t, cmd) in enumerate(st):
        t1 = st[j + 1][0] - 0.05 if j + 1 < len(st) else None
        stage(sc, cmd, t, t1, a, dur, i)
    for t, cmd in beats:
        k, _, arg = cmd.partition(":")
        nxt = [b for b in st if b[0] > t + 0.3]
        t1 = nxt[0][0] - 0.05 if nxt else None
        if k == "t":
            nt = [b[0] for b in beats if b[1].startswith("t:") and b[0] > t]
            sc.add(Pill(arg, (960, 205), t, (nt[0] if nt else None), size=42, accent=True))
        elif k == "stamp":
            sc.add(Stamp(arg, (1280, 700), t, t1, size=(96 if len(arg) <= 16 else int(96 * 16 / len(arg))), rot=-9))
        elif k == "fig":
            stage(sc, cmd, t, t1, a, dur, i)
    sc.footer = F[h] + (" · documenti e schemi ricostruiti" if h not in (12,) else "")
    return sc

def thumbnail(path="thumbnail.jpg"):
    configure(1920, 1080, 30)
    bg = make_bg(25).convert("RGBA"); lay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    im = rich_img("Il banchiere\ndi *Dio*", SERIF, 150, color=WHITE, lh=1.0)
    place(lay, im, (90, 200), "la")
    f2 = font(OSW, 330, 700)
    d.text((1430, 470), "100%", font=f2, fill=GOLD + (255,), anchor="mm", stroke_width=8, stroke_fill=(20, 18, 16, 255))
    f3 = font(OSW, 58, 700)
    d.text((1430, 690), "DI INTERESSI ALL'ANNO", font=f3, fill=WHITE + (255,), anchor="mm")
    place(lay, fx.icon("priest", 260), (1180, 900), "mm"); place(lay, fx.icon("moneybag", 220), (1660, 910), "mm")
    st2 = stamp_img("CASO 025", size=60, rot=-8); place(lay, st2, (380, 110), "mm")
    f = font(OSW, 50, 700); s_ = "IMOLA 1958 · UN VOTO DI SCARTO"; tw = tl(d, s_, f)
    d.rectangle([90, 800, 90 + tw + 60, 905], fill=(230, 190, 40, 255))
    d.text((120, 852), s_, font=f, fill=(20, 18, 16, 255), anchor="lm")
    place(lay, wordmark(70), (90, 985), "lm")
    out = Image.alpha_composite(bg, lay).convert("RGB"); out.save(path, quality=92)
