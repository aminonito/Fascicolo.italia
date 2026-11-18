# Elementi grafici del caso 013 (i Van Gogh rubati ad Amsterdam nel 2002 e ritrovati a Castellammare nel 2016):
# il museo visto da fuori con scala, tetto e corda (scenografia, schema non in scala), la sala con i due dipinti
# (sagome stilizzate, non le opere), icone del caso. Tutto disegnato da codice: nessuna foto, nessuna riproduzione.
import math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "012-parmalat"))
from par import *                      # catena completa: par -> urb -> rom -> mod -> car -> osp -> tor -> maj (+ pon)
import par, urb
import fi
import fx
from fx import *
from mod import label_card

fi.PLACES.update({"Amsterdam": (4.90, 52.37), "Castellammare": (14.48, 40.70), "Napoli": (14.27, 40.85),
                  "Scheveningen": (4.27, 52.11), "Nuenen": (5.55, 51.47), "Milano": (9.19, 45.46), "Roma": (12.50, 41.90)})

NIGHT = (8, 10, 24)
CONCRETE = (150, 150, 146)
_pc = {}
def art(kind, w, h):
    """sagome stilizzate e generiche: NON riproducono le opere"""
    k = (kind, w, h)
    if k in _pc: return _pc[k]
    im = Image.new("RGBA", (w, h), (0, 0, 0, 255)); d = ImageDraw.Draw(im)
    if kind == "sea":            # marina: cielo scuro, mare grigio-verde, striscia di sabbia
        for y in range(h):
            u = y / h
            if u < .45: c = (int(96 + 40 * u), int(104 + 40 * u), int(110 + 30 * u))
            elif u < .72: c = (70, 92, 84)
            else: c = (176, 156, 112)
            d.line([(0, y), (w, y)], fill=c + (255,))
        rng = random.Random(4)
        for _ in range(40):
            x = rng.uniform(0, w); y = rng.uniform(h * .48, h * .70)
            d.arc([x - 30, y - 6, x + 30, y + 6], 200, 340, fill=(200, 206, 196, 255), width=2)
        for _ in range(16):
            x = rng.uniform(0, w); y = rng.uniform(h * .05, h * .4)
            d.ellipse([x - 50, y - 14, x + 50, y + 14], fill=(70, 74, 80, 160))
        for x in (.2, .3, .62):
            d.rectangle([w * x, h * .78, w * x + w * .015, h * .88], fill=(50, 44, 40, 255))
    else:                        # chiesa di campagna tra gli alberi, figure scure davanti
        d.rectangle([0, 0, w, h], fill=(150, 170, 196, 255))
        d.rectangle([0, h * .70, w, h], fill=(150, 140, 96, 255))
        for x in (.08, .86):
            d.ellipse([w * (x - .08), h * .30, w * (x + .1), h * .74], fill=(70, 96, 60, 255))
        d.rectangle([w * .30, h * .42, w * .70, h * .72], fill=(200, 184, 150, 255))
        d.polygon([(w * .28, h * .44), (w * .5, h * .30), (w * .72, h * .44)], fill=(110, 80, 64, 255))
        d.rectangle([w * .44, h * .12, w * .56, h * .42], fill=(196, 180, 146, 255))
        d.polygon([(w * .43, h * .13), (w * .5, h * .02), (w * .57, h * .13)], fill=(110, 80, 64, 255))
        for x in (.36, .60): d.rounded_rectangle([w * x, h * .50, w * x + w * .05, h * .62], 6, fill=(70, 70, 80, 255))
        for j, x in enumerate((.18, .26, .40, .52, .66, .78)):
            cx = w * x; d.rectangle([cx - 6, h * .78, cx + 6, h * .92], fill=(36, 34, 40, 255)); d.ellipse([cx - 6, h * .74, cx + 6, h * .79], fill=(36, 34, 40, 255))
    _pc[k] = im
    return im

ART = [("sea", 51, 34, "LA SPIAGGIA DI SCHEVENINGEN\n1882"), ("church", 32, 41, "LA CHIESA DI NUENEN\n1884-85")]

def framed(kind, hpx, frame=True, torn=False):
    k = ("fr", kind, hpx, frame, torn)
    if k in _pc: return _pc[k]
    wcm, hcm = [(a[1], a[2]) for a in ART if a[0] == kind][0]
    ph = hpx; pw = int(ph * wcm / hcm); b = max(8, ph // 12) if frame else 0
    im = Image.new("RGBA", (pw + 2 * b, ph + 2 * b), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if frame:
        d.rectangle([0, 0, pw + 2 * b - 1, ph + 2 * b - 1], fill=(176, 136, 70, 255), outline=(110, 80, 36, 255), width=3)
        d.rectangle([b // 2, b // 2, pw + b + b // 2, ph + b + b // 2], outline=(220, 186, 110, 255), width=2)
    im.alpha_composite(art(kind, pw, ph), (b, b))
    if torn:
        d = ImageDraw.Draw(im)
        d.polygon([(b, b + ph * .80), (b + pw * .13, b + ph), (b, b + ph)], fill=(226, 214, 186, 255))
    _pc[k] = im
    return im

# ---------------------------------------------------------------- la sala (scenografia interna)
class Sala(El):
    """sala del museo con i due dipinti (schema non in scala). gone: {k: t}; back: t; night; torch; window_t; hl: (k, t)"""
    def __init__(self, box, t0, t1=None, gone=None, back=None, night=False, torch=None, window_t=None, hl=None,
                 label="schema semplificato · non in scala", captions=True):
        super().__init__(t0, t1, 0.4)
        self.box, self.gone, self.back, self.night, self.torch, self.window_t, self.hl = box, gone or {}, back, night, torch, window_t, hl
        self.label, self.captions = label, captions; self._b = None
    def slots(self, bw, bh):
        out = []
        for k, x in enumerate((.32, .66)):
            fr = framed(ART[k][0], int(bh * .34)); out.append((int(bw * x - fr.width / 2), int(bh * .42 - fr.height / 2), fr))
        return out
    def base(self):
        if self._b: return self._b
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0)
        im = Image.new("RGBA", (bw, bh), (232, 230, 224, 255)); d = ImageDraw.Draw(im)
        fy = int(bh * .80)
        d.rectangle([0, fy, bw, bh], fill=(120, 110, 100, 255))
        for k in range(16):
            x = k * bw / 15; d.line([(bw / 2 + (x - bw / 2) * .6, fy), (x, bh)], fill=(100, 92, 84, 255), width=2)
        d.rectangle([0, 0, bw, int(bh * .06)], fill=(200, 200, 196, 255))
        for k in range(6):
            x = bw * (.1 + k * .16); d.rectangle([x - 40, bh * .06, x + 40, bh * .08], fill=(250, 246, 220, 255))
        d.line([(0, fy - 6), (bw, fy - 6)], fill=(170, 166, 160, 255), width=10)
        self._b = (im, fy)
        return self._b
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0); al = int(255 * a)
        base, fy = self.base(); im = base.copy(); d = ImageDraw.Draw(im)
        wx0, wx1 = bw * .88, bw * .98
        br = self.window_t is not None and t >= self.window_t
        d.rectangle([wx0, bh * .16, wx1, bh * .56], fill=(20, 26, 50, 255) if br else (90, 110, 140, 255), outline=(180, 180, 176, 255), width=6)
        if br:
            cx, cy = (wx0 + wx1) / 2, bh * .36
            for k in range(9):
                ang = k * 2 * math.pi / 9; d.line([(cx, cy), (cx + 70 * math.cos(ang), cy + 90 * math.sin(ang))], fill=(220, 230, 240, 255), width=3)
        sl = self.slots(bw, bh)
        for k, (px, py, fr) in enumerate(sl):
            g = self.gone.get(k); back = self.back is not None and t >= self.back
            if g is not None and t >= g and not back:
                u = min(1.0, (t - g) / 0.5)
                if u < 1: im.alpha_composite(set_alpha(fr, 1 - u), (px, int(py - 30 * u)))
                d.rectangle([px + 4, py + 4, px + fr.width - 4, py + fr.height - 4], outline=(196, 190, 176, 255), width=4)
                d.rectangle([px + 10, py + 10, px + fr.width - 10, py + fr.height - 10], fill=(240, 238, 232, 255))
            else:
                if back:
                    u = min(1.0, (t - self.back) / 0.6); im.alpha_composite(set_alpha(fr, u), (px, py))
                else: im.alpha_composite(fr, (px, py))
            if self.captions:
                f = font(OSW, max(16, bh // 34), 600)
                d.multiline_text((px + fr.width / 2, py + fr.height + 14), ART[k][3], font=f, fill=(70, 60, 50, 255), anchor="ma", align="center", spacing=2)
            if self.hl and self.hl[0] == k and t >= self.hl[1]:
                d.rectangle([px - 12, py - 12, px + fr.width + 12, py + fr.height + 12], outline=RED + (255,), width=8)
        if self.night:
            im.alpha_composite(Image.new("RGBA", (bw, bh), NIGHT + (200,)))
            if self.torch is not None and t >= self.torch:
                cx = bw * (.5 + .3 * math.sin((t - self.torch) * 1.1)); cy = bh * (.42 + .1 * math.cos((t - self.torch) * 1.7))
                m = Image.new("L", (bw, bh), 0); ImageDraw.Draw(m).ellipse([cx - 200, cy - 200, cx + 200, cy + 200], fill=170)
                m = m.filter(ImageFilter.GaussianBlur(45))
                lit = base.copy(); dl = ImageDraw.Draw(lit)
                for k, (px, py, fr) in enumerate(sl):
                    g = self.gone.get(k)
                    if g is not None and t >= g:
                        dl.rectangle([px + 10, py + 10, px + fr.width - 10, py + fr.height - 10], fill=(240, 238, 232, 255), outline=(196, 190, 176, 255), width=4)
                    else: lit.alpha_composite(fr, (px, py))
                im = Image.composite(lit, im, m); d = ImageDraw.Draw(im)
        if self.label:
            col = (60, 50, 40, 230) if not self.night else (200, 190, 170, 230)
            d.text((bw - 16, bh - 14), self.label, font=font(COURR, 20), fill=col, anchor="rs")
            d.text((16, bh - 14), "dipinti: sagome stilizzate, non le opere", font=font(COURR, 20), fill=col, anchor="ls")
        m = Image.new("L", (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, bw - 1, bh - 1], 18, fill=al)
        im.putalpha(m); lay.alpha_composite(im, (int(x0), int(y0)))
    def slot_xy(self, k):
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0); px, py, fr = self.slots(bw, bh)[k]
        return (x0 + px + fr.width / 2, y0 + py + fr.height / 2)
    def floor_y(self):
        x0, y0, x1, y1 = self.box; return y0 + int((y1 - y0) * .80) + 40

# ---------------------------------------------------------------- il museo (scenografia esterna)
class Museo(El):
    """edificio moderno stilizzato a due livelli (schema non in scala).
    ladder_t: scala appoggiata sul retro (a sinistra); window_t: finestra rotta; rope_t: corda sulla facciata (a destra);
    lights: [(t, (u, v))] lumi; police_t: luci blu"""
    def __init__(self, box, t0, t1=None, night=True, ladder_t=None, window_t=None, rope_t=None, lights=None, police_t=None,
                 label="schema semplificato · non in scala"):
        super().__init__(t0, t1, 0.4)
        self.box, self.night, self.ladder_t, self.window_t, self.rope_t, self.lights, self.police_t, self.label = box, night, ladder_t, window_t, rope_t, lights, police_t, label
        self._b = None
    def base(self):
        if self._b: return self._b
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0)
        im = Image.new("RGBA", (bw, bh), (0, 0, 0, 255)); d = ImageDraw.Draw(im)
        for k in range(bh):
            c = int(60 + 60 * k / bh); d.line([(0, k), (bw, k)], fill=(c - 30, c - 20, c + 20, 255))
        gy = int(bh * .88)
        d.rectangle([0, gy, bw, bh], fill=(70, 70, 66, 255))
        # corpo basso (primo piano) e corpo alto
        d.rectangle([bw * .06, bh * .48, bw * .94, gy], fill=CONCRETE + (255,))
        d.rectangle([bw * .30, bh * .18, bw * .94, bh * .48], fill=(176, 176, 170, 255))
        d.line([(bw * .06, bh * .48), (bw * .30, bh * .48)], fill=(110, 110, 106, 255), width=8)   # tetto del primo piano
        for r in range(2):
            for c in range(7):
                wx = bw * (.10 + c * .12); wy = bh * (.56 + r * .15)
                d.rectangle([wx, wy, wx + bw * .07, wy + bh * .09], fill=(60, 70, 86, 255))
        for c in range(5):
            wx = bw * (.36 + c * .115); d.rectangle([wx, bh * .26, wx + bw * .08, bh * .40], fill=(60, 70, 86, 255))
        d.rectangle([bw * .46, gy - bh * .14, bw * .54, gy], fill=(50, 56, 66, 255))
        self._b = (im, gy)
        return self._b
    def pt(self, u, v):
        x0, y0, x1, y1 = self.box; return (x0 + (x1 - x0) * u, y0 + (y1 - y0) * v)
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0); al = int(255 * a)
        base, gy = self.base(); im = base.copy(); d = ImageDraw.Draw(im)
        if self.window_t is not None and t >= self.window_t:      # finestra rotta al piano alto
            wx = bw * .36; d.rectangle([wx, bh * .26, wx + bw * .08, bh * .40], fill=(10, 10, 16, 255))
            cx, cy = wx + bw * .04, bh * .33
            for k in range(8):
                ang = k * 2 * math.pi / 8; d.line([(cx, cy), (cx + 40 * math.cos(ang), cy + 50 * math.sin(ang))], fill=(220, 230, 240, 255), width=3)
        if self.night:
            im.alpha_composite(Image.new("RGBA", (bw, bh), NIGHT + (150,))); d = ImageDraw.Draw(im)
        if self.ladder_t is not None and t >= self.ladder_t:       # scala appoggiata al corpo basso
            u = min(1.0, (t - self.ladder_t) / 0.8)
            lx0, lx1 = bw * .10, bw * .14; top = gy - (gy - bh * .45) * u
            col = (210, 190, 120, 255)
            d.line([(lx0, gy), (lx0 + bw * .015, top)], fill=col, width=7); d.line([(lx1, gy), (lx1 + bw * .015, top)], fill=col, width=7)
            y = gy - 30
            while y > top:
                f = (gy - y) / (gy - bh * .45) * bw * .015
                d.line([(lx0 + f, y), (lx1 + f, y)], fill=col, width=5); y -= 34
        if self.rope_t is not None and t >= self.rope_t:          # corda dalla facciata
            u = min(1.0, (t - self.rope_t) / 0.8)
            rx = bw * .90; d.line([(rx, bh * .30), (rx, bh * .30 + (gy - bh * .30) * u)], fill=(220, 200, 150, 255), width=6)
        if self.lights:
            for (tt, (u, v)) in self.lights:
                if t >= tt:
                    cx, cy = bw * u, bh * v; g = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); dg = ImageDraw.Draw(g)
                    dg.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(255, 220, 120, 120)); g = g.filter(ImageFilter.GaussianBlur(14))
                    im.alpha_composite(g); d = ImageDraw.Draw(im); d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 236, 170, 255))
        if self.police_t is not None and t >= self.police_t:
            on = int((t - self.police_t) * 4) % 2 == 0
            g = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); dg = ImageDraw.Draw(g)
            dg.ellipse([bw * .70 - 160, gy - 160, bw * .70 + 160, gy + 60], fill=((60, 110, 255, 110) if on else (40, 60, 160, 50)))
            g = g.filter(ImageFilter.GaussianBlur(40)); im.alpha_composite(g); d = ImageDraw.Draw(im)
        if self.label:
            d.text((bw - 16, bh - 14), self.label, font=font(COURR, 20), fill=(230, 220, 200, 230), anchor="rs")
        m = Image.new("L", (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, bw - 1, bh - 1], 18, fill=al)
        im.putalpha(m); lay.alpha_composite(im, (int(x0), int(y0)))

# ---------------------------------------------------------------- icone del caso
_vc = {}
def vpic(name, size):
    k = (name, size)
    if k in _vc: return _vc[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); dk = (40, 34, 30, 255)
    if name == "ladder":
        c = (210, 190, 120, 255)
        d.line([P(.28, .96), P(.40, .04)], fill=c, width=S // 22); d.line([P(.60, .96), P(.72, .04)], fill=c, width=S // 22)
        for k_ in range(7):
            v = .9 - k_ * .13; f = (1 - v) * .12; d.line([P(.29 + f, v), P(.61 + f, v)], fill=c, width=S // 30)
    elif name == "rope":
        for k_ in range(5):
            d.ellipse([P(.18 + k_ * .02, .22 + k_ * .05), P(.82 - k_ * .02, .70 - k_ * .02)], outline=(210, 180, 120, 255), width=S // 30)
        d.line([P(.5, .70), P(.56, .98)], fill=(210, 180, 120, 255), width=S // 30)
    elif name == "sledge":      # mazza
        d.line([P(.20, .92), P(.62, .34)], fill=(150, 110, 70, 255), width=S // 14)
        d.polygon([P(.48, .14), P(.86, .40), P(.74, .56), P(.36, .30)], fill=(90, 96, 104, 255))
    elif name == "cap":         # berretto
        d.chord([P(.16, .22), P(.84, .86)], 180, 360, fill=(40, 50, 70, 255))
        d.rectangle([P(.16, .52), P(.84, .58)], fill=(30, 36, 50, 255))
        d.polygon([P(.50, .54), P(.96, .58), P(.92, .68), P(.50, .62)], fill=(30, 36, 50, 255))
        d.ellipse([P(.46, .18), P(.54, .26)], fill=(60, 70, 90, 255))
    elif name == "bundle":      # tela arrotolata avvolta in un panno
        d.rounded_rectangle([P(.08, .34), P(.92, .70)], S // 10, fill=(196, 180, 150, 255))
        for k_ in range(6): d.line([P(.16 + k_ * .14, .36), P(.10 + k_ * .14, .68)], fill=(160, 140, 110, 255), width=S // 50)
        d.ellipse([P(.84, .34), P(.98, .70)], fill=(176, 160, 130, 255)); d.ellipse([P(.88, .46), P(.94, .58)], fill=(120, 100, 80, 255))
        d.line([P(.30, .30), P(.30, .74)], fill=(120, 90, 60, 255), width=S // 40); d.line([P(.66, .30), P(.66, .74)], fill=(120, 90, 60, 255), width=S // 40)
    elif name == "gdf":         # distintivo generico (nessuno stemma reale)
        d.polygon([P(.5, .06), P(.88, .22), P(.82, .66), P(.5, .94), P(.18, .66), P(.12, .22)], fill=(200, 160, 50, 255), outline=(120, 90, 30, 255))
        d.polygon([P(.5, .18), P(.76, .30), P(.72, .62), P(.5, .82), P(.28, .62), P(.24, .30)], fill=(40, 70, 110, 255))
        d.text(P(.5, .50), "GdF", font=font(OSW, int(S * .16), 700), fill=(240, 220, 150, 255), anchor="mm")
    elif name == "stopwatch":
        d.ellipse([P(.12, .18), P(.88, .94)], fill=(240, 236, 226, 255), outline=dk, width=S // 30)
        d.rectangle([P(.44, .04), P(.56, .16)], fill=dk)
        d.pieslice([P(.18, .24), P(.82, .88)], -90, -90 + 360 * 220 / 600, fill=RED + (255,))
        d.ellipse([P(.46, .52), P(.54, .60)], fill=dk)
    elif name == "reward":      # busta con 100.000 €
        d.rectangle([P(.08, .26), P(.92, .80)], fill=PAPER + (255,), outline=(120, 100, 80, 255), width=S // 50)
        d.polygon([P(.08, .26), P(.5, .56), P(.92, .26)], fill=(220, 210, 186, 255), outline=(120, 100, 80, 255))
        d.text(P(.5, .70), "100.000 €", font=font(OSW, int(S * .13), 700), fill=RED + (255,), anchor="mm")
    elif name == "lab":         # laboratorio di restauro: lente e pennello
        d.line([P(.20, .90), P(.58, .40)], fill=(150, 110, 70, 255), width=S // 24)
        d.polygon([P(.54, .44), P(.66, .26), P(.72, .30), P(.62, .48)], fill=(60, 50, 40, 255))
        d.ellipse([P(.52, .06), P(.92, .46)], outline=(80, 90, 100, 255), width=S // 24)
    elif name == "windmill":    # Olanda (simbolo generico)
        d.polygon([P(.38, .94), P(.44, .36), P(.56, .36), P(.62, .94)], fill=(160, 120, 90, 255))
        cx, cy = .5, .34
        for k_ in range(4):
            ang = math.radians(45 + 90 * k_); ex, ey = cx + .42 * math.cos(ang), cy + .42 * math.sin(ang)
            d.line([P(cx, cy), P(ex, ey)], fill=(230, 226, 214, 255), width=S // 16)
        d.ellipse([P(.46, .30), P(.54, .38)], fill=dk)
    elif name == "vesuvio":
        d.polygon([P(.02, .92), P(.40, .30), P(.56, .34), P(.98, .92)], fill=(110, 96, 90, 255))
        d.polygon([P(.40, .30), P(.48, .40), P(.56, .34)], fill=(80, 70, 66, 255))
        d.rectangle([P(0, .86), P(1, .98)], fill=(60, 110, 160, 255))
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _vc[k] = im
    return im

def mini_art(kind, size):
    k = ("ma", kind, size)
    if k in _vc: return _vc[k]
    fr = framed(kind, 300); s = size / max(fr.width, fr.height)
    im = fr.resize((max(1, int(fr.width * s)), max(1, int(fr.height * s))), Image.LANCZOS); _vc[k] = im
    return im

_prev_icon = fx.icon
def _icon(name, size, color=None):
    if isinstance(name, str):
        if name.startswith("vg_"): return mini_art(name[3:], size)
        m = vpic(name, size)
        if m is not None: return m
    return _prev_icon(name, size, color)
fx.icon = _icon

def cover_folder(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 28, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 013", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "I VAN GOGH RUBATI", font=font(SERIF, int(w * .085)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "AMSTERDAM 2002 · CASTELLAMMARE 2016", font=font(TYPE, int(w * .045)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im
