"""Reel a partir de FOTOS (reais ou geradas no ChatGPT): movimento de camera lento (Ken Burns),
legendas elegantes, tela final com logo, cortes no ritmo da musica.
uso: python3 reel_imagens.py config.json saida.mp4
config: {"musica": "faixa.mp3", "musica_inicio": 0, "duracao_cena": 4.0,
         "cenas": [{"img": "foto1.jpg", "chamada": "01 · TITULO PEQUENO", "titulo": "Linha 1|Linha 2", "zoom": "in"}],
         "frase_final": "...", "sub_final": "..."}
"""
import json, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from marca import carregar, fonte, titulo_fonte, espacado, W, H

FPS, T = 30, 0.6

def prep(src, out):
    im = Image.open(src).convert('RGB')
    r = max(W * 1.18 / im.width, H * 1.18 / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.05); im = ImageEnhance.Color(im).enhance(0.95)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=55, threshold=2))
    x = (im.width - round(W * 1.18)) // 2; y = (im.height - round(H * 1.18)) // 2
    im.crop((x, y, x + round(W * 1.18), y + round(H * 1.18))).save(out, quality=95)

def legenda(m, chamada, titulo, out):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g = Image.new('L', (1, H))
    for y in range(H):
        t = y / H; a = 0.55 * max(0, 1 - t / 0.16) + 0.92 * max(0, (t - 0.52) / 0.48) ** 1.5
        g.putpixel((0, y), int(255 * min(1, a)))
    sh = Image.new('RGBA', (W, H), m['cor_fundo'] + (255,)); sh.putalpha(g.resize((W, H))); im.alpha_composite(sh)
    if m['logo_img'] is not None:
        L = m['logo_img']; l = L.resize((170, round(L.height * 170 / L.width)), Image.LANCZOS); im.alpha_composite(l, ((W - 170) // 2, 110))
    d = ImageDraw.Draw(im)
    linhas = titulo.split('|'); y = 1440 - 100 * (len(linhas) - 1)
    espacado(d, 90, y - 70, chamada, fonte('media', 28), m['cor_destaque'] + (255,), 8)
    f = titulo_fonte(m, 84)
    for ln in linhas:
        d.text((86, y), ln, font=f, fill=m['cor_texto'] + (255,)); y += 100
    espacado(d, 0, H - 150, m['handle'], fonte('leve', 24), m['cor_secundaria'] + (255,), 7, True)
    im.save(out)

def tela_final(m, titulo, sub, out):
    im = Image.new('RGB', (W, H), m['cor_fundo'])
    glow = Image.new('L', (W, H), 0); ImageDraw.Draw(glow).ellipse([-200, 300, W + 200, 1500], fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(220))
    c = tuple(min(255, int(v * 0.5 + 20)) for v in m['cor_destaque'])
    im = Image.composite(Image.new('RGB', (W, H), c), im, glow)
    if m['logo_img'] is not None:
        L = m['logo_img']; l = L.resize((560, round(L.height * 560 / L.width)), Image.LANCZOS); im.paste(l, ((W - 560) // 2, 620), l)
    else:
        d = ImageDraw.Draw(im); f = titulo_fonte(m, 110); tw = d.textlength(m['nome'], font=f); d.text(((W - tw) / 2, 700), m['nome'], font=f, fill=m['cor_texto'])
    d = ImageDraw.Draw(im)
    f = titulo_fonte(m, 72); tw = d.textlength(titulo, font=f); d.text(((W - tw) / 2, 1000), titulo, font=f, fill=m['cor_texto'])
    f2 = fonte('leve', 32); tw = d.textlength(sub, font=f2); d.text(((W - tw) / 2, 1110), sub, font=f2, fill=m['cor_secundaria'])
    espacado(d, 0, 1240, m['handle'], fonte('leve', 30), m['cor_destaque'], 8, True)
    im.save(out, quality=95)

def batidas(musica, ini, dur):
    try:
        import librosa
        y, sr = librosa.load(musica, sr=22050, offset=ini, duration=dur)
        _, b = librosa.beat.beat_track(y=y, sr=sr)
        return librosa.frames_to_time(b, sr=sr).tolist()
    except Exception as e:
        print('sem librosa/batidas, usando tempo fixo:', e, file=sys.stderr); return []

def main(cfg_path, out):
    m = carregar(); cfg = json.load(open(cfg_path, encoding='utf-8'))
    base = os.path.dirname(os.path.abspath(cfg_path)); P = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    wd = os.path.join(os.path.dirname(os.path.abspath(out)), '_tmp_reel/'); os.makedirs(wd, exist_ok=True)
    cenas = cfg['cenas']; n = len(cenas); dc = cfg.get('duracao_cena', 4.0)
    bt = batidas(P(cfg['musica']), cfg.get('musica_inicio', 0), 60)
    cortes, t = [], cfg.get('duracao_primeira', 3.4)
    for k in range(n):
        cortes.append(min(bt, key=lambda b: abs(b - t)) if bt else t); t = cortes[-1] + dc
    FIM = 3.8; total = cortes[-1] - T / 2 + FIM
    lens = [cortes[0] + T / 2] + [cortes[i + 1] - cortes[i] + T for i in range(n - 1)] + [FIM]
    inputs, fc, idx = [], [], 0
    for k, sc in enumerate(cenas):
        L = lens[k]; nf = int(L * FPS) + 2
        prep(P(sc['img']), f'{wd}img{k}.jpg'); legenda(m, sc.get('chamada', ''), sc.get('titulo', ''), f'{wd}cap{k}.png')
        inputs += ['-loop', '1', '-framerate', '30', '-t', f'{L:.3f}', '-i', f'{wd}img{k}.jpg']; ii = idx; idx += 1
        inputs += ['-loop', '1', '-framerate', '30', '-t', f'{L:.3f}', '-i', f'{wd}cap{k}.png']; ci = idx; idx += 1
        z = "1.0+0.0009*on" if sc.get('zoom', 'in') == 'in' else f"{1.0 + 0.0009 * nf:.4f}-0.0009*on"
        fc.append(f"[{ii}:v]scale={W*4}:-1:flags=lanczos,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W*2}x{H*2}:fps=30,"
                  f"scale={W}:{H}:flags=lanczos,trim=0:{L:.3f},setpts=PTS-STARTPTS,format=yuv420p[b{k}]")
        t0 = 0.05 if k == 0 else T / 2 + 0.25; t1 = L - T / 2 - 0.35
        fc.append(f"[{ci}:v]format=rgba,fade=t=in:st={t0:.2f}:d={0.25 if k == 0 else 0.6}:alpha=1,fade=t=out:st={t1:.2f}:d=0.3:alpha=1[c{k}]")
        fc.append(f"[b{k}][c{k}]overlay=0:0:shortest=1,format=yuv420p,settb=1/30[s{k}]")
    tela_final(m, cfg.get('frase_final', m['frase_final']), cfg.get('sub_final', m['sub_final']), f'{wd}fim.jpg')
    inputs += ['-loop', '1', '-framerate', '30', '-t', f'{FIM}', '-i', f'{wd}fim.jpg']
    fc.append(f"[{idx}:v]scale={W}:{H},trim=0:{FIM},setpts=PTS-STARTPTS,format=yuv420p,settb=1/30[s{n}]"); idx += 1
    trans = ['fade', 'smoothup', 'fade', 'smoothleft', 'fade', 'fadeblack']
    prev = 's0'
    for j, c in enumerate(cortes):
        tr = 'fadeblack' if j == len(cortes) - 1 else trans[j % len(trans)]
        fc.append(f"[{prev}][s{j + 1}]xfade=transition={tr}:duration={T}:offset={c - T / 2:.3f}[x{j}]"); prev = f'x{j}'
    inputs += ['-ss', f"{cfg.get('musica_inicio', 0)}", '-i', P(cfg['musica'])]
    fc.append(f"[{idx}:a]atrim=0:{total:.3f},afade=t=in:st=0:d=0.6,afade=t=out:st={total - 2.6:.3f}:d=2.6,loudnorm=I=-14:TP=-1.5[a]")
    tmp = out[:-4] + '.tmp.mp4'
    cmd = ['ffmpeg', '-y', '-loglevel', 'error'] + inputs + ['-filter_complex', ';'.join(fc), '-map', f'[{prev}]', '-map', '[a]',
           '-r', '30', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
           '-ar', '48000', '-movflags', '+faststart', '-t', f'{total:.3f}', tmp]
    r = subprocess.call(cmd)
    if r == 0: os.replace(tmp, out); print(f'ok {out} ({total:.1f}s)')
    sys.exit(r)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
