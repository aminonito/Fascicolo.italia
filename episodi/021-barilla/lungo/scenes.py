import sys, os, re, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from bar import *
import fx, met
from script import SCENES_H, CH

W, H = 1920, 1080
FY = 870
MAPB = (160, 250, 1760, 880)
SB = (160, 270, 1760, 860)          # scenografia principale: la tangenziale (schema)
WB = (260, 260, 1660, 860)          # scenografia: il muro dei giorni
MT = "mappa: Natural Earth · schema non in scala"

FB = "Il Sole 24 Ore (2025) · Tgcom24 (2025) · Panorama (2025) · L'Eco di Bergamo (2003) · Il Giornale (2005, 2017) · Wikipedia · art643.org"
F = {0: "Fonti: " + FB,
     1: "Fonti: Il Giornale (2005, 2017) · Wikipedia (Fiat Tipo, Tangentopoli) · Il Sole 24 Ore (2025)",
     2: "Fonti: " + FB,
     3: "Fonti: Panorama (2025) · Tgcom24 (2025) · art643.org · Il Sole 24 Ore (2025) · Wikipedia · L'Eco di Bergamo (2003)",
     4: "Fonti: Il Sole 24 Ore (2025) · Tgcom24 · Panorama · L'Eco di Bergamo (2003) · Il Giornale (2005, 2017) · Wikipedia · art643.org",
     5: "Fonti: Il Sole 24 Ore (2025) · Panorama · Tgcom24 · Blitz quotidiano (2016) · Wikipedia · Il Giornale (2005, 2017)",
     6: "Fonti: Il Giornale (2017) · Wikipedia · art643.org · L'Eco di Bergamo (2003) · Il Sole 24 Ore (2025)",
     7: "Fonti: L'Eco di Bergamo (2003) · Blitz quotidiano (2016) · Il Giornale (2005, 2017) · Tgcom24 · Wikipedia · art643.org",
     8: "Fonti: Il Sole 24 Ore (2025) · Panorama · Tgcom24 · L'Eco di Bergamo (2003) · Il Giornale (2007) · Tempi (2011) · Wikipedia",
     9: "Fonti: L'Eco di Bergamo (2003) · art643.org · Il Sole 24 Ore (2025) · Tgcom24 · Wikipedia · Panorama · Blitz quotidiano",
     10: "Fonti: L'Eco di Bergamo (2003) · art643.org · Il Sole 24 Ore (2025) · Panorama · Tgcom24 · Brocardi e Filodiritto (art. 643 c.p.p.) · Wikipedia",
     11: "Fonti: Il Sole 24 Ore (2025) · Tgcom24 · Wikipedia · art643.org · L'Eco di Bergamo (2003) · Blitz quotidiano",
     12: "Fonti: Il Post (2024) · Il Sole 24 Ore (2024, 2025) · Ministero della Giustizia · Brocardi (artt. 314, 643 c.p.p.) · non è consulenza legale",
     13: "Fonti: tutte in descrizione · ricostruzione a scopo divulgativo"}

CHT = {1: "Milano,\n*febbraio 1992*", 2: "I *protagonisti*", 3: "L'*operazione*", 4: "La sera del\n*13 febbraio*",
       5: "Le prime *ore*", 6: "Le accuse\ne i *processi*", 7: "Gli anni\nin *cella*", 8: "La *svolta*", 9: "La *revisione*",
       10: "Il risarcimento\ne il *dopo*", 11: "Le domande *aperte*", 12: "La *lezione*", 13: "Il *verdetto*"}
FIRST = {}
for k, (h, _) in enumerate(SCENES_H):
    FIRST.setdefault(h, k)

BOARD = [("DANIELE BARILLÀ", "imprenditore · Brianza", "person"), ("IL ROS DI GENOVA", "carabinieri · l'operazione", "card"),
         ("L'UFFICIALE", "guida l'operazione · nessun nome", "person"), ("I TRAFFICANTI", "fuggiti · nessun nome", "card"),
         ("I GIUDICI", "condanna · poi revisione", "card"), ("CHI NON SI ARRENDE", "avvocato · giornalista", "person")]
BXY = [(420, 450), (960, 450), (1500, 450), (420, 740), (960, 740), (1500, 740)]

def board_el(n, t0, t1):
    nodes = {}
    for j in range(n + 1):
        nm, role, kind = BOARD[j]
        nodes[f"n{j}"] = dict(xy=BXY[j], name=nm, role=role, t=t0 + (0.2 if j == n else -5), rot=(-3 + 2 * (j % 3)))
    pairs = [(0, 1), (1, 2), (2, 3), (0, 4), (4, 5), (0, 5)]
    links = [(f"n{p}", f"n{q}", t0 - 5 if max(p, q) < n else t0 + 0.6) for p, q in pairs if max(p, q) <= n]
    return Board(nodes, links, t0, t1, cw=220)

# ------------------------------------------------------------------ scaletta visiva: (parola, comando)
V = {
 0: [("13", "cal:13 FEBBRAIO|1992"), ("sera", "i:rose|LA SERA PRIMA DI SAN VALENTINO"), ("Brianza", "map:Nova Milanese|35|Milano,Nova Milanese"), ("imprenditore", "fig:man|UN PICCOLO IMPRENDITORE"), ("Fiat", "i:tipo|FIAT TIPO ROSSO AMARANTO · SCHEMA")],
 1: [("Quella", "strada:night"), ("fermato", "strada:stop"), ("investigatori", "i:nophoto|«UN TRAFFICANTE»"), ("errore", "stamp:ERRORE"), ("ragione", "i:hourglass|ANNI")],
 2: [("Sette", "muro:1999.53"), ("condanna", "i:gavel|CONDANNA DEFINITIVA"), ("revisione", "i:folder|LA REVISIONE"), ("commesso", "stamp:ASSOLTO"), ("questo", "ii:tipo|UN UOMO|tipo_b|UN ALTRO")],
 3: [("Questo", "cover"), ("sbagliato", "t:L'UOMO SBAGLIATO")],
 4: [("Partiamo", "h:Il *luogo*\ne il *momento*"), ("Febbraio", "cal:FEBBRAIO|1992"), ("lira", "i:lire|LA LIRA"), ("cellulari", "i:phone|CELLULARI RARI"), ("uomini", "iii:sportcar|AUTO|fig_icon|UOMINI|mic|RADIO")],
 5: [("Milano", "map:Milano|35|Milano"), ("Brianza", "map:Nova Milanese|35|Milano,Nova Milanese,Monza"), ("paesi", "iii:house|PAESI|factory|CAPANNONI|shop|PICCOLE AZIENDE")],
 6: [("strade", "strada:night"), ("Di", "crowd_cars"), ("modello", "i:tipo|OVUNQUE")],
 7: [("Tipo", "i:tipo|BERLINA A DUE VOLUMI · SCHEMA"), ("comune", "bars:AUTO COMUNI|10|AUTO RARE|3"), ("Due", "ii:tipo|UNA|tipo|L'ALTRA"), ("impossibili", "t:DI NOTTE: QUASI IMPOSSIBILI DA DISTINGUERE")],
 8: [("Non", "h:Un'auto\n*di successo*"), ("eletta", "cal:AUTO EUROPEA DELL'ANNO|1989"), ("strade", "iii:tipo|STRADE|factory|AZIENDE|house|CASE"), ("notizia", "stamp:NESSUNA NOTIZIA")],
 9: [("C'è", "h:Un dettaglio\ndi *calendario*"), ("17", "cal:17 FEBBRAIO|1992"), ("Chiesa", "news:CRONACA|18 febbraio 1992|*Milano:*\narrestato un amministratore|ricostruzione grafica · non l'originale"), ("l'inizio", "t:INIZIA MANI PULITE")],
 10: [("Per", "i:newspaper|PRIME PAGINE SU MANI PULITE"), ("storia", "flow:L'ARRESTO DI BARILLÀ>LONTANO DALLE PRIME PAGINE")],
 11: [("Un'ultima", "h:Il *contesto*"), ("cocaina", "map:Milano|8|Milano"), ("reparti", "iii:policecar|REPARTI SPECIALI|nophoto|INFILTRATI|mic|INFORMATORI"), ("pedinamenti", "strada:follow")],
 12: [("Ed", "i:eye|IL RICONOSCIMENTO A VISTA"), ("debole", "stamp:PUNTO DEBOLE")],
 13: [("Apriamo", "board:0"), ("trent'anni", "big:≈ 30 anni|all'arresto")],
 14: [("È", "map:Nova Milanese|35|Nova Milanese,Milano"), ("materiale", "i:cable|CAVI ELETTRICI"), ("quindicina", "big:15|dipendenti · secondo le fonti")],
 15: [("Ha", "iii:rose|UNA FIDANZATA|family|UNA FAMIGLIA|factory|UN'ATTIVITÀ"), ("Niente", "i:magnifier|NESSUN LEGAME CON LA DROGA NELLE FONTI")],
 16: [("Il", "board:1"), ("raggruppamento", "card:R.O.S.|raggruppamento operativo speciale|carabinieri"), ("Genova", "map:Genova|60|Genova,Milano")],
 17: [("Il", "cal:NASCE IL ROS|1990"), ("indagini", "ii:chain|CRIMINALITÀ ORGANIZZATA|warn|TERRORISMO"), ("tecniche", "iii:nophoto|SOTTO COPERTURA|mic|INFORMATORI|magnifier|INDAGINI")],
 18: [("A", "board:2"), ("nome", "i:nophoto|NESSUN NOME"), ("accusato", "t:ACCUSATO ANNI DOPO · VICENDE DIVERSE")],
 19: [("Il", "board:3"), ("fuggire", "i:question|CHI ERANO?"), ("nessun", "stamp:NESSUN NOME")],
 20: [("Il", "board:4"), ("condannano", "ii:gavel|CHI CONDANNA|scalesok|CHI ASSOLVE"), ("sistema", "tl:PRIMO GRADO|;APPELLO|;CASSAZIONE|")],
 21: [("Infine", "board:5"), ("avvocato", "iii:scales|UN AVVOCATO|pen|UN GIORNALISTA|nophoto|LUI STESSO")],
 22: [("Una", "h:Nota di *metodo*"), ("due", "big:2 fonti|per ogni fatto"), ("coincidono", "t:VERSIONI DIVERSE: LO DICIAMO"), ("dettagli", "i:emptyfolder|UNA SOLA FONTE: FUORI")],
 23: [("Come", "h:Come *nasce*\nquella sera?"), ("un'indagine", "i:magnifier|UN'INDAGINE SULLA COCAINA"), ("Genova", "map:Genova|60|Genova,Milano|Genova>Milano")],
 24: [("Secondo", "i:crate|IL CARICO"), ("cinquanta", "big:50 kg|di cocaina · secondo le ricostruzioni"), ("Viaggia", "i:fiat|UN'ALTRA AUTO · SCHEMA"), ("diretta", "map:Nova Milanese|35|Nova Milanese,Milano")],
 25: [("Nell'operazione", "i:sportcar|UN'ALTRA AUTO DEL GRUPPO"), ("È", "i:tipo|FIAT TIPO ROSSO AMARANTO"), ("tengono", "i:eye|L'AUTO TENUTA D'OCCHIO")],
 26: [("Per", "strada:follow"), ("auto", "iii:sportcar|AUTO CIVETTA|fig_icon|IN BORGHESE|mic|RADIO"), ("distanza", "strada:follow"), ("lontani", "stamp:VISTA PERSA?")],
 27: [("Un", "i:moon|DI SERA"), ("luci", "iii:bulb|FARI|eye|COLORI|plate|TARGHE"), ("forma", "i:tipo|FORMA E COLORE")],
 28: [("Ora", "h:Mettiamo\ninsieme i *pezzi*"), ("seguire", "i:tipo|L'AUTO DA SEGUIRE"), ("zona", "map:Nova Milanese|35|Nova Milanese,Milano"), ("sera", "cal:13 FEBBRAIO|1992"), ("un'altra", "ii:tipo|LA PRIMA|tipo_b|LA SECONDA")],
 29: [("Le", "ii:tipo|STESSO MODELLO|tipo|STESSO COLORE"), ("targhe", "i:plates2|TARGHE SIMILI · DETTAGLI COPERTI"), ("alcune", "flow:QUASI IDENTICHE>TRE CIFRE IN COMUNE")],
 30: [("Facciamo", "i:calc|QUANTO È RARO?"), ("targhe", "i:plate|PROVINCIA + CIFRE E LETTERE"), ("Che", "iii:tipo|STESSO MODELLO|eye|STESSO COLORE|plate|TARGA SIMILE"), ("coincidenza", "stamp:RARISSIMA")],
 31: [("Ma", "i:chart|MILIONI DI AUTO"), ("succede", "strada:night")],
 32: [("Giovedì", "cal:GIOVEDÌ 13 FEBBRAIO|1992"), ("sera", "i:moon|SERA"), ("Daniele", "i:tipo|DANIELE BARILLÀ"), ("fidanzata", "i:rose|L'APPUNTAMENTO")],
 33: [("Nella", "strada:follow"), ("distanza", "t:IL PEDINAMENTO · SCHEMA")],
 34: [("Qui", "h:Cosa dicono\nle *fonti*"), ("Non", "iii:clock_icon|ORARI?|map_icon|PERCORSO?|question|STRADE?"), ("Quello", "i:check|CONCORDI SUL RISULTATO"), ("scambiano", "ii:tipo|LA SUA AUTO|tipo_b|SCAMBIATA")],
 35: [("Per", "t:SCHEMA SEMPLIFICATO · DINAMICA NON DOCUMENTATA"), ("Immaginiamo", "strada:night"), ("davanti", "strada:follow")],
 36: [("A", "strada:swap")],
 37: [("I", "strada:swap"), ("Daniele", "strada:stop"), ("pezzo", "t:«IL PEZZO MANCANTE»")],
 38: [("Lui", "i:question|NON CAPISCE"), ("Non", "iii:crate|CARICHI?|warn|COCAINA?|eye|PEDINAMENTI?"), ("Dice", "i:rose|«ANDAVO DALLA FIDANZATA»"), ("Ma", "i:tipo|PER LORO: LA PROVA")],
 39: [("Rivediamo", "strada:follow"), ("Un'auto", "strada:swap"), ("Stesso", "iii:tipo|MODELLO|eye|COLORE|plate|TARGA"), ("Di", "i:moon|DI SERA")],
 40: [("E", "h:Più dell'auto:\nil *riconoscimento*"), ("riconoscere", "i:eye|«È LUI»"), ("Su", "flow:IL RICONOSCIMENTO>L'ACCUSA")],
 41: [("Anni", "i:mic|IL RACCONTO DI BARILLÀ"), ("punto", "t:IL SUO PUNTO DI VISTA"), ("quell'uomo", "stamp:NON ERA LUI")],
 42: [("Le", "clock:21"), ("caserma", "iii:policecar|CASERMA|prison|CARCERE|court|IL GIUDICE")],
 43: [("L'arresto", "stamp:CONVALIDATO"), ("Da", "flow:FERMATO>INDAGATO"), ("indagato", "i:prison|IN CARCERE")],
 44: [("Spieghiamo", "h:Due *parole*"), ("convalida", "card:CONVALIDA|il controllo di un giudice|sull'arresto"), ("custodia", "card:CUSTODIA CAUTELARE|detenzione prima della sentenza|non è una condanna"), ("fuga", "ii:suitcase|RISCHIO DI FUGA|warn|NUOVI REATI"), ("condanna", "i:cell|MA SI SCONTA IN CELLA")],
 45: [("I", "news:CRONACA|febbraio 1992|*Droga:*\nblitz in Brianza|ricostruzione grafica · non l'originale"), ("presentato", "t:«ESPONENTE DI RILIEVO DELLA MALAVITA»"), ("soprannomina", "big:«L'Escobar della Brianza»|il soprannome dei giornali")],
 46: [("Il", "h:Il *soprannome*"), ("pochi", "flow:IMPRENDITORE SCONOSCIUTO>«BOSS» SULLA CARTA"), ("stampata", "i:press|DIFFICILE DA CANCELLARE")],
 47: [("Fuori", "i:factory|LA SUA VITA SI FERMA"), ("titolare", "i:nophoto|SENZA IL TITOLARE"), ("dipendenti", "crowd")],
 48: [("Le", "h:Che cosa *perde*"), ("l'azienda", "iii:factory_x|L'AZIENDA|rose|LA FIDANZATA|family|IL PADRE"), ("crepacuore", "t:SECONDO LE RICOSTRUZIONI")],
 49: [("Barillà", "h:Una sola *linea*"), ("innocente", "stamp:INNOCENTE"), ("Non", "ii:scales|NON CAMBIA VERSIONE|book|NESSUNA STORIA NUOVA"), ("Ripete", "i:rose|«ANDAVO DALLA FIDANZATA»")],
 50: [("Facciamo", "t:RIEPILOGO · 1"), ("Febbraio", "cal:FEBBRAIO|1992"), ("imprenditore", "strada:swap"), ("Viene", "strada:stop"), ("Lui", "stamp:INNOCENTE"), ("iscriviti", "subscribe")],
 51: [("Arriviamo", "court:IL PROCESSO"), ("L'accusa", "card:L'ACCUSA|traffico di stupefacenti|operazione sulla cocaina"), ("prove", "ii:tipo|L'AUTO|eye|IL RICONOSCIMENTO")],
 52: [("La", "ii:scales|LA DIFESA|tipo_b|ERRORE DI PERSONA"), ("Ma", "i:mic|LA PAROLA DEGLI INVESTIGATORI"), ("E", "bars:PESO DEL RICONOSCIMENTO|9|PESO DEI DUBBI|4")],
 53: [("Il", "court:PRIMO GRADO"), ("diciotto", "big:18 anni|primo grado")],
 54: [("Diciotto", "big:18 anni|di carcere"), ("Per", "i:calc|FACCIAMO UN CONTO"), ("uscito", "tl:1992|ARRESTO;2010|FINE PENA (IPOTESI)")],
 55: [("Poi", "court:APPELLO"), ("ridotta", "bars:PRIMO GRADO (ANNI)|18|APPELLO (ANNI)|15"), ("ancora", "i:prison|RESTA IN CARCERE")],
 56: [("Ricordiamo", "h:I tre *gradi*"), ("tre", "tl:PRIMO GRADO|I FATTI;APPELLO|I FATTI DI NUOVO;CASSAZIONE|SOLO LA LEGGE"), ("Solo", "stamp:DEFINITIVA")],
 57: [("Infine", "court:CASSAZIONE"), ("Corte", "i:book|CONTROLLA LA LEGGE"), ("Conferma", "stamp:CONFERMATA")],
 58: [("A", "i:folder|CASO CHIUSO"), ("Daniele", "card:SENTENZA DEFINITIVA|traffico di stupefacenti|15 anni")],
 59: [("C'è", "h:Un *paradosso*"), ("innocente", "flow:«SONO INNOCENTE»>«NON SI È RAVVEDUTO»"), ("carcere", "i:prison|IL GIUDIZIO DEL CARCERE")],
 60: [("Chi", "i:question|NON AMMETTE?"), ("diniego", "stamp:BENEFICI NEGATI")],
 61: [("È", "h:Il cuore\n*drammatico*"), ("innocente", "i:scalesok|L'UNICA VERITÀ"), ("Ma", "i:question|IL SEGNO DI UNA COLPA?")],
 62: [("Entriamo", "i:cell|GLI ANNI DEL CARCERE"), ("Bergamo", "map:Bergamo|35|Bergamo,Milano,Nova Milanese")],
 63: [("Il", "cal:DENTRO|1993"), ("1994", "cal:DENTRO|1994"), ("Fuori", "iii:newspaper|GOVERNI|chamber|POLITICA|lire|MONETA"), ("Dentro", "i:tally|GIORNI UGUALI")],
 64: [("Mettiamo", "muro:1999.53"), ("oltre", "big:oltre 2.700|giorni di carcere")],
 65: [("Proviamo", "h:I giorni\nin *tappe*"), ("lira", "i:lire|ENTRA: SOLO LA LIRA"), ("l'euro", "cal:L'EURO SUI MERCATI|1999"), ("monete", "cal:MONETE E BANCONOTE|2002")],
 66: [("Le", "h:Il conto *esatto*"), ("chi", "bars:7 ANNI 5 MESI 25 GIORNI|1|DIECI GIORNI IN MENO|0.99|«QUASI 8 ANNI»|1.05"), ("grandezza", "t:L'ORDINE DI GRANDEZZA È LO STESSO")],
 67: [("In", "i:cell|IN CELLA"), ("Scrive", "iii:pen|SCRIVE|letter|CHIEDE|envelope|SI RIVOLGE")],
 68: [("Secondo", "card:FRANCESCO SAVERIO BORRELLI|procuratore capo di Milano|si interessa al caso")],
 69: [("Anche", "i:pen|UN GIORNALISTA"), ("Zurlo", "card:STEFANO ZURLO|cronista giudiziario|Il Giornale"), ("Sarà", "i:book|IL LIBRO, ANNI DOPO")],
 70: [("Ma", "i:folder|UNA CONDANNA DEFINITIVA"), ("Serve", "big:un fatto nuovo|serve per riaprire"), ("inattesa", "i:question|DA DOVE?")],
 71: [("Secondo", "t:RIEPILOGO · 2"), ("Arrestato", "tl:1992|ARRESTO;PRIMO GRADO|18 ANNI;APPELLO|15 ANNI;CASSAZIONE|DEFINITIVA"), ("Sconta", "map:Bergamo|35|Bergamo,Milano")],
 72: [("La", "cal:LA SVOLTA|1997"), ("Riguarda", "board:2")],
 73: [("Quell'anno", "i:prison|ARRESTATO L'UFFICIALE"), ("metodi", "card:L'ACCUSA|metodi illeciti con gli informatori|accuse, non sentenze"), ("pagandoli", "ii:money|PAGAMENTI|crate|DROGA SEQUESTRATA"), ("accusa", "t:SECONDO L'ACCUSA")],
 74: [("Attenzione", "h:*Attenzione*"), ("Le", "flow:ACCUSE ALL'UFFICIALE>ALTRE OPERAZIONI"), ("Nessuna", "stamp:NON PER BARILLÀ")],
 75: [("Nel", "map:Genova|60|Genova"), ("condannato", "bars:PRIMO GRADO 2007 (≈ ANNI)|9.5|APPELLO (ANNI)|4.5"), ("definitivo", "i:question|ESITO DEFINITIVO: NON VERIFICATO")],
 76: [("Ma", "i:folder|LE CARTE DI QUELLA SERA"), ("Se", "flow:METODI CONTESTATI>CARTE DA RILEGGERE")],
 77: [("Il", "court:I MAGISTRATI"), ("Le", "iii:mic|DICHIARAZIONI|eye|RICONOSCIMENTI|tipo|LA SERA")],
 78: [("Ora", "i:magnifier|COL SENNO DI POI"), ("Ma", "tl:PRIMO GRADO|COLPEVOLE;APPELLO|COLPEVOLE;CASSAZIONE|COLPEVOLE"), ("Ci", "i:magnifier|UN EVENTO ESTERNO")],
 79: [("Ed", "h:Una lezione\nsulla *fiducia*"), ("Il", "i:mic|LA PAROLA DEGLI INVESTIGATORI"), ("Quando", "stamp:LA CREPA")],
 80: [("Che", "h:Che cos'è\nla *revisione*?"), ("strumento", "flow:CONDANNA DEFINITIVA>RIAPERTA"), ("quarto", "stamp:NON UN 4° GRADO"), ("casi", "i:book|SOLO CASI PRECISI")],
 81: [("La", "court:CORTE D'APPELLO"), ("Barillà", "map:Genova|60|Genova"), ("accolta", "stamp:ACCOLTA")],
 82: [("La", "i:book|I CASI DELLA LEGGE"), ("inconciliabili", "iii:scales|SENTENZE INCONCILIABILI|magnifier|PROVE NUOVE|warn|ATTI FALSI"), ("Non", "t:NON BASTA DIRE «HANNO SBAGLIATO»")],
 83: [("Il", "cal:12 LUGLIO|1999"), ("esce", "muro:1999.53"), ("Ha", "big:≈ 7 anni e mezzo|in carcere")],
 84: [("Il", "card:REVISIONE|assolto|per non aver commesso il fatto"), ("Su", "t:FONTI NON DEL TUTTO ALLINEATE"), ("maggior", "tl:LUG 1999|UNA FONTE;17 LUG 2000|LA MAGGIOR PARTE")],
 85: [("Per", "big:per non aver commesso il fatto|la formula più piena"), ("Non", "flow:NON «PROVE INSUFFICIENTI»>«NON C'ENTRAVA»")],
 86: [("Il", "news:CRONACA|1992|*«L'Escobar*\ndella Brianza»|ricostruzione grafica · non l'originale"), ("Sui", "news:CRONACA|2000|*L'uomo*\nsbagliato|ricostruzione grafica · non l'originale")],
 87: [("Dopo", "i:mic|L'ANNUNCIO"), ("lascerà", "i:passport|LASCERÀ L'ITALIA"), ("vivere", "i:plane|ALL'ESTERO")],
 88: [("Facciamo", "i:calc|I TEMPI"), ("all'uscita", "tl:FEB 1992|ARRESTO;LUG 1999|USCITA"), ("all'assoluzione", "tl:FEB 1992|ARRESTO;2000|ASSOLUZIONE"), ("1997", "tl:1997|LA SVOLTA;1999|USCITA")],
 89: [("Terzo", "t:RIEPILOGO · 3"), ("1997", "cal:LA SVOLTA|1997"), ("revisione", "court:GENOVA · REVISIONE"), ("esce", "stamp:ASSOLTO")],
 90: [("Chi", "h:La *riparazione*"), ("l'articolo", "card:ART. 643|codice di procedura penale|riparazione dell'errore giudiziario")],
 91: [("La", "iii:hourglass|LA PENA SCONTATA|family|LA FAMIGLIA|nophoto|LA PERSONA"), ("Può", "ii:money|DENARO|calendar_x|RENDITA VITALIZIA")],
 92: [("C'è", "h:Un *limite*"), ("dolo", "flow:DOLO O COLPA GRAVE>NIENTE RIPARAZIONE"), ("Non", "stamp:NON È IL SUO CASO")],
 93: [("Barillà", "card:MAURO FERRANDO|avvocato · Genova|la domanda di riparazione"), ("chiede", "big:12 miliardi|di lire · la richiesta")],
 94: [("Facciamo", "i:calc|LA CONVERSIONE"), ("cambio", "big:1.936,27|lire per un euro · cambio fisso"), ("Dodici", "big:≈ 6,2 milioni|di euro")],
 95: [("Nel", "cal:LA CASSAZIONE|2003"), ("cronache", "big:≈ 4 milioni|di euro · 8 miliardi di lire (cronache 2003)")],
 96: [("Ma", "h:La cifra\n*finale*"), ("recenti", "bars:CRONACHE 2003 (MILIONI DI €)|4|CRONACHE RECENTI · 2007|3"), ("spiegazione", "i:question|IL PASSAGGIO NON CHIARITO")],
 97: [("Facciamo", "i:calc|UN CONTO PRUDENTE"), ("Tra", "flow:3-4 MILIONI ÷ 2.700 GIORNI>1.100-1.500 € AL GIORNO")],
 98: [("Sembra", "i:money|SEMBRA TANTO"), ("Ma", "iii:family|UN PADRE|factory_x|UN'AZIENDA|rose|UNA RELAZIONE"), ("anni", "i:hourglass|GLI ANNI IN CELLA")],
 99: [("Dopo", "h:La storia\ndiventa *racconto*"), ("Zurlo", "i:book|«L'UOMO SBAGLIATO. IL CASO BARILLÀ»")],
 100: [("E", "cal:LA FICTION|2005"), ("Fiorello", "ii:tv|RAI 1 · 2005|clapper|«L'UOMO SBAGLIATO»")],
 101: [("Barillà", "i:plane|ALL'ESTERO"), ("Le", "i:flagless_globe|PAESE: FONTI NON CONCORDI"), ("Il", "i:newspaper|IL SUO NOME RESTA"), ("ogni", "stamp:TRA I PRIMI CITATI")],
 102: [("Spesso", "card:ENZO TORTORA|arrestato nel 1983|assolto nel 1987"), ("Due", "ii:tipo|UN ALTRO AL SUO POSTO|mic|LE PAROLE DI ALTRI")],
 103: [("Il", "cal:REFERENDUM|1987"), ("Vassalli", "card:LEGGE VASSALLI|1988|responsabilità civile dei magistrati"), ("Ma", "i:warn|UNA LEGGE NON BASTA")],
 104: [("Restano", "h:Le domande\n*aperte*"), ("prima", "strada:night"), ("orari", "iii:clock_icon|ORARI?|map_icon|IL PUNTO?|calc|LA DISTANZA?"), ("nessuna", "stamp:NON DOCUMENTATO")],
 105: [("La", "h:*2*"), ("chi", "i:nophoto|I VERI TRAFFICANTI?"), ("nessun", "stamp:NESSUN NOME")],
 106: [("La", "h:*3*"), ("come", "tl:PRIMO GRADO|;APPELLO|;CASSAZIONE|"), ("Le", "i:mic|LA PAROLA DEGLI INVESTIGATORI"), ("documenti", "i:emptyfolder|ATTI NON PUBBLICI IN RETE")],
 107: [("E", "h:E *ancora*"), ("silenzio", "flow:IL SILENZIO>UNA PROVA?"), ("sistema", "i:question|NESSUNA RISPOSTA SEMPLICE")],
 108: [("La", "h:*4* · le date"), ("Arresto", "bars:13 FEBBRAIO (QUASI TUTTE)|10|11 FEBBRAIO (UNA FONTE)|1"), ("Uscita", "tl:12 LUG 1999|USCITA;17 LUG 2000|ASSOLUZIONE"), ("piccole", "t:NORMALE IN UN CASO DI 30 ANNI FA")],
 109: [("La", "h:*5* · i soldi"), ("quattro", "bars:2003 (MILIONI DI €)|4|2007 (MILIONI DI €)|3"), ("Due", "i:question|IL PASSAGGIO?")],
 110: [("La", "h:*6* · le responsabilità"), ("Chi", "i:question|NE HA RISPOSTO?"), ("Nelle", "i:emptyfolder|NESSUN ESITO TROVATO"), ("nessuno", "stamp:NESSUN CONDANNATO")],
 111: [("Ed", "h:Errore\nnon è *reato*"), ("somma", "iii:eye|SVISTE|tipo_b|COINCIDENZE|mic|FIDUCIA"), ("difficile", "i:warn|DIFFICILE DA PREVENIRE")],
 112: [("Che", "h:I *numeri*"), ("1991", "tl:1991|;2022|"), ("222", "big:222|errori giudiziari riconosciuti · 1991-2022"), ("sette", "big:≈ 7|all'anno")],
 113: [("Per", "big:≈ 86 milioni|di euro di riparazioni"), ("media", "big:≈ 2,7 milioni|di euro l'anno")],
 114: [("Ogni", "crowd"), ("Ma", "h:Un numero\n*più grande*")],
 115: [("L'ingiusta", "card:INGIUSTA DETENZIONE|custodia cautelare|poi l'assoluzione"), ("carcere", "ii:cell|IN CARCERE|house|AI DOMICILIARI"), ("1992", "big:oltre 30.000|casi · 1992-2022")],
 116: [("Per", "big:oltre 800 milioni|di euro · ingiuste detenzioni"), ("Sommando", "bars:ERRORI GIUDIZIARI (MLN €)|86|INGIUSTE DETENZIONI (MLN €)|846"), ("totale", "big:oltre 930 milioni|di euro in totale")],
 117: [("E", "cal:SOLO NEL|2022"), ("otto", "ii:gavel|8 ERRORI GIUDIZIARI|cell|OLTRE 500 INGIUSTE DETENZIONI")],
 118: [("Ecco", "h:Cinque *idee*"), ("questo", "t:CONTENUTO INFORMATIVO · NON È CONSULENZA LEGALE")],
 119: [("Primo", "h:*1* · presunzione\ndi innocenza"), ("Costituzione", "card:COSTITUZIONE · ART. 27|non colpevole fino|alla condanna definitiva"), ("Un", "stamp:NON È UNA SENTENZA")],
 120: [("Secondo", "h:*2* · i riconoscimenti\npossono sbagliare"), ("Di", "iii:moon|DI SERA|eye|A DISTANZA|warn|SOTTO STRESS"), ("Il", "ii:tipo|UN'AUTO|tipo_b|CONFUSA")],
 121: [("Terzo", "h:*3* · la revisione\nesiste"), ("Anche", "flow:CONDANNA DEFINITIVA>FATTI NUOVI"), ("raro", "i:hourglass|RARO · LUNGO · POSSIBILE")],
 122: [("Quarto", "h:*4* · la riparazione\nesiste"), ("l'errore", "card:ERRORE GIUDIZIARIO|art. 643 c.p.p.|nessun tetto"), ("l'ingiusta", "card:INGIUSTA DETENZIONE · ART. 314|massimo ≈ 516.000 €|domanda entro 2 anni")],
 123: [("Quinto", "h:*5* · la cronaca\nha un peso"), ("soprannomi", "i:press|I TITOLI RESTANO"), ("Raccontare", "flow:UN ARRESTO>NON È UNA CONDANNA")],
 124: [("Ricapitoliamo", "t:IL VERDETTO"), ("Uno", "cal:13 FEBBRAIO|1992"), ("Daniele", "strada:stop")],
 125: [("Due", "strada:swap"), ("Tre", "bars:PRIMO GRADO|18|APPELLO|15")],
 126: [("Quattro", "cal:LA SVOLTA|1997"), ("Cinque", "court:GENOVA · REVISIONE"), ("esce", "stamp:ASSOLTO")],
 127: [("Sei", "big:3-4 milioni|di euro · cifre non concordi"), ("Ma", "muro:1999.53")],
 128: [("E", "ii:eye|UN RICONOSCIMENTO|gavel|BASTA?"), ("Scrivilo", "i:envelope|SCRIVILO NEI COMMENTI")],
 129: [("Iscriviti", "subscribe")],
}

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

ALIAS = {"map_icon": "globe2", "check": "shield_ok", "stop": "warn", "doc_icon": "letter", "mic": "microphone",
         "clock_icon": "hourglass", "fig_icon": "nophoto"}
def IC(n): return ALIAS.get(n, n)

class CarRow(El):
    """tante auto in coda viste di lato, tutte simili (traffico serale)"""
    def __init__(self, t0, t1=None):
        super().__init__(t0, t1, 0.3)
    def draw(self, lay, t, a):
        k = t - self.t0; cols = [(176, 36, 48), (120, 120, 130), (176, 36, 48), (60, 80, 120), (200, 200, 200), (176, 36, 48)]
        for j in range(12):
            x = 120 + ((j * 300 + k * 120) % 1800); y = 470 if j % 2 else 680
            im = fx.icon("tipo", 240)
            if cols[j % 6] != (176, 36, 48): im = fx.icon("sportcar", 240)
            place(lay, im, (x, y), "mm", a)

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
        sc.add(ClockFace((960, 520), 220, t0, t1, start=hh - 0.4, speed=0.08, label="LE PRIME ORE"), "pop")
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
            routes = [dict(pts=[pts[j], pts[j + 1]], t=t0 + 0.6 + 0.8 * j, d=1.0, icon="person", color=RED) for j in range(len(pts) - 1)]
        sc.add(WorldMap(MAPB, [(t0, cen, ppd * 0.8), (t1 or a + dur, cen, ppd)], t0, t1,
                        pins=[dict(at=q, label=q.upper(), t=t0 + 0.3 + 0.2 * j, side=("l" if q in ("Milano", "Genova") and len(pins) > 1 else "r"), color=(RED if j == 0 else GOLD)) for j, q in enumerate(pins)],
                        routes=routes, title=MT))
    elif k == "strada":
        sc.add(Strada(SB, t0, t1, mode=arg, title="LA TANGENZIALE · schema semplificato · dinamica esatta non documentata"))
    elif k == "muro":
        sc.add(Muro(WB, t0, t1, upto=float(arg), label="GIORNI DI CARCERE (CIRCA)", total=2700, dur=4.0))
    elif k == "crowd_cars":
        sc.add(CarRow(t0, t1))
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
        sc.add(Pill(a_, (520, 560), t0, t1, size=44))
        sc.add(Arrow((880, 560), (1040, 560), t0 + 0.3, t1, color=RED))
        sc.add(Pill(b_, (1400, 560), t0 + 0.7, t1, size=44, accent=True))
    elif k == "cover":
        sc.add(Img(cover_folder21(620), (960, 560), t0, t1, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 021", (1180, 360), t0 + 0.6, t1, size=70, rot=-12))
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
        num = f"{h:02d}" if h < 13 else None
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
    sc.footer = F[h] + (" · documenti e schemi ricostruiti" if h not in (12, 13) else "")
    return sc

def thumbnail(path="thumbnail.jpg"):
    configure(1920, 1080, 30)
    bg = make_bg(21).convert("RGBA"); lay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    im = rich_img("L'uomo\n*sbagliato*", SERIF, 190, color=WHITE, lh=1.0)
    place(lay, im, (90, 190), "la")
    place(lay, fx.icon("tipo", 380), (1190, 430), "mm")
    place(lay, fx.icon("tipo_b", 380), (1680, 430), "mm")
    d.text((1435, 470), "=", font=font(OSW, 130, 700), fill=GOLD + (255,), anchor="mm")
    place(lay, fx.icon("cell", 240), (1560, 740), "mm")
    st2 = stamp_img("CASO 021", size=60, rot=-8); place(lay, st2, (380, 100), "mm")
    st = stamp_img("ASSOLTO", size=80, rot=-10); place(lay, st, (1690, 930), "mm")
    f = font(OSW, 54, 700); s_ = "7 ANNI E MEZZO IN CARCERE PER UN'AUTO IDENTICA"; tw = tl(d, s_, f)
    d.rectangle([90, 790, 90 + tw + 60, 900], fill=(230, 190, 40, 255))
    d.text((120, 845), s_, font=f, fill=(20, 18, 16, 255), anchor="lm")
    place(lay, wordmark(70), (90, 975), "lm")
    out = Image.alpha_composite(bg, lay).convert("RGB"); out.save(path, quality=92)
