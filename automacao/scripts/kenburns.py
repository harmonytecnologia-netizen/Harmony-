"""Ken Burns suave de imagens + crossfade. uso: kb.py cenas.json saida.mp4
cenas.json: {"fps":30,"xf":0.4,"cenas":[{"img":"a.png","dur":3.6,"mov":"in|out|left|right|up|down"}]}"""
import json,sys,subprocess,os,numpy as np
from PIL import Image
W,H=1080,1920
cfg=json.load(open(sys.argv[1])); fps=cfg.get('fps',30); xf=cfg.get('xf',0.4)
tmp=os.path.dirname(os.path.abspath(sys.argv[2]))+'/_kb'; os.makedirs(tmp,exist_ok=True)
clips=[]
for i,c in enumerate(cfg['cenas']):
    im=Image.open(c['img']).convert('RGB')
    S=1.22; r=max(W*S/im.width,H*S/im.height)
    big=im.resize((round(im.width*r),round(im.height*r)),Image.LANCZOS)
    n=int(round((c['dur']+(xf if i<len(cfg['cenas'])-1 else 0))*fps))
    mov=c.get('mov','in'); out=f'{tmp}/c{i}.mp4'
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-c:v','libx264','-preset','veryfast','-crf','16','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
    BW,BH=big.size
    for k in range(n):
        t=k/max(1,n-1); e=t*t*(3-2*t)
        z={'in':1+0.12*e,'out':1.12-0.12*e}.get(mov,1.07)
        ww=BW/(S*z)*S/S*1.0; ww=(W*BW/(W*S))/z
        wh=ww*H/W
        px={'left':1-e,'right':e}.get(mov,0.5); py={'up':1-e,'down':e}.get(mov,0.5)
        x0=(BW-ww)*px; y0=(BH-wh)*py
        fr=big.resize((W,H),Image.BICUBIC,box=(x0,y0,x0+ww,y0+wh))
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait(); clips.append(out)
# crossfade encadeado
ins=[]; [ins.extend(['-i',c]) for c in clips]
fc=[]; prev='0:v'; off=0
for i in range(1,len(clips)):
    off+=cfg['cenas'][i-1]['dur']
    fc.append(f"[{prev}][{i}:v]xfade=transition={cfg['cenas'][i].get('tr','fade')}:duration={xf}:offset={off:.3f}[v{i}]"); prev=f'v{i}'
subprocess.run(['ffmpeg','-y','-loglevel','error']+ins+['-filter_complex',';'.join(fc) if fc else 'null','-map',f'[{prev}]' if fc else '0:v','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','-r',str(fps),sys.argv[2]],check=True)
print('ok',sys.argv[2])
