FORMAT = "reel"
CASE = "FASCICOLO N. 006 · IL CASO TORTORA"
T_ = "[Tortora|Tòrtora]"
SCENES = [
 [("Il volto più amato della TV finisce in manette.", .1), ("E la prova scritta contro di lui è un nome in un'agendina,", .05),
  ("che non era nemmeno il suo.", .25)],
 [(f"Enzo {T_}, il conduttore di Portobello.", .05), ("Roma, [17|diciassette] giugno [1983,|millenovecentottantatré,] all'alba.", .05),
  ("Accusa: camorra e droga.", .2)],
 [("Contro di lui, diciannove accusatori.", .05), ("E nell'agendina di un camorrista c'è scritto:", .05),
  ("[Tortona,|Tortòna,] con la enne.", .05), ("Il numero non è il suo.", .2)],
 [("Il movente, si racconta?", .05), ("Centrini all'uncinetto", .05),
  ("spediti da un detenuto a Portobello, e mai andati in onda.", .2)],
 [("Nel [1985|millenovecentottantacinque] viene condannato a dieci anni.", .05),
  ("Nel [1986|millenovecentottantasei] la Corte d'appello lo assolve con formula piena.", .2)],
 [("Torna in TV, e dice:", .05), ("Dunque, dove eravamo rimasti?", .25)],
 [("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .4)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
