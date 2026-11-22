STYLE = "fascicolo"
CASE = "FASCICOLO N. 020 · IL TOTONERO"
TITLE = "Il Totonero"
CH = ["INTRO", "1 · L'ITALIA DEL PALLONE NEL 1980", "2 · I PROTAGONISTI", "3 · COME NASCE IL GIRO", "4 · LE PARTITE DELL'INVERNO",
      "5 · LA DENUNCIA", "6 · DOMENICA 23 MARZO", "7 · IL PROCESSO SPORTIVO", "8 · IL PROCESSO PENALE", "9 · PAOLO ROSSI",
      "10 · LE DOMANDE APERTE", "11 · LA LEZIONE", "IL VERDETTO"]
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

Y80 = "[1980|millenovecentottanta]"
Y79 = "[1979|millenovecentosettantanove]"
Y82 = "[1982|millenovecentottantadue]"
Y74 = "[1974|millenovecentosettantaquattro]"
Y89 = "[1989|millenovecentottantanove]"
Y86 = "[1986|millenovecentottantasei]"
Y70 = "[1970|millenovecentosettanta]"
ISTAT = "[ISTAT|ìstat]"

SCENES_H = [
 # ------------------------------------------------------------------ INTRO
 S(0, f"Domenica 23 marzo {Y80}. Sono le cinque del pomeriggio. Le partite di serie A stanno finendo, e milioni di italiani sono davanti alla radio o alla televisione per sapere i risultati."),
 S(0, "Ma quel pomeriggio, a bordo campo, ci sono anche le auto delle forze dell'ordine. E davanti alle telecamere della televisione pubblica alcuni calciatori vengono portati via. Tra gli arrestati c'è perfino il presidente del Milan."),
 S(0, "Tutto è partito da due uomini di Roma: un ristoratore e il suo fornitore di frutta e verdura. Scommettevano di nascosto sulle partite. E alla fine hanno denunciato proprio i calciatori."),
 S(0, f"In questo fascicolo vedremo come funzionava il giro delle scommesse clandestine, le partite finite nel mirino, la domenica degli arresti, i due processi con esiti opposti, e la storia di Paolo Rossi: squalificato nel {Y80}, campione del mondo nel {Y82}."),
 # ------------------------------------------------------------------ 1 · L'ITALIA DEL PALLONE
 S(1, f"Partiamo dall'epoca. Siamo alla fine degli anni Settanta. Il calcio è lo sport nazionale, e la domenica pomeriggio è il suo rito: tutte le partite di serie A si giocano nello stesso momento, alle tre."),
 S(1, "Non ci sono le partite in diretta su ogni canale. I gol si ascoltano alla radio, e i servizi arrivano in televisione a fine pomeriggio, con le immagini dai campi. Quella trasmissione, quella domenica, sarà decisiva."),
 S(1, "Per scommettere sul calcio, in Italia, c'è una sola strada legale: il concorso a pronostici dello Stato, la schedina. Si indovinano i risultati di tante partite tutte insieme, e truccarne una sola non basta a vincere."),
 S(1, "Scommettere sul risultato di una singola partita, invece, è vietato. Chi vuole farlo deve rivolgersi agli allibratori clandestini, che raccolgono le puntate fuori da ogni regola."),
 S(1, "Ed è da qui che nasce il soprannome dello scandalo. Il concorso legale si chiama Totocalcio. Il suo gemello illegale, quello delle scommesse in nero, viene chiamato Totonero."),
 S(1, "C'è un altro dettaglio da tenere a mente, perché tornerà alla fine della storia. Nel codice penale di allora non c'è un reato specifico per chi trucca una partita di calcio."),
 S(1, "Esiste la giustizia sportiva, quella della federazione, che può squalificare i giocatori e punire le società. Ma per la giustizia ordinaria, comprare un risultato non è, di per sé, un reato."),
 S(1, f"Teniamo a mente anche la cornice. Nel {Y80} l'Italia ospita il campionato europeo di calcio, a giugno. Il pallone è al centro dell'attenzione del Paese, e la nazionale è attesa da tutti."),
 S(1, "In questo mondo si muovono i nostri protagonisti. Non sono dirigenti né campioni. Sono due commercianti romani che, a un certo punto, decidono di giocare una partita molto più rischiosa di quelle che si vedono in campo."),
 S(1, "Prima di conoscerli, una regola di questo fascicolo. Diciamo solo ciò che risulta da almeno due fonti, e distinguiamo sempre tra le sanzioni della giustizia sportiva e le sentenze dei tribunali. In questo caso, come vedremo, sono molto diverse."),
 # ------------------------------------------------------------------ 2 · I PROTAGONISTI
 S(2, "Apriamo la bacheca. Il primo nome è Alvaro Trinca. È un ristoratore romano. Il suo locale si chiama La Lampara, e si trova vicino a piazza del Popolo, nel centro di Roma."),
 S(2, "Il ristorante è frequentato da molti calciatori, soprattutto della Lazio. Trinca li conosce, ci parla, ne diventa amico. Secondo le ricostruzioni, alcuni di loro lo invitano persino al suo matrimonio."),
 S(2, "Il secondo nome è Massimo Cruciani. Le fonti lo descrivono come un commerciante all'ingrosso di frutta e verdura: è il fornitore del ristorante di Trinca. Tra i due nasce un'amicizia, e poi una specie di società."),
 S(2, "Terzo posto in bacheca: gli allibratori clandestini. Non hanno un volto e non faremo nomi. Sono loro che raccolgono le puntate e che, quando si perde, pretendono di essere pagati."),
 S(2, "Poi ci sono i calciatori. Nella denuncia i due ne nomineranno ventisette, secondo la maggior parte delle ricostruzioni, tra serie A e serie B. Ne citeremo pochissimi, e solo per ciò che risulta dalle decisioni ufficiali."),
 S(2, "Il primo è Felice Colombo, presidente del Milan. La giustizia sportiva lo radierà, cioè lo escluderà dal mondo del calcio. Vedremo perché."),
 S(2, f"Il secondo è Enrico Albertosi, portiere del Milan ed ex portiere della nazionale, secondo ai Mondiali del {Y70}. Sarà squalificato per quattro anni."),
 S(2, "Il terzo è Paolo Rossi, attaccante del Perugia. Non sarà arrestato, ma riceverà un ordine di comparizione e poi una squalifica. Si è sempre dichiarato innocente. La sua storia avrà un capitolo tutto suo."),
 S(2, "Infine, gli ultimi due nomi della bacheca non sono persone, ma istituzioni: la procura di Roma, che indaga per la giustizia ordinaria, e gli organi della federazione, che giudicano per quella sportiva."),
 S(2, "Lo diciamo subito, perché è la chiave di tutto: nel processo penale gli imputati saranno assolti. Le pene di cui parleremo sono sanzioni sportive, non condanne penali."),
 # ------------------------------------------------------------------ 3 · COME NASCE IL GIRO
 S(3, f"Come nasce il giro? Secondo il racconto fatto poi dallo stesso Trinca, tutto comincia nel {Y74}. In una sola settimana viene avvicinato più volte da scommettitori clandestini: al ristorante, in un bar sotto casa, in via Veneto."),
 S(3, "Il motivo è semplice. Trinca conosce i calciatori. E per chi scommette, conoscere chi gioca vale oro. Una voce di spogliatoio, un'informazione su chi è in forma: tutto può spostare una puntata."),
 S(3, "Nella seconda metà degli anni Settanta Trinca comincia a scommettere di nascosto. Coinvolge anche Cruciani. Ma i due, secondo le ricostruzioni, cominciano subito a perdere, e a perdere molto."),
 S(3, f"Nel {Y79}, secondo le ricostruzioni, i due cambiano strategia. Non vogliono più indovinare i risultati. Vogliono conoscerli in anticipo. E per farlo pensano di pagare alcuni giocatori."),
 S(3, "Vediamo lo schema, in modo semplificato. Da una parte ci sono gli scommettitori, cioè loro due. In mezzo, i contatti con i calciatori. Poi la partita. E alla fine gli allibratori, che pagano solo se il risultato è quello giocato."),
 S(3, "Il meccanismo, sulla carta, è questo: si promette denaro ad alcuni giocatori perché la partita finisca in un certo modo. Poi si punta forte su quel risultato con gli allibratori clandestini."),
 S(3, "Ma c'è un punto debole. In campo ci sono ventidue giocatori, un arbitro, gli imprevisti. Pochi calciatori non possono garantire un risultato. E se la partita va diversamente, la puntata è persa."),
 S(3, "Ed è proprio quello che succede. Secondo le ricostruzioni, nelle partite su cui puntano, le cose spesso non vanno come era stato promesso. Il gol arriva quando non dovrebbe. Il pareggio non arriva."),
 S(3, f"Il primo tentativo, secondo le fonti, riguarda un'amichevole tra Palermo e Lazio, nell'autunno del {Y79}. Ma le versioni non coincidono né sulla data né sull'esito delle scommesse: lo segnaliamo e andiamo avanti."),
 S(3, "Fermiamoci sul nome del giro. Totonero. Il nero è il denaro che non passa dai canali ufficiali: niente ricevute, niente tasse, niente controlli. E niente tutele, quando le cose vanno male."),
 S(3, "Perché con un allibratore clandestino non si può fare causa. Se perdi, paghi. E se non paghi, il debito resta. È un dettaglio che spiega quello che i due faranno qualche mese dopo."),
 S(3, "Riepiloghiamo la catena: i due scommettitori, il ristorante come punto d'incontro, alcuni calciatori, la partita, gli allibratori. Ogni anello può rompersi. E nell'inverno del 1980 si rompono quasi tutti."),
 # ------------------------------------------------------------------ 4 · LE PARTITE DELL'INVERNO
 S(4, f"Entriamo nel campionato [1979-80|settantanove-ottanta]. Le indagini si concentreranno su alcune partite di serie A di quella stagione. La prima che diventa un simbolo è Milan-Lazio, giocata il 6 gennaio {Y80}."),
 S(4, "Finisce due a uno per il Milan. Ed è la partita che costerà più cara al presidente rossonero. Secondo le ricostruzioni, intorno a quella gara qualcuno propone una combine."),
 S(4, "Dopo la partita, secondo il racconto riportato dalle fonti, qualcuno chiede un compenso, perché il Milan ha vinto. E il presidente Colombo decide di pagare."),
 S(4, "La somma, secondo le ricostruzioni, è di venti milioni di lire. Il denaro arriva a Roma attraverso un giocatore del Milan, Giorgio Morini. Le fonti non concordano sui dettagli del passaggio di mano."),
 S(4, f"Quanto valgono venti milioni del {Y80}? Con i coefficienti {ISTAT} sul valore della moneta, circa cinquantottomila euro di oggi. Non una fortuna, ma abbastanza per costare carissimo al Milan."),
 S(4, "Una settimana dopo arriva la domenica decisiva per i due scommettitori. È il 13 gennaio. Secondo le ricostruzioni, Trinca e Cruciani puntano centosettantasette milioni di lire su quattro partite insieme."),
 S(4, "Se tutto va come previsto, sperano di incassare un miliardo e trecentocinquanta milioni. Le fonti chiamano questa giocata una martingala: tutto su un'unica combinazione."),
 S(4, f"Facciamo i conti con i coefficienti {ISTAT}. La puntata vale circa cinquecentodiciassettemila euro di oggi. La vincita sperata, quasi quattro milioni di euro. Una scommessa enorme, per un ristoratore e un commerciante di frutta."),
 S(4, "Vediamo le quattro partite sul tabellone. Lazio-Avellino: secondo l'accordo, deve vincere la Lazio. Bologna-Juventus e Genoa-Palermo: due pareggi. E Pescara-Inter, una partita pulita, su cui puntano la vittoria dell'Inter."),
 S(4, "Ma la prima riga salta subito. Lazio-Avellino finisce uno a uno. La Lazio pareggia invece di vincere. E con una sola riga sbagliata, la martingala intera è perduta."),
 S(4, "Su Bologna-Juventus, invece, i giudici sportivi stabiliranno che non c'è stata alcuna combine. Lo diciamo chiaramente: per quella partita la Juventus non è stata punita."),
 S(4, "Ora i due sono nei guai. Hanno debiti con gli allibratori. E provano a recuperare con un'ultima partita combinata: Bologna-Avellino. Secondo le ricostruzioni, l'accordo è per un pareggio."),
 S(4, "Bologna-Avellino finisce uno a zero per il Bologna. Niente pareggio. Trinca e Cruciani, secondo le fonti, perdono tutto."),
 S(4, f"Ma le partite finite nel mirino sono di più. Oltre a quelle viste, le inchieste guarderanno anche ad Avellino-Perugia e ad altre gare della stagione [1979-80|settantanove-ottanta]."),
 S(4, "Avellino-Perugia, finita due a due, sarà la partita di Paolo Rossi. Per ora segniamola sul tabellone. Ci torneremo nel capitolo che porta il suo nome."),
 S(4, "Riepilogo per chi entra adesso. Due scommettitori romani pagano, secondo il loro racconto, alcuni calciatori per truccare le partite. Ma i risultati non tornano. E i debiti crescono, una domenica dopo l'altra."),
 # ------------------------------------------------------------------ 5 · LA DENUNCIA
 S(5, "Quanto devono, alla fine? Secondo le ricostruzioni, i debiti con gli allibratori clandestini arrivano a novecentocinquanta milioni di lire."),
 S(5, f"Con i coefficienti {ISTAT}, sono circa due milioni e settecentottantamila euro di oggi. Un debito impossibile da pagare per due commercianti. E con creditori che non si possono portare in tribunale."),
 S(5, "Così i due fanno una mossa che nessuno si aspetta. Invece di nascondersi, vanno dalla giustizia. E accusano i calciatori."),
 S(5, f"Il primo marzo {Y80} Trinca e Cruciani presentano un esposto alla procura della Repubblica di Roma. La loro tesi è questa: i calciatori hanno preso i soldi per truccare le partite, e poi non hanno rispettato i patti."),
 S(5, "In altre parole, i due si presentano come vittime di una truffa. Truffati da chi avrebbe dovuto perdere, o pareggiare, e invece ha giocato. Un paradosso che i giornali notano subito."),
 S(5, "Nell'esposto ci sono nomi e cognomi. Ventisette calciatori secondo la maggior parte delle fonti, una trentina secondo altre. Di serie A e di serie B, e di diverse squadre."),
 S(5, "Nei giorni successivi i nomi finiscono sui giornali. E il caso esplode. Le voci su partite aggiustate giravano già da settimane: ora c'è una denuncia scritta, depositata in procura."),
 S(5, "Il 4 marzo un giornale pubblica l'intervista a un centrocampista della Lazio, Maurizio Montesi. Racconta di aver ricevuto offerte per truccare una partita. E di averle rifiutate."),
 S(5, "Secondo il suo racconto, per non scendere in campo avrebbe perfino simulato un infortunio. Anche lui, più avanti, riceverà una squalifica di alcuni mesi. Ma la sua intervista conferma che il giro esiste."),
 S(5, "La procura di Roma comincia a lavorare. Interroga i due scommettitori, raccoglie i loro racconti, ricostruisce le partite. E prepara una mossa che nessuno, nel mondo del calcio, si aspetta."),
 S(5, "Intanto il campionato va avanti, domenica dopo domenica. I calciatori accusati continuano a giocare. Le tribune si riempiono, la schedina si compila. Fino al 23 marzo."),
 S(5, "Prima di arrivarci, notiamo una cosa. L'accusa formale, quella di cui parlano i giornali di allora, è di truffa aggravata. È l'unica strada che il codice offre. E questo, come vedremo, peserà sul finale."),
 # ------------------------------------------------------------------ 6 · DOMENICA 23 MARZO
 S(6, "Domenica 23 marzo 1980. Si gioca la ventiquattresima giornata di serie A. Le partite cominciano tutte alla stessa ora, le tre del pomeriggio."),
 S(6, "Gli arresti potevano essere fatti in qualunque momento: a casa, all'alba, lontano dai riflettori. Invece arrivano negli stadi, alla fine delle partite, mentre le telecamere sono accese."),
 S(6, "Chi entra negli stadi? Le fonti non coincidono del tutto: parlano di Guardia di Finanza, di polizia e di carabinieri. Diciamo forze dell'ordine, e mostriamo auto e divise in modo generico."),
 S(6, "Verso le cinque, al fischio finale, le auto di servizio sono a bordo campo e davanti agli spogliatoi. Gli uomini in divisa aspettano i calciatori indicati nell'ordine di cattura."),
 S(6, "La trasmissione della domenica pomeriggio della televisione pubblica, quella dei collegamenti dai campi, manda in onda le immagini degli arresti. Il Paese le vede in diretta, o quasi."),
 S(6, "Andiamo sui campi. A Pescara gioca la Lazio. Lì, a fine partita, vengono arrestati quattro giocatori laziali. Non faremo i loro nomi."),
 S(6, "Gli arresti del Milan riguardano il presidente Felice Colombo, il portiere Enrico Albertosi e Giorgio Morini. Il presidente di una delle squadre più famose d'Italia esce dallo stadio con le forze dell'ordine."),
 S(6, "Altri arresti riguardano giocatori di Avellino, Perugia, Palermo, Genoa e Lecce. Tra quella domenica e i giorni successivi, gli arresti salgono a tredici calciatori, secondo la maggior parte delle fonti."),
 S(6, "Le cifre non coincidono del tutto: una fonte parla di nove calciatori di serie A arrestati quel giorno, altre di dodici o tredici in tutto. Il quadro, comunque, è chiaro: è la domenica più nera del calcio italiano."),
 S(6, "Altri calciatori ricevono un ordine di comparizione, cioè la convocazione dai magistrati. Tra loro c'è Paolo Rossi, attaccante del Perugia. Non viene arrestato: deve presentarsi per essere interrogato."),
 S(6, "L'accusa per gli arrestati è truffa aggravata. Il giorno dopo lo scandalo è su tutte le prime pagine."),
 S(6, "Per il pubblico è uno shock. I campioni della domenica, quelli delle figurine e della schedina, escono dagli stadi accompagnati dalle forze dell'ordine. Il calcio italiano non era mai finito così in cronaca."),
 S(6, "Facciamo un piccolo conto dei tempi. Dall'esposto del primo marzo agli arresti del 23 marzo passano ventidue giorni. Meno di un mese per trasformare un debito di gioco nel più grande scandalo del calcio italiano fino ad allora."),
 S(6, "Secondo riepilogo. Due scommettitori pieni di debiti denunciano i calciatori. Ventidue giorni dopo, gli arresti negli stadi, davanti alle telecamere. Ora la parola passa ai giudici. Anzi, a due tipi di giudici."),
 S(6, "Se questo fascicolo ti sta piacendo, iscriviti a Fascicolo Italia: ogni giorno un nuovo caso."),
 # ------------------------------------------------------------------ 7 · IL PROCESSO SPORTIVO
 S(7, "Il calcio ha la sua giustizia. Non decide sul carcere, ma su chi può giocare, su chi resta in serie A, su chi può guidare una società. E agisce in fretta, perché il campionato non può aspettare."),
 S(7, "Il processo sportivo comincia a maggio del 1980. La prima sentenza arriva nello stesso mese. Per il Milan è un terremoto: la squadra è condannata alla retrocessione in serie B."),
 S(7, "È la prima retrocessione nella storia del Milan. E non arriva per i risultati del campo, ma per una sentenza."),
 S(7, "In primo grado la Lazio se la cava con una multa di dieci milioni di lire. Ma a luglio arriva la sentenza d'appello. E la Lazio viene retrocessa anche lei in serie B."),
 S(7, "Altre società vengono penalizzate. Avellino, Bologna e Perugia partiranno con cinque punti in meno nel campionato successivo. Penalità anche per alcune squadre di serie B."),
 S(7, "Poi i dirigenti. Felice Colombo, presidente del Milan, viene radiato, cioè escluso dal calcio. Il presidente del Bologna viene squalificato per un anno."),
 S(7, "E i calciatori. Le squalifiche finali vanno da pochi mesi a sei anni. La pena più alta, sei anni, tocca a un giocatore dell'Avellino. Non faremo il suo nome."),
 S(7, "Enrico Albertosi, il portiere del Milan, in primo grado viene radiato. In appello la sanzione diventa una squalifica di quattro anni."),
 S(7, "Paolo Rossi, in primo grado, riceve una squalifica di tre anni secondo la maggior parte delle fonti. In appello scende a due anni. È la sanzione con cui resterà fuori dal campo."),
 S(7, "Quanti sono, in tutto, i calciatori squalificati? Le fonti dicono diciotto o venti, a seconda di come si contano le sentenze di primo grado e quelle d'appello. Un'intera generazione di giocatori ferma per mesi o per anni."),
 S(7, "Le sentenze d'appello non vanno tutte nella stessa direzione. Per alcuni la squalifica aumenta, per altri diminuisce. È il segno di un processo difficile, partito in gran parte dalle denunce dei due scommettitori."),
 S(7, "Facciamo il punto sui numeri. Due squadre in serie B. Tre squadre di serie A con cinque punti di penalità. Un presidente radiato. Diciotto o venti calciatori squalificati."),
 S(7, "Il Milan giocherà in serie B la stagione successiva e risalirà subito in serie A. Ma la macchia, come si diceva allora, resta."),
 S(7, "Intanto, in estate, l'Italia ospita gli Europei. Senza Paolo Rossi, escluso per l'inchiesta. Il torneo di casa si gioca con l'ombra dello scandalo ancora addosso."),
 S(7, "Ora una domanda. Se la giustizia sportiva ha punito così duramente, cosa farà quella ordinaria, con un'accusa di truffa aggravata? La risposta arriva prima di Natale."),
 # ------------------------------------------------------------------ 8 · IL PROCESSO PENALE
 S(8, "Torniamo a Roma, in tribunale. Gli imputati sono accusati di truffa aggravata e di concorso in truffa. Il processo penale si celebra davanti al tribunale di Roma."),
 S(8, "Ma qui c'è il problema di cui abbiamo parlato all'inizio. Per il codice di allora, truccare una partita di calcio non è un reato specifico. E la truffa ha bisogno di condizioni precise per esistere."),
 S(8, "Pensiamoci un momento. Chi sarebbe la vittima della truffa? Due scommettitori che pagavano per conoscere il risultato in anticipo, e scommettevano con allibratori illegali. Non è un caso semplice da portare in un'aula."),
 S(8, f"Il 23 dicembre {Y80} arriva la sentenza del tribunale di Roma. Tutti gli imputati vengono assolti. La formula è la più netta: perché il fatto non sussiste."),
 S(8, "Il fatto non sussiste significa che, per i giudici, il reato contestato non c'è. Non è una questione di prove insufficienti. È la fattispecie, cioè la descrizione del reato, che non si adatta a quei fatti."),
 S(8, "Così nasce il paradosso del Totonero. Per la giustizia sportiva ci sono squadre retrocesse, un presidente radiato, calciatori fermi per anni. Per quella penale, nessun colpevole."),
 S(8, "Le due giustizie non si contraddicono davvero: giudicano cose diverse. Quella sportiva giudica la lealtà delle gare e il rispetto delle regole della federazione. Quella penale giudica i reati previsti dalla legge."),
 S(8, f"Il vuoto, però, resta. E viene colmato quasi dieci anni dopo. Il 13 dicembre {Y89} il Parlamento approva la legge numero quattrocentouno, sul gioco e le scommesse clandestine."),
 S(8, "L'articolo uno della legge si intitola: frode in competizioni sportive. Punisce chi offre o promette denaro a un partecipante di una gara per ottenere un risultato diverso da quello leale. E punisce anche chi accetta."),
 S(8, "La stessa legge punisce anche chi organizza scommesse abusive, cioè fuori dai canali autorizzati dallo Stato. In pratica, mette nero su bianco i due pezzi del Totonero: la partita truccata e la scommessa clandestina."),
 S(8, "Da quel momento, chi compra una partita rischia non solo la squalifica, ma anche un processo penale. Le due strade restano separate, ma ora entrambe hanno uno strumento per intervenire."),
 S(8, f"Facciamo il conto. Dagli arresti del {Y80} alla legge del {Y89} passano più di nove anni. Nel frattempo, nel {Y86}, il calcio italiano conoscerà un secondo scandalo legato alle scommesse."),
 S(8, "Terzo riepilogo. Processo sportivo: pene pesanti, a maggio e luglio del 1980. Processo penale: tutti assolti a dicembre, perché il fatto non sussiste. E nel 1989 arriva la legge che rende reato la frode sportiva."),
 # ------------------------------------------------------------------ 9 · PAOLO ROSSI
 S(9, "E adesso il capitolo di Paolo Rossi. Nel 1980 è uno degli attaccanti più famosi d'Italia. Gioca nel Perugia ed è già un nome della nazionale."),
 S(9, "Il suo nome entra nell'inchiesta per una partita: Avellino-Perugia della stagione [1979-80|settantanove-ottanta], finita due a due. L'accusa è di aver concordato il pareggio."),
 S(9, "Rossi ha sempre negato. Il suo racconto è questo: prima della partita, nell'albergo del ritiro del Perugia, ha incontrato due persone. Quando ha capito le loro intenzioni, ha interrotto subito la conversazione."),
 S(9, "Non viene arrestato. Riceve un ordine di comparizione per concorso in truffa. Ma l'inchiesta basta a tenerlo fuori dalla nazionale per gli Europei di casa."),
 S(9, "Poi arriva la giustizia sportiva. Tre anni in primo grado secondo la maggior parte delle fonti, ridotti a due in appello. Per un attaccante nel pieno della carriera, due anni senza giocare sono un'eternità."),
 S(9, "Rossi non accetta la sentenza in silenzio. Nel 1981 definisce il primo processo sportivo una buffonata. E per quelle parole si prende un altro mese di squalifica."),
 S(9, "Intanto succede una cosa sorprendente. La Juventus lo acquista, nonostante la squalifica. Rossi si allena con la squadra senza poter giocare le partite ufficiali."),
 S(9, f"Alla fine il ricorso di Rossi viene accolto dalla commissione d'appello federale, e la squalifica termina a fine aprile del {Y82}. Mancano poche giornate alla fine del campionato."),
 S(9, "Nelle ultime partite segna subito, contro l'Udinese. Gioca solo tre gare in tutto. Pochissime, per pensare a un Mondiale."),
 S(9, "Eppure il commissario tecnico della nazionale, Enzo Bearzot, lo convoca per i Mondiali di Spagna. E lo preferisce ad attaccanti che avevano segnato molto di più in quella stagione."),
 S(9, "All'inizio del torneo Rossi sembra lontano dalla forma: nelle prime partite non segna. Le critiche sono durissime, sia per lui sia per l'allenatore."),
 S(9, "Poi arriva la partita con il Brasile, nel secondo turno. Rossi segna tre gol. E l'Italia elimina la squadra favorita."),
 S(9, "In semifinale contro la Polonia segna altri due gol. In finale, a Madrid, contro la Germania Ovest, segna ancora. L'Italia è campione del mondo."),
 S(9, "Paolo Rossi è il capocannoniere del Mondiale. Due anni prima era squalificato. Pochi mesi dopo vince anche il Pallone d'oro, terzo italiano nella storia."),
 S(9, "C'è un altro effetto del Mondiale. Meno di tre settimane dopo la vittoria, il consiglio federale concede un'amnistia sportiva. Nove calciatori squalificati per il Totonero tornano a giocare, tra loro Enrico Albertosi."),
 S(9, "Paolo Rossi, invece, la sua squalifica l'aveva già scontata tutta. Non ha avuto bisogno dell'amnistia. È morto nel dicembre 2020, a sessantaquattro anni. E fino alla fine ha detto di essere stato accusato ingiustamente."),
 # ------------------------------------------------------------------ 10 · LE DOMANDE APERTE
 S(10, "Arriviamo alle domande aperte. Perché un caso chiuso da decenni lascia ancora punti che le fonti raccontano in modo diverso."),
 S(10, "Prima domanda: come è cominciato tutto? Alcune ricostruzioni partono dal 1974, quando Trinca viene avvicinato dagli scommettitori. Altre fissano l'inizio del piano nel 1979. Le due cose possono convivere, ma le date non coincidono."),
 S(10, "Seconda domanda: la prima partita truccata. Un'amichevole tra Palermo e Lazio nell'autunno del 1979: per una fonte finisce come previsto, per un'altra le scommesse non vengono nemmeno pagate. Le versioni non coincidono."),
 S(10, "Terza domanda: quanti furono gli arrestati? Nove, dodici, tredici calciatori: dipende da quale giorno si conta e da quale fonte si legge. E chi entrò negli stadi? Le fonti citano corpi diversi."),
 S(10, "Quarta domanda: le squalifiche. Per alcuni giocatori le fonti riportano la radiazione, per altri anni di squalifica. Spesso la differenza sta tra primo grado e appello. Per Rossi, quasi tutte dicono tre anni ridotti a due."),
 S(10, "Quinta domanda: quanto pesavano davvero i racconti dei due scommettitori? Erano accusatori e, allo stesso tempo, protagonisti del giro. Le loro parole sono state la base dell'inchiesta. Ma non tutte hanno retto davanti ai giudici sportivi."),
 S(10, "Sesta domanda: il metodo. Arrestare i calciatori negli stadi, davanti alle telecamere, invece che a casa, fu una scelta giusta? È una domanda che riguarda il modo di fare giustizia, non solo il calcio."),
 S(10, "E infine la domanda più grande: perché nel 1980 non c'era una legge contro le partite truccate? Forse perché nessuno pensava che servisse. Il Totonero ha dimostrato il contrario."),
 # ------------------------------------------------------------------ 11 · LA LEZIONE
 S(11, "Che cosa ci insegna oggi questa storia? Le scommesse sportive sono legali e diffuse, sul telefono, a qualunque ora. Proprio per questo, alcune regole del 1980 valgono ancora. Eccone cinque."),
 S(11, "Primo: scommettere solo su siti e punti autorizzati dallo Stato. Chi gioca con operatori illegali non ha alcuna tutela. Lo hanno scoperto anche i due protagonisti di questa storia."),
 S(11, "Secondo: diffidare di chi vende la partita sicura. Nel calcio i risultati certi non esistono. Lo dimostrano proprio le combine del Totonero, fallite una dopo l'altra."),
 S(11, "Terzo: chi gioca, o lavora nello sport, non deve scommettere sulle gare a cui partecipa. Le regole sportive lo vietano. E anche una semplice confidenza può diventare un problema."),
 S(11, "Quarto: le perdite non si inseguono. Puntare di più per recuperare è la strada che ha portato i due scommettitori a un debito di quasi un miliardo di lire."),
 S(11, "Quinto: se il gioco diventa un problema, chiedere aiuto. In Italia esistono servizi pubblici dedicati al gioco d'azzardo patologico. Parlarne presto è la scelta migliore."),
 S(11, "Questa non è una lezione contro il calcio. È una lezione sulla fiducia. Il pubblico guarda una partita perché crede che sia vera. Ed è quella fiducia che il Totonero aveva tradito."),
 # ------------------------------------------------------------------ IL VERDETTO
 S(12, "Ricapitoliamo il fascicolo. Uno: alla fine degli anni Settanta, a Roma, un ristoratore e un commerciante di frutta scommettono di nascosto sulle partite e, secondo il loro racconto, pagano alcuni calciatori."),
 S(12, f"Due: le combine falliscono, i debiti arrivano a novecentocinquanta milioni di lire, e il primo marzo {Y80} i due denunciano i calciatori. Tre: il 23 marzo gli arresti negli stadi, davanti alle telecamere."),
 S(12, "Quattro: la giustizia sportiva manda Milan e Lazio in serie B, radia il presidente del Milan e squalifica diciotto o venti calciatori. Cinque: il tribunale di Roma assolve tutti, perché il fatto non sussiste."),
 S(12, f"Sei: Paolo Rossi, squalificato per due anni e sempre dichiaratosi innocente, torna in campo nel {Y82} e trascina l'Italia al titolo mondiale. E nel {Y89} arriva la legge sulla frode sportiva."),
 S(12, "E tu che ne pensi? Era giusto punire così duramente con la giustizia sportiva, quando quella penale non aveva strumenti? Scrivilo nei commenti."),
 S(12, "Iscriviti a Fascicolo Italia: ogni giorno un nuovo caso."),
]

DROP = [13, 25, 63, 75, 104]   # tolte dopo la voce per stare sotto i 32 minuti
SCENES_H = [x for k, x in enumerate(SCENES_H) if k not in DROP]
SCENES = [p for _, p in SCENES_H]
HEADERS = [CH[h] for h, _ in SCENES_H]

def tokens(cl):
    out = []
    for m in re.finditer(r"\[([^|\]]*)\|([^\]]*)\]|(\S+)", cl):
        if m.group(3): out.append((m.group(3), m.group(3)))
        else: out.append((m.group(1), m.group(2)))
    return out
