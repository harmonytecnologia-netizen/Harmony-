"""Troca a trilha e os efeitos de um Reel ja montado, sem mexer na imagem.
uso: python3 remixar_trilha.py config.json
config: {
  "video": "reel.mp4",               (imagem copiada sem recodificar)
  "saida": "reel_novo.mp4",
  "falas": [{"arquivo": "voz.wav", "t": 0.2}],   (opcional; narracao por cima)
  "musica": "faixa.mp3", "musica_inicio": null,  (null = escolhe o trecho mais forte)
  "efeitos": [{"t": 0.0, "som": "impacto", "vol": 0.6}, {"t": 6.2, "som": "riser", "dur": 1.2}],
  "duck_db": 14, "lufs": -14 }
Regras (pedido do Joao 18/11/2026): musica real e chamativa; poucos efeitos e so cinematograficos
(impacto, riser, swoosh); musica abaixa 14 dB sob a voz; loudness final -14 LUFS.
"""
import json, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../kit_instagram/scripts'))
from efeitos_sonoros import som
SR = 48000


def dec(p, ch, ss=0.0, t=None):
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(ss), '-i', p] + (['-t', str(t)] if t else []) + ['-f', 'f32le', '-ac', str(ch), '-ar', str(SR), '-']
    a = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32)
    return a.reshape(-1, ch) if ch > 1 else a


def dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)


def rms_blocks(x, b):
    n = len(x) // b
    return np.sqrt((x[:n * b].reshape(n, b) ** 2).mean(1) + 1e-12)


def suavizar(g, a_ms, r_ms):
    a = 1 - np.exp(-1 / (SR * a_ms / 1000)); r = 1 - np.exp(-1 / (SR * r_ms / 1000))
    out = np.empty_like(g); y = g[0]
    for i, v in enumerate(g):  # loop em numpy puro e lento; roda em blocos de 10 ms
        y += (a if v < y else r) * (v - y); out[i] = y
    return out


def main(cfg_path):
    cfg = json.load(open(cfg_path, encoding='utf-8'))
    base = os.path.dirname(os.path.abspath(cfg_path)); P = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    video = P(cfg['video']); D = dur(video); N = int(D * SR)
    # narracao
    voz = np.zeros(N, np.float32)
    for f in cfg.get('falas', []):
        a = dec(P(f['arquivo']), 1); i = int(f['t'] * SR); voz[i:i + len(a)] += a[:N - i]
    tem_voz = np.abs(voz).max() > 1e-4
    # musica: trecho mais forte (gancho) se nao informado
    mus_p = P(cfg['musica']); md = dur(mus_p); ini = cfg.get('musica_inicio')
    if ini is None:
        full = dec(mus_p, 1); r = rms_blocks(full, SR // 2); w = int(D * 2); best, ini = -1, 0.0
        for s in range(0, max(1, min(len(r) - w, 180))):
            sc = r[s:s + 6].mean() * 1.5 + r[s:s + w].mean() - 0.6 * r[s:s + w].std()  # gancho forte e trecho estavel
            if sc > best: best, ini = sc, s / 2
    mus = dec(mus_p, 2, ini, D + 0.5)[:N]
    mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
    fi = int(0.12 * SR); fo = int(1.6 * SR)
    mus[:fi] *= np.linspace(0, 1, fi)[:, None]; mus[-fo:] *= np.linspace(1, 0, fo)[:, None]
    rm = np.sqrt((mus ** 2).mean() + 1e-12)
    # ducking: -duck_db onde ha voz (envelope de 10 ms, abre 60 ms antes)
    if tem_voz:
        rv = np.sqrt((voz[np.abs(voz) > 0.01 * np.abs(voz).max()] ** 2).mean())
        mus *= (rv * 0.95) / rm  # musica no nivel da voz quando a voz para
        b = SR // 100; e = rms_blocks(voz, b); ativo = (e > rv * 0.12).astype(float)
        k = int(0.35 / 0.01); ativo = np.convolve(ativo, np.ones(k), 'same') > 0  # segura nas pausas curtas
        ativo = np.roll(ativo, -6)
        g = np.where(ativo, 10 ** (-cfg.get('duck_db', 14) / 20), 1.0)
        g = suavizar(g, 60, 350); g = np.repeat(g, b); g = np.pad(g, (0, max(0, N - len(g))), constant_values=g[-1])[:N]
        mus *= g[:, None]
    else:
        mus *= 0.3 / rm
    # efeitos
    fx = np.zeros(N)
    for ev in cfg.get('efeitos', []):
        s = som(ev['som'], ev.get('dur', 1.0)) * ev.get('vol', 0.5); i = int(ev['t'] * SR); fx[i:i + len(s)] += s[:N - i]
    ref = rv if tem_voz else 0.3
    fx *= ref * 2.2  # efeitos abaixo da voz
    mix = mus + voz[:, None] + fx[:, None]
    raw = P(cfg['saida']) + '.raw'
    with open(raw, 'wb') as fh: fh.write(mix.astype(np.float32).tobytes())
    L = cfg.get('lufs', -14)
    m = subprocess.run(['ffmpeg', '-hide_banner', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', raw, '-af', f'loudnorm=I={L}:TP=-1.0:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
    j = json.loads(m[m.rfind('{'):m.rfind('}') + 1])
    ln = f"volume={L - float(j['input_i']):.2f}dB,alimiter=limit=0.89:level=false"  # ganho exato ate -14 LUFS + teto -1 dBTP
    out = P(cfg['saida']); tmpv = out + '.tmp.mp4'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', video, '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', raw, '-filter_complex', f'[1:a]{ln},aresample=48000[a]',
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-t', f'{D}', '-movflags', '+faststart', tmpv], check=True)
    os.replace(tmpv, out); os.remove(raw)
    print(f'ok {out} ({D:.2f}s) musica {os.path.basename(mus_p)} a partir de {ini:.1f}s')


if __name__ == '__main__':
    main(sys.argv[1])
