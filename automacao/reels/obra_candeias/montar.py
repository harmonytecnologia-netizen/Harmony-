# Reel obra real — Clube Candeias (BC): som embutido no forro. Uso: python3 montar.py <pasta_videos> <saida.mp4>
import subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont
SRC, OUT = sys.argv[1], sys.argv[2]
WD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp'); os.makedirs(WD, exist_ok=True)
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))
V = lambda h: os.path.join(SRC, f'WhatsApp Video 2026-11-13 at {h}.mp4')
PF = os.path.join(R, 'automacao/fonts/Playfair-400-normal.ttf'); IN = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
CENAS = [  # video, inicio, dur, kicker, titulo
    ('08.38.45', 59.0, 2.8, 'OBRA REAL · MOVE', 'Onde está o som|deste salão?'),
    ('08.38.58', 20.6, 2.4, None, 'No forro.|Sem aparecer.'),
    ('08.40.23', 6.0, 2.6, 'BALNEÁRIO CAMBORIÚ', 'Clube Candeias'),
    ('08.38.45', 9.0, 3.0, 'SOM AMBIENTE', 'Música em todo|o salão'),
    ('08.38.16', 24.0, 2.6, None, None),
    ('08.39.59', 3.0, 2.6, 'CONVIVÊNCIA', 'Cada espaço|com clima próprio'),
    ('08.39.56', 4.0, 2.6, 'EVENTOS', 'E som pronto|para receber'),
    ('08.38.58', 1.5, 2.8, 'PROJETO E INSTALAÇÃO', 'MOVE'),
]
X = 0.35
def card(k, kick, tit):
    im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    g = Image.new('L', (1, 900)); [g.putpixel((0, y), int(190 * min(1, y / 600) ** 1.4)) for y in range(900)]
    band = Image.new('RGBA', (1080, 900), (8, 16, 13, 255)); band.putalpha(g.resize((1080, 900))); im.alpha_composite(band, (0, 1020))
    d = ImageDraw.Draw(im); y = 1500
    lines = tit.split('|')
    y -= 92 * (len(lines) - 1)
    if kick:
        fk = ImageFont.truetype(IN, 30); d.rectangle([90, y - 62, 150, y - 58], fill=(84, 223, 174)); d.text((168, y - 80), kick, font=fk, fill=(84, 223, 174))
    ft = ImageFont.truetype(PF, 92 if len(tit) > 6 else 130)
    for ln in lines:
        d.text((86, y), ln, font=ft, fill=(242, 245, 239)); y += 104
    p = f'{WD}/card{k}.png'; im.save(p); return p
parts = []
for k, (v, ss, du, kick, tit) in enumerate(CENAS):
    o = f'{WD}/c{k}.mp4'; z = '+' if k % 2 == 0 else '-'
    zexp = f"1.0+0.06*t/{du}" if z == '+' else f"1.06-0.06*t/{du}"
    vf = (f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,"
          f"hqdn3d=2:2:4:4,cas=0.5,eq=contrast=1.06:saturation=1.08:gamma=0.97,colorbalance=rm=0.03:bm=-0.03,"
          f"scale=w='trunc(1080*({zexp})/2)*2':h='trunc(1920*({zexp})/2)*2':eval=frame,crop=1080:1920,setsar=1")
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(ss), '-i', V(v)]
    if tit:
        cmd += ['-loop', '1', '-i', card(k, kick, tit), '-filter_complex', f"[0:v]{vf}[b];[1:v]format=rgba,fade=in:st=0.15:d=0.35:alpha=1[t];[b][t]overlay=0:0:shortest=1,format=yuv420p[v]", '-map', '[v]']
    else:
        cmd += ['-vf', vf + ',format=yuv420p']
    cmd += ['-t', str(du + X), '-an', '-c:v', 'libx264', '-crf', '17', '-preset', 'veryfast', o]
    subprocess.run(cmd, check=True); parts.append((o, du + X))
fim = f'{WD}/fim.mp4'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', os.path.join(R, 'automacao/assets/tela_final.mp4'), '-vf', 'scale=1080:1920,fps=30,setsar=1,format=yuv420p', '-an', '-c:v', 'libx264', '-crf', '17', fim], check=True)
parts.append((fim, 3.6))
TR = ['fade', 'smoothleft', 'fadeblack', 'hblur', 'smoothright', 'zoomin', 'slideup', 'fade']
ins = []; [ins.extend(['-i', p]) for p, _ in parts]
fc = []; acc = parts[0][1]; last = '0:v'
for i in range(1, len(parts)):
    off = acc - X; lab = f'x{i}'
    fc.append(f'[{last}][{i}:v]xfade=transition={TR[(i - 1) % len(TR)]}:duration={X}:offset={off:.3f}[{lab}]'); last = lab
    acc = off + parts[i][1]
D = acc
mus = os.path.join(R, 'automacao/musicas/Free Advice - Chris von Sneidern.mp3')
fc.append(f'[{len(parts)}:a]atrim=8:{8 + D},asetpts=PTS-STARTPTS,volume=0.8,afade=t=in:d=0.4,afade=t=out:st={D - 1.8}:d=1.8[a]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + ins + ['-i', mus, '-filter_complex', ';'.join(fc), '-map', f'[{last}]', '-map', '[a]',
                '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-t', f'{D:.2f}', OUT], check=True)
print('ok', OUT, round(D, 2))
