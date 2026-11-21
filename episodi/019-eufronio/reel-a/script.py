FORMAT = "reel"
CASE = "FASCICOLO N. 019 · IL CRATERE DI EUFRONIO"
SCENES = [
 [("Per oltre trent'anni un vaso scavato di nascosto è la star di un museo di New York.", .3)],
 [("È il cratere di Eufronio,", .05), ("dipinto ad Atene duemilacinquecento anni fa.", .1),
  ("Nel [1971|millenovecentosettantuno] i tombaroli lo scavano da una tomba etrusca di Cerveteri.", .2)],
 [("Passa in Svizzera.", .1), ("E nel [1972|millenovecentosettantadue] il Metropolitan lo compra per un milione di dollari:", .05), ("un prezzo record.", .2)],
 [("Nel [1995|millenovecentonovantacinque] i carabinieri entrano in un magazzino del porto franco di Ginevra.", .1),
  ("Migliaia di Polaroid mostrano reperti appena usciti dalla terra.", .2)],
 [("Nel [2008|duemilaotto] il vaso torna in Italia.", .1),
  ("E il mercante romano Giacomo Medici è condannato in via definitiva nel [2011.|duemilaundici.]", .2)],
 [("Oggi il cratere è a Cerveteri, vicino alla sua tomba.", .2), ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .2)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
