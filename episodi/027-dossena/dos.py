# Elementi grafici del caso 027 (Alceo Dossena, lo scultore dei falsi, 1916-1937): IL LABORATORIO (scenografia
# ricorrente), la statua che viaggia da Roma ai musei d'America. Tutto disegnato da codice: nessuna foto reale,
# nessuna opera originale riprodotta (sculture come sagome stilizzate), nessun logo di musei.
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "026-vallesusa"))
from vfs import *
import vfs, giu, fi, fx
from fx import *

WPL.update({"Cremona": (10.02, 45.13), "Roma": (12.50, 41.90), "Firenze": (11.25, 43.77), "Venezia": (12.33, 45.44),
            "Boston": (-71.06, 42.36), "New York": (-74.00, 40.71), "Cleveland": (-81.69, 41.50), "Pittsburgh": (-79.99, 40.44),
            "Pescia": (10.69, 43.90), "Rovereto": (11.04, 45.89), "Milano": (9.19, 45.46), "Siena": (11.33, 43.32)})

def cover_folder27(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 38, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 027", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "IL CASO DOSSENA", font=font(SERIF, int(w * .08)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "CREMONA · ROMA · BOSTON", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im

MARB = (236, 230, 218, 255); MARB2 = (200, 192, 178, 255); STONE = (150, 140, 126, 255)
_dk = {}
def dpic(name, size):
    k = (name, size)
    if k in _dk: return _dk[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); lw = max(3, S // 60)
    def figure(cx, top, h, col=MARB, child=False, wings=False, veil=True):
        # sagoma stilizzata di una statua (nessuna opera reale riprodotta)
        if wings:
            d.polygon([P(cx - .02, top + .22 * h), P(cx - .26, top + .05 * h), P(cx - .16, top + .55 * h)], fill=MARB2)
        d.ellipse([P(cx - .07, top), P(cx + .07, top + .15 * h)], fill=col)
        if veil: d.polygon([P(cx - .09, top + .04 * h), P(cx, top - .02 * h), P(cx + .09, top + .04 * h), P(cx + .11, top + .30 * h), P(cx - .11, top + .30 * h)], fill=MARB2)
        d.polygon([P(cx - .08, top + .16 * h), P(cx + .08, top + .16 * h), P(cx + .17, top + h), P(cx - .17, top + h)], fill=col)
        for j in range(4): d.line([P(cx - .10 + j * .065, top + .35 * h), P(cx - .13 + j * .085, top + .98 * h)], fill=MARB2, width=lw)
        if child:
            d.ellipse([P(cx + .02, top + .28 * h), P(cx + .11, top + .37 * h)], fill=col, outline=MARB2, width=lw // 2)
            d.ellipse([P(cx - .02, top + .36 * h), P(cx + .12, top + .55 * h)], fill=col, outline=MARB2, width=lw // 2)
    if name == "statue":            # statua stilizzata su piedistallo
        figure(.50, .06, .74); d.rectangle([P(.28, .82), P(.72, .96)], fill=STONE)
    elif name == "madonna":         # Madonna col Bambino, sagoma generica
        figure(.48, .06, .76, child=True); d.rectangle([P(.26, .84), P(.74, .96)], fill=STONE)
    elif name == "annunc":          # coppia di statue: angelo e Vergine (sagome)
        figure(.30, .10, .72, wings=True, veil=False); figure(.72, .10, .72)
        d.rectangle([P(.10, .84), P(.50, .95)], fill=STONE); d.rectangle([P(.52, .84), P(.92, .95)], fill=STONE)
    elif name == "kore":            # fanciulla arcaica (sagoma)
        figure(.50, .08, .78, veil=False)
        d.line([P(.40, .14), P(.38, .34)], fill=(150, 120, 80, 255), width=lw * 2); d.line([P(.60, .14), P(.62, .34)], fill=(150, 120, 80, 255), width=lw * 2)
        d.rectangle([P(.30, .86), P(.70, .96)], fill=STONE)
    elif name == "athena":          # figura con elmo e scudo (sagoma)
        figure(.48, .10, .74, veil=False)
        d.polygon([P(.41, .12), P(.48, .02), P(.55, .12)], fill=(180, 160, 110, 255))
        d.ellipse([P(.60, .40), P(.86, .70)], fill=MARB2, outline=STONE, width=lw)
        d.rectangle([P(.28, .84), P(.70, .96)], fill=STONE)
    elif name == "sarcoph":         # monumento funebre rinascimentale generico (nessun originale)
        d.rectangle([P(.12, .08), P(.88, .16)], fill=MARB2)
        d.polygon([P(.14, .16), P(.86, .16), P(.80, .30), P(.20, .30)], fill=MARB)
        d.rectangle([P(.18, .30), P(.82, .44)], fill=MARB2)
        d.line([P(.24, .37), P(.76, .37)], fill=STONE, width=lw)  # figura distesa (linea)
        d.ellipse([P(.22, .32), P(.30, .40)], fill=MARB)
        d.rectangle([P(.14, .46), P(.86, .74)], fill=MARB)
        for x in (.22, .78): d.ellipse([P(x - .06, .52), P(x + .06, .66)], outline=STONE, width=lw)
        d.rectangle([P(.34, .54), P(.66, .64)], outline=STONE, width=lw // 2)
        d.rectangle([P(.08, .76), P(.92, .90)], fill=STONE)
    elif name == "tondo":           # tondo in terracotta (generico)
        d.ellipse([P(.08, .08), P(.92, .92)], fill=(196, 110, 70, 255), outline=(150, 80, 50, 255), width=lw * 2)
        d.ellipse([P(.38, .22), P(.56, .40)], fill=(220, 140, 96, 255)); d.polygon([P(.30, .40), P(.64, .40), P(.72, .80), P(.24, .80)], fill=(220, 140, 96, 255))
        d.ellipse([P(.54, .46), P(.66, .58)], fill=(232, 160, 116, 255))
    elif name == "marble":          # blocco di marmo
        d.polygon([P(.14, .34), P(.62, .34), P(.86, .20), P(.38, .20)], fill=(246, 242, 234, 255))
        d.rectangle([P(.14, .34), P(.62, .88)], fill=MARB); d.polygon([P(.62, .34), P(.86, .20), P(.86, .74), P(.62, .88)], fill=MARB2)
        for a_, b_ in (((.22, .44), (.40, .60)), ((.40, .60), (.36, .80)), ((.70, .40), (.78, .62))): d.line([P(*a_), P(*b_)], fill=(170, 164, 156, 255), width=lw // 2 + 1)
    elif name == "broken":          # statua con un braccio spezzato (rotture "antiche")
        figure(.48, .08, .76, veil=False); d.rectangle([P(.28, .84), P(.70, .96)], fill=STONE)
        d.polygon([P(.70, .70), P(.86, .74), P(.82, .82), P(.68, .80)], fill=MARB2)
        d.line([P(.58, .36), P(.66, .44)], fill=(60, 50, 40, 255), width=lw)
    elif name == "xray":            # radiografia: sagoma con chiodi moderni
        d.rectangle([P(.12, .04), P(.88, .96)], fill=(20, 30, 40, 255), outline=(90, 110, 130, 255), width=lw)
        figure(.50, .12, .74, col=(120, 160, 190, 255), veil=False)
        for y in (.40, .55, .70): d.line([P(.44, y), P(.56, y + .02)], fill=(250, 250, 250, 255), width=lw * 2); d.ellipse([P(.42, y - .02), P(.46, y + .02)], fill=(250, 250, 250, 255))
    elif name == "workshop":        # laboratorio dello scultore: banco, attrezzi, blocco
        d.rectangle([P(.06, .60), P(.94, .68)], fill=(130, 90, 54, 255)); d.rectangle([P(.10, .68), P(.16, .94)], fill=(110, 76, 44, 255)); d.rectangle([P(.84, .68), P(.90, .94)], fill=(110, 76, 44, 255))
        d.rectangle([P(.56, .30), P(.82, .60)], fill=MARB); d.ellipse([P(.62, .14), P(.76, .30)], fill=MARB)
        d.line([P(.20, .56), P(.44, .44)], fill=(160, 160, 170, 255), width=lw * 2); d.rectangle([P(.16, .50), P(.26, .60)], fill=(120, 80, 50, 255))
    elif name == "abbey_x":         # abbazia "mai esistita": rudere con punto di domanda
        d.polygon([P(.14, .44), P(.50, .14), P(.86, .44)], fill=(140, 120, 100, 255)); d.rectangle([P(.18, .44), P(.82, .90)], fill=(120, 104, 90, 255))
        d.rectangle([P(.42, .62), P(.58, .90)], fill=(50, 40, 34, 255))
        d.line([P(.18, .60), P(.36, .52), P(.30, .74)], fill=(40, 34, 30, 255), width=lw)
        d.text(P(.50, .40), "?", font=font(OSW, int(S * .30), 700), fill=(230, 190, 40, 255), anchor="mm")
    elif name == "price":           # cartellino del prezzo
        d.polygon([P(.10, .30), P(.70, .30), P(.92, .50), P(.70, .70), P(.10, .70)], fill=(230, 190, 40, 255)); d.ellipse([P(.70, .46), P(.78, .54)], fill=(40, 34, 30, 255))
        d.text(P(.40, .50), "$", font=font(OSW, int(S * .26), 700), fill=(40, 34, 30, 255), anchor="mm")
    elif name == "signature":       # firma su una base di marmo
        d.rectangle([P(.08, .40), P(.92, .72)], fill=MARB, outline=STONE, width=lw)
        d.line([P(.18, .62), P(.28, .48), P(.34, .62), P(.42, .50), P(.50, .60), P(.62, .52), P(.80, .56)], fill=(60, 50, 40, 255), width=lw)
        d.line([P(.62, .74), P(.80, .92)], fill=(160, 160, 170, 255), width=lw * 2)
    elif name == "auction":         # asta: martelletto e cartellino numerato
        d.rectangle([P(.08, .66), P(.60, .76)], fill=(120, 80, 50, 255))
        d.line([P(.30, .20), P(.54, .56)], fill=(150, 104, 60, 255), width=lw * 3); d.rectangle([P(.14, .10), P(.46, .30)], fill=(110, 70, 40, 255))
        d.rectangle([P(.62, .30), P(.92, .70)], fill=(240, 232, 214, 255), outline=STONE, width=lw)
        d.text(P(.77, .50), "39", font=font(OSW, int(S * .18), 700), fill=(40, 34, 30, 255), anchor="mm")
    elif name == "curator":         # lente su una statua: l'esperto
        figure(.40, .10, .76, veil=False); d.rectangle([P(.20, .86), P(.60, .96)], fill=STONE)
        d.ellipse([P(.52, .20), P(.84, .52)], outline=(230, 190, 40, 255), width=lw * 2); d.line([P(.80, .48), P(.94, .64)], fill=(230, 190, 40, 255), width=lw * 3)
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _dk[k] = im; return im

_prev_icon_d = fx.icon
def _icon_d(name, size, color=None):
    if isinstance(name, str):
        m = dpic(name, size)
        if m is not None: return m
    return _prev_icon_d(name, size, color)
fx.icon = _icon_d
giu.pic = lambda name, size: fx.icon(name, size)
