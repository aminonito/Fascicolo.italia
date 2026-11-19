# Elementi grafici del caso 015 (il furto dei 17 dipinti al Museo di Castelvecchio, Verona, 19/11/2015 -
# ritrovamento in Ucraina, maggio 2016): la galleria con 17 quadri (sagome stilizzate e generiche, NON le opere),
# il castello visto da fuori (schema non in scala), icone del caso. Tutto disegnato da codice.
import math, random, os, sys
HERE = CVDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "013-van-gogh"))
from vg import *
import vg, fi, fx
from fx import *

fi.PLACES.update({"Verona": (10.99, 45.44), "Chisinau": (28.86, 47.01), "Odessa": (30.73, 46.48),
                  "Turunchuk": (29.95, 46.55), "Kyiv": (30.52, 50.45), "Venezia": (12.33, 45.44), "Roma": (12.50, 41.90)})
NIGHT = (8, 10, 24)
_cc = {}

PAL = [((60, 46, 34), (150, 110, 70)), ((40, 50, 60), (170, 150, 110)), ((70, 40, 30), (200, 160, 90)),
       ((30, 40, 34), (120, 140, 96)), ((54, 40, 50), (190, 150, 120))]
def pic(k, w, h):
    """dipinto generico n. k: sagoma stilizzata, NON riproduce alcuna opera"""
    key = ("p", k, w, h)
    if key in _cc: return _cc[key]
    rng = random.Random(k * 7 + 1)
    bgc, fg = PAL[k % len(PAL)]
    b = max(4, int(min(w, h) * .08))
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], fill=(150, 112, 56, 255), outline=(96, 70, 34, 255), width=2)
    iw, ih = w - 2 * b, h - 2 * b
    inner = Image.new("RGBA", (iw, ih), bgc + (255,)); di = ImageDraw.Draw(inner)
    kind = k % 3
    if kind == 0:     # ritratto: sagoma
        silhouette(di, iw / 2, ih * 1.02, iw * .7, tuple(max(0, c - 20) for c in bgc))
        di.ellipse([iw * .36, ih * .2, iw * .64, ih * .5], fill=fg + (255,))
    elif kind == 1:   # paesaggio
        di.rectangle([0, ih * .55, iw, ih], fill=tuple(int(c * .7) for c in fg) + (255,))
        di.ellipse([iw * .1, ih * .3, iw * .45, ih * .7], fill=(50, 70, 46, 255))
        di.rectangle([0, 0, iw, ih * .3], fill=(110, 130, 150, 255))
    else:             # scena con figure
        for j in range(3):
            x = iw * (.25 + .25 * j) + rng.uniform(-6, 6)
            di.rectangle([x - iw * .05, ih * .45, x + iw * .05, ih * .9], fill=fg + (255,))
            di.ellipse([x - iw * .05, ih * .32, x + iw * .05, ih * .44], fill=fg + (255,))
    im.alpha_composite(inner, (b, b))
    _cc[key] = im
    return im

class Galleria(El):
    """parete del museo con 17 quadri (schema non in scala). gone: t (spariscono a cascata) ; back: t ; night ; torch ; hl: t"""
    def __init__(self, box, t0, t1=None, gone=None, back=None, night=False, torch=None, hl=None, step=0.12,
                 label="sagome stilizzate · schema non in scala", n=17):
        super().__init__(t0, t1, 0.4)
        self.box, self.gone, self.back, self.night, self.torch, self.hl, self.step, self.label, self.n = box, gone, back, night, torch, hl, step, label, n
        self._b = None
    def slots(self, bw, bh):
        rows = [6, 6, 5]; out = []; k = 0
        for r, cnt in enumerate(rows):
            for c in range(cnt):
                cx = bw * (c + .5 + (.5 if cnt == 5 else 0)) / 6.0 if cnt == 6 else bw * (c + 1) / 6.0
                cy = bh * (.17 + .25 * r)
                h = int(bh * (.17 if (k % 4) else .2)); w = int(h * (.75 if k % 3 == 0 else 1.25))
                out.append((int(cx - w / 2), int(cy - h / 2), w, h)); k += 1
        return out[:self.n]
    def base(self):
        if self._b: return self._b
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0)
        im = Image.new("RGBA", (bw, bh), (226, 220, 206, 255)); d = ImageDraw.Draw(im)
        fy = int(bh * .86)
        d.rectangle([0, fy, bw, bh], fill=(120, 104, 90, 255))
        for k in range(20): d.line([(k * bw / 19, fy), (bw / 2 + (k * bw / 19 - bw / 2) * 1.4, bh)], fill=(100, 88, 76, 255), width=2)
        for k in range(1, 4):  # archi a sesto acuto (schema)
            x = bw * k / 4; d.line([(x, 0), (x, fy)], fill=(206, 198, 182, 255), width=6)
        d.line([(0, fy - 4), (bw, fy - 4)], fill=(170, 160, 146, 255), width=8)
        self._b = (im, fy)
        return self._b
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0)
        base, fy = self.base(); im = base.copy(); d = ImageDraw.Draw(im)
        sl = self.slots(bw, bh); gone_n = 0
        for k, (px, py, w, h) in enumerate(sl):
            pc = pic(k, w, h)
            g = None if self.gone is None else self.gone + k * self.step
            back = self.back is not None and t >= self.back + k * self.step * .5
            if g is not None and t >= g and not back:
                gone_n += 1
                u = min(1.0, (t - g) / 0.4)
                if u < 1: im.alpha_composite(set_alpha(pc, 1 - u), (px, int(py - 20 * u)))
                d.rectangle([px, py, px + w, py + h], outline=(150, 144, 132, 255), width=3)
                for hx in (px + w * .2, px + w * .8): d.ellipse([hx - 5, py - 9, hx + 5, py + 1], fill=(120, 116, 110, 255))
            else:
                if self.back is not None and back:
                    u = min(1.0, (t - self.back - k * self.step * .5) / 0.5); im.alpha_composite(set_alpha(pc, u), (px, py))
                else: im.alpha_composite(pc, (px, py))
            if self.hl is not None and t >= self.hl and k < 4:
                d.rectangle([px - 8, py - 8, px + w + 8, py + h + 8], outline=RED + (255,), width=6)
        if self.night:
            im.alpha_composite(Image.new("RGBA", (bw, bh), NIGHT + (190,)))
            if self.torch is not None and t >= self.torch:
                cx = bw * (.5 + .35 * math.sin((t - self.torch) * 1.0)); cy = bh * (.45 + .15 * math.cos((t - self.torch) * 1.6))
                m = Image.new("L", (bw, bh), 0); ImageDraw.Draw(m).ellipse([cx - 180, cy - 180, cx + 180, cy + 180], fill=170)
                m = m.filter(ImageFilter.GaussianBlur(40))
                lit = base.copy()
                for k, (px, py, w, h) in enumerate(sl):
                    g = None if self.gone is None else self.gone + k * self.step
                    if not (g is not None and t >= g): lit.alpha_composite(pic(k, w, h), (px, py))
                im = Image.composite(lit, im, m)
        im = set_alpha(im, a)
        place(lay, im, (x0, y0), "la")
        if self.label:
            ImageDraw.Draw(lay).text((x1, y1 + 8), self.label, font=font(COURR, 22), fill=GREY + (int(200 * a),), anchor="ra")

class Castello(El):
    """il castello visto da fuori: mura merlate, torre, porta; luce accesa/spenta; schema non in scala"""
    def __init__(self, box, t0, t1=None, night=False, door_t=None, label="schema semplificato · non in scala"):
        super().__init__(t0, t1, 0.4); self.box, self.night, self.door_t, self.label = box, night, door_t, label
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0)
        im = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        sky = (16, 20, 44) if self.night else (120, 150, 190)
        d.rectangle([0, 0, bw, bh], fill=sky + (255,))
        if self.night:
            for k in range(30):
                r = random.Random(k); d.point((r.uniform(0, bw), r.uniform(0, bh * .4)), fill=(220, 220, 240, 255))
        gy = int(bh * .88)
        brick = (150, 70, 50); dark = (110, 50, 36)
        wy = int(bh * .40)
        d.rectangle([0, wy, bw, gy], fill=brick + (255,))
        mw = bw / 22   # merli a coda di rondine
        for k in range(22):
            mx = k * mw
            d.polygon([(mx + mw * .15, wy), (mx + mw * .15, wy - mw * .9), (mx + mw * .5, wy - mw * .5),
                       (mx + mw * .85, wy - mw * .9), (mx + mw * .85, wy)], fill=brick + (255,))
        tx0, tx1 = bw * .62, bw * .80; ty = int(bh * .08)
        d.rectangle([tx0, ty, tx1, gy], fill=dark + (255,))
        tw = (tx1 - tx0) / 4
        for k in range(4):
            mx = tx0 + k * tw
            d.polygon([(mx + tw * .15, ty), (mx + tw * .15, ty - tw * .8), (mx + tw * .5, ty - tw * .45), (mx + tw * .85, ty - tw * .8), (mx + tw * .85, ty)], fill=dark + (255,))
        for yy in range(wy + 20, gy, 26): d.line([(0, yy), (bw, yy)], fill=(130, 60, 42, 255), width=1)
        lit = (250, 220, 120) if self.night else (60, 50, 50)
        for k in range(5):
            wx = bw * (.08 + .1 * k); d.rounded_rectangle([wx, wy + 60, wx + 34, wy + 120], 14, fill=lit + (255,))
        dx = bw * .36; dw = 120; dh = 170
        op = self.door_t is not None and t >= self.door_t
        d.rounded_rectangle([dx, gy - dh, dx + dw, gy + 6], 50, fill=((250, 220, 120) if op else (60, 40, 26)) + (255,), outline=(60, 30, 20, 255), width=6)
        d.rectangle([0, gy, bw, bh], fill=(80, 76, 70, 255))
        if self.night: im.alpha_composite(Image.new("RGBA", (bw, bh), NIGHT + (70,)))
        im = set_alpha(im, a); place(lay, im, (x0, y0), "la")
        if self.label: ImageDraw.Draw(lay).text((x1, y1 + 8), self.label, font=font(COURR, 22), fill=GREY + (int(200 * a),), anchor="ra")

def cover_folder(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 28, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 015", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "I 17 QUADRI DI VERONA", font=font(SERIF, int(w * .08)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "VERONA 2015 · UCRAINA 2016", font=font(TYPE, int(w * .045)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im

# mappa estesa a est (Moldavia e Ucraina): stessa proiezione, cache separata
import inspect
fi.MAPB["lon1"] = 36.0
_src = inspect.getsource(fi.map_base).replace("map_base.png", "map_base_east.png").replace("range(-6, 22, 2)", "range(-6, 38, 2)")
exec(_src, fi.__dict__)
fi._base = None

# icone dei casi 002 (anversa) e 004 (klimt) e 003 (ponzi) non presenti nella catena
for _d in ("002-anversa", "004-klimt", "003-ponzi"):
    sys.path.insert(0, os.path.join(CVDIR, "..", _d))
import anv, klm, pon
_prev_cv = fx.icon
def _cv_icon(name, size, color=None):
    im = _prev_cv(name, size, color)
    if isinstance(name, str) and im is not None and im.getbbox() is None:
        for f in (lambda: anv.aic(name, size, color), lambda: klm.kpic(name, size), lambda: pon.pic(name, size, color)):
            try:
                m = f()
                if m is not None and m.getbbox() is not None: return m
            except Exception: pass
    return im
fx.icon = _cv_icon
