import sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import intro as B   # shared bg, logo, helpers
from intro import W, H, FPS, cx, cy, MINT, ease_out, ease_io, seg, paste, xx, yy

FONT_M = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
FONT_S = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
CREAM = np.array([242, 245, 239], np.float32)

def spaced(text, size, track, font=FONT_M):
    f = ImageFont.truetype(font, size)
    w = sum(f.getlength(c) for c in text) + track * (len(text) - 1)
    im = Image.new('L', (int(w) + 20, int(size * 1.6)), 0)
    d = ImageDraw.Draw(im); x = 10
    for c in text:
        d.text((x, size * 0.2), c, font=f, fill=255); x += f.getlength(c) + track
    return np.asarray(im).astype(np.float32) / 255

def put_mask(img, m, xc, y, color, a):
    if a <= 0: return img
    h, w = m.shape; x0 = int(xc - w / 2); y = int(y)
    al = m * a
    img[y:y + h, x0:x0 + w] = img[y:y + h, x0:x0 + w] * (1 - al[..., None]) + color * al[..., None]
    return img

def add_glow_mask(img, mask_img, color, strength, blur=18):
    g = np.asarray(mask_img.filter(ImageFilter.GaussianBlur(blur))).astype(np.float32) / 255
    return img + color * g[..., None] * strength

def grade(img, i, t, dur, warm=True):
    img = img * B.vign
    if warm:
        img = img * np.array([1.04, 1.0, 0.92], np.float32) + np.array([6, 5, 2], np.float32)
    img *= 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    g = B.grain_bank[i % len(B.grain_bank)]
    img += np.repeat(np.repeat(g, 2, 0), 2, 1)[..., None] * 5.5
    img *= ease_io(seg(t, 0, 0.3)) * (1 - ease_io(seg(t, dur - 0.45, dur)))
    return np.clip(img, 0, 255).astype(np.uint8)

def logo_reveal(img, t, t0, t1, y=None, dur=4.4):
    rv = ease_out(seg(t, t0, t1))
    if rv <= 0: return img
    y = B.LOGO_Y if y is None else y
    def mask(w, rv=rv):
        u = np.linspace(0, 1, w); return np.clip((-0.15 + rv * 1.3 - u) / 0.15, 0, 1)
    sc = (1.06 - 0.06 * rv) * (1 + 0.02 * ease_io(seg(t, t1, dur)))
    return paste(img, B.logo_np, int(cx - B.LW / 2), int(y), min(1, rv * 1.4), mask, sc)

# ===================== CINEMA =====================
TAG_CIN = spaced('CINEMA  ·  SOM  ·  AUTOMAÇÃO', 30, 9)
HANDLE = spaced('@move.s.a', 34, 8)
def cinema(i, dur=4.6):
    t = i / FPS
    img = B.bg.copy() * 0.55
    SW, SH = 940, 529
    sx0, sy0 = cx - SW / 2, cy - SH / 2 - 60
    # line grows, then opens vertically into screen
    lw = ease_out(seg(t, 0.25, 0.9)) * SW
    op = ease_out(seg(t, 0.95, 1.55))
    h = max(3, op * SH)
    flash = math.exp(-((t - 1.5) / 0.18) ** 2)
    if lw > 2:
        m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
        d.rounded_rectangle([cx - lw / 2, sy0 + SH / 2 - h / 2, cx + lw / 2, sy0 + SH / 2 + h / 2], radius=10, fill=255)
        img = add_glow_mask(img, m, np.array([150, 230, 200], np.float32), 0.55 + 1.6 * flash, blur=60)
        ma = np.asarray(m).astype(np.float32) / 255
        # screen interior: bright while line, then settle to deep screen with soft gradient
        bright = 1 - ease_io(seg(t, 1.45, 2.0))
        inner = (np.array([20, 40, 34], np.float32) + 25 * np.exp(-((yy - (sy0 + SH * 0.3)) / 380) ** 2)[..., None])
        col = inner * (1 - bright)[..., None] if False else inner * (1 - bright) + np.array([225, 250, 240], np.float32) * bright
        img = img * (1 - ma[..., None]) + col * ma[..., None]
        # thin mint border
        bm = Image.new('L', (W, H), 0); d2 = ImageDraw.Draw(bm)
        d2.rounded_rectangle([cx - lw / 2, sy0 + SH / 2 - h / 2, cx + lw / 2, sy0 + SH / 2 + h / 2], radius=10, outline=255, width=3)
        bb = np.asarray(bm).astype(np.float32) / 255 * 0.8
        img = img * (1 - bb[..., None]) + MINT * bb[..., None]
    # light spill on floor (reflection)
    refl = op * (0.5 + 1.2 * flash)
    img += (np.exp(-(((xx - cx) / 520) ** 2 + ((yy - (sy0 + SH + 260)) / 140) ** 2)) * refl)[..., None] * np.array([40, 70, 58], np.float32)
    # logo inside screen
    img = logo_reveal(img, t, 1.75, 2.7, y=sy0 + SH / 2 - B.LH / 2 - 10, dur=dur)
    a = ease_out(seg(t, 2.5, 3.2))
    img = put_mask(img, TAG_CIN, cx, sy0 + SH + 70 + (1 - a) * 20, CREAM, a * 0.9)
    img = put_mask(img, HANDLE, cx, sy0 + SH + 150 + (1 - a) * 20, MINT, a)
    return grade(img, i, t, dur)

# ===================== SOM =====================
TAG_SOM = spaced('SONORIZAÇÃO  ·  HOME THEATER', 30, 9)
def som(i, dur=4.6):
    t = i / FPS
    img = B.bg.copy()
    n = 33; gap = 26; bw = 14
    amp = ease_out(seg(t, 0.2, 0.9)) * (1 - ease_io(seg(t, 1.55, 2.0)))
    lift = ease_io(seg(t, 1.55, 2.0))
    if amp > 0.01:
        m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
        for k in range(n):
            u = (k - (n - 1) / 2) / ((n - 1) / 2)
            env = math.exp(-(u * 1.5) ** 2)
            v = 0.35 + 0.65 * abs(math.sin(t * 7.3 + k * 0.9) * math.sin(t * 3.1 + k * 0.37 + 1))
            hh = 18 + 420 * env * v * amp
            x = cx + (k - (n - 1) / 2) * gap
            d.rounded_rectangle([x - bw / 2, cy - 40 - hh / 2, x + bw / 2, cy - 40 + hh / 2], radius=7, fill=255)
        img = add_glow_mask(img, m, MINT, 0.5, 22)
        ma = np.asarray(m).astype(np.float32) / 255
        img = img * (1 - ma[..., None]) + MINT * ma[..., None]
    # bars collapse into wave line then fade as logo arrives
    if 0 < lift and t < 2.6:
        la = 1 - ease_io(seg(t, 2.1, 2.6))
        img = B.wave_line(img, t, 1.0 - 0.3 * lift, la * lift)
    img = logo_reveal(img, t, 2.0, 3.0, dur=dur)
    a = ease_out(seg(t, 2.7, 3.4))
    img = put_mask(img, TAG_SOM, cx, B.LOGO_Y + B.LH + 70 + (1 - a) * 20, CREAM, a * 0.9)
    img = put_mask(img, HANDLE, cx, B.LOGO_Y + B.LH + 150 + (1 - a) * 20, MINT, a)
    # pulse rings behind logo on beat
    return grade(img, i, t, dur)

# ===================== AUTOMAÇÃO =====================
TAG_AUT = spaced('AUTOMAÇÃO RESIDENCIAL', 30, 9)
BTN_TXT = spaced('CENA  ·  CHEGUEI', 34, 7, FONT_S)
LIGHTS = [(cx - 300, 330, 1.45), (cx, 300, 1.62), (cx + 300, 330, 1.79)]
def automacao(i, dur=4.6):
    t = i / FPS
    on = ease_io(seg(t, 1.4, 2.2))
    img = B.bg.copy() * (0.35 + 0.65 * on)
    # downlights turning on one by one, with cones of warm light
    for (lx, ly, t0) in LIGHTS:
        a = ease_out(seg(t, t0, t0 + 0.25))
        if a <= 0: continue
        dy = (yy - ly).clip(0)
        cone = np.exp(-(((xx - lx) / (28 + dy * 0.2)) ** 2)) * np.exp(-dy / 1300) * (1 - np.exp(-dy / 60))
        img += cone[..., None] * np.array([95, 75, 40], np.float32) * a
        spot = np.exp(-(((xx - lx) / 26) ** 2 + ((yy - ly) / 10) ** 2))
        img += spot[..., None] * np.array([255, 240, 210], np.float32) * a
    # scene button + tap
    ba = ease_out(seg(t, 0.25, 0.8)) * (1 - ease_io(seg(t, 1.55, 2.0)))
    if ba > 0:
        press = math.exp(-((t - 1.2) / 0.08) ** 2)
        BWd, BHd = 520, 120
        by = cy - 40
        m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
        s = 1 - 0.04 * press
        d.rounded_rectangle([cx - BWd / 2 * s, by - BHd / 2 * s, cx + BWd / 2 * s, by + BHd / 2 * s], radius=60, fill=255)
        ma = np.asarray(m).astype(np.float32) / 255 * ba
        fill = np.array([28, 52, 44], np.float32) * (1 - seg(t, 1.2, 1.35)) + MINT * 0.95 * seg(t, 1.2, 1.35)
        img = img * (1 - ma[..., None] * 0.9) + fill * ma[..., None] * 0.9
        bm = Image.new('L', (W, H), 0); d2 = ImageDraw.Draw(bm)
        d2.rounded_rectangle([cx - BWd / 2 * s, by - BHd / 2 * s, cx + BWd / 2 * s, by + BHd / 2 * s], radius=60, outline=255, width=3)
        img = put_mask(img, np.asarray(bm).astype(np.float32)[by - 80:by + 80, :] / 255 if False else np.zeros((1, 1)), cx, 0, MINT, 0)
        bb = np.asarray(bm).astype(np.float32) / 255 * ba
        img = img * (1 - bb[..., None]) + MINT * bb[..., None]
        tc = CREAM * (1 - seg(t, 1.2, 1.35)) + np.array([13, 27, 23], np.float32) * seg(t, 1.2, 1.35)
        img = put_mask(img, BTN_TXT, cx, by - BTN_TXT.shape[0] / 2 + 2, tc, ba)
        # ripple
        rp = seg(t, 1.2, 1.7)
        if 0 < rp < 1:
            rm = Image.new('L', (W, H), 0); d3 = ImageDraw.Draw(rm)
            R = 60 + rp * 520
            d3.ellipse([cx - R, by - R, cx + R, by + R], outline=255, width=4)
            ra = np.asarray(rm).astype(np.float32) / 255 * (1 - rp) * ba
            img = img * (1 - ra[..., None]) + MINT * ra[..., None]
    img = logo_reveal(img, t, 2.0, 3.0, dur=dur)
    a = ease_out(seg(t, 2.7, 3.4))
    img = put_mask(img, TAG_AUT, cx, B.LOGO_Y + B.LH + 70 + (1 - a) * 20, CREAM, a * 0.9)
    img = put_mask(img, HANDLE, cx, B.LOGO_Y + B.LH + 150 + (1 - a) * 20, MINT, a)
    return grade(img, i, t, dur)

# ===================== END CARD =====================
CTA1 = spaced('Projeto personalizado para sua casa', 40, 2, FONT_M)
CTA2 = spaced('SOLICITE SEU ORÇAMENTO', 32, 8, FONT_S)
def endcard(i, dur=3.6):
    t = i / FPS
    img = B.bg.copy()
    img = logo_reveal(img, t, 0.1, 0.9, y=B.LOGO_Y - 120, dur=dur)
    a = ease_out(seg(t, 0.7, 1.3))
    y0 = B.LOGO_Y - 120 + B.LH + 110
    img = put_mask(img, CTA1, cx, y0 + (1 - a) * 20, CREAM, a)
    b = ease_out(seg(t, 1.0, 1.6))
    # pill button
    if b > 0:
        PW, PH = 700, 100; py = y0 + 140
        m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
        d.rounded_rectangle([cx - PW / 2, py, cx + PW / 2, py + PH], radius=50, fill=255)
        ma = np.asarray(m).astype(np.float32) / 255 * b
        img = img * (1 - ma[..., None]) + MINT * ma[..., None]
        img = put_mask(img, CTA2, cx, py + PH / 2 - CTA2.shape[0] / 2 + 2, np.array([13, 27, 23], np.float32), b)
        img = put_mask(img, HANDLE, cx, py + PH + 70, CREAM, b * 0.9)
    img = grade(img, i, t, dur + 10)  # no fade-out at end
    return img

STYLES = {'cinema': (cinema, 4.6), 'som': (som, 4.6), 'automacao': (automacao, 4.6), 'end': (endcard, 3.6)}

if __name__ == '__main__':
    name, mode = sys.argv[1], sys.argv[2]
    fn, dur = STYLES[name]
    if mode == 'stills':
        for tt in map(float, sys.argv[3:]):
            Image.fromarray(fn(int(tt * FPS))).save(f'{name}_{tt:.1f}.jpg', quality=90)
    else:
        out = sys.argv[3]
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                              '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
                              '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
        for i in range(int(dur * FPS)):
            p.stdin.write(fn(i).tobytes())
        p.stdin.close(); sys.exit(p.wait())
