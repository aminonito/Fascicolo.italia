from fi import *
W, H = 1080, 1920
def build(i, dur, a, words):
    T = Clock(words, a); sc = Scene(dur)
    if i == 0:
        sc.add(Fingerprint((540, 840), 380, a, None, (220, 210, 196)))
        sc.add(Text("Avevano la sua\n*impronta*", (540, 380), a, size=96, anchor="ma", align="m"))
        sc.add(Stamp("NON L'HANNO\nPRESO", (540, 1270), T("Eppure"), size=74, rot=-8))
    elif i == 1:
        sc.add(Text("AGOSTO 1911 · LOUVRE", (540, 420), a, size=50, fnt=TYPE, color=GOLD, anchor="ma", typewriter=True))
        sc.add(Frame((540, 900), 310, 450, a + 0.1, None, vanish=T("sparisce") + 0.3))
        sc.add(Text("sulla cornice:\nun'impronta del *pollice*", (540, 1230), T("Sulla"), size=56, fnt=PS, anchor="ma", align="m"))
    elif i == 2:
        card = id_card(860, 700, [("NOME", "Vincenzo Peruggia"), ("ANNO", "1909"), ("CITTÀ", "Parigi"), ("NOTE", "foto e impronte")])
        sc.add(Img(card, (540, 900), a, anim="drop", rot=-2), "paper")
        sc.add(Text("già *schedato* nel 1909", (540, 400), a + 0.2, size=70, anchor="ma"))
        sc.add(Stamp("SCHEDATO", (760, 640), T("impronte"), size=60, rot=10))
    elif i == 3:
        sc.add(Text("archivio ordinato\ncon il *sistema Bertillon*", (540, 380), a, size=66, anchor="ma", align="m"))
        sc.add(CardGrid((90, 620, 990, 1220), a + 0.2, None, 9, 10, scan=dur - 1.5))
        sc.add(Text("migliaia di schede, *a mano*", (540, 1270), T("Confrontarla"), size=50, fnt=PS, anchor="ma"))
    elif i == 4:
        sc.add(Text("Lo interrogano\n*a casa sua*", (540, 400), a, size=90, anchor="ma", align="m"))
        sc.add(Trunk((540, 1000), 520, T("quadro")), "paper")
        sc.add(Stamp("NON TROVATA", (540, 1000), T("trovano"), size=80, rot=-10))
    elif i == 5:
        sc.add(Text("Come è stato\n*preso*?", (540, 500), a, size=110, anchor="ma", align="m"))
        sc.add(Text("Storia completa su YouTube", (540, 860), T("storia"), size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(90), (540, 1050), T("Fascicolo"), anim="pop", shadow=False), "hit")
    sc.footer = "Ricostruzione · fonti: CrimeReads, Advance.hr, Auralcrave"
    return sc
