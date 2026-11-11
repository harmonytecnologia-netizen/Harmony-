import numpy as np, potrace
from PIL import Image
im=Image.open('/mnt/user-data/uploads/Logo_MOVE_com_automação_e_segurança.png').convert('RGBA')
im=im.crop(im.getchannel('A').point(lambda v:255 if v>8 else 0).getbbox())
S=2; im=im.resize((im.width*S,im.height*S),Image.LANCZOS)
a=np.array(im).astype(float); A=a[...,3]>128
r,g,b=a[...,0],a[...,1],a[...,2]
mint=A&(g-r>60); cream=A&~mint
def mean(m): return tuple(int(a[...,i][m].mean()) for i in range(3))
cm,mm_=mean(cream),mean(mint); print(cm,mm_)
def path(mask):
    bm=potrace.Bitmap(~mask); pl=bm.trace(turdsize=4,alphamax=1.0,opticurve=True,opttolerance=0.2)
    d=[]
    for c in pl:
        s=c.start_point; d.append(f"M{s.x:.1f},{s.y:.1f}")
        for seg in c.segments:
            if seg.is_corner: d.append(f"L{seg.c.x:.1f},{seg.c.y:.1f}L{seg.end_point.x:.1f},{seg.end_point.y:.1f}")
            else: d.append(f"C{seg.c1.x:.1f},{seg.c1.y:.1f} {seg.c2.x:.1f},{seg.c2.y:.1f} {seg.end_point.x:.1f},{seg.end_point.y:.1f}")
        d.append('Z')
    return ''.join(d)
W,H=im.size
pc,pm=path(cream),path(mint)
hexc=lambda c:'#%02X%02X%02X'%c
def svg(fc,fm,name):
    open(name,'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><path fill="{fc}" fill-rule="evenodd" d="{pc}"/><path fill="{fm}" fill-rule="evenodd" d="{pm}"/></svg>')
svg(hexc(cm),hexc(mm_),'MOVE_logo_claro_vetor.svg')        # para tecido escuro
svg('#0D1B17',hexc(mm_),'MOVE_logo_escuro_vetor.svg')     # para tecido claro
svg('#FFFFFF','#FFFFFF','MOVE_logo_branco_1cor.svg')       # 1 cor (bordado/silk economico)
print(hexc(cm),hexc(mm_),W,H)
