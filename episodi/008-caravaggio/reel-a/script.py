FORMAT = "reel"
CASE = "FASCICOLO N. 008 · IL CARAVAGGIO RUBATO"
SCENES = [
 [("Un Caravaggio alto quasi tre metri,", .05), ("tagliato dalla cornice in una notte.", .1), ("E mai più ritrovato.", .4)],
 [("Palermo, ottobre [1969.|millenovecentosessantanove.]", .15), ("Oratorio di San Lorenzo:", .05),
  ("nessun allarme, nessuna guardia.", .3)],
 [("I ladri tagliano la tela lungo i bordi,", .05), ("la arrotolano,", .05),
  ("e spariscono.", .1), ("Resta solo il telaio vuoto.", .3)],
 [("Poi arrivano le voci dei collaboratori di giustizia.", .1),
  ("Mostrato alle riunioni dei boss.", .05), ("Rosicchiato dai topi in una stalla.", .05), ("Bruciato.", .3)],
 [("Nel [2018|duemiladiciotto] la Commissione antimafia segue un'altra pista:", .05),
  ("un mercante d'arte in Svizzera.", .3)],
 [("Dal [2015|duemilaquindici] sull'altare c'è una copia.", .1), ("L'originale manca da più di cinquant'anni.", .3)],
 [("Secondo te esiste ancora?", .2), ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .3)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
