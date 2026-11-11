# FASCICOLO ITALIA — motore grafico (stile "dossier noir").
# Tutto disegnato da codice: documenti ricostruiti, mappe (Natural Earth), timeline, schemi, bacheca.
import math, json, random, re, os, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

FD = "/home/claude/fonts/"
SERIF = FD + "DMSerifDisplay-Regular.ttf"
TYPE = FD + "SpecialElite-Regular.ttf"
OSW = FD + "Oswald.ttf"
PS = FD + "Poppins-SemiBold.ttf"
PB = FD + "Poppins-ExtraBold.ttf"
COUR = FD + "CourierPrime-Bold.ttf"
COURR = FD + "CourierPrime-Regular.ttf"
HERE = os.path.dirname(os.path.abspath(__file__))

BG = (19, 17, 16)
PAPER = (232, 222, 200)
INK = (38, 33, 29)
RED = (200, 52, 42)
REDL = (232, 92, 78)
GOLD = (218, 176, 96)
WHITE = (238, 234, 226)
GREY = (150, 143, 134)
DIM = (78, 73, 68)
LINE = (120, 112, 102)

W, H, FPS = 1920, 1080, 24
def configure(w, h, fps):
    global W, H, FPS
    W, H, FPS = w, h, fps

_fc = {}
def font(p, s, wght=None):
    k = (p, s, wght)
    if k not in _fc:
        f = ImageFont.truetype(p, s)
        if p == OSW:
            try: f.set_variation_by_axes([wght or 600])
            except Exception: pass
        _fc[k] = f
    return _fc[k]
def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def ease_io(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def back(x):
    x = max(0.0, min(1.0, x)); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def tl(d, s, f):
    return d.textlength(s, font=f)
_tmpd = ImageDraw.Draw(Image.new("RGBA", (4, 4)))

def set_alpha(im, a):
    if a >= 0.999: return im
    im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * a))); return im

def place(lay, im, xy, anchor="mm", a=1.0):
    x, y = xy
    if anchor[0] == "m": x -= im.width / 2
    elif anchor[0] == "r": x -= im.width
    if anchor[1] == "m": y -= im.height / 2
    elif anchor[1] == "b": y -= im.height
    if a < 0.999: im = set_alpha(im, a)
    lay.alpha_composite(im, (int(round(x)), int(round(y))))

# ---------------------------------------------------------------- sfondo
def make_bg(seed=3):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W * 0.5) / (W * 0.75)) ** 2 + ((yy - H * 0.42) / (H * 0.75)) ** 2)
    glow = np.clip(1 - r, 0, 1) ** 1.6 * 22
    arr = np.zeros((H, W, 3), np.float32) + np.array(BG, np.float32)
    arr += glow[..., None] * np.array([1.0, 0.85, 0.7])
    rng = np.random.default_rng(seed)
    low = Image.fromarray((rng.random((H // 8, W // 8)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
    arr += (np.asarray(low, np.float32)[..., None] / 255 - 0.5) * 6
    arr += rng.normal(0, 1.4, (H, W, 1))
    vig = np.clip((r - 0.55) * 0.9, 0, 0.6)
    arr *= (1 - vig[..., None])
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")

def make_grains(n=4, seed=11):
    rng = np.random.default_rng(seed); out = []
    for _ in range(n):
        g = rng.normal(0, 1, (H // 2, W // 2))
        a = (np.clip(np.abs(g) - 1.6, 0, 3) * 26).astype(np.uint8)
        v = np.where(g > 0, 255, 0).astype(np.uint8)
        im = Image.fromarray(np.dstack([v, v, v, a]), "RGBA").resize((W, H), Image.NEAREST)
        out.append(im)
    return out

# ---------------------------------------------------------------- testo ricco
def rich_img(text, fnt, size, color=WHITE, accent=RED, lh=1.12, align="l", spacing=0, wght=None):
    """testo multi-riga con *accento*; restituisce immagine RGBA"""
    f = font(fnt, size, wght)
    lines = text.split("\n")
    def lw(l):
        return sum(tl(_tmpd, p.strip("*"), f) for p in re.split(r"(\*[^*]+\*)", l) if p) + spacing * len(l.replace("*", ""))
    widths = [lw(l) for l in lines]
    asc, desc = f.getmetrics()
    lhp = int(size * lh)
    Wd = int(max(widths) + 16); Ht = int(lhp * (len(lines) - 1) + asc + desc + 12)
    im = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    y = 4
    for l, w in zip(lines, widths):
        x = 8 + ((Wd - 16 - w) / 2 if align == "m" else (Wd - 16 - w if align == "r" else 0))
        for p in re.split(r"(\*[^*]+\*)", l):
            if not p: continue
            col = accent if p.startswith("*") else color
            p2 = p.strip("*")
            if spacing:
                for ch in p2:
                    d.text((x, y), ch, font=f, fill=col + (255,)); x += tl(d, ch, f) + spacing
            else:
                d.text((x, y), p2, font=f, fill=col + (255,)); x += tl(d, p2, f)
        y += lhp
    return im

_ric = {}
def rich_cached(*a, **k):
    key = (a, tuple(sorted(k.items())))
    if key not in _ric: _ric[key] = rich_img(*a, **k)
    return _ric[key]

# ---------------------------------------------------------------- elementi
class El:
    sfx_kind = None
    def __init__(self, t0, t1=None, fade=0.35):
        self.t0, self.t1, self.fade = t0, t1, fade
    def alpha(self, t):
        if t < self.t0: return 0.0
        a = ease((t - self.t0) / self.fade)
        if self.t1 is not None and t > self.t1: a *= max(0.0, 1 - (t - self.t1) / 0.3)
        return a
    def draw(self, lay, t, a): pass

class Text(El):
    def __init__(self, text, xy, t0, t1=None, size=60, fnt=SERIF, color=WHITE, anchor="la", align="l",
                 accent=RED, typewriter=False, slide=18, spacing=0, lh=1.12, wght=None, maxw=None):
        super().__init__(t0, t1)
        self.text, self.xy, self.anchor, self.typewriter, self.slide = text, xy, anchor, typewriter, slide
        self.kw = dict(fnt=fnt, size=size, color=color, accent=accent, align=align, spacing=spacing, lh=lh, wght=wght)
        if maxw:
            while self.kw["size"] > 20 and rich_cached(text, **self.kw).width > maxw: self.kw["size"] -= 2
        self.full = rich_cached(text, **self.kw)
        self.tdur = min(2.2, 0.035 * len(text)) if typewriter else 0
    def draw(self, lay, t, a):
        if self.typewriter:
            n = int(len(self.text) * min(1.0, (t - self.t0) / max(0.01, self.tdur)))
            if n <= 0: return
            sub = self.text[:n]
            if sub.count("*") % 2: sub += "*"
            im = rich_cached(sub, **self.kw)
            # ancorare sulla dimensione finale
            x, y = self.xy
            if self.anchor[0] == "m": x -= self.full.width / 2
            elif self.anchor[0] == "r": x -= self.full.width
            if self.anchor[1] == "m": y -= self.full.height / 2
            elif self.anchor[1] == "b": y -= self.full.height
            if self.kw["align"] == "m": x += (self.full.width - im.width) / 2
            place(lay, im, (x, y), "la", a if self.t1 is not None else 1.0)
            return
        dy = self.slide * (1 - ease((t - self.t0) / 0.4))
        place(lay, self.full, (self.xy[0], self.xy[1] + dy), self.anchor, a)

class Img(El):
    """immagine pronta (documento, disegno). anim: drop | slide | fade | pop"""
    def __init__(self, img, xy, t0, t1=None, anim="drop", anchor="mm", rot=0, shadow=True):
        super().__init__(t0, t1, 0.3)
        if rot: img = img.rotate(rot, expand=True, resample=Image.BICUBIC)
        if shadow:
            pad = 40
            sh = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
            m = img.getchannel("A").point(lambda v: int(v * 0.7))
            blk = Image.new("RGBA", img.size, (0, 0, 0, 255)); blk.putalpha(m)
            sh.alpha_composite(blk, (pad + 10, pad + 16)); sh = sh.filter(ImageFilter.GaussianBlur(14))
            sh.alpha_composite(img, (pad, pad)); img = sh
        self.img, self.xy, self.anim, self.anchor = img, xy, anim, anchor
    def draw(self, lay, t, a):
        k = t - self.t0; im = self.img; x, y = self.xy
        if self.anim == "drop":
            s = 1.0 + 0.10 * (1 - ease(k / 0.45))
            if s > 1.002: im = im.resize((int(im.width * s), int(im.height * s)), Image.BILINEAR)
        elif self.anim == "slide":
            y += 90 * (1 - ease(k / 0.5))
        elif self.anim == "pop":
            s = back(k / 0.35) if k < 0.35 else 1.0
            if abs(s - 1) > 0.003: im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
        place(lay, im, (x, y), self.anchor, a)

class Stamp(El):
    def __init__(self, text, xy, t0, t1=None, color=RED, size=64, rot=-9, sub=None):
        super().__init__(t0, t1, 0.08)
        self.img = stamp_img(text, color, size, rot, sub); self.xy = xy
    def draw(self, lay, t, a):
        k = t - self.t0
        s = 1.0 + 0.9 * (1 - ease(k / 0.16))
        im = self.img
        if s > 1.003: im = im.resize((int(im.width * s), int(im.height * s)), Image.BILINEAR)
        place(lay, im, self.xy, "mm", a * min(1.0, k / 0.06))

class Line(El):
    """linea che si disegna (es. barrare un testo)"""
    def __init__(self, p0, p1, t0, t1=None, color=RED, width=8, dur=0.35):
        super().__init__(t0, t1, 0.05); self.p0, self.p1, self.color, self.w, self.dur = p0, p1, color, width, dur
    def draw(self, lay, t, a):
        f = ease((t - self.t0) / self.dur)
        x = self.p0[0] + (self.p1[0] - self.p0[0]) * f; y = self.p0[1] + (self.p1[1] - self.p0[1]) * f
        ImageDraw.Draw(lay).line([self.p0, (x, y)], fill=self.color + (int(255 * a),), width=self.w)

class Big(El):
    def __init__(self, text, xy, t0, t1=None, size=200, color=WHITE, fnt=SERIF, count=None, sub=None, subsize=40):
        super().__init__(t0, t1, 0.25)
        self.text, self.xy, self.size, self.color, self.fnt, self.count, self.sub, self.subsize = text, xy, size, color, fnt, count, sub, subsize
    def draw(self, lay, t, a):
        txt = self.text
        if self.count:
            v0, v1, fmt, dd = self.count; txt = fmt(v0 + (v1 - v0) * ease((t - self.t0) / dd))
        s = 0.92 + 0.08 * ease((t - self.t0) / 0.3)
        d = ImageDraw.Draw(lay)
        d.text(self.xy, txt, font=font(self.fnt, int(self.size * s)), fill=self.color + (int(255 * a),), anchor="mm")
        if self.sub:
            im = rich_cached(self.sub, fnt=PS, size=self.subsize, color=GREY, align="m")
            place(lay, im, (self.xy[0], self.xy[1] + self.size * 0.62), "mt", a)

class Rows(El):
    def __init__(self, rows, t0, t1=None, x0=260, x1=1660, y=360, gap=110, size=48, lfont=PS, vfont=OSW):
        super().__init__(t0, t1); self.rows, self.x0, self.x1, self.y, self.gap, self.size, self.lf, self.vf = rows, x0, x1, y, gap, size, lfont, vfont
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay)
        for j, r in enumerate(self.rows):
            if t < r["t"]: continue
            ra = int(255 * a * ease((t - r["t"]) / 0.3)); dx = 30 * (1 - ease((t - r["t"]) / 0.35))
            y = self.y + j * self.gap
            d.text((self.x0 + dx, y), r["label"], font=font(self.lf, self.size), fill=r.get("lcolor", WHITE) + (ra,), anchor="lm")
            d.text((self.x1 + dx, y), r["value"], font=font(self.vf, self.size + 8, 600), fill=r.get("color", GOLD) + (ra,), anchor="rm")
            d.line([(self.x0, y + self.gap / 2), (self.x1, y + self.gap / 2)], fill=(60, 56, 52, ra), width=2)

class Chapter(El):
    def __init__(self, num, title, t0, t1):
        super().__init__(t0, t1, 0.3); self.num, self.title = num, title
    def draw(self, lay, t, a):
        k = t - self.t0; d = ImageDraw.Draw(lay); al = int(255 * a)
        cx, cy = W / 2, H * 0.46
        s = W / 1920 if W > H else 1.0
        d.text((cx, cy - 150 * s), f"CAPITOLO {self.num}" if self.num else "CONCLUSIONI", font=font(TYPE, int(44 * s)), fill=RED + (al,), anchor="mm")
        lw = (W * 0.32) * ease(k / 0.6)
        d.line([(cx - lw, cy - 95 * s), (cx + lw, cy - 95 * s)], fill=DIM + (al,), width=2)
        im = rich_cached(self.title, fnt=SERIF, size=int(120 * s) if W > H else 110, color=WHITE, align="m", lh=1.05)
        place(lay, im, (cx, cy - 60 * s + 20 * (1 - ease(k / 0.5))), "mt", a)

# ---------------------------------------------------------------- carta e documenti
_paper_c = {}
def paper(w, h, tone=PAPER, seed=1, aged=0.5):
    key = (w, h, tone, seed, aged)
    if key in _paper_c: return _paper_c[key].copy()
    rng = np.random.default_rng(seed)
    arr = np.zeros((h, w, 3), np.float32) + np.array(tone, np.float32)
    low = Image.fromarray((rng.random((max(2, h // 30), max(2, w // 30))) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    arr += (np.asarray(low, np.float32)[..., None] / 255 - 0.5) * 22 * aged
    arr += rng.normal(0, 4, (h, w, 1))
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    e = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy))
    arr -= (np.clip(1 - e / 40, 0, 1) ** 2 * 40 * aged)[..., None] * np.array([1, 1.1, 1.4])
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    _paper_c[key] = im
    return im.copy()

def recon_label(d, w, h, size=20):
    f = font(COUR, size)
    txt = "RICOSTRUZIONE GRAFICA"
    tw = tl(d, txt, f)
    d.rectangle([w - tw - 34, h - size - 30, w - 14, h - 14], outline=RED + (210,), width=2)
    d.text((w - tw / 2 - 24, h - size / 2 - 22), txt, font=f, fill=RED + (220,), anchor="mm")

def doc_typed(w, h, header, lines, footer=None, seed=2, size=34, label=True, tone=PAPER):
    """foglio battuto a macchina. lines: lista di stringhe ('' = riga vuota; '*x*' rosso)"""
    im = paper(w, h, tone, seed); d = ImageDraw.Draw(im)
    y = 46
    if header:
        im2 = rich_img(header, COUR, int(size * 0.85), INK, RED); im.alpha_composite(im2, (54, y)); y += im2.height + 6
        d.line([(60, y), (w - 60, y)], fill=INK + (200,), width=2); y += 24
    for l in lines:
        if l == "": y += int(size * 0.7); continue
        im2 = rich_img(l, TYPE, size, INK, RED, lh=1.25)
        im.alpha_composite(im2, (58, y)); y += im2.height + 2
    if footer:
        f = font(COURR, 20); d.text((60, h - 72), footer, font=f, fill=(90, 80, 70, 255), anchor="ls")
    if label: recon_label(d, w, h)
    return im

def stamp_img(text, color=RED, size=64, rot=-9, sub=None):
    f = font(OSW, size, 700)
    lines = text.split("\n")
    tw = max(tl(_tmpd, l, f) for l in lines); lh = int(size * 1.08)
    sh = lh * len(lines) + (int(size * 0.5) if sub else 0)
    w, h = int(tw + size * 0.9), int(sh + size * 0.55)
    m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    bw = max(4, size // 12)
    d.rounded_rectangle([bw, bw, w - bw, h - bw], size // 6, outline=255, width=bw)
    y = size * 0.25
    for l in lines:
        d.text((w / 2, y), l, font=f, fill=255, anchor="ma"); y += lh
    if sub: d.text((w / 2, y + 2), sub, font=font(COUR, int(size * 0.36)), fill=255, anchor="ma")
    rng = np.random.default_rng(len(text))
    nz = rng.random((h, w))
    nz = np.asarray(Image.fromarray((nz * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255
    a = np.asarray(m, np.float32) * np.clip((nz - 0.25) * 2.2, 0, 1) * 0.92
    im = Image.new("RGBA", (w, h), color + (0,)); im.putalpha(Image.fromarray(a.astype(np.uint8)))
    return im.rotate(rot, expand=True, resample=Image.BICUBIC)

def newspaper(w, h, masthead, date, headline, sub, seed=5):
    im = paper(w, h, (226, 214, 186), seed, 0.8); d = ImageDraw.Draw(im)
    d.text((w / 2, 40), masthead, font=font(SERIF, int(w * 0.075)), fill=INK + (255,), anchor="mt")
    y = 40 + int(w * 0.095)
    d.line([(40, y), (w - 40, y)], fill=INK + (255,), width=3); d.line([(40, y + 8), (w - 40, y + 8)], fill=INK + (255,), width=1)
    d.text((40, y + 16), date, font=font(COURR, 22), fill=INK + (255,))
    y += 60
    hi = rich_img(headline, SERIF, int(w * 0.07), INK, RED, lh=1.02, align="m")
    im.alpha_composite(hi, (int((w - hi.width) / 2), y)); y += hi.height + 6
    si = rich_img(sub, COURR, 20, (70, 62, 54), RED, align="m")
    im.alpha_composite(si, (int((w - si.width) / 2), y)); y += si.height + 18
    rng = random.Random(seed)
    cols = 3; cw = (w - 80 - 40) / cols
    for c in range(cols):
        x0 = 40 + c * (cw + 20); yy = y
        while yy < h - 80:
            ln = cw * rng.uniform(0.7, 1.0) if rng.random() > 0.12 else cw * rng.uniform(0.2, 0.5)
            d.line([(x0, yy), (x0 + ln, yy)], fill=(120, 110, 96, 255), width=5); yy += 16
    recon_label(d, w, h)
    return im

def id_card(w, h, fields, title="SCHEDA SEGNALETICA", year="1909", seed=7):
    im = paper(w, h, (226, 218, 198), seed); d = ImageDraw.Draw(im)
    d.text((40, 36), title, font=font(COUR, 34), fill=INK + (255,))
    d.text((w - 40, 40), year, font=font(TYPE, 34), fill=RED + (255,), anchor="ra")
    d.line([(40, 86), (w - 40, 86)], fill=INK + (255,), width=2)
    # riquadro foto (sagoma, nessuna foto reale)
    px, py, pw, ph = 40, 110, int(w * 0.30), int(h * 0.55)
    d.rectangle([px, py, px + pw, py + ph], fill=(200, 190, 170, 255), outline=INK + (255,), width=2)
    silhouette(d, px + pw / 2, py + ph * 0.98, pw * 0.8, (110, 100, 88))
    d.text((px + pw / 2, py + ph + 14), "foto non mostrata", font=font(COURR, 18), fill=(110, 100, 88, 255), anchor="ma")
    y = 120; x = px + pw + 40
    for k, v in fields:
        d.text((x, y), k, font=font(COURR, 20), fill=(110, 100, 88, 255)); y += 26
        d.text((x, y), v, font=font(TYPE, 34), fill=INK + (255,)); y += 52
    # impronte (riquadri)
    fy = py + ph + 60
    for j in range(5):
        bx = 40 + j * (w - 80) / 5
        d.rectangle([bx + 6, fy, bx + (w - 80) / 5 - 6, h - 60], outline=INK + (180,), width=2)
        fp = fingerprint_img(int(min((w - 80) / 5 - 30, h - 60 - fy - 20)), seed=j + 3, color=(60, 52, 46))
        im.alpha_composite(fp, (int(bx + ((w - 80) / 5 - fp.width) / 2), int(fy + (h - 60 - fy - fp.height) / 2)))
    recon_label(d, w, h)
    return im

def silhouette(d, cx, by, w, col, a=255):
    """sagoma generica testa+spalle, base a by"""
    hr = w * 0.20
    d.ellipse([cx - hr, by - w * 0.95, cx + hr, by - w * 0.95 + hr * 2.3], fill=col + (a,))
    d.rounded_rectangle([cx - w * 0.45, by - w * 0.45, cx + w * 0.45, by], int(w * 0.18), fill=col + (a,))

_fp = {}
def fingerprint_img(size, seed=1, color=INK):
    key = (size, seed, color)
    if key in _fp: return _fp[key]
    S = size * 2
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    cx, cy = S * 0.5, S * 0.55
    rng = np.random.default_rng(seed)
    nx = (xx - cx) / (S * 0.36); ny = (yy - cy) / (S * 0.46)
    r = np.sqrt(nx ** 2 + ny ** 2)
    ang = np.arctan2(ny, nx)
    warp = 0.06 * np.sin(ang * 3 + seed) + 0.04 * np.sin(ny * 5 + seed)
    rid = 0.5 + 0.5 * np.sin((r + warp) * 2 * np.pi * 9 + 0.7 * np.sin(ang * 2))
    mask = np.clip((1.0 - r) * 6, 0, 1)
    noise = rng.random((S, S)) * 0.35
    a = np.clip((rid - 0.45) * 3 - noise, 0, 1) * mask * 255
    im = Image.new("RGBA", (S, S), color + (0,)); im.putalpha(Image.fromarray(a.astype(np.uint8)))
    im = im.resize((size, size), Image.LANCZOS)
    _fp[key] = im
    return im

class Fingerprint(El):
    def __init__(self, xy, size, t0, t1=None, color=WHITE, lens=True):
        super().__init__(t0, t1, 0.2); self.xy, self.size, self.lens = xy, size, lens
        self.img = fingerprint_img(size, 2, color)
    def draw(self, lay, t, a):
        k = ease((t - self.t0) / 1.2)
        im = self.img
        h = max(1, int(im.height * k))
        place(lay, im.crop((0, 0, im.width, h)), (self.xy[0] - im.width / 2, self.xy[1] - im.height / 2), "la", a)
        if self.lens:
            d = ImageDraw.Draw(lay); r = self.size * 0.62; cx, cy = self.xy
            ang = (t - self.t0) * 0.8
            ox, oy = cx + math.cos(ang) * self.size * 0.08, cy + math.sin(ang) * self.size * 0.08
            d.ellipse([ox - r, oy - r, ox + r, oy + r], outline=GOLD + (int(230 * a),), width=10)
            d.line([(ox + r * 0.7, oy + r * 0.7), (ox + r * 1.25, oy + r * 1.25)], fill=GOLD + (int(230 * a),), width=22)

# ---------------------------------------------------------------- muro vuoto / quadro stilizzato
class Frame(El):
    """muro con quadro stilizzato (sagoma, NON l'opera) che può sparire lasciando 4 ganci"""
    def __init__(self, xy, w, h, t0, t1=None, vanish=None, dims=False, label=None):
        super().__init__(t0, t1); self.xy, self.w, self.h, self.vanish, self.dims, self.label = xy, w, h, vanish, dims, label
        self.pic = self._pic()
    def _pic(self):
        w, h = int(self.w), int(self.h)
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rectangle([0, 0, w - 1, h - 1], fill=(96, 70, 40, 255))
        b = int(w * 0.07)
        yy, xx = np.mgrid[0:h - 2 * b, 0:w - 2 * b].astype(np.float32)
        g = np.zeros((h - 2 * b, w - 2 * b, 3), np.float32) + np.array([62, 66, 48])
        g += (1 - yy / (h - 2 * b))[..., None] * np.array([30, 28, 14])
        inner = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).convert("RGBA")
        di = ImageDraw.Draw(inner); iw, ih = inner.size
        silhouette(di, iw / 2, ih * 1.02, iw * 0.78, (34, 28, 22))
        im.alpha_composite(inner, (b, b))
        d.rectangle([b - 3, b - 3, w - b + 2, h - b + 2], outline=(160, 120, 60, 255), width=3)
        return im
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); cx, cy = self.xy; al = int(255 * a)
        x0, y0 = cx - self.w / 2, cy - self.h / 2
        hooks = [(x0 + self.w * 0.2, y0 - 10), (x0 + self.w * 0.8, y0 - 10), (x0 + self.w * 0.2, y0 + self.h + 10), (x0 + self.w * 0.8, y0 + self.h + 10)]
        va = 1.0
        if self.vanish is not None and t > self.vanish: va = max(0.0, 1 - (t - self.vanish) / 0.6)
        if va < 1:
            d.rectangle([x0, y0, x0 + self.w, y0 + self.h], outline=(90, 84, 78, int(al * (1 - va))), width=2)
            for hx, hy in hooks:
                d.ellipse([hx - 9, hy - 9, hx + 9, hy + 9], fill=(160, 155, 148, int(al * (1 - va))))
                d.line([(hx, hy), (hx, hy + (14 if hy < cy else -14))], fill=(160, 155, 148, int(al * (1 - va))), width=5)
        if va > 0:
            place(lay, self.pic, (x0, y0), "la", a * va)
        if self.dims:
            k = ease((t - self.dims) / 0.6) if isinstance(self.dims, (int, float)) and not isinstance(self.dims, bool) else 1
            if k > 0:
                ka = int(al * k); f = font(OSW, 40, 500)
                d.line([(x0, y0 + self.h + 40), (x0 + self.w, y0 + self.h + 40)], fill=GOLD + (ka,), width=3)
                d.text((cx, y0 + self.h + 50), "53 cm", font=f, fill=GOLD + (ka,), anchor="ma")
                d.line([(x0 + self.w + 40, y0), (x0 + self.w + 40, y0 + self.h)], fill=GOLD + (ka,), width=3)
                d.text((x0 + self.w + 56, cy), "77 cm", font=f, fill=GOLD + (ka,), anchor="lm")
        if self.label:
            d.text((cx, y0 - 60), self.label, font=font(TYPE, 34), fill=GREY + (al,), anchor="ms")

# ---------------------------------------------------------------- timeline
class Timeline(El):
    """events: list of dict(top, bottom, t, hl=False); posizioni equidistanti o x esplicite (0..1)"""
    def __init__(self, x0, x1, y, events, t0, t1=None, size=34):
        super().__init__(t0, t1); self.x0, self.x1, self.y, self.ev, self.size = x0, x1, y, events, size
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); al = int(255 * a)
        k = ease((t - self.t0) / 0.7)
        d.line([(self.x0, self.y), (self.x0 + (self.x1 - self.x0) * k, self.y)], fill=LINE + (al,), width=3)
        n = len(self.ev)
        for j, e in enumerate(self.ev):
            if t < e["t"]: continue
            pos = e.get("x", j / max(1, n - 1))
            x = self.x0 + (self.x1 - self.x0) * pos
            ea = int(al * ease((t - e["t"]) / 0.3)); s = back((t - e["t"]) / 0.3)
            col = RED if e.get("hl") else GOLD
            r = 13 * s
            d.ellipse([x - r, self.y - r, x + r, self.y + r], fill=col + (ea,))
            up = j % 2 == 0 if e.get("alt", True) else True
            d.text((x, self.y - 34), e["top"], font=font(OSW, self.size, 600), fill=(WHITE if e.get("hl") else GOLD) + (ea,), anchor="ms")
            if e.get("bottom"):
                im = rich_cached(e["bottom"], fnt=PS, size=int(self.size * 0.72), color=GREY, align="m", lh=1.1)
                place(lay, im, (x, self.y + 26), "mt", ea / 255)

# ---------------------------------------------------------------- mappa (Natural Earth)
GEO = None
def _geo():
    global GEO
    if GEO is None:
        GEO = json.load(open(os.path.join(HERE, "countries.geojson")))
    return GEO
MAPB = dict(lon0=-6.0, lon1=21.0, lat0=35.5, lat1=53.5, K=210.0)
COSL = math.cos(math.radians(45))
_base = None
def map_base():
    global _base
    if _base is not None: return _base
    cache = os.path.join(HERE, "map_base.png")
    if os.path.exists(cache):
        _base = Image.open(cache).convert("RGB"); return _base
    K = MAPB["K"]; S = 1
    Wb = int((MAPB["lon1"] - MAPB["lon0"]) * COSL * K); Hb = int((MAPB["lat1"] - MAPB["lat0"]) * K)
    im = Image.new("RGB", (Wb, Hb), (22, 27, 30)); d = ImageDraw.Draw(im)
    def P(lon, lat): return ((lon - MAPB["lon0"]) * COSL * K, (MAPB["lat1"] - lat) * K)
    # graticola
    for lo in range(-6, 22, 2): d.line([P(lo, MAPB["lat0"]), P(lo, MAPB["lat1"])], fill=(30, 36, 40), width=2)
    for la in range(36, 54, 2): d.line([P(MAPB["lon0"], la), P(MAPB["lon1"], la)], fill=(30, 36, 40), width=2)
    feats = _geo()["features"]
    for ft in feats:
        name = ft["properties"].get("ADMIN", "")
        g = ft["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        col = (74, 64, 52) if name == "Italy" else ((64, 57, 50) if name == "France" else (52, 48, 44))
        for p in polys:
            ring = p[0]
            if not any(MAPB["lon0"] - 5 < x < MAPB["lon1"] + 5 and MAPB["lat0"] - 5 < y < MAPB["lat1"] + 5 for x, y in ring[::5] + [ring[0]]): continue
            d.polygon([P(x, y) for x, y in ring], fill=col)
    for ft in feats:
        g = ft["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for p in polys:
            ring = p[0]
            if not any(MAPB["lon0"] - 5 < x < MAPB["lon1"] + 5 and MAPB["lat0"] - 5 < y < MAPB["lat1"] + 5 for x, y in ring[::5] + [ring[0]]): continue
            d.line([P(x, y) for x, y in ring] + [P(*ring[0])], fill=(110, 98, 84), width=2)
    rng = np.random.default_rng(4)
    arr = np.asarray(im, np.float32) + rng.normal(0, 2.5, (Hb, Wb, 1))
    _base = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    _base.save(cache)
    return _base

PLACES = {"Parigi": (2.35, 48.86), "Firenze": (11.25, 43.77), "Roma": (12.50, 41.90), "Milano": (9.19, 45.46),
          "Dumenza": (8.78, 46.02), "Torino": (7.69, 45.07), "Napoli": (14.27, 40.85), "Bruxelles": (4.35, 50.85)}
def where(p): return PLACES[p] if isinstance(p, str) else p

class MapEl(El):
    """cam: [(t, luogo, ppd)] ppd = pixel schermo per grado; routes: dict(pts=[luoghi], t, d, color, dashed);
    pins: dict(at, label, t, side='r'|'l'|'t'|'b', color)"""
    def __init__(self, box, cam, t0, t1=None, routes=(), pins=(), title=None):
        super().__init__(t0, t1, 0.4); self.box, self.routes, self.pins, self.title = box, list(routes), list(pins), title
        self.cam = sorted([(c[0], where(c[1]), c[2]) for c in cam], key=lambda c: c[0])
    def view(self, t):
        ks = self.cam
        if t <= ks[0][0]: c = ks[0]; return c[1][0], c[1][1], c[2]
        for p, q in zip(ks, ks[1:]):
            if t <= q[0]:
                u = ease_io((t - p[0]) / max(1e-6, q[0] - p[0]))
                return (p[1][0] + (q[1][0] - p[1][0]) * u, p[1][1] + (q[1][1] - p[1][1]) * u,
                        math.exp(math.log(p[2]) + (math.log(q[2]) - math.log(p[2])) * u))
        c = ks[-1]; return c[1][0], c[1][1], c[2]
    def draw(self, lay, t, a):
        base = map_base(); K = MAPB["K"]
        x0, y0, x1, y1 = self.box; bw, bh = x1 - x0, y1 - y0
        lon, lat, ppd = self.view(t)
        s = K / ppd  # pixel base per pixel schermo
        cx = (lon - MAPB["lon0"]) * COSL * K; cy = (MAPB["lat1"] - lat) * K
        bx0, by0 = cx - bw / 2 * s, cy - bh / 2 * s
        im = base.resize((int(bw), int(bh)), Image.BILINEAR, box=(bx0, by0, bx0 + bw * s, by0 + bh * s)).convert("RGBA")
        def S(p):
            lo, la = where(p)
            return (x0 + ((lo - MAPB["lon0"]) * COSL * K - bx0) / s, y0 + ((MAPB["lat1"] - la) * K - by0) / s)
        # bordo morbido
        m = Image.new("L", im.size, 0); dm = ImageDraw.Draw(m); dm.rounded_rectangle([0, 0, bw - 1, bh - 1], 18, fill=int(255 * a))
        lay.paste(im, (int(x0), int(y0)), m) if a >= 0.999 else lay.alpha_composite(Image.composite(im, Image.new("RGBA", im.size, (0, 0, 0, 0)), m), (int(x0), int(y0)))
        full = lay; lay = Image.new("RGBA", full.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay); al = int(255 * a)
        for r in self.routes:
            if t < r["t"]: continue
            pts = [S(p) for p in r["pts"]]
            L = [0.0]
            for p, q in zip(pts, pts[1:]): L.append(L[-1] + math.dist(p, q))
            f = ease_io((t - r["t"]) / r.get("d", 1.5)) * L[-1]
            path = [pts[0]]
            for j in range(1, len(pts)):
                if L[j] <= f: path.append(pts[j])
                else:
                    u = (f - L[j - 1]) / max(1e-6, L[j] - L[j - 1])
                    path.append((pts[j - 1][0] + (pts[j][0] - pts[j - 1][0]) * u, pts[j - 1][1] + (pts[j][1] - pts[j - 1][1]) * u)); break
            col = r.get("color", RED) + (al,)
            if r.get("dashed", True):
                acc = 0.0
                for p, q in zip(path, path[1:]):
                    seg = math.dist(p, q); n = max(1, int(seg / 6))
                    for i in range(n):
                        u0, u1 = i / n, (i + 1) / n
                        if int((acc + seg * u0) / 22) % 2 == 0:
                            d.line([(p[0] + (q[0] - p[0]) * u0, p[1] + (q[1] - p[1]) * u0), (p[0] + (q[0] - p[0]) * u1, p[1] + (q[1] - p[1]) * u1)], fill=col, width=6)
                    acc += seg
            else:
                d.line(path, fill=col, width=6, joint="curve")
            ex, ey = path[-1]
            ic = r.get("icon")
            if ic:
                import fx
                if ic == "person": fx.draw_person(lay, ex, ey + 30, 0.28, "worker", f / 10, f < L[-1] - 1, alpha=al)
                elif ic == "painting": place(lay, fx.painting_icon(54), (ex, ey), "mm", a)
                else: place(lay, fx.icon(ic, 90), (ex, ey), "mm", a)
                d = ImageDraw.Draw(lay)
            else: d.ellipse([ex - 11, ey - 11, ex + 11, ey + 11], fill=col)
        for p in self.pins:
            if t < p["t"]: continue
            x, y = S(p["at"]); pa = int(al * ease((t - p["t"]) / 0.3)); sc = back((t - p["t"]) / 0.3)
            col = p.get("color", GOLD)
            r = 12 * sc
            d.ellipse([x - r - 6, y - r - 6, x + r + 6, y + r + 6], outline=col + (pa,), width=3)
            d.ellipse([x - r * 0.6, y - r * 0.6, x + r * 0.6, y + r * 0.6], fill=col + (pa,))
            side = p.get("side", "r"); f = font(OSW, p.get("size", 40), 600)
            lab = p["label"]
            off = {"r": (30, 0, "lm"), "l": (-30, 0, "rm"), "t": (0, -34, "ms"), "b": (0, 34, "mt")}[side]
            tw = tl(d, lab, f)
            bx = x + off[0] - (tw if off[2][0] == "r" else (tw / 2 if off[2][0] == "m" else 0))
            by = y + off[1] - (f.size if off[2][1] == "s" else (f.size / 2 if off[2][1] == "m" else 0))
            d.rounded_rectangle([bx - 12, by - 6, bx + tw + 12, by + f.size + 6], 8, fill=(14, 12, 11, int(pa * 0.75)))
            d.text((x + off[0], y + off[1]), lab, font=f, fill=WHITE + (pa,), anchor=off[2])
        if self.title:
            d.text((x0 + 24, y1 - 22), self.title, font=font(COURR, 22), fill=(180, 170, 155, int(al * 0.9)), anchor="ls")
        cm = Image.new("L", full.size, 0); ImageDraw.Draw(cm).rectangle([x0, y0, x1, y1], fill=255)
        lay.putalpha(ImageChops.multiply(lay.getchannel("A"), cm)); full.alpha_composite(lay)

# ---------------------------------------------------------------- schema (pianta semplificata)
class Plan(El):
    """rooms: list (x0,y0,x1,y1,label) in coordinate 0..1 del box; path: list of (pts, t, d); marks: (xy, label, t, kind)"""
    def __init__(self, box, rooms, t0, t1=None, path=(), marks=(), title="SCHEMA SEMPLIFICATO · NON IN SCALA"):
        super().__init__(t0, t1, 0.4); self.box, self.rooms, self.path, self.marks, self.title = box, rooms, list(path), list(marks), title
    def P(self, p):
        x0, y0, x1, y1 = self.box; return (x0 + (x1 - x0) * p[0], y0 + (y1 - y0) * p[1])
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); al = int(255 * a); x0, y0, x1, y1 = self.box
        d.rounded_rectangle([x0 - 30, y0 - 30, x1 + 30, y1 + 50], 16, fill=(26, 30, 34, int(al * 0.92)), outline=(60, 66, 72, al), width=2)
        for gx in range(int(x0), int(x1), 40): d.line([(gx, y0 - 20), (gx, y1 + 20)], fill=(34, 40, 46, al), width=1)
        for gy in range(int(y0), int(y1), 40): d.line([(x0 - 20, gy), (x1 + 20, gy)], fill=(34, 40, 46, al), width=1)
        for j, r in enumerate(self.rooms):
            ra = int(al * ease((t - self.t0 - 0.08 * j) / 0.4))
            if ra <= 0: continue
            p0, p1 = self.P(r[:2]), self.P(r[2:4])
            hl = len(r) > 5 and r[5]
            d.rectangle([p0, p1], fill=((60, 40, 36) if hl else (36, 42, 48)) + (ra,), outline=(180, 196, 210, ra), width=3)
            f = font(OSW, r[6] if len(r) > 6 else 30, 500)
            ls = r[4].split("\n"); lh = f.size * 1.1
            for q, l in enumerate(ls):
                d.text(((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 + (q - (len(ls) - 1) / 2) * lh), l, font=f, fill=(200, 210, 220, ra), anchor="mm")
        for pts, ts, dur in self.path:
            if t < ts: continue
            P = [self.P(p) for p in pts]
            L = [0.0]
            for p, q in zip(P, P[1:]): L.append(L[-1] + math.dist(p, q))
            f = ease_io((t - ts) / dur) * L[-1]
            acc = 0.0; last = P[0]
            for j in range(1, len(P)):
                seg = L[j] - L[j - 1]
                if acc >= f: break
                u1 = min(1.0, (f - acc) / max(1e-6, seg))
                n = max(1, int(seg * u1 / 5))
                for i in range(n):
                    a0, a1 = u1 * i / n, u1 * (i + 1) / n
                    if int((acc + seg * a0) / 18) % 2 == 0:
                        d.line([(P[j - 1][0] + (P[j][0] - P[j - 1][0]) * a0, P[j - 1][1] + (P[j][1] - P[j - 1][1]) * a0),
                                (P[j - 1][0] + (P[j][0] - P[j - 1][0]) * a1, P[j - 1][1] + (P[j][1] - P[j - 1][1]) * a1)], fill=RED + (al,), width=6)
                last = (P[j - 1][0] + (P[j][0] - P[j - 1][0]) * u1, P[j - 1][1] + (P[j][1] - P[j - 1][1]) * u1)
                acc += seg
            r = 14; d.ellipse([last[0] - r, last[1] - r, last[0] + r, last[1] + r], fill=REDL + (al,), outline=WHITE + (al,), width=3)
        for xy, label, tm, kind in self.marks:
            if t < tm: continue
            x, y = self.P(xy); ma = int(al * ease((t - tm) / 0.3)); s = back((t - tm) / 0.3)
            if kind == "x":
                r = 16 * s; d.line([(x - r, y - r), (x + r, y + r)], fill=GOLD + (ma,), width=7); d.line([(x - r, y + r), (x + r, y - r)], fill=GOLD + (ma,), width=7)
            elif kind == "lock":
                d.rounded_rectangle([x - 18 * s, y - 6 * s, x + 18 * s, y + 22 * s], 4, fill=GOLD + (ma,))
                d.arc([x - 12 * s, y - 26 * s, x + 12 * s, y + 6 * s], 180, 360, fill=GOLD + (ma,), width=6)
            elif kind == "dot":
                d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=GOLD + (ma,))
            if label:
                f = font(PS, 28); tw = tl(d, label, f)
                d.rounded_rectangle([x + 26, y - 22, x + 26 + tw + 24, y + 22], 10, fill=(14, 12, 11, int(ma * 0.85)))
                d.text((x + 38, y), label, font=f, fill=WHITE + (ma,), anchor="lm")
        if self.title:
            d.text((x1 + 18, y1 + 38), self.title, font=font(COURR, 20), fill=(150, 160, 170, al), anchor="rs")

# ---------------------------------------------------------------- bacheca investigativa
_card_c = {}
def person_card(name, role, w=250, seed=1):
    key = (name, role, w)
    if key in _card_c: return _card_c[key]
    h = int(w * 1.3)
    im = paper(w, h, (226, 220, 206), seed, 0.4); d = ImageDraw.Draw(im)
    pw = w - 30; ph = int(h * 0.62)
    d.rectangle([15, 15, 15 + pw, 15 + ph], fill=(70, 66, 62, 255))
    silhouette(d, 15 + pw / 2, 15 + ph * 1.0, pw * 0.72, (36, 33, 30))
    f = font(OSW, int(w * 0.13), 600)
    nm = name
    while tl(d, nm, f) > w - 20 and f.size > 14: f = font(OSW, f.size - 2, 600)
    d.text((w / 2, 15 + ph + 12), nm, font=f, fill=INK + (255,), anchor="ma")
    f2 = font(COURR, int(w * 0.075))
    d.text((w / 2, 15 + ph + 18 + f.size), role, font=f2, fill=(100, 90, 80, 255), anchor="ma")
    _card_c[key] = im
    return im

class Board(El):
    """nodes: dict key -> dict(xy, name, role, t, rot, stamp=(testo, t, colore)); links: (a, b, t)"""
    def __init__(self, nodes, links, t0, t1=None, cw=230):
        super().__init__(t0, t1, 0.3); self.nodes, self.links, self.cw = nodes, links, cw
        self.cards = {k: Img(person_card(n["name"], n["role"], cw, seed=hash(k) % 50).rotate(n.get("rot", 0), expand=True, resample=Image.BICUBIC),
                             n["xy"], n["t"], None, "drop") for k, n in nodes.items()}
        self.stamps = {k: Stamp(n["stamp"][0], (n["xy"][0], n["xy"][1] + cw * 0.35), n["stamp"][1], None,
                                n["stamp"][2] if len(n["stamp"]) > 2 else RED, int(cw * 0.2), -12)
                       for k, n in nodes.items() if n.get("stamp")}
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); al = int(255 * a)
        for a_, b_, tt in self.links:
            if t < tt: continue
            p, q = self.nodes[a_]["xy"], self.nodes[b_]["xy"]
            p = (p[0], p[1] - self.cw * 0.55); q = (q[0], q[1] - self.cw * 0.55)
            f = ease((t - tt) / 0.6)
            d.line([p, (p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f)], fill=(190, 40, 34, al), width=5)
        for k, c in self.cards.items():
            ca = c.alpha(t) * a
            if ca > 0.01:
                c.draw(lay, t, ca)
                x, y = self.nodes[k]["xy"]; py = y - self.cw * 0.55
                d.ellipse([x - 13, py - 13, x + 13, py + 13], fill=(200, 40, 34, int(255 * ca)), outline=(255, 160, 150, int(255 * ca)), width=2)
        for k, s in self.stamps.items():
            sa = s.alpha(t) * a
            if sa > 0.01: s.draw(lay, t, sa)

# ---------------------------------------------------------------- archivio schede
class CardGrid(El):
    def __init__(self, box, t0, t1=None, cols=18, rows=8, scan=3.0):
        super().__init__(t0, t1, 0.4); self.box, self.cols, self.rows, self.scan = box, cols, rows, scan
        rng = random.Random(3); self.tone = [[rng.randint(150, 200) for _ in range(cols)] for _ in range(rows)]
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); x0, y0, x1, y1 = self.box; al = int(255 * a)
        cw = (x1 - x0) / self.cols; ch = (y1 - y0) / self.rows
        k = (t - self.t0)
        for r in range(self.rows):
            for c in range(self.cols):
                appear = self.t0 + 0.015 * (r * self.cols + c)
                if t < appear: continue
                v = self.tone[r][c]
                bx, by = x0 + c * cw + 4, y0 + r * ch + 4
                d.rectangle([bx, by, bx + cw - 8, by + ch - 8], fill=(v, v - 8, v - 22, int(al * 0.9)))
                d.line([(bx + 8, by + 14), (bx + cw - 22, by + 14)], fill=(90, 80, 70, al), width=3)
                d.line([(bx + 8, by + 26), (bx + cw - 34, by + 26)], fill=(110, 100, 90, al), width=2)
        u = min(1.0, k / self.scan)
        idx = int(u * self.rows * self.cols * 0.999)
        r, c = idx // self.cols, idx % self.cols
        if 0 < u < 1:
            mx, my = x0 + (c + 0.5) * cw, y0 + (r + 0.5) * ch; R = cw * 0.9
            d.ellipse([mx - R, my - R, mx + R, my + R], outline=GOLD + (al,), width=8)
            d.line([(mx + R * 0.7, my + R * 0.7), (mx + R * 1.3, my + R * 1.3)], fill=GOLD + (al,), width=16)

# ---------------------------------------------------------------- baule
class Trunk(El):
    def __init__(self, xy, w, t0, t1=None, open_t=None, reveal=None):
        super().__init__(t0, t1, 0.3); self.xy, self.w, self.open_t, self.reveal = xy, w, open_t, reveal
    def draw(self, lay, t, a):
        d = ImageDraw.Draw(lay); al = int(255 * a); cx, cy = self.xy; w = self.w; h = w * 0.55
        x0, y0 = cx - w / 2, cy - h / 2
        o = ease((t - self.open_t) / 0.6) if self.open_t and t > self.open_t else 0
        brown, dark, metal = (110, 72, 42), (70, 46, 28), (180, 150, 90)
        if self.reveal is not None and t > self.reveal:
            ra = ease((t - self.reveal) / 0.8)
            fh = h * 0.8
            fw = fh * 0.69
            fx, fy = cx - fw / 2, y0 - fh * 0.9 * ra + h * 0.1
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=(96, 70, 40, int(al * ra)))
            d.rectangle([fx + 12, fy + 12, fx + fw - 12, fy + fh - 12], fill=(64, 66, 48, int(al * ra)))
            silhouette(d, cx, fy + fh - 14, fw * 0.6, (34, 28, 22), int(al * ra))
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=brown + (al,), outline=dark + (al,), width=6)
        for k in (0.25, 0.75):
            d.rectangle([x0 + w * k - 14, y0, x0 + w * k + 14, y0 + h], fill=dark + (al,))
        d.rectangle([x0, y0 + h * 0.78, x0 + w, y0 + h * 0.84], fill=(150, 110, 60, al))
        if o > 0:
            d.text((cx, y0 + h * 0.66), "doppio fondo", font=font(TYPE, int(w * 0.07)), fill=GOLD + (int(al * o),), anchor="mm")
        lid_h = h * 0.32
        lift = lid_h * 2.2 * o
        d.polygon([(x0 - 8, y0 - lid_h - lift), (x0 + w + 8, y0 - lid_h - lift * 1.4), (x0 + w + 8, y0 - lift * 1.4), (x0 - 8, y0 - lift)], fill=(130, 86, 50, al), outline=dark + (al,))
        d.rounded_rectangle([cx - 26, y0 - 18 - lift * 1.2, cx + 26, y0 + 24 - lift * 1.2], 6, fill=metal + (al,))

# ---------------------------------------------------------------- scena
class Scene:
    def __init__(self, dur):
        self.dur = dur; self.items = []; self.sfx = []; self.footer = ""
    def add(self, el, sfx=None):
        self.items.append(el)
        if sfx: self.sfx.append((el.t0, sfx))
        if isinstance(el, Text) and el.typewriter: self.sfx.append((el.t0, "type:%.2f" % el.tdur))
        if isinstance(el, Stamp): self.sfx.append((el.t0, "stamp"))
        return el
    def board(self, *a, **k):
        b = self.add(Board(*a, **k))
        for n in b.nodes.values():
            self.sfx.append((n["t"], "paper"))
            if n.get("stamp"): self.sfx.append((n["stamp"][1], "stamp"))
        return b

def render_items(lay, sc, t):
    for el in sc.items:
        a = el.alpha(t)
        if a > 0.01: el.draw(lay, t, a)

class Clock:
    def __init__(self, words, a): self.w, self.a = words, a
    def __call__(self, prefix, nth=0, end=False):
        hits = [w for w in self.w if w[0].lower().startswith(prefix.lower())]
        if not hits: raise KeyError(prefix)
        w = hits[min(nth, len(hits) - 1)]
        return self.a + (w[2] if end else w[1])

# ---------------------------------------------------------------- logo
def logo_mark(size, color=RED):
    """monogramma: cartellina con FI"""
    S = size * 4; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    tab = [(S * 0.08, S * 0.22), (S * 0.40, S * 0.22), (S * 0.47, S * 0.12), (S * 0.08, S * 0.12)]
    d.polygon(tab, fill=color + (255,))
    d.rounded_rectangle([S * 0.08, S * 0.20, S * 0.92, S * 0.86], int(S * 0.04), fill=color + (255,))
    d.text((S * 0.5, S * 0.55), "FI", font=font(SERIF, int(S * 0.48)), fill=(20, 18, 16, 255), anchor="mm")
    return im.resize((size, size), Image.LANCZOS)

def wordmark(h, sub=True):
    S = 3; HH = h * S
    m = logo_mark(HH)
    f1 = font(OSW, int(HH * 0.46), 700); f2 = font(COUR, int(HH * 0.16))
    t1 = "FASCICOLO"; t2 = "ITALIA"; sp = int(HH * 0.02)
    w1 = sum(tl(_tmpd, c, f1) + sp for c in t1); w2 = sum(tl(_tmpd, c, f1) + sp for c in t2)
    Wd = int(HH * 1.08 + w1 + HH * 0.14 + w2 + HH * 0.1)
    im = Image.new("RGBA", (Wd, HH), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    im.alpha_composite(m, (0, 0))
    x = HH * 1.04; y = HH * 0.40 if sub else HH * 0.5
    for c in t1: d.text((x, y), c, font=f1, fill=WHITE + (255,), anchor="lm"); x += tl(d, c, f1) + sp
    x += HH * 0.12
    for c in t2: d.text((x, y), c, font=f1, fill=RED + (255,), anchor="lm"); x += tl(d, c, f1) + sp
    if sub: d.text((HH * 1.06, HH * 0.80), "COLPI · TRUFFE · MISTERI ITALIANI", font=f2, fill=GREY + (255,), anchor="lm")
    return im.resize((Wd // S, h), Image.LANCZOS)
