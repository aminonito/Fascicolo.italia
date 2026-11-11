# Render FASCICOLO ITALIA. Uso (nella cartella episodio): python3 render.py preview|scene N|events|chapters
import sys, json, os, subprocess, re
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import script as S
FORMAT = getattr(S, "FORMAT", "long")
import fi
if FORMAT == "reel": fi.configure(1080, 1920, 30)
else: fi.configure(1920, 1080, 24)
from fi import *
from PIL import Image, ImageDraw, ImageFilter
from scenes import build

W, H, FPS = fi.W, fi.H, fi.FPS
meta = json.load(open("vo.json"))
N = len(meta)
OUTRO = 3.0 if FORMAT == "long" else 2.2
LEAD = [0.5] + [0.35] * (N - 1)
TAIL = 0.55
frames = []
for i, m in enumerate(meta):
    d = LEAD[i] + m["dur"] + (0.6 + OUTRO if i == N - 1 else TAIL)
    frames.append(int(round(d * FPS)))
STARTS = [sum(frames[:i]) / FPS for i in range(N)]
TOTAL = sum(frames) / FPS
BGI = fi.make_bg()
GRAINS = fi.make_grains(1)
WM = fi.wordmark(58 if FORMAT == "long" else 70, sub=False)
WM_BIG = fi.wordmark(150 if FORMAT == "long" else 120, sub=True)
HEADERS = getattr(S, "HEADERS", [""] * N)

# ---------- sottotitoli
CAP_Y = H - 118 if FORMAT == "long" else 1430
CF = font(PS, 50) if FORMAT == "long" else font(PB, 66)
MAXC = 36 if FORMAT == "long" else 18
def pages(words):
    clauses, cur = [], []
    for w in words:
        cur.append(w)
        if re.search(r"[.?:!,]$", w[0]): clauses.append(cur); cur = []
    if cur: clauses.append(cur)
    out = []
    for cl in clauses:
        parts, cur = [], []
        for w in cl:
            if cur and (len(cur) >= (6 if FORMAT == "long" else 3) or len(" ".join(x[0] for x in cur + [w])) > MAXC):
                parts.append(cur); cur = []
            cur.append(w)
        if cur: parts.append(cur)
        if len(parts) > 1 and len(parts[-1]) == 1 and len(parts[-2]) >= 3:
            parts[-1].insert(0, parts[-2].pop())
        out += parts
    return out
CAP = []
for i, m in enumerate(meta):
    ws = [(w, s + LEAD[i], e + LEAD[i]) for w, s, e in m["words"]]
    ps = pages(ws); lst = []
    for k, p in enumerate(ps):
        t1 = ps[k + 1][0][1] if k + 1 < len(ps) else p[-1][2] + 0.35
        lst.append((p[0][1], t1, p))
    CAP.append(lst)
_cc = {}
def caption_img(p, active):
    key = (tuple(w[0] for w in p), active)
    if key in _cc: return _cc[key]
    d0 = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    sp = d0.textlength(" ", font=CF) + 4
    ws = [d0.textlength(w[0], font=CF) for w in p]
    tw = int(sum(ws) + sp * (len(p) - 1)) + 60; th = int(CF.size * 1.9)
    im = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sh = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    x = 30
    for k, (w, wd) in enumerate(zip(p, ws)):
        col = REDL if k == active else WHITE
        ds.text((x + 2, th / 2 + 4), w[0], font=CF, fill=(0, 0, 0, 230), anchor="lm", stroke_width=3 if FORMAT == "reel" else 0, stroke_fill=(0, 0, 0, 230))
        d.text((x, th / 2), w[0], font=CF, fill=col + (255,), anchor="lm", stroke_width=4 if FORMAT == "reel" else 0, stroke_fill=(12, 10, 9, 255))
        x += wd + sp
    sh = sh.filter(ImageFilter.GaussianBlur(5)); sh.alpha_composite(im)
    _cc[key] = sh
    return sh
def draw_caption(img, i, t):
    for t0, t1, p in CAP[i]:
        if t0 <= t < t1:
            act = 0
            for k, w in enumerate(p):
                if t >= w[1]: act = k
            im = caption_img(p, act)
            mw = W - 120
            if im.width > mw: im = im.resize((mw, int(im.height * mw / im.width)), Image.LANCZOS)
            img.alpha_composite(im, (int(W / 2 - im.width / 2), int(CAP_Y - im.height / 2)))
            return

# ---------- intestazione
def make_hdr(label):
    hdr = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(hdr)
    if FORMAT == "long":
        d.text((56, 52), S.CASE, font=font(TYPE, 26), fill=GREY + (255,))
        if label and label != "INTRO":
            d.text((56, 88), label, font=font(OSW, 30, 600), fill=WHITE + (235,))
            d.rectangle([56, 132, 116, 136], fill=RED + (255,))
        hdr.alpha_composite(WM, (W - 50 - WM.width, 44))
    else:
        hdr.alpha_composite(WM, (int(W / 2 - WM.width / 2), 190))
        d.text((W / 2, 300), S.CASE, font=font(TYPE, 30), fill=GREY + (255,), anchor="mm")
    return hdr
HDRS = {h: make_hdr(h) for h in set(HEADERS)}

def frame(i, sc, n, total):
    t = n / FPS
    t_o = total / FPS - OUTRO if i == N - 1 else 1e9
    img = BGI.copy()
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    render_items(lay, sc, min(t, t_o + 0.01))
    import fx
    cam = fx.cam_at(sc, t)
    if cam is None: cx, cy, z = W / 2, H / 2, 1.0 + 0.035 * min(1.0, t / max(1.0, total / FPS))
    else: cx, cy, z = cam
    if abs(z - 1) > 0.002 or cam is not None:
        cw, ch = W / z, H / z
        bx = min(max(0, cx - cw / 2), W - cw); by = min(max(0, cy - ch / 2), H - ch)
        lay = lay.resize((W, H), Image.BILINEAR, box=(bx, by, bx + cw, by + ch))
    fade = 1.0
    if n < 6: fade = n / 6
    if i < N - 1 and n > total - 6: fade = max(0, (total - 1 - n) / 5)
    if t >= t_o: fade *= max(0.0, 1 - (t - t_o) / 0.35)
    if fade < 0.999: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * fade)))
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    if t >= t_o:
        a2 = ease((t - t_o - 0.2) / 0.5)
        if a2 > 0:
            wm = set_alpha(WM_BIG, a2)
            img.alpha_composite(wm, (int(W / 2 - wm.width / 2), int(H * 0.42 - wm.height / 2)))
            msg = "Iscriviti: ogni settimana un nuovo caso." if FORMAT == "long" else "La storia completa è su YouTube"
            d.text((W / 2, H * 0.42 + wm.height / 2 + 70), msg, font=font(PS, 44), fill=WHITE + (int(230 * a2),), anchor="mm")
    else:
        img.alpha_composite(HDRS[HEADERS[i]])
        draw_caption(img, i, t)
        if sc.footer:
            fy = H - 30 if FORMAT == "long" else 1580
            d.text((W / 2, fy), sc.footer, font=font(COURR, 20 if FORMAT == "long" else 24), fill=(120, 112, 104, 255), anchor="mm")
        if FORMAT == "long":
            g = (STARTS[i] + t) / TOTAL
            d.rectangle([0, H - 5, int(W * g), H], fill=RED + (255,))
    img.alpha_composite(GRAINS[n % len(GRAINS)])
    return img.convert("RGB")

def scene(i):
    total = frames[i]
    return build(i, total / FPS, LEAD[i], meta[i]["words"]), total

def render_scene(i):
    sc, total = scene(i)
    tmp = f"scenes/s{i}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                          "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    for n in range(total):
        p.stdin.write(frame(i, sc, n, total).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, f"scenes/s{i}.mp4")

def events():
    ev = []
    for i in range(N):
        sc, total = scene(i)
        for t, k in sc.sfx: ev.append((STARTS[i] + t, k))
        if i == N - 1:
            ev.append((STARTS[i] + total / FPS - OUTRO + 0.1, "whoosh")); ev.append((STARTS[i] + total / FPS - OUTRO + 0.4, "hit"))
    return ev

if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] != "x":
    os.makedirs("scenes", exist_ok=True); os.makedirs("prev", exist_ok=True)
    cmd = sys.argv[1]
    if cmd == "preview":
        idx = [int(x) for x in sys.argv[2:]] or range(N)
        for i in idx:
            sc, total = scene(i)
            for q, frac in enumerate((0.3, 0.92)):
                frame(i, sc, int(total * frac), total).save(f"prev/p{i:02d}_{q}.jpg", quality=80)
        print([round(f / FPS, 1) for f in frames], round(TOTAL, 1))
    elif cmd == "at":
        i = int(sys.argv[2]); sc, total = scene(i)
        for tt in sys.argv[3:]:
            frame(i, sc, int(float(tt) * FPS), total).save(f"prev/a{i:02d}_{tt}.jpg", quality=80)
    elif cmd == "scene":
        render_scene(int(sys.argv[2]))
    elif cmd == "events":
        json.dump({"events": events(), "starts": STARTS, "lead": LEAD, "total": TOTAL}, open("events.json", "w"))
    elif cmd == "chapters":
        for i, h in enumerate(HEADERS):
            if i == 0 or h != HEADERS[i - 1]:
                s = int(STARTS[i]); print(f"{s//60}:{s%60:02d} {h}")
