"""Reel premium from still images: intro de Som + Ken Burns + serif captions + premium end card, cut to music beats.
usage: reel_premium.py config.json out.mp4
config: {"music": "...mp3", "music_start": 0, "intro": "intro_som.mp4",
         "scenes": [{"img": "...", "kicker": "01 · MEDIR", "title": "Linha 1|Linha 2", "zoom": "in"}, ...],
         "end_title": "Agende uma conversa.", "end_sub": "Projetos de som, cinema e automação."}
"""
import json, subprocess, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
FD = '/home/claude/fonts/'
SERIF = FD + 'Playfair-400-normal.ttf'
SANS_L = '/usr/share/fonts/opentype/inter/Inter-Light.otf'
CREAM = (244, 240, 232); MINT = (84, 223, 174); SUB = (205, 198, 186)
W, H, FPS, T = 1080, 1920, 30, 0.6
LOGO = Image.open('/mnt/user-data/uploads/Logo_MOVE_com_automação_e_segurança.png').convert('RGBA')
LOGO = LOGO.crop(LOGO.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox())

def tracked(d, x, y, text, font, fill, track, center=False):
    tw = sum(d.textlength(c, font=font) + track for c in text) - track
    if center: x = (W - tw) / 2
    for c in text:
        d.text((x, y), c, font=font, fill=fill); x += d.textlength(c, font=font) + track

def prep_image(src, out):
    im = Image.open(src).convert('RGB')
    r = max(W * 1.18 / im.width, H * 1.18 / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.05); im = ImageEnhance.Color(im).enhance(0.93)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=55, threshold=2))
    x = (im.width - round(W * 1.18)) // 2; y = (im.height - round(H * 1.18)) // 2
    im.crop((x, y, x + round(W * 1.18), y + round(H * 1.18))).save(out, quality=95)

def caption(kicker, title, out):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g = Image.new('L', (1, H))
    for y in range(H):
        t = y / H
        a = 0.55 * max(0, 1 - t / 0.16) + 0.92 * max(0, (t - 0.52) / 0.48) ** 1.5
        g.putpixel((0, y), int(255 * min(1, a)))
    sh = Image.new('RGBA', (W, H), (8, 10, 9, 255)); sh.putalpha(g.resize((W, H))); im.alpha_composite(sh)
    l = LOGO.resize((170, round(LOGO.height * 170 / LOGO.width)), Image.LANCZOS)
    im.alpha_composite(l, ((W - 170) // 2, 110))
    d = ImageDraw.Draw(im)
    lines = title.split('|'); y = 1440 - 100 * (len(lines) - 1)
    sh2 = Image.new('RGBA', (W, H), (0,0,0,0)); d2 = ImageDraw.Draw(sh2)
    tracked(d2, 90, y - 68, kicker, ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Medium.otf', 28), (0,0,0,220), 8)
    im.alpha_composite(sh2.filter(ImageFilter.GaussianBlur(5))); d = ImageDraw.Draw(im)
    tracked(d, 90, y - 70, kicker, ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Medium.otf', 28), (110, 235, 190, 255), 8)
    f = ImageFont.truetype(SERIF, 84)
    for ln in lines:
        d.text((86, y), ln, font=f, fill=CREAM + (255,)); y += 100
    d.line([(90, y + 30), (170, y + 30)], fill=(150, 140, 125, 255), width=1)
    tracked(d, 0, H - 150, '@move.s.a', ImageFont.truetype(SANS_L, 24), (170, 162, 150, 255), 7, True)
    im.save(out)

def end_card(title, sub, out):
    im = Image.new('RGB', (W, H), (10, 12, 11))
    glow = Image.new('L', (W, H), 0); ImageDraw.Draw(glow).ellipse([-200, 300, W + 200, 1500], fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(220))
    im = Image.composite(Image.new('RGB', (W, H), (48, 38, 26)), im, glow)
    l = LOGO.resize((560, round(LOGO.height * 560 / LOGO.width)), Image.LANCZOS)
    im.paste(l, ((W - 560) // 2, 620), l)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(SERIF, 72); tw = d.textlength(title, font=f); d.text(((W - tw) / 2, 1000), title, font=f, fill=CREAM)
    f2 = ImageFont.truetype(SANS_L, 32); tw = d.textlength(sub, font=f2); d.text(((W - tw) / 2, 1110), sub, font=f2, fill=SUB)
    d.line([(W / 2 - 40, 1200), (W / 2 + 40, 1200)], fill=(150, 140, 125), width=1)
    tracked(d, 0, 1240, '@move.s.a', ImageFont.truetype(SANS_L, 30), MINT, 8, True)
    im.save(out, quality=95)

def beats(music, start, dur):
    import librosa
    y, sr = librosa.load(music, sr=22050, offset=start, duration=dur)
    _, b = librosa.beat.beat_track(y=y, sr=sr)
    return librosa.frames_to_time(b, sr=sr).tolist()

def main(cfg_path, out):
    cfg = json.load(open(cfg_path)); wd = os.path.dirname(os.path.abspath(out)) + '/_rp/'
    os.makedirs(wd, exist_ok=True)
    scenes = cfg['scenes']; n = len(scenes)
    bt = beats(cfg['music'], cfg.get('music_start', 0), 40)
    # cut points: intro ends ~4.2s, then every ~4s snapped to nearest beat
    cuts, t = [], 4.2
    for k in range(n + 1):
        cuts.append(min(bt, key=lambda b: abs(b - t)) if bt else t); t = cuts[-1] + 4.0
    END = 3.8; total = cuts[-1] - T / 2 + END
    lens = [cuts[0] + T / 2] + [cuts[i + 1] - cuts[i] + T for i in range(n)] + [END]
    inputs, fc = ['-i', cfg['intro']], [f"[0:v]trim=0:{lens[0]:.3f},setpts=PTS-STARTPTS,format=yuv420p,settb=1/30[s0]"]
    idx = 1
    for k, sc in enumerate(scenes):
        L = lens[k + 1]; nf = int(L * FPS) + 2
        prep_image(sc['img'], f'{wd}img{k}.jpg'); caption(sc['kicker'], sc['title'], f'{wd}cap{k}.png')
        inputs += ['-loop', '1', '-framerate', '30', '-t', f'{L:.3f}', '-i', f'{wd}img{k}.jpg']; ii = idx; idx += 1
        inputs += ['-loop', '1', '-framerate', '30', '-t', f'{L:.3f}', '-i', f'{wd}cap{k}.png']; ci = idx; idx += 1
        zin = sc.get('zoom', 'in') == 'in'
        z = "1.0+0.0009*on" if zin else f"{1.0 + 0.0009 * nf:.4f}-0.0009*on"
        fc.append(f"[{ii}:v]zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps=30,"
                  f"trim=0:{L:.3f},setpts=PTS-STARTPTS,format=yuv420p,noise=alls=3:allf=t[b{k}]")
        t0 = T / 2 + 0.25; t1 = L - T / 2 - 0.35
        fc.append(f"[{ci}:v]format=rgba,fade=t=in:st={t0:.2f}:d=0.6:alpha=1,fade=t=out:st={t1:.2f}:d=0.3:alpha=1[c{k}]")
        fc.append(f"[b{k}][c{k}]overlay=0:0:shortest=1,format=yuv420p,settb=1/30[s{k + 1}]")
    end_card(cfg.get('end_title', 'Agende uma conversa.'), cfg.get('end_sub', 'Projetos de som, cinema e automação.'), f'{wd}end.jpg')
    inputs += ['-loop', '1', '-framerate', '30', '-t', f'{END}', '-i', f'{wd}end.jpg']
    fc.append(f"[{idx}:v]zoompan=z='1.0+0.0006*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps=30,trim=0:{END},setpts=PTS-STARTPTS,format=yuv420p,settb=1/30[s{n + 1}]")
    idx += 1
    trans = ['fade', 'smoothup', 'fade', 'smoothleft', 'fade', 'fadeblack', 'fade', 'smoothup']
    prev = 's0'
    for j, c in enumerate(cuts):
        tr = 'circleopen' if j == 0 else ('fadeblack' if j == len(cuts) - 1 else trans[j % len(trans)])
        fc.append(f"[{prev}][s{j + 1}]xfade=transition={tr}:duration={T}:offset={c - T / 2:.3f}[x{j}]"); prev = f'x{j}'
    ms = cfg.get('music_start', 0)
    inputs += ['-ss', f'{ms}', '-i', cfg['music']]
    fc.append(f"[{idx}:a]atrim=0:{total:.3f},afade=t=in:st=0:d=0.6,afade=t=out:st={total - 2.6:.3f}:d=2.6,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
    cmd = ['ffmpeg', '-y', '-loglevel', 'error'] + inputs + ['-filter_complex', ';'.join(fc), '-map', f'[{prev}]', '-map', '[aout]',
           '-r', '30', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-maxrate', '9M', '-bufsize', '18M', '-pix_fmt', 'yuv420p',
           '-profile:v', 'high', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-t', f'{total:.3f}', out]
    print(f'total {total:.2f}s cuts {[round(c, 2) for c in cuts]}', file=sys.stderr)
    sys.exit(subprocess.call(cmd))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
