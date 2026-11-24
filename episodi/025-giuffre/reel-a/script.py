FORMAT = "reel"
CASE = "FASCICOLO N. 025 · IL BANCHIERE DI DIO"
SCENES = [
 [("Anni Cinquanta, Romagna.", .05), ("Un ex impiegato di banca promette interessi del settanta,", .05), ("perfino del cento per cento all'anno.", .3)],
 [("I soldi arrivano da parroci, conventi e famiglie:", .05), ("servono, si dice, a ricostruire chiese.", .05), ("E gli interessi sono un dono della Provvidenza.", .3)],
 [("Ma secondo le ricostruzioni il denaro non viene investito:", .05), ("i nuovi risparmi pagano gli interessi dei vecchi.", .05), ("Uno schema Ponzi.", .3)],
 [("Nell'agosto del [1958|millenovecentocinquantotto] lo scandalo esplode.", .05), ("Lo chiamano il banchiere di Dio.", .3)],
 [("Il Parlamento apre un'inchiesta.", .05), ("E alla Camera la mozione sulla relazione passa per un solo voto:", .05), ("[279|duecentosettantanove] a [278.|duecentosettantotto.]", .3)],
 [("Lui viene dichiarato fallito, ma non va mai in carcere.", .2),
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
