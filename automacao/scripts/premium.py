"""Premium (alto padrão) layout: full-bleed realistic photo, serif title, minimal text."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

FD = '/home/claude/fonts/'
SERIF = FD + 'Playfair-400-normal.ttf'; SERIF_I = FD + 'Playfair-400-italic.ttf'
SANS_L = '/usr/share/fonts/opentype/inter/Inter-Light.otf'; SANS_M = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
CREAM = (244, 240, 232); MINT = (84, 223, 174); SUB = (205, 198, 186)
LOGO = Image.open('/mnt/user-data/uploads/Logo_MOVE_com_automação_e_segurança.png').convert('RGBA')
LOGO = LOGO.crop(LOGO.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox())

def grade(im):
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(0.92)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=2))
    return im

def cover(im, w, h, focus_y=0.5):
    r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = (im.width - w) // 2; y = int((im.height - h) * focus_y)
    return im.crop((x, y, x + w, y + h))

def shade(im, top=0.0, bottom=0.78, start=0.45):
    w, h = im.size
    g = Image.new('L', (1, h))
    for y in range(h):
        t = y / h
        a = top * max(0, 1 - t / 0.25) + bottom * max(0, (t - start) / (1 - start)) ** 1.6
        g.putpixel((0, y), int(255 * min(1, a)))
    layer = Image.new('RGB', (w, h), (8, 10, 9))
    return Image.composite(layer, im, g.resize((w, h)))

def tracked(d, x, y, text, font, fill, track, center_w=None):
    tw = sum(d.textlength(c, font=font) + track for c in text) - track
    if center_w: x = (center_w - tw) / 2
    for c in text:
        d.text((x, y), c, font=font, fill=fill); x += d.textlength(c, font=font) + track
    return tw

SANS_MED = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
KICK = (110, 235, 190)

def soft_shadow(im, draw_fn, blur=10, alpha=200):
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(layer), (0, 0, 0, alpha))
    base = im.convert('RGBA'); base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))
    return base.convert('RGB')

def logo(im, x, y, width, align='left'):
    l = LOGO.resize((width, round(LOGO.height * width / LOGO.width)), Image.LANCZOS)
    if align == 'center': x = (im.width - width) // 2
    im.paste(l, (int(x), int(y)), l)

def feed(photo, kicker, title_lines, body, out):
    W, H = 1080, 1350
    im = shade(grade(cover(photo, W, H, 0.45)), top=0.35, bottom=0.97, start=0.42)
    logo(im, 0, 64, 170, 'center')
    y0 = H - 120 - 92 * len(title_lines) - 130
    ft = ImageFont.truetype(SERIF, 76); fk = ImageFont.truetype(SANS_MED, 24)
    def txt(dd, col, y=y0):
        tracked(dd, 90, y, kicker, fk, col if col else KICK, 7); y += 56
        for ln in title_lines:
            dd.text((86, y), ln, font=ft, fill=col if col else CREAM); y += 92
        return y
    im = soft_shadow(im, lambda dd, c: txt(dd, c), 12, 230)
    d = ImageDraw.Draw(im); y = txt(d, None)
    d.line([(90, y + 26), (170, y + 26)], fill=(150, 140, 125), width=1)
    d.text((90, y + 50), body, font=ImageFont.truetype(SANS_L, 30), fill=SUB)
    tracked(d, 0, H - 58, '@move.s.a', ImageFont.truetype(SANS_L, 20), (160, 152, 140), 6, W)
    im.save(out, quality=94)
    return im

def story(photo, kicker, title_lines, body, out):
    W, H = 1080, 1920
    im = shade(grade(cover(photo, W, H, 0.5)), top=0.45, bottom=0.97, start=0.45)
    logo(im, 0, 120, 220, 'center')
    ft = ImageFont.truetype(SERIF, 90); fk = ImageFont.truetype(SANS_MED, 28)
    def txt(dd, col, y=1290):
        tracked(dd, 90, y, kicker, fk, col if col else KICK, 8); y += 66
        for ln in title_lines:
            dd.text((86, y), ln, font=ft, fill=col if col else CREAM); y += 108
        return y
    im = soft_shadow(im, lambda dd, c: txt(dd, c), 12, 230)
    d = ImageDraw.Draw(im); y = txt(d, None)
    d.line([(90, y + 30), (180, y + 30)], fill=(150, 140, 125), width=1)
    d.text((90, y + 58), body, font=ImageFont.truetype(SANS_L, 34), fill=SUB)
    tracked(d, 0, H - 150, '@move.s.a', ImageFont.truetype(SANS_L, 24), (170, 162, 150), 7, W)
    im.save(out, quality=94)
    return im

if __name__ == '__main__':
    src, outdir = sys.argv[1], sys.argv[2]
    ph = Image.open(src).convert('RGB')
    feed(ph, 'HOME CINEMA PRIVATIVO', ['O silêncio antes', 'do filme começar.'], 'Acústica, luz e som pensados juntos.', outdir + '/premium_feed.jpg')
    story(ph, 'HOME CINEMA PRIVATIVO', ['O silêncio antes', 'do filme começar.'], 'Acústica, luz e som pensados juntos.', outdir + '/premium_story.jpg')
