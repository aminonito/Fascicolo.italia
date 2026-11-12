FORMAT = "reel"
CASE = "FASCICOLO N. 002 · IL COLPO DI ANVERSA"
SCENES = [
 [("Il colpo del secolo è stato tradito", .05), ("da un panino al salame.", .4)],
 [("Anversa, [2003.|duemilatré.]", .15), ("Sotto il palazzo dei diamanti, un caveau con dieci livelli di sicurezza.", .15),
  ("In un [weekend|uìkend] ne svuotano più di cento cassette.", .25)],
 [("La banda acceca un sensore con la lacca per capelli,", .05),
  ("e inganna l'allarme con alluminio e nastro adesivo.", .3)],
 [("Bottino stimato: cento milioni di dollari.", .15), ("Poi la banda getta le prove in un bosco.", .3)],
 [("Il proprietario chiama la polizia per i rifiuti.", .1),
  ("Dentro: una fattura intestata a Leonardo Notarbartolo,", .05), ("e un panino mangiato a metà.", .3)],
 [("Notarbartolo viene condannato a dieci anni.", .15), ("Ma i diamanti non sono mai stati ritrovati.", .3)],
 [("Dove sono finiti?", .2), ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .3)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
