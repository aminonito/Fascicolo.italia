FORMAT = "reel"
CASE = "FASCICOLO N. 021 · L'UOMO SBAGLIATO"
SCENES = [
 [("Sette anni e mezzo in carcere, da innocente, per colpa di un'auto.", .3)],
 [("[13|Tredici] febbraio [1992.|millenovecentonovantadue.]", .05),
  ("Daniele Barillà, imprenditore brianzolo, va dalla fidanzata con la sua Fiat Tipo rossa.", .3)],
 [("I carabinieri stanno seguendo un trafficante di cocaina con un'auto identica, e una targa simile.", .05), ("Scambiano Barillà per lui.", .3)],
 [("Diciotto anni in primo grado, quindici in appello.", .05), ("Condanna definitiva.", .3)],
 [("Nel [1997|millenovecentonovantasette] l'ufficiale che guidava l'operazione viene arrestato, per altre vicende.", .05),
  ("Il caso si riapre.", .3)],
 [("Luglio [1999:|millenovecentonovantanove:]", .05), ("con la revisione esce dal carcere.", .05),
  ("Poi l'assoluzione: non ha commesso il fatto.", .3)],
 [("Lo Stato lo risarcisce con milioni di euro.", .2),
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
