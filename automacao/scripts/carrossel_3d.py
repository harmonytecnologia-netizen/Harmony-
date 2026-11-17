"""Carrossel/story premium a partir de quadros 3D (1080x1350 / 1080x1920). Uso: importar slide()/story3d()."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from premium import shade, grade, cover, logo, tracked, soft_shadow, SERIF, SANS_L, SANS_MED, CREAM, KICK, SUB
from PIL import Image, ImageDraw, ImageFont
VERM = (255, 92, 80)

def _txt(im, y0, num, kick, lines, body, W, ft_size, cor_num=KICK):
    ft = ImageFont.truetype(SERIF, ft_size); fk = ImageFont.truetype(SANS_MED, 26); fb = ImageFont.truetype(SANS_L, 32)
    def draw(dd, col):
        y = y0
        if num: dd.text((90, y - 6), num, font=ImageFont.truetype(SERIF, 64), fill=col or cor_num); y += 84
        tracked(dd, 92, y, kick, fk, col or KICK, 7); y += 58
        for ln in lines: dd.text((86, y), ln, font=ft, fill=col or CREAM); y += int(ft_size * 1.18)
        return y
    im = soft_shadow(im, lambda dd, c: draw(dd, c), 12, 230)
    d = ImageDraw.Draw(im); y = draw(d, None)
    if body:
        d.line([(92, y + 24), (172, y + 24)], fill=(150, 140, 125), width=1)
        yy = y + 46
        for ln in body.split('|'): d.text((92, yy), ln, font=fb, fill=SUB); yy += 44
    return im

def slide(foto, num, kick, lines, body, out, n=None, total=None, focus=0.5, cor_num=KICK):
    W, H = 1080, 1350
    im = shade(grade(cover(foto, W, H, focus)), top=0.35, bottom=0.96, start=0.35)
    logo(im, 0, 60, 150, 'center')
    nb = len(body.split('|')) if body else 0
    y0 = H - 140 - int(76 * 1.18) * len(lines) - 58 - (84 if num else 0) - nb * 44
    im = _txt(im, y0, num, kick, lines, body, W, 76, cor_num)
    d = ImageDraw.Draw(im)
    if n: tracked(d, 0, H - 64, f'{n}/{total}   ·   @move.s.a', ImageFont.truetype(SANS_L, 20), (160, 152, 140), 5, W)
    im.save(out, quality=94); return im

def story3d(foto, kick, lines, body, out, focus=0.5, extra=None):
    W, H = 1080, 1920
    im = shade(grade(cover(foto, W, H, focus)), top=0.45, bottom=0.97, start=0.42)
    logo(im, 0, 120, 220, 'center')
    im = _txt(im, 1180, None, kick, lines, body, W, 92)
    d = ImageDraw.Draw(im)
    if extra:  # botões de enquete
        fb = ImageFont.truetype(SANS_MED, 40); x = 92
        for lab in extra:
            w = d.textlength(lab, font=fb) + 80
            d.rounded_rectangle([x, 1700, x + w, 1790], 45, outline=KICK, width=3); d.text((x + 40, 1722), lab, font=fb, fill=CREAM); x += w + 30
    tracked(d, 0, H - 90, "@move.s.a", ImageFont.truetype(SANS_L, 24), (170, 162, 150), 7, W)
    im.save(out, quality=94); return im
