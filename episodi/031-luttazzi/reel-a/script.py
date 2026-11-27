FORMAT = "reel"
CASE = "FASCICOLO N. 031 · ARRESTATO PER UNA TELEFONATA"
SCENES = [
 [("Roma, [1970.|millenovecentosettanta.]", .05), ("Uno dei volti più famosi della radio e della televisione italiana finisce in carcere.", .05), ("Per una telefonata.", .3)],
 [("È Lelio Luttazzi: musicista, pianista, la voce della Hit Parade alla radio.", .3)],
 [("Un amico, l'attore Walter Chiari, gli fa chiedere di chiamare un conoscente.", .05), ("Luttazzi lo fa.", .05), ("Ma quel telefono è intercettato: il conoscente è uno spacciatore.", .3)],
 [("Arriva la Guardia di Finanza.", .05), ("In casa non trova niente.", .05), ("Ma Luttazzi viene arrestato lo stesso, con l'accusa di spaccio.", .3)],
 [("Ventisette giorni in carcere a Regina Coeli, in isolamento.", .05), ("Poi viene scarcerato e prosciolto: era del tutto estraneo.", .3)],
 [("Ma la sua carriera non tornerà più quella di prima.", .15),
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
