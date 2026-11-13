"""Plano B: artes premium a partir de imagens do repositório (sem ChatGPT/PC).
fundo(img) -> foto; dark(img) -> fundo escuro desfocado da marca para slides de dica."""
import sys, os
REPO = os.path.abspath(os.path.dirname(__file__) + '/../..')
sys.path.insert(0, REPO + '/automacao/scripts')
import premium as P
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw

def img(path, crop=None, flip=False):
    im = Image.open(REPO + '/' + path).convert('RGB')
    if crop:  # (x0,y0,x1,y1) fractions -> novo enquadramento
        w, h = im.size; im = im.crop((int(crop[0]*w), int(crop[1]*h), int(crop[2]*w), int(crop[3]*h)))
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im

def dark(path, crop=None):
    """Slide de dica: fundo escuro + verde da marca, com a foto em um quadro (cartão) no alto."""
    src = img(path, crop)
    im = P.cover(src, 1080, 1350).filter(ImageFilter.GaussianBlur(30))
    im = ImageEnhance.Brightness(im).enhance(0.38); im = ImageEnhance.Color(im).enhance(0.55)
    base = Image.new('RGB', im.size, (13, 27, 23)); im = Image.blend(im, base, 0.45)
    glow = Image.new('L', im.size, 0); d = ImageDraw.Draw(glow)
    d.ellipse((-300, -200, 900, 900), fill=70); glow = glow.filter(ImageFilter.GaussianBlur(220))
    im = Image.composite(Image.new('RGB', im.size, (84, 223, 174)), im, glow.point(lambda v: v // 3))
    card = P.grade(P.cover(src, 900, 560))
    m = Image.new('L', card.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 899, 559), 26, fill=255)
    sh = Image.new('L', im.size, 0); ImageDraw.Draw(sh).rounded_rectangle((90, 196, 990, 756), 26, fill=150)
    im = Image.composite(Image.new('RGB', im.size, (0, 0, 0)), im, sh.filter(ImageFilter.GaussianBlur(24)))
    im.paste(card, (90, 180), m)
    ImageDraw.Draw(im).rounded_rectangle((90, 180, 989, 739), 26, outline=(44, 68, 58), width=2)
    return im

from PIL import ImageFont
def check(lines, kind):
    f = ImageFont.truetype(P.SERIF, 76 if kind == 'feed' else 90); d = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    for ln in lines:
        w = d.textlength(ln, font=f)
        assert w < 1080 - 86 - 70, f'texto largo demais ({int(w)}px): {ln}'


def feed(ph, k, t, b, out): return P.feed(ph, k, t, b, out)
def story(ph, k, t, b, out): return P.story(ph, k, t, b, out)
