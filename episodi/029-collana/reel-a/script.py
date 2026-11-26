FORMAT = "reel"
CASE = "FASCICOLO N. 029 · L'AFFARE DELLA COLLANA"
SCENES = [
 [("Agosto [1784,|millesettecentottantaquattro,] giardini di [Versailles:|Versài:] un cardinale incontra la regina di Francia.", .1), ("Ma quella donna non è la regina.", .3)],
 [("È una giovane parigina che le somiglia, ingaggiata da [Jeanne de la Motte,|Giànn de la Mòtt,] una nobile senza soldi.", .3)],
 [("Il cardinale di [Rohan|Roàn] vuole tornare nelle grazie di Maria Antonietta, e crede alle lettere false scritte a nome suo.", .3)],
 [("Così compra per lei, a rate, una collana di quasi [650|seicentocinquanta] diamanti.", .05), ("Che sparisce: smontata e venduta tra Parigi e Londra.", .3)],
 [("La regina non ne sa nulla.", .05), ("Il cardinale viene arrestato a [Versailles,|Versài,] e alla Bastiglia finisce anche un italiano: Cagliostro.", .3)],
 [("Cardinale, sosia e Cagliostro assolti;", .05), ("[Jeanne|Giànn] condannata.", .05), ("Ma il nome della regina non si riprenderà più.", .15),
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
