"""Monta o video final da serie "<Marca> Explica" (animacao 2D ou 3D):
imagem (quadros ou video) + cartoes de texto por tempo + narracao + efeitos + musica abaixando sob a voz.
uso: python3 montar_explicativo.py config.json saida.mp4
config: {
  "quadros": "frames/%04d.jpg", "fps": 24,          (ou "video": "animacao.mp4")
  "segurar_fim": 1.6,
  "cartoes": [ {"de": 0, "ate": 4.1, "titulo": "Linha branca", "titulo2": "LINHA COLORIDA", "cor2": "erro",
                "pilula": "= 2 Ω  ✗ ERRADO", "cor_pilula": "erro", "rodape": "texto pequeno"},
               {"de": 4.1, "ate": 9, "img": "cartao_pronto.png"} ],
  "falas": [ {"arquivo": "s1.wav", "t": 0.3}, ... ],
  "efeitos": "sfx.wav",           (opcional, de efeitos_sonoros.py)
  "musica": "faixa.mp3", "musica_vol": 0.5, "duracao": 31.6 }
cores: "destaque" (verde da marca) ou "erro" (vermelho).
"""
import json, subprocess, sys, os
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from marca import carregar, fonte, espacado, W, H

def cartao(m, c, out):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    g = Image.new('L', (1, 520))
    for y in range(520): g.putpixel((0, y), int(235 * (1 - y / 520) ** 1.6))
    top = Image.new('RGBA', (W, 520), m['cor_fundo'] + (255,)); top.putalpha(g.resize((W, 520))); im.alpha_composite(top)
    serie = m.get('serie_explica', m['nome'] + ' EXPLICA').split(' ')
    x = 70; f = fonte('preta', 30)
    for i, p in enumerate(serie):
        cor = m['cor_texto'] if i < len(serie) - 1 else m['cor_destaque']; d.text((x, 120), p, font=f, fill=cor + (255,)); x += d.textlength(p + ' ', font=f)
    fh = fonte('semi', 28); d.text((W - 70 - d.textlength(m['handle'], font=fh), 122), m['handle'], font=fh, fill=m['cor_secundaria'] + (255,))
    cor = lambda k: m['cor_erro'] if k == 'erro' else m['cor_destaque']
    f1 = fonte('preta', 72); y = 230
    for txt, cl in ((c.get('titulo'), m['cor_texto']), (c.get('titulo2'), cor(c.get('cor2', 'destaque')))):
        if txt:
            sz = 72
            while d.textlength(txt, font=fonte('preta', sz)) > W - 120 and sz > 40: sz -= 4
            ft = fonte('preta', sz); d.text(((W - d.textlength(txt, font=ft)) / 2, y), txt, font=ft, fill=cl + (255,)); y += sz + 14
    if c.get('pilula'):
        fp = fonte('preta', 48); tw = d.textlength(c['pilula'], font=fp); cp = cor(c.get('cor_pilula', 'destaque'))
        x0 = (W - tw) / 2 - 40; d.rounded_rectangle([x0, 1500, x0 + tw + 80, 1600], 50, fill=m['cor_fundo'] + (235,), outline=cp + (255,), width=5)
        d.text(((W - tw) / 2, 1520), c['pilula'], font=fp, fill=cp + (255,))
    if c.get('rodape'):
        fr = fonte('semi', 32); d.text(((W - d.textlength(c['rodape'], font=fr)) / 2, 1640), c['rodape'], font=fr, fill=m['cor_texto'] + (255,))
    im.save(out)

def dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)

def main(cfg_path, out):
    m = carregar(); cfg = json.load(open(cfg_path, encoding='utf-8'))
    base = os.path.dirname(os.path.abspath(cfg_path)); P = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    wd = os.path.join(os.path.dirname(os.path.abspath(out)), '_tmp_expl/'); os.makedirs(wd, exist_ok=True)
    ins = (['-framerate', str(cfg.get('fps', 24)), '-i', P(cfg['quadros'])] if 'quadros' in cfg else ['-i', P(cfg['video'])])
    fc = [f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},tpad=stop_mode=clone:stop_duration={cfg.get('segurar_fim', 0)},format=rgba[b0]"]
    for k, c in enumerate(cfg.get('cartoes', [])):
        png = P(c['img']) if 'img' in c else f'{wd}cartao{k}.png'
        if 'img' not in c: cartao(m, c, png)
        ins += ['-i', png]
        fc.append(f"[b{k}][{k + 1}:v]overlay=enable='between(t,{c['de']},{c['ate']})'[b{k + 1}]")
    nb = len(cfg.get('cartoes', []))
    fc.append(f"[b{nb}]format=yuv420p[v]")
    video = wd + 'video.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + ins + ['-filter_complex', ';'.join(fc), '-map', '[v]', '-r', '30', '-c:v', 'libx264',
                    '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', video], check=True)
    D = cfg.get('duracao') or dur(video)
    falas = cfg.get('falas', [])
    vin, vf = [], []
    for i, f in enumerate(falas):
        vin += ['-i', P(f['arquivo'])]; ms = int(f['t'] * 1000); vf.append(f"[{i}]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay={ms}|{ms}[f{i}]")
    voz = wd + 'voz.wav'
    if falas:
        vf.append(''.join(f'[f{i}]' for i in range(len(falas))) + f"amix=inputs={len(falas)}:normalize=0,highpass=f=80,acompressor=threshold=-18dB:ratio=3,loudnorm=I=-16:TP=-1.5,apad[n]")
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + vin + ['-filter_complex', ';'.join(vf), '-map', '[n]', '-t', f'{D}', voz], check=True)
    else:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-t', f'{D}', voz], check=True)
    ins = ['-i', video, '-i', voz]; fc = []; mixes = ['[vo]']
    fc.append('[1:a]asplit[vo][sc]')
    n = 2
    if cfg.get('musica'):
        ins += ['-i', P(cfg['musica'])]
        fc.append(f"[{n}:a]atrim=0:{D},volume={cfg.get('musica_vol', 0.5)},afade=t=in:d=0.6,afade=t=out:st={D - 1.6}:d=1.6[mu]")
        fc.append("[mu][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[md]"); mixes.append('[md]'); n += 1
    if cfg.get('efeitos'):
        ins += ['-i', P(cfg['efeitos'])]; fc.append(f"[{n}:a]volume=0.9,apad[fx]"); mixes.append('[fx]'); n += 1
    fc.append(''.join(mixes) + f"amix=inputs={len(mixes)}:normalize=0:duration=first,alimiter=limit=0.95[a]")
    tmp = out[:-4] + '.tmp.mp4'
    r = subprocess.call(['ffmpeg', '-y', '-loglevel', 'error'] + ins + ['-filter_complex', ';'.join(fc), '-map', '0:v', '-map', '[a]', '-c:v', 'copy',
                         '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-t', f'{D}', '-movflags', '+faststart', tmp])
    if r == 0: os.replace(tmp, out); print(f'ok {out} ({D:.1f}s)')
    sys.exit(r)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
