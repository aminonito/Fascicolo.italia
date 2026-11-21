STYLE = "fascicolo"
CASE = "FASCICOLO N. 019 · IL CRATERE DI EUFRONIO"
TITLE = "Il cratere di Eufronio"
CH = ["INTRO", "1 · CERVETERI E IL VASO", "2 · I PROTAGONISTI", "3 · COME FUNZIONA IL TRAFFICO", "4 · IL VIAGGIO DEL VASO",
      "5 · IL MUSEO E I GIORNALI", "6 · LA STORIA DEL LIBANO", "7 · LA SVOLTA DI GINEVRA", "8 · I PROCESSI", "9 · IL RITORNO",
      "10 · LE DOMANDE APERTE", "11 · LA LEZIONE", "IL VERDETTO"]
import re

def S(ch, text):
    """divide il testo in frasi (punto, punto di domanda, due punti) senza toccare le parentesi [display|parlato]"""
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

NY = "[New York|Niù Iork]"
NYT = "[New York Times|Niù Iork Taims]"
MET = "[Metropolitan|Metropòlitan]"
HE = "[Hecht|Ecc]"
SA = "[Sarrafian|Sarrafiàn]"
POL = "[Polaroid|pòlaroid]"

SCENES_H = [
 # ------------------------------------------------------------------ INTRO
 S(0, f"Novembre [1972.|millenovecentosettantadue.] Il {MET} Museum di {NY} presenta il suo nuovo capolavoro: un vaso greco di duemilacinquecento anni fa, pagato un milione di dollari. Un prezzo record."),
 S(0, f"Il museo dice che viene da una vecchia collezione di famiglia in Libano. Ma meno di un anno prima, secondo le ricostruzioni giudiziarie, quel vaso era sottoterra, in una tomba etrusca vicino a Cerveteri, a nord di Roma."),
 S(0, "Lo avevano scavato di nascosto i tombaroli. Ci vorranno più di trent'anni, un incidente stradale, un magazzino a Ginevra pieno di fotografie e un lungo processo per riportarlo a casa."),
 S(0, "In questo fascicolo vedremo cos'è il cratere di Eufronio, chi lo ha venduto e a quanto, come è arrivato a New York, la svolta di Ginevra, cosa hanno deciso i giudici, e perché oggi il vaso si trova di nuovo a pochi chilometri dalla sua tomba."),
 # ------------------------------------------------------------------ 1 · CERVETERI E IL VASO
 S(1, "Partiamo dal luogo. Cerveteri si trova sulla costa del Lazio, a nord di Roma. Nell'antichità era una delle grandi città degli Etruschi, il popolo che abitava l'Italia centrale prima dell'espansione di Roma."),
 S(1, "Gli Etruschi seppellivano i loro morti in vere e proprie città dei morti: le necropoli. Tombe scavate nella roccia o coperte da grandi tumuli di terra, con dentro gli oggetti che accompagnavano il defunto."),
 S(1, "Tra questi oggetti ci sono spesso vasi greci. Gli Etruschi erano ricchi e li importavano da Atene: erano oggetti di lusso, da esibire a banchetto e poi da portare con sé nella tomba."),
 S(1, "Per questo il sottosuolo di Cerveteri è da secoli una specie di cassaforte. E per questo, nel Novecento, attira chi scava di nascosto per vendere ciò che trova. In Italia li chiamano tombaroli."),
 S(1, "Teniamo a mente una regola: in Italia i reperti archeologici che si trovano nel sottosuolo appartengono allo Stato. Scavare di nascosto e vendere ciò che si trova è un reato. Ed esportarlo senza autorizzazione è un altro reato."),
 S(1, "Ora il vaso. Si chiama cratere: un grande recipiente in cui i Greci mescolavano il vino con l'acqua durante il simposio, il banchetto degli uomini. Questo è un cratere a calice, a figure rosse."),
 S(1, "A figure rosse vuol dire che le figure hanno il colore naturale dell'argilla, arancione, mentre lo sfondo è dipinto di nero. Una tecnica nata ad Atene alla fine del sesto secolo avanti Cristo."),
 S(1, "Il cratere è stato realizzato ad Atene intorno al [515|cinquecentoquindici] avanti Cristo. È alto circa quarantasei centimetri e largo circa cinquantacinque. Le misure variano di poco tra le fonti."),
 S(1, "Porta due firme. Quella del vasaio, [Euxitheos,|Eussìteos,] che lo ha modellato. E quella del pittore, Eufronio, uno dei più celebri pittori di vasi della Grecia antica. È da lui che prende il nome."),
 S(1, "Su un lato c'è una scena dell'Iliade: il corpo dell'eroe Sarpedonte, figlio di Zeus, viene portato via da due figure alate, il Sonno e la Morte, [Hypnos|Ìpnos] e [Thanatos,|Tànatos,] sotto lo sguardo del dio [Hermes.|Èrmes.]"),
 S(1, "Sull'altro lato ci sono giovani ateniesi che si armano per la battaglia. Per gli studiosi è uno dei vasi greci più belli che si conoscano: per questo è spesso chiamato anche cratere di Sarpedonte."),
 S(1, "Facciamo un piccolo conto. Dal [515|cinquecentoquindici] avanti Cristo al [1971|millenovecentosettantuno] passano circa duemilaquattrocentottantacinque anni. Quasi tutti passati sottoterra, nel buio di una tomba etrusca."),
 S(1, "Un vaso greco in una tomba etrusca non è una stranezza: è il segno di un commercio antico tra Atene e l'Etruria. Ed è anche il dettaglio che, secoli dopo, aiuterà a capire da dove arrivava davvero."),
 # ------------------------------------------------------------------ 2 · I PROTAGONISTI
 S(2, "Apriamo la bacheca dei protagonisti. Come sempre, diciamo solo ciò che risulta dai documenti e dalle sentenze, e distinguiamo con attenzione chi è stato condannato da chi non lo è stato."),
 S(2, "Al primo posto ci sono i tombaroli. Nelle ricostruzioni sono uomini del posto, che conoscono le campagne di Cerveteri. Non faremo nomi: nessuno di loro, per questo vaso, è stato condannato in un processo di cui abbiamo traccia certa."),
 S(2, "Poi c'è Giacomo Medici. È un mercante d'arte antica romano, attivo a Roma dagli anni Sessanta. Più tardi lavorerà anche in Svizzera, a Ginevra. Lo ritroveremo al centro di tutta la storia."),
 S(2, "Lo diciamo subito, perché è un fatto: Giacomo Medici è stato condannato in via definitiva. La Corte di cassazione ha respinto il suo ricorso nel dicembre [2011.|duemilaundici.] Vedremo per quali reati."),
 S(2, f"Terzo nome: Robert {HE}. È un mercante americano di antichità, che vive in Europa e conosce i grandi musei. È lui a proporre il cratere al {MET}. Morirà nel [2012,|duemiladodici,] a novantadue anni."),
 S(2, f"Su {HE} bisogna essere precisi: è stato processato a Roma, ma il processo si è chiuso per prescrizione. Quindi non è mai stato condannato per questa vicenda."),
 S(2, f"Quarto nome: Dikran {SA}. È un mercante libanese che vive a Beirut. Secondo i documenti presentati al museo, il vaso apparteneva alla sua famiglia da decenni. Morirà in un incidente stradale nel [1977.|millenovecentosettantasette.]"),
 S(2, f"Poi ci sono gli uomini del museo. Dietrich [von Bothmer|fon Bòtmer] è il curatore dell'arte greca e romana del {MET}. Thomas [Hoving|Hòving] è il direttore. Sono loro a volere il vaso per New York."),
 S(2, f"Più avanti arriverà un altro direttore, [Philippe|Filìp] de Montebello. Toccherà a lui, molti anni dopo, firmare l'accordo con l'Italia."),
 S(2, "Infine, dall'altra parte, gli investigatori. I carabinieri del nucleo per la tutela del patrimonio culturale, e un magistrato della procura di Roma, Paolo Giorgio Ferri, che dedicherà anni alla caccia dei reperti trafugati."),
 S(2, "Riepilogo della bacheca: i tombaroli che scavano. Il mercante romano che compra. Il mercante americano che rivende. Il collezionista libanese che fornisce la storia. Il museo che compra. E lo Stato italiano che, più tardi, indaga."),
 # ------------------------------------------------------------------ 3 · COME FUNZIONA IL TRAFFICO
 S(3, "Prima di seguire il vaso, capiamo come funziona questo tipo di traffico. Non serve sapere come si scava: serve capire come un oggetto passa dalla terra di un campo alla vetrina di un museo."),
 S(3, "Gli studiosi lo descrivono come una catena. Al primo anello ci sono i tombaroli. Poi uno o più intermediari locali. Poi un mercante con contatti all'estero. E infine i compratori: collezionisti, case d'asta, musei."),
 S(3, "A ogni passaggio il prezzo sale. E a ogni passaggio l'oggetto perde un pezzo della sua storia vera: il luogo esatto in cui è stato trovato, la tomba, gli altri oggetti che aveva accanto."),
 S(3, "Per un archeologo quella è la perdita più grave. Un vaso staccato dal suo contesto è ancora bello, ma racconta molto meno. Non sappiamo più chi era sepolto lì, con quali altri oggetti, in che epoca."),
 S(3, "Il secondo passaggio chiave è la Svizzera. Per molti anni, secondo le inchieste, il Paese è stato un luogo di transito per le antichità, con regole meno severe di quelle italiane sull'importazione e il commercio."),
 S(3, "C'è poi il porto franco di Ginevra: grandi magazzini doganali in cui le merci possono restare a lungo in deposito. Lo ritroveremo più avanti, perché sarà il luogo della svolta."),
 S(3, "L'ultimo passaggio è il più delicato: la provenienza. Per vendere un pezzo a un grande museo serve una storia che dica da dove arriva. Per esempio, una vecchia collezione privata formata prima delle leggi di tutela."),
 S(3, "Se la storia è vera, l'acquisto è lecito. Se è inventata, il museo compra senza saperlo, o senza volerlo sapere, un oggetto scavato di nascosto. Tenete a mente questa parola: provenienza. È il cuore di tutto il caso."),
 S(3, "Lo vedremo anche nelle fotografie trovate anni dopo a Ginevra: pezzi ancora sporchi di terra, poi restaurati, poi esposti in un museo. La catena, fotografata anello per anello."),
 # ------------------------------------------------------------------ 4 · IL VIAGGIO DEL VASO
 S(4, "Ora seguiamo il viaggio del vaso, tappa per tappa. Partiamo dalla data. Secondo gli atti dei processi italiani, lo scavo avviene nel dicembre [1971,|millenovecentosettantuno,] in una zona chiamata Greppe Sant'Angelo, vicino a Cerveteri."),
 S(4, "Le fonti specificano che il punto esatto e la prima parte del viaggio non sono mai stati stabiliti con certezza. Si parla di una tomba etrusca della necropoli. È la ricostruzione generalmente accettata."),
 S(4, "Il vaso non esce intero. Esce in frammenti, ma completo: tutti i pezzi ci sono, e un restauratore esperto può rimetterli insieme. È un dettaglio che conta, perché tornerà nella storia del Libano."),
 S(4, "Prima tappa: dai tombaroli al mercante. Secondo le ricostruzioni, i tombaroli vendono il vaso a Giacomo Medici per una cifra intorno agli ottantottomila dollari."),
 S(4, "Seconda tappa: la Svizzera. Medici, secondo le stesse ricostruzioni, fa uscire il vaso dall'Italia e lo porta in Svizzera. Lì lo vende a Robert [Hecht|Ecc] per trecentocinquantamila dollari."),
 S(4, f"Terza tappa: il restauro. {HE} affida i frammenti a un restauratore di Zurigo. Il vaso viene ricomposto. Intanto, nel febbraio [1972,|millenovecentosettantadue,] {HE} scrive a [von Bothmer,|fon Bòtmer,] il curatore del {MET}, per proporlo."),
 S(4, "Nel giugno [1972|millenovecentosettantadue] [von Bothmer|fon Bòtmer] e il direttore [Hoving|Hòving] vanno a Zurigo a vederlo. L'accordo arriva in agosto, dopo una trattativa: un milione di dollari. Una fonte indica un milione e duecentomila."),
 S(4, f"Quarta tappa: l'oceano. Il cratere arriva negli Stati Uniti il [31|trentuno] agosto [1972.|millenovecentosettantadue.] Ha attraversato l'oceano: il {MET} ha il suo vaso."),
 S(4, "Facciamo i conti. Ottantottomila dollari ai tombaroli. Trecentocinquantamila al primo mercante. Un milione pagato dal museo. Tra il primo e l'ultimo passaggio il prezzo si moltiplica per più di undici."),
 S(4, "Dalla tomba al museo passano circa nove mesi. Da dicembre a fine agosto. Nove mesi per attraversare due confini, un oceano, un restauro, e diventare un pezzo con una storia nuova."),
 S(4, "Fermiamoci per un primo riepilogo. Un vaso greco di circa duemilacinquecento anni fa. Una tomba etrusca a Cerveteri. Dicembre [1971.|millenovecentosettantuno.] Poi il mercante romano, la Svizzera, il mercante americano, il restauro, e infine New York. Un milione di dollari."),
 # ------------------------------------------------------------------ 5 · IL MUSEO E I GIORNALI
 S(5, f"Il {MET} presenta l'acquisto al pubblico nel novembre [1972.|millenovecentosettantadue.] Il [12|dodici] novembre il cratere è sulla copertina del magazine domenicale del {NYT}. Un grande evento culturale."),
 S(5, "In quel primo momento il museo non dice né il prezzo né la provenienza. Secondo le fonti, la spiegazione è proteggere un canale da cui sperava di comprare altro in futuro."),
 S(5, "Un milione di dollari, per l'epoca, è una cifra enorme. Le fonti lo descrivono come il prezzo più alto mai pagato fino ad allora dal museo per un'opera d'arte, e un record per un'antichità."),
 S(5, "Proprio il silenzio sulla provenienza incuriosisce i giornalisti. Un vaso quasi perfetto, di cui nessuno aveva sentito parlare, compare all'improvviso sul mercato. Da dove arriva?"),
 S(5, f"Nel febbraio [1973|millenovecentosettantatré] il {NYT} pubblica una serie di articoli. Gli articoli mettono in dubbio la versione del museo e scrivono che il vaso potrebbe essere stato scavato illegalmente a Cerveteri alla fine del [1971.|millenovecentosettantuno.]"),
 S(5, f"Escono i nomi: Robert {HE}, Dikran {SA}. Ed esce anche la cifra, il milione di dollari. Il caso diventa pubblico, su entrambe le sponde dell'oceano."),
 S(5, f"Il vaso si guadagna un soprannome che lo accompagnerà per decenni: in inglese, hot pot. Vaso che scotta. Ancora oggi, nei libri e negli articoli in inglese, il caso è ricordato così."),
 S(5, "Anche in Italia la notizia arriva. Ma, almeno per quanto riportano le fonti consultate, non c'è ancora una prova capace di collegare quel vaso a una tomba precisa e a persone precise."),
 S(5, "È la prima lezione del caso: un sospetto, anche forte, non basta. Per riportare indietro un'opera servono documenti, testimoni, e la possibilità di ricostruire la catena. Ci vorranno più di vent'anni."),
 # ------------------------------------------------------------------ 6 · LA STORIA DEL LIBANO
 S(6, f"Vediamo allora la versione ufficiale, quella del Libano. Secondo {HE}, il vaso non viene da un campo di Cerveteri. Viene dalla collezione di Dikran {SA}, a Beirut."),
 S(6, f"{HE} dice di agire come agente di {SA}, con una commissione del dieci per cento. E presenta due lettere."),
 S(6, f"La prima è datata [10|dieci] luglio [1971.|millenovecentosettantuno.] È di {SA} a {HE}, e dice che il vaso può essere consegnato per un prezzo finale di un milione di dollari. Notate la data: cinque mesi prima del presunto scavo."),
 S(6, f"La seconda lettera è del settembre [1972.|millenovecentosettantadue.] {SA} scrive che il padre aveva ottenuto il vaso nel [1920,|millenovecentoventi,] e che era in frammenti. Lo aveva mandato in Svizzera per il restauro qualche anno prima."),
 S(6, "Il museo prova a verificare. Secondo le fonti, alcuni legali del museo vanno a Beirut a incontrare il collezionista. E raccolgono documenti e testimonianze."),
 S(6, f"Tra queste: un pagamento in franchi svizzeri a {SA} nell'ottobre [1971,|millenovecentosettantuno,] pari a circa novecentonovemila dollari. E un impiegato che dice di aver visto un vaso in frammenti a Beirut, nei primi anni Sessanta."),
 S(6, "Con questi elementi il museo difende il suo acquisto. Per il museo, la storia del Libano regge. Per i critici, invece, ci sono troppe coincidenze e troppe cose che non tornano."),
 S(6, f"Nel [1977|millenovecentosettantasette] Dikran {SA} muore in un incidente stradale. Con lui scompare il testimone principale della versione libanese. Nessuno potrà più interrogarlo."),
 S(6, "E così il vaso resta a New York. Per anni, nelle sale del museo, è uno dei pezzi più ammirati. Per l'Italia, invece, resta un sospetto senza prove sufficienti."),
 S(6, "Un'osservazione: in questa fase nessun tribunale ha ancora detto niente. Abbiamo una versione del museo, documentata, e un'inchiesta giornalistica che la contesta. La risposta arriverà da un luogo inaspettato."),
 # ------------------------------------------------------------------ 7 · LA SVOLTA DI GINEVRA
 S(7, "Passano più di vent'anni. Agosto [1995.|millenovecentonovantacinque.] Su una strada a sud di Roma, in direzione di Napoli, un'auto esce di strada. Il conducente muore. Si chiama Pasquale Camera."),
 S(7, "Le fonti lo descrivono come un ex appartenente alle forze dell'ordine entrato nel giro delle antichità. Sulla sua professione precedente e sul luogo esatto dell'incidente le versioni non coincidono del tutto."),
 S(7, "Dopo la sua morte, le indagini portano a un documento che diventerà famoso: un organigramma scritto a mano. Uno schema con i nomi delle persone del commercio di antichità, e i loro collegamenti."),
 S(7, f"Secondo le ricostruzioni, lo schema è attribuito a Camera, e mostra Giacomo Medici in una posizione centrale nel commercio di antichità uscite dall'Italia. Sul luogo in cui fu trovato, le fonti divergono."),
 S(7, "L'organigramma porta gli investigatori a Ginevra. Qui Medici ha un deposito nel porto franco, attraverso una società. Il [13|tredici] settembre [1995|millenovecentonovantacinque] i carabinieri, insieme alle autorità svizzere, entrano in quel magazzino."),
 S(7, "Il magazzino si trova in un grande edificio doganale. Per gli investigatori, aprire quelle stanze significa vedere per la prima volta l'interno della catena, non solo i suoi due estremi: la tomba e il museo."),
 S(7, "Dentro ci sono migliaia di oggetti antichi: vasi, affreschi, statue, frammenti. Alcuni sono ancora incrostati di terra. Le fonti parlano di migliaia di pezzi, molti provenienti dall'Italia."),
 S(7, f"Ma la vera scoperta sono le fotografie. Migliaia di immagini, soprattutto {POL}, archiviate in album e buste. Le fonti indicano numeri diversi, tra tremilaseicento e oltre quattromila."),
 S(7, f"Le {POL} raccontano una sequenza. Prima: oggetti sporchi e rotti, fotografati appena usciti dalla terra, a volte in un campo, in un cortile, sul retro di un furgone."),
 S(7, "Poi: gli stessi oggetti in fase di restauro, con le giunture ancora visibili. Poi: restaurati e perfetti. E infine: esposti in un museo o pubblicati nel catalogo di una grande casa d'asta."),
 S(7, f"Una di queste foto è particolarmente importante. Ritrae Giacomo Medici accanto al cratere di Eufronio, esposto al {MET} di New York. Un legame visivo tra il mercante romano e il vaso."),
 S(7, "Ci sono anche documenti: lettere, fatture, ricevute, appunti sulle vendite. Per gli investigatori sono la mappa di un commercio che va dai campi italiani ai musei di mezzo mondo."),
 S(7, f"Giacomo Medici ha sempre contestato questa lettura. In una lettera del [1998|millenovecentonovantotto] alla rivista americana Archaeology sostiene che la perquisizione è stata brusca, che non è stato fatto subito un inventario, e che gli oggetti avevano origine lecita."),
 S(7, "Contesta anche i numeri. Per lui, gli oggetti erano molti meno di quanto scritto dai giornali: qualche centinaio. Lo segnaliamo perché è la sua versione. I giudici, come vedremo, arriveranno a conclusioni diverse."),
 S(7, f"Le indagini proseguono. Nel febbraio [2001|duemilauno] i carabinieri perquisiscono l'appartamento parigino di Robert {HE}. Trovano un memoriale scritto a mano, in cui la storia del cratere è raccontata in due versioni che non coincidono."),
 S(7, "Secondo riepilogo, per chi arriva adesso. Il vaso è al museo di New York dal [1972.|millenovecentosettantadue.] Nel [1995|millenovecentonovantacinque] un incidente stradale porta a un organigramma, e l'organigramma porta a un magazzino di Ginevra pieno di oggetti e di fotografie."),
 S(7, "Se questa storia ti sta piacendo, iscriviti a Fascicolo Italia: ogni giorno un nuovo caso, raccontato con le fonti."),
 # ------------------------------------------------------------------ 8 · I PROCESSI
 S(8, "Arriviamo in aula. Il processo principale riguarda Giacomo Medici, a Roma. È un processo contro un mercante accusato di aver organizzato l'uscita dall'Italia di reperti scavati di nascosto."),
 S(8, "Tra le accuse, secondo le fonti: associazione per delinquere, ricettazione, ed esportazione illecita di beni archeologici."),
 S(8, "La sentenza di primo grado arriva tra la fine del [2004|duemilaquattro] e il [2005:|duemilacinque:] sulla data esatta le fonti non coincidono. La pena è di dieci anni di reclusione."),
 S(8, "A questa si aggiunge una somma di dieci milioni di euro a favore dello Stato italiano, a risarcimento del danno al patrimonio culturale. Le fonti descrivono questa cifra in modi diversi, come multa o come risarcimento."),
 S(8, "Negli atti del processo, tra gli oggetti trafficati, compare anche il cratere di Eufronio. È da qui che arriva la ricostruzione dello scavo del dicembre [1971.|millenovecentosettantuno.]"),
 S(8, "Medici fa appello. Il [15|quindici] luglio [2009|duemilanove] la Corte d'appello di Roma decide. Per alcuni reati, come l'esportazione illecita, è passato troppo tempo: scatta la prescrizione."),
 S(8, "Ma la ricettazione e l'associazione per delinquere vengono confermate. La pena scende da dieci a otto anni di reclusione. La somma di dieci milioni di euro resta."),
 S(8, "Ultimo grado: la Corte di cassazione. Nel dicembre [2011|duemilaundici] i giudici respingono il ricorso di Medici. La condanna diventa definitiva."),
 S(8, "Facciamo un conto sui tempi. Dalla perquisizione di Ginevra, nel [1995,|millenovecentonovantacinque,] alla sentenza definitiva, nel [2011,|duemilaundici,] passano circa sedici anni. Dallo scavo del vaso, ne passano quaranta."),
 S(8, f"E gli altri? A Roma, a partire dal [2005,|duemilacinque,] sono processati anche Robert {HE} e un'ex curatrice delle antichità del [Getty|Ghetti] Museum, in California. Un processo lungo, con molte udienze."),
 S(8, "Per l'ex curatrice, nel [2010|duemiladieci] il processo si chiude per prescrizione. Non è mai stata condannata. Lo diciamo chiaramente, perché è un punto importante."),
 S(8, f"Per {HE}, il processo si chiude per prescrizione nel gennaio [2012.|duemiladodici.] Poche settimane dopo, nel febbraio [2012,|duemiladodici,] muore a novantadue anni. Anche lui non è mai stato condannato per questa vicenda."),
 S(8, "Questa è una parte del caso che resta divisa. Da un lato una condanna definitiva per il mercante romano. Dall'altro, processi che finiscono senza una sentenza di merito, perché il tempo è scaduto."),
 S(8, "E i tombaroli dello scavo del [1971?|millenovecentosettantuno?] Nelle fonti consultate non c'è traccia di una condanna specifica per il cratere. Per questo non faremo nomi."),
 # ------------------------------------------------------------------ 9 · IL RITORNO
 S(9, "Mentre i processi vanno avanti, qualcosa si muove anche fuori dalle aule. Le prove di Ginevra, le fotografie e le sentenze mettono sotto pressione i musei che avevano comprato pezzi di quella catena."),
 S(9, f"Il [3|tre] febbraio [2006|duemilasei] il {MET} firma un accordo con l'Italia. Il museo restituisce una ventina di oggetti. Tra questi c'è il cratere di Eufronio."),
 S(9, f"Il direttore di allora, [Philippe|Filìp] de Montebello, dichiara secondo le fonti che è altamente probabile che il vaso sia stato sottratto da una tomba etrusca. Per il museo è un'ammissione importante."),
 S(9, "L'accordo prevede tempi precisi: il cratere resta a New York ancora per un po'. Il [18|diciotto] gennaio [2008|duemilaotto] è a Roma, presentato nella mostra Nostoi, capolavori ritrovati. Nostoi, in greco, vuol dire ritorni."),
 S(9, "Facciamo il conto. Dall'arrivo a New York, nell'agosto [1972,|millenovecentosettantadue,] al ritorno in Italia, nel gennaio [2008,|duemilaotto,] passano più di trentacinque anni."),
 S(9, f"Il {MET} non è l'unico. Secondo le fonti, tra il [2006|duemilasei] e il [2009|duemilanove] restituiscono oggetti all'Italia anche il Museum of Fine Arts di Boston, il [Getty|Ghetti] Museum, il museo di Cleveland e altre istituzioni americane."),
 S(9, "Anche la Svizzera cambia. Dopo lo scandalo, il Paese approva una legge sul trasferimento dei beni culturali, e i depositi nei porti franchi diventano più controllati, con inventari e dichiarazioni di origine."),
 S(9, "Dopo la mostra, il cratere viene esposto a Roma, al Museo nazionale etrusco di Villa Giulia. Ci resta per alcuni anni, fino al [2014.|duemilaquattordici.]"),
 S(9, "Nel [2014|duemilaquattordici] arriva una scelta simbolica: il vaso viene portato in prestito temporaneo al Museo nazionale cerite di Cerveteri, a pochi chilometri dalla necropoli in cui era stato scavato."),
 S(9, "Accanto al cratere viene esposta un'altra opera tornata dall'America: una coppa attribuita al pittore [Onesimos,|Onèsimos,] restituita dal [Getty|Ghetti] Museum alla fine degli anni Novanta."),
 S(9, "Nel novembre [2015|duemilaquindici] il ministro della Cultura Dario Franceschini annuncia che il trasferimento diventa definitivo: il cratere e la coppa resteranno a Cerveteri."),
 S(9, "Il vaso, dopo duemilacinquecento anni, un viaggio in Svizzera, più di trent'anni a New York e qualche anno a Roma, è tornato vicino alla sua terra. Non nella tomba: in un museo pubblico, dove tutti possono vederlo."),
 S(9, "Terzo riepilogo. [2006:|duemilasei:] l'accordo con il museo di New York. [2008:|duemilaotto:] il ritorno a Roma. [2011:|duemilaundici:] la condanna definitiva del mercante. [2015:|duemilaquindici:] il cratere resta a Cerveteri."),
 # ------------------------------------------------------------------ 10 · LE DOMANDE APERTE
 S(10, "Arriviamo alle domande aperte. Perché anche in un caso chiuso da una sentenza definitiva restano punti in cui le versioni non coincidono."),
 S(10, "Prima domanda: il luogo esatto. Le fonti parlano di Greppe Sant'Angelo, vicino a Cerveteri, e lo dicono gli atti dei processi italiani. Ma sottolineano anche che il punto preciso dello scavo non è mai stato stabilito con certezza."),
 S(10, "Seconda domanda: il prezzo. Quasi tutte le fonti indicano un milione di dollari. Una indica un milione e duecentomila, con la data del [10|dieci] novembre [1972.|millenovecentosettantadue.] Le cifre intermedie, ottantottomila e trecentocinquantamila, vengono dalle ricostruzioni giornalistiche e giudiziarie."),
 S(10, f"Terza domanda: le prove della versione libanese. Il pagamento in franchi svizzeri e la testimonianza dei frammenti visti a Beirut esistono nei documenti del museo. Allora a che cosa si riferivano? Le fonti non danno una risposta concorde."),
 S(10, "Quarta domanda: i numeri di Ginevra. Le fonti parlano di migliaia di oggetti. Medici, nella sua lettera, parla di qualche centinaio. Le fotografie vengono contate in modi diversi."),
 S(10, "Quinta domanda: l'organigramma. Tutti concordano sulla sua importanza. Ma sul luogo esatto in cui fu trovato e sull'esatto ordine degli eventi del [1995,|millenovecentonovantacinque,] le ricostruzioni non sono identiche."),
 S(10, "Sesta domanda, la più ampia: quanti altri oggetti, passati per la stessa catena, sono ancora nelle collezioni del mondo senza che se ne conosca l'origine? Le restituzioni continuano ancora oggi."),
 S(10, "E un'ultima domanda, che riguarda tutti noi: quanto abbiamo perso? Di quella tomba di Cerveteri non sapremo mai tutto. Il vaso è tornato. Il suo contesto, cioè la storia di chi era sepolto lì, è perso per sempre."),
 # ------------------------------------------------------------------ 11 · LA LEZIONE
 S(11, "Che cosa ci insegna questa storia, oggi? Non serve essere collezionisti o direttori di museo. Bastano poche abitudini, se ci capita di trovare o di comprare qualcosa di antico."),
 S(11, "Primo: la provenienza. Un oggetto archeologico serio ha una storia documentata: da dove viene, chi l'ha posseduto, quando è uscito dal suo Paese. Se la storia manca, o è vaga, è un campanello d'allarme."),
 S(11, "Secondo: i documenti di esportazione. Per far uscire legalmente dall'Italia un bene culturale servono autorizzazioni. Un oggetto senza carte non dovrebbe passare un confine."),
 S(11, "Terzo: se trovi qualcosa. In Italia i reperti trovati nel sottosuolo appartengono allo Stato, e chi trova qualcosa per caso deve avvisare le autorità. Tenerlo, o venderlo, è un reato."),
 S(11, "Quarto: il mercato online. Monete, frammenti, piccoli vasi venduti senza storia sono spesso l'ultimo anello di una catena che parte da uno scavo illegale. Il prezzo basso non è un affare: è un indizio."),
 S(11, "Quinto: segnalare. In Italia esiste un reparto dei carabinieri dedicato proprio alla tutela del patrimonio culturale, con una banca dati dei beni rubati. Le segnalazioni dei cittadini contano."),
 S(11, "E un'ultima cosa, che vale anche per i musei: comprare un capolavoro senza chiedersi da dove arriva significa finanziare chi scava di nascosto. Il cratere di Eufronio lo ha dimostrato."),
 # ------------------------------------------------------------------ IL VERDETTO
 S(12, "Ricapitoliamo il fascicolo. Uno: il cratere di Eufronio è un vaso greco dipinto ad Atene intorno al [515|cinquecentoquindici] avanti Cristo, finito in una tomba etrusca vicino a Cerveteri."),
 S(12, f"Due: secondo le ricostruzioni giudiziarie, nel dicembre [1971|millenovecentosettantuno] i tombaroli lo scavano di nascosto. Passa al mercante Giacomo Medici, poi in Svizzera a Robert {HE}, e nel [1972|millenovecentosettantadue] il {MET} lo compra per un milione di dollari."),
 S(12, f"Tre: la storia della collezione libanese regge per più di vent'anni. Quattro: nel [1995|millenovecentonovantacinque] un organigramma porta al magazzino di Ginevra, con migliaia di oggetti e di {POL}."),
 S(12, f"Cinque: nel [2011|duemilaundici] Giacomo Medici è condannato in via definitiva. Per {HE} e per l'ex curatrice del [Getty|Ghetti] i processi si chiudono per prescrizione. Sei: dal [2008|duemilaotto] il vaso è in Italia, e dal [2015|duemilaquindici] resta a Cerveteri."),
 S(12, "E tu, secondo te, un museo dovrebbe restituire sempre un'opera scavata di nascosto, anche dopo decenni? Scrivilo nei commenti. Le fonti sono tutte nella descrizione."),
 S(12, "Iscriviti a Fascicolo Italia: ogni giorno un nuovo caso."),
]
SCENES = [s for h, s in SCENES_H]
HEADERS = [CH[h] for h, s in SCENES_H]

def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
