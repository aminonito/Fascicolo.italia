FORMAT = "reel"
CASE = "FASCICOLO N. 018 · IL VINO AL METANOLO"
SCENES = [
 [("Nel [1986|millenovecentoottantasei] un bicchiere di vino da tavola manda in ospedale decine di persone.", .2),
  ("[23|Ventitré] non ce la fanno.", .3)],
 [("Nei bottiglioni c'è metanolo:", .1), ("un alcol che esiste anche in natura, ma oltre i limiti è tossico.", .1),
  ("In alcuni, molte volte più del consentito.", .2)],
 [("Perché?", .1), ("Il metanolo alzava la gradazione.", .1),
  ("E dal [1984|millenovecentoottantaquattro] non pagava più l'imposta: costava meno dello zucchero.", .2)],
 [("La procura di Milano risale la filiera,", .05), ("fino a una cantina di Narzole, in provincia di Cuneo.", .2)],
 [("Le esportazioni crollano, nascono nuovi controlli.", .1),
  ("Nel [1992|millenovecentonovantadue] i titolari, padre e figlio, sono condannati in primo grado:", .05), ("[14|quattordici] e [4|quattro] anni.", .2)],
 [("Ma le vittime non sono mai state risarcite.", .2), ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .2)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
