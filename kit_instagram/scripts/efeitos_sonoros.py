"""Efeitos sonoros sintetizados (sem direitos autorais) e trilha de efeitos por tempo.
uso: python3 efeitos_sonoros.py eventos.json duracao saida.wav
eventos.json: [{"t": 1.2, "som": "clique"}, {"t": 3.0, "som": "pop"}, ...]
sons: clique, pop, ding, erro, alarme, whoosh, plim, batida, zumbido(dur)
"""
import json, sys, wave
import numpy as np
SR = 48000

def env(n, a=0.002, r=0.08):
    t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / r)

def som(nome, dur=1.0):
    rng = np.random.default_rng(len(nome))
    if nome == 'clique':
        n = int(0.05 * SR); x = rng.normal(0, 1, n) * env(n, 0.0005, 0.006) + np.sin(2 * np.pi * 2400 * np.arange(n) / SR) * env(n, 0.0005, 0.01) * 0.6
    elif nome == 'pop':
        n = int(0.18 * SR); t = np.arange(n) / SR; f = 900 * np.exp(-t * 18) + 180; x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.05)
    elif nome in ('ding', 'plim'):
        n = int(1.2 * SR); t = np.arange(n) / SR; base = 1320 if nome == 'ding' else 1760
        x = (np.sin(2 * np.pi * base * t) + 0.4 * np.sin(2 * np.pi * base * 2.01 * t) + 0.2 * np.sin(2 * np.pi * base * 3.02 * t)) * env(n, 0.002, 0.35) * 0.5
    elif nome == 'erro':
        n = int(0.5 * SR); t = np.arange(n) / SR; x = np.sign(np.sin(2 * np.pi * 140 * t)) * 0.35 * env(n, 0.005, 0.25)
    elif nome == 'alarme':
        n = int(1.2 * SR); t = np.arange(n) / SR; f = np.where((t * 4).astype(int) % 2 == 0, 880, 660)
        x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.35 * np.minimum(1, (1.2 - t) * 5)
    elif nome == 'whoosh':
        n = int(0.6 * SR); t = np.arange(n) / SR; x = rng.normal(0, 1, n)
        k = np.exp(-((t - 0.3) / 0.13) ** 2); X = np.fft.rfft(x); fr = np.fft.rfftfreq(n, 1 / SR); X *= np.exp(-fr / 2500); x = np.fft.irfft(X, n) * k * 3
    elif nome == 'batida':
        n = int(0.4 * SR); t = np.arange(n) / SR; f = 120 * np.exp(-t * 10) + 45; x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.12)
    elif nome == 'zumbido':
        n = int(dur * SR); t = np.arange(n) / SR; x = (np.sin(2 * np.pi * 60 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)) * 0.12 * np.minimum(1, np.minimum(t, dur - t) * 4)
    else:
        raise SystemExit('som desconhecido: ' + nome)
    return x / (np.abs(x).max() + 1e-9) * 0.8

def main(ev_path, dur, out):
    dur = float(dur); mix = np.zeros(int(dur * SR) + SR)
    for e in json.load(open(ev_path)):
        s = som(e['som'], e.get('dur', 1.0)) * e.get('vol', 1.0); i = int(e['t'] * SR); mix[i:i + len(s)] += s[:len(mix) - i]
    mix = mix[:int(dur * SR)]; mix = mix / max(1, np.abs(mix).max() / 0.95)
    st = np.repeat((mix * 32767).astype(np.int16)[:, None], 2, axis=1)
    with wave.open(out, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
    print('ok', out)

if __name__ == '__main__':
    main(*sys.argv[1:4])
