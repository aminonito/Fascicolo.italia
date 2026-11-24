import json, sys, os
sys.path.insert(0, os.getcwd())
from script import SCENES
meta = []
for si, sc in enumerate(SCENES):
    m = json.load(open(f"vometa/{si}.json"))
    assert m["key"] == json.dumps(sc, ensure_ascii=False), f"scena {si} cambiata: rifare"
    meta.append({"dur": m["dur"], "words": m["words"]})
json.dump(meta, open("vo.json", "w"), ensure_ascii=False, indent=0)
print("TOT", round(sum(m["dur"] for m in meta), 1))
