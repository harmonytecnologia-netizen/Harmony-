import math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

S = '/tmp/claude-0/-home-claude/ab8790be-2718-53fe-a112-dc9313667f61/scratchpad/'
P = S + 'posts/'
FB = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
FS = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
FM = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
FR = '/usr/share/fonts/opentype/inter/Inter-Regular.otf'
BG = (13, 27, 23); BG2 = (20, 40, 33); MINT = (84, 223, 174); CREAM = (242, 245, 239); SUB = (169, 187, 179); LINE = (44, 68, 58)
LOGO = Image.open('/mnt/user-data/uploads/Logo_MOVE_com_automação_e_segurança.png').convert('RGBA')
LOGO = LOGO.crop(LOGO.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox())

def F(path, size): return ImageFont.truetype(path, size)

def bg(w, h):
    im = Image.new('RGB', (w, h), BG)
    g = Image.new('L', (w, h), 0); d = ImageDraw.Draw(g)
    d.ellipse([-w * 0.3, -h * 0.25, w * 1.0, h * 0.6], fill=120)
    g = g.filter(ImageFilter.GaussianBlur(w * 0.25))
    im = Image.composite(Image.new('RGB', (w, h), BG2), im, g)
    noise = Image.effect_noise((w, h), 18).convert('RGB')
    return Image.blend(im, noise, 0.025)

def photo_bg(path, w, h, dark=0.55, grad=True):
    ph = Image.open(path).convert('RGB')
    r = max(w / ph.width, h / ph.height)
    ph = ph.resize((int(ph.width * r) + 1, int(ph.height * r) + 1), Image.LANCZOS)
    x = (ph.width - w) // 2; y = (ph.height - h) // 2
    ph = ph.crop((x, y, x + w, y + h))
    ph = ImageEnhance.Color(ph).enhance(0.8)
    ph = Image.blend(ph, Image.new('RGB', (w, h), (40, 32, 18)), 0.08)
    ov = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    if grad:
        g = Image.new('L', (1, h))
        for yy in range(h): g.putpixel((0, yy), int(255 * (dark * 0.35 + dark * 0.65 * (yy / h) ** 1.2)))
        g = g.resize((w, h))
        layer = Image.new('RGBA', (w, h), BG + (255,)); layer.putalpha(g); ov = layer
    out = ph.convert('RGBA'); out.alpha_composite(ov)
    return out.convert('RGB')

def logo(im, cx, y, width):
    l = LOGO.resize((width, round(LOGO.height * width / LOGO.width)), Image.LANCZOS)
    im.paste(l, (int(cx - width / 2), int(y)), l)
    return l.height

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ''
    for wd in words:
        t = (cur + ' ' + wd).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = wd
    lines.append(cur); return lines

def text_block(d, x, y, text, font, fill, maxw, lh):
    for ln in wrap(d, text, font, maxw):
        d.text((x, y), ln, font=font, fill=fill); y += lh
    return y

def tracked(d, xy, text, font, fill, track):
    x, y = xy
    for c in text:
        d.text((x, y), c, font=font, fill=fill); x += d.textlength(c, font=font) + track
    return x

def tag(d, x, y, text, size=26):
    f = F(FS, size)
    d.rectangle([x, y + size * 0.55, x + 56, y + size * 0.55 + 4], fill=MINT)
    tracked(d, (x + 74, y), text, f, MINT, 5)

def handle(d, w, y):
    f = F(FM, 28); t = '@move.s.a'
    tw = sum(d.textlength(c, font=f) + 6 for c in t)
    tracked(d, ((w - tw) / 2, y), t, f, SUB, 6)

# ---------------- icons (line art, mint) ----------------
def icon(kind, size=340, stroke=10):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = size / 2; m = MINT + (255,); m2 = MINT + (110,)
    if kind == 'speaker':
        d.line([(30, 70), (size - 30, 70)], fill=CREAM + (200,), width=6)
        for r, col in [(110, m), (78, m), (40, m)]:
            d.ellipse([c - r, c + 10 - r, c + r, c + 10 + r], outline=col, width=stroke)
        for k in range(3):
            r = 135 + k * 22
            d.arc([c - r, c + 10 - r, c + r, c + 10 + r], 30, 150, fill=m2, width=6)
    elif kind == 'tv':
        d.rounded_rectangle([30, 70, size - 30, 250], 14, outline=m, width=stroke)
        d.line([(c, 250), (c, 300)], fill=m, width=stroke); d.line([(c - 60, 300), (c + 60, 300)], fill=m, width=stroke)
        for k, dx in enumerate([-30, 0, 30]):
            d.line([(c + dx, 70), (c + dx, 10)], fill=m2, width=6)
        d.polygon([(c - 25, 130), (c - 25, 195), (c + 30, 162)], outline=m, width=6)
    elif kind == 'wifi':
        for k, r in enumerate([150, 105, 60]):
            d.arc([c - r, c + 40 - r, c + r, c + 40 + r], 220, 320, fill=m, width=stroke)
        d.ellipse([c - 16, c + 24, c + 16, c + 56], fill=m)
        d.line([(40, 300), (size - 40, 300)], fill=m2, width=6)
    elif kind == 'switch':
        d.rounded_rectangle([70, 40, size - 70, size - 40], 24, outline=m, width=stroke)
        for k in range(3):
            y = 80 + k * 72
            d.rounded_rectangle([110, y, size - 110, y + 50], 12, outline=m if k != 1 else m, width=6, fill=(MINT + (255,)) if k == 1 else None)
        for k in range(4):
            a = math.radians(-60 + k * 40)
            d.line([(size - 40 + 0 * a, 60), (size - 40 + 40 * math.cos(a), 60 + 40 * math.sin(a))], fill=m2, width=5)
    elif kind == 'rack':
        d.rounded_rectangle([80, 30, size - 80, size - 30], 14, outline=m, width=stroke)
        for k in range(4):
            y = 70 + k * 62
            d.rectangle([110, y, size - 110, y + 40], outline=m, width=5)
            d.ellipse([size - 140, y + 14, size - 128, y + 26], fill=m)
        for k in range(3):
            d.line([(c - 40 + k * 40, size - 30), (c - 40 + k * 40, size)], fill=m2, width=5)
    return im

# ---------------- CAROUSEL 1080x1350 ----------------
W, H = 1080, 1350
def slide_num(n, total=7):
    im = None
    return f'{n}/{total}'

def cover():
    im = photo_bg(P + 'fr_A_5.5.jpg', W, H, dark=0.95); d = ImageDraw.Draw(im)
    logo(im, 190, 70, 260)
    tag(d, 80, 700, 'ANTES DO GESSO')
    y = text_block(d, 80, 760, '5 pontos para planejar o som e a automação da sua casa', F(FB, 78), CREAM, 900, 92)
    d.text((80, y + 40), 'Arraste para o lado  →', font=F(FM, 32), fill=MINT)
    d.text((W - 140, H - 80), '1/7', font=F(FM, 26), fill=SUB)
    return im

TIPS = [
    ('speaker', 'Caixas de som no forro', 'Defina a posição das caixas de embutir e deixe o cabo de som passado até o local do amplificador.'),
    ('tv', 'TV, telão e cinema em casa', 'Tubulação livre atrás da TV ou até o projetor para HDMI, rede e energia, sem fios aparentes.'),
    ('wifi', 'Wi-Fi em todos os ambientes', 'Pontos de rede no teto para os access points. Assim o sinal chega com estabilidade na casa toda.'),
    ('switch', 'Automação e iluminação', 'Caixas mais fundas e fio neutro nos interruptores facilitam automatizar luzes, cortinas e cenas.'),
    ('rack', 'Um lugar para a central', 'Reserve um espaço ventilado para rack, roteador e amplificadores, com tomadas e pontos de rede.'),
]
def tip(k):
    kind, title, body = TIPS[k]
    im = bg(W, H); d = ImageDraw.Draw(im)
    big = F(FB, 300); num = f'0{k + 1}'
    d.text((60, 30), num, font=big, fill=(26, 52, 43))
    ic = icon(kind, 360); im.paste(ic, (W - 440, 140), ic)
    tag(d, 80, 640, 'ANTES DO GESSO')
    y = text_block(d, 80, 700, title, F(FB, 70), CREAM, 920, 84)
    d.line([(80, y + 30), (200, y + 30)], fill=LINE, width=3)
    text_block(d, 80, y + 70, body, F(FR, 40), SUB, 900, 58)
    d.text((80, H - 80), 'MOVE · Som, Automação e Segurança', font=F(FM, 24), fill=(90, 115, 104))
    d.text((W - 140, H - 80), f'{k + 2}/7', font=F(FM, 26), fill=SUB)
    return im

def cta():
    im = bg(W, H); d = ImageDraw.Draw(im)
    lh = logo(im, W / 2, 200, 640)
    y = 200 + lh + 150
    for ln in ['Está construindo', 'ou reformando?']:
        f = F(FB, 72); tw = d.textlength(ln, font=f); d.text(((W - tw) / 2, y), ln, font=f, fill=CREAM); y += 86
    y += 30
    for ln in wrap(d, 'Envie a planta do seu projeto e a MOVE planeja o som, a automação e a rede com você.', F(FR, 38), 820):
        f = F(FR, 38); tw = d.textlength(ln, font=f); d.text(((W - tw) / 2, y), ln, font=f, fill=SUB); y += 56
    y += 60
    bw, bh = 640, 110
    d.rounded_rectangle([(W - bw) / 2, y, (W + bw) / 2, y + bh], 55, fill=MINT)
    f = F(FB, 34); t = 'SOLICITE SEU ORÇAMENTO'; tw = sum(d.textlength(c, font=f) + 3 for c in t)
    tracked(d, ((W - tw) / 2, y + 34), t, f, BG, 3)
    handle(d, W, y + bh + 60)
    d.text((W - 140, H - 80), '7/7', font=F(FM, 26), fill=SUB)
    return im

# ---------------- FEED (single) ----------------
def feed():
    im = bg(W, H); d = ImageDraw.Draw(im)
    # house illustration with lights
    hx, hy, hw = W / 2, 330, 520
    glow = Image.new('L', (W, H), 0); gd = ImageDraw.Draw(glow)
    gd.ellipse([hx - 380, hy - 200, hx + 380, hy + 420], fill=150)
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    im = Image.composite(Image.new('RGB', (W, H), (52, 52, 30)), im, glow); d = ImageDraw.Draw(im)
    roof = [(hx - hw / 2 - 40, hy + 40), (hx, hy - 170), (hx + hw / 2 + 40, hy + 40)]
    d.line(roof, fill=MINT, width=12, joint='curve')
    d.rectangle([hx - hw / 2, hy + 40, hx + hw / 2, hy + 400], outline=MINT, width=12)
    for wx in [hx - 150, hx + 150]:
        d.rectangle([wx - 70, hy + 110, wx + 70, hy + 230], fill=(250, 214, 140), outline=MINT, width=8)
    d.rounded_rectangle([hx - 55, hy + 260, hx + 55, hy + 400], 8, outline=MINT, width=10)
    for k in range(5):
        a = math.radians(200 + k * 35)
        d.line([(hx + 200 * math.cos(a) * 0 + hx * 0, 0)] * 0 or [(hx + 230 * math.cos(a), hy - 40 + 230 * math.sin(a)), (hx + 280 * math.cos(a), hy - 40 + 280 * math.sin(a))], fill=MINT + (0,), width=0) if False else None
    # music notes
    def note(x, y, s, col):
        d.ellipse([x, y, x + s * 1.3, y + s], fill=col)
        d.line([(x + s * 1.25, y + s * 0.5), (x + s * 1.25, y - s * 2.2)], fill=col, width=max(4, int(s / 5)))
        d.line([(x + s * 1.25, y - s * 2.2), (x + s * 2.1, y - s * 1.5)], fill=col, width=max(4, int(s / 5)))
    note(hx + hw / 2 + 50, hy + 120, 34, MINT); note(hx + hw / 2 + 110, hy + 30, 26, (120, 200, 170))
    note(hx - hw / 2 - 120, hy + 90, 28, (120, 200, 170))
    # scene pill
    py = hy + 460; pw, ph = 470, 104
    d.rounded_rectangle([hx - pw / 2, py, hx + pw / 2, py + ph], 52, fill=MINT)
    f = F(FB, 36); t = 'CENA  ·  CHEGUEI'; tw = sum(d.textlength(c, font=f) + 3 for c in t)
    tracked(d, (hx - tw / 2, py + 30), t, f, BG, 3)
    tag(d, 80, 960, 'AUTOMAÇÃO RESIDENCIAL')
    y = text_block(d, 80, 1010, 'Um toque. A casa te recebe.', F(FB, 64), CREAM, 920, 76)
    text_block(d, 80, y + 18, 'Luzes, som ambiente e clima no ponto com uma cena feita para a sua rotina.', F(FR, 36), SUB, 920, 50)
    logo(im, W - 170, H - 95, 200)
    return im

# ---------------- STORIES 1080x1920 ----------------
SW, SH = 1080, 1920
def story_frame(img, top_text, bottom_text):
    im = bg(SW, SH); d = ImageDraw.Draw(im)
    logo(im, SW / 2, 120, 300)
    tag(d, 120, 330, top_text)
    w = 840; h = round(img.height * w / img.width)
    card = img.resize((w, h), Image.LANCZOS)
    x, y = (SW - w) // 2, 400
    sh = Image.new('L', (SW, SH), 0); ImageDraw.Draw(sh).rounded_rectangle([x, y + 20, x + w, y + h + 30], 30, fill=200)
    sh = sh.filter(ImageFilter.GaussianBlur(30)); im = Image.composite(Image.new('RGB', (SW, SH), (3, 8, 6)), im, sh)
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w, h], 30, fill=255)
    im.paste(card, (x, y), m); d = ImageDraw.Draw(im)
    by = y + h + 90; bw, bh = 640, 110
    d.rounded_rectangle([(SW - bw) / 2, by, (SW + bw) / 2, by + bh], 55, fill=MINT)
    f = F(FB, 34); tw = sum(d.textlength(c, font=f) + 3 for c in bottom_text)
    tracked(d, ((SW - tw) / 2, by + 34), bottom_text, f, BG, 3)
    handle(d, SW, by + bh + 50)
    return im

def story_bastidores():
    im = photo_bg(P + 'fr_B_13.5.jpg', SW, SH, dark=0.9); d = ImageDraw.Draw(im)
    logo(im, SW / 2, 120, 300)
    tag(d, 90, 1360, 'BASTIDORES DA OBRA')
    y = text_block(d, 90, 1420, 'Cabeamento passado antes do forro.', F(FB, 72), CREAM, 900, 86)
    text_block(d, 90, y + 20, 'Som, rede e automação já planejados em cada ambiente.', F(FR, 38), SUB, 900, 54)
    return im

def story_cta():
    im = bg(SW, SH); d = ImageDraw.Draw(im)
    logo(im, SW / 2, 380, 720)
    y = 900
    for ln in ['Vai construir', 'ou reformar?']:
        f = F(FB, 84); tw = d.textlength(ln, font=f); d.text(((SW - tw) / 2, y), ln, font=f, fill=CREAM); y += 100
    y += 30
    for ln in wrap(d, 'Me chama no direct e envie a planta ou fotos do ambiente.', F(FR, 42), 800):
        f = F(FR, 42); tw = d.textlength(ln, font=f); d.text(((SW - tw) / 2, y), ln, font=f, fill=SUB); y += 60
    y += 70; bw, bh = 640, 116
    d.rounded_rectangle([(SW - bw) / 2, y, (SW + bw) / 2, y + bh], 58, fill=MINT)
    f = F(FB, 36); t = 'SOLICITE SEU ORÇAMENTO'; tw = sum(d.textlength(c, font=f) + 3 for c in t)
    tracked(d, ((SW - tw) / 2, y + 36), t, f, BG, 3)
    handle(d, SW, y + bh + 60)
    return im

if __name__ == '__main__':
    car = [cover()] + [tip(k) for k in range(5)] + [cta()]
    for i, im in enumerate(car):
        im.save(f'{P}carrossel_{i + 1}.jpg', quality=92)
    fd = feed(); fd.save(f'{P}feed_cena_cheguei.jpg', quality=92)
    story_frame(car[0], 'NOVO POST NO FEED', 'VEJA O CARROSSEL').save(f'{P}story_2_carrossel.jpg', quality=92)
    story_frame(fd, 'NOVO POST NO FEED', 'VEJA NO PERFIL').save(f'{P}story_3_feed.jpg', quality=92)
    story_bastidores().save(f'{P}story_4_bastidores.jpg', quality=92)
    story_cta().save(f'{P}story_5_orcamento.jpg', quality=92)
