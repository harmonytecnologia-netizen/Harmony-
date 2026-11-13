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
    """Fundo escuro + verde da marca: foto desfocada e escurecida com brilho verde suave."""
    im = img(path, crop).resize((1080, 1920), Image.LANCZOS).filter(ImageFilter.GaussianBlur(28))
    im = ImageEnhance.Brightness(im).enhance(0.38); im = ImageEnhance.Color(im).enhance(0.55)
    base = Image.new('RGB', im.size, (13, 27, 23)); im = Image.blend(im, base, 0.45)
    glow = Image.new('L', im.size, 0); d = ImageDraw.Draw(glow)
    d.ellipse((-300, -200, 900, 900), fill=70); glow = glow.filter(ImageFilter.GaussianBlur(220))
    im = Image.composite(Image.new('RGB', im.size, (84, 223, 174)), im, glow.point(lambda v: v // 3))
    return im

def feed(ph, k, t, b, out): return P.feed(ph, k, t, b, out)
def story(ph, k, t, b, out): return P.story(ph, k, t, b, out)
