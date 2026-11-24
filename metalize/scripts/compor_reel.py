"""Monta Reel no estilo "explicativo escuro" da Metalize (referência pedida pelo João em 24/11/2026):
cabeçalho mono espaçado no topo ("METALIZE EXPLICA · TEMA"), pílula "● TEXTO" por trecho,
etiqueta mono no meio da tela, legenda karaokê (palavra falada acende, resto cinza) numa caixa escura,
grade escura com vinheta, cartão final com logo. Voz + música com ducking.
uso: python3 compor_reel.py roteiro.json saida.mp4
roteiro.json: {"quadros": "seq/%04d.jpg", "fps": 24, "duracao": 29.6, "tema": "CALHAS",
  "falas": [{"arquivo": "voz/f1.wav", "t": 0.3, "texto": "..."}],
  "pilulas": [{"de": 0, "ate": 3, "texto": "COMO FUNCIONA", "cor": "amarelo|vermelho|verde"}],
  "etiquetas": [{"de": 0, "ate": 3, "texto": "CALHA", "y": 1180}],
  "fim": {"de": 26.0, "img": "fim.png"}, "musica": "...mp3", "musica_vol": 0.3}
"""
import json, os, sys, subprocess, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.join(os.path.dirname(RAIZ), 'kit_instagram', 'fontes')
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
W, H = 1080, 1920
AMARELO = (251, 207, 14); VERM = (229, 83, 75); VERDE = (88, 214, 141); BRANCO = (245, 244, 240); CINZA = (128, 132, 138)
COR = {'amarelo': AMARELO, 'vermelho': VERM, 'verde': VERDE}
fm = lambda t: ImageFont.truetype(MONO, t)
fb = lambda t: ImageFont.truetype(os.path.join(K, 'Inter-Bold.otf'), t)

def espac(d, x, y, s, f, cor, esp):
    for c in s:
        d.text((x, y), c, font=f, fill=cor); x += d.textlength(c, font=f) + esp
    return x

def vinheta():
    v = Image.new('L', (W, H), 0); d = ImageDraw.Draw(v)
    d.ellipse([-W * 0.25, -H * 0.12, W * 1.25, H * 1.12], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(160))
    out = Image.composite(Image.new('RGBA', (W, H), (0, 0, 0, 0)), Image.new('RGBA', (W, H), (4, 6, 10, 170)), v)
    g = Image.new('L', (1, H))  # topo escuro para o cabeçalho
    for y in range(H): g.putpixel((0, y), int(200 * max(0, 1 - y / 420) ** 1.5))
    topo = Image.new('RGBA', (W, H), (6, 8, 12, 255)); topo.putalpha(g.resize((W, H))); out.alpha_composite(topo)
    return out

def palavras_tempo(falas):
    """tempo de cada palavra proporcional ao nº de letras dentro da duração real do áudio."""
    out = []
    for f in falas:
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f['arquivo']], capture_output=True, text=True).stdout)
        ws = f['texto'].split(); peso = [len(w) + 2 for w in ws]; tot = sum(peso); t = f['t'] + 0.12; util = dur - 0.25
        linha = []; linhas = []
        for w in ws:  # quebra em blocos de até ~24 caracteres
            if linha and len(' '.join(linha + [w])) > 24: linhas.append(linha); linha = []
            linha.append(w)
        if linha: linhas.append(linha)
        k = 0
        for ln in linhas:
            bloco = []
            for w in ln:
                bloco.append((w, t)); t += util * peso[k] / tot; k += 1
            out.append((bloco, bloco[0][1], t))
    for i in range(len(out)):  # bloco fica na tela até o próximo começar (máx +0.6 s)
        b, a, z = out[i]
        prox = out[i + 1][1] if i + 1 < len(out) else z + 0.6
        out[i] = (b, a, min(prox, z + 0.6))
    return out

def legenda(d, im, bloco, t):
    f = fb(62); txt = ' '.join(w for w, _ in bloco)
    tw = d.textlength(txt, font=f); x0 = (W - tw) / 2; y0 = 1330
    caixa = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dc = ImageDraw.Draw(caixa)
    dc.rounded_rectangle([x0 - 34, y0 - 22, x0 + tw + 34, y0 + 92], 22, fill=(14, 16, 20, 205))
    im.alpha_composite(caixa); d = ImageDraw.Draw(im)
    x = x0
    for w, tw0 in bloco:
        cor = BRANCO if t >= tw0 else CINZA
        d.text((x, y0), w, font=f, fill=cor); x += d.textlength(w + ' ', font=f)

def main(cfg_path, out):
    cfg = json.load(open(cfg_path, encoding='utf-8')); base = os.path.dirname(os.path.abspath(cfg_path))
    P = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    for f in cfg['falas']: f['arquivo'] = P(f['arquivo'])
    fps = cfg.get('fps', 24); D = cfg['duracao']; N = int(D * fps)
    quadros = sorted(glob.glob(P(cfg['quadros']).replace('%04d', '*')))
    blocos = palavras_tempo(cfg['falas']); vin = vinheta()
    fim = Image.open(P(cfg['fim']['img'])).convert('RGBA') if cfg.get('fim') else None
    tmp = os.path.join(os.path.dirname(os.path.abspath(out)), '_compor'); os.makedirs(tmp, exist_ok=True)
    cab = f"METALIZE EXPLICA · {cfg.get('tema', '')}"
    for n in range(N):
        t = n / fps
        q = quadros[min(n, len(quadros) - 1)]
        im = Image.open(q).convert('RGB').resize((W, H), Image.LANCZOS)
        im = ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(0.78)).enhance(1.12).convert('RGBA')
        im.alpha_composite(vin); d = ImageDraw.Draw(im)
        if fim and t >= cfg['fim']['de']:
            a = min(1, (t - cfg['fim']['de']) / 0.35); fx = fim.copy(); fx.putalpha(fim.getchannel('A').point(lambda v: int(v * a))); im.alpha_composite(fx)
        else:
            espac(d, 40, 150, cab, fm(30), (200, 204, 210), 7)
            for p in cfg.get('pilulas', []):
                if p['de'] <= t < p['ate']:
                    f = fm(38); tw = sum(d.textlength(c, font=f) + 6 for c in p['texto'])
                    d.rounded_rectangle([28, 205, 28 + 110 + tw, 285], 40, fill=(18, 20, 24, 225), outline=(60, 64, 70, 255), width=2)
                    d.ellipse([52, 228, 86, 262], fill=BRANCO); d.ellipse([100, 240, 110, 250], fill=COR.get(p.get('cor', 'amarelo')))
                    espac(d, 126, 222, p['texto'], f, BRANCO, 6)
            for e in cfg.get('etiquetas', []):
                if e['de'] <= t < e['ate']:
                    f = fm(36); tw = sum(d.textlength(c, font=f) + 6 for c in e['texto']); x = (W - tw) / 2; y = e.get('y', 1150)
                    cor = COR.get(e.get('cor', ''), (70, 74, 80))
                    d.rounded_rectangle([x - 30, y - 16, x + tw + 24, y + 60], 14, fill=(14, 16, 20, 230), outline=cor + (255,), width=3)
                    espac(d, x, y, e['texto'], f, BRANCO, 6)
            for bloco, a, z in blocos:
                if a <= t < z: legenda(d, im, bloco, t); break
        im.convert('RGB').save(os.path.join(tmp, f'{n:04d}.jpg'), quality=92)
    video = os.path.join(tmp, 'v.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', os.path.join(tmp, '%04d.jpg'), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '30', video], check=True)
    ins = ['-i', video]; fc = []
    for i, f in enumerate(cfg['falas']):
        ins += ['-i', f['arquivo']]; ms = int(f['t'] * 1000); fc.append(f"[{i + 1}:a]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay={ms}|{ms}[f{i}]")
    nf = len(cfg['falas'])
    fc.append(''.join(f'[f{i}]' for i in range(nf)) + f"amix=inputs={nf}:normalize=0,highpass=f=80,acompressor=threshold=-18dB:ratio=3,loudnorm=I=-16:TP=-1.5,apad,asplit[vo][sc]")
    mix = '[vo]'
    if cfg.get('musica'):
        ins += ['-i', P(cfg['musica'])]; k = nf + 1
        fc.append(f"[{k}:a]atrim=0:{D},volume={cfg.get('musica_vol', 0.3)},afade=t=in:d=0.6,afade=t=out:st={D - 1.6}:d=1.6[mu]")
        fc.append("[mu][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[md]"); mix += '[md]'
        fc.append(f"{mix}amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]")
    else:
        fc.append("[vo]anull[a]")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + ins + ['-filter_complex', ';'.join(fc), '-map', '0:v', '-map', '[a]', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '192k', '-t', str(D), '-movflags', '+faststart', out], check=True)
    print('ok', out, D)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
