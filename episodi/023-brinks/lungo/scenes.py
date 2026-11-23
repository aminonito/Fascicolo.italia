import sys, os, re, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from brk import *
import fx, met
from script import SCENES_H, CH

W, H = 1920, 1080
FY = 870
MAPB = (160, 250, 1760, 880)
DEP = (160, 250, 1760, 860)          # scenografia principale: il deposito (pianta schematica)
MT = "mappa: Natural Earth · schema non in scala"

FB = "FBI (Famous Cases; storia 2007) · Wikipedia · History.com · Smithsonian (2025) · WGBH (2016) · EBSCO"
F = {0: "Fonti: " + FB,
     1: "Fonti: Wikipedia (Brink's; Great Brink's Robbery) · GlobeNewswire (Brink's, 2019) · FBI · WGBH (2016) · indice CPI USA (BLS)",
     2: "Fonti: FBI (Famous Cases) · Corte suprema USA, Pino v. Landon (1955) · Wikipedia · History.com · Smithsonian · WGBH",
     3: "Fonti: FBI (Famous Cases) · Wikipedia · History.com · Smithsonian (2025) · WGBH (2016) · EBSCO",
     4: "Fonti: FBI (Famous Cases; storia 2007; reperto «Brinks Robbery Cap») · Wikipedia · History.com · Smithsonian · WGBH · indice CPI USA",
     5: "Fonti: FBI (Famous Cases; reperto «Brinks Robbery Cap») · Wikipedia · Smithsonian (2025) · History.com · WGBH",
     6: "Fonti: FBI (Famous Cases) · Wikipedia · Smithsonian (2025) · History.com · WGBH (2016) · EBSCO",
     7: "Fonti: FBI (Famous Cases; storia 2007) · Wikipedia · Smithsonian (2025) · History.com · EBSCO",
     8: "Fonti: FBI (Famous Cases; storia 2007) · Wikipedia · Smithsonian (2025) · History.com · WGBH · EBSCO",
     9: "Fonti: Wikipedia · WGBH (2016) · History.com · Smithsonian (2025) · EBSCO · FBI · indice CPI USA",
     10: "Fonti: Wikipedia · FBI · History.com · Smithsonian · WGBH · EBSCO",
     11: "Consigli generali di prudenza · non consulenza legale né di sicurezza",
     12: "Fonti: tutte in descrizione · ricostruzione a scopo divulgativo"}

CHT = {1: "Boston,\n*1950*", 2: "I *protagonisti*", 3: "Il *piano*", 4: "La sera del\n*17 gennaio*",
       5: "La *scoperta*", 6: "Sei anni\ndi *indagini*", 7: "La *svolta*", 8: "Il *processo*",
       9: "Dopo la\n*sentenza*", 10: "Le domande *aperte*", 11: "La *lezione*", 12: "Il *verdetto*"}
LASTCH = 12
FIRST = {}
for k, (h, _) in enumerate(SCENES_H):
    FIRST.setdefault(h, k)

BOARD = [("L'OBIETTIVO", "deposito Brink's · Boston", "card"), ("ANTHONY PINO", "nato in Italia · condannato", "person"),
         ("JOSEPH McGINNIS", "condannato", "person"), ("JOSEPH «SPECS» O'KEEFE", "il testimone · reo confesso", "person"),
         ("LA BANDA", "11 uomini · 8 condannati", "card"), ("GLI INVESTIGATORI", "polizia di Boston · FBI", "card")]
BXY = [(960, 450), (420, 450), (1500, 450), (420, 740), (960, 740), (1500, 740)]

def board_el(n, t0, t1):
    nodes = {}
    for j in range(n + 1):
        nm, role, kind = BOARD[j]
        nodes[f"n{j}"] = dict(xy=BXY[j], name=nm, role=role, t=t0 + (0.2 if j == n else -5), rot=(-3 + 2 * (j % 3)))
    pairs = [(0, 1), (0, 2), (0, 3), (3, 4), (1, 4), (1, 5)]
    links = [(f"n{p}", f"n{q}", t0 - 5 if max(p, q) < n else t0 + 0.6) for p, q in pairs if max(p, q) <= n]
    return Board(nodes, links, t0, t1, cw=220)

from data import SC
V = {i: b for i, (_, _, b) in enumerate(SC)}

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

ALIAS = {"shield": "shield_ok", "hospital": "hospital2", "reward": "moneybag", "basilica": "convent", "calendar_x": "hourglass", "van": "truck", "warehouse": "boxbooks", "window": "window", "arrow_icon": "front", "scroll_icon": "letter", "note_icon": "music", "stars_icon": "stars", "map_icon": "globe2", "check": "shield_ok", "stop": "warn", "doc_icon": "letter", "mic": "microphone",
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
        cen, ppd = p[0], float(p[1]) * 4; pins = p[2].split(",") if len(p) > 2 and p[2] else [cen]
        if len(pins) > 1:
            ll = [WPL[q] for q in pins]; lo0, lo1 = min(x for x, y in ll), max(x for x, y in ll); la0, la1 = min(y for x, y in ll), max(y for x, y in ll)
            cen = ((lo0 + lo1) / 2, (la0 + la1) / 2); ppd = min(ppd, 1100 / max(0.3, lo1 - lo0), 420 / max(0.3, la1 - la0))
        routes = []
        if len(p) > 3:
            pts = p[3].split(">")
            routes = [dict(pts=[pts[j], pts[j + 1]], t=t0 + 0.6 + 0.8 * j, d=1.0, icon="person", color=RED) for j in range(len(pts) - 1)]
        sc.add(WorldMap(MAPB, [(t0, cen, ppd * 0.8), (t1 or a + dur, cen, ppd)], t0, t1,
                        pins=[dict(at=q, label=q.upper(), t=t0 + 0.3 + 0.2 * j, side=("l" if q in ("Milano", "Genova") and len(pins) > 1 else "r"), color=(RED if j == 0 else GOLD)) for j, q in enumerate(pins)],
                        routes=routes, title=MT))
    elif k == "dep":
        d0, rb, pr, bg, staff, mode = p[:6]
        kw = dict(doors=int(d0), robbers=int(rb), prog=float(pr), bags=float(bg), staff=staff, night=True, dur=3.0, label=(p[6] if len(p) > 6 else None))
        if mode == "1": kw.update(prog_to=1.0)
        if mode == "2": kw.update(bags_to=0.1)
        sc.add(Deposito(DEP, t0, t1, **kw))
    elif k == "str":
        sc.add(Strada(DEP, t0, t1, truck=("parked" if p[0] == "police" else p[0]) if p[0] != "police" else "none", lookout=(p[1] == "1"),
                      police=(p[0] == "police"), label=(p[2] if len(p) > 2 else None)))
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
        sc.add(Img(cover_folder23(620), (960, 560), t0, t1, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 023", (1180, 360), t0 + 0.6, t1, size=70, rot=-12))
    elif k == "subscribe":
        sc.add(Img(wordmark(120), (960, 470), t0, t1, anim="pop", shadow=False), "hit")
        sc.add(Pill("ISCRIVITI · OGNI GIORNO UN NUOVO CASO", (960, 700), t0 + 0.4, t1, size=50, accent=True))
    elif k == "fig":
        sc.add(Figure(walk([(40, FY), (230, FY)], t0, 420), t0, t1, kind=p[0], s=1.0, label=(p[1] if len(p) > 1 and p[1] else None)), "pop")
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
            sc.add(Stamp(arg, (1280, 700), t, t1, size=96, rot=-9))
        elif k == "fig":
            stage(sc, cmd, t, t1, a, dur, i)
    sc.footer = F[h] + (" · documenti e schemi ricostruiti" if h not in (11, 12) else "")
    return sc

def thumbnail(path="thumbnail.jpg"):
    configure(1920, 1080, 30)
    bg = make_bg(23).convert("RGBA"); lay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    im = rich_img("Avevano le\nchiavi di\n*ogni porta*", SERIF, 150, color=WHITE, lh=1.0)
    place(lay, im, (90, 170), "la")
    place(lay, fx.icon("mask", 440), (1430, 420), "mm")
    place(lay, fx.icon("lockcyl", 330), (1690, 690), "mm")
    place(lay, fx.icon("bags", 300), (1230, 720), "mm")
    st2 = stamp_img("CASO 023", size=60, rot=-8); place(lay, st2, (380, 90), "mm")
    st = stamp_img("BOSTON 1950", size=70, rot=-10); place(lay, st, (1600, 930), "mm")
    f = font(OSW, 52, 700); s_ = "2,7 MILIONI DI DOLLARI IN CIRCA 20 MINUTI"; tw = tl(d, s_, f)
    d.rectangle([90, 800, 90 + tw + 60, 905], fill=(230, 190, 40, 255))
    d.text((120, 852), s_, font=f, fill=(20, 18, 16, 255), anchor="lm")
    place(lay, wordmark(70), (90, 975), "lm")
    out = Image.alpha_composite(bg, lay).convert("RGB"); out.save(path, quality=92)
