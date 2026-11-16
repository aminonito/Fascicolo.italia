# Elementi grafici del caso 008 (la Natività di Caravaggio rubata a Palermo, 1969):
# l'oratorio visto dall'interno (scenografia ricorrente, schema non in scala) con l'altare e il quadro
# STILIZZATO (sagoma della composizione, NON l'opera), il taglio della tela, il telaio vuoto, la copia del 2015,
# mappe (Roma -> Palermo, Campania 1980, Svizzera), icone del caso. Tutto disegnato da codice: nessuna foto reale.
import math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "006-tortora")); sys.path.insert(0, os.path.join(HERE, "..", "005-majorana"))
from fi import *
import fi
import fx
from fx import *
import tor                       # icone già pronte (scales, prison, mic...)
import maj                       # (passport, folder, book, question, phone, tv...)
from maj import WorldMap

fi.PLACES.update({"Palermo": (13.36, 38.12), "Laviano": (15.31, 40.78), "Lugano": (8.95, 46.00),
                  "Madrid": (-3.70, 40.42), "Napoli": (14.27, 40.85)})

WALL = (226, 214, 190)
STUCCO = (246, 240, 226)
CANVAS_BG = (40, 30, 22)

# ---------------------------------------------------------------- quadro stilizzato (NON l'opera)
_pc = {}
def nativity_sketch(w, h, copy=False):
    """sagoma della composizione: fondo scuro, luce diagonale, masse delle figure come forme semplici."""
    k = (w, h, copy)
    if k in _pc: return _pc[k]
    im = Image.new("RGBA", (w, h), CANVAS_BG + (255,)); d = ImageDraw.Draw(im)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    light = np.clip(1.0 - np.abs((xx / w) * 0.9 + (yy / h) * 0.6 - 0.95) * 1.6, 0, 1)
    g = np.zeros((h, w, 3), np.float32) + np.array(CANVAS_BG, np.float32)
    g += light[..., None] * np.array([70, 52, 30], np.float32)
    im = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).convert("RGBA"); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * w, b * h)
    # angelo in alto (diagonale chiara)
    d.polygon([P(.18, .10), P(.80, .04), P(.86, .14), P(.30, .24)], fill=(214, 200, 170, 230))
    d.ellipse([P(.70, .04), P(.82, .13)], fill=(200, 160, 120, 255))
    # figure: masse colorate semplici
    d.polygon([P(.28, .40), P(.46, .36), P(.52, .80), P(.22, .82)], fill=(150, 40, 34, 255))     # manto rosso (sagoma)
    d.ellipse([P(.32, .30), P(.44, .40)], fill=(206, 168, 130, 255))
    d.polygon([P(.56, .44), P(.74, .40), P(.80, .86), P(.54, .86)], fill=(110, 90, 60, 255))     # saio
    d.ellipse([P(.60, .34), P(.72, .44)], fill=(190, 150, 110, 255))
    d.polygon([P(.06, .50), P(.22, .46), P(.24, .90), P(.04, .90)], fill=(70, 80, 100, 255))     # figura a sinistra
    d.ellipse([P(.09, .40), P(.21, .50)], fill=(190, 150, 110, 255))
    d.polygon([P(.80, .46), P(.96, .44), P(.97, .90), P(.80, .90)], fill=(220, 214, 196, 255))   # figura a destra (veste chiara)
    d.ellipse([P(.83, .36), P(.94, .46)], fill=(190, 150, 110, 255))
    d.ellipse([P(.36, .80), P(.56, .90)], fill=(236, 220, 190, 255))                              # il Bambino (luce)
    d.rectangle([P(0, .90), P(1, 1)], fill=(60, 46, 32, 255))
    if copy:
        d.text(P(.97, .97), "COPIA 2015", font=font(OSW, max(12, int(w * .07)), 700), fill=(240, 220, 160, 255), anchor="rs")
    _pc[k] = im
    return im

def ragged_frame(w, h, seed=3):
    """telaio vuoto con frammenti di tela rimasti lungo i bordi"""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); rng = random.Random(seed)
    b = max(10, int(w * 0.05))
    d.rectangle([0, 0, w - 1, h - 1], outline=(150, 112, 62, 255), width=b)
    d.rectangle([b, b, w - b, h - b], fill=(60, 50, 40, 255))  # muro dietro scuro
    for side in range(4):
        n = 18
        for i in range(n):
            u0, u1 = i / n, (i + 1) / n; dep = rng.uniform(4, b * 0.9)
            if side == 0: d.polygon([(b + (w - 2 * b) * u0, b), (b + (w - 2 * b) * u1, b), (b + (w - 2 * b) * (u0 + u1) / 2, b + dep)], fill=CANVAS_BG + (255,))
            if side == 1: d.polygon([(b + (w - 2 * b) * u0, h - b), (b + (w - 2 * b) * u1, h - b), (b + (w - 2 * b) * (u0 + u1) / 2, h - b - dep)], fill=CANVAS_BG + (255,))
            if side == 2: d.polygon([(b, b + (h - 2 * b) * u0), (b, b + (h - 2 * b) * u1), (b + dep, b + (h - 2 * b) * (u0 + u1) / 2)], fill=CANVAS_BG + (255,))
            if side == 3: d.polygon([(w - b, b + (h - 2 * b) * u0), (w - b, b + (h - 2 * b) * u1), (w - b - dep, b + (h - 2 * b) * (u0 + u1) / 2)], fill=CANVAS_BG + (255,))
    return im

class Oratory(El):
    """interno dell'oratorio (schema non in scala): pareti con stucchi bianchi, altare, quadro stilizzato.
    cut_t: inizia il taglio lungo i bordi (linea gialla che corre); gone_t: la tela sparisce (arrotolata);
    copy_t: compare la copia 2015; night: oscurità + luce di torcia; dim: velo scuro"""
    def __init__(self, box, t0, t1=None, cut_t=None, gone_t=None, copy_t=None, night=False, torch=None,
                 label="schema semplificato · non in scala", dim=0.0, empty=False):
        super().__init__(t0, t1, 0.4)
        self.box, self.cut_t, self.gone_t, self.copy_t, self.night, self.torch, self.label, self.dim, self.empty = box, cut_t, gone_t, copy_t, night, torch, label, dim, empty
        self._base = None
    def base(self):
        if self._base: return self._base
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0)
        im = Image.new("RGBA", (bw, bh), WALL + (255,)); d = ImageDraw.Draw(im)
        # pavimento a scacchi in prospettiva semplice
        fy = int(bh * 0.80)
        d.rectangle([0, fy, bw, bh], fill=(150, 120, 90, 255))
        for k in range(14):
            x = k * bw / 13
            d.line([(bw / 2 + (x - bw / 2) * 0.55, fy), (x, bh)], fill=(120, 94, 70, 255), width=2)
        for k in range(1, 4):
            y = fy + (bh - fy) * (k / 4) ** 1.4; d.line([(0, y), (bw, y)], fill=(120, 94, 70, 255), width=2)
        # cornicione e lesene con stucchi (motivi semplici)
        d.rectangle([0, 0, bw, int(bh * 0.07)], fill=(214, 200, 174, 255))
        for k in range(26):
            x = k * bw / 25; d.ellipse([x - 8, bh * 0.035 - 8, x + 8, bh * 0.035 + 8], fill=STUCCO + (255,))
        for x in (bw * 0.10, bw * 0.90, bw * 0.26, bw * 0.74):
            d.rectangle([x - 22, bh * 0.07, x + 22, fy], fill=(236, 228, 210, 255), outline=(200, 186, 160, 255), width=2)
            for j in range(5):
                yy = bh * (0.14 + j * 0.13); d.ellipse([x - 16, yy - 16, x + 16, yy + 16], outline=STUCCO + (255,), width=4)
        # finestre laterali
        for x in (bw * 0.18, bw * 0.82):
            d.rounded_rectangle([x - 40, bh * 0.16, x + 40, bh * 0.40], 30, fill=(70, 90, 120, 255), outline=(190, 176, 150, 255), width=5)
        # altare
        ax0, ax1 = bw * 0.36, bw * 0.64
        d.rectangle([ax0, fy - bh * 0.15, ax1, fy], fill=(196, 176, 150, 255), outline=(150, 130, 104, 255), width=3)
        d.rectangle([ax0 - 20, fy - bh * 0.16, ax1 + 20, fy - bh * 0.15 + 8], fill=(170, 150, 120, 255))
        for k in (0.42, 0.58):
            cx_ = bw * k; d.rectangle([cx_ - 5, fy - bh * 0.22, cx_ + 5, fy - bh * 0.16], fill=GOLD + (255,)); d.ellipse([cx_ - 7, fy - bh * 0.25, cx_ + 7, fy - bh * 0.21], fill=(250, 220, 120, 255))
        # cornice dorata del quadro
        ph = int(bh * 0.52); pw = int(ph * 197 / 268); px = int(bw / 2 - pw / 2); py = int(fy - bh * 0.17 - ph)
        d.rectangle([px - 18, py - 18, px + pw + 18, py + ph + 18], fill=(176, 136, 70, 255), outline=(120, 90, 40, 255), width=3)
        self._base = (im, (px, py, pw, ph), fy)
        return self._base
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; bw, bh = int(x1 - x0), int(y1 - y0); al = int(255 * a)
        base, (px, py, pw, ph), fy = self.base(); im = base.copy(); d = ImageDraw.Draw(im)
        gone = self.empty or (self.gone_t is not None and t >= self.gone_t)
        cp = self.copy_t is not None and t >= self.copy_t
        if cp:
            u = ease((t - self.copy_t) / 0.8)
            im.alpha_composite(ragged_frame(pw, ph), (px, py))
            pic = set_alpha(nativity_sketch(pw, ph, copy=True), u)
            im.alpha_composite(pic, (px, py))
        elif gone:
            im.alpha_composite(ragged_frame(pw, ph), (px, py))
        else:
            im.alpha_composite(nativity_sketch(pw, ph), (px, py))
            if self.gone_t is not None and self.cut_t is not None and self.cut_t <= t < self.gone_t:
                pass
        if self.cut_t is not None and t >= self.cut_t and not cp:
            # linea del taglio che corre lungo i bordi
            u = min(1.0, (t - self.cut_t) / 2.4); per = 2 * (pw + ph); L = per * u
            pts = [(px + 6, py + 6), (px + pw - 6, py + 6), (px + pw - 6, py + ph - 6), (px + 6, py + ph - 6), (px + 6, py + 6)]
            acc = 0; path = [pts[0]]
            for p, q in zip(pts, pts[1:]):
                seg = math.dist(p, q)
                if acc + seg <= L: path.append(q); acc += seg
                else:
                    v = (L - acc) / seg; path.append((p[0] + (q[0] - p[0]) * v, p[1] + (q[1] - p[1]) * v)); break
            if not gone or (self.gone_t is not None and t < self.gone_t + 1.0):
                for j in range(0, len(path) - 1):
                    d.line([path[j], path[j + 1]], fill=(250, 210, 70, 255), width=6)
        if self.night:
            ov = Image.new("RGBA", (bw, bh), (6, 8, 20, 200)); im.alpha_composite(ov)
            if self.torch is not None and t >= self.torch:
                cx = px + pw / 2 + math.sin((t - self.torch) * 1.3) * pw * 0.45; cy = py + ph * 0.5 + math.cos((t - self.torch) * 1.7) * ph * 0.3
                m = Image.new("L", (bw, bh), 0); ImageDraw.Draw(m).ellipse([cx - 170, cy - 170, cx + 170, cy + 170], fill=150)
                m = m.filter(ImageFilter.GaussianBlur(40))
                lit = base.copy()
                if gone: lit.alpha_composite(ragged_frame(pw, ph), (px, py))
                else: lit.alpha_composite(nativity_sketch(pw, ph), (px, py))
                im = Image.composite(lit, im, m); d = ImageDraw.Draw(im)
        if self.dim:
            im.alpha_composite(Image.new("RGBA", (bw, bh), (0, 0, 0, int(255 * self.dim)))); d = ImageDraw.Draw(im)
        if self.label:
            d.text((bw - 16, bh - 14), self.label, font=font(COURR, 20), fill=(60, 50, 40, 230) if not self.night else (200, 190, 170, 230), anchor="rs")
            d.text((16, bh - 14), "quadro: sagoma stilizzata, non l'opera", font=font(COURR, 20), fill=(60, 50, 40, 230) if not self.night else (200, 190, 170, 230), anchor="ls")
        m = Image.new("L", (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, bw - 1, bh - 1], 18, fill=al)
        im.putalpha(m); lay.alpha_composite(im, (int(x0), int(y0)))
    def frame_xy(self):
        """centro del quadro in coordinate schermo"""
        x0, y0, x1, y1 = self.box; _, (px, py, pw, ph), _ = self.base()
        return (x0 + px + pw / 2, y0 + py + ph / 2, pw, ph)

# ---------------------------------------------------------------- icone del caso
_cc = {}
def cpic(name, size):
    k = (name, size)
    if k in _cc: return _cc[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S)
    wh = WHITE + (255,); ink = INK + (255,); dk = (34, 32, 30, 255); g = GOLD + (255,)
    if name == "nativity":     # quadro stilizzato con cornice
        pic = nativity_sketch(int(S * .56), int(S * .76))
        d.rectangle([P(.16, .06), P(.84, .94)], fill=(176, 136, 70, 255))
        im.alpha_composite(pic, (int(S * .22), int(S * .12)))
    elif name == "emptyframe":
        im.alpha_composite(ragged_frame(int(S * .64), int(S * .86)), (int(S * .18), int(S * .07)))
    elif name == "roll":       # tela arrotolata
        d.rounded_rectangle([P(.10, .40), P(.90, .64)], S // 12, fill=(196, 170, 130, 255))
        d.ellipse([P(.04, .40), P(.18, .64)], fill=(160, 130, 90, 255)); d.ellipse([P(.075, .46), P(.145, .58)], fill=CANVAS_BG + (255,))
        for x in (.3, .5, .7): d.line([P(x, .41), P(x - .03, .63)], fill=(150, 124, 90, 255), width=S // 90)
    elif name == "carpet":     # tappeto arrotolato rosso
        d.rounded_rectangle([P(.08, .38), P(.92, .66)], S // 10, fill=(150, 50, 44, 255))
        for x in (.25, .45, .65, .85): d.line([P(x, .40), P(x - .05, .64)], fill=(220, 180, 90, 255), width=S // 50)
        d.ellipse([P(.02, .38), P(.16, .66)], fill=(120, 40, 36, 255)); d.ellipse([P(.05, .45), P(.13, .59)], fill=(220, 180, 90, 255))
        for k in range(6): d.line([P(.92, .40 + k * .05), P(.98, .40 + k * .05)], fill=(220, 200, 150, 255), width=S // 90)
    elif name == "oratory":    # facciata semplice di chiesetta
        d.rectangle([P(.16, .40), P(.84, .94)], fill=(222, 206, 176, 255))
        d.polygon([P(.10, .42), P(.50, .14), P(.90, .42)], fill=(196, 176, 146, 255))
        d.rounded_rectangle([P(.40, .62), P(.60, .94)], S // 20, fill=(100, 70, 46, 255))
        d.ellipse([P(.43, .28), P(.57, .40)], fill=(80, 100, 130, 255))
        d.line([P(.50, .02), P(.50, .14)], fill=dk, width=S // 40); d.line([P(.45, .06), P(.55, .06)], fill=dk, width=S // 40)
    elif name == "alarm_off":  # campanella d'allarme barrata
        d.ellipse([P(.18, .18), P(.82, .82)], fill=(200, 60, 50, 255)); d.ellipse([P(.30, .30), P(.70, .70)], fill=(230, 220, 200, 255))
        d.ellipse([P(.44, .44), P(.56, .56)], fill=dk)
        d.line([P(.10, .90), P(.90, .10)], fill=dk, width=S // 14)
    elif name == "stable":     # stalla
        d.polygon([P(.06, .44), P(.50, .14), P(.94, .44)], fill=(120, 60, 44, 255))
        d.rectangle([P(.12, .44), P(.88, .92)], fill=(160, 90, 60, 255))
        d.rectangle([P(.36, .56), P(.64, .92)], fill=(96, 56, 36, 255)); d.line([P(.36, .56), P(.64, .92)], fill=(220, 200, 160, 255), width=S // 40); d.line([P(.64, .56), P(.36, .92)], fill=(220, 200, 160, 255), width=S // 40)
        for k in range(5): d.line([P(.14 + k * .02, .92), P(.20 + k * .03, .80)], fill=(230, 200, 100, 255), width=S // 90)
    elif name == "rat":
        c = (120, 116, 112, 255)
        d.ellipse([P(.20, .40), P(.74, .76)], fill=c); d.polygon([P(.70, .48), P(.94, .60), P(.70, .70)], fill=c)
        d.ellipse([P(.62, .36), P(.76, .50)], fill=(150, 140, 136, 255)); d.ellipse([P(.83, .56), P(.88, .61)], fill=dk)
        d.arc([P(-.10, .40), P(.30, .90)], 270, 80, fill=c, width=S // 40)
    elif name == "pig":
        c = (230, 170, 170, 255)
        d.ellipse([P(.14, .34), P(.80, .78)], fill=c)
        for x in (.24, .38, .56, .68): d.rectangle([P(x, .72), P(x + .06, .88)], fill=c)
        d.ellipse([P(.72, .48), P(.92, .64)], fill=(220, 140, 150, 255)); d.ellipse([P(.78, .54), P(.80, .58)], fill=dk); d.ellipse([P(.84, .54), P(.86, .58)], fill=dk)
        d.polygon([P(.62, .34), P(.70, .20), P(.74, .38)], fill=c); d.ellipse([P(.64, .42), P(.68, .46)], fill=dk)
    elif name == "fire":
        d.polygon([P(.50, .06), P(.78, .44), P(.80, .70), P(.66, .90), P(.34, .90), P(.20, .70), P(.24, .48), P(.36, .58), P(.40, .30)], fill=(230, 110, 40, 255))
        d.polygon([P(.50, .40), P(.64, .62), P(.60, .86), P(.40, .86), P(.36, .66)], fill=(250, 210, 80, 255))
    elif name == "quake":      # casa con crepa
        d.polygon([P(.12, .42), P(.50, .12), P(.88, .42)], fill=(160, 120, 90, 255))
        d.rectangle([P(.18, .42), P(.82, .90)], fill=(200, 186, 160, 255))
        d.line([P(.50, .42), P(.44, .56), P(.56, .66), P(.46, .78), P(.52, .90)], fill=dk, width=S // 30)
        for k in range(3): d.arc([P(.02 - k * .02, .86 - k * .02), P(.98 + k * .02, 1.0 + k * .02)], 200, 340, fill=(200, 60, 50, 255), width=S // 60)
    elif name == "swiss":      # montagne con sigla CH (generico)
        d.polygon([P(.02, .86), P(.36, .24), P(.56, .56), P(.70, .36), P(.98, .86)], fill=(110, 120, 130, 255))
        d.polygon([P(.28, .38), P(.36, .24), P(.44, .38)], fill=wh); d.polygon([P(.64, .46), P(.70, .36), P(.76, .46)], fill=wh)
        d.rounded_rectangle([P(.62, .06), P(.94, .26)], S // 30, fill=(200, 40, 40, 255))
        d.text(P(.78, .16), "CH", font=font(OSW, int(S * .13), 700), fill=wh, anchor="mm")
    elif name == "pieces":     # tela tagliata in 4 pezzi
        pic = nativity_sketch(int(S * .64), int(S * .80)); pw, ph = pic.size
        for (ix, iy) in ((0, 0), (1, 0), (0, 1), (1, 1)):
            part = pic.crop((ix * pw // 2, iy * ph // 2, (ix + 1) * pw // 2, (iy + 1) * ph // 2))
            im.alpha_composite(part.rotate((ix - .5) * 10 + (iy - .5) * 6, expand=True, resample=Image.BICUBIC), (int(S * .12 + ix * (pw // 2 + S * .08)), int(S * .06 + iy * (ph // 2 + S * .06))))
        d = ImageDraw.Draw(im)
    elif name == "scanner":    # scansione digitale (riproduzione)
        d.rectangle([P(.14, .10), P(.86, .90)], fill=(40, 44, 50, 255))
        pic = nativity_sketch(int(S * .60), int(S * .70)); im.alpha_composite(pic, (int(S * .20), int(S * .15))); d = ImageDraw.Draw(im)
        d.rectangle([P(.12, .46), P(.88, .50)], fill=(80, 220, 240, 230))
        for k in range(6): d.line([P(.20 + k * .12, .15), P(.20 + k * .12, .85)], fill=(80, 220, 240, 90), width=S // 120)
    elif name == "toplist":    # lista "top ten"
        d.rectangle([P(.16, .06), P(.84, .94)], fill=(236, 230, 214, 255))
        d.text(P(.50, .17), "TOP TEN", font=font(OSW, int(S * .11), 700), fill=RED + (255,), anchor="mm")
        for k in range(6):
            y = .32 + k * .10; d.text(P(.24, y), f"{k + 1}.", font=font(COURR, int(S * .06)), fill=ink, anchor="lm")
            d.line([P(.34, y), P(.76, y)], fill=(130, 120, 110, 255) if k != 2 else RED + (255,), width=S // 50 if k == 2 else S // 90)
    elif name == "meeting":    # tavolo di riunione visto dall'alto
        d.ellipse([P(.18, .30), P(.82, .70)], fill=(120, 86, 56, 255))
        for k in range(8):
            a_ = k * math.pi / 4; d.ellipse([P(.50 + .40 * math.cos(a_) - .06, .50 + .30 * math.sin(a_) - .06), P(.50 + .40 * math.cos(a_) + .06, .50 + .30 * math.sin(a_) + .06)], fill=(40, 40, 46, 255))
        d.rectangle([P(.38, .40), P(.62, .60)], fill=(176, 136, 70, 255))
    elif name == "cutter":     # taglierino generico (piccolo, non in primo piano)
        d.rounded_rectangle([P(.10, .44), P(.70, .60)], S // 30, fill=(240, 190, 40, 255))
        d.polygon([P(.70, .46), P(.92, .50), P(.70, .58)], fill=(200, 200, 206, 255))
    elif name == "commission":  # aula parlamentare stilizzata
        d.rectangle([P(.10, .30), P(.90, .86)], fill=(214, 200, 174, 255))
        d.polygon([P(.06, .32), P(.50, .10), P(.94, .32)], fill=(190, 170, 140, 255))
        for k in range(5): d.rectangle([P(.18 + k * .14, .36), P(.24 + k * .14, .82)], fill=(236, 228, 210, 255))
        d.text(P(.50, .24), "ANTIMAFIA", font=font(OSW, int(S * .07), 700), fill=ink, anchor="mm")
    elif name == "earth":      # terra con onde sismiche
        d.rectangle([P(.04, .60), P(.96, .92)], fill=(130, 100, 70, 255))
        d.line([P(.04, .60), P(.24, .54), P(.40, .66), P(.58, .52), P(.76, .64), P(.96, .58)], fill=dk, width=S // 40)
        for r in (.14, .26, .38): d.arc([P(.50 - r, .40 - r), P(.50 + r, .40 + r)], 200, 340, fill=(200, 60, 50, 255), width=S // 50)
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _cc[k] = im
    return im

_prev_icon = fx.icon
def _icon(name, size, color=None):
    if isinstance(name, str):
        m = cpic(name, size)
        if m is not None: return m
    return _prev_icon(name, size, color)
fx.icon = _icon

def cover_folder(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 28, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 008", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "LA NATIVITÀ", font=font(SERIF, int(w * .10)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .70), "Palermo · ottobre 1969", font=font(COURR, int(w * .045)), fill=(90, 70, 50, 255), anchor="mm")
    return im

def label_card(lines, w=560, title=None, seed=31, size=34):
    """cartellino da museo / scheda dell'opera (ricostruzione grafica)"""
    h = 90 + len(lines) * (size + 18) + (60 if title else 0)
    im = paper(w, h, (236, 230, 214), seed, 0.3); d = ImageDraw.Draw(im); y = 40
    if title:
        d.text((w / 2, y + 10), title, font=font(OSW, size + 6, 700), fill=INK + (255,), anchor="mm"); y += 60
        d.line([(30, y - 14), (w - 30, y - 14)], fill=(140, 130, 110, 255), width=2)
    for ln in lines:
        d.text((36, y + size / 2), ln, font=font(COURR, size), fill=INK + (255,), anchor="lm"); y += size + 18
    recon_label(d, w, h)
    return im
