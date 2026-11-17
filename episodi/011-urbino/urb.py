# Elementi grafici del caso 011 (il furto di Urbino, 1975-1976): il Palazzo Ducale con l'impalcatura
# (scenografia esterna, schema non in scala), la sala con i tre dipinti (sagome stilizzate, non le opere),
# icone del caso. Tutto disegnato da codice: nessuna foto reale, nessuna riproduzione delle opere.
import math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "010-banca-romana"))
sys.path.insert(0, os.path.join(HERE, "..", "009-modigliani"))
sys.path.insert(0, os.path.join(HERE, "..", "003-ponzi"))
for d_ in ("008-caravaggio", "007-osoppo", "006-tortora", "005-majorana"):
    sys.path.insert(0, os.path.join(HERE, "..", d_))
from fi import *
import fi
import fx
from fx import *
import rom                         # catena di icone già pronte (rom -> mod -> car -> osp -> tor -> maj)
from mod import label_card

fi.PLACES.update({"Urbino": (12.64, 43.73), "Pesaro": (12.91, 43.91), "Rimini": (12.57, 44.06),
                  "Bologna": (11.34, 44.49), "Locarno": (8.80, 46.17), "Sassocorvaro": (12.50, 43.78),
                  "Roma": (12.50, 41.90)})

BRICK = (176, 120, 84)
BRICK2 = (150, 100, 70)
STONE = (222, 210, 186)
NIGHT = (8, 10, 24)

# ---------------------------------------------------------------- i tre dipinti (sagome stilizzate)
_pc = {}
def art(kind, w, h):
    """sagome stilizzate e generiche: NON riproducono le opere"""
    k = (kind, w, h)
    if k in _pc: return _pc[k]
    im = Image.new("RGBA", (w, h), (0, 0, 0, 255)); d = ImageDraw.Draw(im)
    if kind == "flag":       # architettura in prospettiva + piccole figure
        d.rectangle([0, 0, w, h], fill=(200, 186, 160, 255))
        d.rectangle([0, 0, w, h * .18], fill=(150, 170, 196, 255))
        vx, vy = w * .36, h * .62
        for k_ in range(9):
            x = k_ * w / 8; d.line([(vx + (x - vx) * .2, vy), (x, h)], fill=(150, 130, 110, 255), width=2)
        for k_ in range(1, 5):
            y = vy + (h - vy) * (k_ / 5) ** 1.5; d.line([(0, y), (w * .62, y)], fill=(150, 130, 110, 255), width=2)
        d.rectangle([w * .06, h * .16, w * .60, h * .22], fill=(232, 224, 206, 255))
        for x in (w * .08, w * .32, w * .56):
            d.rectangle([x, h * .22, x + w * .035, h * .78], fill=(240, 234, 220, 255))
        d.line([(w * .62, 0), (w * .62, h)], fill=(120, 100, 80, 255), width=3)
        for j, (x, c) in enumerate([(.72, (120, 60, 50)), (.82, (60, 70, 110)), (.92, (150, 110, 60))]):
            cx = w * x; d.rectangle([cx - w * .035, h * .42, cx + w * .035, h * .88], fill=c + (255,))
            d.ellipse([cx - w * .025, h * .34, cx + w * .025, h * .42], fill=(220, 180, 150, 255))
        for x in (.22, .36):
            cx = w * x; d.rectangle([cx - w * .018, h * .55, cx + w * .018, h * .72], fill=(110, 90, 80, 255))
            d.ellipse([cx - w * .014, h * .51, cx + w * .014, h * .56], fill=(220, 180, 150, 255))
    elif kind == "madonna":  # figura centrale con manto, due figure ai lati
        d.rectangle([0, 0, w, h], fill=(120, 116, 110, 255))
        d.rectangle([w * .70, h * .10, w * .92, h * .40], fill=(200, 196, 176, 255))
        for x in (.18, .82):
            cx = w * x; d.polygon([(cx - w * .12, h), (cx, h * .26), (cx + w * .12, h)], fill=(150, 146, 140, 255))
            d.ellipse([cx - w * .06, h * .14, cx + w * .06, h * .28], fill=(220, 190, 160, 255))
        cx = w * .5; d.polygon([(cx - w * .26, h), (cx, h * .26), (cx + w * .26, h)], fill=(40, 60, 110, 255))
        d.ellipse([cx - w * .08, h * .12, cx + w * .08, h * .30], fill=(226, 196, 166, 255))
        d.ellipse([cx - w * .07, h * .52, cx + w * .07, h * .66], fill=(230, 200, 170, 255))
    else:                    # "muta": ritratto di donna a mezza figura, sfondo scuro
        d.rectangle([0, 0, w, h], fill=(40, 52, 40, 255))
        cx = w * .5
        d.polygon([(w * .10, h), (w * .22, h * .52), (cx, h * .44), (w * .78, h * .52), (w * .90, h)], fill=(30, 26, 24, 255))
        d.rectangle([w * .40, h * .44, w * .60, h * .52], fill=(220, 196, 170, 255))
        d.ellipse([cx - w * .15, h * .14, cx + w * .15, h * .48], fill=(226, 200, 172, 255))
        d.chord([cx - w * .17, h * .10, cx + w * .17, h * .40], 180, 360, fill=(90, 60, 40, 255))
        d.ellipse([w * .36, h * .78, w * .64, h * .90], fill=(220, 196, 170, 255))
    _pc[k] = im
    return im

ART = [("flag", 81.5, 58.4, "PIERO DELLA FRANCESCA\nFLAGELLAZIONE"), ("madonna", 53.5, 61, "PIERO DELLA FRANCESCA\nMADONNA DI SENIGALLIA"),
       ("muta", 48, 64, "RAFFAELLO\nLA MUTA")]

def framed(kind, hpx):
    k = ("fr", kind, hpx)
    if k in _pc: return _pc[k]
    wcm, hcm = [(a[1], a[2]) for a in ART if a[0] == kind][0]
    ph = hpx; pw = int(ph * wcm / hcm); b = max(8, ph // 12)
    im = Image.new("RGBA", (pw + 2 * b, ph + 2 * b), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, pw + 2 * b - 1, ph + 2 * b - 1], fill=(176, 136, 70, 255), outline=(110, 80, 36, 255), width=3)
    d.rectangle([b // 2, b // 2, pw + b + b // 2, ph + b + b // 2], outline=(220, 186, 110, 255), width=2)
    im.alpha_composite(art(kind, pw, ph), (b, b))
    _pc[k] = im
    return im

# ---------------------------------------------------------------- la sala (scenografia interna)
class Sala(El):
    """sala del palazzo con i tre dipinti (schema non in scala).
    gone: {indice: t} il dipinto sparisce; back: t tornano tutti; night; torch: t inizio torcia;
    window_t: si apre la finestra sul giardino pensile; hl: (indice, t) evidenzia"""
    def __init__(self, box, t0, t1=None, gone=None, back=None, night=False, torch=None, window_t=None, hl=None,
                 label="schema semplificato · non in scala", captions=True):
        super().__init__(t0, t1, 0.4)
        self.box, self.gone, self.back, self.night, self.torch, self.window_t, self.hl = box, gone or {}, back, night, torch, window_t, hl
        self.label, self.captions = label, captions; self._b = None
    def slots(self, bw, bh):
        fy = int(bh * .80); ph = int(bh * .30); out = []
        for k, x in enumerate((.22, .50, .78)):
            fr = framed(ART[k][0], ph); out.append((int(bw * x - fr.width / 2), int(bh * .44 - fr.height / 2), fr))
        return out, fy
    def base(self):
        if self._b: return self._b
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0)
        im = Image.new("RGBA", (bw, bh), (226, 218, 198, 255)); d = ImageDraw.Draw(im)
        fy = int(bh * .80)
        d.rectangle([0, fy, bw, bh], fill=(160, 120, 86, 255))
        for k in range(16):
            x = k * bw / 15; d.line([(bw / 2 + (x - bw / 2) * .6, fy), (x, bh)], fill=(130, 96, 68, 255), width=2)
        d.rectangle([0, 0, bw, int(bh * .08)], fill=(196, 184, 160, 255))
        for k in range(30):
            x = k * bw / 29; d.rectangle([x - 6, bh * .03, x + 6, bh * .06], fill=(176, 160, 130, 255))
        d.line([(0, fy - 6), (bw, fy - 6)], fill=(176, 160, 130, 255), width=10)
        # porta di pietra a sinistra e finestra a destra (verso il giardino pensile)
        d.rectangle([bw * .02, bh * .30, bw * .08, fy], fill=(120, 96, 70, 255), outline=(200, 186, 160, 255), width=8)
        self._b = (im, fy)
        return self._b
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0); al = int(255 * a)
        base, fy = self.base(); im = base.copy(); d = ImageDraw.Draw(im)
        wx0, wx1 = bw * .91, bw * .985
        op = self.window_t is not None and t >= self.window_t
        d.rectangle([wx0, bh * .22, wx1, bh * .62], fill=(20, 26, 50, 255) if op else (90, 110, 140, 255), outline=(200, 186, 160, 255), width=6)
        if not op: d.line([((wx0 + wx1) / 2, bh * .22), ((wx0 + wx1) / 2, bh * .62)], fill=(200, 186, 160, 255), width=4)
        sl, _ = self.slots(bw, bh)
        for k, (px, py, fr) in enumerate(sl):
            g = self.gone.get(k); back = self.back is not None and t >= self.back
            if g is not None and t >= g and not back:
                u = min(1.0, (t - g) / 0.5)
                if u < 1: im.alpha_composite(set_alpha(fr, 1 - u), (px, int(py - 30 * u)))
                d.rectangle([px + 4, py + 4, px + fr.width - 4, py + fr.height - 4], outline=(196, 182, 150, 255), width=4)
                d.rectangle([px + 10, py + 10, px + fr.width - 10, py + fr.height - 10], fill=(236, 230, 212, 255))
                d.line([(px + fr.width / 2, py - 40), (px + fr.width / 2 - 30, py), ], fill=(120, 110, 100, 255), width=2)
            else:
                if back:
                    u = min(1.0, (t - self.back) / 0.6); im.alpha_composite(set_alpha(fr, u), (px, py))
                else: im.alpha_composite(fr, (px, py))
            if self.captions:
                lab = ART[k][3]; f = font(OSW, max(16, bh // 34), 600)
                d.multiline_text((px + fr.width / 2, py + fr.height + 14), lab, font=f, fill=(70, 56, 44, 255), anchor="ma", align="center", spacing=2)
            if self.hl and self.hl[0] == k and t >= self.hl[1]:
                d.rectangle([px - 12, py - 12, px + fr.width + 12, py + fr.height + 12], outline=RED + (255,), width=8)
        if self.night:
            im.alpha_composite(Image.new("RGBA", (bw, bh), NIGHT + (205,)))
            if self.torch is not None and t >= self.torch:
                cx = bw * (.5 + .36 * math.sin((t - self.torch) * 1.1)); cy = bh * (.45 + .1 * math.cos((t - self.torch) * 1.7))
                m = Image.new("L", (bw, bh), 0); ImageDraw.Draw(m).ellipse([cx - 190, cy - 190, cx + 190, cy + 190], fill=170)
                m = m.filter(ImageFilter.GaussianBlur(45))
                lit = base.copy(); dl = ImageDraw.Draw(lit)
                for k, (px, py, fr) in enumerate(sl):
                    g = self.gone.get(k)
                    if g is not None and t >= g:
                        dl.rectangle([px + 10, py + 10, px + fr.width - 10, py + fr.height - 10], fill=(236, 230, 212, 255), outline=(196, 182, 150, 255), width=4)
                    else: lit.alpha_composite(fr, (px, py))
                im = Image.composite(lit, im, m); d = ImageDraw.Draw(im)
        if self.label:
            col = (60, 50, 40, 230) if not self.night else (200, 190, 170, 230)
            d.text((bw - 16, bh - 14), self.label, font=font(COURR, 20), fill=col, anchor="rs")
            d.text((16, bh - 14), "dipinti: sagome stilizzate, non le opere", font=font(COURR, 20), fill=col, anchor="ls")
        m = Image.new("L", (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, bw - 1, bh - 1], 18, fill=al)
        im.putalpha(m); lay.alpha_composite(im, (int(x0), int(y0)))
    def slot_xy(self, k):
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0); sl, fy = self.slots(bw, bh)
        px, py, fr = sl[k]; return (x0 + px + fr.width / 2, y0 + py + fr.height / 2)
    def floor_y(self):
        x0, y0, x1, y1 = self.box; return y0 + int((y1 - y0) * .80) + 40

# ---------------------------------------------------------------- il palazzo (scenografia esterna)
class Palazzo(El):
    """facciata stilizzata con due torri sottili e logge sovrapposte (schema non in scala).
    night; fog; scaf_t: compare l'impalcatura; climb: [(t, k)] lume dei ladri sull'impalcatura"""
    def __init__(self, box, t0, t1=None, night=False, fog=False, scaf_t=None, lights=None, label="schema semplificato · non in scala"):
        super().__init__(t0, t1, 0.4)
        self.box, self.night, self.fog, self.scaf_t, self.lights, self.label = box, night, fog, scaf_t, lights, label
        self._b = None
    def base(self):
        if self._b: return self._b
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0)
        im = Image.new("RGBA", (bw, bh), (120, 150, 180, 255)); d = ImageDraw.Draw(im)
        for k in range(bh):
            c = int(150 - 50 * k / bh); d.line([(0, k), (bw, k)], fill=(c - 30, c, c + 40, 255))
        gy = int(bh * .88)
        # collina
        d.polygon([(0, gy), (bw * .2, gy - bh * .05), (bw * .8, gy - bh * .04), (bw, gy), (bw, bh), (0, bh)], fill=(90, 110, 70, 255))
        # ali laterali in mattoni
        d.rectangle([bw * .06, bh * .34, bw * .36, gy], fill=BRICK + (255,))
        d.rectangle([bw * .64, bh * .34, bw * .94, gy], fill=BRICK + (255,))
        for x0_ in (bw * .06, bw * .64):
            for r in range(3):
                for c in range(4):
                    wx = x0_ + bw * (.03 + c * .07); wy = bh * (.42 + r * .14)
                    d.rectangle([wx, wy, wx + bw * .03, wy + bh * .07], fill=(60, 50, 50, 255))
        # torri (torricini)
        for cx in (bw * .40, bw * .60):
            d.rectangle([cx - bw * .035, bh * .16, cx + bw * .035, gy], fill=BRICK2 + (255,))
            d.polygon([(cx - bw * .04, bh * .16), (cx, bh * .02), (cx + bw * .04, bh * .16)], fill=(110, 90, 80, 255))
            for r in range(5): d.rectangle([cx - 6, bh * (.22 + r * .12), cx + 6, bh * (.26 + r * .12)], fill=(50, 40, 40, 255))
        # logge sovrapposte in pietra al centro
        lx0, lx1 = bw * .435, bw * .565
        d.rectangle([lx0, bh * .20, lx1, gy], fill=STONE + (255,))
        for r in range(4):
            yy = bh * (.24 + r * .155)
            d.rounded_rectangle([lx0 + 14, yy, lx1 - 14, yy + bh * .11], 40, fill=(70, 60, 56, 255))
            d.line([(lx0, yy + bh * .125), (lx1, yy + bh * .125)], fill=(200, 186, 160, 255), width=4)
        self._b = (im, gy)
        return self._b
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0); al = int(255 * a)
        base, gy = self.base(); im = base.copy(); d = ImageDraw.Draw(im)
        if self.scaf_t is not None and t >= self.scaf_t:
            u = min(1.0, (t - self.scaf_t) / 1.2)
            sx0, sx1 = bw * .03, bw * .39; top = gy - (gy - bh * .30) * u
            col = (190, 196, 204, 255)
            for k in range(9):
                x = sx0 + (sx1 - sx0) * k / 8; d.line([(x, gy), (x, top)], fill=col, width=5)
            y = gy
            while y > top:
                d.line([(sx0, y), (sx1, y)], fill=col, width=4)
                d.rectangle([sx0, y - 8, sx1, y], fill=(150, 120, 80, 255)); y -= bh * .09
            for k in range(8):
                xa = sx0 + (sx1 - sx0) * k / 8; xb = sx0 + (sx1 - sx0) * (k + 1) / 8
                d.line([(xa, gy), (xb, max(top, gy - bh * .18))], fill=(160, 166, 176, 255), width=3)
        if self.night:
            im.alpha_composite(Image.new("RGBA", (bw, bh), NIGHT + (190,)))
            d = ImageDraw.Draw(im)
            for cx in (bw * .40, bw * .60): pass
        if self.lights:
            for (tt, (u, v)) in self.lights:
                if t >= tt:
                    cx, cy = bw * u, bh * v; g = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); dg = ImageDraw.Draw(g)
                    dg.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(255, 220, 120, 120)); g = g.filter(ImageFilter.GaussianBlur(14))
                    im.alpha_composite(g); d = ImageDraw.Draw(im); d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 236, 170, 255))
        if self.fog:
            fg = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); df = ImageDraw.Draw(fg)
            for k in range(7):
                yy = bh * (.30 + k * .10); off = ((t * 40 + k * 230) % (bw + 600)) - 300
                df.ellipse([off - 380, yy - 50, off + 380, yy + 50], fill=(200, 206, 214, 70))
                df.ellipse([bw - off - 300, yy - 30, bw - off + 300, yy + 40], fill=(200, 206, 214, 55))
            fg = fg.filter(ImageFilter.GaussianBlur(30)); im.alpha_composite(fg); d = ImageDraw.Draw(im)
        if self.label:
            d.text((bw - 16, bh - 14), self.label, font=font(COURR, 20), fill=(230, 220, 200, 230), anchor="rs")
        m = Image.new("L", (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, bw - 1, bh - 1], 18, fill=al)
        im.putalpha(m); lay.alpha_composite(im, (int(x0), int(y0)))
    def pt(self, u, v):
        x0, y0, x1, y1 = self.box; return (x0 + (x1 - x0) * u, y0 + (y1 - y0) * v)

# ---------------------------------------------------------------- icone del caso
_uc = {}
def upic(name, size):
    k = (name, size)
    if k in _uc: return _uc[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); dk = (40, 34, 30, 255)
    if name == "velvet":        # rotoli di velluto rosso
        for j, (y, c) in enumerate([(.62, (150, 30, 50)), (.40, (176, 40, 60)), (.18, (130, 24, 44))]):
            d.rounded_rectangle([P(.08, y), P(.92, y + .2)], S // 14, fill=c + (255,))
            d.ellipse([P(.80, y), P(.96, y + .2)], fill=(100, 16, 30, 255)); d.ellipse([P(.85, y + .06), P(.91, y + .14)], fill=(70, 10, 20, 255))
            for q in range(4): d.line([P(.16 + q * .16, y + .03), P(.2 + q * .16, y + .17)], fill=(200, 80, 100, 160), width=S // 60)
    elif name == "scaffold":    # impalcatura di tubi
        c = (190, 196, 204, 255)
        for k in range(4): d.line([P(.12 + k * .25, .04), P(.12 + k * .25, .96)], fill=c, width=S // 26)
        for k in range(4): d.rectangle([P(.06, .18 + k * .24), P(.94, .22 + k * .24)], fill=(150, 120, 80, 255))
        for k in range(3): d.line([P(.12 + k * .25, .94), P(.37 + k * .25, .70)], fill=(160, 166, 176, 255), width=S // 40)
    elif name == "fog":
        for k in range(4):
            y = .22 + k * .18; d.rounded_rectangle([P(.06 + (k % 2) * .1, y), P(.86 + (k % 2) * .08, y + .1)], S // 20, fill=(200, 206, 214, 255))
    elif name == "torch":       # torcia elettrica
        d.polygon([P(.50, .40), P(.94, .10), P(.94, .70)], fill=(255, 230, 140, 110))
        d.rounded_rectangle([P(.06, .34), P(.44, .50)], S // 30, fill=(60, 60, 66, 255)); d.rectangle([P(.40, .30), P(.52, .54)], fill=(90, 90, 96, 255))
    elif name == "guard2":      # due guardiani (simbolo)
        for x in (.32, .68):
            d.ellipse([P(x - .1, .14), P(x + .1, .34)], fill=(230, 200, 170, 255)); d.rounded_rectangle([P(x - .15, .36), P(x + .15, .9)], S // 20, fill=(50, 60, 90, 255))
            d.rectangle([P(x - .12, .10), P(x + .12, .16)], fill=(30, 36, 60, 255))
    elif name == "nuke":        # lista di salvataggio (scudo + elenco)
        d.rectangle([P(.16, .06), P(.84, .94)], fill=PAPER + (255,), outline=(120, 100, 80, 255), width=S // 50)
        d.text(P(.5, .2), "30", font=font(OSW, int(S * .2), 700), fill=RED + (255,), anchor="mm")
        for k in range(5): d.line([P(.26, .40 + k * .1), P(.74 if k % 2 else .6, .40 + k * .1)], fill=(110, 100, 90, 255), width=S // 50)
    elif name == "shop":        # negozio di stoffe
        d.rectangle([P(.08, .30), P(.92, .92)], fill=(200, 186, 160, 255))
        for k in range(6): d.polygon([P(.08 + k * .14, .18), P(.22 + k * .14, .18), P(.22 + k * .14, .34), P(.08 + k * .14, .34)], fill=((180, 40, 50) if k % 2 else (240, 230, 210)) + (255,))
        d.rectangle([P(.16, .44), P(.56, .80)], fill=(90, 110, 130, 255))
        for j, c in enumerate([(176, 40, 60), (60, 80, 140), (200, 160, 60)]): d.rectangle([P(.20 + j * .12, .56), P(.28 + j * .12, .80)], fill=c + (255,))
        d.rectangle([P(.64, .50), P(.84, .92)], fill=(110, 80, 56, 255))
    elif name == "antique":     # antiquario: vaso e cassettone
        d.rectangle([P(.08, .52), P(.62, .94)], fill=(130, 90, 56, 255))
        for k in range(3): d.rectangle([P(.12, .56 + k * .12), P(.58, .64 + k * .12)], fill=(160, 116, 74, 255))
        d.ellipse([P(.66, .40), P(.94, .90)], fill=(60, 90, 140, 255)); d.rectangle([P(.74, .30), P(.86, .44)], fill=(60, 90, 140, 255))
        d.ellipse([P(.22, .20), P(.46, .52)], fill=(200, 160, 80, 255))
    elif name == "armored":     # furgone blindato
        d.rectangle([P(.04, .30), P(.70, .76)], fill=(90, 100, 96, 255)); d.rectangle([P(.70, .42), P(.96, .76)], fill=(110, 120, 116, 255))
        d.rectangle([P(.76, .48), P(.90, .60)], fill=(170, 200, 220, 255))
        for k in range(4):
            for r in range(3): d.ellipse([P(.10 + k * .15, .36 + r * .12), P(.13 + k * .15, .39 + r * .12)], fill=(60, 66, 64, 255))
        for cx in (.20, .56, .84): d.ellipse([P(cx - .08, .70), P(cx + .08, .86)], fill=(30, 30, 34, 255))
    elif name == "ministry":    # palazzo istituzionale generico
        d.polygon([P(.06, .30), P(.5, .08), P(.94, .30)], fill=(220, 210, 190, 255)); d.rectangle([P(.08, .30), P(.92, .88)], fill=(236, 228, 210, 255))
        for k in range(5): d.rectangle([P(.14 + k * .16, .36), P(.22 + k * .16, .82)], fill=(200, 190, 170, 255))
        d.text(P(.5, .21), "MIN", font=font(OSW, int(S * .09), 700), fill=dk, anchor="mm")
    elif name == "lire":        # mazzetta di banconote generiche
        for k in range(3):
            y0 = .62 - k * .16; d.rounded_rectangle([P(.06, y0), P(.94, y0 + .24)], S // 30, fill=(200, 176, 140, 255), outline=(120, 96, 60, 255), width=S // 60)
        d.text(P(.5, .40), "L.", font=font(SERIF, int(S * .14)), fill=(110, 80, 40, 255), anchor="mm")
    elif name == "rocca":       # rocca (fortezza) generica
        d.rectangle([P(.12, .40), P(.88, .92)], fill=(170, 140, 110, 255))
        for x in (.12, .80): d.rectangle([P(x, .22), P(x + .1, .92)], fill=(150, 120, 96, 255))
        d.ellipse([P(.38, .26), P(.62, .50)], fill=(150, 120, 96, 255)); d.rectangle([P(.38, .38), P(.62, .92)], fill=(150, 120, 96, 255))
        d.rounded_rectangle([P(.44, .68), P(.56, .92)], S // 20, fill=(60, 44, 34, 255))
    elif name == "ear":         # telefono che squilla (cornetta + onde)
        d.rounded_rectangle([P(.16, .52), P(.84, .90)], S // 14, fill=(190, 50, 44, 255))
        d.rounded_rectangle([P(.10, .32), P(.90, .48)], S // 12, fill=(160, 40, 36, 255))
        d.ellipse([P(.40, .62), P(.60, .82)], outline=(200, 196, 186, 255), width=S // 40)
        for r in (.10, .18): d.arc([P(.5 - r - .2, .02 - r * .3), P(.5 + r + .2, .30 + r * .3)], 200, 340, fill=GOLD + (255,), width=S // 40)
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _uc[k] = im
    return im

def mini_art(kind, size):
    """icona: dipinto incorniciato rimpicciolito (sagoma stilizzata)"""
    k = ("ma", kind, size)
    if k in _uc: return _uc[k]
    fr = framed(kind, 300); s = size / max(fr.width, fr.height)
    im = fr.resize((max(1, int(fr.width * s)), max(1, int(fr.height * s))), Image.LANCZOS); _uc[k] = im
    return im

_prev_icon = fx.icon
def _icon(name, size, color=None):
    if isinstance(name, str):
        if name.startswith("art_"): return mini_art(name[4:], size)
        m = upic(name, size)
        if m is not None: return m
    return _prev_icon(name, size, color)
fx.icon = _icon

def cover_folder(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 28, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 011", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "IL FURTO DI URBINO", font=font(SERIF, int(w * .085)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "URBINO · 1975-1976", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im

def note_card(lines, w=620, title="APPUNTO", seed=23, size=34):
    return label_card(lines, w, title=title, seed=seed, size=size)
