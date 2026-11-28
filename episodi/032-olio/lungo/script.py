STYLE = "fascicolo"
CASE = "FASCICOLO N. 032 · L'OLIO CHE NON C'ERA"
TITLE = "L'olio che non c'era"
CH = ["INTRO", "1 · L'EPOCA E IL LUOGO", "2 · I PROTAGONISTI", "3 · DAL BRONX A BAYONNE", "4 · IL TRUCCO DEI SERBATOI", "5 · LA SCOMMESSA",
      "6 · IL CROLLO", "7 · I CONTI", "8 · IL PROCESSO", "9 · COSA È SUCCESSO DOPO", "10 · LE DOMANDE APERTE", "11 · LA LEZIONE", "IL VERDETTO"]
import re

def S(ch, text):
    """divide il testo in frasi (punto, punto di domanda, due punti) senza toccare le parentesi [display|parlato]"""
    from num2words import num2words
    parts = re.split(r"(\[[^\]]*\])", text)
    PRON = {"Wall Street Journal": "Uòl Strìt Giòrnal", "Wall Street": "Uòl Strìt", "New York": "Niù Iòrk", "New Jersey": "Niù Gèrsi", "Bayonne": "Baiòn", "American Express": "Amèrican Ekspres", "Warren Buffett": "Uòrren Bàffet", "Buffett": "Bàffet", "Ira Haupt": "Àira Hàupt", "Haupt": "Hàupt", "Williston": "Uìliston", "Beane": "Bìn", "Kennedy": "Kènnedi", "Dallas": "Dàllas", "Food for Peace": "Fud for Pis", "Allied Crude Vegetable Oil Refining Corporation": "Àllaid Crud Vègetabol Oil Rifàining Corporèiscion", "Allied": "Àllaid", "Howard Clark": "Hàuard Clark", "Pulitzer": "Pùlitzer", "Anthony": "Èntoni", "Gobel": "Gòbel", "Omaha": "Òmaha", "Newark": "Niùark", "Manhattan": "Menhèttan", "Bronx": "Bronks", "Norman Miller": "Nòrman Miller", "TIME": "Tàim", "Fortune": "Fòrciun", "Midwest": "Middùest", "futures": "fiùciers", "Washington": "Uòscington"}
    def pr(q):
        for k_, v_ in PRON.items():
            segs = re.split(r"(\[[^\]]*\])", q)
            q = "".join(g if g.startswith("[") else re.sub(r"\b" + k_ + r"\b([.,:;?!]?)", lambda m: "[" + k_ + m.group(1) + "|" + v_ + m.group(1) + "]", g) for g in segs)
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
