import sys, os, re, math
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
from script import SCENES_H, CH

W, H = 1920, 1080
FY = 870
MAPB = (160, 250, 1760, 880)
RBOX = (260, 240, 1660, 860)
MT = "mappa: Natural Earth · schema non in scala"

IT = "Il Tempo (2003)"; QN = "Quotidiano Nazionale (2022, 2023)"; SK = "Sky TG24/ANSA (2022)"; LV = "La Voce di New York (2014, 2016)"; LN = "La Nazione (2023)"
SR = "storiaradiotv (2017)"; CI = "cinemaitaliano (2011)"; AV = "Avvenire (2010)"; IP = "Il Post (2010)"; WE = "Wikipedia (L. Luttazzi; W. Chiari)"
GP = "Il Giornale Popolare (2026)"; AI = "AIVM (2020)"; SO = "Sorrisi (2023)"; BL = "Blitz quotidiano (2010)"; LB = "Libero (2010)"; NR = "Normattiva"
F = {0: "Fonti: " + IT + " · " + QN + " · " + SK + " · " + LV + " · " + SR,
     1: "Fonti: " + LN + " · " + QN + " · " + IT + " · " + SR + " · " + NR,
     2: "Fonti: " + WE + " · " + LN + " · " + QN + " · " + GP + " · " + IT + " · " + AV,
     3: "Fonti: " + WE + " · " + SR + " · " + IT + " · " + IP + " · " + QN + " · " + AV + " · " + SO + " · " + BL,
     4: "Fonti: " + IT + " · " + SR + " · " + GP + " · " + LN + " · " + LV + " · " + AI + " · " + SK,
     5: "Fonti: " + LV + " · " + CI + " · " + QN + " · " + SR + " · " + IT + " · " + GP + " · " + WE,
     6: "Fonti: " + LN + " · " + GP + " · " + AI + " · " + QN + " · " + IT + " · " + SK,
     7: "Fonti: " + IT + " · " + SK + " · " + QN + " · " + LN + " · " + LV + " · " + SR + " · " + CI,
     8: "Fonti: " + IT + " · " + SK + " · " + WE + " · " + GP + " · " + LN + " · " + QN + " · " + LV,
     9: "Fonti: " + CI + " · " + QN + " · " + IT + " · " + SR + " · " + AV + " · " + SO + " · " + SK + " · " + BL + " · " + LB,
     10: "Fonti: " + SR + " · " + AI + " · " + LV + " · " + LN + " · " + WE + " · " + GP + " · " + IT + " · " + QN,
     11: "Indicazioni generali, non consulenza legale · Costituzione art. 27 · c.p.p. art. 314",
     12: "Fonti: tutte in descrizione · ricostruzione a scopo divulgativo"}

CHT = {1: "L'epoca\ne il *luogo*", 2: "I *protagonisti*", 3: "Da Trieste alla\n*Hit Parade*", 4: "La telefonata\ne l'*arresto*", 5: "Regina *Coeli*",
       6: "L'*indagine*", 7: "La *svolta*", 8: "Il *processo*", 9: "Cosa è\nsuccesso *dopo*",
       10: "Le domande *aperte*", 11: "La *lezione*", 12: "Il *verdetto*"}
LASTCH = 12
FIRST = {}
for k, (h, _) in enumerate(SCENES_H):
    FIRST.setdefault(h, k)

BOARD = [("LELIO LUTTAZZI", "musicista · Trieste 1923", "person"), ("WALTER CHIARI", "attore · l'amico", "person"), ("IL CONOSCENTE", "telefono intercettato", "person"),
         ("GUARDIA DI FINANZA", "l'indagine", "card"), ("I GIORNALI", "la prima pagina", "card"), ("ROSSANA", "la seconda moglie", "person")]
BXY = [(330, 400), (750, 400), (1170, 400), (1590, 400), (330, 720), (750, 720), (1170, 720), (1590, 720)]

def board_el(n, t0, t1):
    nodes = {}
    for j in range(n + 1):
        nm, role, kind = BOARD[j]
        nodes[f"n{j}"] = dict(xy=BXY[j], name=nm, role=role, t=t0 + (0.2 if j == n else -5), rot=(-3 + 2 * (j % 3)))
    pairs = [(0, 1), (1, 2), (0, 2), (2, 3), (3, 0), (0, 4), (0, 5)]
    links = [(f"n{p}", f"n{q}", t0 - 5 if max(p, q) < n else t0 + 0.6) for p, q in pairs if max(p, q) <= n]
    return Board(nodes, links, t0, t1, cw=220)

from data import SC
V = {i: b for i, (_, _, b) in enumerate(SC)}

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

ALIAS = {"flask": "potion", "bottle": "potion", "door": "lock", "hand": "coin", "police": "guard2", "eiffel": "museum", "signature": "quill", "questura": "prison", "crowd_icon": "family", "lab": "tubes", "suit": "nophoto", "critic": "meeting", "shield": "shield_ok", "hospital": "hospital2", "reward": "moneybag", "basilica": "convent", "calendar_x": "hourglass", "van": "truck", "warehouse": "boxbooks", "window": "window", "arrow_icon": "front", "scroll_icon": "letter", "note_icon": "music", "stars_icon": "stars", "map_icon": "globe2", "check": "shield_ok", "stop": "warn", "doc_icon": "letter", "mic": "microphone",
         "clock_icon": "hourglass", "fig_icon": "nophoto", "ticket": "tag"}
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
        if len(p[1]) <= 6:
            sc.add(Calendar((960, 560), 320, [(t0, p[0], p[1])], t0, t1), "paper")
        else:
            sc.add(Pill(p[0], (960, 400), t0, t1, size=44, accent=True))
            sc.add(Big(p[1], (960, 560), t0 + 0.2, t1, size=(130 if len(p[1]) <= 14 else 100)))
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
        sc.add(Rete(RBOX, t0, t1, n=int(p[1]), mode=p[0], label=(p[2] if len(p) > 2 and p[2] else None), grow=(int(p[3]) if len(p) > 3 else 0), center="ROMA"))
    elif k == "pyr":
        sc.add(Pyramid((360, 240, 1560, 880), [t0 + 0.2 + 0.5 * j for j in range(5)], t0, t1, top_label="VALLESUSA", labels={0: "i primi", 4: "gli ultimi"}))
    elif k == "office":
        n = int(p[0])
        sc.add(Office((420, 260, 1500, 870), t0, t1, queue=[(t0, 1), (t0 + 1.5, n)], sign="SCHEMA", s=0.5))
    elif k == "growth":
        vals = [float(v) for v in p]
        sc.add(Growth((360, 300, 1560, 820), vals, t0, t1, dur=2.5, labels={0: "inizio", len(vals) - 1: "fine"}, fmt=lambda v: f"{v:g}"))
        sc.add(Text("schema semplificato · valori indicativi", (960, 870), t0, t1, size=24, fnt=COURR, color=GREY, anchor="mm"))
    elif k == "check":
        n = int(p[0]); items = ["Presunzione di innocenza", "Un'intercettazione è un indizio", "Attenzione ai favori per altri", "Ingiusta detenzione: riparazione", "Una smentita vale un arresto"]
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
        q = arg.split(">")
        if len(q) == 2:
            sc.add(Pill(q[0], (520, 560), t0, t1, size=44))
            sc.add(Arrow((880, 560), (1040, 560), t0 + 0.3, t1, color=RED))
            sc.add(Pill(q[1], (1400, 560), t0 + 0.7, t1, size=44, accent=True))
        else:
            for j, x in enumerate((420, 960, 1500)):
                sc.add(Pill(q[j], (x, 560), t0 + 0.6 * j, t1, size=44, accent=(j == 2)))
            for j, x in enumerate((600, 1140)):
                sc.add(Arrow((x, 560), (x + 180, 560), t0 + 0.3 + 0.6 * j, t1, color=RED))
    elif k == "cover":
        sc.add(Img(cover_folder31(620), (960, 560), t0, t1, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 031", (1180, 360), t0 + 0.6, t1, size=70, rot=-12))
    elif k == "home":
        home_el(sc, int(p[0]), t0, t1)
    elif k == "cella":
        cella_el(sc, int(p[0]), t0, t1)
    elif k == "net":
        net_el(sc, int(p[0]), t0, t1)
    elif k == "prints":
        sc.add(Icon("finger", (560, 540), t0, t1, size=330, label="1926 · LO SCONOSCIUTO"), "pop")
        sc.add(Icon("finger", (1360, 540), t0 + 0.5, t1, size=330, label="SCHEDARIO · BRUNERI"), "pop")
        sc.add(Text("=", (960, 470), t0 + 1.0, t1, size=200, fnt=OSW, color=GOLD, anchor="mm"))
        sc.add(Text("schema · impronte stilizzate, non quelle originali", (960, 880), t0, t1, size=24, fnt=COURR, color=GREY, anchor="mm"))
    elif k == "subscribe":
        sc.add(Img(wordmark(120), (960, 470), t0, t1, anim="pop", shadow=False), "hit")
        sc.add(Pill("ISCRIVITI · OGNI GIORNO UN NUOVO CASO", (960, 700), t0 + 0.4, t1, size=50, accent=True))
    elif k == "fig":
        sc.add(Figure(walk([(330, FY), (430, FY)], t0, 300), t0, t1, kind=p[0], s=1.0, label=(p[1] if len(p) > 1 and p[1] else None)), "pop")
    else:
        raise ValueError(cmd)

def home_el(sc, n, t0, t1):
    """LA SCENOGRAFIA: l'attico di Luttazzi. 0 = salotto con pianoforte e telefono; 1 = Luttazzi telefona; 2 = la linea arriva al registratore; 3 = arrivano i finanzieri"""
    sc.add(Icon("fountain", (300, 330), t0, t1, size=200, label="VICINO A TREVI"), "pop")
    if n == 0:
        sc.add(Icon("piano", (1250, 560), t0 + 0.2, t1, size=420), "pop")
        sc.add(Icon("phone", (620, 600), t0 + 0.4, t1, size=240, label="IL TELEFONO DI CASA"), "pop")
    elif n == 1:
        sc.add(Figure([(t0, 760, FY), (t0 + 1.2, 900, FY)], t0, t1, kind="suit", s=1.0, label="LUTTAZZI"), "pop")
        sc.add(Icon("phonecall", (1160, 600), t0 + 0.3, t1, size=280, label="CHIAMA IL NUMERO"), "pop")
    elif n == 2:
        sc.add(Icon("phonecall", (560, 560), t0, t1, size=260, label="LA CHIAMATA"), "pop")
        sc.add(Arrow((760, 560), (1120, 560), t0 + 0.4, t1, color=RED))
        sc.add(Icon("taperec", (1360, 560), t0 + 0.8, t1, size=320, label="REGISTRATA"), "pop")
    else:
        sc.add(Icon("piano", (560, 600), t0, t1, size=300), "pop")
        for j, x in enumerate((1100, 1300)):
            sc.add(Figure([(t0, x + 300, FY), (t0 + 1.4, x, FY)], t0 + 0.2 * j, t1, kind="police", s=0.95, flip=-1), "pop")
        sc.add(Icon("gdf", (1650, 330), t0 + 0.5, t1, size=180), "pop")
    sc.add(Text("schema · ambienti e sagome stilizzati, non in scala · ricostruzione", (960, 892), t0, t1, size=24, fnt=COURR, color=GREY, anchor="mm"))

def cella_el(sc, n, t0, t1):
    """LA SECONDA SCENOGRAFIA: la cella d'isolamento a Regina Coeli. 0 = porta chiusa; 1 = scrive; 2 = le tacche dei giorni; 3 = la porta si apre"""
    if n == 0:
        sc.add(Icon("isolation", (760, 540), t0, t1, size=460, label="CELLA D'ISOLAMENTO"), "pop")
        sc.add(Icon("bars", (1300, 540), t0 + 0.4, t1, size=300), "pop")
    elif n == 1:
        sc.add(Icon("desk", (700, 600), t0, t1, size=340), "pop")
        sc.add(Icon("quill", (1200, 560), t0 + 0.4, t1, size=300, label="GLI APPUNTI"), "pop")
    elif n == 2:
        sc.add(Icon("tally27", (960, 540), t0, t1, size=520, label="27 GIORNI"), "pop")
    else:
        sc.add(Icon("isolation", (700, 540), t0, t1, size=420), "pop")
        sc.add(Arrow((960, 560), (1220, 560), t0 + 0.3, t1, color=GOLD))
        sc.add(Figure([(t0 + 0.4, 1200, FY), (t0 + 2.4, 1550, FY)], t0 + 0.4, t1, kind="suit", s=1.0, label="LIBERO"), "pop")
    sc.add(Text("schema · cella stilizzata, non quella reale · ricostruzione", (960, 892), t0, t1, size=24, fnt=COURR, color=GREY, anchor="mm"))

def net_el(sc, n, t0, t1):
    """rete delle telefonate: chi chiama chi (schema)"""
    pts = [(560, 420, "CHIARI", "clapper"), (960, 640, "LUTTAZZI", "piano"), (1360, 420, "IL CONOSCENTE", "nophoto")]
    for j, (x, y, lab, ic) in enumerate(pts):
        sc.add(Icon(ic, (x, y), t0 + 0.3 * j, t1, size=200, label=lab), "pop")
    sc.add(Arrow((640, 480), (880, 600), t0 + 0.9, t1, color=GOLD))
    sc.add(Arrow((1040, 600), (1280, 480), t0 + 1.3, t1, color=RED))
    if n >= 4:
        sc.add(Icon("taperec", (1360, 760), t0 + 1.6, t1, size=170, label="INTERCETTATO"), "pop")
    sc.add(Text("schema semplificato · ricostruzione", (960, 892), t0, t1, size=24, fnt=COURR, color=GREY, anchor="mm"))

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
    if st and st[0][0] > start:
        st[0] = (start, st[0][1])
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
            sc.add(Stamp(arg, (1420, 300), t, t1, size=(96 if len(arg) <= 16 else int(96 * 16 / len(arg))), rot=-9))
        elif k == "fig":
            stage(sc, cmd, t, t1, a, dur, i)
    sc.footer = F[h] + (" · documenti e schemi ricostruiti" if h not in (12,) else "")
    return sc

def thumbnail(path="thumbnail.jpg"):
    configure(1920, 1080, 30)
    bg = make_bg(31).convert("RGBA"); lay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    im = rich_img("Arrestato\nper una\n*telefonata*", SERIF, 150, color=WHITE, lh=1.0)
    place(lay, im, (90, 150), "la")
    f2 = font(OSW, 300, 700)
    d.text((1440, 300), "27", font=f2, fill=GOLD + (255,), anchor="mm", stroke_width=10, stroke_fill=(20, 18, 16, 255))
    f3 = font(OSW, 110, 700)
    d.text((1440, 520), "GIORNI", font=f3, fill=GOLD + (255,), anchor="mm", stroke_width=6, stroke_fill=(20, 18, 16, 255))
    d.ellipse([1440 - 190, 790 - 190, 1440 + 190, 790 + 190], fill=(236, 226, 200, 255))
    place(lay, fx.icon("phonecall", 330), (1440, 790), "mm")
    st2 = stamp_img("CASO 031", size=60, rot=-8); place(lay, st2, (1700, 110), "mm")
    f = font(OSW, 54, 700); s_ = "IN CARCERE DA INNOCENTE"; tw = tl(d, s_, f)
    d.rectangle([90, 820, 90 + tw + 60, 925], fill=(230, 190, 40, 255))
    d.text((120, 872), s_, font=f, fill=(20, 18, 16, 255), anchor="lm")
    place(lay, wordmark(70), (90, 1005), "lm")
    out = Image.alpha_composite(bg, lay).convert("RGB"); out.save(path, quality=92)
