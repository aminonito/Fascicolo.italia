# Elementi grafici del caso 020 (il Totonero, 1980): stadio e campo stilizzati, schedina e foglietti delle scommesse
# ricostruiti, tabellone delle partite (scenografia ricorrente), cassetta di frutta, tavola del ristorante.
# Tutto disegnato da codice: nessuna foto reale, nessun logo di squadre, emittenti o federazioni, nessun documento originale.
import math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "019-eufronio"))
from euf import *
import euf, met, fi, fx, pon
from fx import *
from pon import WorldMap, WPL

WPL.update({"Roma": (12.50, 41.90), "Milano": (9.19, 45.46), "Pescara": (14.21, 42.46), "Avellino": (14.79, 40.91),
            "Bologna": (11.34, 44.49), "Perugia": (12.39, 43.11), "Palermo": (13.36, 38.12), "Napoli": (14.25, 40.85),
            "Genova": (8.93, 44.41), "Lecce": (18.17, 40.35), "Taranto": (17.24, 40.47), "Torino": (7.68, 45.07),
            "Madrid": (-3.70, 40.42), "Barcellona": (2.17, 41.39), "Vigo": (-8.72, 42.24)})

GRASS = (46, 110, 62); GRASS2 = (54, 124, 70); LINEC = (236, 240, 232)
_pt = {}
def tpic(name, size):
    k = (name, size)
    if k in _pt: return _pt[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); wh = (240, 238, 232, 255); lw = max(3, S // 70)
    if name == "stadium":       # stadio generico visto di tre quarti
        d.ellipse([P(.04, .30), P(.96, .92)], fill=(120, 124, 132, 255))
        d.ellipse([P(.12, .40), P(.88, .84)], fill=(70, 74, 82, 255))
        d.ellipse([P(.20, .48), P(.80, .78)], fill=GRASS + (255,))
        d.line([P(.50, .48), P(.50, .78)], fill=wh, width=lw)
        d.ellipse([P(.45, .58), P(.55, .68)], outline=wh, width=lw)
        for x in (.10, .90):
            d.rectangle([P(x - .012, .08), P(x + .012, .46)], fill=(150, 150, 156, 255))
            d.rectangle([P(x - .06, .04), P(x + .06, .12)], fill=(250, 240, 180, 255))
    elif name == "pitch":       # campo visto dall'alto
        d.rectangle([P(.04, .18), P(.96, .82)], fill=GRASS + (255,))
        for j in range(6): d.rectangle([P(.04 + j * .153, .18), P(.04 + j * .153 + .0765, .82)], fill=GRASS2 + (255,))
        d.rectangle([P(.04, .18), P(.96, .82)], outline=wh, width=lw)
        d.line([P(.50, .18), P(.50, .82)], fill=wh, width=lw); d.ellipse([P(.42, .40), P(.58, .60)], outline=wh, width=lw)
        d.rectangle([P(.04, .34), P(.16, .66)], outline=wh, width=lw); d.rectangle([P(.84, .34), P(.96, .66)], outline=wh, width=lw)
    elif name == "slip":        # foglietto di una scommessa clandestina (generico)
        d.rectangle([P(.18, .06), P(.82, .94)], fill=(244, 236, 206, 255), outline=(170, 150, 110, 255), width=lw)
        f = font(TYPE, int(S * .07))
        for j, (l, r) in enumerate([("PARTITA A", "1"), ("PARTITA B", "X"), ("PARTITA C", "X"), ("PARTITA D", "2")]):
            y = .20 + j * .14
            d.text(P(.24, y), l, font=f, fill=(60, 50, 40, 255), anchor="lm")
            d.text(P(.74, y), r, font=font(OSW, int(S * .09), 700), fill=RED + (255,), anchor="mm")
            d.line([P(.24, y + .06), P(.76, y + .06)], fill=(190, 170, 130, 255), width=lw // 2)
        d.text(P(.50, .84), "?", font=font(OSW, int(S * .12), 700), fill=(120, 100, 70, 255), anchor="mm")
    elif name == "schedina":    # schedina generica del concorso a pronostici (13 righe, nessun marchio)
        d.rectangle([P(.20, .04), P(.80, .96)], fill=(236, 240, 232, 255), outline=(90, 130, 90, 255), width=lw)
        d.rectangle([P(.20, .04), P(.80, .12)], fill=(90, 130, 90, 255))
        d.text(P(.50, .08), "13 PARTITE", font=font(OSW, int(S * .06), 700), fill=wh, anchor="mm")
        rr = random.Random(4)
        for j in range(13):
            y = .155 + j * .061
            for c, x in enumerate((.56, .65, .74)):
                d.rectangle([P(x - .03, y - .02), P(x + .03, y + .02)], outline=(90, 130, 90, 255), width=max(1, lw // 2))
                if rr.random() < .36: d.line([P(x - .025, y - .015), P(x + .025, y + .015)], fill=(30, 40, 120, 255), width=lw)
            d.line([P(.25, y), P(.48, y)], fill=(150, 160, 150, 255), width=max(1, lw // 2))
    elif name == "whistle":
        d.ellipse([P(.10, .38), P(.56, .84)], fill=(200, 204, 210, 255))
        d.rectangle([P(.33, .38), P(.90, .56)], fill=(200, 204, 210, 255))
        d.ellipse([P(.25, .53), P(.41, .69)], fill=(60, 64, 70, 255))
        d.line([P(.20, .40), P(.10, .12)], fill=RED + (255,), width=lw * 2)
    elif name == "scoreboard":  # tabellone luminoso generico
        d.rectangle([P(.06, .20), P(.94, .74)], fill=(24, 24, 28, 255), outline=(120, 120, 130, 255), width=lw)
        d.text(P(.50, .47), "1 - 1", font=font(OSW, int(S * .26), 700), fill=(250, 200, 60, 255), anchor="mm")
        d.rectangle([P(.46, .74), P(.54, .96)], fill=(100, 100, 110, 255))
    elif name == "restaurant":  # tavola apparecchiata
        d.ellipse([P(.08, .40), P(.92, .70)], fill=(236, 230, 214, 255))
        d.rectangle([P(.08, .55), P(.92, .82)], fill=(200, 60, 50, 255))
        for x in range(8): d.rectangle([P(.08 + x * .105, .55), P(.08 + x * .105 + .052, .82)], fill=(236, 230, 214, 255))
        d.ellipse([P(.26, .44), P(.44, .54)], fill=wh, outline=(170, 160, 150, 255), width=lw // 2)
        d.ellipse([P(.56, .44), P(.74, .54)], fill=wh, outline=(170, 160, 150, 255), width=lw // 2)
        d.polygon([P(.47, .18), P(.53, .18), P(.55, .46), P(.45, .46)], fill=(70, 110, 70, 255))
        d.rectangle([P(.48, .10), P(.52, .18)], fill=(70, 110, 70, 255))
    elif name == "fruit":       # cassetta di frutta e verdura
        d.rectangle([P(.08, .50), P(.92, .90)], fill=(190, 150, 90, 255), outline=(120, 90, 50, 255), width=lw)
        for y in (.63, .77): d.line([P(.08, y), P(.92, y)], fill=(120, 90, 50, 255), width=lw)
        rr = random.Random(9)
        for _ in range(11):
            x, y, r = rr.uniform(.16, .84), rr.uniform(.36, .50), rr.uniform(.06, .09)
            col = rr.choice([(220, 60, 40), (240, 160, 40), (120, 170, 60), (230, 200, 60)])
            d.ellipse([P(x - r, y - r), P(x + r, y + r)], fill=col + (255,))
    elif name == "shirt":       # maglia generica senza colori di squadra riconoscibili
        d.polygon([P(.30, .12), P(.42, .18), P(.58, .18), P(.70, .12), P(.94, .30), P(.84, .46), P(.76, .40), P(.76, .92),
                   P(.24, .92), P(.24, .40), P(.16, .46), P(.06, .30)], fill=(220, 222, 226, 255))
        d.text(P(.50, .58), "10", font=font(OSW, int(S * .26), 700), fill=(40, 60, 120, 255), anchor="mm")
    elif name == "betbook":     # quaderno dell'allibratore
        d.rectangle([P(.16, .08), P(.84, .92)], fill=(60, 60, 66, 255))
        d.rectangle([P(.22, .12), P(.80, .88)], fill=(236, 230, 214, 255))
        f = font(TYPE, int(S * .06))
        for j in range(7):
            y = .20 + j * .095
            d.text(P(.27, y), "lire", font=f, fill=(90, 80, 70, 255), anchor="lm")
            d.text(P(.76, y), "".join(random.Random(j).choice("0123456789") for _ in range(3)) + ".000", font=f, fill=RED + (255,), anchor="rm")
    elif name == "microphone":
        d.ellipse([P(.36, .08), P(.64, .40)], fill=(150, 150, 160, 255))
        d.rectangle([P(.46, .38), P(.54, .80)], fill=(60, 60, 66, 255)); d.rectangle([P(.32, .80), P(.68, .88)], fill=(60, 60, 66, 255))
    elif name == "law":         # codice / gazzetta generica
        d.rectangle([P(.18, .08), P(.82, .92)], fill=(150, 40, 40, 255))
        d.rectangle([P(.24, .14), P(.76, .86)], outline=(230, 200, 120, 255), width=lw)
        d.text(P(.50, .40), "LEGGE", font=font(OSW, int(S * .12), 700), fill=(240, 210, 130, 255), anchor="mm")
        d.text(P(.50, .58), "401", font=font(OSW, int(S * .16), 700), fill=(240, 210, 130, 255), anchor="mm")
    elif name == "policecar":   # auto di servizio generica, senza scritte
        d.rounded_rectangle([P(.06, .46), P(.94, .74)], S // 30, fill=(60, 66, 74, 255))
        d.polygon([P(.24, .46), P(.34, .28), P(.68, .28), P(.80, .46)], fill=(60, 66, 74, 255))
        d.polygon([P(.30, .45), P(.37, .32), P(.49, .32), P(.49, .45)], fill=(170, 200, 220, 255))
        d.polygon([P(.53, .45), P(.53, .32), P(.66, .32), P(.74, .45)], fill=(170, 200, 220, 255))
        d.rectangle([P(.44, .20), P(.56, .28)], fill=(70, 130, 255, 255))
        for x in (.26, .74): d.ellipse([P(x - .09, .64), P(x + .09, .82)], fill=(20, 20, 22, 255)); d.ellipse([P(x - .04, .69), P(x + .04, .77)], fill=(150, 150, 150, 255))
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _pt[k] = im
    return im

_prev_icon_t = fx.icon
def _icon_t(name, size, color=None):
    if name in ("bottle", "bottle_bad"): name = "money"
    if isinstance(name, str):
        m = tpic(name, size)
        if m is not None: return m
    return _prev_icon_t(name, size, color)
fx.icon = _icon_t

def cover_folder20(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 31, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .28), "FASCICOLO N. 020", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .50), "IL TOTONERO", font=font(SERIF, int(w * .09)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .66), "ROMA · 1979-1982", font=font(TYPE, int(w * .05)), fill=(90, 70, 50, 255), anchor="mm")
    recon_label(d, w, h)
    return im

class Tabellone(El):
    """scenografia ricorrente: il tabellone delle partite. rows = [(casa, ospite, pronostico, risultato)];
    il pronostico appare in oro, poi il risultato; se diverso compare una X rossa sulla riga."""
    def __init__(self, box, rows, t0, t1=None, title="TABELLONE · schema semplificato", reveal=True, gap=0.55):
        super().__init__(t0, t1, 0.3); self.box, self.rows, self.title, self.reveal, self.gap = box, rows, title, reveal, gap
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; d = ImageDraw.Draw(lay); al = int(255 * a)
        d.rounded_rectangle([x0, y0, x1, y1], 16, fill=(20, 22, 26, int(235 * a)), outline=(110, 110, 120, al), width=4)
        d.text(((x0 + x1) / 2, y0 + 34), self.title, font=font(OSW, 32, 600), fill=GOLD + (al,), anchor="mm")
        n = len(self.rows); rh = min(110, (y1 - y0 - 120) / max(1, n)); fz = int(min(46, rh * 0.5))
        cx = [x0 + (x1 - x0) * f for f in (.05, .50, .70, .86)]
        d.text((cx[2], y0 + 76), "ACCORDO", font=font(OSW, 24, 600), fill=GREY + (al,), anchor="mm")
        d.text((cx[3], y0 + 76), "FINALE", font=font(OSW, 24, 600), fill=GREY + (al,), anchor="mm")
        for j, r in enumerate(self.rows):
            tt = self.t0 + 0.3 + self.gap * j
            if t < tt: continue
            u = ease((t - tt) / 0.3); ra = int(al * u); y = y0 + 120 + rh * (j + 0.5)
            casa, osp, pro, ris = r[:4]; sg = r[4] if len(r) > 4 else ris
            d.text((cx[0], y), f"{casa} – {osp}", font=font(OSW, fz, 600), fill=WHITE + (ra,), anchor="lm")
            if pro: d.text((cx[2], y), pro, font=font(OSW, fz + 6, 700), fill=GOLD + (ra,), anchor="mm")
            tr = tt + 0.35
            if ris and (not self.reveal or t > tr):
                d.text((cx[3], y), ris, font=font(OSW, fz + 6, 700), fill=WHITE + (ra,), anchor="mm")
                if pro and pro not in ("?", "") and sg != pro and t > tr + 0.2:
                    s = rh * 0.32; xx = cx[3] + 90
                    d.line([(xx - s, y - s), (xx + s, y + s)], fill=RED + (ra,), width=8); d.line([(xx - s, y + s), (xx + s, y - s)], fill=RED + (ra,), width=8)
                elif pro and sg == pro and t > tr + 0.2:
                    d.text((cx[3] + 90, y), "✓", font=font(PS, fz + 6), fill=(110, 200, 120, ra), anchor="mm")
            d.line([(x0 + 30, y + rh / 2), (x1 - 30, y + rh / 2)], fill=(60, 60, 66, ra), width=2)

class Campo(El):
    """scenografia del 23 marzo: il campo visto dall'alto, i giocatori (pallini) e, da t_pol, le auto e le divise
    che entrano dal bordo; tabellone con il minuto che scorre."""
    def __init__(self, box, t0, t1=None, t_pol=None, minute=(80, 90), label="DOMENICA 23 MARZO 1980 · ORE 15", seed=3):
        super().__init__(t0, t1, 0.35); self.box, self.t_pol, self.minute, self.label, self.seed = box, t_pol, minute, label, seed
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; d = ImageDraw.Draw(lay); al = int(255 * a)
        d.rectangle([x0, y0, x1, y1], fill=GRASS + (al,))
        sw = (x1 - x0) / 10
        for j in range(0, 10, 2): d.rectangle([x0 + j * sw, y0, x0 + (j + 1) * sw, y1], fill=GRASS2 + (al,))
        lw = 5; c = LINEC + (al,)
        d.rectangle([x0 + 20, y0 + 20, x1 - 20, y1 - 20], outline=c, width=lw)
        mx = (x0 + x1) / 2; my = (y0 + y1) / 2; ph = (y1 - y0)
        d.line([(mx, y0 + 20), (mx, y1 - 20)], fill=c, width=lw); d.ellipse([mx - ph * .16, my - ph * .16, mx + ph * .16, my + ph * .16], outline=c, width=lw)
        for xa, xb in ((x0 + 20, x0 + 20 + (x1 - x0) * .14), (x1 - 20 - (x1 - x0) * .14, x1 - 20)):
            d.rectangle([xa, my - ph * .28, xb, my + ph * .28], outline=c, width=lw)
        rr = random.Random(self.seed)
        k = t - self.t0
        for j in range(22):
            bx, by = rr.uniform(x0 + 80, x1 - 80), rr.uniform(y0 + 60, y1 - 60)
            ox, oy = 40 * math.sin(k * 0.9 + j), 25 * math.cos(k * 0.7 + j * 1.3)
            if self.t_pol and t > self.t_pol + 1.5:   # fine partita: i giocatori si fermano e vanno verso il centro
                u = ease(min(1, (t - self.t_pol - 1.5) / 2.0)); ox, oy = lerp(ox, (mx - bx) * 0.6, u), lerp(oy, (my - by) * 0.6, u)
            col = (230, 230, 236) if j < 11 else (40, 70, 150)
            px, py = bx + ox, by + oy
            d.ellipse([px - 15, py - 15, px + 15, py + 15], fill=col + (al,), outline=(20, 20, 20, al), width=2)
        bxx, byy = mx + 40 * math.sin(k * 1.7), my + 30 * math.cos(k * 1.3)
        d.ellipse([bxx - 8, byy - 8, bxx + 8, byy + 8], fill=(250, 250, 250, al), outline=(0, 0, 0, al), width=2)
        # tabellone
        m0, m1 = self.minute; mn = int(min(m1, m0 + k * 1.2))
        d.rounded_rectangle([x1 - 250, y0 - 70, x1, y0 - 8], 10, fill=(20, 20, 24, al))
        d.text((x1 - 125, y0 - 39), f"{mn}'", font=font(OSW, 44, 700), fill=(250, 200, 60, al), anchor="mm")
        d.text((x0, y0 - 39), self.label, font=font(OSW, 34, 600), fill=WHITE + (al,), anchor="lm")
        if self.t_pol and t > self.t_pol:
            u = ease(min(1, (t - self.t_pol) / 1.4))
            for j in range(4):
                px = lerp(x0 - 120, x0 + 120 + j * 150, u); py = y1 - 50
                d.rounded_rectangle([px - 50, py - 22, px + 50, py + 22], 8, fill=(60, 66, 74, al), outline=(20, 20, 20, al), width=2)
                if int(t * 4) % 2 == j % 2: d.ellipse([px - 12, py - 34, px + 12, py - 18], fill=(80, 140, 255, al))
            for j in range(6):
                px = lerp(x1 + 60, x1 - 200 - j * 70, ease(min(1, max(0, (t - self.t_pol - 0.4) / 1.6)))); py = y0 + 80 + j * 60
                d.ellipse([px - 16, py - 16, px + 16, py + 16], fill=(30, 34, 40, al), outline=(220, 220, 220, al), width=3)
        d.text((mx, y1 + 26), "schema semplificato · non in scala · nessuna squadra reale riconoscibile", font=font(COURR, 22), fill=GREY + (al,), anchor="mm")

met.STEPS = [("scomm", "slip", "GLI SCOMMETTITORI"), ("inter", "restaurant", "I CONTATTI"), ("calc", "shirt", "ALCUNI GIOCATORI"),
             ("part", "ball", "LA PARTITA"), ("alli", "betbook", "GLI ALLIBRATORI")]
