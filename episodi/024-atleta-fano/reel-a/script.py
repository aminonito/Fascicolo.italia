FORMAT = "reel"
CASE = "FASCICOLO N. 024 · L'ATLETA DI FANO"
SCENES = [
 [("Estate del [1964:|millenovecentosessantaquattro:] un peschereccio di Fano tira su la rete,", .05), ("e dentro c'è una statua di bronzo di oltre duemila anni.", .3)],
 [("Nessuno la denuncia.", .05), ("La nascondono in un campo di cavoli,", .05), ("poi a Gubbio, nella casa di un sacerdote.", .3)],
 [("Tre fratelli la comprano per tre milioni e mezzo di lire.", .05), ("Processati, alla fine sono assolti:", .05), ("non si prova dove fosse stata trovata.", .3)],
 [("Ricompare a Monaco di Baviera.", .05), ("Nel [1977|millenovecentosettantasette] il museo [Getty|Ghetti] in California la compra per quasi quattro milioni di dollari.", .3)],
 [("Nel [2018|duemiladiciotto] la Cassazione conferma la confisca:", .05), ("la statua spetta allo Stato italiano.", .05), ("Nel [2024|duemilaventiquattro] anche la Corte di Strasburgo dà ragione all'Italia.", .3)],
 [("Ma, a quanto risulta, è ancora in California.", .2),
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
