# Elementi grafici del caso 003 (schema Ponzi): mappa atlantica, ufficio con la fila, piramide, buoni postali, icone.
import math, random, os, json
from fi import *
import fi
from fx import *
from fx import draw_person

HERE3 = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- icone del caso
_pc = {}
def pic(name, size, color=None):
    k = (name, size, color)
    if k in _pc: return _pc[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); w = max(2, S // 22)
    g = GOLD + (255,); pap = (236, 228, 208, 255); ink = INK + (255,); grn = (88, 128, 84, 255)
    if name == "coupon":
        d.rectangle([P(.06, .18), P(.94, .82)], fill=(214, 226, 236, 255))
        for k in range(15):
            x = .06 + k * .0586
            d.ellipse([P(x - .012, .165), P(x + .012, .195)], fill=(0, 0, 0, 0))
            d.ellipse([P(x - .012, .805), P(x + .012, .835)], fill=(0, 0, 0, 0))
        d.rectangle([P(.10, .24), P(.90, .76)], outline=(70, 96, 130, 255), width=w // 2)
        d.ellipse([P(.14, .32), P(.40, .68)], outline=(70, 96, 130, 255), width=w // 2)
        d.line([P(.14, .50), P(.40, .50)], fill=(70, 96, 130, 255), width=w // 3)
        d.arc([P(.20, .32), P(.34, .68)], 0, 360, fill=(70, 96, 130, 255), width=w // 3)
        for k, y in enumerate((.36, .46, .56, .64)):
            d.line([P(.46, y), P(.86 - .08 * (k % 2), y)], fill=(70, 96, 130, 255), width=w // 2)
    elif name == "stamp":
        d.rectangle([P(.14, .10), P(.86, .90)], fill=(240, 234, 222, 255))
        for k in range(9):
            for (x, y) in ((.14 + k * .09, .10), (.14 + k * .09, .90)):
                d.ellipse([P(x - .025, y - .025), P(x + .025, y + .025)], fill=(0, 0, 0, 0))
            for (x, y) in ((.14, .10 + k * .1), (.86, .10 + k * .1)):
                d.ellipse([P(x - .025, y - .025), P(x + .025, y + .025)], fill=(0, 0, 0, 0))
        d.rectangle([P(.22, .18), P(.78, .82)], fill=(200, 60, 52, 255))
        d.ellipse([P(.36, .28), P(.64, .56)], fill=(240, 220, 200, 255))
        d.text(P(.5, .70), "POSTA", font=font(OSW, S // 9, 700), fill=(255, 255, 255, 255), anchor="mm")
    elif name == "ship":
        d.polygon([P(.04, .58), P(.96, .58), P(.84, .80), P(.14, .80)], fill=(40, 44, 52, 255))
        d.rectangle([P(.20, .46), P(.78, .58)], fill=(230, 226, 214, 255))
        for k in range(6): d.ellipse([P(.25 + k * .09, .50), P(.29 + k * .09, .54)], fill=(60, 60, 70, 255))
        d.rectangle([P(.34, .26), P(.44, .46)], fill=RED + (255,)); d.rectangle([P(.54, .26), P(.64, .46)], fill=RED + (255,))
        d.rectangle([P(.34, .26), P(.44, .30)], fill=(30, 30, 30, 255)); d.rectangle([P(.54, .26), P(.64, .30)], fill=(30, 30, 30, 255))
        for k, (x, y, r) in enumerate(((.42, .18, .05), (.50, .10, .06), (.62, .16, .05))):
            d.ellipse([P(x - r, y - r), P(x + r, y + r)], fill=(150, 150, 150, 160))
        d.line([P(0, .86), P(1, .86)], fill=(90, 130, 170, 255), width=w)
    elif name == "villa":
        d.rectangle([P(.12, .36), P(.88, .78)], fill=(226, 214, 190, 255))
        d.polygon([P(.06, .38), P(.5, .10), P(.94, .38)], fill=(150, 70, 56, 255))
        for k in range(4): d.rectangle([P(.24 + k * .16, .42), P(.30 + k * .16, .76)], fill=(250, 246, 236, 255))
        d.rectangle([P(.44, .58), P(.56, .78)], fill=(90, 62, 40, 255))
        d.rounded_rectangle([P(.10, .82), P(.90, .96)], S // 30, fill=(90, 170, 210, 255))
        d.line([P(.18, .88), P(.38, .88)], fill=(200, 236, 250, 255), width=w // 2); d.line([P(.56, .91), P(.80, .91)], fill=(200, 236, 250, 255), width=w // 2)
    elif name == "car":
        d.rounded_rectangle([P(.04, .48), P(.96, .68)], S // 40, fill=(34, 36, 44, 255))
        d.rounded_rectangle([P(.50, .36), P(.94, .52)], S // 40, fill=(44, 48, 58, 255))
        d.rectangle([P(.90, .38), P(.96, .52)], fill=(200, 196, 180, 255))
        d.rounded_rectangle([P(.10, .14), P(.50, .52)], S // 30, fill=(28, 30, 36, 255))
        d.rectangle([P(.16, .20), P(.44, .36)], fill=(160, 190, 210, 255))
        d.line([P(.04, .58), P(.96, .58)], fill=g, width=w // 2)
        for x in (.24, .78):
            d.ellipse([P(x - .14, .54), P(x + .14, .86)], fill=(18, 18, 20, 255)); d.ellipse([P(x - .07, .62), P(x + .07, .78)], fill=(210, 200, 180, 255))
    elif name == "dollar":
        for k in range(3):
            o = k * .05
            d.rectangle([P(.08 + o, .30 - o), P(.88 + o, .70 - o)], fill=(150, 180, 140, 255), outline=(60, 90, 60, 255), width=w // 2)
        d.ellipse([P(.40, .30 - .10), P(.66, .60)], outline=(60, 90, 60, 255), width=w // 2)
        d.text(P(.53, .40), "$", font=font(SERIF, S // 4), fill=(40, 70, 40, 255), anchor="mm")
    elif name in ("coin", "euro"):
        d.ellipse([P(.08, .08), P(.92, .92)], fill=(214, 168, 70, 255), outline=(150, 110, 30, 255), width=w)
        d.ellipse([P(.20, .20), P(.80, .80)], outline=(240, 210, 130, 255), width=w // 2)
        d.text(P(.5, .5), "€" if name == "euro" else "$", font=font(PB, S // 3), fill=(120, 84, 20, 255), anchor="mm")
    elif name == "phone":
        d.rounded_rectangle([P(.28, .06), P(.72, .94)], S // 14, fill=(30, 32, 38, 255))
        d.rectangle([P(.32, .14), P(.68, .82)], fill=(24, 60, 50, 255))
        d.line([P(.36, .70), P(.44, .58), P(.52, .62), P(.64, .26)], fill=(110, 230, 150, 255), width=w)
        d.polygon([P(.64, .22), P(.58, .30), P(.68, .32)], fill=(110, 230, 150, 255))
    elif name == "warning":
        d.polygon([P(.5, .06), P(.96, .88), P(.04, .88)], fill=(230, 180, 40, 255))
        d.polygon([P(.5, .18), P(.86, .82), P(.14, .82)], fill=(30, 26, 22, 255))
        d.rectangle([P(.46, .36), P(.54, .64)], fill=(230, 180, 40, 255)); d.ellipse([P(.45, .68), P(.55, .78)], fill=(230, 180, 40, 255))
    elif name == "check":
        d.rectangle([P(.04, .26), P(.96, .74)], fill=(220, 230, 214, 255), outline=(90, 110, 90, 255), width=w // 2)
        d.text(P(.10, .32), "ASSEGNO", font=font(OSW, S // 12, 700), fill=(70, 90, 70, 255))
        d.line([P(.10, .52), P(.62, .52)], fill=(120, 140, 120, 255), width=w // 3)
        d.line([P(.56, .66), P(.66, .58), P(.74, .66), P(.84, .58), P(.90, .64)], fill=RED + (255,), width=w // 2)
        d.rectangle([P(.66, .32), P(.90, .44)], outline=(90, 110, 90, 255), width=w // 3)
    elif name == "palm":
        d.line([P(.50, .96), P(.52, .70), P(.56, .40)], fill=(120, 84, 50, 255), width=S // 14)
        for a_ in (-160, -120, -60, -20, -90):
            r = math.radians(a_); x1, y1 = .56 + .38 * math.cos(r), .40 + .30 * math.sin(r) + .14
            d.line([P(.56, .40), P((.56 + x1) / 2, .40 + (y1 - .40) / 2 - .06), P(x1, y1)], fill=(60, 130, 70, 255), width=S // 16, joint="curve")
    elif name == "chart":
        d.line([P(.10, .10), P(.10, .90), P(.92, .90)], fill=(200, 196, 186, 255), width=w)
        d.line([P(.14, .80), P(.34, .66), P(.52, .70), P(.70, .40), P(.88, .16)], fill=g, width=w)
    elif name == "megaphone":
        d.polygon([P(.14, .40), P(.70, .14), P(.70, .86), P(.14, .60)], fill=RED + (255,))
        d.rectangle([P(.06, .38), P(.16, .62)], fill=(60, 60, 64, 255)); d.rectangle([P(.24, .60), P(.34, .86)], fill=(60, 60, 64, 255))
        for r in (.12, .2): d.arc([P(.70 - r, .50 - r * 2), P(.70 + r * 1.5, .50 + r * 2)], -40, 40, fill=(240, 230, 210, 255), width=w // 2)
    elif name == "hourglass":
        d.rectangle([P(.20, .06), P(.80, .14)], fill=(120, 84, 50, 255)); d.rectangle([P(.20, .86), P(.80, .94)], fill=(120, 84, 50, 255))
        d.polygon([P(.26, .14), P(.74, .14), P(.54, .50), P(.74, .86), P(.26, .86), P(.46, .50)], fill=(200, 220, 230, 160))
        d.polygon([P(.34, .26), P(.66, .26), P(.5, .46)], fill=(220, 190, 120, 255)); d.polygon([P(.32, .86), P(.68, .86), P(.5, .70)], fill=(220, 190, 120, 255))
    elif name == "shield_ok":
        d.polygon([P(.5, .06), P(.88, .20), P(.82, .62), P(.5, .94), P(.18, .62), P(.12, .20)], fill=(70, 130, 90, 255))
        d.line([P(.30, .50), P(.45, .66), P(.72, .34)], fill=(240, 250, 240, 255), width=S // 12, joint="curve")
    elif name == "question":
        d.ellipse([P(.08, .08), P(.92, .92)], fill=(60, 70, 90, 255))
        d.text(P(.5, .52), "?", font=font(SERIF, S // 2), fill=(240, 236, 226, 255), anchor="mm")
    elif name == "hospital":
        d.rectangle([P(.14, .30), P(.86, .92)], fill=(220, 216, 206, 255))
        d.rectangle([P(.42, .40), P(.58, .70)], fill=RED + (255,)); d.rectangle([P(.34, .48), P(.66, .62)], fill=RED + (255,))
        d.polygon([P(.08, .32), P(.5, .10), P(.92, .32)], fill=(150, 140, 128, 255))
    elif name == "bank":
        d.polygon([P(.06, .32), P(.5, .08), P(.94, .32)], fill=(176, 164, 144, 255))
        for k in range(4): d.rectangle([P(.16 + k * .2, .36), P(.24 + k * .2, .80)], fill=(200, 190, 170, 255))
        d.rectangle([P(.08, .82), P(.92, .92)], fill=(176, 164, 144, 255))
    im = im.resize((size, size), Image.LANCZOS); _pc[k] = im
    return im

class PIcon(Icon):
    def __init__(self, name, xy, t0, t1=None, size=120, **k):
        super().__init__(pic(name, size), xy, t0, t1, size=size, **k)

def coupon_doc(w=520, seed=3):
    """buono di risposta internazionale: ricostruzione grafica stilizzata"""
    h = int(w * 0.62)
    im = paper(w, h, (214, 226, 236), seed, 0.35); d = ImageDraw.Draw(im)
    d.rectangle([18, 18, w - 18, h - 18], outline=(70, 96, 130, 255), width=4)
    d.text((w / 2, 36), "UNIONE POSTALE UNIVERSALE", font=font(OSW, int(w * 0.05), 600), fill=(50, 76, 110, 255), anchor="ma")
    d.text((w / 2, 36 + w * 0.07), "BUONO DI RISPOSTA", font=font(SERIF, int(w * 0.075)), fill=(30, 50, 80, 255), anchor="ma")
    d.text((w / 2, 36 + w * 0.16), "INTERNAZIONALE", font=font(SERIF, int(w * 0.075)), fill=(30, 50, 80, 255), anchor="ma")
    cx, cy, r = w * 0.2, h * 0.68, w * 0.1
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(70, 96, 130, 255), width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(70, 96, 130, 255), width=2); d.ellipse([cx - r * .45, cy - r, cx + r * .45, cy + r], outline=(70, 96, 130, 255), width=2)
    d.text((w * 0.36, h * 0.60), "si cambia con francobolli", font=font(COURR, int(w * 0.04)), fill=(40, 60, 90, 255))
    d.text((w * 0.36, h * 0.70), "in un altro Paese", font=font(COURR, int(w * 0.04)), fill=(40, 60, 90, 255))
    recon_label(d, w, h, size=max(14, int(w * 0.032)))
    return im

# ---------------------------------------------------------------- mappa atlantica (Natural Earth)
WPAD = 900
WB = dict(lon0=-100.0, lon1=50.0, lat0=-38.0, lat1=62.0, K=28.0)
WPL = {"Lugo": (11.91, 44.42), "Parma": (10.33, 44.80), "Boston": (-71.06, 42.36), "Montreal": (-73.57, 45.50),
       "Atlanta": (-84.39, 33.75), "Rio": (-43.20, -22.90), "Roma": (12.50, 41.90), "Florida": (-81.66, 30.33),
       "Spagna": (-3.70, 40.42), "Lexington": (-71.23, 42.44), "Napoli": (14.27, 40.85), "Genova": (8.93, 44.41)}
def wwhere(p): return WPL[p] if isinstance(p, str) else p
_wb = None
def world_base():
    global _wb
    if _wb is not None: return _wb
    cache = os.path.join(HERE3, "world_base.png")
    if os.path.exists(cache):
        _wb = Image.open(cache).convert("RGB"); return _wb
    _wb = _world_raw()
    _wb.save(cache); return _wb
def _world_raw():
    K = WB["K"]; Wb = int((WB["lon1"] - WB["lon0"]) * K); Hb = int((WB["lat1"] - WB["lat0"]) * K)
    im = Image.new("RGB", (Wb, Hb), (22, 27, 30)); d = ImageDraw.Draw(im)
    P = lambda lo, la: ((lo - WB["lon0"]) * K, (WB["lat1"] - la) * K)
    for lo in range(-100, 51, 10): d.line([P(lo, WB["lat0"]), P(lo, WB["lat1"])], fill=(30, 36, 40), width=2)
    for la in range(-30, 61, 10): d.line([P(WB["lon0"], la), P(WB["lon1"], la)], fill=(30, 36, 40), width=2)
    feats = json.load(open(os.path.join(fi.HERE, "countries.geojson")))["features"]
    hl = {"Italy": (96, 78, 56), "United States of America": (78, 70, 60), "Canada": (64, 60, 56), "Brazil": (70, 72, 58)}
    for ft in feats:
        name = ft["properties"].get("ADMIN", ""); g = ft["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for p in polys:
            d.polygon([P(x, y) for x, y in p[0]], fill=hl.get(name, (50, 47, 44)))
    for ft in feats:
        g = ft["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for p in polys: d.line([P(x, y) for x, y in p[0]] + [P(*p[0][0])], fill=(110, 100, 88), width=2)
    pad = Image.new("RGB", (Wb + 2 * WPAD, Hb + 2 * WPAD), (22, 27, 30)); pad.paste(im, (WPAD, WPAD))
    return pad

class WorldMap(El):
    """cam: [(t, luogo, ppd)]; routes: dict(pts, t, d, color, icon=pic name, dashed); pins: dict(at, label, t, side)"""
    def __init__(self, box, cam, t0, t1=None, routes=(), pins=(), title="mappa: Natural Earth · percorsi indicativi"):
        super().__init__(t0, t1, 0.4); self.box, self.routes, self.pins, self.title = box, list(routes), list(pins), title
        self.cam = sorted([(c[0], wwhere(c[1]), c[2]) for c in cam], key=lambda c: c[0])
    def view(self, t):
        ks = self.cam
        if t <= ks[0][0]: c = ks[0]; return c[1][0], c[1][1], c[2]
        for p, q in zip(ks, ks[1:]):
            if t <= q[0]:
                u = ease_io((t - p[0]) / max(1e-6, q[0] - p[0]))
                return (p[1][0] + (q[1][0] - p[1][0]) * u, p[1][1] + (q[1][1] - p[1][1]) * u, math.exp(math.log(p[2]) + (math.log(q[2]) - math.log(p[2])) * u))
        c = ks[-1]; return c[1][0], c[1][1], c[2]
    def draw(self, lay, t, a):
        base = world_base(); K = WB["K"]; x0, y0, x1, y1 = self.box; bw, bh = x1 - x0, y1 - y0
        lon, lat, ppd = self.view(t); s = K / ppd
        cx = (lon - WB["lon0"]) * K + WPAD; cy = (WB["lat1"] - lat) * K + WPAD
        bx0, by0 = cx - bw / 2 * s, cy - bh / 2 * s
        bb = (bx0, by0, bx0 + bw * s, by0 + bh * s)
        if bb[0] >= 0 and bb[1] >= 0 and bb[2] <= base.width and bb[3] <= base.height:
            im = base.resize((int(bw), int(bh)), Image.BILINEAR, box=bb).convert("RGBA")
        else:
            im = base.crop(tuple(int(round(v)) for v in bb)).resize((int(bw), int(bh)), Image.BILINEAR).convert("RGBA")
        def S(p):
            lo, la = wwhere(p); return (((lo - WB["lon0"]) * K + WPAD - bx0) / s, ((WB["lat1"] - la) * K + WPAD - by0) / s)
        d = ImageDraw.Draw(im)
        for r in self.routes:
            if t < r["t"]: continue
            pts = [S(p) for p in r["pts"]]
            # arco
            path = []
            for p, q in zip(pts, pts[1:]):
                L = math.dist(p, q); bend = r.get("bend", 0.18)
                mx, my = (p[0] + q[0]) / 2 - (q[1] - p[1]) * bend, (p[1] + q[1]) / 2 + (q[0] - p[0]) * bend
                path += [((1 - u) ** 2 * p[0] + 2 * (1 - u) * u * mx + u * u * q[0], (1 - u) ** 2 * p[1] + 2 * (1 - u) * u * my + u * u * q[1]) for u in [i / 40 for i in range(41)]]
            f = ease_io((t - r["t"]) / r.get("d", 1.5)); k = max(2, int(len(path) * f))
            col = r.get("color", RED) + (255,)
            for i in range(0, k - 1, 2): d.line([path[i], path[i + 1]], fill=col, width=6)
            if r.get("icon") and f < 1.0 or r.get("keep"):
                px, py = path[k - 1]
                ic = pic(r["icon"], 80) if r.get("icon") in ("ship",) else icon(r.get("icon", "envelope"), 70)
                place(im, ic, (px, py - 30), "mm", 1.0)
        for p in self.pins:
            if t < p["t"]: continue
            x, y = S(p["at"]); k = ease((t - p["t"]) / 0.3); col = p.get("color", RED)
            if not (-50 < x < bw + 50 and -50 < y < bh + 50): continue
            d.ellipse([x - 13 * k, y - 13 * k, x + 13 * k, y + 13 * k], fill=col + (255,), outline=(255, 240, 230, 255), width=3)
            f = font(OSW, p.get("size", 34), 600); tw = tl(d, p["label"], f); side = p.get("side", "r")
            lx = x + 26 if side == "r" else x - 26 - tw
            ly = y - 22 if side in ("r", "l") else (y - 66 if side == "t" else y + 22)
            if side in ("t", "b"): lx = x - tw / 2
            d.rounded_rectangle([lx - 10, ly - 4, lx + tw + 10, ly + 44], 8, fill=(14, 12, 11, int(220 * k)))
            d.text((lx, ly), p["label"], font=f, fill=WHITE + (int(255 * k),))
        d.rectangle([0, 0, bw - 1, bh - 1], outline=(90, 84, 76, 255), width=3)
        if self.title:
            d.text((bw - 14, bh - 12), self.title, font=font(COURR, 18), fill=(150, 143, 134, 255), anchor="rb")
        place(lay, im, (x0, y0), "la", a)

# ---------------------------------------------------------------- l'ufficio (scenografia ricorrente)
class Office(El):
    """facciata dell'ufficio con insegna, fila di risparmiatori, mucchio di soldi.
    queue: [(t, n)] persone in fila; cash: [(t, frazione)]; run_t: la fila diventa 'restituzione'; closed_t: cartello CHIUSO"""
    def __init__(self, box, t0, t1=None, queue=(), cash=(), run_t=None, closed_t=None, sign="SECURITIES EXCHANGE CO.", s=0.42, seed=4):
        super().__init__(t0, t1, 0.4); self.box, self.queue, self.cash, self.run_t, self.closed_t, self.sign, self.s = box, sorted(queue), sorted(cash), run_t, closed_t, sign, s
        rng = random.Random(seed); self.kinds = [rng.choice(("man", "suit", "expert", "poet", "worker")) for _ in range(60)]
        self.ph = [rng.uniform(0, 6) for _ in range(60)]
    def door(self):
        x0, y0, x1, y1 = self.box; w = x1 - x0
        return (x0 + w * 0.5, y1)
    def val(self, keys, t, default=0.0):
        v = default; prev_v = default; prev_t = None
        for kt, kv in keys:
            if t >= kt: prev_v, v, prev_t = v, kv, kt
        if prev_t is None: return default
        return lerp(prev_v, v, ease((t - prev_t) / 0.8))
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); x0, y0, x1, y1 = self.box; w, h = x1 - x0, y1 - y0; al = int(255 * a)
        brick = (120, 70, 52, al)
        d.rectangle([x0, y0, x1, y1], fill=brick)
        for r in range(int(h / 28)):
            yy = y0 + r * 28; d.line([(x0, yy), (x1, yy)], fill=(100, 58, 44, al), width=2)
        # insegna
        d.rectangle([x0 + w * .06, y0 + h * .06, x1 - w * .06, y0 + h * .22], fill=(24, 28, 30, al), outline=GOLD + (al,), width=3)
        f = font(OSW, int(h * .085), 600)
        while tl(d, self.sign, f) > w * 0.82 and f.size > 12: f = font(OSW, f.size - 2, 600)
        d.text((x0 + w / 2, y0 + h * .14), self.sign, font=f, fill=GOLD + (al,), anchor="mm")
        # vetrine
        for cxr in (.2, .8):
            d.rectangle([x0 + w * (cxr - .13), y0 + h * .32, x0 + w * (cxr + .13), y0 + h * .72], fill=(200, 180, 120, al), outline=(60, 40, 30, al), width=4)
            d.line([(x0 + w * cxr, y0 + h * .32), (x0 + w * cxr, y0 + h * .72)], fill=(60, 40, 30, al), width=3)
        # porta
        d.rectangle([x0 + w * .40, y0 + h * .34, x0 + w * .60, y1], fill=(46, 32, 24, al), outline=(30, 20, 14, al), width=4)
        d.ellipse([x0 + w * .56 - 6, y0 + h * .66 - 6, x0 + w * .56 + 6, y0 + h * .66 + 6], fill=GOLD + (al,))
        # soldi in vetrina (mucchio)
        c = self.val(self.cash, t)
        if c > 0.01:
            n = int(1 + c * 14)
            for k in range(n):
                row, col = divmod(k, 5)
                bx = x0 + w * .09 + col * w * .042 + (row % 2) * w * .02; by = y0 + h * .70 - row * h * .07
                d.rectangle([bx, by - h * .05, bx + w * .05, by], fill=(150, 184, 136, al), outline=(60, 96, 60, al), width=2)
                bx2 = x0 + w * .69 + col * w * .042 + (row % 2) * w * .02
                d.rectangle([bx2, by - h * .05, bx2 + w * .05, by], fill=(150, 184, 136, al), outline=(60, 96, 60, al), width=2)
        if self.closed_t and t > self.closed_t:
            k = ease((t - self.closed_t) / 0.3); cx, cy = x0 + w * .5, y0 + h * .52
            d.rounded_rectangle([cx - w * .12, cy - h * .06, cx + w * .12, cy + h * .06], 8, fill=RED + (int(al * k),))
            d.text((cx, cy), "CHIUSO", font=font(OSW, int(h * .08), 700), fill=WHITE + (int(al * k),), anchor="mm")
        d.rectangle([x0 - 30, y1, x1 + 600, y1 + 10], fill=(70, 66, 60, al))
        # fila
        n = int(round(self.val(self.queue, t)))
        dx = 64 * self.s / 0.42
        run = self.run_t is not None and t > self.run_t
        for k in range(min(n, 60)):
            px = x1 + 50 + k * dx; py = y1
            if px > W + 60: break
            mv = False
            if run:  # in fila verso l'uscita: tutti si agitano
                py += math.sin((t - self.run_t) * 9 + self.ph[k]) * 3
            draw_person(lay, px, py, self.s, self.kinds[k], self.ph[k] + t * 3, mv, arms=("up" if run and k % 3 == 0 else "down"), alpha=al, flip=-1)
            if not run and k % 4 == 1:
                place(lay, pic("dollar", int(70 * self.s / 0.42)), (px + 20 * self.s / 0.42, py - 110 * self.s / 0.42), "mm", a)

# ---------------------------------------------------------------- piramide: i nuovi pagano i vecchi
class Pyramid(El):
    """livelli di risparmiatori; levels: [t_comparsa] (livello 0 = primi); flow_t: monete che salgono; crash_t: crollo"""
    def __init__(self, box, levels, t0, t1=None, flow=True, crash_t=None, labels=None, top_label="PONZI"):
        super().__init__(t0, t1, 0.3); self.box, self.levels, self.flow, self.crash_t, self.labels, self.top_label = box, levels, flow, crash_t, labels or {}, top_label
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); x0, y0, x1, y1 = self.box; w, h = x1 - x0, y1 - y0; al = int(255 * a)
        L = len(self.levels); rh = h / (L + 1)
        cx = x0 + w / 2
        crash = ease((t - self.crash_t) / 1.2) if self.crash_t and t > self.crash_t else 0
        # vertice
        ty = y0 + rh * 0.95
        d.rounded_rectangle([cx - 90, ty - 70, cx + 90, ty - 10], 10, fill=RED + (al,))
        d.text((cx, ty - 40), self.top_label, font=font(OSW, 34, 700), fill=WHITE + (al,), anchor="mm")
        for li, tl_ in enumerate(self.levels):
            if t < tl_: continue
            k = ease((t - tl_) / 0.4); n = 2 ** (li + 1) if li < 4 else 2 ** 4 + 8 * (li - 3)
            y = y0 + rh * (li + 2) + 20 * crash * (li + 1) * (1 + li * .3)
            span = w * min(0.96, 0.18 + 0.2 * (li + 1)); s = max(0.16, 0.40 - 0.06 * li)
            for j in range(n):
                px = cx - span / 2 + span * (j + .5) / n
                py = y + (1 - k) * 40 + crash * 140 * ((j * 37 % 11) / 11)
                draw_person(lay, px, py, s, ("man", "suit", "worker", "expert", "poet")[(j + li) % 5], j + t * 2, False, alpha=int(al * k * (1 - crash * .6)))
            if li in self.labels:
                d.text((x1 - 8, y - rh * .35), self.labels[li], font=font(OSW, 28, 600), fill=GREY + (int(al * k),), anchor="rm")
            # monete che salgono al livello sopra
            if self.flow and not crash:
                yu = (y0 + rh * (li + 1)) if li else ty - 10
                for m in range(3):
                    u = ((t - tl_) * 0.8 + m / 3) % 1.0
                    mx = cx + (m - 1) * span * 0.18 * (1 - u)
                    place(lay, pic("coin", 44), (mx, y - rh * .55 - (y - rh * .55 - yu) * u + 30), "mm", a * k * min(1, (1 - u) * 4))
        if crash > 0:
            d.line([(x0 + w * .15, y0 + h * .2), (x1 - w * .15, y1 - h * .05)], fill=RED + (int(al * crash),), width=14)
            d.line([(x1 - w * .15, y0 + h * .2), (x0 + w * .15, y1 - h * .05)], fill=RED + (int(al * crash),), width=14)

class Growth(El):
    """grafico che cresce: pts [(x, y_valore)] in un box; t0..t0+dur"""
    def __init__(self, box, vals, t0, t1=None, dur=2.5, labels=None, color=GOLD, fmt=None):
        super().__init__(t0, t1, 0.3); self.box, self.vals, self.dur, self.labels, self.color, self.fmt = box, vals, dur, labels or {}, color, fmt
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); x0, y0, x1, y1 = self.box; al = int(255 * a); n = len(self.vals); mx = max(self.vals)
        d.line([(x0, y0), (x0, y1), (x1, y1)], fill=(120, 112, 102, al), width=3)
        f = ease_io((t - self.t0) / self.dur); kk = f * (n - 1)
        bw = (x1 - x0) / n * 0.7
        for i, v in enumerate(self.vals):
            if i > kk + 0.001: break
            u = min(1.0, kk - i + 1) if i else 1.0
            bx = x0 + (x1 - x0) * (i + .15) / n; bh = (y1 - y0 - 40) * v / mx * u
            d.rectangle([bx, y1 - bh, bx + bw, y1], fill=self.color + (al,))
            if i in self.labels:
                d.text((bx + bw / 2, y1 + 12), self.labels[i], font=font(OSW, 26, 600), fill=GREY + (al,), anchor="ma")
            if self.fmt and (i == int(kk) or i == n - 1 and f >= 1):
                d.text((bx + bw / 2, y1 - bh - 10), self.fmt(v), font=font(OSW, 34, 600), fill=WHITE + (al,), anchor="mb")

class Check(El):
    """lista di controllo: voci con spunta rossa (segnali d'allarme)"""
    def __init__(self, items, xy, t0, t1=None, size=40, width=900, icon_name="warning"):
        super().__init__(t0, t1, 0.3); self.items, self.xy, self.size, self.width, self.icon = items, xy, size, width, icon_name
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); x, y = self.xy; al = int(255 * a)
        for j, (tt, txt) in enumerate(self.items):
            if t < tt: continue
            k = ease((t - tt) / 0.35); yy = y + j * self.size * 2.0; dx = 40 * (1 - k)
            d.rounded_rectangle([x + dx, yy - self.size * .9, x + dx + self.width, yy + self.size * .9], 12, fill=(30, 27, 25, int(220 * a * k)))
            place(lay, pic(self.icon, int(self.size * 1.3)), (x + dx + self.size * 0.95, yy), "mm", a * k)
            d.text((x + dx + self.size * 2, yy), txt, font=font(PS, self.size), fill=WHITE + (int(al * k),), anchor="lm")
