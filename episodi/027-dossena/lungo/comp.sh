D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 raw.mp4)
VB=$(python3 -c "print(max(180, int(90*8*1000/$D - 110)))")
echo "VB $VB"
ffmpeg -y -v error -i raw.mp4 -vf hqdn3d=6:4:8:8 -c:v libx264 -preset slow -tune animation -b:v ${VB}k -pass 1 -an -f null /dev/null
ffmpeg -y -v error -i raw.mp4 -vf hqdn3d=6:4:8:8 -c:v libx264 -preset slow -tune animation -b:v ${VB}k -pass 2 -c:a aac -b:a 96k -movflags +faststart finale.mp4
python3 ../../../engine/check_voice.py finale.mp4
echo FINE
