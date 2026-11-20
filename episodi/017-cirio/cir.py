# Elementi grafici del caso 017 (il crac Cirio, 2002-2021): scatole di conserve generiche, il "travaso" del debito
# dalle banche ai risparmiatori (scenografia ricorrente, schema semplificato), l'albero del gruppo. Tutto disegnato da codice:
# nessuna foto reale, nessun logo o marchio riprodotto (né Cirio né squadre né banche), nessun documento originale.
import math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "012-parmalat"))
from par import *
import par
import fi
import fx
from fx import *
import pon
from pon import WorldMap, WPL

WPL.update({"Torino": (7.68, 45.07), "Roma": (12.50, 41.90), "Lussemburgo": (6.13, 49.61), "Parigi": (2.35, 48.86),
            "Londra": (-0.13, 51.51), "Liverpool": (-2.98, 53.41), "Sydney": (151.2, -33.87), "Napoli": (14.27, 40.85),
            "San Paolo": (-46.63, -23.55), "Sudafrica": (28.0, -26.2), "Birmingham": (-1.89, 52.49), "Parma": (10.33, 44.80),
            "Bologna": (11.34, 44.49), "Collecchio": (10.21, 44.75), "Berlino": (13.40, 52.52), "Vienna": (16.37, 48.21)})
fi.PLACES.update({"Torino": (7.68, 45.07), "Roma": (12.50, 41.90), "Napoli": (14.27, 40.85), "Parma": (10.33, 44.80),
                  "Bologna": (11.34, 44.49), "Milano": (9.19, 45.46), "Nizza Monferrato": (8.36, 44.77)})

TOM = (196, 52, 40)
LEAF = (70, 130, 70)

_pc3 = {}
def cpic(name, size):
    k = (name, size)
    if k in _pc3: return _pc3[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); dk = (40, 34, 30, 255); wh = (240, 238, 232, 255)
    if name == "can":            # barattolo di pomodori generico, nessun marchio
        d.ellipse([P(.22, .82), P(.78, .96)], fill=(150, 150, 156, 255))
        d.rectangle([P(.22, .16), P(.78, .89)], fill=(190, 192, 198, 255))
        d.rectangle([P(.22, .30), P(.78, .76)], fill=(220, 60, 46, 255))
        d.ellipse([P(.22, .09), P(.78, .23)], fill=(214, 216, 222, 255), outline=(150, 150, 156, 255), width=S // 60)
        d.ellipse([P(.36, .40), P(.64, .66)], fill=(236, 90, 64, 255)); d.polygon([P(.44, .40), P(.50, .34), P(.56, .40), P(.50, .43)], fill=LEAF + (255,))
        d.text(P(.50, .72), "POMODORI", font=font(OSW, int(S * .07), 700), fill=wh, anchor="mm")
    elif name == "peas":         # barattolo di piselli generico
        d.rectangle([P(.22, .16), P(.78, .89)], fill=(190, 192, 198, 255))
        d.rectangle([P(.22, .30), P(.78, .76)], fill=(60, 120, 64, 255))
        d.ellipse([P(.22, .09), P(.78, .23)], fill=(214, 216, 222, 255), outline=(150, 150, 156, 255), width=S // 60)
        for (x, y) in ((.38, .46), (.50, .44), (.62, .46), (.44, .56), (.56, .56)):
            d.ellipse([P(x - .05, y - .05), P(x + .05, y + .05)], fill=(150, 210, 110, 255))
        d.text(P(.50, .70), "PISELLI", font=font(OSW, int(S * .07), 700), fill=wh, anchor="mm")
    elif name == "tomato":
        d.ellipse([P(.12, .22), P(.88, .92)], fill=TOM + (255,))
        d.ellipse([P(.26, .32), P(.44, .48)], fill=(236, 120, 100, 255))
        for a_ in range(5):
            an = a_ * 2 * math.pi / 5 - math.pi / 2
            d.polygon([P(.50, .24), P(.50 + .22 * math.cos(an - .3), .24 + .12 * math.sin(an - .3)), P(.50 + .30 * math.cos(an), .24 + .16 * math.sin(an))], fill=LEAF + (255,))
        d.rectangle([P(.48, .08), P(.52, .24)], fill=(80, 110, 60, 255))
    elif name == "medal":
        d.polygon([P(.30, .04), P(.46, .04), P(.56, .40), P(.40, .40)], fill=(60, 90, 160, 255))
        d.polygon([P(.70, .04), P(.54, .04), P(.44, .40), P(.60, .40)], fill=(200, 60, 50, 255))
        d.ellipse([P(.22, .38), P(.78, .94)], fill=GOLD + (255,), outline=(150, 110, 40, 255), width=S // 40)
        d.text(P(.50, .66), "1867", font=font(OSW, int(S * .13), 700), fill=(110, 80, 30, 255), anchor="mm")
    elif name == "chain":        # catena che si spezza (default a catena)
        for k in range(4):
            x = .10 + k * .21
            d.ellipse([P(x, .38), P(x + .26, .62)], outline=(180, 182, 190, 255), width=S // 22)
    elif name == "shield_q":     # scudetto generico tricolore senza stemmi
        d.polygon([P(.18, .10), P(.82, .10), P(.82, .50), P(.50, .92), P(.18, .50)], fill=wh)
        d.polygon([P(.18, .10), P(.39, .10), P(.39, .73), P(.18, .50)], fill=(60, 140, 70, 255))
        d.polygon([P(.61, .10), P(.82, .10), P(.82, .50), P(.61, .73)], fill=(200, 50, 46, 255))
        d.line([P(.18, .10), P(.82, .10), P(.82, .50), P(.50, .92), P(.18, .50), P(.18, .10)], fill=(120, 110, 90, 255), width=S // 50)
    elif name == "luxbank":      # sportello con bandierina generica e "LUX"
        d.rectangle([P(.12, .40), P(.88, .90)], fill=(210, 206, 196, 255))
        d.polygon([P(.06, .40), P(.50, .14), P(.94, .40)], fill=(170, 160, 140, 255))
        for x in (.22, .42, .62): d.rectangle([P(x, .48), P(x + .12, .84)], fill=(160, 154, 140, 255))
        d.text(P(.50, .31), "LUX", font=font(OSW, int(S * .10), 700), fill=dk, anchor="mm")
    elif name == "rating_q":     # pagella / giudizio con punto di domanda
        d.rounded_rectangle([P(.14, .08), P(.86, .92)], S // 20, fill=wh, outline=(120, 110, 90, 255), width=S // 60)
        d.text(P(.50, .30), "RATING", font=font(OSW, int(S * .11), 700), fill=dk, anchor="mm")
        d.text(P(.50, .64), "?", font=font(OSW, int(S * .34), 700), fill=RED + (255,), anchor="mm")
    elif name == "pie":          # torta: rischio in un solo paniere
        d.pieslice([P(.08, .08), P(.92, .92)], -90, 200, fill=(200, 60, 50, 255))
        d.pieslice([P(.08, .08), P(.92, .92)], 200, 270, fill=(90, 140, 200, 255))
    elif name == "basket":
        d.polygon([P(.10, .44), P(.90, .44), P(.78, .90), P(.22, .90)], fill=(170, 120, 70, 255))
        for k in range(5): d.line([P(.18 + k * .16, .46), P(.26 + k * .12, .88)], fill=(120, 80, 40, 255), width=S // 40)
        d.arc([P(.22, .06), P(.78, .70)], 180, 360, fill=(120, 80, 40, 255), width=S // 20)
        for (x, c) in ((.32, TOM), (.50, (220, 190, 60)), (.68, LEAF)): d.ellipse([P(x - .1, .30), P(x + .1, .50)], fill=c + (255,))
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _pc3[k] = im
    return im

_prev_icon3 = fx.icon
def _icon3(name, size, color=None):
    if isinstance(name, str):
        m = cpic(name, size)
        if m is not None: return m
    return _prev_icon3(name, size, color)
fx.icon = _icon3

def cover_folder17(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 28, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 017", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "IL CRAC CIRIO", font=font(SERIF, int(w * .09)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "ROMA · 2002-2021", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im

def bond17(w=520, title="OBBLIGAZIONE", lines=("emittente: società del gruppo", "sede: Lussemburgo", "scadenza: novembre 2002"), seed=4):
    h = int(w * 0.66); im = paper(w, h, (226, 216, 190), seed, 0.3); d = ImageDraw.Draw(im)
    d.rectangle([16, 16, w - 16, h - 16], outline=(120, 100, 60, 255), width=4)
    d.text((w / 2, h * .15), title, font=font(SERIF, int(w * .08)), fill=(80, 60, 30, 255), anchor="mm")
    y = h * .30
    for ln in lines:
        d.text((w / 2, y), ln, font=font(COURR, int(w * .040)), fill=INK + (255,), anchor="mm"); y += h * .11
    for k in range(5):
        x = w * .12 + k * w * .158
        d.rectangle([x, h * .66, x + w * .13, h * .84], outline=(150, 120, 70, 255), width=2)
        d.text((x + w * .065, h * .75), "cedola", font=font(COURR, int(w * .026)), fill=(110, 90, 50, 255), anchor="mm")
    recon_label(d, w, h, size=max(14, int(w * 0.03)))
    return im

class DebtShift(El):
    """scenografia ricorrente: due colonne, BANCHE e RISPARMIATORI. N blocchi di debito; shift [(t, quota 0..1)]
    = quota di blocchi passati dalle banche ai risparmiatori (si muovono in arco). zero_t: i blocchi dei risparmiatori
    diventano grigi 'BLOCCATI'. schema semplificato, non in scala."""
    def __init__(self, box, t0, t1=None, shift=((0, 0.0),), zero_t=None, n=10, title="DI CHI È IL DEBITO? · schema semplificato · non in scala"):
        super().__init__(t0, t1, 0.4); self.box, self.shift, self.zero_t, self.n, self.title = box, sorted(shift), zero_t, n, title
    def q(self, t):
        ks = self.shift; v = 0.0; i = -1
        for j, (kt, kv) in enumerate(ks):
            if t >= kt: i = j
        if i < 0: return ks[0][1] if ks[0][0] <= self.t0 else 0.0
        p0 = ks[i - 1][1] if i > 0 else (0.0 if ks[0][0] > self.t0 else ks[0][1])
        kt, kv = ks[i]
        return p0 + (kv - p0) * ease_io(min(1, (t - kt) / 2.0))
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; w, h = x1 - x0, y1 - y0; d = ImageDraw.Draw(lay); al = int(255 * a)
        d.rounded_rectangle([x0, y0, x1, y1], 18, fill=(236, 230, 214, al), outline=(150, 130, 100, al), width=4)
        d.text(((x0 + x1) / 2, y0 + 30), self.title, font=font(COURR, 22), fill=(110, 96, 80, al), anchor="mm")
        lx = x0 + w * .25; rx = x0 + w * .75
        fo = font(OSW, 40, 700)
        d.text((lx, y0 + 80), "BANCHE", font=fo, fill=(60, 80, 130, al), anchor="mm")
        d.text((rx, y0 + 80), "RISPARMIATORI", font=fo, fill=(150, 40, 36, al), anchor="mm")
        base = y1 - 30; bh = (h - 150) / (self.n + 0.5); bw = w * .30
        q = self.q(t) * self.n; moved = int(q); frac = q - moved
        nb = self.n - moved - (1 if frac > 0 else 0)
        for k in range(self.n - moved):
            yy = base - (k + 1) * bh
            if k == self.n - moved - 1 and frac > 0: continue
            d.rounded_rectangle([lx - bw / 2, yy + 3, lx + bw / 2, yy + bh - 3], 6, fill=(90, 110, 160, al), outline=(50, 60, 100, al), width=2)
        zero = self.zero_t is not None and t >= self.zero_t
        col = (130, 126, 120) if zero else (190, 70, 60)
        for k in range(moved):
            yy = base - (k + 1) * bh
            d.rounded_rectangle([rx - bw / 2, yy + 3, rx + bw / 2, yy + bh - 3], 6, fill=col + (al,), outline=(70, 40, 36, al), width=2)
        if frac > 0:   # blocco in volo
            u = ease_io(frac); yA = base - (self.n - moved) * bh; yB = base - (moved + 1) * bh
            xx = lx + (rx - lx) * u; yy = yA + (yB - yA) * u - math.sin(u * math.pi) * h * .25
            d.rounded_rectangle([xx - bw / 2, yy + 3, xx + bw / 2, yy + bh - 3], 6, fill=(200, 140, 60, al), outline=(90, 60, 30, al), width=2)
        d.line([((x0 + x1) / 2, y0 + 110), ((x0 + x1) / 2, y1 - 20)], fill=(150, 130, 100, al), width=3)
        if zero and moved:
            d.text((rx, base - moved * bh / 2), "BLOCCATI", font=font(OSW, 46, 700), fill=WHITE + (al,), anchor="mm")

class GroupTree(El):
    """albero del gruppo: radice in alto, figli che compaiono a tempi diversi. nodes: [(label, t, color)], cut: {indice: t}"""
    def __init__(self, box, root, nodes, t0, t1=None, cut=None, root_t=None, title="IL GRUPPO · schema semplificato"):
        super().__init__(t0, t1, 0.4); self.box, self.root, self.nodes, self.cut, self.root_t, self.title = box, root, nodes, cut or {}, root_t, title
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; d = ImageDraw.Draw(lay); al = int(255 * a); w = x1 - x0
        d.text(((x0 + x1) / 2, y1 - 6), self.title, font=font(COURR, 22), fill=(180, 170, 150, al), anchor="mb")
        rx, ry = (x0 + x1) / 2, y0 + 70
        f = font(OSW, 40, 700); tw = tl(d, self.root, f)
        d.rounded_rectangle([rx - tw / 2 - 26, ry - 40, rx + tw / 2 + 26, ry + 40], 14, fill=(150, 40, 36, al), outline=GOLD + (al,), width=3)
        d.text((rx, ry), self.root, font=f, fill=WHITE + (al,), anchor="mm")
        n = len(self.nodes); fy = y0 + (y1 - y0) * .62; f2 = font(OSW, 32, 600)
        for k, nd in enumerate(self.nodes):
            lab, tt = nd[0], nd[1]; col = nd[2] if len(nd) > 2 else (60, 80, 120)
            if t < tt: continue
            u = ease((t - tt) / 0.4); nx = x0 + w * (k + 0.5) / n
            cut = k in self.cut and t >= self.cut[k]
            lc = (RED if cut else GOLD) + (int(al * u),)
            mx_, my_ = (rx + nx) / 2, (ry + 40 + fy - 50) / 2
            d.line([(rx, ry + 40), (rx, my_), (nx, my_), (nx, fy - 50 * u)], fill=lc, width=4)
            lines = lab.split("\n"); bw_ = max(tl(d, s, f2) for s in lines) + 40; bh_ = 46 * len(lines) + 24
            d.rounded_rectangle([nx - bw_ / 2, fy - 50, nx + bw_ / 2, fy - 50 + bh_], 12, fill=col + (int(al * u),), outline=(230, 220, 200, int(al * u)), width=2)
            for j, s in enumerate(lines):
                d.text((nx, fy - 50 + 34 + j * 46), s, font=f2, fill=WHITE + (int(al * u),), anchor="mm")
            if cut:
                d.line([(nx - 30, my_ - 20), (nx + 30, my_ + 20)], fill=RED + (al,), width=8)
