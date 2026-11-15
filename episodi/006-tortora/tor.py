# Elementi grafici del caso 006 (Enzo Tortora): studio TV stilizzato (scenografia ricorrente), aula di tribunale
# con gabbia, agendina RICOSTRUITA (Tortona / Tortora), centrini, giornale ricostruito, urna del referendum.
# Tutto disegnato da codice: nessuna foto reale, nessun logo.
import math, random, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "005-majorana"))
from fi import *
import fi
import fx
from fx import *
import maj                      # icone generiche già pronte (phone, tv, folder, question, passport...)
from maj import clue_card, Clues, mpic

fi.PLACES.update({"Bergamo": (9.67, 45.70), "Strasburgo": (7.75, 48.58)})
GREEN = (70, 160, 90)

_tc = {}
def tpic(name, size):
    k = (name, size)
    if k in _tc: return _tc[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); w = max(2, S // 22)
    g = GOLD + (255,); wh = WHITE + (255,); ink = INK + (255,)
    if name == "parrot":
        gr = (60, 160, 80, 255); dk = (40, 110, 60, 255)
        d.line([P(.20, .86), P(.84, .86)], fill=(120, 84, 50, 255), width=S // 18)
        d.polygon([P(.44, .60), P(.36, .98), P(.54, .96)], fill=(200, 60, 50, 255))
        d.ellipse([P(.30, .36), P(.66, .84)], fill=gr)
        d.ellipse([P(.36, .14), P(.70, .46)], fill=gr)
        d.chord([P(.28, .44), P(.60, .80)], 90, 270, fill=dk)
        d.ellipse([P(.54, .24), P(.62, .32)], fill=wh); d.ellipse([P(.565, .26), P(.605, .30)], fill=ink)
        d.polygon([P(.66, .26), P(.82, .32), P(.68, .42)], fill=(240, 200, 80, 255))
        d.line([P(.44, .82), P(.44, .88)], fill=(90, 80, 70, 255), width=S // 40); d.line([P(.54, .82), P(.54, .88)], fill=(90, 80, 70, 255), width=S // 40)
    elif name == "doily":
        c = (244, 240, 230, 255)
        for k in range(16):
            an = k * math.pi / 8; x, y = .5 + .36 * math.cos(an), .5 + .36 * math.sin(an)
            d.ellipse([P(x - .09, y - .09), P(x + .09, y + .09)], fill=c)
        d.ellipse([P(.18, .18), P(.82, .82)], fill=c)
        for r in (.26, .18, .10):
            d.ellipse([P(.5 - r, .5 - r), P(.5 + r, .5 + r)], outline=(190, 182, 166, 255), width=S // 60)
        for k in range(12):
            an = k * math.pi / 6; d.line([P(.5 + .10 * math.cos(an), .5 + .10 * math.sin(an)), P(.5 + .30 * math.cos(an), .5 + .30 * math.sin(an))], fill=(190, 182, 166, 255), width=S // 80)
        for k in range(16):
            an = k * math.pi / 8; x, y = .5 + .36 * math.cos(an), .5 + .36 * math.sin(an)
            d.ellipse([P(x - .03, y - .03), P(x + .03, y + .03)], fill=(200, 192, 176, 255))
    elif name == "addressbook":
        d.rounded_rectangle([P(.16, .06), P(.84, .94)], S // 20, fill=(40, 60, 96, 255))
        d.rectangle([P(.22, .10), P(.80, .90)], fill=(232, 224, 204, 255))
        for k in range(6): d.line([P(.28, .26 + k * .11), P(.74, .26 + k * .11)], fill=(150, 160, 190, 255), width=S // 90)
        d.rounded_rectangle([P(.78, .40), P(.94, .54)], S // 40, fill=RED + (255,))
        d.text(P(.86, .47), "T", font=font(OSW, int(S * .10), 700), fill=wh, anchor="mm")
        d.text(P(.50, .20), "RUBRICA", font=font(OSW, int(S * .07), 600), fill=ink, anchor="mm")
    elif name == "ballot":
        d.polygon([P(.14, .42), P(.86, .42), P(.80, .92), P(.20, .92)], fill=(200, 196, 186, 255))
        d.rectangle([P(.12, .36), P(.88, .44)], fill=(160, 156, 146, 255)); d.rectangle([P(.38, .38), P(.62, .41)], fill=(40, 36, 32, 255))
        d.rectangle([P(.36, .06), P(.64, .38)], fill=wh, outline=(120, 110, 100, 255), width=S // 60)
        d.line([P(.42, .20), P(.48, .28)], fill=RED + (255,), width=S // 30); d.line([P(.48, .28), P(.58, .12)], fill=RED + (255,), width=S // 30)
        d.text(P(.50, .66), "REFERENDUM", font=font(OSW, int(S * .07), 600), fill=ink, anchor="mm")
    elif name == "mic":
        d.rounded_rectangle([P(.38, .08), P(.62, .50)], S // 8, fill=(170, 170, 176, 255))
        for k in range(4): d.line([P(.40, .16 + k * .08), P(.60, .16 + k * .08)], fill=(110, 110, 116, 255), width=S // 70)
        d.arc([P(.30, .24), P(.70, .62)], 0, 180, fill=g, width=S // 30)
        d.line([P(.50, .62), P(.50, .86)], fill=g, width=S // 30); d.line([P(.34, .88), P(.66, .88)], fill=g, width=S // 24)
    elif name == "tvcam":
        d.rectangle([P(.14, .26), P(.70, .56)], fill=(60, 60, 66, 255)); d.rectangle([P(.70, .32), P(.90, .50)], fill=(40, 40, 46, 255))
        d.ellipse([P(.84, .34), P(.94, .48)], fill=(120, 150, 170, 255))
        d.ellipse([P(.18, .30), P(.24, .36)], fill=RED + (255,))
        d.line([P(.42, .56), P(.42, .80)], fill=(90, 90, 96, 255), width=S // 24)
        for x in (.20, .42, .64): d.line([P(.42, .80), P(x, .96)], fill=(90, 90, 96, 255), width=S // 30)
    elif name == "cage":
        d.rectangle([P(.08, .10), P(.92, .94)], outline=(150, 150, 156, 255), width=S // 30)
        for k in range(1, 8): d.line([P(.08 + k * .105, .10), P(.08 + k * .105, .94)], fill=(150, 150, 156, 255), width=S // 40)
        d.line([P(.08, .30), P(.92, .30)], fill=(150, 150, 156, 255), width=S // 50)
    elif name == "scales":
        d.line([P(.50, .12), P(.50, .86)], fill=g, width=S // 26); d.line([P(.30, .90), P(.70, .90)], fill=g, width=S // 20)
        d.line([P(.14, .26), P(.86, .26)], fill=g, width=S // 30)
        for x in (.14, .86):
            d.line([P(x, .26), P(x - .10, .56)], fill=g, width=S // 60); d.line([P(x, .26), P(x + .10, .56)], fill=g, width=S // 60)
            d.chord([P(x - .14, .46), P(x + .14, .66)], 0, 180, fill=g)
        d.ellipse([P(.46, .08), P(.54, .16)], fill=g)
    elif name == "parliament":
        d.rectangle([P(.10, .80), P(.90, .88)], fill=(180, 170, 150, 255))
        d.pieslice([P(.14, .30), P(.86, 1.10)], 180, 360, fill=(190, 180, 160, 255))
        for r in (.30, .22, .14):
            d.arc([P(.5 - r, .70 - r), P(.5 + r, .70 + r)], 180, 360, fill=(110, 100, 90, 255), width=S // 40)
        d.text(P(.50, .20), "PARLAMENTO EUROPEO", font=font(OSW, int(S * .065), 600), fill=wh, anchor="mm")
    elif name == "crochet":
        d.line([P(.20, .86), P(.80, .14)], fill=(180, 180, 190, 255), width=S // 24)
        d.arc([P(.74, .06), P(.88, .20)], 200, 40, fill=(180, 180, 190, 255), width=S // 30)
        d.arc([P(.10, .50), P(.60, .96)], 120, 360, fill=(240, 236, 226, 255), width=S // 40)
    elif name == "prison":
        d.rectangle([P(.10, .30), P(.90, .92)], fill=(130, 124, 116, 255))
        for k in range(5): d.rectangle([P(.16 + k * .15, .40), P(.24 + k * .15, .52)], fill=(30, 28, 26, 255))
        for k in range(5):
            for j in range(3): d.line([P(.18 + k * .15 + j * .025, .40), P(.18 + k * .15 + j * .025, .52)], fill=(160, 160, 166, 255), width=S // 120)
        d.rectangle([P(.40, .66), P(.60, .92)], fill=(50, 44, 40, 255))
        d.polygon([P(.06, .32), P(.50, .12), P(.94, .32)], fill=(96, 90, 84, 255))
    else:
        return None
    im = im.resize((size, size), Image.LANCZOS); _tc[k] = im
    return im

_prev_icon = fx.icon
def _icon(name, size, color=None):
    if isinstance(name, str):
        m = tpic(name, size)
        if m is not None: return m
    return _prev_icon(name, size, color)
fx.icon = _icon

# ---------------------------------------------------------------- scenografia: studio TV stilizzato
class Studio(El):
    """studio televisivo (schema): sipario, luci, trespolo con pappagallo, banco dei telefoni.
    ring: (t0, t1) telefoni che squillano; dark: istante in cui le luci si spengono; sign: testo sul fondale"""
    def __init__(self, box, t0, t1=None, ring=None, dark=None, parrot=True, sign="STUDIO TV · VENERDÌ SERA", label="ricostruzione · schema"):
        super().__init__(t0, t1, 0.4); self.box, self.ring, self.dark, self.parrot, self.sign, self.label = box, ring, dark, parrot, sign, label
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; w, h = x1 - x0, y1 - y0; d = ImageDraw.Draw(lay)
        dk = 0.0 if self.dark is None or t < self.dark else ease((t - self.dark) / 0.8)
        al = int(255 * a); lit = 1 - 0.65 * dk
        sh = lambda c: tuple(int(v * lit) for v in c) + (al,)
        d.rectangle([x0, y0, x1, y1], fill=sh((40, 22, 30)))
        for k in range(14):
            xx = x0 + k * w / 14
            d.rectangle([xx, y0, xx + w / 28, y0 + h * .72], fill=sh((120, 30, 40)))
            d.rectangle([xx + w / 28, y0, xx + w / 14, y0 + h * .72], fill=sh((96, 22, 32)))
        d.rectangle([x0, y0, x1, y0 + h * .07], fill=sh((70, 16, 24)))
        if self.sign:
            d.rectangle([x0 + w * .30, y0 + h * .12, x0 + w * .70, y0 + h * .24], fill=sh((22, 20, 30)), outline=GOLD + (int(al * lit),), width=3)
            d.text((x0 + w * .5, y0 + h * .18), self.sign, font=font(OSW, int(h * .055), 600), fill=sh(GOLD), anchor="mm")
        d.polygon([(x0, y0 + h * .72), (x1, y0 + h * .72), (x1, y1), (x0, y1)], fill=sh((70, 58, 50)))
        for k in range(9):
            d.line([(x0 + w * .5 + (k - 4) * w * .03, y0 + h * .72), (x0 + w * .5 + (k - 4) * w * .14, y1)], fill=sh((84, 70, 60)), width=2)
        if dk < 0.99:
            for cx in (x0 + w * .18, x0 + w * .5, x0 + w * .82):
                cone = Image.new("RGBA", lay.size, (0, 0, 0, 0)); dc = ImageDraw.Draw(cone)
                dc.polygon([(cx - 20, y0 + 10), (cx + 20, y0 + 10), (cx + w * .12, y1), (cx - w * .12, y1)], fill=(255, 240, 200, int(26 * a * (1 - dk))))
                lay.alpha_composite(cone)
                d.ellipse([cx - 22, y0 + 2, cx + 22, y0 + 30], fill=(240, 230, 200, int(al * (1 - dk))))
        # banco dei telefoni
        bx0, bx1, by = x0 + w * .58, x0 + w * .96, y0 + h * .80
        d.rectangle([bx0, by, bx1, by + h * .12], fill=sh((150, 130, 100)))
        for k in range(5):
            px = bx0 + (k + 0.5) * (bx1 - bx0) / 5; py = by - h * .02
            rr = self.ring and self.ring[0] <= t <= self.ring[1] and math.sin((t - self.ring[0]) * 18 + k * 1.7) > 0.2
            jig = (math.sin(t * 70 + k) * 4) if rr else 0
            place(lay, fx.icon("phone", int(h * .09)), (px + jig, py), "mm", a * lit)
            if rr: d.ellipse([px - 9, py - h * .08 - 9, px + 9, py - h * .08 + 9], fill=RED + (al,))
        if self.parrot:
            px, py = x0 + w * .14, y0 + h * .62
            d.line([(px, py + h * .06), (px, y1 - h * .05)], fill=sh((120, 84, 50)), width=8)
            d.line([(px - 50, y1 - h * .05), (px + 50, y1 - h * .05)], fill=sh((120, 84, 50)), width=8)
            bob = math.sin(t * 3) * 4
            place(lay, tpic("parrot", int(h * .2)), (px, py + bob), "mm", a * lit)
        if self.label: d.text((x1 - 14, y1 - 10), self.label, font=font(COURR, 20), fill=(200, 190, 176, int(al * .8)), anchor="rs")

# ---------------------------------------------------------------- aula di tribunale (schema)
class Aula(El):
    """aula: banco dei giudici con 3 toghe, gabbia degli imputati a sinistra, scritta LA LEGGE È UGUALE PER TUTTI"""
    def __init__(self, box, t0, t1=None, judges_t=None, cage_t=None, who=None, label="schema semplificato · non in scala", motto=True):
        super().__init__(t0, t1, 0.4); self.box, self.judges_t, self.cage_t, self.who, self.label, self.motto = box, judges_t, cage_t, who, label, motto
    def draw(self, lay, t, a):
        x0, y0, x1, y1 = self.box; w, h = x1 - x0, y1 - y0; d = ImageDraw.Draw(lay); al = int(255 * a)
        d.rectangle([x0, y0, x1, y1], fill=(58, 48, 40, al))
        for k in range(10): d.rectangle([x0 + k * w / 10 + 6, y0 + 10, x0 + (k + 1) * w / 10 - 6, y0 + h * .55], fill=(70, 58, 48, al))
        if self.motto: d.text((x0 + w * .62, y0 + h * .10), "LA LEGGE È UGUALE PER TUTTI", font=font(SERIF, int(h * .055)), fill=(200, 180, 140, al), anchor="mm")
        d.rectangle([x0, y0 + h * .62, x1, y1], fill=(84, 66, 52, al))
        # banco dei giudici
        bx0, bx1 = x0 + w * .36, x0 + w * .90; by = y0 + h * .42
        if self.judges_t is not None and t >= self.judges_t:
            ja = a * ease((t - self.judges_t) / 0.4)
            for k in range(3):
                draw_person(lay, bx0 + (k + 0.5) * (bx1 - bx0) / 3, by + h * .10, 0.62 * h / 700, "judge", alpha=int(255 * ja))
        d.rectangle([bx0, by, bx1, by + h * .22], fill=(110, 78, 50, al), outline=(70, 50, 34, al), width=4)
        d.rectangle([bx0 + 20, by + 16, bx1 - 20, by + h * .22 - 16], outline=(140, 104, 70, al), width=3)
        cx = x0 + w * .62; place(lay, fx.icon("scales", int(h * .14)), (cx, by + h * .11), "mm", a)
        # gabbia
        if self.cage_t is not None and t >= self.cage_t:
            ca = a * ease((t - self.cage_t) / 0.4); cal = int(255 * ca)
            gx0, gx1, gy0, gy1 = x0 + w * .03, x0 + w * .30, y0 + h * .30, y1 - h * .04
            d.rectangle([gx0, gy1 - 16, gx1, gy1], fill=(60, 60, 64, cal))
            if self.who: draw_person(lay, (gx0 + gx1) / 2, gy1 - 18, 0.9 * h / 700, "suit", alpha=cal)
            for k in range(13): d.line([(gx0 + k * (gx1 - gx0) / 12, gy0), (gx0 + k * (gx1 - gx0) / 12, gy1)], fill=(170, 170, 176, cal), width=5)
            d.line([(gx0, gy0), (gx1, gy0)], fill=(170, 170, 176, cal), width=8)
            d.line([(gx0, gy0 + (gy1 - gy0) * .5), (gx1, gy0 + (gy1 - gy0) * .5)], fill=(170, 170, 176, cal), width=4)
        if self.label: d.text((x1 - 14, y1 - 10), self.label, font=font(COURR, 20), fill=(200, 190, 176, int(al * .8)), anchor="rs")

# ---------------------------------------------------------------- agendina ricostruita
def agenda_img(w, h, entry="Tortona", seed=9):
    im = paper(w, h, (236, 230, 212), seed, 0.5); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 24, h], fill=(40, 60, 96, 255))
    d.rounded_rectangle([w - 70, 40, w - 10, 130], 10, fill=RED + (255,)); d.text((w - 40, 85), "T", font=font(OSW, 56, 700), fill=WHITE + (255,), anchor="mm")
    for k in range(9): d.line([(60, 120 + k * (h - 180) / 9), (w - 90, 120 + k * (h - 180) / 9)], fill=(150, 160, 196, 255), width=2)
    rng = random.Random(seed)
    hand = font(TYPE, int(h * .075))
    rows = ["T........  ■■ ■■■■", entry + "   ■■■ ■■■■■", "T.......  ■■■ ■■■", "T.........  ■■ ■■■■■"]
    for k, r in enumerate(rows):
        y = 120 + (k * 2 + 1) * (h - 180) / 9 - 6
        col = (30, 40, 90, 255) if k == 1 else (80, 86, 110, 255)
        d.text((70, y), r, font=hand, fill=col, anchor="lb")
    recon_label(d, w, h)
    return im

def lettere(w, h, word, hl, color=RED):
    """parola scritta a mano con una lettera evidenziata (indice hl)"""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = font(TYPE, int(h * .7)); tot = sum(tl(d, c, f) for c in word); x = (w - tot) / 2
    for k, c in enumerate(word):
        d.text((x, h * .5), c, font=f, fill=(color if k == hl else WHITE) + (255,), anchor="lm")
        if k == hl:
            cw = tl(d, c, f); d.ellipse([x - 18, h * .5 - h * .42, x + cw + 18, h * .5 + h * .42], outline=color + (255,), width=6)
        x += tl(d, c, f)
    return im

def card_box(lines, w=560, h=300, title=None):
    """riquadro scuro con righe"""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 18, fill=(28, 26, 24, 235), outline=GOLD + (255,), width=3)
    y = 30
    if title: d.text((w / 2, y), title, font=font(OSW, 34, 600), fill=GOLD + (255,), anchor="mt"); y += 60
    for l in lines:
        r = rich_img(l, PS, 34, WHITE, REDL, align="m"); im.alpha_composite(r, (int((w - r.width) / 2), y)); y += r.height + 8
    return im

def cover_folder(w=520):
    h = int(w * 0.78); im = paper(w, h, (196, 160, 104), 21, 0.6); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, w - 30, h - 30], outline=(120, 90, 50, 255), width=3)
    d.text((w / 2, h * .30), "FASCICOLO N. 006", font=font(TYPE, int(w * .07)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .52), "IL CASO TORTORA", font=font(SERIF, int(w * .1)), fill=INK + (255,), anchor="mm")
    d.text((w / 2, h * .72), "Roma · Napoli · 1983-1987", font=font(COURR, int(w * .045)), fill=(90, 70, 50, 255), anchor="mm")
    return im
