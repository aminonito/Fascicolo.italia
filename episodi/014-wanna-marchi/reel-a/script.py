FORMAT = "reel"
CASE = "FASCICOLO N. 014 · IL SALE DEL MALOCCHIO"
SCENES = [
 [("Una bustina di sale da cucina.", .1), ("Poi una telefonata:", .05), ("il sale non si è sciolto,", .05),
  ("lei ha il malocchio.", .1), ("Per toglierlo, quattro milioni di lire.", .4)],
 [("Dietro c'è la regina delle televendite,", .05), ("[Wanna|Vanna] Marchi,", .05),
  ("con la figlia Stefania Nobile", .05), ("e un sedicente maestro di vita brasiliano.", .3)],
 [("Nel [2001|duemilauno] una telespettatrice avvisa Striscia la notizia.", .1),
  ("Finge di stare al gioco,", .05), ("con le telecamere nascoste in casa.", .3)],
 [("Il servizio va in onda.", .1), ("Il [24|ventiquattro] gennaio [2002|duemiladue]", .05),
  ("la Guardia di Finanza arresta madre e figlia.", .1), ("Il maestro fugge in Brasile.", .3)],
 [("Nel [2009|duemilanove] le condanne diventano definitive:", .05),
  ("nove anni e sei mesi per [Wanna|Vanna] Marchi,", .05), ("nove anni e quattro mesi per la figlia.", .3)],
 [("Come si cade in una trappola così?", .2), ("La storia completa è su YouTube:", .05), ("Fascicolo Italia.", .3)],
]
HEADERS = [""] * len(SCENES)
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
