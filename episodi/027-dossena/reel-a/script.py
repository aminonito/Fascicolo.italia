FORMAT = "reel"
CASE = "FASCICOLO N. 027 · IL CASO DOSSENA"
SCENES = [
 [("Una tomba del [1430,|millequattrocentotrenta,] pagata oltre centomila dollari da un museo di Boston.", .05), ("Ma è stata scolpita intorno al [1920.|millenovecentoventi.]", .3)],
 [("L'autore è Alceo Dossena, scalpellino di Cremona.", .05), ("Scolpisce Madonne, angeli e statue greche nello stile dei grandi maestri.", .3)],
 [("Due mercanti di Roma le vendono come antiche.", .05), ("E finiscono nei musei americani.", .3)],
 [("Un'Annunciazione attribuita a Simone Martini viene pagata almeno centocinquantamila dollari.", .3)],
 [("Nel [1928|millenovecentoventotto] scoppia lo scandalo.", .05), ("Ma Dossena viene assolto: dice di non sapere che le vendevano come antiche.", .3)],
 [("Nel [1933|millenovecentotrentatré] trentanove sue sculture vanno all'asta: circa novemila dollari in tutto.", .2),
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
