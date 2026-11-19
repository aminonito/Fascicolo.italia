# Elementi grafici del caso 014 (Wanna Marchi e la società Asciè, 2001-2009): studio delle televendite
# (scenografia ricorrente), salotto con telecamere nascoste (la trappola), icone del caso (sale, edera, numeri
# del lotto, vasetto di crema, occhio del "malocchio", banconota generica in lire, pacco).
# Tutto disegnato da codice: nessuna foto reale, nessun logo o marchio di emittenti o programmi.
import math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "012-parmalat"))
from par import *                      # catena completa di icone e scenografie (tor.Studio, Aula, WorldMap...)
import par
import fi
import fx
from fx import *
from pon import WorldMap, WPL
Aula = sys.modules["tor"].Aula if "tor" in sys.modules else None

WPL.update({"Bologna": (11.34, 44.49), "Milano": (9.19, 45.46), "Brasile": (-47.9, -15.8), "Genova": (8.93, 44.41)})
fi.PLACES.update({"Bologna": (11.34, 44.49), "Milano": (9.19, 45.46), "Solaro": (9.08, 45.61)})
fx.COAT.update(dict(host=(150, 36, 52), mage=(92, 60, 130), clerk=(70, 90, 110)))
PURPLE = (150, 110, 200)

# ---------------------------------------------------------------- icone del caso
_wc = {}
def wpic(name, size):
    k = (name, size)
    if k in _wc: return _wc[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); w = max(2, S // 22)
    ink = INK + (255,); wh = (246, 244, 238, 255)
    if name == "salt":          # bustina di sale da cucina generica
        d.polygon([P(.22, .14), P(.78, .14), P(.84, .92), P(.16, .92)], fill=(236, 236, 240, 255), outline=(150, 150, 160, 255))
        d.rectangle([P(.22, .10), P(.78, .18)], fill=(200, 200, 210, 255))
        for k in range(3): d.line([P(.26 + k * .2, .10), P(.30 + k * .2, .18)], fill=(170, 170, 180, 255), width=w // 2)
        d.text(P(.5, .50), "SALE", font=font(OSW, int(S * .17), 700), fill=(60, 80, 140, 255), anchor="mm")
        for k in range(14):
            rx, ry = .30 + (k * 37 % 40) / 100, .66 + (k * 23 % 22) / 100
            d.rectangle([P(rx, ry), P(rx + .03, ry + .03)], fill=(250, 250, 255, 255), outline=(190, 190, 200, 255))
    elif name == "salt_pile":   # mucchietto di sale
        d.pieslice([P(.10, .40), P(.90, 1.30)], 180, 360, fill=(244, 244, 248, 255))
        rng = random.Random(4)
        for k in range(60):
            x, y = rng.uniform(.18, .82), rng.uniform(.52, .84)
            d.rectangle([P(x, y), P(x + .025, y + .025)], fill=(255, 255, 255, 255), outline=(200, 200, 210, 255))
    elif name == "ivy":         # rametto di edera
        d.line([P(.14, .92), P(.40, .60), P(.62, .38), P(.86, .10)], fill=(90, 110, 60, 255), width=S // 30)
        for (cx, cy, r) in ((.28, .70, .13), (.50, .48, .14), (.70, .26, .12), (.20, .48, .10), (.62, .58, .11), (.84, .14, .08)):
            pts = [P(cx, cy - r), P(cx + r * .9, cy - r * .2), P(cx + r * .5, cy + r * .8), P(cx, cy + r * .4), P(cx - r * .5, cy + r * .8), P(cx - r * .9, cy - r * .2)]
            d.polygon(pts, fill=(60, 130, 70, 255), outline=(40, 90, 50, 255))
            d.line([P(cx, cy - r * .6), P(cx, cy + r * .3)], fill=(150, 200, 140, 255), width=max(1, w // 3))
    elif name == "lotto":       # schedina generica con 4 numeri
        d.rounded_rectangle([P(.10, .12), P(.90, .88)], S // 24, fill=(244, 240, 226, 255), outline=(170, 140, 80, 255), width=w // 2)
        d.text(P(.5, .23), "NUMERI", font=font(OSW, int(S * .11), 700), fill=RED + (255,), anchor="mm")
        for k, n in enumerate(("7", "21", "48", "90")):
            cx, cy = .30 + (k % 2) * .40, .48 + (k // 2) * .25
            d.ellipse([P(cx - .14, cy - .11), P(cx + .14, cy + .11)], outline=ink, width=w // 2)
            d.text(P(cx, cy), n, font=font(OSW, int(S * .12), 700), fill=ink, anchor="mm")
    elif name == "balls":       # palline numerate
        cols = [(200, 52, 42), (218, 176, 96), (60, 110, 170), (80, 150, 90), (150, 110, 200)]
        for k, n in enumerate(("12", "33", "57", "71", "86")):
            cx = .14 + k * .18; cy = .52 + (.10 if k % 2 else -.06)
            d.ellipse([P(cx - .11, cy - .11), P(cx + .11, cy + .11)], fill=cols[k] + (255,))
            d.ellipse([P(cx - .07, cy - .06), P(cx + .07, cy + .07)], fill=wh)
            d.text(P(cx, cy + .005), n, font=font(OSW, int(S * .075), 700), fill=ink, anchor="mm")
    elif name == "jar":         # vasetto di crema generico
        d.rounded_rectangle([P(.18, .40), P(.82, .90)], S // 14, fill=(240, 230, 220, 255), outline=(170, 150, 130, 255), width=w // 2)
        d.rounded_rectangle([P(.14, .26), P(.86, .42)], S // 24, fill=(200, 160, 170, 255))
        d.rectangle([P(.24, .54), P(.76, .74)], fill=(220, 120, 140, 255))
        d.text(P(.5, .64), "CREMA", font=font(OSW, int(S * .09), 700), fill=wh, anchor="mm")
    elif name == "algae":       # alghe stilizzate
        for k in range(5):
            x = .18 + k * .16
            pts = [P(x + .05 * math.sin(j * 1.3 + k), .92 - j * .14) for j in range(6)]
            d.line(pts, fill=(60, 140 + k * 10, 100, 255), width=S // 18, joint="curve")
    elif name == "eye":         # occhio del "malocchio" (simbolo)
        d.chord([P(.04, .20), P(.96, .80)], 200, 340, fill=wh)
        d.chord([P(.04, .20), P(.96, .80)], 20, 160, fill=wh)
        d.polygon([P(.08, .50), P(.5, .26), P(.92, .50), P(.5, .74)], fill=wh)
        d.ellipse([P(.36, .32), P(.64, .68)], fill=(60, 110, 170, 255)); d.ellipse([P(.44, .42), P(.56, .58)], fill=(20, 20, 24, 255))
        d.ellipse([P(.47, .40), P(.52, .45)], fill=wh)
        d.line([P(.08, .50), P(.5, .26), P(.92, .50)], fill=ink, width=w)
    elif name == "amulet":      # cornetto/talismano generico
        d.line([P(.50, .06), P(.50, .20)], fill=GOLD + (255,), width=w)
        d.ellipse([P(.44, .14), P(.56, .24)], outline=GOLD + (255,), width=w // 2)
        d.polygon([P(.36, .24), P(.64, .24), P(.60, .50), P(.52, .80), P(.44, .94), P(.46, .70), P(.40, .48)], fill=RED + (255,))
    elif name == "lire":        # banconota generica in lire (ricostruzione, nessun disegno reale)
        d.rounded_rectangle([P(.04, .24), P(.96, .76)], S // 30, fill=(214, 196, 150, 255), outline=(140, 120, 80, 255), width=w // 2)
        d.ellipse([P(.10, .34), P(.36, .66)], outline=(140, 120, 80, 255), width=w // 2)
        d.text(P(.64, .44), "100.000", font=font(OSW, int(S * .13), 700), fill=(90, 70, 40, 255), anchor="mm")
        d.text(P(.64, .62), "LIRE", font=font(OSW, int(S * .09), 600), fill=(90, 70, 40, 255), anchor="mm")
    elif name == "parcel":      # pacco postale
        d.polygon([P(.10, .34), P(.50, .18), P(.90, .34), P(.50, .50)], fill=(196, 160, 110, 255))
        d.polygon([P(.10, .34), P(.50, .50), P(.50, .92), P(.10, .76)], fill=(170, 130, 86, 255))
        d.polygon([P(.90, .34), P(.50, .50), P(.50, .92), P(.90, .76)], fill=(150, 112, 72, 255))
        d.line([P(.30, .26), P(.70, .42), P(.70, .84)], fill=(230, 220, 190, 255), width=w)
    elif name == "hiddencam":   # telecamera nascosta (piccola, con led rosso)
        d.rounded_rectangle([P(.14, .34), P(.74, .70)], S // 20, fill=(40, 40, 46, 255))
        d.polygon([P(.74, .42), P(.94, .30), P(.94, .74), P(.74, .62)], fill=(60, 60, 66, 255))
        d.ellipse([P(.22, .40), P(.30, .48)], fill=RED + (255,))
        d.ellipse([P(.38, .42), P(.58, .62)], fill=(20, 20, 24, 255), outline=(120, 120, 130, 255), width=w // 2)
    elif name == "glass_salt":  # bicchiere d'acqua con sale sul fondo
        d.polygon([P(.24, .10), P(.76, .10), P(.68, .92), P(.32, .92)], fill=(170, 200, 230, 110), outline=(220, 235, 245, 255))
        d.polygon([P(.26, .30), P(.74, .30), P(.68, .92), P(.32, .92)], fill=(120, 170, 220, 120))
        d.polygon([P(.33, .80), P(.67, .80), P(.66, .91), P(.34, .91)], fill=(250, 250, 255, 255))
    elif name == "studio_tv":   # televisore con scritta televendita
        d.rounded_rectangle([P(.06, .14), P(.94, .80)], S // 20, fill=(40, 38, 40, 255))
        d.rectangle([P(.12, .20), P(.88, .72)], fill=(70, 40, 60, 255))
        d.text(P(.5, .46), "TELEVENDITA", font=font(OSW, int(S * .10), 700), fill=GOLD + (255,), anchor="mm")
        d.line([P(.40, .80), P(.30, .94)], fill=(40, 38, 40, 255), width=w); d.line([P(.60, .80), P(.70, .94)], fill=(40, 38, 40, 255), width=w)
    elif name == "gdf":         # distintivo generico (nessuno stemma reale)
        d.polygon([P(.5, .06), P(.88, .22), P(.82, .66), P(.5, .94), P(.18, .66), P(.12, .22)], fill=(200, 160, 50, 255), outline=(120, 90, 30, 255))
        d.polygon([P(.5, .18), P(.76, .30), P(.72, .62), P(.5, .82), P(.28, .62), P(.24, .30)], fill=(40, 70, 110, 255))
        d.text(P(.5, .50), "GdF", font=font(OSW, int(S * .16), 700), fill=(240, 220, 150, 255), anchor="mm")
    elif name == "warn":        # telefono con fulmine (minaccia)
        d.polygon([P(.50, .06), P(.96, .88), P(.04, .88)], fill=GOLD + (255,))
        d.text(P(.5, .60), "!", font=font(OSW, int(S * .42), 700), fill=ink, anchor="mm")
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _wc[k] = im
    return im

_prev_icon_w = fx.icon
def _icon_w(name, size, color=None):
    if isinstance(name, str):
        m = wpic(name, size)
        if m is not None: return m
    return _prev_icon_w(name, size, color)
fx.icon = _icon_w

# ---------------------------------------------------------------- scenografia: studio delle televendite
class Tele(El):
    """studio televisivo delle televendite (schema): fondale, luci, cartello, banco con i prodotti,
    telefoni che squillano, contatore di telefonate. items: [(t, nome_icona)] prodotti sul banco (gli ultimi 4).
    calls: (t0, t1) telefoni che squillano; mood: 'beauty' (rosa) o 'luck' (viola, magia)."""
    def __init__(self, box, t0, t1=None, items=(), calls=None, sign="TELEVENDITE", mood="beauty", label="ricostruzione · schema"):
        super().__init__(t0, t1, 0.4); self.box, self.items, self.calls, self.sign, self.mood, self.label = box, list(items), calls, sign, mood, label
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; w, h = x1 - x0, y1 - y0; d = ImageDraw.Draw(lay); al = int(255 * a)
        base = (60, 30, 44) if self.mood == "beauty" else (40, 26, 60)
        c1 = (150, 60, 90) if self.mood == "beauty" else (96, 60, 150)
        c2 = (120, 44, 72) if self.mood == "beauty" else (74, 44, 120)
        d.rectangle([x0, y0, x1, y1], fill=base + (al,))
        for k in range(12):
            xx = x0 + k * w / 12
            d.rectangle([xx, y0, xx + w / 24, y0 + h * .70], fill=c1 + (al,))
            d.rectangle([xx + w / 24, y0, xx + w / 12, y0 + h * .70], fill=c2 + (al,))
        if self.mood == "luck":
            rng = random.Random(3)
            for k in range(26):
                sx, sy = x0 + rng.uniform(.02, .98) * w, y0 + rng.uniform(.05, .62) * h
                tw = 0.5 + 0.5 * math.sin(t * 3 + k)
                r = 3 + 3 * tw
                d.polygon([(sx, sy - r * 2), (sx + r * .6, sy - r * .6), (sx + r * 2, sy), (sx + r * .6, sy + r * .6), (sx, sy + r * 2), (sx - r * .6, sy + r * .6), (sx - r * 2, sy), (sx - r * .6, sy - r * .6)], fill=(255, 230, 150, int(al * (0.4 + 0.6 * tw))))
        if self.sign:
            d.rectangle([x0 + w * .30, y0 + h * .08, x0 + w * .70, y0 + h * .21], fill=(22, 20, 30, al), outline=GOLD + (al,), width=3)
            d.text((x0 + w * .5, y0 + h * .145), self.sign, font=font(OSW, int(h * .06), 600), fill=GOLD + (al,), anchor="mm")
        d.rectangle([x0, y0 + h * .70, x1, y1], fill=(70, 58, 50, al))
        for k in range(9):
            d.line([(x0 + w * .5 + (k - 4) * w * .03, y0 + h * .70), (x0 + w * .5 + (k - 4) * w * .11, y1)], fill=(84, 70, 60, al), width=2)
        for cx in (x0 + w * .2, x0 + w * .5, x0 + w * .8):
            cone = Image.new("RGBA", lay.size, (0, 0, 0, 0)); dc = ImageDraw.Draw(cone)
            dc.polygon([(cx - 18, y0 + 8), (cx + 18, y0 + 8), (cx + w * .11, y1), (cx - w * .11, y1)], fill=(255, 240, 200, int(24 * a)))
            lay.alpha_composite(cone)
            d.ellipse([cx - 20, y0 + 2, cx + 20, y0 + 28], fill=(240, 230, 200, al))
        # banco al centro con i prodotti
        bx0, bx1, by = x0 + w * .22, x0 + w * .62, y0 + h * .66
        d.rectangle([bx0, by, bx1, by + h * .16], fill=(200, 180, 150, al), outline=(150, 120, 90, al), width=3)
        d.rectangle([bx0, by + h * .16, bx1, by + h * .19], fill=(140, 110, 80, al))
        vis = [it for it in self.items if t >= it[0]][-4:]
        for k, (ti, nm) in enumerate(vis):
            u = min(1, (t - ti) / 0.35); s_ = 0.6 + 0.4 * back(u) if u < 1 else 1
            px = bx0 + (k + 0.5) * (bx1 - bx0) / 4; py = by - h * .07
            im = fx.icon(nm, int(h * .15 * s_)); place(lay, im, (px, py), "mm", a * min(1, u * 2))
        # banco dei telefoni a destra
        tx0, tx1, ty = x0 + w * .68, x0 + w * .97, y0 + h * .80
        d.rectangle([tx0, ty, tx1, ty + h * .10], fill=(150, 130, 100, al))
        for k in range(4):
            px = tx0 + (k + 0.5) * (tx1 - tx0) / 4; py = ty - h * .02
            rr = self.calls and self.calls[0] <= t <= self.calls[1] and math.sin((t - self.calls[0]) * 16 + k * 1.9) > 0.1
            jig = (math.sin(t * 70 + k) * 4) if rr else 0
            place(lay, fx.icon("phone", int(h * .08)), (px + jig, py), "mm", a)
            if rr: d.ellipse([px - 8, py - h * .07 - 8, px + 8, py - h * .07 + 8], fill=RED + (al,))
        if self.label: d.text((x1 - 14, y1 - 10), self.label, font=font(COURR, 20), fill=(200, 190, 176, int(al * .8)), anchor="rs")

# ---------------------------------------------------------------- scenografia: il salotto della trappola
class Salotto(El):
    """salotto (schema): parete, finestra, quadretto, tavolino con telefono, divano, porta.
    cams: [(t, (u, v))] telecamere nascoste (posizioni relative) che compaiono con un cerchio rosso;
    ring: (t0, t1) il telefono squilla; door_t: la porta si apre"""
    def __init__(self, box, t0, t1=None, cams=(), ring=None, door_t=None, label="ricostruzione · schema non in scala"):
        super().__init__(t0, t1, 0.4); self.box, self.cams, self.ring, self.door_t, self.label = box, list(cams), ring, door_t, label
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; w, h = x1 - x0, y1 - y0; d = ImageDraw.Draw(lay); al = int(255 * a)
        d.rectangle([x0, y0, x1, y1], fill=(92, 80, 66, al))
        for k in range(24): d.line([(x0 + k * w / 24, y0), (x0 + k * w / 24, y0 + h * .72)], fill=(100, 88, 72, al), width=6)
        d.rectangle([x0, y0 + h * .72, x1, y1], fill=(110, 82, 58, al))
        for k in range(10): d.line([(x0, y0 + h * .72 + k * h * .03), (x1, y0 + h * .72 + k * h * .03)], fill=(96, 70, 50, al), width=2)
        # finestra
        fx0, fy0 = x0 + w * .06, y0 + h * .12
        d.rectangle([fx0, fy0, fx0 + w * .18, fy0 + h * .34], fill=(120, 160, 190, al), outline=(220, 210, 190, al), width=8)
        d.line([(fx0 + w * .09, fy0), (fx0 + w * .09, fy0 + h * .34)], fill=(220, 210, 190, al), width=6)
        # quadretto
        d.rectangle([x0 + w * .40, y0 + h * .16, x0 + w * .52, y0 + h * .32], fill=(160, 140, 100, al), outline=(120, 90, 50, al), width=6)
        # porta (destra)
        dx0, dx1 = x0 + w * .80, x0 + w * .94; dy0 = y0 + h * .20
        op = 0 if self.door_t is None or t < self.door_t else ease(min(1, (t - self.door_t) / 0.6))
        d.rectangle([dx0, dy0, dx1, y0 + h * .72], fill=(40, 30, 24, al))
        d.rectangle([dx0, dy0, dx1 - (dx1 - dx0) * .8 * op, y0 + h * .72], fill=(130, 92, 60, al), outline=(90, 60, 40, al), width=4)
        d.ellipse([dx1 - (dx1 - dx0) * .8 * op - 24, y0 + h * .46, dx1 - (dx1 - dx0) * .8 * op - 12, y0 + h * .49], fill=GOLD + (al,))
        # divano
        sx0, sx1, sy = x0 + w * .10, x0 + w * .42, y0 + h * .58
        d.rounded_rectangle([sx0, sy, sx1, sy + h * .20], 20, fill=(120, 60, 60, al))
        d.rounded_rectangle([sx0 - 14, sy + h * .06, sx0 + 26, sy + h * .22], 12, fill=(100, 50, 50, al))
        d.rounded_rectangle([sx1 - 26, sy + h * .06, sx1 + 14, sy + h * .22], 12, fill=(100, 50, 50, al))
        # tavolino con telefono
        tx, ty = x0 + w * .60, y0 + h * .66
        d.rectangle([tx - w * .07, ty, tx + w * .07, ty + h * .03], fill=(150, 110, 70, al))
        d.line([(tx - w * .06, ty + h * .03), (tx - w * .06, ty + h * .16)], fill=(150, 110, 70, al), width=6)
        d.line([(tx + w * .06, ty + h * .03), (tx + w * .06, ty + h * .16)], fill=(150, 110, 70, al), width=6)
        rr = self.ring and self.ring[0] <= t <= self.ring[1] and math.sin((t - self.ring[0]) * 16) > 0.0
        jig = math.sin(t * 70) * 4 if rr else 0
        place(lay, fx.icon("phone", int(h * .10)), (tx + jig, ty - h * .045), "mm", a)
        if rr:
            for r_ in (20, 34): d.arc([tx - r_, ty - h * .10 - r_, tx + r_, ty - h * .10 + r_], 200, 340, fill=RED + (al,), width=4)
        for (tc, (u, v)) in self.cams:
            if t < tc: continue
            ca = a * min(1, (t - tc) / 0.3); cx, cy = x0 + w * u, y0 + h * v
            place(lay, fx.icon("hiddencam", int(h * .09)), (cx, cy), "mm", ca)
            pr = 40 + 8 * math.sin(t * 6)
            d.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], outline=RED + (int(255 * ca),), width=5)
        if self.label: d.text((x1 - 14, y1 - 10), self.label, font=font(COURR, 20), fill=(220, 210, 196, int(al * .8)), anchor="rs")

def cover_folder(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 33, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 014", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "IL SALE DEL MALOCCHIO", font=font(SERIF, int(w * .075)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "TELEVENDITE · 2001-2009", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im

def phone_note(lines, w=520, title="LA TELEFONATA", seed=12):
    """appunto/trascrizione ricostruita (non originale)"""
    return label_card(lines, w, title=title, seed=seed, size=30)
