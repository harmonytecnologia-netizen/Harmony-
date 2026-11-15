import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R='/home/claude/harmony-/'
W,H=1080,1920
FS=R+'kit_instagram/fontes/'
def fnt(sz):
    import glob
    return ImageFont.truetype(FS+'Inter-SemiBold.otf',sz)
def faz(out, texto, diam=230, y=1180, nome=True):
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    face=Image.open(R+'automacao/iamin/iamin_close_pad.png').convert('RGB')
    # recorte do rosto
    fc=face.crop((230,240,480,490)).resize((diam,diam),Image.LANCZOS)
    m=Image.new('L',(diam,diam),0); ImageDraw.Draw(m).ellipse((0,0,diam-1,diam-1),fill=255)
    x0=60
    d=ImageDraw.Draw(im)
    d.ellipse((x0-6,y-6,x0+diam+6,y+diam+6),fill=(84,223,174,255))
    im.paste(fc,(x0,y),m)
    f=fnt(44); fn=fnt(30)
    # balão
    linhas=texto.split('\n'); lw=max(d.textlength(l,font=f) for l in linhas)
    bx=x0+diam+40; by=y+diam//2-(len(linhas)*58+70)//2
    bw=lw+70; bh=len(linhas)*58+(70 if nome else 40)
    d.rounded_rectangle((bx,by,bx+bw,by+bh),36,fill=(13,27,23,235),outline=(84,223,174,255),width=4)
    d.polygon([(bx,by+bh//2-18),(bx-26,by+bh//2),(bx,by+bh//2+18)],fill=(84,223,174,255))
    yy=by+22
    if nome: d.text((bx+35,yy),'IAMIN · MOVE',font=fn,fill=(84,223,174,255)); yy+=44
    for l in linhas: d.text((bx+35,yy),l,font=f,fill=(242,245,239,255)); yy+=58
    im.save(out)
faz('ov_iamin1.png','Isso acontece muito.\nPresta atenção!')
faz('ov_iamin2.png','Olha onde estava\no problema...')
faz('ov_iamin3.png','E você, o que faria?\nComenta aí!',diam=280,y=1150)
