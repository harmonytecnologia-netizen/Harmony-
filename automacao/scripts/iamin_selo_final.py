import sys,os
sys.path.insert(0,'/home/claude/harmony-/kit_instagram/scripts')
from marca import fonte,W,H
from PIL import Image,ImageDraw,ImageFilter
A='/home/claude/harmony-/automacao/'
MINT=(70,218,167); BG=(10,13,12); TX=(242,240,234); SEC=(169,162,150)
def badge(out,nome='Iamin · MOVE',y=1250,conceito=True):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    av=Image.open(A+'iamin/avatar.png').convert('RGBA').resize((150,150),Image.LANCZOS)
    x=60
    d.rounded_rectangle([x-8,y-8,x+150+300,y+158],80,fill=BG+(200,))
    d.ellipse([x-5,y-5,x+155,y+155],outline=MINT+(255,),width=5)
    m=Image.new('L',(150,150),0); ImageDraw.Draw(m).ellipse([0,0,149,149],fill=255); im.paste(av,(x,y),m)
    d.text((x+175,y+38),'Iamin',font=fonte('negrito',40),fill=TX+(255,))
    d.text((x+175,y+90),'da MOVE explica',font=fonte('media',28),fill=MINT+(255,))
    if conceito:
        f=fonte('leve',24); t='Ambiente conceito.'; d.text((W-60-d.textlength(t,font=f),1830),t,font=f,fill=SEC+(220,))
    im.save(out)
def final(out,frase='Fale com a gente.',sub='Orçamento pelo direct  ·  @move.s.a'):
    im=Image.new('RGBA',(W,H),BG+(255,)); d=ImageDraw.Draw(im)
    g=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(g).ellipse([140,560,940,1260],fill=MINT+(40,)); g=g.filter(ImageFilter.GaussianBlur(160)); im.alpha_composite(g)
    lg=Image.open(A+'assets/logo_claro.png').convert('RGBA'); bb=lg.getchannel('A').getbbox(); lg=lg.crop(bb)
    lw=560; lg=lg.resize((lw,round(lg.height*lw/lg.width)),Image.LANCZOS); im.alpha_composite(lg,((W-lw)//2,700))
    f=fonte('serifa',78); d.text(((W-d.textlength(frase,font=f))/2,1000),frase,font=f,fill=TX+(255,))
    f2=fonte('media',34); d.text(((W-d.textlength(sub,font=f2))/2,1120),sub,font=f2,fill=MINT+(255,))
    im.save(out)
if __name__=='__main__':
    badge('/home/claude/w/badge.png'); final('/home/claude/w/final.png')
