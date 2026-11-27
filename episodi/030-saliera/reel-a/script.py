FORMAT = "reel"
CASE = "FASCICOLO N. 030 · LA SALIERA DI CELLINI"
SCENES = [
 [("Vienna, maggio [2003.|duemilatré.]", .05), ("Di notte un uomo sale su un'impalcatura, entra in un museo e porta via un capolavoro d'oro da circa cinquanta milioni di euro.", .3)],
 [("È la Saliera di Benvenuto Cellini, creata a Parigi per il re di Francia quasi cinque secoli prima.", .3)],
 [("Scatta l'allarme.", .05), ("Ma i guardiani pensano a un falso allarme e lo spengono.", .05), ("Il furto si scopre solo la mattina.", .3)],
 [("Nel [2005|duemilacinque] il ricattatore chiede dieci milioni di euro di riscatto.", .05), ("E come prova, il tridente di Nettuno, staccato dall'opera.", .3)],
 [("Lo tradisce una telecamera, che lo riprende mentre compra il telefono usato per il ricatto.", .05), ("Ed è un esperto di sistemi d'allarme.", .3)],
 [("Porta la polizia in un bosco: la Saliera è sepolta in una cassa.", .15),
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
