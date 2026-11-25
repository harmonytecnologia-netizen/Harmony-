"""Produz a fila da Metalize (@metalize.metalurgica): fila/AAAA-MM-DD/plano.json + artes.
uso: python3 metalize/scripts/produzir.py [--dias 4] [--data AAAA-MM-DD] [--forcar]
Frequência (pedido do João, 24/11/2026):
  09h: 3 stories | 15h: 3 stories | 20h: 1 story (convite/pergunta)
  Seg: Reel "Metalize Explica 3D" (se houver pronto em metalize/reels/prontos, senão feed)
  Qua: carrossel | Sex: feed — sempre às 20h, com o story do post.
Não publica: quem publica são as tarefas agendadas.
"""
import json, os, sys, datetime, random, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(RAIZ)
F = os.path.join(REPO, 'kit_instagram', 'fontes')
RAW = 'https://raw.githubusercontent.com/harmonytecnologia-netizen/Harmony-/metalize/metalize/fila/{d}/{a}'
OURO = (251, 207, 14); CREME = (243, 240, 234); CINZA = (167, 162, 154); FUNDO = (11, 12, 13)  # amarelo da logomarca
KICK = {'curiosidade': 'VOCÊ SABIA?', 'aprendiz': 'DICA DE OFICINA', 'detalhe': 'DETALHE DE ALTO PADRÃO', 'pergunta': 'QUAL É A SUA?', 'cta': 'METALIZE METALÚRGICA'}
HANDLE = '@metalize.metalurgica'

def fn(nome, t): return ImageFont.truetype(os.path.join(F, nome), t)
SERIF = lambda t: fn('Inter-Bold.otf', int(t * 0.86))  # títulos em sans forte, como o logo
LEVE = lambda t: fn('Inter-Light.otf', t)
MED = lambda t: fn('Inter-Medium.otf', t)
LOGO = Image.open(os.path.join(RAIZ, 'logo.png')).convert('RGBA'); LOGO = LOGO.crop(LOGO.getbbox())

def fundo(nome, w, h, var=0):
    p = os.path.join(RAIZ, 'fundos', f'3d_{nome}.jpg')
    if not os.path.exists(p):
        p = os.path.join(RAIZ, 'fundos', '3d_chapa.jpg')
    im = Image.open(p).convert('RGB')
    if var % 2: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    r = max(w / im.width, h / im.height) * (1 + 0.08 * (var % 3))
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = (im.width - w) // 2; y = (im.height - h) // 2
    im = im.crop((x, y, x + w, y + h))
    im = ImageEnhance.Contrast(im).enhance(1.05); im = ImageEnhance.Color(im).enhance(0.9)
    return im

def sombra(im, inicio=0.35, forca=0.96, topo=0.45):
    w, h = im.size; g = Image.new('L', (1, h))
    for y in range(h):
        t = y / h
        a = topo * max(0, 1 - t / 0.2) + forca * max(0, (t - inicio) / (1 - inicio)) ** 1.3
        g.putpixel((0, y), int(255 * min(1, a)))
    return Image.composite(Image.new('RGB', (w, h), FUNDO), im, g.resize((w, h)))

def espac(d, x, y, s, f, cor, esp, centro=None):
    tw = sum(d.textlength(c, font=f) + esp for c in s) - esp
    if centro: x = (centro - tw) / 2
    for c in s: d.text((x, y), c, font=f, fill=cor); x += d.textlength(c, font=f) + esp
    return tw

def quebra(d, s, f, larg):
    linhas, l = [], ''
    for p in [w for w in s.replace('(66) ', '(66)\u00a0').split(' ') if w]:
        t = (l + ' ' + p).strip()
        if d.textlength(t, font=f) <= larg: l = t
        else: linhas.append(l); l = p
    if l: linhas.append(l)
    return linhas

def logo(im, larg, y):
    l = LOGO.resize((larg, round(LOGO.height * larg / LOGO.width)), Image.LANCZOS)
    im.paste(l, ((im.width - larg) // 2, y), l)

def ilustrativa(d, w):
    f = LEVE(22); s = 'Imagem ilustrativa.'; d.text((w - 36 - d.textlength(s, font=f), 36), s, font=f, fill=(215, 212, 205))

def bloco_texto(im, kicker, titulo, texto, base_y, tam_t=92, larg=900):
    d = ImageDraw.Draw(im); w = im.width; x = (w - larg) // 2
    ft = SERIF(tam_t); fb = LEVE(40 if im.height > 1500 else 36)
    tl = titulo.split('|'); bl = quebra(d, texto, fb, larg) if texto else []
    altura = 60 + len(tl) * (tam_t + 14) + 64 + len(bl) * (fb.size + 16)
    y = base_y - altura
    espac(d, x, y, kicker, MED(26), OURO, 7); y += 60
    for ln in tl: d.text((x, y), ln, font=ft, fill=CREME); y += tam_t + 14
    d.line([(x, y + 34), (x + 90, y + 34)], fill=OURO, width=3); y += 64
    for ln in bl: d.text((x, y), ln, font=fb, fill=(222, 218, 210)); y += fb.size + 16
    return d

def story(item, out, var=0):
    W, H = 1080, 1920
    im = sombra(fundo(item['fundo'], W, H, var))
    logo(im, 230, 90)
    d = bloco_texto(im, KICK.get(item['tipo'], 'METALIZE'), item['titulo'], item['texto'], H - 250)
    espac(d, 0, H - 150, HANDLE, LEVE(26), CINZA, 6, W); ilustrativa(d, W)
    im.save(out, quality=93)

def feed(item, out, var=0):
    W, H = 1080, 1350
    im = sombra(fundo(item['fundo'], W, H, var), inicio=0.4)
    logo(im, 190, 56)
    d = bloco_texto(im, item['kicker'], item['titulo'], item['texto'], H - 120, tam_t=84)
    ilustrativa(d, W); im.save(out, quality=93)

def carrossel(item, pasta, pref):
    W, H = 1080, 1350; arqs = []
    im = sombra(fundo(item['fundo'], W, H), inicio=0.38); logo(im, 190, 56)
    d = bloco_texto(im, 'GUIA METALIZE', item['capa'], 'Arraste para o lado →', H - 120, tam_t=96); ilustrativa(d, W)
    p = f'{pref}_1.jpg'; im.save(os.path.join(pasta, p), quality=93); arqs.append(p)
    base = fundo('chapa', W, H).filter(ImageFilter.GaussianBlur(18)); base = Image.blend(base, Image.new('RGB', (W, H), FUNDO), 0.78)
    for i, (t, txt) in enumerate(item['slides'], 2):
        im = base.copy(); d = ImageDraw.Draw(im)
        d.text((90, 150), f'{i - 1:02d}', font=SERIF(170), fill=OURO)
        y = 480
        for ln in quebra(d, t, SERIF(78), 900): d.text((90, y), ln, font=SERIF(78), fill=CREME); y += 92
        d.line([(90, y + 20), (180, y + 20)], fill=OURO, width=3); y += 70
        for ln in quebra(d, txt, LEVE(42), 900): d.text((90, y), ln, font=LEVE(42), fill=(222, 218, 210)); y += 60
        espac(d, 0, H - 100, HANDLE, LEVE(24), CINZA, 6, W)
        p = f'{pref}_{i}.jpg'; im.save(os.path.join(pasta, p), quality=93); arqs.append(p)
    im = base.copy(); d = ImageDraw.Draw(im); logo(im, 420, 300)
    for k, (s, f, c) in enumerate((('Projetos em metal sob medida.', SERIF(58), CREME), ('Orçamento pelo direct', LEVE(38), (222, 218, 210)), ('WhatsApp (66) 99632-0774', MED(36), OURO))):
        d.text(((W - d.textlength(s, font=f)) / 2, 760 + k * 90), s, font=f, fill=c)
    p = f'{pref}_{len(arqs) + 1}.jpg'; im.save(os.path.join(pasta, p), quality=93); arqs.append(p)
    return arqs

def story_do_post(img_path, out, rotulo='NOVO POST NO FEED'):
    W, H = 1080, 1920; post = Image.open(img_path).convert('RGB')
    bg = post.resize((W, round(post.height * W / post.width))).filter(ImageFilter.GaussianBlur(30))
    bg = Image.blend(bg.resize((W, H)), Image.new('RGB', (W, H), FUNDO), 0.6)
    p = post.resize((880, round(post.height * 880 / post.width)), Image.LANCZOS); y = (H - p.height) // 2 + 40
    bg.paste(p, ((W - 880) // 2, y)); d = ImageDraw.Draw(bg)
    espac(d, 0, y - 90, rotulo, MED(30), OURO, 8, W); logo(bg, 200, 90)
    espac(d, 0, y + p.height + 60, 'toque para ver', LEVE(28), CINZA, 5, W)
    bg.save(out, quality=93)

def main():
    a = sys.argv[1:]
    dias = int(a[a.index('--dias') + 1]) if '--dias' in a else 4
    hoje = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))).date()
    inicio = datetime.date.fromisoformat(a[a.index('--data') + 1]) if '--data' in a else hoje
    forcar = '--forcar' in a
    banco = json.load(open(os.path.join(RAIZ, 'banco', 'pautas.json'), encoding='utf-8'))
    pu = os.path.join(RAIZ, 'banco', 'usados.json')
    usados = json.load(open(pu)) if os.path.exists(pu) else {'stories': [], 'carrosseis': [], 'feeds': [], 'reels': [], 'voltas': 0}

    def pega(lista, chave, filtro=lambda x: True):
        cand = [x for x in banco[lista] if filtro(x) and x['id'] not in usados[chave]]
        if not cand:  # banco esgotado: recomeça a volta para esse grupo
            ids = {x['id'] for x in banco[lista] if filtro(x)}
            usados[chave] = [i for i in usados[chave] if i not in ids]; usados['voltas'] += 1
            cand = [x for x in banco[lista] if filtro(x)]
        x = cand[0]; usados[chave].append(x['id']); return x

    feitos = []
    for k in range(dias):
        dia = inicio + datetime.timedelta(days=k); ds = dia.isoformat()
        pasta = os.path.join(RAIZ, 'fila', ds); pp = os.path.join(pasta, 'plano.json')
        if os.path.exists(pp) and not forcar: continue
        os.makedirs(pasta, exist_ok=True); url = lambda f: RAW.format(d=ds, a=f)
        var = dia.toordinal()
        plano = {'data': ds, 'conta': '17841449079341071', '09h': [], '15h': [], '20h': []}
        grade = {'09h': ['curiosidade', 'aprendiz', 'detalhe'], '15h': ['curiosidade', 'aprendiz', 'pergunta'], '20h': ['cta']}
        for hora, tipos in grade.items():
            for n, tipo in enumerate(tipos, 1):
                it = pega('stories', 'stories', lambda x, t=tipo: x['tipo'] == t)
                f = f'story_{hora}_{n}.jpg'; story(it, os.path.join(pasta, f), var + n)
                plano[hora].append({'acao': 'create_story', 'arquivo': url(f), 'pauta': it['id'] + ' ' + it['titulo'].replace('|', ' ')})
        wd = dia.weekday(); post = []
        reel = None
        if wd == 0:
            rp = os.path.join(RAIZ, 'reels', 'prontos')
            for j in sorted(os.listdir(rp)) if os.path.isdir(rp) else []:
                if j.endswith('.json') and j not in usados['reels']:
                    reel = json.load(open(os.path.join(rp, j), encoding='utf-8')); usados['reels'].append(j); break
        if reel:
            post.append({'acao': 'create_video_post', 'arquivo': reel['video_url'], 'legenda': reel['legenda'], 'thumb_offset': reel.get('thumb_offset', 2000), 'pauta': 'Reel ' + reel.get('tema', '')})
            post.append({'acao': 'create_story', 'arquivo': reel['video_url'], 'pauta': 'story do Reel'})
        elif wd == 2:
            it = pega('carrosseis', 'carrosseis'); arqs = carrossel(it, pasta, 'carrossel')
            post.append({'acao': 'create_carousel_post', 'arquivos': [url(x) for x in arqs], 'legenda': it['legenda'], 'pauta': it['id'] + ' ' + it['capa'].replace('|', ' ')})
            story_do_post(os.path.join(pasta, arqs[0]), os.path.join(pasta, 'story_post.jpg'), 'NOVO CARROSSEL NO FEED')
            post.append({'acao': 'create_story', 'arquivo': url('story_post.jpg'), 'pauta': 'story do carrossel'})
        elif wd in (0, 4):
            it = pega('feeds', 'feeds'); feed(it, os.path.join(pasta, 'feed.jpg'), var)
            post.append({'acao': 'create_image_post', 'arquivo': url('feed.jpg'), 'legenda': it['legenda'], 'pauta': it['id'] + ' ' + it['titulo'].replace('|', ' ')})
            story_do_post(os.path.join(pasta, 'feed.jpg'), os.path.join(pasta, 'story_post.jpg'))
            post.append({'acao': 'create_story', 'arquivo': url('story_post.jpg'), 'pauta': 'story do feed'})
        plano['20h'] = post + plano['20h']
        json.dump(plano, open(pp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        feitos.append(ds)
    json.dump(usados, open(pu, 'w'), indent=1)
    print('dias produzidos:', feitos or 'nenhum (fila já completa)')
    sobra = {t: sum(1 for x in banco['stories'] if x['tipo'] == t and x['id'] not in usados['stories']) for t in KICK}
    print('stories ainda não usados por tipo:', sobra)

if __name__ == '__main__':
    main()
