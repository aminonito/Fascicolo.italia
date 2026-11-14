# Elementi grafici del caso 005 (Ettore Majorana): mare notturno con piroscafo (scenografia ricorrente),
# mappa del mondo (Italia -> Sud America), foto del 1955 e cartolina del 1920 RICOSTRUITE (sagome, non originali),
# confronto dei tratti, bacheca degli indizi, icone del caso. Tutto disegnato da codice.
import math, random, os, json
from fi import *
import fi
import fx
from fx import *
from fx import draw_person

fi.PLACES.update({"Palermo": (13.36, 38.12), "Catania": (15.09, 37.50), "Lipsia": (12.37, 51.34),
                  "Copenaghen": (12.57, 55.68)})

NAVY = (24, 34, 52)
SEA = (22, 44, 62)

# ---------------------------------------------------------------- icone del caso
_mc = {}
def mpic(name, size):
    k = (name, size)
    if k in _mc: return _mc[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); w = max(2, S // 22)
    g = GOLD + (255,); wh = WHITE + (255,); ink = INK + (255,)
    if name == "ship":
        d.polygon([P(.04, .58), P(.96, .58), P(.84, .80), P(.14, .80)], fill=(30, 30, 36, 255))
        d.rectangle([P(.04, .74), P(.90, .80)], fill=RED + (255,))
        d.rectangle([P(.22, .44), P(.76, .58)], fill=(226, 220, 206, 255))
        d.rectangle([P(.32, .34), P(.62, .44)], fill=(210, 204, 190, 255))
        for k in range(6): d.ellipse([P(.26 + k * .085, .49), P(.30 + k * .085, .53)], fill=(240, 210, 120, 255))
        d.rectangle([P(.44, .16), P(.54, .34)], fill=(30, 30, 36, 255)); d.rectangle([P(.44, .16), P(.54, .21)], fill=RED + (255,))
    elif name == "atom":
        for an in (0, 60, 120):
            e = Image.new("RGBA", (S, S), (0, 0, 0, 0)); de = ImageDraw.Draw(e)
            de.ellipse([P(.08, .36), P(.92, .64)], outline=(150, 200, 236, 255), width=S // 26)
            im.alpha_composite(e.rotate(an, resample=Image.BICUBIC))
        d.ellipse([P(.42, .42), P(.58, .58)], fill=RED + (255,))
    elif name == "neutrino":
        d.ellipse([P(.30, .30), P(.70, .70)], fill=(150, 200, 236, 255))
        for k in range(3): d.arc([P(.12 - k * .04, .12 - k * .04), P(.88 + k * .04, .88 + k * .04)], 200 + k * 30, 300 + k * 30, fill=(150, 200, 236, 160), width=S // 30)
        d.line([P(.02, .50), P(.26, .50)], fill=(150, 200, 236, 200), width=S // 30)
    elif name == "passport":
        d.rounded_rectangle([P(.20, .08), P(.80, .92)], S // 18, fill=(110, 30, 34, 255))
        d.ellipse([P(.36, .30), P(.64, .58)], outline=g, width=S // 30)
        d.line([P(.36, .44), P(.64, .44)], fill=g, width=S // 40); d.line([P(.50, .30), P(.50, .58)], fill=g, width=S // 40)
        d.text(P(.50, .74), "PASSAPORTO", font=font(OSW, int(S * .07), 600), fill=g, anchor="mm")
    elif name == "folder":
        d.polygon([P(.06, .20), P(.40, .20), P(.46, .28), P(.94, .28), P(.94, .86), P(.06, .86)], fill=(196, 160, 104, 255))
        d.rectangle([P(.12, .34), P(.88, .80)], fill=(232, 222, 200, 255))
        for k in range(4): d.line([P(.18, .44 + k * .09), P(.80 - (k % 2) * .14, .44 + k * .09)], fill=(120, 110, 96, 255), width=S // 50)
        d.text(P(.50, .26), "APPUNTI", font=font(OSW, int(S * .06), 600), fill=ink, anchor="mm")
    elif name == "telegram":
        d.rectangle([P(.08, .20), P(.92, .80)], fill=(236, 226, 196, 255), outline=(120, 100, 80, 255), width=w)
        d.rectangle([P(.08, .20), P(.92, .32)], fill=(70, 90, 140, 255))
        d.text(P(.50, .26), "TELEGRAMMA", font=font(OSW, int(S * .07), 600), fill=wh, anchor="mm")
        for k in range(3): d.rectangle([P(.16, .42 + k * .11), P(.80 - k * .12, .47 + k * .11)], fill=(60, 54, 48, 255))
    elif name == "convent":
        d.rectangle([P(.12, .46), P(.88, .92)], fill=(200, 188, 166, 255))
        d.polygon([P(.06, .48), P(.50, .26), P(.94, .48)], fill=(140, 70, 50, 255))
        d.rectangle([P(.42, .06), P(.58, .46)], fill=(210, 198, 176, 255)); d.polygon([P(.38, .10), P(.50, .0), P(.62, .10)], fill=(140, 70, 50, 255))
        d.line([P(.50, .12), P(.50, .26)], fill=ink, width=S // 40); d.line([P(.45, .17), P(.55, .17)], fill=ink, width=S // 40)
        for k in range(3): d.chord([P(.20 + k * .22, .58), P(.36 + k * .22, .90)], 180, 360, fill=(70, 56, 46, 255)); d.rectangle([P(.20 + k * .22, .74), P(.36 + k * .22, .92)], fill=(70, 56, 46, 255))
    elif name == "car":
        yl = (226, 184, 60, 255)
        d.rounded_rectangle([P(.04, .46), P(.96, .72)], S // 14, fill=yl)
        d.polygon([P(.24, .46), P(.34, .26), P(.70, .26), P(.80, .46)], fill=yl)
        d.polygon([P(.30, .45), P(.37, .30), P(.50, .30), P(.50, .45)], fill=(150, 190, 210, 255)); d.polygon([P(.54, .45), P(.54, .30), P(.67, .30), P(.74, .45)], fill=(150, 190, 210, 255))
        for x in (.24, .76): d.ellipse([P(x - .11, .60), P(x + .11, .82)], fill=(26, 24, 22, 255)); d.ellipse([P(x - .05, .66), P(x + .05, .76)], fill=(170, 170, 176, 255))
        d.rectangle([P(.90, .52), P(.97, .58)], fill=(250, 240, 200, 255))
    elif name == "phone":
        d.rounded_rectangle([P(.14, .52), P(.86, .90)], S // 14, fill=(40, 36, 34, 255))
        d.ellipse([P(.36, .58), P(.64, .86)], fill=(220, 210, 190, 255)); d.ellipse([P(.46, .68), P(.54, .76)], fill=(40, 36, 34, 255))
        d.rounded_rectangle([P(.06, .26), P(.94, .42)], S // 16, fill=(40, 36, 34, 255))
        d.rectangle([P(.06, .32), P(.20, .52)], fill=(40, 36, 34, 255)); d.rectangle([P(.80, .32), P(.94, .52)], fill=(40, 36, 34, 255))
    elif name == "tv":
        d.rounded_rectangle([P(.06, .18), P(.94, .82)], S // 14, fill=(60, 52, 46, 255))
        d.rounded_rectangle([P(.12, .24), P(.74, .76)], S // 18, fill=(110, 140, 150, 255))
        d.text(P(.43, .50), "?", font=font(SERIF, int(S * .36)), fill=wh, anchor="mm")
        d.ellipse([P(.79, .30), P(.89, .40)], fill=g); d.ellipse([P(.79, .48), P(.89, .58)], fill=g)
        d.line([P(.40, .18), P(.28, .04)], fill=wh, width=w); d.line([P(.48, .18), P(.62, .04)], fill=wh, width=w)
    elif name == "hotel":
        d.rectangle([P(.16, .12), P(.84, .94)], fill=(170, 150, 126, 255))
        for r in range(4):
            for c in range(3): d.rectangle([P(.24 + c * .2, .2 + r * .15), P(.36 + c * .2, .3 + r * .15)], fill=(240, 210, 120, 255) if (r + c) % 2 else (70, 60, 52, 255))
        d.rectangle([P(.42, .80), P(.58, .94)], fill=(70, 50, 36, 255))
        d.rectangle([P(.24, .02), P(.76, .12)], fill=RED + (255,)); d.text(P(.50, .07), "ALBERGO", font=font(OSW, int(S * .07), 600), fill=wh, anchor="mm")
    elif name == "book":
        d.polygon([P(.06, .20), P(.50, .28), P(.50, .90), P(.06, .82)], fill=(232, 222, 200, 255), outline=(120, 100, 80, 255))
        d.polygon([P(.94, .20), P(.50, .28), P(.50, .90), P(.94, .82)], fill=(222, 212, 190, 255), outline=(120, 100, 80, 255))
        for k in range(5):
            d.line([P(.12, .34 + k * .1), P(.44, .40 + k * .1)], fill=(120, 110, 96, 255), width=S // 60)
            d.line([P(.56, .40 + k * .1), P(.88, .34 + k * .1)], fill=(120, 110, 96, 255), width=S // 60)
    elif name == "question":
        d.ellipse([P(.06, .06), P(.94, .94)], fill=RED + (255,))
        d.text(P(.50, .52), "?", font=font(SERIF, int(S * .66)), fill=wh, anchor="mm")
    elif name == "nophoto":
        d.rounded_rectangle([P(.08, .26), P(.92, .82)], S // 14, fill=(60, 50, 44, 255)); d.ellipse([P(.32, .36), P(.68, .72)], fill=(20, 20, 24, 255), outline=wh, width=w)
        d.line([P(.10, .10), P(.90, .90)], fill=RED + (255,), width=S // 12)
    elif name == "chalk":
        d.rectangle([P(.04, .14), P(.96, .78)], fill=(40, 70, 56, 255), outline=(140, 100, 60, 255), width=S // 30)
        d.text(P(.50, .30), "NEUTRINO", font=font(OSW, int(S * .10), 600), fill=(230, 230, 220, 255), anchor="mm"); d.text(P(.50, .45), "= ANTINEUTRINO ?", font=font(OSW, int(S * .10), 600), fill=(230, 230, 220, 255), anchor="mm")
        d.line([P(.16, .58), P(.84, .58)], fill=(230, 230, 220, 200), width=S // 70)
        d.line([P(.30, .78), P(.22, .96)], fill=(140, 100, 60, 255), width=S // 30); d.line([P(.70, .78), P(.78, .96)], fill=(140, 100, 60, 255), width=S // 30)
    elif name == "flagless_globe":
        d.ellipse([P(.06, .06), P(.94, .94)], fill=(40, 80, 120, 255))
        d.polygon([P(.30, .20), P(.48, .26), P(.44, .46), P(.30, .52), P(.22, .36)], fill=(110, 150, 90, 255))
        d.polygon([P(.56, .50), P(.74, .52), P(.70, .80), P(.58, .74)], fill=(110, 150, 90, 255))
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _mc[k] = im
    return im

_orig_icon = fx.icon
def _icon(name, size, color=None):
    if isinstance(name, str):
        m = mpic(name, size)
        if m is not None: return m
    return _orig_icon(name, size, color)
fx.icon = _icon

# ---------------------------------------------------------------- scenografia: mare notturno con piroscafo
def ship_img(w):
    k = ("shipbig", w)
    if k in _mc: return _mc[k]
    h = int(w * 0.42); S = 2
    im = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * w * S, b * h * S)
    d.polygon([P(0, .55), P(1, .55), P(.93, .95), P(.06, .95)], fill=(28, 28, 34, 255))
    d.rectangle([P(.02, .86), P(.96, .95)], fill=(150, 40, 34, 255))
    d.rectangle([P(.16, .34), P(.80, .55)], fill=(214, 208, 194, 255))
    d.rectangle([P(.28, .20), P(.66, .34)], fill=(200, 194, 180, 255))
    for k_ in range(14): d.ellipse([P(.03 + k_ * .066, .64), P(.05 + k_ * .066, .70)], fill=(250, 214, 120, 255))
    for k_ in range(9): d.rectangle([P(.20 + k_ * .065, .40), P(.24 + k_ * .065, .48)], fill=(250, 214, 120, 255))
    d.rectangle([P(.44, .02), P(.53, .20)], fill=(30, 30, 36, 255)); d.rectangle([P(.44, .02), P(.53, .07)], fill=RED + (255,))
    d.line([P(.08, .55), P(.08, .12)], fill=(60, 60, 66, 255), width=S * 3); d.line([P(.92, .55), P(.92, .16)], fill=(60, 60, 66, 255), width=S * 3)
    d.line([P(.08, .12), P(.92, .16)], fill=(60, 60, 66, 160), width=S)
    im = im.resize((w, h), Image.LANCZOS); _mc[k] = im
    return im

class Sea(El):
    """box; ship: [(t, x0..1)] posizione orizzontale della nave; flip=-1 verso sinistra;
    deck: (t_on, t_off) omino sul ponte; dawn: t in cui il cielo schiarisce; port: True = banchina a sinistra"""
    def __init__(self, box, t0, t1=None, ship=((0, .5),), flip=1, deck=None, dawn=None, port=None, ghost=None, sw=0.42, label=None):
        super().__init__(t0, t1, 0.4); self.box, self.ship, self.flip, self.deck, self.dawn, self.port, self.ghost, self.sw, self.label = box, sorted(ship), flip, deck, dawn, port, ghost, sw, label
        x0, y0, x1, y1 = box; bw, bh = int(x1 - x0), int(y1 - y0)
        rng = random.Random(5); self.stars = [(rng.uniform(0, bw), rng.uniform(0, bh * 0.5), rng.uniform(1, 3)) for _ in range(70)]
        self.sim = ship_img(int(bw * sw))
        if flip < 0: self.sim = self.sim.transpose(Image.FLIP_LEFT_RIGHT)
    def sx(self, t):
        ks = self.ship
        if t <= ks[0][0]: return ks[0][1]
        for p, q in zip(ks, ks[1:]):
            if t <= q[0]: return lerp(p[1], q[1], ease_io((t - p[0]) / max(1e-6, q[0] - p[0])))
        return ks[-1][1]
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0); al = int(255 * a)
        im = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        dw = ease((t - self.dawn) / 2.0) if self.dawn is not None and t > self.dawn else 0
        hor = int(bh * 0.58)
        for yy in range(0, hor, 6):
            u = yy / hor
            c0 = (int(lerp(10, 70, dw) + 20 * u), int(lerp(14, 90, dw) + 24 * u), int(lerp(30, 130, dw) + 30 * u))
            if dw: c0 = (int(c0[0] + 120 * dw * u * u), int(c0[1] + 60 * dw * u * u), c0[2])
            d.rectangle([0, yy, bw, yy + 6], fill=c0 + (255,))
        for sx_, sy_, r in self.stars:
            sa = int(220 * (1 - dw) * (0.6 + 0.4 * math.sin(t * 2 + sx_)))
            d.ellipse([sx_ - r / 2, sy_ - r / 2, sx_ + r / 2, sy_ + r / 2], fill=(240, 236, 220, max(0, sa)))
        mx, my = bw * 0.82, bh * 0.16; mr = bh * 0.06
        if dw < 1: d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(236, 230, 200, int(255 * (1 - dw))))
        if dw > 0:
            sy = hor - bh * 0.08 * dw; sr = bh * 0.07
            d.ellipse([bw * .2 - sr, sy - sr, bw * .2 + sr, sy + sr], fill=(250, 190, 110, int(255 * dw)))
        for yy in range(hor, bh, 6):
            u = (yy - hor) / max(1, bh - hor)
            d.rectangle([0, yy, bw, yy + 6], fill=(int(18 + 10 * dw + 6 * u), int(36 + 20 * dw + 10 * u), int(54 + 30 * dw + 6 * u), 255))
        if self.port:
            d.polygon([(0, hor - bh * .18), (bw * .10, hor - bh * .22), (bw * .16, hor - bh * .10), (bw * .26, hor - bh * .06), (bw * .26, hor + 4), (0, hor + 4)], fill=(36, 36, 44, 255))
            for k in range(8): d.rectangle([bw * .02 + k * bw * .028, hor - bh * (.10 + .04 * (k % 3)), bw * .02 + k * bw * .028 + 6, hor - bh * (.10 + .04 * (k % 3)) + 6], fill=(250, 214, 120, 255))
            d.rectangle([0, hor, bw * .26, hor + bh * .05], fill=(70, 66, 60, 255))
            d.text((bw * .13, hor - bh * .26), self.port, font=font(OSW, int(bh * .05), 600), fill=WHITE + (220,), anchor="ms")
        sx = self.sx(t) * bw; bob = math.sin(t * 1.6) * bh * 0.008
        sy = hor + bh * 0.06 - self.sim.height + bob
        ga = 1.0
        if self.ghost is not None and t > self.ghost: ga = max(0.25, 1 - ease((t - self.ghost) / 1.0) * 0.75)
        place(im, self.sim, (sx - self.sim.width / 2, sy), "la", ga)
        if self.deck and self.deck[0] <= t:
            on = ease((t - self.deck[0]) / 0.4)
            if self.deck[1] is not None and t > self.deck[1]: on *= max(0, 1 - (t - self.deck[1]) / 0.8)
            if on > 0.02: draw_person(im, sx + self.sim.width * 0.12 * self.flip, sy + self.sim.height * 0.36, 0.30, "suit", alpha=int(255 * on))
        for k in range(14):
            yy = hor + 14 + k * (bh - hor) / 14
            pts = [(xx, yy + math.sin(xx / 60 + t * 1.4 + k) * 4) for xx in range(0, bw + 20, 20)]
            d.line(pts, fill=(80, 110, 130, 90 + 4 * k), width=2)
        if self.label: d.text((24, bh - 24), self.label, font=font(COURR, 22), fill=(180, 190, 200, 220), anchor="ls")
        m = Image.new("L", (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, bw - 1, bh - 1], 18, fill=al)
        im.putalpha(ImageChops.multiply(im.getchannel("A"), m))
        lay.alpha_composite(im, (int(x0), int(y0)))

# ---------------------------------------------------------------- mappa del mondo (Natural Earth)
_wm = {}
def world_base(box, lon0, lon1, lat0, lat1, hl=()):
    key = (box, lon0, lon1, lat0, lat1, tuple(hl))
    if key in _wm: return _wm[key]
    x0, y0, x1, y1 = box; bw, bh = int(x1 - x0), int(y1 - y0)
    im = Image.new("RGBA", (bw, bh), (22, 27, 30, 255)); d = ImageDraw.Draw(im)
    def P(lo, la): return ((lo - lon0) / (lon1 - lon0) * bw, (lat1 - la) / (lat1 - lat0) * bh)
    for lo in range(-180, 181, 10): d.line([P(lo, lat0), P(lo, lat1)], fill=(30, 36, 40, 255), width=1)
    for la in range(-80, 81, 10): d.line([P(lon0, la), P(lon1, la)], fill=(30, 36, 40, 255), width=1)
    feats = fi._geo()["features"]
    for ft in feats:
        name = ft["properties"].get("ADMIN", ""); gm = ft["geometry"]
        polys = gm["coordinates"] if gm["type"] == "MultiPolygon" else [gm["coordinates"]]
        col = (110, 84, 56) if name in hl else (52, 48, 44)
        for p in polys:
            ring = p[0]
            if not any(lon0 - 10 < x < lon1 + 10 and lat0 - 10 < y < lat1 + 10 for x, y in ring[::3] + [ring[0]]): continue
            d.polygon([P(x, y) for x, y in ring], fill=col + (255,), outline=(110, 98, 84, 255))
    _wm[key] = (im, P)
    return _wm[key]

class WorldMap(El):
    """routes: dict(a=(lon,lat), b=(lon,lat), t, d, bend, icon); pins: dict(at, label, t, side, color)"""
    def __init__(self, box, t0, t1=None, view=(-95, 35, -45, 62), hl=("Italy", "Venezuela"), routes=(), pins=(), title="mappa: Natural Earth · schema non in scala"):
        super().__init__(t0, t1, 0.4); self.box, self.view, self.hl, self.routes, self.pins, self.title = box, view, hl, list(routes), list(pins), title
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0); al = int(255 * a)
        base, P = world_base(self.box, *self.view, hl=self.hl)
        im = base.copy(); d = ImageDraw.Draw(im)
        for r in self.routes:
            if t < r["t"]: continue
            p, q = P(*r["a"]), P(*r["b"]); bend = r.get("bend", 0.25)
            mx, my = (p[0] + q[0]) / 2 - (q[1] - p[1]) * bend, (p[1] + q[1]) / 2 + (q[0] - p[0]) * bend
            f = ease_io((t - r["t"]) / r.get("d", 1.6)); n = 60; k = max(2, int(n * f))
            pts = [((1 - u) ** 2 * p[0] + 2 * (1 - u) * u * mx + u * u * q[0], (1 - u) ** 2 * p[1] + 2 * (1 - u) * u * my + u * u * q[1]) for u in [i / n for i in range(k + 1)]]
            for i in range(0, len(pts) - 1, 2): d.line([pts[i], pts[i + 1]], fill=r.get("color", RED) + (255,), width=6)
            ex, ey = pts[-1]
            ic = r.get("icon")
            if ic: place(im, fx.icon(ic, 80), (ex, ey), "mm", 1.0)
            else: d.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], fill=RED + (255,))
        for pn in self.pins:
            if t < pn["t"]: continue
            x, y = P(*pn["at"]); pa = int(255 * ease((t - pn["t"]) / 0.3)); s = back((t - pn["t"]) / 0.3); col = pn.get("color", GOLD)
            r = 12 * s
            d.ellipse([x - r - 6, y - r - 6, x + r + 6, y + r + 6], outline=col + (pa,), width=3); d.ellipse([x - r * .6, y - r * .6, x + r * .6, y + r * .6], fill=col + (pa,))
            f = font(OSW, pn.get("size", 38), 600); lab = pn["label"]; tw = tl(d, lab, f); side = pn.get("side", "r")
            if side == "r": bx, by = x + 30, y - f.size / 2
            elif side == "l": bx, by = x - 30 - tw, y - f.size / 2
            elif side == "t": bx, by = x - tw / 2, y - 34 - f.size
            else: bx, by = x - tw / 2, y + 30
            d.rounded_rectangle([bx - 12, by - 6, bx + tw + 12, by + f.size + 6], 8, fill=(14, 12, 11, int(pa * 0.8)))
            d.text((bx, by), lab, font=f, fill=WHITE + (pa,), anchor="la")
        if self.title: d.text((20, bh - 16), self.title, font=font(COURR, 20), fill=(180, 170, 155, 230), anchor="ls")
        m = Image.new("L", (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, bw - 1, bh - 1], 18, fill=al)
        im.putalpha(m); lay.alpha_composite(im, (int(x0), int(y0)))

# ---------------------------------------------------------------- documenti ricostruiti
def photo1955(w):
    """foto ricostruita: due sagome sui gradini (NON la foto originale)"""
    h = int(w * 1.12)
    im = paper(w, h, (236, 228, 210), 21, 0.5); d = ImageDraw.Draw(im)
    b = int(w * 0.06); ph = int(h * 0.72)
    d.rectangle([b, b, w - b, b + ph], fill=(150, 128, 98, 255))
    for k in range(4): d.rectangle([b, b + ph - (k + 1) * ph * 0.08, w - b, b + ph - k * ph * 0.08], fill=(120 + k * 10, 102 + k * 8, 78 + k * 6, 255))
    d.rectangle([b + w * .05, b + ph * .06, b + w * .34, b + ph * .5], fill=(110, 92, 70, 255))
    silhouette(d, w * 0.36, b + ph - ph * 0.12, w * 0.40, (60, 48, 36))
    silhouette(d, w * 0.66, b + ph - ph * 0.12, w * 0.38, (74, 60, 44))
    d.text((w / 2, b + ph + h * 0.07), "Valencia, 12-6-1955", font=font(TYPE, int(w * 0.075)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, b + ph + h * 0.15), "sagome · foto originale non mostrata", font=font(COURR, int(w * 0.04)), fill=(110, 100, 88, 255), anchor="mm")
    recon_label(d, w, h, size=max(14, int(w * 0.035)))
    return im

def postcard(w):
    h = int(w * 0.64)
    im = paper(w, h, (230, 220, 196), 31, 0.6); d = ImageDraw.Draw(im)
    d.line([(w * .55, h * .1), (w * .55, h * .85)], fill=(120, 100, 80, 255), width=2)
    d.rectangle([w * .80, h * .08, w * .93, h * .30], fill=(160, 60, 50, 255), outline=(120, 40, 30, 255), width=3)
    d.text((w * .865, h * .19), "1920", font=font(OSW, int(w * .032), 600), fill=WHITE + (255,), anchor="mm")
    for k in range(3): d.line([(w * .60, h * (.46 + k * .12)), (w * .94, h * (.46 + k * .12))], fill=(120, 110, 96, 255), width=2)
    d.text((w * .61, h * .44), "W. G. Conklin", font=font(TYPE, int(w * .045)), fill=INK + (255,), anchor="ls")
    d.text((w * .61, h * .56), "U.S.A.", font=font(TYPE, int(w * .045)), fill=INK + (255,), anchor="ls")
    for k in range(6): d.line([(w * .06, h * (.18 + k * .1)), (w * (.50 - (k % 3) * .06), h * (.18 + k * .1))], fill=(90, 84, 120, 255), width=3)
    d.text((w * .08, h * .80), "Q. Majorana", font=font(TYPE, int(w * .05)), fill=(60, 60, 120, 255), anchor="ls")
    recon_label(d, w, h, size=max(14, int(w * 0.03)))
    return im

def letter(w, h, date, salut, quote, seed=41, sign="E. Majorana"):
    im = paper(w, h, (236, 230, 214), seed, 0.4); d = ImageDraw.Draw(im)
    d.text((w - 50, 50), date, font=font(TYPE, 30), fill=INK + (255,), anchor="ra")
    d.text((50, 120), salut, font=font(TYPE, 36), fill=INK + (255,))
    q = rich_img(quote, TYPE, 38, INK, RED, lh=1.3); im.alpha_composite(q, (60, 190))
    y = 200 + q.height + 30; rng = random.Random(seed)
    while y < h - 130:
        d.line([(60, y), (60 + (w - 120) * rng.uniform(.6, 1), y)], fill=(150, 140, 126, 255), width=6); y += 34
    d.text((w - 60, h - 80), sign, font=font(TYPE, 32), fill=INK + (255,), anchor="rs")
    recon_label(d, w, h)
    return im

def telegram_img(w, h, lines):
    im = paper(w, h, (236, 226, 196), 52, 0.3); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, 80], fill=(70, 90, 140, 255))
    d.text((w / 2, 40), "TELEGRAMMA · PALERMO", font=font(OSW, 40, 600), fill=WHITE + (255,), anchor="mm")
    d.text((40, 110), "26 MARZO 1938 · DESTINATARIO: PROF. CARRELLI · NAPOLI", font=font(COURR, 22), fill=INK + (255,))
    y = 170
    for l in lines:
        d.rectangle([40, y - 6, w - 40, y + 50], fill=(248, 244, 230, 255))
        d.text((56, y + 22), l, font=font(COUR, 40), fill=INK + (255,), anchor="lm"); y += 72
    recon_label(d, w, h)
    return im

def book_cover(w):
    h = int(w * 1.45)
    im = paper(w, h, (226, 214, 186), 61, 0.5); d = ImageDraw.Draw(im)
    d.rectangle([w * .08, h * .06, w * .92, h * .94], outline=INK + (255,), width=3)
    d.text((w / 2, h * .18), "Leonardo Sciascia", font=font(TYPE, int(w * .08)), fill=INK + (255,), anchor="mm")
    t = rich_img("La scomparsa\ndi *Majorana*", SERIF, int(w * .12), INK, RED, align="m", lh=1.05)
    im.alpha_composite(t, (int((w - t.width) / 2), int(h * .34)))
    d.text((w / 2, h * .84), "1975", font=font(OSW, int(w * .08), 600), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .90), "schema, non l'originale", font=font(COURR, int(w * .045)), fill=(110, 100, 88, 255), anchor="mm")
    return im

def cover_folder(w=520):
    c = paper(w, int(w * 1.23), (196, 160, 104), 9, 0.7); d = ImageDraw.Draw(c); s = w / 520
    d.rectangle([50 * s, 110 * s, 470 * s, 330 * s], fill=(232, 222, 200, 255), outline=INK + (255,), width=3)
    d.text((260 * s, 145 * s), "FASCICOLO N. 005", font=font(COUR, int(32 * s)), fill=INK + (255,), anchor="ma")
    d.text((260 * s, 200 * s), "IL CASO", font=font(TYPE, int(40 * s)), fill=INK + (255,), anchor="ma")
    d.text((260 * s, 252 * s), "MAJORANA", font=font(TYPE, int(52 * s)), fill=RED + (255,), anchor="ma")
    d.text((260 * s, 380 * s), "Napoli · 1938 - 2015", font=font(COURR, int(26 * s)), fill=INK + (255,), anchor="ma")
    return c

# ---------------------------------------------------------------- confronto dei tratti (schema)
def head_profile(w, col):
    h = int(w * 1.25); im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    silhouette(d, w / 2, h - 4, w * 0.95, col)
    return im

class FaceCompare(El):
    """due sagome affiancate + linee dei tratti che si allineano. feats: [(t, label)]"""
    def __init__(self, box, t0, t1=None, feats=(), overlay=None, left="FOTO 1955 · BINI", right="PADRE · 50 ANNI"):
        super().__init__(t0, t1, 0.35); self.box, self.feats, self.overlay, self.left, self.right = box, list(feats), overlay, left, right
        x0, y0, x1, y1 = box; self.hw = int((y1 - y0) * 0.62)
        self.hl = head_profile(self.hw, (150, 128, 98)); self.hr = head_profile(self.hw, (120, 130, 150))
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; d = ImageDraw.Draw(lay); al = int(255 * a)
        d.rounded_rectangle([x0, y0, x1, y1], 16, fill=(26, 30, 34, int(al * .92)), outline=(60, 66, 72, al), width=2)
        cxl, cxr = x0 + (x1 - x0) * .27, x0 + (x1 - x0) * .73; cy = y0 + 40 + self.hr.height / 2
        o = ease((t - self.overlay) / 1.2) if self.overlay is not None and t > self.overlay else 0
        place(lay, self.hl, (lerp(cxl, (cxl + cxr) / 2, o), cy), "mm", a)
        place(lay, self.hr, (lerp(cxr, (cxl + cxr) / 2, o), cy), "mm", a * (1 - 0.45 * o))
        f = font(OSW, 30, 600)
        if o < 0.5:
            d.text((cxl, y1 - 24), self.left, font=f, fill=GOLD + (int(al * (1 - 2 * o)),), anchor="ms")
            d.text((cxr, y1 - 24), self.right, font=f, fill=GOLD + (int(al * (1 - 2 * o)),), anchor="ms")
        top = cy - self.hr.height / 2
        ys = [0.10, 0.22, 0.34, 0.46, 0.58]
        for j, (tt, lab) in enumerate(self.feats):
            if t < tt: continue
            u = ease((t - tt) / 0.5); yy = top + self.hr.height * ys[j % len(ys)] + (j == 4) * 10
            xa, xb = x0 + 30, x0 + 30 + (x1 - x0 - 60) * u
            for xx in range(int(xa), int(xb), 22): d.line([(xx, yy), (min(xb, xx + 12), yy)], fill=RED + (al,), width=4)
            d.text((x1 - 34, yy - 10), lab, font=font(OSW, 28, 600), fill=WHITE + (int(al * u),), anchor="rs")
        d.text((x0 + 20, y0 + 28), "SCHEMA · SAGOME, NON FOTO REALI", font=font(COURR, 20), fill=(150, 160, 170, al), anchor="ls")

# ---------------------------------------------------------------- bacheca degli indizi
def clue_card(icon_name, label, w=260):
    k = ("clue", icon_name, label, w)
    if k in _mc: return _mc[k]
    h = int(w * 1.1); im = paper(w, h, (232, 224, 204), hash(label) % 40, 0.4); d = ImageDraw.Draw(im)
    ic = fx.icon(icon_name, int(w * 0.62)); im.alpha_composite(ic, (int((w - ic.width) / 2), int(h * 0.08)))
    f = font(OSW, int(w * 0.11), 600); ls = label.split("\n")
    for q, l in enumerate(ls):
        while tl(d, l, f) > w - 20 and f.size > 14: f = font(OSW, f.size - 2, 600)
        d.text((w / 2, h * 0.76 + q * f.size * 1.1), l, font=f, fill=INK + (255,), anchor="mm")
    _mc[k] = im
    return im

class Clues(El):
    """bacheca di sughero: cards [(xy, icon, label, t, rot)], links [(i, j, t)], marks [(i, testo, t)]"""
    def __init__(self, box, cards, t0, t1=None, links=(), cw=250):
        super().__init__(t0, t1, 0.35); self.box, self.cards, self.links, self.cw = box, cards, list(links), cw
        self.ims = [clue_card(c[1], c[2], cw).rotate(c[4] if len(c) > 4 else 0, expand=True, resample=Image.BICUBIC) for c in cards]
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; d = ImageDraw.Draw(lay); al = int(255 * a)
        d.rounded_rectangle([x0, y0, x1, y1], 14, fill=(120, 88, 58, int(al * .95)), outline=(80, 56, 36, al), width=10)
        rng = random.Random(2)
        for _ in range(140):
            px, py = rng.uniform(x0 + 14, x1 - 14), rng.uniform(y0 + 14, y1 - 14)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(96, 68, 44, al))
        for i, j, tt in self.links:
            if t < tt: continue
            p = self.cards[i][0]; q = self.cards[j][0]; p = (p[0], p[1] - self.cw * .5); q = (q[0], q[1] - self.cw * .5)
            f = ease((t - tt) / 0.6)
            d.line([p, (lerp(p[0], q[0], f), lerp(p[1], q[1], f))], fill=(200, 40, 34, al), width=5)
        for c, im in zip(self.cards, self.ims):
            if t < c[3]: continue
            k = t - c[3]; ca = a * ease(k / 0.3); dy = -40 * (1 - ease(k / 0.35))
            place(lay, im, (c[0][0], c[0][1] + dy), "mm", ca)
            px, py = c[0][0], c[0][1] + dy - self.cw * .5
            d = ImageDraw.Draw(lay)
            d.ellipse([px - 12, py - 12, px + 12, py + 12], fill=(200, 40, 34, int(255 * ca)), outline=(255, 160, 150, int(255 * ca)), width=2)
