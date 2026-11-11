# FASCICOLO ITALIA — motore video

True crime italiano "senza sangue": colpi, truffe, furti d'arte, sparizioni ed errori giudiziari.
Le istruzioni editoriali complete sono nel progetto Claude: `reel/istruzioni_fascicolo.md`.

## Struttura
- `engine/` motore grafico e audio (tutto disegnato da codice)
  - `fi.py` base: sfondo, testi, documenti ricostruiti (`doc_typed`, `newspaper`, `id_card`), timbri, mappe Natural Earth (`MapEl`), pianta semplificata (`Plan`), bacheca (`Board`), timeline, archivio (`CardGrid`), baule (`Trunk`), quadro stilizzato (`Frame`), logo.
  - `fx.py` montaggio "nuovo": omini animati (`Figure`), icone (`Icon`: lock, pliers, knob, magnifier, easel, camera, house, museum, envelope, train, handcuffs, gavel, crown, bicorne, money, glass, frame_empty, bed, moon, sun, newspaper, drawer, bars, stairs, corridor, smock, bench), `Pill`, `Arrow`, `ClockFace`, `Calendar`, `Door`, `Flash`, `Crowd`, `Bar`, `Wall`, `Facade`, `Bubble`, movimenti di camera `scene_cam(sc, (t, cx, cy, zoom), ...)`.
  - `vo.py` voce Kokoro (im_nicola; `python3 vo.py 1.0` per il lungo, `1.1` per i reel).
  - `render.py` (preview | scene N | events | chapters), `contact.py` (fogli di controllo: 4 fotogrammi per scena), `audio.py` (musica d'indagine + effetti), `build.sh` (tutto il montaggio).
  - `setup.sh` installa font, voce e librerie.
- `episodi/<nnn>-<caso>/lungo|reel-a|reel-b/` → `script.py` + `scenes.py` di ogni video (esempio completo: `001-gioconda`).
- `media/` file pubblicati (link raw per Metricool). Ogni file < 95 MB.

## Comandi
```
bash engine/setup.sh
cd episodi/<nnn>-<caso>/lungo
python3 ../../../engine/vo.py 1.0          # voce -> vo.json + audio/
python3 ../../../engine/contact.py         # prev/cNN.jpg: GUARDARLI TUTTI
bash ../../../engine/build.sh raw.mp4      # render + audio + capitoli
ffmpeg -i raw.mp4 -vf hqdn3d=6:4:8:8 -c:v libx264 -preset medium -b:v 1250k -maxrate 1800k -bufsize 3600k -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart finale.mp4
```
Per i reel: `script.py` con `FORMAT = "reel"` (1080x1920, 30 fps), velocità voce 1.1; per comprimere usare `-b:v 2500k`.

## script.py (lungo)
`STYLE`, `CASE` ("FASCICOLO N. 00X · TITOLO"), `TITLE`, `CH` (capitoli), `SCENES_H = [(capitolo, [(frase, pausa), ...]), ...]`, `SCENES`, `HEADERS`, `tokens()`. Numeri e nomi stranieri come `[display|parlato]` (es. `[Sauvet|Sovè]`, `[1911.|millenovecentoundici.]`). Mai parole con apostrofo attaccato a una parentesi quadra.

## scenes.py
`from fi import *` e `from fx import *`; `build(i, dur, a, words)` con `T = Clock(words, a)`, `T("parola", nth)` = istante in cui la parola viene detta (prefisso; attenzione alle parole con apostrofo: `T("l'originale")`). Pavimento degli omini `FY = 870` (lungo). Area utile y 150-900, sottotitoli a y 962.
