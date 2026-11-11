import numpy as np, math, sys
from PIL import Image
from scipy import ndimage
from skimage import measure
import pyembroidery as pe
SRC='../uniforme/MOVE_logo_claro_vetor.png'
WIDTH_MM=float(sys.argv[1]) if len(sys.argv)>1 else 100
im=Image.open(SRC).convert('RGBA'); a=np.array(im)
A=a[...,3]>128
rows=np.where(A.any(1))[0]
# corta a linha pequena "SOM · AUTOMAÇÃO · SEGURANÇA": acha o maior vão horizontal
gaps=np.where(np.diff(rows)>5)[0]
cut=rows[gaps[-1]]+1 if len(gaps) else a.shape[0]
a=a[:cut]; A=A[:cut]
ys,xs=np.where(A); a=a[ys.min():ys.max()+1, xs.min():xs.max()+1]
img=Image.fromarray(a); s=WIDTH_MM*10/img.width   # 1 px = 0.1 mm
img=img.resize((round(img.width*s),round(img.height*s)),Image.LANCZOS); a=np.array(img).astype(int)
A=a[...,3]>128; mint=A&((a[...,1]-a[...,0])>60); cream=A&~mint
mint=ndimage.binary_opening(mint,iterations=1); cream=ndimage.binary_opening(cream,iterations=1)
H,W=A.shape; print('tamanho mm',W/10,H/10)
ROW=4; MAXST=30; MINST=6
def runs_of(mask):
    runs=[]; openr=[]
    for y in range(1,H-1,ROW):
        r=mask[y]; segs=[]; x=0
        d=np.diff(np.concatenate([[0],r.astype(int),[0]])); st=np.where(d==1)[0]; en=np.where(d==-1)[0]
        segs=[(s0+1,e0-2) for s0,e0 in zip(st,en) if e0-s0>=4]
        new_open=[]
        used=set()
        for sg in segs:
            cand=[i for i,(run) in enumerate(openr) if i not in used and not (run[-1][2]<sg[0] or run[-1][1]>sg[1])]
            if len(cand)==1:
                # só continua se o segmento anterior também só toca este
                prev=openr[cand[0]][-1]; touches=[q for q in segs if not (q[1]<prev[1] or q[0]>prev[2])]
                if len(touches)==1:
                    openr[cand[0]].append((y,)+sg); used.add(cand[0]); new_open.append(openr[cand[0]]); continue
            nr=[(y,)+sg]; runs.append(nr); new_open.append(nr)
        openr=new_open
    return runs
def fill_run(run,k0=0):
    pts=[]
    for k,(y,x0,x1) in enumerate(run):
        xsr=[x0,x1] if k%2==0 else [x1,x0]
        L=abs(x1-x0); n=max(1,math.ceil(L/MAXST)); off=(k%3)*MAXST/3
        line=[xsr[0]]
        step=MAXST*(1 if xsr[1]>xsr[0] else -1)
        p=xsr[0]+ (off if xsr[1]>xsr[0] else -off)
        if abs(p-xsr[0])<MINST: p+=step
        while (p-xsr[1])*(1 if step>0 else -1)<-MINST:
            line.append(p); p+=step
        line.append(xsr[1])
        pts+= [(x,y) for x in line]
    return pts
def contour_run(mask):
    out=[]
    for c in measure.find_contours(mask.astype(float),0.5):
        if len(c)<20: continue
        c=c[::1]; seg=[(c[0][1],c[0][0])]; acc=0
        for i in range(1,len(c)):
            acc+=math.dist(c[i],c[i-1])
            if acc>=25: seg.append((c[i][1],c[i][0])); acc=0
        seg.append(seg[0]); out.append(seg)
    return out
pat=pe.EmbPattern()
def add_block(mask,color):
    pat.add_thread({'color':color})
    first=True; cur=None
    def go(pts):
        nonlocal first,cur
        if not pts: return
        if cur is not None and math.dist(cur,pts[0])>30:
            pat.add_stitch_absolute(pe.TRIM,cur[0],cur[1])
            pat.add_stitch_absolute(pe.JUMP,pts[0][0],pts[0][1])
        elif cur is None:
            pat.add_stitch_absolute(pe.JUMP,pts[0][0],pts[0][1])
        for x,y in pts: pat.add_stitch_absolute(pe.STITCH,x,y)
        # nós de travamento
        cur=pts[-1]
    # underlay: contorno levemente para dentro
    inner=ndimage.binary_erosion(mask,iterations=5)
    for c in contour_run(inner): go(c)
    rs=runs_of(mask)
    rs.sort(key=lambda r:(r[0][1],r[0][0]))
    rem=rs[:]
    while rem:
        if cur is None: r=rem.pop(0)
        else:
            i=min(range(len(rem)),key=lambda i:math.dist(cur,(rem[i][0][1],rem[i][0][0])))
            r=rem.pop(i)
        go(fill_run(r))
    pat.add_stitch_absolute(pe.TRIM,cur[0],cur[1])
add_block(mint,'#46DAA7')
pat.add_command(pe.COLOR_CHANGE)
add_block(cream,'#F8F4EB')
pat.add_command(pe.END)
pat.move_center_to_origin()
tag=f'{int(WIDTH_MM)}mm'
for ext in ['dst','pes','jef','exp']:
    pe.write(pat,f'MOVE_bordado_{tag}.{ext}')
pe.write_png(pat,f'sim_{tag}.png',{'background':'#0D1B17','linewidth':2})
n=sum(1 for s in pat.stitches if s[2]==pe.STITCH); print('pontos',n,'trocas de cor',pat.count_color_changes())
