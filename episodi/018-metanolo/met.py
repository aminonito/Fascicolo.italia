# Elementi grafici del caso 018 (il vino al metanolo, 1986): bottiglioni generici senza marchio, la "filiera" del vino
# (scenografia ricorrente, schema semplificato), il misuratore del metanolo rispetto al limite di legge.
# Tutto disegnato da codice: nessuna foto reale, nessun marchio o etichetta reale, nessun documento originale.
import math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "017-cirio"))
sys.path.insert(0, os.path.join(HERE, "..", "014-wanna-marchi"))
sys.path.insert(0, os.path.join(HERE, "..", "016-pieta"))
from cir import *                       # catena completa (par, urb, rom, mod, car, osp, tor, maj, pon)
import cir, wm
import fi
import fx
from fx import *
import pon
from pon import WorldMap, WPL

WPL.update({"Narzole": (7.87, 44.60), "Incisa Scapaccino": (8.38, 44.80), "Asti": (8.21, 44.90), "Cuneo": (7.55, 44.38),
            "Milano": (9.19, 45.46), "Genova": (8.93, 44.41), "Torino": (7.68, 45.07), "Puglia": (17.0, 40.6),
            "Emilia-Romagna": (11.9, 44.35), "Sète": (3.70, 43.40), "Marsiglia": (5.37, 43.30), "Karlsruhe": (8.40, 49.01),
            "Roma": (12.50, 41.90), "Treviso": (12.24, 45.67), "Washington": (-77.04, 38.90), "Londra": (-0.13, 51.51),
            "Vienna": (16.37, 48.21), "Bonn": (7.10, 50.73), "Liguria": (8.9, 44.3), "Lombardia": (9.6, 45.6),
            "Piemonte": (7.9, 44.9), "Langhe": (8.0, 44.6)})

WINE = (128, 24, 40)
GLASSG = (70, 110, 70)

_pm = {}
def mpic(name, size):
    k = (name, size)
    if k in _pm: return _pm[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); dk = (40, 34, 30, 255); wh = (240, 238, 232, 255)
    if name in ("bottle", "bottle_bad", "bottle_ok"):    # bottiglione da 2 litri generico, nessun marchio
        d.rounded_rectangle([P(.28, .34), P(.72, .96)], S // 12, fill=GLASSG + (255,))
        d.polygon([P(.28, .40), P(.42, .22), P(.58, .22), P(.72, .40)], fill=GLASSG + (255,))
        d.rectangle([P(.43, .06), P(.57, .24)], fill=GLASSG + (255,))
        d.rectangle([P(.42, .03), P(.58, .09)], fill=(180, 150, 100, 255))
        d.rounded_rectangle([P(.30, .46), P(.70, .92)], S // 16, fill=WINE + (255,))
        d.rectangle([P(.33, .55), P(.67, .80)], fill=(236, 228, 206, 255))
        d.text(P(.50, .62), "VINO", font=font(OSW, int(S * .08), 700), fill=WINE + (255,), anchor="mm")
        d.text(P(.50, .72), "DA TAVOLA", font=font(OSW, int(S * .05), 600), fill=dk, anchor="mm")
        d.line([P(.34, .40), P(.34, .90)], fill=(170, 210, 170, 120), width=S // 40)
        if name == "bottle_bad":
            d.ellipse([P(.56, .02), P(.98, .44)], fill=RED + (255,)); d.text(P(.77, .23), "!", font=font(OSW, int(S * .28), 700), fill=wh, anchor="mm")
        if name == "bottle_ok":
            d.ellipse([P(.56, .02), P(.98, .44)], fill=(60, 140, 80, 255)); d.line([P(.66, .23), P(.75, .32), P(.89, .13)], fill=wh, width=S // 22)
    elif name == "wglass":     # bicchiere di vino rosso
        d.chord([P(.22, .04), P(.78, .62)], 0, 180, fill=WINE + (255,))
        d.arc([P(.22, -.24), P(.78, .62)], 0, 180, fill=(220, 220, 228, 255), width=S // 40)
        d.line([P(.22, .19), P(.22, .33)], fill=(220, 220, 228, 255), width=S // 40); d.line([P(.78, .19), P(.78, .33)], fill=(220, 220, 228, 255), width=S // 40)
        d.rectangle([P(.48, .62), P(.52, .88)], fill=(220, 220, 228, 255)); d.ellipse([P(.30, .86), P(.70, .96)], fill=(220, 220, 228, 255))
    elif name == "grapes":
        for (x, y) in ((.38, .34), (.52, .34), (.66, .34), (.45, .48), (.59, .48), (.52, .62), (.31, .48), (.73, .48), (.45, .74), (.59, .74), (.52, .86)):
            d.ellipse([P(x - .09, y - .09), P(x + .09, y + .09)], fill=(110, 40, 90, 255), outline=(70, 20, 60, 255), width=S // 80)
        d.polygon([P(.52, .24), P(.70, .06), P(.86, .16), P(.66, .24)], fill=LEAF + (255,)); d.line([P(.52, .26), P(.50, .10)], fill=(110, 80, 50, 255), width=S // 30)
    elif name == "barrel":
        d.ellipse([P(.16, .12), P(.84, .28)], fill=(150, 100, 60, 255))
        d.polygon([P(.16, .20), P(.10, .55), P(.16, .88), P(.84, .88), P(.90, .55), P(.84, .20)], fill=(160, 105, 60, 255))
        for y in (.30, .78): d.line([P(.12, y), P(.88, y)], fill=(90, 80, 76, 255), width=S // 24)
        for x in (.32, .5, .68): d.line([P(x, .22), P(x, .88)], fill=(130, 85, 48, 255), width=S // 90)
        d.ellipse([P(.16, .80), P(.84, .96)], fill=(130, 85, 48, 255))
    elif name == "tanker":     # autocisterna generica
        d.rounded_rectangle([P(.04, .34), P(.70, .70)], S // 8, fill=(200, 200, 206, 255), outline=(120, 120, 128, 255), width=S // 60)
        d.text(P(.37, .52), "CISTERNA", font=font(OSW, int(S * .07), 700), fill=(90, 90, 98, 255), anchor="mm")
        d.rounded_rectangle([P(.72, .40), P(.96, .74)], S // 30, fill=(180, 50, 40, 255)); d.rectangle([P(.78, .44), P(.92, .56)], fill=(180, 210, 230, 255))
        d.rectangle([P(.04, .70), P(.96, .76)], fill=(60, 60, 66, 255))
        for x in (.16, .34, .56, .84): d.ellipse([P(x - .07, .70), P(x + .07, .84)], fill=dk); d.ellipse([P(x - .03, .74), P(x + .03, .80)], fill=(150, 150, 156, 255))
    elif name == "flask":      # beuta da laboratorio con la formula del metanolo
        d.polygon([P(.40, .06), P(.60, .06), P(.60, .36), P(.86, .88), P(.14, .88), P(.40, .36)], fill=(220, 230, 236, 200), outline=(160, 180, 190, 255))
        d.polygon([P(.30, .58), P(.70, .58), P(.86, .88), P(.14, .88)], fill=(190, 210, 240, 255))
        d.rectangle([P(.37, .02), P(.63, .07)], fill=(160, 180, 190, 255))
        d.text(P(.50, .76), "CH3OH", font=font(OSW, int(S * .11), 700), fill=(40, 60, 110, 255), anchor="mm")
    elif name == "sugar":      # sacco di zucchero
        d.polygon([P(.20, .22), P(.80, .22), P(.86, .92), P(.14, .92)], fill=(236, 230, 214, 255), outline=(170, 160, 140, 255))
        d.polygon([P(.20, .22), P(.34, .08), P(.66, .08), P(.80, .22)], fill=(220, 212, 190, 255))
        d.text(P(.50, .58), "ZUCCHERO", font=font(OSW, int(S * .09), 700), fill=dk, anchor="mm")
        for (x, y) in ((.3, .96), (.5, .97), (.7, .95)): d.rectangle([P(x - .02, y - .02), P(x + .02, y + .02)], fill=wh)
    elif name == "tubes":      # provette di analisi
        for j, (x, c) in enumerate(((.26, WINE), (.50, (150, 30, 50)), (.74, (110, 20, 40)))):
            d.rounded_rectangle([P(x - .08, .10), P(x + .08, .88)], S // 14, fill=(230, 236, 240, 200), outline=(160, 180, 190, 255), width=S // 80)
            d.rounded_rectangle([P(x - .07, .46 + j * .06), P(x + .07, .87)], S // 16, fill=c + (255,))
        d.rectangle([P(.10, .62), P(.90, .68)], fill=(140, 110, 70, 255))
    elif name == "tax":        # tassa: moneta con la scritta IMPOSTA
        d.ellipse([P(.12, .12), P(.88, .88)], fill=GOLD + (255,), outline=(150, 110, 40, 255), width=S // 30)
        d.text(P(.50, .50), "IMPOSTA", font=font(OSW, int(S * .12), 700), fill=(110, 80, 30, 255), anchor="mm")
    elif name == "notax":
        d.ellipse([P(.12, .12), P(.88, .88)], fill=GOLD + (255,), outline=(150, 110, 40, 255), width=S // 30)
        d.text(P(.50, .50), "IMPOSTA", font=font(OSW, int(S * .12), 700), fill=(110, 80, 30, 255), anchor="mm")
        d.line([P(.18, .82), P(.82, .18)], fill=RED + (255,), width=S // 12)
    elif name == "hospital2":
        d.rectangle([P(.12, .30), P(.88, .94)], fill=(230, 232, 236, 255), outline=(150, 150, 160, 255), width=S // 60)
        d.rectangle([P(.40, .06), P(.60, .30)], fill=(230, 232, 236, 255))
        d.rectangle([P(.46, .10), P(.54, .26)], fill=RED + (255,)); d.rectangle([P(.42, .14), P(.58, .22)], fill=RED + (255,))
        for x in (.22, .42, .62):
            for y in (.40, .58): d.rectangle([P(x, y), P(x + .14, y + .12)], fill=(150, 190, 220, 255))
        d.rectangle([P(.42, .76), P(.58, .94)], fill=(110, 90, 70, 255))
    elif name == "eye_x":      # occhio barrato (la vista)
        d.ellipse([P(.06, .28), P(.94, .72)], fill=wh, outline=dk, width=S // 40)
        d.ellipse([P(.36, .32), P(.64, .68)], fill=(90, 70, 50, 255)); d.ellipse([P(.45, .42), P(.55, .58)], fill=dk)
        d.line([P(.14, .86), P(.86, .14)], fill=RED + (255,), width=S // 14)
    elif name == "lorry_wine": # bottiglioni sugli scaffali del supermercato
        d.rectangle([P(.04, .10), P(.96, .92)], fill=(200, 190, 170, 255), outline=(120, 110, 90, 255), width=S // 60)
        for y in (.40, .70): d.rectangle([P(.04, y), P(.96, y + .04)], fill=(120, 110, 90, 255))
        for row, y in enumerate((.14, .44)):
            for j in range(5):
                x = .10 + j * .17
                d.rounded_rectangle([P(x, y + .08), P(x + .12, y + .26)], S // 50, fill=GLASSG + (255,)); d.rectangle([P(x + .04, y), P(x + .08, y + .09)], fill=GLASSG + (255,))
                d.rectangle([P(x + .01, y + .14), P(x + .11, y + .20)], fill=(236, 228, 206, 255))
        d.text(P(.50, .82), "VINO DA TAVOLA", font=font(OSW, int(S * .07), 700), fill=dk, anchor="mm")
    elif name == "river_red":  # fiume che si tinge di rosso
        d.rectangle([P(0, 0), P(1, 1)], fill=(110, 140, 90, 255))
        d.polygon([P(.30, 0), P(.55, 0), P(.70, .5), P(.60, 1), P(.32, 1), P(.44, .5)], fill=(80, 120, 170, 255))
        d.polygon([P(.44, .5), P(.70, .5), P(.60, 1), P(.32, 1)], fill=WINE + (255,))
    elif name == "certificate":
        d.rectangle([P(.14, .06), P(.86, .94)], fill=(236, 230, 214, 255), outline=(150, 130, 100, 255), width=S // 50)
        d.text(P(.50, .18), "CERTIFICATO", font=font(OSW, int(S * .08), 700), fill=dk, anchor="mm")
        for y in (.32, .42, .52, .62): d.line([P(.24, y), P(.76, y)], fill=(160, 150, 130, 255), width=S // 90)
        d.ellipse([P(.54, .66), P(.80, .90)], fill=(60, 140, 80, 255)); d.line([P(.60, .78), P(.66, .84), P(.75, .72)], fill=wh, width=S // 40)
    elif name == "register":   # anagrafe vitivinicola: schedario
        d.rectangle([P(.10, .20), P(.90, .92)], fill=(150, 120, 80, 255))
        for j, y in enumerate((.26, .50, .74)):
            d.rectangle([P(.16, y), P(.84, y + .18)], fill=(190, 160, 110, 255)); d.rectangle([P(.42, y + .06), P(.58, y + .11)], fill=(90, 70, 40, 255))
        d.rectangle([P(.30, .06), P(.70, .20)], fill=(236, 230, 214, 255)); d.text(P(.50, .13), "ANAGRAFE", font=font(OSW, int(S * .06), 700), fill=dk, anchor="mm")
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _pm[k] = im
    return im

_prev_icon_m = fx.icon
def _icon_m(name, size, color=None):
    if isinstance(name, str):
        m = mpic(name, size)
        if m is not None: return m
    return _prev_icon_m(name, size, color)
fx.icon = _icon_m

def cover_folder18(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 28, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 018", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "IL VINO AL METANOLO", font=font(SERIF, int(w * .075)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "MILANO · 1986-1992", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im

STEPS = [("metanolo", "flask", "IL METANOLO"), ("cantina", "barrel", "LA CANTINA"), ("imbottigliatore", "bottle", "L'IMBOTTIGLIATORE"),
         ("negozio", "lorry_wine", "IL SUPERMERCATO"), ("tavola", "wglass", "LA TAVOLA")]

class Filiera(El):
    """scenografia ricorrente: la catena del vino da tavola (metanolo -> cantina -> imbottigliatore -> supermercato -> tavola).
    upto: quante tappe sono visibili; bad: da quale tappa in poi il percorso diventa rosso (None = nessuna);
    hl: tappa evidenziata; flow_t: istante in cui parte il bottiglione che scorre lungo la catena. schema semplificato."""
    def __init__(self, box, t0, t1=None, upto=5, bad=None, hl=None, flow_t=None, cut=None, title="LA FILIERA · schema semplificato · non in scala"):
        super().__init__(t0, t1, 0.4); self.box, self.upto, self.bad, self.hl, self.flow_t, self.cut, self.title = box, upto, bad, hl, flow_t, cut, title
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; d = ImageDraw.Draw(lay); al = int(255 * a); n = len(STEPS)
        d.rounded_rectangle([x0, y0, x1, y1], 18, fill=(30, 26, 24, int(200 * a)), outline=(120, 100, 80, al), width=3)
        d.text(((x0 + x1) / 2, y1 - 22), self.title, font=font(COURR, 22), fill=(180, 170, 150, al), anchor="mm")
        cy = y0 + (y1 - y0) * 0.44; xs = [x0 + (x1 - x0) * (j + 0.5) / n for j in range(n)]
        sz = int(min(200, (x1 - x0) / n * 0.62))
        for j in range(min(self.upto, n) - 1):
            tt = self.t0 + 0.25 * (j + 1)
            if t < tt: continue
            u = ease((t - tt) / 0.4); bad = self.bad is not None and j >= self.bad
            col = (200, 50, 40) if bad else (150, 130, 100)
            xa, xb = xs[j] + sz * 0.55, xs[j + 1] - sz * 0.55
            d.line([(xa, cy), (xa + (xb - xa) * u, cy)], fill=col + (al,), width=10)
            if u > 0.9: d.polygon([(xb, cy), (xb - 22, cy - 16), (xb - 22, cy + 16)], fill=col + (al,))
            if self.cut is not None and j == self.cut:
                xm = (xa + xb) / 2; d.line([(xm - 30, cy - 40), (xm + 30, cy + 40)], fill=RED + (al,), width=12); d.line([(xm - 30, cy + 40), (xm + 30, cy - 40)], fill=RED + (al,), width=12)
        for j, (key, ic, lab) in enumerate(STEPS[:self.upto]):
            tt = self.t0 + 0.25 * j
            if t < tt: continue
            u = back(min(1, (t - tt) / 0.35)); s = max(4, int(sz * u))
            if self.hl == j:
                r = sz * 0.68 + 6 * math.sin(t * 6)
                d.ellipse([xs[j] - r, cy - r, xs[j] + r, cy + r], outline=GOLD + (al,), width=6)
            im = fx.icon(ic, sz)
            if s != sz: im = im.resize((s, s), Image.BILINEAR)
            place(lay, im, (xs[j], cy), "mm", a)
            bad = self.bad is not None and j >= self.bad + 1
            f = font(OSW, 30, 600); tw = tl(d, lab, f); ly = cy + sz * 0.5 + 40
            d.rounded_rectangle([xs[j] - tw / 2 - 12, ly - 22, xs[j] + tw / 2 + 12, ly + 22], 10, fill=((150, 40, 36) if bad else (14, 12, 11)) + (int(220 * a),))
            d.text((xs[j], ly), lab, font=f, fill=WHITE + (al,), anchor="mm")
        if self.flow_t is not None and t > self.flow_t:
            u = min(1.0, (t - self.flow_t) / 3.0); pos = u * (min(self.upto, n) - 1)
            jx = int(pos); fr = pos - jx
            xx = xs[jx] + (xs[min(jx + 1, n - 1)] - xs[jx]) * fr if jx < n - 1 else xs[-1]
            place(lay, fx.icon("bottle_bad" if self.bad is not None else "bottle", int(sz * 0.5)), (xx, cy - sz * 0.75), "mm", a)

class Gauge(El):
    """misuratore del metanolo: barra con la soglia di legge (0,3) e il valore misurato che sale.
    keys [(t, valore)] in 'per cento' indicativo; vmax = fondo scala. schema semplificato, valori come detti nel video."""
    def __init__(self, box, keys, t0, t1=None, limit=0.3, vmax=6.0, unit="%", title="METANOLO NEL VINO · schema semplificato", labels=None):
        super().__init__(t0, t1, 0.3); self.box, self.keys, self.limit, self.vmax, self.unit, self.title = box, sorted(keys), limit, vmax, unit, title
        self.labels = labels or {}
    def val(self, t):
        v = 0.0; prev = (self.t0, 0.0)
        for kt, kv in self.keys:
            if t >= kt: v0 = prev[1]; v = v0 + (kv - v0) * ease_io(min(1, (t - kt) / 1.2)); prev = (kt, kv)
        return v
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; d = ImageDraw.Draw(lay); al = int(255 * a)
        d.rounded_rectangle([x0, y0, x1, y1], 18, fill=(236, 230, 214, al), outline=(150, 130, 100, al), width=4)
        d.text(((x0 + x1) / 2, y0 + 34), self.title, font=font(COURR, 24), fill=(110, 96, 80, al), anchor="mm")
        bx0, bx1 = x0 + 80, x1 - 80; by0, by1 = y0 + (y1 - y0) * 0.42, y0 + (y1 - y0) * 0.62
        d.rounded_rectangle([bx0, by0, bx1, by1], 14, fill=(210, 204, 190, al), outline=(120, 110, 90, al), width=3)
        v = self.val(t); f = max(0.0, min(1.0, v / self.vmax))
        col = (60, 140, 80) if v <= self.limit else (200, 50, 40)
        if f > 0.002: d.rounded_rectangle([bx0 + 4, by0 + 4, bx0 + 4 + (bx1 - bx0 - 8) * f, by1 - 4], 12, fill=col + (al,))
        lx = bx0 + (bx1 - bx0) * self.limit / self.vmax
        d.line([(lx, by0 - 40), (lx, by1 + 40)], fill=INK + (al,), width=6)
        d.text((lx, by0 - 52), f"LIMITE {str(self.limit).replace('.', ',')}{self.unit}", font=font(OSW, 34, 700), fill=INK + (al,), anchor="mb")
        if v > 0.001:
            txt = f"{v:.1f}".replace(".", ",") + self.unit
            d.text((bx0 + (bx1 - bx0) * f, by1 + 30), txt, font=font(OSW, 60, 700), fill=col + (al,), anchor="mt")
        for xv, lab in self.labels.items():
            xx = bx0 + (bx1 - bx0) * xv / self.vmax
            d.text((xx, y1 - 30), lab, font=font(COURR, 24), fill=(90, 80, 70, al), anchor="mm")

def sentence18(lines, w=640, title="SENTENZA DI PRIMO GRADO · 1992", seed=41):
    return label_card(lines, w, title=title, seed=seed)
