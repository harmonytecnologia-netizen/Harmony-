import math, re
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
logo_svg=open('MOVE_logo_claro_vetor.svg').read()
LW,LH=map(float,re.search(r'viewBox="0 0 (\S+) (\S+)"',logo_svg).groups())
paths=re.findall(r'<path fill="([^"]+)" fill-rule="evenodd" d="([^"]+)"/>',logo_svg)
W=3300  # unidades = 0.1 mm  -> 300 mm de largura
def text_path(txt,font_path,size,track):
    f=TTFont(font_path); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm; s=size/upm
    x=0; out=[]
    for ch in txt:
        g=cmap.get(ord(ch))
        if not g: continue
        pen=SVGPathPen(gs); tp=TransformPen(pen,(s,0,0,-s,x,0)); gs[g].draw(tp); out.append(pen.getCommands())
        x+=gs[g].width*s+track
    return ''.join(out), x-track
IM='/usr/share/fonts/opentype/inter/Inter-Medium.otf'; IL='/usr/share/fonts/opentype/inter/Inter-Light.otf'
def build(cream,mint,name):
    els=[]; y=0
    sc=W*0.40/LW; lx=(W-LW*sc)/2
    y=40
    for fill,d in paths:
        col=cream if fill!='#46DAA7' else mint
        els.append(f'<path transform="translate({lx:.1f},{y}) scale({sc:.5f})" fill="{col}" fill-rule="evenodd" d="{d}"/>')
    y+=LH*sc+120
    # onda sonora
    pts=[]; N=600
    for i in range(N+1):
        t=i/N; x=150+t*(W-300)
        env=math.sin(math.pi*t)**1.5
        a=110*env*(0.55+0.45*math.sin(2*math.pi*t*3.1+1))
        pts.append(f"{x:.1f},{y+150-a*math.sin(2*math.pi*t*11):.1f}")
    els.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{mint}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>')
    pts2=[]
    for i in range(N+1):
        t=i/N; x=150+t*(W-300); env=math.sin(math.pi*t)**2
        a=70*env*(0.6+0.4*math.cos(2*math.pi*t*2.3))
        pts2.append(f"{x:.1f},{y+150+a*math.sin(2*math.pi*t*7+0.8):.1f}")
    els.append(f'<polyline points="{" ".join(pts2)}" fill="none" stroke="{cream}" stroke-opacity="0.55" stroke-width="9" stroke-linecap="round"/>')
    y+=300+150
    IB='/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
    d,tw=text_path('AUTOMAÇÃO',IB,100,8); size=100*(W*0.80)/tw
    for word in ['AUTOMAÇÃO','SOM','SEGURANÇA']:
        d,tw=text_path(word,IB,size,8*size/100); y+=size*0.78
        els.append(f'<path transform="translate({(W-tw)/2:.1f},{y:.1f})" fill="{cream}" d="{d}"/>'); y+=size*0.22
    y+=size*0.35
    d,tw=text_path('@move.s.a   ·   (47) 99909-4744',IL,95,10); els.append(f'<path transform="translate({(W-tw)/2:.1f},{y})" fill="{mint}" d="{d}"/>')
    H=y+60
    open(name,'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" width="300mm" height="{H/10:.0f}mm">'+''.join(els)+'</svg>')
build('#F8F4EB','#46DAA7','MOVE_costas_claro.svg')
build('#0D1B17','#2BB98A','MOVE_costas_escuro.svg')
