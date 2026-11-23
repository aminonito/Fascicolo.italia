FORMAT = "reel"
CASE = "FASCICOLO N. 023 · IL COLPO DI BOSTON"
SCENES = [
 [("Avevano copiato le chiavi di ogni porta:", .05), ("smontavano le serrature, facevano fare la chiave e le rimettevano a posto.", .3)],
 [("Boston, [17|diciassette] gennaio [1950.|millenovecentocinquanta.]", .05), ("Il deposito dei furgoni portavalori [Brink's.|Brinks.]", .3)],
 [("La mente, per quasi tutte le fonti, è un ladro nato in Italia:", .05), ("Anthony Pino.", .3)],
 [("Sette uomini entrano con maschere di gomma e cappotti da marinaio.", .05), ("Legano cinque dipendenti.", .3)],
 [("In una ventina di minuti: oltre un milione e duecentomila dollari in contanti, più assegni e titoli.", .3)],
 [("Per sei anni, nessuna prova.", .05), ("Poi uno di loro, Joseph [O'Keefe,|O Chìf,] si sente tradito e parla.", .05), ("Mancano pochi giorni alla prescrizione.", .3)],
 [("Otto condannati all'ergastolo.", .05), ("Dei contanti, recuperati meno di sessantamila dollari.", .2),
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
