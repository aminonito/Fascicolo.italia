FORMAT = "reel"
CASE = "FASCICOLO N. 010 · LA BANCA ROMANA"
SCENES = [
 [("Una banca italiana con banconote gemelle:", .05), ("stesso valore,", .05), ("stesso identico numero di serie.", .4)],
 [("Roma, [1889.|milleottocentoottantanove.]", .1), ("Gli ispettori trovano biglietti oltre il limite di legge,", .05),
  ("un buco in cassa,", .05), ("e numeri di serie doppi.", .3)],
 [("Ma la relazione resta nascosta.", .1), ("Per tre anni.", .3)],
 [("Nel dicembre [1892|milleottocentonovantadue] il deputato Napoleone [Colajanni|Colaianni] la legge alla Camera.", .1),
  ("Scoppia lo scandalo della Banca Romana.", .3)],
 [("Il governatore Bernardo Tanlongo viene arrestato.", .1),
  ("Ma nel [1894|milleottocentonovantaquattro] il tribunale assolve tutti gli imputati.", .3)],
 [("E dallo scandalo nasce la Banca d'Italia.", .3)],
 [("Quella sentenza ti convince?", .2), ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .3)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
