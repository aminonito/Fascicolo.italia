# Elementi grafici del caso 012 (il crac Parmalat, 2003): il bilancio (scenografia ricorrente, schema semplificato),
# la lettera di conferma ricostruita, l'obbligazione generica, icone del caso. Tutto disegnato da codice:
# nessuna foto reale, nessun logo o marchio riprodotto, nessun documento originale.
import math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "011-urbino"))
from urb import *                      # catena: urb -> rom -> mod -> car -> osp -> tor -> maj (+ pon)
import urb
import fi
import fx
from fx import *
import pon
from pon import WorldMap, WPL

WPL.update({"New York": (-74.0, 40.71), "Cayman": (-81.25, 19.31), "Parma": (10.33, 44.80), "Milano": (9.19, 45.46),
            "Collecchio": (10.21, 44.75), "Quito": (-78.47, -0.18)})
fi.PLACES.update({"Parma": (10.33, 44.80), "Milano": (9.19, 45.46), "Collecchio": (10.21, 44.75), "Bologna": (11.34, 44.49),
                  "Roma": (12.50, 41.90)})

MILKB = (60, 110, 180)
GREEN = (96, 150, 104)

# ---------------------------------------------------------------- icone del caso
_pc2 = {}
def ppic(name, size):
    k = (name, size)
    if k in _pc2: return _pc2[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); dk = (40, 34, 30, 255); wh = (240, 238, 232, 255)
    if name == "milk":          # cartone di latte generico (nessun marchio)
        d.polygon([P(.26, .26), P(.50, .08), P(.74, .26)], fill=(220, 222, 226, 255))
        d.rectangle([P(.44, .04), P(.56, .12)], fill=(220, 222, 226, 255))
        d.rectangle([P(.26, .26), P(.74, .96)], fill=wh)
        d.rectangle([P(.26, .56), P(.74, .96)], fill=MILKB + (255,))
        d.text(P(.50, .44), "LATTE", font=font(OSW, int(S * .11), 700), fill=MILKB + (255,), anchor="mm")
        for k in range(3): d.arc([P(.30 + k * .14, .62), P(.44 + k * .14, .76)], 200, 340, fill=wh, width=S // 50)
    elif name == "cow":         # mucca stilizzata
        d.rounded_rectangle([P(.14, .34), P(.78, .70)], S // 10, fill=wh)
        for (x, y, r) in ((.30, .44, .07), (.52, .56, .08), (.64, .40, .05)): d.ellipse([P(x - r, y - r), P(x + r, y + r)], fill=dk)
        d.rounded_rectangle([P(.70, .26), P(.94, .50)], S // 14, fill=wh); d.rounded_rectangle([P(.80, .40), P(.96, .52)], S // 30, fill=(230, 170, 170, 255))
        d.ellipse([P(.80, .32), P(.84, .36)], fill=dk); d.polygon([P(.72, .26), P(.70, .16), P(.78, .24)], fill=(200, 190, 170, 255))
        for x in (.20, .32, .58, .70): d.rectangle([P(x, .68), P(x + .06, .92)], fill=wh)
        d.ellipse([P(.42, .66), P(.54, .78)], fill=(230, 170, 170, 255))
    elif name == "bond":        # obbligazione generica (titolo con cedole)
        d.rectangle([P(.06, .14), P(.94, .86)], fill=(228, 220, 196, 255), outline=(120, 100, 60, 255), width=S // 50)
        d.rectangle([P(.12, .20), P(.88, .80)], outline=(170, 140, 80, 255), width=S // 80)
        d.text(P(.50, .32), "OBBLIGAZIONE", font=font(OSW, int(S * .09), 700), fill=(90, 70, 40, 255), anchor="mm")
        for k in range(4): d.rectangle([P(.16 + k * .18, .56), P(.30 + k * .18, .74)], outline=(150, 120, 70, 255), width=S // 90)
        d.text(P(.50, .46), "1.000 €", font=font(SERIF, int(S * .08)), fill=(90, 70, 40, 255), anchor="mm")
    elif name == "island":      # isola con palma e cassetta delle lettere (società di comodo)
        d.ellipse([P(.04, .70), P(.96, .96)], fill=(60, 110, 150, 255))
        d.ellipse([P(.18, .66), P(.82, .86)], fill=(220, 200, 140, 255))
        d.line([P(.36, .76), P(.40, .30)], fill=(130, 90, 50, 255), width=S // 22)
        for a_ in (-2.6, -2.0, -1.2, -0.5):
            d.line([P(.40, .30), P(.40 + .24 * math.cos(a_), .30 + .18 * math.sin(a_) + .1)], fill=(70, 140, 70, 255), width=S // 22)
        d.rectangle([P(.62, .52), P(.64, .76)], fill=(90, 70, 50, 255)); d.rounded_rectangle([P(.54, .42), P(.76, .56)], S // 40, fill=(200, 60, 50, 255))
    elif name == "box_empty":   # scatola vuota
        d.polygon([P(.14, .36), P(.50, .50), P(.86, .36), P(.50, .24)], fill=(110, 80, 50, 255))
        d.polygon([P(.14, .36), P(.50, .50), P(.50, .92), P(.14, .78)], fill=(190, 150, 100, 255))
        d.polygon([P(.86, .36), P(.50, .50), P(.50, .92), P(.86, .78)], fill=(160, 120, 76, 255))
        d.polygon([P(.14, .36), P(.02, .22), P(.38, .10), P(.50, .24)], fill=(200, 160, 110, 255))
        d.polygon([P(.86, .36), P(.98, .22), P(.62, .10), P(.50, .24)], fill=(176, 136, 90, 255))
    elif name == "fax":
        d.rounded_rectangle([P(.08, .40), P(.92, .86)], S // 20, fill=(70, 74, 80, 255))
        d.rectangle([P(.24, .10), P(.76, .46)], fill=wh, outline=(150, 150, 150, 255), width=S // 90)
        for k in range(4): d.line([P(.30, .18 + k * .07), P(.70 if k % 2 else .58, .18 + k * .07)], fill=(120, 120, 120, 255), width=S // 90)
        d.rectangle([P(.16, .52), P(.48, .64)], fill=(160, 200, 160, 255))
        for r in range(2):
            for c in range(3): d.ellipse([P(.56 + c * .1, .52 + r * .12), P(.62 + c * .1, .58 + r * .12)], fill=(200, 196, 186, 255))
        d.rectangle([P(.20, .74), P(.80, .78)], fill=(30, 30, 34, 255))
    elif name == "scissors":
        for s_ in (-1, 1):
            d.line([P(.50, .50), P(.50 + .40 * s_, .08)], fill=(190, 192, 200, 255), width=S // 14)
            d.ellipse([P(.50 + .22 * s_ - .14, .66), P(.50 + .22 * s_ + .14, .94)], outline=RED + (255,), width=S // 22)
            d.line([P(.50, .50), P(.50 + .16 * s_, .70)], fill=RED + (255,), width=S // 18)
    elif name == "ball":        # pallone stilizzato
        d.ellipse([P(.08, .08), P(.92, .92)], fill=wh, outline=dk, width=S // 50)
        pts = [P(.50 + .16 * math.cos(a_ * 2 * math.pi / 5 - math.pi / 2), .50 + .16 * math.sin(a_ * 2 * math.pi / 5 - math.pi / 2)) for a_ in range(5)]
        d.polygon(pts, fill=dk)
        for a_ in range(5):
            ang = a_ * 2 * math.pi / 5 - math.pi / 2
            d.line([P(.50 + .16 * math.cos(ang), .50 + .16 * math.sin(ang)), P(.50 + .38 * math.cos(ang), .50 + .38 * math.sin(ang))], fill=dk, width=S // 50)
    elif name == "trophy":
        g = GOLD + (255,)
        d.chord([P(.22, .00), P(.78, .62)], 0, 180, fill=g); d.rectangle([P(.22, .08), P(.78, .32)], fill=g)
        for s_ in (-1, 1): d.arc([P(.50 + .22 * s_ - .14, .12), P(.50 + .22 * s_ + .14, .40)], 0, 360, fill=g, width=S // 26)
        d.rectangle([P(.45, .60), P(.55, .78)], fill=g); d.rectangle([P(.30, .78), P(.70, .90)], fill=(130, 90, 40, 255))
    elif name == "plane":
        c = (220, 222, 228, 255)
        d.polygon([P(.06, .50), P(.20, .44), P(.90, .44), P(.98, .50), P(.90, .56), P(.20, .56)], fill=c)
        d.polygon([P(.44, .46), P(.62, .46), P(.40, .10), P(.32, .10)], fill=c); d.polygon([P(.44, .54), P(.62, .54), P(.40, .90), P(.32, .90)], fill=c)
        d.polygon([P(.10, .46), P(.20, .46), P(.12, .26), P(.06, .26)], fill=c)
    elif name == "family":      # famiglia di risparmiatori
        for x, h_, c in ((.26, .9, (70, 90, 130)), (.52, .84, (150, 70, 70)), (.76, .62, (80, 130, 90))):
            r = .08 if h_ > .7 else .065
            d.ellipse([P(x - r, 1 - h_), P(x + r, 1 - h_ + 2 * r)], fill=(226, 196, 166, 255))
            d.rounded_rectangle([P(x - r * 1.4, 1 - h_ + 2 * r + .02), P(x + r * 1.4, .96)], S // 30, fill=c + (255,))
    elif name == "piggy":       # salvadanaio
        d.ellipse([P(.10, .26), P(.86, .82)], fill=(230, 150, 160, 255)); d.ellipse([P(.76, .42), P(.96, .62)], fill=(220, 130, 140, 255))
        for x in (.24, .62): d.rectangle([P(x, .74), P(x + .1, .92)], fill=(220, 130, 140, 255))
        d.rectangle([P(.40, .24), P(.58, .30)], fill=dk); d.ellipse([P(.70, .40), P(.74, .44)], fill=dk)
    elif name == "calc":        # calcolatrice
        d.rounded_rectangle([P(.20, .06), P(.80, .94)], S // 20, fill=(60, 64, 70, 255))
        d.rectangle([P(.28, .14), P(.72, .30)], fill=(170, 200, 160, 255))
        d.text(P(.68, .22), "÷", font=font(COUR, int(S * .12)), fill=dk, anchor="rm")
        for r in range(4):
            for c in range(3): d.rounded_rectangle([P(.28 + c * .15, .38 + r * .13), P(.40 + c * .15, .48 + r * .13)], S // 60, fill=(200, 196, 186, 255))
    elif name == "pasteur":     # impianto: pentolone/serbatoio con termometro
        d.rounded_rectangle([P(.12, .30), P(.62, .90)], S // 14, fill=(190, 196, 204, 255))
        d.ellipse([P(.12, .22), P(.62, .38)], fill=(210, 216, 224, 255))
        d.line([P(.62, .50), P(.80, .50)], fill=(150, 156, 164, 255), width=S // 24)
        d.rounded_rectangle([P(.76, .12), P(.88, .80)], S // 30, fill=wh); d.ellipse([P(.72, .74), P(.92, .94)], fill=RED + (255,))
        d.rectangle([P(.80, .40), P(.84, .80)], fill=RED + (255,))
    elif name == "thermo":      # termometro alto (UHT)
        d.rounded_rectangle([P(.40, .04), P(.60, .78)], S // 20, fill=wh); d.ellipse([P(.32, .70), P(.68, .98)], fill=RED + (255,))
        d.rectangle([P(.46, .14), P(.54, .80)], fill=RED + (255,))
        for k in range(6): d.line([P(.60, .12 + k * .1), P(.68, .12 + k * .1)], fill=wh, width=S // 60)
    elif name == "nofridge":    # frigorifero sbarrato
        d.rounded_rectangle([P(.24, .06), P(.76, .94)], S // 20, fill=(220, 224, 230, 255)); d.line([P(.24, .38), P(.76, .38)], fill=(150, 156, 164, 255), width=S // 40)
        d.rectangle([P(.64, .16), P(.68, .30)], fill=(150, 156, 164, 255)); d.rectangle([P(.64, .46), P(.68, .64)], fill=(150, 156, 164, 255))
        d.line([P(.10, .10), P(.90, .90)], fill=RED + (255,), width=S // 14)
    elif name == "globe2":      # mondo generico
        d.ellipse([P(.08, .08), P(.92, .92)], fill=(60, 110, 150, 255))
        for poly in ([(.30, .20), (.46, .24), (.42, .46), (.28, .40)], [(.56, .30), (.80, .36), (.72, .62), (.58, .54)], [(.34, .58), (.46, .62), (.40, .84)]):
            d.polygon([P(*p) for p in poly], fill=(110, 160, 100, 255))
    elif name == "letter_bank": # lettera con intestazione (generica)
        d.rectangle([P(.16, .04), P(.84, .96)], fill=wh, outline=(150, 150, 150, 255), width=S // 80)
        d.rectangle([P(.24, .10), P(.76, .22)], fill=(60, 80, 130, 255))
        for k in range(6): d.line([P(.24, .32 + k * .09), P(.76 if k % 2 else .64, .32 + k * .09)], fill=(120, 120, 120, 255), width=S // 70)
        d.line([P(.52, .86), P(.74, .82)], fill=(40, 60, 120, 255), width=S // 60)
    elif name == "court":       # tribunale generico
        d.polygon([P(.06, .30), P(.5, .08), P(.94, .30)], fill=(210, 200, 180, 255)); d.rectangle([P(.08, .30), P(.92, .36)], fill=(210, 200, 180, 255))
        for k in range(5): d.rectangle([P(.14 + k * .16, .40), P(.22 + k * .16, .84)], fill=(226, 218, 200, 255))
        d.rectangle([P(.04, .84), P(.96, .94)], fill=(190, 180, 160, 255))
        d.line([P(.40, .20), P(.60, .20)], fill=dk, width=S // 50); d.line([P(.50, .14), P(.50, .26)], fill=dk, width=S // 50)
    elif name == "water":       # bottiglia d'acqua minerale generica
        d.rounded_rectangle([P(.34, .26), P(.66, .96)], S // 12, fill=(150, 200, 230, 200), outline=(200, 230, 245, 255), width=S // 50)
        d.polygon([P(.34, .30), P(.42, .14), P(.58, .14), P(.66, .30)], fill=(150, 200, 230, 200))
        d.rectangle([P(.42, .04), P(.58, .14)], fill=(60, 110, 180, 255))
        d.rectangle([P(.34, .50), P(.66, .70)], fill=(240, 238, 232, 255))
        d.text(P(.50, .60), "ACQUA", font=font(OSW, int(S * .07), 700), fill=(60, 110, 180, 255), anchor="mm")
    elif name == "calendar_x":  # scadenza
        d.rounded_rectangle([P(.10, .12), P(.90, .92)], S // 20, fill=(236, 228, 210, 255)); d.rectangle([P(.10, .12), P(.90, .32)], fill=RED + (255,))
        d.text(P(.50, .62), "8", font=font(SERIF, int(S * .36)), fill=INK + (255,), anchor="mm")
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _pc2[k] = im
    return im

_prev_icon2 = fx.icon
def _icon2(name, size, color=None):
    if isinstance(name, str):
        m = ppic(name, size)
        if m is not None: return m
    return _prev_icon2(name, size, color)
fx.icon = _icon2

# ---------------------------------------------------------------- documenti ricostruiti
def confirm_letter(w=520, fake=False, seed=9):
    """lettera di conferma del conto: RICOSTRUZIONE GRAFICA, intestazione generica (nessun logo reale)"""
    h = int(w * 1.25); im = paper(w, h, (244, 242, 236), seed, 0.15); d = ImageDraw.Draw(im)
    d.rectangle([40, 34, w - 40, 34 + h * .12], outline=(60, 80, 130, 255), width=3)
    d.text((w / 2, 34 + h * .06), "INTESTAZIONE DELLA BANCA", font=font(OSW, int(w * .052), 600), fill=(60, 80, 130, 255), anchor="mm")
    if fake:
        d.line([(30, 28), (w - 30, 28)], fill=RED + (255,), width=3)
        d.text((w - 40, 30 + h * .15), "copiata con lo scanner", font=font(COURR, int(w * .036)), fill=RED + (255,), anchor="ra")
    y = h * .24
    d.text((48, y), "CONFERMA DI SALDO", font=font(TYPE, int(w * .06)), fill=INK + (255,)); y += w * .1
    for ln in ("Conto: BONLAT FINANCING", "Sede: isole Cayman", "Saldo al 31.12.2002:"):
        d.text((48, y), ln, font=font(COURR, int(w * .045)), fill=INK + (255,)); y += w * .075
    d.text((w / 2, y + w * .06), "€ 3.950.000.000", font=font(SERIF, int(w * .095)), fill=INK + (255,), anchor="mm"); y += w * .18
    d.line([(w * .52, y + 30), (w * .86, y + 18)], fill=(40, 60, 120, 255), width=3)
    d.text((w * .69, y + 46), "firma", font=font(COURR, int(w * .034)), fill=(110, 100, 90, 255), anchor="mm")
    recon_label(d, w, h)
    return im

def bond_doc(w=520, seed=4):
    h = int(w * 0.62); im = paper(w, h, (226, 216, 190), seed, 0.3); d = ImageDraw.Draw(im)
    d.rectangle([16, 16, w - 16, h - 16], outline=(120, 100, 60, 255), width=4)
    d.text((w / 2, h * .16), "OBBLIGAZIONE", font=font(SERIF, int(w * .085)), fill=(80, 60, 30, 255), anchor="mm")
    d.text((w / 2, h * .34), "prestito a un'azienda", font=font(COURR, int(w * .042)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .46), "rimborso alla scadenza + interessi", font=font(COURR, int(w * .042)), fill=INK + (255,), anchor="mm")
    for k in range(5):
        x = w * .12 + k * w * .158
        d.rectangle([x, h * .58, x + w * .13, h * .80], outline=(150, 120, 70, 255), width=2)
        d.text((x + w * .065, h * .69), "cedola", font=font(COURR, int(w * .026)), fill=(110, 90, 50, 255), anchor="mm")
    recon_label(d, w, h, size=max(14, int(w * 0.03)))
    return im

def cover_folder(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 28, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 012", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "IL CRAC PARMALAT", font=font(SERIF, int(w * .085)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "PARMA · 2003", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im

def sentence_card(lines, w=600, title="SENTENZA DEFINITIVA", seed=41):
    return label_card(lines, w, title=title, seed=seed, size=32)

# ---------------------------------------------------------------- scenografia: il bilancio
class Ledger(El):
    """bilancio semplificato su due colonne. A sinistra la CASSA (blocchi verdi + blocco oro 'CONTO BONLAT 3,95 MLD');
    a destra i DEBITI: parte dichiarata (rossa) e parte nascosta (grigia con '?') che cresce: hidden [(t, quota 0..1)].
    fake_t: il blocco oro diventa vuoto tratteggiato 'NON ESISTE'; reveal_t: la parte nascosta diventa rossa '14 MLD'."""
    def __init__(self, box, t0, t1=None, cash_t=None, gold_t=None, fake_t=None, hidden=((0, 0.0),), reveal_t=None,
                 title="IL BILANCIO · schema semplificato · non in scala", hl_gold=None, reveal_text="IL BUCO VERO"):
        super().__init__(t0, t1, 0.4)
        self.box, self.cash_t, self.gold_t, self.fake_t, self.hidden, self.reveal_t, self.title, self.hl_gold = box, cash_t, gold_t, fake_t, sorted(hidden), reveal_t, title, hl_gold
        self.reveal_text = reveal_text
    def hv(self, t):
        ks = self.hidden; i = -1
        for j, (kt, kv) in enumerate(ks):
            if t >= kt: i = j
        if i < 0: return 0.0
        if i == 0: return ks[0][1] * ease((t - ks[0][0]) / 0.9) if ks[0][0] > self.t0 else ks[0][1]
        p0 = ks[i - 1][1]; kt, kv = ks[i]
        return p0 + (kv - p0) * ease((t - kt) / 0.9)
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; w, h = x1 - x0, y1 - y0; d = ImageDraw.Draw(lay); al = int(255 * a)
        d.rounded_rectangle([x0, y0, x1, y1], 18, fill=(236, 230, 214, al), outline=(150, 130, 100, al), width=4)
        d.text(((x0 + x1) / 2, y0 + 34), self.title, font=font(COURR, 24), fill=(110, 96, 80, al), anchor="mm")
        mx = (x0 + x1) / 2
        d.line([(mx, y0 + 70), (mx, y1 - 24)], fill=(150, 130, 100, al), width=3)
        d.line([(x0 + 30, y0 + 120), (x1 - 30, y0 + 120)], fill=(150, 130, 100, al), width=3)
        z = min(1.0, w / 1000); fo = font(OSW, int(40 * max(z, 0.7)), 700)
        d.text(((x0 + mx) / 2, y0 + 92), "SOLDI IN CASSA" if w >= 800 else "CASSA", font=fo, fill=(50, 90, 60, al), anchor="mm")
        d.text(((mx + x1) / 2, y0 + 92), "DEBITI", font=fo, fill=(150, 40, 36, al), anchor="mm")
        base = y1 - 40; top = y0 + 150; Hm = base - top
        # cassa
        cw = (mx - x0) * .56; cx0 = (x0 + mx) / 2 - cw / 2
        nb = 4 if self.cash_t is None else min(4, int(max(0, t - self.cash_t) / 0.18) + 1) if t >= self.cash_t else 0
        bh = Hm * 0.13
        for k in range(nb):
            yy = base - (k + 1) * bh
            d.rounded_rectangle([cx0, yy + 4, cx0 + cw, yy + bh - 4], 8, fill=GREEN + (al,), outline=(60, 100, 66, al), width=3)
        if self.gold_t is not None and t >= self.gold_t:
            k = ease((t - self.gold_t) / 0.4); gh = Hm * 0.40; yy = base - 4 * bh - gh
            fake = self.fake_t is not None and t >= self.fake_t
            if not fake:
                d.rounded_rectangle([cx0, yy + 4 + (1 - k) * -40, cx0 + cw, yy + gh - 4 + (1 - k) * -40], 10, fill=GOLD + (int(al * k),), outline=(150, 110, 40, int(al * k)), width=4)
                tc = (60, 40, 10, int(al * k))
                d.text((cx0 + cw / 2, yy + gh * .36), "CONTO BONLAT", font=font(OSW, int(34 * max(z, .6)), 700), fill=tc, anchor="mm")
                d.text((cx0 + cw / 2, yy + gh * .62), "3,95 MLD €", font=font(OSW, int(46 * max(z, .6)), 700), fill=tc, anchor="mm")
                if self.hl_gold is not None and t > self.hl_gold:
                    p = 0.5 + 0.5 * math.sin((t - self.hl_gold) * 6)
                    d.rounded_rectangle([cx0 - 12, yy - 8, cx0 + cw + 12, yy + gh + 8], 14, outline=RED + (int(al * (0.4 + 0.6 * p)),), width=6)
            else:
                kf = ease((t - self.fake_t) / 0.4)
                for xx in range(int(cx0), int(cx0 + cw), 28): d.line([(xx, yy + 4), (min(xx + 14, cx0 + cw), yy + 4)], fill=RED + (al,), width=4)
                for xx in range(int(cx0), int(cx0 + cw), 28): d.line([(xx, yy + gh - 4), (min(xx + 14, cx0 + cw), yy + gh - 4)], fill=RED + (al,), width=4)
                for yv in range(int(yy + 4), int(yy + gh - 4), 28): d.line([(cx0, yv), (cx0, min(yv + 14, yy + gh))], fill=RED + (al,), width=4); d.line([(cx0 + cw, yv), (cx0 + cw, min(yv + 14, yy + gh))], fill=RED + (al,), width=4)
                d.text((cx0 + cw / 2, yy + gh / 2), "NON ESISTE", font=font(OSW, int(44 * max(z, .6)), 700), fill=RED + (int(al * kf),), anchor="mm")
        # debiti
        dw = (x1 - mx) * .56; dx0 = (mx + x1) / 2 - dw / 2
        dh = Hm * 0.16
        d.rounded_rectangle([dx0, base - dh + 4, dx0 + dw, base - 4], 8, fill=(190, 70, 60, al), outline=(130, 40, 36, al), width=3)
        d.text((dx0 + dw / 2, base - dh / 2), "DICHIARATI", font=font(OSW, int(30 * max(z, .6)), 700), fill=WHITE + (al,), anchor="mm")
        hv = self.hv(t)
        if hv > 0.01:
            hh = (Hm - dh - 10) * hv; yy = base - dh - hh
            rev = self.reveal_t is not None and t >= self.reveal_t
            col = (176, 40, 36) if rev else (110, 106, 100)
            d.rounded_rectangle([dx0, yy + 4, dx0 + dw, base - dh], 8, fill=col + (al,), outline=(70, 66, 62, al), width=3)
            if not rev:
                for yv in range(int(yy + 20), int(base - dh), 34): d.line([(dx0 + 10, yv), (dx0 + dw - 10, yv - 18)], fill=(140, 136, 130, al), width=3)
                if hh > 90: d.text((dx0 + dw / 2, yy + hh / 2), "NASCOSTI ?", font=font(OSW, int(40 * max(z, .6)), 700), fill=WHITE + (al,), anchor="mm")
            else:
                if hh > 90: d.text((dx0 + dw / 2, yy + hh / 2), self.reveal_text, font=font(OSW, int(52 * max(z, .6)), 700), fill=WHITE + (al,), anchor="mm")

class Savers(El):
    """fila di risparmiatori con l'obbligazione in mano; drop_t: le obbligazioni 'cadono' (diventano grigie)"""
    def __init__(self, box, n, t0, t1=None, drop_t=None, s=0.55, seed=5):
        super().__init__(t0, t1, 0.3); self.box, self.n, self.drop_t, self.s = box, n, drop_t, s
        rng = random.Random(seed); x0, y0, x1, y1 = box
        self.p = [(x0 + (i + 0.5) * (x1 - x0) / n + rng.uniform(-10, 10), y1, rng.choice(("man", "suit", "expert", "man")), rng.uniform(0, 6)) for i in range(n)]
    def draw(self, lay, t, a):
        for i, (x, y, k, ph) in enumerate(self.p):
            ti = self.t0 + i * 0.07
            if t < ti: continue
            aa = a * ease((t - ti) / 0.3)
            draw_person(lay, x, y, self.s, k, ph, False, alpha=int(255 * aa))
            dr = 0.0 if self.drop_t is None or t < self.drop_t + i * 0.05 else ease((t - self.drop_t - i * 0.05) / 0.5)
            kk = self.s / 0.55; ic = fx.icon("bond", int(70 * kk))
            if dr > 0:
                ic = ic.convert("LA").convert("RGBA")
            place(lay, ic, (x + 50 * kk, y - 95 * kk + dr * 80), "mm", aa * (1 - 0.5 * dr))
