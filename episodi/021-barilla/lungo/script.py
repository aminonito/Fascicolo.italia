STYLE = "fascicolo"
CASE = "FASCICOLO N. 021 · L'UOMO SBAGLIATO"
TITLE = "L'uomo sbagliato"
CH = ["INTRO", "1 · MILANO, FEBBRAIO 1992", "2 · I PROTAGONISTI", "3 · L'OPERAZIONE", "4 · LA SERA DEL 13 FEBBRAIO",
      "5 · LE PRIME ORE", "6 · LE ACCUSE E I PROCESSI", "7 · GLI ANNI IN CELLA", "8 · LA SVOLTA", "9 · LA REVISIONE",
      "10 · IL RISARCIMENTO E IL DOPO", "11 · LE DOMANDE APERTE", "12 · LA LEZIONE", "IL VERDETTO"]
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

ROS = "[ROS|ros]"
G27 = "[2.700|duemilasettecento]"

SCENES_H = [
 # ------------------------------------------------------------------ INTRO
 S(0, "13 febbraio 1992, la sera prima di San Valentino. In Brianza, a nord di Milano, un piccolo imprenditore sale sulla sua auto per raggiungere la fidanzata. È una Fiat Tipo rosso amaranto."),
 S(0, "Quella sera non arriverà all'appuntamento. Viene fermato dai carabinieri e arrestato. Per gli investigatori è un trafficante di cocaina. Lui dice che è un errore. Ha ragione, ma per dimostrarlo ci vorranno anni."),
 S(0, "Sette anni e mezzo di carcere, una condanna definitiva, poi la revisione e l'assoluzione: non ha commesso il fatto. In questo fascicolo vedremo come si arriva a scambiare un uomo per un altro, e come si torna indietro."),
 S(0, "Questo è il caso di Daniele Barillà. Per tutti, da un certo punto in poi, diventa l'uomo sbagliato."),
 # ------------------------------------------------------------------ 1 · MILANO, FEBBRAIO 1992
 S(1, "Partiamo dal luogo e dal momento. Febbraio 1992. L'Italia usa ancora la lira, i telefoni cellulari sono rari e costosi, e per seguire un'auto servono uomini, macchine e radio."),
 S(1, "Milano è la capitale economica del paese. Intorno alla città, verso nord, c'è la Brianza: una zona fitta di paesi, capannoni e piccole aziende, spesso a conduzione familiare."),
 S(1, "Le strade che collegano tutto questo sono le tangenziali e le statali. Di sera sono piene di auto che si somigliano. E all'inizio degli anni Novanta un modello si vede ovunque: la Fiat Tipo."),
 S(1, "La Tipo è una berlina compatta a due volumi, uscita alla fine degli anni Ottanta. È un'auto comune, prodotta in grandi numeri. Due Tipo dello stesso colore, di notte, sono quasi impossibili da distinguere."),
 S(1, "Non è un'auto qualunque: nel 1989 la Tipo era stata eletta auto europea dell'anno. In pochi anni diventa una presenza fissa sulle strade italiane, nei parcheggi delle aziende e sotto le case. Proprio per questo, vederne una non fa notizia."),
 S(1, "C'è poi un dettaglio di calendario. Pochi giorni dopo l'arresto di cui parliamo, il 17 febbraio 1992, a Milano viene arrestato un amministratore pubblico, Mario Chiesa. È l'inizio dell'inchiesta Mani Pulite."),
 S(1, "Per mesi i giornali e la procura di Milano saranno assorbiti da quella inchiesta. La storia di Daniele Barillà comincia proprio in quei giorni, e per anni resterà lontana dalle prime pagine."),
 S(1, "Un'ultima cosa sul contesto. In quegli anni il traffico di cocaina verso l'Europa cresce, e le forze dell'ordine lavorano con reparti specializzati, infiltrati e informatori. È un lavoro difficile, che vive di pedinamenti e di riconoscimenti a vista."),
 S(1, "Ed è proprio un riconoscimento a vista il punto debole di questa storia. Teniamolo a mente: tornerà più volte."),
 # ------------------------------------------------------------------ 2 · I PROTAGONISTI
 S(2, "Apriamo la bacheca del fascicolo. Il primo nome è il suo: Daniele Barillà. Al momento dell'arresto ha circa trent'anni."),
 S(2, "È un piccolo imprenditore della zona di Nova Milanese, in Brianza. Lavora nel materiale elettrico: secondo le ricostruzioni assembla cavi, e la sua azienda dà lavoro a una quindicina di persone."),
 S(2, "Ha una fidanzata, una famiglia, un'attività avviata. Niente, nelle fonti che abbiamo consultato, lo collega al traffico di droga prima di quella sera."),
 S(2, "Il secondo elemento della bacheca è un reparto: il [ROS|ros] dei carabinieri, il raggruppamento operativo speciale. L'operazione di quella sera è condotta da uomini del [ROS|ros] di Genova."),
 S(2, "Il [ROS|ros] è un reparto giovane: nasce alla fine del 1990 per le indagini sulla criminalità organizzata e sul terrorismo. Lavora con tecniche investigative speciali, come le operazioni sotto copertura e la gestione di informatori."),
 S(2, "A guidarla è un ufficiale del reparto. Il suo nome compare in molte fonti, ma non lo useremo: come vedremo, anni dopo sarà accusato per i suoi metodi di lavoro, in vicende diverse da questa."),
 S(2, "Il terzo elemento sono i trafficanti, quelli veri. Le fonti parlano di un carico di cocaina e di uomini che riescono a fuggire. Ma nessun nome è confermato da due fonti, quindi sulla bacheca resta una sagoma."),
 S(2, "Il quarto elemento sono i giudici: quelli che lo condannano, e quelli che anni dopo lo assolvono. In mezzo c'è un sistema, quello della giustizia penale, con i suoi tre gradi di giudizio."),
 S(2, "Infine, ci sono le persone che non si arrendono. Un avvocato, un giornalista che scriverà un libro sul caso, e lo stesso Barillà, che per tutto il tempo continuerà a dirsi innocente."),
 S(2, "Una nota di metodo, come sempre. In questo fascicolo usiamo solo fatti riportati da almeno due fonti indipendenti. Dove le fonti non coincidono, lo diciamo. E alcuni dettagli, anche noti, restano fuori perché ne abbiamo trovata una sola."),
 # ------------------------------------------------------------------ 3 · L'OPERAZIONE
 S(3, "Come nasce quella sera? Dall'altra parte della storia c'è un'indagine sul traffico di cocaina. Il [ROS|ros] di Genova segue da tempo un gruppo di trafficanti e prepara un'operazione."),
 S(3, "Secondo le ricostruzioni, il carico è grande: cinquanta chili di cocaina. Viaggia su un'auto, una Fiat Uno, diretta proprio verso la zona di Nova Milanese."),
 S(3, "Nell'operazione compare anche un'altra auto, guidata da un uomo del gruppo. È una Fiat Tipo rosso amaranto. È l'auto che i carabinieri tengono d'occhio."),
 S(3, "Per seguirla serve un pedinamento: auto civetta, uomini in borghese, comunicazioni via radio. Chi pedina deve restare a distanza per non farsi notare. E più si sta lontani, più è facile perdere di vista l'obiettivo."),
 S(3, "Un pedinamento di sera ha un problema in più. Le luci dei fari abbagliano, i colori si confondono, le targhe si leggono a fatica. Di un'auto restano la forma e il colore."),
 S(3, "Ora mettiamo insieme i pezzi. Un'auto da seguire: una Fiat Tipo rosso amaranto. Una zona: Nova Milanese e la tangenziale. Una sera: il 13 febbraio. E, nella stessa zona, un'altra Fiat Tipo dello stesso colore."),
 S(3, "Le due auto non sono solo dello stesso modello e dello stesso colore. Secondo le fonti, anche le targhe si somigliano: alcune ricostruzioni parlano di targhe quasi identiche, altre di tre cifre in comune."),
 S(3, "Facciamo un piccolo calcolo per capire quanto è raro. Le targhe di allora avevano la sigla della provincia e una serie di cifre e lettere. Che due auto uguali, dello stesso colore, con targhe simili, siano nello stesso posto alla stessa ora è una coincidenza rarissima."),
 S(3, "Ma le coincidenze rare, in un paese con milioni di auto, prima o poi succedono. E quella sera succede."),
 # ------------------------------------------------------------------ 4 · LA SERA DEL 13 FEBBRAIO
 S(4, "Giovedì 13 febbraio 1992. È sera. Daniele Barillà esce con la sua Fiat Tipo rosso amaranto. Deve raggiungere la fidanzata: l'indomani è San Valentino."),
 S(4, "Nella stessa zona, i carabinieri del [ROS|ros] stanno seguendo l'altra Tipo, quella del gruppo di trafficanti. La seguono a distanza, come si fa in un pedinamento."),
 S(4, "Qui le fonti diventano poche e precise solo su un punto. Non conosciamo gli orari, il percorso esatto, le strade imboccate. Quello che le fonti dicono, in modo concorde, è il risultato: gli investigatori scambiano l'auto di Barillà per quella che stavano seguendo."),
 S(4, "Per questo, nella nostra ricostruzione, la dinamica è solo uno schema. Immaginiamo la tangenziale vista dall'alto: l'auto pedinata davanti, i carabinieri dietro."),
 S(4, "A un certo punto l'auto pedinata esce dalla scena. Nella stessa corsia compare un'altra Tipo, identica. E chi insegue, ora, insegue lei."),
 S(4, "I veri trafficanti, secondo le fonti, riescono a fuggire. Daniele Barillà invece viene fermato. Per chi lo ferma è il pezzo mancante di un'operazione antidroga."),
 S(4, "Lui non capisce. Non sa niente di cocaina, di carichi, di pedinamenti. Dice che sta andando dalla fidanzata. Ma per chi lo ha fermato, quell'auto è la prova."),
 S(4, "Rivediamo lo schema una seconda volta, perché tutto il caso sta in questi pochi secondi. Un'auto esce, un'altra entra. Stesso modello, stesso colore, targa simile. Di sera."),
 S(4, "E c'è un elemento che pesa più dell'auto: il riconoscimento. Gli investigatori dicono di riconoscere in lui l'uomo che stavano seguendo. Su quel riconoscimento si costruirà l'accusa."),
 S(4, "Anni dopo, Barillà racconterà che proprio la testimonianza di chi lo arrestò fu decisiva contro di lui. È il suo punto di vista, ma i processi successivi gli daranno ragione su una cosa: quell'uomo non era lui."),
 # ------------------------------------------------------------------ 5 · LE PRIME ORE
 S(5, "Le prime ore dopo un arresto sono le più importanti. L'arrestato viene portato in caserma, poi in carcere, e un giudice deve convalidare l'arresto in tempi brevi."),
 S(5, "L'arresto di Daniele Barillà viene convalidato. Da quel momento non è più un uomo fermato per un controllo: è un indagato per traffico di stupefacenti, in carcere."),
 S(5, "Spieghiamo due parole che torneranno. La convalida è il controllo di un giudice sull'arresto. La custodia cautelare è la detenzione prima della sentenza: serve, ad esempio, quando c'è il rischio di fuga o di nuovi reati. Non è una condanna, ma si sconta in cella."),
 S(5, "I giornali raccontano il blitz. Lui viene presentato come un esponente di rilievo della malavita milanese. Qualcuno lo soprannomina l'Escobar della Brianza."),
 S(5, "Il soprannome dice molto. In pochi giorni un piccolo imprenditore sconosciuto diventa, sulla carta, un boss del narcotraffico. E l'immagine pubblica, una volta stampata, è difficile da cancellare."),
 S(5, "Fuori, intanto, la sua vita si ferma. L'azienda resta senza il titolare. I dipendenti, i clienti, i fornitori si trovano davanti a una notizia incomprensibile."),
 S(5, "Le fonti concordano su quello che perde negli anni successivi: l'azienda, la fidanzata, e il padre, che muore mentre lui è ancora in carcere. Secondo le ricostruzioni, di crepacuore."),
 S(5, "Barillà sceglie una linea che non cambierà più: si proclama innocente. Non cambia versione, non racconta una storia diversa. Ripete che quella sera era solo un uomo che andava dalla fidanzata."),
 S(5, "Facciamo il primo riepilogo, per chi entra adesso. Febbraio 1992: un imprenditore della Brianza con una Fiat Tipo rossa viene scambiato per un trafficante, seguito dai carabinieri con un'auto identica. Viene arrestato. Lui si dice innocente. Se questi fascicoli ti interessano, iscriviti al canale."),
 # ------------------------------------------------------------------ 6 · LE ACCUSE E I PROCESSI
 S(6, "Arriviamo al processo. L'accusa è traffico di stupefacenti, legato all'operazione sulla cocaina. Le prove principali sono l'auto e il riconoscimento degli investigatori."),
 S(6, "La difesa sostiene l'errore di persona. Ma contro di lui c'è la parola di chi conduceva l'operazione. E in un'aula di tribunale la testimonianza di un investigatore ha un peso molto forte."),
 S(6, "Il primo grado si chiude con una condanna pesantissima: diciotto anni di carcere."),
 S(6, "Diciotto anni. Per capire quanto sono, facciamo un conto: se li avesse scontati tutti, sarebbe uscito nel 2010, a quasi cinquant'anni."),
 S(6, "Poi c'è l'appello. La pena viene ridotta: quindici anni. È ancora una condanna, e lui resta in carcere."),
 S(6, "Ricordiamo come funziona. In Italia un processo penale ha tre gradi: il primo, l'appello, che riesamina i fatti, e la Cassazione, che controlla solo l'applicazione della legge. Solo dopo l'ultimo grado una condanna diventa definitiva."),
 S(6, "Infine la Cassazione. La Corte suprema non riesamina i fatti, ma controlla che la legge sia stata applicata correttamente. Conferma. La condanna diventa definitiva."),
 S(6, "A questo punto, per lo Stato, la questione è chiusa. Daniele Barillà è un trafficante di droga condannato con sentenza definitiva a quindici anni."),
 S(6, "C'è un paradosso, in questa fase, che le fonti raccontano in modo concorde. Il suo continuo dirsi innocente viene letto contro di lui. Per il carcere è un detenuto che non si è ravveduto."),
 S(6, "Chi non ammette la colpa, infatti, viene considerato da alcuni come un criminale che non ha cambiato idea. E questo gli costa anche il diniego di alcuni benefici previsti per i detenuti."),
 S(6, "È il cuore drammatico degli errori giudiziari. Per l'innocente, l'unica verità possibile è dirsi innocente. Ma una volta condannato, quella stessa frase può sembrare il segno di una colpa."),
 # ------------------------------------------------------------------ 7 · GLI ANNI IN CELLA
 S(7, "Entriamo negli anni del carcere. Daniele Barillà ne trascorre la maggior parte nel carcere di Bergamo."),
 S(7, "Il calendario corre: 1992, 1993, 1994. Fuori, l'Italia cambia governi, sistema politico, moneta in arrivo. Dentro, i giorni sono tutti uguali."),
 S(7, "Mettiamo i numeri su un muro. Tra l'arresto e l'uscita passeranno circa sette anni e mezzo: oltre [2.700|duemilasettecento] giorni."),
 S(7, "Proviamo a tradurre quei giorni in tappe. Quando entra in carcere, la lira è ancora l'unica moneta. Quando esce, l'euro è già stato introdotto sui mercati finanziari, il primo gennaio 1999. Le monete e le banconote arriveranno nel 2002."),
 S(7, "Le fonti, sul conto esatto, non coincidono: c'è chi scrive sette anni, cinque mesi e venticinque giorni, chi dieci giorni in meno, chi arrotonda a quasi otto anni. Ma l'ordine di grandezza è lo stesso."),
 S(7, "In cella Barillà non smette di cercare una via d'uscita legale. Scrive, chiede, si rivolge a chiunque possa riaprire il caso."),
 S(7, "Secondo le ricostruzioni, a interessarsi alla sua vicenda è anche il procuratore capo di Milano dell'epoca, Francesco Saverio Borrelli, il magistrato simbolo di Mani Pulite."),
 S(7, "Anche un giornalista segue la storia: Stefano Zurlo, cronista giudiziario de Il Giornale. Sarà lui, anni dopo, a scrivere il libro sul caso."),
 S(7, "Ma per riaprire una condanna definitiva non bastano le convinzioni, né le firme importanti. Serve un fatto nuovo. E quel fatto arriva da una direzione inattesa."),
 S(7, "Secondo riepilogo. Arrestato nel febbraio 1992, Barillà è condannato a diciotto anni in primo grado, quindici in appello, condanna confermata in Cassazione. Sconta la pena soprattutto a Bergamo, continuando a dirsi innocente."),
 # ------------------------------------------------------------------ 8 · LA SVOLTA
 S(8, "La svolta arriva nel 1997, e non riguarda Barillà. Riguarda chi lo aveva arrestato."),
 S(8, "Quell'anno viene arrestato l'ufficiale del [ROS|ros] che aveva guidato l'operazione. È accusato di metodi illeciti nella gestione degli informatori: secondo l'accusa, anche pagandoli o gestendoli con droga sequestrata."),
 S(8, "Attenzione a un punto. Le accuse a quell'ufficiale riguardano i suoi metodi e altre operazioni. Nessuna sentenza, tra quelle che abbiamo trovato, lo dichiara responsabile dell'arresto di Barillà."),
 S(8, "Nel processo di Genova sui metodi del reparto, l'ufficiale sarà condannato in primo grado nel 2007 a circa nove anni e mezzo, ridotti in appello a quattro anni e mezzo. L'esito definitivo non siamo riusciti a confermarlo con due fonti."),
 S(8, "Ma per Barillà conta un'altra cosa. Se l'operazione di quella sera era guidata da chi ora è accusato di metodi illeciti, allora anche quelle carte meritano di essere riaperte."),
 S(8, "Il caso torna così sui tavoli dei magistrati. Le dichiarazioni, i riconoscimenti, la ricostruzione di quella sera vengono riletti con occhi diversi."),
 S(8, "Ora che sappiamo come va a finire, è facile dire che l'errore era evidente. Ma per sette anni, tre gradi di giudizio lo avevano considerato colpevole. Ci vuole un evento esterno per incrinare quella certezza."),
 S(8, "Ed è anche una lezione sulla fiducia. Il sistema si era fidato della parola degli investigatori. Quando quella fiducia vacilla per altre ragioni, si apre una crepa anche nel caso di Barillà."),
 # ------------------------------------------------------------------ 9 · LA REVISIONE
 S(9, "Che cos'è la revisione? È lo strumento con cui la legge italiana permette di riaprire una condanna definitiva. Non è un quarto grado di giudizio: si può chiedere solo in casi precisi, ad esempio quando emergono prove nuove."),
 S(9, "La revisione si discute davanti a una corte d'appello. Nel caso di Barillà, la richiesta viene accolta dalla Corte d'appello di Genova."),
 S(9, "La legge elenca i casi in cui la revisione è possibile. Ad esempio quando i fatti della condanna sono inconciliabili con quelli di un'altra sentenza, quando emergono o si scoprono prove nuove, o quando si dimostra che la condanna si basa su atti falsi. Non basta dire che i giudici hanno sbagliato."),
 S(9, "Il 12 luglio 1999 Daniele Barillà esce dal carcere. Ha passato dentro circa sette anni e mezzo."),
 S(9, "Il processo di revisione si chiude con l'assoluzione per non aver commesso il fatto. Su questo passaggio le fonti non sono del tutto allineate: per la maggior parte l'assoluzione definitiva arriva il 17 luglio 2000; per una fonte tutto si chiude già nel luglio 1999."),
 S(9, "Per non aver commesso il fatto è la formula più piena. Non significa che le prove non bastavano. Significa che quell'uomo, con quel traffico, non c'entrava."),
 S(9, "Il soprannome di qualche anno prima, l'Escobar della Brianza, si rovescia. Sui giornali ora diventa l'uomo sbagliato."),
 S(9, "Dopo l'assoluzione, secondo le cronache dell'epoca, Barillà annuncia che lascerà l'Italia. E qualche tempo dopo lo fa davvero: va a vivere all'estero."),
 S(9, "Facciamo un conto sui tempi. Dall'arresto all'uscita dal carcere: sette anni e cinque mesi circa. Dall'arresto all'assoluzione definitiva: più di otto anni. Dall'arresto del 1997 all'uscita: circa due anni."),
 S(9, "Terzo riepilogo. Nel 1997 l'ufficiale che aveva guidato l'operazione viene arrestato per altre vicende. Il caso si riapre: la Corte d'appello di Genova accoglie la revisione, Barillà esce il 12 luglio 1999 ed è assolto per non aver commesso il fatto."),
 # ------------------------------------------------------------------ 10 · IL RISARCIMENTO E IL DOPO
 S(10, "Chi viene assolto dopo una revisione ha diritto a una riparazione da parte dello Stato. Lo prevede l'articolo 643 del codice di procedura penale."),
 S(10, "La riparazione è commisurata alla durata della pena scontata e alle conseguenze personali e familiari della condanna. Può essere pagata in denaro, o come rendita vitalizia."),
 S(10, "C'è però un limite: la riparazione non spetta a chi ha causato l'errore con dolo o colpa grave, ad esempio accusandosi falsamente. Non è il caso di Barillà, che si è sempre detto innocente."),
 S(10, "Barillà, assistito dall'avvocato genovese Mauro Ferrando, chiede circa dodici miliardi di lire: oltre sei milioni di euro."),
 S(10, "Facciamo la conversione. Il cambio fisso tra lira ed euro è di [1.936,27|millenovecentotrentasei virgola ventisette] lire per un euro. Dodici miliardi di lire corrispondono quindi a circa sei milioni e duecentomila euro."),
 S(10, "Nel febbraio 2003 la Cassazione condanna lo Stato a pagare. Le cronache di allora parlano di circa quattro milioni di euro, otto miliardi di vecchie lire."),
 S(10, "Ma sulla cifra finale le fonti non coincidono. Gli articoli più recenti parlano di circa tre milioni di euro, liquidati nel 2007, più interessi e spese. La spiegazione più probabile è una battaglia sul calcolo durata anni, ma non abbiamo trovato due fonti che la confermino."),
 S(10, "Facciamo un conto prudente. Tra tre e quattro milioni di euro, divisi per circa [2.700|duemilasettecento] giorni di carcere, fanno tra mille e cento e mille e cinquecento euro per ogni giorno."),
 S(10, "Sembra tanto. Ma nessuna cifra restituisce un padre morto mentre il figlio era in cella, un'azienda chiusa, una relazione finita, gli anni tra i trenta e i quaranta passati in cella."),
 S(10, "Dopo, la storia diventa racconto. Stefano Zurlo scrive il libro L'uomo sbagliato. Il caso Barillà."),
 S(10, "E nel 2005 Rai 1 trasmette una fiction ispirata al caso, con lo stesso titolo, L'uomo sbagliato, interpretata da Beppe Fiorello."),
 S(10, "Barillà vive all'estero. Le fonti non concordano sul paese, e non lo indichiamo. Il suo nome però resta nelle cronache: ogni volta che in Italia si parla di errori giudiziari, il suo caso è tra i primi a essere citati."),
 S(10, "Spesso viene ricordato accanto a quello di Enzo Tortora, il presentatore arrestato nel 1983 e assolto nel 1987, di cui abbiamo parlato in un altro fascicolo. Due storie diverse, unite da una frase: arrestato al posto di un altro, o per le parole di altri."),
 S(10, "Il caso Tortora aveva già lasciato un segno nelle leggi: dopo il referendum del 1987 sulla responsabilità civile dei magistrati arriva la legge Vassalli, del 1988. Ma come mostra la storia di Barillà, una legge non basta a evitare che un errore accada."),
 # ------------------------------------------------------------------ 11 · LE DOMANDE APERTE
 S(11, "Restano domande aperte. La prima: che cosa è successo esattamente sulla strada, quella sera? Gli orari, il punto dello scambio, la distanza tra le auto: nessuna fonte che abbiamo trovato lo racconta in modo verificabile."),
 S(11, "La seconda: chi erano i veri trafficanti? Le fonti parlano di uomini fuggiti e di processi a parte, ma nessun nome è confermato da due fonti. Per questo non ne facciamo."),
 S(11, "La terza: come mai un riconoscimento sbagliato ha retto per tre gradi di giudizio? Le fonti indicano il peso dato alla parola degli investigatori. Ma i documenti completi dei processi non sono pubblici in rete."),
 S(11, "E ancora: perché il silenzio di un uomo che si dice innocente è stato letto come una prova del contrario? È una domanda che riguarda tutto il sistema, non solo questo caso. E non ha una risposta semplice."),
 S(11, "La quarta riguarda le date. Arresto il 13 febbraio per quasi tutte le fonti, l'undici per una. Uscita il 12 luglio 1999, assoluzione definitiva nel 2000 per la maggior parte delle fonti. Le piccole differenze sono normali in un caso vecchio di trent'anni."),
 S(11, "La quinta riguarda i soldi: quattro milioni nel 2003, tre milioni nel 2007. Due cifre, due momenti, e nessuna fonte che spieghi in modo chiaro il passaggio dall'una all'altra."),
 S(11, "La sesta riguarda le responsabilità. Chi ha sbagliato, quella sera, ne ha risposto? Nelle fonti che abbiamo consultato non abbiamo trovato esiti. E per quell'arresto, a quanto risulta, nessuno è stato condannato."),
 S(11, "Ed è giusto dirlo chiaramente: un errore giudiziario non è per forza un reato di qualcuno. Può nascere da una somma di sviste, coincidenze, fiducia mal riposta. Ed è proprio per questo che è così difficile da prevenire."),
 # ------------------------------------------------------------------ 12 · LA LEZIONE
 S(12, "Che cosa ci insegna oggi il caso Barillà? Partiamo dai numeri. Dal 1991 al 2022, in Italia, gli errori giudiziari riconosciuti dopo una revisione sono stati 222: circa sette all'anno."),
 S(12, "Per quei casi lo Stato ha pagato circa 86 milioni di euro di riparazioni: in media circa due milioni e settecentomila euro l'anno."),
 S(12, "Ogni riga di quella statistica è una persona come Daniele Barillà: qualcuno che è stato condannato in via definitiva, e poi riconosciuto innocente. Ma c'è un numero molto più grande: quello delle ingiuste detenzioni."),
 S(12, "L'ingiusta detenzione riguarda chi passa un periodo in custodia cautelare, in carcere o ai domiciliari, prima del processo, e poi viene assolto. Dal 1992 al 2022 i casi sono stati più di trentamila."),
 S(12, "Per le ingiuste detenzioni lo Stato ha pagato in trent'anni oltre ottocento milioni di euro. Sommando le due voci, il totale supera i novecentotrenta milioni."),
 S(12, "E nel solo 2022, i dati raccolti dall'associazione errorigiudiziari punto com e ripresi dai giornali contano otto errori giudiziari e oltre cinquecento casi di ingiusta detenzione."),
 S(12, "Ecco allora cinque idee da portare via, con una premessa: questo è un contenuto informativo, non una consulenza legale."),
 S(12, "Primo: la presunzione di innocenza. La Costituzione dice che l'imputato non è considerato colpevole fino alla condanna definitiva. Un arresto, un soprannome sui giornali, non sono una sentenza."),
 S(12, "Secondo: i riconoscimenti a vista possono sbagliare. Di sera, a distanza, sotto stress, il cervello completa quello che vede. Il caso Barillà nasce da un'auto e da un volto confusi con altri."),
 S(12, "Terzo: la revisione esiste. Anche una condanna definitiva può essere riaperta, se emergono fatti nuovi. È raro, è lungo, ma è possibile."),
 S(12, "Quarto: la riparazione esiste. Per l'errore giudiziario la legge non fissa un tetto. Per l'ingiusta detenzione il massimo è di circa cinquecentosedicimila euro, e la domanda va presentata alla corte d'appello entro due anni."),
 S(12, "Quinto: la cronaca ha un peso. I soprannomi e i titoli dei giornali restano anche quando le sentenze cambiano. Raccontare un arresto come una condanna è un errore che fa danni anche fuori dalle aule."),
 # ------------------------------------------------------------------ IL VERDETTO
 S(13, "Ricapitoliamo il fascicolo. Uno: il 13 febbraio 1992 Daniele Barillà, piccolo imprenditore della Brianza, viene arrestato mentre va dalla fidanzata con la sua Fiat Tipo rosso amaranto."),
 S(13, "Due: i carabinieri del [ROS|ros] stavano seguendo un trafficante con un'auto identica e una targa simile. Lo scambiano per lui. Tre: diciotto anni in primo grado, quindici in appello, condanna definitiva."),
 S(13, "Quattro: nel 1997 l'ufficiale che guidava l'operazione viene arrestato per i suoi metodi, in altre vicende, e il caso si riapre. Cinque: la Corte d'appello di Genova accoglie la revisione. Barillà esce il 12 luglio 1999 ed è assolto per non aver commesso il fatto."),
 S(13, "Sei: lo Stato lo risarcisce con una cifra tra tre e quattro milioni di euro. Ma i circa sette anni e mezzo di carcere non tornano."),
 S(13, "E tu che ne pensi? Un riconoscimento a vista dovrebbe bastare per condannare qualcuno? Scrivilo nei commenti."),
 S(13, "Iscriviti a Fascicolo Italia: ogni giorno un nuovo caso."),
]

SCENES = [p for _, p in SCENES_H]
HEADERS = [CH[h] for h, _ in SCENES_H]

def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
