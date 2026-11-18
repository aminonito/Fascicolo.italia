FORMAT = "reel"
CASE = "FASCICOLO N. 013 · I VAN GOGH DI CASTELLAMMARE"
SCENES = [
 [("Due [Van Gogh|van Gog] rubati in pochi minuti.", .1), ("E ritrovati quasi quattordici anni dopo, in un'inchiesta sulla camorra.", .4)],
 [("Amsterdam, dicembre [2002.|duemiladue.]", .1), ("Due ladri appoggiano una scala al Museo [Van Gogh,|van Gog,]", .05),
  ("salgono sul tetto,", .05), ("sfondano una finestra con una mazza,", .05), ("e portano via due quadri.", .3)],
 [("Scappano calandosi con una corda.", .1), ("Ma nella fuga perdono un berretto,", .05),
  ("con il loro [DNA.|di enne a.]", .1), ("Nel [2004|duemilaquattro] sono condannati.", .3)],
 [("I quadri, però, non si trovano.", .1), ("Anni dopo, uno dei ladri dirà di averli venduti in Italia.", .3)],
 [("Settembre [2016.|duemilasedici.]", .05), ("La Guardia di Finanza indaga su un clan della camorra.", .05),
  ("A Castellammare di Stabia trova due tele avvolte in un panno.", .1), ("Sono i due [Van Gogh.|van Gog.]", .3)],
 [("Perché tenere nascosti quadri invendibili?", .2), ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .3)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
