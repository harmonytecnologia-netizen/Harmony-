"""Arte de post (feed 1080x1350) e story (1080x1920) a partir de uma foto + textos da marca.
uso: python3 arte_post.py foto.jpg "CHAMADA" "Titulo linha 1|linha 2" "detalhe pequeno" saida_feed.jpg saida_story.jpg [--ia]
--ia acrescenta a etiqueta de imagem ilustrativa (legenda_ia do marca.json).
"""
import sys, os
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from marca import carregar, fonte, titulo_fonte, espacado

def arte(m, foto, chamada, titulo, detalhe, w, h, out, ia):
    im = Image.open(foto).convert('RGB'); r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    im = im.crop(((im.width - w) // 2, (im.height - h) // 2, (im.width - w) // 2 + w, (im.height - h) // 2 + h)).convert('RGBA')
    g = Image.new('L', (1, h))
    for y in range(h):
        t = y / h; g.putpixel((0, y), int(255 * min(1, 0.5 * max(0, 1 - t / 0.15) + 0.95 * max(0, (t - 0.45) / 0.55) ** 1.4)))
    sh = Image.new('RGBA', (w, h), m['cor_fundo'] + (255,)); sh.putalpha(g.resize((w, h))); im.alpha_composite(sh)
    if m['logo_img'] is not None:
        L = m['logo_img']; l = L.resize((150, round(L.height * 150 / L.width)), Image.LANCZOS); im.alpha_composite(l, ((w - 150) // 2, 70))
    d = ImageDraw.Draw(im); linhas = titulo.split('|'); y = h - 330 - 92 * (len(linhas) - 1)
    espacado(d, 80, y - 64, chamada, fonte('media', 26), m['cor_destaque'] + (255,), 8)
    f = titulo_fonte(m, 78)
    for ln in linhas: d.text((76, y), ln, font=f, fill=m['cor_texto'] + (255,)); y += 92
    espacado(d, 80, y + 26, detalhe, fonte('leve', 26), m['cor_secundaria'] + (255,), 4)
    espacado(d, 0, h - 90, m['handle'], fonte('leve', 24), m['cor_secundaria'] + (255,), 7, True, w)
    if ia: d.text((w - 30 - d.textlength(m['legenda_ia'], font=fonte('leve', 20)), 30), m['legenda_ia'], font=fonte('leve', 20), fill=(220, 220, 220, 200))
    im.convert('RGB').save(out, quality=94)

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if x != '--ia']; ia = '--ia' in sys.argv; m = carregar()
    arte(m, a[0], a[1], a[2], a[3], 1080, 1350, a[4], ia)
    arte(m, a[0], a[1], a[2], a[3], 1080, 1920, a[5], ia)
    print('ok', a[4], a[5])
