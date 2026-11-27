# Elementi grafici del caso 030 (la Saliera di Cellini, Vienna 2003-2006): LA SALIERA stilizzata (scenografia ricorrente),
# il museo con l'impalcatura, la vetrina, il tridente, il telefono, il bosco con la cassa sepolta.
# Tutto disegnato da codice: nessuna foto, nessuna riproduzione dell'opera originale (solo schemi stilizzati).
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "029-collana"))
sys.path.insert(0, os.path.join(HERE, "..", "028-smemorato"))
sys.path.insert(0, os.path.join(HERE, "..", "027-dossena"))
from col import *
import col, smem, fx

WPL.update({"Vienna": (16.37, 48.21), "Firenze": (11.25, 43.77), "Roma": (12.50, 41.90), "Parigi": (2.35, 48.86),
            "Fontainebleau": (2.70, 48.40), "Innsbruck": (11.39, 47.27), "Zwettl": (15.17, 48.60)})

GK = (222, 180, 62, 255); GK2 = (170, 130, 40, 255); EBO = (40, 30, 26, 255); ENB = (40, 90, 170, 255); ENG = (40, 130, 80, 255)
GL = (170, 205, 225, 120); GLE = (120, 160, 190, 255); STONE = (196, 184, 160, 255); STONE2 = (150, 138, 116, 255); SCAF = (150, 150, 160, 255)
_cs = {}
def spic30(name, size):
    k = (name, size)
    if k in _cs: return _cs[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); lw = max(3, S // 60)
    def saliera(cx, cy, s, shine=True):
        X = lambda a: cx + (a - .5) * s; Y = lambda b: cy + (b - .5) * s
        Q = lambda a, b: (X(a) * S, Y(b) * S)
        W_ = max(2, int(lw * s * 1.6))
        d.rounded_rectangle([Q(.06, .74), Q(.94, .90)], radius=S * s * .05, fill=EBO)              # base d'ebano
        for j in range(4):                                                                          # statuette della base
            x = .18 + j * .21
            d.rectangle([Q(x - .035, .77), Q(x + .035, .87)], fill=(70, 52, 40, 255))
            d.ellipse([Q(x - .014, .775), Q(x + .014, .805)], fill=GK); d.polygon([Q(x - .022, .87), Q(x, .80), Q(x + .022, .87)], fill=GK)
        d.ellipse([Q(.08, .60), Q(.92, .78)], fill=GK, outline=GK2, width=W_)                      # piano d'oro
        d.chord([Q(.12, .62), Q(.50, .76)], 90, 270, fill=ENB)                                     # mare (smalto blu)
        d.chord([Q(.50, .62), Q(.88, .76)], 270, 450, fill=ENG)                                    # terra (smalto verde)
        for j in range(4): d.arc([Q(.16 + j * .07, .66), Q(.22 + j * .07, .70)], 0, 180, fill=(200, 220, 250, 255), width=W_)
        # NETTUNO (sinistra): sdraiato, busto inclinato, gambe verso sinistra
        d.polygon([Q(.10, .64), Q(.30, .60), Q(.34, .65), Q(.12, .68)], fill=GK, outline=GK2)     # gambe
        d.polygon([Q(.28, .62), Q(.40, .62), Q(.38, .38), Q(.30, .40)], fill=GK, outline=GK2)     # busto
        d.ellipse([Q(.30, .28), Q(.39, .38)], fill=GK, outline=GK2)                                 # testa
        d.line([Q(.22, .66), Q(.22, .12)], fill=GK2, width=W_ * 2)                                  # tridente
        d.line([Q(.18, .14), Q(.26, .14)], fill=GK2, width=W_ * 2)
        for dx in (-.04, 0, .04): d.polygon([Q(.22 + dx - .012, .14), Q(.22 + dx, .07), Q(.22 + dx + .012, .14)], fill=GK2)
        d.line([Q(.31, .46), Q(.23, .40)], fill=GK, width=W_ * 2)                                   # braccio
        d.polygon([Q(.40, .56), Q(.50, .56), Q(.48, .62), Q(.42, .62)], fill=GK, outline=GK2)      # navicella del sale
        d.line([Q(.45, .56), Q(.45, .48)], fill=GK2, width=W_)
        # LA TERRA (destra): sdraiata, gambe verso destra
        d.polygon([Q(.70, .60), Q(.90, .64), Q(.88, .68), Q(.66, .65)], fill=GK, outline=GK2)
        d.polygon([Q(.60, .62), Q(.72, .62), Q(.70, .40), Q(.62, .42)], fill=GK, outline=GK2)
        d.ellipse([Q(.61, .30), Q(.70, .40)], fill=GK, outline=GK2)
        d.rectangle([Q(.76, .46), Q(.86, .60)], fill=GK, outline=GK2, width=W_)                    # tempietto del pepe
        for x in (.78, .81, .84): d.line([Q(x, .48), Q(x, .59)], fill=GK2, width=W_)
        d.polygon([Q(.74, .46), Q(.81, .39), Q(.88, .46)], fill=GK, outline=GK2)
        if shine:
            for (a, b) in ((.35, .24), (.66, .26), (.52, .70)):
                d.line([Q(a - .02, b), Q(a + .02, b)], fill=(255, 250, 220, 255), width=W_); d.line([Q(a, b - .02), Q(a, b + .02)], fill=(255, 250, 220, 255), width=W_)
    def vetrina(broken=False, empty=False):
        d.rectangle([P(.18, .78), P(.82, .96)], fill=(90, 70, 50, 255))
        d.rectangle([P(.16, .24), P(.84, .78)], fill=(70, 90, 110, 255), outline=GLE, width=lw)
        if not empty: saliera(.5, .55, .56, shine=not broken)
        d.line([P(.22, .30), P(.34, .42)], fill=(200, 225, 240, 255), width=lw)
        if broken:
            for a_ in range(0, 360, 40):
                r = .26; d.line([P(.46, .46), P(.46 + r * math.cos(math.radians(a_)), .46 + r * .9 * math.sin(math.radians(a_)))], fill=(240, 245, 250, 255), width=lw)
            d.polygon([P(.36, .36), P(.56, .34), P(.58, .56), P(.38, .58)], fill=(0, 0, 0, 0))
            for (x, y) in ((.30, .90), (.60, .92), (.70, .88), (.42, .93)): d.polygon([P(x, y), P(x + .04, y - .02), P(x + .03, y + .02)], fill=(220, 235, 245, 255))
    if name == "saliera":
        saliera(.5, .5, .96)
    elif name == "saliera_gold":          # solo la parte in oro, senza base (per le schede)
        saliera(.5, .55, .96, shine=True)
    elif name == "vitrine":
        vetrina()
    elif name == "vitrine_broken":
        vetrina(broken=True, empty=True)
    elif name == "vitrine_back":
        vetrina(broken=False, empty=False); d.rectangle([P(.16, .24), P(.84, .78)], outline=GK, width=lw * 2)
    elif name == "trident":
        d.line([P(.5, .92), P(.5, .22)], fill=GK, width=lw * 3)
        d.arc([P(.30, .06), P(.70, .40)], 0, 180, fill=GK, width=lw * 3)
        for x in (.30, .5, .70): d.polygon([P(x - .04, .22), P(x, .06), P(x + .04, .22)], fill=GK)
    elif name == "facade":              # facciata del museo con impalcatura
        d.rectangle([P(.04, .20), P(.96, .92)], fill=STONE)
        d.polygon([P(.02, .20), P(.50, .04), P(.98, .20)], fill=STONE2)
        for r_ in range(2):
            for c in range(5):
                x = .10 + c * .17; y = .32 + r_ * .30
                d.rounded_rectangle([P(x, y), P(x + .10, y + .18)], radius=S * .02, fill=(60, 70, 90, 255))
        for x in (.06, .30, .54, .78):
            d.line([P(x, .20), P(x, .94)], fill=SCAF, width=lw)
        for y in (.30, .56, .82): d.line([P(.04, y), P(.96, y)], fill=SCAF, width=lw)
        for y in (.30, .56): d.rectangle([P(.04, y - .01), P(.96, y + .01)], fill=(130, 110, 80, 255))
    elif name == "facade_win":          # con la finestra rotta
        im2 = spic30("facade", size); _cs.pop(("facade", size), None)
        im = im2.resize((S, S)); d = ImageDraw.Draw(im)
        x, y = .44, .32; d.rounded_rectangle([P(x, y), P(x + .10, y + .18)], radius=S * .02, fill=(230, 230, 210, 255), outline=RED + (255,), width=lw * 2)
        for a_ in range(0, 360, 60):
            d.line([P(x + .05, y + .09), P(x + .05 + .06 * math.cos(math.radians(a_)), y + .09 + .08 * math.sin(math.radians(a_)))], fill=(60, 70, 90, 255), width=lw)
    elif name == "forest_box":          # il bosco con la cassa sepolta
        d.rectangle([P(.0, .60), P(1, 1)], fill=(110, 84, 56, 255))
        d.rectangle([P(.0, .58), P(1, .62)], fill=(60, 100, 50, 255))
        for x, h_ in ((.12, .46), (.32, .52), (.70, .50), (.90, .44)):
            d.rectangle([P(x - .02, .58 - h_ * .35), P(x + .02, .60)], fill=(80, 60, 40, 255))
            d.polygon([P(x - .12, .58 - h_ * .30), P(x, .58 - h_), P(x + .12, .58 - h_ * .30)], fill=(40, 90, 55, 255))
        d.rectangle([P(.40, .72), P(.62, .88)], fill=(150, 120, 80, 255), outline=(90, 70, 40, 255), width=lw)
        d.line([P(.40, .80), P(.62, .80)], fill=(90, 70, 40, 255), width=lw)
        d.text(P(.51, .64), "?", font=font(OSW, int(S * .10)), fill=GK, anchor="mm")
    elif name == "box_closed":
        d.rectangle([P(.16, .34), P(.84, .82)], fill=(150, 120, 80, 255), outline=(90, 70, 40, 255), width=lw * 2)
        d.line([P(.16, .48), P(.84, .48)], fill=(90, 70, 40, 255), width=lw)
    elif name == "box_open":
        d.rectangle([P(.16, .50), P(.84, .88)], fill=(150, 120, 80, 255), outline=(90, 70, 40, 255), width=lw * 2)
        d.polygon([P(.16, .50), P(.30, .26), P(.98, .26), P(.84, .50)], fill=(120, 95, 60, 255))
        saliera(.5, .48, .44)
    elif name == "alarm":                # sirena d'allarme che suona
        d.rectangle([P(.30, .66), P(.70, .76)], fill=(80, 80, 90, 255))
        d.chord([P(.32, .30), P(.68, .90)], 180, 360, fill=(220, 50, 40, 255))
        for r in (.30, .40):
            d.arc([P(.5 - r, .60 - r), P(.5 + r, .60 + r)], 200, 250, fill=GK, width=lw * 2)
            d.arc([P(.5 - r, .60 - r), P(.5 + r, .60 + r)], 290, 340, fill=GK, width=lw * 2)
    elif name == "sms":                  # telefono con un messaggio
        d.rounded_rectangle([P(.30, .10), P(.70, .90)], radius=S * .05, fill=(40, 40, 46, 255))
        d.rectangle([P(.34, .18), P(.66, .74)], fill=(150, 200, 160, 255))
        for y in (.30, .40, .50): d.line([P(.38, y), P(.62, y)], fill=(40, 60, 40, 255), width=lw)
        d.ellipse([P(.46, .78), P(.54, .86)], fill=(90, 90, 100, 255))
    elif name == "cctv":                 # telecamera di sorveglianza
        d.line([P(.20, .20), P(.20, .40)], fill=(90, 90, 100, 255), width=lw * 2)
        d.polygon([P(.20, .30), P(.70, .38), P(.66, .56), P(.18, .46)], fill=(200, 200, 205, 255), outline=(90, 90, 100, 255))
        d.ellipse([P(.64, .40), P(.76, .54)], fill=(40, 40, 50, 255))
        d.polygon([P(.76, .46), P(.98, .30), P(.98, .78)], fill=(255, 240, 150, 90))
    elif name == "goldsmith":            # banco dell'orafo con martelletto
        d.rectangle([P(.08, .62), P(.92, .72)], fill=(110, 80, 50, 255)); d.rectangle([P(.14, .72), P(.20, .94)], fill=(90, 64, 40, 255)); d.rectangle([P(.80, .72), P(.86, .94)], fill=(90, 64, 40, 255))
        d.ellipse([P(.30, .48), P(.52, .62)], fill=GK, outline=GK2, width=lw)
        d.line([P(.60, .60), P(.80, .30)], fill=(110, 80, 50, 255), width=lw * 2); d.rectangle([P(.74, .22), P(.90, .32)], fill=(120, 120, 130, 255))
    elif name == "perseus":              # statua in bronzo stilizzata (sagoma generica)
        d.rectangle([P(.30, .80), P(.70, .96)], fill=STONE2)
        d.ellipse([P(.42, .10), P(.56, .24)], fill=(90, 70, 50, 255))
        d.polygon([P(.40, .26), P(.58, .26), P(.62, .56), P(.36, .56)], fill=(90, 70, 50, 255))
        d.line([P(.42, .56), P(.38, .80)], fill=(90, 70, 50, 255), width=lw * 3); d.line([P(.56, .56), P(.62, .80)], fill=(90, 70, 50, 255), width=lw * 3)
        d.line([P(.58, .30), P(.80, .14)], fill=(90, 70, 50, 255), width=lw * 2)
        d.line([P(.40, .32), P(.24, .44)], fill=(130, 130, 140, 255), width=lw * 2)
    elif name == "fireplace":            # fonderia / forno
        d.rectangle([P(.16, .30), P(.84, .92)], fill=(120, 70, 50, 255))
        d.chord([P(.30, .44), P(.70, .96)], 180, 360, fill=(30, 20, 20, 255))
        d.polygon([P(.40, .90), P(.46, .66), P(.52, .80), P(.58, .62), P(.62, .90)], fill=(240, 150, 40, 255))
    elif name == "scaffold_man":         # sagoma che sale sull'impalcatura (nessuna persona reale)
        for x in (.20, .80): d.line([P(x, .06), P(x, .96)], fill=SCAF, width=lw * 2)
        for y in (.20, .42, .64, .86): d.line([P(.20, y), P(.80, y)], fill=SCAF, width=lw * 2)
        d.ellipse([P(.44, .24), P(.56, .36)], fill=(236, 230, 218, 255))
        d.line([P(.50, .36), P(.50, .56)], fill=(236, 230, 218, 255), width=lw * 3)
        d.line([P(.50, .40), P(.36, .24)], fill=(236, 230, 218, 255), width=lw * 2); d.line([P(.50, .40), P(.64, .30)], fill=(236, 230, 218, 255), width=lw * 2)
        d.line([P(.50, .56), P(.40, .68)], fill=(236, 230, 218, 255), width=lw * 2); d.line([P(.50, .56), P(.60, .64)], fill=(236, 230, 218, 255), width=lw * 2)
    elif name == "wind":                 # soffio di vento stilizzato
        for k_, y in enumerate((.32, .50, .68)):
            d.line([P(.14, y), P(.70 - k_ * .08, y)], fill=(200, 215, 230, 255), width=lw * 2)
            d.arc([P(.62 - k_ * .08, y - .12), P(.86 - k_ * .08, y)], 270, 450 if False else 90, fill=(200, 215, 230, 255), width=lw * 2)
    elif name == "shards":               # piccoli frammenti dorati
        for (x, y, r) in ((.30, .40, .10), (.58, .32, .08), (.46, .62, .12), (.72, .60, .07), (.24, .70, .06)):
            d.polygon([P(x - r, y), P(x, y - r * 1.2), P(x + r, y - r * .2), P(x + r * .4, y + r)], fill=GK, outline=GK2)
    elif name == "gold":                 # lingotti d'oro generici
        for (x, y) in ((.20, .62), (.50, .62), (.35, .40)):
            d.polygon([P(x, y + .18), P(x + .30, y + .18), P(x + .26, y), P(x + .04, y)], fill=GK, outline=GK2)
            d.line([P(x + .06, y + .04), P(x + .24, y + .04)], fill=(255, 240, 180, 255), width=lw)
    elif name == "eurobag":              # sacco di soldi generico con simbolo dell'euro
        d.polygon([P(.40, .16), P(.60, .16), P(.56, .30), P(.44, .30)], fill=(180, 150, 100, 255))
        d.ellipse([P(.18, .26), P(.82, .92)], fill=(190, 160, 110, 255), outline=(120, 95, 60, 255), width=lw)
        d.text(P(.5, .60), "€", font=font(OSW, int(S * .30)), fill=(90, 70, 40, 255), anchor="mm")
    elif name == "fleur":                # giglio stilizzato (simbolo generico della Francia antica)
        d.ellipse([P(.42, .10), P(.58, .56)], fill=GK)
        d.chord([P(.10, .26), P(.50, .66)], 90, 300, fill=GK); d.chord([P(.50, .26), P(.90, .66)], 240, 450, fill=GK)
        d.rectangle([P(.30, .58), P(.70, .66)], fill=GK); d.polygon([P(.44, .66), P(.56, .66), P(.50, .90)], fill=GK)
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _cs[k] = im; return im

_prev_icon_30 = fx.icon
def _icon_30(name, size, color=None):
    if isinstance(name, str):
        m = spic30(name, size)
        if m is not None: return m
    return _prev_icon_30(name, size, color)
fx.icon = _icon_30
smem.giu.pic = lambda name, size: fx.icon(name, size)

def cover_folder30(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 39, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 030", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "LA SALIERA", font=font(SERIF, int(w * .09)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "VIENNA · 2003-2006", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im
