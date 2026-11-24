ffmpeg -y -i raw.mp4 -vf hqdn3d=6:4:8:8 -c:v libx264 -preset slow -tune animation -b:v 288k -pass 1 -an -f null /dev/null
ffmpeg -y -i raw.mp4 -vf hqdn3d=6:4:8:8 -c:v libx264 -preset slow -tune animation -b:v 288k -pass 2 -c:a aac -b:a 96k -movflags +faststart finale.mp4
