# voce solo per le scene nuove o cambiate; riusa l'audio delle scene già pronte (stesso testo)
import json, os, shutil, sys
sys.path.insert(0, os.getcwd())
import soundfile as sf, numpy as np
from script import SCENES, tokens
old = json.load(open("scenes_old.json")); oldmeta = json.load(open("vo_old.json"))
key = lambda sc: json.dumps([[c, p] for c, p in sc], ensure_ascii=False)
oldidx = {key(sc): i for i, sc in enumerate(old)}
from kokoro_onnx import Kokoro
k = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
SR = 24000
def trim(a):
    idx = np.where(np.abs(a) > 0.008)[0]
    return a[max(0, idx[0] - 300): idx[-1] + 600]
os.makedirs("audio", exist_ok=True); meta = []
for si, sc in enumerate(SCENES):
    kk = key([list(p) for p in sc])
    if kk in oldidx:
        j = oldidx[kk]; shutil.copy(f"audio_old/s{j}.wav", f"audio/s{si}.wav"); meta.append(oldmeta[j]); continue
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
    meta.append({"dur": len(full) / SR, "words": words}); print("NEW", si, round(len(full) / SR, 1), flush=True)
json.dump(meta, open("vo.json", "w"), ensure_ascii=False, indent=0)
print("TOT", round(sum(m["dur"] for m in meta), 1))
