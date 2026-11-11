# Musica (ambient investigativo, generata) + effetti + traccia voce. Uso: python3 audio.py (dopo render.py events)
import json, numpy as np, soundfile as sf, os
from scipy.signal import butter, sosfilt
SR = 48000
E = json.load(open("events.json")); TOT = E["total"]
n = int(TOT * SR) + SR
rng = np.random.default_rng(7)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)
def lp(x, f): return sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
def hp(x, f): return sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)
mid = lambda m: 440 * 2 ** ((m - 69) / 12)

# ---------------- musica: re minore, lenta, tesa ----------------
mus = np.zeros(n)
def add(buf, sig, t0, amp):
    s = int(t0 * SR); e = min(len(buf), s + len(sig))
    if e > s: buf[s:e] += amp * sig[:e - s]
bar = 4.0  # secondi per accordo
prog = [[50, 57, 62, 65], [46, 53, 58, 62], [43, 50, 55, 58], [45, 52, 57, 61]]  # Dm Bb Gm A
t = 0.0; k = 0
while t < TOT + bar:
    ch = prog[k % 4]; L = int(bar * 1.15 * SR); tt = np.arange(L) / SR
    env = np.minimum(1, tt / 1.2) * np.minimum(1, (bar * 1.15 - tt) / 1.2)
    pad = sum(np.sin(2 * np.pi * mid(m) * dt * tt + ph) for m in ch for dt, ph in ((1, 0), (1.003, 1.3))) / 8
    add(mus, lp(pad * env, 1800), t, 0.10)
    bass = np.sin(2 * np.pi * mid(ch[0] - 12) * tt) * env
    add(mus, bass, t, 0.10)
    # pulsazione bassa (battito)
    for b in (0, 2):
        Lk = int(0.5 * SR); tk = np.arange(Lk) / SR
        kick = np.sin(2 * np.pi * (45 + 30 * np.exp(-tk * 20)) * tk) * np.exp(-tk * 9)
        add(mus, kick, t + b, 0.16 if b == 0 else 0.09)
    # note di pianoforte rade
    if k % 2 == 1:
        for j, m in enumerate(rng.choice([62, 65, 69, 72, 74, 77], 2, replace=False)):
            Lp = int(2.5 * SR); tp = np.arange(Lp) / SR
            pn = (np.sin(2 * np.pi * mid(m) * tp) + 0.3 * np.sin(2 * np.pi * 2 * mid(m) * tp)) * np.exp(-tp * 1.6) * np.minimum(1, tp / 0.005)
            add(mus, pn, t + 1.0 + j * 1.5, 0.05)
    # tic-tac leggero
    for b in range(8):
        Lt = int(0.03 * SR); tick = hp(rng.normal(0, 1, Lt), 4000) * np.exp(-np.arange(Lt) / SR * 200)
        add(mus, tick, t + b * 0.5, 0.012 if b % 2 else 0.02)
    t += bar; k += 1
air = lp(rng.normal(0, 1, n), 400) * 0.01
mus += air
fade = np.ones(n); fl = int(2.5 * SR); fade[-fl:] = np.linspace(1, 0, fl); fade[:int(1.0 * SR)] = np.linspace(0, 1, int(1.0 * SR))
mus = (mus * fade)[: int(TOT * SR)]
sf.write("audio/music.wav", mus.astype(np.float32), SR)

# ---------------- effetti ----------------
N2 = int(TOT * SR)
fx = np.zeros(N2 + 2 * SR)
for t0, kind in sorted(E["events"], key=lambda e: e[0]):
    if kind.startswith("type:"):
        d = float(kind.split(":")[1]); c = 0.0
        while c < d:
            Lc = int(0.025 * SR); click = bp(rng.normal(0, 1, Lc), 1500, 6000) * np.exp(-np.arange(Lc) / SR * 250)
            add(fx, click, t0 + c, rng.uniform(0.05, 0.09)); c += rng.uniform(0.05, 0.11)
    elif kind == "stamp":
        L = int(0.35 * SR); tt = np.arange(L) / SR
        thud = np.sin(2 * np.pi * (70 + 60 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 14)
        slap = bp(rng.normal(0, 1, L), 300, 3000) * np.exp(-tt * 45)
        add(fx, thud * 0.5 + slap * 0.35, t0, 0.5)
    elif kind == "paper":
        L = int(0.45 * SR); tt = np.arange(L) / SR
        sig = bp(rng.normal(0, 1, L), 1200, 7000) * np.sin(np.pi * tt / 0.45) ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * tt))
        add(fx, sig, t0, 0.07)
    elif kind == "whoosh":
        L = int(0.6 * SR); tt = np.arange(L) / SR; nz = rng.normal(0, 1, L); out = np.zeros(L)
        for j in range(10):
            a, b = j * L // 10, (j + 1) * L // 10; f = 300 + 2500 * j / 9
            out[a:b] = bp(nz, f * 0.7, f * 1.3)[a:b]
        add(fx, out * np.sin(np.pi * tt / 0.6) ** 2, max(0, t0 - 0.2), 0.16)
    elif kind == "hit":
        L = int(1.6 * SR); tt = np.arange(L) / SR
        boom = np.sin(2 * np.pi * (40 + 25 * np.exp(-tt * 6)) * tt) * np.exp(-tt * 2.5)
        add(fx, boom + 0.15 * lp(rng.normal(0, 1, L), 900) * np.exp(-tt * 5), t0, 0.35)
    elif kind == "pop":
        L = int(0.1 * SR); tt = np.arange(L) / SR
        add(fx, np.sin(2 * np.pi * (380 + 300 * tt / 0.1) * tt) * np.exp(-tt * 40), t0, 0.12)
fx = fx[:N2]
sf.write("audio/sfx.wav", fx.astype(np.float32), SR)

# ---------------- voce ----------------
vo = np.zeros(N2)
for i, st in enumerate(E["starts"]):
    a, sr = sf.read(f"audio/s{i}.wav", dtype="float32")
    a = np.interp(np.arange(int(len(a) * SR / sr)) * sr / SR, np.arange(len(a)), a)
    s = int((st + E["lead"][i]) * SR); e = min(N2, s + len(a)); vo[s:e] += a[:e - s]
sf.write("audio/voice.wav", vo.astype(np.float32), SR)
print("audio ok", round(TOT, 1))
