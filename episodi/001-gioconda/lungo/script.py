STYLE = "fascicolo"
CASE = "FASCICOLO N. 001 · LA GIOCONDA"
TITLE = "L'italiano che rubò la Gioconda"
CH = ["INTRO", "1 · IL LADRO", "2 · LUNEDÌ MATTINA", "3 · IL MURO VUOTO", "4 · L'INDAGINE",
      "5 · LA LETTERA", "6 · IL PROCESSO", "7 · COME FINÌ", "IL VERDETTO"]
SCENES_H = [
 # 0 intro
 (0, [("Parigi, lunedì [21|ventuno] agosto [1911.|millenovecentoundici.]", .5), ("Il museo del Louvre è chiuso al pubblico.", .35),
      ("Dentro, un uomo con il camice bianco degli operai stacca un quadro dal muro,", .1), ("lo nasconde sotto il camice,", .1),
      ("ed esce dalla porta.", .5), ("Nessuno se ne accorge per più di ventiquattro ore.", .6)]),
 (0, [("Quel quadro è la Gioconda di Leonardo.", .4), ("E quell'uomo non è un genio del crimine:", .15),
      ("è un decoratore italiano di [29|ventinove] anni, che al Louvre ci aveva lavorato.", .4),
      ("Questo è il fascicolo sul furto più famoso della storia dell'arte.", .3),
      ("Vedremo come è uscito dal museo,", .1), ("perché la polizia non l'ha trovato per oltre due anni,", .1), ("e come il quadro è finito a Firenze.", .7)]),
 # 1 il ladro
 (1, [("Si chiama Vincenzo Peruggia.", .3), ("È nato nel [1881|milleottocentottantuno] a Dumenza, in provincia di Varese,", .1),
      ("e come tanti italiani dell'epoca è emigrato in Francia per lavorare.", .2), ("Fa il decoratore e il vetraio.", .5)]),
 (1, [("Al Louvre ci ha lavorato per un periodo, come vetraio.", .2),
      ("Tra i lavori a cui partecipa ci sono anche le teche di vetro che proteggono i dipinti:", .1),
      ("compresa, secondo le ricostruzioni, quella della Gioconda.", .3),
      ("Conosce i corridoi, le scale di servizio,", .1), ("e il camice bianco che indossano tutti gli operai.", .5)]),
 (1, [("C'è un dettaglio che conterà più avanti.", .3), ("Nel [1909|millenovecentonove] Peruggia era già stato fermato dalla polizia di Parigi,", .1),
      ("che lo aveva schedato:", .1), ("con la foto segnaletica e le impronte digitali.", .6)]),
 (1, [("E la Gioconda?", .3), ("Nel [1911|millenovecentoundici] è appesa nel Salon [Carré,|Carrè,] una delle sale più importanti del museo.", .2),
      ("È un quadro piccolo:", .1), ("[77|settantasette] centimetri per [53.|cinquantatré.]", .3),
      ("È famosa tra gli esperti,", .1), ("ma non è ancora l'opera più celebre del mondo.", .6)]),
 # 2 lunedi mattina
 (2, [("Lunedì [21|ventuno] agosto.", .3), ("Il lunedì il Louvre è chiuso al pubblico:", .1),
      ("dentro ci sono solo custodi, operai e addetti alle pulizie.", .2),
      ("Peruggia entra verso le sette del mattino, vestito come gli altri operai.", .5)]),
 (2, [("Su questo punto, le versioni non coincidono.", .3),
      ("Secondo alcune ricostruzioni avrebbe passato la notte nascosto in un ripostiglio.", .2),
      ("Lui, interrogato, dirà di essere entrato quella mattina, dalla porta degli operai.", .5)]),
 (2, [("Nel Salon [Carré|Carrè] non c'è nessuno.", .2), ("Peruggia stacca il quadro dai quattro ganci che lo tengono al muro,", .1),
      ("e lo porta su una scala di servizio.", .2), ("Lì toglie la cornice e la teca di vetro,", .1), ("e le lascia sul posto.", .5)]),
 (2, [("Poi scende verso l'uscita.", .2), ("Ma la porta in fondo alla scala è chiusa a chiave.", .2),
      ("Prova a smontare la maniglia, senza riuscirci.", .3),
      ("E in quel momento arriva un idraulico del museo:", .1), ("un certo [Sauvet.|Sovè.]", .5)]),
 (2, [("[Sauvet|Sovè] vede un operaio in camice, bloccato davanti a una porta senza maniglia.", .2), ("Non sospetta niente.", .2),
      ("Prende le sue pinze, apre la porta, e lo lascia uscire.", .3),
      ("Il ladro della Gioconda esce dal Louvre grazie all'aiuto di un dipendente del museo.", .3),
      ("Più tardi, un passante racconterà di aver visto un uomo gettare una maniglia in un fosso.", .5)]),
 (2, [("Peruggia torna nella sua stanza,", .05), ("in [rue|ru] [de|de] [l'Hôpital|lopitàl] [Saint-Louis.|sen luì.]", .2),
      ("Nasconde il quadro.", .3), ("E aspetta.", .7)]),
 # 3 muro vuoto
 (3, [("Martedì [22|ventidue] agosto.", .3), ("Il pittore Louis [Béroud|Berù] entra nel Salon [Carré|Carrè] per dipingere una copia della Gioconda.", .2),
      ("Al suo posto trova il muro vuoto.", .2), ("E quattro ganci di ferro.", .6)]),
 (3, [("I custodi non si allarmano:", .1), ("pensano che il quadro sia dai fotografi del museo.", .3),
      ("Solo dopo ore di ricerche capiscono che non è da nessuna parte.", .3), ("La Gioconda è stata rubata.", .6)]),
 (3, [("La notizia esce sui giornali il [23|ventitré] agosto,", .1), ("e fa il giro del mondo.", .3),
      ("Il Louvre resta chiuso per una settimana.", .2), ("Quando riapre, il [29|ventinove] agosto, si forma la fila.", .2),
      ("Migliaia di persone vengono a vedere...", .25), ("il muro vuoto.", .3),
      ("Tra loro, secondo le cronache, c'è anche lo scrittore Franz Kafka.", .6)]),
 # 4 indagine
 (4, [("Cornice e vetro vengono ritrovati sulla scala.", .2), ("E sulla cornice c'è un'impronta del pollice.", .3),
      ("A occuparsene è Alphonse [Bertillon,|Bertiión,] il pioniere delle schede segnaletiche.", .5)]),
 (4, [("Ricordate?", .2), ("Le impronte di Peruggia erano già negli archivi della polizia.", .3),
      ("Ma quell'archivio era ordinato con il sistema di [Bertillon,|Bertiión,] non per impronte digitali.", .2),
      ("Confrontare un'impronta con migliaia di schede, a mano, era quasi impossibile.", .3),
      ("Così, quell'impronta non porta a nessuno.", .6)]),
 (4, [("Gli investigatori interrogano chi lavora, o ha lavorato, al Louvre.", .2), ("Passano anche da Peruggia, a casa sua.", .3),
      ("La Gioconda è lì, a pochi metri.", .4), ("Ma non la trovano.", .7)]),
 (4, [("Intanto, i sospetti cadono su altri.", .2), ("A settembre viene arrestato il poeta [Guillaume|Ghiòm] [Apollinaire,|Apollinèr,]", .05),
      ("amico di un uomo che aveva rubato delle statuette dal Louvre.", .2), ("Resta in carcere alcuni giorni.", .2),
      ("Viene interrogato anche il suo amico, il pittore Pablo Picasso.", .3),
      ("Entrambi risulteranno estranei al furto della Gioconda.", .6)]),
 # 5 lettera
 (5, [("Passano due anni e quattro mesi.", .3), ("Il quadro resta nella stanza di Peruggia, in un baule con il doppio fondo.", .3),
      ("Poi, nel novembre [1913,|millenovecentotredici,] Peruggia fa la sua mossa.", .6)]),
 (5, [("Scrive a un antiquario di Firenze, Alfredo Geri.", .2), ("Si firma: Leonardo [V.|vu.]", .3),
      ("Dice di avere la Gioconda e di volerla riportare in Italia,", .05), ("possibilmente agli Uffizi.", .3),
      ("E chiede [500.000|cinquecentomila] lire.", .5)]),
 (5, [("Quanto sono, oggi?", .3), ("Con i coefficienti ISTAT sul valore della moneta,", .1),
      ("[500.000|cinquecentomila] lire del [1913|millenovecentotredici] valgono circa [2,3|due virgola tre] milioni di euro.", .6)]),
 (5, [("Geri avvisa il direttore degli Uffizi, Giovanni Poggi.", .2), ("Insieme fissano un appuntamento.", .3),
      ("Il [10|dieci] dicembre Peruggia arriva a Firenze in treno,", .1), ("e prende una stanza all'Hotel Tripoli.", .5)]),
 (5, [("Il giorno [11|undici] dicembre, nella stanza d'albergo, apre il baule.", .3), ("Sotto il doppio fondo c'è la Gioconda.", .3),
      ("Poggi la esamina: è l'originale.", .3), ("Con una scusa, portano il quadro agli Uffizi per verificarlo.", .3),
      ("Poco dopo, Peruggia viene arrestato in albergo.", .7)]),
 # 6 processo
 (6, [("Perché l'ha fatto?", .3), ("Peruggia dice di averla rubata per l'Italia.", .2),
      ("Era convinto che la Gioconda fosse stata portata via da Napoleone.", .3), ("Ma non è così.", .3),
      ("Fu Leonardo stesso a portarla in Francia,", .1), ("e il quadro passò poi, legalmente, al re Francesco Primo.", .6)]),
 (6, [("Il processo si tiene a Firenze, il [4|quattro] e il [5|cinque] giugno [1914.|millenovecentoquattordici.]", .3),
      ("Peruggia viene condannato a un anno e quindici giorni.", .3),
      ("In appello, il [29|ventinove] luglio, la pena scende a sette mesi e otto giorni.", .3),
      ("Gran parte dell'opinione pubblica italiana è dalla sua parte.", .6)]),
 # 7 come fini
 (7, [("E la Gioconda?", .3), ("Prima di tornare in Francia viene esposta agli Uffizi, poi a Roma e a Milano,", .1),
      ("tra folle di visitatori.", .3), ("Il [4|quattro] gennaio [1914|millenovecentoquattordici] torna al Louvre.", .3),
      ("Nei primi due giorni la vanno a vedere oltre centomila persone.", .6)]),
 (7, [("Peruggia, dopo la guerra, torna a vivere in Francia.", .2), ("Muore nel [1925,|millenovecentoventicinque,] a [44|quarantaquattro] anni.", .4),
      ("La Gioconda, invece, da quel furto esce trasformata.", .2),
      ("Per due anni i giornali di tutto il mondo hanno parlato di lei.", .3),
      ("Ed è anche così che è diventata il quadro più famoso del pianeta.", .7)]),
 # 8 verdetto
 (8, [("Ricapitolando.", .3), ("Un furto senza armi e senza violenza.", .2),
      ("Un camice bianco, una scala di servizio, e un idraulico gentile.", .3),
      ("Un'impronta che nessuno riesce a collegare.", .3),
      ("E un solo errore: provare a vendere il quadro.", .6)]),
 (8, [("E tu cosa ne pensi?", .2), ("Vincenzo Peruggia era un ladro, o un patriota?", .3), ("Scrivilo nei commenti.", .3),
      ("Le fonti sono tutte nella descrizione.", .2), ("Iscriviti a Fascicolo Italia:", .1), ("ogni settimana apriamo un nuovo caso.", .4)]),
]
SCENES = [s for h, s in SCENES_H]
HEADERS = [CH[h] for h, s in SCENES_H]
import re
def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
