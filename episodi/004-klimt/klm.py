# Elementi grafici del caso 004 (Klimt di Piacenza): sezione della galleria con lucernario e cortile,
# nicchia nel muro con l'edera, raggi X del doppio ritratto, icone del caso. Tutto stilizzato, NON le opere.
import math, random, os
from fi import *
import fi
from fx import *
from fx import draw_person

fi.PLACES.update({"Piacenza": (9.69, 45.05), "Vienna": (16.37, 48.21), "Venezia": (12.33, 45.44)})

BRICK = (128, 66, 48)
IVY = [(52, 96, 52), (70, 120, 60), (40, 80, 44), (88, 136, 70)]

def lady_pic(w, h, hat=False, xray=False, sepia=False):
    """ritratto stilizzato generico (sagoma), NON l'opera"""
    w, h = int(w), int(h)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    b = int(w * 0.07)
    if xray:
        d.rectangle([0, 0, w - 1, h - 1], fill=(30, 44, 58, 255))
        d.rectangle([b, b, w - b, h - b], fill=(58, 82, 104, 255))
        col = (200, 222, 236)
    elif sepia:
        d.rectangle([0, 0, w - 1, h - 1], fill=(236, 226, 204, 255))
        d.rectangle([b, b, w - b, h - b], fill=(176, 150, 112, 255))
        col = (92, 70, 48)
    else:
        d.rectangle([0, 0, w - 1, h - 1], fill=(150, 112, 52, 255))
        d.rectangle([b, b, w - b, h - b], fill=(56, 74, 60, 255))
        for k in range(14):
            rr = random.Random(k)
            x = rr.uniform(b, w - b); y = rr.uniform(b, h - b); r = rr.uniform(w * .02, w * .05)
            d.ellipse([x - r, y - r, x + r, y + r], fill=(84, 104, 76, 255))
        col = (226, 196, 170)
    iw = w - 2 * b; cx = w / 2; by = h - b
    sw = iw * 0.80
    silhouette(d, cx, by, sw, (120, 60, 50) if not (xray or sepia) else col)
    hr = sw * 0.20; hy = by - sw * 0.95
    if not (xray or sepia):
        d.ellipse([cx - hr * .8, hy + hr * .35, cx + hr * .8, hy + hr * 2.1], fill=col + (255,))
        d.chord([cx - hr * 1.05, hy - hr * .05, cx + hr * 1.05, hy + hr * 1.5], 180, 360, fill=(70, 40, 30, 255))
    if hat:
        hc = (220, 236, 246, 255) if xray else ((70, 52, 36, 255) if sepia else (60, 40, 30, 255))
        d.ellipse([cx - hr * 2.1, hy + hr * .05, cx + hr * 2.1, hy + hr * .55], fill=hc)
        d.rounded_rectangle([cx - hr * 1.05, hy - hr * .75, cx + hr * 1.05, hy + hr * .35], int(hr * .4), fill=hc)
        d.polygon([(cx - sw * .45, by - sw * .42), (cx + sw * .45, by - sw * .42), (cx + sw * .1, by - sw * .2), (cx - sw * .1, by - sw * .2)], fill=hc)
    d.rectangle([b - 3, b - 3, w - b + 2, h - b + 2], outline=(200, 170, 90, 255) if not (xray or sepia) else col + (255,), width=3)
    return im

_kc = {}
def kpic(name, size):
    k = (name, size)
    if k in _kc: return _kc[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); w = max(2, S // 22)
    if name == "sack":
        d.polygon([P(.30, .22), P(.70, .22), P(.86, .55), P(.80, .88), P(.20, .88), P(.14, .55)], fill=(22, 22, 24, 255))
        d.polygon([P(.36, .08), P(.64, .08), P(.58, .24), P(.42, .24)], fill=(30, 30, 34, 255))
        d.line([P(.38, .24), P(.62, .24)], fill=(90, 90, 96, 255), width=w)
        d.line([P(.32, .50), P(.60, .70)], fill=(60, 60, 66, 255), width=w // 2)
    elif name == "crate":
        d.rectangle([P(.08, .25), P(.92, .88)], fill=(150, 112, 66, 255), outline=(90, 64, 36, 255), width=w)
        for y in (.46, .67): d.line([P(.08, y), P(.92, y)], fill=(110, 80, 46, 255), width=w // 2)
        d.text(P(.5, .56), "FRAGILE", font=font(OSW, int(S * .15), 700), fill=(170, 40, 30, 255), anchor="mm")
    elif name == "leaf":
        d.polygon([P(.5, .05), P(.92, .45), P(.62, .5), P(.5, .95), P(.38, .5), P(.08, .45)], fill=IVY[1] + (255,))
        d.line([P(.5, .2), P(.5, .9)], fill=IVY[2] + (255,), width=w // 2)
    elif name == "xray":
        d.rounded_rectangle([P(.12, .12), P(.88, .88)], int(S * .06), fill=(40, 60, 80, 255), outline=(170, 210, 236, 255), width=w)
        for k in range(5): d.line([P(.2, .26 + k * .12), P(.8, .26 + k * .12)], fill=(120, 170, 210, 255), width=w // 2)
        d.ellipse([P(.38, .3), P(.62, .56)], outline=(220, 240, 250, 255), width=w)
    elif name == "dollar":
        d.ellipse([P(.08, .08), P(.92, .92)], fill=GOLD + (255,))
        d.text(P(.5, .52), "$", font=font(OSW, int(S * .6), 700), fill=INK + (255,), anchor="mm")
    elif name == "book":
        d.polygon([P(.06, .22), P(.5, .30), P(.94, .22), P(.94, .84), P(.5, .92), P(.06, .84)], fill=(236, 228, 208, 255))
        d.line([P(.5, .30), P(.5, .92)], fill=(150, 140, 120, 255), width=w)
        d.rectangle([P(.14, .36), P(.42, .70)], fill=(176, 150, 112, 255))
        for k in range(5): d.line([P(.58, .38 + k * .08), P(.86, .38 + k * .08)], fill=(150, 140, 120, 255), width=w // 2)
    elif name == "case":
        d.rectangle([P(.14, .10), P(.86, .80)], fill=(170, 210, 230, 70), outline=(210, 236, 246, 255), width=w)
        d.rectangle([P(.30, .22), P(.70, .66)], fill=(150, 112, 52, 255))
        d.rectangle([P(.34, .26), P(.66, .62)], fill=(56, 74, 60, 255))
        d.rectangle([P(.08, .80), P(.92, .90)], fill=(90, 80, 70, 255))
        d.line([P(.20, .16), P(.30, .40)], fill=(240, 250, 255, 200), width=w // 2)
    elif name == "fishing":
        d.line([P(.15, .9), P(.75, .1)], fill=(120, 90, 60, 255), width=w)
        d.line([P(.75, .1), P(.85, .55)], fill=(220, 220, 220, 255), width=max(1, w // 3))
        d.arc([P(.78, .52), P(.92, .70)], 0, 200, fill=(200, 200, 200, 255), width=w // 2)
    im = im.resize((size, size), Image.LANCZOS); _kc[k] = im
    return im

class KIcon(Icon):
    def __init__(self, name, xy, t0, t1=None, size=120, **k):
        super().__init__(kpic(name, size), xy, t0, t1, size=size, **k)


class Gallery(El):
    """SCENOGRAFIA: sezione della Galleria Ricci Oddi (schema non in scala): tetto con lucernario, sala con quadri,
    cortile con muro coperto d'edera. Tempi: hl (evidenzia), boxes (casse), lift (filo che solleva il quadro),
    gone (quadro sparito), roof_frame (cornice vuota sul tetto), niche (nicchia aperta nel muro), back (quadro in teca)"""
    def __init__(self, box, t0, t1=None, hl=None, boxes=None, lift=None, gone=None, roof_frame=None, niche=None, back=None,
                 question=None, title="SCHEMA SEMPLIFICATO · NON IN SCALA"):
        super().__init__(t0, t1, 0.4)
        self.box = box; self.hl, self.boxes, self.lift, self.gone = hl, boxes, lift, gone
        self.roof_frame, self.niche, self.back, self.question, self.title = roof_frame, niche, back, question, title
        x0, y0, x1, y1 = box; w = x1 - x0; h = y1 - y0
        self.bx1 = x0 + w * 0.70
        self.roof_y = y0 + h * 0.22
        self.floor_y = y1 - h * 0.05
        self.sky_x = x0 + w * 0.36
        self.pw = w * 0.085; self.ph = self.pw * 1.25
        self.pc = (self.sky_x, self.roof_y + (self.floor_y - self.roof_y) * 0.42)
        self.lady = lady_pic(self.pw, self.ph)
        rng = random.Random(4)
        self.wall = (x0 + w * 0.80, y0 + h * 0.30, x1, self.floor_y)
        wx0, wy0, wx1, wy1 = self.wall
        self.leaves = [(rng.uniform(wx0, wx1), rng.uniform(wy0, wy1), rng.uniform(10, 20) * w / 1500, rng.choice(IVY)) for _ in range(160)]
        self.nc = (wx0 + (wx1 - wx0) * 0.5, wy0 + (wy1 - wy0) * 0.62)
    def painting_pos(self, t):
        x, y = self.pc
        if self.lift is not None and t > self.lift + 1.0:
            u = ease_io(min(1.0, (t - self.lift - 1.0) / 1.8))
            y = lerp(y, self.roof_y - self.ph * 0.6, u)
        return x, y
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); al = int(255 * a); x0, y0, x1, y1 = self.box; w = x1 - x0; h = y1 - y0
        # cielo/ esterno
        d.rectangle([x0, self.roof_y + 6, self.bx1, self.floor_y], fill=(58, 36, 32, al))
        # quadri laterali
        for k, fx_ in enumerate((0.10, 0.22, 0.52, 0.62)):
            px = x0 + w * fx_; py = self.roof_y + (self.floor_y - self.roof_y) * (0.30 + 0.06 * (k % 2))
            pw, ph = w * 0.06, w * 0.075
            d.rectangle([px - pw / 2, py - ph / 2, px + pw / 2, py + ph / 2], fill=(120, 92, 50, al))
            d.rectangle([px - pw / 2 + 7, py - ph / 2 + 7, px + pw / 2 - 7, py + ph / 2 - 7], fill=((70, 86, 104), (96, 70, 56), (84, 96, 70), (104, 84, 60))[k] + (al,))
        # casse
        if self.boxes is not None and t > self.boxes:
            for k, bx in enumerate((0.08, 0.17, 0.55, 0.60)):
                kt = self.boxes + 0.15 * k
                if t < kt: continue
                s = int(w * 0.07); place(lay, kpic("crate", s), (x0 + w * bx, self.floor_y - s * 0.38 + 10 * (1 - ease((t - kt) / 0.3))), "mm", a)
        # quadro di Klimt
        gone = self.gone is not None and t > self.gone and (self.back is None or t < self.back)
        px, py = self.painting_pos(t)
        hx0, hy0 = self.pc[0] - self.pw / 2, self.pc[1] - self.ph / 2
        if gone or (self.lift is not None and t > self.lift + 1.0 and (self.back is None or t < self.back)):
            for hx, hy in ((hx0 + self.pw * .2, hy0 - 6), (hx0 + self.pw * .8, hy0 - 6)):
                d.ellipse([hx - 6, hy - 6, hx + 6, hy + 6], fill=(170, 165, 158, al))
            d.rectangle([hx0, hy0, hx0 + self.pw, hy0 + self.ph], outline=(110, 100, 90, al), width=2)
        if not gone:
            if self.back is not None and t > self.back:
                ka = a * ease((t - self.back) / 0.5)
                place(lay, self.lady, (self.pc[0] - self.pw / 2, self.pc[1] - self.ph / 2), "la", ka)
                d.rectangle([hx0 - 16, hy0 - 16, hx0 + self.pw + 16, hy0 + self.ph + 16], outline=(210, 236, 246, int(255 * ka)), width=4)
                d.line([(hx0 - 4, hy0 + 10), (hx0 + self.pw * 0.3, hy0 - 10)], fill=(240, 250, 255, int(200 * ka)), width=3)
            elif not (self.lift is not None and t > self.lift + 2.8):
                place(lay, self.lady, (px - self.pw / 2, py - self.ph / 2), "la", a)
        if self.hl is not None and t > self.hl and not gone and (self.lift is None or t < self.lift):
            p = 0.5 + 0.5 * math.sin((t - self.hl) * 5)
            d.rectangle([hx0 - 12, hy0 - 12, hx0 + self.pw + 12, hy0 + self.ph + 12], outline=GOLD + (int(al * (0.5 + 0.5 * p)),), width=5)
        # filo dal lucernario
        if self.lift is not None and self.lift < t < self.lift + 3.2:
            k = ease(min(1.0, (t - self.lift) / 0.9))
            ty = lerp(self.roof_y, py - self.ph / 2, k) if t < self.lift + 1.0 else py - self.ph / 2
            d.line([(self.sky_x, self.roof_y - 40), (self.sky_x, ty)], fill=(235, 235, 235, al), width=3)
            d.arc([self.sky_x - 10, ty - 4, self.sky_x + 10, ty + 16], 0, 200, fill=(235, 235, 235, al), width=3)
        # tetto e lucernario
        d.polygon([(x0 - 10, self.roof_y), (self.bx1 + 10, self.roof_y), (self.bx1 + 10, self.roof_y + 18), (x0 - 10, self.roof_y + 18)], fill=(96, 86, 76, al))
        sw = w * 0.07
        d.rectangle([self.sky_x - sw / 2, self.roof_y - 2, self.sky_x + sw / 2, self.roof_y + 20], fill=(30, 34, 40, al))
        op = self.lift is not None and t > self.lift - 0.6
        if op:
            d.line([(self.sky_x + sw / 2, self.roof_y), (self.sky_x + sw / 2 - sw * 0.6, self.roof_y - sw * 0.55)], fill=(170, 210, 230, al), width=7)
        else:
            d.line([(self.sky_x - sw / 2, self.roof_y + 2), (self.sky_x + sw / 2, self.roof_y + 2)], fill=(170, 210, 230, al), width=7)
        f = font(OSW, max(18, int(w * 0.017)), 500)
        d.text((self.sky_x, self.roof_y - sw * 0.7), "LUCERNARIO", font=f, fill=(170, 210, 230, al), anchor="ms")
        # pareti esterne
        d.rectangle([x0 - 10, self.roof_y, x0 + 6, self.floor_y], fill=(96, 86, 76, al))
        d.rectangle([self.bx1 - 6, self.roof_y, self.bx1 + 10, self.floor_y], fill=(96, 86, 76, al))
        d.rectangle([x0 - 30, self.floor_y, x1 + 10, self.floor_y + 14], fill=(90, 80, 70, al))
        d.text(((x0 + self.bx1) / 2, self.floor_y + 22), "GALLERIA RICCI ODDI · PIACENZA", font=f, fill=GREY + (al,), anchor="ma")
        # cornice vuota sul tetto
        if self.roof_frame is not None and t > self.roof_frame:
            ka = int(al * ease((t - self.roof_frame) / 0.3)); fxc = self.sky_x + w * 0.14
            fw, fh = self.pw * 1.1, self.pw * 0.32
            d.polygon([(fxc - fw / 2, self.roof_y), (fxc + fw / 2, self.roof_y), (fxc + fw / 2 - 14, self.roof_y - fh), (fxc - fw / 2 + 14, self.roof_y - fh)], outline=(200, 160, 80, ka), width=8)
            d.text((fxc, self.roof_y - fh - 14), "CORNICE VUOTA", font=f, fill=GOLD + (ka,), anchor="ms")
        # cortile e muro con edera
        wx0, wy0, wx1, wy1 = self.wall
        d.rectangle([wx0, wy0, wx1, wy1], fill=BRICK + (al,))
        for yy in range(int(wy0) + 14, int(wy1), 22): d.line([(wx0, yy), (wx1, yy)], fill=(104, 54, 40, al), width=2)
        nx, ny = self.nc; nw = (wx1 - wx0) * 0.34
        opened = self.niche is not None and t > self.niche
        if opened:
            k = ease((t - self.niche) / 0.6)
            d.rectangle([nx - nw / 2, ny - nw / 2, nx + nw / 2, ny + nw / 2], fill=(14, 12, 12, al))
            place(lay, kpic("sack", int(nw * 0.9)), (nx, ny + 4), "mm", a * k)
            d.rectangle([nx - nw / 2, ny - nw / 2, nx - nw / 2 + nw * (1 - 0.85 * k), ny + nw / 2], fill=(150, 150, 154, al), outline=(90, 90, 96, al), width=2)
        for lx, ly, lr, lc in self.leaves:
            if opened and math.dist((lx, ly), (nx, ny)) < nw * 1.1: continue
            d.ellipse([lx - lr, ly - lr * .7, lx + lr, ly + lr * .7], fill=lc + (al,))
        d.text(((wx0 + wx1) / 2, wy0 - 12), "CORTILE", font=f, fill=GREY + (al,), anchor="ms")
        if self.question is not None and t > self.question:
            ka = int(al * ease((t - self.question) / 0.3))
            d.text((nx, wy0 - 60), "?", font=font(SERIF, int(w * 0.06)), fill=GOLD + (ka,), anchor="ms")
        if self.title:
            d.text((x1, self.floor_y + 52), self.title, font=font(COURR, 18), fill=(150, 160, 170, al), anchor="rs")


class Niche(El):
    """primo piano del muro: l'edera viene tolta, appare lo sportello, si apre, dentro il sacco nero, poi la tela"""
    def __init__(self, box, t0, t1=None, clear=None, door=None, open_=None, sack=None, canvas=None, seed=6):
        super().__init__(t0, t1, 0.4)
        self.box, self.clear, self.door, self.open, self.sack, self.canvas = box, clear, door, open_, sack, canvas
        x0, y0, x1, y1 = box; rng = random.Random(seed)
        self.leaves = [(rng.uniform(x0 - 20, x1 + 20), rng.uniform(y0 - 20, y1 + 20), rng.uniform(20, 42), rng.uniform(0, 6.28), rng.choice(IVY), rng.random()) for _ in range(420)]
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); al = int(255 * a); x0, y0, x1, y1 = self.box
        w = x1 - x0; h = y1 - y0
        d.rectangle([x0, y0, x1, y1], fill=BRICK + (al,))
        for r, yy in enumerate(range(int(y0), int(y1), 46)):
            d.line([(x0, yy), (x1, yy)], fill=(98, 50, 36, al), width=4)
            for xx in range(int(x0) + (60 if r % 2 else 0), int(x1), 120): d.line([(xx, yy), (xx, min(y1, yy + 46))], fill=(98, 50, 36, al), width=4)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; dw = min(w, h) * 0.46
        if self.door is not None and t > self.door:
            k = ease((t - self.door) / 0.4); ka = int(al * k)
            d.rectangle([cx - dw / 2 - 8, cy - dw / 2 - 8, cx + dw / 2 + 8, cy + dw / 2 + 8], fill=(70, 66, 62, ka))
            d.rectangle([cx - dw / 2, cy - dw / 2, cx + dw / 2, cy + dw / 2], fill=(10, 9, 9, ka))
            if self.sack is not None and t > self.sack:
                place(lay, kpic("sack", int(dw * 0.95)), (cx, cy + 6), "mm", a * ease((t - self.sack) / 0.3))
            ok = ease((t - self.open) / 0.6) if (self.open is not None and t > self.open) else 0
            pw = dw * (1 - 0.88 * ok)
            d.rectangle([cx - dw / 2, cy - dw / 2, cx - dw / 2 + pw, cy + dw / 2], fill=(150, 152, 156, ka), outline=(96, 98, 104, ka), width=4)
            for rx in (0.12, 0.88):
                for ry in (0.12, 0.88):
                    d.ellipse([cx - dw / 2 + pw * rx - 5, cy - dw / 2 + dw * ry - 5, cx - dw / 2 + pw * rx + 5, cy - dw / 2 + dw * ry + 5], fill=(96, 98, 104, ka))
        for lx, ly, lr, ang, lc, rnd in self.leaves:
            la = al
            if self.clear is not None and t > self.clear:
                dd = math.dist((lx, ly), (cx, cy)) / max(w, h)
                tt = self.clear + rnd * 0.6 + dd * 1.2
                if t > tt:
                    u = ease((t - tt) / 0.4); la = int(al * (1 - u))
                    lx += (lx - cx) * 0.3 * u; ly += 80 * u
                if la <= 0: continue
            pts = [(lx + math.cos(ang + q * 2.1) * lr, ly + math.sin(ang + q * 2.1) * lr * 0.8) for q in range(3)]
            d.polygon(pts, fill=lc + (la,))
        if self.canvas is not None and t > self.canvas:
            k = t - self.canvas; s = back(k / 0.4) if k < 0.4 else 1
            pw = dw * 0.9 * s
            if pw > 4:
                im = lady_pic(pw, pw * 1.25)
                place(lay, im, (cx + dw * 0.9, cy - dw * 0.2 - 30 * ease(k / 0.5)), "mm", a)


class XRay(El):
    """ritratto stilizzato con barra di scansione: sotto compare un secondo ritratto (con cappello)"""
    def __init__(self, xy, w, h, t0, t1=None, scan=None, dur=2.2, label=True):
        super().__init__(t0, t1, 0.35)
        self.xy, self.w, self.h, self.scan, self.dur, self.label = xy, int(w), int(h), scan, dur, label
        self.top = lady_pic(w, h); self.xr = lady_pic(w, h, hat=True, xray=True)
    def draw(self, lay, t, a):
        cx, cy = self.xy; x0, y0 = cx - self.w / 2, cy - self.h / 2
        place(lay, self.top, (x0, y0), "la", a)
        if self.scan is not None and t > self.scan:
            u = ease_io(min(1.0, (t - self.scan) / self.dur)); cw = int(self.w * u)
            if cw > 1:
                place(lay, self.xr.crop((0, 0, cw, self.h)), (x0, y0), "la", a)
            d = ImageDraw.Draw(lay); al = int(255 * a)
            if u < 1:
                d.rectangle([x0 + cw - 4, y0 - 20, x0 + cw + 4, y0 + self.h + 20], fill=(150, 220, 255, al))
            if self.label and u >= 1:
                d.text((cx, y0 + self.h + 30), "RAGGI X · ricostruzione grafica", font=font(COURR, 24), fill=(150, 200, 230, al), anchor="ma")


class Compare(El):
    """due ritratti stilizzati: a sinistra quello di Piacenza, a destra quello 'del libro' (seppia); si sovrappongono"""
    def __init__(self, xy, w, h, t0, t1=None, b_t=None, merge=None, labels=("PIACENZA", "IL RITRATTO PERDUTO")):
        super().__init__(t0, t1, 0.35)
        self.xy, self.w, self.h, self.b_t, self.merge, self.labels = xy, int(w), int(h), b_t, merge, labels
        self.A = lady_pic(w, h); self.B = lady_pic(w, h, hat=True, sepia=True)
    def draw(self, lay, t, a):
        cx, cy = self.xy; gap = self.w * 0.75
        u = ease_io(min(1.0, (t - self.merge) / 1.2)) if (self.merge is not None and t > self.merge) else 0
        ax = cx - gap * (1 - u); bx = cx + gap * (1 - u)
        d = ImageDraw.Draw(lay); al = int(255 * a); f = font(OSW, 32, 600)
        place(lay, self.A, (ax, cy), "mm", a)
        if u < 0.5: d.text((ax, cy + self.h / 2 + 24), self.labels[0], font=f, fill=WHITE + (int(al * (1 - u * 2)),), anchor="ma")
        if self.b_t is not None and t > self.b_t:
            kb = ease((t - self.b_t) / 0.4)
            place(lay, self.B, (bx, cy), "mm", a * kb * (1 - 0.5 * u))
            if u < 0.5: d.text((bx, cy + self.h / 2 + 24), self.labels[1], font=f, fill=GOLD + (int(al * kb * (1 - u * 2)),), anchor="ma")
        if u >= 1:
            d.text((cx, cy + self.h / 2 + 24), "STESSA POSA", font=f, fill=GOLD + (al,), anchor="ma")


def thumb_lady(w):
    return lady_pic(w, w * 1.25)
