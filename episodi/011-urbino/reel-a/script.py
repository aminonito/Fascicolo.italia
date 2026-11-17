FORMAT = "reel"
CASE = "FASCICOLO N. 011 · IL FURTO DI URBINO"
SCENES = [
 [("Tre capolavori rubati in una notte.", .1), ("E la pista parte da un acquisto di velluto.", .4)],
 [("Urbino, febbraio [1975.|millenovecentosettantacinque.]", .1), ("Nebbia,", .05), ("un'impalcatura sulla facciata,", .05),
  ("e un museo senza allarme.", .1), ("Dal Palazzo Ducale spariscono due Piero della Francesca e un Raffaello.", .3)],
 [("Poche ore dopo il furto, a Pesaro, una ragazza compra tanto velluto per il fidanzato.", .1),
  ("Proprio il velluto in cui le autorità chiedono di avvolgere i quadri.", .3)],
 [("Il sospetto arriva ai carabinieri.", .1), ("I quadri sono troppo famosi per venderli,", .05),
  ("e arriva la richiesta di riscatto.", .3)],
 [("I carabinieri si fingono acquirenti.", .1), ("Il [23|ventitré] marzo [1976,|millenovecentosettantasei,] in un albergo di Locarno,", .05),
  ("i tre quadri vengono ritrovati.", .3)],
 [("Perché rubare quadri invendibili?", .2), ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .3)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
