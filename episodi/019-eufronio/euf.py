# Elementi grafici del caso 019 (il cratere di Eufronio, 1971-2015): vaso stilizzato generico (nessuna riproduzione
# delle pitture originali), tumulo etrusco, Polaroid ricostruite, magazzino del Porto franco, il "viaggio" del vaso.
# Tutto disegnato da codice: nessuna foto reale, nessun documento originale, nessun logo.
import math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "018-metanolo"))
from met import *
import met, fi, fx, pon
from fx import *
from pon import WorldMap, WPL

WPL.update({"Cerveteri": (12.10, 42.00), "Roma": (12.50, 41.90), "Zurigo": (8.54, 47.37), "Ginevra": (6.14, 46.20),
            "New York": (-74.0, 40.71), "Beirut": (35.50, 33.89), "Parigi": (2.35, 48.86), "Atene": (23.73, 37.98),
            "Malibu": (-118.78, 34.03), "Boston": (-71.06, 42.36), "Londra": (-0.13, 51.51), "Santa Marinella": (11.85, 42.03),
            "Ladispoli": (12.07, 41.95), "Civitavecchia": (11.80, 42.09), "Napoli": (14.25, 40.85), "Basilea": (7.59, 47.56)})

TERRA = (196, 96, 52); BLK = (24, 18, 16)
_pe = {}
def epic(name, size):
    k = (name, size)
    if k in _pe: return _pe[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); dk = (40, 34, 30, 255); wh = (240, 238, 232, 255)
    if name in ("krater", "krater_broken", "krater_dirty", "bottle", "bottle_bad"):
        if name == "bottle": name = "krater"
        if name == "bottle_bad": name = "krater_dirty"
        # cratere a calice stilizzato: corpo nero, fascia arancio con sagome generiche (non le pitture originali)
        body = [P(.14, .10), P(.86, .10), P(.80, .30), P(.72, .62), P(.60, .70), P(.40, .70), P(.28, .62), P(.20, .30)]
        d.polygon(body, fill=BLK + (255,), outline=(205, 170, 120, 255))
        d.line(body + [body[0]], fill=(205, 170, 120, 255), width=S // 60)
        d.polygon([P(.19, .24), P(.81, .24), P(.76, .46), P(.24, .46)], fill=TERRA + (255,))
        rnd = random.Random(7)
        for j in range(5):
            x = .30 + j * .10; d.ellipse([P(x - .025, .27), P(x + .025, .32)], fill=BLK + (255,))
            d.line([P(x, .32), P(x + rnd.uniform(-.02, .02), .43)], fill=BLK + (255,), width=S // 50)
            d.line([P(x - .03, .36), P(x + .03, .36)], fill=BLK + (255,), width=S // 70)
        for x in (.22, .78):
            d.arc([P(x - .07, .52), P(x + .07, .66)], 0, 360, fill=(205, 170, 120, 255), width=S // 40)
        d.rectangle([P(.45, .70), P(.55, .80)], fill=BLK + (255,), outline=(205, 170, 120, 255), width=S // 90)
        d.polygon([P(.32, .90), P(.68, .90), P(.58, .80), P(.42, .80)], fill=BLK + (255,), outline=(205, 170, 120, 255))
        d.line([P(.32, .90), P(.68, .90), P(.58, .80), P(.42, .80), P(.32, .90)], fill=(205, 170, 120, 255), width=S // 90)
        d.line([P(.24, .50), P(.76, .50)], fill=TERRA + (255,), width=S // 80)
        d.rectangle([P(.14, .08), P(.86, .11)], fill=TERRA + (255,))
        if name == "krater_broken":
            for (a_, b_) in (((.30, .10), (.42, .40)), ((.42, .40), (.36, .68)), ((.60, .10), (.55, .35)), ((.55, .35), (.70, .55))):
                d.line([P(*a_), P(*b_)], fill=(230, 220, 200, 255), width=S // 45)
        if name == "krater_dirty":
            rr = random.Random(3)
            for _ in range(40):
                x, y, r = rr.uniform(.18, .8), rr.uniform(.12, .72), rr.uniform(.02, .06)
                d.ellipse([P(x - r, y - r), P(x + r, y + r)], fill=(120, 90, 60, 200))
    elif name == "tomb":        # tumulo etrusco stilizzato con ingresso
        d.ellipse([P(.04, .30), P(.96, 1.10)], fill=(110, 120, 80, 255))
        d.rectangle([P(.04, .70), P(.96, .92)], fill=(150, 140, 110, 255))
        d.rectangle([P(.40, .58), P(.60, .92)], fill=(40, 32, 28, 255))
        d.polygon([P(.38, .58), P(.62, .58), P(.50, .48)], fill=(150, 140, 110, 255))
        for x in (.12, .26, .74, .88): d.line([P(x, .72), P(x, .90)], fill=(120, 110, 90, 255), width=S // 90)
    elif name == "polaroid":
        d.rectangle([P(.14, .08), P(.86, .92)], fill=(244, 242, 236, 255), outline=(190, 186, 176, 255), width=S // 120)
        d.rectangle([P(.20, .14), P(.80, .70)], fill=(60, 54, 48, 255))
        sub = epic("krater_dirty", int(size * 0.5)); im.alpha_composite(sub.resize((int(S * .5), int(S * .5))), (int(S * .25), int(S * .17)))
    elif name == "spade":       # vanga
        d.rectangle([P(.47, .06), P(.53, .62)], fill=(150, 110, 70, 255))
        d.rectangle([P(.38, .04), P(.62, .10)], fill=(150, 110, 70, 255))
        d.polygon([P(.34, .60), P(.66, .60), P(.62, .92), P(.50, .97), P(.38, .92)], fill=(170, 176, 182, 255))
    elif name == "warehouse":   # magazzino del porto franco (generico)
        d.rectangle([P(.06, .24), P(.94, .92)], fill=(140, 144, 150, 255))
        for r in range(4):
            for c in range(6):
                d.rectangle([P(.12 + c * .135, .32 + r * .14), P(.20 + c * .135, .40 + r * .14)], fill=(70, 80, 96, 255))
        d.rectangle([P(.04, .18), P(.96, .26)], fill=(100, 104, 110, 255))
        d.text(P(.50, .22), "PORTO FRANCO", font=font(OSW, int(S * .06), 700), fill=wh, anchor="mm")
        d.rectangle([P(.42, .76), P(.58, .92)], fill=(50, 50, 56, 255))
    elif name == "skyline":     # una grande città americana, generica
        rr = random.Random(5)
        x = .04
        while x < .92:
            w = rr.uniform(.07, .12); h = rr.uniform(.25, .75)
            d.rectangle([P(x, .92 - h), P(x + w, .92)], fill=(90, 100, 120, 255))
            for yy in range(int(h / .07)):
                d.rectangle([P(x + w * .3, .92 - h + .03 + yy * .07), P(x + w * .7, .92 - h + .05 + yy * .07)], fill=(220, 200, 120, 255))
            x += w + .01
        d.rectangle([P(.02, .92), P(.98, .96)], fill=(60, 60, 70, 255))
    elif name == "temple":      # museo classico generico (colonne)
        d.polygon([P(.08, .30), P(.50, .08), P(.92, .30)], fill=(220, 214, 200, 255))
        for x in (.16, .32, .48, .64, .80): d.rectangle([P(x, .34), P(x + .06, .84)], fill=(230, 226, 214, 255))
        d.rectangle([P(.06, .30), P(.94, .35)], fill=(200, 194, 180, 255)); d.rectangle([P(.04, .84), P(.96, .92)], fill=(200, 194, 180, 255))
    elif name == "dollar_bag":
        d.ellipse([P(.16, .30), P(.84, .94)], fill=(110, 140, 80, 255)); d.polygon([P(.36, .32), P(.64, .32), P(.72, .10), P(.28, .10)], fill=(110, 140, 80, 255))
        d.rectangle([P(.34, .28), P(.66, .34)], fill=(70, 90, 50, 255)); d.text(P(.50, .64), "$", font=font(OSW, int(S * .36), 700), fill=wh, anchor="mm")
    elif name == "crate":
        d.rectangle([P(.10, .26), P(.90, .90)], fill=(170, 125, 75, 255), outline=(110, 75, 40, 255), width=S // 50)
        for y in (.47, .68): d.line([P(.10, y), P(.90, y)], fill=(110, 75, 40, 255), width=S // 60)
        d.line([P(.10, .26), P(.90, .90)], fill=(110, 75, 40, 255), width=S // 50)
        d.text(P(.50, .16), "FRAGILE", font=font(OSW, int(S * .09), 700), fill=RED + (255,), anchor="mm")
    elif name == "letter":
        d.rectangle([P(.16, .10), P(.84, .90)], fill=(236, 230, 214, 255), outline=(170, 160, 140, 255), width=S // 120)
        for j in range(9): d.line([P(.24, .22 + j * .07), P(.76 - (j % 3) * .06, .22 + j * .07)], fill=(90, 80, 70, 255), width=S // 110)
        d.line([P(.50, .84), P(.74, .80)], fill=(30, 40, 120, 255), width=S // 70)
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _pe[k] = im
    return im

_prev_icon_e = fx.icon
def _icon_e(name, size, color=None):
    if isinstance(name, str):
        m = epic(name, size)
        if m is not None: return m
    return _prev_icon_e(name, size, color)
fx.icon = _icon_e

def cover_folder19(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 29, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 019", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "IL CRATERE DI EUFRONIO", font=font(SERIF, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "CERVETERI · 1971-2015", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im

STAGES = [("krater_dirty", "APPENA SCAVATO"), ("krater_broken", "IN FRAMMENTI"), ("krater", "RESTAURATO"), ("temple", "IN MUSEO")]

class Polaroids(El):
    """scenografia ricorrente del magazzino di Ginevra: una parete di Polaroid ricostruite.
    n: quante foto; seq: se True mostra la sequenza scavo -> frammenti -> restauro -> museo; hl: foto evidenziata"""
    def __init__(self, box, t0, t1=None, n=12, seq=False, hl=None, title="POLAROID · RICOSTRUZIONE GRAFICA · non originali"):
        super().__init__(t0, t1, 0.4); self.box, self.n, self.seq, self.hl, self.title = box, n, seq, hl, title
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; d = ImageDraw.Draw(lay); al = int(255 * a)
        d.rounded_rectangle([x0, y0, x1, y1], 18, fill=(52, 44, 38, int(220 * a)), outline=(120, 100, 80, al), width=3)
        d.text(((x0 + x1) / 2, y1 - 22), self.title, font=font(COURR, 22), fill=(190, 180, 160, al), anchor="mm")
        if self.seq:
            n = 4; xs = [x0 + (x1 - x0) * (j + 0.5) / n for j in range(n)]; cy = y0 + (y1 - y0) * 0.45; sz = 260
            for j, (ic, lab) in enumerate(STAGES):
                tt = self.t0 + 0.6 * j
                if t < tt: continue
                u = back(min(1, (t - tt) / 0.35)); s = max(4, int(sz * u))
                card = Image.new("RGBA", (sz, int(sz * 1.15)), (244, 242, 236, 255)); cd = ImageDraw.Draw(card)
                cd.rectangle([14, 14, sz - 14, sz - 14], fill=(60, 54, 48, 255))
                card.alpha_composite(fx.icon(ic, sz - 50), (25, 25))
                cd.text((sz / 2, sz + 8), lab, font=font(OSW, 26, 700), fill=(40, 34, 30, 255), anchor="mm")
                card = card.rotate((-4, 3, -2, 4)[j], expand=True, resample=Image.BICUBIC)
                if s != sz: card = card.resize((max(4, int(card.width * u)), max(4, int(card.height * u))), Image.BILINEAR)
                place(lay, card, (xs[j], cy), "mm", a)
                if j < n - 1 and t > tt + 0.4:
                    d.polygon([(xs[j] + 150, cy), (xs[j] + 128, cy - 16), (xs[j] + 128, cy + 16)], fill=RED + (al,))
            return
        cols = 6; rows = max(1, (self.n + cols - 1) // cols); cw = (x1 - x0) / cols; ch = (y1 - y0 - 50) / rows
        rnd = random.Random(11); kinds = ["krater_dirty", "krater_broken", "antique", "krater", "krater_dirty", "tomb"]
        for j in range(self.n):
            tt = self.t0 + 0.08 * j
            if t < tt: continue
            c, r = j % cols, j // cols; cx = x0 + cw * (c + 0.5); cy = y0 + 20 + ch * (r + 0.5)
            sz = int(min(cw, ch) * 0.78)
            card = Image.new("RGBA", (sz, int(sz * 1.12)), (244, 242, 236, 255)); cd = ImageDraw.Draw(card)
            cd.rectangle([8, 8, sz - 8, sz - 8], fill=(60, 54, 48, 255))
            card.alpha_composite(fx.icon(kinds[j % len(kinds)], sz - 30), (15, 15))
            card = card.rotate(rnd.uniform(-6, 6), expand=True, resample=Image.BICUBIC)
            place(lay, card, (cx, cy), "mm", a)
            if self.hl == j:
                rr = sz * 0.7 + 6 * math.sin(t * 6); d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=GOLD + (al,), width=6)

met.STEPS = [("tomba", "spade", "I TOMBAROLI"), ("inter", "truck", "INTERMEDIARI"), ("mercante", "crate", "IL MERCANTE"),
             ("restauro", "krater_broken", "IL RESTAURO"), ("museo", "temple", "IL MUSEO")]
