FORMAT = "reel"
CASE = "FASCICOLO N. 032 · L'OLIO CHE NON C'ERA"
SCENES = [
 [("[New|Niù] [Jersey,|Gèrsi,] [1963.|millenovecentosessantatré.]", .05), ("Un uomo ottiene prestiti milionari dando in garanzia l'olio dei suoi serbatoi.", .05), ("Ma in molti serbatoi c'è soprattutto acqua.", .3)],
 [("È Tino De Angelis, figlio di immigrati italiani, ex garzone di macelleria nel [Bronx.|Bronks.]", .3)],
 [("Gli ispettori misurano dall'alto: vedono olio.", .05), ("Sotto, secondo le ricostruzioni, c'è acqua.", .05), ("E dei tubi spostano l'olio tra i serbatoi.", .2)],
 [("Sulla carta, oltre ottocentomila tonnellate d'olio.", .05), ("Nei serbatoi, meno di un decimo.", .2)],
 [("Novembre [1963:|sessantatré:] crolla tutto.", .05), ("Cinquantuno creditori, anche grandi banche, restano con crediti per oltre centocinquanta milioni di dollari.", .05), ("Garantiti da olio che non c'era.", .3)],
 [("De Angelis si dichiara colpevole.", .05), ("Esce dal carcere dopo circa sette anni.", .1),
  ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .2)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
