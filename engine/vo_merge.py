# Unisce la voce: svuota audio/s*.wav, copia dalla cache la voce di OGNI scena attuale e scrive vo.json.
# Si ferma se manca una scena, se un file è incoerente o se un vo_par.py/vo.py è ancora in esecuzione.
import json, sys, os, soundfile as sf, shutil
sys.path.insert(0, os.getcwd())
SPEED = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
os.environ.setdefault("VOICE", "im_nicola")
from script import SCENES
def voice_procs():
    out = []
    for p in os.listdir("/proc"):
        if not p.isdigit() or int(p) == os.getpid(): continue
        try: argv = open(f"/proc/{p}/cmdline", "rb").read().decode(errors="ignore").split("\0")
        except OSError: continue
        if argv and "python" in os.path.basename(argv[0]) and any(os.path.basename(x) in ("vo_par.py", "vo.py") for x in argv[1:3]):
            out.append(p)
    return out
run = voice_procs()
if run: sys.exit(f"STOP: processi voce ancora attivi {run}: aspetta che finiscano (wait) e rilancia")
VOICE = os.environ["VOICE"]
import hashlib
def key_of(sc): return json.dumps({"sc": sc, "speed": SPEED, "voice": VOICE}, ensure_ascii=False)
miss = [si for si, sc in enumerate(SCENES) if not os.path.exists(f"vocache/{hashlib.sha1(key_of(sc).encode()).hexdigest()[:16]}.json")]
if miss: sys.exit(f"STOP: manca la voce delle scene {miss}: rilancia vo_par.py (velocità {SPEED})")
os.makedirs("audio", exist_ok=True)
for f in os.listdir("audio"):
    if f.startswith("s") and f.endswith(".wav") and f[1:-4].isdigit(): os.remove("audio/" + f)
meta = []
for si, sc in enumerate(SCENES):
    h = hashlib.sha1(key_of(sc).encode()).hexdigest()[:16]; m = json.load(open(f"vocache/{h}.json"))
    assert m["key"] == key_of(sc), f"scena {si}: cache incoerente"
    info = sf.info(f"vocache/{h}.wav"); assert info.frames == m["n"], f"scena {si}: wav e json non coincidono"
    shutil.copy(f"vocache/{h}.wav", f"audio/s{si}.wav")
    meta.append({"dur": m["dur"], "words": m["words"]})
json.dump(meta, open("vo.json", "w"), ensure_ascii=False, indent=0)
print("scene", len(meta), "TOT", round(sum(m["dur"] for m in meta), 1))
