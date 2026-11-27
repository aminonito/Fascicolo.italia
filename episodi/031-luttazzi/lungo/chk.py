import json, re, sys
from data import SC
vo = json.load(open("vo.json"))
cs = lambda s: re.sub(r"[^\w']", "", s.lower())
fix = {}
for i, (ch, t, b) in enumerate(SC):
    ws = [cs(w[0]) for w in vo[i]["words"]]
    for w, c in b:
        p = cs(w)
        if any(x == p for x in ws) or any(x.startswith(p) for x in ws): continue
        cand = [x for x in ws if ("'" + p) in x or x.split("'")[-1].startswith(p)]
        print(i, repr(w), "->", cand[:1])
        if cand: fix[(i, w)] = cand[0]
if "--fix" in sys.argv:
    s = open("data.py").read().split("\n")
    # data lines: one scene per line starting with ' (' ; map scene index to line
    idx = [k for k, l in enumerate(s) if l.startswith(" (") and re.match(r" \(\d+,", l)]
    for (i, w), new in fix.items():
        k = idx[i]; s[k] = s[k].replace("('" + w + "',", '("' + new + '",', 1)
    open("data.py", "w").write("\n".join(s))
