# Elementi grafici del caso 009 (le false teste di Modigliani, Livorno 1984): il Fosso Reale con la ruspa
# (scenografia ricorrente, schema non in scala), la sala della mostra con i piedistalli, teste di pietra
# STILIZZATE (sagome generiche, non le opere), icone del caso. Tutto disegnato da codice: nessuna foto reale, nessun logo.
import math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ("008-caravaggio", "007-osoppo", "006-tortora", "005-majorana"):
    sys.path.insert(0, os.path.join(HERE, "..", d_))
from fi import *
import fi
import fx
from fx import *
import car                       # icone (question, book, tv, mic, phone, folder, toplist...)
import osp                       # (hammer, river, clapper...)

fi.PLACES.update({"Livorno": (10.31, 43.55), "Parigi": (2.35, 48.86)})

STONE = (196, 190, 178)
GRANITE = (150, 148, 146)
WATER = (52, 84, 96)
BANK = (170, 150, 120)

# ---------------------------------------------------------------- testa di pietra stilizzata (sagoma generica)
_hc = {}
def stone_head(w, h, seed=1, tone=STONE, mud=0.0):
    k = (w, h, seed, tone, round(mud, 2))
    if k in _hc: return _hc[k]
    S = 3; W_, H_ = w * S, h * S
    im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im); rng = random.Random(seed)
    P = lambda a, b: (a * W_, b * H_)
    sk = 0.03 * (seed % 3 - 1)
    dark = tuple(max(0, c - 40) for c in tone) + (255,)
    # collo / base
    d.rectangle([P(.36, .78), P(.64, 1.0)], fill=dark)
    # volto allungato
    d.ellipse([P(.22 + sk, .04), P(.78 + sk, .86)], fill=tone + (255,))
    # naso lungo e sottile
    d.polygon([P(.50 + sk, .22), P(.46 + sk, .56), P(.54 + sk, .56)], fill=dark)
    # occhi a mandorla (incisi)
    for x in (.38, .62):
        d.ellipse([P(x - .07 + sk, .34), P(x + .07 + sk, .40)], fill=dark)
    # bocca piccola
    d.line([P(.46 + sk, .66), P(.54 + sk, .66)], fill=dark, width=W_ // 50)
    # texture della pietra
    for _ in range(60):
        x, y = rng.uniform(.25, .75), rng.uniform(.08, .84)
        d.point(P(x + sk, y), fill=(tone[0] - 30, tone[1] - 30, tone[2] - 30, 255))
    if mud > 0:
        ov = Image.new("RGBA", (W_, H_), (90, 74, 50, 0)); od = ImageDraw.Draw(ov)
        for _ in range(int(12 * mud)):
            x, y, r = rng.uniform(.2, .8), rng.uniform(.4, .95), rng.uniform(.05, .12)
            od.ellipse([P(x - r, y - r * .6), P(x + r, y + r * .6)], fill=(90, 74, 50, 200))
        ov.putalpha(Image.fromarray(np.minimum(np.array(ov.getchannel("A")), np.array(im.getchannel("A")))))
        im.alpha_composite(ov)
    im = im.resize((w, h), Image.LANCZOS); _hc[k] = im
    return im

# ---------------------------------------------------------------- scenografia: il Fosso Reale
class Canal(El):
    """canale visto di fronte (schema non in scala): palazzi, sponda di pietra, acqua, ruspa sulla sponda sinistra.
    digs: istanti in cui il braccio scende; finds: [(t, seed, tone)] teste che escono e si posano sulla sponda;
    crowd: istante in cui appare la gente sulla sponda; drop: [(t, seed)] pietra gettata (cade dall'alto)."""
    def __init__(self, box, t0, t1=None, digs=(), finds=(), crowd=None, drop=(), label="schema semplificato · non in scala", dim=0.0, ruspa=True):
        super().__init__(t0, t1, 0.4)
        self.box, self.digs, self.finds, self.crowd, self.drop, self.label, self.dim, self.ruspa = box, sorted(digs), list(finds), crowd, list(drop), label, dim, ruspa
        self._base = None
    def base(self):
        if self._base: return self._base
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0)
        im = Image.new("RGBA", (bw, bh), (120, 150, 170, 255)); d = ImageDraw.Draw(im)
        for k in range(bh // 2):
            c = int(150 + 60 * k / (bh / 2)); d.line([(0, k), (bw, k)], fill=(c - 40, c - 10, c + 10, 255))
        rng = random.Random(4); x = 0
        hy = int(bh * 0.40)
        while x < bw:     # palazzi livornesi semplici
            ww = rng.randint(120, 220); hh = rng.randint(int(bh * .18), int(bh * .30))
            col = rng.choice([(214, 170, 120), (226, 196, 150), (200, 140, 110), (230, 210, 170)])
            d.rectangle([x, hy - hh, x + ww, hy], fill=col + (255,))
            d.rectangle([x, hy - hh - 10, x + ww, hy - hh], fill=(150, 90, 70, 255))
            for r in range(2):
                for c in range(max(1, ww // 50)):
                    wx = x + 18 + c * 50; wy = hy - hh + 24 + r * 46
                    if wy + 28 < hy: d.rectangle([wx, wy, wx + 20, wy + 28], fill=(70, 80, 96, 255))
            x += ww + rng.randint(4, 14)
        # sponda di pietra
        wy = int(bh * 0.52)
        d.rectangle([0, hy, bw, wy], fill=BANK + (255,))
        for k in range(0, bw, 60):
            for j, yy in enumerate(range(hy, wy, 26)):
                d.rectangle([k + (30 if j % 2 else 0), yy, k + 56 + (30 if j % 2 else 0), yy + 22], outline=(140, 120, 94, 255), width=2)
        d.rectangle([0, hy - 8, bw, hy + 4], fill=(140, 124, 100, 255))
        self._base = (im, hy, wy)
        return self._base
    def arm(self, t):
        """discesa del braccio 0..1"""
        u = 0.0
        for td in self.digs:
            if td <= t < td + 2.6:
                k = (t - td) / 2.6; u = max(u, math.sin(math.pi * k))
        return u
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0)
        base, hy, wy = self.base(); im = base.copy(); d = ImageDraw.Draw(im)
        # acqua animata
        d.rectangle([0, wy, bw, bh], fill=WATER + (255,))
        for j in range(8):
            yy = wy + 20 + j * (bh - wy) / 8
            for k in range(0, bw, 90):
                ox = (t * 40 + j * 37) % 90
                d.line([(k + ox, yy), (k + ox + 40, yy)], fill=(90, 130, 140, 255), width=3)
        # folla sulla sponda
        if self.crowd is not None and t >= self.crowd:
            rng = random.Random(9)
            for k in range(14):
                cx = 560 + k * (bw - 640) / 14 + rng.uniform(-10, 10)
                if t >= self.crowd + k * 0.05:
                    col = rng.choice([(90, 80, 70), (60, 80, 120), (150, 60, 50), (200, 190, 170), (70, 90, 70)])
                    d.rectangle([cx - 11, hy - 52, cx + 11, hy - 6], fill=col + (255,))
                    d.ellipse([cx - 10, hy - 76, cx + 10, hy - 54], fill=(214, 176, 140, 255))
        # teste ritrovate posate sulla sponda (a destra della ruspa)
        for n, (tf, seed, tone) in enumerate(self.finds):
            if t >= tf + 1.6:
                hd = stone_head(96, 132, seed, tone, mud=0.6); im.alpha_composite(hd, (int(bw * 0.30 + n * 120), hy - 128))
        # ruspa
        if self.ruspa:
            bx, by = int(bw * 0.12), hy
            d.rectangle([bx - 90, by - 40, bx + 90, by - 4], fill=(40, 40, 40, 255))
            for k in range(5): d.ellipse([bx - 86 + k * 36, by - 30, bx - 58 + k * 36, by - 2], fill=(70, 70, 70, 255))
            d.rectangle([bx - 70, by - 130, bx + 50, by - 40], fill=(230, 170, 40, 255))
            d.rectangle([bx - 50, by - 120, bx + 10, by - 78], fill=(150, 190, 210, 255))
            u = self.arm(t)
            # eventuale testa in benna
            carrying = None
            for (tf, seed, tone) in self.finds:
                if tf <= t < tf + 1.6: carrying = (tf, seed, tone)
            if carrying: u = max(u, 1.0 - min(1.0, (t - carrying[0]) / 1.4))
            sh = (bx + 40, by - 110)
            el = (bx + 230, by - 230 + 160 * u)
            tip = (bx + 330, by - 60 + (wy - hy + 120) * u)
            d.line([sh, el], fill=(220, 160, 30, 255), width=24); d.line([el, tip], fill=(220, 160, 30, 255), width=18)
            d.polygon([(tip[0] - 40, tip[1] - 10), (tip[0] + 40, tip[1] - 10), (tip[0] + 30, tip[1] + 40), (tip[0] - 30, tip[1] + 40)], fill=(60, 60, 60, 255))
            if u > 0.6:
                d.ellipse([tip[0] - 60, wy - 8, tip[0] + 60, wy + 14], outline=(170, 200, 210, 255), width=3)
            if carrying:
                hd = stone_head(70, 96, carrying[1], carrying[2], mud=0.8); im.alpha_composite(hd, (int(tip[0] - 35), int(tip[1] - 90)))
                d = ImageDraw.Draw(im)
        # pietra gettata (cade in acqua)
        for (td, seed) in self.drop:
            if td <= t < td + 1.4:
                k = (t - td) / 0.9
                if k < 1:
                    hd = stone_head(70, 96, seed); yy = int(hy - 140 + (wy - hy + 160) * k * k)
                    im.alpha_composite(hd, (int(bw * 0.62), yy)); d = ImageDraw.Draw(im)
                else:
                    r = 40 + 120 * (k - 1); d.ellipse([bw * 0.62 + 35 - r, wy + 30 - r * .2, bw * 0.62 + 35 + r, wy + 30 + r * .2], outline=(200, 230, 240, 255), width=4)
        if self.dim:
            im.alpha_composite(Image.new("RGBA", (bw, bh), (0, 0, 0, int(255 * self.dim)))); d = ImageDraw.Draw(im)
        if self.label:
            d.text((bw - 16, bh - 14), self.label, font=font(COURR, 20), fill=(220, 230, 236, 230), anchor="rs")
            d.text((16, bh - 14), "Fosso Reale · Livorno", font=font(COURR, 20), fill=(220, 230, 236, 230), anchor="ls")
        m = Image.new("L", (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, bw - 1, bh - 1], 18, fill=int(255 * a))
        im.putalpha(m); lay.alpha_composite(im, (int(x0), int(y0)))

# ---------------------------------------------------------------- sala della mostra con piedistalli
class Gallery(El):
    """sala di museo (schema): n piedistalli; heads: [(t, seed, tone)] che compaiono; fakes: [(t, idx)] timbro FALSO;
    labels: testo sotto ogni piedistallo"""
    def __init__(self, box, t0, t1=None, heads=(), fakes=(), labels=None, label="schema semplificato · teste stilizzate", dim=0.0):
        super().__init__(t0, t1, 0.4)
        self.box, self.heads, self.fakes, self.labels, self.label, self.dim = box, list(heads), list(fakes), labels, label, dim
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0)
        im = Image.new("RGBA", (bw, bh), (232, 226, 214, 255)); d = ImageDraw.Draw(im)
        fy = int(bh * 0.80)
        d.rectangle([0, fy, bw, bh], fill=(150, 116, 84, 255))
        for k in range(12): d.line([(k * bw / 11, fy), (k * bw / 11 + (k - 5.5) * 30, bh)], fill=(126, 96, 70, 255), width=2)
        d.rectangle([0, 0, bw, 30], fill=(206, 198, 184, 255))
        n = max(3, len(self.heads))
        for k in range(n):
            cx = bw * (k + 0.5) / n
            d.ellipse([cx - 110, 34, cx + 110, 70], fill=(255, 250, 230, 120))      # luce dall'alto
            d.rectangle([cx - 70, fy - 220, cx + 70, fy], fill=(246, 244, 238, 255), outline=(190, 184, 172, 255), width=3)
            d.rectangle([cx - 82, fy - 232, cx + 82, fy - 214], fill=(236, 232, 224, 255))
            if self.labels and k < len(self.labels):
                d.text((cx, fy - 110), self.labels[k], font=font(OSW, 26, 600), fill=INK + (255,), anchor="mm")
        for k, (th, seed, tone) in enumerate(self.heads):
            if t >= th:
                u = ease(min(1, (t - th) / 0.5)); cx = bw * (k + 0.5) / n
                hd = set_alpha(stone_head(150, 206, seed, tone), u)
                im.alpha_composite(hd, (int(cx - 75), int(fy - 232 - 206 + 20 * (1 - u))))
        d = ImageDraw.Draw(im)
        for (tf, k) in self.fakes:
            if t >= tf:
                cx = bw * (k + 0.5) / n; st = stamp_img("FALSO", RED, 46, -10)
                im.alpha_composite(st, (int(cx - st.width / 2), int(fy - 360)))
        if self.dim:
            im.alpha_composite(Image.new("RGBA", (bw, bh), (0, 0, 0, int(255 * self.dim)))); d = ImageDraw.Draw(im)
        if self.label:
            d.text((bw - 16, bh - 14), self.label, font=font(COURR, 20), fill=(240, 230, 210, 230), anchor="rs")
            d.text((16, bh - 14), "Villa Maria · Livorno", font=font(COURR, 20), fill=(240, 230, 210, 230), anchor="ls")
        m = Image.new("L", (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, bw - 1, bh - 1], 18, fill=int(255 * a))
        im.putalpha(m); lay.alpha_composite(im, (int(x0), int(y0)))

# ---------------------------------------------------------------- icone del caso
_mc = {}
def mpic(name, size):
    k = (name, size)
    if k in _mc: return _mc[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S)
    wh = WHITE + (255,); ink = INK + (255,); dk = (34, 32, 30, 255)
    if name in ("head", "head_g", "head_m"):
        tone = GRANITE if name == "head_g" else STONE
        hd = stone_head(int(S * .56), int(S * .78), 2 if name == "head" else 3, tone, mud=0.7 if name == "head_m" else 0)
        im.alpha_composite(hd, (int(S * .22), int(S * .04)))
        d.rectangle([P(.26, .82), P(.74, .96)], fill=(120, 110, 100, 255))
    elif name == "drill":      # trapano elettrico generico (senza marchio)
        d.rounded_rectangle([P(.14, .26), P(.68, .48)], S // 20, fill=(60, 64, 70, 255))
        d.rounded_rectangle([P(.30, .44), P(.48, .86)], S // 30, fill=(200, 120, 40, 255))
        d.rectangle([P(.68, .32), P(.78, .42)], fill=(150, 150, 156, 255))
        d.line([P(.78, .37), P(.96, .37)], fill=(190, 190, 196, 255), width=S // 40)
        d.rectangle([P(.34, .52), P(.40, .60)], fill=dk)
        d.line([P(.40, .86), P(.30, .96), P(.12, .96)], fill=dk, width=S // 60)
    elif name == "chisel":     # martello e scalpello
        d.rectangle([P(.20, .58), P(.70, .66)], fill=(150, 150, 156, 255)); d.polygon([P(.70, .58), P(.86, .62), P(.70, .66)], fill=(190, 190, 196, 255))
        d.rectangle([P(.06, .56), P(.20, .68)], fill=(120, 80, 50, 255))
        d.line([P(.30, .14), P(.56, .46)], fill=(140, 96, 60, 255), width=S // 18)
        d.rectangle([P(.18, .10), P(.42, .22)], fill=(80, 80, 86, 255))
    elif name == "excavator":
        d.rectangle([P(.06, .72), P(.56, .84)], fill=(40, 40, 40, 255))
        for k in range(5): d.ellipse([P(.08 + k * .095, .74), P(.16 + k * .095, .82)], fill=(80, 80, 80, 255))
        d.rectangle([P(.10, .44), P(.46, .72)], fill=(230, 170, 40, 255)); d.rectangle([P(.14, .48), P(.30, .62)], fill=(150, 190, 210, 255))
        d.line([P(.42, .52), P(.70, .20)], fill=(220, 160, 30, 255), width=S // 16); d.line([P(.70, .20), P(.88, .58)], fill=(220, 160, 30, 255), width=S // 20)
        d.polygon([P(.80, .56), P(.96, .56), P(.92, .72), P(.82, .72)], fill=(60, 60, 60, 255))
    elif name == "magazine":   # settimanale generico
        d.rectangle([P(.18, .06), P(.82, .94)], fill=(240, 236, 228, 255))
        d.rectangle([P(.18, .06), P(.82, .22)], fill=RED + (255,))
        d.text(P(.50, .14), "SETTIMANALE", font=font(OSW, int(S * .07), 700), fill=wh, anchor="mm")
        hd = stone_head(int(S * .26), int(S * .34), 5); im.alpha_composite(hd, (int(S * .26), int(S * .28)))
        d.text(P(.70, .40), "?", font=font(SERIF, int(S * .2)), fill=RED + (255,), anchor="mm")
        for k in range(5): d.line([P(.24, .68 + k * .05), P(.76 - (k % 2) * .1, .68 + k * .05)], fill=(120, 116, 110, 255), width=S // 90)
    elif name == "eiffel":
        d.polygon([P(.50, .04), P(.56, .40), P(.72, .92), P(.60, .92), P(.50, .66), P(.40, .92), P(.28, .92), P(.44, .40)], fill=(90, 84, 80, 255))
        d.rectangle([P(.36, .56), P(.64, .60)], fill=(90, 84, 80, 255)); d.rectangle([P(.42, .36), P(.58, .40)], fill=(90, 84, 80, 255))
    elif name == "fortress":   # fortezza generica
        d.rectangle([P(.08, .44), P(.92, .90)], fill=(170, 100, 70, 255))
        for k in range(6): d.rectangle([P(.08 + k * .16, .36), P(.16 + k * .16, .46)], fill=(170, 100, 70, 255))
        d.rectangle([P(.40, .16), P(.60, .44)], fill=(150, 86, 60, 255))
        for k in range(3): d.rectangle([P(.40 + k * .08, .10), P(.44 + k * .08, .18)], fill=(150, 86, 60, 255))
        d.rounded_rectangle([P(.42, .64), P(.58, .90)], S // 20, fill=(60, 40, 30, 255))
        d.rectangle([P(0, .90), P(1, .98)], fill=WATER + (255,))
    elif name == "tvlive":     # televisore con DIRETTA
        d.rounded_rectangle([P(.08, .18), P(.92, .80)], S // 20, fill=(50, 48, 46, 255))
        d.rectangle([P(.14, .24), P(.74, .74)], fill=(80, 110, 130, 255))
        hd = stone_head(int(S * .22), int(S * .32), 6); im.alpha_composite(hd, (int(S * .33), int(S * .32)))
        d.rounded_rectangle([P(.16, .26), P(.40, .34)], S // 60, fill=RED + (255,)); d.text(P(.28, .30), "DIRETTA", font=font(OSW, int(S * .05), 700), fill=wh, anchor="mm")
        for k in range(3): d.ellipse([P(.78, .30 + k * .12), P(.86, .38 + k * .12)], fill=(120, 116, 110, 255))
        d.line([P(.30, .80), P(.22, .92)], fill=dk, width=S // 40); d.line([P(.70, .80), P(.78, .92)], fill=dk, width=S // 40)
    elif name == "centenary":  # torta / "100"
        d.rounded_rectangle([P(.12, .30), P(.88, .80)], S // 20, fill=(236, 230, 214, 255), outline=(176, 136, 70, 255), width=S // 50)
        d.text(P(.50, .55), "100", font=font(OSW, int(S * .30), 700), fill=RED + (255,), anchor="mm")
        d.text(P(.50, .20), "1884 · 1984", font=font(OSW, int(S * .09), 700), fill=GOLD + (255,), anchor="mm")
    elif name == "mud":        # benna con fango
        d.polygon([P(.14, .30), P(.86, .30), P(.76, .82), P(.24, .82)], fill=(70, 70, 70, 255))
        d.ellipse([P(.16, .14), P(.84, .44)], fill=(96, 80, 56, 255))
        for k in range(4): d.ellipse([P(.30 + k * .12, .80), P(.36 + k * .12, .90)], fill=(96, 80, 56, 255))
    elif name == "critic":     # cartellino AUTENTICA
        d.rectangle([P(.12, .20), P(.88, .80)], fill=(240, 236, 228, 255), outline=(150, 140, 120, 255), width=S // 60)
        d.text(P(.50, .40), "AUTENTICA", font=font(OSW, int(S * .13), 700), fill=(40, 120, 60, 255), anchor="mm")
        d.line([P(.24, .58), P(.42, .70), P(.78, .50)], fill=(40, 120, 60, 255), width=S // 24)
    elif name == "photos":     # tre fotografie
        for k, (x, y, r) in enumerate(((.14, .20, -8), (.32, .28, 4), (.48, .18, 10))):
            ph = Image.new("RGBA", (int(S * .40), int(S * .46)), (246, 244, 236, 255)); pd = ImageDraw.Draw(ph)
            pd.rectangle([S * .03, S * .03, S * .37, S * .34], fill=(120, 140, 120, 255))
            hd = stone_head(int(S * .14), int(S * .2), 7 + k, STONE); ph.alpha_composite(hd, (int(S * .13), int(S * .10)))
            ph = ph.rotate(r, expand=True, resample=Image.BICUBIC); im.alpha_composite(ph, (int(S * x), int(S * y)))
        d = ImageDraw.Draw(im)
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _mc[k] = im
    return im

_prev_icon = fx.icon
def _icon(name, size, color=None):
    if isinstance(name, str):
        m = mpic(name, size)
        if m is not None: return m
    return _prev_icon(name, size, color)
fx.icon = _icon

def cover_folder(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 28, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 009", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "LE TESTE DI MODÌ", font=font(SERIF, int(w * .09)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .70), "Livorno · estate 1984", font=font(COURR, int(w * .045)), fill=(90, 70, 50, 255), anchor="mm")
    return im

def label_card(lines, w=560, title=None, seed=31, size=34):
    h = 90 + len(lines) * (size + 18) + (60 if title else 0)
    im = paper(w, h, (236, 230, 214), seed, 0.3); d = ImageDraw.Draw(im); y = 40
    if title:
        d.text((w / 2, y + 10), title, font=font(OSW, size + 6, 700), fill=INK + (255,), anchor="mm"); y += 60
        d.line([(30, y - 14), (w - 30, y - 14)], fill=(140, 130, 110, 255), width=2)
    for ln in lines:
        d.text((36, y + size / 2), ln, font=font(COURR, size), fill=INK + (255,), anchor="lm"); y += size + 18
    recon_label(d, w, h)
    return im
