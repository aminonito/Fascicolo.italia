FORMAT = "reel"
CASE = "FASCICOLO N. 028 · LO SMEMORATO DI COLLEGNO"
SCENES = [
 [("Nel [1927|millenovecentoventisette] due donne guardano la foto dello stesso uomo senza memoria.", .1), ("E tutte e due dicono: è mio marito.", .2)],
 [("Un anno prima, a Torino, viene fermato mentre ruba un vaso al cimitero ebraico.", .05), ("Non sa dire chi è: finisce nel manicomio di Collegno.", .3)],
 [("Per Giulia Canella è suo marito Giulio, professore di filosofia disperso in guerra nel [1916.|millenovecentosedici.]", .3)],
 [("Ma una lettera anonima fa un altro nome: Mario Bruneri, tipografo torinese ricercato per truffa.", .05), ("Sua moglie lo riconosce.", .05), ("E le impronte coincidono.", .3)],
 [("Nel [1931,|millenovecentotrentuno,] dopo quattro anni di cause, la sentenza: è Bruneri.", .05), ("Ma Giulia non ci crede: parte con lui per il Brasile.", .3)],
 [("Muore lì nel [1941,|millenovecentoquarantuno,] con il nome di Giulio Canella.", .15),
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
