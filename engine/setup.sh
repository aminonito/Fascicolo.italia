#!/bin/bash
# Installa dipendenze, voce Kokoro e font per FASCICOLO ITALIA. Idempotente.
set -e
pip install --break-system-packages -q kokoro-onnx soundfile scipy pillow numpy shapely 2>/dev/null
mkdir -p /home/claude/tts /home/claude/fonts
cd /home/claude/tts
for f in kokoro-v1.0.onnx voices-v1.0.bin; do [ -s $f ] || curl -sSL --max-time 300 -o $f https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f; done
cd /home/claude/fonts
g(){ [ -s "$2" ] || curl -sSL --max-time 60 -o "$2" "https://raw.githubusercontent.com/google/fonts/main/$1"; }
g apache/specialelite/SpecialElite-Regular.ttf SpecialElite-Regular.ttf
g ofl/dmserifdisplay/DMSerifDisplay-Regular.ttf DMSerifDisplay-Regular.ttf
g ofl/poppins/Poppins-SemiBold.ttf Poppins-SemiBold.ttf
g ofl/poppins/Poppins-ExtraBold.ttf Poppins-ExtraBold.ttf
g "ofl/oswald/Oswald%5Bwght%5D.ttf" Oswald.ttf
g ofl/courierprime/CourierPrime-Bold.ttf CourierPrime-Bold.ttf
g ofl/courierprime/CourierPrime-Regular.ttf CourierPrime-Regular.ttf
ls -la /home/claude/fonts | wc -l
echo setup-ok
