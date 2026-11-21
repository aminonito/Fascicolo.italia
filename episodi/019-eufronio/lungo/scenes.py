import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from euf import *
import fx, met
from script import SCENES_H, CH

W, H = 1920, 1080
FY = 870
MAPB = (160, 250, 1760, 880)
FB = (160, 300, 1760, 860)          # scenografia: la catena del traffico
PB = (160, 250, 1760, 880)          # scenografia: le Polaroid di Ginevra
MT = "mappa: Natural Earth · percorsi indicativi · schema non in scala"

F = {0: "Fonti: Trafficking Culture · Wikipedia · FutureLearn · Smarthistory · Ministero della Cultura",
     1: "Fonti: Wikipedia · Trafficking Culture · Smarthistory · FutureLearn · Ministero della Cultura",
     2: "Fonti: Trafficking Culture · UNODC SHERLOC · Swissinfo · Chasing Aphrodite · CoinsWeekly · Boston Globe · FutureLearn",
     3: "Fonti: Trafficking Culture (Organigram) · NPR (The Medici Conspiracy) · Lithub · Swissinfo",
     4: "Fonti: Trafficking Culture · FutureLearn · Wikipedia · Smarthistory",
     5: "Fonti: Trafficking Culture · FutureLearn · Smarthistory · New York Sun",
     6: "Fonti: Trafficking Culture · FutureLearn · Wikipedia",
     7: "Fonti: Trafficking Culture · Swissinfo · Lithub · NPR · Archaeology (1998) · FutureLearn",
     8: "Fonti: UNODC SHERLOC · Trafficking Culture · Swissinfo · The Art Newspaper · Artfix Daily · Chasing Aphrodite",
     9: "Fonti: Trafficking Culture · FutureLearn · Wikipedia · Swissinfo · Smarthistory · Ministero della Cultura (2015)",
     10: "Fonti: Trafficking Culture · FutureLearn · Wikipedia · Archaeology (1998) · Lithub · Swissinfo",
     11: "Contenuto informativo · ricostruzione a scopo divulgativo",
     12: "Fonti: tutte in descrizione · ricostruzione a scopo divulgativo"}

CHT = {1: "Cerveteri\ne il *vaso*", 2: "I *protagonisti*", 3: "Come funziona\nil *traffico*", 4: "Il *viaggio*\ndel vaso",
       5: "Il museo\ne i *giornali*", 6: "La storia\ndel *Libano*", 7: "La svolta\ndi *Ginevra*", 8: "I *processi*",
       9: "Il *ritorno*", 10: "Le domande *aperte*", 11: "La *lezione*", 12: "Il *verdetto*"}
FIRST = {}
for k, (h, _) in enumerate(SCENES_H):
    FIRST.setdefault(h, k)

# ------------------------------------------------------------------ scaletta visiva: (parola, comando)
# palco: h, big, i, ii, iii, cal, card, doc, news, map, worldroute, board, crowd, tl, court, bars, flow, cover, subscribe,
#   trip (viaggio del vaso: legs|hl), chain (catena: upto|bad|hl|flow), pol (n|hl) / polseq, vase (stato)
# sovrapposti: t (pill in alto), stamp, fig
V = {
 0: [("Novembre", "cal:NOVEMBRE|1972"), ("Metropolitan", "i:temple|IL MUSEO DI NEW YORK"), ("vaso", "vase:krater"), ("milione", "big:$ 1.000.000|pagati dal museo"), ("prezzo", "stamp:RECORD")],
 1: [("museo", "map:Beirut|10|Beirut"), ("Ma", "cal:DICEMBRE|1971"), ("quel", "i:tomb|UNA TOMBA ETRUSCA"), ("Cerveteri", "map:Cerveteri|60|Cerveteri,Roma")],
 2: [("Lo", "ii:spade|I TOMBAROLI|lock|DI NASCOSTO"), ("Ci", "iii:car|UN INCIDENTE|warehouse|UN MAGAZZINO|polaroid|LE FOTOGRAFIE"), ("processo", "court:UN LUNGO PROCESSO")],
 3: [("In", "cover"), ("chi", "ii:crate|CHI LO HA VENDUTO|dollar_bag|A QUANTO"), ("New", "trip:2"), ("svolta", "i:warehouse|LA SVOLTA DI GINEVRA"), ("giudici", "court:I GIUDICI"), ("perché", "vase:krater")],
 4: [("Partiamo", "h:Il *luogo*"), ("Cerveteri", "map:Cerveteri|60|Cerveteri,Roma"), ("Nell'antichità", "i:fortress|UNA CITTÀ ETRUSCA")],
 5: [("Gli", "i:tomb|LA NECROPOLI"), ("Tombe", "iii:tomb|TUMULI|mountain|ROCCIA|antique|OGGETTI")],
 6: [("Tra", "vase:krater"), ("Gli", "map:Atene|4|Atene,Cerveteri|Atene>Cerveteri"), ("esibire", "ii:wglass|BANCHETTO|tomb|TOMBA")],
 7: [("Per", "i:safe|UNA CASSAFORTE SOTTOTERRA"), ("E", "ii:spade|SCAVI CLANDESTINI|lock|DI NASCOSTO"), ("Italia", "fig:man|I TOMBAROLI")],
 8: [("Teniamo", "h:Una *regola*"), ("in", "doc:LA LEGGE · SCHEMA|reperti archeologici nel sottosuolo|appartengono allo Stato|ricostruzione grafica"), ("Scavare", "stamp:REATO"), ("Ed", "ii:passport|ESPORTAZIONE|lock|SENZA AUTORIZZAZIONE")],
 9: [("Ora", "vase:krater"), ("un", "ii:wglass|VINO|water|ACQUA"), ("Questo", "t:CRATERE A CALICE · FIGURE ROSSE")],
 10: [("A", "vase:krater"), ("Una", "cal:ATENE|VI sec. a.C.")],
 11: [("Il", "cal:ATENE|515 a.C."), ("alto", "big:46 × 55 cm|altezza × diametro · circa"), ("Le", "t:MISURE QUASI UGUALI TRA LE FONTI")],
 12: [("Porta", "h:Due *firme*"), ("Quella", "card:FIRMA 1 · IL VASAIO|Euxitheos|ha modellato il vaso"), ("E", "card:FIRMA 2 · IL PITTORE|Eufronio|ha dipinto le scene"), ("lui", "vase:krater")],
 13: [("Su", "i:book|L'ILIADE"), ("il", "iii:crown|SARPEDONTE|moon|IL SONNO|hourglass|LA MORTE")],
 14: [("Sull'altro", "crowd"), ("lato", "t:GIOVANI ATENIESI SI ARMANO"), ("Per", "vase:krater"), ("per", "t:DETTO ANCHE CRATERE DI SARPEDONTE")],
 15: [("Facciamo", "i:calc|UN CONTO"), ("Dal", "tl:515 a.C.|ATENE;1971|LO SCAVO"), ("Quasi", "big:≈ 2.485 anni|quasi tutti sottoterra")],
 16: [("Un", "map:Atene|4|Atene,Cerveteri|Atene>Cerveteri"), ("Ed", "i:magnifier|UN INDIZIO")],
 17: [("Apriamo", "board:0"), ("Come", "ii:court|SENTENZE|newspaper|DOCUMENTI")],
 18: [("Al", "board:0"), ("Nelle", "map:Cerveteri|80|Cerveteri"), ("Non", "i:nophoto|NESSUN NOME")],
 19: [("Poi", "board:1"), ("mercante", "map:Roma|80|Roma"), ("Più", "map:Ginevra|20|Roma,Ginevra|Roma>Ginevra")],
 20: [("Lo", "board:1"), ("La", "card:GIACOMO MEDICI|Corte di cassazione · dicembre 2011|ricorso respinto|condanna definitiva"), ("Vedremo", "t:LO VEDREMO NEL CAPITOLO 8")],
 21: [("Terzo", "board:2"), ("mercante", "i:suitcase|MERCANTE AMERICANO"), ("lui", "i:temple|PROPONE IL VASO AL MUSEO"), ("Morirà", "cal:MORTE|2012")],
 22: [("Su", "board:2"), ("è", "ii:court|PROCESSATO A ROMA|hourglass|PRESCRIZIONE"), ("Quindi", "stamp:MAI CONDANNATO")],
 23: [("Quarto", "board:3"), ("libanese", "map:Beirut|20|Beirut"), ("Secondo", "i:letter|I DOCUMENTI"), ("Morirà", "cal:INCIDENTE|1977")],
 24: [("Poi", "i:temple|IL MUSEO"), ("Dietrich", "board:4"), ("Thomas", "board:5"), ("Sono", "i:skyline|NEW YORK")],
 25: [("Più", "board:6"), ("Toccherà", "i:meeting|L'ACCORDO CON L'ITALIA")],
 26: [("Infine", "fig:police|GLI INVESTIGATORI"), ("I", "board:7"), ("caccia", "i:magnifier|LA CACCIA AI REPERTI")],
 27: [("Riepilogo", "board:7"), ("i", "i:spade|I TOMBAROLI SCAVANO"), ("mercante", "i:crate|IL MERCANTE ROMANO COMPRA"), ("mercante", "i:suitcase|IL MERCANTE AMERICANO RIVENDE"), ("collezionista", "i:letter|IL COLLEZIONISTA: LA STORIA"), ("museo", "i:temple|IL MUSEO COMPRA"), ("Stato", "i:magnifier|LO STATO INDAGA")],
 28: [("Prima", "h:Come *funziona*"), ("Non", "i:nophoto|NIENTE ISTRUZIONI"), ("capire", "flow:LA TERRA>LA VETRINA")],
 29: [("Gli", "chain:1|||"), ("Poi", "chain:2|||"), ("Poi", "chain:3|||"), ("E", "chain:5|||")],
 30: [("A", "bars:TOMBAROLI|1|MERCANTE|4|MUSEO|11"), ("E", "chain:5||0|1"), ("luogo", "iii:tomb|LA TOMBA|antique|GLI OGGETTI|map_icon|IL LUOGO")],
 31: [("Per", "i:magnifier|L'ARCHEOLOGO"), ("Un", "ii:krater|IL VASO|question|IL CONTESTO?"), ("Non", "iii:question|CHI?|antique|CON COSA?|hourglass|QUANDO?")],
 32: [("Il", "map:Zurigo|30|Zurigo,Ginevra,Roma"), ("Per", "i:swiss|UN LUOGO DI TRANSITO"), ("regole", "ii:swiss|SVIZZERA: TRANSITO|scales|REGOLE MENO SEVERE")],
 33: [("C'è", "i:warehouse|IL PORTO FRANCO DI GINEVRA"), ("grandi", "ii:crate|DEPOSITO|lock|A LUNGO"), ("Lo", "t:IL LUOGO DELLA SVOLTA")],
 34: [("L'ultimo", "h:La *provenienza*"), ("Per", "ii:temple|IL MUSEO|letter|UNA STORIA"), ("Per", "card:PROVENIENZA · ESEMPIO|collezione privata|formata prima delle leggi|di tutela")],
 35: [("Se", "ii:check|STORIA VERA|warn|STORIA INVENTATA"), ("Tenete", "h:*Provenienza*"), ("cuore", "stamp:IL CUORE DEL CASO")],
 36: [("Lo", "polseq"), ("La", "t:LA CATENA, ANELLO PER ANELLO")],
 37: [("Ora", "trip:0"), ("Partiamo", "cal:DICEMBRE|1971"), ("Secondo", "map:Cerveteri|90|Cerveteri"), ("Greppe", "t:GREPPE S. ANGELO · CERVETERI")],
 38: [("Le", "i:question|IL PUNTO ESATTO?"), ("Si", "i:tomb|UNA TOMBA DELLA NECROPOLI"), ("ricostruzione", "t:RICOSTRUZIONE GENERALMENTE ACCETTATA")],
 39: [("Il", "vase:krater_broken"), ("Esce", "i:puzzle|IN FRAMMENTI, MA COMPLETO"), ("dettaglio", "i:letter|RICORDATEVELO")],
 40: [("Prima", "trip:0"), ("Secondo", "big:≈ $ 88.000|ai tombaroli · secondo le ricostruzioni")],
 41: [("Seconda", "trip:1"), ("Medici", "map:Zurigo|20|Cerveteri,Zurigo|Cerveteri>Zurigo"), ("Lì", "big:$ 350.000|il prezzo pagato da Hecht · secondo le ricostruzioni")],
 42: [("Terza", "i:krater_broken|I FRAMMENTI"), ("Hecht", "map:Zurigo|90|Zurigo"), ("Il", "vase:krater"), ("Intanto", "i:letter|FEBBRAIO 1972 · LA LETTERA")],
 43: [("Nel", "cal:GIUGNO|1972"), ("L'accordo", "cal:AGOSTO|1972"), ("un", "big:$ 1.000.000|il prezzo"), ("Una", "t:PER UNA FONTE: $ 1.200.000")],
 44: [("Quarta", "trip:2"), ("Il", "cal:31 AGOSTO|1972"), ("Ha", "i:temple|IL VASO AL MUSEO")],
 45: [("Facciamo", "i:calc|I CONTI"), ("Ottantottomila", "bars:TOMBAROLI ($)|88000|MERCANTE ($)|350000|MUSEO ($)|1000000"), ("Tra", "big:× 11|dal primo all'ultimo passaggio")],
 46: [("Dalla", "tl:DIC. 1971|LO SCAVO;GIU. 1972|ZURIGO;AGO. 1972|NEW YORK"), ("Nove", "big:≈ 9 mesi|dalla tomba al museo")],
 47: [("Fermiamoci", "t:RIEPILOGO · 1"), ("Un", "vase:krater"), ("Una", "map:Cerveteri|60|Cerveteri"), ("Dicembre", "cal:DICEMBRE|1971"), ("Poi", "trip:2"), ("Un", "big:$ 1.000.000|")],
 48: [("Il", "cal:NOVEMBRE|1972"), ("Il", "news:MAGAZINE DOMENICALE|12 novembre 1972|*Il nuovo capolavoro*\ndel museo|ricostruzione grafica · non l'originale"), ("Un", "crowd")],
 49: [("In", "ii:question|IL PREZZO?|question|LA PROVENIENZA?"), ("Secondo", "i:lock|PROTEGGERE UN CANALE")],
 50: [("Un", "big:$ 1.000.000|nel 1972"), ("Le", "stamp:RECORD"), ("prezzo", "i:trophy|IL PREZZO PIÙ ALTO PAGATO DAL MUSEO"), ("record", "ii:krater|UN RECORD|trophy|PER UN'ANTICHITÀ")],
 51: [("Proprio", "i:newspaper|I GIORNALISTI"), ("Un", "vase:krater"), ("Da", "h:Da dove\n*arriva*?")],
 52: [("Nel", "cal:FEBBRAIO|1973"), ("Gli", "news:INCHIESTA|febbraio 1973|*Il vaso del museo*\nscavato in Italia?|ricostruzione grafica · non l'originale"), ("Cerveteri", "map:Cerveteri|60|Cerveteri")],
 53: [("Escono", "board:3"), ("Ed", "big:$ 1.000.000|"), ("Il", "worldroute:New York>Roma")],
 54: [("Il", "vase:krater"), ("in", "h:*Hot pot*"), ("scotta", "i:fire|VASO CHE SCOTTA"), ("Ancora", "i:book|NEI LIBRI")],
 55: [("Anche", "map:Roma|40|Roma"), ("Ma", "i:question|NESSUNA PROVA SUFFICIENTE"), ("collegare", "ii:tomb|UNA TOMBA PRECISA?|nophoto|PERSONE PRECISE?")],
 56: [("prima", "h:Un sospetto\n*non basta*"), ("Per", "iii:letter|DOCUMENTI|mic|TESTIMONI|chain|LA CATENA"), ("Ci", "big:> 20 anni|di attesa")],
 57: [("Vediamo", "h:La versione\ndel *Libano*"), ("Secondo", "ii:question|NON DA CERVETERI?|krater|"), ("Viene", "map:Beirut|30|Beirut")],
 58: [("Hecht", "i:suitcase|AGENTE DEL COLLEZIONISTA?"), ("commissione", "big:10%|la commissione dichiarata"), ("E", "ii:letter|LETTERA 1|letter|LETTERA 2")],
 59: [("La", "doc:LETTERA · 10 LUGLIO 1971|da: D. Sarrafian|a: R. Hecht|«consegna per 1 milione di dollari»"), ("Notate", "tl:LUG. 1971|LA LETTERA;DIC. 1971|LO SCAVO"), ("cinque", "big:5 mesi|prima del presunto scavo")],
 60: [("La", "doc:LETTERA · SETTEMBRE 1972|da: D. Sarrafian|«ottenuto da mio padre nel 1920»|«in frammenti»"), ("Lo", "map:Zurigo|10|Beirut,Zurigo|Beirut>Zurigo")],
 61: [("Il", "i:magnifier|LA VERIFICA"), ("Secondo", "worldroute:New York>Beirut"), ("E", "ii:letter|DOCUMENTI|mic|TESTIMONIANZE")],
 62: [("Tra", "big:≈ $ 909.000|in franchi svizzeri · ottobre 1971"), ("E", "ii:puzzle|FRAMMENTI|map_icon|BEIRUT, ANNI '60")],
 63: [("Con", "i:shield_ok|IL MUSEO DIFENDE L'ACQUISTO"), ("Per", "ii:check|PER IL MUSEO: REGGE|question|PER I CRITICI: NO")],
 64: [("Nel", "cal:INCIDENTE|1977"), ("Con", "board:3"), ("Nessuno", "stamp:TESTIMONE PERSO")],
 65: [("E", "i:skyline|IL VASO RESTA A NEW YORK"), ("Per", "crowd"), ("Per", "map:Roma|40|Roma")],
 66: [("Un'osservazione", "h:Nessun *tribunale*,\nper ora"), ("Abbiamo", "ii:temple|LA VERSIONE DEL MUSEO|newspaper|L'INCHIESTA"), ("La", "i:question|DA DOVE ARRIVERÀ?")],
 67: [("Passano", "tl:1973|L'INCHIESTA;1995|LA SVOLTA"), ("Agosto", "cal:AGOSTO|1995"), ("Su", "map:Napoli|20|Roma,Napoli"), ("Il", "i:car|UN INCIDENTE STRADALE")],
 68: [("Le", "fig:man|PASQUALE CAMERA"), ("Sulla", "t:VERSIONI NON DEL TUTTO CONCORDI"), ("Sulla", "ii:question|PROFESSIONE?|map_icon|LUOGO?")],
 69: [("Dopo", "i:magnifier|LE INDAGINI"), ("un", "card:ORGANIGRAMMA · SCHEMA|commercio di antichità|nomi e collegamenti|ricostruzione grafica"), ("Uno", "i:chain|I COLLEGAMENTI")],
 70: [("Secondo", "board:1"), ("Sul", "t:SUL LUOGO DEL RITROVAMENTO LE FONTI DIVERGONO")],
 71: [("L'organigramma", "map:Ginevra|60|Ginevra"), ("Qui", "i:warehouse|IL DEPOSITO NEL PORTO FRANCO"), ("Il", "cal:13 SETTEMBRE|1995"), ("carabinieri", "fig:police|CARABINIERI")],
 72: [("Il", "i:warehouse|UN EDIFICIO DOGANALE"), ("Per", "chain:5|||")],
 73: [("Dentro", "pol:6|"), ("vasi", "iii:krater|VASI|antique|AFFRESCHI|krater_broken|FRAMMENTI"), ("Alcuni", "vase:krater_dirty"), ("Le", "t:MIGLIAIA DI PEZZI")],
 74: [("Ma", "h:Le *fotografie*"), ("Migliaia", "pol:18|"), ("indicano", "bars:FONTE A|3600|FONTE B|4000")],
 75: [("Le", "polseq"), ("oggetti", "vase:krater_dirty"), ("cortile", "iii:map_icon|UN CAMPO|house|UN CORTILE|truck|UN FURGONE")],
 76: [("Poi", "vase:krater_broken"), ("Poi", "vase:krater"), ("E", "i:temple|IN MUSEO O IN CATALOGO")],
 77: [("Una", "pol:12|4"), ("Ritrae", "ii:nophoto|IL MERCANTE|krater|IL CRATERE AL MUSEO"), ("Un", "flow:IL MERCANTE>IL VASO")],
 78: [("Ci", "iii:letter|LETTERE|notes|FATTURE|register|RICEVUTE"), ("Per", "chain:5|||")],
 79: [("Giacomo", "board:1"), ("In", "doc:LETTERA · 1998 · SINTESI|di G. Medici alla rivista Archaeology|contesta la perquisizione|sostiene l'origine lecita"), ("inventario", "ii:register|INVENTARIO?|check|ORIGINE LECITA?")],
 80: [("Contesta", "bars:LE FONTI|3000|MEDICI|300"), ("Lo", "t:LA VERSIONE DI MEDICI"), ("giudici", "court:I GIUDICI")],
 81: [("Le", "map:Parigi|60|Parigi"), ("Nel", "cal:FEBBRAIO|2001"), ("Trovano", "ii:notes|VERSIONE A|notes|VERSIONE B"), ("coincidono", "stamp:NON COINCIDONO")],
 82: [("Secondo", "t:RIEPILOGO · 2"), ("Il", "trip:2"), ("Nel", "flow:L'INCIDENTE>L'ORGANIGRAMMA"), ("Ginevra", "pol:12|")],
 83: [("Se", "subscribe")],
 84: [("Arriviamo", "h:In *aula*"), ("Il", "court:TRIBUNALE DI ROMA"), ("accusato", "t:UN MERCANTE ACCUSATO DI TRAFFICO")],
 85: [("Tra", "iii:handshake|ASSOCIAZIONE|crate|RICETTAZIONE|passport|ESPORTAZIONE")],
 86: [("La", "tl:FINE 2004|SECONDO UNA FONTE;2005|SECONDO UN'ALTRA"), ("sulla", "t:DATA: FONTI NON CONCORDI"), ("La", "big:10 anni|di reclusione · primo grado")],
 87: [("A", "big:10 mln €|a favore dello Stato"), ("Le", "ii:money|MULTA?|scales|RISARCIMENTO?")],
 88: [("Negli", "doc:ATTI · SCHEMA|oggetti trafficati|...|il cratere di Eufronio"), ("qui", "cal:DICEMBRE|1971")],
 89: [("Medici", "i:envelope|L'APPELLO"), ("Il", "cal:15 LUGLIO|2009"), ("Per", "i:hourglass|PRESCRIZIONE PER ALCUNI REATI")],
 90: [("Ma", "ii:crate|RICETTAZIONE: CONFERMATA|handshake|ASSOCIAZIONE: CONFERMATA"), ("pena", "bars:PRIMO GRADO|10|APPELLO|8"), ("somma", "big:10 mln €|confermati")],
 91: [("Ultimo", "court:CORTE DI CASSAZIONE"), ("Nel", "cal:DICEMBRE|2011"), ("diventa", "card:GIACOMO MEDICI|appello: 8 anni|Cassazione 2011: ricorso respinto|condanna definitiva")],
 92: [("Facciamo", "i:calc|I TEMPI"), ("Dalla", "tl:1995|GINEVRA;2011|DEFINITIVA"), ("Dallo", "big:40 anni|dallo scavo alla sentenza definitiva")],
 93: [("E", "h:E gli *altri*?"), ("A", "ii:court|PROCESSO A ROMA|temple|EX CURATRICE · CALIFORNIA"), ("Un", "court:TRIBUNALE DI ROMA")],
 94: [("Per", "cal:PRESCRIZIONE|2010"), ("Non", "stamp:MAI CONDANNATA")],
 95: [("Per", "board:2"), ("Poche", "cal:MORTE|FEB. 2012"), ("Anche", "stamp:MAI CONDANNATO")],
 96: [("Questa", "h:Un finale\n*diviso*"), ("Da", "ii:gavel|CONDANNA DEFINITIVA|hourglass|PRESCRIZIONE")],
 97: [("E", "i:spade|I TOMBAROLI"), ("Nelle", "i:nophoto|NESSUN NOME")],
 98: [("Mentre", "h:Fuori dalle *aule*"), ("Le", "iii:polaroid|LE FOTO|court|LE SENTENZE|temple|I MUSEI")],
 99: [("Il", "cal:3 FEBBRAIO|2006"), ("firma", "i:meeting|L'ACCORDO"), ("ventina", "big:≈ 20|oggetti restituiti"), ("Tra", "vase:krater")],
 100: [("Il", "board:6"), ("Per", "stamp:AMMISSIONE")],
 101: [("L'accordo", "i:hourglass|ANCORA UN PO' A NEW YORK"), ("Il", "trip:3"), ("Nostoi", "h:*Nostoi*\n= ritorni")],
 102: [("Facciamo", "i:calc|IL CONTO"), ("Dall'arrivo", "tl:AGO. 1972|NEW YORK;GEN. 2008|ROMA"), ("anni", "big:> 35 anni|a New York")],
 103: [("Il", "i:temple|NON SOLO IL MET"), ("Secondo", "iii:temple|BOSTON|temple|GETTY|temple|CLEVELAND")],
 104: [("Anche", "map:Ginevra|20|Ginevra,Zurigo"), ("Dopo", "doc:SVIZZERA · NUOVE REGOLE|trasferimento dei beni culturali|inventari nei porti franchi|dichiarazione d'origine")],
 105: [("Dopo", "map:Roma|60|Roma"), ("Ci", "tl:2008|VILLA GIULIA;2014|CERVETERI")],
 106: [("Nel", "cal:PRESTITO|2014"), ("il", "trip:5")],
 107: [("Accanto", "ii:krater|IL CRATERE|wglass|LA COPPA"), ("una", "i:temple|DA UN MUSEO DELLA CALIFORNIA")],
 108: [("Nel", "cal:NOVEMBRE|2015"), ("definitivo", "stamp:DEFINITIVO"), ("coppa", "ii:krater|IL CRATERE|wglass|LA COPPA")],
 109: [("Il", "trip:5"), ("Non", "i:temple|UN MUSEO PUBBLICO"), ("tutti", "crowd")],
 110: [("Terzo", "t:RIEPILOGO · 3"), ("2006", "tl:2006|ACCORDO;2008|RITORNO;2011|CONDANNA;2015|CERVETERI")],
 111: [("Arriviamo", "h:Le domande\n*aperte*"), ("Perché", "ii:gavel|SENTENZA|question|PUNTI APERTI")],
 112: [("Prima", "t:1 · IL LUOGO ESATTO"), ("Le", "map:Cerveteri|90|Cerveteri"), ("Ma", "i:question|IL PUNTO PRECISO?")],
 113: [("Seconda", "t:2 · IL PREZZO"), ("Quasi", "bars:QUASI TUTTE ($)|1000000|UNA FONTE ($)|1200000"), ("intermedie", "i:newspaper|RICOSTRUZIONI")],
 114: [("Terza", "t:3 · LA VERSIONE LIBANESE"), ("Il", "ii:money|IL PAGAMENTO|puzzle|I FRAMMENTI"), ("Allora", "i:question|A COSA SI RIFERIVANO?")],
 115: [("Quarta", "t:4 · I NUMERI DI GINEVRA"), ("Le", "pol:12|"), ("Medici", "bars:LE FONTI|3000|MEDICI|300")],
 116: [("Quinta", "t:5 · L'ORGANIGRAMMA"), ("Tutti", "card:ORGANIGRAMMA · SCHEMA|commercio di antichità|nomi e collegamenti|ricostruzione grafica"), ("Ma", "i:question|DOVE? QUANDO?")],
 117: [("Sesta", "t:6 · QUANTI ALTRI?"), ("quanti", "iii:temple|COLLEZIONI|temple|MUSEI|crate|DEPOSITI"), ("Le", "i:plane|LE RESTITUZIONI CONTINUANO")],
 118: [("E", "h:Quanto abbiamo\n*perso*?"), ("Di", "i:tomb|LA TOMBA"), ("Il", "vase:krater"), ("contesto", "stamp:CONTESTO PERSO")],
 119: [("Che", "h:La *lezione*"), ("Non", "i:temple|NON SOLO PER I MUSEI"), ("Bastano", "t:CINQUE ABITUDINI")],
 120: [("Primo", "t:1 · LA PROVENIENZA"), ("Un", "card:PROVENIENZA · ESEMPIO GENERICO|da dove viene: ...|chi l'ha posseduto: ...|uscito dal Paese: ..."), ("Se", "i:warn|CAMPANELLO D'ALLARME")],
 121: [("Secondo", "t:2 · I DOCUMENTI D'ESPORTAZIONE"), ("Per", "ii:passport|AUTORIZZAZIONE|certificate|DOCUMENTI"), ("carte", "stamp:SENZA CARTE: NO")],
 122: [("Terzo", "t:3 · SE TROVI QUALCOSA"), ("In", "ii:antique|UN REPERTO|phone|AVVISA LE AUTORITÀ"), ("Tenerlo", "stamp:REATO")],
 123: [("Quarto", "t:4 · IL MERCATO ONLINE"), ("Monete", "iii:coin|MONETE|krater_broken|FRAMMENTI|antique|PICCOLI VASI"), ("basso", "i:warn|UN INDIZIO, NON UN AFFARE")],
 124: [("Quinto", "t:5 · SEGNALARE"), ("In", "fig:police|CARABINIERI"), ("Le", "i:register|BANCA DATI DEI BENI RUBATI")],
 125: [("E", "i:temple|ANCHE I MUSEI"), ("comprare", "flow:COMPRARE SENZA CHIEDERE>FINANZIARE LO SCAVO"), ("Il", "vase:krater")],
 126: [("Ricapitoliamo", "cover"), ("Uno", "vase:krater"), ("Atene", "map:Atene|4|Atene,Cerveteri|Atene>Cerveteri"), ("Cerveteri", "i:tomb|UNA TOMBA ETRUSCA")],
 127: [("Due", "cal:DICEMBRE|1971"), ("Passa", "trip:2")],
 128: [("Tre", "map:Beirut|20|Beirut"), ("Quattro", "pol:12|")],
 129: [("Cinque", "card:GIACOMO MEDICI|Cassazione 2011|condanna definitiva"), ("Per", "ii:hourglass|HECHT: PRESCRIZIONE|hourglass|EX CURATRICE: PRESCRIZIONE"), ("Sei", "trip:5")],
 130: [("E", "ii:temple|RESTITUIRE?|question|SEMPRE?"), ("Scrivilo", "i:envelope|SCRIVILO NEI COMMENTI")],
 131: [("Iscriviti", "subscribe")],
}

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

ALIAS = {"puzzle": "krater_broken", "handshake": "meeting", "clock": "hourglass", "map_icon": "globe2", "check": "shield_ok", "water": "glass"}
def IC(n): return ALIAS.get(n, n)

BOARD = [("I TOMBAROLI", "Cerveteri · nessun nome", "card"), ("GIACOMO MEDICI", "mercante · condanna definitiva 2011", "person"),
         ("ROBERT HECHT", "mercante · mai condannato", "person"), ("DIKRAN SARRAFIAN", "collezionista · Beirut", "person"),
         ("D. VON BOTHMER", "curatore · museo di New York", "person"), ("THOMAS HOVING", "direttore · museo di New York", "person"),
         ("P. DE MONTEBELLO", "direttore · accordo 2006", "person"), ("CARABINIERI · P. G. FERRI", "tutela patrimonio · procura di Roma", "card")]
BXY = [(330, 440), (720, 440), (1110, 440), (1500, 440), (330, 730), (720, 730), (1110, 730), (1500, 730)]

def board_el(n, t0, t1):
    nodes = {}
    for j in range(n + 1):
        nm, role, kind = BOARD[j]
        nodes[f"n{j}"] = dict(xy=BXY[j], name=nm, role=role, t=t0 + (0.2 if j == n else -5), rot=(-3 + 2 * (j % 3)))
    pairs = [(0, 1), (1, 2), (2, 3), (2, 4), (4, 5), (5, 6), (7, 1)]
    links = [(f"n{p}", f"n{q}", t0 - 5 if max(p, q) < n else t0 + 0.6) for p, q in pairs if max(p, q) <= n]
    return Board(nodes, links, t0, t1, cw=200)

TRIP = ["Cerveteri", "Zurigo", "New York", "Roma", "Cerveteri"]
TICON = ["truck", "truck", "plane", "plane", "truck"]
def trip_el(legs, t0, t1, a, dur):
    if legs == 0:
        pts = ["Cerveteri"]
    else:
        pts = TRIP[:legs + 1] if legs < 5 else TRIP
    allp = ["Cerveteri", "Zurigo", "New York", "Roma"]
    cen = (-32.0, 44.0); ppd = 9.0
    if legs <= 1: cen, ppd = (10.3, 44.6), 70.0
    shown = []
    for q in pts:
        if q not in shown: shown.append(q)
    if legs == 3: shown = [q for q in shown if q != "Cerveteri"]
    routes = []
    for j in range(len(pts) - 1):
        if pts[j] == pts[j + 1]: continue
        newest = j == len(pts) - 2
        routes.append(dict(pts=[pts[j], pts[j + 1]], t=(t0 + 0.6 if newest else t0 - 5), d=1.2, icon=(TICON[j] if newest else None), color=(RED if newest else GOLD)))
    if legs == 5:
        routes = [dict(pts=["Roma", "Cerveteri"], t=t0 + 0.6, d=1.0, icon="truck", color=RED)]
        cen, ppd = (12.3, 41.95), 300.0; shown = ["Roma", "Cerveteri"]
    return WorldMap(MAPB, [(t0, cen, ppd * 0.92), (t1 or a + dur, cen, ppd)], t0, t1,
                    pins=[dict(at=q, label=q.upper(), t=t0 + 0.2 + 0.15 * j, side=("l" if (legs == 5 and q == "Cerveteri") else "r"), color=(RED if q == "Cerveteri" else GOLD)) for j, q in enumerate(shown)],
                    routes=[r for r in routes if r["icon"] is not None or True], title="IL VIAGGIO DEL VASO · " + MT)

def stage(sc, cmd, t0, t1, a, dur, i):
    k, _, arg = cmd.partition(":"); p = arg.split("|") if arg else []
    if k == "h":
        sc.add(Text(arg, (960, 430), t0, t1, size=104, anchor="ma", align="m"))
    elif k == "big":
        sc.add(Big(p[0], (960, 520), t0, t1, size=150 if len(p[0]) < 14 else 96, sub=(p[1] if len(p) > 1 and p[1] else None)))
    elif k == "i":
        sc.add(Icon(IC(p[0]), (960, 560), t0, t1, size=360, label=(p[1] if len(p) > 1 and p[1] else None)), "pop")
    elif k in ("ii", "iii"):
        n = len(p) // 2; xs = [660, 1260] if n == 2 else [520, 960, 1400]
        for j in range(n):
            sc.add(Icon(IC(p[2 * j]), (xs[j], 560), t0 + j * 0.35, t1, size=300 if n == 2 else 260, label=(p[2 * j + 1] or None)), "pop")
    elif k == "vase":
        sc.add(Icon(p[0], (960, 560), t0, t1, size=520), "pop")
        sc.add(Text("vaso stilizzato · non è la pittura originale", (960, 862), t0, t1, size=22, fnt=COURR, color=GREY, anchor="mm"))
    elif k == "cal":
        sc.add(Calendar((960, 560), 320, [(t0, p[0], p[1])], t0, t1), "paper")
    elif k == "card":
        sc.add(Img(label_card(p[1:], 860, title=p[0], seed=i), (960, 570), t0, t1, anim="drop", rot=-2 + (i % 3)), "paper")
    elif k == "doc":
        sc.add(Img(doc_typed(760, 540, p[0], p[1:], seed=i), (960, 570), t0, t1, anim="drop", rot=-2), "paper")
    elif k == "news":
        sc.add(Img(newspaper(720, 600, p[0], p[1], p[2], p[3], seed=i), (960, 580), t0, t1, anim="drop", rot=-3), "paper")
    elif k == "map":
        cen, ppd = p[0], float(p[1]) * 4; pins = p[2].split(",") if len(p) > 2 and p[2] else [cen]
        if len(pins) > 1:
            ll = [WPL[q] for q in pins]; lo0, lo1 = min(x for x, y in ll), max(x for x, y in ll); la0, la1 = min(y for x, y in ll), max(y for x, y in ll)
            cen = ((lo0 + lo1) / 2, (la0 + la1) / 2); ppd = min(ppd, 1100 / max(0.3, lo1 - lo0), 420 / max(0.3, la1 - la0))
        routes = []
        if len(p) > 3:
            pts = p[3].split(">")
            routes = [dict(pts=[pts[j], pts[j + 1]], t=t0 + 0.6 + 0.8 * j, d=1.0, icon="ship" if "Atene" in pts else "truck", color=RED) for j in range(len(pts) - 1)]
        sc.add(WorldMap(MAPB, [(t0, cen, ppd * 0.8), (t1 or a + dur, cen, ppd)], t0, t1,
                        pins=[dict(at=q, label=q.upper(), t=t0 + 0.3 + 0.2 * j, side=("l" if (q == "Roma" and len(pins) > 1) else "r"), color=(RED if j == 0 else GOLD)) for j, q in enumerate(pins)],
                        routes=routes, title=MT))
    elif k == "worldroute":
        pts = arg.split(">"); ll = [WPL[q] for q in pts]
        lo0, lo1 = min(x for x, y in ll), max(x for x, y in ll); la0, la1 = min(y for x, y in ll), max(y for x, y in ll)
        cen = ((lo0 + lo1) / 2, (la0 + la1) / 2); ppd = min(1300 / max(1, lo1 - lo0), 480 / max(1, la1 - la0), 40)
        sc.add(WorldMap(MAPB, [(t0, cen, ppd * 0.85), (t1 or a + dur, cen, ppd)], t0, t1,
                        pins=[dict(at=q, label=q.upper(), t=t0 + 0.3 + 0.5 * j, side="r", color=(RED if j == 0 else GOLD)) for j, q in enumerate(pts)],
                        routes=[dict(pts=[pts[j], pts[j + 1]], t=t0 + 0.6 + 0.9 * j, d=1.0, icon="plane", color=GOLD) for j in range(len(pts) - 1)], title=MT))
    elif k == "trip":
        sc.add(trip_el(int(p[0]), t0, t1, a, dur))
    elif k == "chain":
        upto = int(p[0]); bad = int(p[1]) if len(p) > 1 and p[1] != "" else None
        hl = int(p[2]) if len(p) > 2 and p[2] != "" else None; fl = len(p) > 3 and p[3] == "1"
        sc.add(met.Filiera(FB, t0, t1, upto=upto, bad=bad, hl=hl, flow_t=(t0 + 0.8 if fl else None), title="LA CATENA DEL TRAFFICO · schema semplificato"))
    elif k == "pol":
        sc.add(Polaroids(PB, t0, t1, n=int(p[0]), hl=(int(p[1]) if len(p) > 1 and p[1] else None)))
    elif k == "polseq":
        sc.add(Polaroids(PB, t0, t1, seq=True))
    elif k == "board":
        sc.add(board_el(int(p[0]), t0, t1))
    elif k == "crowd":
        sc.add(Crowd((200, 420, 1720, 860), 26, t0, t1, s=0.42, seed=i))
    elif k == "tl":
        evs = [e.split("|") for e in arg.split(";")]
        sc.add(Timeline(300, 1620, 600, [dict(top=e[0], bottom=e[1], t=t0 + 0.3 + 0.6 * j, hl=(j == len(evs) - 1)) for j, e in enumerate(evs)], t0, t1, size=46))
    elif k == "court":
        sc.add(Icon("court", (960, 470), t0, t1, size=380, label=arg), "pop")
        sc.add(Figure([(t0, 1420, FY)], t0 + 0.3, t1, kind="judge", s=0.9, flip=-1), "pop")
    elif k == "bars":
        vals = [(p[2 * j], float(p[2 * j + 1])) for j in range(len(p) // 2)]; mx = max(v for _, v in vals)
        gap = 150 if len(vals) <= 3 else 120
        for j, (lab, v) in enumerate(vals):
            y = 420 + j * gap
            sc.add(Text(lab, (300, y - 40), t0 + 0.2 * j, t1, size=40, fnt=OSW, color=GOLD))
            sc.add(Bar(300, y + 20, 1300, 60, [(t0 + 0.2 * j, 0.0), (t0 + 0.2 * j + 0.8, v / mx)], t0 + 0.2 * j, t1, color=(RED if j == len(vals) - 1 else (90, 110, 160))))
        sc.add(Text("schema semplificato · proporzioni come dette nel video", (960, 860), t0, t1, size=24, fnt=COURR, color=GREY, anchor="mm"))
    elif k == "flow":
        a_, b_ = arg.split(">")
        sc.add(Pill(a_, (500, 560), t0, t1, size=46))
        sc.add(Arrow((860, 560), (1060, 560), t0 + 0.3, t1, color=RED))
        sc.add(Pill(b_, (1420, 560), t0 + 0.7, t1, size=46, accent=True))
    elif k == "cover":
        sc.add(Img(cover_folder19(620), (960, 560), t0, t1, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 019", (1180, 360), t0 + 0.6, t1, size=70, rot=-12))
    elif k == "subscribe":
        sc.add(Img(wordmark(120), (960, 470), t0, t1, anim="pop", shadow=False), "hit")
        sc.add(Pill("ISCRIVITI · OGNI GIORNO UN NUOVO CASO", (960, 700), t0 + 0.4, t1, size=50, accent=True))
    elif k == "fig":
        sc.add(Figure(walk([(-120, FY), (300, FY)], t0, 420), t0, t1, kind=p[0], s=1.0, label=(p[1] if len(p) > 1 and p[1] else None)), "pop")
    else:
        raise ValueError(cmd)

def build(i, dur, a, words):
    used = {}
    def T(p, n=None):
        cs = lambda s: re.sub(r"[^\w']", "", s.lower())
        hits = [w for w in words if cs(w[0]) == cs(p)] or [w for w in words if cs(w[0]).startswith(cs(p))]
        if n is None:
            n = used.get(p, 0); used[p] = n + 1
        if hits: return a + hits[min(n, len(hits) - 1)][1]
        return None
    sc = Scene(dur)
    h = SCENES_H[i][0]
    start = a
    if FIRST.get(h) == i and h > 0:
        num = f"{h:02d}" if h < 12 else None
        sc.add(Chapter(num, CHT[h], a, a + 2.4)); start = a + 2.5
    beats = []
    for w, cmd in V.get(i, []):
        t = T(w); t = (a + 0.5 if t is None else t - 0.25)
        beats.append((max(start, t), cmd))
    beats.sort(key=lambda b: b[0])
    st = [b for b in beats if b[1].split(":")[0] not in ("t", "stamp", "fig")]
    for j, (t, cmd) in enumerate(st):
        t1 = st[j + 1][0] - 0.05 if j + 1 < len(st) else None
        stage(sc, cmd, t, t1, a, dur, i)
    for t, cmd in beats:
        k, _, arg = cmd.partition(":")
        nxt = [b for b in st if b[0] > t + 0.3]
        t1 = nxt[0][0] - 0.05 if nxt else None
        if k == "t":
            nt = [b[0] for b in beats if b[1].startswith("t:") and b[0] > t]
            sc.add(Pill(arg, (960, 205), t, (nt[0] if nt else None), size=42, accent=True))
        elif k == "stamp":
            sc.add(Stamp(arg, (1280, 700), t, t1, size=96, rot=-9))
        elif k == "fig":
            stage(sc, cmd, t, t1, a, dur, i)
    sc.footer = F[h] + (" · documenti e schemi ricostruiti" if h not in (11, 12) else "")
    return sc

def thumbnail(path="thumbnail.jpg"):
    configure(1920, 1080, 30)
    bg = make_bg(19).convert("RGBA"); lay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    im = rich_img("Il vaso\nscavato\ndi *nascosto*", SERIF, 170, color=WHITE, lh=1.0)
    place(lay, im, (90, 150), "la")
    place(lay, fx.icon("krater", 600), (1460, 470), "mm")
    place(lay, fx.icon("tomb", 180), (1100, 690), "mm")
    st = stamp_img("$ 1.000.000", size=90, rot=-10); place(lay, st, (1600, 860), "mm")
    st2 = stamp_img("CASO 019", size=60, rot=-8); place(lay, st2, (380, 90), "mm")
    f = font(OSW, 54, 700); s_ = "DA UNA TOMBA ETRUSCA A NEW YORK · E RITORNO"; tw = tl(d, s_, f)
    d.rectangle([90, 790, 90 + tw + 60, 900], fill=(230, 190, 40, 255))
    d.text((120, 845), s_, font=f, fill=(20, 18, 16, 255), anchor="lm")
    place(lay, wordmark(70), (90, 975), "lm")
    out = Image.alpha_composite(bg, lay).convert("RGB"); out.save(path, quality=92)
