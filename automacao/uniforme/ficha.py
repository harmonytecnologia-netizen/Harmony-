from PIL import Image, ImageDraw, ImageFont
W,H=2480,3508  # A4 300dpi
FD='/home/claude/fonts/'; SERIF=FD+'Playfair-400-normal.ttf'
IL='/usr/share/fonts/opentype/inter/Inter-Light.otf'; IM='/usr/share/fonts/opentype/inter/Inter-Medium.otf'; IR='/usr/share/fonts/opentype/inter/Inter-Regular.otf'
DK=(13,27,23); MINT=(70,218,167); TXT=(30,36,33); GR=(110,118,114)
p=Image.new('RGB',(W,H),(250,249,246)); d=ImageDraw.Draw(p)
d.rectangle([0,0,W,330],fill=DK)
lc=Image.open('MOVE_logo_claro_vetor.png'); lw=620; lc=lc.resize((lw,round(lc.height*lw/lc.width)),Image.LANCZOS); p.paste(lc,(160,(330-lc.height)//2),lc)
d.text((W-160,120),'FICHA TÉCNICA — UNIFORME',font=ImageFont.truetype(IM,46),fill=(240,240,235),anchor='ra')
d.text((W-160,190),'Personalização: silk/DTF 2 cores ou bordado',font=ImageFont.truetype(IL,36),fill=(190,205,198),anchor='ra')
y=420
def h(t):
    global y; d.text((160,y),t,font=ImageFont.truetype(SERIF,64),fill=TXT); y+=100
def line(a,b):
    global y; d.text((160,y),a,font=ImageFont.truetype(IM,38),fill=TXT); d.text((760,y),b,font=ImageFont.truetype(IR,38),fill=TXT); y+=62
h('Cores da malha')
line('Cor 1 — Verde MOVE','verde quase preto (referência #0D1B17). Pedir amostra de malha.')
line('Cor 2 — Off-white','branco quente / algodão cru claro (sem preto: suja com gesso).')
y+=30; h('Cores da estampa')
sw=[((248,244,235),'Off-white','#F8F4EB'),((70,218,167),'Verde-menta','#46DAA7  (≈ Pantone 3385 C)')]
for c,n,code in sw:
    d.rounded_rectangle([160,y,260,y+70],12,fill=c,outline=(200,200,200)); d.text((300,y+12),n,font=ImageFont.truetype(IM,38),fill=TXT); d.text((760,y+12),code,font=ImageFont.truetype(IR,38),fill=TXT); y+=100
d.text((160,y),'Malha off-white: usar MOVE_logo_escuro_vetor.svg (verde-escuro #0D1B17 + verde-menta).',font=ImageFont.truetype(IL,36),fill=GR); y+=90
h('Peças e posição do logo')
rows=[('Camiseta manga curta','Frente: peito esquerdo, 9 cm de largura, 8 cm abaixo da gola.','Costas (parte alta): AUTOMAÇÃO / SOM / SEGURANÇA + onda + MOVE, 28 cm de largura, topo 6 cm abaixo da gola.'),
('Camiseta manga longa','Igual à manga curta.','Opcional: "SOM · AUTOMAÇÃO · SEGURANÇA" na manga esquerda, 2 cm de altura.'),
('Moletom com capuz','Frente: peito esquerdo, 10 cm (bordado recomendado).','Costas (parte alta): mesma arte, 30 cm de largura, topo 8 cm abaixo da costura do capuz.'),
('Calça jogger moletom','Coxa esquerda, abaixo do bolso: 8 cm de largura.',''),
('Bermuda moletom','Perna esquerda, 5 cm acima da barra: 7 cm de largura.','')]
for t,a,b in rows:
    d.text((160,y),t,font=ImageFont.truetype(IM,42),fill=TXT); y+=64
    for s in (a,b):
        if s: d.text((200,y),'•  '+s,font=ImageFont.truetype(IR,36),fill=TXT); y+=56
    y+=26
y+=20; h('Arquivos enviados')
for s in ['MOVE_logo_claro_vetor.svg — para malha escura (off-white + verde-menta)','MOVE_costas_claro.svg / MOVE_costas_escuro.svg — arte das costas (malha verde / malha off-white)','MOVE_logo_branco_1cor.svg — versão 1 cor','MOVE_logo_escuro_vetor.svg — para malha clara (se precisar)','PNGs 4000 px com fundo transparente das mesmas versões']:
    d.text((200,y),'•  '+s,font=ImageFont.truetype(IR,36),fill=TXT); y+=56
d.text((160,H-140),'MOVE  ·  @move.s.a  ·  (47) 99909-4744',font=ImageFont.truetype(IL,34),fill=GR)
p.save('ficha.png'); print(y)
