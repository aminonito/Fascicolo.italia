STYLE = "fascicolo"
CASE = "FASCICOLO N. 017 · IL CRAC CIRIO"
TITLE = "Il crac Cirio"
CH = ["INTRO", "1 · UNA SCATOLA DEL 1856", "2 · IL FINANZIERE", "3 · IL GRUPPO E LA LAZIO", "4 · I BOND",
      "5 · NOVEMBRE 2002", "6 · IL CROLLO", "7 · L'INCHIESTA", "8 · IL PROCESSO", "9 · DOPO IL CRAC",
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
 S(0, "Novembre [2002.|duemiladue.] Una delle aziende alimentari più antiche d'Italia non restituisce un prestito da centocinquanta milioni di euro. È solo il primo pezzo del domino."),
 S(0, "Nel giro di pochi giorni vanno in default tutte le sue obbligazioni: un miliardo e centoventicinque milioni di euro. In mano a circa trentacinquemila risparmiatori."),
 S(0, "L'azienda è la Cirio. Quella delle scatole di pomodori, nata a Torino nel [1856.|milleottocentocinquantasei.] E il suo padrone, in quegli anni, è anche il presidente della Lazio campione d'Italia."),
 S(0, "Non è una storia di rapine o di casseforti. Nessuno entra di notte in una banca. Eppure alla fine mancano più di un miliardo di euro, e migliaia di persone perdono i loro risparmi."),
 S(0, "In questo fascicolo vedremo come nasce un marchio storico, come un finanziere costruisce un impero tra conserve, latte e calcio, dove finiscono i debiti, e perché ci vorranno quasi vent'anni per arrivare a una sentenza definitiva."),
 # ------------------------------------------------------------------ 1 · UNA SCATOLA DEL 1856
 S(1, "Partiamo dall'inizio. Torino, metà dell'Ottocento. L'Italia unita ancora non esiste. Il cibo si conserva con il sale, con l'olio, con l'aceto, oppure si consuma subito."),
 S(1, "Qualche decennio prima, in Francia, Nicolas [Appert|Appèr] ha messo a punto un metodo nuovo: chiudere il cibo in un contenitore e scaldarlo, così che duri a lungo. Il metodo prende il suo nome: appertizzazione."),
 S(1, "Nel [1856|milleottocentocinquantasei] a Torino un imprenditore, Francesco Cirio, avvia la sua produzione di conserve. Le ricostruzioni non coincidono sul primo prodotto: per alcune fonti sono piselli in scatola, per altre pomodori."),
 S(1, "Quello che conta è l'idea. Una verdura raccolta d'estate si può mangiare in inverno, e soprattutto si può spedire lontano senza che si guasti."),
 S(1, "Nel [1867|milleottocentosessantasette] Cirio porta i suoi prodotti all'Esposizione Universale di Parigi, e riceve dei riconoscimenti. È una vetrina mondiale per un'azienda nata da poco."),
 S(1, "Da lì le conserve partono per l'estero. Le fonti parlano di esportazioni in tutto il mondo, da Liverpool fino a Sydney, dall'altra parte del pianeta."),
 S(1, "Dopo l'unità d'Italia l'attività si allarga verso il Sud, dove il clima è perfetto per il pomodoro. In Campania nasce una delle prime fabbriche italiane dedicate proprio alla conservazione del pomodoro."),
 S(1, "È così che il nome Cirio diventa, per milioni di famiglie, quasi un sinonimo di pomodori pelati. Un marchio che attraversa le guerre, il boom economico, i cambi di proprietà."),
 S(1, "Nel Novecento l'azienda passa di mano più volte. Per un periodo finisce nell'orbita delle partecipazioni dello Stato, insieme ad altri marchi alimentari come Bertolli e De Rica."),
 S(1, "Poi, nei primi anni Novanta, lo Stato decide di vendere molte delle sue aziende. È la stagione delle privatizzazioni. E qui entra in scena il protagonista di questa storia."),
 # ------------------------------------------------------------------ 2 · IL FINANZIERE
 S(2, "Sergio Cragnotti nasce a Roma il [9|nove] gennaio [1940.|millenovecentoquaranta.] Il suo mondo, fin da giovane, è quello dell'industria e della finanza."),
 S(2, "Gran parte della sua carriera iniziale si svolge lontano dall'Italia. Per diversi anni lavora in Brasile, a capo di aziende industriali."),
 S(2, "Poi entra nell'orbita del gruppo Ferruzzi, uno dei grandi gruppi industriali italiani dell'epoca. Ed è lì che fa il salto: diventa un manager di primo piano della Montedison, il colosso della chimica."),
 S(2, "Sono gli anni delle grandi operazioni finanziarie, delle fusioni, delle scalate. Cragnotti impara a muoversi tra banche, Borsa e società estere."),
 S(2, "All'inizio degli anni Novanta decide di mettersi in proprio. Fonda una società di investimenti, la Cragnotti e [Partners,|pàrtners,] con base all'estero."),
 S(2, "Con questa società compra aziende in diversi Paesi. Tra le prime acquisizioni c'è una società brasiliana, la [Bombril.|Bombrìl.] Ricordatevi questo nome: tornerà nei processi."),
 S(2, "Poi arriva l'occasione italiana. Tra il [1993|millenovecentonovantatré] e il [1994,|millenovecentonovantaquattro,] con le privatizzazioni, Cragnotti prende il controllo del gruppo Cirio, Bertolli, De Rica."),
 S(2, "Il progetto è ambizioso: costruire un grande gruppo alimentare italiano. Conserve, olio, latte, e marchi conosciuti in tutto il mondo."),
 S(2, "Ma c'è un dettaglio che diventerà decisivo. L'espansione non viene finanziata con il capitale dei soci. Viene finanziata soprattutto con i debiti."),
 S(2, "Prima con i prestiti delle banche. Poi, come vedremo, con le obbligazioni. Tenete a mente questo meccanismo, perché è il cuore di tutto il caso."),
 # ------------------------------------------------------------------ 3 · IL GRUPPO E LA LAZIO
 S(3, "Prima del grande gruppo alimentare, però, Cragnotti ha già comprato un'altra cosa: una squadra di calcio. Dal febbraio del [1992|millenovecentonovantadue] è il presidente della Lazio."),
 S(3, "È l'inizio di un'epoca d'oro per i tifosi biancocelesti. Arrivano giocatori famosi, la squadra cresce stagione dopo stagione."),
 S(3, "Nel [1998|millenovecentonovantotto] la Lazio diventa il primo club italiano quotato in Borsa. Nello stesso anno vince la Coppa Italia."),
 S(3, "Nel [1999|millenovecentonovantanove] arriva un trofeo europeo: la Coppa delle Coppe, vinta in finale a Birmingham, in Inghilterra."),
 S(3, "In quegli anni con la maglia della Lazio giocano campioni come Pavel [Nedved,|Nèdved,] Christian Vieri e Marcelo Salas. A Birmingham, nella finale contro il Maiorca, il gol decisivo è proprio di [Nedved.|Nèdved.]"),
 S(3, "E nel [2000|duemila] la Lazio vince lo scudetto, all'ultima giornata. Nella stessa stagione arriva anche la Coppa Italia. È il punto più alto della presidenza Cragnotti."),
 S(3, "Intanto il gruppo alimentare continua a crescere. Il ramo del latte si allarga: nel [1998|millenovecentonovantotto] arriva anche la Centrale del Latte di Roma, comprata dal Comune."),
 S(3, "Negli stessi anni il gruppo punta anche sul marchio Del Monte, con la società Del Monte Royal. Un altro acquisto importante, un altro pezzo dell'impero."),
 S(3, "Nel [1999,|millenovecentonovantanove,] invece, il gruppo vende tutto il settore del latte, riunito nella società Eurolat, a un altro colosso italiano: la Parmalat."),
 S(3, "Il prezzo di quella vendita viene riportato in modi diversi, perché le fonti misurano cose diverse: il valore complessivo della società, oppure il prezzo al netto dei debiti. Quello che è certo è che la vendita, anni dopo, finirà davanti a un giudice."),
 S(3, "Ricapitoliamo come appare il gruppo alla fine degli anni Novanta. In cima, le società di famiglia. Sotto, la Cirio con le conserve, il marchio Del Monte, la brasiliana Bombril, e una partecipazione nella Lazio."),
 S(3, "Le quote della Lazio in mano al gruppo cambiano nel tempo, e le fonti non coincidono sulle percentuali. Ma il legame è stretto: il gruppo alimentare e la squadra sono parte dello stesso mondo."),
 S(3, "E il conto? A fine [1999|millenovecentonovantanove] il gruppo ha debiti per oltre un miliardo di euro. Circa l'ottantacinque per cento di questi debiti è verso le banche."),
 S(3, "Un miliardo di debiti, quasi tutti con le banche. E i debiti con le banche, prima o poi, vanno restituiti. Ed è qui che la storia cambia direzione."),
 # ------------------------------------------------------------------ 4 · I BOND
 S(4, "Per capire cosa succede dopo, serve un minuto di spiegazione. Cos'è un'obbligazione? È un prestito. Tu dai dei soldi a un'azienda, e lei si impegna a restituirli a una data precisa, la scadenza."),
 S(4, "Nel frattempo ti paga degli interessi, le cedole. Se l'azienda è solida, è un investimento tranquillo. Se l'azienda non ha i soldi alla scadenza, quel prestito può non tornare indietro."),
 S(4, "Quando un'azienda non paga, si dice che va in default. E siccome chi presta non può controllare da solo i conti, di solito si affida a due strumenti: il giudizio delle agenzie di rating, e un prospetto informativo che spiega i rischi."),
 S(4, "Ora torniamo alla Cirio. Tra il [2000|duemila] e il [2002|duemiladue] il gruppo colloca sul mercato sette prestiti obbligazionari. In totale, un miliardo e centoventicinque milioni di euro."),
 S(4, "Le obbligazioni non vengono emesse in Italia. Vengono emesse da società del gruppo con sede in Lussemburgo, create apposta per raccogliere i soldi."),
 S(4, "Che cos'è una società veicolo? È una società costruita per uno scopo preciso, in questo caso raccogliere denaro sul mercato e girarlo al gruppo. Spesso ha sede in un Paese con regole e tasse favorevoli, e dentro ha poco o nulla oltre ai debiti."),
 S(4, "Secondo le ricostruzioni, quei titoli nascono per gli investitori professionali: fondi, banche, operatori esperti. Non c'è un'offerta pubblica rivolta ai piccoli risparmiatori."),
 S(4, "Eppure è proprio lì che finiscono. Attraverso gli sportelli delle banche, quei bond arrivano nei portafogli di migliaia di famiglie. Secondo le associazioni dei consumatori, circa trentacinquemila risparmiatori."),
 S(4, "Perché un risparmiatore compra un bond Cirio? Il marchio è famosissimo, è in tutte le cucine. E le obbligazioni di aziende molto indebitate, di solito, rendono più dei titoli considerati più sicuri."),
 S(4, "Ma un rendimento più alto, in finanza, ha quasi sempre un significato preciso: più rischio. Chi presta a un'azienda molto indebitata chiede di essere pagato di più."),
 S(4, "E adesso guardiamo il dato che, per l'accusa e per i giudici, conta di più. Dove vanno i soldi raccolti con le obbligazioni?"),
 S(4, "Le ricostruzioni dei commissari e dei periti dicono la stessa cosa, anche se con numeri diversi. A fine [1999|millenovecentonovantanove] il debito del gruppo era quasi tutto verso le banche. Nel [2002|duemiladue] la maggior parte è in mano agli obbligazionisti."),
 S(4, "In pratica il debito cambia padrone. Le banche si fanno restituire una parte dei loro prestiti. Al loro posto, il rischio passa a chi ha comprato i bond."),
 S(4, "Secondo i giudici, tra il [2000|duemila] e il [2002|duemiladue] quelle obbligazioni vengono vendute quando il gruppo è già in difficoltà, anche per chiudere le posizioni con le banche. È il punto su cui si giocheranno i processi."),
 S(4, "Facciamo un conto per capire le proporzioni. Un miliardo e centoventicinque milioni diviso trentacinquemila fa circa trentaduemila euro a testa."),
 S(4, "È solo un ordine di grandezza, perché una parte dei titoli era in mano a investitori professionali, e ogni risparmiatore aveva cifre diverse. Ma dà l'idea: per molte famiglie si tratta dei risparmi di una vita."),
 S(4, "Prima di andare avanti, un breve riepilogo per chi ci ha appena raggiunto. Un marchio storico. Un finanziere che lo compra con i debiti. Debiti spostati dalle banche ai risparmiatori, con sette prestiti emessi dal Lussemburgo."),
 S(4, "Se questi fascicoli ti piacciono, iscriviti a Fascicolo Italia: è il modo più semplice per non perdere il prossimo caso. E ora, novembre [2002.|duemiladue.]"),
 # ------------------------------------------------------------------ 5 · NOVEMBRE 2002
 S(5, "Una delle obbligazioni scade il [3|tre] novembre [2002.|duemiladue.] È un prestito da centocinquanta milioni di euro, emesso da una società del gruppo con sede in Lussemburgo."),
 S(5, "Alla scadenza i soldi per rimborsarlo non ci sono. I risparmiatori che aspettano il loro capitale non ricevono niente."),
 S(5, "Ogni emissione di obbligazioni ha un garante dei diritti di chi ha prestato i soldi: si chiama [trustee,|trastì,] e in questo caso è una società con sede a Londra."),
 S(5, "Pochi giorni dopo, il [7|sette] novembre secondo alcune fonti, l'otto secondo altre, il [trustee|trastì] dichiara ufficialmente il default. Il prestito non è stato restituito."),
 S(5, "Un conto per capire il peso di quel primo titolo. Centocinquanta milioni su un miliardo e centoventicinque sono circa il tredici per cento del totale. Un pezzo relativamente piccolo, che però basta a far crollare tutto il resto."),
 S(5, "E qui scatta un meccanismo che molti risparmiatori non conoscevano. Si chiama [cross default,|cròss default,] inadempimento incrociato."),
 S(5, "Funziona così: nei contratti delle obbligazioni c'è scritto che, se l'emittente non paga uno dei suoi prestiti, anche gli altri possono essere considerati in default. Un debito non pagato trascina tutti gli altri."),
 S(5, "È esattamente quello che succede. Nei giorni successivi vanno in default anche le altre emissioni del gruppo. In totale, un miliardo e centoventicinque milioni di euro."),
 S(5, "In due settimane, sette prestiti diventano carta quasi senza valore. Le obbligazioni restano nei portafogli, ma nessuno sa più se e quando torneranno indietro i soldi."),
 S(5, "Titoli emessi in Lussemburgo, legati a un gruppo pieno di debiti: dettagli che non erano certo scritti sull'etichetta di una scatola di pomodori."),
 S(5, "Proviamo a metterci nei loro panni. Hai comprato un'obbligazione con il nome di una marca che vedi tutti i giorni al supermercato. Ti sembrava una scelta prudente. E all'improvviso il titolo è bloccato."),
 S(5, "Facciamo un altro conto. Dalla fondazione a Torino, nel [1856,|milleottocentocinquantasei,] al default del [2002|duemiladue] passano centoquarantasei anni. Il marchio è sopravvissuto a due guerre mondiali. Non sopravvive, nella sua forma di allora, ai debiti."),
 # ------------------------------------------------------------------ 6 · IL CROLLO
 S(6, "Dopo il default, il crollo si trasmette a tutto quello che è collegato al gruppo. Compresa la squadra di calcio."),
 S(6, "Il [3|tre] gennaio [2003|duemilatré] Cragnotti si dimette da presidente della Lazio. All'inizio di quell'anno lascia anche la guida della Cirio."),
 S(6, "Per il gruppo si prepara un piano di ristrutturazione dei debiti, con l'aiuto di consulenti finanziari."),
 S(6, "Ma il piano deve essere approvato da chi ha in mano i bond. Nel luglio del [2003|duemilatré] l'assemblea degli obbligazionisti lo boccia."),
 S(6, "A quel punto resta una sola strada. Nell'estate del [2003|duemilatré] il Tribunale di Roma dichiara lo stato di insolvenza, e le principali società del gruppo entrano in amministrazione straordinaria."),
 S(6, "Che cos'è l'amministrazione straordinaria? È la procedura prevista in Italia per le grandi imprese in crisi. L'azienda non viene chiusa subito: la gestione passa a commissari nominati dallo Stato."),
 S(6, "Attenzione alle parole. Insolvenza vuol dire che un'impresa non è più in grado di pagare regolarmente i suoi debiti. Non vuol dire che qualcuno abbia commesso un reato. Quello lo devono stabilire, eventualmente, i giudici."),
 S(6, "I commissari hanno due compiti. Provare a salvare quello che si può salvare, cioè le fabbriche, i marchi, i posti di lavoro. E vendere i beni per pagare, almeno in parte, i creditori."),
 S(6, "I commissari preparano la vendita delle attività. Tra queste c'è il cuore storico del gruppo: il ramo delle conserve, con i marchi Cirio e De Rica."),
 S(6, "Intanto i risparmiatori si rivolgono alle associazioni dei consumatori, che li assistono e li rappresentano. La domanda di tutti è una: chi ci ha venduto quei titoli, e perché?"),
 S(6, "Il caso Cirio diventa un simbolo. E pochi mesi dopo, alla fine del [2003,|duemilatré,] crolla anche la Parmalat, con un buco molto più grande. In Italia si apre una lunga discussione su come proteggere i risparmiatori."),
 S(6, "Riepilogo per chi ci ha appena raggiunto. Sette bond emessi dal Lussemburgo. Il primo non viene rimborsato a novembre [2002,|duemiladue,] e trascina gli altri. Nel [2003|duemilatré] il piano di salvataggio viene bocciato, e arriva l'amministrazione straordinaria."),
 # ------------------------------------------------------------------ 7 · L'INCHIESTA
 S(7, "Mentre i commissari lavorano sui conti, lavora anche la Procura di Roma. Nel [2003|duemilatré] si apre l'inchiesta sul dissesto del gruppo."),
 S(7, "Le ipotesi di reato si allargano mese dopo mese. Tra queste, la più grave è la bancarotta fraudolenta."),
 S(7, "Che cos'è la bancarotta? È il reato di chi, quando un'impresa fallisce o diventa insolvente, ha danneggiato i creditori. Ce ne sono diversi tipi."),
 S(7, "Si parla di bancarotta distrattiva quando i beni o i soldi dell'azienda vengono portati via, distratti, per altri scopi. E di bancarotta preferenziale quando, in una situazione di crisi, si pagano alcuni creditori a scapito degli altri."),
 S(7, "Tenete a mente queste due parole, distrattiva e preferenziale. Nel caso Cirio le ritroveremo entrambe: i soldi spostati verso altre società, e le banche rimborsate prima dei risparmiatori."),
 S(7, "Nell'inchiesta finiscono decine di persone. Tra loro familiari e collaboratori di Cragnotti, e anche alcuni dirigenti di banca. Per tutti, in questa fase, si tratta solo di indagati."),
 S(7, "Poi arriva la svolta. L'undici febbraio [2004|duemilaquattro] Sergio Cragnotti viene arrestato, su richiesta della Procura di Roma."),
 S(7, "L'ex presidente della Lazio campione d'Italia, l'uomo che aveva comprato un pezzo di storia dell'industria alimentare, viene arrestato a meno di quattro anni dallo scudetto."),
 S(7, "Le indagini durano anni. Bisogna ricostruire migliaia di operazioni tra società italiane ed estere, e capire dove sono finiti i soldi raccolti con i bond."),
 S(7, "Il [25|venticinque] settembre [2007|duemilasette] il giudice dell'udienza preliminare decide il rinvio a giudizio. Il processo vero e proprio può cominciare. Gli imputati sono trentacinque."),
 # ------------------------------------------------------------------ 8 · IL PROCESSO
 S(8, "Siamo a Roma, in un'aula del Tribunale. Il processo dura anni. Davanti ai giudici passano periti, consulenti, testimoni e gli avvocati dei risparmiatori."),
 S(8, "Nel [2011|duemilaundici] i pubblici ministeri fanno le loro richieste. Per Cragnotti chiedono quindici anni di carcere."),
 S(8, "Il [4|quattro] luglio [2011|duemilaundici] arriva la sentenza di primo grado. Sergio Cragnotti è condannato a nove anni di reclusione, per bancarotta e truffa."),
 S(8, "Viene condannato a quattro anni anche un banchiere, all'epoca ai vertici di una grande banca romana che aveva avuto rapporti stretti con il gruppo. Condanne anche per alcuni familiari e collaboratori."),
 S(8, "Non tutti gli imputati vengono condannati: altri vengono assolti. Dirlo è importante: per la legge chi è assolto è innocente."),
 S(8, "Il tribunale stabilisce anche una provvisionale, cioè un anticipo sul risarcimento, di duecento milioni di euro a favore dell'amministrazione straordinaria. A pagarla sono chiamati i condannati e una banca come responsabile civile."),
 S(8, "Facciamo il confronto. Duecento milioni su un miliardo e centoventicinque milioni di obbligazioni in default: è meno di un quinto. E si tratta di un primo grado, quindi di una decisione non ancora definitiva."),
 S(8, "Ma in Italia una condanna diventa definitiva solo dopo tre gradi di giudizio: il tribunale, la corte d'appello e la Cassazione. Fino ad allora, ogni imputato è considerato non colpevole."),
 S(8, "In appello, a Roma, la sua pena scende a otto anni e otto mesi. Nell'aprile del [2015|duemilaquindici] la Corte d'appello conferma i quattro anni per il banchiere."),
 S(8, "Poi tocca alla Cassazione, l'ultimo grado di giudizio. Siamo nell'ottobre del [2017.|duemiladiciassette.] Quindici anni dopo il default."),
 S(8, "Per il banchiere la condanna a quattro anni diventa definitiva. Tre di questi anni sono coperti dall'indulto, una misura del [2006|duemilasei] che ha cancellato una parte delle pene per molti reati."),
 S(8, "Per Cragnotti, invece, la Cassazione annulla una parte della condanna e rinvia il caso a un nuovo processo d'appello. Il punto riguarda la bancarotta distrattiva legata alla società brasiliana Bombril."),
 S(8, "Annullare con rinvio non vuol dire assolvere. Vuol dire che un nuovo collegio di giudici deve rivalutare quel punto. Il resto delle responsabilità, secondo le fonti, resta confermato."),
 S(8, "Il [26|ventisei] giugno [2019|duemiladiciannove] la Corte d'appello di Roma, nel nuovo giudizio, ridetermina la pena di Cragnotti: cinque anni e tre mesi."),
 S(8, "Cragnotti ricorre ancora in Cassazione. Nel marzo del [2021|duemilaventuno] la Cassazione dichiara il ricorso inammissibile. La condanna a cinque anni e tre mesi diventa definitiva."),
 S(8, "Che cosa vuol dire inammissibile? Che la Cassazione non entra nemmeno nel merito del ricorso, perché non ha i requisiti richiesti dalla legge. A quel punto, la sentenza precedente diventa definitiva."),
 S(8, "Fermiamoci sulle date. Il primo bond non rimborsato è del novembre [2002.|duemiladue.] La condanna definitiva per Cragnotti è del marzo [2021.|duemilaventuno.] In mezzo ci sono più di diciotto anni."),
 S(8, "Riepilogo per chi entra adesso. Default a novembre [2002.|duemiladue.] Amministrazione straordinaria nel [2003.|duemilatré.] Arresto nel [2004.|duemilaquattro.] Primo grado nel [2011:|duemilaundici:] nove anni. Definitiva nel [2021:|duemilaventuno:] cinque anni e tre mesi."),
 # ------------------------------------------------------------------ 9 · DOPO IL CRAC
 S(9, "Accanto al processo penale c'è anche la causa civile. E riguarda proprio la vendita del latte alla Parmalat del [1999.|millenovecentonovantanove.]"),
 S(9, "Il [13|tredici] febbraio [2008|duemilaotto] il Tribunale civile di Roma condanna Cragnotti e la banca che aveva assistito l'operazione a pagare trecento milioni di euro all'amministrazione straordinaria della Cirio."),
 S(9, "È una sentenza di primo grado civile. Ma racconta quanto quella vendita, avvenuta tre anni prima del default, fosse considerata importante per capire il dissesto."),
 S(9, "E le fabbriche? Il marchio? Nel [2004|duemilaquattro] i commissari vendono il ramo delle conserve Cirio e De Rica a Conserve Italia, un consorzio di cooperative agricole italiane."),
 S(9, "Il prezzo riportato dalle fonti non coincide: si parla di un'offerta di poco più di centocinquanta milioni, e di una vendita intorno ai centosessantotto milioni di euro."),
 S(9, "Il marchio, quindi, sopravvive. Le scatole di pomodori Cirio continuano a stare sugli scaffali, oggi prodotte da un gruppo di agricoltori associati."),
 S(9, "La Lazio, invece, aveva già cambiato presidente all'inizio del [2003.|duemilatré.] Per i tifosi, la stagione dei grandi trofei è finita insieme all'impero del suo presidente."),
 S(9, "E i risparmiatori? Una parte di loro si costituisce parte civile nel processo, per chiedere di essere risarcita. Ma tra le obbligazioni perse e i risarcimenti, la distanza resta enorme."),
 S(9, "Il caso Cirio, insieme al caso Parmalat, apre in Italia un lungo dibattito sul risparmio. Si discute di trasparenza, di conflitti di interesse delle banche, di come vengono vendute le obbligazioni agli sportelli."),
 S(9, "Un ultimo riepilogo prima delle domande aperte. Condanna definitiva per Cragnotti nel [2021.|duemilaventuno.] Condanna definitiva a quattro anni per un banchiere nel [2017.|duemiladiciassette.] Il marchio Cirio, intanto, vive ancora, nelle mani di cooperative agricole."),
 # ------------------------------------------------------------------ 10 · LE DOMANDE APERTE
 S(10, "Restano alcune domande, e alcuni punti in cui le fonti non coincidono. Il primo riguarda le cifre."),
 S(10, "Il totale delle obbligazioni in default è un miliardo e centoventicinque milioni per la maggior parte delle fonti. Altre arrotondano a un miliardo e due, o parlano di un miliardo e duecentocinquanta milioni emessi in tutto. Dipende da cosa si conta."),
 S(10, "Anche la data del default non è riportata da tutti allo stesso modo: il [3|tre] novembre è la scadenza del prestito, il [7|sette] o l'otto novembre la dichiarazione ufficiale."),
 S(10, "La seconda domanda è quella che i risparmiatori si sono fatti per anni: chi sapeva? Chi vendeva quei titoli allo sportello conosceva le condizioni del gruppo?"),
 S(10, "Su questo le sentenze hanno dato risposte diverse per persone diverse. Alcuni sono stati condannati, altri assolti. Ed è giusto fermarsi a quello che dicono i giudici."),
 S(10, "La terza domanda riguarda la Parmalat. La vendita del latte del [1999|millenovecentonovantanove] lega i due crac più famosi di quegli anni. Una sentenza civile di primo grado l'ha già considerata un danno per la Cirio."),
 S(10, "E l'ultima domanda è la più semplice: si poteva evitare? Un gruppo con oltre un miliardo di debiti già nel [1999,|millenovecentonovantanove,] e sette prestiti emessi in tre anni. I segnali, a guardarli oggi, c'erano."),
 # ------------------------------------------------------------------ 11 · LA LEZIONE
 S(11, "Che cosa possiamo imparare dal caso Cirio? Non è un consiglio di investimento: è un elenco di domande da fare prima di firmare."),
 S(11, "Prima domanda: chi emette questo titolo, e da dove? Se l'emittente è una società veicolo all'estero, conviene capire chi garantisce davvero il rimborso."),
 S(11, "Seconda domanda: perché rende così tanto? Un rendimento molto più alto della media è quasi sempre il prezzo di un rischio più alto."),
 S(11, "Terza domanda: esiste un giudizio di rating? Esiste un prospetto che spiega i rischi? Se il titolo era pensato per investitori professionali, è adatto a me?"),
 S(11, "Quarta domanda: quanti dei miei risparmi sto mettendo su un solo nome? Concentrare tutto su un'unica azienda, anche famosa, vuol dire che se va male quella azienda, va male tutto."),
 S(11, "Quinta: ho capito che cosa succede se l'azienda non paga? Un'obbligazione non è un conto corrente. Se l'emittente va in default, i soldi possono non tornare, o tornare solo in parte e dopo anni."),
 S(11, "Una marca famosa non è una garanzia. Nel caso Cirio molti risparmiatori si sono fidati del nome stampato sulle scatole di pomodori. Ma il nome sul titolo non dice quanto è indebitato chi lo emette."),
 S(11, "Dove informarsi? La Consob e la Banca d'Italia pubblicano guide gratuite per i risparmiatori, con le domande da fare in banca e le parole da conoscere. Leggerle prima di firmare costa pochi minuti."),
 # ------------------------------------------------------------------ IL VERDETTO
 S(12, "Ricapitoliamo il fascicolo. Uno: un marchio nato a Torino nel [1856|milleottocentocinquantasei] diventa, negli anni Novanta, parte di un grande gruppo costruito a debito."),
 S(12, "Due: tra il [2000|duemila] e il [2002|duemiladue] il gruppo emette sette obbligazioni dal Lussemburgo, per un miliardo e centoventicinque milioni, che arrivano a circa trentacinquemila risparmiatori."),
 S(12, "Tre: nel novembre [2002|duemiladue] un bond da centocinquanta milioni non viene rimborsato, e il default trascina tutti gli altri. Quattro: nel [2003|duemilatré] arriva l'amministrazione straordinaria."),
 S(12, "Cinque: per i giudici quei titoli furono venduti quando il gruppo era già in crisi. Sei: Sergio Cragnotti è condannato in via definitiva nel [2021|duemilaventuno] a cinque anni e tre mesi."),
 S(12, "E tu, avresti comprato un'obbligazione solo perché portava il nome di una marca famosa? Scrivilo nei commenti. Le fonti sono tutte nella descrizione."),
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
