#!/bin/bash
# Uso: cd <cartella episodio> && bash /home/claude/fi/engine/build.sh output.mp4 [musica_vol]
set -e
E="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT=${1:-out.mp4}; MV=${2:-0.55}
mkdir -p audio scenes prev
python3 $E/render.py events
python3 $E/audio.py
VCH="highpass=f=80,equalizer=f=300:t=q:w=1.2:g=-2.5,equalizer=f=3000:t=q:w=1.2:g=2,equalizer=f=7500:t=q:w=1.5:g=-2,acompressor=threshold=-24dB:ratio=3:attack=5:release=90:makeup=3,alimiter=limit=0.9"
ffmpeg -y -v error -i audio/voice.wav -i audio/music.wav -i audio/sfx.wav -filter_complex "[0]$VCH,asplit=2[v][vsc];[1]volume=$MV,highpass=f=40[m];[m][vsc]sidechaincompress=threshold=0.015:ratio=6:attack=15:release=400:makeup=1[md];[2]volume=0.8[fx];[v][md][fx]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]" -map "[a]" -ar 48000 audio/mix_final.wav
N=$(python3 -c "import json;print(len(json.load(open('vo.json'))))")
seq 0 $((N-1)) | xargs -P $(nproc) -I{} python3 $E/render.py scene {}
: > scenes/list.txt; for i in $(seq 0 $((N-1))); do echo "file 's$i.mp4'" >> scenes/list.txt; done
ffmpeg -y -v error -f concat -safe 0 -i scenes/list.txt -c copy v.mp4
ffmpeg -y -v error -i v.mp4 -i audio/mix_final.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
python3 $E/render.py chapters
