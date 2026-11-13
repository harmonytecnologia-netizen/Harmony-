"""Reel PRO a partir de VIDEOS REAIS do celular: estabiliza, cor de cinema, cortes no ritmo da musica,
zoom lento alternado, transicoes variadas, legendas numeradas animadas e tela final com logo.
uso: python3 reel_videos.py config.json saida.mp4
config: {"musica": "faixa.mp3", "musica_inicio": 0, "duracao_cena": 2.6, "velocidade": 1.1, "estabilizar": true,
         "cenas": [{"video": "obra1.mp4", "inicio": 0.5, "legenda": ["01", "TEXTO LINHA 1|LINHA 2"]},
                   {"video": "obra2.mp4", "inicio": 3.0}],
         "frase_final": "...", "sub_final": "..."}
Dica: 6-10 cenas de 2-3 s = Reel de 20-30 s. Gancho: a cena mais impressionante PRIMEIRO.
"""
import json, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from marca import carregar, fonte, W, H
from reel_imagens import tela_final, batidas

T = 0.4
TRANS = ['circleopen', 'smoothleft', 'hblur', 'zoomin', 'fadewhite', 'smoothright', 'slideup', 'hblur', 'fadeblack']
COR = ("eq=contrast=1.08:saturation=0.9:gamma=0.98,colorbalance=rs=0.04:bs=-0.05:rm=0.03:bm=-0.03,"
       "curves=all='0/0.03 0.5/0.5 1/0.97',vignette=angle=PI/5")

def tem_vidstab():
    o = subprocess.run(['ffmpeg', '-hide_banner', '-filters'], capture_output=True, text=True).stdout
    return 'vidstabdetect' in o

def estabilizar(src, out):
    if os.path.exists(out): return out
    if tem_vidstab():
        trf = out + '.trf'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-vf', f'vidstabdetect=shakiness=6:result={trf}', '-f', 'null', '-'], check=True)
        vf = f'vidstabtransform=input={trf}:smoothing=20:zoom=4,unsharp=5:5:0.6'
    else:
        vf = 'deshake,unsharp=5:5:0.6'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-vf', vf + ',hqdn3d=2:2:4:4', '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', out], check=True)
    return out

def legenda_png(m, k, rotulo, texto, wd):
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); GH = 900
    g = Image.new('L', (1, GH))
    for y in range(GH): g.putpixel((0, y), int(175 * min(1, y / 480) ** 1.5))
    band = Image.new('RGBA', (W, GH), m['cor_fundo'] + (255,)); band.putalpha(g.resize((W, GH))); sh.alpha_composite(band, (0, H - GH))
    sh.save(f'{wd}sh{k}.png')
    linhas = texto.split('|'); f = fonte('semi', 60); fl = fonte('media', 28)
    BW, BH = 1000, 110 + 80 * len(linhas)
    out = Image.new('RGBA', (BW, BH), (0, 0, 0, 0)); sd = Image.new('RGBA', (BW, BH), (0, 0, 0, 0)); ds = ImageDraw.Draw(sd)
    y = 62
    for ln in linhas: ds.text((0, y + 4), ln, font=f, fill=(0, 0, 0, 210)); y += 80
    out.alpha_composite(sd.filter(ImageFilter.GaussianBlur(7))); d = ImageDraw.Draw(out)
    d.rectangle([0, 22, 80, 27], fill=m['cor_destaque'] + (255,)); d.text((98, 6), rotulo, font=fl, fill=m['cor_destaque'] + (255,))
    y = 62
    for ln in linhas: d.text((0, y), ln, font=f, fill=m['cor_texto'] + (255,)); y += 80
    out.save(f'{wd}tx{k}.png'); return BH

def main(cfg_path, out):
    m = carregar(); cfg = json.load(open(cfg_path, encoding='utf-8'))
    base = os.path.dirname(os.path.abspath(cfg_path)); P = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    wd = os.path.join(os.path.dirname(os.path.abspath(out)), '_tmp_reelv/'); os.makedirs(wd, exist_ok=True)
    cenas = cfg['cenas']; n = len(cenas); dc = cfg.get('duracao_cena', 2.6); vel = cfg.get('velocidade', 1.1)
    fontes = {}
    for sc in cenas:
        v = P(sc['video'])
        if v not in fontes:
            fontes[v] = estabilizar(v, f'{wd}est_{len(fontes)}.mp4') if cfg.get('estabilizar', True) else v
    bt = batidas(P(cfg['musica']), cfg.get('musica_inicio', 0), 60)
    cortes, t = [], dc
    for k in range(n):
        cortes.append(min(bt, key=lambda b: abs(b - t)) if bt else t); t = cortes[-1] + dc
    FIM = 3.6; total = cortes[-1] - T / 2 + FIM
    lens = [cortes[0] + T / 2] + [cortes[i + 1] - cortes[i] + T for i in range(n - 1)] + [FIM]
    inputs, fc, idx = [], [], 0
    for k, sc in enumerate(cenas):
        L = lens[k]; nf = int(L * 30) + 2
        inputs += ['-ss', f"{sc.get('inicio', 0)}", '-t', f'{L * vel + 0.3:.3f}', '-i', fontes[P(sc['video'])]]; vi = idx; idx += 1
        z = "1.0+0.0016*on" if k % 2 == 0 else f"{1.0 + 0.0016 * nf:.4f}-0.0016*on"
        ch = (f"[{vi}:v]setpts=(PTS-STARTPTS)/{vel},fps=30,trim=0:{L:.3f},setpts=PTS-STARTPTS,"
              f"scale=1296:2304:force_original_aspect_ratio=increase,crop=1296:2304,"
              f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,{COR},format=yuv420p")
        if sc.get('legenda'):
            BH = legenda_png(m, k, *sc['legenda'], wd)
            inputs += ['-loop', '1', '-t', f'{L:.3f}', '-i', f'{wd}sh{k}.png']; si = idx; idx += 1
            inputs += ['-loop', '1', '-t', f'{L:.3f}', '-i', f'{wd}tx{k}.png']; ti = idx; idx += 1
            t0 = (0.1 if k == 0 else T / 2 + 0.15); t1 = L - T / 2 - 0.25
            fc.append(ch + f"[b{k}]")
            fc.append(f"[{si}:v]format=rgba,fade=t=in:st={max(0, t0 - 0.1):.2f}:d=0.4:alpha=1,fade=t=out:st={t1:.2f}:d=0.3:alpha=1[sh{k}]")
            fc.append(f"[{ti}:v]format=rgba,fade=t=in:st={t0:.2f}:d=0.35:alpha=1,fade=t=out:st={t1:.2f}:d=0.25:alpha=1[tx{k}]")
            fc.append(f"[b{k}][sh{k}]overlay=0:0:shortest=1[c{k}]")
            yb = 1300 - BH // 2
            fc.append(f"[c{k}][tx{k}]overlay=x=90:y='{yb}+60*pow(max(0\\,1-(t-{t0:.2f})/0.45)\\,3)':shortest=1,format=yuv420p,settb=1/30[s{k}]")
        else:
            fc.append(ch + f",settb=1/30[s{k}]")
    tela_final(m, cfg.get('frase_final', m['frase_final']), cfg.get('sub_final', m['sub_final']), f'{wd}fim.jpg')
    inputs += ['-loop', '1', '-framerate', '30', '-t', f'{FIM}', '-i', f'{wd}fim.jpg']
    fc.append(f"[{idx}:v]scale={W}:{H},trim=0:{FIM},setpts=PTS-STARTPTS,format=yuv420p,settb=1/30[s{n}]"); idx += 1
    prev = 's0'
    for j, c in enumerate(cortes):
        fc.append(f"[{prev}][s{j + 1}]xfade=transition={TRANS[j % len(TRANS)] if j < len(cortes) - 1 else 'fadeblack'}:duration={T}:offset={c - T / 2:.3f}[x{j}]"); prev = f'x{j}'
    inputs += ['-ss', f"{cfg.get('musica_inicio', 0)}", '-i', P(cfg['musica'])]
    fc.append(f"[{idx}:a]atrim=0:{total:.3f},afade=t=in:st=0:d=0.3,afade=t=out:st={total - 2.4:.3f}:d=2.4,loudnorm=I=-14:TP=-1.5[a]")
    tmp = out[:-4] + '.tmp.mp4'
    cmd = ['ffmpeg', '-y', '-loglevel', 'error'] + inputs + ['-filter_complex', ';'.join(fc), '-map', f'[{prev}]', '-map', '[a]',
           '-r', '30', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
           '-ar', '48000', '-movflags', '+faststart', '-t', f'{total:.3f}', tmp]
    r = subprocess.call(cmd)
    if r == 0: os.replace(tmp, out); print(f'ok {out} ({total:.1f}s)')
    sys.exit(r)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
