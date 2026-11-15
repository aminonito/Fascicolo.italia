FORMAT = "reel"
CASE = "FASCICOLO N. 007 · LA RAPINA DI VIA OSOPPO"
SCENES = [
 [("Sette uomini, pochi minuti,", .05), ("e più di cento milioni di lire.", .1), ("Senza sparare un colpo.", .4)],
 [("Milano, [1958.|millenovecentocinquantotto.]", .15), ("Giorno di paga.", .1),
  ("Un camioncino sperona il furgone portavalori di una banca in via Osoppo.", .25)],
 [("Banditi in tuta blu e passamontagna disarmano l'agente,", .05),
  ("caricano i soldi e spariscono.", .3)],
 [("Bottino in contanti: [114|centoquattordici] milioni di lire.", .1), ("Oggi, circa un milione e ottocentomila euro.", .3)],
 [("Ma i banditi buttano le tute nel fiume Olona.", .1),
  ("E il fiume è in secca per i lavori.", .3)],
 [("Un'etichetta sulle tute guida gli investigatori.", .1), ("In poche settimane la banda viene arrestata,", .05), ("e condannata.", .3)],
 [("Perché Milano simpatizzava con loro?", .2), ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .3)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
