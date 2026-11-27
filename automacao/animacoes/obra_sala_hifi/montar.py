"""Reel OBRA REAL com áudio real: sala com caixas de torre (pasta clientes/VID-20250716-WA0165.mp4).
Sem voz de IA (nova estratégia 27/11). Texto grande + áudio original da sala + tela final."""
import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont
R=os.path.abspath(os.path.dirname(__file__)+'/../../..')
SRC=sys.argv[1]; OUT=sys.argv[2]
F=R+'/kit_instagram/fontes/'
W,H=1080,1920
cards=[ # (ini, fim, linhas, destaque) — tempos no vídeo final
 (0.0,2.8,['Dá pra ter som','de verdade sem','estragar a sala?'],None),
 (2.8,5.8,['Aumenta o volume:','esse é o som','real da sala'],'ÁUDIO REAL DA OBRA'),
 (5.8,8.8,['Caixas de torre','nos cantos, no','tom da madeira'],None),
 (8.8,11.4,['O som entra','no projeto junto','com a decoração'],None),
 (11.4,14.0,['Salva pra','sua obra'],'PROJETO DE SOM MOVE'),
]
OFF=2.4
os.makedirs('ov',exist_ok=True)
fb=ImageFont.truetype(F+'Inter-Black.otf',92); fk=ImageFont.truetype(F+'Inter-Bold.otf',40)
for i,(a,b,ls,k) in enumerate(cards):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    y=560 if i==0 else 1180
    if k:
        tw=d.textlength(k,font=fk); d.rounded_rectangle([(W-tw)/2-26,y-90,(W+tw)/2+26,y-20],18,fill=(84,223,174,255))
        d.text(((W-tw)/2,y-82),k,font=fk,fill=(13,27,23,255))
    for j,l in enumerate(ls):
        tw=d.textlength(l,font=fb)
        d.text(((W-tw)/2,y+j*112),l,font=fb,fill=(242,245,239,255),stroke_width=7,stroke_fill=(13,27,23,255))
    im.save(f'ov/c{i}.png')
# vídeo base: girar, tirar o adesivo (delogo), escalar 1080x1920, punch-in alternado a cada ~1,7 s
cuts=[2.4,3.8,5.2,6.6,8.1,9.6,11.0,12.4,13.8,15.1,16.4]
zs=[1.0,1.10,1.0,1.12,1.0,1.08,1.0,1.12,1.0,1.06]
parts=[]
for i in range(len(cuts)-1):
    a,b,z=cuts[i],cuts[i+1],zs[i]
    vf=f"delogo=x=36:y=150:w=140:h=104,scale={int(W*z)}:{int(H*z)}:flags=lanczos,crop={W}:{H},eq=contrast=1.05:saturation=1.08,unsharp=5:5:0.6,fps=30,setsar=1"
    o=f'seg{i}.mp4'; parts.append(o)
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i',SRC,'-vf',vf,'-an','-c:v','libx264','-preset','veryfast','-crf','17',o],check=True)
open('lista.txt','w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','lista.txt','-c','copy','base.mp4'],check=True)
# overlays
inp=['-i','base.mp4']+sum([['-i',f'ov/c{i}.png'] for i in range(len(cards))],[])
fc='[0:v]'; last='[0:v]'
chain=[]
for i,(a,b,_,_) in enumerate(cards):
    nxt=f'[v{i}]'
    chain.append(f"{last}[{i+1}:v]overlay=0:0:enable='between(t,{a},{b})'{nxt}"); last=nxt
subprocess.run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(chain),'-map',last,'-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','corpo.mp4'],check=True)
# junta tela final; áudio real da sala (16,4 s) + fade, depois silêncio suave na tela final
TF=R+'/automacao/assets/tela_final.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-i','corpo.mp4','-i',TF,'-ss',str(OFF),'-t','14.0','-i',SRC,
 '-filter_complex',"[0:v]fps=30,setsar=1[a];[1:v]scale=1080:1920,fps=30,setsar=1[b];[a][b]concat=n=2:v=1:a=0[v];"
 "[2:a]aresample=48000,highpass=f=40,afade=t=in:d=0.15,afade=t=out:st=12.9:d=1.1,apad=pad_dur=3.6,loudnorm=I=-14:TP=-1.5:LRA=11[au]",
 '-map','[v]','-map','[au]','-t','17.6','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',OUT],check=True)
print('ok',OUT)
