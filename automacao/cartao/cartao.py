import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
DPI=600; mm=lambda v: round(v*DPI/25.4)
W,H=mm(96),mm(56); B=mm(3)  # 90x50 + 3mm sangria
FD='/home/claude/fonts/'; SERIF=FD+'Playfair-400-normal.ttf'
IL='/usr/share/fonts/opentype/inter/Inter-Light.otf'; IM='/usr/share/fonts/opentype/inter/Inter-Medium.otf'
CREAM=(244,240,232); MINT=(84,223,174); SUB=(196,206,200)
tex=Image.open('textura.png').convert('RGB')
def bg(flip=False):
    t=tex.transpose(Image.FLIP_LEFT_RIGHT) if flip else tex
    r=max(W/t.width,H/t.height); t=t.resize((round(t.width*r),round(t.height*r)),Image.LANCZOS)
    x=(t.width-W)//2; y=(t.height-H)//2; return t.crop((x,y,x+W,y+H))
L=Image.open('/mnt/user-data/uploads/Logo_MOVE_com_automação_e_segurança.png').convert('RGBA')
L=L.crop(L.getchannel('A').point(lambda v:255 if v>8 else 0).getbbox())
def tracked(d,x,y,s,f,fill,tr,center_w=None,cx=None):
    tw=sum(d.textlength(c,font=f)+tr for c in s)-tr
    if cx is not None: x=cx-tw/2
    for c in s: d.text((x,y),c,font=f,fill=fill); x+=d.textlength(c,font=f)+tr
    return tw
# FRENTE
f=bg(); f=ImageEnhance.Brightness(f).enhance(0.92)
w=mm(52); l=L.resize((w,round(L.height*w/L.width)),Image.LANCZOS)
im=f.convert('RGBA'); a=l.getchannel('A')
sh=Image.new('RGBA',(W,H),(0,0,0,0)); s=Image.new('RGBA',l.size,(0,0,0,0)); s.putalpha(a.point(lambda p:int(p*.6)))
x=(W-w)//2; y=(H-l.height)//2-mm(2)
sh.paste(s,(x,y+mm(.5)),s); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(mm(.6)))); im.alpha_composite(l,(x,y))
d=ImageDraw.Draw(im)
tracked(d,0,H-B-mm(8),'@move.s.a',ImageFont.truetype(IL,mm(2.2)),SUB,mm(.5),cx=W/2)
im.convert('RGB').save('frente.png',dpi=(DPI,DPI))
# VERSO
v=ImageEnhance.Brightness(bg(True)).enhance(0.85).convert('RGBA'); d=ImageDraw.Draw(v)
X=B+mm(6); Y=B+mm(5.5)
d.text((X,Y),'Projetos sob medida',font=ImageFont.truetype(SERIF,mm(3.6)),fill=CREAM)
tracked(d,X,Y+mm(5.8),'ALTO PADRÃO',ImageFont.truetype(IM,mm(1.7)),MINT,mm(.55))
items=['Sonorização e som ambiente','Home theater e cinema em casa','Automação residencial','Segurança e redes']
fy=Y+mm(9.8); fi=ImageFont.truetype(IL,mm(2.15))
for it in items:
    d.ellipse([X,fy+mm(.85),X+mm(.9),fy+mm(1.75)],fill=MINT); d.text((X+mm(2.3),fy),it,font=fi,fill=CREAM); fy+=mm(3.3)
d.line([(X,fy+mm(1.2)),(X+mm(8),fy+mm(1.2))],fill=(150,160,150),width=mm(.15))
d.text((X,fy+mm(2.4)),'(47) 99909-4744',font=ImageFont.truetype(IM,mm(2.5)),fill=CREAM)
d.text((X,fy+mm(5.9)),'harmonytecnologia@gmail.com',font=ImageFont.truetype(IL,mm(1.9)),fill=SUB)
# QRs
def qr(url):
    q=qrcode.QRCode(border=0,error_correction=qrcode.constants.ERROR_CORRECT_M,box_size=20); q.add_data(url); q.make(fit=True)
    return q.make_image(fill_color=(13,27,23),back_color=(244,240,232)).convert('RGB')
qs=mm(13); pad=mm(1.1); gx=W-B-mm(5)-qs; 
for i,(url,lab) in enumerate([('https://instagram.com/move.s.a','INSTAGRAM'),('https://wa.me/5547999094744','WHATSAPP')]):
    gy=B+mm(6)+i*(qs+pad*2+mm(4.6))
    card=Image.new('RGBA',(qs+pad*2,qs+pad*2),(0,0,0,0)); ImageDraw.Draw(card).rounded_rectangle([0,0,qs+pad*2-1,qs+pad*2-1],mm(1.2),fill=CREAM+(255,))
    card.paste(qr(url).resize((qs,qs),Image.NEAREST),(pad,pad))
    v.alpha_composite(card,(gx-pad,gy-pad))
    tracked(d,0,gy+qs+pad+mm(.9),lab,ImageFont.truetype(IM,mm(1.45)),MINT,mm(.45),cx=gx+qs/2)
v.convert('RGB').save('verso.png',dpi=(DPI,DPI))
# PDF (tamanho com sangria)
fr=Image.open('frente.png'); vr=Image.open('verso.png')
fr.save('MOVE_cartao_visita_grafica.pdf',save_all=True,append_images=[vr],resolution=DPI)
# previews sem sangria
for n in ['frente','verso']:
    Image.open(n+'.png').crop((B,B,W-B,H-B)).resize((900,500),Image.LANCZOS).save(n+'_prev.jpg',quality=92)
print(W,H)
