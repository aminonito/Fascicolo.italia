# Elementi grafici del caso 016 (la Pietà di Michelangelo colpita a martellate in San Pietro, 21/5/1972 -
# restauro e ritorno dietro il vetro, marzo 1973): la statua come SAGOMA STILIZZATA (non riproduce l'opera),
# la cappella come scenografia (schema non in scala), frammenti, martello, mappa del mondo. Tutto disegnato da codice.
import math, random, os, sys, inspect
PTDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PTDIR, "..", "015-castelvecchio"))
from cv import *
import cv, fi, fx, pon
from fx import *

MARBLE = (232, 228, 218)
MARBLE_D = (186, 180, 168)
MARBLE_DD = (150, 144, 134)
BREAK = (206, 196, 176)

# ------------------------------------------------------------------ la statua (sagoma stilizzata)
_pc = {}
def pieta_img(w, arm=True, nose=True, cracks=0.0, eye=True, seed=3):
    """sagoma piramidale generica: madonna seduta con velo, figura distesa sulle ginocchia. NON riproduce l'opera."""
    key = (w, arm, nose, round(cracks, 2), eye)
    if key in _pc: return _pc[key]
    S = 2; W_ = w * S; H_ = int(w * 1.0) * S
    im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda u, v: (u * W_, v * H_)
    M = MARBLE + (255,); D = MARBLE_D + (255,); DD = MARBLE_DD + (255,)
    # basamento roccioso
    d.polygon([P(.06, .86), P(.94, .86), P(.98, 1.0), P(.02, 1.0)], fill=(200, 194, 182, 255))
    # manto della madonna (piramide)
    d.polygon([P(.10, .88), P(.30, .50), P(.38, .30), P(.62, .30), P(.72, .50), P(.92, .88)], fill=M)
    for k in range(7):   # pieghe
        x = .16 + k * .11
        d.line([P(x + .06, .56), P(x, .87)], fill=D, width=int(3 * S))
    # velo e testa
    d.polygon([P(.38, .33), P(.42, .14), P(.50, .09), P(.58, .14), P(.62, .33)], fill=D)
    d.ellipse([P(.445, .135), P(.555, .265)], fill=M)                       # volto
    if eye:
        d.arc([P(.465, .18), P(.495, .20)], 0, 180, fill=DD, width=int(2 * S))
        d.arc([P(.505, .18), P(.535, .20)], 0, 180, fill=DD, width=int(2 * S))
    else:
        d.polygon([P(.462, .175), P(.50, .17), P(.49, .205), P(.465, .2)], fill=BREAK + (255,))
    if nose:
        d.polygon([P(.50, .19), P(.485, .225), P(.51, .225)], fill=DD)
    else:
        d.polygon([P(.49, .195), P(.482, .228), P(.515, .228), P(.507, .2)], fill=BREAK + (255,))
    d.arc([P(.48, .232), P(.52, .248)], 0, 180, fill=DD, width=int(2 * S))
    # fascia sul petto
    d.line([P(.40, .34), P(.60, .42)], fill=D, width=int(7 * S))
    # figura distesa sulle ginocchia
    C = (242, 238, 230, 255)
    for col, ex in ((DD, 5), (C, 0)):
        d.ellipse([P(.18 - ex / 900, .50 - ex / 900), P(.28 + ex / 900, .60 + ex / 900)], fill=col)   # testa
        d.line([P(.25, .58), P(.42, .62), P(.62, .64)], fill=col, width=int((30 + ex) * S), joint="curve")  # busto
        d.line([P(.62, .64), P(.78, .66)], fill=col, width=int((24 + ex) * S))               # cosce
        d.line([P(.78, .66), P(.84, .84)], fill=col, width=int((18 + ex) * S))               # gambe
        d.line([P(.32, .62), P(.30, .80)], fill=col, width=int((12 + ex) * S))               # braccio che pende
    # braccio sinistro della madonna (aperto)
    if arm:
        d.line([P(.62, .36), P(.68, .46)], fill=M, width=int(16 * S))
        d.line([P(.68, .46), P(.80, .44)], fill=M, width=int(14 * S))
        d.ellipse([P(.79, .41), P(.85, .47)], fill=M)
    else:
        d.line([P(.62, .36), P(.675, .45)], fill=M, width=int(16 * S))
        d.ellipse([P(.66, .435), P(.69, .465)], fill=BREAK + (255,))
    # crepe
    if cracks > 0:
        rng = random.Random(seed)
        for k in range(int(26 * cracks)):
            x, y = rng.uniform(.40, .62), rng.uniform(.12, .45)
            pts = [P(x, y)]
            for j in range(3):
                x += rng.uniform(-.025, .025); y += rng.uniform(.0, .03); pts.append(P(x, y))
            d.line(pts, fill=(120, 112, 100, int(255 * min(1, cracks))), width=int(1.6 * S))
    im = im.resize((w, int(w * 1.0)), Image.LANCZOS)
    _pc[key] = im
    return im

class Pieta(El):
    """statua stilizzata. hits: [t] colpi (scossa + schegge); arm_t/nose_t/eye_t: distacco; fix_t: torna integra;
    glass_t: lastra di vetro davanti; label"""
    def __init__(self, xy, w, t0, t1=None, hits=(), arm_t=None, nose_t=None, eye_t=None, fix_t=None, glass_t=None,
                 broken=False, label="sagoma stilizzata · non è l'opera", fall=True):
        super().__init__(t0, t1, 0.4)
        self.xy, self.w, self.hits, self.arm_t, self.nose_t, self.eye_t, self.fix_t, self.glass_t, self.broken, self.label, self.fall = \
            xy, w, sorted(hits), arm_t, nose_t, eye_t, fix_t, glass_t, broken, label, fall
        self.rng = random.Random(7)
        self.chips = [(self.rng.uniform(.44, .66), self.rng.uniform(.14, .48), self.rng.uniform(-1, 1), self.rng.uniform(.3, 1)) for _ in range(12)]
    def draw(self, lay, t, a):
        x, y = self.xy; w = self.w
        fixed = self.fix_t is not None and t >= self.fix_t
        arm = not ((self.broken or (self.arm_t is not None and t >= self.arm_t)) and not fixed)
        nose = not ((self.broken or (self.nose_t is not None and t >= self.nose_t)) and not fixed)
        eye = not ((self.broken or (self.eye_t is not None and t >= self.eye_t)) and not fixed)
        nh = sum(1 for h in self.hits if t >= h)
        cr = 0.0 if fixed else min(1.0, nh / 8.0 + (0.8 if self.broken else 0))
        if fixed and t < self.fix_t + 1.0: cr = 0.8 * (1 - (t - self.fix_t))
        im = pieta_img(w, arm, nose, cr, eye)
        sx = 0
        for h in self.hits:
            if 0 <= t - h < 0.18: sx = 6 * math.sin((t - h) * 90)
        x0, y0 = x - w / 2 + sx, y - w
        place(lay, im, (x0, y0), "la", a)
        d = ImageDraw.Draw(lay)
        for h in self.hits:   # schegge
            k = t - h
            if 0 <= k < 0.9:
                for (u, v, dx, sp) in self.chips[:6]:
                    px = x0 + u * w + dx * 160 * k * sp; py = y0 + v * w + (-120 * k + 420 * k * k) * sp
                    s = 6 + 4 * sp
                    d.polygon([(px, py - s), (px + s, py), (px, py + s * .7), (px - s * .8, py)], fill=MARBLE + (int(255 * a * (1 - k / 0.9)),))
        if self.fall and self.arm_t is not None and self.arm_t <= t < self.arm_t + 0.9 and not fixed:   # il braccio cade
            k = (t - self.arm_t) / 0.9
            px = x0 + .76 * w + 30 * k; py = y0 + .45 * w + (w * .5) * k * k
            seg = Image.new("RGBA", (int(w * .24), int(w * .1)), (0, 0, 0, 0)); ds = ImageDraw.Draw(seg)
            ds.rounded_rectangle([0, 0, seg.width - 1, seg.height - 1], seg.height // 2, fill=MARBLE + (255,))
            seg = seg.rotate(-200 * k, expand=True, resample=Image.BICUBIC)
            place(lay, seg, (px, py), "mm", a)
        if self.glass_t is not None and t >= self.glass_t:
            g = ease((t - self.glass_t) / 0.5)
            gx0, gy0, gx1, gy1 = x - w * .62, y - w * 1.12 + (1 - g) * 60, x + w * .62, y + 10
            gl = Image.new("RGBA", lay.size, (0, 0, 0, 0)); dg = ImageDraw.Draw(gl)
            dg.rectangle([gx0, gy0, gx1, gy1], fill=(170, 205, 225, int(60 * a * g)), outline=(225, 240, 250, int(230 * a * g)), width=6)
            for k in range(4):
                xx = gx0 + (gx1 - gx0) * (.12 + k * .2)
                dg.line([(xx, gy0 + 40), (xx + 90, gy0 + 160)], fill=(240, 250, 255, int(120 * a * g)), width=5)
            lay.alpha_composite(gl)
        if self.label:
            d.text((x + w / 2, y + 14), self.label, font=font(COURR, 20), fill=GREY + (int(200 * a),), anchor="ra")

class Swing(El):
    """martello che colpisce: pivot (mano), hits [t]"""
    def __init__(self, xy, size, t0, t1=None, hits=(), flip=1):
        super().__init__(t0, t1, 0.2); self.xy, self.size, self.hits, self.flip = xy, size, sorted(hits), flip
        self.im = fx.icon("hammer", size)
    def draw(self, lay, t, a):
        ang = 40
        for h in self.hits:
            k = t - h
            if -0.25 <= k < 0: ang = 40 + 60 * (1 + k / 0.25)
            elif 0 <= k < 0.12: ang = 100 - 80 * (k / 0.12)
            elif 0.12 <= k < 0.3: ang = 20 + 20 * ((k - .12) / .18)
        im = self.im.rotate(ang * self.flip, expand=True, resample=Image.BICUBIC)
        place(lay, im, self.xy, "mm", a)

class Cappella(El):
    """scenografia: la prima cappella a destra (schema non in scala): arco, pilastri, pavimento, balaustra, statua.
    Parametri statua passati a Pieta via pk; screen_t: parete del laboratorio; frags: (t, n) frammenti a terra"""
    def __init__(self, box, t0, t1=None, pk=None, screen_t=None, screen_off=None, frags=None, rail=True,
                 label="schema semplificato · non in scala", dim=0):
        super().__init__(t0, t1, 0.4)
        self.box, self.screen_t, self.screen_off, self.frags, self.rail, self.label, self.dim = box, screen_t, screen_off, frags, rail, label, dim
        x0, y0, x1, y1 = box; bw, bh = x1 - x0, y1 - y0
        self.fy = y0 + bh * .80
        pk = dict(pk or {}); pk.setdefault("label", None)
        self.sw = int(min(bw * .36, bh * .52))
        self.pieta = Pieta((x0 + bw / 2, y0 + bh * .70), self.sw, t0, None, **pk)
        self._b = None
        rng = random.Random(5)
        self.fr = [(rng.uniform(.3, .7), rng.uniform(.82, .97), rng.uniform(4, 11), rng.uniform(0, 6)) for _ in range(60)]
    def base(self):
        if self._b: return self._b
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0)
        im = Image.new("RGBA", (bw, bh), (70, 58, 50, 255)); d = ImageDraw.Draw(im)
        fy = int(bh * .80)
        # parete di fondo con nicchia ad arco
        d.rectangle([0, 0, bw, fy], fill=(150, 128, 104, 255))
        ax0, ax1 = bw * .26, bw * .74
        d.rectangle([ax0, bh * .26, ax1, fy], fill=(96, 80, 70, 255))
        d.pieslice([ax0, bh * .02, ax1, bh * .5], 180, 360, fill=(96, 80, 70, 255))
        d.arc([ax0 - 18, bh * .02 - 18, ax1 + 18, bh * .5 + 18], 180, 360, fill=(200, 176, 120, 255), width=12)
        for xx in (ax0 - 18, ax1 + 18): d.line([(xx, bh * .26), (xx, fy)], fill=(200, 176, 120, 255), width=12)
        # pilastri
        for px in (bw * .04, bw * .86):
            d.rectangle([px, 0, px + bw * .10, fy], fill=(176, 156, 132, 255))
            for k in range(3): d.line([(px + bw * (.025 + k * .025), 20), (px + bw * (.025 + k * .025), fy - 20)], fill=(150, 132, 110, 255), width=4)
        # pavimento a scacchi in prospettiva
        d.rectangle([0, fy, bw, bh], fill=(120, 100, 86, 255))
        for k in range(14):
            xa = bw * k / 13; d.line([(xa, fy), (bw / 2 + (xa - bw / 2) * 1.6, bh)], fill=(98, 82, 70, 255), width=3)
        for k in range(1, 4): yy = fy + (bh - fy) * (k / 4) ** 1.3; d.line([(0, yy), (bw, yy)], fill=(98, 82, 70, 255), width=3)
        self._b = im
        return im
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0)
        im = self.base().copy()
        place(lay, set_alpha(im, a), (x0, y0), "la")
        self.pieta.draw(lay, t, a)
        d = ImageDraw.Draw(lay)
        if self.frags is not None and t >= self.frags[0]:
            n = int(self.frags[1])
            for k, (u, v, s, r) in enumerate(self.fr[:n]):
                px, py = x0 + u * bw, y0 + v * bh
                if py < self.fy + 4: continue
                d.polygon([(px + s * math.cos(r + j * 2.1), py + s * .6 * math.sin(r + j * 2.1)) for j in range(3)], fill=MARBLE + (int(255 * a),))
        if self.rail:
            ry = y0 + bh * .86; al = int(255 * a)
            d.rectangle([x0 + bw * .12, ry - 70, x1 - bw * .12, ry - 56], fill=(206, 196, 180, al))
            for k in range(23):
                xx = x0 + bw * .13 + k * (bw * .74 / 22)
                d.rounded_rectangle([xx - 7, ry - 56, xx + 7, ry], 6, fill=(196, 186, 170, al))
            d.rectangle([x0 + bw * .12, ry, x1 - bw * .12, ry + 12], fill=(186, 176, 160, al))
        if self.screen_t is not None and t >= self.screen_t and not (self.screen_off is not None and t >= self.screen_off):
            k = ease((t - self.screen_t) / 0.6)
            sw = self.sw * 1.25; cx = x0 + bw / 2; top = y0 + bh * .70 - self.sw * 1.08
            sx0 = cx - sw / 2; sx1 = cx - sw / 2 + sw * k
            d.rectangle([sx0, top, sx1, self.fy + 6], fill=(150, 108, 66, int(250 * a)), outline=(100, 70, 40, int(255 * a)), width=5)
            for j in range(1, 8):
                xx = sx0 + sw * j / 8
                if xx < sx1: d.line([(xx, top), (xx, self.fy)], fill=(120, 84, 50, int(255 * a)), width=3)
        if self.dim: lay.alpha_composite(Image.new("RGBA", lay.size, (8, 8, 14, int(self.dim * a))))
        if self.label:
            d.text((x1, y1 + 8), self.label, font=font(COURR, 22), fill=GREY + (int(200 * a),), anchor="ra")

class Frags(El):
    """circa cento frammenti: sparsi (t0) e poi catalogati in griglia (sort_t), con contatore"""
    def __init__(self, box, t0, t1=None, n=100, sort_t=None, sort_d=3.0, counter=True, seed=9):
        super().__init__(t0, t1, 0.3); self.box, self.n, self.sort_t, self.sort_d, self.counter = box, n, sort_t, sort_d, counter
        rng = random.Random(seed); x0, y0, x1, y1 = box
        self.p = []
        cols = 20; rows = math.ceil(n / cols)
        for i in range(n):
            r, c = divmod(i, cols)
            gx = x0 + (c + .5) * (x1 - x0) / cols; gy = y0 + 60 + (r + .5) * (y1 - y0 - 80) / rows
            self.p.append((rng.uniform(x0, x1), rng.uniform(y0 + 40, y1), gx, gy, rng.uniform(5, 16), rng.uniform(0, 6), rng.randint(3, 5)))
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); al = int(255 * a); done = 0
        for i, (sx, sy, gx, gy, s, r, nv) in enumerate(self.p):
            u = 0.0
            if self.sort_t is not None:
                ti = self.sort_t + self.sort_d * i / self.n
                u = ease_io(min(1, max(0, (t - ti) / 0.5)))
                if u >= 1: done += 1
            x = lerp(sx, gx, u); y = lerp(sy, gy, u)
            pts = [(x + s * math.cos(r + j * 2 * math.pi / nv), y + s * .75 * math.sin(r + j * 2 * math.pi / nv)) for j in range(nv)]
            d.polygon(pts, fill=MARBLE + (al,), outline=MARBLE_DD + (al,))
            if u >= 1:
                d.text((x, y + s + 6), str(i + 1), font=font(COURR, 12), fill=GOLD + (al,), anchor="ma")
        if self.counter and self.sort_t is not None and t >= self.sort_t:
            x0, y0, x1, y1 = self.box
            d.text(((x0 + x1) / 2, y0), "FRAMMENTI CLASSIFICATI: %d" % done, font=font(OSW, 40, 600), fill=WHITE + (al,), anchor="ma")

def signature_img(w=900):
    h = int(w * .30); im = paper(w, h, (226, 220, 206), 13, 0.3); d = ImageDraw.Draw(im)
    d.rounded_rectangle([20, h * .30, w - 20, h * .66], 18, fill=(214, 208, 194, 255), outline=(170, 160, 146, 255), width=3)
    d.text((w / 2, h * .48), "MICHAEL·ANGELVS·BONAROTVS·FLORENT·FACIEBA[T]", font=font(TYPE, int(w * .036)), fill=(80, 72, 62, 255), anchor="mm")
    d.text((w / 2, h * .16), "LA FIRMA SULLA FASCIA", font=font(OSW, int(w * .04), 600), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .80), "grafia semplificata · le trascrizioni variano tra le fonti", font=font(COURR, int(w * .024)), fill=(110, 96, 80, 255), anchor="mm")
    recon_label(d, w, h)
    return im

def contract_img(w=560):
    return doc_typed(w, int(w * 1.18), "CONTRATTO · ROMA, AGOSTO 1498",
                     ["Committente:", "card. Jean de Bilhères,", "ambasciatore del re di Francia", "",
                      "Scultore:", "Michelangelo Buonarroti,", "fiorentino, anni 23", "",
                      "Opera: una Pietà di marmo"], footer="schema del contenuto", seed=21, size=30)

def letter_img(w=520):
    return doc_typed(w, int(w * 1.0), "A SUA SANTITÀ PAOLO VI",
                     ["Roma, 1971-1972", "", "...chiedo di essere", "ricevuto in udienza...", "", "(testo non originale)"],
                     footer=None, seed=33, size=30)

def order_img(w=560):
    return doc_typed(w, int(w * 1.05), "ROMA · GENNAIO 1973",
                     ["Il giudice dispone", "il ricovero in", "ospedale psichiatrico", "per almeno due anni.", "",
                      "Nessun processo."], footer="schema del contenuto", seed=44, size=32)

def cover_folder(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 28, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 016", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "LA PIETÀ E IL MARTELLO", font=font(SERIF, int(w * .075)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "ROMA 1972 · 1973", font=font(TYPE, int(w * .045)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im

# ------------------------------------------------------------------ icone del caso
_pi = {}
def ppic(name, size):
    k = (name, size)
    if k in _pi: return _pi[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); w = max(2, S // 22)
    if name == "pieta":
        p = pieta_img(int(S * .9)); im.alpha_composite(p, (int(S * .05), int(S * .05)))
    elif name == "pieta_b":
        p = pieta_img(int(S * .9), arm=False, nose=False, cracks=.8); im.alpha_composite(p, (int(S * .05), int(S * .05)))
    elif name == "eye":
        d.ellipse([P(.06, .28), P(.94, .72)], fill=(240, 236, 226, 255), outline=(60, 50, 40, 255), width=w)
        d.ellipse([P(.36, .32), P(.64, .68)], fill=(60, 90, 120, 255)); d.ellipse([P(.45, .42), P(.55, .58)], fill=(10, 10, 10, 255))
    elif name == "glue":     # tubetto di colla + polvere di marmo
        d.rounded_rectangle([P(.08, .30), P(.58, .56)], S // 20, fill=(200, 200, 206, 255), outline=(120, 120, 126, 255), width=w)
        d.polygon([P(.58, .36), P(.72, .40), P(.72, .46), P(.58, .50)], fill=(160, 160, 166, 255))
        d.ellipse([P(.50, .62), P(.94, .92)], fill=(236, 232, 222, 255))
        for k in range(18):
            rr = random.Random(k); x = rr.uniform(.52, .92); y = rr.uniform(.55, .66)
            d.ellipse([P(x, y), P(x + .02, y + .02)], fill=(236, 232, 222, 255))
    elif name == "mould":    # calco
        d.rounded_rectangle([P(.12, .12), P(.88, .88)], S // 12, fill=(214, 206, 186, 255), outline=(150, 140, 120, 255), width=w)
        d.ellipse([P(.32, .26), P(.68, .70)], fill=(176, 166, 146, 255))
        d.polygon([P(.50, .40), P(.46, .54), P(.54, .54)], fill=(150, 140, 120, 255))
    elif name == "letter_m":
        d.ellipse([P(.06, .06), P(.94, .94)], fill=(226, 220, 206, 255), outline=GOLD + (255,), width=w * 2)
        d.text(P(.5, .52), "M", font=font(SERIF, int(S * .55)), fill=(110, 96, 80, 255), anchor="mm")
    elif name == "fire":     # vigile del fuoco (elmetto)
        d.chord([P(.12, .20), P(.88, .90)], 180, 360, fill=(200, 60, 40, 255)); d.rectangle([P(.04, .54), P(.96, .62)], fill=(170, 40, 30, 255))
        d.ellipse([P(.42, .26), P(.58, .42)], fill=GOLD + (255,))
    elif name == "chisel_s":  # scultore: scalpello e mazzuolo
        d.line([P(.18, .82), P(.58, .42)], fill=(170, 170, 176, 255), width=S // 12); d.polygon([P(.58, .42), P(.70, .30), P(.64, .48)], fill=(200, 200, 206, 255))
        d.ellipse([P(.56, .10), P(.90, .38)], fill=(130, 90, 56, 255))
    elif name == "kangaroo":  # cartello stradale generico "Australia"
        d.polygon([P(.5, .04), P(.96, .5), P(.5, .96), P(.04, .5)], fill=(236, 190, 40, 255), outline=(30, 30, 30, 255))
        d.ellipse([P(.36, .38), P(.62, .62)], fill=(30, 30, 30, 255)); d.ellipse([P(.56, .28), P(.68, .40)], fill=(30, 30, 30, 255))
        d.line([P(.40, .60), P(.24, .74)], fill=(30, 30, 30, 255), width=w * 2); d.line([P(.52, .62), P(.60, .76)], fill=(30, 30, 30, 255), width=w * 2)
    elif name == "soap":
        d.rounded_rectangle([P(.12, .34), P(.88, .78)], S // 8, fill=(170, 210, 220, 255), outline=(110, 150, 160, 255), width=w)
        for (x, y, r) in ((.3, .26, .07), (.46, .18, .05), (.6, .24, .06)): d.ellipse([P(x - r, y - r), P(x + r, y + r)], outline=(200, 230, 240, 255), width=w)
    elif name == "geo":       # martello da geologo con sasso
        d.ellipse([P(.06, .62), P(.46, .92)], fill=(120, 110, 100, 255))
        hm = fx.icon("hammer", int(S * .7)); im.alpha_composite(hm, (int(S * .3), int(S * .02)))
    elif name == "dove":      # Pentecoste: colomba stilizzata
        d.ellipse([P(.22, .38), P(.70, .64)], fill=(240, 240, 236, 255)); d.ellipse([P(.62, .30), P(.82, .48)], fill=(240, 240, 236, 255))
        d.polygon([P(.80, .38), P(.94, .40), P(.80, .44)], fill=GOLD + (255,))
        d.polygon([P(.30, .44), P(.44, .10), P(.58, .44)], fill=(226, 226, 222, 255)); d.polygon([P(.24, .52), P(.04, .62), P(.24, .60)], fill=(226, 226, 222, 255))
    elif name == "basilica":
        d.ellipse([P(.30, .10), P(.70, .50)], fill=(200, 190, 170, 255)); d.rectangle([P(.46, .02), P(.54, .12)], fill=(200, 190, 170, 255))
        d.rectangle([P(.06, .44), P(.94, .90)], fill=(214, 204, 184, 255))
        for k in range(8): d.rectangle([P(.10 + k * .105, .50), P(.15 + k * .105, .86)], fill=(236, 228, 210, 255))
        d.rectangle([P(.02, .88), P(.98, .96)], fill=(190, 180, 160, 255))
    elif name == "debate":    # due fumetti
        d.ellipse([P(.02, .10), P(.56, .52)], fill=(236, 230, 216, 255)); d.ellipse([P(.44, .44), P(.98, .86)], fill=(220, 70, 60, 255))
        d.text(P(.29, .31), "?", font=font(OSW, int(S * .26), 700), fill=INK + (255,), anchor="mm")
        d.text(P(.71, .65), "!", font=font(OSW, int(S * .26), 700), fill=WHITE + (255,), anchor="mm")
    elif name == "puzzle":
        for (x, y, c) in ((.08, .08, (226, 220, 206)), (.52, .08, (200, 194, 180)), (.08, .52, (200, 194, 180)), (.52, .52, (226, 220, 206))):
            d.rectangle([P(x, y), P(x + .4, y + .4)], fill=c + (255,), outline=(120, 110, 96, 255), width=w)
        d.ellipse([P(.44, .20), P(.60, .36)], fill=(226, 220, 206, 255)); d.ellipse([P(.20, .44), P(.36, .60)], fill=(226, 220, 206, 255))
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _pi[k] = im
    return im

_prev_pt = fx.icon
def _pt_icon(name, size, color=None):
    if isinstance(name, str):
        m = ppic(name, size)
        if m is not None: return m
    return _prev_pt(name, size, color)
fx.icon = _pt_icon
pon.icon = _pt_icon
fi.PLACES.update({"Carrara": (10.10, 44.08)})

# ------------------------------------------------------------------ mappa del mondo larga (fino all'Australia)
pon.WB.update(lon0=-30.0, lon1=160.0, lat0=-46.0, lat1=62.0, K=14.0)
pon.WPAD = 700
_src = inspect.getsource(pon.world_base).replace("world_base.png", "world_base_pt.png")
exec(_src, pon.__dict__)
_src = inspect.getsource(pon._world_raw).replace("range(-100, 51, 10)", "range(-30, 161, 10)").replace("range(-30, 61, 10)", "range(-40, 61, 10)") \
    .replace('"Italy": (96, 78, 56)', '"Italy": (96, 78, 56), "Hungary": (96, 78, 56), "Australia": (96, 78, 56)')
exec(_src, pon.__dict__)
pon._wb = None
pon.WPL.update({"Ungheria": (19.0, 47.6), "Sydney": (151.2, -33.87), "Roma": (12.5, 41.9), "NewYork": (-74.0, 40.7)})
WorldMap = pon.WorldMap
