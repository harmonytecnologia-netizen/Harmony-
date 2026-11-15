# Reel de trabalho real: manutenção (teclado + SSD + GPU). Gerado automaticamente.
import subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
H=os.path.dirname(os.path.abspath(__file__)); B=H+'/../../biblioteca'
os.chdir(H); os.makedirs('tmp',exist_ok=True)
A=ImageFont.truetype('anton.ttf',128); S=ImageFont.truetype('../../fonts/Poppins-Bold.ttf',46)
segs=[('20260506_121216',0.3,1.6,['OLHA O ESTADO','DESSE TECLADO!'],'#ffe14f'),
 ('20260506_121216',5.2,1.2,['SUJEIRA EM','TODA TECLA'],'#ffffff'),
 ('20260506_125031',0.8,1.4,['LIMPEZA','COMPLETA'],'#22d3ee'),
 ('20260506_125031',4.6,1.2,['TECLA','POR TECLA'],'#ffffff'),
 ('20260506_175215',1.0,1.5,['E O RGB','VOLTOU!'],'#ff4fd8'),
 ('20260506_175215',7.5,1.1,['NOVO','DE NOVO'],'#ffe14f'),
 ('20260521_202918',3.0,1.5,['AGORA:','SSD NO PC'],'#22d3ee'),
 ('20260521_202918',8.5,1.2,['PARAFUSADO','DO JEITO CERTO'],'#ffffff'),
 ('20260525_095620',0.8,1.5,['PLACA DE VÍDEO','NO RGB'],'#8b5cff'),
 ('20260525_095620',6.8,1.3,['TUDO TESTADO','NO WINDOWS'],'#ffffff'),
 ('20260605_150826',1.2,1.5,['O PRÓXIMO PC','JÁ CHEGOU...'],'#ffe14f')]
def card(lines,cor,y0=1130,sub=None):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im)
    y=y0
    for i,l in enumerate(lines):
        w=d.textlength(l,font=A); x=(1080-w)/2
        c=cor if i==len(lines)-1 else '#ffffff'
        d.text((x,y),l,font=A,fill=c,stroke_width=10,stroke_fill='#07040f'); y+=150
    if sub:
        for s in sub:
            w=d.textlength(s,font=S); d.text(((1080-w)/2,y+10),s,font=S,fill='#ffffff',stroke_width=5,stroke_fill='#07040f'); y+=66
    # marca
    m='@harmony_computer'; w=d.textlength(m,font=S)
    d.text(((1080-w)/2,270),m,font=S,fill='#ffffff',stroke_width=4,stroke_fill='#7a3cff')
    return im
parts=[]
for k,(f,ss,du,lines,cor) in enumerate(segs):
    card(lines,cor).save(f'tmp/t{k}.png')
    o=f'tmp/s{k}.mp4'
    vf=("[0:v]eq=contrast=1.08:saturation=1.25,scale=w='1080*(1.12-0.08*t/%s)':h=-2:eval=frame,crop=1080:1920,"
        "fade=t=in:st=0:d=0.10:color=white[v];[v][1:v]overlay=0:0,format=yuv420p" % du)
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(ss),'-t',str(du),'-i',f'{B}/reais/{f}.mp4','-i',f'tmp/t{k}.png',
        '-filter_complex',vf,'-r','30','-c:v','libx264','-crf','20','-preset','veryfast','-an',o],check=True)
    parts.append(o)
# CTA final 2.6 s sobre frame desfocado da GPU
subprocess.run(['ffmpeg','-v','error','-y','-ss','0.4','-i',f'{B}/reais/20260525_095620.mp4','-frames:v','1','tmp/bg.png'],check=True)
bg=Image.open('tmp/bg.png').convert('RGB').filter(ImageFilter.GaussianBlur(18))
bg=Image.blend(bg,Image.new('RGB',bg.size,'#07040f'),0.45).convert('RGBA')
bg.alpha_composite(card(['QUER O SEU','PC ASSIM?','MANDA','ORÇAMENTO'],'#ffe14f',y0=640,sub=['no Direct 📩'.replace(' 📩',''),'Enviamos para todo o Brasil']))
bg.convert('RGB').save('tmp/cta.png')
subprocess.run(['ffmpeg','-v','error','-y','-i','tmp/cta.png','-frames:v','78','-vf',"zoompan=z='1+0.0015*on':d=78:s=1080x1920:fps=30,fade=t=in:st=0:d=0.12:color=white,format=yuv420p",
    '-c:v','libx264','-crf','20','-preset','veryfast','tmp/cta.mp4'],check=True)
parts.append('tmp/cta.mp4')
open('tmp/list.txt','w').write(''.join(f"file '{os.path.basename(p)}'\n" for p in parts))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','tmp/list.txt','-c','copy','tmp/v.mp4'],check=True)
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','tmp/v.mp4']))
subprocess.run(['ffmpeg','-v','error','-y','-i','tmp/v.mp4','-ss','6','-i',f'{B}/musicas/bad_news_steve_kane.mp3',
    '-filter_complex',f'[1:a]atrim=0:{dur},afade=t=in:d=0.3,afade=t=out:st={dur-1.2}:d=1.2,loudnorm=I=-14:TP=-1.5[a]',
    '-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart','jpc_real_manutencao.mp4'],check=True)
print('ok',dur)
