"""Utilidades comuns: carrega marca.json, fontes do kit e desenha texto."""
import json, os
from PIL import Image, ImageFont

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.join(KIT, 'fontes')
W, H = 1080, 1920

def hexrgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def carregar(caminho=None):
    caminho = caminho or os.environ.get('MARCA', os.path.join(KIT, 'marca.json'))
    m = json.load(open(caminho, encoding='utf-8'))
    base = os.path.dirname(os.path.abspath(caminho))
    for k in [k for k in m if k.startswith('cor_')]:
        m[k] = hexrgb(m[k])
    lp = m.get('logo')
    m['logo_img'] = None
    if lp:
        lp = lp if os.path.isabs(lp) else os.path.join(base, lp)
        if os.path.exists(lp):
            im = Image.open(lp).convert('RGBA')
            bb = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
            m['logo_img'] = im.crop(bb) if bb else im
    return m

def fonte(nome, tam):
    arq = {'leve': 'Inter-Light.otf', 'media': 'Inter-Medium.otf', 'semi': 'Inter-SemiBold.otf',
           'negrito': 'Inter-Bold.otf', 'preta': 'Inter-Black.otf', 'serifa': 'Playfair-Regular.ttf'}[nome]
    return ImageFont.truetype(os.path.join(FONTES, arq), tam)

def titulo_fonte(m, tam):
    return fonte('serifa', tam) if m.get('estilo', 'premium') == 'premium' else fonte('preta', int(tam * 0.92))

def espacado(d, x, y, texto, f, cor, esp, centro=False, largura=W):
    tw = sum(d.textlength(c, font=f) + esp for c in texto) - esp
    if centro: x = (largura - tw) / 2
    for c in texto:
        d.text((x, y), c, font=f, fill=cor); x += d.textlength(c, font=f) + esp
