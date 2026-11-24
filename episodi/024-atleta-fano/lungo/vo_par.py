# voce in parallelo: python3 vo_par.py <k> <n>  -> scene i con i % n == k; meta per scena in vometa/
import soundfile as sf, numpy as np, json, sys, os
sys.path.insert(0, os.getcwd())
from kokoro_onnx import Kokoro
from script import SCENES, tokens
K, N = int(sys.argv[1]), int(sys.argv[2])
k = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
SR = 24000
os.makedirs("audio", exist_ok=True); os.makedirs("vometa", exist_ok=True)
def trim(a):
    idx = np.where(np.abs(a) > 0.008)[0]
    return a[max(0, idx[0] - 300): idx[-1] + 600]
for si, sc in enumerate(SCENES):
    if si % N != K or os.path.exists(f"vometa/{si}.json"): continue
    buf = []; t = 0.0; words = []
    for cl, pause in sc:
        tk = tokens(cl); spoken = " ".join(s for d, s in tk if s)
        a, _ = k.create(spoken, voice="im_nicola", speed=1.0, lang="it"); a = trim(a); dur = len(a) / SR
        wts = [max(1, len(k.tokenizer.phonemize(s, "it").replace(" ", ""))) if s else 0 for d, s in tk]
        tot = sum(wts); lead = 0.04; body = dur - lead - 0.05; c = t + lead
        for (d, s), w in zip(tk, wts):
            dd = body * w / tot
            if d: words.append((d, round(c, 3), round(c + dd, 3)))
            c += dd
        buf.append(a); buf.append(np.zeros(int(pause * SR), np.float32)); t += dur + pause
    full = np.concatenate(buf); sf.write(f"audio/s{si}.wav", full, SR)
    json.dump({"dur": len(full) / SR, "words": words, "key": json.dumps(sc, ensure_ascii=False)}, open(f"vometa/{si}.json", "w"), ensure_ascii=False)
    print(si, round(len(full) / SR, 1), flush=True)
