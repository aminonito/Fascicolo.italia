FORMAT = "reel"
CASE = "FASCICOLO N. 001 · LA GIOCONDA"
SCENES = [
 [("Il ladro della Gioconda è uscito dal Louvre", .05), ("grazie a un dipendente del museo.", .4)],
 [("Parigi, lunedì [21|ventuno] agosto [1911.|millenovecentoundici.]", .2), ("Il museo è chiuso al pubblico.", .15), ("Un uomo in camice bianco stacca la Gioconda dal muro.", .3)],
 [("Su una scala di servizio toglie cornice e vetro,", .05), ("e nasconde il quadro sotto il camice.", .3)],
 [("Ma la porta in fondo alla scala è chiusa a chiave.", .2), ("Arriva un idraulico del museo.", .15), ("Pensa che sia un collega bloccato,", .05), ("prende le pinze, e gli apre la porta.", .35)],
 [("Quell'uomo è Vincenzo Peruggia, un decoratore italiano.", .2), ("E la Gioconda resterà nascosta per oltre due anni.", .35)],
 [("Come l'hanno ritrovata?", .2), ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .3)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
