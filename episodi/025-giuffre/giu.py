# Elementi grafici del caso 025 (il caso Giuffrè, "il banchiere di Dio", 1949-1964): la RETE (scenografia ricorrente:
# l'ufficio di Imola al centro, parrocchie, conventi e famiglie intorno, monete che vanno e vengono), piramide, sportello.
# Tutto disegnato da codice: nessuna foto reale, nessun documento originale, nessun logo.
import math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "023-brinks"))
sys.path.insert(0, os.path.join(HERE, "..", "003-ponzi"))
from brk import *
import brk, fi, fx, pon
from fx import *
from pon import WorldMap, WPL, Pyramid, Office, Growth, Check

WPL.update({"Imola": (11.71, 44.35), "Bologna": (11.34, 44.49), "Ferrara": (11.62, 44.84), "Forlì": (12.04, 44.22),
            "Cesena": (12.24, 44.14), "Rimini": (12.57, 44.06), "Ravenna": (12.20, 44.42), "Ancona": (13.52, 43.62),
            "Macerata": (13.45, 43.30), "Firenze": (11.25, 43.77), "Sesto Fiorentino": (11.20, 43.83),
            "Castel San Pietro": (11.59, 44.40), "Lugo": (11.91, 44.42), "Roma": (12.50, 41.90), "Boston": (-71.06, 42.36)})

def pic(name, size): return fx.icon(name, size)

NODE_IC = ["convent", "priest", "family", "house", "convent", "priest", "family", "house", "convent", "priest", "family", "house"]
NODE_LB = ["CONVENTO", "PARROCO", "FAMIGLIA", "RISPARMIATORE", "CONVENTO", "PARROCO", "FAMIGLIA", "RISPARMIATORE",
           "CONVENTO", "PARROCO", "FAMIGLIA", "RISPARMIATORE"]

class Rete(El):
    """scenografia principale: la rete di Giuffrè. Centro = l'ufficio di Imola; intorno fino a 12 nodi.
    mode: 'rete' (i nodi compaiono) | 'su' (soldi verso il centro) | 'giu' (interessi verso i nodi) |
    'ponzi' (i nodi nuovi pagano i vecchi passando dal centro) | 'stop' (crollo: flussi fermi, croce rossa)"""
    def __init__(self, box, t0, t1=None, n=8, mode="rete", label=None, center="IMOLA", grow=0, title="schema semplificato · non in scala"):
        super().__init__(t0, t1, 0.35)
        self.box, self.n, self.mode, self.label, self.center, self.grow, self.title = box, n, mode, label, center, grow, title
    def pos(self, j, N):
        x0, y0, x1, y1 = self.box; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 10
        ang = -math.pi / 2 + 2 * math.pi * j / N
        return cx + (x1 - x0) * 0.40 * math.cos(ang), cy + (y1 - y0) * 0.36 * math.sin(ang)
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; d = ImageDraw.Draw(lay); al = int(255 * a); k = t - self.t0
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 10
        d.rounded_rectangle([x0, y0, x1, y1], 18, fill=(36, 32, 30, int(170 * a)), outline=(90, 80, 70, al), width=2)
        N = 12; base = self.n - self.grow
        vis = base + min(self.grow, int(k / 0.45) + 1) if self.grow else self.n
        new0 = max(0, self.n - max(3, self.n // 3))
        stop = self.mode == "stop"; cr = ease(min(1.0, k / 1.0)) if stop else 0
        for j in range(vis):
            px, py = self.pos(j, N)
            kk = ease(min(1.0, (k - (j - base) * 0.45) / 0.4)) if (self.grow and j >= base) else 1.0
            col = (120, 112, 102) if stop else (170, 150, 110)
            d.line([(cx, cy), (px, py)], fill=col + (int(al * kk * .8),), width=3)
            # monete
            if not stop:
                go_in = self.mode in ("su",) or (self.mode == "ponzi" and j >= new0)
                go_out = self.mode == "giu" or (self.mode == "ponzi" and j < new0)
                if go_in or go_out:
                    for m in range(2):
                        u = ((k * 0.55 + m / 2 + j * 0.13) % 1.0)
                        if go_out: u = 1 - u
                        mx, my = lerp(px, cx, u), lerp(py, cy, u)
                        place(lay, pic("coin", 40), (mx, my), "mm", a * kk * min(1.0, 4 * min(u, 1 - u) + .2))
            im = pic(NODE_IC[j % 12], 110)
            if stop: im = im.convert("LA").convert("RGBA")
            place(lay, im, (px, py - 12), "mm", a * kk)
            lab = NODE_LB[j % 12]
            if self.mode == "ponzi": lab = "NUOVO" if j >= new0 else "VECCHIO"
            d.text((px, py + 52), lab, font=font(OSW, 24, 600), fill=(GOLD if (self.mode == "ponzi" and j >= new0) else GREY) + (int(al * kk),), anchor="mm")
        # centro: l'ufficio
        d.rounded_rectangle([cx - 120, cy - 80, cx + 120, cy + 80], 14, fill=(60, 44, 30, al), outline=GOLD + (al,), width=4)
        place(lay, pic("desk", 120), (cx, cy - 18), "mm", a)
        d.text((cx, cy + 52), self.center, font=font(OSW, 30, 700), fill=GOLD + (al,), anchor="mm")
        if stop and cr > 0:
            d.line([(cx - 90, cy - 70), (cx + 90, cy + 70)], fill=RED + (int(al * cr),), width=14)
            d.line([(cx + 90, cy - 70), (cx - 90, cy + 70)], fill=RED + (int(al * cr),), width=14)
        d.text(((x0 + x1) / 2, y1 + 22), self.title, font=font(COURR, 22), fill=GREY + (al,), anchor="mm")
        if self.label:
            f = font(OSW, 32, 700); tw = tl(d, self.label, f)
            d.rounded_rectangle([x0 + 16, y0 + 12, x0 + 40 + tw, y0 + 58], 10, fill=(14, 12, 11, int(220 * a)))
            d.text((x0 + 28, y0 + 35), self.label, font=f, fill=GOLD + (al,), anchor="lm")

def cover_folder25(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 38, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 025", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "IL BANCHIERE DI DIO", font=font(SERIF, int(w * .075)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "IMOLA · 1949-1964", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im

def receipt_img(w=640):
    """ricevuta generica (ricostruzione): nessun testo originale, nessuna firma reale"""
    h = int(w * 0.62); im = paper(w, h, (236, 226, 200), 20, 0.5); d = ImageDraw.Draw(im)
    d.text((w / 2, h * .16), "RICEVUTA", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    for j in range(4): d.line([(w * .1, h * (.34 + j * .13)), (w * .9, h * (.34 + j * .13))], fill=(160, 150, 130, 255), width=2)
    d.text((w * .1, h * .30), "Ricevo la somma di Lire ..........", font=font(TYPE, int(w * .045)), fill=INK + (255,), anchor="lb")
    d.text((w * .1, h * .43), "interesse convenuto: .....%", font=font(TYPE, int(w * .045)), fill=INK + (255,), anchor="lb")
    d.line([(w * .55, h * .80), (w * .9, h * .80)], fill=INK + (255,), width=2)
    d.text((w * .72, h * .86), "firma", font=font(TYPE, int(w * .035)), fill=(90, 80, 70, 255), anchor="mm")
    recon_label(d, w, h)
    return im

# ------------------------------------------------------------------ icone del caso
_gk = {}
def gpic(name, size):
    k = (name, size)
    if k in _gk: return _gk[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); lw = max(3, S // 60)
    if name == "priest":        # sacerdote generico (sagoma con talare e colletto)
        d.ellipse([P(.38, .08), P(.62, .32)], fill=(222, 196, 166, 255))
        d.polygon([P(.30, .34), P(.70, .34), P(.78, .94), P(.22, .94)], fill=(30, 28, 30, 255))
        d.rectangle([P(.46, .33), P(.54, .38)], fill=(245, 245, 240, 255))
        for j in range(6): d.ellipse([P(.485, .42 + j * .08), P(.515, .45 + j * .08)], fill=(90, 90, 90, 255))
    elif name == "desk":        # scrivania con registro e mucchio di banconote: l'ufficio
        d.rectangle([P(.08, .52), P(.92, .60)], fill=(120, 80, 46, 255))
        d.rectangle([P(.12, .60), P(.20, .92)], fill=(100, 66, 38, 255)); d.rectangle([P(.80, .60), P(.88, .92)], fill=(100, 66, 38, 255))
        d.polygon([P(.18, .50), P(.48, .50), P(.50, .36), P(.20, .36)], fill=(236, 226, 200, 255), outline=(120, 110, 90, 255))
        for j in range(3): d.line([P(.24, .40 + j * .03), P(.45, .40 + j * .03)], fill=(120, 110, 90, 255), width=lw // 2)
        for j in range(4): d.rectangle([P(.56, .44 - j * .045), P(.84, .50 - j * .045)], fill=(196, 180, 120, 255), outline=(120, 100, 60, 255), width=lw // 2)
        d.text(P(.70, .33), "L.", font=font(SERIF, int(S * .12)), fill=(120, 90, 40, 255), anchor="mm")
    elif name == "urn":         # urna per il voto segreto (senza scritte)
        d.polygon([P(.18, .40), P(.82, .40), P(.74, .92), P(.26, .92)], fill=(200, 196, 186, 255), outline=(110, 106, 100, 255))
        d.rectangle([P(.12, .34), P(.88, .42)], fill=(160, 150, 140, 255))
        d.rectangle([P(.36, .06), P(.64, .36)], fill=(250, 250, 245, 255), outline=(110, 106, 100, 255), width=lw)
        d.line([P(.42, .20), P(.48, .28), P(.60, .12)], fill=(200, 50, 40, 255), width=lw * 2)
    elif name == "villa":       # villa di campagna toscana generica
        d.rectangle([P(.16, .40), P(.84, .88)], fill=(226, 200, 150, 255), outline=(140, 110, 70, 255), width=lw)
        d.polygon([P(.10, .42), P(.50, .18), P(.90, .42)], fill=(170, 80, 50, 255))
        for j in range(3):
            d.rectangle([P(.24 + j * .2, .50), P(.34 + j * .2, .62)], fill=(80, 100, 90, 255))
        d.rectangle([P(.44, .70), P(.56, .88)], fill=(100, 66, 38, 255))
        d.rectangle([P(.02, .86), P(.98, .92)], fill=(90, 130, 70, 255))
        for x in (.04, .92): d.ellipse([P(x - .02, .30), P(x + .06, .86)], fill=(50, 90, 60, 255))
    elif name == "commenda":    # medaglia di onorificenza generica (senza stemmi reali)
        d.polygon([P(.36, .04), P(.50, .04), P(.56, .36), P(.44, .36)], fill=(40, 130, 70, 255))
        d.polygon([P(.50, .04), P(.64, .04), P(.56, .36), P(.44, .36)], fill=(200, 50, 50, 255))
        pts = [P(.5 + .30 * math.cos(math.pi / 2 + j * math.pi / 5) * (1 if j % 2 == 0 else .5), .64 - .30 * math.sin(math.pi / 2 + j * math.pi / 5) * (1 if j % 2 == 0 else .5)) for j in range(10)]
        d.polygon(pts, fill=(220, 180, 70, 255), outline=(140, 100, 30, 255))
    elif name == "receipt":
        r = receipt_img(int(S * .9)); im.alpha_composite(r, (int(S * .05), int(S * .5 - r.height / 2)))
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _gk[k] = im; return im

_prev_icon_g = fx.icon
def _icon_g(name, size, color=None):
    if isinstance(name, str):
        m = gpic(name, size)
        if m is not None: return m
    return _prev_icon_g(name, size, color)
fx.icon = _icon_g
