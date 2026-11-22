# Elementi grafici del caso 021 (Daniele Barillà, 1992-2000): due utilitarie rosse identiche viste dall'alto,
# la tangenziale stilizzata (scenografia ricorrente dello scambio), il muro dei giorni in cella, targhe generiche.
# Tutto disegnato da codice: nessuna foto reale, nessun logo, nessuna targa reale, nessun documento originale.
import math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "020-totonero"))
from tot import *
import tot, euf, met, fi, fx, pon
from fx import *
from pon import WorldMap, WPL

WPL.update({"Nova Milanese": (9.20, 45.59), "Milano": (9.19, 45.46), "Bergamo": (9.67, 45.70), "Genova": (8.93, 44.41),
            "Monza": (9.27, 45.58), "Livorno": (10.31, 43.55), "Firenze": (11.25, 43.77), "Roma": (12.50, 41.90),
            "Parigi": (2.35, 48.86), "Madrid": (-3.70, 40.42), "Torino": (7.68, 45.07)})

CARRED = (176, 36, 48); CARBLU = (40, 52, 80)
_pb = {}
def bpic(name, size):
    k = (name, size)
    if k in _pb: return _pb[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); lw = max(3, S // 70)
    def wheel(x, y, r):
        d.ellipse([P(x - r, y - r), P(x + r, y + r)], fill=(24, 24, 26, 255)); d.ellipse([P(x - r * .45, y - r * .45), P(x + r * .45, y + r * .45)], fill=(170, 170, 176, 255))
    if name in ("tipo", "tipo_b"):     # utilitaria due volumi generica, vista di lato (nessun marchio)
        c = CARRED + (255,)
        d.rounded_rectangle([P(.04, .46), P(.96, .70)], S // 22, fill=c)
        d.polygon([P(.14, .47), P(.30, .26), P(.74, .26), P(.90, .47)], fill=c)
        d.polygon([P(.20, .46), P(.33, .30), P(.50, .30), P(.50, .46)], fill=(160, 200, 220, 255))
        d.polygon([P(.54, .46), P(.54, .30), P(.72, .30), P(.84, .46)], fill=(160, 200, 220, 255))
        d.rectangle([P(.40, .73), P(.60, .80)], fill=(240, 240, 236, 255), outline=(30, 30, 30, 255), width=max(1, lw // 2))
        wheel(.25, .71, .09); wheel(.75, .71, .09)
        if name == "tipo_b":
            d.text(P(.50, .14), "?", font=font(OSW, int(S * .16), 700), fill=GOLD + (255,), anchor="mm")
    elif name == "plate":              # targa generica con caratteri nascosti
        d.rounded_rectangle([P(.04, .34), P(.96, .66)], S // 30, fill=(244, 244, 240, 255), outline=(30, 30, 30, 255), width=lw)
        d.rectangle([P(.04, .34), P(.13, .66)], fill=(40, 70, 160, 255))
        d.text(P(.24, .50), "", font=font(OSW, int(S * .14), 700), fill=(24, 24, 26, 255), anchor="mm")
        for j in range(4): d.ellipse([P(.40 + j * .13, .46), P(.46 + j * .13, .54)], fill=(24, 24, 26, 255))
    elif name == "plates2":            # due targhe simili, dettagli coperti
        for j, y in enumerate((.18, .58)):
            d.rounded_rectangle([P(.06, y), P(.94, y + .26)], S // 30, fill=(244, 244, 240, 255), outline=(30, 30, 30, 255), width=lw)
            d.rectangle([P(.06, y), P(.14, y + .26)], fill=(40, 70, 160, 255))
            d.text(P(.24, y + .13), "", font=font(OSW, int(S * .10), 700), fill=(24, 24, 26, 255), anchor="mm")
            for q in range(6): d.ellipse([P(.36 + q * .095, y + .105), P(.40 + q * .095, y + .155)], fill=(24, 24, 26, 255))
        d.text(P(.50, .51), "≈", font=font(OSW, int(S * .12), 700), fill=RED + (255,), anchor="mm")
    elif name == "rose":
        d.line([P(.50, .45), P(.50, .92)], fill=(60, 120, 60, 255), width=lw * 2)
        d.ellipse([P(.30, .40), P(.48, .55)], fill=(70, 140, 70, 255))
        for r, col in ((.20, (170, 30, 50)), (.14, (200, 40, 60)), (.08, (150, 20, 40))):
            d.ellipse([P(.50 - r, .30 - r), P(.50 + r, .30 + r)], fill=col + (255,))
    elif name == "cell":               # cella: muro, branda e sbarre
        d.rectangle([P(.06, .10), P(.94, .90)], fill=(120, 118, 112, 255))
        d.rectangle([P(.12, .62), P(.60, .74)], fill=(80, 70, 60, 255))
        d.rectangle([P(.58, .20), P(.86, .44)], fill=(170, 200, 220, 255))
        for x in (.62, .68, .74, .80):
            d.line([P(x + .02, .20), P(x + .02, .44)], fill=(40, 40, 44, 255), width=lw)
        for x in [.10 + j * .08 for j in range(11)]:
            d.line([P(x, .06), P(x, .94)], fill=(36, 36, 40, 255), width=lw + 2)
    elif name == "tally":              # tacche dei giorni
        d.rectangle([P(.06, .14), P(.94, .86)], fill=(150, 146, 136, 255))
        for g in range(6):
            x0 = .12 + g * .135
            for j in range(4): d.line([P(x0 + j * .025, .32), P(x0 + j * .025, .68)], fill=(40, 36, 32, 255), width=lw)
            d.line([P(x0 - .01, .62), P(x0 + .09, .36)], fill=(40, 36, 32, 255), width=lw)
    elif name == "hunger":             # piatto vuoto (sciopero della fame)
        d.ellipse([P(.12, .30), P(.88, .86)], fill=(236, 236, 232, 255), outline=(150, 150, 150, 255), width=lw)
        d.ellipse([P(.28, .42), P(.72, .74)], outline=(190, 190, 190, 255), width=lw)
        d.line([P(.06, .20), P(.94, .94)], fill=RED + (255,), width=lw * 2)
    elif name == "pen":
        d.polygon([P(.20, .86), P(.28, .70), P(.80, .18), P(.90, .28), P(.38, .80)], fill=(40, 60, 120, 255))
        d.polygon([P(.20, .86), P(.28, .70), P(.38, .80)], fill=(220, 200, 160, 255))
    elif name == "scalesok":           # bilancia in equilibrio con spunta
        g = (200, 170, 80, 255)
        d.line([P(.50, .18), P(.50, .84)], fill=g, width=lw * 2); d.line([P(.18, .30), P(.82, .30)], fill=g, width=lw * 2)
        for x in (.22, .78):
            d.line([P(x, .30), P(x - .1, .56)], fill=g, width=lw); d.line([P(x, .30), P(x + .1, .56)], fill=g, width=lw)
            d.chord([P(x - .14, .46), P(x + .14, .66)], 0, 180, fill=g)
        d.rectangle([P(.34, .84), P(.66, .90)], fill=g)
    elif name == "family_x":           # famiglia stilizzata (silhouette generiche)
        for x, s in ((.30, 1.0), (.70, 1.0)):
            d.ellipse([P(x - .09 * s, .20), P(x + .09 * s, .38)], fill=(200, 200, 206, 255))
            d.rounded_rectangle([P(x - .14 * s, .42), P(x + .14 * s, .86)], S // 20, fill=(200, 200, 206, 255))
        d.line([P(.50, .20), P(.50, .90)], fill=RED + (255,), width=lw * 2)
    elif name == "factory_x":          # piccola officina chiusa
        d.polygon([P(.08, .40), P(.30, .26), P(.30, .40), P(.52, .26), P(.52, .40), P(.74, .26), P(.74, .40), P(.92, .40), P(.92, .86), P(.08, .86)], fill=(150, 156, 166, 255))
        d.rectangle([P(.40, .56), P(.60, .86)], fill=(70, 74, 82, 255))
        d.rectangle([P(.20, .66), P(.80, .76)], fill=RED + (255,))
        d.text(P(.50, .71), "CHIUSO", font=font(OSW, int(S * .07), 700), fill=(255, 255, 255, 255), anchor="mm")
    elif name == "cable":              # cavi elettrici
        for j, col in enumerate(((200, 60, 50), (40, 90, 170), (230, 190, 40))):
            pts = [P(.08 + u * .84, .35 + j * .14 + .06 * math.sin(u * 7 + j)) for u in [k / 20 for k in range(21)]]
            d.line(pts, fill=col + (255,), width=lw * 2)
        d.rectangle([P(.04, .26), P(.14, .78)], fill=(60, 60, 64, 255)); d.rectangle([P(.86, .26), P(.96, .78)], fill=(60, 60, 64, 255))
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _pb[k] = im
    return im

_prev_icon_b = fx.icon
def _icon_b(name, size, color=None):
    if isinstance(name, str):
        m = bpic(name, size)
        if m is not None: return m
    return _prev_icon_b(name, size, color)
fx.icon = _icon_b

def cover_folder21(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 37, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 021", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "L'UOMO SBAGLIATO", font=font(SERIF, int(w * .085)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "MILANO · 1992-2000", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im

def topcar(L, col, lamp=False, label=None):
    W_ = int(L * 0.46); im = Image.new("RGBA", (L, W_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([2, 2, L - 3, W_ - 3], W_ // 4, fill=col + (255,), outline=(20, 18, 16, 255), width=3)
    d.rectangle([L * .24, W_ * .16, L * .38, W_ * .84], fill=(150, 190, 210, 255))
    d.rectangle([L * .64, W_ * .16, L * .76, W_ * .84], fill=(150, 190, 210, 255))
    if lamp: d.rectangle([L * .46, W_ * .30, L * .56, W_ * .70], fill=(60, 120, 240, 255))
    return im

class Strada(El):
    """scenografia ricorrente: la tangenziale vista dall'alto (schema). mode:
    'night' strada vuota con lampioni; 'follow' l'auto pedinata e i carabinieri dietro; 'swap' l'auto pedinata esce,
    l'auto di Barillà (identica) entra e i carabinieri seguono lei; 'stop' auto ferma, lampeggiante, manette."""
    def __init__(self, box, t0, t1=None, mode="follow", title="LA TANGENZIALE · schema semplificato · non in scala"):
        super().__init__(t0, t1, 0.35); self.box, self.mode, self.title = box, mode, title
        self.cA = topcar(170, CARRED); self.cB = topcar(170, CARRED); self.cC = topcar(170, CARBLU, lamp=True)
    def lab(self, d, x, y, s, a, col=WHITE, bg=(14, 12, 11)):
        f = font(OSW, 28, 600); tw = tl(d, s, f)
        d.rounded_rectangle([x - tw / 2 - 10, y - 20, x + tw / 2 + 10, y + 20], 9, fill=bg + (int(220 * a),))
        d.text((x, y), s, font=f, fill=col + (int(255 * a),), anchor="mm")
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; d = ImageDraw.Draw(lay); al = int(255 * a); k = t - self.t0
        d.rectangle([x0, y0, x1, y1], fill=(22, 26, 30, al))
        ry0, ry1 = y0 + (y1 - y0) * .28, y0 + (y1 - y0) * .62
        d.rectangle([x0, ry0, x1, ry1], fill=(58, 60, 64, al))
        mid = (ry0 + ry1) / 2
        for j in range(int((x1 - x0) / 80) + 2):
            xx = x0 + ((j * 80 - k * 160) % (x1 - x0 + 80)) - 40
            if x0 < xx < x1 - 40: d.line([(xx, mid), (xx + 40, mid)], fill=(230, 230, 220, al), width=5)
        # rampa di uscita in basso a destra
        ex = x0 + (x1 - x0) * .58
        d.polygon([(ex, ry1), (ex + 150, ry1), (ex + 330, y1), (ex + 180, y1)], fill=(58, 60, 64, al))
        # rampa d'ingresso in alto a destra
        ix = x0 + (x1 - x0) * .66
        d.polygon([(ix, ry0), (ix + 150, ry0), (ix + 20, y0), (ix - 130, y0)], fill=(58, 60, 64, al))
        for j in range(9):   # lampioni
            lx = x0 + 60 + j * (x1 - x0 - 120) / 8
            d.ellipse([lx - 9, ry0 - 30, lx + 9, ry0 - 12], fill=(250, 220, 140, al))
            d.ellipse([lx - 26, ry0 - 46, lx + 26, ry0 + 4], fill=(250, 220, 140, int(40 * a)))
        d.text(((x0 + x1) / 2, y1 + 24), self.title, font=font(COURR, 22), fill=GREY + (al,), anchor="mm")
        d.text((x0 + 16, y0 + 18), "SERA · 13 FEBBRAIO 1992", font=font(OSW, 30, 600), fill=GOLD + (al,), anchor="lm")
        lane = mid + 40; m = self.mode
        if m == "night": return
        if m == "follow":
            xa = lerp(x0 - 100, x0 + (x1 - x0) * .70, ease(min(1, k / 4.0))); xc = xa - 330
            place(lay, self.cC, (xc, lane), "mm", a); place(lay, self.cA, (xa, lane), "mm", a)
            self.lab(d, xa, lane - 70, "L'AUTO PEDINATA", a, bg=(120, 24, 34)); self.lab(d, xc, lane - 70, "CARABINIERI", a)
        elif m == "swap":
            u = ease(min(1, k / 3.0)); xa = lerp(ex - 60, ex + 260, u); ya = lerp(lane, y1 - 30, u)
            if u < 0.98:
                im = self.cA.rotate(-34 * u, expand=True); place(lay, im, (xa, ya), "mm", a * (1 - 0.6 * u))
                self.lab(d, xa, ya - 70, "ESCE DALLA SCENA?", a * (1 - u))
            v = ease(min(1, max(0, k - 1.2) / 2.6)); xb = lerp(ix - 70, ix + 160, v); yb = lerp(y0 + 30, lane - 80, v)
            place(lay, self.cB.rotate(30 * (1 - v), expand=True), (xb, yb), "mm", a)
            if v > 0.4: self.lab(d, xb, yb - 70, "DANIELE BARILLÀ", a, col=GOLD)
            xc = lerp(ex - 420, ix - 20, ease(min(1, k / 4.2)))
            place(lay, self.cC, (xc, lane), "mm", a); self.lab(d, xc, lane + 70, "CARABINIERI", a)
            if k > 3.2:
                d.text((xc, lane - 80), "?", font=font(OSW, 70, 700), fill=GOLD + (al,), anchor="mm")
        elif m == "stop":
            xb = x0 + (x1 - x0) * .62; xc = xb - 260
            place(lay, self.cB, (xb, lane), "mm", a); place(lay, self.cC, (xc, lane), "mm", a)
            if int(k * 4) % 2 == 0: d.ellipse([xc - 60, lane - 60, xc + 60, lane + 60], fill=(60, 120, 255, int(60 * a)))
            self.lab(d, xb, lane - 70, "DANIELE BARILLÀ", a, col=GOLD); self.lab(d, xc, lane + 70, "CARABINIERI", a)
            if k > 1.0: place(lay, fx.icon("handcuffs", 150), (xb + 200, lane - 20), "mm", a)

class Muro(El):
    """il muro dei giorni: anni dal 1992 al 1999, colonne di tacche che si riempiono e contatore."""
    def __init__(self, box, t0, t1=None, upto=1999.5, label="GIORNI DI CARCERE", total=2706, dur=4.0):
        super().__init__(t0, t1, 0.35); self.box, self.upto, self.label, self.total, self.dur = box, upto, label, total, dur
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; d = ImageDraw.Draw(lay); al = int(255 * a)
        d.rectangle([x0, y0, x1, y1], fill=(110, 106, 98, al))
        rr = random.Random(5)
        for j in range(60):
            bx, by = rr.uniform(x0, x1), rr.uniform(y0, y1); d.rectangle([bx, by, bx + 60, by + 28], outline=(96, 92, 86, al), width=2)
        u = ease(min(1, (t - self.t0) / self.dur))
        years = list(range(1992, 2000)); cw = (x1 - x0 - 80) / len(years)
        yr_now = 1992 + 1.12 / 12 + u * (self.upto - 1992 - 1.12 / 12)
        for j, y in enumerate(years):
            cx = x0 + 40 + cw * (j + 0.5)
            d.text((cx, y1 - 30), str(y), font=font(OSW, 34, 600), fill=(30, 26, 22, al), anchor="mm")
            fill = max(0, min(1, yr_now - y)) if y > 1992 else max(0, min(1, (yr_now - 1992 - 1.12 / 12) / (1 - 1.12 / 12)))
            n = int(fill * 24)
            for g in range(n):
                gx = cx - cw * 0.32 + (g % 4) * cw * 0.16; gy = y0 + 70 + (g // 4) * 52
                d.line([(gx, gy), (gx, gy + 40)], fill=(30, 26, 22, al), width=5)
        fr = min(1, (self.upto - 1992 - 1.12 / 12) / (1999.53 - 1992 - 1.12 / 12)); n = int(self.total * fr * u)
        d.rounded_rectangle([x0 + 20, y0 + 14, x0 + 560, y0 + 64], 10, fill=(14, 12, 11, int(220 * a)))
        d.text((x0 + 36, y0 + 39), f"{self.label}: {n:,}".replace(",", "."), font=font(OSW, 34, 700), fill=GOLD + (al,), anchor="lm")
        d.text(((x0 + x1) / 2, y1 + 24), "schema · 13/2/1992 → 12/7/1999 · ogni tacca non è un giorno", font=font(COURR, 22), fill=GREY + (al,), anchor="mm")
