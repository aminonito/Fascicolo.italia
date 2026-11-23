# Elementi grafici del caso 022 (biblioteca dei Girolamini, Napoli 2011-2026): libri antichi stilizzati, scaffali,
# la SALA della biblioteca (scenografia ricorrente che si svuota), il libro della Luna (schema, non l'originale),
# catalogo d'asta, sigilli. Tutto disegnato da codice: nessuna foto reale, nessun logo, nessun documento originale.
import math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "021-barilla"))
from bar import *
import bar, tot, euf, met, fi, fx, pon
from fx import *
from pon import WorldMap, WPL

WPL.update({"Napoli": (14.27, 40.85), "Verona": (10.99, 45.44), "Monaco di Baviera": (11.58, 48.14), "Montecassino": (13.81, 41.49),
            "New York": (-74.00, 40.71), "Venezia": (12.33, 45.44), "Roma": (12.50, 41.90), "Londra": (-0.13, 51.51),
            "Cesena": (12.24, 44.14), "Milano": (9.19, 45.46)})

LEATHER = [(120, 62, 40), (90, 50, 36), (140, 96, 52), (70, 60, 48), (110, 40, 36), (150, 120, 80), (60, 70, 60)]
_pg = {}
def gpic(name, size):
    k = (name, size)
    if k in _pg: return _pg[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); lw = max(3, S // 70)
    gold = (214, 178, 92, 255)
    def spine(x0, y0, x1, y1, col):
        d.rectangle([P(x0, y0), P(x1, y1)], fill=col + (255,), outline=(30, 20, 14, 255), width=max(1, lw // 2))
        for yy in (y0 + (y1 - y0) * .18, y0 + (y1 - y0) * .82):
            d.line([P(x0, yy), P(x1, yy)], fill=gold, width=max(1, lw // 2))
    if name == "oldbook":              # libro antico rilegato in pelle, di tre quarti
        d.polygon([P(.22, .14), P(.74, .10), P(.80, .86), P(.28, .90)], fill=(110, 62, 40, 255), outline=(40, 24, 16, 255))
        d.polygon([P(.74, .10), P(.82, .14), P(.88, .88), P(.80, .86)], fill=(236, 226, 200, 255))
        for j in range(6): d.line([P(.78 + j * .012, .14), P(.84 + j * .008, .86)], fill=(200, 188, 160, 255), width=1)
        d.rectangle([P(.34, .30), P(.66, .46)], outline=gold, width=lw)
        d.line([P(.26, .22), P(.76, .19)], fill=gold, width=lw); d.line([P(.30, .80), P(.79, .77)], fill=gold, width=lw)
    elif name == "openbook":           # libro aperto con righe di testo
        d.polygon([P(.06, .26), P(.50, .32), P(.50, .86), P(.06, .78)], fill=(240, 232, 210, 255), outline=(90, 70, 50, 255))
        d.polygon([P(.94, .26), P(.50, .32), P(.50, .86), P(.94, .78)], fill=(234, 226, 204, 255), outline=(90, 70, 50, 255))
        for j in range(8):
            y = .36 + j * .052
            d.line([P(.12, y), P(.44, y + .02)], fill=(110, 100, 90, 255), width=max(1, lw // 2))
            d.line([P(.56, y + .02), P(.88, y)], fill=(110, 100, 90, 255), width=max(1, lw // 2))
    elif name in ("shelf", "shelf_gaps"):  # scaffale pieno o con vuoti
        d.rectangle([P(.10, .06), P(.90, .94)], fill=(84, 54, 32, 255))
        rr = random.Random(3)
        for r in range(4):
            y0, y1 = .10 + r * .21, .28 + r * .21
            d.rectangle([P(.14, y0), P(.86, y1)], fill=(40, 26, 18, 255))
            x = .15
            while x < .84:
                w = rr.uniform(.03, .055); gap = (name == "shelf_gaps" and rr.random() < .45)
                if not gap: spine(x, y0 + rr.uniform(0, .03), min(.85, x + w), y1, rr.choice(LEATHER))
                x += w + .004
            d.rectangle([P(.12, y1), P(.88, y1 + .02)], fill=(110, 74, 44, 255))
    elif name == "boxbooks":           # scatola di cartone con libri
        d.polygon([P(.12, .40), P(.88, .40), P(.84, .90), P(.16, .90)], fill=(190, 150, 96, 255), outline=(110, 80, 40, 255))
        for j, col in enumerate(LEATHER[:5]):
            x = .20 + j * .12
            d.rectangle([P(x, .18 + (j % 2) * .06), P(x + .10, .44)], fill=col + (255,), outline=(30, 20, 14, 255))
        d.polygon([P(.12, .40), P(.88, .40), P(.94, .30), P(.06, .30)], fill=(206, 168, 110, 255))
    elif name == "libstamp":           # timbro di biblioteca generico (cerchio con «BIBL.»)
        d.ellipse([P(.14, .14), P(.86, .86)], outline=(150, 40, 60, 255), width=lw * 2)
        d.ellipse([P(.24, .24), P(.76, .76)], outline=(150, 40, 60, 255), width=lw)
        d.text(P(.50, .50), "BIBL.", font=font(OSW, int(S * .14), 700), fill=(150, 40, 60, 255), anchor="mm")
    elif name == "libstamp_x":         # timbro raschiato
        d.ellipse([P(.14, .14), P(.86, .86)], outline=(150, 40, 60, 140), width=lw * 2)
        d.text(P(.50, .50), "BIBL.", font=font(OSW, int(S * .14), 700), fill=(150, 40, 60, 120), anchor="mm")
        rr = random.Random(9)
        for j in range(26):
            y = rr.uniform(.2, .8); d.line([P(.12, y), P(.88, y + rr.uniform(-.05, .05))], fill=(236, 228, 210, 255), width=lw)
    elif name == "moonbook":           # libro aperto con fasi lunari ad acquerello (schema, non l'originale)
        d.polygon([P(.04, .24), P(.50, .30), P(.50, .86), P(.04, .80)], fill=(238, 228, 200, 255), outline=(90, 70, 50, 255))
        d.polygon([P(.96, .24), P(.50, .30), P(.50, .86), P(.96, .80)], fill=(232, 222, 196, 255), outline=(90, 70, 50, 255))
        for j, (cx, cy) in enumerate(((.17, .42), (.37, .62), (.63, .46), (.83, .66))):
            r = .08
            R_ = int(r * S); mm = Image.new("L", (2 * R_, 2 * R_), 0); ImageDraw.Draw(mm).ellipse([0, 0, 2 * R_ - 1, 2 * R_ - 1], fill=255)
            mo = Image.new("RGBA", (2 * R_, 2 * R_), (90, 84, 96, 255)); md = ImageDraw.Draw(mo)
            off = int((-1.1, -.45, .45, 1.1)[j] * R_)
            md.ellipse([off, 0, off + 2 * R_ - 1, 2 * R_ - 1], fill=(232, 220, 186, 255))
            im.paste(mo, (int(cx * S) - R_, int(cy * S) - R_), mm)
            d.ellipse([P(cx - r, cy - r), P(cx + r, cy + r)], outline=(80, 70, 60, 255), width=max(1, lw // 2))
    elif name == "telescope":
        d.polygon([P(.14, .52), P(.78, .22), P(.84, .34), P(.20, .64)], fill=(150, 110, 60, 255), outline=(60, 40, 20, 255))
        d.polygon([P(.76, .20), P(.90, .14), P(.94, .26), P(.82, .34)], fill=(110, 80, 40, 255))
        d.line([P(.46, .44), P(.30, .90)], fill=(80, 60, 40, 255), width=lw); d.line([P(.46, .44), P(.62, .90)], fill=(80, 60, 40, 255), width=lw)
        d.line([P(.46, .44), P(.48, .92)], fill=(80, 60, 40, 255), width=lw)
    elif name == "jupiter":            # Giove e quattro satelliti
        d.ellipse([P(.40, .40), P(.60, .60)], fill=(220, 190, 150, 255))
        d.line([P(.40, .47), P(.60, .47)], fill=(170, 120, 80, 255), width=lw); d.line([P(.41, .54), P(.59, .54)], fill=(170, 120, 80, 255), width=lw)
        for x in (.12, .26, .72, .86): d.ellipse([P(x - .025, .475), P(x + .025, .525)], fill=(240, 240, 240, 255))
        d.line([P(.06, .50), P(.94, .50)], fill=(120, 120, 140, 120), width=1)
    elif name == "moon":
        d.ellipse([P(.18, .18), P(.82, .82)], fill=(214, 210, 196, 255))
        rr = random.Random(4)
        for j in range(9):
            x, y, r = rr.uniform(.3, .7), rr.uniform(.3, .7), rr.uniform(.03, .07)
            d.ellipse([P(x - r, y - r), P(x + r, y + r)], fill=(170, 166, 152, 255))
    elif name == "seal":               # porta con nastro di sequestro
        d.rectangle([P(.24, .10), P(.76, .92)], fill=(96, 64, 40, 255), outline=(40, 26, 16, 255), width=lw)
        d.rectangle([P(.30, .16), P(.70, .48)], outline=(60, 40, 24, 255), width=lw); d.rectangle([P(.30, .54), P(.70, .86)], outline=(60, 40, 24, 255), width=lw)
        for a_, b_ in (((.10, .30), (.90, .62)), ((.10, .62), (.90, .30))):
            d.line([P(*a_), P(*b_)], fill=(230, 60, 50, 255), width=lw * 4)
        d.rounded_rectangle([P(.30, .40), P(.70, .52)], 8, fill=(240, 236, 226, 255))
        d.text(P(.50, .46), "SEQUESTRO", font=font(OSW, int(S * .06), 700), fill=(160, 30, 30, 255), anchor="mm")
    elif name == "petition":           # foglio con firme
        d.rectangle([P(.20, .08), P(.80, .92)], fill=(244, 240, 230, 255), outline=(120, 110, 100, 255), width=lw)
        d.text(P(.50, .17), "PETIZIONE", font=font(OSW, int(S * .07), 700), fill=(40, 36, 32, 255), anchor="mm")
        rr = random.Random(2)
        for j in range(11):
            y = .28 + j * .055; pts = [P(.28 + u * .44, y + .012 * math.sin(u * 12 + j)) for u in [q / 12 for q in range(int(rr.uniform(6, 13)))]]
            if len(pts) > 1: d.line(pts, fill=(40, 60, 130, 255), width=max(1, lw // 2))
    elif name == "catalog":            # catalogo d'asta generico
        d.rectangle([P(.18, .08), P(.82, .92)], fill=(30, 40, 60, 255), outline=(20, 20, 30, 255), width=lw)
        d.text(P(.50, .24), "ASTA", font=font(OSW, int(S * .12), 700), fill=gold, anchor="mm")
        d.text(P(.50, .36), "LIBRI ANTICHI", font=font(OSW, int(S * .06), 600), fill=(220, 220, 220, 255), anchor="mm")
        for j in range(5):
            y = .48 + j * .08
            d.rectangle([P(.26, y), P(.36, y + .05)], fill=(200, 190, 170, 255))
            d.line([P(.40, y + .025), P(.74, y + .025)], fill=(160, 160, 170, 255), width=max(1, lw // 2))
    elif name == "lots":               # lotti ritirati
        d.rectangle([P(.14, .10), P(.86, .90)], fill=(244, 240, 230, 255), outline=(120, 110, 100, 255), width=lw)
        for j in range(8):
            y = .18 + j * .09
            d.text(P(.20, y), f"LOTTO {100 + j * 7}", font=font(COURR, int(S * .05)), fill=(40, 36, 32, 255), anchor="lm")
            d.line([P(.18, y), P(.80, y)], fill=(200, 40, 40, 255), width=lw)
    elif name == "facsimile":          # libro vecchio = libro nuovo (facsimile)
        d.rectangle([P(.06, .26), P(.42, .78)], fill=(236, 226, 196, 255), outline=(90, 70, 50, 255), width=lw)
        d.rectangle([P(.58, .26), P(.94, .78)], fill=(250, 248, 240, 255), outline=(90, 90, 100, 255), width=lw)
        d.text(P(.24, .52), "1610", font=font(OSW, int(S * .09), 700), fill=(90, 70, 50, 255), anchor="mm")
        d.text(P(.76, .52), "1964", font=font(OSW, int(S * .09), 700), fill=(60, 60, 80, 255), anchor="mm")
        d.text(P(.50, .52), "≠", font=font(OSW, int(S * .12), 700), fill=RED + (255,), anchor="mm")
    elif name == "blot":               # frontespizio con macchiolina cerchiata
        d.rectangle([P(.18, .08), P(.82, .92)], fill=(238, 228, 200, 255), outline=(90, 70, 50, 255), width=lw)
        for j in range(4): d.line([P(.30, .20 + j * .07), P(.70, .20 + j * .07)], fill=(90, 80, 70, 255), width=lw)
        d.ellipse([P(.46, .56), P(.50, .60)], fill=(30, 26, 22, 255))
        d.ellipse([P(.36, .46), P(.60, .70)], outline=RED + (255,), width=lw)
        for j in range(3): d.line([P(.30, .76 + j * .05), P(.70, .76 + j * .05)], fill=(90, 80, 70, 255), width=max(1, lw // 2))
    elif name == "abbey":              # abbazia su un colle (schema)
        d.polygon([P(.02, .92), P(.30, .58), P(.56, .66), P(.98, .92)], fill=(90, 120, 80, 255))
        d.rectangle([P(.26, .40), P(.76, .66)], fill=(230, 226, 214, 255), outline=(120, 110, 100, 255), width=lw)
        for j in range(6): d.rectangle([P(.30 + j * .075, .46), P(.34 + j * .075, .56)], fill=(90, 90, 100, 255))
        d.polygon([P(.44, .40), P(.51, .26), P(.58, .40)], fill=(200, 190, 170, 255))
    elif name == "library":            # facciata con colonne e libro
        d.polygon([P(.10, .30), P(.50, .10), P(.90, .30)], fill=(214, 200, 170, 255))
        d.rectangle([P(.12, .30), P(.88, .86)], fill=(236, 226, 200, 255))
        for j in range(5): d.rectangle([P(.18 + j * .15, .36), P(.24 + j * .15, .82)], fill=(206, 192, 160, 255))
        d.rectangle([P(.10, .84), P(.90, .92)], fill=(190, 176, 146, 255))
    elif name == "keys":
        for j, (x, y, r) in enumerate(((.36, .32, .14), (.60, .40, .12))):
            d.ellipse([P(x - r, y - r), P(x + r, y + r)], outline=gold, width=lw * 2)
            d.line([P(x, y + r), P(x + .02, .86)], fill=gold, width=lw * 2)
            d.line([P(x + .02, .74), P(x + .10, .74)], fill=gold, width=lw * 2); d.line([P(x + .02, .82), P(x + .08, .82)], fill=gold, width=lw * 2)
    elif name == "window":             # finestra intatta
        d.rectangle([P(.20, .10), P(.80, .90)], fill=(110, 80, 50, 255))
        d.rectangle([P(.26, .16), P(.74, .84)], fill=(150, 190, 220, 255))
        d.line([P(.50, .16), P(.50, .84)], fill=(110, 80, 50, 255), width=lw * 2); d.line([P(.26, .50), P(.74, .50)], fill=(110, 80, 50, 255), width=lw * 2)
    elif name == "music":              # spartito con note
        d.rectangle([P(.12, .16), P(.88, .84)], fill=(244, 238, 222, 255), outline=(120, 110, 100, 255), width=lw)
        for g in range(2):
            for j in range(5): d.line([P(.18, .26 + g * .30 + j * .04), P(.82, .26 + g * .30 + j * .04)], fill=(60, 56, 50, 255), width=max(1, lw // 2))
            for j, (x, y) in enumerate(((.28, .34), (.42, .30), (.56, .38), (.70, .32))):
                yy = y + g * .30; d.ellipse([P(x - .03, yy - .02), P(x + .03, yy + .02)], fill=(30, 26, 22, 255)); d.line([P(x + .03, yy), P(x + .03, yy - .12)], fill=(30, 26, 22, 255), width=lw)
    elif name == "stars":              # cielo stellato / Via Lattea
        d.ellipse([P(.04, .04), P(.96, .96)], fill=(16, 22, 48, 255))
        rr = random.Random(11)
        for j in range(160):
            u = rr.random(); x = .12 + u * .76; y = .80 - u * .60 + rr.gauss(0, .07)
            r = rr.uniform(.004, .012); d.ellipse([P(x - r, y - r), P(x + r, y + r)], fill=(240, 240, 220, 255))
    elif name == "front":              # due edifici uno di fronte all'altro
        d.rectangle([P(.06, .40), P(.38, .86)], fill=(214, 200, 170, 255)); d.polygon([P(.06, .40), P(.22, .24), P(.38, .40)], fill=(190, 176, 146, 255))
        d.rectangle([P(.62, .40), P(.94, .86)], fill=(214, 200, 170, 255)); d.polygon([P(.62, .40), P(.78, .24), P(.94, .40)], fill=(190, 176, 146, 255))
        d.line([P(.40, .62), P(.60, .62)], fill=RED + (255,), width=lw * 2); d.polygon([P(.60, .58), P(.60, .66), P(.66, .62)], fill=RED + (255,))
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _pg[k] = im
    return im

_prev_icon_g = fx.icon
def _icon_g(name, size, color=None):
    if isinstance(name, str):
        m = gpic(name, size)
        if m is not None: return m
    return _prev_icon_g(name, size, color)
fx.icon = _icon_g

def cover_folder22(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 38, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 022", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "IL BIBLIOTECARIO", font=font(SERIF, int(w * .085)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "NAPOLI · 2011-2026", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im

class Sala(El):
    """scenografia ricorrente: la sala storica della biblioteca (schema). Gli scaffali si svuotano secondo 'fill' (0-1).
    mode: 'day' sala illuminata; 'night' buio, finestra con la luna, scatole che escono verso la porta;
    'mess' libri a terra; 'seized' nastro di sequestro; 'open' riapertura con visitatori."""
    def __init__(self, box, t0, t1=None, mode="day", fill=1.0, fill_to=None, label=None, dur=4.0,
                 title="LA SALA · schema semplificato · non in scala"):
        super().__init__(t0, t1, 0.35); self.box, self.mode, self.fill, self.fill_to, self.label, self.dur, self.title = box, mode, fill, fill_to, label, dur, title
        rr = random.Random(22); self.books = []
        x0, y0, x1, y1 = box; self.cases = []
        nb = 5; cw = (x1 - x0 - 120) / nb
        for c in range(nb):
            cx0 = x0 + 60 + c * cw + 14; cx1 = cx0 + cw - 28
            self.cases.append((cx0, cx1))
            for r in range(5):
                sy0 = y0 + 90 + r * 74; sy1 = sy0 + 60; x = cx0 + 10
                while x < cx1 - 14:
                    w = rr.uniform(9, 17); hgt = rr.uniform(40, 58)
                    self.books.append((x, sy1 - hgt, x + w, sy1, rr.choice(LEATHER), rr.random()))
                    x += w + 1.5
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; d = ImageDraw.Draw(lay); al = int(255 * a); k = t - self.t0
        dark = self.mode == "night"
        d.rectangle([x0, y0, x1, y1], fill=((40, 34, 30) if dark else (196, 176, 140)) + (al,))
        # volta e cornice
        d.rectangle([x0, y0, x1, y0 + 60], fill=((30, 26, 24) if dark else (226, 210, 176)) + (al,))
        d.rectangle([x0, y1 - 70, x1, y1], fill=((50, 40, 34) if dark else (150, 110, 74)) + (al,))
        for j in range(int((x1 - x0) / 60)):
            d.line([(x0 + j * 60, y1 - 70), (x0 + j * 60 + 30, y1)], fill=((60, 48, 40) if dark else (130, 94, 60)) + (al,), width=2)
        fl = self.fill if self.fill_to is None else lerp(self.fill, self.fill_to, ease(min(1, k / self.dur)))
        for cx0, cx1 in self.cases:
            d.rectangle([cx0, y0 + 76, cx1, y0 + 90 + 5 * 74], fill=((50, 34, 22) if dark else (92, 60, 36)) + (al,))
            for r in range(5):
                sy1 = y0 + 90 + r * 74 + 60
                d.rectangle([cx0, sy1, cx1, sy1 + 8], fill=((70, 50, 34) if dark else (120, 80, 48)) + (al,))
        for bx0, by0, bx1, by1, col, rnd in self.books:
            if rnd > fl: continue
            c = tuple(int(v * (0.45 if dark else 1)) for v in col)
            d.rectangle([bx0, by0, bx1, by1], fill=c + (al,))
            d.line([(bx0, by0 + 8), (bx1, by0 + 8)], fill=(214, 178, 92, int(al * (0.4 if dark else 0.9))), width=1)
        m = self.mode
        if m == "night":
            wx = x1 - 170; d.rectangle([wx, y0 + 80, wx + 110, y0 + 230], fill=(20, 30, 60, al))
            d.ellipse([wx + 30, y0 + 105, wx + 80, y0 + 155], fill=(230, 226, 200, al))
            for j in range(3):
                u = ((k * 0.35 + j / 3) % 1.0)
                bx = lerp(x0 + 200, x1 - 120, u); by = y1 - 120
                place(lay, fx.icon("boxbooks", 150), (bx, by), "mm", a * min(1, 4 * (1 - u)))
            d.rectangle([x1 - 120, y1 - 300, x1 - 20, y1 - 70], fill=(240, 220, 150, int(90 * a)))
        if m == "mess":
            rr = random.Random(7)
            for j in range(26):
                bx = rr.uniform(x0 + 80, x1 - 80); by = rr.uniform(y1 - 110, y1 - 40); col = rr.choice(LEATHER)
                ang = rr.uniform(-30, 30); im = Image.new("RGBA", (70, 22), col + (255,))
                place(lay, im.rotate(ang, expand=True), (bx, by), "mm", a)
        if m == "seized":
            for (p0, p1) in (((x0 + 40, y0 + 120), (x1 - 40, y1 - 160)), ((x0 + 40, y1 - 160), (x1 - 40, y0 + 120))):
                d.line([p0, p1], fill=(230, 60, 50, al), width=26)
            d.rounded_rectangle([(x0 + x1) / 2 - 240, (y0 + y1) / 2 - 50, (x0 + x1) / 2 + 240, (y0 + y1) / 2 + 30], 12, fill=(244, 240, 230, al))
            d.text(((x0 + x1) / 2, (y0 + y1) / 2 - 10), "SOTTO SEQUESTRO", font=font(OSW, 56, 700), fill=(160, 30, 30, al), anchor="mm")
        if m == "open":
            for j in range(4):
                fxp = x0 + 300 + j * 330 + 30 * math.sin(k + j)
                col = ((60, 70, 90), (120, 50, 50), (70, 90, 70), (90, 80, 110))[j] + (al,)
                d.ellipse([fxp - 20, y1 - 250, fxp + 20, y1 - 210], fill=(214, 190, 160, al))
                d.rounded_rectangle([fxp - 34, y1 - 205, fxp + 34, y1 - 110], 16, fill=col)
                d.rectangle([fxp - 26, y1 - 112, fxp - 6, y1 - 60], fill=(40, 40, 46, al)); d.rectangle([fxp + 6, y1 - 112, fxp + 26, y1 - 60], fill=(40, 40, 46, al))
        d.text(((x0 + x1) / 2, y1 + 22), self.title, font=font(COURR, 22), fill=GREY + (al,), anchor="mm")
        if self.label:
            f = font(OSW, 32, 700); tw = tl(d, self.label, f)
            d.rounded_rectangle([x0 + 16, y0 + 12, x0 + 40 + tw, y0 + 58], 10, fill=(14, 12, 11, int(220 * a)))
            d.text((x0 + 28, y0 + 35), self.label, font=f, fill=GOLD + (al,), anchor="lm")
