"""Efeitos sonoros sintetizados (sem direitos autorais) e trilha de efeitos por tempo.
uso: python3 efeitos_sonoros.py eventos.json duracao saida.wav
eventos.json: [{"t": 1.2, "som": "clique"}, {"t": 3.0, "som": "pop"}, ...]
sons cinematograficos (USAR): impacto, riser(dur), swoosh | antigos (NAO usar em Reel, pedido do Joao 18/11): clique, pop, ding, plim, erro, alarme, whoosh, batida, zumbido(dur)
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
    # --- cinematograficos (pedido do Joao 18/11/2026: nada de plim/clique de joguinho) ---
    elif nome == 'impacto':  # impacto grave de trailer: sub caindo + corpo de ruido abafado + cauda
        n = int(2.2 * SR); t = np.arange(n) / SR
        f = 38 + 70 * np.exp(-t * 7); sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.55)
        nz = rng.normal(0, 1, n); X = np.fft.rfft(nz); fr = np.fft.rfftfreq(n, 1 / SR); X *= 1 / (1 + (fr / 400) ** 2); nz = np.fft.irfft(X, n)
        nz = nz / (np.abs(nz).max() + 1e-9) * env(n, 0.001, 0.12)
        cauda = np.convolve(rng.normal(0, 1, int(0.9 * SR)) * np.exp(-np.arange(int(0.9 * SR)) / SR / 0.35), sub[:4800] * 0.02, 'same')[:n]
        x = sub * 1.0 + nz * 0.55; x[:len(cauda)] += cauda * 0.3
    elif nome == 'riser':  # subida de tensao (dur s) que corta seco na virada
        n = int(dur * SR); t = np.arange(n) / SR; p = t / dur
        nz = rng.normal(0, 1, n); X = np.fft.rfft(nz); fr = np.fft.rfftfreq(n, 1 / SR); X *= np.exp(-fr / 6000); nz = np.fft.irfft(X, n)
        f = 120 * (2 ** (p * 3.2)); ton = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR)
        x = (nz / (np.abs(nz).max() + 1e-9) * 0.6 + ton * 0.35) * p ** 2.2 * np.minimum(1, (dur - t) * 60)
    elif nome == 'swoosh':  # swoosh cinematografico grave e longo (passagem de camera)
        n = int(1.1 * SR); t = np.arange(n) / SR; nz = rng.normal(0, 1, n)
        X = np.fft.rfft(nz); fr = np.fft.rfftfreq(n, 1 / SR); X *= np.exp(-fr / 1400) * (1 - np.exp(-fr / 80)); nz = np.fft.irfft(X, n)
        k = np.exp(-((t - 0.42) / 0.2) ** 2) * (1 + 0.6 * np.sin(2 * np.pi * 3 * t)); x = nz * k
        x = x + 0.25 * np.sin(2 * np.pi * np.cumsum(70 + 40 * np.exp(-((t - 0.42) / 0.2) ** 2)) / SR) * k
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
