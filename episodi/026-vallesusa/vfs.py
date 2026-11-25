# Elementi grafici del caso 026 (Felice Riva e il crac del Cotonificio Vallesusa, 1960-1984): L'IMPERO (scenografia
# ricorrente: la sede al centro e gli stabilimenti intorno, che si spengono col fallimento), rocchetti, telai, cinema.
# Tutto disegnato da codice: nessuna foto reale, nessun documento originale, nessun logo (né del Milan né di aziende).
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "025-giuffre"))
from giu import *
import giu, fi, fx
from fx import *

WPL.update({"Legnano": (8.91, 45.60), "Milano": (9.19, 45.46), "Torino": (7.68, 45.07), "Susa": (7.05, 45.14),
            "Borgone": (7.24, 45.12), "Rivarolo": (7.72, 45.33), "Nizza": (7.27, 43.70), "Parigi": (2.35, 48.86),
            "Atene": (23.73, 37.98), "Beirut": (35.50, 33.89), "Forte dei Marmi": (10.17, 43.96),
            "Lugano": (8.95, 46.00), "Saint Moritz": (9.84, 46.50), "Londra": (-0.13, 51.51)})

giu.NODE_IC = ["factory"] * 12
giu.NODE_LB = ["BORGONE", "S. ANTONINO", "BUSSOLENO", "SUSA", "PIANEZZA", "TORINO", "RIVAROLO", "LANZO",
               "STABILIMENTO", "STABILIMENTO", "STABILIMENTO", "STABILIMENTO"]

def cover_folder26(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 38, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 026", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "IL CRAC VALLESUSA", font=font(SERIF, int(w * .075)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "LEGNANO · 1965 · BEIRUT", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im

_vk = {}
def vpic(name, size):
    k = (name, size)
    if k in _vk: return _vk[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); lw = max(3, S // 60)
    if name == "spool":         # rocchetto di filo di cotone
        d.rectangle([P(.22, .14), P(.78, .22)], fill=(150, 104, 60, 255))
        d.rectangle([P(.22, .78), P(.78, .86)], fill=(150, 104, 60, 255))
        d.rectangle([P(.30, .22), P(.70, .78)], fill=(236, 232, 220, 255))
        for j in range(12): d.line([P(.30, .25 + j * .045), P(.70, .23 + j * .045)], fill=(200, 194, 178, 255), width=lw)
        d.line([P(.70, .60), P(.88, .70), P(.80, .90)], fill=(236, 232, 220, 255), width=lw)
    elif name == "loom":        # telaio meccanico generico
        d.rectangle([P(.10, .30), P(.18, .90)], fill=(90, 90, 96, 255)); d.rectangle([P(.82, .30), P(.90, .90)], fill=(90, 90, 96, 255))
        d.rectangle([P(.10, .26), P(.90, .34)], fill=(110, 110, 118, 255))
        for j in range(14): d.line([P(.22 + j * .04, .34), P(.22 + j * .04, .70)], fill=(236, 232, 220, 255), width=lw // 2 + 1)
        d.rectangle([P(.18, .68), P(.82, .78)], fill=(226, 220, 200, 255))
        d.ellipse([P(.38, .78), P(.62, .98)], outline=(70, 70, 76, 255), width=lw)
    elif name == "cotton":      # fiocco di cotone
        d.line([P(.50, .60), P(.50, .95)], fill=(90, 70, 40, 255), width=lw * 2)
        for cx, cy in ((.36, .40), (.64, .40), (.50, .26), (.40, .56), (.60, .56)):
            d.ellipse([P(cx - .16, cy - .16), P(cx + .16, cy + .16)], fill=(246, 244, 236, 255), outline=(200, 196, 186, 255), width=lw // 2)
        d.polygon([P(.30, .62), P(.50, .70), P(.70, .62), P(.50, .80)], fill=(120, 90, 50, 255))
    elif name == "cinema":      # insegna generica di un cinema
        d.rectangle([P(.10, .20), P(.90, .62)], fill=(60, 40, 40, 255), outline=(220, 180, 70, 255), width=lw)
        for j in range(9): d.ellipse([P(.13 + j * .085, .23), P(.17 + j * .085, .27)], fill=(250, 220, 120, 255))
        for j in range(9): d.ellipse([P(.13 + j * .085, .55), P(.17 + j * .085, .59)], fill=(250, 220, 120, 255))
        d.text(P(.50, .42), "CINEMA", font=font(OSW, int(S * .14), 700), fill=(250, 220, 120, 255), anchor="mm")
        d.rectangle([P(.20, .62), P(.80, .94)], fill=(40, 34, 32, 255)); d.rectangle([P(.42, .70), P(.58, .94)], fill=(110, 80, 50, 255))
    elif name == "umbrella":    # ombrellone da spiaggia
        d.pieslice([P(.10, .12), P(.90, .72)], 180, 360, fill=(220, 80, 60, 255))
        for j in range(4): d.pieslice([P(.10, .12), P(.90, .72)], 180 + j * 45, 180 + j * 45 + 22, fill=(246, 240, 226, 255))
        d.line([P(.50, .40), P(.50, .92)], fill=(90, 70, 50, 255), width=lw * 2)
        d.rectangle([P(.02, .90), P(.98, .98)], fill=(226, 200, 140, 255))
    elif name == "amnesty":     # foglio con il timbro "estinto": amnistia/indulto (generico)
        d.rectangle([P(.20, .08), P(.80, .92)], fill=(240, 232, 214, 255), outline=(140, 130, 110, 255), width=lw)
        for j in range(7): d.line([P(.28, .20 + j * .07), P(.72, .20 + j * .07)], fill=(150, 140, 120, 255), width=lw // 2 + 1)
        d.ellipse([P(.42, .62), P(.78, .90)], outline=(190, 50, 40, 255), width=lw)
        d.text(P(.60, .76), "ESTINTO", font=font(OSW, int(S * .07), 700), fill=(190, 50, 40, 255), anchor="mm")
    elif name == "fuse":        # filatoio: fusi in fila
        d.rectangle([P(.06, .80), P(.94, .88)], fill=(90, 90, 96, 255))
        for j in range(6):
            x = .14 + j * .145
            d.line([P(x, .20), P(x, .80)], fill=(110, 110, 118, 255), width=lw)
            d.ellipse([P(x - .05, .40), P(x + .05, .72)], fill=(240, 236, 226, 255), outline=(190, 184, 170, 255), width=lw // 2)
    elif name == "warplane":    # cielo di guerra generico: nuvola di fumo su palazzi (nessuna violenza)
        for j, h_ in enumerate((.40, .55, .30, .50, .45)):
            d.rectangle([P(.08 + j * .17, 1 - h_ - .06), P(.22 + j * .17, .94)], fill=(110, 104, 98, 255))
        for cx, cy, r in ((.40, .26, .14), (.56, .20, .12), (.66, .30, .12), (.30, .32, .10)):
            d.ellipse([P(cx - r, cy - r), P(cx + r, cy + r)], fill=(150, 146, 140, 255))
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _vk[k] = im; return im

_prev_icon_v = fx.icon
def _icon_v(name, size, color=None):
    if isinstance(name, str):
        m = vpic(name, size)
        if m is not None: return m
    return _prev_icon_v(name, size, color)
fx.icon = _icon_v
giu.pic = lambda name, size: fx.icon(name, size)
