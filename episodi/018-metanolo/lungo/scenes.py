import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from met import *
import fx, pon
from script import SCENES_H, CH

W, H = 1920, 1080
FY = 870
MAPB = (160, 250, 1760, 880)
FB = (160, 300, 1760, 860)          # scenografia ricorrente: la filiera
GB = (260, 330, 1660, 820)          # misuratore del metanolo
MT = "mappa: Natural Earth · percorsi indicativi · schema non in scala"

F = {0: "Fonti: Wikipedia · Linkiesta · GreenMe · La Nazione · Il Sole 24 Ore · Il Giorno",
     1: "Fonti: Il Fatto Alimentare · Dissapore · Wikipedia · Linkiesta · Il Giorno · ACU · ISTAT · TIME (1986)",
     2: "Fonti: Wikipedia · ACU · Dissapore · Linkiesta · GreenMe · La Nazione · TIME (1986)",
     3: "Fonti: Wikipedia · Linkiesta · Dissapore · GreenMe · La Nazione · ACU · LeggePerTutti",
     4: "Fonti: Il Giorno · Linkiesta · ACU · Dissapore · Wikipedia · TIME (1986) · Il Fatto Alimentare",
     5: "Fonti: ACU · La Nazione · Ordinanza Min. Sanità 12/4/1986 (FAOLEX) · TIME (1986) · CS Monitor (1986)",
     6: "Fonti: Wikipedia · ACU · Linkiesta · Dissapore · TIME (1986) · CS Monitor (1986) · LeggePerTutti",
     7: "Fonti: ACU · FAOLEX (L. 462/1986) · Il Sole 24 Ore · Wikipedia · Linkiesta · GreenMe · LeggePerTutti",
     8: "Fonti: Wikipedia · Linkiesta · GreenMe · ACU · CK12 · Dissapore · Il Giorno · ISTAT",
     9: "Fonti: Il Sole 24 Ore · Linkiesta · Dissapore · Il Giorno · Wikipedia · Il Fatto Alimentare · CK12",
     10: "Fonti: Wikipedia · LeggePerTutti · ACU · Dissapore · Linkiesta · GreenMe",
     11: "Contenuto informativo · ricostruzione a scopo divulgativo",
     12: "Fonti: tutte in descrizione · ricostruzione a scopo divulgativo"}

CHT = {1: "Il vino\ndegli *italiani*", 2: "I *protagonisti*", 3: "La *scorciatoia*", 4: "Marzo *1986*", 5: "L'*allarme*",
       6: "L'*indagine*", 7: "La *svolta*", 8: "Il *processo*", 9: "Dopo lo *scandalo*", 10: "Le domande *aperte*",
       11: "La *lezione*", 12: "Il *verdetto*"}
FIRST = {}
for k, (h, _) in enumerate(SCENES_H):
    FIRST.setdefault(h, k)

# ------------------------------------------------------------------ scaletta visiva: (parola, comando)
# comandi "di palco": h, big, i, ii, iii, cal, card, doc, news, map, crowd, tl, court, bars, flow, cover, subscribe,
#   fil (filiera: upto|bad|hl|flow|cut), gauge (v1,v2,..|vmax), board (n), bottles (n), shelf
# comandi "sovrapposti": t (pill in alto), stamp, fig
V = {
 0: [("Marzo", "cal:MARZO|1986"), ("Lombardia", "map:Milano|20|Milano,Torino,Genova"), ("Hanno", "i:wglass|UN BICCHIERE DI VINO"), ("comprato", "shelf")],
 1: [("Nelle", "cal:MARZO-APRILE|1986"), ("pagine", "i:newspaper|UNA PAGINA DURA"), ("ventitré", "big:23|morti"), ("centocinquantatré", "big:153|intossicati"), ("Diverse", "i:eye_x|LA VISTA")],
 2: [("Nei", "i:bottle_bad|I BOTTIGLIONI"), ("Una", "ii:flask|METANOLO|sugar|ZUCCHERO"), ("aggiungeva", "i:bottle_bad|PER ALZARE LA GRADAZIONE"), ("incidente", "h:Non un incidente:\nuna *frode*")],
 3: [("Non", "iii:safe|NIENTE CASSEFORTI|balaclava|NIENTE RAPINE|warn|NIENTE ARMI"), ("C'è", "fil:1|||"), ("cantina", "fil:5||||"), ("tavola", "fil:5|0|4|1|")],
 4: [("In", "cover"), ("vino", "i:bottle|IL VINO DEGLI ANNI OTTANTA"), ("metanolo", "i:flask|PERCHÉ CONVENIVA"), ("procura", "i:magnifier|L'INDAGINE"), ("giudici", "court:I GIUDICI"), ("quarant'anni", "tl:1986|LO SCANDALO;1992|LA SENTENZA;2026|40 ANNI DOPO")],
 5: [("Partiamo", "cal:ITALIA|1985"), ("Il", "i:grapes|UN PRODOTTO DA DEGUSTARE?"), ("È", "ii:wglass|OGNI GIORNO|bottle|SULLA TAVOLA")],
 6: [("Le", "i:globe2|GRANDE PRODUTTORE ED ESPORTATORE"), ("vino", "bottles:6"), ("Poca", "ii:certificate|DENOMINAZIONE: POCA|lire|PREZZO: MOLTA")],
 7: [("Il", "i:bottle|2 LITRI"), ("Si", "shelf"), ("spesso", "i:magnifier|CHI L'HA FATTO?")],
 8: [("Secondo", "i:family|IL RACCONTO DI UNA FAMIGLIA"), ("Barbera", "big:1.890 lire|un bottiglione da 2 litri · secondo Il Giorno"), ("Con", "big:< 3 €|di oggi · coefficienti ISTAT")],
 9: [("Nel", "i:bottle|VINO DA TAVOLA"), ("prezzo", "flow:PIÙ GRADI>PIÙ VALORE"), ("Più", "ii:wglass|MENO GRADI = MENO VALORE|money|PIÙ GRADI = PIÙ VALORE"), ("Un", "i:box_empty|UN VINO DEBOLE SI VENDE PEGGIO")],
 10: [("Il", "ii:grapes|UVA MATURA|sun|SOLE"), ("Ma", "iii:sun|ANNO CALDO|moon|ANNO FREDDO|grapes|MENO ZUCCHERI"), ("non", "i:warn|GRADAZIONE BASSA")],
 11: [("Una", "i:sugar|ZUCCHERO NEL MOSTO?"), ("Ma", "cal:VIETATO DAL|1965"), ("E", "ii:sugar|ZUCCHERO|tax|IMPOSTA")],
 12: [("Poi", "i:ship|IL MERCATO ESTERO"), ("Nel", "bars:QUANTITÀ 1985|17|VALORE 1985|20"), ("le", "t:EXPORT 1985: +17% QUANTITÀ · +20% VALORE"), ("È", "h:Un momento\n*d'oro*")],
 13: [("Il", "map:Milano|5|Milano,Sète,Karlsruhe|Milano>Sète"), ("Germania", "worldroute:Milano>Washington"), ("Ed", "stamp:ATTENZIONE")],
 14: [("Per", "i:tubes|UN PASSO NELLA CHIMICA"), ("Perché", "fig:man|NON UNA PERSONA"), ("molecola", "h:Una *molecola*")],
 15: [("Si", "i:flask|METANOLO · ALCOL METILICO"), ("un", "iii:flask|1 CARBONIO|flask|4 IDROGENO|flask|1 OSSIGENO"), ("È", "ii:flask|METANOLO|wglass|ETANOLO (IL VINO)")],
 16: [("I", "ii:flask|METANOLO|wglass|ETANOLO"), ("secondo", "iii:eye|ASPETTO|warn|ODORE|wglass|SAPORE"), ("Chi", "i:question|NON SE NE ACCORGE"), ("Ma", "i:warn|OLTRE CERTE QUANTITÀ: TOSSICO")],
 17: [("Una", "i:grapes|LA FERMENTAZIONE"), ("Per", "i:scales|LA LEGGE"), ("fissa", "gauge:0|1")],
 18: [("Il", "doc:DECRETO · 1965|frodi nei mosti e nei vini|limite del metanolo|vini rossi: 0,30 ml / 100 ml"), ("per", "gauge:0|1"), ("Teniamo", "big:0,3|il numero da ricordare")],
 19: [("Il", "i:factory|L'INDUSTRIA"), ("come", "iii:flask|SOLVENTE|tanker|COMBUSTIBILE|tubes|CHIMICA"), ("Non", "i:warn|NON È DA BERE"), ("E", "i:bottle_bad|NEL VINO")],
 20: [("Apriamo", "board:0"), ("Al", "map:Narzole|60|Narzole,Cuneo,Torino"), ("Narzole", "t:NARZOLE · PROVINCIA DI CUNEO")],
 21: [("La", "board:1"), ("È", "ii:barrel|VINO DA TAVOLA|tanker|ANCHE SFUSO"), ("aziende", "fil:2|||")],
 22: [("Diciamolo", "i:scales|SOLO I FATTI"), ("di", "ii:magnifier|INDAGINI|court|SENTENZE"), ("Nel", "cal:PRIMO GRADO|1992"), ("Ci", "t:CI ARRIVEREMO")],
 23: [("Poi", "map:Incisa Scapaccino|70|Incisa Scapaccino,Narzole,Asti"), ("Compra", "board:2"), ("supermercati", "shelf")],
 24: [("Le", "ii:bottle|ROSSO DA TAVOLA|bottle|BIANCO DA TAVOLA"), ("dalla", "fil:3|||"), ("È", "t:IL PRIMO ANELLO DELLA CATENA")],
 25: [("Dall'altra", "i:ministry|LE ISTITUZIONI"), ("A", "board:3"), ("Nobili", "t:SOSTITUTO PROCURATORE · MILANO")],
 26: [("A", "map:Roma|12|Roma"), ("ministro", "board:4"), ("Sarà", "i:certificate|CERTIFICATI PER L'EXPORT")],
 27: [("E", "crowd"), ("Pensionati", "shelf"), ("Non", "i:nophoto|NESSUN NOME"), ("vittime", "board:5")],
 28: [("Tra", "board:6"), ("Sua", "i:eye_x|PERDE LA VISTA"), ("Negli", "i:megaphone|IL COMITATO DELLE VITTIME")],
 29: [("Infine", "board:7"), ("il", "map:Treviso|40|Treviso,Narzole"), ("Nel", "cal:CONTROLLO|1984"), ("Anche", "t:LO VEDREMO")],
 30: [("Ecco", "t:RIEPILOGO · 1"), ("luogo", "map:Narzole|30|Narzole,Asti,Milano"), ("sostanza", "i:flask|IL METANOLO"), ("limite", "big:0,3|il limite (ml ogni 100 ml)"), ("filiera", "fil:5|||1|")],
 31: [("Ora", "h:La domanda\n*chiave*"), ("perché", "ii:flask|METANOLO|bottle|NEL VINO?"), ("La", "i:lire|ECONOMICA")],
 32: [("Il", "i:flask|ALZA LA GRADAZIONE"), ("Un", "ii:bottle|VINO DEBOLE|bottle_bad|«PIÙ FORTE»"), ("forte", "flow:PIÙ GRADI>PIÙ VENDIBILE")],
 33: [("E", "i:scales|UNA LEGGE"), ("Nell'estate", "cal:LUGLIO|1984"), ("una", "doc:LEGGE · LUGLIO 1984|tassazione degli alcolici|distillati italiani e comunitari|metanolo: esente dall'imposta"), ("Tra", "ii:tax|PRIMA: IMPOSTA|notax|DOPO: ESENTE")],
 34: [("Lo", "ii:ministry|IL FISCO|ship|IL COMMERCIO"), ("Ma", "i:notax|EFFETTO COLLATERALE"), ("Più", "ii:flask|METANOLO: ESENTE|sugar|ZUCCHERO: TASSATO")],
 35: [("Secondo", "i:magnifier|MENO CONTROLLI SULLA VENDITA"), ("uffici", "i:ministry|UFFICI TECNICI DELLA FINANZA"), ("finanza", "t:SECONDO ALCUNE RICOSTRUZIONI")],
 36: [("Il", "h:Una *scorciatoia*"), ("un", "ii:flask|INDUSTRIALE|wglass|QUASI INDISTINGUIBILE"), ("Una", "i:lire|SOLO IL PREZZO")],
 37: [("Quanto", "i:tanker|QUANTO METANOLO?"), ("Le", "tl:DIC. 1985|INIZIO;MAR. 1986|FINE"), ("in", "big:2,5 t|di metanolo venduto · dic. 1985 - mar. 1986")],
 38: [("Facciamo", "i:calc|UN CONTO"), ("Da", "cal:GIORNI|105"), ("Due", "big:2.500 kg ÷ 105|"), ("ventiquattro", "big:≈ 24 kg|di metanolo al giorno")],
 39: [("C'è", "h:Un *precedente*"), ("Nel", "map:Treviso|30|Treviso,Narzole|Treviso>Narzole"), ("trova", "i:tubes|VALORI FUORI NORMA")],
 40: [("Scattano", "ii:lock|SEQUESTRO|doc_icon|DENUNCIA"), ("Ma", "i:drawer|LA PRATICA SI PERDE"), ("La", "fil:2|||")],
 41: [("È", "i:question|UN PUNTO DISCUSSO"), ("un", "cal:ALLARME|1984"), ("E", "stamp:NON BASTÒ")],
 42: [("Come", "fil:5|||"), ("Il", "i:handshake|PASSA DI MANO"), ("Si", "iii:barrel|SFUSO|tubes|TAGLIO|truck|RIVENDITA")],
 43: [("Chi", "ii:bottle|IMBOTTIGLIA|grapes|NON COLTIVA"), ("Compra", "iii:barrel|FORNITORE A|barrel|FORNITORE B|barrel|FORNITORE C"), ("Se", "fil:5|1|||")],
 44: [("Ed", "fil:5|0||1|"), ("scaffali", "map:Milano|20|Milano,Torino,Genova"), ("tre", "t:LOMBARDIA · PIEMONTE · LIGURIA")],
 45: [("Milano", "map:Milano|90|Milano"), ("Nei", "cal:MARZO|1986"), ("Casi", "i:question|NESSUNO COLLEGA I CASI")],
 46: [("Nello", "i:hospital2|RICOVERO D'URGENZA"), ("Ha", "ii:wglass|UN BICCHIERE|bottle|UN BOTTIGLIONE"), ("Si", "i:eye_x|PERDE LA VISTA")],
 47: [("Le", "ii:hospital2|SACCO?|hospital2|NIGUARDA?"), ("per", "t:FONTI NON CONCORDI"), ("Ma", "i:magnifier|AVVELENAMENTO?")],
 48: [("Secondo", "i:bottle|IL BOTTIGLIONE"), ("Viene", "i:tubes|ANALISI"), ("Dentro", "i:tubes|MOLTO OLTRE IL LIMITE")],
 49: [("Quanto", "h:Quanto *superiori*?"), ("Qui", "i:tubes|CAMPIONI DIVERSI"), ("Il", "gauge:0.3,5.7|6"), ("cinque", "t:TIME, APRILE 1986: FINO AL 5,7%")],
 50: [("Altre", "i:warn|MOLTE VOLTE LA SOGLIA"), ("Ricordate", "big:0,3|il limite"), ("Anche", "i:warn|LONTANISSIMI DAL LIMITE")],
 51: [("Il", "cal:MARZO 1986|17"), ("Arrivano", "map:Milano|20|Milano,Torino,Genova"), ("È", "t:17 MARZO 1986: L'INIZIO")],
 52: [("I", "i:hospital2|I SINTOMI"), ("malessere", "ii:eye_x|LA VISTA|bed|RICOVERO"), ("Non", "h:Niente dettagli:\n*bastano i numeri*")],
 53: [("Il", "cal:MARZO 1986|18"), ("ANSA", "news:CRONACA|19 marzo 1986|*Vino al metanolo*\nmorti a Milano|la procura apre un'inchiesta"), ("La", "board:3"), ("Nobili", "t:ALBERTO NOBILI · PROCURA DI MILANO")],
 54: [("Le", "i:tubes|LE PRIME ANALISI"), ("un", "ii:bottle_bad|BARBERA DA TAVOLA|bottle_bad|BIANCO DA TAVOLA"), ("imbottigliati", "fil:4|1|2||")],
 55: [("Il", "fig:man|IL FIGLIO"), ("aver", "i:phone|LA TELEFONATA"), ("È", "t:UNA TESTIMONIANZA")],
 56: [("Intanto", "i:newspaper|IL BILANCIO SALE"), ("Le", "crowd")],
 57: [("Nei", "shelf"), ("vino", "stamp:RITIRATO"), ("Molte", "ii:bottle|BOTTIGLIONE|bottle_ok|BOTTIGLIA DI QUALITÀ"), ("La", "h:La paura\n*non distingue*")],
 58: [("Fermiamoci", "t:RIEPILOGO · 2"), ("Marzo", "cal:MARZO|1986"), ("metanolo", "fil:5|0|||"), ("Ora", "h:L'allarme\n*si allarga*")],
 59: [("Gli", "ii:clock|IN FRETTA|bottle_bad|OGNI BOTTIGLIONE"), ("Le", "map:Milano|20|Milano,Genova,Bologna"), ("Emilia-Romagna", "stamp:SEQUESTRI")],
 60: [("I", "fig:police|I NAS"), ("Le", "i:tubes|ANALISI"), ("ogni", "i:magnifier|OGNI PARTITA SOSPETTA")],
 61: [("In", "i:parliament_it|IN SENATO"), ("Pandolfi", "board:4"), ("seicentomila", "big:600.000 litri|in circolazione · secondo il ministro")],
 62: [("Seicentomila", "bottles:10"), ("Facciamo", "i:calc|UN CONTO"), ("divisi", "big:600.000 ÷ 2 = 300.000|bottiglioni"), ("Messi", "h:In fila:\n*decine di chilometri*")],
 63: [("Il", "cal:APRILE 1986|12"), ("Vieta", "doc:ORDINANZA · 12 APRILE 1986|Ministero della Sanità|vietata la vendita dei vini|delle ditte in elenco"), ("vini", "stamp:VIETATO")],
 64: [("Nella", "doc:TABELLA A|ditte inquisite: 7|Piemonte · Puglia|Emilia-Romagna"), ("Piemonte", "map:Puglia|5|Narzole,Puglia,Emilia-Romagna"), ("Nella", "doc:TABELLA B|decine di aziende|campioni sopra i limiti|o sospetti")],
 65: [("L'ordinanza", "cal:GAZZETTA UFFICIALE|14 APR."), ("Chi", "ii:truck|RITIRARE LE PARTITE|ministry|DENUNCIA AL SINDACO"), ("sindaco", "ii:lock|SEQUESTRO|tubes|ANALISI")],
 66: [("Intanto", "h:Oltre i *confini*"), ("In", "map:Sète|10|Puglia,Sète|Puglia>Sète"), ("nave", "i:ship|NAVE CISTERNA BLOCCATA")],
 67: [("In", "map:Karlsruhe|20|Karlsruhe,Narzole"), ("Sul", "bottles:8"), ("si", "t:NUMERI NON CONCORDI")],
 68: [("Negli", "worldroute:Milano>Washington"), ("impone", "stamp:RESTRIZIONI"), ("toglie", "ii:handshake|ACCORDO|certificate|")],
 69: [("La", "i:certificate|IL CERTIFICATO"), ("Il", "board:4"), ("tutto", "doc:CERTIFICATO D'ANALISI|vino destinato all'estero|metanolo entro i limiti|ricostruzione")],
 70: [("Per", "i:ship|EXPORT FERMO"), ("Anche", "ii:barrel|CANTINE ONESTE|calendar_x|ORDINI ANNULLATI")],
 71: [("Torniamo", "map:Milano|90|Milano"), ("Il", "i:magnifier|COME UN'INCHIESTA SU UN FURTO"), ("seguire", "fil:5|0||1|")],
 72: [("Si", "fil:5|0|4||"), ("Dall'etichetta", "fil:5|0|2||"), ("Da", "fil:5|0|1||")],
 73: [("Ogni", "iii:doc_icon|BOLLA|doc_icon|FATTURA|register|REGISTRO"), ("E", "map:Narzole|25|Milano,Asti,Narzole|Milano>Asti>Narzole")],
 74: [("La", "map:Narzole|90|Narzole"), ("Ciravegna", "board:1"), ("Secondo", "ii:shield_ok|I CARABINIERI|newspaper|I DOCUMENTI")],
 75: [("Dopo", "doc:COMUNICAZIONE GIUDIZIARIA|ipotesi di reato:|omicidio colposo plurimo|lesioni colpose · frodi nei vini"), ("omicidio", "t:IPOTESI DI REATO, NON CONDANNE")],
 76: [("Una", "h:*Colposo*"), ("colposo", "i:scales|SENZA INTENZIONE"), ("L'accusa", "flow:UNA FRODE>LE CONSEGUENZE")],
 77: [("Pochi", "i:handcuffs|DUE ARRESTI"), ("Giovanni", "board:1"), ("Secondo", "i:mic|NON RISPONDE")],
 78: [("Ma", "h:Non *una sola* cantina"), ("Il", "fil:5|1|1||"), ("tagliare", "iii:barrel|ALTRE CANTINE|barrel|ALTRE CANTINE|barrel|ALTRE CANTINE")],
 79: [("Secondo", "big:≈ 60|aziende coinvolte secondo la procura"), ("Gli", "ii:tanker|IL TRASPORTO|flask|IL METANOLO"), ("chi", "fil:3|0|0||")],
 80: [("In", "cal:SETTIMANE|5"), ("Per", "bottles:12"), ("tempo", "t:UN TEMPO MOLTO BREVE")],
 81: [("Con", "i:drawer|IL PRECEDENTE"), ("il", "tl:1984|CONTROLLO;1984|DENUNCIA;1986|LO SCANDALO")],
 82: [("È", "h:Non solo\nuna *truffa*"), ("Diventa", "iii:magnifier|QUANTI CONTROLLI?|ministry|CHI LI FA?|question|PERCHÉ NO?")],
 83: [("C'è", "i:magnifier|UN EPISODIO"), ("nei", "map:Narzole|50|Narzole,Asti"), ("Tanaro", "i:river_red|IL TANARO")],
 84: [("È", "i:newspaper|DISSAPORE"), ("Lo", "t:UN RACCONTO, NON UN DATO VERIFICATO"), ("come", "i:question|DA PRENDERE CON CAUTELA")],
 85: [("Terza", "t:RIEPILOGO · 3"), ("Ventitré", "big:23 · 153|morti · intossicati"), ("Narzole", "map:Narzole|40|Narzole"), ("sessantina", "fil:5|0|||"), ("frontiere", "i:ship|FERMO ALLE FRONTIERE")],
 86: [("Se", "subscribe")],
 87: [("Ora", "h:La *svolta*"), ("Lo", "i:scales|NUOVE REGOLE"), ("Non", "tl:MARZO|SCANDALO;GIUGNO|DECRETO;AGOSTO|LEGGE")],
 88: [("Il", "cal:GIUGNO 1986|18"), ("Il", "doc:LEGGE 7 AGOSTO 1986 N. 462|prevenzione e repressione|delle sofisticazioni alimentari|(ricostruzione)"), ("[462", "stamp:LEGGE")],
 89: [("Che", "h:Che cosa *cambia*?"), ("Prima", "i:ministry|ISPETTORATO REPRESSIONE FRODI"), ("Oggi", "t:OGGI: ICQRF")],
 90: [("Vengono", "ii:police_icon|NAS|ship|DOGANE"), ("E", "i:register|ANAGRAFE VITIVINICOLA"), ("un", "fil:5|||")],
 91: [("L'idea", "fil:5||||"), ("se", "iii:register|OGNI PASSAGGIO|doc_icon|REGISTRATO|lock|TRACCIATO"), ("È", "h:La *tracciabilità*")],
 92: [("Anche", "i:grapes|I PRODUTTORI"), ("Ad", "map:Asti|60|Asti"), ("denominazioni", "iii:map_icon|ZONA|grapes|UVA|barrel|LAVORAZIONE")],
 93: [("Il", "i:lire|ANCHE COMMERCIALE"), ("dopo", "ii:bottle|ORIGINE INCERTA|bottle_ok|ORIGINE CERTA"), ("garanzia", "i:certificate|UNA GARANZIA IN PIÙ")],
 94: [("I", "i:ship|L'EXPORT"), ("Nel", "bars:1985|100|1986|63"), ("trentasette", "t:1986: -37% QUANTITÀ · -1/4 VALORE")],
 95: [("Altre", "bars:STIMA A|37|STIMA B|40|STIMA C|45"), ("cifre", "t:CALO % · STIME NON CONCORDI"), ("record", "h:Da anno record\na *anno nero*")],
 96: [("Facciamo", "i:calc|UN ULTIMO CONTO"), ("Un", "bottles:10"), ("sessantatré", "big:da 100 a 63|bottiglie esportate")],
 97: [("Secondo", "tl:1986|CROLLO;ANNI '90|RIPRESA"), ("E", "ii:bottle|BOTTIGLIONE|bottle_ok|QUALITÀ")],
 98: [("Andiamo", "h:In *aula*"), ("Il", "court:CORTE D'ASSISE DI MILANO"), ("Le", "tl:1986|I FATTI;1991|IN AULA;1992|SENTENZA")],
 99: [("Gli", "board:1"), ("chi", "iii:tanker|TRASPORTO|barrel|CANTINE|truck|RIVENDITA")],
 100: [("In", "fil:5|0|||"), ("dalle", "iii:flask|METANOLO|barrel|VINI TAGLIATI|lorry_wine|SUPERMERCATI")],
 101: [("Nel", "cal:PRIMO GRADO|1992"), ("Le", "big:fino a 16 anni|le condanne più alte"), ("sedici", "i:gavel|")],
 102: [("Giovanni", "card:SENTENZA DI PRIMO GRADO · 1992|Giovanni Ciravegna: 14 anni|Daniele Ciravegna: 4 anni|Corte d'assise di Milano"), ("principale", "t:PRIMO GRADO"), ("Il", "stamp:CONDANNATI")],
 103: [("Le", "tl3"), ("Per", "i:nophoto|NESSUN ALTRO NOME")],
 104: [("C'è", "i:lire|LA PARTE ECONOMICA"), ("I", "big:1 miliardo|di lire di risarcimento")],
 105: [("Quanto", "i:calc|QUANTO VALE OGGI?"), ("Con", "big:≈ 1.036.000 €|1 mld di lire 1992 · coefficienti ISTAT"), ("Se", "big:< 6.000 €|a testa, se diviso tra 176 persone")],
 106: [("Ma", "i:box_empty|I SOLDI NON ARRIVANO"), ("Secondo", "stamp:NULLATENENTI"), ("beni", "flow:BENI E DENARO>AD ALTRI")],
 107: [("Il", "fig:man|IL FIGLIO DI UNA VITTIMA"), ("i", "i:tv|INTERVISTE E TRASMISSIONI"), ("Nessuna", "stamp:MAI PAGATO")],
 108: [("E", "board:1"), ("Secondo", "cal:FUORI DAL CARCERE|2001"), ("Torna", "map:Langhe|60|Langhe"), ("riprende", "i:barrel|TORNA A FARE VINO")],
 109: [("In", "i:tv|UN'INTERVISTA"), ("Muore", "cal:MORTE|2013"), ("Non", "stamp:NESSUN RISARCIMENTO")],
 110: [("Quarta", "t:RIEPILOGO · 4"), ("Primo", "card:PRIMO GRADO · 1992|padre: 14 anni|figlio: 4 anni|condanne fino a 16 anni"), ("Un", "big:1 mld di lire|risarcimento mai pagato")],
 111: [("Che", "cal:DOPO|40 ANNI"), ("Prima", "crowd"), ("Le", "board:6")],
 112: [("Negli", "i:parliament_it|INTERROGAZIONI PARLAMENTARI"), ("Ferlicca", "iii:envelope|LETTERE|envelope|LETTERE|envelope|LETTERE"), ("Le", "i:box_empty|NESSUN INDENNIZZO")],
 113: [("Molti", "crowd"), ("Chi", "ii:eye_x|LA VISTA PERSA|lire|PENSIONE DI INVALIDITÀ"), ("È", "h:Una storia che\n*non finisce*")],
 114: [("Poi", "i:grapes|IL VINO"), ("Lo", "ii:bottle|PRIMA|bottle_ok|DOPO"), ("Secondo", "bars:1986|10|OGGI|60"), ("Oggi", "t:VINI DOC/IGT · % DELLA PRODUZIONE · IL SOLE 24 ORE")],
 115: [("Sempre", "bars:EXPORT 1986 (MLN €)|800|OGGI (MLN €)|8000"), ("L'associazione", "h:La rivoluzione\ndella *qualità*")],
 116: [("Lo", "i:question|NON L'UNICA CAUSA"), ("Il", "ii:bottle|BOTTIGLIONE ANONIMO|certificate|ORIGINE IN ETICHETTA")],
 117: [("Cambiano", "i:magnifier|I CONTROLLI"), ("Oggi", "big:> 100.000|controlli l'anno · secondo Il Sole 24 Ore"), ("ispettorato", "iii:ministry|ISPETTORATO|police_icon|NAS|tubes|LABORATORI")],
 118: [("Lo", "h:La *memoria*"), ("Nel", "ii:tv|2021 · RAI|mic|2023 · PODCAST")],
 119: [("Nel", "cal:40 ANNI|2026"), ("E", "i:envelope|LE RICHIESTE DELLE FAMIGLIE")],
 120: [("Arriviamo", "h:Le domande\n*aperte*"), ("La", "i:calc|I NUMERI"), ("Ventitré", "big:23 · 153|le cifre più citate")],
 121: [("Quante", "i:eye_x|QUANTI CIECHI?"), ("Alcune", "bars:FONTE A|15|FONTE B|19|FONTE C|23"), ("E", "t:ALCUNI CASI POTREBBERO ESSERE SFUGGITI")],
 122: [("La", "cal:MARZO 1986|17 O 18?"), ("L'inizio", "t:17 O 18 MARZO: FONTI NON CONCORDI"), ("In", "tl:INIZIO MARZO|PRIME MORTI;17-18 MARZO|L'ALLARME")],
 123: [("La", "i:factory|LE AZIENDE"), ("La", "big:≈ 60|secondo la procura"), ("Altre", "big:≈ 30|secondo altre ricostruzioni"), ("Dipende", "t:DIPENDE DA COSA SI CONTA")],
 124: [("La", "i:drawer|LA PRATICA DEL 1984"), ("Perché", "i:question|DOVE SI È FERMATA?")],
 125: [("La", "doc:LEGGE · LUGLIO 1984|tassazione degli alcolici|metanolo esente|(ricostruzione)"), ("Chi", "i:notax|UN INCENTIVO NON PREVISTO")],
 126: [("infine", "i:question|L'ULTIMA DOMANDA"), ("difficile", "h:La domanda\n*più difficile*"), ("risarcita", "i:box_empty|NESSUN RISARCIMENTO"), ("sentenza", "ii:court|LA SENTENZA C'È|box_empty|I SOLDI NO"), ("Stato", "i:ministry|E LO STATO?")],
 127: [("Che", "h:La *lezione*"), ("Non", "i:tubes|NON SERVE LA CHIMICA"), ("Bastano", "t:CINQUE ABITUDINI")],
 128: [("Primo", "t:1 · L'ETICHETTA"), ("Su", "card:ETICHETTA · ESEMPIO GENERICO|imbottigliato da: ...|sede: ...|lotto: L.000|vol: 12%"), ("Un", "i:question|SENZA RESPONSABILE")],
 129: [("Secondo", "t:2 · L'ORIGINE"), ("Le", "iii:certificate|DOC|certificate|DOCG|certificate|IGT"), ("Non", "i:magnifier|UNA TRACCIA, NON UNA GARANZIA")],
 130: [("Terzo", "t:3 · IL PREZZO"), ("Un", "i:lire|PREZZO MOLTO BASSO?"), ("Ma", "i:question|UNA DOMANDA DA FARSI"), ("Nel", "ii:flask|IL METANOLO|lire|UN COSTO TAGLIATO")],
 131: [("Quarto", "t:4 · L'ORIGINE INCERTA"), ("Alcolici", "iii:bottle|SENZA ETICHETTA|barrel|SFUSO IGNOTO|suitcase|IN VIAGGIO"), ("è", "i:warn|I CONTROLLI NON ARRIVANO")],
 132: [("Quinto", "t:5 · LE SEGNALAZIONI"), ("Se", "ii:police_icon|NAS|ministry|ICQRF"), ("Nel", "i:hospital2|1986: L'ALLARME DA UN OSPEDALE"), ("Oggi", "i:magnifier|PIÙ CONTROLLI")],
 133: [("E", "i:scales|CHI SCRIVE LE LEGGI"), ("Una", "flow:UNA NORMA FISCALE>UN INCENTIVO PERICOLOSO")],
 134: [("Ricapitoliamo", "cover"), ("Uno", "ii:notax|METANOLO DETASSATO|sugar|ZUCCHERO TASSATO")],
 135: [("Due", "big:23 · 153|morti · intossicati · marzo 1986"), ("Diverse", "i:eye_x|LA VISTA")],
 136: [("Tre", "fil:5|0|0|1|"), ("Quattro", "ii:ship|EXPORT IN CROLLO|register|NUOVI CONTROLLI")],
 137: [("Cinque", "card:PRIMO GRADO · 1992|Giovanni Ciravegna: 14 anni|Daniele Ciravegna: 4 anni"), ("Sei", "stamp:MAI PAGATO")],
 138: [("E", "ii:certificate|L'ETICHETTA|lire|IL PREZZO"), ("Scrivilo", "i:envelope|SCRIVILO NEI COMMENTI")],
 139: [("Iscriviti", "subscribe")],
}

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

# icone alternative quando un nome non esiste nella libreria
ALIAS = {"handshake": "meeting", "clock": "hourglass", "lab": "tubes", "hospital": "hospital2", "doc_icon": "newspaper",
         "police_icon": "shield_ok", "parliament_it": "ministry", "map_icon": "globe2", "eye": "magnifier", "lire": "money"}
def IC(n): return ALIAS.get(n, n)

BOARD = [("NARZOLE (CN)", "cantina Ciravegna", "card"), ("G. e D. CIRAVEGNA", "padre e figlio · titolari", "person"),
         ("IMBOTTIGLIATORE", "ditta dell'Astigiano", "card"), ("ALBERTO NOBILI", "pm · procura di Milano", "person"),
         ("F. M. PANDOLFI", "ministro dell'Agricoltura", "person"), ("LE VITTIME", "nessun nome", "card"),
         ("ROBERTO FERLICCA", "comitato vittime", "person"), ("REPRESSIONE FRODI", "ufficio di Treviso", "card")]
BXY = [(330, 440), (330, 730), (720, 440), (1110, 440), (1500, 440), (720, 730), (1110, 730), (1500, 730)]

def board_el(n, t0, t1):
    nodes = {}
    for j in range(n + 1):
        nm, role, kind = BOARD[j]
        nodes[f"n{j}"] = dict(xy=BXY[j], name=nm, role=role, t=t0 + (0.2 if j == n else -5), rot=(-3 + 2 * (j % 3)))
    links = [("n0", "n1", t0 - 5)] if n >= 1 else []
    if n >= 2: links.append(("n0", "n2", t0 - 5 if n > 2 else t0 + 0.6))
    if n >= 3: links.append(("n2", "n3", t0 - 5 if n > 3 else t0 + 0.6))
    if n >= 5: links.append(("n2", "n5", t0 - 5 if n > 5 else t0 + 0.6))
    if n >= 6: links.append(("n5", "n6", t0 - 5 if n > 6 else t0 + 0.6))
    if n >= 7: links.append(("n7", "n0", t0 + 0.6))
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
            routes = [dict(pts=[pts[j], pts[j + 1]], t=t0 + 0.6 + 0.8 * j, d=1.0, icon="truck" if i > 60 else "ship", color=RED) for j in range(len(pts) - 1)]
        sc.add(WorldMap(MAPB, [(t0, cen, ppd * 0.8), (t1 or a + dur, cen, ppd)], t0, t1,
                        pins=[dict(at=q, label=q.upper(), t=t0 + 0.3 + 0.2 * j, side="r", color=(RED if j == 0 else GOLD)) for j, q in enumerate(pins)],
                        routes=routes, title=MT))
    elif k == "worldroute":
        pts = arg.split(">"); ll = [WPL[q] for q in pts]
        lo0, lo1 = min(x for x, y in ll), max(x for x, y in ll); la0, la1 = min(y for x, y in ll), max(y for x, y in ll)
        cen = ((lo0 + lo1) / 2, (la0 + la1) / 2); ppd = min(1300 / max(1, lo1 - lo0), 480 / max(1, la1 - la0), 40)
        sc.add(WorldMap(MAPB, [(t0, cen, ppd * 0.85), (t1 or a + dur, cen, ppd)], t0, t1,
                        pins=[dict(at=q, label=q.upper(), t=t0 + 0.3 + 0.5 * j, side="r", color=(RED if j == 0 else GOLD)) for j, q in enumerate(pts)],
                        routes=[dict(pts=[pts[j], pts[j + 1]], t=t0 + 0.6 + 0.9 * j, d=1.0, icon="ship", color=GOLD) for j in range(len(pts) - 1)], title=MT))
    elif k == "fil":
        upto = int(p[0]); bad = int(p[1]) if len(p) > 1 and p[1] != "" else None
        hl = int(p[2]) if len(p) > 2 and p[2] != "" else None; fl = len(p) > 3 and p[3] == "1"
        sc.add(Filiera(FB, t0, t1, upto=upto, bad=bad, hl=hl, flow_t=(t0 + 0.8 if fl else None)))
    elif k == "gauge":
        vs = [float(x) for x in p[0].split(",")]; vmax = float(p[1]) if len(p) > 1 else 6.0
        keys = [(t0 + 0.3 + 1.3 * j, v) for j, v in enumerate(vs)]
        sc.add(Gauge(GB, keys, t0, t1, vmax=vmax, unit=" ml/100 ml" if vmax <= 1 else "%",
                     title="METANOLO NEL VINO · schema semplificato · valori come detti nel video"))
    elif k == "board":
        sc.add(board_el(int(p[0]), t0, t1))
    elif k == "bottles":
        n = int(p[0]); cols = min(n, 6); rows = (n + cols - 1) // cols
        for j in range(n):
            x = 960 + (j % cols - (cols - 1) / 2) * 230; y = 560 + (j // cols - (rows - 1) / 2) * 260
            sc.add(Icon("bottle", (x, y), t0 + j * 0.12, t1, size=220), "pop")
    elif k == "shelf":
        sc.add(Icon("lorry_wine", (960, 540), t0, t1, size=520, label="SUPERMERCATO · VINO DA TAVOLA"), "pop")
        sc.add(Figure(walk([(-120, FY), (420, FY)], t0, 380), t0, t1, kind="man", s=0.9), "pop")
    elif k == "crowd":
        sc.add(Crowd((200, 420, 1720, 860), 26, t0, t1, s=0.42, seed=i))
    elif k == "tl":
        evs = [e.split("|") for e in arg.split(";")]
        sc.add(Timeline(300, 1620, 600, [dict(top=e[0], bottom=e[1], t=t0 + 0.3 + 0.6 * j, hl=(j == len(evs) - 1)) for j, e in enumerate(evs)], t0, t1, size=46))
    elif k == "tl3":
        sc.add(Timeline(360, 1560, 600, [dict(top="1° GRADO", bottom="1992 · Milano", t=t0 + 0.3, hl=True), dict(top="APPELLO", bottom="esiti non concordi", t=t0 + 1.2),
                                         dict(top="CASSAZIONE", bottom="esiti non concordi", t=t0 + 2.1)], t0, t1, size=46))
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
        sc.add(Text("schema semplificato · valori come detti nel video", (960, 860), t0, t1, size=24, fnt=COURR, color=GREY, anchor="mm"))
    elif k == "flow":
        a_, b_ = arg.split(">")
        sc.add(Pill(a_, (560, 560), t0, t1, size=52))
        sc.add(Arrow((800, 560), (1120, 560), t0 + 0.3, t1, color=RED))
        sc.add(Pill(b_, (1380, 560), t0 + 0.7, t1, size=52, accent=True))
    elif k == "cover":
        sc.add(Img(cover_folder18(620), (960, 560), t0, t1, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 018", (1180, 360), t0 + 0.6, t1, size=70, rot=-12))
    elif k == "subscribe":
        sc.add(Img(wordmark(120), (960, 470), t0, t1, anim="pop", shadow=False), "hit")
        sc.add(Pill("ISCRIVITI · OGNI GIORNO UN NUOVO CASO", (960, 700), t0 + 0.4, t1, size=50, accent=True))
    elif k == "fig":
        sc.add(Figure(walk([(-120, FY), (300, FY)], t0, 420), t0, t1, kind=p[0], s=1.0, label=(p[1] if len(p) > 1 and p[1] else None)), "pop")
    else:
        raise ValueError(cmd)

def build(i, dur, a, words):
    T0 = Clock(words, a)
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
    bg = make_bg(18).convert("RGBA"); lay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    im = rich_img("Il vino al\n*metanolo*", SERIF, 190, color=WHITE, lh=1.0)
    place(lay, im, (90, 170), "la")
    b = fx.icon("bottle_bad", 620); place(lay, b, (1480, 470), "mm")
    fl = fx.icon("flask", 280); place(lay, fl, (1130, 560), "mm")
    st = stamp_img("1986", size=110, rot=-10); place(lay, st, (1640, 860), "mm")
    st2 = stamp_img("CASO 018", size=60, rot=-8); place(lay, st2, (380, 90), "mm")
    f = font(OSW, 54, 700); s_ = "COSTAVA MENO DELLO ZUCCHERO · 23 VITTIME"; tw = tl(d, s_, f)
    d.rectangle([90, 760, 90 + tw + 60, 880], fill=(230, 190, 40, 255))
    d.text((120, 820), s_, font=f, fill=(20, 18, 16, 255), anchor="lm")
    place(lay, wordmark(70), (90, 960), "lm")
    out = Image.alpha_composite(bg, lay).convert("RGB"); out.save(path, quality=92)
