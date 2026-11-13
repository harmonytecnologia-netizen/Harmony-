set -e
cd "$(dirname "$0")"; V=../voice
# 3D frames -> upscaled 1080x1920, hold last frame 1.6 s, overlays by time
ffmpeg -y -loglevel error -framerate 24 -i /mnt/user-data/uploads/Downloads/MOVE_render3D/frames720/%04d.jpg \
 -i ov/a.png -i ov/b.png -i ov/c.png -i ov/d.png -i ov/e.png \
 -filter_complex "[0:v]scale=1080:1920:flags=lanczos,tpad=stop_mode=clone:stop_duration=1.6,format=rgba[b];\
[b][1:v]overlay=enable='between(t,0,4.1)'[v1];[v1][2:v]overlay=enable='between(t,4.1,8.9)'[v2];\
[v2][3:v]overlay=enable='between(t,8.9,15.4)'[v3];[v3][4:v]overlay=enable='between(t,16.0,24.6)'[v4];\
[v4][5:v]overlay=enable='gte(t,24.6)',format=yuv420p[v]" \
 -map "[v]" -r 30 -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p video.tmp.mp4 && mv video.tmp.mp4 video.mp4
# narration placed by time
ffmpeg -y -loglevel error -i $V/s1.wav -i $V/s2.wav -i $V/s3.wav -i $V/s4.wav -i $V/s5.wav -filter_complex \
"[0]adelay=300|300[a];[1]adelay=4300|4300[b];[2]adelay=8950|8950[c];[3]adelay=16450|16450[d];[4]adelay=25400|25400[e];\
[a][b][c][d][e]amix=inputs=5:normalize=0,aresample=48000,pan=stereo|c0=c0|c1=c0,highpass=f=80,acompressor=threshold=-18dB:ratio=3,loudnorm=I=-16:TP=-1.5[n]" -map "[n]" -t 31.6 voice.wav
# music ducked under voice + sfx
ffmpeg -y -loglevel error -i video.mp4 -i "/mnt/user-data/uploads/Downloads/If You're Asking My Advice - Asher Fulero.mp3" -i sfx.wav -i voice.wav -filter_complex \
"[1:a]atrim=0:31.6,volume=0.5,afade=t=in:d=0.6,afade=t=out:st=30:d=1.6[m];[3:a]asplit[vo][sc];[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[md];\
[2:a]volume=0.9,apad[s];[md][s][vo]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart MOVE_explica_impedancia_3D.tmp.mp4 && mv MOVE_explica_impedancia_3D.tmp.mp4 MOVE_explica_impedancia_3D.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 MOVE_explica_impedancia_3D.mp4
