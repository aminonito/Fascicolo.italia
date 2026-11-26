# Elementi grafici del caso 028 (lo smemorato di Collegno, caso Bruneri-Canella, 1926-1941): IL VOLTO SENZA NOME
# (scenografia ricorrente: una sagoma con la barba e il punto di domanda, che due famiglie reclamano), impronte
# digitali, cartolina, manicomio, tribunale. Tutto disegnato da codice: nessuna foto reale, nessuna pagina di giornale
# originale (solo ricostruzioni generiche), nessun logo di testate o programmi tv.
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "027-dossena"))
from dos import *
import dos, vfs, giu, fi, fx
from fx import *

WPL.update({"Torino": (7.68, 45.07), "Collegno": (7.57, 45.08), "Verona": (10.99, 45.44), "Padova": (11.88, 45.41),
            "Desenzano": (10.54, 45.47), "Pallanza": (8.55, 45.92), "Firenze": (11.25, 43.77), "Roma": (12.50, 41.90),
            "Monastir": (21.33, 41.03), "Salonicco": (22.94, 40.64), "Rio de Janeiro": (-43.20, -22.90), "Milano": (9.19, 45.46),
            "Taranto": (17.24, 40.47)})

def cover_folder28(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 38, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 028", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "LO SMEMORATO", font=font(SERIF, int(w * .08)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "TORINO · COLLEGNO · VERONA", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im

SK = (214, 186, 160, 255); SK2 = (176, 148, 122, 255); HAIR = (92, 84, 78, 255); BEARD = (120, 112, 104, 255)
DARK = (40, 34, 30, 255); PAPER = (238, 230, 210, 255); GOLDC = (230, 190, 40, 255); REDC = (200, 50, 40, 255)
BRONZE = (170, 120, 60, 255)
_sk = {}
def spic(name, size):
    k = (name, size)
    if k in _sk: return _sk[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); lw = max(3, S // 60)
    def head(cx, cy, r, beard=True, col=SK, q=False):
        # sagoma generica di un uomo con la barba (nessun ritratto reale)
        d.polygon([P(cx - r * 1.9, cy + r * 3.2), P(cx - r * 1.5, cy + r * 1.6), P(cx + r * 1.5, cy + r * 1.6), P(cx + r * 1.9, cy + r * 3.2)], fill=DARK)
        d.ellipse([P(cx - r, cy - r * 1.15), P(cx + r, cy + r * 1.15)], fill=col)
        d.chord([P(cx - r * 1.02, cy - r * 1.2), P(cx + r * 1.02, cy + r * .2)], 180, 360, fill=HAIR)
        if beard:
            d.polygon([P(cx - r * .95, cy + r * .05), P(cx + r * .95, cy + r * .05), P(cx + r * .55, cy + r * 1.2), P(cx, cy + r * 1.75), P(cx - r * .55, cy + r * 1.2)], fill=BEARD)
            d.rectangle([P(cx - r * .35, cy + r * .42), P(cx + r * .35, cy + r * .52)], fill=SK2)
        d.ellipse([P(cx - r * .45, cy - r * .3), P(cx - r * .25, cy - r * .12)], fill=DARK)
        d.ellipse([P(cx + r * .25, cy - r * .3), P(cx + r * .45, cy - r * .12)], fill=DARK)
        if q:
            d.text(P(cx + r * 1.7, cy - r * 1.0), "?", font=font(OSW, int(S * r * 1.6), 700), fill=GOLDC, anchor="mm")
    if name == "beard":              # il volto senza nome (sagoma)
        head(.47, .38, .17, q=True)
    elif name == "beard_n":          # sagoma con cartellino di matricola
        head(.50, .34, .16)
        d.rectangle([P(.22, .78), P(.78, .94)], fill=PAPER, outline=DARK, width=lw)
        d.text(P(.50, .86), "N. 44170", font=font(OSW, int(S * .09), 700), fill=DARK, anchor="mm")
    elif name == "two_claim":        # due donne (sagome) e un uomo al centro
        head(.50, .30, .11, q=False)
        for x, c in ((.16, (120, 60, 70, 255)), (.84, (60, 80, 120, 255))):
            d.ellipse([P(x - .07, .44), P(x + .07, .60)], fill=SK)
            d.chord([P(x - .08, .42), P(x + .08, .58)], 180, 360, fill=HAIR)
            d.polygon([P(x - .10, .62), P(x + .10, .62), P(x + .14, .96), P(x - .14, .96)], fill=c)
        d.line([P(.26, .56), P(.36, .44)], fill=GOLDC, width=lw * 2); d.line([P(.74, .56), P(.64, .44)], fill=GOLDC, width=lw * 2)
    elif name == "finger":           # impronta digitale stilizzata (spirale)
        cx, cy = .50, .52
        d.ellipse([P(.14, .06), P(.86, .98)], fill=PAPER)
        for j in range(8):
            r = .04 + j * .042
            d.arc([P(cx - r * .8, cy - r), P(cx + r * .8, cy + r * 1.05)], 30 + j * 25, 330 + j * 25, fill=(60, 60, 70, 255), width=lw)
    elif name == "finger2":          # due impronte a confronto con il segno di uguale
        for cx in (.25, .75):
            d.rectangle([P(cx - .2, .16), P(cx + .2, .74)], fill=PAPER)
            for j in range(6):
                r = .025 + j * .03
                d.arc([P(cx - r * .8, .45 - r), P(cx + r * .8, .45 + r * 1.05)], 30 + j * 25, 330 + j * 25, fill=(60, 60, 70, 255), width=lw)
            d.rectangle([P(cx - .2, .16), P(cx + .2, .74)], outline=DARK, width=lw)
        d.text(P(.50, .45), "=", font=font(OSW, int(S * .16), 700), fill=GOLDC, anchor="mm")
        d.text(P(.25, .84), "1926", font=font(OSW, int(S * .08), 700), fill=(200, 200, 200, 255), anchor="mm")
        d.text(P(.75, .84), "SCHEDARIO", font=font(OSW, int(S * .07), 700), fill=(200, 200, 200, 255), anchor="mm")
    elif name == "vase":             # vaso funerario di metallo (generico)
        d.polygon([P(.36, .20), P(.64, .20), P(.60, .28), P(.40, .28)], fill=BRONZE)
        d.ellipse([P(.26, .26), P(.74, .78)], fill=BRONZE)
        d.rectangle([P(.40, .76), P(.60, .86)], fill=(140, 96, 50, 255)); d.rectangle([P(.32, .86), P(.68, .92)], fill=(120, 84, 44, 255))
        d.arc([P(.32, .34), P(.68, .70)], 200, 300, fill=(210, 160, 90, 255), width=lw * 2)
    elif name == "cemetery":         # cancello e lapidi (generico)
        for x in (.18, .40, .62):
            d.rounded_rectangle([P(x, .46), P(x + .16, .80)], radius=S * .06, fill=(170, 166, 160, 255))
            d.line([P(x + .04, .56), P(x + .12, .56)], fill=(120, 116, 110, 255), width=lw)
        d.rectangle([P(.06, .80), P(.94, .88)], fill=(90, 110, 70, 255))
        for x in range(10): d.line([P(.08 + x * .09, .30), P(.08 + x * .09, .80)], fill=(50, 50, 56, 255), width=lw)
        d.line([P(.06, .34), P(.94, .34)], fill=(50, 50, 56, 255), width=lw)
    elif name == "asylum":           # grande edificio con cortile e muro di cinta (generico)
        d.rectangle([P(.08, .40), P(.92, .82)], fill=(196, 176, 150, 255))
        d.polygon([P(.04, .42), P(.50, .22), P(.96, .42)], fill=(150, 90, 70, 255))
        for r_ in (.50, .64):
            for x in range(7): d.rectangle([P(.13 + x * .11, r_), P(.19 + x * .11, r_ + .08)], fill=(70, 70, 80, 255))
        d.rectangle([P(.44, .66), P(.56, .82)], fill=DARK)
        d.rectangle([P(.02, .82), P(.98, .92)], fill=(160, 150, 136, 255))
    elif name == "postcard":         # cartolina generica con francobollo
        d.rectangle([P(.06, .22), P(.94, .80)], fill=PAPER, outline=(150, 130, 100, 255), width=lw)
        d.line([P(.52, .28), P(.52, .74)], fill=(150, 130, 100, 255), width=lw)
        for y in (.36, .46, .56, .66): d.line([P(.12, y), P(.46, y + .01)], fill=(70, 70, 120, 255), width=lw)
        d.rectangle([P(.74, .28), P(.88, .44)], fill=(180, 80, 70, 255), outline=(120, 50, 40, 255), width=lw)
        for y in (.54, .62, .70): d.line([P(.58, y), P(.88, y)], fill=(150, 130, 100, 255), width=lw)
    elif name == "anon":             # lettera anonima: busta e foglio con "?"
        d.rectangle([P(.16, .14), P(.84, .86)], fill=PAPER, outline=(150, 130, 100, 255), width=lw)
        for y in (.30, .40, .50, .60): d.line([P(.24, y), P(.76, y)], fill=(90, 90, 100, 255), width=lw)
        d.text(P(.70, .74), "?", font=font(OSW, int(S * .2), 700), fill=REDC, anchor="mm")
        d.text(P(.36, .74), "ANONIMA", font=font(OSW, int(S * .06), 700), fill=REDC, anchor="mm")
    elif name == "press":            # tipografia: torchio e caratteri
        d.rectangle([P(.16, .20), P(.84, .30)], fill=(70, 70, 80, 255)); d.rectangle([P(.24, .30), P(.32, .80)], fill=(70, 70, 80, 255))
        d.rectangle([P(.68, .30), P(.76, .80)], fill=(70, 70, 80, 255)); d.rectangle([P(.30, .56), P(.70, .64)], fill=(120, 120, 130, 255))
        d.rectangle([P(.10, .80), P(.90, .88)], fill=(90, 70, 50, 255))
        d.rectangle([P(.36, .66), P(.64, .78)], fill=PAPER)
        d.text(P(.50, .72), "A B C", font=font(TYPE, int(S * .06)), fill=DARK, anchor="mm")
    elif name == "helmet":           # elmetto della Grande guerra (generico)
        d.chord([P(.18, .28), P(.82, .84)], 180, 360, fill=(96, 104, 80, 255))
        d.rectangle([P(.12, .54), P(.88, .60)], fill=(80, 88, 66, 255))
        d.line([P(.50, .30), P(.50, .54)], fill=(120, 128, 100, 255), width=lw)
    elif name == "rings":            # due fedi
        d.ellipse([P(.14, .30), P(.56, .72)], outline=GOLDC, width=lw * 3)
        d.ellipse([P(.44, .30), P(.86, .72)], outline=(210, 170, 40, 255), width=lw * 3)
    elif name == "dnay":             # doppia elica stilizzata
        for j in range(24):
            y = .10 + j * .034; a_ = .5 + .22 * math.sin(j * .55); b_ = .5 - .22 * math.sin(j * .55)
            d.line([P(a_, y), P(b_, y)], fill=(150, 150, 170, 255), width=lw // 2 + 1)
            d.ellipse([P(a_ - .02, y - .02), P(a_ + .02, y + .02)], fill=(80, 140, 200, 255))
            d.ellipse([P(b_ - .02, y - .02), P(b_ + .02, y + .02)], fill=REDC)
    elif name == "rio":              # baia con montagna a pan di zucchero e palma (generico)
        d.rectangle([P(.04, .70), P(.96, .90)], fill=(60, 110, 160, 255))
        d.polygon([P(.50, .70), P(.62, .30), P(.70, .28), P(.80, .70)], fill=(80, 110, 80, 255))
        d.polygon([P(.30, .70), P(.40, .52), P(.50, .70)], fill=(90, 120, 90, 255))
        d.line([P(.20, .70), P(.24, .34)], fill=(120, 90, 60, 255), width=lw * 2)
        for a_ in (-60, -20, 20, 60, 100, 140):
            r = .14; d.line([P(.24, .34), P(.24 + r * math.cos(math.radians(a_ + 180)), .34 + r * .6 * math.sin(math.radians(a_ + 180)))], fill=(60, 130, 70, 255), width=lw * 2)
        d.ellipse([P(.78, .10), P(.90, .22)], fill=GOLDC)
    elif name == "mask":             # maschere del teatro
        d.ellipse([P(.10, .20), P(.56, .74)], fill=PAPER, outline=DARK, width=lw)
        d.ellipse([P(.20, .36), P(.28, .44)], fill=DARK); d.ellipse([P(.38, .36), P(.46, .44)], fill=DARK); d.arc([P(.22, .46), P(.44, .62)], 20, 160, fill=DARK, width=lw)
        d.ellipse([P(.44, .30), P(.90, .84)], fill=(220, 190, 120, 255), outline=DARK, width=lw)
        d.ellipse([P(.54, .46), P(.62, .54)], fill=DARK); d.ellipse([P(.72, .46), P(.80, .54)], fill=DARK); d.arc([P(.56, .64), P(.78, .78)], 200, 340, fill=DARK, width=lw)
    elif name == "film":             # pellicola
        d.rectangle([P(.08, .30), P(.92, .70)], fill=(40, 40, 44, 255))
        for x in range(9):
            d.rectangle([P(.11 + x * .09, .33), P(.16 + x * .09, .38)], fill=PAPER); d.rectangle([P(.11 + x * .09, .62), P(.16 + x * .09, .67)], fill=PAPER)
        for x in range(3): d.rectangle([P(.14 + x * .26, .41), P(.34 + x * .26, .59)], fill=(150, 160, 170, 255))
    elif name == "witness":          # testimoni: tre sagome con fumetto
        for x in (.22, .50, .78):
            d.ellipse([P(x - .07, .40), P(x + .07, .56)], fill=SK); d.polygon([P(x - .11, .58), P(x + .11, .58), P(x + .14, .92), P(x - .14, .92)], fill=(70, 74, 90, 255))
        d.rounded_rectangle([P(.30, .08), P(.70, .30)], radius=S * .04, fill=PAPER); d.polygon([P(.46, .30), P(.52, .30), P(.50, .38)], fill=PAPER)
        d.text(P(.50, .19), "È LUI!", font=font(OSW, int(S * .08), 700), fill=DARK, anchor="mm")
    elif name == "chair_doc":        # perizia: medico con cartella
        d.rectangle([P(.24, .14), P(.76, .86)], fill=PAPER, outline=(150, 130, 100, 255), width=lw)
        d.text(P(.50, .24), "PERIZIA", font=font(OSW, int(S * .08), 700), fill=DARK, anchor="mm")
        for y in (.38, .48, .58, .68): d.line([P(.32, y), P(.68, y)], fill=(90, 90, 100, 255), width=lw)
        d.ellipse([P(.58, .70), P(.74, .84)], outline=REDC, width=lw)
    elif name == "steam":            # piroscafo verso il Brasile
        d.polygon([P(.08, .62), P(.92, .62), P(.80, .80), P(.18, .80)], fill=(40, 40, 50, 255))
        d.rectangle([P(.26, .46), P(.70, .62)], fill=PAPER)
        d.rectangle([P(.40, .26), P(.50, .46)], fill=REDC); d.rectangle([P(.56, .30), P(.64, .46)], fill=REDC)
        d.rectangle([P(.04, .80), P(.96, .90)], fill=(60, 110, 160, 255))
    elif name in ("woman", "woman2"):  # sagoma generica di donna anni Venti (nessun ritratto reale)
        col = (120, 60, 70, 255) if name == "woman" else (60, 80, 120, 255)
        d.ellipse([P(.38, .14), P(.62, .42)], fill=SK)
        d.chord([P(.36, .10), P(.64, .38)], 180, 360, fill=HAIR); d.rectangle([P(.36, .24), P(.42, .40)], fill=HAIR); d.rectangle([P(.58, .24), P(.64, .40)], fill=HAIR)
        d.ellipse([P(.43, .26), P(.47, .30)], fill=DARK); d.ellipse([P(.53, .26), P(.57, .30)], fill=DARK)
        d.polygon([P(.40, .46), P(.60, .46), P(.72, .94), P(.28, .94)], fill=col)
        d.rectangle([P(.46, .42), P(.54, .47)], fill=SK)
    elif name == "grave":            # croce e nome
        d.rectangle([P(.44, .10), P(.56, .80)], fill=(170, 166, 160, 255)); d.rectangle([P(.28, .26), P(.72, .36)], fill=(170, 166, 160, 255))
        d.rectangle([P(.16, .80), P(.84, .90)], fill=(90, 110, 70, 255))
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _sk[k] = im; return im

_prev_icon_s = fx.icon
def _icon_s(name, size, color=None):
    if isinstance(name, str):
        m = spic(name, size)
        if m is not None: return m
    return _prev_icon_s(name, size, color)
fx.icon = _icon_s
giu.pic = lambda name, size: fx.icon(name, size)
