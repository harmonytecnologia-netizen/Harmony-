import subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = '/tmp/claude-0/-home-claude/ab8790be-2718-53fe-a112-dc9313667f61/scratchpad/'
FS = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
FM = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
T = 0.4          # transition length
SPEED = 1.1
CUTS = [4.25, 6.78, 9.75, 12.49, 15.02, 17.58, 20.5, 23.06, 25.59]
TRANS = ['circleopen', 'smoothleft', 'hblur', 'zoomin', 'fadewhite', 'smoothright', 'slideup', 'hblur', 'fadeblack']
# source, start(s), zoom direction (+1 in / -1 out), caption (label, text) or None
SCENES = [
    ('A', 0.3, +1, ('01', 'OBRA EM ANDAMENTO')),
    ('A', 4.2, -1, ('02', 'PASSAGEM DE|CABEAMENTO')),
    ('B', 3.0, +1, ('03', 'INFRAESTRUTURA PARA|SOM E AUTOMAÇÃO')),
    ('A', 10.5, -1, None),
    ('B', 12.6, +1, ('04', 'CADA AMBIENTE|PLANEJADO')),
    ('A', 16.0, -1, None),
    ('A', 25.3, +1, None),
    ('B', 24.0, -1, ('05', 'TUDO PENSADO ANTES|DO ACABAMENTO')),
]
INTRO, END = S + 'r_som.mp4', S + 'r_end.mp4'
END_LEN = 3.6

def caption_pngs(k, label, text):
    W, H = 1080, 1920
    # shade (static)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    GH = 900
    g = Image.new('L', (1, GH))
    for y in range(GH): g.putpixel((0, y), int(175 * min(1, y / 480) ** 1.5))
    g = g.resize((W, GH)); band = Image.new('RGBA', (W, GH), (8, 16, 13, 255)); band.putalpha(g)
    sh.alpha_composite(band, (0, H - GH)); sh.save(f'{S}pshade{k}.png')
    # text block (animated)
    lines = text.split('|')
    f = ImageFont.truetype(FS, 60); fl = ImageFont.truetype(FM, 28)
    BW, BH = 1000, 110 + 80 * len(lines)
    tx = Image.new('RGBA', (BW, BH), (0, 0, 0, 0)); d = ImageDraw.Draw(tx)
    d.rectangle([0, 22, 80, 27], fill=(84, 223, 174, 255))
    d.text((98, 6), label, font=fl, fill=(84, 223, 174, 255))
    shadow = Image.new('RGBA', (BW, BH), (0, 0, 0, 0)); ds = ImageDraw.Draw(shadow)
    y = 62
    for ln in lines:
        x = 0
        for c in ln:
            ds.text((x, y + 4), c, font=f, fill=(0, 0, 0, 210)); x += f.getlength(c) + 4
        y += 80
    shadow = shadow.filter(ImageFilter.GaussianBlur(7))
    out = Image.new('RGBA', (BW, BH), (0, 0, 0, 0)); out.alpha_composite(shadow); out.alpha_composite(tx)
    d = ImageDraw.Draw(out); y = 62
    for ln in lines:
        x = 0
        for c in ln:
            d.text((x, y), c, font=f, fill=(242, 245, 239, 255)); x += f.getlength(c) + 4
        y += 80
    out.save(f'{S}ptext{k}.png')
    return BH

GRADE = ("eq=contrast=1.1:saturation=0.86:gamma=0.97,"
         "colorbalance=rs=0.05:gs=0.01:bs=-0.06:rm=0.035:bm=-0.035:rh=0.025:bh=-0.03,"
         "curves=all='0/0.035 0.5/0.5 1/0.97',vignette=angle=PI/5,noise=alls=4:allf=t")

# clip lengths
lens = []
lens.append(CUTS[0] + T / 2)                                   # intro
for i in range(len(SCENES)):
    lens.append(CUTS[i + 1] - CUTS[i] + T)
total = CUTS[-1] - T / 2 + END_LEN
lens.append(END_LEN)

inputs, fc = [], []
idx = 0
inputs += ['-i', INTRO]; fc.append(f"[{idx}:v]trim=0:{lens[0]:.3f},setpts=PTS-STARTPTS,format=yuv420p,settb=1/30[s0]"); idx += 1
for k, (src, st, zdir, cap) in enumerate(SCENES):
    L = lens[k + 1]
    srclen = L * SPEED + 0.2
    inputs += ['-ss', f'{st}', '-t', f'{srclen:.3f}', '-i', f'{S}stab_{src}.mp4']
    vi = idx; idx += 1
    n = int(L * 30) + 2
    z = f"1.0+0.0016*on" if zdir > 0 else f"{1.0 + 0.0016 * n:.4f}-0.0016*on"
    chain = (f"[{vi}:v]setpts=(PTS-STARTPTS)/{SPEED},fps=30,trim=0:{L:.3f},setpts=PTS-STARTPTS,"
             f"scale=1296:2304:flags=lanczos,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,"
             f"{GRADE},format=yuv420p")
    if cap:
        BH = caption_pngs(k, *cap)
        inputs += ['-loop', '1', '-t', f'{L:.3f}', '-i', f'{S}pshade{k}.png']; si = idx; idx += 1
        inputs += ['-loop', '1', '-t', f'{L:.3f}', '-i', f'{S}ptext{k}.png']; ti = idx; idx += 1
        t0 = T / 2 + 0.15; t1 = L - T / 2 - 0.25
        fc.append(chain + f"[b{k}]")
        fc.append(f"[{si}:v]format=rgba,fade=t=in:st={t0 - 0.1:.2f}:d=0.4:alpha=1,fade=t=out:st={t1:.2f}:d=0.3:alpha=1[sh{k}]")
        fc.append(f"[{ti}:v]format=rgba,fade=t=in:st={t0:.2f}:d=0.35:alpha=1,fade=t=out:st={t1:.2f}:d=0.25:alpha=1[tx{k}]")
        fc.append(f"[b{k}][sh{k}]overlay=0:0:shortest=1[c{k}]")
        ybase = 1300 - BH // 2
        fc.append(f"[c{k}][tx{k}]overlay=x=90:y='{ybase}+60*pow(max(0\\,1-(t-{t0:.2f})/0.45)\\,3)':shortest=1,format=yuv420p,settb=1/30[s{k + 1}]")
    else:
        fc.append(chain + f",settb=1/30[s{k + 1}]")
inputs += ['-i', END]; fc.append(f"[{idx}:v]trim=0:{END_LEN},setpts=PTS-STARTPTS,format=yuv420p,settb=1/30[s{len(SCENES) + 1}]"); idx += 1

prev = 's0'
for j, c in enumerate(CUTS):
    out = f'x{j}'
    fc.append(f"[{prev}][s{j + 1}]xfade=transition={TRANS[j]}:duration={T}:offset={c - T / 2:.3f}[{out}]")
    prev = out
fc.append(f"[{prev}]format=yuv420p[vout]")

cmd = ['ffmpeg', '-y', '-loglevel', 'error'] + inputs + ['-filter_complex', ';'.join(fc), '-map', '[vout]', '-r', '30',
       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', sys.argv[1]]
print(f'total {total:.2f}s', file=sys.stderr)
sys.exit(subprocess.call(cmd))
