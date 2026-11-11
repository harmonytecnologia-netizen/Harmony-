from PIL import Image, ImageFilter
logo=Image.open('MOVE_logo_claro_vetor.png').convert('RGBA')
def place(im,cx,cy,w,lg=None):
    l=(lg or logo); l=l.resize((w,round(l.height*w/l.width)),Image.LANCZOS)
    l.putalpha(l.getchannel('A').point(lambda p:int(p*0.92)))
    l=l.filter(ImageFilter.GaussianBlur(0.4))
    im.alpha_composite(l,(int(cx-l.width/2),int(cy-l.height/2)))
def run(src,out,pts,lg=None):
    im=Image.open(src).convert('RGBA')
    for cx,cy,w in pts: place(im,cx,cy,w,lg)
    im.convert('RGB').save(out)
