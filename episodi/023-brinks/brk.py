# Elementi grafici del caso 023 (la rapina della Brink's, Boston 1950): maschera di gomma generica, binocolo,
# cilindro della serratura, cappotto da marinaio, sacchi di denaro, la PIANTA del deposito (scenografia ricorrente:
# porte, serrature, sala conta, dipendenti, banda) e la STRADA (Prince Street, vedetta sul tetto, camion).
# Tutto disegnato da codice: nessuna foto reale, nessun logo, nessun documento originale.
import math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "022-girolamini"))
from gir import *
import gir, fi, fx
from fx import *
from pon import WorldMap, WPL

WPL.update({"Boston": (-71.06, 42.36), "Stoughton": (-71.10, 42.12), "Towanda": (-76.44, 41.77), "Baltimora": (-76.61, 39.29),
            "Washington": (-77.04, 38.90), "Pittsburgh": (-80.00, 40.44), "Chicago": (-87.63, 41.88), "New York": (-74.00, 40.71),
            "Italia": (13.0, 42.5), "Leicester": (-71.91, 42.25)})

_bk = {}
def bpic(name, size):
    k = (name, size)
    if k in _bk: return _bk[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); lw = max(3, S // 60)
    if name == "mask":            # maschera di gomma generica, sorriso fisso (nessun personaggio)
        d.ellipse([P(.18, .08), P(.82, .92)], fill=(236, 200, 150, 255), outline=(120, 80, 50, 255), width=lw)
        d.ellipse([P(.30, .34), P(.44, .46)], fill=(20, 18, 16, 255)); d.ellipse([P(.56, .34), P(.70, .46)], fill=(20, 18, 16, 255))
        d.arc([P(.30, .50), P(.70, .80)], 15, 165, fill=(150, 40, 40, 255), width=lw * 2)
        d.ellipse([P(.22, .55), P(.32, .63)], fill=(230, 150, 130, 255)); d.ellipse([P(.68, .55), P(.78, .63)], fill=(230, 150, 130, 255))
        d.line([P(.50, .46), P(.47, .58)], fill=(150, 100, 70, 255), width=lw)
    elif name == "binoculars":
        for x in (.18, .54):
            d.rounded_rectangle([P(x, .30), P(x + .28, .80)], S // 20, fill=(40, 42, 48, 255), outline=(10, 10, 12, 255), width=lw)
            d.ellipse([P(x + .03, .62), P(x + .25, .86)], fill=(90, 120, 160, 255), outline=(10, 10, 12, 255), width=lw)
        d.rectangle([P(.44, .40), P(.56, .58)], fill=(60, 62, 70, 255))
    elif name == "lockcyl":       # cilindro di serratura estratto + chiave
        d.rounded_rectangle([P(.14, .34), P(.62, .66)], S // 14, fill=(200, 170, 80, 255), outline=(110, 90, 40, 255), width=lw)
        d.ellipse([P(.08, .34), P(.24, .66)], fill=(220, 190, 100, 255), outline=(110, 90, 40, 255), width=lw)
        d.rectangle([P(.14, .48), P(.20, .52)], fill=(40, 30, 20, 255))
        d.ellipse([P(.66, .40), P(.84, .58)], outline=(180, 180, 190, 255), width=lw * 2)
        d.polygon([P(.60, .47), P(.68, .47), P(.68, .51), P(.66, .55), P(.63, .51), P(.60, .51)], fill=(180, 180, 190, 255))
    elif name == "peacoat":       # cappotto da marinaio con doppia fila di bottoni
        d.polygon([P(.30, .14), P(.70, .14), P(.86, .30), P(.80, .90), P(.20, .90), P(.14, .30)], fill=(30, 40, 70, 255), outline=(10, 14, 30, 255))
        d.polygon([P(.38, .14), P(.50, .34), P(.62, .14)], fill=(220, 220, 220, 255))
        for y in (.44, .58, .72):
            for x in (.42, .58): d.ellipse([P(x - .025, y - .025), P(x + .025, y + .025)], fill=(200, 180, 120, 255))
    elif name == "chauffeurcap":  # berretto da autista generico, senza scritte
        d.ellipse([P(.14, .30), P(.86, .62)], fill=(40, 44, 50, 255))
        d.rectangle([P(.24, .48), P(.76, .64)], fill=(30, 32, 36, 255))
        d.pieslice([P(.20, .56), P(.80, .80)], 0, 180, fill=(20, 20, 22, 255))
        d.rectangle([P(.24, .52), P(.76, .56)], fill=(160, 140, 90, 255))
    elif name == "bags":          # sacchi di tela
        for j, (x, y) in enumerate(((.30, .58), (.62, .56), (.46, .40))):
            d.ellipse([P(x - .17, y - .12), P(x + .17, y + .26)], fill=(196, 176, 130, 255), outline=(110, 90, 60, 255), width=lw)
            d.rectangle([P(x - .05, y - .18), P(x + .05, y - .10)], fill=(150, 120, 80, 255))
            d.text(P(x, y + .08), "$", font=font(OSW, int(S * .14), 700), fill=(90, 70, 40, 255), anchor="mm")
    elif name == "cabinet":       # schedario
        d.rectangle([P(.24, .10), P(.76, .92)], fill=(110, 118, 120, 255), outline=(40, 44, 46, 255), width=lw)
        for j in range(4):
            y = .14 + j * .195; d.rectangle([P(.28, y), P(.72, y + .17)], outline=(60, 64, 66, 255), width=lw)
            d.rectangle([P(.44, y + .07), P(.56, y + .10)], fill=(200, 200, 200, 255))
    elif name == "flashlight":
        d.polygon([P(.08, .44), P(.40, .44), P(.48, .36), P(.48, .64), P(.40, .56), P(.08, .56)], fill=(60, 60, 66, 255))
        d.polygon([P(.50, .38), P(.94, .16), P(.94, .84), P(.50, .62)], fill=(250, 230, 140, 160))
    elif name == "key":
        d.ellipse([P(.10, .34), P(.40, .66)], outline=(214, 178, 92, 255), width=lw * 3)
        d.rectangle([P(.38, .46), P(.90, .54)], fill=(214, 178, 92, 255))
        for x in (.66, .76, .86): d.rectangle([P(x, .54), P(x + .05, .66)], fill=(214, 178, 92, 255))
    elif name == "rope":
        for j in range(3):
            d.ellipse([P(.18 + j * .06, .22 + j * .05), P(.82 - j * .06, .78 - j * .05)], outline=(196, 160, 100, 255), width=lw * 2)
        d.line([P(.70, .70), P(.90, .92)], fill=(196, 160, 100, 255), width=lw * 2)
    elif name == "tape":
        d.ellipse([P(.14, .20), P(.74, .80)], fill=(200, 196, 186, 255), outline=(120, 116, 110, 255), width=lw)
        d.ellipse([P(.32, .38), P(.56, .62)], fill=(40, 40, 44, 255))
        d.polygon([P(.60, .70), P(.92, .62), P(.94, .74), P(.64, .80)], fill=(220, 216, 206, 255))
    elif name == "glove":
        d.rounded_rectangle([P(.28, .40), P(.72, .88)], S // 12, fill=(40, 40, 44, 255))
        for j, x in enumerate((.30, .41, .52, .63)):
            d.rounded_rectangle([P(x, .12 + (j % 2) * .04), P(x + .09, .50)], S // 30, fill=(40, 40, 44, 255))
        d.rounded_rectangle([P(.12, .46), P(.34, .62)], S // 30, fill=(40, 40, 44, 255))
    elif name == "shoe":
        d.polygon([P(.10, .40), P(.46, .40), P(.56, .56), P(.90, .62), P(.90, .74), P(.10, .74)], fill=(70, 46, 30, 255))
        d.rectangle([P(.08, .74), P(.92, .84)], fill=(40, 40, 40, 255))
        d.text(P(.50, .91), "GOMMA", font=font(OSW, int(S * .07), 700), fill=(200, 200, 200, 255), anchor="mm")
    elif name == "bell":
        d.pieslice([P(.22, .18), P(.78, .74)], 180, 360, fill=(214, 178, 92, 255))
        d.rectangle([P(.22, .46), P(.78, .70)], fill=(214, 178, 92, 255)); d.rectangle([P(.14, .70), P(.86, .76)], fill=(180, 150, 70, 255))
        d.ellipse([P(.44, .76), P(.56, .88)], fill=(180, 150, 70, 255))
    elif name == "wall":
        for r in range(6):
            for c in range(5):
                x = .08 + c * .17 + (.085 if r % 2 else 0); y = .14 + r * .12
                d.rectangle([P(x, y), P(x + .16, y + .11)], fill=(150, 70, 50, 255), outline=(90, 50, 40, 255))
        d.rectangle([P(.40, .38), P(.62, .62)], fill=(30, 26, 24, 255)); d.text(P(.51, .50), "$", font=font(OSW, int(S * .16), 700), fill=(214, 178, 92, 255), anchor="mm")
    elif name == "stopwatch":
        d.ellipse([P(.16, .20), P(.84, .88)], fill=(236, 230, 214, 255), outline=(214, 178, 92, 255), width=lw * 2)
        d.rectangle([P(.44, .06), P(.56, .20)], fill=(214, 178, 92, 255))
        d.line([P(.50, .54), P(.50, .30)], fill=(30, 30, 30, 255), width=lw); d.line([P(.50, .54), P(.66, .62)], fill=(200, 40, 40, 255), width=lw)
    elif name == "dollar":
        for j in range(3):
            o = j * .05
            d.rectangle([P(.12 + o, .28 + o), P(.80 + o, .64 + o)], fill=(150, 180, 130, 255), outline=(60, 90, 60, 255), width=lw)
        d.ellipse([P(.38, .36), P(.64, .66)], outline=(60, 90, 60, 255), width=lw)
        d.text(P(.51, .51), "$", font=font(OSW, int(S * .14), 700), fill=(40, 70, 40, 255), anchor="mm")
    elif name == "sensor":
        d.rounded_rectangle([P(.22, .18), P(.78, .82)], S // 16, fill=(220, 220, 214, 255), outline=(80, 80, 80, 255), width=lw)
        d.ellipse([P(.40, .28), P(.60, .48)], fill=(200, 40, 40, 255))
        for j in range(3): d.rectangle([P(.32, .56 + j * .07), P(.68, .60 + j * .07)], fill=(90, 90, 90, 255))
    elif name == "bond":          # titolo generico in dollari, senza intestazioni reali
        d.rectangle([P(.12, .22), P(.88, .78)], fill=(232, 222, 190, 255), outline=(120, 100, 60, 255), width=lw)
        d.rectangle([P(.17, .27), P(.83, .73)], outline=(160, 130, 80, 255), width=max(1, lw // 2))
        d.text(P(.50, .40), "TITOLO", font=font(OSW, int(S * .09), 700), fill=(90, 70, 40, 255), anchor="mm")
        d.text(P(.50, .58), "$ 1.000", font=font(OSW, int(S * .08), 700), fill=(90, 70, 40, 255), anchor="mm")
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _bk[k] = im; return im

_prev_icon_b = fx.icon
def _icon_b(name, size, color=None):
    if isinstance(name, str):
        m = bpic(name, size)
        if m is not None: return m
    return _prev_icon_b(name, size, color)
fx.icon = _icon_b

def cover_folder23(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 38, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 023", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "IL COLPO DI BOSTON", font=font(SERIF, int(w * .08)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "BOSTON · 1950-1956", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im

def _man(d, x, y, s, body, head=(214, 190, 160), al=255, mask=False, down=False):
    """omino visto dall'alto/di lato in pianta: cerchio testa + corpo; down=True disteso a terra"""
    if down:
        d.rounded_rectangle([x - 34 * s, y - 10 * s, x + 26 * s, y + 10 * s], int(9 * s), fill=body + (al,))
        d.ellipse([x + 22 * s, y - 11 * s, x + 44 * s, y + 11 * s], fill=head + (al,))
        return
    d.rounded_rectangle([x - 16 * s, y - 10 * s, x + 16 * s, y + 40 * s], int(10 * s), fill=body + (al,))
    d.ellipse([x - 13 * s, y - 36 * s, x + 13 * s, y - 10 * s], fill=((236, 200, 150) if mask else head) + (al,))
    if mask:
        d.ellipse([x - 7 * s, y - 28 * s, x - 2 * s, y - 23 * s], fill=(20, 18, 16, al)); d.ellipse([x + 2 * s, y - 28 * s, x + 7 * s, y - 23 * s], fill=(20, 18, 16, al))
        d.arc([x - 7 * s, y - 24 * s, x + 7 * s, y - 14 * s], 20, 160, fill=(150, 40, 40, al), width=max(1, int(2 * s)))
        d.rectangle([x - 14 * s, y - 40 * s, x + 14 * s, y - 33 * s], fill=(30, 32, 36, al))

class Deposito(El):
    """scenografia ricorrente: PIANTA del secondo piano del deposito (schema semplificato, non in scala).
    doors: quante serrature sono 'copiate' (0-5, diventano oro); robbers: quanti uomini mascherati entrano (0-7);
    prog: avanzamento della banda lungo il percorso (0-1, animato fino a prog_to); staff: 'work' | 'tied' | 'none';
    bags: frazione dei sacchi ancora in sala (anima fino a bags_to); night: luci basse; alarm: luce rossa."""
    PATH = [(0.04, 0.80), (0.20, 0.80), (0.20, 0.40), (0.40, 0.40), (0.40, 0.20), (0.62, 0.20), (0.70, 0.45)]
    DOORS = [(0.10, 0.80), (0.20, 0.60), (0.30, 0.40), (0.40, 0.30), (0.52, 0.20)]
    def __init__(self, box, t0, t1=None, doors=0, robbers=0, prog=1.0, prog_to=None, staff="work", bags=1.0, bags_to=None,
                 night=True, alarm=False, label=None, dur=4.0, title="IL DEPOSITO · SECONDO PIANO · schema semplificato · non in scala"):
        super().__init__(t0, t1, 0.35)
        self.box, self.doors, self.robbers, self.prog, self.prog_to = box, doors, robbers, prog, prog_to
        self.staff, self.bags, self.bags_to, self.night, self.alarm, self.label, self.dur, self.title = staff, bags, bags_to, night, alarm, label, dur, title
    def P(self, u, v):
        x0, y0, x1, y1 = self.box; return (x0 + u * (x1 - x0), y0 + v * (y1 - y0))
    def pathpt(self, f):
        pts = [self.P(*q) for q in self.PATH]; L = [math.dist(a, b) for a, b in zip(pts, pts[1:])]; tot = sum(L); s = f * tot
        for (a, b), l in zip(zip(pts, pts[1:]), L):
            if s <= l: u = s / max(1, l); return (lerp(a[0], b[0], u), lerp(a[1], b[1], u))
            s -= l
        return pts[-1]
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; d = ImageDraw.Draw(lay); al = int(255 * a); k = t - self.t0; P = self.P
        floor = (58, 60, 66) if self.night else (150, 146, 136)
        d.rectangle([x0, y0, x1, y1], fill=floor + (al,), outline=(20, 20, 24, al), width=6)
        # stanze: corridoio/scale (sinistra), corridoio interno, sala conta (destra) con gabbia/caveau
        wall = (24, 24, 28, al)
        d.rectangle([P(.00, .66), P(.24, .94)], outline=wall, width=5)
        d.text(P(.12, .90), "SCALE DA PRINCE ST.", font=font(COURR, 20), fill=(230, 230, 230, al), anchor="mm")
        d.rectangle([P(.24, .30), P(.44, .66)], outline=wall, width=5)
        d.rectangle([P(.44, .06), P(.98, .94)], outline=wall, width=6)
        room = (70, 74, 82) if self.night else (176, 170, 158)
        d.rectangle([P(.45, .07), P(.97, .93)], fill=room + (al,))
        d.text(P(.71, .12), "SALA DELLA CONTA", font=font(OSW, 30, 700), fill=(240, 236, 220, al), anchor="mm")
        # caveau / gabbia
        d.rectangle([P(.80, .22), P(.96, .62)], fill=(40, 42, 48, al), outline=(150, 150, 160, al), width=4)
        for j in range(8):
            xx = P(.80 + j * .02, 0)[0]; d.line([(xx, P(0, .22)[1]), (xx, P(0, .62)[1])], fill=(150, 150, 160, int(al * .7)), width=2)
        d.text(P(.88, .66), "CASSAFORTE · APERTA", font=font(COURR, 20), fill=(230, 230, 230, al), anchor="mm")
        # tavoli
        for (u, v) in ((.55, .40), (.55, .70), (.70, .70)):
            d.rectangle([P(u - .05, v - .05), P(u + .05, v + .05)], fill=(120, 90, 60, al))
        # sacchi
        bf = self.bags if self.bags_to is None else lerp(self.bags, self.bags_to, ease(min(1, k / self.dur)))
        nb = 14
        for j in range(nb):
            if j / nb >= bf: continue
            u = .60 + (j % 7) * .045; v = .80 + (j // 7) * .06
            c = P(u, v); d.ellipse([c[0] - 16, c[1] - 14, c[0] + 16, c[1] + 18], fill=(196, 176, 130, al), outline=(110, 90, 60, al))
        # porte con serrature
        for j, (u, v) in enumerate(self.DOORS):
            c = P(u, v); ok = j < self.doors
            d.rectangle([c[0] - 14, c[1] - 14, c[0] + 14, c[1] + 14], fill=((214, 178, 92) if ok else (150, 60, 50)) + (al,), outline=(10, 10, 10, al), width=2)
            d.text((c[0], c[1] - 30), str(j + 1), font=font(OSW, 24, 700), fill=(240, 240, 240, al), anchor="mm")
        # dipendenti
        sp = [(.55, .32), (.50, .62), (.62, .62), (.66, .78), (.75, .62)]
        if self.staff == "work":
            for u, v in sp: c = P(u, v); _man(d, c[0], c[1], 0.9, (90, 110, 150), al=al)
        elif self.staff == "tied":
            for j, (u, v) in enumerate(sp):
                c = P(.50 + (j % 3) * .07, .46 + (j // 3) * .10); _man(d, c[0], c[1], 0.9, (90, 110, 150), al=al, down=True)
                d.line([c[0] - 10, c[1] - 12, c[0] - 4, c[1] + 12], fill=(220, 200, 150, al), width=4)
        # banda
        if self.robbers:
            f = self.prog if self.prog_to is None else lerp(self.prog, self.prog_to, ease(min(1, k / self.dur)))
            for j in range(self.robbers):
                ff = max(0.0, f - j * 0.035)
                c = self.pathpt(ff) if ff < 0.999 else P(.60 + (j % 4) * .07, .30 + (j // 4) * .14)
                if ff <= 0 and f < 1: continue
                _man(d, c[0], c[1], 0.85, (30, 40, 70), al=al, mask=True)
        if self.alarm and int(k * 3) % 2 == 0:
            d.rectangle([x0, y0, x1, y1], outline=(230, 50, 40, al), width=16)
        d.text(((x0 + x1) / 2, y1 + 22), self.title, font=font(COURR, 22), fill=GREY + (al,), anchor="mm")
        if self.label:
            f = font(OSW, 32, 700); tw = tl(d, self.label, f)
            d.rounded_rectangle([x0 + 16, y0 + 12, x0 + 40 + tw, y0 + 58], 10, fill=(14, 12, 11, int(220 * a)))
            d.text((x0 + 28, y0 + 35), self.label, font=f, fill=GOLD + (al,), anchor="lm")

class Strada(El):
    """scenografia esterna: Prince Street (schema). truck: 'none' | 'arrive' | 'parked' | 'leave';
    lookout: vedetta sul tetto di fronte con la torcia; night; label."""
    def __init__(self, box, t0, t1=None, truck="none", lookout=False, night=True, label=None, dur=3.5, police=False,
                 title="PRINCE STREET · BOSTON · schema semplificato · non in scala"):
        super().__init__(t0, t1, 0.35); self.box, self.truck, self.lookout, self.night, self.label, self.dur, self.police, self.title = box, truck, lookout, night, label, dur, police, title
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; d = ImageDraw.Draw(lay); al = int(255 * a); k = t - self.t0
        sky = (16, 20, 40) if self.night else (150, 180, 210)
        d.rectangle([x0, y0, x1, y1], fill=sky + (al,))
        if self.night: d.ellipse([x0 + (x1 - x0) * .42, y0 + 30, x0 + (x1 - x0) * .42 + 60, y0 + 90], fill=(230, 226, 200, al))
        gy = y1 - 120
        # edifici di sfondo (lato opposto)
        rr = random.Random(5)
        for j in range(9):
            bx = x0 + j * (x1 - x0) / 9; bw = (x1 - x0) / 9 - 6; bh = rr.uniform(220, 360)
            d.rectangle([bx, gy - 90 - bh, bx + bw, gy - 90], fill=((40, 36, 40) if self.night else (150, 120, 100)) + (al,))
            for r in range(int(bh // 60)):
                for c in range(3):
                    lit = rr.random() < (0.35 if self.night else 0)
                    d.rectangle([bx + 14 + c * bw / 3, gy - 90 - bh + 20 + r * 60, bx + 14 + c * bw / 3 + bw / 3 - 28, gy - 90 - bh + 50 + r * 60],
                                fill=((240, 210, 120) if lit else (24, 24, 30) if self.night else (90, 110, 130)) + (al,))
        # deposito (in primo piano a destra)
        bx0, bx1 = x0 + (x1 - x0) * .52, x0 + (x1 - x0) * .92
        d.rectangle([bx0, y0 + 120, bx1, gy], fill=((80, 70, 64) if self.night else (170, 140, 110)) + (al,), outline=(20, 20, 20, al), width=4)
        for fl in range(3):
            fy = y0 + 150 + fl * ((gy - y0 - 150) / 3)
            for c in range(5):
                lit = (fl == 1) and self.night
                d.rectangle([bx0 + 30 + c * (bx1 - bx0 - 40) / 5, fy, bx0 + 30 + c * (bx1 - bx0 - 40) / 5 + 60, fy + 70],
                            fill=((250, 220, 130) if lit else (30, 30, 36)) + (al,))
        d.rounded_rectangle([(bx0 + bx1) / 2 - 250, y0 + 78, (bx0 + bx1) / 2 + 250, y0 + 122], 8, fill=(14, 12, 11, int(220 * a)))
        d.text(((bx0 + bx1) / 2, y0 + 100), "IL DEPOSITO · 2° PIANO: LA CONTA", font=font(OSW, 28, 700), fill=(240, 236, 220, al), anchor="mm")
        d.rectangle([bx0 + 40, gy - 110, bx0 + 110, gy], fill=(50, 34, 24, al))
        # strada
        d.rectangle([x0, gy, x1, y1], fill=(44, 44, 48, al))
        for j in range(12): d.rectangle([x0 + j * (x1 - x0) / 12 + 20, gy + 56, x0 + j * (x1 - x0) / 12 + 80, gy + 64], fill=(200, 190, 120, al))
        # vedetta sul tetto di fronte (a sinistra)
        if self.lookout:
            lx, ly = x0 + (x1 - x0) * .26, gy - 90 - 330
            _man(d, lx, ly - 40, 1.0, (60, 60, 70), al=al)
            if int(k * 2.5) % 2 == 0:
                d.polygon([(lx + 18, ly - 46), (bx0, y0 + 220), (bx0, y0 + 320)], fill=(250, 230, 140, int(al * .35)))
            d.text((lx, ly + 24), "LA VEDETTA", font=font(OSW, 24, 700), fill=(250, 230, 140, al), anchor="mm")
        # camion
        if self.truck != "none":
            u = 1.0
            if self.truck == "arrive": u = ease(min(1, k / self.dur))
            if self.truck == "leave": u = 1 + ease(min(1, k / self.dur)) * 1.2
            tx = lerp(x0 - 300, bx0 - 260, min(u, 1)) + (max(0, u - 1) * -900)
            ty = gy + 20
            d.rectangle([tx, ty - 120, tx + 230, ty], fill=(60, 110, 70, al)); d.rectangle([tx, ty - 130, tx + 230, ty - 112], fill=(120, 110, 80, al))
            d.rectangle([tx + 230, ty - 80, tx + 300, ty], fill=(50, 96, 60, al)); d.rectangle([tx + 250, ty - 72, tx + 290, ty - 44], fill=(150, 180, 200, al))
            for wx in (tx + 50, tx + 250): d.ellipse([wx - 24, ty - 18, wx + 24, ty + 30], fill=(20, 20, 20, al))
        if self.police:
            for j in range(2):
                px = x0 + 120 + j * 260; py = gy + 20
                d.rectangle([px, py - 70, px + 200, py], fill=(30, 30, 34, al)); d.rectangle([px + 40, py - 100, px + 150, py - 68], fill=(30, 30, 34, al))
                d.rectangle([px + 80, py - 114, px + 110, py - 100], fill=((230, 50, 40) if int(k * 4 + j) % 2 else (60, 90, 230)) + (al,))
                for wx in (px + 40, px + 160): d.ellipse([wx - 20, py - 16, wx + 20, py + 24], fill=(10, 10, 10, al))
        d.text(((x0 + x1) / 2, y1 + 22), self.title, font=font(COURR, 22), fill=GREY + (al,), anchor="mm")
        if self.label:
            f = font(OSW, 32, 700); tw = tl(d, self.label, f)
            d.rounded_rectangle([x0 + 16, y0 + 12, x0 + 40 + tw, y0 + 58], 10, fill=(14, 12, 11, int(220 * a)))
            d.text((x0 + 28, y0 + 35), self.label, font=f, fill=GOLD + (al,), anchor="lm")
