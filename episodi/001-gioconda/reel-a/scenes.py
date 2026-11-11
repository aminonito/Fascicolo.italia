from fi import *
W, H = 1080, 1920
PBOX = (110, 570, 970, 1210)
ROOMS = [(0.02, 0.70, 0.30, 0.97, "Ingresso\noperai"), (0.02, 0.03, 0.46, 0.40, "Salon\nCarré", True, 32),
         (0.52, 0.03, 0.74, 0.62, "Scala di\nservizio", False, 26), (0.76, 0.50, 0.84, 0.62, ""), (0.86, 0.22, 0.995, 0.97, "Cortile", False, 26)]
P_SC = [(0.18, 0.30), (0.46, 0.30), (0.56, 0.30)]
P_DOWN = [(0.56, 0.30), (0.56, 0.56), (0.76, 0.56)]
P_OUT = [(0.76, 0.56), (0.885, 0.56), (0.885, 0.94)]
def build(i, dur, a, words):
    T = Clock(words, a); sc = Scene(dur)
    if i == 0:
        sc.add(Frame((540, 1060), 300, 436, a, None, vanish=a + 0.9))
        sc.add(Text("È uscito\ngrazie a un\n*dipendente*\ndel museo", (540, 420), T("grazie"), size=90, anchor="ma", align="m"))
        sc.add(Stamp("CASO 001", (800, 1230), T("museo"), size=70, rot=-10))
    elif i == 1:
        sc.add(Text("PARIGI · 21 AGOSTO 1911", (540, 430), a, size=50, fnt=TYPE, color=GOLD, anchor="ma", typewriter=True))
        sc.add(Text("museo *chiuso*", (540, 530), T("chiuso"), size=70, anchor="ma"))
        sc.add(Frame((540, 1000), 300, 436, a + 0.2, None, vanish=T("stacca") + 0.4, label="Salon Carré"))
        sc.add(Text("un uomo in *camice bianco*", (540, 1250), T("camice"), size=50, fnt=PS, anchor="ma"))
    elif i == 2:
        sc.add(Text("Toglie *cornice e vetro*", (540, 380), a, size=66, anchor="ma"))
        sc.add(Plan(PBOX, ROOMS, a, None, [(P_SC, a + 0.2, 1.8)], [((0.56, 0.14), "", T("cornice"), "x")]))
    elif i == 3:
        sc.add(Text("Porta *chiusa a chiave*", (540, 380), a, size=66, anchor="ma"))
        sc.add(Plan(PBOX, ROOMS, a, None, [(P_SC, -9, .1), (P_DOWN, a + 0.1, 1.4), (P_OUT, T("apre"), 1.4)],
                    [((0.80, 0.42), "", T("chiusa"), "lock")]))
        sc.add(Stamp("L'IDRAULICO\nGLI APRE", (540, 1300), T("apre") + 0.2, size=64, rot=-6))
    elif i == 4:
        sc.add(Img(person_card("V. PERUGGIA", "decoratore italiano", 380, 3), (540, 820), a, anim="drop"), "paper")
        sc.add(Text("Vincenzo *Peruggia*", (540, 400), a, size=80, anchor="ma"))
        sc.add(Big("28 mesi", (540, 1200), T("nascosta"), size=120, color=GOLD, fnt=OSW, sub="la Gioconda resta nascosta"))
    elif i == 5:
        sc.add(Text("Come l'hanno\n*ritrovata*?", (540, 500), a, size=100, anchor="ma", align="m"))
        sc.add(Text("Storia completa su YouTube", (540, 860), T("storia"), size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(90), (540, 1050), T("Fascicolo"), anim="pop", shadow=False), "hit")
    sc.footer = "Ricostruzione · fonti: History.com, The Week, CrimeReads"
    return sc
