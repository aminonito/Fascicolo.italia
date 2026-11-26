# Elementi grafici del caso 029 (l'affare della collana, Versailles-Parigi 1784-1786): LA COLLANA (scenografia ricorrente:
# una collana stilizzata che perde i diamanti scena dopo scena), sagome generiche di regina e cardinale, boschetto, diamanti.
# Tutto disegnato da codice: nessun ritratto reale, nessun dipinto, nessun gioiello originale (solo schemi).
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "028-smemorato"))
sys.path.insert(0, os.path.join(HERE, "..", "027-dossena"))
from smem import *
import smem, fx

WPL.update({"Versailles": (2.13, 48.80), "Strasburgo": (7.75, 48.58), "San Leo": (12.34, 43.90), "Bruxelles": (4.35, 50.85),
            "La Chaise-Dieu": (3.70, 45.32), "Palermo": (13.36, 38.12), "Londra": (-0.13, 51.51), "Parigi": (2.35, 48.86),
            "Vienna": (16.37, 48.21), "Roma": (12.50, 41.90), "Venezia": (12.33, 45.44)})

DIA = (220, 236, 250, 255); DIA2 = (150, 190, 225, 255); GOLDK = (214, 172, 60, 255); PURP = (150, 30, 50, 255)
_ck = {}
def cpic(name, size):
    k = (name, size)
    if k in _ck: return _ck[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); lw = max(3, S // 60)
    def gem(cx, cy, r, col=DIA):
        d.polygon([P(cx, cy - r), P(cx + r * .8, cy - r * .2), P(cx, cy + r), P(cx - r * .8, cy - r * .2)], fill=col, outline=(90, 120, 150, 255))
        d.line([P(cx - r * .8, cy - r * .2), P(cx + r * .8, cy - r * .2)], fill=(120, 150, 180, 255), width=max(1, lw // 2))
    if name.startswith("necklace"):      # collana stilizzata: necklace, necklace_half, necklace_empty
        miss = {"necklace": 0.0, "necklace_half": 0.5, "necklace_empty": 1.0}.get(name, 0.0)
        for row, (ry, n) in enumerate(((.30, 15), (.40, 17), (.50, 19))):
            for j in range(n):
                a = math.pi * (0.08 + 0.84 * j / (n - 1))
                x = .5 - .40 * math.cos(a); y = .14 + (ry + .02 * row) * math.sin(a) * 1.25
                if (j * 7 + row * 3) % 10 < miss * 10:
                    d.ellipse([P(x - .008, y - .008), P(x + .008, y + .008)], fill=GOLDK)
                else:
                    gem(x, y, .022 + .004 * row)
        for j, x in enumerate((.36, .5, .64)):
            if miss < 1 and not (miss > 0 and j == 1):
                gem(x, .80 + (.04 if j == 1 else 0), .045 if j == 1 else .035)
            d.line([P(x, .68), P(x, .76 + (.04 if j == 1 else 0))], fill=GOLDK, width=lw)
    elif name == "diamond":
        gem(.5, .5, .36)
        for a_ in (30, 150, 270):
            r = .44; d.line([P(.5 + r * math.cos(math.radians(a_)), .5 + r * math.sin(math.radians(a_))), P(.5 + (r + .08) * math.cos(math.radians(a_)), .5 + (r + .08) * math.sin(math.radians(a_)))], fill=GOLDC, width=lw)
    elif name == "diamonds":
        for (x, y, r) in ((.30, .40, .14), (.62, .34, .17), (.48, .66, .15), (.76, .66, .11), (.20, .70, .10)):
            gem(x, y, r)
    elif name == "queen":                # sagoma generica di una regina del Settecento (nessun ritratto)
        d.ellipse([P(.38, .16), P(.62, .42)], fill=SK)
        d.ellipse([P(.34, .02), P(.66, .26)], fill=(225, 225, 230, 255))
        d.polygon([P(.40, .06), P(.44, .0), P(.50, .05), P(.56, .0), P(.60, .06)], fill=GOLDC)
        d.ellipse([P(.43, .27), P(.47, .31)], fill=DARK); d.ellipse([P(.53, .27), P(.57, .31)], fill=DARK)
        d.polygon([P(.42, .46), P(.58, .46), P(.86, .96), P(.14, .96)], fill=(70, 100, 160, 255))
        d.rectangle([P(.46, .42), P(.54, .47)], fill=SK)
    elif name == "lady":                 # sagoma generica di donna del Settecento
        d.ellipse([P(.38, .16), P(.62, .42)], fill=SK)
        d.ellipse([P(.36, .06), P(.64, .26)], fill=HAIR)
        d.ellipse([P(.43, .27), P(.47, .31)], fill=DARK); d.ellipse([P(.53, .27), P(.57, .31)], fill=DARK)
        d.polygon([P(.42, .46), P(.58, .46), P(.80, .96), P(.20, .96)], fill=(120, 60, 70, 255))
        d.rectangle([P(.46, .42), P(.54, .47)], fill=SK)
    elif name == "lady_white":           # la donna in abito bianco nel boschetto
        d.ellipse([P(.38, .16), P(.62, .42)], fill=SK)
        d.ellipse([P(.35, .04), P(.65, .26)], fill=(225, 225, 230, 255))
        d.ellipse([P(.43, .27), P(.47, .31)], fill=DARK); d.ellipse([P(.53, .27), P(.57, .31)], fill=DARK)
        d.polygon([P(.42, .46), P(.58, .46), P(.84, .96), P(.16, .96)], fill=(240, 238, 232, 255), outline=(170, 170, 170, 255))
        d.rectangle([P(.46, .42), P(.54, .47)], fill=SK)
    elif name == "cardinal":             # sagoma generica di un cardinale (nessun ritratto)
        d.ellipse([P(.38, .18), P(.62, .44)], fill=SK)
        d.chord([P(.38, .14), P(.62, .34)], 180, 360, fill=PURP)
        d.ellipse([P(.43, .29), P(.47, .33)], fill=DARK); d.ellipse([P(.53, .29), P(.57, .33)], fill=DARK)
        d.polygon([P(.40, .48), P(.60, .48), P(.78, .96), P(.22, .96)], fill=PURP)
        d.polygon([P(.36, .48), P(.64, .48), P(.58, .62), P(.42, .62)], fill=(200, 60, 70, 255))
        d.line([P(.50, .62), P(.50, .80)], fill=GOLDC, width=lw * 2); d.line([P(.44, .68), P(.56, .68)], fill=GOLDC, width=lw * 2)
    elif name == "grove":                # boschetto di notte
        d.rectangle([P(.04, .82), P(.96, .90)], fill=(50, 80, 50, 255))
        for x, h_ in ((.16, .50), (.38, .40), (.62, .46), (.84, .52)):
            d.rectangle([P(x - .02, .82 - h_ * .4), P(x + .02, .84)], fill=(90, 70, 50, 255))
            d.ellipse([P(x - .13, .82 - h_), P(x + .13, .82 - h_ * .35)], fill=(40, 100, 60, 255))
        d.ellipse([P(.78, .04), P(.92, .18)], fill=(240, 230, 190, 255))
    elif name == "jeweler":              # il gioielliere: banco con astuccio
        d.rectangle([P(.10, .58), P(.90, .88)], fill=(110, 80, 50, 255))
        d.rounded_rectangle([P(.24, .30), P(.76, .58)], radius=S * .03, fill=(30, 30, 60, 255))
        d.arc([P(.32, .34), P(.68, .70)], 200, 340, fill=DIA, width=lw * 2)
        for x in (.36, .44, .50, .56, .64): gem(x, .44 + abs(x - .5) * -.3 + .08, .025)
    elif name == "livre":                # moneta generica d'oro (nessuna moneta reale)
        d.ellipse([P(.18, .18), P(.82, .82)], fill=GOLDK, outline=(150, 110, 30, 255), width=lw * 2)
        d.text(P(.5, .5), "L", font=font(SERIF, int(S * .34)), fill=(120, 80, 20, 255), anchor="mm")
    elif name == "quill":                # penna d'oca e lettera
        d.rectangle([P(.16, .20), P(.70, .86)], fill=PAPER, outline=(150, 130, 100, 255), width=lw)
        for y in (.34, .44, .54, .64): d.line([P(.24, y), P(.62, y)], fill=(90, 90, 100, 255), width=lw)
        d.polygon([P(.86, .10), P(.92, .16), P(.56, .74), P(.52, .74)], fill=(235, 235, 235, 255), outline=(120, 120, 120, 255))
    elif name == "potion":               # boccetta di un «rimedio» (nessuna etichetta)
        d.rectangle([P(.44, .10), P(.56, .26)], fill=(120, 90, 60, 255))
        d.rectangle([P(.40, .24), P(.60, .32)], fill=(170, 170, 180, 255))
        d.ellipse([P(.22, .30), P(.78, .90)], fill=(110, 60, 150, 255), outline=(200, 200, 210, 255), width=lw)
        d.ellipse([P(.32, .42), P(.44, .54)], fill=(190, 150, 230, 255))
        for a_ in (200, 250, 300, 340):
            r = .40; d.ellipse([P(.5 + r * math.cos(math.radians(a_)) - .02, .58 + r * math.sin(math.radians(a_)) - .02), P(.5 + r * math.cos(math.radians(a_)) + .02, .58 + r * math.sin(math.radians(a_)) + .02)], fill=GOLDC)
    elif name == "mirrors":              # galleria degli specchi stilizzata
        d.rectangle([P(.04, .20), P(.96, .86)], fill=(120, 96, 60, 255))
        for x in (.10, .30, .50, .70): d.rectangle([P(x, .30), P(x + .16, .76)], fill=(190, 210, 225, 255), outline=GOLDK, width=lw)
        d.line([P(.04, .86), P(.96, .86)], fill=GOLDK, width=lw * 2)
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _ck[k] = im; return im

_prev_icon_c = fx.icon
def _icon_c(name, size, color=None):
    if isinstance(name, str):
        m = cpic(name, size)
        if m is not None: return m
    return _prev_icon_c(name, size, color)
fx.icon = _icon_c
smem.giu.pic = lambda name, size: fx.icon(name, size)

def cover_folder29(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 38, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 029", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "LA COLLANA", font=font(SERIF, int(w * .09)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "VERSAILLES · PARIGI · 1785", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im
