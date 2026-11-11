FORMAT = "reel"
CASE = "FASCICOLO N. 001 · LA GIOCONDA"
SCENES = [
 [("La polizia aveva l'impronta del ladro della Gioconda,", .05), ("e anche la sua scheda in archivio.", .2), ("Eppure non l'ha preso.", .4)],
 [("Agosto [1911:|millenovecentoundici:]", .1), ("dal Louvre sparisce la Gioconda.", .2), ("Sulla cornice abbandonata c'è un'impronta del pollice.", .3)],
 [("Il ladro, Vincenzo Peruggia,", .05), ("era già stato schedato dalla polizia di Parigi nel [1909,|millenovecentonove,]", .05), ("con le impronte digitali.", .3)],
 [("Ma l'archivio era ordinato con il sistema di [Bertillon,|Bertiión,]", .05), ("non per impronte.", .2), ("Confrontarla a mano con migliaia di schede era quasi impossibile.", .3)],
 [("Non solo:", .1), ("la polizia lo interroga, a casa sua.", .2), ("Il quadro è lì, nascosto.", .2), ("E non lo trovano.", .35)],
 [("Come è stato preso, due anni dopo?", .2), ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .3)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
