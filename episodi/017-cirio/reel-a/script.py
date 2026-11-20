FORMAT = "reel"
CASE = "FASCICOLO N. 017 · IL CRAC CIRIO"
SCENES = [
 [("Una scatola di pomodori nata a Torino nel [1856.|milleottocentocinquantasei.]", .2),
  ("E [35.000|trentacinquemila] risparmiatori con obbligazioni bloccate.", .2)],
 [("È la Cirio.", .2), ("Negli anni Novanta la guida Sergio Cragnotti,", .05),
  ("presidente della Lazio campione d'Italia nel [2000.|duemila.]", .2)],
 [("Dal [2000|duemila] al [2002|duemiladue] il gruppo colloca sette prestiti obbligazionari,", .05),
  ("tramite società in Lussemburgo.", .1), ("Finiscono anche nei risparmi delle famiglie.", .2)],
 [("Novembre [2002:|duemiladue:]", .1), ("un bond da [150|centocinquanta] milioni non viene rimborsato.", .1),
  ("A catena, va in default un miliardo e [125|centoventicinque] milioni.", .2)],
 [("Per i giudici, quei bond furono venduti a gruppo già in crisi.", .2),
  ("Per Cragnotti, condanna definitiva nel [2021:|duemilaventuno:]", .05), ("[5|cinque] anni e [3|tre] mesi.", .2)],
 [("Come si riconosce un bond rischioso?", .2), ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .2)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
