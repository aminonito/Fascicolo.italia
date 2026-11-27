STYLE = "fascicolo"
CASE = "FASCICOLO N. 030 · LA SALIERA DI CELLINI"
TITLE = "La Saliera di Cellini"
CH = ["INTRO", "1 · L'EPOCA E IL LUOGO", "2 · I PROTAGONISTI", "3 · CELLINI E LA SALIERA", "4 · LA NOTTE DEL FURTO", "5 · LA SCOPERTA",
      "6 · L'INDAGINE E IL RISCATTO", "7 · LA SVOLTA", "8 · IL PROCESSO", "9 · COSA È SUCCESSO DOPO", "10 · LE DOMANDE APERTE", "11 · LA LEZIONE", "IL VERDETTO"]
import re

def S(ch, text):
    """divide il testo in frasi (punto, punto di domanda, due punti) senza toccare le parentesi [display|parlato]"""
    from num2words import num2words
    parts = re.split(r"(\[[^\]]*\])", text)
    PRON = {"Wilfried": "Vìlfrid", "Gehrer": "Ghèrer", "Elisabeth": "Elìsabet", "Louvre": "Lùvr", "Robert": "Ròbert", "Der Standard": "Der Stàndard", "Ambras": "Àmbras", "Clemente": "Clemènte", "AP": "a pi"}
    def pr(q):
        for k_, v_ in PRON.items():
            q = re.sub(r"\b" + k_ + r"\b([.,:;?!]?)", lambda m: "[" + k_ + m.group(1) + "|" + v_ + m.group(1) + "]", q)
        return q
    parts = re.split(r"(\[[^\]]*\])", text)
    text = "".join(q if q.startswith("[") else pr(q) for q in parts)
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
