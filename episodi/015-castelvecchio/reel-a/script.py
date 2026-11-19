FORMAT = "reel"
CASE = "FASCICOLO N. 015 · I 17 QUADRI DI VERONA"
SCENES = [
 [("Diciassette quadri rubati in una sola sera.", .2), ("E ritrovati, sei mesi dopo, su un'isola in Ucraina.", .4)],
 [("Verona, diciannove novembre [2015.|duemilaquindici.]", .2),
  ("Il Museo di Castelvecchio sta per chiudere,", .05), ("e l'allarme non è ancora acceso.", .3)],
 [("Entrano tre uomini armati e mascherati.", .1), ("Bloccano la guardia giurata e la cassiera,", .05),
  ("e portano via diciassette dipinti:", .05), ("Tintoretto, Mantegna, Pisanello, [Rubens.|Rùbens.]", .3)],
 [("Scappano con l'auto della guardia.", .05), ("Valore: circa quindici milioni.", .3)],
 [("Marzo [2016:|duemilasedici:]", .05), ("tredici arresti, tra Verona e la Moldavia.", .1),
  ("Tra loro, la guardia giurata di quella sera.", .3)],
 [("A maggio, le guardie di frontiera ucraine li trovano su un'isola del [Dnestr,|Dnièstr,]", .05),
  ("avvolti in sacchi di plastica.", .3)],
 [("Dove dovevano finire?", .2), ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .3)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
