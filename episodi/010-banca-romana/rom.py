# Elementi grafici del caso 010 (lo scandalo della Banca Romana, 1889-1894): la banca con la cassa
# (scenografia ricorrente, schema non in scala), banconote RICOSTRUITE (disegni generici, non riproduzioni),
# l'aula della Camera (schema), icone del caso. Tutto disegnato da codice: nessuna foto reale, nessun logo.
import math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "009-modigliani"))
sys.path.insert(0, os.path.join(HERE, "..", "003-ponzi"))
for d_ in ("008-caravaggio", "007-osoppo", "006-tortora", "005-majorana"):
    sys.path.insert(0, os.path.join(HERE, "..", d_))
from fi import *
import fi
import fx
from fx import *
from fx import draw_person
import mod                        # catena: mod -> car -> osp -> tor -> maj (icone già pronte)
from mod import label_card
from tor import Aula
import pon

fi.PLACES.update({"Roma": (12.50, 41.90), "Firenze": (11.25, 43.77), "Napoli": (14.27, 40.85),
                  "Palermo": (13.36, 38.12), "Torino": (7.69, 45.07)})

NOTE = (214, 200, 160)
NOTE2 = (190, 206, 176)
MARBLE = (226, 218, 200)

# ---------------------------------------------------------------- banconota ricostruita (disegno generico)
_nc = {}
def banknote(w, value="100", serial="N. 048217", seed=1, tone=NOTE, hl=False, bank="BANCA ROMANA"):
    k = (w, value, serial, seed, tone, hl, bank)
    if k in _nc: return _nc[k]
    h = int(w * 0.56); S = 2; W_, H_ = w * S, h * S
    im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ink = (70, 56, 40, 255); dk = tuple(max(0, c - 70) for c in tone) + (255,)
    d.rounded_rectangle([0, 0, W_ - 1, H_ - 1], int(W_ * .03), fill=tone + (255,))
    rng = random.Random(seed)
    for _ in range(140):   # trama
        x, y = rng.uniform(0, W_), rng.uniform(0, H_)
        d.line([(x, y), (x + rng.uniform(-30, 30), y + rng.uniform(-6, 6))], fill=tuple(c - 18 for c in tone) + (255,), width=2)
    m = int(W_ * .04)
    d.rounded_rectangle([m, m, W_ - m, H_ - m], int(W_ * .02), outline=dk, width=max(3, W_ // 160))
    d.rounded_rectangle([m + 14, m + 14, W_ - m - 14, H_ - m - 14], int(W_ * .02), outline=dk, width=max(2, W_ // 400))
    # medaglione a sinistra (rosone generico)
    cx, cy, r = W_ * .22, H_ * .52, H_ * .26
    for j in range(10):
        a0 = j * math.pi / 5
        d.ellipse([cx + math.cos(a0) * r * .45 - r * .45, cy + math.sin(a0) * r * .45 - r * .45,
                   cx + math.cos(a0) * r * .45 + r * .45, cy + math.sin(a0) * r * .45 + r * .45], outline=dk, width=3)
    d.ellipse([cx - r * .35, cy - r * .35, cx + r * .35, cy + r * .35], fill=dk)
    d.text((W_ * .62, H_ * .22), bank, font=font(SERIF, int(H_ * .11)), fill=ink, anchor="mm")
    d.text((W_ * .62, H_ * .50), value, font=font(SERIF, int(H_ * .26)), fill=ink, anchor="mm")
    d.text((W_ * .62, H_ * .68), "LIRE", font=font(OSW, int(H_ * .09), 700), fill=ink, anchor="mm")
    sf = font(COUR, int(H_ * .085))
    d.text((W_ * .62, H_ * .84), serial, font=sf, fill=(150, 30, 26, 255), anchor="mm")
    if hl:
        tw = tl(d, serial, sf)
        d.rounded_rectangle([W_ * .62 - tw / 2 - 18, H_ * .84 - H_ * .08, W_ * .62 + tw / 2 + 18, H_ * .84 + H_ * .08], 14, outline=RED + (255,), width=8)
    d.text((W_ * .22, H_ - m - 22), "ricostruzione grafica", font=font(COURR, int(H_ * .05)), fill=(90, 80, 60, 255), anchor="mb")
    im = im.resize((w, h), Image.LANCZOS); _nc[k] = im
    return im

class Twins(El):
    """due banconote identiche: arrivano da sinistra e da destra, poi il numero di serie si evidenzia (hl_t) e compare '='"""
    def __init__(self, xy, w, t0, t1=None, hl_t=None, serial="N. 048217", gap=60, eq=True, value="100"):
        super().__init__(t0, t1, 0.3); self.xy, self.w, self.hl_t, self.serial, self.gap, self.eq, self.value = xy, w, hl_t, serial, gap, eq, value
    def draw(self, lay, t, a):
        x, y = self.xy; hl = self.hl_t is not None and t >= self.hl_t
        nb = banknote(self.w, self.value, self.serial, 3, hl=hl)
        for k, sgn in enumerate((-1, 1)):
            u = ease((t - self.t0 - 0.25 * k) / 0.6)
            xx = x + sgn * (self.w / 2 + self.gap / 2) + sgn * 500 * (1 - u)
            place(lay, nb.rotate(sgn * -3, expand=True, resample=Image.BICUBIC), (xx, y), "mm", a * u)
        if hl and self.eq:
            k = ease((t - self.hl_t) / 0.3); d = ImageDraw.Draw(lay)
            d.ellipse([x - 44, y - 44, x + 44, y + 44], fill=RED + (int(255 * a * k),))
            d.text((x, y - 4), "=", font=font(OSW, 70, 700), fill=WHITE + (int(255 * a * k),), anchor="mm")

# ---------------------------------------------------------------- scenografia: la banca con la cassa
class Bank(El):
    """facciata neoclassica a sinistra (insegna), cassa a destra con pile di biglietti e la linea LIMITE DI LEGGE.
    level: [(t, quota)] altezza delle pile rispetto al limite (1.0 = al limite); dup_t: pile rosse dei biglietti doppi;
    hole_t: vuoto in cassa ('-9 MLN'); closed_t: porta sbarrata 'IN LIQUIDAZIONE'; insp: [(t, kind)] ispettori davanti"""
    def __init__(self, box, t0, t1=None, level=((0, 0.6),), dup_t=None, hole_t=None, closed_t=None, insp=(),
                 sign="BANCA ROMANA", label="schema semplificato · non in scala", dim=0.0, limit=True):
        super().__init__(t0, t1, 0.4)
        self.box, self.level, self.dup_t, self.hole_t, self.closed_t, self.insp = box, sorted(level), dup_t, hole_t, closed_t, list(insp)
        self.sign, self.label, self.dim, self.limit = sign, label, dim, limit
    def lev(self, t):
        ks = self.level; i = -1
        for j, (kt, kv) in enumerate(ks):
            if t >= kt: i = j
        if i <= 0: return ks[0][1]
        p0 = ks[i - 1][1]; kt, kv = ks[i]
        return p0 + (kv - p0) * ease((t - kt) / 0.9)
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; w, h = x1 - x0, y1 - y0; d = ImageDraw.Draw(lay); al = int(255 * a)
        sh = lambda c, k=1.0: tuple(int(v * (1 - self.dim) * k) for v in c) + (al,)
        # --- facciata (60% sinistra)
        fx1 = x0 + w * .52
        d.rectangle([x0, y0 + h * .18, fx1, y1], fill=sh(MARBLE))
        d.polygon([(x0 - 10, y0 + h * .18), ((x0 + fx1) / 2, y0), (fx1 + 10, y0 + h * .18)], fill=sh((206, 196, 176)))
        d.rectangle([x0 + w * .03, y0 + h * .20, fx1 - w * .03, y0 + h * .30], fill=sh((60, 52, 44)))
        d.text(((x0 + fx1) / 2, y0 + h * .25), self.sign, font=font(SERIF, int(h * .065)), fill=sh(GOLD), anchor="mm")
        for k in range(6):
            cx = x0 + w * .05 + k * (fx1 - x0 - w * .10) / 5
            d.rectangle([cx - w * .016, y0 + h * .32, cx + w * .016, y1 - h * .08], fill=sh((240, 234, 220)))
            d.rectangle([cx - w * .024, y0 + h * .31, cx + w * .024, y0 + h * .34], fill=sh((200, 190, 170)))
        d.rectangle([x0, y1 - h * .08, fx1, y1], fill=sh((180, 170, 150)))
        dx = (x0 + fx1) / 2
        d.rectangle([dx - w * .045, y0 + h * .52, dx + w * .045, y1 - h * .08], fill=sh((90, 62, 40)))
        if self.closed_t is not None and t >= self.closed_t:
            k = ease((t - self.closed_t) / 0.4); ca = int(al * k)
            for s_ in (-1, 1):
                d.line([(dx - w * .06, y0 + h * (.60 if s_ < 0 else .80)), (dx + w * .06, y0 + h * (.80 if s_ < 0 else .60))], fill=(120, 84, 50, ca), width=int(h * .03))
            f = font(OSW, int(h * .045), 700); tx = "IN LIQUIDAZIONE"; tw_ = tl(d, tx, f)
            d.rounded_rectangle([dx - tw_ / 2 - 14, y0 + h * .40, dx + tw_ / 2 + 14, y0 + h * .48], 8, fill=RED + (ca,))
            d.text((dx, y0 + h * .44), tx, font=f, fill=WHITE + (ca,), anchor="mm")
        # --- cassa (destra)
        cx0, cx1 = x0 + w * .58, x1; cy0 = y0 + h * .10
        d.rounded_rectangle([cx0, cy0, cx1, y1], 16, fill=sh((70, 74, 80)), outline=sh((40, 42, 46)), width=6)
        d.rounded_rectangle([cx0 + 18, cy0 + 18, cx1 - 18, y1 - 18], 10, fill=sh((40, 38, 36)))
        d.rounded_rectangle([(cx0 + cx1) / 2 - 90, cy0 - 22, (cx0 + cx1) / 2 + 90, cy0 + 22], 10, fill=sh((70, 74, 80)))
        d.text(((cx0 + cx1) / 2, cy0), "LA CASSA", font=font(OSW, int(h * .045), 700), fill=sh((230, 226, 216)), anchor="mm")
        base = y1 - 30; top = cy0 + 40; Hmax = base - top
        limy = base - Hmax * 0.5     # quota 1.0
        lv = self.lev(t)
        n = 5; sw = (cx1 - cx0 - 60) / n
        dup = 0.0 if self.dup_t is None or t < self.dup_t else ease((t - self.dup_t) / 0.8)
        hole = 0.0 if self.hole_t is None or t < self.hole_t else ease((t - self.hole_t) / 0.5)
        for k in range(n):
            if hole > 0 and k == 2: continue
            hh = min(Hmax - 10, (base - limy) * lv * (0.92 + 0.08 * ((k * 37) % 5) / 4))
            xx = cx0 + 30 + k * sw
            for j in range(int(hh / 14)):
                yy = base - j * 14
                d.rectangle([xx + 6, yy - 12, xx + sw - 6, yy], fill=sh(NOTE if (j % 2) else (200, 186, 146)), outline=sh((120, 104, 70)))
            if dup > 0:
                dh = min(Hmax - 10 - hh, (base - limy) * 0.45 * dup)
                for j in range(int(dh / 14)):
                    yy = base - int(hh / 14) * 14 - j * 14
                    d.rectangle([xx + 6, yy - 12, xx + sw - 6, yy], fill=(206, 70, 60, al), outline=(130, 30, 26, al))
        if hole > 0:
            xx = cx0 + 30 + 2 * sw
            d.rectangle([xx + 6, base - (base - limy) * .7, xx + sw - 6, base], outline=(RED[0], RED[1], RED[2], int(al * hole)), width=4)
            d.text((xx + sw / 2, base - (base - limy) * .35), "?", font=font(OSW, int(h * .09), 700), fill=RED + (int(al * hole),), anchor="mm")
        if self.limit:
            for xx in range(int(cx0 + 24), int(cx1 - 24), 30):
                d.line([(xx, limy), (xx + 16, limy)], fill=(240, 200, 90, al), width=5)
            d.rounded_rectangle([cx0 + 30, limy - 44, cx0 + 270, limy - 8], 8, fill=(30, 28, 26, int(al * .85)))
            d.text((cx0 + 40, limy - 26), "LIMITE DI LEGGE", font=font(OSW, 26, 600), fill=(240, 200, 90, al), anchor="lm")
        for (ti, kind) in self.insp:
            if t < ti: continue
            u = ease((t - ti) / 1.0); xx = x0 - 60 + (dx - w * .12 - (x0 - 60)) * u + (self.insp.index((ti, kind))) * 110
            draw_person(lay, xx, y1 + 2, 0.82 * h / 720, kind, phase=t * 6, moving=u < 1, alpha=int(al * min(1, (t - ti) / 0.3)))
        if self.label: d.text((x1 - 14, y1 + 26), self.label, font=font(COURR, 20), fill=(200, 190, 176, int(al * .8)), anchor="rs")

# ---------------------------------------------------------------- aula della Camera (schema)
class Hemicycle(El):
    """emiciclo visto di fronte: file di seggi (puntini-deputati), banco della presidenza, oratore in piedi.
    speak_t: l'oratore si alza con un foglio; stir_t: i deputati si agitano; papers: fogli che volano"""
    def __init__(self, box, t0, t1=None, speak_t=None, stir_t=None, fill_t=None, label="schema semplificato · non in scala", dim=0.0):
        super().__init__(t0, t1, 0.4); self.box, self.speak_t, self.stir_t, self.fill_t, self.label, self.dim = box, speak_t, stir_t, fill_t, label, dim
        rng = random.Random(7); self.seats = []
        x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0; cx, cy = (x0 + x1) / 2, y0 + h * .98
        self.hf = hf = min(1.35, (w / 2 - 40) / (h * .90))
        for r in range(5):
            R = h * (.36 + r * .11)
            n = 12 + r * 5
            for j in range(n):
                ang = math.pi * (0.06 + 0.88 * j / (n - 1))
                self.seats.append((cx - math.cos(ang) * R * hf, cy - math.sin(ang) * R, rng.random(), r))
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; w, h = x1 - x0, y1 - y0; d = ImageDraw.Draw(lay); al = int(255 * a)
        kd = 1 - self.dim
        d.rectangle([x0, y0, x1, y1], fill=(int(54 * kd), int(40 * kd), int(36 * kd), al))
        cx, cy = (x0 + x1) / 2, y0 + h * .98
        for r in range(5, -1, -1):
            R = h * (.30 + r * .11)
            d.pieslice([cx - R * self.hf - 30, cy - R - 30, cx + R * self.hf + 30, cy + R + 30], 180, 360,
                       fill=(int((110 - r * 6) * kd), int((52 - r * 3) * kd), int((44 - r * 3) * kd), al))
        fl = 1.0 if self.fill_t is None else ease((t - self.fill_t) / 1.2) if t > self.fill_t else 0
        stir = self.stir_t is not None and t >= self.stir_t
        for (sx, sy, rr, r) in self.seats:
            if rr > fl: continue
            jy = math.sin(t * 9 + rr * 30) * 5 if stir else 0
            col = (40, 38, 50) if rr < .6 else (60, 56, 62)
            d.ellipse([sx - 11, sy - 26 + jy, sx + 11, sy - 4 + jy], fill=(214, 186, 160, al))
            d.rounded_rectangle([sx - 15, sy - 6 + jy, sx + 15, sy + 22 + jy], 6, fill=col + (al,))
            if stir and rr < .25: d.line([(sx + 12, sy - 4 + jy), (sx + 26, sy - 34 + jy)], fill=(214, 186, 160, al), width=5)
        # presidenza
        d.rectangle([cx - w * .16, y1 - h * .20, cx + w * .16, y1], fill=(120, 84, 52, al), outline=(70, 50, 34, al), width=4)
        d.rectangle([cx - w * .04, y1 - h * .30, cx + w * .04, y1 - h * .20], fill=(140, 100, 64, al))
        if self.speak_t is not None and t >= self.speak_t:
            k = ease((t - self.speak_t) / 0.5); sx = x0 + w * .22
            draw_person(lay, sx, y1 - 4, 1.0 * h / 720, "suit", arms="up" if (t - self.speak_t) % 3 < 1.5 else "down", alpha=int(al * k))
            d.rectangle([sx + 26, y1 - h * .36, sx + 74, y1 - h * .30], fill=(244, 240, 230, int(al * k)))
            d.polygon([(sx - 60, y1), (sx + 60, y1), (sx + 46, y1 - h * .14), (sx - 46, y1 - h * .14)], fill=(120, 84, 52, int(al * k)))
        if self.label: d.text((x1 - 14, y1 - 10), self.label, font=font(COURR, 20), fill=(200, 190, 176, int(al * .8)), anchor="rs")

# ---------------------------------------------------------------- icone del caso
_rc = {}
def rpic(name, size):
    k = (name, size)
    if k in _rc: return _rc[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S)
    wh = WHITE + (255,); ink = INK + (255,); dk = (34, 32, 30, 255); gold = GOLD + (255,)
    if name == "press":          # torchio da stampa
        d.rectangle([P(.12, .82), P(.88, .92)], fill=(70, 60, 54, 255))
        d.rectangle([P(.18, .20), P(.26, .84)], fill=(90, 80, 72, 255)); d.rectangle([P(.74, .20), P(.82, .84)], fill=(90, 80, 72, 255))
        d.rectangle([P(.14, .12), P(.86, .22)], fill=(110, 98, 88, 255))
        d.rectangle([P(.47, .22), P(.53, .44)], fill=(160, 150, 140, 255))
        d.rectangle([P(.28, .44), P(.72, .52)], fill=(130, 120, 110, 255))
        d.rectangle([P(.26, .62), P(.74, .70)], fill=NOTE + (255,))
        d.line([P(.30, .06), P(.70, .06)], fill=(150, 140, 130, 255), width=S // 30)
        d.ellipse([P(.27, .02), P(.33, .10)], fill=RED + (255,)); d.ellipse([P(.67, .02), P(.73, .10)], fill=RED + (255,))
    elif name == "notes":        # mazzetta di banconote
        for j in range(4):
            off = j * .035
            d.rounded_rectangle([P(.10 + off, .30 - off), P(.86 + off, .72 - off)], S // 30, fill=(NOTE if j % 2 else (200, 186, 146)) + (255,), outline=(120, 104, 70, 255), width=S // 120)
        d.text(P(.58, .52), "L.", font=font(SERIF, int(S * .2)), fill=(90, 70, 40, 255), anchor="mm")
        d.rectangle([P(.42, .26), P(.56, .78)], fill=(170, 60, 50, 255))
    elif name == "notes_dup":    # mazzetta rossa (biglietti doppi)
        for j in range(4):
            off = j * .035
            d.rounded_rectangle([P(.10 + off, .30 - off), P(.86 + off, .72 - off)], S // 30, fill=(206, 80, 66, 255), outline=(120, 30, 26, 255), width=S // 120)
        d.text(P(.58, .50), "×2", font=font(OSW, int(S * .22), 700), fill=wh, anchor="mm")
    elif name == "safe":         # cassaforte
        d.rounded_rectangle([P(.12, .12), P(.88, .86)], S // 20, fill=(84, 88, 96, 255))
        d.rounded_rectangle([P(.20, .20), P(.80, .78)], S // 30, fill=(110, 114, 122, 255))
        d.ellipse([P(.38, .34), P(.62, .58)], fill=(60, 62, 70, 255)); d.ellipse([P(.45, .41), P(.55, .51)], fill=gold)
        d.rectangle([P(.18, .86), P(.28, .94)], fill=dk); d.rectangle([P(.72, .86), P(.82, .94)], fill=dk)
    elif name == "report":       # relazione sigillata
        d.rectangle([P(.20, .08), P(.80, .92)], fill=PAPER + (255,))
        d.text(P(.50, .20), "RELAZIONE", font=font(OSW, int(S * .09), 700), fill=ink, anchor="mm")
        for j in range(7): d.line([P(.28, .32 + j * .07), P(.72, .32 + j * .07)], fill=(120, 112, 100, 255), width=S // 90)
        d.line([P(.20, .60), P(.80, .60)], fill=RED + (255,), width=S // 28)
        d.ellipse([P(.40, .52), P(.60, .70)], fill=(150, 30, 26, 255))
    elif name == "chamber":      # aula a emiciclo
        d.pieslice([P(.04, .20), P(.96, 1.16)], 180, 360, fill=(110, 52, 44, 255))
        d.pieslice([P(.20, .40), P(.80, 1.0)], 180, 360, fill=(70, 40, 36, 255))
        for r, n in ((.40, 9), (.30, 7)):
            for j in range(n):
                ang = math.pi * (.08 + .84 * j / (n - 1))
                x, y = .5 - math.cos(ang) * r * 1.05, .68 - math.sin(ang) * r
                d.ellipse([P(x - .025, y - .025), P(x + .025, y + .025)], fill=(220, 200, 170, 255))
        d.rectangle([P(.04, .68), P(.96, .76)], fill=(150, 110, 70, 255))
        d.text(P(.50, .88), "CAMERA", font=font(OSW, int(S * .11), 700), fill=wh, anchor="mm")
    elif name == "bankold":      # palazzo della banca (piccolo)
        d.polygon([P(.06, .30), P(.50, .08), P(.94, .30)], fill=(206, 196, 176, 255))
        d.rectangle([P(.10, .30), P(.90, .84)], fill=MARBLE + (255,))
        for j in range(5): d.rectangle([P(.16 + j * .16, .38), P(.22 + j * .16, .78)], fill=(244, 240, 228, 255))
        d.rectangle([P(.06, .84), P(.94, .92)], fill=(180, 170, 150, 255))
        d.ellipse([P(.42, .16), P(.58, .26)], fill=gold)
    elif name == "newbank":      # banca nuova (più grande, con stella)
        d.polygon([P(.04, .28), P(.50, .04), P(.96, .28)], fill=(196, 170, 120, 255))
        d.rectangle([P(.08, .28), P(.92, .86)], fill=(236, 226, 200, 255))
        for j in range(6): d.rectangle([P(.13 + j * .13, .36), P(.19 + j * .13, .80)], fill=(250, 246, 236, 255))
        d.rectangle([P(.04, .86), P(.96, .94)], fill=(170, 150, 110, 255))
        pts = [];
        for j in range(10):
            r = .07 if j % 2 == 0 else .03; ang = -math.pi / 2 + j * math.pi / 5
            pts.append(P(.50 + math.cos(ang) * r, .18 + math.sin(ang) * r))
        d.polygon(pts, fill=wh)
    elif name == "emptyfolder":  # cartella vuota (documenti spariti)
        d.polygon([P(.08, .26), P(.40, .26), P(.46, .18), P(.08, .18)], fill=(196, 160, 104, 255))
        d.rectangle([P(.08, .24), P(.92, .84)], fill=(210, 176, 120, 255))
        d.rectangle([P(.16, .34), P(.84, .76)], fill=(170, 138, 90, 255))
        d.text(P(.50, .55), "?", font=font(OSW, int(S * .3), 700), fill=RED + (255,), anchor="mm")
    elif name == "serial":       # numero di serie sotto la lente
        d.rounded_rectangle([P(.04, .30), P(.80, .70)], S // 30, fill=NOTE + (255,))
        d.text(P(.42, .50), "N. 0482", font=font(COUR, int(S * .12)), fill=(150, 30, 26, 255), anchor="mm")
        d.ellipse([P(.50, .14), P(.90, .54)], outline=(218, 176, 96, 255), width=S // 24)
        d.line([P(.84, .48), P(.98, .64)], fill=(218, 176, 96, 255), width=S // 18)
    elif name == "crane":        # gru di cantiere
        d.rectangle([P(.30, .14), P(.36, .90)], fill=(220, 170, 50, 255))
        d.rectangle([P(.10, .12), P(.92, .18)], fill=(220, 170, 50, 255))
        d.line([P(.80, .18), P(.80, .46)], fill=dk, width=S // 60)
        d.rectangle([P(.72, .46), P(.88, .56)], fill=(150, 90, 60, 255))
        d.rectangle([P(.18, .90), P(.48, .96)], fill=dk)
        for j in range(3): d.rectangle([P(.50 + j * .14, .66), P(.62 + j * .14, .92)], fill=(190, 140, 110, 255))
    elif name == "crash":        # grafico in discesa
        d.line([P(.10, .10), P(.10, .90), P(.92, .90)], fill=(200, 196, 186, 255), width=S // 40)
        d.line([P(.14, .30), P(.34, .24), P(.52, .34), P(.66, .56), P(.86, .82)], fill=RED + (255,), width=S // 24)
        d.polygon([P(.86, .90), P(.92, .74), P(.78, .78)], fill=RED + (255,))
    elif name == "coin":
        d.ellipse([P(.10, .10), P(.90, .90)], fill=(200, 160, 80, 255)); d.ellipse([P(.18, .18), P(.82, .82)], outline=(150, 110, 50, 255), width=S // 40)
        d.text(P(.50, .50), "L.", font=font(SERIF, int(S * .36)), fill=(120, 80, 30, 255), anchor="mm")
    elif name == "istat":        # calcolatrice / coefficiente
        d.rounded_rectangle([P(.20, .06), P(.80, .94)], S // 20, fill=(60, 64, 70, 255))
        d.rectangle([P(.28, .14), P(.72, .30)], fill=(170, 200, 160, 255))
        d.text(P(.68, .22), "×10.164", font=font(COUR, int(S * .07)), fill=dk, anchor="rm")
        for r in range(4):
            for c in range(3): d.rounded_rectangle([P(.28 + c * .15, .38 + r * .13), P(.40 + c * .15, .48 + r * .13)], S // 60, fill=(200, 196, 186, 255))
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _rc[k] = im
    return im

_PON = {"bank", "chart", "hourglass", "warning", "megaphone", "check", "shield_ok"}
_prev_icon = fx.icon
def _icon(name, size, color=None):
    if isinstance(name, str):
        m = rpic(name, size)
        if m is not None: return m
        if name in _PON: return pon.pic(name, size)
    return _prev_icon(name, size, color)
fx.icon = _icon

def cover_folder(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 28, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 010", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "LA BANCA ROMANA", font=font(SERIF, int(w * .085)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "ROMA · 1889-1894", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im
