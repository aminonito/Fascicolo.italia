# Controllo finale anti-voci-sovrapposte sul file video. Uso: python3 check_voice.py video.mp4
# Una sola voce Kokoro non parla mai più di ~7 s senza una pausa: un tratto di parlato continuo molto più lungo
# (o due attacchi di voce sovrapposti) vuol dire due scene che parlano insieme. Esce con errore se lo trova.
import sys, subprocess, numpy as np
from scipy.signal import butter, sosfilt
SR = 16000; LIM = 10.5
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
a = sosfilt(butter(4, [300, 3400], "band", fs=SR, output="sos"), np.frombuffer(raw, np.float32).astype(np.float64))
hop = SR // 100; fr = len(a) // hop
db = 20 * np.log10(np.sqrt((a[:fr * hop].reshape(fr, hop) ** 2).mean(1)) + 1e-7)
v = db > np.percentile(db, 95) - 22
bad = []; s = None; gap = 0
for i, x in enumerate(np.append(v, [False] * 20)):
    if x:
        s = i if s is None else s; gap = 0
    elif s is not None:
        gap += 1
        if gap >= 12:
            L = (i - gap - s) / 100
            if L > LIM: bad.append((s / 100, L))
            s = None; gap = 0
for t, L in bad: print(f"  parlato continuo di {L:.1f}s a {int(t//60)}:{int(t%60):02d}: voci sovrapposte?")
if bad: sys.exit("STOP: possibili voci sovrapposte, NON pubblicare: rifare vo_merge + build")
print("voce ok: nessuna sovrapposizione")
