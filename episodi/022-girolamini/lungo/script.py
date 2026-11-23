STYLE = "fascicolo"
CASE = "FASCICOLO N. 022 · IL BIBLIOTECARIO"
TITLE = "Il bibliotecario"
CH = ["INTRO", "1 · NAPOLI, LA BIBLIOTECA", "2 · I PROTAGONISTI", "3 · IL NUOVO DIRETTORE", "4 · LE NOTTI DEI GIROLAMINI",
      "5 · LA DENUNCIA", "6 · L'INDAGINE E L'ASTA DI MONACO", "7 · L'ARRESTO E IL FALSO GALILEO", "8 · I PROCESSI",
      "9 · DOVE SONO FINITI I LIBRI", "10 · LE DOMANDE APERTE", "11 · LA LEZIONE", "IL VERDETTO"]
import re

def S(ch, text):
    """divide il testo in frasi (punto, punto di domanda, due punti) senza toccare le parentesi [display|parlato]"""
    from num2words import num2words
    parts = re.split(r"(\[[^\]]*\])", text)
    text = "".join(q if q.startswith("[") else re.sub(r"\b(\d+)\b", lambda m: f"[{m.group(1)}|{num2words(int(m.group(1)), lang='it')}]", q) for q in parts)
    text = re.sub(r"\[([^|\]]*)\|([^\]]*)\]([.,:;?!])", r"[\1\3|\2\3]", text)
    out, cur, depth = [], "", 0
    for k, c in enumerate(text):
        cur += c
        if c == "[": depth += 1
        elif c == "]": depth -= 1
        nxt = text[k + 1] if k + 1 < len(text) else " "
        if depth == 0 and c in ".?:!" and nxt == " ":
            out.append([cur.strip(), .3]); cur = ""
        elif depth == 0 and c == "]" and cur.rstrip("]").endswith((".", "?", ":")) and nxt == " ":
            out.append([cur.strip(), .3]); cur = ""
    if cur.strip(): out.append([cur.strip(), .3])
    out[-1][1] = .6
    return (ch, [tuple(p) for p in out])

SN = "[Sidereus Nuncius|Sìdereus Nùncius]"
WIL = "[Wilding|Uàilding]"
NY = "[New York|Niu Iork]"
K160 = "[160.000|centosessantamila]"
K15 = "[1.500|millecinquecento]"
K2 = "[2.000|duemila]"
K5 = "[5.000|cinquemila]"
D500 = "[500.000|cinquecentomila]"
ZIS = "[Zisska|Zìsca]"

SCENES_H = [
 # ------------------------------------------------------------------ INTRO
 S(0, "Napoli, primavera del 2012. In una delle biblioteche più antiche d'Italia i libri stanno sparendo. Non per colpa di un ladro entrato da una finestra, ma, secondo le sentenze, per mano dell'uomo che doveva custodirli: il direttore."),
 S(0, "Nel giro di circa un anno migliaia di volumi antichi escono dagli scaffali. Alcuni finiscono in un deposito in provincia di Verona, altri all'estero. Centinaia arrivano in una casa d'aste di Monaco di Baviera, e la vendita viene fermata la sera prima."),
 S(0, f"E dietro al direttore c'è un'altra storia, ancora più incredibile: un libro di Galileo Galilei, il {SN}, che per anni studiosi di tutto il mondo hanno creduto autentico. Era un falso."),
 S(0, "In questo fascicolo vedremo com'era la biblioteca, chi la guidava, come sono state scoperte le sparizioni, cosa hanno deciso i giudici e dove sono finiti i libri. Questo è il caso della biblioteca dei Girolamini."),
 # ------------------------------------------------------------------ 1 · NAPOLI, LA BIBLIOTECA
 S(1, "Partiamo dal luogo. Siamo nel centro storico di Napoli, in via Duomo, quasi di fronte alla cattedrale. Qui sorge il complesso dei Girolamini: una chiesa, un convento con i suoi chiostri e una biblioteca."),
 S(1, "Il complesso nasce alla fine del Cinquecento, quando a Napoli si stabiliscono i padri Oratoriani, i seguaci di San Filippo Neri. A Napoli li chiamano Filippini, oppure Girolamini, ed è da loro che il luogo prende il nome."),
 S(1, "La data da ricordare è il 1586. Da quell'anno la biblioteca è aperta al pubblico. Le fonti la indicano come la più antica biblioteca pubblica di Napoli, e la seconda in Italia dopo la Malatestiana di Cesena."),
 S(1, "Che cosa vuol dire, nel Cinquecento, una biblioteca aperta al pubblico? Vuol dire che i libri non sono chiusi in un monastero per pochi religiosi: chi studia può entrare e leggere. Per l'epoca è una scelta rara."),
 S(1, "Nei secoli la raccolta cresce con donazioni, lasciti e acquisti. Oggi conta circa centosessantamila volumi. Tra questi ci sono circa cinquemila cinquecentine, cioè libri stampati nel Cinquecento, e decine di incunaboli."),
 S(1, "Gli incunaboli sono i libri stampati nei primi decenni della stampa a caratteri mobili, prima del 1501. Sul loro numero esatto ai Girolamini le fonti non coincidono: alcune parlano di poco meno di cento, altre di circa centoventi."),
 S(1, "C'è poi un archivio musicale con manoscritti dal Cinquecento all'Ottocento. E ci sono libri di filosofia, di teologia, di storia della Chiesa. È una biblioteca da studiosi, non da turisti."),
 S(1, "Fra i suoi frequentatori più illustri c'è il filosofo Giambattista Vico, nel Settecento. Su suo consiglio gli Oratoriani acquistano la raccolta privata dell'erudito Giuseppe Valletta. Una delle sale più belle porta ancora il suo nome: la sala Vico."),
 S(1, "Facciamo un conto per capire la scala. Dal 1586 al 2011 passano oltre quattrocentoventi anni. In tutto questo tempo la biblioteca ha attraversato regni, guerre, rivoluzioni, l'unità d'Italia. I suoi libri sono rimasti lì."),
 S(1, f"E proviamo a immaginare centosessantamila volumi. Se ogni libro occupasse in media tre centimetri di scaffale, servirebbero quasi cinque chilometri di ripiani. È una stima indicativa, ma rende l'idea: in un posto così, un vuoto può passare inosservato."),
 S(1, "Un ultimo elemento del contesto. La biblioteca dei Girolamini è una biblioteca statale, affidata al Ministero della Cultura. Questo significa una cosa importante: quei libri sono patrimonio pubblico. Appartengono a tutti."),
 S(1, "Ed è proprio questo che, più avanti, farà la differenza nelle accuse. Chi porta via un libro da una biblioteca pubblica che dirige non commette un furto qualunque. Commette un reato che ha un nome preciso. Ci arriveremo."),
 # ------------------------------------------------------------------ 2 · I PROTAGONISTI
 S(2, "Apriamo la bacheca dei protagonisti. Al centro c'è la biblioteca, con i suoi scaffali e le sue sale storiche. Intorno, le persone che entrano in questa storia."),
 S(2, "Il primo è Marino Massimo De Caro. Prima di arrivare a Napoli è un commerciante di libri antichi, legato a Verona. Ha anche un incarico al ministero, come consulente. Le sentenze lo hanno poi condannato in via definitiva."),
 S(2, "Il secondo è Tomaso Montanari, storico dell'arte e docente universitario. È lui, secondo tutte le ricostruzioni, il primo a raccontare pubblicamente cosa stava succedendo nella biblioteca."),
 S(2, "Poi ci sono i bibliotecari. Persone che lavorano lì ogni giorno, che vedono, e che a un certo punto raccontano agli investigatori quello che hanno visto. Le loro testimonianze saranno decisive."),
 S(2, "Ci sono i carabinieri e la procura di Napoli, che apriranno l'inchiesta e metteranno sotto sequestro l'intero complesso. E c'è una casa d'aste di Monaco di Baviera, dove una parte dei libri sta per essere venduta."),
 S(2, f"Infine c'è un personaggio lontano da Napoli: Nick {WIL}, studioso di storia del libro. Sarà lui a smascherare il falso Galileo."),
 S(2, "Una nota di metodo, come in ogni fascicolo. Ogni fatto che sentirete è confermato da almeno due fonti. Quando le fonti non coincidono, ve lo diciamo. E delle persone non condannate non facciamo il nome."),
 S(2, "Per questo non sentirete i nomi di altri imputati, di intermediari o di persone coinvolte in filoni diversi dell'inchiesta. Il nostro racconto si concentra sui fatti accertati e sulle condanne definitive."),
 S(2, "Primo riepilogo, per chi arriva adesso. Una biblioteca pubblica dal 1586, circa centosessantamila volumi, patrimonio dello Stato. Un nuovo direttore che viene dal commercio di libri antichi. E una domanda: che cosa succede quando chi custodisce è anche chi vende?"),
 # ------------------------------------------------------------------ 3 · IL NUOVO DIRETTORE
 S(3, "Come arriva un commerciante di libri antichi a dirigere una biblioteca di stato? Facciamo un passo indietro, alla primavera del 2011."),
 S(3, "De Caro in quel periodo è consulente del ministro allora in carica. Nella primavera del 2011 riceve un incarico legato alla tutela del patrimonio librario. E nel giugno del 2011 diventa direttore della biblioteca dei Girolamini."),
 S(3, "Su quella nomina, più tardi, il giudice per le indagini preliminari scriverà parole durissime: secondo il giudice è avvenuta contro ogni regola, grazie all'influenza legata al suo ruolo di consigliere del ministro."),
 S(3, "Fermiamoci un attimo su questo punto. Di solito chi dirige una biblioteca pubblica è un funzionario, un bibliotecario di carriera, qualcuno che ha superato un concorso. Il direttore dei Girolamini arriva invece da un altro mondo: quello del commercio."),
 S(3, "Non è un dettaglio. Chi compra e vende libri antichi conosce il loro valore sul mercato, sa quali edizioni sono più ricercate, sa dove si vendono. È esattamente il tipo di conoscenza che, nelle mani sbagliate, diventa un rischio."),
 S(3, "C'è un altro elemento che le fonti sottolineano: lo stato della biblioteca. Un patrimonio enorme, ma un inventario difficile da ricostruire. Negli anni successivi, rifare i conti di quello che c'era si rivelerà un lavoro lunghissimo."),
 S(3, "E senza un inventario preciso, chi può dire con certezza che cosa manca? È una domanda che tornerà più volte in questo fascicolo, perché ancora oggi non esiste un numero unico dei libri portati via."),
 S(3, "Il nuovo direttore, dunque, prende le chiavi a giugno del 2011. Nel giro di pochi giorni, secondo le ricostruzioni, la biblioteca cambia volto."),
 # ------------------------------------------------------------------ 4 · LE NOTTI DEI GIROLAMINI
 S(4, "Eccoci al cuore del caso. Che cosa succede ai Girolamini tra l'estate del 2011 e la primavera del 2012? Le fonti concordano su un punto: in quei mesi una grande quantità di libri lascia la biblioteca."),
 S(4, "I bibliotecari raccontano di aver assistito a ripetuti prelievi, anche di notte. Altre testimonianze parlano di furgoni carichi che uscivano dai cortili a tarda sera. Scatole, casse, pacchi di volumi."),
 S(4, "Secondo le ricostruzioni, anche le telecamere di sorveglianza avrebbero ripreso il direttore mentre portava via scatole di libri. Saranno, insieme alle testimonianze, tra gli elementi raccolti dagli investigatori."),
 S(4, "Quali libri? Non volumi qualsiasi. Le fonti parlano di edizioni rare del Cinquecento e del Seicento, opere di scienza e di astronomia, prime edizioni di autori come Galileo, Copernico e Keplero."),
 S(4, "E nelle sale, intanto, la biblioteca cambia aspetto. Chi la visita in quei mesi trova libri ammucchiati sul pavimento, scaffali in disordine, sale polverose. Un'immagine lontanissima da quella di una biblioteca storica."),
 S(4, "Facciamo un conto. Le stime più citate parlano di oltre duemila volumi portati via in circa un anno. Duemila diviso trecentosessantacinque fa più di cinque libri al giorno. Ogni giorno, per un anno."),
 S(4, "E ricordiamo che non stiamo parlando di romanzi da edicola. Un singolo libro antico raro può valere migliaia, a volte centinaia di migliaia di euro. Il danno non si misura solo in numero di volumi."),
 S(4, "C'è anche un altro dettaglio importante. Ogni libro di una biblioteca storica porta dei segni: timbri, numeri di collocazione, note di possesso. Sono la carta d'identità del volume. E sono proprio questi segni che, più avanti, tradiranno i libri rubati."),
 S(4, "Secondo un avviso della casa d'aste che vedremo tra poco, su molti volumi finiti in vendita quei segni di provenienza erano stati rimossi in fretta e in modo maldestro. Ma un segno cancellato, per un esperto, è a sua volta un segnale."),
 S(4, "Dove vanno i libri? Una parte resta in Italia, in depositi nel Veronese. Un'altra parte prende la strada dell'estero: Germania, Regno Unito e non solo. Ma per ora nessuno, fuori dalla biblioteca, sa niente."),
 S(4, "Secondo riepilogo, per chi si è appena collegato. Napoli, biblioteca dei Girolamini, aperta al pubblico dal 1586. A giugno 2011 arriva un nuovo direttore. In pochi mesi migliaia di libri antichi spariscono dagli scaffali."),
 # ------------------------------------------------------------------ 5 · LA DENUNCIA
 S(5, "Arriviamo all'inizio del 2012. Tomaso Montanari visita la biblioteca. Quello che vede non gli piace: libri a terra, disordine, sale trascurate."),
 S(5, "E chi lavora lì gli racconta qualcosa di molto grave: i libri stanno uscendo dalla biblioteca, e a portarli via sarebbe il direttore. Montanari decide di scriverne."),
 S(5, "A metà aprile del 2012 il suo articolo esce sui giornali. Descrive una biblioteca polverosa e disordinata, i libri sul pavimento, e i movimenti sospetti nei cortili di sera. È la prima volta che la storia diventa pubblica."),
 S(5, "Intorno all'articolo nasce una petizione di intellettuali e studiosi, che chiede al ministro di rimuovere il direttore. Le firme raccolte sono circa duemila."),
 S(5, "La reazione è rapidissima. Nello stesso periodo si parla di circa millecinquecento volumi mancanti. La procura di Napoli si muove, e ad aprile i carabinieri mettono sotto sequestro la biblioteca. Il direttore viene allontanato dall'incarico."),
 S(5, "Fermiamoci su questa sequenza, perché è velocissima. Un articolo, una petizione, il sequestro: tutto nel giro di pochi giorni. Dopo mesi in cui nessuno aveva fermato niente, ora la macchina si mette in moto."),
 S(5, "Un sequestro significa che nessuno può più entrare o portare via nulla senza l'autorizzazione dei magistrati. La biblioteca, aperta al pubblico da più di quattro secoli, chiude. E resterà chiusa molto, molto a lungo."),
 S(5, "Ma a questo punto un problema resta. Mettere i sigilli alle porte serve a proteggere quello che c'è ancora. Non riporta indietro quello che è già uscito. E una parte dei libri, in quei giorni, sta per essere venduta."),
 S(5, "A circa metà del nostro viaggio, se questo fascicolo ti sta piacendo, iscriviti a Fascicolo Italia: ogni giorno un nuovo caso, raccontato con le fonti."),
 # ------------------------------------------------------------------ 6 · L'INDAGINE E L'ASTA DI MONACO
 S(6, "Inizia l'indagine. Gli investigatori devono rispondere a tre domande: quali libri mancano, dove sono finiti, e chi li ha portati via. Nessuna delle tre è semplice."),
 S(6, f"La prima risposta arriva da Monaco di Baviera. Lì una casa d'aste specializzata in libri antichi, la {ZIS}, ha in programma una grande vendita dal nove all'undici maggio del 2012."),
 S(6, "Nel catalogo compaiono centinaia di libri antichi. Esperti del settore notano qualcosa che non torna: segni che riportano ai Girolamini. La segnalazione arriva alle autorità."),
 S(6, "La sera dell'otto maggio, la vigilia dell'asta, le autorità tedesche avvertono la casa d'aste che alcuni libri saranno sequestrati. La vendita di quei lotti viene fermata. Per un soffio."),
 S(6, "Quanti libri c'erano? Qui le fonti non coincidono: si va da oltre quattrocento a circa cinquecento, fino a più di seicento libri e manoscritti secondo altre ricostruzioni. In ogni caso, centinaia."),
 S(6, "Facciamo un conto sui tempi. Dal sequestro della biblioteca, ad aprile, all'asta di Monaco, a maggio, passano poche settimane. Se l'articolo fosse uscito un mese dopo, quei libri sarebbero stati dispersi tra decine di acquirenti."),
 S(6, "Intanto l'indagine in Italia va avanti. Sempre a maggio, in provincia di Verona, vengono trovati depositi di libri antichi. Dentro ci sono volumi con il timbro dei Girolamini."),
 S(6, "Sul numero dei libri trovati nel Veronese le fonti danno cifre diverse: alcune parlano di circa duecentoquaranta volumi della biblioteca, altre di un migliaio di libri, di cui alcune centinaia con il timbro. Il dato certo è che il filo porta a Verona."),
 S(6, "A questo punto l'inchiesta si allarga. Gli investigatori seguono i libri attraverso i passaggi di mano, tra intermediari, librerie e case d'aste, in Italia e all'estero. Un lavoro lungo, fatto di cataloghi, timbri e confronti."),
 S(6, "Anche il titolare della casa d'aste di Monaco finirà nell'inchiesta: nell'agosto del 2013 viene arrestato in Germania su mandato d'arresto europeo. Sugli esiti del suo processo le fonti non coincidono, e per questo non ne facciamo il nome."),
 # ------------------------------------------------------------------ 7 · L'ARRESTO E IL FALSO GALILEO
 S(7, "Torniamo a Napoli, a maggio del 2012. La procura chiede e ottiene l'arresto del direttore. Marino Massimo De Caro viene arrestato insieme ad alcuni collaboratori. L'accusa principale è peculato."),
 S(7, "Che cos'è il peculato? È il reato del pubblico ufficiale che si appropria di beni che ha in custodia per il suo ruolo. Non un furto da estraneo, ma l'appropriazione da parte di chi doveva custodire. Esattamente il caso di un direttore con i libri della sua biblioteca."),
 S(7, "A giugno le accuse si allargano: oltre al peculato, gli investigatori ipotizzano un'associazione per delinquere. Il percorso dei libri va da Napoli a Verona, e da lì verso l'estero."),
 S(7, "E poi arriva la confessione. Negli interrogatori De Caro ammette di aver portato via i libri. Lo dicono le fonti dell'epoca, che però descrivono un racconto pieno di zone d'ombra."),
 S(7, f"Ed è qui che il caso dei Girolamini incrocia un'altra storia, nata anni prima e lontano da Napoli. Una storia che riguarda Galileo Galilei, e un suo libro famosissimo: il {SN}."),
 S(7, f"Il {SN}, cioè il messaggero delle stelle, esce a Venezia nel marzo del 1610. Sono poche pagine in latino. Galileo vi racconta quello che ha visto con il cannocchiale che si è costruito da solo."),
 S(7, "È una rivoluzione. La Luna non è liscia e perfetta: ha montagne, valli e crateri. La Via Lattea è fatta di innumerevoli stelle. E intorno a Giove girano quattro satelliti, che Galileo chiama astri medicei."),
 S(7, "La prima tiratura è di cinquecentocinquanta copie. Oggi ne sopravvivono circa centocinquanta. Per un collezionista è uno dei libri più desiderati della storia della scienza."),
 S(7, f"Ora, immaginate una copia mai vista prima: con la firma di Galileo e, al posto delle incisioni della Luna, degli acquerelli. Come se Galileo avesse dipinto la Luna di sua mano."),
 S(7, f"Questa copia compare sul mercato. Nel 2005 viene venduta a un libraio antiquario di {NY} per circa mezzo milione di dollari. Tra i venditori, secondo le ricostruzioni, c'è proprio De Caro."),
 S(7, "Il libro viene studiato a lungo da un gruppo di esperti, che lo considerano autentico. Nel 2011 gli vengono dedicati due volumi di studi. Per molti è la scoperta del secolo."),
 S(7, f"Ma Nick {WIL} non è convinto, e decide di verificare. Confronta il libro con altre copie e con le riproduzioni moderne. E trova la prova decisiva: un piccolo segno sul frontespizio."),
 S(7, "Quel segno, secondo le sue ricerche, non viene dal Seicento. Corrisponde a una macchiolina presente in un facsimile stampato nel 1964. Un difetto di una riproduzione moderna, finito dentro un libro che doveva avere quattro secoli."),
 S(7, f"In altre parole: il libro di {NY} era stato fabbricato copiando un facsimile del Novecento. Non era un originale ritoccato, era un falso costruito da zero. Nel 2012 la notizia esce, e nel 2014 gli stessi studiosi che lo avevano esaminato pubblicano un volume che lo dichiara falso."),
 S(7, "E De Caro? Secondo lo studioso, ammette di aver fatto realizzare altre copie false. Su quante fossero le fonti non coincidono. Il quadro però è chiaro: il direttore dei Girolamini era legato anche a un giro di falsi."),
 S(7, "Perché un falso è così utile a chi ruba libri? Secondo la ricostruzione di alcuni studiosi, una copia falsa può prendere il posto di un originale sullo scaffale. E finché nessuno controlla, nessuno se ne accorge."),
 S(7, f"Terzo riepilogo prima dei processi. Il direttore è arrestato e confessa. L'accusa principale è peculato. E la sua figura si lega anche a un falso Galileo, venduto a {NY} e creduto autentico per anni da studiosi di tutto il mondo."),
 # ------------------------------------------------------------------ 8 · I PROCESSI
 S(8, "Arriviamo ai processi. La vicenda giudiziaria dei Girolamini è lunga e si divide in più filoni. Noi ci fermiamo su quello che risulta con certezza dalle fonti."),
 S(8, "Il primo processo per De Caro si celebra con il rito abbreviato, una procedura che si basa sugli atti delle indagini e che prevede uno sconto di pena. A marzo del 2013 arriva la sentenza di primo grado."),
 S(8, "La condanna è a sette anni di reclusione per peculato, con l'interdizione perpetua dai pubblici uffici. Vuol dire che non potrà più ricoprire alcun incarico pubblico. Nello stesso procedimento vengono condannati anche alcuni collaboratori."),
 S(8, "Poi i gradi successivi. La condanna a sette anni per peculato diventa definitiva: le fonti la danno come definitiva entro il 2015. È la parte della storia su cui non ci sono più dubbi."),
 S(8, "De Caro sconta la pena in detenzione domiciliare, cioè a casa e non in cella. Le fonti non indicano con precisione le date di questo passaggio."),
 S(8, "Accanto al processo penale c'è la Corte dei conti, il giudice che si occupa dei danni causati alle casse e ai beni dello Stato. Per il danno alla biblioteca stabilisce un risarcimento di quasi venti milioni di euro."),
 S(8, "Facciamo un conto. Venti milioni di euro diviso duemila libri fa circa diecimila euro a volume. È solo una media, perché alcuni libri valgono molto di più e altri molto meno. Ma dà l'ordine di grandezza del danno."),
 S(8, "Ci sono poi altri filoni, aperti negli anni successivi, sull'ipotesi di un'associazione per delinquere e su altre persone coinvolte. Su questi esiti le cronache riportano cifre e decisioni diverse, e per questo non entriamo nei dettagli."),
 S(8, "Una cosa va detta chiaramente: tra le persone indagate negli anni ce ne sono state alcune poi assolte. Chi non è stato condannato in via definitiva, in questo fascicolo, non viene indicato come colpevole."),
 S(8, f"Quarto riepilogo. Primavera 2012: l'articolo, la petizione, il sequestro. Maggio: l'asta di Monaco fermata la sera prima e l'arresto del direttore. Marzo 2013: sette anni per peculato, poi definitivi. E in mezzo, un falso Galileo venduto a {NY}."),
 # ------------------------------------------------------------------ 9 · DOVE SONO FINITI I LIBRI
 S(9, "Ora la domanda più importante: dove sono finiti i libri? La risposta è un lungo lavoro di recupero, durato anni, e non ancora concluso."),
 S(9, "Il caso di Monaco è il più spettacolare. Dopo anni di procedure, nel febbraio del 2015 le autorità tedesche restituiscono all'Italia i libri sequestrati alla casa d'aste. Sono circa cinquecento volumi."),
 S(9, "Anche qui le fonti danno numeri leggermente diversi: circa cinquecento libri per un valore di oltre due milioni di euro secondo alcune, cinquecentoquarantatré libri per due milioni e mezzo secondo altre. Tra loro, prime edizioni di Galileo, Copernico e Keplero."),
 S(9, "Altri libri tornano dall'Italia, dal Veronese, e da altri paesi. Nel 2013 si parlava di circa duemilasettecento volumi recuperati. Nel 2015 le cronache parlavano di circa quattromila. Le cifre cambiano a seconda delle fonti e del momento."),
 S(9, "E quanti erano in tutto i libri sottratti? Anche qui, nessun numero unico. Nel 2012 si parlava di millecinquecento volumi mancanti, poi di oltre duemila, e altre stime arrivano fino a quattromila. Un'associazione internazionale di librai antiquari ha scritto che non si sapeva nemmeno quanti fossero davvero."),
 S(9, "Il motivo lo abbiamo già visto: senza un inventario aggiornato, sapere che cosa manca è difficilissimo. E rifare l'inventario di centosessantamila volumi richiede anni."),
 S(9, "Il caso non tocca solo Napoli. Anche l'abbazia di Montecassino ha denunciato la sparizione di libri antichi nel 2011. Secondo le ricostruzioni, De Caro si presentava come studioso e consulente del ministero, mentre qualcuno distraeva i monaci."),
 S(9, "E la biblioteca? Resta sotto sequestro e chiusa al pubblico per anni. Una biblioteca aperta dal 1586, chiusa per oltre un decennio a causa di chi doveva dirigerla."),
 S(9, "La riapertura arriva solo il 22 aprile del 2026, dopo circa quattordici anni. Le sale storiche, compresa la sala Vico, tornano visitabili, con una mostra dedicata alla biblioteca di un nobile del Rinascimento meridionale, Andrea Matteo terzo Acquaviva."),
 S(9, "Facciamo l'ultimo conto. Dal sequestro della primavera 2012 alla riapertura dell'aprile 2026 passano quattordici anni. Quasi il doppio dei sette anni di condanna inflitti al direttore."),
 # ------------------------------------------------------------------ 10 · LE DOMANDE APERTE
 S(10, "Restano diverse domande aperte. La prima: quanti libri sono stati portati via, davvero? Abbiamo visto stime da millecinquecento a quattromila. Senza un inventario precedente affidabile, il numero esatto potrebbe non essere mai noto."),
 S(10, "La seconda: quanti mancano ancora? Una parte dei volumi è tornata, ma molti risultano ancora dispersi in collezioni private, in Italia e all'estero. Ogni tanto un libro riemerge da un catalogo e torna a casa."),
 S(10, "La terza: come è stato possibile? Un uomo senza la carriera tipica di un bibliotecario arriva a dirigere una biblioteca di Stato. Per mesi nessun controllo interno lo ferma. A fermarlo è un articolo di giornale."),
 S(10, "La quarta riguarda il falso Galileo. Quante copie false sono state fatte, e dove sono? Le fonti parlano di numeri diversi. Qualche falso potrebbe essere ancora in circolazione, magari al posto di un originale."),
 S(10, "La quinta riguarda i filoni secondari: le decisioni su altri imputati e altre accuse sono arrivate a distanza di anni, con esiti che le cronache riportano in modo non sempre coincidente. Per questo ci siamo fermati alle condanne certe."),
 S(10, "E infine una domanda più grande: quante altre biblioteche, archivi e abbazie hanno inventari incompleti? Il caso dei Girolamini è diventato un esempio studiato proprio per questo."),
 # ------------------------------------------------------------------ 11 · LA LEZIONE
 S(11, "Che cosa ci insegna questa storia? Ecco cinque idee, per chi ama i libri, per chi li compra e per chi lavora nei luoghi della cultura."),
 S(11, "Primo: i timbri contano. Un libro antico con il timbro di una biblioteca pubblica, o con un timbro cancellato, è un campanello d'allarme. Chi compra deve chiedere da dove viene, e farsi mostrare i documenti."),
 S(11, "Secondo: l'inventario è la prima difesa. Una biblioteca che sa esattamente che cosa possiede si accorge subito di un vuoto. Una biblioteca senza inventario aggiornato può perdere libri per mesi senza saperlo."),
 S(11, "Terzo: i controlli non devono dipendere da una sola persona. Ai Girolamini il direttore aveva le chiavi di tutto. Più persone che verificano, registri dei prestiti e delle uscite, telecamere controllate da altri: sono regole semplici, ma funzionano."),
 S(11, "Quarto: chi vede, parli. In questa storia sono stati decisivi i bibliotecari che hanno raccontato e uno studioso che ha scritto. In Italia esiste un reparto dei carabinieri dedicato alla tutela del patrimonio culturale, a cui si può segnalare un'opera sospetta."),
 S(11, "Quinto: anche gli esperti possono sbagliare. Il falso Galileo ha ingannato specialisti per anni. Un documento troppo bello, una scoperta troppo sensazionale, meritano sempre un controllo in più."),
 # ------------------------------------------------------------------ IL VERDETTO
 S(12, "Ricapitoliamo il fascicolo. Uno: la biblioteca dei Girolamini, a Napoli, è aperta al pubblico dal 1586 e custodisce circa centosessantamila volumi."),
 S(12, "Due: a giugno del 2011 ne diventa direttore Marino Massimo De Caro, commerciante di libri antichi e consulente del ministero. Tre: in circa un anno migliaia di volumi lasciano la biblioteca, anche di notte."),
 S(12, "Quattro: nella primavera del 2012 un articolo di Tomaso Montanari fa scoppiare il caso. Seguono il sequestro, l'asta di Monaco fermata la sera prima e l'arresto. Cinque: De Caro confessa ed è condannato in via definitiva a sette anni per peculato."),
 S(12, f"Sei: il falso Galileo venduto a {NY} viene smascherato. E la biblioteca riapre solo nel 2026, dopo quattordici anni. Molti libri sono tornati, altri mancano ancora."),
 S(12, "E tu che ne pensi? Come si protegge un patrimonio così grande? Scrivilo nei commenti."),
 S(12, "Iscriviti a Fascicolo Italia: ogni giorno un nuovo caso."),
]

SCENES = [p for _, p in SCENES_H]
HEADERS = [CH[h] for h, _ in SCENES_H]

def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
