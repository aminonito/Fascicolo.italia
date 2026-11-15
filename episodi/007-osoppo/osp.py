# Elementi grafici del caso 007 (rapina di via Osoppo, Milano 1958): incrocio via Osoppo / via Caccialepori
# visto dall'alto (scenografia ricorrente, schema non in scala) con i mezzi che si muovono, letto dell'Olona,
# icone del caso. Tutto disegnato da codice: nessuna foto reale, nessun logo.
import math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "006-tortora")); sys.path.insert(0, os.path.join(HERE, "..", "005-majorana"))
from fi import *
import fi
import fx
from fx import *
import tor                       # icone già pronte (scales, prison, mic...) + maj (car, phone, question, passport, folder...)
from maj import clue_card, Clues, WorldMap

fi.PLACES.update({"Modena": (10.93, 44.65), "Cervinia": (7.63, 45.93)})
BLUE = (60, 96, 150)
VAN = (70, 84, 96)

_oc = {}
def opic(name, size):
    k = (name, size)
    if k in _oc: return _oc[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); w = max(2, S // 22)
    g = GOLD + (255,); wh = WHITE + (255,); ink = INK + (255,); dk = (34, 32, 30, 255)
    def wheel(x, y, r=.07):
        d.ellipse([P(x - r, y - r), P(x + r, y + r)], fill=dk); d.ellipse([P(x - r * .45, y - r * .45), P(x + r * .45, y + r * .45)], fill=(150, 150, 156, 255))
    if name == "van":       # furgone portavalori (vista laterale, generico)
        d.rounded_rectangle([P(.06, .30), P(.72, .74)], S // 30, fill=VAN + (255,))
        d.polygon([P(.72, .40), P(.86, .40), P(.95, .58), P(.95, .74), P(.72, .74)], fill=(84, 98, 110, 255))
        d.polygon([P(.75, .44), P(.85, .44), P(.91, .57), P(.75, .57)], fill=(150, 190, 210, 255))
        d.rectangle([P(.12, .40), P(.30, .50)], fill=(40, 46, 52, 255))
        for x in (.14, .20, .26): d.line([P(x, .40), P(x, .50)], fill=(150, 150, 156, 255), width=S // 120)
        d.text(P(.40, .58), "VALORI", font=font(OSW, int(S * .09), 700), fill=GOLD + (255,), anchor="mm")
        wheel(.22, .76, .085); wheel(.80, .76, .085)
    elif name == "truck":   # camioncino generico
        d.rectangle([P(.04, .34), P(.62, .70)], fill=(120, 110, 90, 255))
        for k in range(4): d.line([P(.08 + k * .14, .36), P(.08 + k * .14, .68)], fill=(96, 88, 72, 255), width=S // 90)
        d.polygon([P(.64, .30), P(.84, .30), P(.96, .52), P(.96, .74), P(.64, .74)], fill=(170, 60, 50, 255))
        d.polygon([P(.68, .35), P(.82, .35), P(.90, .52), P(.68, .52)], fill=(150, 190, 210, 255))
        wheel(.20, .76, .08); wheel(.80, .76, .08)
    elif name == "fiat":    # berlina anni 50 generica
        d.rounded_rectangle([P(.04, .48), P(.96, .72)], S // 14, fill=(200, 180, 140, 255))
        d.chord([P(.22, .24), P(.78, .74)], 180, 360, fill=(200, 180, 140, 255))
        d.chord([P(.28, .30), P(.72, .70)], 180, 360, fill=(150, 190, 210, 255))
        d.line([P(.50, .30), P(.50, .50)], fill=(200, 180, 140, 255), width=S // 40)
        wheel(.24, .74, .09); wheel(.76, .74, .09)
    elif name == "sportcar":
        d.rounded_rectangle([P(.04, .52), P(.96, .72)], S // 16, fill=(160, 40, 40, 255))
        d.chord([P(.26, .32), P(.70, .76)], 180, 360, fill=(160, 40, 40, 255))
        d.chord([P(.31, .37), P(.65, .72)], 180, 360, fill=(150, 190, 210, 255))
        wheel(.24, .74, .085); wheel(.76, .74, .085)
    elif name == "overalls":  # tuta da operaio blu
        b = BLUE + (255,); bd = (40, 66, 110, 255)
        d.polygon([P(.30, .10), P(.70, .10), P(.80, .26), P(.92, .52), P(.80, .56), P(.70, .36), P(.70, .94), P(.53, .94), P(.50, .60), P(.47, .94), P(.30, .94), P(.30, .36), P(.20, .56), P(.08, .52), P(.20, .26)], fill=b)
        d.polygon([P(.42, .10), P(.50, .22), P(.58, .10)], fill=bd)
        d.line([P(.50, .22), P(.50, .58)], fill=bd, width=S // 60)
        d.rectangle([P(.34, .30), P(.45, .40)], outline=bd, width=S // 70)
        d.line([P(.30, .48), P(.70, .48)], fill=bd, width=S // 40)
    elif name == "balaclava":
        c = (40, 40, 44, 255)
        d.ellipse([P(.22, .08), P(.78, .80)], fill=c); d.rectangle([P(.30, .60), P(.70, .94)], fill=c)
        d.rounded_rectangle([P(.30, .34), P(.70, .48)], S // 30, fill=(214, 176, 140, 255))
        d.ellipse([P(.37, .37), P(.45, .45)], fill=wh); d.ellipse([P(.55, .37), P(.63, .45)], fill=wh)
        d.ellipse([P(.395, .395), P(.425, .425)], fill=ink); d.ellipse([P(.575, .395), P(.605, .425)], fill=ink)
    elif name == "moneybag":
        c = (190, 160, 110, 255)
        d.ellipse([P(.14, .30), P(.86, .96)], fill=c); d.polygon([P(.34, .34), P(.40, .14), P(.60, .14), P(.66, .34)], fill=c)
        d.line([P(.34, .26), P(.66, .26)], fill=(120, 90, 50, 255), width=S // 30)
        d.text(P(.50, .64), "L.", font=font(SERIF, int(S * .26)), fill=(110, 80, 40, 255), anchor="mm")
    elif name == "cheque":
        d.rectangle([P(.06, .26), P(.94, .74)], fill=(214, 228, 214, 255), outline=(110, 140, 110, 255), width=S // 70)
        d.text(P(.12, .32), "ASSEGNO", font=font(OSW, int(S * .08), 600), fill=(60, 90, 60, 255), anchor="la")
        for k in range(3): d.line([P(.12, .50 + k * .07), P(.70, .50 + k * .07)], fill=(140, 160, 140, 255), width=S // 90)
        d.text(P(.88, .64), "L.", font=font(SERIF, int(S * .12)), fill=(60, 90, 60, 255), anchor="rm")
    elif name == "river":
        d.rectangle([P(.04, .30), P(.96, .70)], fill=(120, 100, 76, 255))
        for k in range(3):
            y = .40 + k * .10; pts = [P(.06 + i * .04, y + .025 * math.sin(i * 1.3)) for i in range(23)]
            d.line(pts, fill=(80, 130, 170, 255), width=S // 50)
    elif name == "tag":     # etichetta
        d.polygon([P(.20, .22), P(.80, .22), P(.80, .78), P(.20, .78)], fill=(236, 230, 214, 255))
        d.rectangle([P(.20, .22), P(.80, .78)], outline=(150, 140, 120, 255), width=S // 60)
        d.text(P(.50, .38), "CONFEZIONI", font=font(OSW, int(S * .08), 600), fill=ink, anchor="mm")
        d.text(P(.50, .54), "MODENA", font=font(OSW, int(S * .12), 700), fill=RED + (255,), anchor="mm")
        d.text(P(.50, .68), "tg. 48", font=font(COURR, int(S * .07)), fill=ink, anchor="mm")
    elif name == "clapper":
        d.rectangle([P(.12, .40), P(.88, .88)], fill=dk)
        d.polygon([P(.10, .26), P(.86, .14), P(.88, .30), P(.12, .40)], fill=dk)
        for k in range(5): d.polygon([P(.14 + k * .15, .37), P(.22 + k * .15, .24), P(.29 + k * .15, .23), P(.21 + k * .15, .36)], fill=wh)
        for k in range(3): d.line([P(.18, .54 + k * .11), P(.82, .54 + k * .11)], fill=(120, 120, 120, 255), width=S // 80)
    elif name == "shop":    # salumeria
        d.rectangle([P(.10, .30), P(.90, .92)], fill=(180, 170, 150, 255))
        for k in range(6): d.polygon([P(.08 + k * .14, .22), P(.22 + k * .14, .22), P(.20 + k * .14, .36), P(.10 + k * .14, .36)], fill=(RED if k % 2 == 0 else WHITE) + (255,))
        d.rectangle([P(.18, .46), P(.58, .80)], fill=(150, 190, 210, 255)); d.rectangle([P(.64, .46), P(.82, .92)], fill=(90, 70, 50, 255))
        d.ellipse([P(.24, .60), P(.40, .74)], fill=(220, 190, 120, 255)); d.rounded_rectangle([P(.40, .56), P(.54, .76)], S // 30, fill=(170, 80, 70, 255))
        d.text(P(.50, .14), "SALUMERIA", font=font(OSW, int(S * .09), 700), fill=wh, anchor="mm")
    elif name == "hammer":
        d.line([P(.30, .86), P(.60, .40)], fill=(150, 110, 70, 255), width=S // 14)
        d.polygon([P(.44, .22), P(.82, .44), P(.74, .58), P(.36, .36)], fill=(140, 140, 146, 255))
    elif name == "payenv":  # busta paga
        d.rectangle([P(.10, .24), P(.90, .80)], fill=(222, 206, 170, 255), outline=(150, 130, 100, 255), width=S // 70)
        d.polygon([P(.10, .24), P(.50, .52), P(.90, .24)], outline=(150, 130, 100, 255), fill=(210, 192, 154, 255))
        d.text(P(.50, .68), "PAGA", font=font(OSW, int(S * .10), 700), fill=ink, anchor="mm")
    elif name == "factory":
        d.polygon([P(.06, .90), P(.06, .50), P(.28, .36), P(.28, .50), P(.50, .36), P(.50, .50), P(.72, .36), P(.72, .90)], fill=(130, 120, 110, 255))
        d.rectangle([P(.76, .14), P(.88, .90)], fill=(110, 100, 92, 255))
        for k in range(3): d.ellipse([P(.78 + k * .03, .02 - k * .0), P(.92 + k * .03, .12)], fill=(180, 180, 180, 160))
        for k in range(3): d.rectangle([P(.12 + k * .20, .62), P(.22 + k * .20, .74)], fill=(240, 200, 90, 255))
    elif name == "suitcase":
        d.rounded_rectangle([P(.12, .30), P(.88, .86)], S // 20, fill=(130, 90, 56, 255))
        d.rounded_rectangle([P(.38, .18), P(.62, .32)], S // 30, outline=(90, 60, 36, 255), width=S // 30)
        d.line([P(.12, .50), P(.88, .50)], fill=(90, 60, 36, 255), width=S // 50)
    elif name == "identikit":
        d.rectangle([P(.14, .08), P(.86, .92)], fill=(236, 230, 214, 255))
        d.ellipse([P(.32, .20), P(.68, .62)], outline=ink, width=S // 60)
        d.line([P(.40, .36), P(.46, .36)], fill=ink, width=S // 50); d.line([P(.54, .36), P(.60, .36)], fill=ink, width=S // 50)
        d.line([P(.50, .40), P(.48, .48)], fill=ink, width=S // 70); d.line([P(.44, .53), P(.56, .53)], fill=ink, width=S // 70)
        d.arc([P(.24, .58), P(.76, 1.0)], 200, 340, fill=ink, width=S // 60)
        d.text(P(.50, .84), "IDENTIKIT", font=font(OSW, int(S * .08), 700), fill=RED + (255,), anchor="mm")
    elif name == "mountain":
        d.polygon([P(.04, .86), P(.40, .20), P(.62, .56), P(.74, .40), P(.96, .86)], fill=(110, 120, 130, 255))
        d.polygon([P(.32, .35), P(.40, .20), P(.48, .35), P(.42, .32)], fill=wh)
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _oc[k] = im
    return im

_prev_icon = fx.icon
def _icon(name, size, color=None):
    if isinstance(name, str):
        m = opic(name, size)
        if m is not None: return m
    return _prev_icon(name, size, color)
fx.icon = _icon

# ---------------------------------------------------------------- veicoli visti dall'alto
def topcar(kind, L):
    """sagoma vista dall'alto, muso verso destra"""
    col = {"van": VAN, "truck": (170, 60, 50), "fiat": (200, 180, 140), "getaway": (160, 40, 40), "car": (90, 100, 120)}[kind]
    W_ = int(L * (0.46 if kind in ("van", "truck") else 0.44)); im = Image.new("RGBA", (L, W_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([2, 2, L - 3, W_ - 3], W_ // 5, fill=col + (255,), outline=(20, 18, 16, 255), width=3)
    if kind == "van":
        d.rectangle([L * .08, W_ * .2, L * .66, W_ * .8], fill=(84, 98, 112, 255))
        d.text((L * .37, W_ * .5), "VALORI", font=font(OSW, int(W_ * .34), 700), fill=GOLD + (255,), anchor="mm")
        d.rectangle([L * .74, W_ * .14, L * .86, W_ * .86], fill=(150, 190, 210, 255))
    elif kind == "truck":
        d.rectangle([L * .04, W_ * .1, L * .64, W_ * .9], fill=(120, 110, 90, 255))
        d.rectangle([L * .76, W_ * .14, L * .88, W_ * .86], fill=(150, 190, 210, 255))
    else:
        d.rectangle([L * .26, W_ * .16, L * .40, W_ * .84], fill=(150, 190, 210, 255))
        d.rectangle([L * .62, W_ * .16, L * .74, W_ * .84], fill=(150, 190, 210, 255))
    return im

class Crossing(El):
    """incrocio via Osoppo (orizzontale) / via Caccialepori (verticale), schema non in scala.
    cars: dict(kind, keys=[(t, x, y, ang)] in coordinate 0..1 del box, label, t0, t1)
    marks: dict(t, x, y, text) fumetti/scoppi; olona: mostra il letto del fiume in alto"""
    def __init__(self, box, t0, t1=None, cars=(), marks=(), olona=False, label="schema semplificato · non in scala", dim=0.0):
        super().__init__(t0, t1, 0.4); self.box, self.cars, self.marks, self.olona, self.label, self.dim = box, list(cars), list(marks), olona, label, dim
        self._base = None
    def base(self):
        if self._base: return self._base
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0)
        im = Image.new("RGBA", (bw, bh), (40, 42, 40, 255)); d = ImageDraw.Draw(im)
        rw = int(bh * 0.22); cy = int(bh * 0.58); cx = int(bw * 0.58)
        rng = random.Random(4)
        for bx0, by0, bx1, by1 in [(0, 0, cx - rw // 2, cy - rw // 2), (cx + rw // 2, 0, bw, cy - rw // 2), (0, cy + rw // 2, cx - rw // 2, bh), (cx + rw // 2, cy + rw // 2, bw, bh)]:
            d.rectangle([bx0, by0, bx1, by1], fill=(70, 66, 60, 255))
            for _ in range(5):
                a_ = rng.uniform(bx0 + 10, max(bx0 + 11, bx1 - 120)); b_ = rng.uniform(by0 + 10, max(by0 + 11, by1 - 90))
                d.rectangle([a_, b_, min(bx1 - 8, a_ + rng.uniform(70, 160)), min(by1 - 8, b_ + rng.uniform(50, 110))], fill=(88, 82, 74, 255), outline=(58, 54, 50, 255), width=2)
        d.rectangle([0, cy - rw // 2, bw, cy + rw // 2], fill=(96, 96, 98, 255))
        d.rectangle([cx - rw // 2, 0, cx + rw // 2, bh], fill=(96, 96, 98, 255))
        for x in range(0, bw, 70):
            if abs(x - cx) > rw // 2 + 20: d.line([x, cy, x + 36, cy], fill=(230, 230, 220, 255), width=4)
        for y in range(0, bh, 70):
            if abs(y - cy) > rw // 2 + 20: d.line([cx, y, cx, y + 36], fill=(230, 230, 220, 255), width=4)
        if self.olona:
            d.rectangle([0, 18, cx - rw // 2 - 20, 70], fill=(120, 100, 76, 255))
            d.text((20, 44), "OLONA (IN SECCA)", font=font(OSW, 26, 600), fill=(240, 220, 180, 255), anchor="lm")
        f = font(OSW, 30, 600)
        d.text((40, cy + rw // 2 - 14), "VIA OSOPPO", font=f, fill=(240, 236, 220, 255), anchor="ls")
        d.text((cx + rw // 2 - 10, bh - 30), "VIA CACCIALEPORI", font=f, fill=(240, 236, 220, 255), anchor="rs")
        self._base = (im, cx, cy, rw)
        return self._base
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0); al = int(255 * a)
        base, cx, cy, rw = self.base(); im = base.copy(); d = ImageDraw.Draw(im)
        for c in self.cars:
            if t < c.get("t0", -99) or t > c.get("t1", 1e9): continue
            ks = c["keys"]
            if t <= ks[0][0]: k = ks[0][1:]
            elif t >= ks[-1][0]: k = ks[-1][1:]
            else:
                for p, q in zip(ks, ks[1:]):
                    if p[0] <= t <= q[0]:
                        u = ease_io((t - p[0]) / max(1e-6, q[0] - p[0])); k = tuple(lerp(p[j], q[j], u) for j in (1, 2, 3)); break
            L = int(bh * c.get("L", 0.20))
            car = topcar(c["kind"], L).rotate(-k[2], expand=True, resample=Image.BICUBIC)
            place(im, car, (k[0] * bw, k[1] * bh), "mm", 1.0)
            if c.get("label"):
                fl = font(OSW, 26, 600); lab = c["label"]; tw = tl(d, lab, fl); lx, ly = k[0] * bw, k[1] * bh - L * 0.42
                d.rounded_rectangle([lx - tw / 2 - 10, ly - 18, lx + tw / 2 + 10, ly + 18], 8, fill=(14, 12, 11, 210))
                d.text((lx, ly), lab, font=fl, fill=WHITE + (255,), anchor="mm")
        for m in self.marks:
            if t < m["t"] or t > m["t"] + m.get("d", 1.6): continue
            u = ease((t - m["t"]) / 0.25); x, y = m["x"] * bw, m["y"] * bh; r = 70 * u
            pts = [(x + (r if j % 2 == 0 else r * .5) * math.cos(j * math.pi / 8), y + (r if j % 2 == 0 else r * .5) * math.sin(j * math.pi / 8)) for j in range(16)]
            d.polygon(pts, fill=(250, 210, 70, 235), outline=RED + (255,))
            if m.get("text"): d.text((x, y), m["text"], font=font(OSW, int(30 * u) + 1, 700), fill=INK + (255,), anchor="mm")
        if self.dim:
            ov = Image.new("RGBA", (bw, bh), (0, 0, 0, int(255 * self.dim))); im.alpha_composite(ov); d = ImageDraw.Draw(im)
        if self.label: d.text((bw - 16, 30), self.label, font=font(COURR, 20), fill=(220, 210, 190, 230), anchor="rs")
        m = Image.new("L", (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, bw - 1, bh - 1], 18, fill=al)
        im.putalpha(m); lay.alpha_composite(im, (int(x0), int(y0)))

def sentence_card(rows, w=640, title="LE CONDANNE · 1958", seed=17):
    """tabellina delle pene (dalle ricostruzioni giornalistiche delle sentenze)"""
    h = 120 + 60 * len(rows) + 60
    im = paper(w, h, PAPER, seed, 0.4); d = ImageDraw.Draw(im)
    d.text((w / 2, 50), title, font=font(OSW, 40, 700), fill=INK + (255,), anchor="mm")
    d.line([(30, 86), (w - 30, 86)], fill=(120, 110, 100, 255), width=2)
    for k, (n, p) in enumerate(rows):
        y = 120 + k * 60
        d.text((40, y), n, font=font(COURR, 30), fill=INK + (255,), anchor="lm")
        d.text((w - 40, y), p, font=font(OSW, 32, 600), fill=RED + (255,), anchor="rm")
    recon_label(d, w, h)
    return im

fi.PLACES.update({"Caracas": (-66.9, 10.5)})

def cover_folder(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 27, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .30), "FASCICOLO N. 007", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .52), "VIA OSOPPO", font=font(SERIF, int(w * .11)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .72), "Milano · 27 febbraio 1958", font=font(COURR, int(w * .045)), fill=(90, 70, 50, 255), anchor="mm")
    return im
