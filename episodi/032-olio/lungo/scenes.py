import sys, os, re, math
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
from script import SCENES_H, CH

W, H = 1920, 1080
FY = 870
MAPB = (160, 250, 1760, 880)
RBOX = (260, 240, 1660, 860)
MT = "mappa: Natural Earth · schema non in scala"

TM = "TIME (1965)"; WS = "Wikipedia (Salad oil scandal)"; WT = "Wikipedia (T. De Angelis)"; WB = "Wikipedia (The Great Salad Oil Swindle)"
MW = "MoneyWeek (2020)"; TF = "TodayIFoundOut (2015)"; BZ = "Benzinga (2021)"; AG = "AgWeb (2023)"; FO = "Fortune (2024)"; DM = "DaveManuel (2025)"; BLS = "indice CPI USA (BLS)"
F = {0: "Fonti: " + TM + " · " + WS + " · " + WT + " · " + BZ + " · " + TF,
     1: "Fonti: " + TF + " · " + WS + " · " + FO + " · " + TM + " · " + BZ,
     2: "Fonti: " + WT + " · " + BZ + " · " + FO + " · " + WS + " · " + WB + " · " + AG,
     3: "Fonti: " + TM + " · " + WT + " · " + BZ + " · " + AG + " · " + TF + " · " + MW + " · " + FO,
     4: "Fonti: " + TM + " · " + WS + " · " + WT + " · " + TF + " · " + FO + " · " + AG + " · " + MW,
     5: "Fonti: " + TM + " · " + WS + " · " + BZ + " · " + AG + " · " + FO + " · " + TF,
     6: "Fonti: " + WS + " · " + WT + " · " + TM + " · " + BZ + " · " + AG + " · " + TF + " · " + FO,
     7: "Fonti: " + TM + " · " + WS + " · " + WT + " · " + FO + " · " + TF + " · " + BZ + " · " + AG + " · " + BLS,
     8: "Fonti: " + WS + " · " + WT + " · " + TM + " · " + TF + " · " + BZ + " · " + AG + " · " + MW,
     9: "Fonti: " + FO + " · " + WS + " · " + TM + " · " + WT + " · " + WB + " · " + MW + " · " + BZ + " · " + AG + " · " + TF,
     10: "Fonti: " + WS + " · " + WT + " · " + TM + " · " + FO + " · " + AG + " · " + BZ,
     11: "Indicazioni generali, non consulenza finanziaria",
     12: "Fonti: tutte in descrizione · ricostruzione a scopo divulgativo"}

CHT = {1: "L'epoca\ne il *luogo*", 2: "I *protagonisti*", 3: "Dal Bronx\na *Bayonne*", 4: "Il trucco\ndei *serbatoi*", 5: "La *scommessa*",
       6: "Il *crollo*", 7: "I *conti*", 8: "Il *processo*", 9: "Cosa è\nsuccesso *dopo*",
       10: "Le domande *aperte*", 11: "La *lezione*", 12: "Il *verdetto*"}
LASTCH = 12
FIRST = {}
for k, (h, _) in enumerate(SCENES_H):
    FIRST.setdefault(h, k)

BOARD = [("TINO DE ANGELIS", "imprenditore · New York 1915", "person"), ("I MAGAZZINI", "controllata di American Express", "card"), ("51 CREDITORI", "banche e industrie", "card"),
         ("IRA HAUPT", "società di Wall Street", "card"), ("GLI ISPETTORI", "i controlli", "person"), ("NORMAN MILLER", "giornalista · Wall Street Journal", "person")]
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
        sc.add(Rete(RBOX, t0, t1, n=int(p[1]), mode=p[0], label=(p[2] if len(p) > 2 and p[2] else None), grow=(int(p[3]) if len(p) > 3 else 0), center="ALLIED"))
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
        n = int(p[0]); items = ["Chi controlla non dipenda dal controllato", "Numeri troppo grandi? Confrontali", "La leva moltiplica tutto", "Un nome famoso non è una garanzia", "Informati su chi custodisce i soldi"]
        sc.add(Check([(t0 - 5 if j < n - 1 else t0 + 0.2, f"{j + 1}. {items[j]}") for j in range(n)], (500, 300), t0, t1, size=40, width=920))
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
        sc.add(Img(cover_folder32(620), (960, 560), t0, t1, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 032", (1180, 360), t0 + 0.6, t1, size=70, rot=-12))
    elif k == "farm":
        farm_el(sc, int(p[0]), t0, t1)
    elif k == "floor":
        floor_el(sc, int(p[0]), t0, t1)
    elif k == "chain":
        chain_el(sc, int(p[0]), t0, t1)
    elif k == "subscribe":
        sc.add(Img(wordmark(120), (960, 470), t0, t1, anim="pop", shadow=False), "hit")
        sc.add(Pill("ISCRIVITI · OGNI GIORNO UN NUOVO CASO", (960, 700), t0 + 0.4, t1, size=50, accent=True))
    elif k == "fig":
        sc.add(Figure(walk([(330, FY), (430, FY)], t0, 300), t0, t1, kind=p[0], s=1.0, label=(p[1] if len(p) > 1 and p[1] else None)), "pop")
    else:
        raise ValueError(cmd)

def farm_el(sc, n, t0, t1):
    """LA SCENOGRAFIA: il parco serbatoi di Bayonne. 0 = il deposito sul porto; 1 = il controllo dall'alto; 2 = i serbatoi in sezione;
    3 = i tubi; 4 = le ricevute false; 5 = arrivano gli ispettori dei creditori"""
    sc.add(Icon("skyline", (1650, 300), t0, t1, size=200, label="MANHATTAN"), "pop")
    if n == 0:
        sc.add(Icon("tankfarm", (860, 560), t0, t1, size=560, label="BAYONNE · IL DEPOSITO"), "pop")
        sc.add(Icon("tanker", (1500, 700), t0 + 0.5, t1, size=260), "pop")
    elif n == 1:
        sc.add(Icon("tank", (900, 560), t0, t1, size=520), "pop")
        sc.add(Icon("dipstick", (1230, 360), t0 + 0.4, t1, size=200, label="LA MISURA DALL'ALTO"), "pop")
        sc.add(Figure([(t0, 360, FY), (t0 + 1.2, 520, FY)], t0, t1, kind="expert", s=0.95, label="ISPETTORE"), "pop")
        sc.add(Figure([(t0 + 0.3, 1620, FY)], t0 + 0.3, t1, kind="worker", s=0.95, flip=-1, label="CUSTODE"), "pop")
    elif n == 2:
        for j, x in enumerate((520, 960, 1400)):
            sc.add(Icon("tank_x" if j != 1 else "tank_x", (x, 560), t0 + 0.3 * j, t1, size=360), "pop")
        sc.add(Pill("SOTTO L'OLIO, L'ACQUA", (960, 210), t0 + 0.9, t1, size=40, accent=True))
    elif n == 3:
        sc.add(Icon("pipes", (960, 540), t0, t1, size=560, label="L'OLIO SPOSTATO DA UN SERBATOIO ALL'ALTRO"), "pop")
        sc.add(Arrow((760, 760), (1160, 760), t0 + 0.6, t1, color=GOLD))
    elif n == 4:
        for j, x in enumerate((640, 960, 1280)):
            sc.add(Icon("wreceipt", (x, 560 - 20 * j), t0 + 0.3 * j, t1, size=320), "pop")
        sc.add(Stamp("FALSE", (1300, 330), t0 + 1.2, t1, size=90, rot=-10))
    else:
        sc.add(Icon("tank_x", (1000, 560), t0, t1, size=440, label="LA VERITÀ"), "pop")
        for j, x in enumerate((360, 540)):
            sc.add(Figure([(t0, x - 200, FY), (t0 + 1.3, x, FY)], t0 + 0.2 * j, t1, kind="expert", s=0.9), "pop")
        sc.add(Icon("magnifier", (1480, 520), t0 + 0.7, t1, size=220), "pop")
    sc.add(Text("schema · serbatoi e sagome stilizzati, non in scala · ricostruzione", (960, 892), t0, t1, size=24, fnt=COURR, color=GREY, anchor="mm"))

def floor_el(sc, n, t0, t1):
    """LA SECONDA SCENOGRAFIA: Wall Street. 0 = la Borsa; 1 = i contratti e il prezzo che sale; 2 = il prezzo che crolla; 3 = società sospese e panico; 4 = la lezione"""
    sc.add(Icon("exchange", (330, 420), t0, t1, size=300, label="WALL STREET"), "pop")
    if n == 0:
        sc.add(Crowd((620, 520, 1760, 860), 14, t0 + 0.3, t1, s=0.42, seed=3))
        sc.add(Icon("ticker", (1200, 330), t0 + 0.5, t1, size=220), "pop")
    elif n == 1:
        sc.add(Icon("price_up", (1150, 520), t0 + 0.2, t1, size=440, label="CONTRATTI SULL'OLIO"), "pop")
        sc.add(Icon("oildrop", (1620, 360), t0 + 0.6, t1, size=180), "pop")
    elif n == 2:
        sc.add(Icon("price_down", (1150, 520), t0 + 0.2, t1, size=440, label="IL PREZZO SCENDE"), "pop")
        sc.add(Icon("dollar", (1620, 360), t0 + 0.6, t1, size=180, label="SERVE DENARO"), "pop")
    elif n == 3:
        sc.add(Crowd((620, 520, 1760, 860), 22, t0 + 0.2, t1, s=0.42, seed=7))
        sc.add(Pill("SOSPESE", (1180, 330), t0 + 0.6, t1, size=56, accent=True))
    else:
        sc.add(Icon("shield_ok", (1150, 520), t0 + 0.2, t1, size=400, label="I CLIENTI"), "pop")
    sc.add(Text("schema · ambienti e sagome stilizzati · ricostruzione", (960, 892), t0, t1, size=24, fnt=COURR, color=GREY, anchor="mm"))

def chain_el(sc, n, t0, t1):
    """la catena della garanzia: olio -> ricevuta -> banca -> denaro"""
    seq = [("tank_full", "L'OLIO DICHIARATO"), ("inspector", "LA VERIFICA"), ("wreceipt", "LA RICEVUTA"), ("bank", "LA BANCA"), ("dollar_bag", "IL PRESTITO")]
    show = {0: [0, 2], 1: [0, 1, 2], 2: [2, 3, 4]}[n]
    xs = [420, 960, 1500] if len(show) == 3 else [620, 1300]
    for j, (q, x) in enumerate(zip(show, xs)):
        sc.add(Icon(seq[q][0], (x, 540), t0 + 0.5 * j, t1, size=300, label=seq[q][1]), "pop")
        if j: sc.add(Arrow((xs[j - 1] + 180, 540), (x - 180, 540), t0 + 0.5 * j - 0.2, t1, color=RED))
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
    bg = make_bg(32).convert("RGBA"); lay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    im = rich_img("L'olio\nera\n*acqua*", SERIF, 170, color=WHITE, lh=1.0)
    place(lay, im, (90, 120), "la")
    place(lay, fx.icon("tank_x", 520), (1430, 600), "mm")
    f2 = font(OSW, 200, 700)
    d.text((1430, 200), "$150 MLN", font=f2, fill=GOLD + (255,), anchor="mm", stroke_width=10, stroke_fill=(20, 18, 16, 255))
    st2 = stamp_img("CASO 032", size=60, rot=-8); place(lay, st2, (1760, 960), "mm")
    f = font(OSW, 54, 700); s_ = "51 CREDITORI"; tw = tl(d, s_, f)
    d.rectangle([90, 820, 90 + tw + 60, 925], fill=(230, 190, 40, 255))
    d.text((120, 872), s_, font=f, fill=(20, 18, 16, 255), anchor="lm")
    place(lay, wordmark(70), (90, 1005), "lm")
    out = Image.alpha_composite(bg, lay).convert("RGB"); out.save(path, quality=92)
