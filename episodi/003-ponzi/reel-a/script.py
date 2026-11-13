FORMAT = "reel"
CASE = "FASCICOLO N. 003 · LO SCHEMA PONZI"
SCENES = [
 [("Il suo cognome è diventato il nome di una truffa.", .1), ("Ed era italiano.", .4)],
 [("[Boston,|Bòston,] [1920.|millenovecentoventi.]", .15), ("Carlo Ponzi promette il cinquanta per cento in quarantacinque giorni,", .05),
  ("grazie a un buono delle poste.", .3)],
 [("Fuori dal suo ufficio, file fino in strada.", .1), ("Nei giorni migliori incassa duecentocinquantamila dollari al giorno.", .3)],
 [("Ma il guadagno non esiste.", .15), ("I primi vengono pagati con i soldi di chi arriva dopo.", .3)],
 [("Un giornale fa i conti:", .05), ("servirebbero più di centocinquanta milioni di buoni.", .1),
  ("Ne circolano poche decine di migliaia.", .3)],
 [("Lo schema crolla.", .1), ("Ponzi finisce in carcere,", .05), ("e muore povero in Brasile.", .3)],
 [("Rendimenti alti e sicuri? È il primo segnale d'allarme.", .2), ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .3)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
