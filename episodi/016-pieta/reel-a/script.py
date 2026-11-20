FORMAT = "reel"
CASE = "FASCICOLO N. 016 · LA PIETÀ E IL MARTELLO"
SCENES = [
 [("Una quindicina di colpi di martello,", .05), ("sulla statua più famosa di Michelangelo.", .4)],
 [("Roma, ventuno maggio [1972.|millenovecentosettantadue.]", .2),
  ("In San Pietro, un uomo scavalca la balaustra della Pietà,", .05),
  ("e la colpisce con un martello da geologo.", .3)],
 [("Il braccio sinistro della Madonna si stacca.", .05), ("Il naso va in pezzi.", .1),
  ("A terra restano circa cento frammenti.", .3)],
 [("Un visitatore se ne porta via uno.", .1),
  ("Mesi dopo, torna indietro per posta,", .05), ("dagli Stati Uniti.", .3)],
 [("L'uomo non viene mai processato:", .05), ("è giudicato infermo di mente.", .3)],
 [("I restauratori rimettono ogni pezzo al suo posto.", .1),
  ("Dieci mesi dopo la Pietà torna,", .05), ("dietro un vetro antiproiettile.", .3)],
 [("Era giusto cancellare i segni?", .2), ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .3)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
