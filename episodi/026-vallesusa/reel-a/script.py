FORMAT = "reel"
CASE = "FASCICOLO N. 026 · IL CRAC VALLESUSA"
SCENES = [
 [("Ottomila operai senza lavoro.", .05), ("E il loro padrone ha trent'anni, ed è stato presidente del Milan.", .3)],
 [("Lui è Felice Riva, l'erede del Cotonificio Vallesusa:", .05), ("una trentina di stabilimenti, circa quindicimila dipendenti.", .3)],
 [("Nel [1965|millenovecentosessantacinque] il gruppo fallisce,", .05), ("con oltre quarantasei miliardi di lire di debiti:", .05), ("circa cinquecentosettanta milioni di euro di oggi.", .3)],
 [("Nel [1969|millenovecentosessantanove] lo arrestano all'uscita di un cinema.", .05), ("Ma dopo pochi giorni il mandato viene annullato per un vizio di forma.", .3)],
 [("E il passaporto ce l'ha ancora.", .05), ("Nizza, Parigi, Atene. E poi Beirut.", .3)],
 [("Tredici anni in Libano. E tra amnistie e cittadinanza libanese, la condanna non la sconterà mai.", .2),
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
