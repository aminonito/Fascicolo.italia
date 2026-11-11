# FASCICOLO ITALIA — elementi animati: omini, icone, camera, folle, orologi, calendari, porte.
import math, random
from fi import *
import fi

SKIN = (198, 164, 134)
COAT = dict(worker=(234, 232, 224), plumber=(64, 92, 128), police=(36, 46, 84), suit=(78, 72, 66), painter=(150, 104, 62),
            guard=(52, 58, 68), judge=(26, 24, 22), man=(96, 88, 80), expert=(110, 100, 90), poet=(90, 70, 60))
PANTS = (44, 41, 39)

def lerp(a, b, u): return a + (b - a) * u

# ---------------------------------------------------------------- omino
def draw_person(lay, x, y, s, kind="worker", phase=0.0, moving=False, carry=None, arms="down", alpha=255, flip=1):
    d = ImageDraw.Draw(lay); A = alpha
    coat = COAT.get(kind, COAT["man"]) + (A,)
    d.ellipse([x - 50 * s, y - 10 * s, x + 50 * s, y + 10 * s], fill=(0, 0, 0, int(A * 0.35)))
    sw = math.sin(phase) * 0.5 if moving else 0.0
    hip = (x, y - 92 * s)
    legc = (coat if kind == "plumber" else PANTS + (A,))
    for k in (1, -1):
        fx_ = x + math.sin(sw * k) * 70 * s
        d.line([hip, (fx_, y - 4 * s)], fill=legc, width=int(18 * s))
        d.ellipse([fx_ - 14 * s, y - 12 * s, fx_ + 16 * s, y + 4 * s], fill=(28, 26, 24, A))
    bottom = y - (58 if kind in ("worker", "painter", "judge") else 84) * s
    bulge = 10 * s if carry == "hidden" else 0
    # braccia dietro
    sh_l, sh_r = (x - 34 * s, y - 176 * s), (x + 34 * s, y - 176 * s)
    def hand(side):
        if arms == "up": return (x + side * 64 * s, y - 250 * s)
        if arms == "hold" or carry == "painting": return (x + side * 22 * s, y - 126 * s)
        if arms == "point" and side == flip: return (x + side * 96 * s, y - 170 * s)
        return (x + side * (42 * s) + (math.sin(sw * -side) * 40 * s if moving else 0), y - 96 * s)
    for side, sh in ((-1, sh_l), (1, sh_r)):
        hd = hand(side)
        d.line([sh, hd], fill=coat, width=int(16 * s))
        d.ellipse([hd[0] - 9 * s, hd[1] - 9 * s, hd[0] + 9 * s, hd[1] + 9 * s], fill=SKIN + (A,))
    d.rounded_rectangle([x - 38 * s - bulge, y - 194 * s, x + 38 * s + bulge, bottom], int(20 * s), fill=coat)
    if carry == "hidden":
        d.rectangle([x - 26 * s, y - 170 * s, x + 26 * s, y - 92 * s], outline=(200, 196, 186, int(A * 0.8)), width=max(1, int(3 * s)))
    if kind == "police":
        for by in (-160, -130, -100):
            d.ellipse([x - 4 * s, y + by * s - 4 * s, x + 4 * s, y + by * s + 4 * s], fill=GOLD + (A,))
    d.ellipse([x - 25 * s, y - 248 * s, x + 25 * s, y - 196 * s], fill=SKIN + (A,))
    if kind == "police":
        d.rectangle([x - 24 * s, y - 262 * s, x + 24 * s, y - 236 * s], fill=COAT["police"] + (A,))
        d.rectangle([x - 30 * s, y - 238 * s, x + 30 * s, y - 232 * s], fill=(20, 20, 30, A))
    elif kind == "painter":
        d.ellipse([x - 30 * s, y - 258 * s, x + 26 * s, y - 232 * s], fill=(120, 30, 30, A))
    elif kind in ("suit", "expert", "poet", "man", "judge"):
        d.chord([x - 26 * s, y - 252 * s, x + 26 * s, y - 214 * s], 180, 360, fill=(40, 34, 30, A))
    elif kind == "plumber":
        d.chord([x - 27 * s, y - 254 * s, x + 27 * s, y - 220 * s], 180, 360, fill=(40, 60, 90, A))
    if carry == "painting":
        im = painting_icon(int(78 * s))
        place(lay, im, (x, y - 140 * s), "mm", A / 255)
    elif carry == "glass":
        d.rectangle([x - 46 * s, y - 210 * s, x + 46 * s, y - 80 * s], fill=(170, 200, 220, int(A * 0.35)), outline=(220, 235, 245, A), width=max(1, int(3 * s)))
    elif carry == "pliers":
        hd = hand(1); place(lay, icon("pliers", int(60 * s)), (hd[0] + 10 * s, hd[1] - 10 * s), "mm", A / 255)
    elif carry == "magnifier":
        hd = hand(1); place(lay, icon("magnifier", int(70 * s)), (hd[0] + 20 * s, hd[1] - 20 * s), "mm", A / 255)
    elif carry == "easel":
        place(lay, icon("easel", int(150 * s)), (x + 90 * s, y - 70 * s), "mm", A / 255)

class Figure(El):
    """keys: [(t, x, y)] percorso; carry: [(t, modo)]; arms: [(t, modo)]"""
    def __init__(self, keys, t0, t1=None, kind="worker", s=1.0, carry=None, arms=None, label=None, flip=1):
        super().__init__(t0, t1, 0.3)
        self.keys = sorted(keys); self.kind, self.s, self.label, self.flip = kind, (s * 1.35 if s >= 0.6 else s), label, flip
        self.carry = sorted(carry or []); self.arms = sorted(arms or [])
    def pos(self, t):
        ks = self.keys
        if t <= ks[0][0]: return ks[0][1], ks[0][2], False, 0.0
        dist = 0.0
        for p, q in zip(ks, ks[1:]):
            seg = math.dist(p[1:], q[1:])
            if t <= q[0]:
                u = (t - p[0]) / max(1e-6, q[0] - p[0])
                return lerp(p[1], q[1], u), lerp(p[2], q[2], u), seg > 1, dist + seg * u
            dist += seg
        return ks[-1][1], ks[-1][2], False, dist
    def state(self, lst, t, default=None):
        v = default
        for tt, m in lst:
            if t >= tt: v = m
        return v
    def draw(self, lay, t, a):
        x, y, mv, dist = self.pos(t)
        draw_person(lay, x, y, self.s, self.kind, dist / (26 * self.s), mv, self.state(self.carry, t), self.state(self.arms, t, "down"), int(255 * a), self.flip)
        if self.label:
            d = ImageDraw.Draw(lay); f = font(OSW, max(18, int(34 * self.s + 8)), 600); tw = tl(d, self.label, f)
            ly = y - 290 * self.s
            d.rounded_rectangle([x - tw / 2 - 14, ly - f.size * 0.75, x + tw / 2 + 14, ly + f.size * 0.75], 10, fill=(14, 12, 11, int(200 * a)))
            d.text((x, ly), self.label, font=f, fill=WHITE + (int(255 * a),), anchor="mm")

# ---------------------------------------------------------------- icone
_ic = {}
def painting_icon(w):
    k = ("painting", w)
    if k in _ic: return _ic[k]
    fr = Frame((0, 0), w, int(w * 1.45), 0); _ic[k] = fr.pic
    return fr.pic

def icon(name, size, color=None):
    k = (name, size, color)
    if k in _ic: return _ic[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = (color or WHITE) + (255,); g = GOLD + (255,); w = max(2, S // 22)
    P = lambda a, b: (a * S, b * S)
    if name == "lock":
        d.rounded_rectangle([P(.18, .44), P(.82, .94)], S // 10, fill=g)
        d.arc([P(.28, .10), P(.72, .62)], 180, 360, fill=g, width=S // 10)
        d.ellipse([P(.45, .60), P(.55, .70)], fill=(40, 30, 20, 255)); d.rectangle([P(.48, .66), P(.52, .80)], fill=(40, 30, 20, 255))
    elif name == "pliers":
        d.line([P(.2, .2), P(.62, .62)], fill=(170, 170, 176, 255), width=S // 9); d.line([P(.2, .62), P(.62, .2)], fill=(170, 170, 176, 255), width=S // 9)
        d.line([P(.62, .62), P(.92, .92)], fill=RED + (255,), width=S // 7); d.line([P(.2, .62) if False else P(.62, .2), P(.92, .1)], fill=RED + (255,), width=S // 7)
    elif name == "knob":
        d.ellipse([P(.2, .2), P(.8, .8)], fill=g, outline=(120, 90, 40, 255), width=w); d.rectangle([P(.45, .75), P(.55, 1.0)], fill=(140, 110, 50, 255))
    elif name == "magnifier":
        d.ellipse([P(.08, .08), P(.62, .62)], outline=g, width=S // 10); d.line([P(.55, .55), P(.92, .92)], fill=g, width=S // 7)
    elif name == "easel":
        d.line([P(.5, .05), P(.15, .98)], fill=(150, 110, 70, 255), width=S // 16); d.line([P(.5, .05), P(.85, .98)], fill=(150, 110, 70, 255), width=S // 16)
        d.rectangle([P(.22, .18), P(.78, .62)], fill=(230, 222, 200, 255), outline=(120, 90, 60, 255), width=w)
    elif name == "camera":
        d.rectangle([P(.12, .32), P(.88, .82)], fill=(60, 50, 44, 255), outline=c, width=w); d.ellipse([P(.36, .42), P(.64, .70)], fill=(20, 20, 24, 255), outline=c, width=w)
        d.rectangle([P(.2, .2), P(.38, .32)], fill=c)
    elif name == "house":
        d.polygon([P(.08, .48), P(.5, .1), P(.92, .48)], fill=(110, 80, 60, 255)); d.rectangle([P(.18, .46), P(.82, .94)], fill=(150, 140, 126, 255))
        d.rectangle([P(.42, .64), P(.58, .94)], fill=(70, 50, 36, 255)); d.rectangle([P(.24, .54), P(.36, .66)], fill=(240, 210, 120, 255)); d.rectangle([P(.64, .54), P(.76, .66)], fill=(240, 210, 120, 255))
    elif name == "museum":
        d.polygon([P(.04, .32), P(.5, .06), P(.96, .32)], fill=(200, 190, 170, 255)); d.rectangle([P(.06, .32), P(.94, .38)], fill=(200, 190, 170, 255))
        for k in range(6): d.rectangle([P(.12 + k * .14, .40), P(.18 + k * .14, .84)], fill=(220, 212, 194, 255))
        d.rectangle([P(.04, .84), P(.96, .94)], fill=(200, 190, 170, 255))
    elif name == "envelope":
        d.rectangle([P(.06, .22), P(.94, .78)], fill=PAPER + (255,), outline=(120, 100, 80, 255), width=w)
        d.line([P(.06, .22), P(.5, .54), P(.94, .22)], fill=(120, 100, 80, 255), width=w); d.ellipse([P(.42, .46), P(.58, .62)], fill=RED + (255,))
    elif name == "train":
        d.rectangle([P(.06, .30), P(.70, .74)], fill=(60, 64, 72, 255)); d.rectangle([P(.70, .44), P(.94, .74)], fill=(80, 84, 92, 255))
        d.rectangle([P(.14, .22), P(.26, .34)], fill=(80, 84, 92, 255)); d.rectangle([P(.12, .40), P(.30, .54)], fill=(240, 210, 120, 255)); d.rectangle([P(.40, .40), P(.58, .54)], fill=(240, 210, 120, 255))
        for cx in (.2, .5, .82): d.ellipse([P(cx - .08, .68), P(cx + .08, .84)], fill=(30, 30, 34, 255))
    elif name == "handcuffs":
        d.ellipse([P(.06, .30), P(.46, .70)], outline=(190, 190, 196, 255), width=S // 12); d.ellipse([P(.54, .30), P(.94, .70)], outline=(190, 190, 196, 255), width=S // 12)
        d.line([P(.44, .5), P(.56, .5)], fill=(190, 190, 196, 255), width=S // 16)
    elif name == "gavel":
        d.rectangle([P(.12, .16), P(.56, .42)], fill=(130, 84, 44, 255)); d.line([P(.34, .40), P(.80, .88)], fill=(150, 100, 56, 255), width=S // 10)
        d.rectangle([P(.50, .86), P(.98, .96)], fill=(110, 70, 36, 255))
    elif name == "crown":
        d.polygon([P(.08, .74), P(.08, .30), P(.30, .52), P(.5, .22), P(.70, .52), P(.92, .30), P(.92, .74)], fill=g); d.rectangle([P(.08, .74), P(.92, .86)], fill=g)
    elif name == "bicorne":
        d.chord([P(.04, .30), P(.96, 1.0)], 180, 360, fill=(30, 30, 34, 255)); d.ellipse([P(.44, .40), P(.56, .52)], fill=(200, 40, 40, 255))
    elif name == "money":
        for k in range(4):
            y0 = .70 - k * .14
            d.rounded_rectangle([P(.08, y0), P(.92, y0 + .2)], S // 30, fill=(120, 150, 110, 255), outline=(70, 96, 64, 255), width=w)
        d.ellipse([P(.42, .30), P(.58, .46)], outline=(70, 96, 64, 255), width=w)
    elif name == "glass":
        d.rectangle([P(.12, .08), P(.88, .92)], fill=(170, 200, 220, 90), outline=(220, 235, 245, 255), width=w)
        for k in range(3): d.line([P(.2 + k * .2, .2), P(.36 + k * .2, .4)], fill=(240, 250, 255, 200), width=w)
    elif name == "frame_empty":
        d.rectangle([P(.12, .04), P(.88, .96)], outline=(170, 128, 64, 255), width=S // 12)
    elif name == "bed":
        d.rectangle([P(.04, .5), P(.96, .76)], fill=(150, 130, 110, 255)); d.rectangle([P(.04, .3), P(.14, .86)], fill=(110, 80, 60, 255)); d.rectangle([P(.86, .44), P(.96, .86)], fill=(110, 80, 60, 255))
        d.rounded_rectangle([P(.16, .40), P(.34, .54)], S // 30, fill=(230, 226, 214, 255))
    elif name == "moon":
        d.ellipse([P(.15, .15), P(.85, .85)], fill=(230, 220, 170, 255)); d.ellipse([P(.35, .05), P(1.0, .75)], fill=(0, 0, 0, 0))
    elif name == "sun":
        d.ellipse([P(.28, .28), P(.72, .72)], fill=g)
        for k in range(8):
            a_ = k * math.pi / 4; d.line([P(.5 + .3 * math.cos(a_), .5 + .3 * math.sin(a_)), P(.5 + .46 * math.cos(a_), .5 + .46 * math.sin(a_))], fill=g, width=w * 2)
    elif name == "newspaper":
        d.rectangle([P(.1, .1), P(.9, .9)], fill=(226, 214, 186, 255)); d.rectangle([P(.18, .18), P(.82, .30)], fill=(40, 34, 30, 255))
        for k in range(5): d.line([P(.18, .40 + k * .1), P(.82 if k % 2 else .6, .40 + k * .1)], fill=(110, 100, 90, 255), width=w)
    elif name == "drawer":
        d.rectangle([P(.06, .06), P(.94, .94)], fill=(120, 90, 60, 255))
        for r in range(3):
            for cc in range(2):
                d.rectangle([P(.12 + cc * .42, .12 + r * .28), P(.46 + cc * .42, .34 + r * .28)], fill=(150, 116, 80, 255)); d.rectangle([P(.24 + cc * .42, .22 + r * .28), P(.34 + cc * .42, .25 + r * .28)], fill=g)
    elif name == "bars":
        for k in range(6): d.rectangle([P(.06 + k * .17, .02), P(.12 + k * .17, .98)], fill=(90, 92, 98, 255))
        d.rectangle([P(0, .1), P(1, .16)], fill=(90, 92, 98, 255)); d.rectangle([P(0, .84), P(1, .9)], fill=(90, 92, 98, 255))
    elif name == "stairs":
        for k in range(5): d.rectangle([P(.1 + k * .16, .8 - k * .16), P(.9, .96 - k * .16)], fill=(150, 140, 126, 255))
    elif name == "corridor":
        d.polygon([P(.05, .05), P(.95, .05), P(.62, .38), P(.38, .38)], fill=(80, 74, 68, 255)); d.polygon([P(.05, .95), P(.95, .95), P(.62, .62), P(.38, .62)], fill=(120, 110, 100, 255))
        d.polygon([P(.05, .05), P(.38, .38), P(.38, .62), P(.05, .95)], fill=(100, 92, 84, 255)); d.polygon([P(.95, .05), P(.62, .38), P(.62, .62), P(.95, .95)], fill=(100, 92, 84, 255))
        d.rectangle([P(.38, .38), P(.62, .62)], fill=(240, 220, 160, 255))
    elif name == "smock":
        d.polygon([P(.3, .08), P(.7, .08), P(.92, .3), P(.8, .4), P(.74, .3), P(.76, .94), P(.24, .94), P(.26, .3), P(.2, .4), P(.08, .3)], fill=(234, 232, 224, 255))
    elif name == "bench":
        d.rectangle([P(.04, .40), P(.96, .92)], fill=(110, 72, 40, 255)); d.rectangle([P(.0, .32), P(1.0, .42)], fill=(140, 96, 56, 255))
        d.ellipse([P(.42, .52), P(.58, .70)], fill=g)
    im = im.resize((size, size), Image.LANCZOS); _ic[k] = im
    return im

class Icon(El):
    def __init__(self, name, xy, t0, t1=None, size=120, anim="pop", color=None, move=None, label=None, rot=0):
        super().__init__(t0, t1, 0.2); self.im = icon(name, size, color) if isinstance(name, str) else name
        if rot: self.im = self.im.rotate(rot, expand=True, resample=Image.BICUBIC)
        self.xy, self.anim, self.move, self.label = xy, anim, move, label
    def draw(self, lay, t, a):
        k = t - self.t0; im = self.im; x, y = self.xy
        if self.move:  # (t_start, dur, (x1,y1), arc)
            ts, du, (x1, y1), arc = self.move
            u = ease_io((t - ts) / du) if t > ts else 0
            x, y = lerp(x, x1, u), lerp(y, y1, u) - arc * math.sin(math.pi * u)
        if self.anim == "pop" and k < 0.35:
            s = back(k / 0.35)
            if s > 0.02: im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
        elif self.anim == "shake" and k < 0.6:
            x += math.sin(k * 60) * 10 * (1 - k / 0.6)
        place(lay, im, (x, y), "mm", a)
        if self.label:
            d = ImageDraw.Draw(lay); f = font(OSW, 30, 600); tw = tl(d, self.label, f); ly = y + self.im.height / 2 + 26
            d.rounded_rectangle([x - tw / 2 - 12, ly - 22, x + tw / 2 + 12, ly + 22], 10, fill=(14, 12, 11, int(210 * a)))
            d.text((x, ly), self.label, font=f, fill=WHITE + (int(255 * a),), anchor="mm")

class Pill(El):
    def __init__(self, text, xy, t0, t1=None, size=36, bg=(14, 12, 11), fg=WHITE, accent=False):
        super().__init__(t0, t1, 0.25); self.text, self.xy, self.size = text, xy, size
        self.bg = RED if accent else bg; self.fg = fg
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); f = font(OSW, self.size, 600); tw = tl(d, self.text, f); x, y = self.xy
        dy = 14 * (1 - ease((t - self.t0) / 0.3))
        d.rounded_rectangle([x - tw / 2 - 20, y - self.size * 0.82 + dy, x + tw / 2 + 20, y + self.size * 0.82 + dy], 12, fill=self.bg + (int(225 * a),))
        d.text((x, y + dy), self.text, font=f, fill=self.fg + (int(255 * a),), anchor="mm")

class Arrow(El):
    def __init__(self, p0, p1, t0, t1=None, color=GOLD, width=8, dur=0.5, bend=0.0, dashed=False):
        super().__init__(t0, t1, 0.05); self.p0, self.p1, self.color, self.w, self.dur, self.bend, self.dashed = p0, p1, color, width, dur, bend, dashed
    def pts(self, n=40):
        (x0, y0), (x1, y1) = self.p0, self.p1
        mx, my = (x0 + x1) / 2 - (y1 - y0) * self.bend, (y0 + y1) / 2 + (x1 - x0) * self.bend
        return [((1 - u) ** 2 * x0 + 2 * (1 - u) * u * mx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * my + u * u * y1) for u in [i / n for i in range(n + 1)]]
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); P = self.pts(); f = ease((t - self.t0) / self.dur); k = max(2, int(len(P) * f))
        col = self.color + (int(255 * a),)
        if self.dashed:
            for i in range(0, k - 1, 2): d.line([P[i], P[i + 1]], fill=col, width=self.w)
        else: d.line(P[:k], fill=col, width=self.w, joint="curve")
        if f > 0.95:
            (xa, ya), (xb, yb) = P[-3], P[-1]; ang = math.atan2(yb - ya, xb - xa); h = self.w * 3.2
            d.polygon([(xb, yb), (xb - h * math.cos(ang - .5), yb - h * math.sin(ang - .5)), (xb - h * math.cos(ang + .5), yb - h * math.sin(ang + .5))], fill=col)

class ClockFace(El):
    """orologio: ore di partenza, velocità in ore per secondo"""
    def __init__(self, xy, r, t0, t1=None, start=7.0, speed=0.0, label=None):
        super().__init__(t0, t1, 0.3); self.xy, self.r, self.start, self.speed, self.label = xy, r, start, speed, label
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); x, y = self.xy; r = self.r * (back((t - self.t0) / 0.35) if t - self.t0 < 0.35 else 1); al = int(255 * a)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(232, 222, 200, al), outline=GOLD + (al,), width=max(3, int(r / 12)))
        for k in range(12):
            an = k * math.pi / 6; d.line([(x + r * .8 * math.sin(an), y - r * .8 * math.cos(an)), (x + r * .92 * math.sin(an), y - r * .92 * math.cos(an))], fill=INK + (al,), width=max(2, int(r / 25)))
        h = self.start + self.speed * max(0, t - self.t0)
        for ln, wd, an in ((r * .5, r / 9, (h % 12) / 12 * 2 * math.pi), (r * .78, r / 14, (h % 1) * 2 * math.pi)):
            d.line([(x, y), (x + ln * math.sin(an), y - ln * math.cos(an))], fill=INK + (al,), width=max(2, int(wd)))
        d.ellipse([x - r / 12, y - r / 12, x + r / 12, y + r / 12], fill=RED + (al,))
        if self.label: d.text((x, y + r + 34), self.label, font=font(OSW, int(r * 0.42), 600), fill=GOLD + (al,), anchor="mm")

class Calendar(El):
    """pagine: [(t, sopra, grande)] — sfoglia"""
    def __init__(self, xy, w, pages, t0, t1=None):
        super().__init__(t0, t1, 0.3); self.xy, self.w, self.pages = xy, w, pages
    def draw(self, lay, t, a):
        cur = self.pages[0]; tc = self.pages[0][0]
        for p in self.pages:
            if t >= p[0]: cur = p; tc = p[0]
        d = ImageDraw.Draw(lay); x, y = self.xy; w = self.w; h = w * 1.05; al = int(255 * a)
        k = ease((t - tc) / 0.18); dy = (1 - k) * -18
        d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], 14, fill=(236, 228, 210, al))
        d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y - h / 2 + w * 0.28], 14, fill=RED + (al,))
        d.rectangle([x - w / 2, y - h / 2 + w * 0.18, x + w / 2, y - h / 2 + w * 0.28], fill=RED + (al,))
        d.text((x, y - h / 2 + w * 0.14), cur[1], font=font(OSW, int(w * 0.14), 600), fill=WHITE + (al,), anchor="mm")
        big = cur[2]; fs = int(w * (0.5 if len(big) <= 2 else 0.3 if len(big) <= 4 else 0.2))
        d.text((x, y + w * 0.14 + dy), big, font=font(SERIF, fs), fill=INK + (int(al * k),), anchor="mm")

class Door(El):
    def __init__(self, xy, w, h, t0, t1=None, lock_t=None, unlock_t=None, open_t=None, knob_off=None):
        super().__init__(t0, t1, 0.3); self.xy, self.w, self.h = xy, w, h
        self.lock_t, self.unlock_t, self.open_t, self.knob_off = lock_t, unlock_t, open_t, knob_off
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); x, y = self.xy; w, h = self.w, self.h; al = int(255 * a)
        d.rectangle([x - w / 2 - 14, y - h - 14, x + w / 2 + 14, y], fill=(60, 50, 42, al))
        d.rectangle([x - w / 2, y - h, x + w / 2, y], fill=(14, 12, 10, al))
        o = ease((t - self.open_t) / 0.6) if self.open_t and t > self.open_t else 0
        dw = w * (1 - 0.8 * o)
        d.polygon([(x - w / 2, y - h), (x - w / 2 + dw, y - h - 12 * o), (x - w / 2 + dw, y + 12 * o), (x - w / 2, y)], fill=(120, 84, 52, al), outline=(80, 54, 32, al))
        for k in (0.2, 0.55):
            d.rectangle([x - w / 2 + dw * 0.15, y - h + h * k, x - w / 2 + dw * 0.85, y - h + h * (k + 0.3)], outline=(90, 62, 38, al), width=4)
        if not (self.knob_off and t > self.knob_off):
            kx = x - w / 2 + dw * 0.85; d.ellipse([kx - 10, y - h / 2 - 10, kx + 10, y - h / 2 + 10], fill=GOLD + (al,))
        if self.lock_t and t > self.lock_t and not (self.unlock_t and t > self.unlock_t):
            lt = t - self.lock_t; sh = math.sin(lt * 50) * 8 * max(0, 1 - lt / 0.5)
            place(lay, icon("lock", int(w * 0.5)), (x + sh, y - h - w * 0.4), "mm", a)

class Flash(El):
    def __init__(self, t0, dur=0.35):
        super().__init__(t0, t0 + 0.01, 0.01); self.dur = dur
    def alpha(self, t):
        return 0 if t < self.t0 or t > self.t0 + self.dur else 1
    def draw(self, lay, t, a):
        k = 1 - (t - self.t0) / self.dur
        lay.alpha_composite(Image.new("RGBA", lay.size, (255, 250, 240, int(200 * k))))

class Crowd(El):
    """folla di omini: in coda che cammina (queue) o che appare a griglia"""
    def __init__(self, box, n, t0, t1=None, s=0.35, mode="grid", walk=None, kinds=("man", "suit", "expert", "poet"), seed=3, stagger=0.04):
        super().__init__(t0, t1, 0.3); self.box, self.n, self.s, self.mode, self.walk, self.stagger = box, n, s, mode, walk, stagger
        rng = random.Random(seed); x0, y0, x1, y1 = box
        cols = max(1, int(math.sqrt(n * (x1 - x0) / max(1, (y1 - y0)))))
        rows = math.ceil(n / cols)
        self.p = []
        for i in range(n):
            r, c = divmod(i, cols)
            self.p.append((x0 + (c + 0.5 + rng.uniform(-.3, .3)) * (x1 - x0) / cols, y0 + (r + 1) * (y1 - y0) / rows + rng.uniform(-6, 6), rng.choice(kinds), rng.uniform(0, 6)))
        self.p.sort(key=lambda q: q[1])
    def draw(self, lay, t, a):
        for i, (x, y, k, ph) in enumerate(self.p):
            ti = self.t0 + i * self.stagger
            if t < ti: continue
            aa = a * ease((t - ti) / 0.3)
            dx = 0; mv = False
            if self.walk:  # velocità px/s verso destra
                dx = self.walk * (t - self.t0); mv = True
            draw_person(lay, x + dx, y, self.s, k, ph + (t - self.t0) * 8, mv, alpha=int(255 * aa))

class Bar(El):
    """barra orizzontale che cresce/si accorcia: keys [(t, frazione)]"""
    def __init__(self, x, y, wmax, h, keys, t0, t1=None, color=RED, label=None):
        super().__init__(t0, t1, 0.25); self.x, self.y, self.wmax, self.h, self.keys, self.color, self.label = x, y, wmax, h, keys, color, label
    def draw(self, lay, t, a):
        v = 0.0; prev = (self.t0, 0.0)
        for kt, kv in self.keys:
            if t >= kt: prev = (kt, v if v else kv); v = kv
        # interpolazione semplice
        v0 = 0.0; vv = 0.0
        for j, (kt, kv) in enumerate(self.keys):
            if t >= kt:
                vstart = self.keys[j - 1][1] if j else 0.0
                vv = lerp(vstart, kv, ease((t - kt) / 0.8))
        d = ImageDraw.Draw(lay); al = int(255 * a)
        d.rounded_rectangle([self.x, self.y, self.x + self.wmax, self.y + self.h], 10, fill=(40, 37, 34, al))
        if vv > 0.005: d.rounded_rectangle([self.x, self.y, self.x + self.wmax * vv, self.y + self.h], 10, fill=self.color + (al,))

class Wall(El):
    """parete di galleria con tanti quadri; uno (idx) è la Gioconda, evidenziabile e rimovibile"""
    def __init__(self, box, t0, t1=None, hl_t=None, gone_t=None, seed=5):
        super().__init__(t0, t1, 0.4); self.box, self.hl_t, self.gone_t = box, hl_t, gone_t
        rng = random.Random(seed); x0, y0, x1, y1 = box; self.frames = []
        cols = [(x0 + 30, 300, 210), (x0 + 380, 240, 300), (x0 + 690, 150, 216), (x0 + 900, 260, 200), (x0 + 1210, 220, 290)]
        for k, (x, w, h) in enumerate(cols):
            self.frames.append((x, y0 + 60 + rng.randint(0, 80), w, h, (rng.randint(60, 110), rng.randint(50, 90), rng.randint(40, 70))))
        self.gi = 2
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); al = int(255 * a); x0, y0, x1, y1 = self.box
        d.rectangle([x0, y0, x1, y1], fill=(58, 34, 30, al))
        d.rectangle([x0, y1 - 20, x1, y1], fill=(90, 70, 50, al))
        for k, (x, y, w, h, col) in enumerate(self.frames):
            if k == self.gi:
                gone = self.gone_t is not None and t > self.gone_t
                if not gone:
                    place(lay, painting_icon(int(w)).resize((int(w), int(h)), Image.LANCZOS), (x, y), "la", a)
                else:
                    for hx, hy in ((x + w * .2, y - 6), (x + w * .8, y - 6), (x + w * .2, y + h + 6), (x + w * .8, y + h + 6)):
                        d.ellipse([hx - 7, hy - 7, hx + 7, hy + 7], fill=(170, 165, 158, al))
                if self.hl_t is not None and t > self.hl_t and not gone:
                    p = 0.5 + 0.5 * math.sin((t - self.hl_t) * 5)
                    d.rectangle([x - 14, y - 14, x + w + 14, y + h + 14], outline=GOLD + (int(al * (0.5 + 0.5 * p)),), width=6)
            else:
                d.rectangle([x, y, x + w, y + h], fill=(120, 92, 50, al))
                d.rectangle([x + 14, y + 14, x + w - 14, y + h - 14], fill=col + (al,))
                d.polygon([(x + 14, y + h - 14), (x + w * 0.45, y + h * 0.45), (x + w - 14, y + h - 14)], fill=tuple(int(v * 0.7) for v in col) + (al,))

class Facade(El):
    """facciata di museo stilizzata (non in scala)"""
    def __init__(self, box, t0, t1=None, label=None, closed_t=None):
        super().__init__(t0, t1, 0.4); self.box, self.label, self.closed_t = box, label, closed_t
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); x0, y0, x1, y1 = self.box; al = int(255 * a); w = x1 - x0; h = y1 - y0
        stone = (176, 164, 144, al); dark = (120, 110, 96, al)
        d.rectangle([x0, y0 + h * .25, x1, y1], fill=stone)
        d.rectangle([x0 + w * .38, y0 + h * .08, x0 + w * .62, y1], fill=(190, 178, 156, al))
        d.polygon([(x0 + w * .36, y0 + h * .1), (x0 + w * .5, y0 - h * .08), (x0 + w * .64, y0 + h * .1)], fill=dark)
        for r in range(2):
            for c in range(16):
                cx = x0 + w * (0.03 + c * 0.061)
                if x0 + w * .37 < cx < x0 + w * .61: continue
                d.rectangle([cx, y0 + h * (.36 + r * .3), cx + w * .03, y0 + h * (.52 + r * .3)], fill=(60, 54, 48, al))
        d.rectangle([x0 + w * .46, y0 + h * .62, x0 + w * .54, y1], fill=(50, 40, 32, al))
        d.rectangle([x0 - 20, y1, x1 + 20, y1 + 14], fill=dark)
        if self.label:
            d.text((x0 + w * .5, y0 + h * .28), self.label, font=font(SERIF, int(h * .09)), fill=(60, 50, 40, al), anchor="mm")
        if self.closed_t and t > self.closed_t:
            k = ease((t - self.closed_t) / 0.3); f = font(OSW, int(h * .09), 700)
            cx, cy = x0 + w * .5, y0 + h * .78
            d.rounded_rectangle([cx - w * .09, cy - h * .06, cx + w * .09, cy + h * .06], 8, fill=RED + (int(al * k),))
            d.text((cx, cy), "CHIUSO", font=f, fill=WHITE + (int(al * k),), anchor="mm")

class Bubble(El):
    """nuvoletta di pensiero con icona dentro"""
    def __init__(self, xy, r, t0, t1=None, inner=None, text=None):
        super().__init__(t0, t1, 0.25); self.xy, self.r, self.inner, self.text = xy, r, inner, text
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); x, y = self.xy; r = self.r * (back((t - self.t0) / 0.35) if t - self.t0 < 0.35 else 1); al = int(240 * a)
        d.ellipse([x - r * 1.3, y - r, x + r * 1.3, y + r], fill=(236, 230, 216, al))
        d.ellipse([x - r * 0.5, y + r * 1.0, x - r * 0.2, y + r * 1.3], fill=(236, 230, 216, al))
        d.ellipse([x - r * 0.8, y + r * 1.4, x - r * 0.62, y + r * 1.58], fill=(236, 230, 216, al))
        if self.inner: place(lay, icon(self.inner, int(r * 1.2)), (x, y - (r * .15 if self.text else 0)), "mm", a)
        if self.text: d.text((x, y + r * .55), self.text, font=font(OSW, int(r * .32), 600), fill=INK + (al,), anchor="mm")

def scene_cam(sc, *keys):
    """keys: (t, cx, cy, zoom)"""
    sc.cam = sorted(keys)
def cam_at(sc, t):
    ks = getattr(sc, "cam", None)
    if not ks: return None
    if t <= ks[0][0]: return ks[0][1:]
    for p, q in zip(ks, ks[1:]):
        if t <= q[0]:
            u = ease_io((t - p[0]) / max(1e-6, q[0] - p[0]))
            return tuple(lerp(p[i], q[i], u) for i in (1, 2, 3))
    return ks[-1][1:]
