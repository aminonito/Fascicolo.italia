FORMAT = "reel"
CASE = "FASCICOLO N. 020 · IL TOTONERO"
SCENES = [
 [("Domenica [23|ventitré] marzo [1980:|millenovecentottanta:]", .05), ("a fine partita, negli stadi, le forze dell'ordine portano via i calciatori davanti alle telecamere.", .3)],
 [("A Roma un ristoratore e il suo fornitore di frutta scommettono di nascosto.", .05),
  ("E, secondo il loro racconto, pagano giocatori per truccare partite.", .2)],
 [("Ma i risultati non tornano:", .05), ("i debiti con gli allibratori arrivano a novecentocinquanta milioni di lire.", .05),
  ("Il primo marzo denunciano i calciatori.", .2)],
 [("Tredici calciatori in manette, e il presidente del Milan.", .1),
  ("A dicembre il tribunale li assolve: il fatto non sussiste.", .2)],
 [("La giustizia sportiva manda Milan e Lazio in B.", .1),
  ("Paolo Rossi, che si è sempre detto innocente, è squalificato due anni.", .2)],
 [("Torna nel [1982|millenovecentottantadue] e l'Italia vince il Mondiale.", .2), ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .2)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
