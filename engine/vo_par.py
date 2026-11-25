# Voce in parallelo, a prova di sovrapposizioni. Uso (dalla cartella del video):
#   for k in 0 1 2 3; do python3 vo_par.py <k> 4 [velocità] & done; wait     <- SEMPRE "wait" prima di vo_merge
#   python3 vo_merge.py
# Ogni scena è salvata in vocache/<hash del testo>.wav + .json: se le scene vengono spostate, aggiunte o tolte
# la voce già fatta si riusa da sola (niente remap a mano) e una scena modificata ha un hash nuovo -> voce nuova.
# audio/ NON viene toccata qui: la riempie solo vo_merge.py.
import soundfile as sf, numpy as np, json, sys, os, hashlib
sys.path.insert(0, os.getcwd())
from kokoro_onnx import Kokoro
from script import SCENES, tokens
K, N = int(sys.argv[1]), int(sys.argv[2])
SPEED = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
VOICE = os.environ.get("VOICE", "im_nicola")
SR = 24000
def key_of(sc): return json.dumps({"sc": sc, "speed": SPEED, "voice": VOICE}, ensure_ascii=False)
def hid(sc): return hashlib.sha1(key_of(sc).encode()).hexdigest()[:16]
os.makedirs("vocache", exist_ok=True)
k = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
def trim(a):
    idx = np.where(np.abs(a) > 0.008)[0]
    return a[max(0, idx[0] - 300): idx[-1] + 600]
for si, sc in enumerate(SCENES):
    h = hid(sc)
    if si % N != K or os.path.exists(f"vocache/{h}.json"): continue
    buf = []; t = 0.0; words = []
    for cl, pause in sc:
        tk = tokens(cl); spoken = " ".join(s for d, s in tk if s)
        a, _ = k.create(spoken, voice=VOICE, speed=SPEED, lang="it"); a = trim(a); dur = len(a) / SR
        wts = [max(1, len(k.tokenizer.phonemize(s, "it").replace(" ", ""))) if s else 0 for d, s in tk]
        tot = sum(wts); lead = 0.04; body = dur - lead - 0.05; c = t + lead
        for (d, s), w in zip(tk, wts):
            dd = body * w / tot
            if d: words.append((d, round(c, 3), round(c + dd, 3)))
            c += dd
        buf.append(a); buf.append(np.zeros(int(pause * SR), np.float32)); t += dur + pause
    full = np.concatenate(buf).astype(np.float32)
    # scrittura atomica: prima il wav, poi il json; mai file a metà
    sf.write(f"vocache/{h}.tmp.wav", full, SR); os.replace(f"vocache/{h}.tmp.wav", f"vocache/{h}.wav")
    json.dump({"dur": len(full) / SR, "n": len(full), "words": words, "key": key_of(sc)},
              open(f"vocache/{h}.tmp.json", "w"), ensure_ascii=False)
    os.replace(f"vocache/{h}.tmp.json", f"vocache/{h}.json")
    print(si, round(len(full) / SR, 1), flush=True)
