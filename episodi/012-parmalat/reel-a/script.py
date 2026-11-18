FORMAT = "reel"
CASE = "FASCICOLO N. 012 · IL CRAC PARMALAT"
SCENES = [
 [("Quasi quattro miliardi in un conto a New York.", .1), ("Ma il conto non esisteva.", .4)],
 [("Dicembre [2003.|duemilatré.]", .1), ("La Parmalat, colosso del latte,", .05),
  ("non riesce a rimborsare un'obbligazione da [150|centocinquanta] milioni.", .3)],
 [("Eppure nei suoi conti c'erano [3,95|tre virgola novantacinque] miliardi,", .05),
  ("su un conto della Bank of America, intestato a una società delle Cayman.", .3)],
 [("Il [19|diciannove] dicembre la banca risponde: quel conto non esiste.", .1),
  ("Secondo le ricostruzioni, era fatta con uno scanner.", .3)],
 [("Il buco: circa [14|quattordici] miliardi.", .1), ("Decine di migliaia di risparmiatori restano con titoli quasi senza valore.", .05),
  ("Per Calisto Tanzi, condanna definitiva per bancarotta: [17|diciassette] anni e [5|cinque] mesi.", .3)],
 [("Come ha fatto un foglio falso a ingannare il mercato?", .2), ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .3)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
