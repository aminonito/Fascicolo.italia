import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fi import *
from fx import *
import fi
from anv import *

W, H = 1920, 1080
FY = 870
fi.PLACES.update({"Anversa": (4.40, 51.22), "Palermo": (13.36, 38.12), "Bruxelles": (4.35, 50.85), "Terreno": (4.42, 50.98)})
F_BASE = "Fonti: Wikipedia · National Geographic · Money.it · Forbes Italia"
CUT = (300, 190, 1620, 880)

def walk(pts, t0, speed=260):
    keys = [(t0, pts[0][0], pts[0][1])]; t = t0
    for p, q in zip(pts, pts[1:]):
        t += math.dist(p, q) / speed; keys.append((t, q[0], q[1]))
    return keys

def build(i, dur, a, words):
    T = Clock(words, a); sc = Scene(dur)
    if i == 0:
        ts = T("Sotto") - 0.3
        sc.add(Calendar((330, 470), 230, [(a, "FEBBRAIO", "2003")], a, ts), "paper")
        sc.add(MapEl((640, 200, 1820, 860), [(0, (4.4, 51.0), 160), (ts, (4.4, 51.0), 300)], a, ts,
                     pins=[dict(at="Anversa", label="Anversa", t=a + 0.3, side="r"), dict(at="Bruxelles", label="Bruxelles", t=T("Belgio"), side="r")],
                     title="mappa: Natural Earth"), "whoosh")
        tw = T("In") - 0.3
        cut = sc.add(Cutaway(CUT, ts, tw, hl=[(T("caveau"), "vault")]))
        sc.add(Pill("10 LIVELLI DI SICUREZZA", (960, 230), T("dieci"), tw, size=40, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (T("caveau") - 0.2, 960, 540, 1.0), (T("caveau") + 0.8, 960, 760, 1.35), (tw, 960, 760, 1.4), (tw + 0.3, 960, 540, 1.0), (dur, 960, 540, 1.03))
        tb = T("Un", 1) - 0.3
        sc.add(ClockFace((300, 420), 120, tw + 0.1, tb, start=20, speed=10, label="UN WEEKEND"), "pop")
        sc.add(Boxes((560, 220, 1820, 760), 14, 6, tw + 0.1, tb, open_t=T("svuota"), n_open=60, rate=22, counter=(1190, 830)))
        sc.add(Big("~100 milioni $", (960, 470), tb + 0.1, size=150, color=GOLD, fnt=OSW, count=(0, 100, lambda z: f"~{z:.0f} milioni $", 1.4), sub="bottino stimato · la cifra più citata"), "hit")
        for k in range(6):
            sc.add(AIcon("diamond", (960, 470), tb + 0.2 + 0.08 * k, size=110, move=(tb + 0.2 + 0.08 * k, 0.8, (330 + 250 * k, 760), 120)), "pop" if k % 2 == 0 else None)
        sc.footer = "Fonti: Wikipedia · National Geographic · Money.it · History Daily"
    elif i == 1:
        t1 = T("Viene") - 0.3
        sc.add(Figure(walk([(2100, FY), (1300, FY)], a, 500), a, T("Questo") - 0.3, kind="police", flip=-1, arms=[(T("polizia"), "point")]))
        sc.add(Icon("magnifier", (1300, 380), T("polizia"), t1, size=160), "pop")
        sc.add(Line((1180, 380), (1420, 380), T("polizia") + 0.4, t1, RED, 12, 0.3))
        sc.add(AIcon("trashbag", (520, 600), T("sacco") - 0.2, T("Questo") - 0.3, size=330), "pop")
        sc.add(Pill("UN SACCO DELLA SPAZZATURA", (520, 830), T("sacco"), T("Questo") - 0.3, size=34))
        sc.add(AIcon("sandwich", (960, 470), T("panino") - 0.2, T("Questo") - 0.3, size=300), "pop")
        sc.add(Pill("UN PANINO AL SALAME, A METÀ", (960, 680), T("panino"), T("Questo") - 0.3, size=34, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (T("panino"), 960, 540, 1.0), (T("panino") + 0.8, 960, 520, 1.25), (T("Questo") - 0.4, 960, 520, 1.28), (T("Questo") - 0.1, 960, 540, 1.0), (dur, 960, 540, 1.0))
        t3 = T("Vedremo") - 0.3
        cover = paper(520, 640, (196, 160, 104), 9, 0.7); d = ImageDraw.Draw(cover)
        d.rectangle([50, 110, 470, 310], fill=(232, 222, 200, 255), outline=INK + (255,), width=3)
        d.text((260, 145), "FASCICOLO N. 002", font=font(COUR, 32), fill=INK + (255,), anchor="ma")
        d.text((260, 200), "IL COLPO DI", font=font(TYPE, 38), fill=INK + (255,), anchor="ma")
        d.text((260, 248), "ANVERSA", font=font(TYPE, 54), fill=RED + (255,), anchor="ma")
        d.text((260, 360), "Belgio · febbraio 2003", font=font(COURR, 26), fill=INK + (255,), anchor="ma")
        t3 = T("superato") - 0.4
        sc.add(Img(cover, (960, 520), T("Questo"), t3, anim="drop", rot=-3), "paper")
        sc.add(Stamp("CASO 002", (1130, 300), T("fascicolo") + 0.2, t3, size=70, rot=-12))
        sc.add(Text("una banda\ndi *italiani*", (110, 430), T("banda"), t3, size=60, maxw=520))
        sc.add(AIcon("shield", (420, 470), T("superato") - 0.2, size=220, label="COME HANNO SUPERATO I 10 LIVELLI"), "pop")
        sc.add(AIcon("trashbag", (960, 470), T("errore"), size=220, label="L'ERRORE CHE LI HA TRADITI"), "pop")
        sc.add(AIcon("diamond", (1500, 470), T("diamanti") - 0.2, size=220, label="I DIAMANTI MAI RITROVATI"), "pop")
        sc.footer = F_BASE
    elif i == 2:
        tc = T("Vicino") - 0.3
        sc.add(Chapter("01", "La *fortezza*", a, tc))
        sc.add(AIcon("diamond", (960, 160 + 560), a + 0.4, tc, size=90), "pop")
        sc.add(MapEl((120, 190, 1100, 860), [(0, (4.4, 51.0), 160), (tc, (4.4, 51.0), 160), (tc + 2.0, "Anversa", 700), (dur, "Anversa", 760)], tc,
                     pins=[dict(at="Anversa", label="Anversa", t=tc + 0.4, side="r")], title="mappa: Natural Earth"), "whoosh")
        sc.add(Pill("QUARTIERE DEI DIAMANTI", (1460, 230), T("quartiere"), size=40, accent=True))
        for k in range(3):
            sc.add(AIcon("diamond", (1300 + k * 160, 400), T("pietre") + 0.12 * k, size=110), "pop")
        sc.add(Pill("DA TUTTO IL MONDO", (1460, 520), T("mondo") - 0.2, size=34))
        for k, (x, y) in enumerate([(1250, 640), (1460, 620), (1670, 650)]):
            sc.add(Icon("camera", (x, y), T("telecamere") + 0.15 * k, size=110), "pop")
        sc.add(Figure(walk([(2100, FY), (1460, FY)], T("sorveglianza") - 0.6, 500), T("sorveglianza") - 0.6, kind="guard", flip=-1, s=0.7, label="SORVEGLIANZA PRIVATA"))
        sc.footer = "Fonti: Forbes Italia · Wikipedia · National Geographic · mappa Natural Earth"
    elif i == 3:
        sc.add(Text("Il cuore\ndel *quartiere*", (40, 220), a, T("Ci") - 0.3, size=44, maxw=420))
        cut = sc.add(Cutaway(CUT, T("palazzo") - 0.2, hl=[(T("uffici"), "office"), (T("caveau"), "vault")]))
        sc.add(Pill("SCHUPSTRAAT 9 · ANVERSA", (1700, 260), T("numero"), T("sotterranei"), size=32, accent=True))
        o = cut.office()
        for k in range(3):
            sc.add(Figure([(0, o[0] + 40 + k * 70, o[3] - 4)], T("uffici") + 0.1 * k, T("sotterranei"), kind="suit", s=0.26), "pop")
        sc.add(Pill("UFFICI DI COMMERCIANTI", (1700, 400), T("commercianti") - 0.2, T("sotterranei"), size=30))
        scene_cam(sc, (0, 960, 540, 1.0), (T("sotterranei") - 0.1, 960, 540, 1.0), (T("sotterranei") + 1.2, 960, 720, 1.3), (dur, 960, 730, 1.32))
        sc.add(Pill("2 PIANI SOTTO LA STRADA", (960, 660), T("due") , size=26))
        sc.footer = "Fonti: Wikipedia · History Daily · schema semplificato, non in scala"
    elif i == 4:
        bx = sc.add(Boxes((140, 200, 1060, 860), 9, 6, a, open_t=None, hl=(T("Ogni"), 22)))
        sc.add(AIcon("diamond", (1250, 330), T("diamanti"), T("Ogni") - 0.2, size=170, label="DIAMANTI"), "pop")
        sc.add(AIcon("gold", (1480, 330), T("oro"), T("Ogni") - 0.2, size=170, label="ORO"), "pop")
        sc.add(Icon("crown", (1710, 330), T("gioielli"), T("Ogni") - 0.2, size=150, label="GIOIELLI"), "pop")
        sc.add(AIcon("key", (1290, 400), T("chiave"), T("Il", 0) if False else None, size=200, label="LA SUA CHIAVE"), "pop")
        sc.add(AIcon("dial", (1690, 400), T("combinazione"), size=190, label="LA SUA COMBINAZIONE"), "pop")
        sc.add(Stamp("TRA I PIÙ SICURI\nAL MONDO", (1480, 720), T("sicuri"), size=60, rot=-8, color=GOLD))
        scene_cam(sc, (0, 960, 540, 1.0), (T("Ogni") - 0.1, 960, 540, 1.0), (T("Ogni") + 0.8, 760, 560, 1.12), (dur, 900, 540, 1.04))
        sc.footer = "Fonti: History Daily · Forbes Italia · Wikipedia"
    elif i == 5:
        sc.add(Text("10 protezioni", (960, 165), a, size=58, anchor="ma"))
        sc.add(VaultDoor((960, 560), 175, T("porta") - 0.2, dial_t=T("combinazioni") - 0.5, dial_d=2.2, plates_t=T("campo")))
        sc.add(Pill("100+ MILIONI DI COMBINAZIONI", (960, 860 - 10), T("cento"), T("Telecamere"), size=30, accent=True))
        slots = [("camera", 250, 330, "TELECAMERE", T("Telecamere")), ("sensor", 470, 330, "CALORE", T("calore")),
                 ("sensor", 250, 620, "MOVIMENTO", T("movimento")), ("radar", 470, 620, "RADAR DOPPLER", T("radar")),
                 ("seismo", 1450, 330, "SENSORE SISMICO", T("sismico")), ("bulb", 1670, 330, "LUCE", T("luce")),
                 ("magnet", 1560, 620, "CAMPO MAGNETICO", T("campo"))]
        for nm, x, y, lab, tt in slots:
            if nm == "camera": sc.add(Icon("camera", (x, y), tt, size=130, label=lab), "pop")
            else: sc.add(Sensor(nm, (x, y), tt, size=130, label=lab), "pop")
        scene_cam(sc, (0, 960, 540, 1.0), (T("campo") - 0.1, 960, 540, 1.0), (T("campo") + 1.0, 1150, 500, 1.2), (dur, 1160, 500, 1.22))
        sc.footer = "Fonti: Wikipedia · History Daily · Money.it · La Capital"
    elif i == 6:
        tc = T("Si") - 0.3
        sc.add(Chapter("02", "L'*inquilino*", a, tc))
        sc.add(Text("Leonardo\n*Notarbartolo*", (110, 200), tc + 0.1, size=84, maxw=760))
        sc.add(Img(person_card("L. NOTARBARTOLO", "commerciante di gioielli", 300, 4), (330, 640), tc + 0.3, anim="drop", rot=-3), "paper")
        sc.add(MapEl((760, 190, 1820, 860), [(0, (10.5, 41.8), 75), (T("Ad") - 0.2, (10.5, 41.8), 75), (T("Ad") + 1.5, (6.0, 48.5), 75), (dur, (6.0, 48.5), 78)], tc + 0.1,
                     routes=[dict(pts=["Palermo", "Torino"], t=T("palermitano") + 0.3, d=1.4, icon="person"), dict(pts=["Torino", "Anversa"], t=T("Ad"), d=1.8, icon="person", color=GOLD)],
                     pins=[dict(at="Palermo", label="Palermo", t=T("palermitano"), side="r"), dict(at="Torino", label="Torino", t=T("Torino"), side="l"),
                           dict(at="Anversa", label="Anversa", t=T("Anversa"), side="r")], title="mappa: Natural Earth · percorso indicativo"), "whoosh")
        sc.add(Pill("COMMERCIO DI GIOIELLI", (1290, 240), T("commercio"), T("Ad") - 0.2, size=34))
        sc.add(Pill("SI PRESENTA COME COMMERCIANTE DI PIETRE", (1290, 240), T("presenta"), size=32, accent=True))
        sc.footer = "Fonti: Forbes Italia · Balarm · Money.it"
    elif i == 7:
        cut = sc.add(Cutaway((620, 190, 1840, 880), a, hl=[(T("ufficio"), "office"), (T("cassetta"), "vault")], path_t=T("scendere")))
        sc.add(Text("Una cosa *semplice*", (110, 200), a, T("Prende"), size=56))
        let = doc_typed(460, 400, "CONTRATTO D'AFFITTO", ["Locale: ufficio", "Palazzo: Diamond Center", "Inquilino:", "L. Notarbartolo", "Uso: commercio"], footer="contenuto indicativo", seed=12, size=28)
        sc.add(Img(let, (330, 470), T("affitto") - 0.1, T("inquilino") - 0.1, anim="drop", rot=-3), "paper")
        sc.add(Pill("+ UNA CASSETTA NEL CAVEAU", (330, 300), T("diritto"), size=32, accent=True))
        sc.add(AIcon("key", (330, 470), T("cassetta") - 0.1, size=200), "pop")
        o = cut.office()
        sc.add(Figure([(0, (o[0] + o[2]) / 2, o[3] - 4)], T("ufficio") + 0.2, T("scendere"), kind="suit", s=0.28), "pop")
        sc.add(Figure([(0, 330, FY)], T("occhi") - 0.3, kind="guard", s=0.75, label="LE GUARDIE"), "pop")
        sc.add(Figure([(0, 480, FY)], T("occhi") - 0.1, kind="guard", s=0.75), "pop")
        sc.footer = "Fonti: Wikipedia · National Geographic · Forbes Italia · documento: ricostruzione grafica"
    elif i == 8:
        ts = T("Secondo") - 0.3
        pages = [(a + 0.2 + 0.1 * k, "MESI", str(k + 1)) for k in range(24)]
        sc.add(Calendar((420, 470), 260, pages, a + 0.1, ts), "paper")
        sc.add(Pill("2 ANNI?", (1000, 380), T("due"), ts, size=60))
        sc.add(Pill("4 ANNI?", (1400, 380), T("quattro"), ts, size=60, accent=True))
        sc.add(Text("le fonti *non coincidono*", (1200, 560), T("fonti") , ts, size=50, anchor="ma"))
        sc.add(VaultDoor((1250, 600), 200, ts, dial_t=T("compongono") - 0.2, dial_d=2.4))
        sc.add(Pill("SECONDO L'ACCUSA", (420, 230), ts + 0.1, size=34, accent=True))
        sc.add(Icon("camera", (1250, 290), T("telecamera") - 0.2, size=90), "pop")
        sc.add(Pill("TELECAMERA NASCOSTA", (1250, 200), T("telecamera"), T("estintore") - 0.3, size=30))
        sc.add(Figure(walk([(-150, FY), (880, FY)], T("filma") - 1.0, 600), T("filma") - 1.0, kind="guard", arms=[(T("compongono"), "point")], label="GUARDIA"))
        sc.add(AIcon("extinguisher", (300, 640), T("estintore") - 0.3, size=280), "pop")
        sc.add(Arrow((1200, 320), (380, 560), T("registrazione"), None, GOLD, 6, 0.6, bend=0.15, dashed=True))
        sc.add(Pill("LA REGISTRAZIONE", (760, 290), T("registrazione") + 0.3, size=30))
        sc.footer = "Fonti: Wikipedia · Forbes Italia · National Geographic"
    elif i == 9:
        sc.add(Text("Non è *solo*", (960, 168), a, size=56, anchor="ma"))
        nodes = {"n": dict(xy=(960, 420), name="NOTARBARTOLO", role="10 anni", t=a + 0.2, rot=-2),
                 "g": dict(xy=(420, 720), name="IL GENIO", role="E. D'Onorio", t=T("Genio") - 0.1, rot=2),
                 "m": dict(xy=(780, 720), name="IL MOSTRO", role="F. Finotto", t=T("Mostro") - 0.1, rot=-3),
                 "s": dict(xy=(1140, 720), name="SPEEDY", role="P. Tavano", t=T("Speedy") - 0.1, rot=3),
                 "r": dict(xy=(1500, 720), name="RE DELLE CHIAVI", role="identità ignota", t=T("quinto"), rot=-2, stamp=("MAI IDENTIFICATO", T("Chi") , RED))}
        sc.board(nodes, [("n", "g", T("Genio")), ("n", "m", T("Mostro")), ("n", "s", T("Speedy")), ("n", "r", T("Re"))], a, cw=200)
        sc.add(Pill("3 ITALIANI CONDANNATI CON LUI", (1500, 300), T("tre"), T("quinto") - 0.2, size=32))
        sc.add(AIcon("question", (1500, 680), T("Chi"), size=150), "pop")
        sc.footer = "Fonti: Wikipedia · Money.it · La Capital (sentenze)"
    elif i == 10:
        tc = T("sabato") - 0.3
        sc.add(Chapter("03", "Il *weekend*", a, tc))
        sc.add(Calendar((330, 470), 240, [(tc + 0.1, "SABATO", "15"), (T("domenica"), "DOMENICA", "16"), (T("febbraio"), "FEBBRAIO", "2003")], tc + 0.1, T("Nessuno") - 0.2), "paper")
        cut = sc.add(Cutaway((620, 190, 1840, 880), tc + 0.1, lights_off=T("tranquillo")))
        sc.add(Icon("moon", (1700, 260), T("tranquillo"), size=130), "pop")
        sc.add(Stamp("CHIUSO FINO A\nLUNEDÌ", (1230, 760), T("chiuso"), size=56, rot=-8))
        sc.add(ClockFace((330, 470), 150, T("Nessuno") - 0.1, None, start=20, speed=9, label="UN GIORNO E MEZZO"), "pop")
        scene_cam(sc, (0, 960, 540, 1.0), (T("caveau") - 0.2, 960, 540, 1.0), (T("caveau") + 0.8, 1230, 720, 1.2), (T("Nessuno") - 0.4, 1230, 720, 1.2), (T("Nessuno") + 0.3, 960, 540, 1.0), (dur, 960, 540, 1.02))
        sc.footer = "Fonti: Wikipedia · Money.it · History Daily · Dawn (AFP)"
    elif i == 11:
        sc.add(Pill("1 · SENSORE DI CALORE E MOVIMENTO", (960, 190), a, size=40))
        sen = sc.add(Sensor("sensor", (1400, 380), a + 0.2, size=220, off_t=T("cieco")), "pop")
        sc.add(Boxes((80, 240, 520, 720), 4, 5, a + 0.2))
        sc.add(Pill("SECONDO LE RICOSTRUZIONI", (960, 270), T("Secondo"), T("pellicola"), size=28, accent=True))
        sc.add(Figure(walk([(-150, FY), (1020, FY)], T("visita") - 1.2, 500), T("visita") - 1.2, kind="suit", arms=[(T("spruzza"), "up")], label="UNA «NORMALE VISITA»"))
        sc.add(AIcon("spray", (1100, 560), T("spruzza") - 0.1, T("cieco"), size=120), "pop")
        sc.add(Spray((1120, 520), (1340, 400), T("spruzza") + 0.1, dur=1.8))
        sc.add(Pill("LACCA PER CAPELLI", (1400, 640), T("lacca"), size=36, accent=True))
        sc.add(Pill("UNA PELLICOLA INVISIBILE", (1400, 740), T("pellicola"), size=32))
        scene_cam(sc, (0, 960, 540, 1.0), (T("spruzza") - 0.2, 960, 540, 1.0), (T("spruzza") + 0.8, 1250, 480, 1.35), (T("cieco") + 0.6, 1250, 480, 1.35), (dur, 1100, 520, 1.1))
        sc.footer = "Fonti: Wikipedia · Money.it · Forbes Italia"
    elif i == 12:
        sc.add(Pill("2 · IL CAMPO MAGNETICO DELLA PORTA", (960, 190), a, size=40))
        sc.add(VaultDoor((700, 560), 230, a + 0.1, plates_t=T("piastre"), foil_t=T("alluminio") + 0.2, open_t=T("aprire")))
        sc.add(Text("se si separano,\nl'allarme *suona*", (1500, 290), T("separano"), T("La"), size=50, anchor="ma", align="m"))
        sc.add(Stamp("ALLARME", (1500, 470), T("suona"), T("La"), size=70, rot=-6))
        sc.add(AIcon("foil", (1360, 420), T("alluminio") - 0.2, size=170, label="LASTRA DI ALLUMINIO"), "pop")
        sc.add(AIcon("tape", (1640, 420), T("nastro"), size=150, label="NASTRO ADESIVO"), "pop")
        sc.add(Pill("SECONDO LE RICOSTRUZIONI", (1500, 640), T("secondo"), T("Così") - 0.2, size=28, accent=True))
        sc.add(Pill("PER L'ALLARME: PORTA CHIUSA", (1500, 700), T("resta") - 0.2, size=34, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (T("piastre") - 0.1, 960, 540, 1.0), (T("piastre") + 0.7, 960, 520, 1.3), (T("separano") + 1.5, 960, 520, 1.3), (T("La") , 960, 540, 1.0), (dur, 960, 540, 1.0))
        sc.footer = "Fonti: Wikipedia · Money.it"
    elif i == 13:
        sc.add(Pill("3 · LA PORTA D'ACCIAIO", (960, 190), a, size=40))
        sc.add(AIcon("dial", (420, 470), T("combinazione") - 0.2, size=230, label="COMBINAZIONE"), "pop")
        sc.add(AIcon("key", (420, 760 - 20), T("chiave") - 0.2, size=230, label="CHIAVE LUNGA E SPECIALE"), "pop")
        tv = T("La", 0)
        sc.add(AIcon("videotape", (900, 440), T("filmati") - 0.2, T("chiave", 1) - 0.2, size=170), "pop")
        sc.add(Arrow((800, 440), (560, 460), T("filmati"), T("chiave", 1) - 0.2, GOLD, 6, 0.4))
        sc.add(Pill("DAI FILMATI DELLA TELECAMERA", (900, 580), T("filmati") + 0.2, T("chiave", 1) - 0.2, size=28))
        sc.add(AIcon("question", (760, 700), T("chiave", 1), size=150), "pop")
        sc.add(Stamp("LE VERSIONI\nNON COINCIDONO", (900, 470), T("versioni"), T("sicuro") - 0.1, size=52, rot=-8))
        sc.add(VaultDoor((1450, 560), 230, a + 0.2, dial_t=T("combinazione"), dial_d=2.5, open_t=T("apre") - 0.3))
        sc.add(Flash(T("apre") + 0.2))
        sc.footer = "Fonti: Wikipedia · Money.it · Forbes Italia"
    elif i == 14:
        sc.add(Pill("4 · GLI ULTIMI SENSORI", (960, 190), a, size=40))
        sc.add(VaultPlan((240, 300, 1680, 840), a, T("cassette") - 0.4))
        sc.add(Sensor("bulb", (900, 450), a + 0.2, T("cassette") - 0.4, size=140, off_t=T("coperto") + 0.3, label="LUCE"), "pop")
        sc.add(AIcon("tape", (600, 260), T("coperto") - 0.3, T("cassette") - 0.4, size=110, move=(T("coperto") - 0.3, 0.6, (900, 450), 80)), "pop")
        sc.add(Sensor("sensor", (1450, 450), T("Contro") - 0.3, T("cassette") - 0.4, size=140, off_t=T("nasconde"), label="CALORE"), "pop")
        sc.add(Figure(walk([(500, 760), (1300, 760)], T("scudo") - 0.4, 260), T("scudo") - 0.4, T("cassette") - 0.4, kind="worker", s=0.55))
        sc.add(AIcon("shield", (580, 690), T("scudo") - 0.4, T("cassette") - 0.4, size=200, move=(T("scudo") - 0.4 + 0.01, (1300 - 500) / 260, (1380, 690), 0)))
        sc.add(Pill("SCUDO DI PLASTICA", (1000, 330), T("scudo"), T("cassette") - 0.4, size=32, accent=True))
        sc.add(Boxes((260, 250, 1660, 860), 14, 6, T("cassette") - 0.3), "whoosh")
        sc.footer = "Fonti: Wikipedia · Money.it · schema semplificato, non in scala"
    elif i == 15:
        tc = T("Diamanti") - 0.3
        bx = sc.add(Boxes((300, 180, 1620, 760), 21, 9, a, tc, open_t=a + 0.3, n_open=109, rate=109 / max(1.0, T("109") - a - 0.1), counter=(960, 840)))
        sc.add(Pill("109 SU 189", (1500, 840), T("109"), tc, size=44, accent=True))
        sc.add(Pill("PRIME NOTIZIE: 123", (420, 840), T("123"), tc, size=36))
        items = [("diamond", T("Diamanti")), ("gold", T("oro")), ("crown", T("gioielli")), ("money", T("contanti"))]
        for k, (nm, tt) in enumerate(items):
            x = 330 + k * 300
            if nm in ("crown", "money"): sc.add(Icon(nm, (x, 470), tt, size=230, move=(T("borsoni") + 0.1 * k, 0.6, (1450, 600), 120)), "pop")
            else: sc.add(AIcon(nm, (x, 470), tt, size=230, move=(T("borsoni") + 0.1 * k, 0.6, (1450, 600), 120)), "pop")
        sc.add(AIcon("bag", (1450, 620), T("tutto") - 0.2, T("Poi") - 0.2, size=360), "pop")
        sc.add(Pill("TUTTO NEI BORSONI", (1450, 300), T("borsoni"), T("Poi") - 0.2, size=40, accent=True))
        tp = T("Poi") - 0.2
        sc.add(Boxes((300, 180, 1620, 760), 21, 9, tp, None, open_t=tp - 100, n_open=109, rate=1000))
        for k in range(3):
            sc.add(Figure(walk([(900 + k * 150, FY), (2200 + k * 150, FY)], T("escono") + k * 0.25, 520), tp, kind="worker", s=0.6, carry=[(0, "hidden")]))
        scene_cam(sc, (0, 960, 540, 1.0), (T("silenzio") - 0.3, 960, 540, 1.0), (dur, 960, 470, 1.15))
        sc.footer = "Fonti: Wikipedia · Money.it · La Capital · Dawn (AFP, 2003)"
    elif i == 16:
        tc = T("Una") - 0.3
        sc.add(Chapter("04", "Lunedì *mattina*", a, tc))
        sc.add(Calendar((300, 400), 220, [(tc, "LUNEDÌ", "17")], tc + 0.1), "paper")
        sc.add(Icon("sun", (300, 700), tc + 0.2, size=150), "pop")
        sc.add(VaultDoor((1250, 540), 220, tc + 0.1, open_t=T("socchiusa") - 0.2))
        sc.add(Figure(walk([(-150, FY), (850, FY)], tc + 0.2, 380), tc + 0.2, T("Dentro") - 0.2, kind="guard", label="GUARDIA"))
        sc.add(Pill("PORTA SOCCHIUSA", (1250, 190 + 40), T("socchiusa"), T("Dentro") - 0.2, size=36, accent=True))
        sc.add(Boxes((560, 220, 1820, 760), 14, 6, T("Dentro") - 0.2, None, open_t=T("Dentro") - 60, n_open=60, rate=1000))
        sc.add(Figure([(0, 380, FY)], T("Dentro") - 0.1, kind="guard", arms=[(T("Chiama"), "up")]))
        sc.add(Figure(walk([(2100, FY), (1500, FY)], T("polizia") - 0.4, 600), T("polizia") - 0.4, kind="police", flip=-1))
        sc.add(Stamp("FURTO", (1190, 480), T("svuotate"), size=110, rot=-10))
        sc.footer = "Fonti: History Daily · Dawn (AFP, 2003)"
    elif i == 17:
        sc.add(Text("Quanto è stato *rubato*?", (960, 165), a, size=62, anchor="ma"))
        sc.add(Text("cifra più citata", (420, 300), T("cifra"), size=40, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Big("~100 milioni $", (420, 420), T("cento"), size=100, color=GOLD, fnt=OSW, count=(0, 100, lambda z: f"~{z:.0f} milioni $", 1.2)))
        sc.add(AIcon("diamond", (240, 640), T("diamanti"), size=140), "pop")
        sc.add(AIcon("gold", (420, 640), T("oro"), size=140), "pop")
        sc.add(Icon("crown", (600, 640), T("gioielli"), size=120), "pop")
        sc.add(Figure([(0, 960, FY)], T("Notarbartolo") - 0.3, kind="suit", s=0.7, label="NOTARBARTOLO, ANNI DOPO"), "pop")
        sc.add(Text("secondo lui", (1500, 270), T("dirà"), size=40, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Big("~20 milioni", (1500, 380), T("venti") - 0.1, size=100, color=WHITE, fnt=OSW))
        sc.add(Bar(1240, 460, 520, 40, [(T("dirà"), 1.0), (T("venti"), 0.2)], T("dirà")))
        sc.add(Stamp("CIFRA VERA:\nMAI SAPUTA", (1500, 660), T("vera"), size=66, rot=-8))
        sc.footer = "Fonti: Wikipedia · National Geographic · History Daily · Money.it"
    elif i == 18:
        sc.add(Figure([(0, 300, FY)], a, kind="police", arms=[(T("Chi") , "point")]))
        sc.add(Figure([(0, 520, FY)], a + 0.15, kind="police", carry=[(0, "magnifier")]))
        sc.add(Pill("POLIZIA DI ANVERSA: UN ENIGMA", (960, 200), a + 0.2, size=38))
        for k in range(10):
            sc.add(AIcon("shield", (720 + (k % 5) * 200, 350 + (k // 5) * 200), T("dieci") + 0.06 * k, T("Chi") - 0.2, size=150), "pop" if k % 3 == 0 else None)
        sc.add(Pill("NESSUN ALLARME È SCATTATO", (1120, 790), T("nessun"), T("Chi") - 0.2, size=36, accent=True))
        sc.add(Big("CHI?", (1000, 470), T("Chi"), size=200, color=WHITE, fnt=SERIF), "hit")
        sc.add(Big("COME?", (1500, 650), T("come"), size=200, color=REDL, fnt=SERIF), "hit")
        sc.footer = "Fonti: Wikipedia · History Daily"
    elif i == 19:
        tc = T("Dopo") - 0.3
        sc.add(Chapter("05", "Il *panino*", a, tc))
        for k in range(5): sc.add(AIcon("tree", (200 + k * 380, 800), a + 0.1 * k, tc, size=180))
        tm = T("Si") - 0.3
        sc.add(Icon("envelope", (420, 420), T("buste"), tm, size=180, label="BUSTE"), "pop")
        sc.add(AIcon("card", (760, 420), T("carte"), tm, size=180, label="CARTE"), "pop")
        sc.add(AIcon("trashbag", (1150, 420), T("materiale") - 0.3, tm, size=200, label="MATERIALE"), "pop")
        sc.add(Pill("LIBERARSI DELLE PROVE", (960, 230), T("liberarsi"), tm, size=40, accent=True))
        sc.add(MapEl((260, 190, 1660, 860), [(0, (4.40, 51.03), 520), (dur, (4.40, 51.03), 600)], tm,
                     routes=[dict(pts=["Anversa", "Terreno"], t=T("l'autostrada") , d=2.0)],
                     pins=[dict(at="Anversa", label="Anversa", t=tm + 0.2, side="r"), dict(at="Bruxelles", label="Bruxelles", t=T("Bruxelles"), side="r"),
                           dict(at="Terreno", label="terreno privato (zona indicativa)", t=T("terreno"), side="r", color=RED)],
                     title="mappa: Natural Earth · percorso e luogo indicativi"))
        sc.add(Pill("AUTOSTRADA E19", (960, 230), T("l'autostrada"), size=36))
        sc.footer = "Fonti: Wikipedia · Money.it · La Capital"
    elif i == 20:
        for k in range(5): sc.add(AIcon("tree", (160 + k * 400, 640), a + 0.08 * k, size=360))
        sc.add(Figure(walk([(-150, FY), (520, FY)], a, 420), a, kind="man", label="AUGUST VAN CAMP · PROPRIETARIO", arms=[(T("Trova"), "point"), (T("chiama"), "up")]))
        for k in range(4):
            sc.add(AIcon("trashbag", (900 + k * 180, 790 - (k % 2) * 30), T("spazzatura") + 0.2 * k, size=170), "pop")
        sc.add(Pill("È STUFO", (520, 330), T("stufo"), T("Trova"), size=44, accent=True))
        sc.add(Figure(walk([(2100, FY), (1650, FY)], T("polizia") - 0.3, 520), T("polizia") - 0.3, kind="police", flip=-1))
        let = doc_typed(520, 300, "SEGNALAZIONE", ["Motivo: rifiuti abbandonati", "Luogo: terreno privato"], footer=None, seed=21, size=30)
        sc.add(Img(let, (1180, 330), T("segnalazione") - 0.1, anim="drop", rot=-3), "paper")
        sc.footer = "Fonti: Wikipedia · History Daily · La Capital · documento: ricostruzione grafica"
    elif i == 21:
        sc.add(AIcon("trashbag", (960, 600), a, T("C'è") + 0.2, size=320))
        env = doc_typed(420, 260, "BUSTA", ["ANTWERP", "DIAMOND CENTER"], footer=None, seed=31, size=36)
        sc.add(Img(env, (380, 400), T("buste"), anim="drop", rot=-6), "paper")
        fat = doc_typed(420, 330, "FATTURA", ["intestata a:", "*L. Notarbartolo*"], footer=None, seed=32, size=34)
        sc.add(Img(fat, (960, 400), T("fattura"), anim="drop", rot=3), "paper")
        sc.add(AIcon("card", (1520, 400), T("biglietto"), size=260, label="BIGLIETTO DA VISITA DI UN COMPLICE"), "pop")
        sc.add(AIcon("sandwich", (960, 720), T("panino"), size=300), "pop")
        sc.add(Pill("PANINO AL SALAME · MANGIATO A METÀ", (960, 880), T("mangiato"), size=34, accent=True))
        scene_cam(sc, (0, 960, 540, 1.0), (T("panino") - 0.1, 960, 540, 1.0), (T("panino") + 0.8, 960, 620, 1.15), (dur, 960, 620, 1.18))
        sc.footer = "Fonti: Money.it · Forbes Italia · La Capital · Wikipedia · documenti: ricostruzione grafica"
    elif i == 22:
        sc.add(AIcon("sandwich", (420, 470), a, size=260))
        sc.add(Figure(walk([(2100, FY), (760, FY)], a, 700), a, T("Ma") - 0.2, kind="expert", flip=-1, carry=[(0, "magnifier")], arms=[(T("DNA") , "point")]))
        sc.add(AIcon("dna", (1150, 460), T("DNA") - 0.1, T("Ma") - 0.2, size=320), "pop")
        sc.add(Pill("DI CHI? LE FONTI NON CONCORDANO", (1250, 230), T("chi") , T("Ma") - 0.2, size=34, accent=True))
        tm = T("Ma") - 0.2
        fat = doc_typed(300, 220, "FATTURA", ["L. Notarbartolo"], footer=None, seed=32, size=28)
        sc.add(Img(fat, (420, 760), tm, anim="drop", rot=3), "paper")
        sc.add(Icon("envelope", (760, 760), tm + 0.2, size=160), "pop")
        sc.add(Img(person_card("LA BANDA", "4 condannati", 220, 7), (1500, 520), T("banda") - 0.3, anim="drop"), "paper")
        for p in [(420, 470), (420, 700), (760, 720)]:
            sc.add(Arrow(p, (1360, 520), T("dritto") - 0.2, None, RED, 6, 0.6, bend=0.1))
        sc.add(Stamp("TRADITO DA UN\nSACCO DI RIFIUTI", (960, 330), T("tradito"), size=58, rot=-6))
        sc.footer = "Fonti: Wikipedia · National Geographic · Forbes Italia · La Capital"
    elif i == 23:
        sc.add(Calendar((300, 450), 200, [(a, "POCHI GIORNI DOPO", "FEB")], a, T("Lì") - 0.2), "paper")
        cut = sc.add(Cutaway((720, 190, 1840, 880), a))
        sc.add(Pill("TORNA NEL PALAZZO CHE AVEVA SVUOTATO", (500, 230), T("palazzo"), T("Viene") - 0.2, size=30))
        sc.add(Figure(walk([(-150, FY), (720, FY)], T("torna") - 0.3, 360), T("torna") - 0.3, kind="suit", label="NOTARBARTOLO"))
        sc.add(Figure(walk([(2100, FY), (980, FY)], T("investigatori") - 0.4, 700), T("investigatori") - 0.4, kind="police", flip=-1))
        sc.add(Figure(walk([(2300, FY), (1160, FY)], T("investigatori") - 0.2, 700), T("investigatori") - 0.2, kind="police", flip=-1))
        sc.add(Icon("handcuffs", (720, 620), T("arrestato") - 0.2, size=130), "pop")
        sc.add(Stamp("ARRESTATO", (520, 330), T("arrestato"), size=84, rot=-8))
        scene_cam(sc, (0, 960, 540, 1.0), (T("arrestato") - 0.4, 960, 540, 1.0), (T("arrestato") + 0.5, 800, 620, 1.12), (dur, 800, 620, 1.13))
        sc.footer = "Fonti: Wikipedia · La Capital · Money.it"
    elif i == 24:
        tc = T("Notarbartolo") - 0.3
        sc.add(Chapter("06", "Il *processo*", a, tc))
        sc.add(Calendar((960, 820 - 60), 150, [(a + 0.3, "ANVERSA", "2005")], a + 0.3, tc), "paper")
        sc.add(Figure([(0, 300, 620)], tc, kind="judge", s=0.8))
        sc.add(Icon("bench", (300, 680), tc, size=320, anim="fade"))
        sc.add(Icon("gavel", (520, 460), T("condannato"), size=140, anim="shake"), "stamp")
        rows = [("Notarbartolo · organizzatore", "10 ANNI", T("condannato"), 1.0), ("Il Genio", "5 ANNI", T("Genio"), 0.5),
                ("Il Mostro", "5 ANNI", T("Mostro"), 0.5), ("Speedy", "5 ANNI", T("Speedy"), 0.5)]
        for k, (lab, v, tt, f) in enumerate(rows):
            y = 300 + k * 125
            sc.add(Text(lab, (720, y - 50), tt, size=34, fnt=PS, color=WHITE))
            sc.add(Bar(720, y, 760, 36, [(tt, f)], tt, color=RED if k == 0 else GOLD))
            sc.add(Text(v, (1500, y - 10), tt + 0.3, size=44, fnt=OSW, color=WHITE))
        sc.add(Pill("RE DELLE CHIAVI: MAI IDENTIFICATO", (1100, 840), T("Re"), size=34, accent=True))
        sc.footer = "Fonti: Wikipedia · Money.it · La Capital"
    elif i == 25:
        tq = T("Nel", 1) - 0.3
        for k in range(8):
            x0 = 600 + (k % 4) * 240; y0 = 380 + (k // 4) * 200
            sc.add(AIcon("diamond", (x0, y0), a + 0.05 * k, T("Quasi") + 1.0 + 0.1 * k, size=130, move=(T("Quasi") + 0.1 * k, 1.0, (x0 + (k - 4) * 160, -200), 0)), "pop" if k % 3 == 0 else None)
        sc.add(Big("?", (960, 520), T("Quasi") + 1.0, tq, size=320, color=GOLD))
        sc.add(Stamp("MAI RITROVATI", (1500, 300), T("ritrovati"), tq, size=70, rot=-8))
        sc.add(Calendar((330, 430), 200, [(tq + 0.1, "LIBERTÀ CONDIZIONALE", "2009")], tq + 0.1), "paper")
        sc.add(Door((960, FY), 220, 400, tq + 0.1, open_t=tq + 0.6))
        sc.add(Figure(walk([(960, FY), (1300, FY)], tq + 1.0, 260), tq + 0.9, kind="suit", label="NOTARBARTOLO"))
        sc.add(Pill("OBBLIGO: RISARCIRE LE VITTIME", (1400, 300), T("l'obbligo"), size=34))
        sc.add(Icon("money", (1650, 640), T("risarcire"), size=170), "pop")
        sc.add(Stamp("NON ARRIVA", (1650, 640), T("arriva"), size=60, rot=-10))
        sc.footer = "Fonti: Wikipedia · Money.it · La Capital"
    elif i == 26:
        tn = T("Nel", 1) - 0.3
        m = doc_typed(560, 420, "MANDATO D'ARRESTO EUROPEO · 2011", ["Persona: L. Notarbartolo", "Motivo: violazione", "delle condizioni", "della libertà condizionale"], footer="contenuto riassunto", seed=41, size=30)
        sc.add(Img(m, (420, 500), a + 0.1, tn, anim="drop", rot=-2), "paper")
        sc.add(Stamp("2011", (700, 330), T("mandato"), tn, size=64, rot=8))
        tt = T("Torna") - 0.3
        sc.add(MapEl((760, 190, 1820, 860), [(0, (3.5, 49.8), 120), (tt, (3.0, 49.3), 150)], a + 0.2, tt,
                     pins=[dict(at="Anversa", label="Anversa", t=a + 0.4, side="r"), dict(at="Parigi", label="Parigi · aeroporto", t=T("Parigi"), side="r", color=RED)],
                     title="mappa: Natural Earth"))
        sc.add(AIcon("plane", (1140, 360), T("aeroporto") - 0.3, tt, size=170), "pop")
        sc.add(Calendar((300, 450), 200, [(tn, "FERMATO NEL", "2013")], tn, tt), "paper")
        sc.add(Icon("handcuffs", (300, 700), T("fermato"), tt, size=140), "pop")
        sc.add(Icon("bars", (960, 600), tt + 0.1, size=300, anim="fade"), "stamp")
        sc.add(Timeline(220, 1700, 380, [dict(top="2003", bottom="il colpo", t=tt + 0.2), dict(top="2005", bottom="10 anni", t=tt + 0.4),
                                         dict(top="2009", bottom="condizionale", t=tt + 0.6), dict(top="2011", bottom="mandato", t=tt + 0.8),
                                         dict(top="2013", bottom="fermato", t=tt + 1.0), dict(top="2017", bottom="fine pena", t=T("2017"), hl=True)], tt + 0.1))
        sc.footer = "Fonti: Wikipedia · Money.it · documento: ricostruzione grafica"
    elif i == 27:
        tc = T("È") - 0.3
        sc.add(Chapter("07", "L'altra *versione*", a, tc))
        sc.add(Figure([(0, 300, FY)], tc + 0.1, kind="suit", label="NOTARBARTOLO"))
        iv = doc_typed(560, 380, "INTERVISTA · RIVISTA USA", ["«Ci ha ingaggiati", "un commerciante", "di diamanti.»", "", "(truffa all'assicurazione)"], footer="contenuto riassunto", seed=51, size=30)
        tm = T("È", 1) - 0.3
        sc.add(Img(iv, (760, 470), T("un'intervista") - 0.2, tm, anim="drop", rot=-2), "paper")
        sc.add(Figure(walk([(2100, FY), (1450, FY)], T("ingaggiata") - 0.6, 600), T("ingaggiata") - 0.6, tm, kind="suit", flip=-1, label="UN COMMERCIANTE?"))
        sc.add(AIcon("question", (1450, 400), T("commerciante"), tm, size=140), "pop")
        sc.add(Pill("TRUFFA ALL'ASSICURAZIONE?", (1450, 230), T("truffa"), tm, size=36, accent=True))
        sc.add(Stamp("MAI DIMOSTRATA", (960, 470), tm + 0.2, size=90, rot=-8))
        sc.add(Pill("INVESTIGATORI ED ESPERTI: NON CREDIBILE", (960, 680), T("investigatori"), size=36))
        sc.footer = "Fonti: Wikipedia (Wired, 2009) · Money.it"
    elif i == 28:
        tm = T("Ma") - 0.3
        sc.add(Text("Un racconto *popolare*", (960, 175), a, tm, size=60, anchor="ma"))
        sc.add(AIcon("book", (420, 480), T("libri"), tm, size=230, label="LIBRI"), "pop")
        sc.add(AIcon("tv", (960, 480), T("serie"), tm, size=240, label="SERIE TV ITALIANA · 2023"), "pop")
        sc.add(AIcon("tv", (1500, 480), T("documentario") - 0.2, tm, size=240, label="DOCUMENTARIO · 2025"), "pop")
        sc.add(Pill("NOTARBARTOLO RACCONTA LA SUA VERITÀ", (1300, 760), T("racconta"), tm, size=32))
        sc.add(AIcon("diamond", (960, 500), tm + 0.1, size=330), "pop")
        sc.add(AIcon("question", (1300, 340), T("dove"), size=200), "pop")
        scene_cam(sc, (0, 960, 540, 1.0), (tm, 960, 540, 1.0), (dur, 960, 520, 1.12))
        sc.footer = "Fonti: Wikipedia · Money.it · Forbes Italia · Libero"
    elif i == 29:
        sc.add(Chapter("", "Il *verdetto*", a, T("Un") - 0.3))
        rows = [("Livelli di sicurezza", "10", T("Un"), "shield"), ("Chi entra", "un inquilino", T("inquilino"), "key"),
                ("Gli attrezzi", "lacca e nastro adesivo", T("bomboletta"), "spray"), ("Il bottino", "mai ritrovato", T("bottino"), "diamond"),
                ("L'errore", "un sacco di rifiuti", T("errore"), "trashbag")]
        sc.add(Rows([dict(label=l, value=v, t=t, color=(REDL if k == 4 else GOLD)) for k, (l, v, t, _) in enumerate(rows)], T("Un") - 0.2, x0=420, x1=1700, y=290, gap=125, size=46))
        for k, (l, v, t, ic) in enumerate(rows):
            sc.add(AIcon(ic, (300, 290 + k * 125), t, size=95), "pop")
        sc.footer = F_BASE
    elif i == 30:
        sc.add(Text("Capolavoro o\n*colpo di fortuna*?", (960, 175), T("Il"), size=90, anchor="ma", align="m"))
        sc.add(AIcon("diamond", (560, 560), T("capolavoro"), size=200, label="CAPOLAVORO"), "pop")
        sc.add(AIcon("trashbag", (1360, 560), T("fortuna"), size=200, label="FINITO MALE"), "pop")
        sc.add(Text("Scrivilo nei commenti", (960, 720), T("Scrivilo"), size=50, fnt=PS, color=GREY, anchor="ma"))
        sc.add(Img(wordmark(100), (960, 840), T("Iscriviti"), anim="pop", shadow=False), "hit")
        sc.footer = "Tutte le fonti nella descrizione · ricostruzione a scopo divulgativo"
    return sc

def thumbnail(path="thumbnail.jpg"):
    im = make_bg(7); d = ImageDraw.Draw(im)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    VaultDoor((1460, 560), 300, -10, open_t=-10).draw(lay, 0.6, 1.0)
    im.alpha_composite(lay)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    place(lay, aic("sandwich", 330), (1560, 830), "mm", 1.0)
    for k, (x, y) in enumerate([(1180, 300), (1700, 260), (1250, 780)]):
        place(lay, aic("diamond", 130), (x, y), "mm", 1.0)
    im.alpha_composite(lay)
    t = rich_img("IL COLPO\nDEL SECOLO\nE IL *PANINO*", SERIF, 140, WHITE, RED, lh=1.0)
    im.alpha_composite(t, (90, 150))
    st = stamp_img("CASO 002", RED, 70, -10); im.alpha_composite(st, (1540, 70))
    d.text((100, 840), "10 LIVELLI DI SICUREZZA. TRADITI DAI RIFIUTI.", font=font(OSW, 50, 600), fill=GOLD + (255,))
    wm = wordmark(60, sub=False); im.alpha_composite(wm, (100, 960))
    im.convert("RGB").save(path, quality=92)
