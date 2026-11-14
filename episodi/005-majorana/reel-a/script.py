FORMAT = "reel"
CASE = "FASCICOLO N. 005 · IL CASO MAJORANA"
M = "[Majorana|Maioràna]"
SCENES = [
 [("Un genio della fisica ritira lo stipendio, prende il passaporto,", .05), ("e sparisce nel nulla.", .25)],
 [(f"Si chiama Ettore {M}.", .1), ("Per Enrico Fermi era un genio, come Galileo e Newton.", .2)],
 [("Napoli, marzo [1938.|millenovecentotrentotto.]", .1), ("Prende una nave per Palermo.", .05),
  ("Scrive che tornerà, e si imbarca per il ritorno.", .1), ("Poi, più nessuna notizia certa.", .2)],
 [("Per decenni si parla di tutto:", .05), ("il mare,", .05), ("un convento,", .05), ("l'Argentina.", .2)],
 [("Nel [2008|duemilaotto] un emigrato racconta di averlo conosciuto in Venezuela,", .05),
  ("con un altro nome: signor Bini.", .1), ("E c'è una foto, del [1955.|millenovecentocinquantacinque.]", .2)],
 [("Nel [2015|duemilaquindici] la procura di Roma conclude:", .05), ("era vivo,", .05),
  ("e se n'era andato di sua volontà.", .15), ("Ma perché?", .25)],
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
