# Elementi grafici del caso 031 (Lelio Luttazzi, Roma 1970): pianoforte, radio d'epoca, classifica della Hit Parade,
# registratore delle intercettazioni, smoking, barca a vela, fontana stilizzata, libro di memorie, televisore con palco.
# Tutto disegnato da codice: nessuna foto, nessun logo, nessuna riproduzione di copertine originali.
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
for p in ("030-saliera", "029-collana", "028-smemorato", "027-dossena", "026-vallesusa", "025-giuffre"):
    sys.path.insert(0, os.path.join(HERE, "..", p))
from sal import *
import sal, smem, fx

WPL.update({"Trieste": (13.77, 45.65), "Milano": (9.19, 45.46), "Roma": (12.50, 41.90), "Bologna": (11.34, 44.49),
            "Torino": (7.69, 45.07), "Sanremo": (7.78, 43.82)})

BLK = (28, 26, 30, 255); IVR = (236, 230, 214, 255); WOOD = (120, 78, 44, 255); WOOD2 = (84, 54, 30, 255)
GD = (222, 180, 62, 255); RD = (196, 48, 40, 255); BL = (60, 90, 150, 255); SEA = (50, 100, 150, 255)
_cl = {}
def spic31(name, size):
    k = (name, size)
    if k in _cl: return _cl[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); lw = max(3, S // 60)
    if name == "piano":                  # pianoforte a coda stilizzato
        d.polygon([P(.10, .40), P(.62, .40), P(.90, .52), P(.88, .66), P(.10, .66)], fill=BLK)
        d.line([P(.14, .40), P(.70, .16)], fill=BLK, width=lw * 2)                 # coperchio aperto
        d.polygon([P(.14, .40), P(.70, .16), P(.80, .44)], fill=(50, 46, 52, 255))
        d.rectangle([P(.10, .58), P(.46, .66)], fill=IVR)
        for j in range(12): d.line([P(.11 + j * .03, .58), P(.11 + j * .03, .66)], fill=(150, 150, 150, 255), width=max(1, lw // 2))
        for j in range(8): d.rectangle([P(.125 + j * .042, .58), P(.14 + j * .042, .62)], fill=BLK)
        for x in (.16, .52, .82): d.rectangle([P(x - .02, .66), P(x + .02, .88)], fill=BLK)
        d.rectangle([P(.40, .88), P(.50, .90)], fill=GD)
    elif name == "radio":                # radio d'epoca
        d.rounded_rectangle([P(.12, .26), P(.88, .82)], radius=S * .08, fill=WOOD, outline=WOOD2, width=lw)
        d.rounded_rectangle([P(.18, .32), P(.56, .76)], radius=S * .04, fill=(200, 176, 130, 255))
        for j in range(7): d.line([P(.21, .37 + j * .055), P(.53, .37 + j * .055)], fill=(150, 120, 80, 255), width=lw)
        d.rectangle([P(.60, .34), P(.84, .48)], fill=(240, 220, 160, 255), outline=WOOD2, width=lw)
        d.line([P(.66, .36), P(.66, .46)], fill=RD, width=lw)
        for x in (.66, .78): d.ellipse([P(x - .05, .58), P(x + .05, .68)], fill=(60, 40, 26, 255))
        for j, r in enumerate((.10, .17, .24)):
            d.arc([P(.80 - r, .14 - r * .6), P(.80 + r, .14 + r * .6)], 200, 340, fill=GD, width=lw)
    elif name == "hitparade":            # classifica settimanale stilizzata: 8 posizioni, senza titoli
        d.rectangle([P(.16, .08), P(.84, .94)], fill=IVR, outline=(120, 110, 90, 255), width=lw)
        d.rectangle([P(.16, .08), P(.84, .22)], fill=RD)
        d.text(P(.50, .15), "HIT PARADE", font=font(OSW, int(S * .085)), fill=(255, 255, 255, 255), anchor="mm")
        for j in range(8):
            y = .29 + j * .08
            d.text(P(.23, y), f"{j + 1}.", font=font(OSW, int(S * .05)), fill=BLK, anchor="mm")
            d.line([P(.30, y), P(.78 - (j % 3) * .06, y)], fill=(GD if j == 0 else (90, 90, 90, 255)), width=lw * (2 if j == 0 else 1))
    elif name == "taperec":              # registratore a bobine (le intercettazioni)
        d.rounded_rectangle([P(.08, .30), P(.92, .82)], radius=S * .04, fill=(70, 72, 80, 255), outline=(40, 40, 46, 255), width=lw)
        for x in (.30, .70):
            d.ellipse([P(x - .15, .36), P(x + .15, .66)], fill=(30, 30, 34, 255), outline=(150, 150, 160, 255), width=lw)
            d.ellipse([P(x - .04, .47), P(x + .04, .55)], fill=(180, 180, 190, 255))
        d.line([P(.30, .66), P(.70, .66)], fill=(120, 90, 50, 255), width=lw)
        for j, x in enumerate((.30, .42, .54, .66)): d.rectangle([P(x, .71), P(x + .08, .77)], fill=(RD if j == 0 else (200, 200, 200, 255)))
    elif name == "phonecall":            # telefono con onde: una telefonata
        d.rounded_rectangle([P(.20, .50), P(.80, .86)], radius=S * .06, fill=BLK)
        d.ellipse([P(.38, .56), P(.62, .80)], fill=IVR); d.ellipse([P(.46, .64), P(.54, .72)], fill=BLK)
        d.rounded_rectangle([P(.14, .34), P(.86, .46)], radius=S * .05, fill=BLK)
        for j, r in enumerate((.10, .17, .24)):
            d.arc([P(.50 - r, .22 - r), P(.50 + r, .22 + r)], 210, 330, fill=GD, width=lw * 2)
    elif name == "tuxedo":               # smoking con papillon (nessun volto)
        d.polygon([P(.14, .92), P(.24, .30), P(.76, .30), P(.86, .92)], fill=BLK)
        d.polygon([P(.38, .30), P(.62, .30), P(.56, .92), P(.44, .92)], fill=(245, 245, 245, 255))
        d.polygon([P(.38, .30), P(.50, .62), P(.30, .56)], fill=(50, 48, 54, 255)); d.polygon([P(.62, .30), P(.50, .62), P(.70, .56)], fill=(50, 48, 54, 255))
        d.polygon([P(.40, .30), P(.50, .36), P(.40, .42)], fill=BLK); d.polygon([P(.60, .30), P(.50, .36), P(.60, .42)], fill=BLK)
        d.ellipse([P(.47, .33), P(.53, .39)], fill=BLK)
        d.ellipse([P(.64, .50), P(.74, .60)], fill=(250, 250, 240, 255))   # fiore all'occhiello
    elif name == "sailboat":             # barca a vela
        d.polygon([P(.12, .70), P(.88, .70), P(.76, .82), P(.24, .82)], fill=(240, 236, 226, 255), outline=(120, 110, 90, 255))
        d.line([P(.50, .70), P(.50, .12)], fill=WOOD2, width=lw * 2)
        d.polygon([P(.52, .14), P(.52, .66), P(.84, .66)], fill=IVR); d.polygon([P(.48, .20), P(.48, .66), P(.22, .66)], fill=(220, 214, 200, 255))
        for j in range(3): d.arc([P(.05 + j * .30, .82), P(.35 + j * .30, .92)], 0, 180, fill=SEA, width=lw * 2)
    elif name == "sea":                  # mare e onde
        for j in range(4):
            y = .30 + j * .15
            for q in range(3): d.arc([P(.06 + q * .30, y), P(.36 + q * .30, y + .12)], 180, 360, fill=SEA, width=lw * 2)
        d.ellipse([P(.70, .08), P(.86, .24)], fill=GD)
    elif name == "fountain":             # fontana monumentale stilizzata (generica)
        d.rectangle([P(.10, .20), P(.90, .62)], fill=(214, 204, 184, 255), outline=(150, 140, 120, 255), width=lw)
        for x in (.22, .40, .60, .78): d.rectangle([P(x - .03, .24), P(x + .03, .58)], fill=(186, 176, 156, 255))
        d.rounded_rectangle([P(.40, .30), P(.60, .58)], radius=S * .08, fill=(170, 160, 140, 255))
        d.ellipse([P(.06, .62), P(.94, .88)], fill=(110, 170, 210, 255), outline=(150, 140, 120, 255), width=lw)
        for x in (.30, .50, .70): d.arc([P(x - .10, .50), P(x + .10, .74)], 200, 340, fill=(220, 240, 255, 255), width=lw)
    elif name == "memoir":               # libro di memorie (ricostruzione generica, nessuna copertina originale)
        d.polygon([P(.24, .12), P(.80, .12), P(.80, .90), P(.24, .90)], fill=(40, 70, 110, 255))
        d.rectangle([P(.20, .12), P(.26, .90)], fill=(26, 46, 74, 255))
        d.text(P(.53, .36), "OPERAZIONE", font=font(OSW, int(S * .072)), fill=IVR, anchor="mm")
        d.text(P(.53, .48), "MONTECRISTO", font=font(OSW, int(S * .072)), fill=GD, anchor="mm")
        for j in range(3): d.line([P(.40, .66 + j * .05), P(.66, .66 + j * .05)], fill=(150, 170, 200, 255), width=lw)
    elif name == "tvstage":              # televisore d'epoca con palco e sipario (generico)
        d.rounded_rectangle([P(.10, .16), P(.90, .80)], radius=S * .06, fill=(60, 50, 44, 255))
        d.rounded_rectangle([P(.16, .22), P(.72, .74)], radius=S * .05, fill=(200, 205, 210, 255))
        d.polygon([P(.16, .22), P(.30, .22), P(.24, .74), P(.16, .74)], fill=RD); d.polygon([P(.72, .22), P(.58, .22), P(.64, .74), P(.72, .74)], fill=RD)
        d.rectangle([P(.16, .64), P(.72, .74)], fill=(150, 130, 100, 255))
        for x in (.38, .50): d.ellipse([P(x - .03, .40), P(x + .03, .46)], fill=BLK); d.rectangle([P(.355, .46), P(.405, .64)], fill=BLK) if x == .38 else d.rectangle([P(.475, .46), P(.525, .64)], fill=(180, 60, 60, 255))
        for y in (.32, .46, .60): d.ellipse([P(.78, y), P(.84, y + .06)], fill=(170, 160, 150, 255))
        d.line([P(.24, .80), P(.18, .92)], fill=(60, 50, 44, 255), width=lw * 2); d.line([P(.76, .80), P(.82, .92)], fill=(60, 50, 44, 255), width=lw * 2)
    elif name == "filmreel":             # bobina di pellicola
        d.ellipse([P(.14, .14), P(.86, .86)], fill=(60, 62, 70, 255), outline=(30, 30, 34, 255), width=lw)
        for a in range(6):
            x = .5 + .22 * math.cos(a * math.pi / 3); y = .5 + .22 * math.sin(a * math.pi / 3)
            d.ellipse([P(x - .08, y - .08), P(x + .08, y + .08)], fill=(28, 28, 32, 255))
        d.ellipse([P(.45, .45), P(.55, .55)], fill=(200, 200, 210, 255))
        d.polygon([P(.80, .62), P(.98, .70), P(.98, .78), P(.78, .70)], fill=(40, 40, 44, 255))
    elif name == "isolation":            # cella d'isolamento: porta blindata con spioncino
        d.rectangle([P(.10, .08), P(.90, .94)], fill=(90, 88, 84, 255))
        d.rectangle([P(.28, .14), P(.72, .92)], fill=(70, 74, 80, 255), outline=(40, 40, 44, 255), width=lw * 2)
        d.rectangle([P(.42, .30), P(.58, .38)], fill=(20, 20, 24, 255))
        for y in (.50, .70): d.line([P(.28, y), P(.72, y)], fill=(50, 52, 58, 255), width=lw)
        d.ellipse([P(.62, .54), P(.68, .60)], fill=(170, 170, 170, 255))
    elif name == "tally27":              # 27 tacche sul muro
        d.rectangle([P(.04, .10), P(.96, .90)], fill=(170, 160, 140, 255))
        for g in range(6):
            x0 = .10 + g * .145; n = 5 if g < 5 else 2
            for j in range(min(n, 4)): d.line([P(x0 + j * .025, .30), P(x0 + j * .025, .70)], fill=(60, 50, 40, 255), width=lw)
            if n == 5: d.line([P(x0 - .01, .62), P(x0 + .09, .38)], fill=(60, 50, 40, 255), width=lw)
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _cl[k] = im; return im

_prev_icon_31 = fx.icon
def _icon_31(name, size, color=None):
    if isinstance(name, str):
        m = spic31(name, size)
        if m is not None: return m
    return _prev_icon_31(name, size, color)
fx.icon = _icon_31
smem.giu.pic = lambda name, size: fx.icon(name, size)

def cover_folder31(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 41, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 031", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "UNA TELEFONATA", font=font(SERIF, int(w * .08)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "ROMA · 1970", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im
