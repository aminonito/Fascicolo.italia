STYLE = "fascicolo"
CASE = "FASCICOLO N. 026 · IL CRAC VALLESUSA"
TITLE = "Il crac Vallesusa"
CH = ["INTRO", "1 · LEGNANO E IL COTONE", "2 · I PROTAGONISTI", "3 · IL GIOVANE PADRONE", "4 · IL MILAN", "5 · LE CREPE",
      "6 · IL CRAC", "7 · L'ARRESTO", "8 · LA FUGA", "9 · BEIRUT", "10 · IL RITORNO E I CONTI",
      "11 · LE DOMANDE APERTE", "12 · LA LEZIONE", "IL VERDETTO"]
import re

def S(ch, text):
    """divide il testo in frasi (punto, punto di domanda, due punti) senza toccare le parentesi [display|parlato]"""
    from num2words import num2words
    parts = re.split(r"(\[[^\]]*\])", text)
    text = "".join(q if q.startswith("[") else re.sub(r"\b(\d+)\b", lambda m: f"[{m.group(1)}|{num2words(int(m.group(1)), lang='it')}]", q) for q in parts)
    text = re.sub(r"\[([^|\]]*)\|([^\]]*)\]([.,:;?!])", r"[\1\3|\2\3]", text)
    out, cur, depth = [], "", 0
    for k, c in enumerate(text):
        cur += c
        if c == "[": depth += 1
        elif c == "]": depth -= 1
        nxt = text[k + 1] if k + 1 < len(text) else " "
        if depth == 0 and c in ".?:!" and nxt == " ":
            out.append([cur.strip(), .3]); cur = ""
        elif depth == 0 and c == "]" and cur.rstrip("]").endswith((".", "?", ":")) and nxt == " ":
            out.append([cur.strip(), .3]); cur = ""
    if cur.strip(): out.append([cur.strip(), .3])
    out[-1][1] = .6
    return (ch, [tuple(p) for p in out])

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import SC
SCENES_H = [S(ch, t) for ch, t, _ in SC]
SCENES = [p for _, p in SCENES_H]
HEADERS = [CH[h] for h, _ in SCENES_H]

def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
