FORMAT = "reel"
CASE = "FASCICOLO N. 022 · IL BIBLIOTECARIO"
SCENES = [
 [("Il direttore di una delle biblioteche più antiche d'Italia ne portava via i libri, anche di notte.", .3)],
 [("Napoli, biblioteca dei Girolamini:", .05), ("aperta al pubblico dal [1586,|millecinquecentottantasei,] circa [160.000|centosessantamila] volumi.", .3)],
 [("Giugno [2011:|duemilaundici:]", .05), ("il nuovo direttore è un commerciante di libri antichi, Marino Massimo De Caro.", .3)],
 [("In un anno spariscono migliaia di libri.", .05), ("Ad aprile [2012|duemiladodici] uno storico dell'arte lo denuncia sui giornali.", .3)],
 [("A Monaco centinaia di volumi stanno per andare all'asta.", .05), ("Fermati la sera prima.", .3)],
 [("De Caro confessa:", .05), ("sette anni per peculato, definitivi.", .05), ("E aveva venduto a [New York|Niu Iork] un falso Galileo, per mezzo milione di dollari.", .3)],
 [("La biblioteca ha riaperto solo nel [2026.|duemilaventisei.]", .2),
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
