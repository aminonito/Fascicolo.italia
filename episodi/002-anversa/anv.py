# Elementi grafici del caso 002 (colpo di Anversa): caveau, porta blindata, cassette, sensori, icone.
import math, random
from fi import *
import fi
from fx import *

_ai = {}
def aic(name, size, color=None):
    """icone extra del caso"""
    k = (name, size)
    if k in _ai: return _ai[k]
    S = size * 3; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda a, b: (a * S, b * S); w = max(2, S // 22)
    g = GOLD + (255,); st = (170, 176, 184, 255); dk = (60, 64, 70, 255)
    if name == "diamond":
        top = [P(.12, .36), P(.30, .14), P(.70, .14), P(.88, .36)]
        d.polygon(top + [P(.5, .92)], fill=(200, 230, 245, 255))
        d.polygon([P(.12, .36), P(.88, .36), P(.5, .92)], fill=(150, 200, 228, 255))
        d.polygon([P(.30, .14), P(.5, .36), P(.70, .14)], fill=(230, 246, 255, 255))
        for a_, b_ in ((P(.30, .14), P(.38, .36)), (P(.70, .14), P(.62, .36)), (P(.38, .36), P(.5, .92)), (P(.62, .36), P(.5, .92))):
            d.line([a_, b_], fill=(110, 160, 190, 255), width=w // 2)
        d.line(top + [P(.5, .92), P(.12, .36)], fill=(240, 250, 255, 255), width=w // 2)
    elif name == "gold":
        for k, (x, y) in enumerate(((.1, .55), (.5, .55), (.3, .3))):
            d.polygon([P(x, y + .3), P(x + .4, y + .3), P(x + .34, y + .08), P(x + .06, y + .08)], fill=(230, 186, 70, 255), outline=(150, 110, 30, 255))
    elif name == "spray":
        d.rounded_rectangle([P(.32, .30), P(.68, .96)], S // 14, fill=(190, 60, 120, 255))
        d.rectangle([P(.38, .16), P(.62, .32)], fill=(220, 220, 228, 255)); d.rectangle([P(.46, .08), P(.60, .16)], fill=(240, 240, 240, 255))
        d.text(P(.5, .62), "LACCA", font=font(OSW, S // 9, 700), fill=(255, 255, 255, 255), anchor="mm")
    elif name == "sandwich":
        d.chord([P(.06, .20), P(.94, .70)], 180, 360, fill=(214, 160, 90, 255))
        d.rectangle([P(.08, .45), P(.92, .52)], fill=(120, 170, 70, 255))
        for k in range(4): d.ellipse([P(.12 + k * .2, .47), P(.30 + k * .2, .62)], fill=(190, 70, 70, 255), outline=(240, 220, 210, 255), width=w // 2)
        d.rectangle([P(.08, .60), P(.92, .72)], fill=(222, 170, 100, 255))
        d.pieslice([P(.70, .18), P(1.06, .80)], 120, 240, fill=(0, 0, 0, 0))  # morso
        d.ellipse([P(.74, .26), P(1.02, .72)], fill=(0, 0, 0, 0))
    elif name == "trashbag":
        d.polygon([P(.2, .32), P(.8, .32), P(.92, .82), P(.5, .96), P(.08, .82)], fill=(36, 38, 40, 255))
        d.ellipse([P(.08, .40), P(.92, .96)], fill=(40, 42, 46, 255))
        d.polygon([P(.38, .34), P(.5, .10), P(.62, .34)], fill=(46, 48, 52, 255)); d.rectangle([P(.40, .30), P(.60, .36)], fill=g)
        d.arc([P(.22, .50), P(.6, .9)], 200, 300, fill=(90, 92, 98, 255), width=w)
    elif name == "key":
        d.ellipse([P(.04, .34), P(.30, .66)], outline=g, width=S // 14)
        d.rectangle([P(.28, .46), P(.96, .54)], fill=g)
        for x in (.62, .74, .86): d.rectangle([P(x, .54), P(x + .06, .68)], fill=g)
    elif name == "extinguisher":
        d.rounded_rectangle([P(.30, .26), P(.70, .96)], S // 8, fill=RED + (255,))
        d.rectangle([P(.42, .12), P(.58, .26)], fill=dk); d.line([P(.58, .16), P(.84, .30), P(.84, .60)], fill=dk, width=w)
        d.rectangle([P(.36, .50), P(.64, .70)], fill=(240, 230, 210, 255))
    elif name == "tape":
        d.ellipse([P(.1, .1), P(.9, .9)], fill=(200, 196, 184, 255)); d.ellipse([P(.32, .32), P(.68, .68)], fill=(0, 0, 0, 0))
        d.ellipse([P(.32, .32), P(.68, .68)], outline=(150, 140, 126, 255), width=w)
        d.polygon([P(.86, .52), P(1.0, .56), P(1.0, .72), P(.82, .66)], fill=(210, 206, 194, 255))
    elif name == "foil":
        d.polygon([P(.08, .2), P(.92, .12), P(.88, .86), P(.12, .9)], fill=(200, 206, 214, 255), outline=(240, 244, 248, 255))
        for k in range(4): d.line([P(.2 + k * .18, .2), P(.14 + k * .2, .84)], fill=(160, 166, 176, 255), width=w // 2)
    elif name == "shield":
        d.rounded_rectangle([P(.14, .06), P(.86, .94)], S // 14, fill=(220, 226, 236, 150), outline=(240, 244, 250, 255), width=w)
        for k in range(3): d.line([P(.24 + k * .2, .16), P(.40 + k * .2, .36)], fill=(255, 255, 255, 200), width=w)
    elif name == "car":
        d.rounded_rectangle([P(.04, .44), P(.96, .74)], S // 14, fill=(80, 90, 104, 255))
        d.polygon([P(.22, .46), P(.32, .24), P(.70, .24), P(.80, .46)], fill=(70, 80, 94, 255))
        d.polygon([P(.30, .44), P(.36, .30), P(.50, .30), P(.50, .44)], fill=(160, 190, 210, 255)); d.polygon([P(.54, .44), P(.54, .30), P(.66, .30), P(.72, .44)], fill=(160, 190, 210, 255))
        for x in (.24, .76): d.ellipse([P(x - .1, .62), P(x + .1, .84)], fill=(26, 26, 28, 255))
        d.rectangle([P(.88, .50), P(.96, .56)], fill=(250, 230, 150, 255))
    elif name == "tree":
        d.rectangle([P(.45, .62), P(.55, .96)], fill=(90, 64, 42, 255))
        d.polygon([P(.5, .04), P(.86, .50), P(.14, .50)], fill=(46, 84, 56, 255)); d.polygon([P(.5, .24), P(.92, .72), P(.08, .72)], fill=(40, 74, 50, 255))
    elif name == "bag":
        d.rounded_rectangle([P(.06, .36), P(.94, .88)], S // 10, fill=(40, 40, 46, 255)); d.arc([P(.30, .14), P(.70, .56)], 180, 360, fill=(30, 30, 34, 255), width=S // 16)
        d.line([P(.10, .52), P(.90, .52)], fill=(90, 90, 96, 255), width=w // 2)
    elif name == "sensor":
        d.chord([P(.18, .30), P(.82, .94)], 180, 360, fill=(220, 220, 224, 255)); d.rectangle([P(.14, .58), P(.86, .66)], fill=(160, 160, 166, 255))
        d.ellipse([P(.42, .40), P(.58, .56)], fill=(200, 40, 40, 255))
    elif name == "radar":
        d.pieslice([P(.06, .06), P(.94, .94)], 200, 340, fill=(60, 120, 90, 255)); d.ellipse([P(.42, .42), P(.58, .58)], fill=(120, 220, 160, 255))
        for r in (.18, .3, .42): d.arc([P(.5 - r, .5 - r), P(.5 + r, .5 + r)], 200, 340, fill=(120, 220, 160, 255), width=w // 2)
    elif name == "magnet":
        d.arc([P(.14, .10), P(.86, .82)], 180, 360, fill=RED + (255,), width=S // 7)
        d.rectangle([P(.14, .44), P(.28, .80)], fill=RED + (255,)); d.rectangle([P(.72, .44), P(.86, .80)], fill=RED + (255,))
        d.rectangle([P(.14, .80), P(.28, .92)], fill=st); d.rectangle([P(.72, .80), P(.86, .92)], fill=st)
    elif name == "bulb":
        d.ellipse([P(.22, .06), P(.78, .62)], fill=(250, 226, 120, 255)); d.rectangle([P(.38, .58), P(.62, .80)], fill=(170, 170, 176, 255))
        for y in (.64, .70, .76): d.line([P(.38, y), P(.62, y)], fill=(110, 110, 116, 255), width=w // 2)
    elif name == "seismo":
        pts = [P(.04 + k * .046, .5 + (0.32 if k % 2 else -0.32) * math.sin(k / 3) ) for k in range(21)]
        d.line(pts, fill=(120, 220, 160, 255), width=w)
    elif name == "dial":
        d.ellipse([P(.06, .06), P(.94, .94)], fill=(150, 156, 164, 255), outline=(220, 224, 230, 255), width=w)
        d.ellipse([P(.30, .30), P(.70, .70)], fill=(90, 94, 100, 255))
        for k in range(20):
            a_ = k / 20 * 2 * math.pi; d.line([P(.5 + .36 * math.cos(a_), .5 + .36 * math.sin(a_)), P(.5 + .43 * math.cos(a_), .5 + .43 * math.sin(a_))], fill=(40, 40, 44, 255), width=w // 2)
    elif name == "videotape":
        d.rectangle([P(.06, .26), P(.94, .74)], fill=(30, 30, 34, 255)); d.ellipse([P(.18, .36), P(.40, .58)], fill=(200, 200, 200, 255)); d.ellipse([P(.60, .36), P(.82, .58)], fill=(200, 200, 200, 255))
        d.rectangle([P(.34, .62), P(.66, .72)], fill=(240, 236, 220, 255))
    elif name == "plane":
        d.polygon([P(.04, .5), P(.86, .44), P(.98, .5), P(.86, .56)], fill=(220, 224, 230, 255))
        d.polygon([P(.40, .46), P(.56, .10), P(.64, .10), P(.58, .46)], fill=(200, 204, 210, 255)); d.polygon([P(.40, .54), P(.56, .90), P(.64, .90), P(.58, .54)], fill=(200, 204, 210, 255))
        d.polygon([P(.08, .48), P(.14, .30), P(.20, .30), P(.18, .48)], fill=(200, 204, 210, 255))
    elif name == "card":
        d.rectangle([P(.06, .24), P(.94, .76)], fill=(240, 236, 222, 255), outline=(140, 130, 116, 255), width=w // 2)
        d.line([P(.14, .40), P(.62, .40)], fill=INK + (255,), width=w); d.line([P(.14, .54), P(.80, .54)], fill=(120, 112, 102, 255), width=w // 2); d.line([P(.14, .64), P(.70, .64)], fill=(120, 112, 102, 255), width=w // 2)
    elif name == "tv":
        d.rounded_rectangle([P(.06, .16), P(.94, .80)], S // 16, fill=(40, 40, 44, 255)); d.rectangle([P(.12, .22), P(.88, .72)], fill=(120, 30, 30, 255))
        d.polygon([P(.42, .36), P(.42, .60), P(.62, .48)], fill=(255, 255, 255, 255)); d.rectangle([P(.36, .82), P(.64, .88)], fill=(60, 60, 64, 255))
    elif name == "dna":
        for k in range(26):
            u = k / 25; y = .06 + u * .88; ph = u * math.pi * 3
            xa, xb = .5 + .3 * math.sin(ph), .5 - .3 * math.sin(ph)
            if k % 2 == 0: d.line([P(xa, y), P(xb, y)], fill=(150, 160, 170, 255), width=w // 2)
            d.ellipse([P(xa - .04, y - .02), P(xa + .04, y + .02)], fill=(120, 200, 230, 255)); d.ellipse([P(xb - .04, y - .02), P(xb + .04, y + .02)], fill=RED + (255,))
    elif name == "question":
        d.text(P(.5, .5), "?", font=font(SERIF, int(S * .9)), fill=g, anchor="mm")
    elif name == "book":
        d.rectangle([P(.16, .08), P(.84, .92)], fill=(140, 50, 40, 255)); d.rectangle([P(.16, .08), P(.24, .92)], fill=(100, 34, 28, 255))
        d.rectangle([P(.34, .24), P(.74, .34)], fill=g)
    im = im.resize((size, size), Image.LANCZOS); _ai[k] = im
    return im

class AIcon(Icon):
    def __init__(self, name, xy, t0, t1=None, size=120, **k):
        super().__init__(aic(name, size), xy, t0, t1, size=size, **k)

# ---------------------------------------------------------------- spezzone di palazzo (sezione)
class Cutaway(El):
    """sezione del palazzo: piani sopra la strada, due piani interrati, caveau a -2.
    hl: [(t, 'office'|'vault'|None)], path_t: percorso rosso ufficio -> caveau"""
    def __init__(self, box, t0, t1=None, hl=(), path_t=None, label="ANTWERP DIAMOND CENTER", lights_off=None):
        super().__init__(t0, t1, 0.4); self.box, self.hl, self.path_t, self.label, self.lights_off = box, list(hl), path_t, label, lights_off
    def geo(self):
        x0, y0, x1, y1 = self.box; w = x1 - x0; h = y1 - y0
        gy = y0 + h * 0.58
        return x0, y0, x1, y1, w, h, gy
    def office(self):
        x0, y0, x1, y1, w, h, gy = self.geo(); fh = (gy - y0 - h * 0.06) / 4
        return (x0 + w * 0.62, gy - fh * 3 + fh * 0.18, x0 + w * 0.80, gy - fh * 2 - fh * 0.12)
    def vault(self):
        x0, y0, x1, y1, w, h, gy = self.geo(); bh = (y1 - gy) / 2
        return (x0 + w * 0.22, gy + bh + 10, x0 + w * 0.78, y1 - 8)
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); al = int(255 * a); x0, y0, x1, y1, w, h, gy = self.geo()
        # cielo/notte e terreno
        d.rectangle([x0 - 60, gy, x1 + 60, y1 + 10], fill=(48, 40, 34, int(al * 0.95)))
        for k in range(40):
            rx = x0 - 50 + (k * 97) % (w + 100); ry = gy + 12 + (k * 53) % int(y1 - gy)
            d.ellipse([rx, ry, rx + 6, ry + 4], fill=(70, 60, 50, al))
        d.line([(x0 - 60, gy), (x1 + 60, gy)], fill=(150, 140, 126, al), width=4)
        d.text((x0 - 40, gy - 12), "STRADA", font=font(COURR, 22), fill=GREY + (al,), anchor="ls")
        # palazzo sopra
        bx0, bx1 = x0 + w * 0.16, x0 + w * 0.84; top = y0 + h * 0.06
        d.rectangle([bx0, top, bx1, gy], fill=(84, 88, 94, al), outline=(130, 136, 144, al), width=3)
        fh = (gy - top) / 4
        lit = not (self.lights_off and t > self.lights_off)
        for f in range(4):
            fy = top + f * fh
            d.line([(bx0, fy), (bx1, fy)], fill=(110, 116, 124, al), width=2)
            for c in range(7):
                wx = bx0 + 20 + c * (bx1 - bx0 - 40) / 7
                on = lit and ((f * 7 + c) % 3 != 0)
                d.rectangle([wx + 6, fy + fh * 0.25, wx + (bx1 - bx0 - 40) / 7 - 10, fy + fh * 0.75], fill=((230, 200, 120) if on else (44, 50, 58)) + (al,))
        d.text(((bx0 + bx1) / 2, top - 14), self.label, font=font(OSW, int(h * 0.05), 600), fill=WHITE + (al,), anchor="ms")
        # interrati
        bh = (y1 - gy) / 2
        for k in range(2):
            ly0 = gy + k * bh
            d.rectangle([bx0, ly0 + 6, bx1, ly0 + bh - 4], fill=(30, 32, 36, al), outline=(90, 96, 104, al), width=3)
            d.text((bx0 + 14, ly0 + bh / 2), f"-{k + 1}", font=font(OSW, int(h * 0.05), 600), fill=GREY + (al,), anchor="lm")
        vx0, vy0, vx1, vy1 = self.vault()
        d.rectangle([vx0, vy0, vx1, vy1], fill=(58, 60, 66, al), outline=(190, 196, 204, al), width=5)
        n = 12
        for c in range(n):
            for r in range(3):
                cx0 = vx0 + 70 + c * (vx1 - vx0 - 90) / n; cy0 = vy0 + 10 + r * (vy1 - vy0 - 20) / 3
                d.rectangle([cx0, cy0, cx0 + (vx1 - vx0 - 90) / n - 4, cy0 + (vy1 - vy0 - 20) / 3 - 4], fill=(120, 126, 134, al), outline=(80, 84, 90, al))
        dr = (vy1 - vy0) * 0.42; dcx, dcy = vx0 + 34, (vy0 + vy1) / 2
        d.ellipse([dcx - dr, dcy - dr, dcx + dr, dcy + dr], fill=(150, 156, 164, al), outline=(220, 224, 230, al), width=3)
        d.text(((vx0 + vx1) / 2, vy1 + 8), "CAVEAU", font=font(OSW, int(h * 0.04), 600), fill=GOLD + (al,), anchor="ma")
        cur = None
        for tt, which in self.hl:
            if t >= tt: cur = (tt, which)
        if cur and cur[1]:
            p = 0.5 + 0.5 * math.sin((t - cur[0]) * 5)
            r = self.vault() if cur[1] == "vault" else self.office()
            d.rectangle([r[0] - 10, r[1] - 10, r[2] + 10, r[3] + 10], outline=GOLD + (int(al * (0.5 + 0.5 * p)),), width=6)
        if self.path_t is not None and t > self.path_t:
            o = self.office(); v = self.vault()
            pts = [((o[0] + o[2]) / 2, o[3]), (bx0 + 40, o[3]), (bx0 + 40, gy + bh * 1.5), (v[0] + 34, gy + bh * 1.5)]
            L = [0.0]
            for p_, q_ in zip(pts, pts[1:]): L.append(L[-1] + math.dist(p_, q_))
            f = ease_io((t - self.path_t) / 2.0) * L[-1]
            last = pts[0]
            for j in range(1, len(pts)):
                if L[j - 1] >= f: break
                u = min(1.0, (f - L[j - 1]) / max(1e-6, L[j] - L[j - 1]))
                q = (pts[j - 1][0] + (pts[j][0] - pts[j - 1][0]) * u, pts[j - 1][1] + (pts[j][1] - pts[j - 1][1]) * u)
                seg = math.dist(pts[j - 1], q); nn = max(1, int(seg / 9))
                for i in range(nn):
                    if i % 2 == 0:
                        a0, a1 = i / nn, (i + 1) / nn
                        d.line([(pts[j - 1][0] + (q[0] - pts[j - 1][0]) * a0, pts[j - 1][1] + (q[1] - pts[j - 1][1]) * a0),
                                (pts[j - 1][0] + (q[0] - pts[j - 1][0]) * a1, pts[j - 1][1] + (q[1] - pts[j - 1][1]) * a1)], fill=RED + (al,), width=6)
                last = q
            d.ellipse([last[0] - 13, last[1] - 13, last[0] + 13, last[1] + 13], fill=REDL + (al,), outline=WHITE + (al,), width=3)

# ---------------------------------------------------------------- porta blindata rotonda
class VaultDoor(El):
    def __init__(self, xy, r, t0, t1=None, dial_t=None, dial_d=2.0, open_t=None, plates_t=None, foil_t=None, label=None):
        super().__init__(t0, t1, 0.3); self.xy, self.r = xy, r
        self.dial_t, self.dial_d, self.open_t, self.plates_t, self.foil_t, self.label = dial_t, dial_d, open_t, plates_t, foil_t, label
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); x, y = self.xy; r = self.r; al = int(255 * a)
        d.rectangle([x - r * 1.25, y - r * 1.25, x + r * 1.25, y + r * 1.25], fill=(70, 74, 80, al), outline=(120, 126, 134, al), width=4)
        d.ellipse([x - r * 1.04, y - r * 1.04, x + r * 1.04, y + r * 1.04], fill=(12, 12, 14, al))
        o = ease((t - self.open_t) / 1.0) if self.open_t is not None and t > self.open_t else 0
        if o > 0:  # interno: cassette che si intravedono
            for c in range(4):
                for rr in range(4):
                    bx = x - r * 0.7 + c * r * 0.36; by = y - r * 0.7 + rr * r * 0.36
                    d.rectangle([bx, by, bx + r * 0.32, by + r * 0.32], fill=(110, 116, 124, int(al * o)), outline=(70, 74, 80, int(al * o)))
        sw = 1 - 0.82 * o  # la porta ruota: si stringe verso destra
        dx = x + r * (1 - sw) * 1.0
        d.ellipse([dx - r * sw, y - r, dx + r * sw, y + r], fill=(160, 166, 174, al), outline=(220, 226, 232, al), width=5)
        d.ellipse([dx - r * 0.86 * sw, y - r * 0.86, dx + r * 0.86 * sw, y + r * 0.86], outline=(120, 126, 134, al), width=3)
        if sw > 0.4:
            ang = 0.0
            if self.dial_t is not None and t > self.dial_t:
                u = min(1.0, (t - self.dial_t) / self.dial_d); ang = math.sin(u * math.pi * 3) * 2.4 + u * 1.2
            dr = r * 0.26 * sw
            d.ellipse([dx - dr, y - dr, dx + dr, y + dr], fill=(110, 116, 124, al), outline=(230, 234, 240, al), width=3)
            for k in range(12):
                aa = ang + k * math.pi / 6
                d.line([(dx + dr * 0.7 * math.cos(aa) * 1, y + dr * 0.7 * math.sin(aa)), (dx + dr * math.cos(aa), y + dr * math.sin(aa))], fill=(30, 30, 34, al), width=3)
            d.line([(dx, y), (dx + dr * 0.6 * math.cos(ang - math.pi / 2), y + dr * 0.6 * math.sin(ang - math.pi / 2))], fill=RED + (al,), width=5)
            for k in range(6):  # bulloni
                aa = k * math.pi / 3
                bx, by = dx + r * 0.62 * sw * math.cos(aa), y + r * 0.62 * math.sin(aa)
                d.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(200, 204, 210, al))
        if self.plates_t is not None and t > self.plates_t:
            pa = int(al * ease((t - self.plates_t) / 0.3))
            px = x + r * 1.06; py = y - r * 0.2
            d.rectangle([px - 22, py - 50, px - 4, py + 50], fill=(200, 60, 50, pa))
            d.rectangle([px + 4, py - 50, px + 22, py + 50], fill=(200, 60, 50, pa))
            if not (self.foil_t and t > self.foil_t):
                for k in range(3):
                    rr = 30 + 18 * ((t * 1.5 + k / 3) % 1)
                    d.arc([px - rr, py - rr * 1.6, px + rr, py + rr * 1.6], -60, 60, fill=(240, 120, 110, int(pa * 0.6)), width=3)
            if self.foil_t and t > self.foil_t:
                fa = ease((t - self.foil_t) / 0.4)
                d.rectangle([px - 30, py - 60, px + 30, py + 60], fill=(205, 210, 218, int(pa * fa)), outline=(245, 248, 252, int(pa * fa)), width=3)
                for k in range(3): d.line([(px - 22 + k * 20, py - 50), (px - 30 + k * 22, py + 50)], fill=(160, 166, 176, int(pa * fa)), width=2)
        if self.label: d.text((x, y + r * 1.25 + 40), self.label, font=font(OSW, 34, 600), fill=GOLD + (al,), anchor="mm")

# ---------------------------------------------------------------- muro di cassette
class Boxes(El):
    """griglia di cassette; open_t0..: si aprono in ordine casuale con ritmo rate (al secondo) fino a n_open"""
    def __init__(self, box, cols, rows, t0, t1=None, open_t=None, n_open=0, rate=8.0, seed=4, counter=None, hl=None):
        super().__init__(t0, t1, 0.4); self.box, self.cols, self.rows, self.open_t, self.n_open, self.rate = box, cols, rows, open_t, n_open, rate
        rng = random.Random(seed); idx = list(range(cols * rows)); rng.shuffle(idx); self.order = idx; self.counter, self.hl = counter, hl
    def cell(self, i):
        x0, y0, x1, y1 = self.box; cw = (x1 - x0) / self.cols; ch = (y1 - y0) / self.rows
        r, c = divmod(i, self.cols); return x0 + c * cw, y0 + r * ch, cw, ch
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); al = int(255 * a); x0, y0, x1, y1 = self.box
        d.rectangle([x0 - 16, y0 - 16, x1 + 16, y1 + 16], fill=(48, 50, 56, al), outline=(150, 156, 164, al), width=4)
        opened = {}
        if self.open_t is not None and t > self.open_t:
            k = min(self.n_open, int((t - self.open_t) * self.rate))
            for j in range(k): opened[self.order[j]] = self.open_t + j / self.rate
        for i in range(self.cols * self.rows):
            bx, by, cw, ch = self.cell(i)
            if i in opened:
                u = ease((t - opened[i]) / 0.3)
                d.rectangle([bx + 4, by + 4, bx + cw - 4, by + ch - 4], fill=(14, 14, 16, al))
                ow = (cw - 8) * (1 - 0.75 * u)
                d.polygon([(bx + 4, by + 4), (bx + 4 + ow, by + 4 - 6 * u), (bx + 4 + ow, by + ch - 4 + 6 * u), (bx + 4, by + ch - 4)], fill=(150, 156, 166, al), outline=(90, 94, 100, al))
            else:
                d.rectangle([bx + 4, by + 4, bx + cw - 4, by + ch - 4], fill=(132, 138, 148, al), outline=(84, 88, 96, al), width=2)
                d.ellipse([bx + cw * 0.75 - 6, by + ch / 2 - 6, bx + cw * 0.75 + 6, by + ch / 2 + 6], fill=GOLD + (al,))
                d.text((bx + 10, by + 8), f"{i + 1:03d}", font=font(COURR, max(12, int(ch * 0.18))), fill=(60, 62, 68, al))
        if self.hl is not None and t > self.hl[0]:
            bx, by, cw, ch = self.cell(self.hl[1]); p = 0.5 + 0.5 * math.sin((t - self.hl[0]) * 5)
            d.rectangle([bx - 2, by - 2, bx + cw + 2, by + ch + 2], outline=GOLD + (int(al * (0.5 + 0.5 * p)),), width=6)
        if self.counter and self.open_t is not None and t > self.open_t:
            k = min(self.n_open, int((t - self.open_t) * self.rate))
            cx, cy = self.counter
            d.rounded_rectangle([cx - 150, cy - 46, cx + 150, cy + 46], 12, fill=(14, 12, 11, int(al * 0.85)))
            d.text((cx, cy), f"{k} APERTE", font=font(OSW, 54, 700), fill=GOLD + (al,), anchor="mm")

# ---------------------------------------------------------------- sensore con onde
class Sensor(El):
    def __init__(self, name, xy, t0, t1=None, size=150, off_t=None, label=None, waves=True):
        super().__init__(t0, t1, 0.25); self.im = aic(name, size); self.xy, self.size, self.off_t, self.label, self.waves = xy, size, off_t, label, waves
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); x, y = self.xy; al = int(255 * a); k = t - self.t0
        off = self.off_t is not None and t > self.off_t
        im = self.im
        if k < 0.35:
            s = back(k / 0.35)
            if s > 0.02: im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
        if self.waves and not off:
            for j in range(3):
                rr = self.size * (0.55 + 0.5 * ((t * 0.9 + j / 3) % 1))
                fa = 1 - ((t * 0.9 + j / 3) % 1)
                d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=(120, 220, 160, int(al * 0.6 * fa)), width=4)
        place(lay, im if not off else set_alpha(im.convert("LA").convert("RGBA"), 0.55), (x, y), "mm", a)
        if off:
            u = ease((t - self.off_t) / 0.3); r = self.size * 0.5
            d.line([(x - r * u, y - r * u), (x + r * u, y + r * u)], fill=RED + (al,), width=10)
            d.line([(x - r * u, y + r * u), (x + r * u, y - r * u)], fill=RED + (al,), width=10)
        if self.label:
            f = font(OSW, 30, 600); tw = tl(d, self.label, f); ly = y + self.size / 2 + 34
            d.rounded_rectangle([x - tw / 2 - 12, ly - 22, x + tw / 2 + 12, ly + 22], 10, fill=(14, 12, 11, int(210 * a)))
            d.text((x, ly), self.label, font=f, fill=WHITE + (al,), anchor="mm")

# ---------------------------------------------------------------- nuvola di spruzzo
class Spray(El):
    def __init__(self, p0, p1, t0, dur=1.2, t1=None, color=(240, 230, 250)):
        super().__init__(t0, t1, 0.1); self.p0, self.p1, self.dur, self.color = p0, p1, dur, color
        rng = random.Random(7); self.parts = [(rng.random(), rng.uniform(-1, 1), rng.uniform(4, 12)) for _ in range(90)]
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); k = t - self.t0
        if k > self.dur + 0.8: return
        (x0, y0), (x1, y1) = self.p0, self.p1; L = math.dist(self.p0, self.p1); nx, ny = -(y1 - y0) / L, (x1 - x0) / L
        for ph, side, r in self.parts:
            u = ((k * 1.6 + ph) % 1.0) if k < self.dur else min(1.0, ph + (k - self.dur))
            fade = (1 - u) * (1 if k < self.dur else max(0, 1 - (k - self.dur) / 0.8))
            px = x0 + (x1 - x0) * u + nx * side * 50 * u; py = y0 + (y1 - y0) * u + ny * side * 50 * u
            d.ellipse([px - r, py - r, px + r, py + r], fill=self.color + (int(150 * a * fade),))

# ---------------------------------------------------------------- pianta del caveau (vista dall'alto)
class VaultPlan(El):
    """vista dall'alto: corridoio, porta (sinistra), stanza cassette; sensori marcati"""
    def __init__(self, box, t0, t1=None):
        super().__init__(t0, t1, 0.4); self.box = box
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); al = int(255 * a); x0, y0, x1, y1 = self.box
        d.rounded_rectangle([x0 - 30, y0 - 30, x1 + 30, y1 + 50], 16, fill=(26, 30, 34, int(al * 0.92)), outline=(60, 66, 72, al), width=2)
        for gx in range(int(x0), int(x1), 40): d.line([(gx, y0 - 20), (gx, y1 + 20)], fill=(34, 40, 46, al), width=1)
        for gy in range(int(y0), int(y1), 40): d.line([(x0 - 20, gy), (x1 + 20, gy)], fill=(34, 40, 46, al), width=1)
        w = x1 - x0; h = y1 - y0
        d.rectangle([x0, y0 + h * .35, x0 + w * .28, y0 + h * .65], fill=(36, 42, 48, al), outline=(180, 196, 210, al), width=3)
        d.text((x0 + w * .14, y0 + h * .5), "corridoio", font=font(OSW, 28, 500), fill=(200, 210, 220, al), anchor="mm")
        d.rectangle([x0 + w * .30, y0, x1, y1], fill=(44, 40, 38, al), outline=(180, 196, 210, al), width=3)
        for c in range(10):
            d.rectangle([x0 + w * .34 + c * w * .065, y0 + 10, x0 + w * .34 + c * w * .065 + w * .055, y0 + h * .12], fill=(120, 126, 134, al))
            d.rectangle([x0 + w * .34 + c * w * .065, y1 - h * .12, x0 + w * .34 + c * w * .065 + w * .055, y1 - 10], fill=(120, 126, 134, al))
        d.rectangle([x0 + w * .28, y0 + h * .4, x0 + w * .32, y0 + h * .6], fill=(170, 176, 184, al))
        d.text((x0 + w * .30, y0 + h * .66), "porta", font=font(OSW, 26, 500), fill=GOLD + (al,), anchor="ma")
        d.text((x0 + w * .65, y0 + h * .5), "SALA DELLE CASSETTE", font=font(OSW, 34, 500), fill=(200, 210, 220, al), anchor="mm")
        d.text((x1 + 18, y1 + 38), "SCHEMA SEMPLIFICATO · NON IN SCALA", font=font(COURR, 20), fill=(150, 160, 170, al), anchor="rs")
