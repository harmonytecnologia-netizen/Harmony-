import sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
DUR = 4.4
N = int(DUR * FPS)
LOGO = '/mnt/user-data/uploads/Logo_MOVE_com_automação_e_segurança.png'
FONT = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
MINT = np.array([84, 223, 174], np.float32)

def ease_out(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def ease_io(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
def seg(t, a, b): return min(max((t - a) / (b - a), 0), 1)

# ---------- static layers ----------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
cx, cy = W / 2, H / 2
r = np.sqrt(((xx - cx) / W) ** 2 + ((yy - cy) / H * 0.9) ** 2)
bg = np.zeros((H, W, 3), np.float32)
center = np.array([22, 42, 35], np.float32); edge = np.array([7, 15, 13], np.float32)
k = np.clip(r / 0.62, 0, 1)[..., None] ** 1.4
bg = center * (1 - k) + edge * k
vign = (1 - np.clip((r - 0.32) / 0.45, 0, 1) ** 1.8 * 0.55)[..., None]

logo = Image.open(LOGO).convert('RGBA')
bbox = logo.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
logo = logo.crop(bbox)
LW = 900
LH = round(logo.height * LW / logo.width)
logo = logo.resize((LW, LH), Image.LANCZOS)
logo_np = np.asarray(logo).astype(np.float32) / 255.0
LOGO_Y = int(cy - LH / 2 - 40)

# handle text
font = ImageFont.truetype(FONT, 34)
txt = '@move.s.a'
spaced_w = sum(font.getlength(c) for c in txt) + 8 * (len(txt) - 1)
tl = Image.new('L', (int(spaced_w) + 20, 60), 0)
d = ImageDraw.Draw(tl); x = 10
for c in txt:
    d.text((x, 8), c, font=font, fill=255); x += font.getlength(c) + 8
tl_np = np.asarray(tl).astype(np.float32) / 255.0
TXT_Y = LOGO_Y + LH + 120

rng = np.random.default_rng(7)
grain_bank = [rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32) for _ in range(8)]

def wave_line(img, t, progress, alpha):
    """mint wave drawn from center outward"""
    if alpha <= 0 or progress <= 0: return img
    pil = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(pil)
    half = progress * (W * 0.42)
    pts = []
    for i in range(121):
        u = -1 + 2 * i / 120
        x = cx + u * half
        y = cy - 40 + math.sin(u * 2.6 + t * 2.0) * 38 * progress * (1 - abs(u) ** 2)
        pts.append((x, y))
    d.line(pts, fill=255, width=6, joint='curve')
    glow = pil.filter(ImageFilter.GaussianBlur(18))
    m = np.asarray(pil).astype(np.float32) / 255 * alpha
    g = np.asarray(glow).astype(np.float32) / 255 * alpha * 1.4
    img = img + MINT * g[..., None] * 0.55
    img = img * (1 - m[..., None]) + MINT * m[..., None]
    return img

def paste(img, src_rgba, x0, y0, opacity, mask_cols=None, scale=1.0):
    if opacity <= 0: return img
    s = src_rgba
    if scale != 1.0:
        p = Image.fromarray((s * 255).astype(np.uint8), 'RGBA')
        p = p.resize((round(p.width * scale), round(p.height * scale)), Image.LANCZOS)
        s = np.asarray(p).astype(np.float32) / 255
        x0 -= (s.shape[1] - src_rgba.shape[1]) // 2
        y0 -= (s.shape[0] - src_rgba.shape[0]) // 2
    h, w = s.shape[:2]
    a = s[..., 3] * opacity
    if mask_cols is not None:
        a = a * mask_cols(w)[None, :]
    region = img[y0:y0 + h, x0:x0 + w]
    img[y0:y0 + h, x0:x0 + w] = region * (1 - a[..., None]) + s[..., :3] * 255 * a[..., None]
    return img

def frame(i):
    t = i / FPS
    img = bg.copy()
    # slow light drift (vintage warm leak, top-right)
    lx = W * (0.85 - 0.1 * t / DUR); ly = H * 0.12
    leak = np.exp(-(((xx - lx) / 520) ** 2 + ((yy - ly) / 620) ** 2))
    img += leak[..., None] * np.array([38, 22, 6], np.float32) * (0.6 + 0.4 * math.sin(t * 1.3))

    # 1) wave line draws out (0.15-1.0), fades as logo arrives (1.1-1.7)
    lp = ease_out(seg(t, 0.15, 1.0))
    la = 1 - ease_io(seg(t, 1.15, 1.75))
    img = wave_line(img, t, lp, la)

    # 2) logo reveal: soft left->right wipe + settle scale
    rv = ease_out(seg(t, 0.95, 2.05))
    if rv > 0:
        def mask(w, rv=rv):
            edge_x = -0.15 + rv * 1.3
            u = np.linspace(0, 1, w)
            return np.clip((edge_x - u) / 0.15, 0, 1)
        push = 1.0 + 0.025 * ease_io(seg(t, 2.0, DUR))
        sc = (1.06 - 0.06 * rv) * push
        img = paste(img, logo_np, int(cx - LW / 2), LOGO_Y, min(1, rv * 1.4), mask, sc)
        # sheen sweeping across logo once
        sh = seg(t, 2.0, 2.9)
        if 0 < sh < 1:
            band_x = cx - LW / 2 - 200 + sh * (LW + 400)
            band = np.exp(-((xx[LOGO_Y:LOGO_Y + LH] - band_x - (yy[LOGO_Y:LOGO_Y + LH] - LOGO_Y) * 0.5) / 60) ** 2)
            la_ = np.zeros((LH, W), np.float32)
            la_[:, int(cx - LW / 2):int(cx - LW / 2) + LW] = logo_np[..., 3]
            img[LOGO_Y:LOGO_Y + LH] += (band * la_)[..., None] * 70

    # 3) handle + divider
    ta = ease_out(seg(t, 2.1, 2.9))
    if ta > 0:
        dy = int((1 - ta) * 24)
        dw = int(120 * ta)
        y = TXT_Y - 40
        img[y:y + 3, int(cx - dw):int(cx + dw)] = img[y:y + 3, int(cx - dw):int(cx + dw)] * (1 - ta) + MINT * ta
        th, tw = tl_np.shape
        x0 = int(cx - tw / 2); y0 = TXT_Y + dy
        a = tl_np * ta * 0.92
        col = np.array([242, 245, 239], np.float32)
        img[y0:y0 + th, x0:x0 + tw] = img[y0:y0 + th, x0:x0 + tw] * (1 - a[..., None]) + col * a[..., None]

    # vintage grade: warm, lifted blacks, vignette, grain, subtle flicker
    img = img * vign
    img = img * np.array([1.04, 1.0, 0.92], np.float32) + np.array([6, 5, 2], np.float32)
    flick = 1 + 0.012 * math.sin(t * 37) * math.sin(t * 13)
    img *= flick
    g = grain_bank[i % len(grain_bank)]
    g = np.repeat(np.repeat(g, 2, 0), 2, 1)
    img += g[..., None] * 5.5

    # fade in / out
    fin = ease_io(seg(t, 0, 0.35)); fout = 1 - ease_io(seg(t, DUR - 0.45, DUR))
    img *= fin * fout
    return np.clip(img, 0, 255).astype(np.uint8)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'stills':
        for tt in map(float, sys.argv[2:]):
            Image.fromarray(frame(int(tt * FPS))).save(f'still_{tt:.1f}.jpg', quality=90)
    else:
        out = sys.argv[2]
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                              '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast',
                              '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
        for i in range(N):
            p.stdin.write(frame(i).tobytes())
        p.stdin.close(); sys.exit(p.wait())
