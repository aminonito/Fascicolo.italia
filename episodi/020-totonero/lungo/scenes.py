import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from tot import *
import fx, met
from script import SCENES_H, CH

W, H = 1920, 1080
FY = 870
MAPB = (160, 250, 1760, 880)
FB = (160, 300, 1760, 860)          # scenografia: la catena delle scommesse
TB = (300, 230, 1620, 880)          # scenografia: il tabellone delle partite
CB = (260, 320, 1660, 840)          # scenografia: il campo del 23 marzo
MT = "mappa: Natural Earth · schema non in scala"

F = {0: "Fonti: Il Post (2012, 2020) · Linkiesta · Gli Eroi del Calcio · Tuttomercatoweb · Wikipedia · Panorama",
     1: "Fonti: Il Post (2012, 2020) · Wikipedia · Linkiesta · Panorama",
     2: "Fonti: Il Post (2012, 2016, 2020) · Wikipedia · Panorama · Linkiesta · Gli Eroi del Calcio",
     3: "Fonti: Il Post (2012, 2020) · Wikipedia · Tuttomercatoweb",
     4: "Fonti: Il Post (2012, 2020) · Panorama · Tuttomercatoweb · Il Fatto Quotidiano · ISTAT",
     5: "Fonti: Il Post (2012, 2020) · Gli Eroi del Calcio · Wikipedia · Tuttomercatoweb · Linkiesta · ISTAT",
     6: "Fonti: Il Post (2012, 2020) · Linkiesta · Gli Eroi del Calcio · Tuttomercatoweb · Il Fatto Quotidiano · Wikipedia",
     7: "Fonti: Il Post (2012, 2020) · Gli Eroi del Calcio · Wikipedia · Linkiesta · Panorama",
     8: "Fonti: Il Post (2012, 2020) · Gli Eroi del Calcio · Linkiesta · Wikipedia · L. 401/1989 (Normattiva, MioLegale)",
     9: "Fonti: Il Post (2012, 2016, 2020) · Avvenire (2020) · Gli Eroi del Calcio · Wikipedia · Panorama",
     10: "Fonti: Il Post (2012, 2020) · Wikipedia · Tuttomercatoweb · Linkiesta · Gli Eroi del Calcio · Panorama",
     11: "Contenuto informativo · non è un invito al gioco · ricostruzione a scopo divulgativo",
     12: "Fonti: tutte in descrizione · ricostruzione a scopo divulgativo"}

CHT = {1: "L'Italia del *pallone*", 2: "I *protagonisti*", 3: "Come nasce\nil *giro*", 4: "Le partite\ndell'*inverno*",
       5: "La *denuncia*", 6: "Domenica\n*23 marzo*", 7: "Il processo\n*sportivo*", 8: "Il processo\n*penale*",
       9: "*Paolo Rossi*", 10: "Le domande *aperte*", 11: "La *lezione*", 12: "Il *verdetto*"}
FIRST = {}
for k, (h, _) in enumerate(SCENES_H):
    FIRST.setdefault(h, k)

TABS = {
 "jan13": [("LAZIO", "AVELLINO", "1", ""), ("BOLOGNA", "JUVENTUS", "X", ""), ("GENOA", "PALERMO", "X", ""), ("PESCARA", "INTER", "2", "")],
 "jan13r": [("LAZIO", "AVELLINO", "1", "1-1", "X"), ("BOLOGNA", "JUVENTUS", "X", ""), ("GENOA", "PALERMO", "X", ""), ("PESCARA", "INTER", "2", "")],
 "milan": [("MILAN", "LAZIO", "", "2-1")],
 "ba0": [("BOLOGNA", "AVELLINO", "X", "")],
 "ba": [("BOLOGNA", "AVELLINO", "X", "1-0", "1")],
 "all": [("MILAN", "LAZIO", "", "2-1"), ("LAZIO", "AVELLINO", "", "1-1"), ("BOLOGNA", "JUVENTUS", "", "1-1"), ("BOLOGNA", "AVELLINO", "", "1-0"), ("AVELLINO", "PERUGIA", "", "2-2")],
 "rossi": [("AVELLINO", "PERUGIA", "", "2-2")],
}
TABT = {"jan13": "13 GENNAIO 1980 · LA MARTINGALA · schema", "jan13r": "13 GENNAIO 1980 · LA MARTINGALA · schema", "milan": "6 GENNAIO 1980",
        "ba0": "L'ULTIMA PARTITA · schema", "ba": "L'ULTIMA PARTITA · schema", "all": "ALCUNE PARTITE NEL MIRINO · 1979-80", "rossi": "STAGIONE 1979-80"}

# ------------------------------------------------------------------ scaletta visiva: (parola, comando)
V = {
 0: [("Domenica", "cal:DOMENICA 23 MARZO|1980"), ("cinque", "clock:17"), ("partite", "i:stadium|SERIE A"), ("milioni", "ii:microphone|LA RADIO|tv|LA TELEVISIONE")],
 1: [("Ma", "campo:pol"), ("telecamere", "ii:tvcam|LE TELECAMERE|tv|IN TV"), ("Tra", "i:policecar|ANCHE IL PRESIDENTE DEL MILAN")],
 2: [("Tutto", "map:Roma|25|Roma"), ("un", "ii:restaurant|UN RISTORATORE|fruit|UN FORNITORE DI FRUTTA"), ("Scommettevano", "i:slip|SCOMMESSE DI NASCOSTO"), ("alla", "doc:ESPOSTO · SCHEMA|alla Procura di Roma|i calciatori denunciati|ricostruzione grafica")],
 3: [("In", "cover"), ("giro", "chain:5|||1"), ("domenica", "campo:pol"), ("processi", "ii:gavel|GIUSTIZIA SPORTIVA|court|GIUSTIZIA PENALE"), ("Paolo", "ii:shirt|SQUALIFICATO|trophy|CAMPIONE DEL MONDO")],
 4: [("Partiamo", "h:L'*epoca*"), ("Il", "i:ball|LO SPORT NAZIONALE"), ("tutte", "clock:15"), ("alle", "t:TUTTE LE PARTITE ALLA STESSA ORA")],
 5: [("Non", "i:tv|NIENTE DIRETTE OVUNQUE"), ("I", "ii:microphone|I GOL ALLA RADIO|tv|LE IMMAGINI A FINE POMERIGGIO"), ("Quella", "i:tvcam|UNA TRASMISSIONE DECISIVA")],
 6: [("Per", "h:Una sola strada\n*legale*"), ("il", "i:schedina|LA SCHEDINA"), ("Si", "flow:TANTE PARTITE>UNA SOLA GIOCATA")],
 7: [("Scommettere", "ii:ball|UNA PARTITA SOLA|warn|VIETATO"), ("Chi", "i:betbook|GLI ALLIBRATORI CLANDESTINI")],
 8: [("Ed", "h:Il *nome*"), ("Il", "ii:schedina|TOTOCALCIO · LEGALE|betbook|TOTONERO · IN NERO"), ("Totonero", "stamp:TOTONERO")],
 9: [("C'è", "i:magnifier|UN DETTAGLIO"), ("Nel", "i:book|IL CODICE PENALE DI ALLORA"), ("trucca", "stamp:NESSUN REATO SPECIFICO")],
 10: [("Esiste", "ii:gavel|GIUSTIZIA SPORTIVA|court|GIUSTIZIA ORDINARIA"), ("Ma", "flow:COMPRARE UN RISULTATO>NON È UN REATO")],
 11: [("Teniamo", "h:La *cornice*"), ("Nel", "cal:GIUGNO|1980"), ("campionato", "i:trophy|GLI EUROPEI IN ITALIA"), ("nazionale", "crowd")],
 12: [("In", "ii:restaurant|UN RISTORATORE|fruit|UN COMMERCIANTE"), ("Non", "t:NÉ DIRIGENTI NÉ CAMPIONI"), ("Sono", "i:slip|UNA PARTITA RISCHIOSA")],
 13: [("Apriamo", "board:0"), ("È", "i:restaurant|UN RISTORATORE ROMANO"), ("Il", "map:Roma|25|Roma"), ("piazza", "t:LA LAMPARA · VICINO A PIAZZA DEL POPOLO")],
 14: [("Il", "i:shirt|MOLTI CALCIATORI"), ("Trinca", "fig:suit|IL RISTORATORE"), ("Secondo", "i:meeting|INVITATO ALLE NOZZE")],
 15: [("Il", "board:1"), ("Le", "i:fruit|INGROSSO DI FRUTTA E VERDURA"), ("Tra", "ii:restaurant|IL RISTORANTE|fruit|IL FORNITORE"), ("società", "stamp:SOCI")],
 16: [("Terzo", "board:2"), ("Non", "i:nophoto|NESSUN NOME"), ("Sono", "i:betbook|LE PUNTATE")],
 17: [("Poi", "board:3"), ("Nella", "big:27|calciatori denunciati · secondo la maggior parte delle fonti"), ("Ne", "i:nophoto|POCHISSIMI NOMI")],
 18: [("Il", "board:4"), ("La", "card:FELICE COLOMBO|presidente del Milan|giustizia sportiva: radiato")],
 19: [("Il", "board:5"), ("ex", "cal:MONDIALI|1970"), ("Sarà", "big:4 anni|di squalifica · giustizia sportiva")],
 20: [("Il", "board:6"), ("Non", "doc:ORDINE DI COMPARIZIONE · SCHEMA|convocazione dai magistrati|non è un arresto|ricostruzione grafica"), ("Si", "t:SI È SEMPRE DICHIARATO INNOCENTE"), ("La", "i:shirt|IL CAPITOLO 9")],
 21: [("Infine", "board:7"), ("la", "ii:court|LA PROCURA DI ROMA|gavel|LA FEDERAZIONE")],
 22: [("Lo", "h:La *chiave*"), ("nel", "stamp:ASSOLTI"), ("Le", "flow:SANZIONI SPORTIVE>NON CONDANNE PENALI")],
 23: [("Come", "h:Come *nasce*?"), ("Secondo", "cal:INIZIO|1974"), ("In", "iii:restaurant|AL RISTORANTE|wglass|AL BAR|map_icon|VIA VENETO")],
 24: [("Nella", "i:slip|SCOMMESSE DI NASCOSTO"), ("Coinvolge", "ii:restaurant|TRINCA|fruit|CRUCIANI"), ("Ma", "bars:PUNTATE|60|VINCITE|20")],
 25: [("Nel", "cal:NUOVA STRATEGIA|1979"), ("Non", "i:question|INDOVINARE?"), ("Vogliono", "i:magnifier|SAPERLO PRIMA"), ("E", "ii:money|DENARO|shirt|AD ALCUNI GIOCATORI")],
 26: [("Vediamo", "chain:1|||"), ("In", "chain:3|||"), ("Poi", "chain:4|||"), ("E", "chain:5|||")],
 27: [("Il", "chain:5||2|"), ("si", "ii:money|LA PROMESSA|ball|IL RISULTATO"), ("Poi", "chain:5||4|1")],
 28: [("Ma", "h:Il punto *debole*"), ("In", "big:22 + 1|giocatori in campo + un arbitro"), ("Pochi", "i:question|NESSUNA GARANZIA"), ("E", "chain:5|3||")],
 29: [("Ed", "i:ball|IL RISULTATO"), ("Secondo", "chain:5|3||"), ("Il", "i:ball|IL GOL CHE NON DOVEVA"), ("pareggio", "stamp:NIENTE PAREGGIO")],
 30: [("Il", "map:Palermo|30|Palermo,Roma"), ("Ma", "ii:question|LA DATA?|question|L'ESITO?"), ("lo", "t:VERSIONI NON CONCORDI")],
 31: [("Fermiamoci", "h:*Totonero*"), ("Il", "i:money|DENARO IN NERO"), ("niente", "iii:letter|RICEVUTE|tax|TASSE|magnifier|CONTROLLI"), ("E", "stamp:NESSUNA TUTELA")],
 32: [("Perché", "i:court|NIENTE CAUSA"), ("Se", "ii:betbook|SE PERDI|money|PAGHI"), ("È", "i:hourglass|QUALCHE MESE DOPO")],
 33: [("Riepiloghiamo", "t:RIEPILOGO · LA CATENA"), ("i", "chain:5|||1"), ("Ogni", "chain:5|1||"), ("E", "cal:INVERNO|1980")],
 34: [("Entriamo", "cal:STAGIONE|1979-80"), ("Le", "tab:all"), ("La", "tab:milan")],
 35: [("Finisce", "big:2 - 1|Milan-Lazio · 6 gennaio 1980"), ("Ed", "board:4"), ("Secondo", "i:meeting|UNA COMBINE PROPOSTA")],
 36: [("Dopo", "ii:ball|IL MILAN VINCE|money|UN COMPENSO?"), ("E", "fig:suit|IL PRESIDENTE")],
 37: [("La", "big:20 milioni|di lire · secondo le ricostruzioni"), ("Il", "map:Roma|10|Milano,Roma|Milano>Roma"), ("Le", "t:DETTAGLI NON CONCORDI TRA LE FONTI")],
 38: [("Quanto", "i:calc|QUANTO VALGONO?"), ("Con", "big:≈ 58.000 €|di oggi · coefficienti ISTAT"), ("Non", "stamp:CARISSIMO")],
 39: [("Una", "cal:DOMENICA 13 GENNAIO|1980"), ("Secondo", "big:177 milioni|di lire · su quattro partite insieme"), ("quattro", "i:slip|UNA SOLA GIOCATA")],
 40: [("Se", "big:1.350 milioni|di lire · la vincita sperata"), ("Le", "h:La *martingala*"), ("tutto", "i:slip|TUTTO SU UNA COMBINAZIONE")],
 41: [("Facciamo", "i:calc|CON I COEFFICIENTI ISTAT"), ("La", "bars:PUNTATA (€ DI OGGI)|517000|VINCITA SPERATA (€ DI OGGI)|3947000"), ("Una", "ii:restaurant|UN RISTORATORE|fruit|UN COMMERCIANTE")],
 42: [("Vediamo", "tab:jan13"), ("E", "t:PESCARA-INTER: PARTITA PULITA")],
 43: [("Ma", "tab:jan13r"), ("E", "stamp:PERSO")],
 44: [("Su", "tab:jan13"), ("giudici", "i:gavel|NESSUNA COMBINE"), ("Lo", "stamp:JUVENTUS NON PUNITA")],
 45: [("Ora", "i:betbook|I DEBITI"), ("E", "i:slip|L'ULTIMO TENTATIVO"), ("Bologna-Avellino", "tab:ba0")],
 46: [("Bologna-Avellino", "tab:ba"), ("Trinca", "stamp:PERDONO TUTTO")],
 47: [("Ma", "tab:all"), ("Oltre", "t:LE PARTITE NEL MIRINO")],
 48: [("Avellino-Perugia", "tab:rossi"), ("Ci", "i:shirt|CAPITOLO 9")],
 49: [("Riepilogo", "t:RIEPILOGO · 1"), ("Due", "ii:restaurant|TRINCA|fruit|CRUCIANI"), ("Ma", "tab:jan13r"), ("E", "bars:GENNAIO|30|FEBBRAIO|60|MARZO|95")],
 50: [("Quanto", "i:betbook|IL CONTO FINALE"), ("Secondo", "big:950 milioni|di lire · debiti con gli allibratori clandestini")],
 51: [("Con", "big:≈ 2.780.000 €|di oggi · coefficienti ISTAT"), ("Un", "stamp:IMPAGABILE"), ("E", "i:court|NESSUN TRIBUNALE PER QUEI CREDITI")],
 52: [("Così", "h:Una mossa\n*a sorpresa*"), ("Invece", "i:court|VANNO DALLA GIUSTIZIA"), ("E", "i:shirt|ACCUSANO I CALCIATORI")],
 53: [("Il", "cal:1 MARZO|1980"), ("Trinca", "doc:ESPOSTO · SCHEMA|alla Procura della Repubblica di Roma|1 marzo 1980|ricostruzione grafica"), ("La", "flow:I SOLDI PRESI>I PATTI NON RISPETTATI")],
 54: [("In", "h:*Truffati*?"), ("Truffati", "ii:shirt|DOVEVANO PERDERE|ball|HANNO GIOCATO"), ("Un", "i:newspaper|IL PARADOSSO")],
 55: [("Nell'esposto", "doc:ESPOSTO · SCHEMA|nomi e cognomi|serie A e serie B|ricostruzione grafica"), ("Ventisette", "bars:LA MAGGIOR PARTE DELLE FONTI|27|ALTRE|30")],
 56: [("Nei", "news:CRONACA|marzo 1980|*Calcio e scommesse:*\nla denuncia|ricostruzione grafica · non l'originale"), ("Le", "crowd"), ("ora", "i:court|DEPOSITATA IN PROCURA")],
 57: [("Il", "cal:4 MARZO|1980"), ("un", "i:newspaper|L'INTERVISTA"), ("Racconta", "ii:money|L'OFFERTA|stop|RIFIUTATA")],
 58: [("Secondo", "i:hospital2|L'INFORTUNIO SIMULATO"), ("Anche", "big:alcuni mesi|di squalifica · giustizia sportiva"), ("Ma", "stamp:IL GIRO ESISTE")],
 59: [("La", "board:7"), ("Interroga", "iii:mic|INTERROGATORI|letter|RACCONTI|ball|PARTITE"), ("E", "i:question|UNA MOSSA A SORPRESA")],
 60: [("Intanto", "i:stadium|IL CAMPIONATO CONTINUA"), ("Le", "ii:schedina|LA SCHEDINA|crowd_icon|LE TRIBUNE"), ("Fino", "cal:DOMENICA 23 MARZO|1980")],
 61: [("Domenica", "cal:DOMENICA 23 MARZO|1980"), ("Si", "t:24ª GIORNATA DI SERIE A"), ("Le", "clock:15")],
 62: [("Gli", "iii:house|A CASA|sun|ALL'ALBA|lock|LONTANO DAI RIFLETTORI"), ("Invece", "i:stadium|NEGLI STADI"), ("mentre", "i:tvcam|TELECAMERE ACCESE")],
 63: [("Chi", "h:Chi entra\nnegli *stadi*?"), ("Le", "iii:policecar|GUARDIA DI FINANZA|policecar|POLIZIA|policecar|CARABINIERI"), ("Diciamo", "t:FORZE DELL'ORDINE · RAPPRESENTAZIONE GENERICA")],
 64: [("Verso", "clock:17"), ("al", "campo:pol"), ("Gli", "fig:police|L'ORDINE DI CATTURA")],
 65: [("La", "i:tv|LA TRASMISSIONE DELLA DOMENICA"), ("manda", "ii:tvcam|LE IMMAGINI|handcuffs|GLI ARRESTI"), ("Il", "crowd")],
 66: [("Andiamo", "map:Pescara|60|Pescara,Roma"), ("Lì", "campo:pol"), ("Non", "i:nophoto|NESSUN NOME")],
 67: [("Gli", "board:4"), ("Albertosi", "board:5"), ("Il", "i:policecar|IL PRESIDENTE ESCE DALLO STADIO")],
 68: [("Altri", "map:Roma|9|Avellino,Perugia,Palermo,Genova,Lecce"), ("Tra", "big:13|calciatori arrestati · la maggior parte delle fonti")],
 69: [("Le", "bars:UNA FONTE (SOLO SERIE A, QUEL GIORNO)|9|UN'ALTRA|12|ALTRE|13"), ("Il", "h:La domenica\npiù *nera*")],
 70: [("Altri", "doc:ORDINE DI COMPARIZIONE · SCHEMA|convocazione dai magistrati|non è un arresto|ricostruzione grafica"), ("Tra", "board:6"), ("Non", "i:mic|L'INTERROGATORIO")],
 71: [("L'accusa", "card:L'ACCUSA|truffa aggravata"), ("Il", "news:CRONACA|24 marzo 1980|*Scandalo nel calcio:*\narresti negli stadi|ricostruzione grafica · non l'originale")],
 72: [("Facciamo", "i:calc|I TEMPI"), ("Dall'esposto", "tl:1 MARZO|L'ESPOSTO;23 MARZO|GLI ARRESTI"), ("Meno", "big:22 giorni|dall'esposto agli arresti")],
 73: [("Secondo", "t:RIEPILOGO · 2"), ("Due", "ii:betbook|I DEBITI|doc_icon|LA DENUNCIA"), ("Ventidue", "campo:pol"), ("Ora", "ii:gavel|GIUSTIZIA SPORTIVA|court|GIUSTIZIA PENALE")],
 74: [("Se", "subscribe")],
 75: [("Il", "i:gavel|LA GIUSTIZIA SPORTIVA"), ("Non", "iii:shirt|CHI GIOCA|stadium|CHI RESTA IN A|suitcase|CHI GUIDA I CLUB"), ("E", "i:hourglass|IN FRETTA")],
 76: [("Il", "cal:MAGGIO|1980"), ("La", "court:PRIMO GRADO · GIUSTIZIA SPORTIVA"), ("Per", "big:SERIE B|il Milan · primo grado")],
 77: [("È", "i:stadium|PRIMA RETROCESSIONE DEL MILAN"), ("prima", "stamp:PRIMA VOLTA"), ("E", "ii:stadium|NON IL CAMPO|gavel|UNA SENTENZA")],
 78: [("In", "big:10 milioni|di lire · la multa alla Lazio in primo grado"), ("Ma", "cal:LUGLIO|1980"), ("E", "big:SERIE B|anche la Lazio · appello")],
 79: [("Altre", "h:Le *penalità*"), ("Avellino", "bars:AVELLINO · −5 PUNTI|5|BOLOGNA · −5 PUNTI|5|PERUGIA · −5 PUNTI|5"), ("Penalità", "t:PENALITÀ ANCHE IN SERIE B")],
 80: [("Poi", "h:I *dirigenti*"), ("Felice", "card:FELICE COLOMBO|presidente del Milan|radiato"), ("Il", "big:1 anno|al presidente del Bologna")],
 81: [("E", "h:I *calciatori*"), ("Le", "bars:MINIMO|0.25|MASSIMO|6"), ("La", "big:6 anni|la pena più alta · un giocatore dell'Avellino"), ("Non", "i:nophoto|NESSUN NOME")],
 82: [("Enrico", "board:5"), ("In", "tl:PRIMO GRADO|RADIAZIONE;APPELLO|4 ANNI")],
 83: [("Paolo", "board:6"), ("In", "bars:PRIMO GRADO (ANNI)|3|APPELLO (ANNI)|2"), ("È", "stamp:2 ANNI")],
 84: [("Quanti", "h:Quanti?"), ("Le", "bars:ALCUNE FONTI|18|ALTRE|20"), ("Un'intera", "crowd")],
 85: [("Le", "flow:PER ALCUNI: AUMENTA>PER ALTRI: DIMINUISCE"), ("È", "i:letter|LE DENUNCE DEI DUE")],
 86: [("Facciamo", "t:I NUMERI"), ("punto", "i:calc|I NUMERI"), ("Due", "big:2|squadre in serie B"), ("Tre", "big:3|squadre con 5 punti di penalità"), ("Un", "big:1|presidente radiato"), ("Diciotto", "big:18-20|calciatori squalificati")],
 87: [("Il", "tl:1980-81|SERIE B;1981-82|DI NUOVO IN A"), ("Ma", "stamp:LA MACCHIA")],
 88: [("Intanto", "cal:EUROPEI|1980"), ("Senza", "i:shirt|SENZA PAOLO ROSSI"), ("Il", "i:stadium|IL TORNEO DI CASA")],
 89: [("Ora", "h:E la giustizia\n*ordinaria*?"), ("Se", "ii:gavel|SPORTIVA: DURISSIMA|court|PENALE: ?"), ("La", "cal:PRIMA DI NATALE|1980")],
 90: [("Torniamo", "court:TRIBUNALE DI ROMA"), ("Gli", "doc:IMPUTAZIONE · SCHEMA|truffa aggravata|concorso in truffa|ricostruzione grafica")],
 91: [("Ma", "i:book|IL CODICE DI ALLORA"), ("Per", "stamp:NESSUN REATO SPECIFICO"), ("E", "i:magnifier|LA TRUFFA: CONDIZIONI PRECISE")],
 92: [("Pensiamoci", "h:Chi è la\n*vittima*?"), ("Due", "ii:slip|SCOMMETTITORI|betbook|ALLIBRATORI ILLEGALI"), ("Non", "i:question|UN CASO DIFFICILE")],
 93: [("Il", "cal:23 DICEMBRE|1980"), ("Tutti", "stamp:ASSOLTI"), ("La", "card:TRIBUNALE DI ROMA · 23/12/1980|tutti assolti|perché il fatto non sussiste")],
 94: [("Il", "h:Il fatto\n*non sussiste*"), ("Non", "ii:magnifier|NON MANCANO SOLO PROVE|book|IL REATO NON C'È")],
 95: [("Così", "h:Il *paradosso*"), ("Per", "iii:stadium|SERIE B|gavel|RADIAZIONE|hourglass|SQUALIFICHE"), ("Per", "stamp:NESSUN COLPEVOLE")],
 96: [("Le", "ii:gavel|SPORTIVA: LEALTÀ DELLE GARE|court|PENALE: REATI DI LEGGE"), ("Quella", "flow:REGOLE DELLA FEDERAZIONE>SANZIONI SPORTIVE"), ("Quella", "flow:LEGGE PENALE>CONDANNE")],
 97: [("Il", "h:Il *vuoto*"), ("E", "tl:1980|IL TOTONERO;1989|LA LEGGE"), ("Il", "i:law|13 DICEMBRE 1989")],
 98: [("L'articolo", "doc:LEGGE 401/1989 · ART. 1 · SINTESI|frode in competizioni sportive|chi offre o promette denaro|per un risultato non leale|punito anche chi accetta"), ("E", "stamp:ANCHE CHI ACCETTA")],
 99: [("La", "i:betbook|SCOMMESSE ABUSIVE"), ("In", "ii:ball|LA PARTITA TRUCCATA|betbook|LA SCOMMESSA CLANDESTINA")],
 100: [("Facciamo", "i:calc|IL CONTO"), ("Dagli", "big:> 9 anni|dagli arresti alla legge"), ("Nel", "cal:SECONDO SCANDALO|1986")],
 101: [("Terzo", "t:RIEPILOGO · 3"), ("Processo", "tl:MAG-LUG 1980|SPORTIVO;DIC 1980|PENALE;1989|LA LEGGE"), ("tutti", "stamp:ASSOLTI"), ("E", "i:law|FRODE SPORTIVA")],
 102: [("E", "board:6"), ("Nel", "i:shirt|PERUGIA · 1980"), ("Gioca", "i:ball|UN NOME DELLA NAZIONALE")],
 103: [("Il", "tab:rossi"), ("L'accusa", "stamp:PAREGGIO CONCORDATO?")],
 104: [("Rossi", "h:Rossi *nega*"), ("prima", "i:hotel|L'ALBERGO DEL RITIRO"), ("Quando", "ii:meeting|DUE PERSONE|stop|CONVERSAZIONE INTERROTTA")],
 105: [("Non", "doc:ORDINE DI COMPARIZIONE · SCHEMA|concorso in truffa|non è un arresto|ricostruzione grafica"), ("Ma", "cal:EUROPEI|1980"), ("Europei", "stamp:FUORI DALLA NAZIONALE")],
 106: [("Poi", "i:gavel|LA GIUSTIZIA SPORTIVA"), ("Tre", "bars:PRIMO GRADO (ANNI)|3|APPELLO (ANNI)|2"), ("Per", "i:hourglass|DUE ANNI FERMO")],
 107: [("Rossi", "i:mic|LE SUE PAROLE"), ("Nel", "card:1981|«il primo processo sportivo:|una buffonata»"), ("E", "big:+1 mese|di squalifica")],
 108: [("Intanto", "h:Una *sorpresa*"), ("La", "i:shirt|LA JUVENTUS LO ACQUISTA"), ("Rossi", "fig:man|SOLO ALLENAMENTI")],
 109: [("Alla", "i:gavel|RICORSO ACCOLTO"), ("squalifica", "cal:FINE APRILE|1982"), ("Mancano", "i:hourglass|POCHE GIORNATE")],
 110: [("Nelle", "i:ball|SEGNA SUBITO"), ("tre", "big:3|partite prima del Mondiale"), ("pensare", "i:question|BASTANO?")],
 111: [("Eppure", "fig:suit|IL COMMISSARIO TECNICO"), ("Mondiali", "map:Madrid|12|Madrid"), ("E", "ii:shirt|SCELTO LUI|question|E GLI ALTRI?")],
 112: [("All'inizio", "i:question|NIENTE GOL"), ("Le", "i:newspaper|CRITICHE DURISSIME")],
 113: [("Poi", "h:Il *Brasile*"), ("Rossi", "iii:ball|1|ball|2|ball|3"), ("E", "stamp:FAVORITA ELIMINATA")],
 114: [("In", "ii:ball|SEMIFINALE · 2 GOL|ball|FINALE · 1 GOL"), ("In", "map:Madrid|12|Madrid"), ("L'Italia", "i:trophy|CAMPIONI DEL MONDO")],
 115: [("Paolo", "i:trophy|CAPOCANNONIERE"), ("Due", "tl:1980|SQUALIFICATO;1982|CAMPIONE DEL MONDO"), ("Pochi", "i:ball|PALLONE D'ORO")],
 116: [("C'è", "h:L'*amnistia*"), ("Meno", "cal:AMNISTIA · ESTATE|1982"), ("Nove", "big:9|calciatori tornano a giocare"), ("Albertosi", "board:5")],
 117: [("Paolo", "board:6"), ("Non", "stamp:GIÀ SCONTATA"), ("È", "cal:DICEMBRE|2020"), ("E", "t:SI È SEMPRE DICHIARATO INNOCENTE")],
 118: [("Arriviamo", "h:Le domande\n*aperte*"), ("Perché", "ii:check|FATTI CERTI|question|VERSIONI DIVERSE")],
 119: [("Prima", "t:1 · L'INIZIO"), ("Prima", "i:question|COME È COMINCIATO?"), ("Alcune", "tl:1974|IL PRIMO CONTATTO;1979|IL PIANO"), ("Le", "i:question|QUALE DATA?")],
 120: [("Seconda", "t:2 · LA PRIMA PARTITA"), ("Seconda", "i:ball|LA PRIMA PARTITA?"), ("Un'amichevole", "map:Palermo|30|Palermo,Roma"), ("per", "ii:check|COME PREVISTO?|question|NON PAGATA?")],
 121: [("Terza", "t:3 · GLI ARRESTATI"), ("Terza", "i:handcuffs|QUANTI?"), ("Nove", "bars:UNA FONTE|9|UN'ALTRA|12|ALTRE|13"), ("E", "iii:policecar|GUARDIA DI FINANZA|policecar|POLIZIA|policecar|CARABINIERI")],
 122: [("Quarta", "t:4 · LE SQUALIFICHE"), ("Quarta", "i:gavel|LE SQUALIFICHE"), ("Per", "ii:stop|RADIAZIONE|hourglass|ANNI DI SQUALIFICA"), ("Per", "bars:PRIMO GRADO (ANNI)|3|APPELLO (ANNI)|2")],
 123: [("Quinta", "t:5 · I DUE ACCUSATORI"), ("Quinta", "i:letter|I RACCONTI"), ("Erano", "ii:restaurant|ACCUSATORI|slip|PROTAGONISTI"), ("Ma", "i:gavel|NON TUTTO HA RETTO")],
 124: [("Sesta", "t:6 · IL METODO"), ("Sesta", "i:tvcam|IL METODO"), ("Arrestare", "ii:stadium|NEGLI STADI|house|A CASA"), ("È", "i:scales|COME SI FA GIUSTIZIA")],
 125: [("E", "h:La domanda\npiù *grande*"), ("perché", "i:law|NESSUNA LEGGE NEL 1980"), ("Il", "stamp:SERVIVA")],
 126: [("Che", "h:La *lezione*"), ("Le", "i:slip|LE SCOMMESSE OGGI"), ("Eccone", "t:CINQUE REGOLE")],
 127: [("Primo", "t:1 · SOLO OPERATORI AUTORIZZATI"), ("scommettere", "ii:check|AUTORIZZATO|warn|ILLEGALE"), ("Lo", "ii:restaurant|TRINCA|fruit|CRUCIANI")],
 128: [("Secondo", "t:2 · NESSUNA PARTITA SICURA"), ("diffidare", "i:warn|«PARTITA SICURA»"), ("Lo", "tab:jan13r")],
 129: [("Terzo", "t:3 · CHI GIOCA NON SCOMMETTE"), ("chi", "ii:shirt|CHI GIOCA|stop|NON SCOMMETTE"), ("E", "i:meeting|ANCHE UNA CONFIDENZA")],
 130: [("Quarto", "t:4 · NON INSEGUIRE LE PERDITE"), ("le", "bars:PRIMA|30|POI|60|ALLA FINE|95"), ("Puntare", "big:950 milioni|di lire di debiti")],
 131: [("Quinto", "t:5 · CHIEDERE AIUTO"), ("se", "i:meeting|CHIEDERE AIUTO"), ("In", "i:hospital2|SERVIZI PUBBLICI DEDICATI")],
 132: [("Questa", "h:Una lezione\nsulla *fiducia*"), ("Il", "crowd"), ("Ed", "stamp:FIDUCIA TRADITA")],
 133: [("Ricapitoliamo", "cover"), ("Uno", "ii:restaurant|UN RISTORATORE|fruit|UN COMMERCIANTE"), ("pagano", "chain:5|||1")],
 134: [("Due", "big:950 milioni|di lire di debiti"), ("primo", "cal:1 MARZO|1980"), ("Tre", "campo:pol")],
 135: [("Quattro", "bars:SERIE B|2|PENALIZZATE|3|SQUALIFICATI|20"), ("Cinque", "card:TRIBUNALE DI ROMA|23 dicembre 1980|tutti assolti|il fatto non sussiste")],
 136: [("Sei", "tl:1980|SQUALIFICATO;1982|CAMPIONE DEL MONDO"), ("E", "i:law|LEGGE 401 · 1989")],
 137: [("E", "ii:gavel|GIUSTO?|question|TROPPO?"), ("Scrivilo", "i:envelope|SCRIVILO NEI COMMENTI")],
 138: [("Iscriviti", "subscribe")],
}

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

ALIAS = {"map_icon": "globe2", "check": "shield_ok", "stop": "warn", "crowd_icon": "stadium", "doc_icon": "letter", "up": "chart",
         "down": "calendar_x", "hotel": "hotel", "medal": "medal", "mic": "microphone"}
def IC(n): return ALIAS.get(n, n)

BOARD = [("ALVARO TRINCA", "ristoratore · Roma", "person"), ("MASSIMO CRUCIANI", "commerciante di frutta", "person"),
         ("GLI ALLIBRATORI", "clandestini · nessun nome", "card"), ("I CALCIATORI", "27 denunciati · pochi nomi", "card"),
         ("FELICE COLOMBO", "presidente del Milan · radiato", "person"), ("ENRICO ALBERTOSI", "portiere · 4 anni (sportiva)", "person"),
         ("PAOLO ROSSI", "Perugia · 2 anni · sempre innocente", "person"), ("I GIUDICI", "procura di Roma · federazione", "card")]
BXY = [(330, 440), (720, 440), (1110, 440), (1500, 440), (330, 730), (720, 730), (1110, 730), (1500, 730)]

def board_el(n, t0, t1):
    nodes = {}
    for j in range(n + 1):
        nm, role, kind = BOARD[j]
        nodes[f"n{j}"] = dict(xy=BXY[j], name=nm, role=role, t=t0 + (0.2 if j == n else -5), rot=(-3 + 2 * (j % 3)))
    pairs = [(0, 1), (1, 2), (0, 3), (3, 4), (4, 5), (3, 6), (7, 3)]
    links = [(f"n{p}", f"n{q}", t0 - 5 if max(p, q) < n else t0 + 0.6) for p, q in pairs if max(p, q) <= n]
    return Board(nodes, links, t0, t1, cw=200)

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
    elif k == "cal":
        sc.add(Calendar((960, 560), 320, [(t0, p[0], p[1])], t0, t1), "paper")
    elif k == "clock":
        hh = int(p[0])
        sc.add(ClockFace((960, 520), 220, t0, t1, start=hh - 0.4, speed=0.08, label=f"ORE {hh}"), "pop")
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
            routes = [dict(pts=[pts[j], pts[j + 1]], t=t0 + 0.6 + 0.8 * j, d=1.0, icon="envelope", color=RED) for j in range(len(pts) - 1)]
        sc.add(WorldMap(MAPB, [(t0, cen, ppd * 0.8), (t1 or a + dur, cen, ppd)], t0, t1,
                        pins=[dict(at=q, label=q.upper(), t=t0 + 0.3 + 0.2 * j, side=("l" if q in ("Roma", "Genova") and len(pins) > 1 else "r"), color=(RED if j == 0 else GOLD)) for j, q in enumerate(pins)],
                        routes=routes, title=MT))
    elif k == "chain":
        upto = int(p[0]); bad = int(p[1]) if len(p) > 1 and p[1] != "" else None
        hl = int(p[2]) if len(p) > 2 and p[2] != "" else None; fl = len(p) > 3 and p[3] == "1"
        sc.add(met.Filiera(FB, t0, t1, upto=upto, bad=bad, hl=hl, flow_t=(t0 + 0.8 if fl else None), title="LA CATENA DELLE SCOMMESSE · schema semplificato"))
    elif k == "tab":
        sc.add(Tabellone(TB, TABS[arg], t0, t1, title=TABT[arg]))
    elif k == "campo":
        sc.add(Campo(CB, t0, t1, t_pol=t0 + 0.8, minute=(87, 90)))
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
        sc.add(Text("schema semplificato · proporzioni indicative", (960, 860), t0, t1, size=24, fnt=COURR, color=GREY, anchor="mm"))
    elif k == "flow":
        a_, b_ = arg.split(">")
        sc.add(Pill(a_, (500, 560), t0, t1, size=46))
        sc.add(Arrow((860, 560), (1060, 560), t0 + 0.3, t1, color=RED))
        sc.add(Pill(b_, (1420, 560), t0 + 0.7, t1, size=46, accent=True))
    elif k == "cover":
        sc.add(Img(cover_folder20(620), (960, 560), t0, t1, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 020", (1180, 360), t0 + 0.6, t1, size=70, rot=-12))
    elif k == "subscribe":
        sc.add(Img(wordmark(120), (960, 470), t0, t1, anim="pop", shadow=False), "hit")
        sc.add(Pill("ISCRIVITI · OGNI GIORNO UN NUOVO CASO", (960, 700), t0 + 0.4, t1, size=50, accent=True))
    elif k == "fig":
        sc.add(Figure(walk([(120, FY), (380, FY)], t0, 420), t0, t1, kind=p[0], s=1.0, label=(p[1] if len(p) > 1 and p[1] else None)), "pop")
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
    bg = make_bg(20).convert("RGBA"); lay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    im = rich_img("Arrestati\nallo *stadio*", SERIF, 180, color=WHITE, lh=1.0)
    place(lay, im, (90, 170), "la")
    place(lay, fx.icon("stadium", 620), (1440, 470), "mm")
    place(lay, fx.icon("policecar", 280), (1130, 640), "mm")
    st = stamp_img("TOTONERO 1980", size=80, rot=-10); place(lay, st, (1560, 880), "mm")
    st2 = stamp_img("CASO 020", size=60, rot=-8); place(lay, st2, (380, 90), "mm")
    f = font(OSW, 54, 700); s_ = "SCOMMESSE CLANDESTINE · SERIE A · 23 MARZO 1980"; tw = tl(d, s_, f)
    d.rectangle([90, 790, 90 + tw + 60, 900], fill=(230, 190, 40, 255))
    d.text((120, 845), s_, font=f, fill=(20, 18, 16, 255), anchor="lm")
    place(lay, wordmark(70), (90, 975), "lm")
    out = Image.alpha_composite(bg, lay).convert("RGB"); out.save(path, quality=92)
