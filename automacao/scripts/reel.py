import subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = '/mnt/user-data/attachments/ab8790be-2718-53fe-a112-dc9313667f61/'
A = D + 'b2fa8058-WhatsApp_Video_2026-11-06_at_08.29.46.mp4'
Bv = D + 'cbbb82fc-WhatsApp_Video_2026-11-06_at_08.30.21.mp4'
FS = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
FM = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
SPEED = 1.15

SEGS = [  # src, start, end, small label, big caption
    (A, 0.0, 2.7, '01', 'OBRA EM ANDAMENTO'),
    (A, 4.0, 7.0, '02', 'PASSAGEM DE CABEAMENTO'),
    (Bv, 3.0, 8.5, '03', 'INFRAESTRUTURA PARA|SOM E AUTOMAÇÃO'),
    (A, 10.0, 14.5, None, None),
    (Bv, 18.0, 20.0, '04', 'CADA AMBIENTE PLANEJADO'),
    (A, 25.0, 28.5, None, None),
    (Bv, 24.0, 27.5, '05', 'TUDO PENSADO|ANTES DO ACABAMENTO'),
]

def caption_png(path, label, text):
    W, H = 1080, 1920
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    # soft dark gradient at the lower part for legibility
    GH = 1020
    grad = Image.new('L', (1, GH))
    for y in range(GH): grad.putpixel((0, y), int(185 * min(1, (y / 520)) ** 1.5))
    grad = grad.resize((W, GH))
    shade = Image.new('RGBA', (W, GH), (8, 16, 13, 255)); shade.putalpha(grad)
    im.alpha_composite(shade, (0, H - GH))
    # text shadow layer
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    d = ImageDraw.Draw(im)
    lines = text.split('|')
    f = ImageFont.truetype(FS, 52); fl = ImageFont.truetype(FM, 26)
    y = 1300 - 70 * (len(lines) - 1)
    x = 90
    d.rectangle([x, y - 46, x + 70, y - 41], fill=(84, 223, 174, 255))
    d.text((x + 88, y - 60), label, font=fl, fill=(84, 223, 174, 255))
    y0 = y
    for ln in lines:
        cx = x
        for c in ln:
            ds.text((cx, y + 3), c, font=f, fill=(0, 0, 0, 200)); cx += f.getlength(c) + 3
        y += 70
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    base = Image.new('RGBA', (W, H), (0, 0, 0, 0)); base.alpha_composite(im); base.alpha_composite(sh)
    im = base; d = ImageDraw.Draw(im); y = y0
    for ln in lines:
        cx = x
        for c in ln:
            d.text((cx, y), c, font=f, fill=(242, 245, 239, 255)); cx += f.getlength(c) + 3
        y += 70
    im.save(path)

for k, (src, s, e, lab, txt) in enumerate(SEGS):
    if txt: caption_png(f'cap{k}.png', lab, txt)

GRADE = ("deshake,scale=1080:-2,crop=1080:1920,setsar=1,"
         "eq=contrast=1.07:saturation=0.8:gamma=0.97,"
         "colorbalance=rs=0.05:gs=0.01:bs=-0.06:rm=0.04:gm=0.0:bm=-0.04:rh=0.03:bh=-0.03,"
         "curves=all='0/0.045 0.5/0.5 1/0.96',vignette=angle=PI/4.5,noise=alls=7:allf=t,fps=30")

inputs, chains, labels = [], [], []
idx = 0
for k, (src, s, e, lab, txt) in enumerate(SEGS):
    inputs += ['-ss', f'{s}', '-t', f'{e - s + 0.5}', '-i', src]
    vi = idx; idx += 1
    dur = (e - s) / SPEED
    c = f"[{vi}:v]trim=0:{e - s},setpts=(PTS-STARTPTS)/{SPEED},{GRADE},trim=0:{dur:.3f},setpts=PTS-STARTPTS[v{k}]"
    chains.append(c)
    if txt:
        inputs += ['-loop', '1', '-t', f'{dur:.3f}', '-i', f'cap{k}.png']
        ci = idx; idx += 1
        chains.append(f"[{ci}:v]format=rgba,fade=t=in:st=0.25:d=0.4:alpha=1,fade=t=out:st={dur - 0.45:.3f}:d=0.35:alpha=1[c{k}]")
        chains.append(f"[v{k}][c{k}]overlay=0:0:shortest=1,format=yuv420p[o{k}]")
        labels.append(f'[o{k}]')
    else:
        chains.append(f"[v{k}]format=yuv420p[o{k}]"); labels.append(f'[o{k}]')
chains.append(''.join(labels) + f"concat=n={len(SEGS)}:v=1:a=0[out]")
cmd = ['ffmpeg', '-y', '-loglevel', 'error'] + inputs + ['-filter_complex', ';'.join(chains), '-map', '[out]', '-r', '30',
       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', sys.argv[1]]
sys.exit(subprocess.call(cmd))
