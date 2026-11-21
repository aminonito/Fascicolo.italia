STYLE = "fascicolo"
CASE = "FASCICOLO N. 018 · IL VINO AL METANOLO"
TITLE = "Il vino al metanolo"
CH = ["INTRO", "1 · IL VINO DEGLI ITALIANI", "2 · I PROTAGONISTI", "3 · LA SCORCIATOIA", "4 · MARZO 1986",
      "5 · L'ALLARME", "6 · L'INDAGINE", "7 · LA SVOLTA", "8 · IL PROCESSO", "9 · DOPO LO SCANDALO",
      "10 · LE DOMANDE APERTE", "11 · LA LEZIONE", "IL VERDETTO"]
import re

def S(ch, text):
    """divide il testo in frasi (punto, punto di domanda, due punti) senza toccare le parentesi [display|parlato]"""
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

SCENES_H = [
 # ------------------------------------------------------------------ INTRO
 S(0, "Marzo [1986.|millenovecentoottantasei.] In Lombardia, in Piemonte e in Liguria alcune persone si sentono male dopo cena. Hanno bevuto un bicchiere di vino rosso da tavola, comprato al supermercato."),
 S(0, "Nelle settimane seguenti il bilancio diventa una delle pagine più dure della storia alimentare italiana: ventitré morti e centocinquantatré intossicati. Diverse persone perdono la vista."),
 S(0, "Nei bottiglioni c'è metanolo. Una sostanza che costava meno dello zucchero, e che qualcuno aggiungeva al vino per alzarne la gradazione. Non è un incidente: è una frode."),
 S(0, "Non ci sono casseforti, né rapine, né armi. C'è una filiera: una cantina, un imbottigliatore, dei camion, gli scaffali di un supermercato. E alla fine, la tavola di una famiglia."),
 S(0, "In questo fascicolo vedremo com'era il vino degli italiani negli anni Ottanta, perché il metanolo conveniva, come la procura di Milano ha risalito la catena, cosa hanno deciso i giudici, e perché quarant'anni dopo le vittime aspettano ancora un risarcimento."),
 # ------------------------------------------------------------------ 1 · IL VINO DEGLI ITALIANI
 S(1, "Partiamo da com'era l'Italia di metà anni Ottanta. Il vino non è ancora, per la maggior parte delle persone, un prodotto da degustare. È una bevanda di tutti i giorni, che sta sulla tavola come il pane."),
 S(1, "Le fonti descrivono un Paese che è soprattutto un grande produttore, consumatore ed esportatore di vino da tavola economico. Poca attenzione alla denominazione, molta attenzione al prezzo."),
 S(1, "Il formato simbolo di quegli anni è il bottiglione da due litri. Si compra al supermercato insieme alla spesa, spesso senza guardare chi lo ha prodotto o chi lo ha imbottigliato."),
 S(1, "Secondo il racconto di una delle famiglie colpite al quotidiano Il Giorno, un bottiglione di Barbera da due litri costava milleottocentonovanta lire. Con i coefficienti dell'ISTAT, oggi sarebbero meno di tre euro."),
 S(1, "Nel vino da tavola c'è una regola economica semplice: il prezzo dipende in buona parte dalla gradazione alcolica. Più gradi ha il vino, più vale. Un vino debole, a parità di litri, si vende peggio."),
 S(1, "Il modo naturale per avere più gradi è avere uva più matura e più zuccherina. Ma il clima cambia di anno in anno, e non tutte le partite raggiungono la gradazione che il mercato chiede."),
 S(1, "Una scorciatoia sarebbe aggiungere zucchero al mosto. Ma in Italia, dal [1965,|millenovecentosessantacinque,] aggiungere zucchero al vino è vietato. E lo zucchero, per di più, era gravato da un'imposta."),
 S(1, "Poi c'è il mercato estero. Nel [1985|millenovecentoottantacinque] le esportazioni italiane di vino crescono, secondo le fonti, del diciassette per cento in quantità e del venti per cento in valore. È un momento d'oro."),
 S(1, "Il vino italiano viaggia in cisterna e in bottiglia verso la Francia, la Germania Ovest, gli Stati Uniti. Ed è proprio questo successo che, poche settimane dopo, renderà il colpo ancora più pesante."),
 S(1, "Per capire cosa succede, però, dobbiamo fare un passo nella chimica. Perché la protagonista di questa storia non è una persona. È una molecola."),
 S(1, "Si chiama metanolo, o alcol metilico. La sua formula è semplice: un atomo di carbonio, quattro di idrogeno, uno di ossigeno. È un parente stretto dell'alcol del vino, l'etanolo."),
 S(1, "I due si assomigliano moltissimo: secondo le fonti hanno aspetto, odore e sapore molto simili. Chi beve un vino con troppo metanolo non se ne accorge. Ma il corpo sì: oltre certe quantità il metanolo è tossico."),
 S(1, "Una piccola quantità di metanolo si forma anche in modo naturale, durante la fermentazione dell'uva. Per questo la legge non lo vieta del tutto: fissa un limite massimo."),
 S(1, "Il limite, nel [1986,|millenovecentoottantasei,] è fissato da un decreto del [1965|millenovecentosessantacinque] sulle frodi nei vini: per i rossi, zero virgola tre millilitri ogni cento. Teniamo a mente questo numero: zero virgola tre."),
 S(1, "Il metanolo si usa nell'industria: come solvente, come combustibile, nella chimica. Non è fatto per essere bevuto. E nel vino, come vedremo, non doveva finire mai in quelle quantità."),
 # ------------------------------------------------------------------ 2 · I PROTAGONISTI
 S(2, "Apriamo la bacheca dei protagonisti. Al centro c'è una cantina di Narzole, un paese in provincia di Cuneo, in Piemonte."),
 S(2, "La guida Giovanni Ciravegna, insieme al figlio Daniele. È un'azienda vinicola che produce e vende vino da tavola, anche sfuso, ad altre aziende."),
 S(2, "Diciamolo subito: di loro diremo solo quello che risulta dalle indagini e dalle sentenze. Nel [1992|millenovecentonovantadue] saranno condannati in primo grado. Ci arriveremo."),
 S(2, "Poi c'è un imbottigliatore dell'Astigiano, a Incisa Scapaccino. Compra vino, lo mette in bottiglioni con la propria etichetta e lo distribuisce, tra l'altro, ai supermercati della Lombardia."),
 S(2, "Le fonti indicano che il vino rosso e bianco da tavola venduto con quell'etichetta proveniva dalla cantina di Narzole. È il primo anello della catena che i magistrati dovranno ricostruire."),
 S(2, "Dall'altra parte della bacheca ci sono le istituzioni. A Milano un sostituto procuratore, Alberto Nobili, riceverà l'incarico di indagare sulle prime morti sospette."),
 S(2, "A Roma il ministro dell'Agricoltura è Filippo Maria Pandolfi. Sarà lui a riferire in Parlamento i numeri del vino sotto accusa e ad annunciare i nuovi certificati per l'esportazione."),
 S(2, "E poi ci sono le persone comuni. Pensionati, casalinghe, lavoratori che comprano un bottiglione al supermercato sotto casa. Non faremo i loro nomi: in questa storia sono le vittime."),
 S(2, "Tra le loro famiglie c'è Roberto Ferlicca. Sua madre è tra le prime persone intossicate e perde la vista. Negli anni seguenti Ferlicca diventerà la voce del comitato delle vittime."),
 S(2, "Infine c'è un ente di controllo poco conosciuto: il servizio di repressione delle frodi, con un ufficio a Treviso. Nel [1984|millenovecentoottantaquattro] aveva già incrociato la strada della cantina di Narzole. Anche questo lo vedremo."),
 S(2, "Ecco la prima scheda di riepilogo. Il luogo: il Piemonte del vino da tavola. La sostanza: il metanolo, tollerato solo in tracce. Il limite: zero virgola tre. E una filiera che va dalla cantina fino alla tavola."),
 # ------------------------------------------------------------------ 3 · LA SCORCIATOIA
 S(3, "Ora la domanda chiave: perché qualcuno dovrebbe mettere metanolo nel vino? La risposta, secondo tutte le ricostruzioni, è economica."),
 S(3, "Il metanolo, essendo un alcol, alza la gradazione del vino. Un vino debole, con l'aggiunta di metanolo, diventa sulla carta un vino più forte, e quindi più vendibile."),
 S(3, "E qui entra in gioco una legge. Nell'estate del [1984|millenovecentoottantaquattro] una norma fiscale cambia la tassazione degli alcolici. Tra le altre cose, il metanolo viene esentato dall'imposta di fabbricazione."),
 S(3, "Lo scopo della norma riguardava il fisco e il commercio, non il vino. Ma l'effetto collaterale, raccontano le fonti, è che il metanolo diventa molto economico. Più economico dello zucchero, che invece l'imposta la paga."),
 S(3, "Secondo alcune ricostruzioni, con la detassazione si allentano anche i controlli sulla vendita del metanolo, che prima passava sotto l'occhio degli uffici tecnici della finanza."),
 S(3, "Il risultato è una scorciatoia: un prodotto industriale, quasi indistinguibile dall'alcol buono, che costa poco e alza i gradi. Una tentazione pericolosa per chi ragiona solo sul prezzo."),
 S(3, "Quanto metanolo circola? Le fonti concordano su un dato: dalla metà di dicembre del [1985|millenovecentoottantacinque] al marzo del [1986|millenovecentoottantasei] in Italia ne vengono venduti circa due tonnellate e mezzo, in buona parte finiti nel vino."),
 S(3, "Facciamo un conto. Da metà dicembre alla fine di marzo passano circa centocinque giorni. Due tonnellate e mezzo divise per centocinque giorni fanno circa ventiquattro chili di metanolo al giorno."),
 S(3, "C'è poi un precedente. Nel [1984|millenovecentoottantaquattro] un controllo della repressione frodi di Treviso trova nel vino della cantina di Narzole valori di metanolo fuori dalla norma."),
 S(3, "Scattano un sequestro e una denuncia penale. Ma, secondo le ricostruzioni, la pratica si perde per strada. La cantina continua a lavorare."),
 S(3, "È uno dei punti che, anni dopo, faranno più discutere: un segnale d'allarme c'era stato, due anni prima. E non era bastato a fermare la catena."),
 S(3, "Come funziona la catena, in pratica? Il vino da tavola passa di mano più volte. Si compra sfuso, si taglia, cioè si mescola con altri vini, si rivende ad altre aziende."),
 S(3, "Chi imbottiglia spesso non produce l'uva. Compra vino già fatto, a volte da più fornitori, e lo mette nei bottiglioni. Se una partita è contaminata, il problema viaggia con lei."),
 S(3, "Ed è così che una frode nata in una cantina può finire, in pochi giorni, sugli scaffali di decine di supermercati in tre regioni diverse."),
 # ------------------------------------------------------------------ 4 · MARZO 1986
 S(4, "Milano, inizio di marzo del [1986.|millenovecentoottantasei.] Nei primi giorni del mese si registrano le prime morti sospette. Casi che, all'inizio, nessuno collega tra loro."),
 S(4, "Nello stesso periodo una donna di sessant'anni viene ricoverata d'urgenza. Ha bevuto un bicchiere di Barbera a cena, da un bottiglione comprato al supermercato. Si salverà, ma perderà la vista."),
 S(4, "Le fonti non coincidono sull'ospedale e sulla data esatta del ricovero: per alcune è l'ospedale Sacco, per altre il Niguarda, entrambi a Milano. Ma su un punto concordano: i medici sospettano un avvelenamento."),
 S(4, "Secondo il racconto della famiglia, il bottiglione non era finito. Viene portato in ospedale e analizzato. Dentro c'è metanolo, in quantità molto superiori al limite di legge."),
 S(4, "Quanto superiori? Qui le fonti danno numeri diversi, a seconda dei campioni. Il settimanale americano TIME, in quei giorni, parla di vino con metanolo fino al cinque virgola sette per cento."),
 S(4, "Altre ricostruzioni parlano di valori molte volte oltre la soglia. Ricordate il limite: zero virgola tre. Anche nella stima più bassa, siamo lontanissimi."),
 S(4, "Il diciassette marzo i casi esplodono. Arrivano segnalazioni di intossicazioni in Lombardia, in Piemonte e in Liguria. È la data che quasi tutte le fonti indicano come l'inizio dello scandalo."),
 S(4, "I sintomi, riportano le cronache, sono quelli tipici dell'avvelenamento da metanolo: malessere, disturbi della vista, nei casi più gravi la perdita di coscienza. Non entriamo nei dettagli: bastano i numeri."),
 S(4, "Il diciotto marzo l'agenzia ANSA dà la notizia. La procura di Milano apre un fascicolo e il sostituto procuratore Alberto Nobili riceve l'incarico di indagare."),
 S(4, "Le prime analisi puntano su due vini: un Barbera da tavola e un bianco da tavola, imbottigliati dalla ditta dell'Astigiano e venduti nei supermercati della Lombardia."),
 S(4, "Il figlio della donna rimasta cieca racconterà, anni dopo, di aver chiamato lui stesso l'agenzia di stampa per diffondere l'allarme. È il suo ricordo: le fonti lo riportano come testimonianza."),
 S(4, "Intanto il numero delle vittime sale di giorno in giorno. Le cronache di quelle settimane aggiornano il bilancio quasi ogni mattina."),
 S(4, "Nei supermercati il vino sospetto viene tolto dagli scaffali. Molte persone smettono di comprare vino, di qualunque marca. La paura non distingue tra un bottiglione e una bottiglia di qualità."),
 # ------------------------------------------------------------------ 5 · L'ALLARME
 S(5, "Fermiamoci un momento per la seconda scheda di riepilogo. Marzo [1986:|millenovecentoottantasei:] metanolo nel vino da tavola, intossicazioni in tre regioni, la procura di Milano al lavoro. Ora l'allarme si allarga."),
 S(5, "Gli inquirenti devono fare in fretta: ogni bottiglione rimasto in una cantina o in un supermercato è un rischio. Le forze dell'ordine sequestrano vino in Lombardia, Piemonte, Liguria ed Emilia-Romagna."),
 S(5, "I carabinieri dei NAS, il nucleo antisofisticazioni, girano i supermercati. Le analisi si moltiplicano: ogni partita sospetta deve passare dal laboratorio."),
 S(5, "In Senato il ministro Pandolfi riferisce una cifra che fa impressione: in circolazione ci sarebbero circa seicentomila litri di vino contaminato."),
 S(5, "Seicentomila litri. Facciamo un conto: divisi per due litri, fanno circa trecentomila bottiglioni. Messi in fila, uno dopo l'altro, coprirebbero decine di chilometri."),
 S(5, "Il [12|dodici] aprile il ministero della Sanità firma un'ordinanza urgente. Vieta in tutta Italia la vendita e la somministrazione dei vini prodotti o imbottigliati da un elenco di aziende."),
 S(5, "Nella prima tabella ci sono sette ditte inquisite per adulterazione con metanolo, in Piemonte, in Puglia e in Emilia-Romagna. Nella seconda, decine di altre aziende i cui campioni sono risultati sopra i limiti o sospetti."),
 S(5, "L'ordinanza viene pubblicata in Gazzetta Ufficiale il [14|quattordici] aprile. Chi si è rifornito da quelle aziende deve ritirare le partite e denunciarle al sindaco, che dispone il sequestro e le analisi."),
 S(5, "Intanto l'allarme supera i confini. In Francia, nel porto di Sète, viene bloccata una nave cisterna carica di vino italiano proveniente dalla Puglia."),
 S(5, "In Germania Ovest, nel Baden-Württemberg, le autorità sequestrano bottiglie di Barbera contaminato. Sul numero esatto le fonti non coincidono: si parla di centinaia, per alcune oltre mille bottiglie."),
 S(5, "Negli Stati Uniti, secondo il Christian Science Monitor, l'agenzia federale che controlla gli alcolici impone restrizioni all'importazione del vino italiano, e le toglie solo dopo un accordo con il governo di Roma."),
 S(5, "La condizione è un certificato. Il ministro Pandolfi annuncia che tutto il vino destinato all'estero dovrà avere un certificato di analisi che attesti l'assenza di metanolo oltre i limiti."),
 S(5, "Per alcune settimane, raccontano gli operatori del settore, l'export si blocca quasi del tutto. Anche le cantine che non hanno nulla a che fare con la frode vedono gli ordini annullati."),
 # ------------------------------------------------------------------ 6 · L'INDAGINE
 S(6, "Torniamo a Milano, nell'ufficio del pubblico ministero. Il principio dell'indagine è lo stesso di un'inchiesta su un furto: seguire la merce all'indietro, passaggio dopo passaggio."),
 S(6, "Si parte dai bottiglioni delle vittime. Dall'etichetta si arriva all'imbottigliatore dell'Astigiano. Da lì bisogna capire chi gli ha venduto il vino."),
 S(6, "Ogni passaggio lascia una traccia: una bolla di trasporto, una fattura, un registro di cantina. E ogni traccia porta un po' più a sud, verso la provincia di Cuneo."),
 S(6, "La strada porta a Narzole, alla cantina Ciravegna. Secondo le ricostruzioni, l'imbottigliatore collabora con i carabinieri e consegna i suoi documenti."),
 S(6, "Dopo i primi decessi partono le comunicazioni giudiziarie. Le ipotesi di reato sono pesanti: omicidio colposo plurimo, lesioni colpose e violazione della legge sulle frodi nei vini."),
 S(6, "Una precisazione importante: colposo significa senza l'intenzione di uccidere. L'accusa sostiene che la morte delle persone sia la conseguenza di una frode, non lo scopo."),
 S(6, "Pochi giorni dopo, Giovanni e Daniele Ciravegna vengono arrestati. Secondo le ricostruzioni, durante le indagini il padre sceglie di non rispondere."),
 S(6, "Ma l'indagine non si ferma a una sola cantina. Il vino di Narzole era stato venduto anche ad altre aziende, che lo avevano usato per tagliare i propri vini."),
 S(6, "Secondo la procura di Milano le aziende coinvolte, a vario titolo, sono una sessantina. Gli inquirenti ricostruiscono anche il percorso del metanolo: chi lo vendeva, chi lo trasportava, chi lo comprava."),
 S(6, "In cinque settimane, raccontano le fonti, la procura ricostruisce il quadro generale della frode. Per un'indagine con decine di aziende e centinaia di partite, è un tempo molto breve."),
 S(6, "Con gli arresti arriva anche un'altra scoperta, quella del precedente del [1984:|millenovecentoottantaquattro:] il controllo di Treviso, il sequestro, la denuncia rimasta senza seguito."),
 S(6, "È qui che la vicenda smette di essere solo una storia di truffa. Diventa anche una storia di controlli: quanti ce n'erano, chi doveva farli, e perché un primo allarme non aveva fermato nulla."),
 S(6, "C'è anche un episodio che alcune ricostruzioni raccontano e che resta impresso: nei giorni dei controlli, in Piemonte, qualcuno svuota le proprie vasche di vino per paura delle verifiche, e il fiume Tanaro si colora di rosso."),
 S(6, "È un dettaglio riportato in particolare dalla rivista Dissapore, che ha ricostruito la vicenda con testimoni dell'epoca. Lo citiamo così: come racconto, non come dato verificato da più fonti."),
 # ------------------------------------------------------------------ 7 · LA SVOLTA
 S(7, "Terza scheda di riepilogo. Ventitré morti, centocinquantatré intossicati, una cantina di Narzole al centro dell'inchiesta, una sessantina di aziende coinvolte e il vino italiano fermo alle frontiere."),
 S(7, "Se siete arrivati fin qui e queste storie vi interessano, iscrivetevi a Fascicolo Italia. Ogni giorno apriamo un nuovo caso."),
 S(7, "Ora la svolta. Lo scandalo del metanolo è uno di quei momenti in cui un intero settore cambia regole. Non in anni: in pochi mesi."),
 S(7, "Il diciotto giugno il governo approva un decreto legge con misure urgenti contro le sofisticazioni alimentari. Il Parlamento lo converte nella legge numero [462|quattrocentosessantadue] del sette agosto [1986.|millenovecentoottantasei.]"),
 S(7, "Che cosa cambia? Prima di tutto nasce l'Ispettorato centrale per la repressione delle frodi, presso il ministero dell'Agricoltura. Oggi si chiama ICQRF ed è ancora uno dei principali organi di controllo sul cibo."),
 S(7, "Vengono rafforzati i carabinieri dei NAS e i controlli alle dogane. E nasce un'anagrafe vitivinicola su base regionale: un registro di chi produce vino e di quanto ne produce."),
 S(7, "L'idea è semplice: se ogni passaggio del vino è registrato, diventa molto più difficile far sparire una partita o farne comparire una dal nulla. È la tracciabilità."),
 S(7, "Anche i produttori cambiano strategia. Ad Asti la Camera di commercio propone di estendere le denominazioni d'origine controllate, cioè regole più strette su zona, uva e lavorazione."),
 S(7, "Il motivo è anche commerciale: dopo il metanolo, un vino senza origine certa fa paura. Un vino con una denominazione e un disciplinare dà al consumatore una garanzia in più."),
 S(7, "I numeri dell'export raccontano il prezzo pagato. Nel [1986|millenovecentoottantasei] le esportazioni di vino crollano del trentasette per cento in quantità, e perdono circa un quarto del valore dell'anno prima."),
 S(7, "Altre stime parlano di un calo intorno al quaranta o al quarantacinque per cento. Le cifre non coincidono, ma il senso sì: un anno record si trasforma in un anno nero."),
 S(7, "Facciamo un ultimo conto. Un calo del trentasette per cento vuol dire che, su cento bottiglie che partivano per l'estero, nel [1986|millenovecentoottantasei] ne partono circa sessantatré."),
 S(7, "Secondo diverse ricostruzioni ci vorranno anni, fino agli anni Novanta, perché l'export torni ai livelli di prima. E nel frattempo cambia proprio il tipo di vino che l'Italia vende."),
 # ------------------------------------------------------------------ 8 · IL PROCESSO
 S(8, "Andiamo in aula. Il processo si celebra a Milano, davanti alla Corte d'assise. Le udienze arrivano nei primi anni Novanta, oltre cinque anni dopo i fatti."),
 S(8, "Gli imputati sono i titolari della cantina di Narzole e altre persone della filiera: chi ha trasportato il metanolo, chi ha comprato e rivenduto il vino."),
 S(8, "In aula si ricostruisce tutta la catena: dalle partite di metanolo ai vini tagliati, fino ai bottiglioni arrivati nei supermercati."),
 S(8, "Nel [1992|millenovecentonovantadue] arriva la sentenza di primo grado. Le condanne più alte arrivano fino a sedici anni di reclusione."),
 S(8, "Giovanni Ciravegna, indicato come il principale responsabile, è condannato a quattordici anni. Il figlio Daniele a quattro anni."),
 S(8, "Le fonti che abbiamo consultato non riportano in modo concorde gli esiti dei gradi successivi né le pene degli altri imputati. Per questo non li citiamo e non facciamo altri nomi."),
 S(8, "C'è poi la parte economica. I giudici stabiliscono un risarcimento di circa un miliardo di lire a favore delle vittime riconosciute."),
 S(8, "Quanto vale oggi? Con i coefficienti dell'ISTAT sul valore della moneta, un miliardo di lire del [1992|millenovecentonovantadue] corrisponde a circa un milione di euro di oggi. Se lo dividessimo tra tutte le centosettantasei persone tra morti e intossicati, sarebbero meno di seimila euro a testa."),
 S(8, "Ma quei soldi non arrivano. Secondo le fonti, al momento di pagare i condannati risultano nullatenenti: beni e denaro erano passati ad altri."),
 S(8, "Il figlio di una delle vittime lo dirà più volte, in interviste e trasmissioni: i risarcimenti non sono mai arrivati. Nessuna delle fonti che abbiamo letto riporta un pagamento."),
 S(8, "E Giovanni Ciravegna? Secondo le ricostruzioni esce dal carcere nel [2001,|duemilauno,] dopo aver beneficiato di riduzioni di pena. Torna nelle Langhe e, raccontano le fonti, riprende a produrre vino."),
 S(8, "In un'intervista televisiva si descrive come il più danneggiato di tutti. Muore nel [2013.|duemilatredici.] Non ha mai risarcito le famiglie."),
 # ------------------------------------------------------------------ 9 · DOPO LO SCANDALO
 S(9, "Quarta scheda di riepilogo. Primo grado nel [1992:|millenovecentonovantadue:] quattordici anni al padre, quattro al figlio, condanne fino a sedici anni. Un miliardo di lire di risarcimento, mai pagato."),
 S(9, "Che cosa resta, quarant'anni dopo? Prima di tutto le vittime. Le famiglie si riuniscono in un comitato, guidato da Roberto Ferlicca, che da allora chiede allo Stato un indennizzo."),
 S(9, "Negli anni il caso torna più volte in Parlamento, con interrogazioni parlamentari. Ferlicca racconta di aver scritto a tutti i presidenti del Consiglio. Le risposte, dice, non sono mai arrivate in forma di risarcimento."),
 S(9, "Molti sopravvissuti, nel frattempo, sono morti. Chi aveva perso la vista ha vissuto con una pensione di invalidità. È la parte della storia che non finisce con una sentenza."),
 S(9, "Poi c'è il vino. Lo scandalo cambia il modo in cui l'Italia produce e vende vino. Secondo Il Sole 24 Ore, nel [1986|millenovecentoottantasei] i vini a denominazione o indicazione geografica erano circa il dieci per cento della produzione. Oggi sono oltre il sessanta."),
 S(9, "Sempre secondo il quotidiano, il valore delle esportazioni è passato da circa ottocento milioni di euro del [1986|millenovecentoottantasei] a oltre otto miliardi. L'associazione agricola Coldiretti parla di una rivoluzione della qualità."),
 S(9, "Lo scandalo non è l'unica causa di questo cambiamento, ma tutte le fonti lo indicano come lo spartiacque. Il bottiglione anonimo perde terreno, cresce la bottiglia con l'origine scritta in etichetta."),
 S(9, "Cambiano anche i controlli. Oggi, secondo Il Sole 24 Ore, sul settore agroalimentare si fanno oltre centomila controlli l'anno, tra ispettorato, NAS, carabinieri, Guardia di Finanza e aziende sanitarie."),
 S(9, "Lo scandalo diventa anche memoria. Nel [2021|duemilaventuno] la Rai gli dedica una puntata di un programma di storia, e nel [2023|duemilaventitré] esce un podcast intitolato proprio Metanolo."),
 S(9, "Nel [2026|duemilaventisei] i giornali ricordano i quarant'anni dello scandalo. E le richieste delle famiglie sono ancora sul tavolo."),
 # ------------------------------------------------------------------ 10 · LE DOMANDE APERTE
 S(10, "Arriviamo alle domande aperte, e alle versioni che non coincidono. La prima riguarda i numeri. Ventitré morti e centocinquantatré intossicati sono le cifre più citate, ma non tutti concordano sul resto."),
 S(10, "Quante persone sono rimaste cieche? Alcune fonti dicono quindici, altre diciannove, altre ancora ventitré. E secondo medici e inquirenti dell'epoca, citati da Dissapore, alcuni casi potrebbero essere sfuggiti ai conteggi."),
 S(10, "La seconda domanda riguarda le date. L'inizio dello scandalo viene fissato al diciassette o al diciotto marzo. In realtà le prime morti sospette risalgono a giorni prima, quando nessuno ancora collegava i casi."),
 S(10, "La terza riguarda le aziende. La procura parlava di una sessantina di aziende coinvolte. Altre ricostruzioni parlano di una trentina che avevano tagliato il vino di Narzole. Dipende da cosa si conta."),
 S(10, "La quarta riguarda i controlli. Perché il segnale del [1984|millenovecentoottantaquattro] non ha avuto seguito? Le fonti registrano il fatto, ma nessuna spiega con certezza dove si sia fermata quella pratica."),
 S(10, "La quinta riguarda la legge del [1984.|millenovecentoottantaquattro.] Chi l'ha scritta non pensava al vino. Ma la detassazione del metanolo ha creato un incentivo che nessuno, a quanto risulta, aveva previsto."),
 S(10, "E infine la domanda più semplice e più difficile: perché, quarant'anni dopo, nessuna vittima risulta risarcita? La sentenza c'è. I soldi no. Ed è una domanda che riguarda anche lo Stato, non solo i condannati."),
 # ------------------------------------------------------------------ 11 · LA LEZIONE
 S(11, "Che cosa ci insegna oggi questa storia? Non serve diventare esperti di chimica. Bastano alcune abitudini, quelle che dopo il [1986|millenovecentoottantasei] sono diventate regole."),
 S(11, "Primo: l'etichetta. Su una bottiglia di vino devono comparire chi l'ha imbottigliato e dove, il numero del lotto, la gradazione. Un prodotto senza queste informazioni è un prodotto senza responsabile."),
 S(11, "Secondo: l'origine. Le denominazioni, come DOC, DOCG e IGT, significano regole scritte su zona e lavorazione, e controlli in più. Non sono una garanzia assoluta, ma sono una traccia."),
 S(11, "Terzo: il prezzo. Un prezzo molto basso non è la prova di una frode. Ma è una domanda da farsi. Nel [1986|millenovecentoottantasei] il vino al metanolo era economico proprio perché qualcuno aveva tagliato un costo."),
 S(11, "Quarto: le bevande di origine incerta. Alcolici senza etichetta, sfusi di provenienza sconosciuta, prodotti comprati fuori dai canali normali, in Italia o in viaggio: è lì che i controlli non arrivano."),
 S(11, "Quinto: le segnalazioni. Se un prodotto sembra irregolare, esistono i NAS e l'ispettorato repressione frodi. Nel [1986|millenovecentoottantasei] fu un ospedale a dare l'allarme. Oggi il sistema di controllo è molto più esteso."),
 S(11, "E un'ultima cosa: la lezione vale anche per chi scrive le leggi. Una norma pensata per altro, come la detassazione del metanolo, può creare incentivi pericolosi dove nessuno guarda."),
 # ------------------------------------------------------------------ IL VERDETTO
 S(12, "Ricapitoliamo il fascicolo. Uno: nell'Italia degli anni Ottanta il vino da tavola si vende soprattutto in base alla gradazione, e il metanolo, detassato dal [1984,|millenovecentoottantaquattro,] costa meno dello zucchero."),
 S(12, "Due: nel marzo [1986|millenovecentoottantasei] il vino al metanolo provoca ventitré morti e centocinquantatré intossicati in Lombardia, Piemonte e Liguria. Diverse persone perdono la vista."),
 S(12, "Tre: la procura di Milano risale la filiera fino alla cantina di Narzole. Quattro: l'export crolla e nascono nuovi controlli, dall'ispettorato antifrodi all'anagrafe del vino."),
 S(12, "Cinque: nel [1992|millenovecentonovantadue] Giovanni Ciravegna è condannato in primo grado a quattordici anni, il figlio a quattro. Sei: il risarcimento di un miliardo di lire non è mai stato pagato."),
 S(12, "E tu, quando compri una bottiglia, leggi l'etichetta o guardi solo il prezzo? Scrivilo nei commenti. Le fonti sono tutte nella descrizione."),
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
