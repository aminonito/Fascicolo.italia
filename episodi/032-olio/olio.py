# Elementi grafici del caso 032 (lo scandalo dell'olio di soia, Bayonne 1963 - Tino De Angelis): serbatoio, serbatoio in
# sezione (acqua sotto, olio sopra), parco serbatoi, nastro di misura, tubi, goccia d'olio, pianta di soia, ricevuta di
# deposito generica, grano, maiale, vassoio della mensa, nave cisterna, banca, borsa con colonne, nastro delle quotazioni,
# frecce del prezzo, assegno da viaggio generico, cassaforte svizzera, porta del penitenziario.
# Tutto disegnato da codice: nessuna foto, nessun logo, nessun documento originale.
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "031-luttazzi"))
from ltz import *
import ltz, fx

WPL.update({"Bayonne": (-74.11, 40.67), "New York": (-74.00, 40.71), "Dallas": (-96.80, 32.78), "Washington": (-77.04, 38.90),
            "Chicago": (-87.63, 41.88), "Omaha": (-95.93, 41.26), "Lewisburg": (-76.88, 40.96), "Newark": (-74.17, 40.74),
            "North Bergen": (-74.02, 40.80), "Indianapolis": (-86.16, 39.77), "Ginevra": (6.14, 46.20), "Madrid": (-3.70, 40.42),
            "Belgrado": (20.46, 44.79), "Italia": (13.0, 42.5), "Roma": (12.50, 41.90), "Londra": (-0.13, 51.51)})

STL = (150, 156, 164, 255); STD = (96, 102, 110, 255); OIL = (222, 176, 52, 255); OILD = (170, 126, 30, 255)
WAT = (70, 130, 190, 255); WATD = (44, 96, 150, 255); INKC = (28, 26, 30, 255); PAP = (238, 230, 210, 255)
GRN = (80, 140, 70, 255); RD2 = (196, 48, 40, 255); GD2 = (222, 180, 62, 255)
_c32 = {}
def spic32(name, size):
    k = (name, size)
    if k in _c32: return _c32[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); lw = max(3, S // 60)
    def tank(x0, x1, y0, y1, fill=STL):
        d.rectangle([P(x0, y0 + .04), P(x1, y1)], fill=fill, outline=STD, width=lw)
        d.ellipse([P(x0, y0), P(x1, y0 + .08)], fill=(176, 182, 190, 255), outline=STD, width=lw)
        for j in range(1, 4):
            y = y0 + .04 + (y1 - y0 - .04) * j / 4; d.line([P(x0, y), P(x1, y)], fill=STD, width=max(1, lw // 2))
    if name == "tank":                     # serbatoio cilindrico con scala
        tank(.20, .80, .10, .90)
        for j in range(9): d.line([P(.74, .16 + j * .08), P(.84, .12 + j * .08)], fill=INKC, width=lw)
        d.line([P(.84, .12), P(.84, .88)], fill=INKC, width=lw)
        d.rectangle([P(.44, .08), P(.56, .12)], fill=INKC)            # botola di misura
    elif name == "tank_x":                 # serbatoio in sezione: tanta acqua, un velo d'olio
        d.rectangle([P(.22, .12), P(.78, .90)], fill=(230, 232, 236, 255))
        d.rectangle([P(.22, .30), P(.78, .90)], fill=WAT)
        for j in range(4): d.arc([P(.26 + j * .13, .50), P(.38 + j * .13, .58)], 200, 340, fill=WATD, width=lw)
        d.rectangle([P(.22, .22), P(.78, .30)], fill=OIL)
        d.rectangle([P(.22, .12), P(.78, .90)], outline=STD, width=lw * 2)
        d.text(P(.50, .26), "OLIO", font=font(OSW, int(S * .05)), fill=INKC, anchor="mm")
        d.text(P(.50, .66), "ACQUA", font=font(OSW, int(S * .09)), fill=(235, 245, 255, 255), anchor="mm")
    elif name == "tank_full":              # serbatoio in sezione pieno d'olio (come dicono le carte)
        d.rectangle([P(.22, .12), P(.78, .90)], fill=(230, 232, 236, 255))
        d.rectangle([P(.22, .20), P(.78, .90)], fill=OIL)
        d.rectangle([P(.22, .12), P(.78, .90)], outline=STD, width=lw * 2)
        d.text(P(.50, .56), "OLIO", font=font(OSW, int(S * .09)), fill=INKC, anchor="mm")
    elif name == "tankfarm":               # parco serbatoi
        for (x, y, w, h) in ((.04, .40, .26, .50), (.36, .28, .30, .62), (.70, .44, .26, .46), (.20, .60, .22, .30), (.56, .62, .22, .28)):
            tank(x, x + w, y, y + h)
        d.line([P(.02, .92), P(.98, .92)], fill=INKC, width=lw)
    elif name == "pipes":                  # tubi che collegano i serbatoi
        for x in (.08, .40, .72):
            tank(x, x + .22, .14, .66)
        for x in (.19, .51):
            d.line([P(x, .66), P(x, .80), P(x + .32, .80), P(x + .32, .66)], fill=RD2, width=lw * 3)
        d.polygon([P(.44, .76), P(.50, .80), P(.44, .84)], fill=RD2); d.polygon([P(.76, .76), P(.82, .80), P(.76, .84)], fill=RD2)
        d.ellipse([P(.30, .76), P(.38, .84)], fill=GD2, outline=INKC, width=lw)
    elif name == "dipstick":               # nastro di misura con peso, calato dalla botola
        d.rectangle([P(.30, .10), P(.70, .18)], fill=STD)
        d.line([P(.50, .18), P(.50, .78)], fill=(200, 190, 120, 255), width=lw * 3)
        for j in range(10): d.line([P(.47, .22 + j * .055), P(.53, .22 + j * .055)], fill=INKC, width=max(1, lw // 2))
        d.polygon([P(.44, .78), P(.56, .78), P(.53, .90), P(.47, .90)], fill=INKC)
        d.arc([P(.30, .04), P(.70, .30)], 200, 340, fill=OIL, width=lw)
    elif name == "oildrop":                # goccia d'olio
        d.polygon([P(.50, .08), P(.76, .56), P(.24, .56)], fill=OIL)
        d.ellipse([P(.24, .38), P(.76, .90)], fill=OIL)
        d.ellipse([P(.36, .54), P(.46, .66)], fill=(255, 236, 170, 255))
    elif name == "soy":                    # pianta di soia: baccelli e foglie
        d.line([P(.50, .92), P(.50, .14)], fill=GRN, width=lw * 2)
        for j, (y, s) in enumerate(((.24, 1), (.42, -1), (.60, 1))):
            d.ellipse([P(.50 + s * .02, y - .06), P(.50 + s * .32, y + .06)] if s > 0 else [P(.18, y - .06), P(.48, y + .06)], fill=(110, 170, 90, 255))
        for (x, y) in ((.34, .34), (.64, .52), (.36, .72)):
            d.rounded_rectangle([P(x - .05, y - .09), P(x + .05, y + .09)], radius=S * .04, fill=(196, 176, 100, 255), outline=(140, 120, 60, 255), width=lw)
            for q in (-.04, 0, .04): d.ellipse([P(x - .025, y + q - .02), P(x + .025, y + q + .02)], fill=(230, 210, 130, 255))
    elif name == "wreceipt":               # ricevuta di deposito generica (ricostruzione)
        d.rectangle([P(.12, .14), P(.88, .86)], fill=PAP, outline=(120, 100, 70, 255), width=lw)
        d.rectangle([P(.12, .14), P(.88, .26)], fill=(60, 90, 70, 255))
        d.text(P(.50, .20), "RICEVUTA DI DEPOSITO", font=font(OSW, int(S * .05)), fill=PAP, anchor="mm")
        for j in range(5): d.line([P(.20, .36 + j * .07), P(.80 - (j % 2) * .16, .36 + j * .07)], fill=(120, 110, 90, 255), width=lw)
        d.text(P(.30, .76), "OLIO", font=font(OSW, int(S * .06)), fill=OILD, anchor="mm")
        d.ellipse([P(.62, .66), P(.80, .84)], outline=RD2, width=lw)
        d.text(P(.50, .92), "ricostruzione generica", font=font(COURR, int(S * .035)), fill=(200, 200, 200, 255), anchor="mm")
    elif name == "wheat":                  # spiga di grano
        d.line([P(.50, .92), P(.50, .20)], fill=(180, 140, 60, 255), width=lw * 2)
        for j in range(6):
            y = .22 + j * .09
            d.ellipse([P(.38, y), P(.50, y + .10)], fill=GD2); d.ellipse([P(.50, y), P(.62, y + .10)], fill=GD2)
    elif name == "pig":                    # maiale stilizzato
        d.ellipse([P(.16, .30), P(.80, .74)], fill=(236, 170, 170, 255), outline=(170, 100, 100, 255), width=lw)
        d.ellipse([P(.70, .40), P(.92, .62)], fill=(236, 170, 170, 255), outline=(170, 100, 100, 255), width=lw)
        d.ellipse([P(.84, .46), P(.94, .56)], fill=(210, 130, 130, 255))
        d.polygon([P(.66, .32), P(.72, .20), P(.78, .36)], fill=(220, 150, 150, 255))
        for x in (.26, .40, .56, .68): d.rectangle([P(x, .70), P(x + .05, .86)], fill=(220, 150, 150, 255))
        d.ellipse([P(.74, .44), P(.78, .48)], fill=INKC)
    elif name == "tray":                   # vassoio della mensa scolastica (generico)
        d.rounded_rectangle([P(.08, .30), P(.92, .80)], radius=S * .05, fill=(190, 196, 204, 255), outline=STD, width=lw)
        d.rounded_rectangle([P(.14, .36), P(.50, .74)], radius=S * .04, fill=(220, 224, 230, 255))
        d.ellipse([P(.20, .44), P(.44, .66)], fill=(200, 120, 90, 255))
        d.rounded_rectangle([P(.56, .36), P(.86, .52)], radius=S * .03, fill=(220, 224, 230, 255))
        d.rounded_rectangle([P(.56, .58), P(.86, .74)], radius=S * .03, fill=(220, 224, 230, 255))
        d.ellipse([P(.62, .40), P(.80, .50)], fill=(120, 170, 80, 255)); d.rectangle([P(.64, .60), P(.78, .72)], fill=(240, 240, 240, 255))
    elif name == "tanker":                 # nave da carico anni '60 (generica)
        d.polygon([P(.04, .60), P(.96, .60), P(.86, .80), P(.12, .80)], fill=(60, 70, 90, 255))
        d.rectangle([P(.04, .58), P(.96, .62)], fill=RD2)
        d.rectangle([P(.70, .38), P(.86, .58)], fill=(230, 230, 230, 255)); d.rectangle([P(.74, .26), P(.80, .38)], fill=(200, 60, 50, 255))
        for x in (.16, .30, .44, .58): d.ellipse([P(x, .52), P(x + .10, .60)], fill=STL)
        for j in range(3): d.arc([P(.05 + j * .30, .82), P(.35 + j * .30, .92)], 0, 180, fill=WAT, width=lw * 2)
    elif name == "bank":                   # banca generica con colonne
        d.polygon([P(.10, .32), P(.50, .10), P(.90, .32)], fill=(210, 200, 180, 255), outline=STD)
        d.rectangle([P(.12, .32), P(.88, .38)], fill=(190, 180, 160, 255))
        for x in (.18, .34, .50, .66, .82): d.rectangle([P(x - .04, .38), P(x + .04, .80)], fill=(226, 218, 200, 255), outline=STD, width=max(1, lw // 2))
        d.rectangle([P(.08, .80), P(.92, .88)], fill=(190, 180, 160, 255))
        d.text(P(.50, .23), "$", font=font(OSW, int(S * .10)), fill=OILD, anchor="mm")
    elif name == "exchange":               # borsa: facciata a sei colonne, generica
        d.polygon([P(.06, .30), P(.50, .12), P(.94, .30)], fill=(220, 214, 200, 255), outline=STD)
        for j in range(6):
            x = .14 + j * .145; d.rectangle([P(x - .04, .32), P(x + .04, .82)], fill=(236, 230, 216, 255), outline=STD, width=max(1, lw // 2))
        d.rectangle([P(.04, .82), P(.96, .90)], fill=(200, 194, 180, 255))
        d.line([P(.48, .26), P(.48, .06)], fill=INKC, width=lw); d.polygon([P(.48, .06), P(.62, .09), P(.48, .12)], fill=(90, 110, 160, 255))
    elif name == "ticker":                 # nastro delle quotazioni
        d.rounded_rectangle([P(.30, .10), P(.70, .40)], radius=S * .04, fill=(60, 62, 70, 255))
        d.ellipse([P(.40, .16), P(.60, .34)], fill=(200, 200, 210, 255))
        pts = [P(.50, .40), P(.36, .56), P(.62, .70), P(.40, .86), P(.58, .96)]
        d.line(pts, fill=PAP, width=lw * 5, joint="curve")
        d.text(P(.46, .62), "▲ ▼", font=font(OSW, int(S * .05)), fill=INKC, anchor="mm")
    elif name == "price_up":               # freccia del prezzo che sale (nessun valore)
        d.line([P(.10, .80), P(.36, .60), P(.54, .66), P(.86, .22)], fill=GRN, width=lw * 4)
        d.polygon([P(.78, .18), P(.92, .14), P(.90, .30)], fill=GRN)
        d.line([P(.08, .88), P(.92, .88)], fill=INKC, width=lw); d.line([P(.08, .88), P(.08, .10)], fill=INKC, width=lw)
    elif name == "price_down":             # freccia del prezzo che crolla (nessun valore)
        d.line([P(.10, .22), P(.40, .30), P(.56, .26), P(.88, .80)], fill=RD2, width=lw * 4)
        d.polygon([P(.80, .82), P(.94, .86), P(.92, .70)], fill=RD2)
        d.line([P(.08, .88), P(.92, .88)], fill=INKC, width=lw); d.line([P(.08, .88), P(.08, .10)], fill=INKC, width=lw)
    elif name == "cheque":                 # assegno da viaggio generico (nessun marchio)
        d.rounded_rectangle([P(.08, .26), P(.92, .74)], radius=S * .03, fill=(200, 226, 210, 255), outline=(80, 120, 90, 255), width=lw)
        d.text(P(.20, .38), "TRAVELERS CHEQUE", font=font(OSW, int(S * .045)), fill=(40, 80, 60, 255), anchor="lm")
        d.text(P(.80, .56), "$", font=font(OSW, int(S * .16)), fill=(40, 80, 60, 255), anchor="mm")
        for j in range(2): d.line([P(.20, .56 + j * .08), P(.60, .56 + j * .08)], fill=(80, 120, 90, 255), width=lw)
        d.text(P(.50, .80), "generico · nessun marchio", font=font(COURR, int(S * .035)), fill=(200, 200, 200, 255), anchor="mm")
    elif name == "safe":                   # cassaforte (conto all'estero)
        d.rounded_rectangle([P(.16, .14), P(.84, .86)], radius=S * .04, fill=(80, 84, 92, 255), outline=(40, 42, 48, 255), width=lw * 2)
        d.ellipse([P(.36, .34), P(.64, .62)], fill=(170, 172, 180, 255), outline=(40, 42, 48, 255), width=lw)
        for a_ in range(8):
            x = .50 + .11 * math.cos(a_ * math.pi / 4); y = .48 + .11 * math.sin(a_ * math.pi / 4)
            d.line([P(.50, .48), P(x, y)], fill=(60, 62, 70, 255), width=lw)
        d.rectangle([P(.70, .40), P(.76, .56)], fill=(200, 200, 210, 255))
        d.text(P(.50, .76), "N. 000000", font=font(COURR, int(S * .05)), fill=(220, 220, 220, 255), anchor="mm")
    elif name == "pen_gate":               # cancello del penitenziario
        d.rectangle([P(.06, .20), P(.94, .90)], fill=(150, 140, 126, 255))
        d.rectangle([P(.30, .40), P(.70, .90)], fill=(60, 62, 70, 255))
        for x in (.36, .44, .52, .60): d.line([P(x, .40), P(x, .90)], fill=(130, 132, 140, 255), width=lw * 2)
        d.rectangle([P(.06, .12), P(.94, .22)], fill=(120, 110, 98, 255))
        for x in (.14, .80): d.rectangle([P(x, .30), P(x + .08, .40)], fill=(60, 62, 70, 255))
    elif name == "inspector":              # cartellina dell'ispettore con spunta
        d.rounded_rectangle([P(.20, .10), P(.80, .92)], radius=S * .04, fill=(160, 120, 70, 255))
        d.rectangle([P(.26, .18), P(.74, .86)], fill=PAP)
        d.rectangle([P(.40, .06), P(.60, .14)], fill=STD)
        for j in range(4):
            y = .30 + j * .14; d.rectangle([P(.30, y), P(.38, y + .08)], outline=INKC, width=lw)
            d.line([P(.31, y + .04), P(.34, y + .07), P(.39, y - .01)], fill=GRN, width=lw)
            d.line([P(.44, y + .04), P(.68, y + .04)], fill=(120, 110, 90, 255), width=lw)
    elif name == "weekend":                # notte di fine settimana: luna e calendario
        d.rectangle([P(.12, .30), P(.62, .88)], fill=PAP, outline=INKC, width=lw)
        d.rectangle([P(.12, .30), P(.62, .42)], fill=RD2)
        d.text(P(.37, .64), "SAB\nDOM", font=font(OSW, int(S * .08)), fill=INKC, anchor="mm", align="center")
        d.ellipse([P(.62, .08), P(.90, .36)], fill=(240, 230, 170, 255)); d.ellipse([P(.70, .04), P(.96, .30)], fill=(0, 0, 0, 0))
    elif name == "phone_desk":             # telefono da scrivania anni '60
        d.rounded_rectangle([P(.18, .46), P(.82, .84)], radius=S * .08, fill=(170, 46, 40, 255), outline=(240, 220, 200, 255), width=lw)
        d.ellipse([P(.38, .52), P(.62, .76)], fill=(236, 228, 210, 255))
        for a_ in range(10):
            x = .50 + .085 * math.cos(a_ * math.pi / 5); y = .64 + .085 * math.sin(a_ * math.pi / 5)
            d.ellipse([P(x - .014, y - .014), P(x + .014, y + .014)], fill=(60, 40, 36, 255))
        d.rounded_rectangle([P(.12, .30), P(.88, .44)], radius=S * .06, fill=(170, 46, 40, 255), outline=(240, 220, 200, 255), width=lw)
        for j, r in enumerate((.08, .14)):
            d.arc([P(.50 - r, .16 - r), P(.50 + r, .16 + r)], 210, 330, fill=(222, 180, 62, 255), width=lw * 2)
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _c32[k] = im; return im

_prev_icon_32 = fx.icon
def _icon_32(name, size, color=None):
    if isinstance(name, str):
        m = spic32(name, size)
        if m is not None: return m
    return _prev_icon_32(name, size, color)
fx.icon = _icon_32

def cover_folder32(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 42, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 032", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "L'OLIO CHE NON C'ERA", font=font(SERIF, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "BAYONNE · 1963", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im
