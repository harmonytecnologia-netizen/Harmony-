"""Trilha original sintetizada (plano B, sem direitos de terceiros): jazz/soul suave, piano elétrico + baixo + bateria leve.
uso: python3 musica_sintetizada.py saida.wav [bpm] [semente]"""
import sys, numpy as np, wave
SR = 44100
out = sys.argv[1]; BPM = float(sys.argv[2]) if len(sys.argv) > 2 else 86; seed = int(sys.argv[3]) if len(sys.argv) > 3 else 7
rng = np.random.default_rng(seed); beat = 60 / BPM; bars = 16; L = int(SR * beat * 4 * bars) + SR * 3
mix = np.zeros((L, 2))
def midi(n): return 440 * 2 ** ((n - 69) / 12)
def ep(f, dur, vel):  # piano elétrico (FM simples)
    t = np.arange(int(SR * dur)) / SR
    env = np.exp(-t * 2.2) * (1 - np.exp(-t * 200))
    mod = np.sin(2 * np.pi * f * 1.0 * t) * 1.3 * np.exp(-t * 4)
    return vel * env * (np.sin(2 * np.pi * f * t + mod) + 0.25 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 3))
def bass(f, dur, vel):
    t = np.arange(int(SR * dur)) / SR
    env = np.exp(-t * 1.6) * (1 - np.exp(-t * 300))
    return vel * env * (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t))
def kick():
    t = np.arange(int(SR * 0.35)) / SR; f = 50 + 70 * np.exp(-t * 30)
    return 0.9 * np.exp(-t * 9) * np.sin(2 * np.pi * np.cumsum(f) / SR)
def hat(v):
    t = np.arange(int(SR * 0.06)) / SR; n = rng.standard_normal(len(t)); n = np.diff(n, prepend=0)
    return v * np.exp(-t * 70) * n
def snare():
    t = np.arange(int(SR * 0.2)) / SR
    return 0.35 * np.exp(-t * 22) * (rng.standard_normal(len(t)) * 0.7 + np.sin(2 * np.pi * 190 * t))
def add(sig, at, pan=0.0):
    i = int(at * SR); sig = sig[:max(0, L - i)]
    mix[i:i + len(sig), 0] += sig * (1 - pan) ; mix[i:i + len(sig), 1] += sig * (1 + pan)
# Progressão (ii-V-I-vi em Ré bemol, voicings de 9ª)
prog = [([63, 66, 70, 73], 51), ([61, 65, 68, 72], 56), ([60, 65, 68, 72], 49), ([58, 61, 65, 68], 54)]
for b in range(bars):
    ch, root = prog[b % 4]; t0 = b * 4 * beat
    for k, n in enumerate(ch):  # acorde levemente arpejado
        add(ep(midi(n), beat * 3.6, 0.12), t0 + k * 0.018 + (0.0 if b % 2 == 0 else beat * 0.5 * 0), pan=(k - 1.5) * 0.15)
    add(ep(midi(ch[-1] + 12), beat * 1.5, 0.05), t0 + beat * 2.5, pan=0.3)
    for q, off in enumerate([0, 1.5, 2, 3.5]):
        add(bass(midi(root - 12 + (7 if q == 2 else 0)), beat * 1.2, 0.32), t0 + off * beat)
    if b >= 1:
        for q in range(4):
            if q in (0, 2): add(kick(), t0 + q * beat)
            if q in (1, 3): add(snare(), t0 + q * beat, pan=0.05)
        for e in range(8):
            sw = 0.16 * beat if e % 2 else 0  # swing
            add(hat(0.10 if e % 2 else 0.16), t0 + e * beat / 2 + sw, pan=-0.3)
# reverb simples (ruído com decaimento) + saturação suave
ir_t = np.arange(int(SR * 1.6)) / SR; ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 3.2); ir /= np.abs(ir).sum() / 6
for c in range(2):
    wet = np.convolve(mix[:, c], ir)[:L]; mix[:, c] = mix[:, c] + 0.22 * wet
mix = np.tanh(mix * 1.4); mix /= np.abs(mix).max() / 0.89
fade = int(SR * 2.5); mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype('<i2').tobytes())
print('ok', out, round(L / SR, 1), 's')
