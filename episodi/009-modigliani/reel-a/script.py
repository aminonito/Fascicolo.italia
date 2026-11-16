FORMAT = "reel"
CASE = "FASCICOLO N. 009 · LE TESTE DI MODIGLIANI"
SCENES = [
 [("Tre teste di pietra ripescate in un canale.", .05), ("I grandi critici dicono: sono di Modigliani.", .1),
  ("Una l'avevano fatta tre studenti,", .05), ("con un trapano.", .4)],
 [("Livorno, estate [1984.|millenovecentoottantaquattro.]", .1),
  ("La leggenda: nel [1909|millenovecentonove] Modigliani gettò alcune sculture nel Fosso Reale.", .3)],
 [("Il Comune fa dragare il canale.", .05), ("il [24|ventiquattro] luglio,", .05), ("dal fango esce una testa.", .1), ("Poi altre due.", .3)],
 [("Giulio Carlo Argan le considera autentiche.", .3)],
 [("Poi, su Panorama, parlano tre studenti:", .05), ("la seconda testa l'abbiamo scolpita noi,", .05),
  ("con un trapano.", .1), ("E lo rifanno in diretta tv.", .3)],
 [("Le altre due?", .1), ("Le aveva fatte Angelo Froglia,", .05), ("portuale e artista:", .05),
  ("un esperimento su media ed esperti.", .3)],
 [("Ci avresti creduto?", .2), ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .3)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
