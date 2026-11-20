import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from cir import *
import fx, pon
from script import SCENES_H, CH

W, H = 1920, 1080
FY = 870
MAPB = (160, 250, 1760, 880)
DB = (360, 250, 1560, 880)          # scenografia ricorrente: il debito che cambia padrone
TB = (160, 300, 1760, 860)          # albero del gruppo
MT = "mappa: Natural Earth · percorsi indicativi · schema non in scala"

F = {0: "Fonti: Il Giornale · Luiss CERADI · Blitz quotidiano · Money.it · Focus",
     1: "Fonti: Focus · Wikipedia (Cirio; Francesco Cirio) · Money.it · Luiss CERADI",
     2: "Fonti: Lazio Stories · WSC · Wikipedia · Luiss CERADI · Money.it",
     3: "Fonti: Lazio Stories · UEFA · WSC · Luiss CERADI · Il Giornale · AGCM · Blitz quotidiano",
     4: "Fonti: Blitz quotidiano · Luiss CERADI · Lazio Stories · La Notizia · Il Giornale · Money.it",
     5: "Fonti: Luiss CERADI · Lazio Stories · Il Giornale · Blitz quotidiano",
     6: "Fonti: UEFA · Blitz quotidiano · Luiss CERADI · Money.it · Il Giornale",
     7: "Fonti: Il Giornale · Luiss CERADI · Blitz quotidiano · Lazio Stories",
     8: "Fonti: Blitz quotidiano · Edotto · Calcio e Finanza · Finanza.com · La Notizia · Money.it",
     9: "Fonti: Il Giornale (2008) · Money.it · Conserve Italia · just-food · Wikipedia · UEFA",
     10: "Fonti: Il Giornale · Blitz quotidiano · Luiss CERADI · Edotto · Lazio Stories",
     11: "Contenuto informativo, non è consulenza finanziaria",
     12: "Fonti: tutte in descrizione · ricostruzione a scopo divulgativo"}

CHT = {1: "Una scatola\ndel *1856*", 2: "Il *finanziere*", 3: "Il gruppo\ne la *Lazio*", 4: "I *bond*", 5: "Novembre *2002*",
       6: "Il *crollo*", 7: "L'*inchiesta*", 8: "Il *processo*", 9: "Dopo il *crac*", 10: "Le domande *aperte*",
       11: "La *lezione*", 12: "Il *verdetto*"}
FIRST = {}
for k, (h, _) in enumerate(SCENES_H):
    FIRST.setdefault(h, k)

# ------------------------------------------------------------------ scaletta visiva: (parola, comando)
# comandi "di palco" (sostituiscono la grafica precedente): h, big, i, ii, iii, cal, card, bond, bonds, map, debt, tree,
#   savers, crowd, clock, tl, court, news, doc, cover, wall, scales
# comandi "sovrapposti" (si aggiungono): t (pill in alto), stamp, fig
V = {
 0: [("Novembre", "cal:NOVEMBRE|2002"), ("Una", "ii:can|UN'AZIENDA STORICA|factory|"), ("prestito", "bond:150 milioni di euro|scadenza: novembre 2002"), ("solo", "bonds:6"), ("domino", "t:IL PRIMO PEZZO DEL DOMINO")],
 1: [("Nel", "bonds:7"), ("tutte", "stamp:DEFAULT"), ("un", "big:1,125 MLD €|obbligazioni in default"), ("In", "savers"), ("trentacinquemila", "t:CIRCA 35.000 RISPARMIATORI")],
 2: [("L'azienda", "i:can|LA CIRIO"), ("Quella", "iii:tomato|POMODORI|can|SCATOLE|peas|CONSERVE"), ("Torino", "map:Torino|9|Torino"), ("E", "ii:can|CONSERVE|ball|CALCIO"), ("Lazio", "i:shield_q|CAMPIONE D'ITALIA")],
 3: [("Non", "ii:safe|NIENTE CASSEFORTI|balaclava|NIENTE RAPINE"), ("Nessuno", "i:bank|NESSUNO ENTRA DI NOTTE"), ("Eppure", "big:> 1 MLD €|mancano all'appello"), ("migliaia", "crowd")],
 4: [("In", "cover"), ("come", "i:can|UN MARCHIO STORICO"), ("finanziere", "fig:suit|UN FINANZIERE"), ("impero", "iii:can|CONSERVE|milk|LATTE|ball|CALCIO"), ("debiti", "debt:0.3"), ("vent'anni", "tl:2002|DEFAULT;2021|DEFINITIVA")],
 5: [("Torino", "map:Torino|14|Torino"), ("L'Italia", "h:L'Italia unita\n*non esiste ancora*"), ("Il", "iii:salt|SALE|water|OLIO|jar|ACETO"), ("oppure", "i:clock")],
 6: [("Qualche", "map:Parigi|14|Parigi"), ("chiudere", "i:jar|CHIUDERE"), ("scaldarlo", "i:thermo|E SCALDARE"), ("Il", "h:L'*appertizzazione*"), ("appertizzazione", "t:DAL NOME DI NICOLAS APPERT")],
 7: [("Nel", "cal:TORINO|1856"), ("Francesco", "card:SCHEDA|Francesco Cirio|Torino, 1856|avvia la produzione|di conserve"), ("Le", "ii:peas|PISELLI?|tomato|POMODORI?"), ("per", "t:LE FONTI NON COINCIDONO")],
 8: [("Quello", "i:bulb|L'IDEA"), ("Una", "ii:sun|RACCOLTA D'ESTATE|moon|MANGIATA D'INVERNO"), ("soprattutto", "i:ship|SPEDITA LONTANO")],
 9: [("Nel", "cal:PARIGI|1867"), ("Esposizione", "i:eiffel|ESPOSIZIONE UNIVERSALE"), ("riceve", "i:medal|RICONOSCIMENTI"), ("È", "h:Una vetrina\n*mondiale*")],
 10: [("Da", "i:ship|ESPORTAZIONI"), ("Le", "map:Liverpool|5|Torino,Liverpool|Torino>Liverpool"), ("Sydney", "ii:ship|FINO A SYDNEY|globe2|IN TUTTO IL MONDO")],
 11: [("Dopo", "map:Napoli|10|Torino,Napoli|Torino>Napoli"), ("dove", "i:sun|IL CLIMA DEL SUD"), ("In", "ii:factory|CAMPANIA|tomato|POMODORO")],
 12: [("È", "crowd"), ("quasi", "i:can|POMODORI PELATI"), ("Un", "tl:1856|NASCE;1867|PARIGI;1900|NOVECENTO;1990|PRIVATIZZAZIONI")],
 13: [("Nel", "ii:handshake|CAMBI DI PROPRIETÀ|factory|"), ("Per", "i:ministry|PARTECIPAZIONI DELLO STATO"), ("insieme", "iii:can|CIRIO|jar|BERTOLLI|peas|DE RICA")],
 14: [("Poi", "i:ministry|LO STATO VENDE"), ("È", "h:Le *privatizzazioni*"), ("E", "fig:suit|IL PROTAGONISTA")],
 15: [("Sergio", "card:SCHEDA|Sergio Cragnotti|nato a Roma|9 gennaio 1940"), ("Roma", "map:Roma|10|Roma"), ("Il", "ii:factory|INDUSTRIA|bank|FINANZA"), ("finanza", "fig:suit|SAGOMA · NESSUNA FOTO")],
 16: [("Gran", "worldroute:Roma>San Paolo"), ("Per", "i:factory|IN BRASILE"), ("industriali", "t:PER DIVERSI ANNI")],
 17: [("Poi", "i:factory|IL GRUPPO FERRUZZI"), ("Ed", "h:Il *salto*"), ("diventa", "ii:lab|LA CHIMICA|suit_icon|MANAGER"), ("Montedison", "t:MONTEDISON")],
 18: [("Sono", "iii:handshake|FUSIONI|chart|BORSA|bank|BANCHE"), ("Cragnotti", "map:Lussemburgo|16|Roma,Lussemburgo|Roma>Lussemburgo"), ("estere", "t:BANCHE, BORSA, SOCIETÀ ESTERE")],
 19: [("All'inizio", "h:*In proprio*"), ("Fonda", "card:LA SOCIETÀ|Cragnotti & Partners|società di investimenti|base all'estero"), ("estero", "i:globe2|")],
 20: [("Con", "worldroute:Roma>San Paolo"), ("Tra", "i:factory|BOMBRIL · BRASILE"), ("Ricordatevi", "stamp:RICORDATE"), ("tornerà", "i:court|TORNERÀ NEI PROCESSI")],
 21: [("Poi", "map:Roma|9|Roma"), ("Tra", "tl:1993|;1994|IL CONTROLLO"), ("Cragnotti", "tree0"), ("controllo", "t:CIRIO · BERTOLLI · DE RICA")],
 22: [("Il", "h:Un progetto\n*ambizioso*"), ("costruire", "i:factory|UN GRANDE GRUPPO"), ("Conserve", "iii:can|CONSERVE|jar|OLIO|milk|LATTE"), ("marchi", "i:globe2|MARCHI NEL MONDO")],
 23: [("Ma", "i:magnifier|UN DETTAGLIO"), ("L'espansione", "ii:moneybag|CAPITALE DEI SOCI|warn|POCO"), ("Viene", "big:DEBITI|così cresce il gruppo")],
 24: [("Prima", "i:bank|I PRESTITI DELLE BANCHE"), ("Poi", "bond:obbligazioni|del gruppo"), ("Tenete", "debt:0.0"), ("cuore", "t:IL CUORE DEL CASO")],
 25: [("Prima", "i:ball|UNA SQUADRA DI CALCIO"), ("Dal", "cal:FEBBRAIO|1992"), ("presidente", "card:PRESIDENTE|S.S. Lazio|dal 1992|Sergio Cragnotti")],
 26: [("È", "crowd"), ("Arrivano", "iii:ball|CAMPIONI|trophy|TROFEI|chart|CRESCITA"), ("cresce", "t:STAGIONE DOPO STAGIONE")],
 27: [("Nel", "cal:BORSA|1998"), ("primo", "ii:chart|PRIMO CLUB QUOTATO|ball|"), ("Nello", "i:trophy|COPPA ITALIA 1998")],
 28: [("Nel", "cal:EUROPA|1999"), ("la", "i:trophy|COPPA DELLE COPPE"), ("Birmingham", "map:Birmingham|10|Roma,Birmingham|Roma>Birmingham")],
 29: [("In", "iii:ball|NEDVED|ball|VIERI|ball|SALAS"), ("A", "map:Birmingham|8|Birmingham"), ("gol", "i:trophy|1999 · BIRMINGHAM")],
 30: [("E", "i:shield_q|SCUDETTO 2000"), ("all'ultima", "t:ALL'ULTIMA GIORNATA"), ("Nella", "ii:shield_q|SCUDETTO|trophy|COPPA ITALIA"), ("È", "h:Il punto\n*più alto*")],
 31: [("Intanto", "tree1"), ("Il", "i:milk|IL RAMO DEL LATTE"), ("nel", "ii:milk|CENTRALE DEL LATTE|ministry|COMUNE DI ROMA")],
 32: [("Negli", "tree2"), ("Un", "t:UN ALTRO PEZZO DELL'IMPERO")],
 33: [("Nel", "cal:VENDITA|1999"), ("Eurolat", "ii:milk|EUROLAT|factory|"), ("Parmalat", "tree3")],
 34: [("Il", "ii:calc|VALORE COMPLESSIVO|moneybag|AL NETTO DEI DEBITI"), ("il", "t:LE FONTI MISURANO COSE DIVERSE"), ("Quello", "i:court|ANNI DOPO · IN TRIBUNALE")],
 35: [("Ricapitoliamo", "tree4"), ("In", "t:IL GRUPPO A FINE ANNI NOVANTA")],
 36: [("Le", "i:pie|QUOTE DELLA LAZIO?"), ("le", "t:PERCENTUALI NON CONCORDI"), ("Ma", "ii:can|IL GRUPPO|ball|LA SQUADRA")],
 37: [("E", "i:calc|IL CONTO"), ("A", "big:> 1 MLD €|debiti a fine 1999"), ("Circa", "debt:0.0"), ("ottantacinque", "t:CIRCA L'85% VERSO LE BANCHE")],
 38: [("Un", "debt:0.0"), ("E", "i:bank|VANNO RESTITUITI"), ("Ed", "h:La storia\n*cambia direzione*")],
 39: [("Per", "i:magnifier|UN MINUTO DI SPIEGAZIONE"), ("Cos'è", "h:Che cos'è\nun'*obbligazione*?"), ("È", "bond:un prestito|a un'azienda"), ("Tu", "ii:family|TU PRESTI|factory|L'AZIENDA"), ("scadenza", "cal:SCADENZA|DATA")],
 40: [("Nel", "i:coupon|LE CEDOLE"), ("Se", "i:shield_ok|AZIENDA SOLIDA"), ("Se", "i:box_empty|SOLDI NON RESTITUITI")],
 41: [("Quando", "stamp:DEFAULT"), ("Quando", "h:*Default*"), ("E", "i:magnifier|CHI CONTROLLA?"), ("il", "ii:rating_q|RATING|report|PROSPETTO")],
 42: [("Ora", "i:can|LA CIRIO"), ("Tra", "bonds:7"), ("In", "big:1,125 MLD €|7 prestiti obbligazionari · 2000-2002")],
 43: [("Le", "map:Lussemburgo|14|Roma,Lussemburgo"), ("Vengono", "i:luxbank|SOCIETÀ IN LUSSEMBURGO"), ("create", "map:Lussemburgo|9|Roma,Lussemburgo|Roma>Lussemburgo")],
 44: [("Che", "h:Che cos'è una\n*società veicolo*?"), ("È", "i:luxbank|RACCOGLIE DENARO"), ("girarlo", "ii:luxbank|VEICOLO|factory|GRUPPO"), ("Spesso", "i:box_empty|DENTRO: SOLO DEBITI")],
 45: [("Secondo", "fig:suit|PROFESSIONISTI"), ("fondi", "iii:bank|BANCHE|chart|FONDI|suit_icon|ESPERTI"), ("Non", "i:family|NESSUNA OFFERTA AL PUBBLICO")],
 46: [("Eppure", "h:Eppure…"), ("Attraverso", "ii:bank|LO SPORTELLO|family|LE FAMIGLIE"), ("Secondo", "savers"), ("trentacinquemila", "t:CIRCA 35.000 RISPARMIATORI")],
 47: [("Perché", "h:Perché un *bond Cirio*?"), ("Il", "i:can|UN MARCHIO FAMOSO"), ("E", "ii:shield_ok|PIÙ SICURI: RENDONO MENO|warning|PIÙ INDEBITATI: RENDONO DI PIÙ")],
 48: [("Ma", "h:Più rendimento\n= *più rischio*"), ("più", "i:warning|PIÙ RISCHIO"), ("Chi", "ii:moneybag|PRESTI|warn|AZIENDA INDEBITATA")],
 49: [("E", "i:magnifier|IL DATO CHIAVE"), ("Dove", "h:Dove vanno\n*i soldi*?")],
 50: [("Le", "ii:report|COMMISSARI|lab|PERITI"), ("A", "debt:0.0"), ("Nel", "debt:0.7"), ("maggior", "t:IL DEBITO PASSA AGLI OBBLIGAZIONISTI")],
 51: [("In", "debt:0.7"), ("Le", "t:LE BANCHE RIENTRANO"), ("Al", "t:IL RISCHIO PASSA A CHI HA I BOND")],
 52: [("Secondo", "i:court|SECONDO I GIUDICI"), ("quelle", "debt:0.75"), ("È", "i:gavel|IL PUNTO DEI PROCESSI")],
 53: [("Facciamo", "i:calc|UN CONTO"), ("Un", "big:1.125.000.000 € ÷ 35.000|"), ("trentaduemila", "big:≈ 32.000 €|a testa · solo un ordine di grandezza")],
 54: [("È", "t:SOLO UN ORDINE DI GRANDEZZA"), ("una", "ii:suit_icon|PROFESSIONALI|family|RISPARMIATORI"), ("Ma", "i:piggy|I RISPARMI DI UNA VITA")],
 55: [("Prima", "t:RIEPILOGO"), ("Un", "i:can|UN MARCHIO STORICO"), ("Un", "fig:suit|UN FINANZIERE"), ("Debiti", "debt:0.7"), ("sette", "map:Lussemburgo|10|Lussemburgo")],
 56: [("Se", "subscribe"), ("E", "cal:NOVEMBRE|2002")],
 57: [("Una", "cal:NOVEMBRE 2002|3"), ("È", "bond:150 milioni di euro|sede: Lussemburgo|scadenza: 3 novembre 2002"), ("Lussemburgo", "map:Lussemburgo|10|Lussemburgo")],
 58: [("Alla", "i:box_empty|I SOLDI NON CI SONO"), ("I", "savers"), ("niente", "stamp:NON RIMBORSATO")],
 59: [("Ogni", "i:shield|IL GARANTE DEI BOND"), ("si", "h:Il *trustee*"), ("Londra", "map:Londra|10|Londra,Lussemburgo")],
 60: [("Pochi", "cal:NOVEMBRE 2002|7-8"), ("il", "t:7 O 8 NOVEMBRE: FONTI NON CONCORDI"), ("dichiara", "doc:DICHIARAZIONE DI DEFAULT|prestito da 150 milioni|non rimborsato"), ("Il", "stamp:DEFAULT")],
 61: [("Un", "i:calc|UN CONTO"), ("Centocinquanta", "big:150 / 1.125 ≈ 13%|del totale"), ("Un", "i:pie|UN PEZZO PICCOLO")],
 62: [("E", "i:chain|UN MECCANISMO"), ("Si", "h:*Cross default*\ninadempimento incrociato")],
 63: [("Funziona", "doc:CONTRATTO · CLAUSOLA|se un prestito non è pagato|anche gli altri possono|essere in default"), ("anche", "bonds:7"), ("Un", "stamp:A CATENA")],
 64: [("È", "bonds:7"), ("Nei", "stamp:DEFAULT"), ("In", "big:1,125 MLD €|in default")],
 65: [("In", "cal:NOVEMBRE 2002|2 SETT."), ("sette", "bonds:7"), ("Le", "savers")],
 66: [("Titoli", "map:Lussemburgo|10|Lussemburgo"), ("dettagli", "i:can|L'ETICHETTA NON LO DICE")],
 67: [("Proviamo", "fig:man|UN RISPARMIATORE"), ("Hai", "ii:shop|IL SUPERMERCATO|can|UNA MARCA NOTA"), ("Ti", "i:shield_ok|SEMBRAVA PRUDENTE"), ("E", "stamp:BLOCCATO")],
 68: [("Facciamo", "i:calc|UN ALTRO CONTO"), ("Dalla", "tl:1856|TORINO;2002|DEFAULT"), ("centoquarantasei", "big:146 anni|dalla fondazione al default"), ("Non", "debt:0.75|z")],
 69: [("Dopo", "tree5"), ("Compresa", "i:ball|ANCHE LA SQUADRA")],
 70: [("Il", "cal:GENNAIO 2003|3"), ("Cragnotti", "fig:suit|DIMISSIONI"), ("All'inizio", "i:can|LASCIA ANCHE LA CIRIO")],
 71: [("Per", "doc:PIANO DI RISTRUTTURAZIONE|debiti del gruppo|schema"), ("consulenti", "ii:suit_icon|CONSULENTI|calc|")],
 72: [("Ma", "crowd"), ("Nel", "cal:LUGLIO|2003"), ("boccia", "stamp:BOCCIATO")],
 73: [("A", "h:Una sola\n*strada*"), ("Nell'estate", "court:TRIBUNALE DI ROMA"), ("insolvenza", "stamp:INSOLVENZA"), ("amministrazione", "t:AMMINISTRAZIONE STRAORDINARIA")],
 74: [("Che", "h:Che cos'è l'*amministrazione*\n*straordinaria*?"), ("È", "i:factory|GRANDI IMPRESE IN CRISI"), ("L'azienda", "ii:factory|NON CHIUDE SUBITO|ministry|COMMISSARI DELLO STATO")],
 75: [("Attenzione", "i:magnifier|ATTENZIONE ALLE PAROLE"), ("Insolvenza", "h:*Insolvenza*\nnon riesce a pagare"), ("Non", "i:shield_ok|NON È UN REATO"), ("Quello", "i:court|LO STABILISCONO I GIUDICI")],
 76: [("I", "ii:report|COMMISSARIO|report|COMMISSARIO"), ("Provare", "iii:factory|FABBRICHE|can|MARCHI|family|LAVORO"), ("E", "i:moneybag|PAGARE I CREDITORI")],
 77: [("I", "tree6"), ("Tra", "i:can|CIRIO E DE RICA"), ("cuore", "t:IL CUORE STORICO DEL GRUPPO")],
 78: [("Intanto", "crowd"), ("che", "i:megaphone|ASSOCIAZIONI DEI CONSUMATORI"), ("La", "h:Chi ci ha venduto\n*quei titoli*?")],
 79: [("Il", "i:can|UN SIMBOLO"), ("E", "ii:milk|PARMALAT|newspaper|FINE 2003"), ("In", "i:meeting|UN LUNGO DIBATTITO")],
 80: [("Riepilogo", "t:RIEPILOGO"), ("Sette", "bonds:7"), ("Il", "stamp:DEFAULT"), ("Nel", "tl:2002|DEFAULT;2003|AMM. STRAORDINARIA")],
 81: [("Mentre", "ii:report|COMMISSARI|court|PROCURA DI ROMA"), ("Nel", "cal:INCHIESTA|2003")],
 82: [("Le", "doc:IPOTESI DI REATO|…|…|bancarotta fraudolenta"), ("Tra", "stamp:BANCAROTTA")],
 83: [("Che", "h:Che cos'è la\n*bancarotta*?"), ("È", "ii:factory|IMPRESA INSOLVENTE|family|CREDITORI DANNEGGIATI"), ("Ce", "t:DIVERSI TIPI")],
 84: [("Si", "h:Bancarotta *distrattiva*"), ("portati", "flow:AZIENDA>ALTRI SCOPI"), ("E", "h:Bancarotta *preferenziale*"), ("si", "flow:PRIMA ALCUNI>POI GLI ALTRI")],
 85: [("Tenete", "ii:report|DISTRATTIVA|report|PREFERENZIALE"), ("i", "flow:SOLDI>ALTRE SOCIETÀ"), ("e", "debt:0.75")],
 86: [("Nell'inchiesta", "crowd"), ("Tra", "iii:family|FAMILIARI|suit_icon|COLLABORATORI|bank|DIRIGENTI DI BANCA"), ("Per", "stamp:SOLO INDAGATI")],
 87: [("Poi", "h:La *svolta*"), ("L'undici", "cal:FEBBRAIO 2004|11"), ("Sergio", "fig:police|"), ("arrestato", "i:handcuffs|ARRESTATO")],
 88: [("L'ex", "i:shield_q|EX PRESIDENTE"), ("l'uomo", "i:can|UN PEZZO DI STORIA"), ("viene", "tl:2000|SCUDETTO;2004|ARRESTO")],
 89: [("Le", "i:hourglass|ANNI DI INDAGINI"), ("Bisogna", "worldroute:Roma>Lussemburgo>San Paolo"), ("capire", "i:magnifier|DOVE SONO FINITI I SOLDI?")],
 90: [("Il", "cal:SETTEMBRE 2007|25"), ("Il", "i:gavel|RINVIO A GIUDIZIO"), ("Gli", "crowd"), ("trentacinque", "t:35 IMPUTATI")],
 91: [("Siamo", "court:TRIBUNALE DI ROMA"), ("Il", "i:hourglass|ANNI DI UDIENZE"), ("Davanti", "iii:lab|PERITI|suit_icon|CONSULENTI|family|RISPARMIATORI")],
 92: [("Nel", "cal:RICHIESTE|2011"), ("Per", "big:15 anni|la richiesta dell'accusa")],
 93: [("Il", "cal:LUGLIO 2011|4"), ("Sergio", "card:PRIMO GRADO|Sergio Cragnotti|bancarotta e truffa|9 anni"), ("nove", "stamp:PRIMO GRADO")],
 94: [("Viene", "card:PRIMO GRADO|un banchiere|4 anni"), ("Condanne", "iii:family|FAMILIARI|suit_icon|COLLABORATORI|gavel|")],
 95: [("Non", "scales"), ("altri", "stamp:ASSOLTI"), ("per", "i:shield_ok|CHI È ASSOLTO È INNOCENTE")],
 96: [("Il", "h:La *provvisionale*"), ("di", "big:200 MLN €|anticipo sul risarcimento"), ("A", "ii:gavel|CONDANNATI|bank|RESPONSABILE CIVILE")],
 97: [("Facciamo", "i:calc|IL CONFRONTO"), ("Duecento", "bars:IN DEFAULT|1125|PROVVISIONALE|200"), ("E", "stamp:NON DEFINITIVA")],
 98: [("Ma", "tl3"), ("Fino", "i:shield_ok|NON COLPEVOLE FINO ALLA FINE")],
 99: [("In", "card:APPELLO|Sergio Cragnotti|8 anni e 8 mesi"), ("Nell'aprile", "cal:APRILE|2015"), ("conferma", "card:APPELLO|il banchiere|4 anni confermati")],
 100: [("Poi", "court:CORTE DI CASSAZIONE"), ("Siamo", "cal:OTTOBRE|2017"), ("Quindici", "tl:2002|DEFAULT;2017|CASSAZIONE")],
 101: [("Per", "card:DEFINITIVA|il banchiere|4 anni"), ("Tre", "bars:PENA|4|INDULTO|3"), ("indulto", "t:INDULTO DEL 2006")],
 102: [("Per", "card:CASSAZIONE 2017|Sergio Cragnotti|annullamento con rinvio|(una parte)"), ("Il", "worldroute:Roma>San Paolo"), ("Bombril", "t:BOMBRIL · BANCAROTTA DISTRATTIVA")],
 103: [("Annullare", "h:Annullare con rinvio\n*≠ assolvere*"), ("Vuol", "court:NUOVO APPELLO"), ("Il", "stamp:CONFERMATO IL RESTO")],
 104: [("Il", "cal:GIUGNO 2019|26"), ("ridetermina", "card:APPELLO BIS|Sergio Cragnotti|5 anni e 3 mesi")],
 105: [("Cragnotti", "court:CORTE DI CASSAZIONE"), ("Nel", "cal:MARZO|2021"), ("La", "card:SENTENZA DEFINITIVA|Sergio Cragnotti|5 anni e 3 mesi|marzo 2021"), ("definitiva", "stamp:DEFINITIVA")],
 106: [("Che", "h:*Inammissibile*"), ("Che", "i:report|IL RICORSO"), ("A", "stamp:DEFINITIVA")],
 107: [("Fermiamoci", "i:hourglass|LE DATE"), ("Il", "tl:2002|DEFAULT;2021|DEFINITIVA"), ("In", "big:> 18 anni|dal default alla sentenza definitiva")],
 108: [("Riepilogo", "tlfull")],
 109: [("Accanto", "ii:gavel|PENALE|report|CIVILE"), ("E", "ii:can|CIRIO|milk|PARMALAT")],
 110: [("Il", "cal:FEBBRAIO 2008|13"), ("condanna", "court:TRIBUNALE CIVILE"), ("trecento", "big:300 MLN €|all'amministrazione straordinaria · primo grado civile")],
 111: [("È", "i:court|SENTENZA CIVILE"), ("primo", "stamp:PRIMO GRADO"), ("Ma", "tl:1999|VENDITA DEL LATTE;2002|DEFAULT")],
 112: [("E", "i:factory|E LE FABBRICHE?"), ("Nel", "cal:VENDITA|2004"), ("Conserve", "iii:tree|COOPERATIVE|can|CIRIO|peas|DE RICA")],
 113: [("Il", "bars:OFFERTA|150|VENDITA|168"), ("si", "t:CIFRE NON CONCORDI")],
 114: [("Il", "i:can|IL MARCHIO SOPRAVVIVE"), ("Le", "ii:shop|SUGLI SCAFFALI|tree|AGRICOLTORI ASSOCIATI")],
 115: [("La", "i:shield_q|LA LAZIO"), ("Per", "crowd")],
 116: [("E", "savers"), ("Una", "court:PARTE CIVILE"), ("Ma", "bars:BOND IN DEFAULT|1125|PROVVISIONALE|200")],
 117: [("Il", "ii:can|CIRIO|milk|PARMALAT"), ("Si", "iii:eye|TRASPARENZA|bank|CONFLITTI DI INTERESSE|family|LO SPORTELLO")],
 118: [("Un", "t:RIEPILOGO"), ("Condanna", "card:DEFINITIVA|Sergio Cragnotti|5 anni e 3 mesi|2021"), ("Condanna", "card:DEFINITIVA|un banchiere|4 anni|2017"), ("Il", "i:can|IL MARCHIO VIVE ANCORA")],
 119: [("Restano", "i:question|LE DOMANDE APERTE"), ("Il", "i:calc|LE CIFRE")],
 120: [("Il", "big:1,125 MLD €|la cifra più citata"), ("Altre", "bars:1,125 MLD|1125|1,2 MLD|1200|1,25 MLD|1250"), ("Dipende", "t:DIPENDE DA COSA SI CONTA")],
 121: [("Anche", "cal:NOVEMBRE 2002|3"), ("il", "t:3 NOV: SCADENZA · 7 O 8 NOV: DICHIARAZIONE")],
 122: [("La", "i:question|CHI SAPEVA?"), ("Chi", "ii:bank|LO SPORTELLO|family|IL CLIENTE")],
 123: [("Su", "scales"), ("Alcuni", "ii:gavel|CONDANNATI|shield_ok|ASSOLTI"), ("Ed", "i:court|QUELLO CHE DICONO I GIUDICI")],
 124: [("La", "ii:can|CIRIO|milk|PARMALAT"), ("La", "flow:EUROLAT 1999>PARMALAT"), ("Una", "stamp:PRIMO GRADO CIVILE")],
 125: [("E", "i:question|SI POTEVA EVITARE?"), ("Un", "big:> 1 MLD €|debiti già nel 1999"), ("e", "bonds:7"), ("I", "i:warning|I SEGNALI C'ERANO")],
 126: [("Che", "h:La *lezione*"), ("Non", "t:NON È CONSULENZA FINANZIARIA"), ("è", "i:report|5 DOMANDE PRIMA DI FIRMARE")],
 127: [("Prima", "h:*1*\nChi emette, e da dove?"), ("Se", "i:luxbank|SOCIETÀ VEICOLO?"), ("chi", "i:shield|CHI GARANTISCE?")],
 128: [("Seconda", "h:*2*\nPerché rende così tanto?"), ("Un", "ii:chart|RENDIMENTO ALTO|warning|= RISCHIO ALTO")],
 129: [("Terza", "h:*3*\nRating e prospetto?"), ("esiste", "i:rating_q|RATING?"), ("Esiste", "i:report|PROSPETTO?"), ("Se", "fig:suit|PER PROFESSIONISTI?")],
 130: [("Quarta", "h:*4*\nQuanto su un solo nome?"), ("Concentrare", "i:pie|TUTTO IN UN SOLO NOME"), ("vuol", "i:basket|MEGLIO DIVIDERE IL RISCHIO")],
 131: [("Quinta", "h:*5*\nE se non paga?"), ("Un'obbligazione", "ii:bond|OBBLIGAZIONE|piggy|CONTO CORRENTE"), ("Se", "stamp:DEFAULT")],
 132: [("Una", "i:can|UNA MARCA FAMOSA…"), ("Nel", "savers"), ("Ma", "bond:il nome sul titolo|non dice quanto è indebitato|chi lo emette")],
 133: [("Dove", "i:book|DOVE INFORMARSI"), ("La", "ii:book|GUIDE CONSOB|book|GUIDE BANCA D'ITALIA"), ("Leggerle", "i:clock")],
 134: [("Ricapitoliamo", "h:Il *verdetto*"), ("Uno", "i:can|1 · TORINO 1856"), ("diventa", "debt:0.2")],
 135: [("Due", "bonds:7"), ("trentacinquemila", "savers")],
 136: [("Tre", "bond:150 milioni|non rimborsato"), ("default", "stamp:DEFAULT"), ("Quattro", "court:AMMINISTRAZIONE STRAORDINARIA")],
 137: [("Cinque", "debt:0.75"), ("Sei", "card:SENTENZA DEFINITIVA|Sergio Cragnotti|5 anni e 3 mesi|2021")],
 138: [("E", "h:E tu, avresti\ncomprato quel *bond*?"), ("Scrivilo", "i:bubble_icon|SCRIVILO NEI COMMENTI"), ("Le", "i:report|FONTI IN DESCRIZIONE")],
 139: [("Iscriviti", "subscribe")],
}

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

# icone alternative quando un nome non esiste nella libreria
ALIAS = {"handshake": "meeting", "suit_icon": "head", "bubble_icon": "envelope", "clock": "hourglass", "lab": "magnifier", "coupon": "bond",
         "shield": "shield_ok", "warn": "warning", "eye": "magnifier", "tree": "coop"}
def IC(n): return ALIAS.get(n, n)

TREE_N = [("CIRIO\nCONSERVE", (150, 40, 36)), ("LATTE\n(EUROLAT)", (60, 110, 180)), ("DEL MONTE", (70, 120, 70)),
          ("BOMBRIL\nBRASILE", (120, 90, 60)), ("LAZIO\n(QUOTA)", (90, 130, 190))]

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
    elif k == "card":
        sc.add(Img(label_card(p[1:], 640, title=p[0], seed=i), (960, 560), t0, t1, anim="drop", rot=-2 + (i % 3)), "paper")
    elif k == "bond":
        sc.add(Img(bond17(760, lines=tuple(p), seed=i), (960, 570), t0, t1, anim="drop", rot=-2 + (i % 4)), "paper")
    elif k == "doc":
        sc.add(Img(doc_typed(720, 520, p[0], p[1:], seed=i), (960, 570), t0, t1, anim="drop", rot=-2), "paper")
    elif k == "bonds":
        n = int(p[0])
        for j in range(n):
            sc.add(Img(bond17(330, lines=("2000-2002",), seed=j + i), (420 + (j % 4) * 360, 430 + (j // 4) * 280), t0 + j * 0.18, t1, anim="drop", rot=-6 + (j * 3) % 12), "paper")
    elif k == "map":
        cen, ppd = p[0], float(p[1]) * 4; pins = p[2].split(",") if len(p) > 2 and p[2] else [cen]
        if len(pins) > 1:
            ll = [WPL[q] for q in pins]; lo0, lo1 = min(x for x, y in ll), max(x for x, y in ll); la0, la1 = min(y for x, y in ll), max(y for x, y in ll)
            cen = ((lo0 + lo1) / 2, (la0 + la1) / 2); ppd = min(ppd, 1100 / max(1, lo1 - lo0), 420 / max(1, la1 - la0))
        routes = [dict(pts=p[3].split(">"), t=t0 + 0.6, d=1.2, icon="money", color=GOLD)] if len(p) > 3 else []
        sc.add(WorldMap(MAPB, [(t0, cen, ppd * 0.8), (t1 or a + dur, cen, ppd)], t0, t1,
                        pins=[dict(at=q, label=q.upper(), t=t0 + 0.3 + 0.2 * j, side="r", color=(RED if j == 0 else GOLD)) for j, q in enumerate(pins)],
                        routes=routes, title=MT))
    elif k == "worldroute":
        pts = arg.split(">"); ll = [pon.wwhere(q) if hasattr(pon, "wwhere") else WPL[q] for q in pts]
        lo0, lo1 = min(x for x, y in ll), max(x for x, y in ll); la0, la1 = min(y for x, y in ll), max(y for x, y in ll)
        cen = ((lo0 + lo1) / 2, (la0 + la1) / 2); ppd = min(1300 / max(1, lo1 - lo0), 480 / max(1, la1 - la0), 40)
        sc.add(WorldMap(MAPB, [(t0, cen, ppd * 0.85), (t1 or a + dur, cen, ppd)], t0, t1,
                        pins=[dict(at=q, label=q.upper(), t=t0 + 0.3 + 0.5 * j, side="r", color=(RED if j == 0 else GOLD)) for j, q in enumerate(pts)],
                        routes=[dict(pts=[pts[j], pts[j + 1]], t=t0 + 0.6 + 0.9 * j, d=1.0, icon="ship" if i < 15 else "plane", color=GOLD) for j in range(len(pts) - 1)], title=MT))
    elif k == "debt":
        q = float(p[0]); z = len(p) > 1
        q0 = 0.0 if q < 0.3 else 0.25
        sc.add(DebtShift(DB, t0, t1, shift=[(t0, q0), (t0 + 0.6, q)], zero_t=(t0 + 1.8 if z else None), n=10))
    elif k.startswith("tree"):
        n = int(k[4:]); nodes = []
        for j, (lab, col) in enumerate(TREE_N):
            if j <= n or n >= 4:
                nodes.append((lab, t0 + (0.2 + 0.5 * j if (j == n or n >= 4) else -5), col))
        cut = {1: t0 + 0.8} if n in (3, 4, 5, 6) else {}
        if n >= 5: cut = {0: t0 + 0.9, 1: t0 - 5, 2: t0 + 1.2, 3: t0 + 1.5, 4: t0 + 1.8}
        sc.add(GroupTree(TB, "LE SOCIETÀ DI FAMIGLIA", nodes[:5] if n > 0 else nodes[:1], t0, t1, cut=cut))
        if n == 3: sc.add(Pill("LATTE VENDUTO ALLA PARMALAT (1999)", (960, 860), t0 + 0.9, t1, size=34, accent=True))
    elif k == "savers":
        sc.add(Savers((260, 520, 1660, 860), 7, t0, t1, drop_t=t0 + 1.2, s=0.8, seed=i))
    elif k == "crowd":
        sc.add(Crowd((200, 420, 1720, 860), 26, t0, t1, s=0.42, seed=i))
    elif k == "tl":
        evs = [e.split("|") for e in arg.split(";")]
        sc.add(Timeline(300, 1620, 600, [dict(top=e[0], bottom=e[1], t=t0 + 0.3 + 0.6 * j, hl=(j == len(evs) - 1)) for j, e in enumerate(evs)], t0, t1, size=46))
    elif k == "tl3":
        sc.add(Timeline(360, 1560, 600, [dict(top="1° GRADO", bottom="tribunale", t=t0 + 0.3), dict(top="2° GRADO", bottom="corte d'appello", t=t0 + 1.2),
                                         dict(top="3° GRADO", bottom="Cassazione", t=t0 + 2.1, hl=True)], t0, t1, size=46))
    elif k == "tlfull":
        evs = [("2002", "default", "Default"), ("2003", "amm. straordinaria", "Amministrazione"), ("2004", "arresto", "Arresto"),
               ("2011", "1° grado: 9 anni", "Primo"), ("2021", "definitiva:\n5 anni e 3 mesi", "Definitiva")]
        sc.add(Timeline(220, 1700, 600, [dict(top=y, bottom=b, t=TT(w) - 0.2, hl=(j == 4)) for j, (y, b, w) in enumerate(evs)], t0, t1, size=46))
    elif k == "court":
        sc.add(Icon("court", (960, 470), t0, t1, size=380, label=arg), "pop")
        sc.add(Figure([(t0, 1420, FY)], t0 + 0.3, t1, kind="judge", s=0.9, flip=-1), "pop")
    elif k == "scales":
        sc.add(Icon("scales", (960, 540), t0, t1, size=380, label="LA GIUSTIZIA DECIDE CASO PER CASO"), "pop")
    elif k == "bars":
        vals = [(p[2 * j], float(p[2 * j + 1])) for j in range(len(p) // 2)]; mx = max(v for _, v in vals)
        for j, (lab, v) in enumerate(vals):
            y = 420 + j * 150
            sc.add(Text(lab, (300, y - 40), t0 + 0.2 * j, t1, size=40, fnt=OSW, color=GOLD))
            sc.add(Bar(300, y + 20, 1300, 60, [(t0 + 0.2 * j, 0.0), (t0 + 0.2 * j + 0.8, v / mx)], t0 + 0.2 * j, t1, color=(RED if j == len(vals) - 1 else (90, 110, 160))))
    elif k == "flow":
        a_, b_ = arg.split(">")
        sc.add(Pill(a_, (560, 560), t0, t1, size=52))
        sc.add(Arrow((800, 560), (1120, 560), t0 + 0.3, t1, color=RED))
        sc.add(Pill(b_, (1380, 560), t0 + 0.7, t1, size=52, accent=True))
    elif k == "cover":
        sc.add(Img(cover_folder17(620), (960, 560), t0, t1, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 017", (1180, 360), t0 + 0.6, t1, size=70, rot=-12))
    elif k == "subscribe":
        sc.add(Img(wordmark(120), (960, 470), t0, t1, anim="pop", shadow=False), "hit")
        sc.add(Pill("ISCRIVITI · OGNI GIORNO UN NUOVO CASO", (960, 700), t0 + 0.4, t1, size=50, accent=True))
    elif k == "fig":
        sc.add(Figure(walk([(-120, FY), (300, FY)], t0, 420), t0, t1, kind=p[0], s=1.0, label=(p[1] if len(p) > 1 and p[1] else None)), "pop")
    else:
        raise ValueError(cmd)

TT = None
def build(i, dur, a, words):
    global TT
    T0 = Clock(words, a)
    used = {}
    def T(p, n=None):
        cs = lambda s: re.sub(r"[^\w']", "", s.lower())
        hits = [w for w in words if cs(w[0]) == cs(p)] or [w for w in words if cs(w[0]).startswith(cs(p))]
        if n is None:
            n = used.get(p, 0); used[p] = n + 1
        if hits: return a + hits[min(n, len(hits) - 1)][1]
        return None
    TT = lambda w: (T(w, 0) or a + 0.5)
    sc = Scene(dur); E = a + dur
    h = SCENES_H[i][0]
    start = a
    if FIRST.get(h) == i and h > 0:
        num = f"{h:02d}" if h < 12 else None
        title = CHT[h]
        sc.add(Chapter(num, title, a, a + 2.4)); start = a + 2.5
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
    bg = make_bg(17).convert("RGBA"); lay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    im = rich_img("Il crac\n*Cirio*", SERIF, 210, color=WHITE, lh=1.0)
    place(lay, im, (90, 170), "la")
    can = fx.icon("can", 520); place(lay, can, (1500, 430), "mm")
    for j in range(3):
        b = bond17(330, lines=("default",), seed=j + 3).rotate(-12 + j * 10, expand=True, resample=Image.BICUBIC)
        place(lay, b, (1450 + j * 150, 900 - j * 30), "mm")
    st = stamp_img("DEFAULT", size=110, rot=-10); place(lay, st, (1560, 250), "mm")
    st2 = stamp_img("CASO 017", size=60, rot=-8); place(lay, st2, (380, 90), "mm")
    f = font(OSW, 54, 700); s_ = "OLTRE 1,1 MILIARDI IN BOND · 35.000 RISPARMIATORI"; tw = tl(d, s_, f)
    d.rectangle([90, 760, 90 + tw + 60, 880], fill=(230, 190, 40, 255))
    d.text((120, 820), s_, font=f, fill=(20, 18, 16, 255), anchor="lm")
    place(lay, wordmark(70), (90, 960), "lm")
    out = Image.alpha_composite(bg, lay).convert("RGB"); out.save(path, quality=92)
