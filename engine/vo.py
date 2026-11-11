# Voce narrante FASCICOLO ITALIA (Kokoro, voce fissa im_nicola). Uso: python3 vo.py [velocità]
import soundfile as sf, numpy as np, json, sys, os
sys.path.insert(0, os.getcwd())
from kokoro_onnx import Kokoro
from script import SCENES, tokens
k = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
VOICE = os.environ.get("VOICE", "im_nicola")
SPEED = float(sys.argv[1]) if len(sys.argv) > 1 else 1.1
SR = 24000
os.makedirs("audio", exist_ok=True)
def trim(a):
    idx = np.where(np.abs(a) > 0.008)[0]
    return a[max(0, idx[0] - 300): idx[-1] + 600]
meta = []
for si, sc in enumerate(SCENES):
    buf = []; t = 0.0; words = []
    for cl, pause in sc:
        tk = tokens(cl)
        spoken = " ".join(s for d, s in tk if s)
        a, _ = k.create(spoken, voice=VOICE, speed=SPEED, lang="it"); a = trim(a)
        dur = len(a) / SR
        wts = [max(1, len(k.tokenizer.phonemize(s, "it").replace(" ", ""))) if s else 0 for d, s in tk]
        tot = sum(wts); lead = 0.04; body = dur - lead - 0.05; c = t + lead
        for (d, s), w in zip(tk, wts):
            dd = body * w / tot
            if d: words.append((d, round(c, 3), round(c + dd, 3)))
            c += dd
        buf.append(a); buf.append(np.zeros(int(pause * SR), np.float32)); t += dur + pause
    full = np.concatenate(buf)
    sf.write(f"audio/s{si}.wav", full, SR)
    meta.append({"dur": len(full) / SR, "words": words})
    print(si, round(len(full) / SR, 1), flush=True)
json.dump(meta, open("vo.json", "w"), ensure_ascii=False, indent=0)
print("TOT", round(sum(m["dur"] for m in meta), 1))
