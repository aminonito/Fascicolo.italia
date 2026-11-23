import sys, os, re, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
from gir import *
import fx, met
from script import SCENES_H, CH

W, H = 1920, 1080
FY = 870
MAPB = (160, 250, 1760, 880)
SALA = (160, 250, 1760, 860)         # scenografia principale: la sala della biblioteca (schema)
MT = "mappa: Natural Earth · schema non in scala"

FB = "Il Post (2014) · AGI (2023) · Finestre sull'Arte (2026) · L'Espresso (2013, 2015) · ILAB · Wikipedia · Doppiozero (2014)"
F = {0: "Fonti: " + FB,
     1: "Fonti: FAI (biblioteca e complesso dei Girolamini) · MuseiOnline · Finestre sull'Arte (2026) · AGI (2023) · SiViaggia (2026) · Wikipedia",
     2: "Fonti: Il Post (2014) · Doppiozero (2014) · historyofinformation.com · Wikipedia · ILAB · Live Science (2019) · JSTOR Daily",
     3: "Fonti: Il Post (2014) · Doppiozero (2014) · L'Espresso (2013) · AGI (2023) · Il Fatto Quotidiano (2012, ordinanza del gip) · ILAB",
     4: "Fonti: Il Post (2014) · Doppiozero · historyofinformation.com · Artribune (2020) · ILAB (2012-2013) · Finestre sull'Arte · The Local (2015)",
     5: "Fonti: historyofinformation.com · ILAB (2012-2013) · Il Post (2014) · Wikipedia · AGI (2023) · L'Espresso (2015) · The Local (2015)",
     6: "Fonti: ILAB (2012-2015) · L'Espresso (2013) · historyofinformation.com · UNODC SHERLOC · AGI (2023) · The Local (2015)",
     7: "Fonti: Il Post (2014) · Doppiozero (2014) · L'Espresso (2013, 2015) · Live Science (2019) · JSTOR Daily · INAF (2010) · Wikipedia",
     8: "Fonti: L'Espresso (2013, 2015) · ILAB (2013) · AGI (2023) · Finestre sull'Arte (2026) · Wikipedia · La Nazione (2024)",
     9: "Fonti: ILAB (2015) · The Local (2015) · L'Espresso (2013, 2015) · AGI (2023, 2026) · Finestre sull'Arte · SiViaggia · inITALY (2026)",
     10: "Fonti: ILAB · AGI (2023) · Wikipedia · L'Espresso · JSTOR Daily · Live Science · La Nazione (2024)",
     11: "Fonti: AGI (2023) · ILAB · L'Espresso (2013) · Ministero della Cultura · consigli generali, non consulenza legale",
     12: "Fonti: tutte in descrizione · ricostruzione a scopo divulgativo"}

CHT = {1: "Napoli,\nla *biblioteca*", 2: "I *protagonisti*", 3: "Il nuovo\n*direttore*", 4: "Le notti\ndei *Girolamini*",
       5: "La *denuncia*", 6: "L'indagine e\nl'asta di *Monaco*", 7: "L'arresto e il\nfalso *Galileo*", 8: "I *processi*",
       9: "Dove sono finiti\ni *libri*", 10: "Le domande *aperte*", 11: "La *lezione*", 12: "Il *verdetto*"}
LASTCH = 12
FIRST = {}
for k, (h, _) in enumerate(SCENES_H):
    FIRST.setdefault(h, k)

BOARD = [("LA BIBLIOTECA", "Girolamini · Napoli · dal 1586", "card"), ("IL DIRETTORE", "M. M. De Caro · condannato", "person"),
         ("LO STORICO DELL'ARTE", "Tomaso Montanari · la denuncia", "person"), ("I BIBLIOTECARI", "i testimoni · nessun nome", "person"),
         ("CARABINIERI E PROCURA", "Napoli · l'inchiesta", "card"), ("LO STUDIOSO", "Nick Wilding · il falso Galileo", "person")]
BXY = [(960, 450), (420, 450), (1500, 450), (420, 740), (960, 740), (1500, 740)]

def board_el(n, t0, t1):
    nodes = {}
    for j in range(n + 1):
        nm, role, kind = BOARD[j]
        nodes[f"n{j}"] = dict(xy=BXY[j], name=nm, role=role, t=t0 + (0.2 if j == n else -5), rot=(-3 + 2 * (j % 3)))
    pairs = [(0, 1), (0, 2), (0, 3), (3, 4), (1, 4), (1, 5)]
    links = [(f"n{p}", f"n{q}", t0 - 5 if max(p, q) < n else t0 + 0.6) for p, q in pairs if max(p, q) <= n]
    return Board(nodes, links, t0, t1, cw=220)

# ------------------------------------------------------------------ scaletta visiva: (parola, comando)
V = {
 0: [("Napoli", "map:Napoli|60|Napoli"), ("biblioteche", "sala:day|1|1|NAPOLI · PRIMAVERA 2012"), ("sparendo", "sala:day|1|0.55|I LIBRI SPARISCONO"), ("ladro", "i:window|NESSUNA FINESTRA FORZATA"), ("custodirli", "i:keys|CHI AVEVA LE CHIAVI"), ("direttore", "stamp:IL DIRETTORE")],
 1: [("Nel", "sala:night|0.8|0.5|IN CIRCA UN ANNO"), ("deposito", "map:Verona|35|Napoli,Verona|Napoli>Verona"), ("Centinaia", "i:catalog|MONACO DI BAVIERA"), ("vendita", "stamp:FERMATA")],
 2: [("dietro", "h:Un'altra *storia*"), ("Galileo", "i:telescope|GALILEO GALILEI"), ("Sidereus", "i:moonbook|SCHEMA · NON L'ORIGINALE"), ("falso", "stamp:FALSO")],
 3: [("In", "iii:library|LA BIBLIOTECA|nophoto|IL DIRETTORE|gavel|I GIUDICI"), ("dove", "i:boxbooks|DOVE SONO FINITI I LIBRI?"), ("Questo", "cover"), ("Girolamini", "t:LA BIBLIOTECA DEI GIROLAMINI")],
 4: [("Partiamo", "map:Napoli|60|Napoli"), ("Duomo", "iii:basilica|LA CATTEDRALE|arrow_icon|DI FRONTE|library|I GIROLAMINI"), ("complesso", "iii:basilica|UNA CHIESA|convent|UN CONVENTO|openbook|UNA BIBLIOTECA")],
 5: [("Il", "cal:FINE CINQUECENTO|1586"), ("Oratoriani", "fig:man|I PADRI ORATORIANI"), ("Filippini", "t:FILIPPINI · GIROLAMINI")],
 6: [("La", "big:1586|la biblioteca apre al pubblico"), ("pubblico", "sala:day|1|1|APERTA AL PUBBLICO DAL 1586"), ("Malatestiana", "map:Napoli|10|Cesena,Napoli"), ("seconda", "tl:CESENA · MALATESTIANA|LA PRIMA;NAPOLI · GIROLAMINI|LA SECONDA")],
 7: [("Che", "h:Una biblioteca\n*aperta*"), ("monastero", "ii:convent|CHIUSA NEI MONASTERI|openbook|APERTA A CHI STUDIA"), ("studia", "fig:expert|CHI STUDIA"), ("rara", "stamp:RARO")],
 8: [("Nei", "iii:letter|DONAZIONI|scroll_icon|LASCITI|money|ACQUISTI"), ("centosessantamila", "big:≈ 160.000|volumi"), ("cinquemila", "big:≈ 5.000|cinquecentine · libri del Cinquecento"), ("incunaboli", "i:oldbook|E DECINE DI INCUNABOLI")],
 9: [("Gli", "i:oldbook|INCUNABOLI · PRIMA DEL 1501"), ("numero", "bars:UNA FONTE · 94|94|UN'ALTRA FONTE · 120|120"), ("alcune", "t:LE FONTI NON COINCIDONO")],
 10: [("C'è", "i:note_icon|ARCHIVIO MUSICALE · XVI-XIX SEC."), ("filosofia", "iii:openbook|FILOSOFIA|basilica|TEOLOGIA|oldbook|STORIA DELLA CHIESA"), ("studiosi", "fig:expert|UNA BIBLIOTECA DA STUDIOSI")],
 11: [("Fra", "card:GIAMBATTISTA VICO|filosofo · Settecento|frequentatore della biblioteca"), ("Valletta", "flow:CONSIGLIO DI VICO>RACCOLTA VALLETTA"), ("sale", "sala:day|1|1|LA SALA VICO")],
 12: [("Facciamo", "i:calc|UN CONTO"), ("passano", "tl:1586|APERTURA;1861|UNITÀ D'ITALIA;2011|IL NUOVO DIRETTORE"), ("quattrocentoventi", "big:oltre 420 anni|di biblioteca aperta"), ("rimasti", "i:shelf|I LIBRI SONO RIMASTI LÌ")],
 13: [("proviamo", "i:shelf|160.000 VOLUMI"), ("tre", "flow:160.000 × 3 CM>≈ 4,8 KM DI SCAFFALI"), ("stima", "t:STIMA INDICATIVA"), ("vuoto", "i:shelf_gaps|UN VUOTO PASSA INOSSERVATO")],
 14: [("Un", "h:Di *chi* sono\nquei libri?"), ("statale", "i:ministry|BIBLIOTECA STATALE · MINISTERO DELLA CULTURA"), ("patrimonio", "big:patrimonio pubblico|appartiene a tutti"), ("tutti", "crowd")],
 15: [("Ed", "i:folder|LE ACCUSE"), ("porta", "flow:BIBLIOTECA PUBBLICA>CHI LA DIRIGE"), ("nome", "stamp:UN REATO PRECISO")],
 16: [("Apriamo", "board:0"), ("Intorno", "t:I PROTAGONISTI")],
 17: [("Il", "board:1"), ("commerciante", "iii:oldbook|LIBRI ANTICHI|money|IL COMMERCIO|map_icon|VERONA"), ("ministero", "i:ministry|CONSULENTE AL MINISTERO"), ("condannato", "stamp:CONDANNA DEFINITIVA")],
 18: [("Il", "board:2"), ("primo", "i:press|IL PRIMO A RACCONTARLO")],
 19: [("Poi", "board:3"), ("vedono", "i:eye|CHI VEDE OGNI GIORNO"), ("testimonianze", "stamp:TESTIMONI")],
 20: [("Ci", "board:4"), ("sequestro", "i:seal|IL SEQUESTRO"), ("casa", "i:catalog|UNA CASA D'ASTE · MONACO")],
 21: [("Infine", "board:5"), ("smascherare", "i:magnifier|IL FALSO GALILEO")],
 22: [("Una", "h:Nota di *metodo*"), ("due", "big:2 fonti|per ogni fatto"), ("coincidono", "t:VERSIONI DIVERSE: LO DICIAMO"), ("condannate", "i:nophoto|NON CONDANNATI: NESSUN NOME")],
 23: [("Per", "iii:nophoto|ALTRI IMPUTATI|nophoto|INTERMEDIARI|nophoto|ALTRI FILONI"), ("fatti", "ii:check|FATTI ACCERTATI|gavel|CONDANNE DEFINITIVE")],
 24: [("Primo", "t:RIEPILOGO · 1"), ("biblioteca", "sala:day|1|1|DAL 1586 · ≈ 160.000 VOLUMI"), ("direttore", "i:boxbooks|DAL COMMERCIO DI LIBRI ANTICHI"), ("custodisce", "ii:keys|CHI CUSTODISCE|money|CHI VENDE")],
 25: [("Come", "h:Come si diventa\n*direttore*?"), ("passo", "cal:PRIMAVERA|2011")],
 26: [("De", "i:ministry|CONSULENTE DEL MINISTRO"), ("incarico", "card:L'INCARICO|primavera 2011|tutela del patrimonio librario"), ("giugno", "cal:GIUGNO|2011"), ("diventa", "i:keys|DIRETTORE DEI GIROLAMINI")],
 27: [("Su", "court:IL GIP"), ("regola", "card:L'ORDINANZA DEL GIP|nomina «contro ogni regola»|grazie al ruolo di consigliere")],
 28: [("Fermiamoci", "h:Chi dirige\nuna *biblioteca*?"), ("funzionario", "fig:expert|BIBLIOTECARIO DI CARRIERA"), ("concorso", "i:letter|UN CONCORSO"), ("commercio", "fig:suit|DAL COMMERCIO")],
 29: [("Non", "i:money|IL VALORE DI MERCATO"), ("edizioni", "iii:oldbook|LE EDIZIONI|money|I PREZZI|catalog|DOVE SI VENDONO"), ("rischio", "stamp:UN RISCHIO")],
 30: [("C'è", "h:Lo stato\ndella *biblioteca*"), ("enorme", "sala:mess|0.9|0.9|UN PATRIMONIO ENORME"), ("inventario", "i:register|L'INVENTARIO"), ("lunghissimo", "i:hourglass|ANNI DI LAVORO")],
 31: [("E", "i:register|SENZA INVENTARIO PRECISO"), ("manca", "i:question|CHE COSA MANCA?"), ("numero", "stamp:NESSUN NUMERO UNICO")],
 32: [("Il", "i:keys|LE CHIAVI"), ("giugno", "cal:GIUGNO|2011"), ("cambia", "sala:day|1|0.85|LA BIBLIOTECA CAMBIA VOLTO")],
 33: [("Eccoci", "h:Il cuore\ndel *caso*"), ("l'estate", "tl:ESTATE 2011|;PRIMAVERA 2012|"), ("concordano", "sala:day|1|0.7|I LIBRI ESCONO"), ("quantità", "i:boxbooks|UNA GRANDE QUANTITÀ")],
 34: [("I", "sala:night|0.7|0.6|DI NOTTE"), ("furgoni", "i:van|FURGONI CARICHI"), ("Scatole", "iii:boxbooks|SCATOLE|crate|CASSE|parcel|PACCHI")],
 35: [("Secondo", "i:hiddencam|LE TELECAMERE"), ("telecamere", "fig:man|SCATOLE DI LIBRI"), ("Saranno", "ii:eye|TESTIMONIANZE|camera|IMMAGINI"), ("raccolti", "t:SECONDO LE RICOSTRUZIONI")],
 36: [("Quali", "h:*Quali* libri?"), ("qualsiasi", "i:oldbook|EDIZIONI RARE"), ("Cinquecento", "tl:CINQUECENTO|;SEICENTO|"), ("scienza", "iii:telescope|SCIENZA|moon|ASTRONOMIA|oldbook|PRIME EDIZIONI"), ("Galileo", "t:GALILEO · COPERNICO · KEPLERO")],
 37: [("E", "sala:mess|0.6|0.6|LIBRI A TERRA"), ("pavimento", "i:shelf_gaps|SCAFFALI IN DISORDINE"), ("Un'immagine", "stamp:ABBANDONO")],
 38: [("Facciamo", "i:calc|UN CONTO"), ("duemila", "big:oltre 2.000|volumi in circa un anno"), ("diviso", "flow:2.000 ÷ 365>PIÙ DI 5 AL GIORNO"), ("Ogni", "clock:22|OGNI GIORNO")],
 39: [("E", "i:newspaper|NON ROMANZI DA EDICOLA"), ("singolo", "bars:LIBRO COMUNE|1|LIBRO ANTICO RARO|9"), ("danno", "t:IL DANNO NON È SOLO UN NUMERO")],
 40: [("C'è", "h:I *segni*\ndei libri"), ("timbri", "iii:libstamp|TIMBRI|tag|COLLOCAZIONE|pen|NOTE DI POSSESSO"), ("carta", "card:CARTA D'IDENTITÀ|del volume|timbro · numero · note"), ("tradiranno", "stamp:IL TRADIMENTO")],
 41: [("Secondo", "i:libstamp_x|SEGNI RIMOSSI IN FRETTA"), ("maldestro", "t:SECONDO LA CASA D'ASTE"), ("segnale", "i:magnifier|UN SEGNALE PER UN ESPERTO")],
 42: [("Dove", "h:*Dove* vanno?"), ("Veronese", "map:Verona|35|Napoli,Verona|Napoli>Verona"), ("dell'estero", "map:Monaco di Baviera|12|Napoli,Monaco di Baviera,Londra"), ("nessuno", "i:question|NESSUNO SA NIENTE")],
 43: [("Secondo", "t:RIEPILOGO · 2"), ("Napoli", "sala:day|1|1|APERTA DAL 1586"), ("giugno", "cal:NUOVO DIRETTORE|2011"), ("migliaia", "sala:day|1|0.5|MIGLIAIA DI LIBRI SPARITI")],
 44: [("Arriviamo", "cal:INIZIO|2012"), ("Montanari", "fig:expert|TOMASO MONTANARI"), ("vede", "sala:mess|0.6|0.6|LIBRI A TERRA · DISORDINE")],
 45: [("E", "i:eye|CHI LAVORA LÌ"), ("grave", "flow:I LIBRI ESCONO>IL DIRETTORE?"), ("scriverne", "i:pen|DECIDE DI SCRIVERNE")],
 46: [("A", "news:CRONACA|aprile 2012|*I libri*\nspariti|ricostruzione grafica · non l'originale"), ("Descrive", "sala:mess|0.6|0.6|COME LA DESCRIVE"), ("movimenti", "i:truck|MOVIMENTI SOSPETTI NEI CORTILI"), ("pubblica", "stamp:PUBBLICO")],
 47: [("Intorno", "i:petition|LA PETIZIONE"), ("studiosi", "iii:pen|INTELLETTUALI|openbook|STUDIOSI|ministry|AL MINISTRO"), ("direttore", "i:keys|«RIMUOVETE IL DIRETTORE»"), ("firme", "big:≈ 2.000|firme")],
 48: [("La", "h:La *reazione*"), ("millecinquecento", "big:≈ 1.500|volumi mancanti"), ("procura", "sala:seized|0.55|0.55|APRILE 2012"), ("Il", "i:keys|DIRETTORE ALLONTANATO")],
 49: [("Fermiamoci", "h:Tutto in\npochi *giorni*"), ("articolo", "tl:ARTICOLO|;PETIZIONE|;SEQUESTRO|"), ("mesi", "i:hourglass|MESI SENZA CONTROLLI"), ("macchina", "stamp:SI PARTE")],
 50: [("Un", "i:seal|SOTTO SEQUESTRO"), ("chiude", "sala:seized|0.55|0.55|CHIUSA"), ("resterà", "i:calendar_x|A LUNGO")],
 51: [("Ma", "h:Un *problema*"), ("sigilli", "i:seal|PROTEGGE CIÒ CHE RESTA"), ("Non", "i:boxbooks|NON RIPORTA INDIETRO"), ("venduta", "i:catalog|IN VENDITA")],
 52: [("A", "subscribe")],
 53: [("Inizia", "h:Inizia\nl'*indagine*"), ("tre", "iii:question|QUALI LIBRI?|map_icon|DOVE?|nophoto|CHI?"), ("semplice", "stamp:NIENTE DI SEMPLICE")],
 54: [("La", "map:Monaco di Baviera|12|Napoli,Monaco di Baviera|Napoli>Monaco di Baviera"), ("casa", "i:catalog|CASA D'ASTE · LIBRI ANTICHI"), ("nove", "cal:ASTA · 9-11 MAGGIO|2012")],
 55: [("Nel", "i:catalog|IL CATALOGO"), ("Esperti", "i:magnifier|QUALCOSA NON TORNA"), ("segni", "ii:libstamp|SEGNI DEI GIROLAMINI|libstamp_x|SEGNI RIMOSSI"), ("segnalazione", "i:policecar|LE AUTORITÀ")],
 56: [("La", "cal:SERA DELL'8 MAGGIO|2012"), ("autorità", "i:policecar|LE AUTORITÀ TEDESCHE"), ("sequestrati", "i:seal|LIBRI DA SEQUESTRARE"), ("vendita", "i:lots|LOTTI RITIRATI"), ("soffio", "stamp:PER UN SOFFIO")],
 57: [("Quanti", "h:*Quanti* libri?"), ("fonti", "bars:UNA FONTE · OLTRE 400|400|ALTRE FONTI · ≈ 500|500|ALTRE ANCORA · OLTRE 600|600"), ("centinaia", "t:IN OGNI CASO: CENTINAIA")],
 58: [("Facciamo", "i:calc|I TEMPI"), ("sequestro", "tl:APRILE|SEQUESTRO;MAGGIO|L'ASTA"), ("mese", "iii:nophoto|ACQUIRENTE|nophoto|ACQUIRENTE|nophoto|ACQUIRENTE")],
 59: [("Intanto", "map:Verona|35|Verona,Napoli"), ("depositi", "i:warehouse|DEPOSITI NEL VERONESE"), ("timbro", "i:libstamp|IL TIMBRO DEI GIROLAMINI")],
 60: [("Sul", "h:*Quanti* a Verona?"), ("alcune", "bars:UNA FONTE · ≈ 240 DELLA BIBLIOTECA|240|UN'ALTRA · ≈ 1.000 LIBRI IN TUTTO|1000"), ("filo", "map:Verona|35|Napoli,Verona|Napoli>Verona")],
 61: [("A", "h:L'inchiesta\nsi *allarga*"), ("passaggi", "iii:nophoto|INTERMEDIARI|shop|LIBRERIE|catalog|CASE D'ASTE"), ("lavoro", "iii:catalog|CATALOGHI|libstamp|TIMBRI|magnifier|CONFRONTI")],
 62: [("Anche", "i:catalog|IL TITOLARE DELLA CASA D'ASTE"), ("nell'agosto", "cal:ARRESTATO IN GERMANIA|AGO 2013"), ("esiti", "i:nophoto|ESITI NON CONCORDI · NESSUN NOME")],
 63: [("Torniamo", "cal:MAGGIO|2012"), ("l'arresto", "i:handcuffs|L'ARRESTO"), ("Marino", "card:MARINO MASSIMO DE CARO|direttore dei Girolamini|arrestato · maggio 2012"), ("peculato", "stamp:PECULATO")],
 64: [("Che", "h:Che cos'è il\n*peculato*?"), ("reato", "card:PECULATO|art. 314 codice penale|il pubblico ufficiale che si appropria"), ("estraneo", "ii:nophoto|UN ESTRANEO|keys|CHI CUSTODISCE"), ("Esattamente", "i:library|IL DIRETTORE E LA SUA BIBLIOTECA")],
 65: [("A", "cal:GIUGNO|2012"), ("un'associazione", "card:L'ACCUSA SI ALLARGA|associazione per delinquere|ipotesi degli investigatori"), ("percorso", "map:Verona|12|Napoli,Verona,Monaco di Baviera|Napoli>Verona>Monaco di Baviera")],
 66: [("E", "i:mic|LA CONFESSIONE"), ("ammette", "stamp:AMMETTE"), ("zone", "i:question|ZONE D'OMBRA")],
 67: [("Ed", "h:Un'altra\n*storia*"), ("Galileo", "i:telescope|GALILEO GALILEI"), ("Sidereus", "i:moonbook|IL SIDEREUS NUNCIUS · SCHEMA")],
 68: [("Il", "map:Venezia|35|Venezia"), ("Venezia", "cal:VENEZIA · MARZO|1610"), ("latino", "i:openbook|POCHE PAGINE IN LATINO"), ("cannocchiale", "i:telescope|IL CANNOCCHIALE")],
 69: [("È", "h:Una *rivoluzione*"), ("Luna", "i:moon|MONTAGNE, VALLI, CRATERI"), ("Via", "i:stars_icon|LA VIA LATTEA: INNUMEREVOLI STELLE"), ("Giove", "i:jupiter|4 SATELLITI DI GIOVE · ASTRI MEDICEI")],
 70: [("La", "big:550|copie stampate"), ("sopravvivono", "bars:STAMPATE NEL 1610 · 550|550|SOPRAVVISSUTE OGGI · ≈ 150|150"), ("collezionista", "i:money|UNO DEI LIBRI PIÙ DESIDERATI")],
 71: [("Ora", "h:Una copia\n*mai vista*"), ("firma", "ii:pen|LA FIRMA DI GALILEO|moonbook|ACQUERELLI DELLA LUNA"), ("Come", "t:SCHEMA · NON È IL LIBRO ORIGINALE")],
 72: [("Questa", "i:catalog|SUL MERCATO"), ("2005", "map:New York|10|Napoli,New York|Napoli>New York"), ("mezzo", "big:≈ 500.000 $|il prezzo · 2005"), ("venditori", "card:TRA I VENDITORI|Marino Massimo De Caro|secondo le ricostruzioni")],
 73: [("Il", "fig:expert|UN GRUPPO DI ESPERTI"), ("2011", "cal:DUE VOLUMI DI STUDI|2011"), ("secolo", "stamp:LA SCOPERTA DEL SECOLO?")],
 74: [("Ma", "card:NICK WILDING|studioso di storia del libro|decide di verificare"), ("Confronta", "ii:moonbook|LA COPIA DI NEW YORK|facsimile|LE RIPRODUZIONI"), ("prova", "i:blot|UN PICCOLO SEGNO")],
 75: [("Quel", "i:blot|IL SEGNO SUL FRONTESPIZIO"), ("facsimile", "i:facsimile|IL FACSIMILE DEL 1964"), ("difetto", "flow:DIFETTO DEL 1964>NEL LIBRO «DEL 1610»")],
 76: [("In", "h:In altre\n*parole*"), ("copiando", "flow:UN FACSIMILE DEL NOVECENTO>UN FALSO"), ("zero", "stamp:FALSO"), ("2012", "tl:2005|LA VENDITA;2011|GLI STUDI;2012|LA NOTIZIA;2014|IL VOLUME: È FALSO")],
 77: [("E", "i:mic|L'AMMISSIONE"), ("copie", "iii:moonbook|COPIA?|moonbook|COPIA?|moonbook|COPIA?"), ("quante", "t:QUANTE? LE FONTI NON COINCIDONO"), ("quadro", "flow:I LIBRI RUBATI>UN GIRO DI FALSI")],
 78: [("Perché", "h:A che cosa\n*serve* un falso?"), ("posto", "ii:oldbook|L'ORIGINALE ESCE|moonbook|IL FALSO RESTA"), ("controlla", "stamp:NESSUNO SE NE ACCORGE")],
 79: [("Terzo", "t:RIEPILOGO · 3"), ("arrestato", "i:handcuffs|ARRESTO E CONFESSIONE"), ("peculato", "stamp:PECULATO"), ("Galileo", "map:New York|10|Napoli,New York"), ("creduto", "i:moonbook|CREDUTO AUTENTICO PER ANNI")],
 80: [("Arriviamo", "court:I PROCESSI"), ("filoni", "iii:folder|FILONE 1|folder|FILONE 2|folder|FILONE 3"), ("certezza", "i:check|SOLO CIÒ CHE È CERTO")],
 81: [("Il", "card:RITO ABBREVIATO|si decide sugli atti|sconto di pena"), ("atti", "i:folder|GLI ATTI DELLE INDAGINI"), ("sconto", "big:sconto|di pena · previsto dal rito"), ("marzo", "court:PRIMO GRADO · MARZO 2013")],
 82: [("La", "big:7 anni|di reclusione per peculato"), ("l'interdizione", "card:INTERDIZIONE PERPETUA|dai pubblici uffici|per sempre"), ("collaboratori", "iii:nophoto|CONDANNATI|nophoto|NESSUN NOME|nophoto|PRIMO GRADO")],
 83: [("Poi", "tl:PRIMO GRADO|2013;DEFINITIVA|ENTRO IL 2015"), ("definitiva", "stamp:DEFINITIVA"), ("dubbi", "i:check|NESSUN DUBBIO")],
 84: [("De", "ii:house|DETENZIONE DOMICILIARE|cell|NON IN CELLA"), ("date", "i:calendar_x|DATE NON INDICATE")],
 85: [("Accanto", "court:CORTE DEI CONTI"), ("danno", "big:≈ 20 milioni|di euro · il risarcimento")],
 86: [("Facciamo", "i:calc|UN CONTO"), ("diviso", "flow:20 MILIONI ÷ 2.000>≈ 10.000 € A LIBRO"), ("media", "bars:LIBRO MENO PREZIOSO|1|MEDIA|4|LIBRO PIÙ PREZIOSO|9"), ("grandezza", "t:SOLO UN ORDINE DI GRANDEZZA")],
 87: [("Ci", "iii:folder|ASSOCIAZIONE?|nophoto|ALTRE PERSONE|folder|ALTRI FILONI"), ("diverse", "i:question|ESITI RIPORTATI IN MODO DIVERSO")],
 88: [("Una", "h:Da dire\n*chiaramente*"), ("assolte", "stamp:ASSOLTI"), ("Chi", "i:nophoto|NON CONDANNATI: NON COLPEVOLI")],
 89: [("Quarto", "t:RIEPILOGO · 4"), ("l'articolo", "tl:APR 2012|ARTICOLO E SEQUESTRO;MAG 2012|ASTA FERMATA · ARRESTO;MAR 2013|7 ANNI"), ("mezzo", "i:moonbook|IL FALSO GALILEO")],
 90: [("Ora", "h:*Dove* sono finiti\ni libri?"), ("recupero", "i:boxbooks|IL RECUPERO"), ("concluso", "stamp:NON CONCLUSO")],
 91: [("Il", "map:Monaco di Baviera|12|Monaco di Baviera,Napoli|Monaco di Baviera>Napoli"), ("febbraio", "cal:RESTITUITI|FEB 2015"), ("cinquecento", "big:≈ 500|volumi tornano in Italia")],
 92: [("Anche", "bars:UNA FONTE · ≈ 500 LIBRI|500|UN'ALTRA · 543 LIBRI|543"), ("valore", "big:2 - 2,5 milioni|di euro · stime non concordi"), ("Galileo", "iii:telescope|GALILEO|moon|COPERNICO|jupiter|KEPLERO")],
 93: [("Altri", "map:Verona|35|Verona,Napoli|Verona>Napoli"), ("2013", "bars:RECUPERATI · CRONACHE 2013 · ≈ 2.700|2700|RECUPERATI · CRONACHE 2015 · ≈ 4.000|4000"), ("cifre", "t:CIFRE DIVERSE PER FONTE E MOMENTO")],
 94: [("E", "h:Quanti *in tutto*?"), ("millecinquecento", "bars:STIMA 2012 · 1.500|1500|STIMA SUCCESSIVA · OLTRE 2.000|2000|STIMA PIÙ ALTA · 4.000|4000"), ("Un'associazione", "i:question|«NON SI SA NEMMENO QUANTI»")],
 95: [("Il", "i:register|L'INVENTARIO"), ("difficilissimo", "i:shelf_gaps|CHE COSA MANCA?"), ("rifare", "i:hourglass|ANNI DI LAVORO")],
 96: [("Il", "map:Montecassino|35|Montecassino,Napoli"), ("Montecassino", "i:abbey|ABBAZIA DI MONTECASSINO · 2011"), ("presentava", "ii:nophoto|«UNO STUDIOSO»|ministry|«CONSULENTE DEL MINISTERO»"), ("monaci", "t:SECONDO LE RICOSTRUZIONI")],
 97: [("E", "sala:seized|0.6|0.6|SOTTO SEQUESTRO"), ("anni", "i:calendar_x|CHIUSA PER ANNI"), ("Una", "flow:APERTA DAL 1586>CHIUSA OLTRE UN DECENNIO")],
 98: [("La", "cal:LA RIAPERTURA · 22 APRILE|2026"), ("sale", "sala:open|0.8|0.8|APRILE 2026 · DI NUOVO APERTA"), ("Acquaviva", "i:openbook|MOSTRA: RINASCIMENTO MERIDIONALE")],
 99: [("Facciamo", "i:calc|L'ULTIMO CONTO"), ("riapertura", "tl:2012|SEQUESTRO;2026|RIAPERTURA"), ("doppio", "bars:ANNI DI CONDANNA · 7|7|ANNI DI CHIUSURA · 14|14")],
 100: [("Restano", "h:Le domande\n*aperte*"), ("prima", "h:*1*"), ("stime", "bars:STIMA PIÙ BASSA · 1.500|1500|STIMA PIÙ ALTA · 4.000|4000"), ("Senza", "i:register|NESSUN INVENTARIO AFFIDABILE")],
 101: [("La", "h:*2*"), ("tornata", "ii:boxbooks|TORNATI|question|DISPERSI"), ("riemerge", "i:catalog|RIEMERGE DA UN CATALOGO")],
 102: [("La", "h:*3*"), ("Un", "i:keys|LE CHIAVI A UNA PERSONA"), ("controllo", "stamp:NESSUN CONTROLLO"), ("fermarlo", "i:press|UN ARTICOLO")],
 103: [("La", "h:*4* · i falsi"), ("copie", "iii:moonbook|?|moonbook|?|moonbook|?"), ("circolazione", "ii:oldbook|L'ORIGINALE?|moonbook|IL FALSO?")],
 104: [("La", "h:*5* · gli altri filoni"), ("decisioni", "iii:folder|ANNI DOPO|question|ESITI DIVERSI|gavel|ALTRE DECISIONI"), ("certe", "stamp:SOLO CONDANNE CERTE")],
 105: [("E", "h:Una domanda\n*più grande*"), ("biblioteche", "iii:library|BIBLIOTECHE|folder|ARCHIVI|abbey|ABBAZIE"), ("esempio", "i:openbook|UN CASO STUDIATO")],
 106: [("Che", "h:Cinque *idee*"), ("ama", "iii:openbook|CHI AMA I LIBRI|money|CHI LI COMPRA|keys|CHI LI CUSTODISCE")],
 107: [("Primo", "h:*1* · i timbri\ncontano"), ("timbro", "ii:libstamp|TIMBRO DI BIBLIOTECA|libstamp_x|TIMBRO CANCELLATO"), ("compra", "i:letter|CHIEDI DA DOVE VIENE")],
 108: [("Secondo", "h:*2* · l'inventario\nè la prima difesa"), ("sa", "i:register|SAI COSA POSSIEDI?"), ("senza", "i:shelf_gaps|ALTRIMENTI: MESI DI VUOTI")],
 109: [("Terzo", "h:*3* · più di\nuna persona"), ("chiavi", "i:keys|UNA SOLA PERSONA"), ("Più", "iii:nophoto|PIÙ CONTROLLI|register|REGISTRI|camera|TELECAMERE"), ("regole", "stamp:FUNZIONANO")],
 110: [("Quarto", "h:*4* · chi vede,\nparli"), ("decisivi", "ii:eye|I BIBLIOTECARI|pen|LO STUDIOSO"), ("carabinieri", "card:CARABINIERI|tutela patrimonio culturale|si può segnalare un'opera sospetta")],
 111: [("Quinto", "h:*5* · anche gli\nesperti sbagliano"), ("falso", "i:moonbook|ANNI DI INGANNO"), ("controllo", "i:magnifier|UN CONTROLLO IN PIÙ")],
 112: [("Ricapitoliamo", "t:IL VERDETTO"), ("Uno", "sala:day|1|1|DAL 1586 · ≈ 160.000 VOLUMI")],
 113: [("Due", "cal:IL NUOVO DIRETTORE|2011"), ("Tre", "sala:night|0.8|0.5|ANCHE DI NOTTE")],
 114: [("Quattro", "news:CRONACA|aprile 2012|*I libri*\nspariti|ricostruzione grafica · non l'originale"), ("sequestro", "i:seal|SEQUESTRO · ASTA FERMATA · ARRESTO"), ("Cinque", "big:7 anni|per peculato · definitiva")],
 115: [("Sei", "i:blot|IL FALSO GALILEO SMASCHERATO"), ("riapre", "sala:open|0.8|0.8|RIAPERTA NEL 2026"), ("Molti", "ii:boxbooks|TORNATI|question|ANCORA DISPERSI")],
 116: [("E", "ii:library|UN PATRIMONIO|question|COME SI PROTEGGE?"), ("Scrivilo", "i:envelope|SCRIVILO NEI COMMENTI")],
 117: [("Iscriviti", "subscribe")],
}

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

ALIAS = {"basilica": "convent", "calendar_x": "hourglass", "van": "truck", "warehouse": "boxbooks", "window": "window", "arrow_icon": "front", "scroll_icon": "letter", "note_icon": "music", "stars_icon": "stars", "map_icon": "globe2", "check": "shield_ok", "stop": "warn", "doc_icon": "letter", "mic": "microphone",
         "clock_icon": "hourglass", "fig_icon": "nophoto"}
def IC(n): return ALIAS.get(n, n)


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
        sc.add(ClockFace((960, 520), 220, t0, t1, start=hh - 0.4, speed=0.08, label=(p[1] if len(p) > 1 else "")), "pop")
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
    elif k == "sala":
        sc.add(Sala(SALA, t0, t1, mode=p[0], fill=float(p[1]), fill_to=float(p[2]), label=(p[3] if len(p) > 3 else None)))
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
        sc.add(Img(cover_folder22(620), (960, 560), t0, t1, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 022", (1180, 360), t0 + 0.6, t1, size=70, rot=-12))
    elif k == "subscribe":
        sc.add(Img(wordmark(120), (960, 470), t0, t1, anim="pop", shadow=False), "hit")
        sc.add(Pill("ISCRIVITI · OGNI GIORNO UN NUOVO CASO", (960, 700), t0 + 0.4, t1, size=50, accent=True))
    elif k == "fig":
        sc.add(Figure(walk([(40, FY), (230, FY)], t0, 420), t0, t1, kind=p[0], s=1.0, label=(p[1] if len(p) > 1 and p[1] else None)), "pop")
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
        num = f"{h:02d}" if h < LASTCH else None
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
    bg = make_bg(22).convert("RGBA"); lay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    im = rich_img("Il direttore\nche portava via\ni *libri*", SERIF, 150, color=WHITE, lh=1.0)
    place(lay, im, (90, 170), "la")
    place(lay, fx.icon("shelf_gaps", 520), (1450, 430), "mm")
    place(lay, fx.icon("boxbooks", 300), (1700, 690), "mm")
    place(lay, fx.icon("moonbook", 260), (1250, 720), "mm")
    st2 = stamp_img("CASO 022", size=60, rot=-8); place(lay, st2, (380, 90), "mm")
    st = stamp_img("PECULATO", size=74, rot=-10); place(lay, st, (1640, 930), "mm")
    f = font(OSW, 52, 700); s_ = "NAPOLI: MIGLIAIA DI LIBRI ANTICHI SPARITI"; tw = tl(d, s_, f)
    d.rectangle([90, 800, 90 + tw + 60, 905], fill=(230, 190, 40, 255))
    d.text((120, 852), s_, font=f, fill=(20, 18, 16, 255), anchor="lm")
    place(lay, wordmark(70), (90, 975), "lm")
    out = Image.alpha_composite(bg, lay).convert("RGB"); out.save(path, quality=92)
