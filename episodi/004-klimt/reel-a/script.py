FORMAT = "reel"
CASE = "FASCICOLO N. 004 · IL KLIMT DI PIACENZA"
SCENES = [
 [("Un quadro di [Klimt|Klìmt] sparisce per ventidue anni.", .2), ("E riappare nel muro del museo da cui era stato rubato.", .25)],
 [("Piacenza, febbraio [1997.|millenovecentonovantasette.]", .15), ("Dalla Galleria Ricci [Oddi|Òddi] sparisce il Ritratto di signora.", .1),
  ("Sul tetto resta solo la cornice.", .1), ("Vuota.", .2)],
 [("Pochi mesi prima, una studentessa aveva scoperto che sotto c'era un altro ritratto di [Klimt.|Klìmt.]", .1),
  ("L'unico doppio ritratto del pittore.", .2)],
 [("Poi un falso intercettato,", .05), ("indagini archiviate,", .05), ("anni di silenzio.", .2)],
 [("Dicembre [2019.|duemiladiciannove.]", .1), ("Alcuni giardinieri tolgono l'edera da un muro della galleria.", .1),
  ("Dietro uno sportello, un sacco nero.", .1), ("Dentro, il quadro.", .2)],
 [("La perizia lo conferma: è autentico.", .15), ("Ma chi l'ha rubato,", .05), ("ancora oggi, non si sa.", .2)],
 [("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .4)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
