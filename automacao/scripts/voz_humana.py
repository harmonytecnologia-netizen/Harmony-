#!/usr/bin/env python3
"""Tratamento da voz da Iamin para soar mais humana (pedido do João, 25/11/2026).

Uso:  python3 voz_humana.py entrada.mp3 saida.wav [velocidade]
      velocidade padrão 1.0 (NÃO acelerar acima de 1.03: deixa robótico)

O que faz (substitui o antigo "silenceremove 0,22 s + atempo 1.07", que cortava
os respiros e acelerava a fala, deixando a voz picotada e com cara de robô):
  1. corta só o silêncio do começo e do fim;
  2. pausas longas viram respiros naturais de ~0,3 s (não somem);
  3. EQ de locução: tira ronco (<80 Hz), corpo em 200 Hz, presença em 3 kHz;
  4. de-esser (o "S" chiado das vozes de TTS);
  5. compressor suave (volume constante, como locutor);
  6. ambiência de sala bem leve (tira o "seco de robô");
  7. volume final -16 LUFS (padrão de Reels).
"""
import subprocess
import sys


def tratar(entrada, saida, velocidade=1.0):
    vel = max(0.9, min(float(velocidade), 1.03))
    filtros = ",".join([
        # 1 e 2: silêncio das pontas fora; pausas > 0,45 s reduzidas a 0,3 s
        "silenceremove=start_periods=1:start_threshold=-45dB:start_duration=0.05",
        "areverse",
        "silenceremove=start_periods=1:start_threshold=-45dB:start_duration=0.05",
        "areverse",
        "silenceremove=stop_periods=-1:stop_duration=0.45:stop_threshold=-45dB:stop_silence=0.3",
        f"atempo={vel}",
        # 3: EQ de locução
        "highpass=f=80",
        "equalizer=f=200:t=q:w=1:g=1.5",
        "equalizer=f=3000:t=q:w=1.2:g=2",
        "equalizer=f=9000:t=q:w=1:g=-1.5",
        # 4: de-esser
        "deesser=i=0.4:m=0.5:f=0.5",
        # 5: compressor suave
        "acompressor=threshold=-20dB:ratio=3:attack=10:release=150:makeup=2",
        # 6: ambiência leve
        "aecho=0.9:0.6:22|37:0.10|0.06",
        # 7: volume final
        "loudnorm=I=-16:TP=-1.5:LRA=7",
        "aresample=48000",
    ])
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", entrada,
                    "-af", filtros, "-ac", "1", saida], check=True)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    tratar(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 1.0)
    print("ok:", sys.argv[2])
