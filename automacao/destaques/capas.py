from PIL import Image, ImageDraw, ImageFont, ImageFilter
R='/home/claude/harmony-/'; F=R+'kit_instagram/fontes/'
src=Image.open('icones_chatgpt.png').convert('RGB')
cx=[195,481,767,1053,1340]; cy=507; r=150
itens=[('casos','CASOS DA MOVE','Problemas reais que a gente resolveu'),
       ('som','APRENDENDO SOBRE SOM','Dicas para o seu som soar como deve'),
       ('automacao','AUTOMAÇÃO','Luz, cortina, cenas e comando de voz'),
       ('projetos','PROJETOS','Obras e instalações da MOVE'),
       ('orcamento','ORÇAMENTO','Chame no direct e envie a sua planta')]
logo=Image.open(R+'automacao/assets/logo_claro.png').convert('RGBA')
logo=logo.resize((260,int(260*logo.height/logo.width)))
for (k,t,s),x in zip(itens,cx):
    W,H=1080,1920
    bg=Image.new('RGB',(W,H),(13,27,23))
    # brilho suave no centro
    g=Image.new('L',(W,H),0); ImageDraw.Draw(g).ellipse((140,560,940,1360),fill=90); g=g.filter(ImageFilter.GaussianBlur(160))
    bg=Image.composite(Image.new('RGB',(W,H),(26,60,48)),bg,g)
    ic=src.crop((x-r,cy-r,x+r,cy+r)).resize((620,620),Image.LANCZOS)
    m=Image.new('L',(620,620),0); ImageDraw.Draw(m).ellipse((4,4,616,616),fill=255); m=m.filter(ImageFilter.GaussianBlur(3))
    bg.paste(ic,(230,650),m)
    im=bg.convert('RGBA'); im.alpha_composite(logo,((W-logo.width)//2,150))
    d=ImageDraw.Draw(im)
    f=ImageFont.truetype(F+'Inter-Bold.otf',64)
    while d.textlength(t,font=f)>960: f=ImageFont.truetype(F+'Inter-Bold.otf',f.size-4)
    d.text(((W-d.textlength(t,font=f))/2,1390),t,font=f,fill=(242,245,239))
    fs=ImageFont.truetype(F+'Inter-Light.otf',38)
    d.text(((W-d.textlength(s,font=fs))/2,1490),s,font=fs,fill=(169,187,179))
    fh=ImageFont.truetype(F+'Inter-Medium.otf',32); h='@move.s.a'
    d.text(((W-d.textlength(h,font=fh))/2,1760),h,font=fh,fill=(84,223,174))
    im.convert('RGB').save(f'capa_{k}.jpg',quality=95)
