# Elementi grafici del caso 024 (l'Atleta di Fano, 1964-2024): statua stilizzata generica (sagoma, nessuna
# riproduzione dell'opera), peschereccio, rete, mare in sezione, campo di cavoli, nave antica, il "viaggio".
# Tutto disegnato da codice: nessuna foto reale, nessun documento originale, nessun logo.
import math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "023-brinks"))
from brk import *
import brk, fi, fx
from fx import *
import pon, inspect
# ------------------------------------------------------------------ mappa larga fino alla California
pon.WB.update(lon0=-130.0, lon1=45.0, lat0=12.0, lat1=62.0, K=28.0)
pon.WPAD = 900
exec(inspect.getsource(pon.world_base).replace("world_base.png", "world_base_fan.png"), pon.__dict__)
exec(inspect.getsource(pon._world_raw).replace("range(-100, 51, 10)", "range(-130, 46, 10)").replace("range(-30, 61, 10)", "range(10, 61, 10)"), pon.__dict__)
pon._wb = None
from pon import WorldMap, WPL

WPL.update({"Fano": (13.02, 43.84), "Pedaso": (13.84, 43.10), "Gubbio": (12.58, 43.35), "Perugia": (12.39, 43.11),
            "Roma": (12.50, 41.90), "Monaco di Baviera": (11.58, 48.14), "Londra": (-0.13, 51.51), "Lussemburgo": (6.13, 49.61),
            "Boston": (-71.06, 42.36), "Malibu": (-118.78, 34.03), "Pesaro": (12.91, 43.91), "Strasburgo": (7.75, 48.57),
            "Atene": (23.73, 37.98), "Olimpia": (21.63, 37.64), "Ancona": (13.52, 43.62), "Croazia": (15.5, 44.6),
            "Washington": (-77.04, 38.90), "Mare Adriatico": (14.6, 43.3)})

BRONZE = (150, 104, 58); BRONZE_D = (96, 64, 36); PATINA = (70, 120, 100); SEA = (22, 58, 92); SEA_D = (10, 26, 48)
_fk = {}

def statue_img(h, crust=0.0, wreath=False, lying=False, label=True):
    """sagoma stilizzata generica di un giovane in bronzo con il braccio destro alzato verso la testa;
    gambe interrotte alle caviglie. crust 0..1 = incrostazioni marine. Non è una riproduzione dell'opera."""
    k = ("st", h, round(crust, 2), wreath, lying, label)
    if k in _fk: return _fk[k]
    S = 3; W_, H_ = int(h * 0.62) * S, h * S
    im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda x, y: (x * W_, y * H_)
    c = BRONZE + (255,); o = BRONZE_D + (255,); lw = max(2, W_ // 80)
    # gambe (peso sulla destra), tagliate alle caviglie
    d.polygon([P(.40, .52), P(.50, .52), P(.47, .74), P(.45, .95), P(.38, .95), P(.39, .74)], fill=c, outline=o)
    d.polygon([P(.52, .52), P(.62, .52), P(.66, .74), P(.66, .94), P(.59, .94), P(.56, .74)], fill=c, outline=o)
    # busto
    d.polygon([P(.36, .20), P(.66, .20), P(.64, .38), P(.62, .54), P(.38, .54), P(.36, .38)], fill=c, outline=o)
    # braccio sinistro lungo il fianco
    d.polygon([P(.64, .21), P(.71, .23), P(.74, .38), P(.73, .50), P(.68, .50), P(.67, .38)], fill=c, outline=o)
    # braccio destro alzato verso la testa
    d.polygon([P(.37, .21), P(.30, .23), P(.22, .14), P(.30, .06), P(.36, .08), P(.30, .15), P(.38, .19)], fill=c, outline=o)
    # collo e testa
    d.rectangle([P(.47, .15), P(.55, .21)], fill=c)
    d.ellipse([P(.42, .03), P(.60, .16)], fill=c, outline=o, width=lw)
    if wreath:
        for j in range(9):
            ang = math.pi * (0.95 + j * 0.13)
            x, y = .51 + .10 * math.cos(ang), .085 + .05 * math.sin(ang)
            d.ellipse([P(x - .025, y - .012), P(x + .025, y + .012)], fill=(110, 150, 70, 255))
    # occhi vuoti (le paste vitree/pietre non ci sono più)
    d.ellipse([P(.46, .08), P(.49, .095)], fill=(30, 22, 16, 255)); d.ellipse([P(.53, .08), P(.56, .095)], fill=(30, 22, 16, 255))
    # luce
    d.line([P(.40, .24), P(.42, .50)], fill=(200, 150, 90, 160), width=lw)
    if crust > 0:
        rr = random.Random(7)
        for _ in range(int(260 * crust)):
            x, y = rr.uniform(.22, .74), rr.uniform(.04, .95)
            px, py = int(x * W_), int(y * H_)
            if 0 <= px < W_ and 0 <= py < H_ and im.getpixel((px, py))[3] > 0:
                r = rr.uniform(.008, .02) * W_
                col = rr.choice([(196, 190, 170), (150, 160, 140), PATINA, (120, 110, 96)])
                d.ellipse([px - r, py - r, px + r, py + r], fill=col + (230,))
    im = im.resize((W_ // S, H_ // S), Image.LANCZOS)
    if lying: im = im.rotate(90, expand=True)
    if label:
        lab = Image.new("RGBA", (im.width, im.height + 34), (0, 0, 0, 0)); lab.paste(im, (0, 0))
        dd = ImageDraw.Draw(lab)
        dd.text((lab.width / 2, im.height + 18), "SAGOMA STILIZZATA · NON È L'OPERA", font=font(COURR, max(12, min(20, lab.width // 16))), fill=GREY + (255,), anchor="mm")
        im = lab
    _fk[k] = im; return im

def fpic(name, size):
    k = (name, size)
    if k in _fk: return _fk[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); lw = max(3, S // 60)
    if name == "statue":
        st = statue_img(int(size * 0.95), label=False); _fk[k] = st; return st
    elif name == "statue_crust":
        st = statue_img(int(size * 0.95), crust=0.9, label=False); _fk[k] = st; return st
    elif name == "statue_wreath":
        st = statue_img(int(size * 0.95), wreath=True, label=False); _fk[k] = st; return st
    elif name == "boat":          # peschereccio generico
        d.polygon([P(.06, .58), P(.94, .58), P(.82, .80), P(.16, .80)], fill=(200, 70, 50, 255), outline=(80, 30, 20, 255))
        d.rectangle([P(.10, .52), P(.90, .60)], fill=(240, 236, 220, 255))
        d.rectangle([P(.52, .30), P(.76, .52)], fill=(240, 236, 220, 255), outline=(90, 90, 90, 255), width=lw)
        d.rectangle([P(.56, .35), P(.62, .42)], fill=(120, 170, 210, 255)); d.rectangle([P(.66, .35), P(.72, .42)], fill=(120, 170, 210, 255))
        d.line([P(.30, .10), P(.30, .54)], fill=(90, 70, 50, 255), width=lw * 2)
        d.line([P(.30, .14), P(.08, .52)], fill=(90, 70, 50, 255), width=lw)
        for j in range(4): d.arc([P(.04 + j * .22, .80), P(.26 + j * .22, .92)], 180, 360, fill=(120, 170, 210, 255), width=lw)
    elif name == "fishing":       # pesce stilizzato
        d.ellipse([P(.14, .32), P(.72, .68)], fill=(120, 160, 190, 255), outline=(50, 80, 110, 255), width=lw)
        d.polygon([P(.70, .50), P(.92, .30), P(.92, .70)], fill=(120, 160, 190, 255), outline=(50, 80, 110, 255))
        d.ellipse([P(.24, .42), P(.32, .50)], fill=(20, 20, 30, 255))
        d.arc([P(.36, .36), P(.56, .64)], 270, 90, fill=(70, 100, 130, 255), width=lw)
    elif name == "handshake":     # due mani che si stringono (schema)
        d.polygon([P(.05, .40), P(.38, .40), P(.62, .56), P(.50, .66), P(.30, .58), P(.05, .58)], fill=(214, 180, 140, 255), outline=(120, 90, 60, 255))
        d.polygon([P(.95, .40), P(.62, .40), P(.38, .56), P(.50, .66), P(.70, .58), P(.95, .58)], fill=(190, 150, 110, 255), outline=(120, 90, 60, 255))
        d.rectangle([P(.0, .36), P(.10, .62)], fill=(60, 80, 130, 255)); d.rectangle([P(.90, .36), P(1.0, .62)], fill=(70, 70, 76, 255))
    elif name == "net":
        for j in range(9):
            d.line([P(.1 + j * .1, .1), P(.3 + j * .05, .9)], fill=(200, 190, 150, 255), width=lw)
        for j in range(8):
            y = .15 + j * .1; d.line([P(.1 + j * .025, y), P(.9 - j * .005, y)], fill=(200, 190, 150, 255), width=lw)
        for j in range(5): d.ellipse([P(.08 + j * .2, .04), P(.16 + j * .2, .12)], fill=(220, 120, 40, 255))
    elif name == "cabbage":
        for j, (x, y, r) in enumerate([(.30, .62, .20), (.70, .62, .20), (.50, .45, .24)]):
            d.ellipse([P(x - r, y - r * .8), P(x + r, y + r * .8)], fill=(90, 150, 80, 255), outline=(40, 90, 40, 255), width=lw)
            d.line([P(x, y - r * .6), P(x, y + r * .6)], fill=(170, 210, 150, 255), width=lw)
        d.rectangle([P(.04, .80), P(.96, .92)], fill=(110, 80, 50, 255))
    elif name == "wreath":        # corona d'ulivo
        for j in range(16):
            ang = math.pi * 2 * j / 16
            x, y = .5 + .30 * math.cos(ang), .5 + .30 * math.sin(ang)
            d.ellipse([P(x - .07, y - .03), P(x + .07, y + .03)], fill=(110, 150, 70, 255), outline=(60, 90, 40, 255))
    elif name == "anchor":
        d.ellipse([P(.42, .06), P(.58, .22)], outline=(170, 170, 180, 255), width=lw * 2)
        d.line([P(.5, .22), P(.5, .86)], fill=(170, 170, 180, 255), width=lw * 3)
        d.line([P(.30, .34), P(.70, .34)], fill=(170, 170, 180, 255), width=lw * 2)
        d.arc([P(.18, .50), P(.82, .92)], 20, 160, fill=(170, 170, 180, 255), width=lw * 3)
    elif name == "oldship":       # nave antica generica
        d.polygon([P(.08, .56), P(.92, .56), P(.78, .76), P(.20, .76)], fill=(120, 80, 50, 255), outline=(60, 40, 20, 255))
        d.line([P(.5, .10), P(.5, .56)], fill=(90, 60, 40, 255), width=lw * 2)
        d.polygon([P(.24, .16), P(.76, .16), P(.72, .48), P(.28, .48)], fill=(230, 220, 190, 255), outline=(140, 120, 90, 255))
        d.polygon([P(.86, .56), P(.98, .42), P(.94, .58)], fill=(120, 80, 50, 255))
        for j in range(4): d.arc([P(.04 + j * .22, .76), P(.26 + j * .22, .88)], 180, 360, fill=(120, 170, 210, 255), width=lw)
    elif name == "waves":
        for r in range(3):
            for j in range(4): d.arc([P(.02 + j * .24, .25 + r * .2), P(.26 + j * .24, .45 + r * .2)], 180, 360, fill=(120, 170, 210, 255), width=lw * 2)
    elif name == "carbon":        # datazione al radiocarbonio: legno del nucleo + "C14"
        d.rectangle([P(.14, .40), P(.62, .70)], fill=(140, 100, 60, 255), outline=(80, 50, 30, 255), width=lw)
        for j in range(4): d.line([P(.16, .45 + j * .06), P(.60, .44 + j * .06)], fill=(100, 70, 40, 255), width=lw)
        d.text(P(.78, .55), "C14", font=font(OSW, int(S * .16), 700), fill=GOLD + (255,), anchor="mm")
    elif name == "crate":
        d.rectangle([P(.12, .28), P(.88, .84)], fill=(170, 130, 80, 255), outline=(90, 60, 30, 255), width=lw)
        for j in range(3): d.line([P(.12, .40 + j * .15), P(.88, .40 + j * .15)], fill=(110, 80, 40, 255), width=lw)
        d.line([P(.12, .28), P(.88, .84)], fill=(110, 80, 40, 255), width=lw)
        d.text(P(.50, .20), "FRAGILE", font=font(OSW, int(S * .09), 700), fill=RED + (255,), anchor="mm")
    elif name == "strasbourg":    # Corte europea: palazzo generico con stelle
        d.rectangle([P(.10, .40), P(.90, .86)], fill=(200, 200, 205, 255), outline=(90, 90, 100, 255), width=lw)
        for j in range(6): d.rectangle([P(.15 + j * .125, .46), P(.21 + j * .125, .80)], fill=(120, 150, 190, 255))
        for j in range(12):
            ang = 2 * math.pi * j / 12; x, y = .5 + .15 * math.cos(ang), .22 + .15 * math.sin(ang)
            d.regular_polygon((x * S, y * S, S * .02), 5, fill=(240, 200, 40, 255))
    elif name == "priest":        # casa con piccola croce: la canonica (schema)
        d.polygon([P(.10, .46), P(.5, .14), P(.90, .46)], fill=(120, 80, 60, 255)); d.rectangle([P(.18, .44), P(.82, .92)], fill=(200, 186, 160, 255))
        d.rectangle([P(.44, .66), P(.56, .92)], fill=(80, 56, 40, 255))
        d.line([P(.5, .02), P(.5, .16)], fill=(200, 170, 80, 255), width=lw * 2); d.line([P(.45, .06), P(.55, .06)], fill=(200, 170, 80, 255), width=lw * 2)
    elif name == "olympia":       # podio / vittoria
        d.rectangle([P(.38, .44), P(.62, .90)], fill=(220, 200, 120, 255)); d.rectangle([P(.10, .60), P(.38, .90)], fill=(190, 190, 200, 255)); d.rectangle([P(.62, .68), P(.90, .90)], fill=(190, 130, 80, 255))
        d.text(P(.5, .66), "1", font=font(OSW, int(S * .2), 700), fill=(60, 40, 20, 255), anchor="mm")
        for j in range(10):
            ang = math.pi * 2 * j / 10; x, y = .5 + .12 * math.cos(ang), .24 + .10 * math.sin(ang)
            d.ellipse([P(x - .04, y - .02), P(x + .04, y + .02)], fill=(110, 150, 70, 255))
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _fk[k] = im; return im

_prev_icon_f = fx.icon
def _icon_f(name, size, color=None):
    if isinstance(name, str):
        m = fpic(name, size)
        if m is not None: return m
    return _prev_icon_f(name, size, color)
fx.icon = _icon_f

def cover_folder24(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 38, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 024", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "L'ATLETA DI FANO", font=font(SERIF, int(w * .085)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "ADRIATICO · 1964-2024", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im


class Mare(El):
    """scenografia principale: il mare in sezione. mode:
    'fondo' statua adagiata sul fondale; 'rete' la rete scende e la solleva; 'bordo' statua sul ponte;
    'rotta' il peschereccio va verso il porto; 'nave' nave antica che affonda (nessuna persona); 'vuoto' fondale senza statua.
    crust 0..1 incrostazioni; label in alto a sinistra."""
    def __init__(self, box, t0, t1=None, mode="fondo", label=None, dur=3.0, crust=0.8, night=False, depth=None,
                 title="MARE ADRIATICO · sezione · schema semplificato · non in scala"):
        super().__init__(t0, t1, 0.35)
        self.box, self.mode, self.label, self.dur, self.crust, self.night, self.depth, self.title = box, mode, label, dur, crust, night, depth, title
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; d = ImageDraw.Draw(lay); al = int(255 * a); k = t - self.t0
        u = ease(min(1.0, k / self.dur)); W_ = x1 - x0
        sy = y0 + (y1 - y0) * 0.30          # superficie
        by = y1 - 70                        # fondale
        sky = (20, 26, 50) if self.night else (120, 160, 200)
        d.rectangle([x0, y0, x1, sy], fill=sky + (al,))
        # acqua con gradiente
        n = 12
        for j in range(n):
            ya, yb = sy + (by - sy) * j / n, sy + (by - sy) * (j + 1) / n
            c = tuple(int(SEA[q] + (SEA_D[q] - SEA[q]) * j / n) for q in range(3))
            d.rectangle([x0, ya, x1, yb + 1], fill=c + (al,))
        for j in range(16):
            wx = x0 + j * W_ / 16 + (k * 30) % (W_ / 16)
            if wx < x1 - 40: d.arc([wx, sy - 10, wx + 70, sy + 12], 180, 360, fill=(200, 225, 240, al), width=3)
        # fondale
        d.rectangle([x0, by, x1, y1], fill=(110, 96, 70, al))
        rr = random.Random(3)
        for _ in range(60):
            px = rr.uniform(x0, x1); qy = by + rr.uniform(4, 60); d.ellipse([px - 6, qy - 3, px + 6, qy + 3], fill=(140, 124, 96, al))
        for j in range(7):
            px = x0 + 80 + j * (W_ - 160) / 6
            for q in range(3): d.line([(px + q * 8, by), (px + q * 8 + math.sin(k * 2 + j + q) * 10, by - 60 - q * 14)], fill=(60, 120, 80, al), width=4)
        # barca
        boat_x = x0 + W_ * 0.62
        if self.mode == "rotta": boat_x = lerp(x0 + W_ * 0.75, x0 + W_ * 0.10, u)
        if self.mode != "nave":
            bp = fpic("boat", 230); img = bp.copy(); img.putalpha(img.getchannel("A").point(lambda v: v * a))
            lay.alpha_composite(img, (int(boat_x - 115), int(sy - 170)))
        sx, sy2 = x0 + W_ * 0.38, by - 30
        st_on = self.mode in ("fondo", "rete", "bordo", "rotta")
        # rete
        if self.mode in ("fondo", "rete"):
            reach = u if self.mode == "rete" else 0.15
            ny = lerp(sy + 30, by - 20, min(1.0, reach * 1.6))
            if self.mode == "rete" and u > 0.6: ny = lerp(by - 20, by - 160, (u - 0.6) / 0.4)
            d.line([(boat_x - 60, sy - 40), (sx + 40, ny)], fill=(200, 190, 150, al), width=3)
            if self.mode == "rete":
                for j in range(6): d.line([(sx - 120 + j * 50, ny - 40), (sx - 80 + j * 40, ny + 40)], fill=(200, 190, 150, int(al * .8)), width=2)
                d.line([(sx - 130, ny - 30), (sx + 140, ny - 30)], fill=(220, 120, 40, al), width=5)
        if st_on:
            lift = 0.0
            if self.mode == "rete": lift = max(0.0, (u - 0.6) / 0.4)
            stim = statue_img(260, crust=self.crust, lying=True, label=False)
            if self.mode in ("bordo", "rotta"):
                stim = statue_img(150, crust=self.crust, lying=True, label=False)
                px, py = boat_x - 200, sy - 58 - stim.height // 2
            else:
                px, py = sx - stim.width // 2, lerp(sy2 - stim.height, sy2 - stim.height - 140, lift)
            img = stim.copy(); img.putalpha(img.getchannel("A").point(lambda v: v * a))
            lay.alpha_composite(img, (int(px), int(py)))
        if self.mode == "nave":
            yy = lerp(sy - 150, by - 160, u); rot = -25 * u
            ship = fpic("oldship", 300).rotate(rot, expand=True); img = ship.copy(); img.putalpha(img.getchannel("A").point(lambda v: v * a * (1 - .3 * u)))
            lay.alpha_composite(img, (int(x0 + W_ * 0.45 - img.width / 2), int(yy)))
        if self.depth:
            d.line([(x1 - 90, sy), (x1 - 90, by)], fill=(240, 236, 220, al), width=3)
            for yy in (sy, by): d.line([(x1 - 110, yy), (x1 - 70, yy)], fill=(240, 236, 220, al), width=3)
            d.text((x1 - 110, (sy + by) / 2), self.depth, font=font(OSW, 30, 700), fill=(240, 236, 220, al), anchor="rm")
        d.text(((x0 + x1) / 2, y1 + 22), self.title, font=font(COURR, 22), fill=GREY + (al,), anchor="mm")
        if self.label:
            f = font(OSW, 32, 700); tw = tl(d, self.label, f)
            d.rounded_rectangle([x0 + 16, y0 + 12, x0 + 40 + tw, y0 + 58], 10, fill=(14, 12, 11, int(220 * a)))
            d.text((x0 + 28, y0 + 35), self.label, font=f, fill=GOLD + (al,), anchor="lm")


class Sala(El):
    """scenografia del museo (schema): sala con piedistallo e statua, vetrina/luci; mode 'statua' | 'vuoto' | 'cassa'"""
    def __init__(self, box, t0, t1=None, mode="statua", label=None, sign="IL MUSEO · SCHEMA", visitors=0,
                 title="schema semplificato · non in scala"):
        super().__init__(t0, t1, 0.35)
        self.box, self.mode, self.label, self.sign, self.visitors, self.title = box, mode, label, sign, visitors, title
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; d = ImageDraw.Draw(lay); al = int(255 * a); k = t - self.t0
        W_ = x1 - x0; fy = y1 - 60
        d.rectangle([x0, y0, x1, fy], fill=(70, 62, 58, al))
        for j in range(5):
            cx = x0 + 120 + j * (W_ - 240) / 4
            d.rectangle([cx - 30, y0 + 40, cx + 30, fy], fill=(90, 82, 76, al))
        d.rectangle([x0, fy, x1, y1], fill=(120, 100, 80, al))
        for j in range(3):
            lx = x0 + W_ * (0.3 + 0.2 * j); d.polygon([(lx - 10, y0), (lx + 10, y0), (lx + 90, fy), (lx - 90, fy)], fill=(255, 240, 200, int(al * .025)))
        cx = (x0 + x1) / 2
        if self.mode in ("statua", "cassa"):
            d.rectangle([cx - 120, fy - 110, cx + 120, fy], fill=(200, 196, 186, al), outline=(120, 116, 110, al), width=3)
        if self.mode == "statua":
            st = statue_img(380, crust=0.0, label=False); img = st.copy(); img.putalpha(img.getchannel("A").point(lambda v: v * a))
            lay.alpha_composite(img, (int(cx - st.width / 2), int(fy - 110 - st.height)))
        elif self.mode == "cassa":
            cr = fpic("crate", 300); img = cr.copy(); img.putalpha(img.getchannel("A").point(lambda v: v * a))
            lay.alpha_composite(img, (int(cx - 150), int(fy - 110 - 270)))
        for j in range(self.visitors):
            vx = x0 + 160 + j * 260 + (60 if j >= 2 else 0)
            if abs(vx - cx) < 200: vx += 420
            brk._man(d, vx, fy - 60, 1.4, [(70, 90, 130), (130, 70, 60), (60, 110, 80), (120, 110, 60)][j % 4], al=al)
        f = font(OSW, 28, 700); tw = tl(d, self.sign, f)
        d.rounded_rectangle([cx - tw / 2 - 20, y0 + 10, cx + tw / 2 + 20, y0 + 54], 8, fill=(14, 12, 11, int(220 * a)))
        d.text((cx, y0 + 32), self.sign, font=f, fill=(240, 236, 220, al), anchor="mm")
        d.text(((x0 + x1) / 2, y1 + 22), self.title, font=font(COURR, 22), fill=GREY + (al,), anchor="mm")
        if self.label:
            f = font(OSW, 32, 700); tw = tl(d, self.label, f)
            d.rounded_rectangle([x0 + 16, y0 + 12, x0 + 40 + tw, y0 + 58], 10, fill=(14, 12, 11, int(220 * a)))
            d.text((x0 + 28, y0 + 35), self.label, font=f, fill=GOLD + (al,), anchor="lm")
