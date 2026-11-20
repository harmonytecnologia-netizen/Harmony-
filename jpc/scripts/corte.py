#!/usr/bin/env python3
"""Corte vertical 1080x1920 para Shorts/TikTok/Reels da JPC (cortes autorizados de streamers).

Exemplo:
  python3 jpc/scripts/corte.py --entrada bruto.mp4 --inicio 00:12:31 --fim 00:13:05 \
      --gancho "ELE NAO ESPERAVA ISSO" --credito "@streamer" --layout cam-cima --cam 1500,780,420,300 \
      --saida jpc/cortes/prontos/2026-11-19_streamer_fuga.mp4

Layouts:
  jogo-cheio  jogo cortado no centro ocupando a tela, fundo borrado (padrao)
  cam-cima    webcam (--cam x,y,w,h em pixels do video original) em cima, jogo embaixo
Opcional: --narracao arquivo.wav (comentario da JPC; abaixa o audio do streamer enquanto toca)
          --musica trilha.mp3 (bem baixa, -24 dB)
"""
import argparse, os, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.join(AQUI, "..", "fonts")
ANTON = None
for nome in ("Anton-Regular.ttf", "anton.ttf"):
    p = os.path.join(FONTES, nome)
    if os.path.exists(p):
        ANTON = p
POPPINS = os.path.join(FONTES, "Poppins-Bold.ttf")
if ANTON is None:
    ANTON = POPPINS


def esc(t):
    return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%")


def quebra(t, n=16):
    linhas, atual = [], ""
    for p in t.split():
        if len(atual) + len(p) + 1 > n and atual:
            linhas.append(atual)
            atual = p
        else:
            atual = (atual + " " + p).strip()
    if atual:
        linhas.append(atual)
    return linhas


def segundos(t):
    if t is None:
        return None
    partes = [float(x) for x in str(t).split(":")]
    s = 0.0
    for x in partes:
        s = s * 60 + x
    return s


def ass_tempo(t):
    h = int(t // 3600); m = int(t % 3600 // 60); sec = t % 60
    return f"{h}:{m:02d}:{sec:05.2f}"


def gerar_legenda(arquivo, ini, dur, modelo, destino, corrigir=None):
    """Transcreve so o trecho do corte e escreve .ass com 3 palavras por vez, palavra falada em amarelo."""
    from faster_whisper import WhisperModel
    tmp = destino + ".wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(ini)] + (["-t", str(dur)] if dur else []) +
                   ["-i", arquivo, "-ac", "1", "-ar", "16000", tmp], check=True)
    m = WhisperModel(modelo, device="cpu", compute_type="int8")
    import wave, numpy as np
    with wave.open(tmp) as wf:
        audio = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    segs, _ = m.transcribe(audio, language="pt", word_timestamps=True, vad_filter=True)
    palavras = [w for sgm in segs for w in (sgm.words or [])]
    # --corrigir "ERRADA:CERTA" ou "ERRADA@PROXIMA:CERTA" (so quando a palavra seguinte for PROXIMA)
    textos = [w.word.strip().upper() for w in palavras]
    for regra in (corrigir or []):
        alvo, novo = regra.split(":", 1)
        alvo, prox = (alvo.split("@", 1) + [None])[:2]
        for i, t in enumerate(textos):
            if t.strip(".,!?") == alvo.upper().strip(".,!?") and (prox is None or (i + 1 < len(textos) and textos[i + 1] == prox.upper())):
                textos[i] = novo.upper()
    os.remove(tmp)
    cab = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\n"
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
           "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
           "Style: L,Anton,86,&H00FFFFFF,&H00FFFFFF,&H000F0407,&H64000000,0,0,0,0,100,100,1,0,1,7,2,2,60,60,560,1\n\n"
           "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    linhas = []
    for i in range(0, len(palavras), 3):
        grupo = palavras[i:i + 3]
        for j, w in enumerate(grupo):
            fim = grupo[j + 1].start if j + 1 < len(grupo) else w.end
            txt = " ".join(("{\\c&H4FE1FF&\\fscx112\\fscy112}" + textos[i + k] + "{\\r}") if k == j
                           else textos[i + k] for k, x in enumerate(grupo))
            linhas.append(f"Dialogue: 0,{ass_tempo(w.start)},{ass_tempo(max(fim, w.start + 0.05))},L,,0,0,0,,{txt}")
    with open(destino, "w", encoding="utf-8") as f:
        f.write(cab + "\n".join(linhas) + "\n")
    return len(palavras)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", required=True)
    ap.add_argument("--inicio", default="0")
    ap.add_argument("--fim")
    ap.add_argument("--gancho", required=True)
    ap.add_argument("--credito", required=True, help="@ do streamer (obrigatorio: so cortes autorizados; vai na descricao)")
    ap.add_argument("--credito-no-video", action="store_true", help="mostrar o @ pequeno no canto do video (so se o streamer exigir)")
    ap.add_argument("--layout", default="jogo-cheio", choices=["jogo-cheio", "cam-cima"])
    ap.add_argument("--cam")
    ap.add_argument("--narracao")
    ap.add_argument("--musica")
    ap.add_argument("--final", default="Quer um PC pra rodar isso? Manda ORÇAMENTO no @harmony_computer")
    ap.add_argument("--legenda", action="store_true", help="legenda automatica palavra por palavra (Whisper local, gratis)")
    ap.add_argument("--modelo", default="small", help="modelo Whisper: base/small/medium")
    ap.add_argument("--saida", default="corte.mp4")
    ap.add_argument("--corrigir", nargs="*", default=[], help='corrige palavras da legenda: "ERRADA:CERTA" ou "ERRADA@PROXIMA:CERTA"')
    a = ap.parse_args()

    ini, fim = segundos(a.inicio), segundos(a.fim)
    dur = (fim - ini) if fim else None
    if dur is not None and not (5 <= dur <= 90):
        sys.exit("Corte deve ter entre 5 e 90 s (ideal 20-45 s).")

    entradas = ["-ss", str(ini)] + (["-t", str(dur)] if dur else []) + ["-i", a.entrada]
    if a.layout == "cam-cima":
        if not a.cam:
            sys.exit("--layout cam-cima precisa de --cam x,y,w,h")
        x, y, w, h = [int(v) for v in a.cam.split(",")]
        v = (f"[0:v]split=2[g][c];"
             f"[c]crop={w}:{h}:{x}:{y},scale=1080:640:force_original_aspect_ratio=increase,crop=1080:640[cam];"
             f"[g]scale=-2:1280,crop=1080:1280[jogo];"
             f"[cam][jogo]vstack=inputs=2,setsar=1,fps=30[base]")
    else:
        v = ("[0:v]split=2[a][b];"
             "[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,eq=brightness=-0.15[fundo];"
             "[b]scale=1080:-2,scale='min(1080,iw)':-2[frente];"
             "[fundo][frente]overlay=(W-w)/2:(H-h)/2,setsar=1,fps=30[base]")

    # gancho (0-3 s), credito fixo, cartao final
    txt = "[base]"
    filtros = [v]
    y0 = 300
    for i, linha in enumerate(quebra(a.gancho.upper())):
        filtros.append(
            f"{txt}drawtext=fontfile='{ANTON}':text='{esc(linha)}':fontsize=92:fontcolor=#ffe14f:"
            f"borderw=6:bordercolor=#07040f:x=(w-tw)/2:y={y0 + i*105}:enable='lt(t,3.2)'[g{i}]")
        txt = f"[g{i}]"
    # credito discreto: pequeno, semitransparente, canto direito na emenda cam/jogo (ou acima da area de botoes)
    if not a.credito_no_video:
        filtros.append(f"{txt}null[cr]")
    y_cr = 600 if a.layout == "cam-cima" else "h-430"
    if a.credito_no_video:
      filtros.append(
        f"{txt}drawtext=fontfile='{POPPINS}':text='{esc(a.credito)}':fontsize=28:"
        f"fontcolor=white@0.85:box=1:boxcolor=#07040f@0.45:boxborderw=8:x=w-tw-40:y={y_cr}[cr]")
    txt = "[cr]"
    if dur:
        for i, linha in enumerate(quebra(a.final, 22)):
            filtros.append(
                f"{txt}drawtext=fontfile='{POPPINS}':text='{esc(linha)}':fontsize=58:fontcolor=white:"
                f"borderw=5:bordercolor=#07040f:x=(w-tw)/2:y={820 + i*80}:enable='gt(t,{dur-2.5:.2f})'[f{i}]")
            txt = f"[f{i}]"
    if a.legenda:
        ass = os.path.abspath(a.saida) + ".ass"
        n_pal = gerar_legenda(a.entrada, ini, dur, a.modelo, ass, a.corrigir)
        print(f"legenda: {n_pal} palavras")
        filtros.append(f"{txt}subtitles='{ass}':fontsdir='{FONTES}'[leg]")
        txt = "[leg]"
    filtros.append(f"{txt}null[vout]")

    # audio
    extra, n = [], 1
    aud = "[0:a]aresample=48000,loudnorm=I=-14:TP=-1.5[orig]"
    mix = ["[orig]"]
    if a.narracao:
        extra += ["-i", a.narracao]
        aud += f";[{n}:a]aresample=48000,volume=1.6,asplit=2[narr][sc]"
        aud += ";[orig][sc]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=300[duck]"
        mix = ["[duck]", "[narr]"]
        n += 1
    if a.musica:
        extra += ["-stream_loop", "-1", "-i", a.musica]
        aud += f";[{n}:a]aresample=48000,volume=-24dB[mus]"
        mix.append("[mus]")
        n += 1
    aud += f";{''.join(mix)}amix=inputs={len(mix)}:duration=first:normalize=0[aout]" if len(mix) > 1 else ";[orig]anull[aout]"

    cmd = (["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + entradas + extra +
           ["-filter_complex", ";".join(filtros) + ";" + aud, "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart"] + (["-t", str(dur)] if dur else []) + [a.saida])
    os.makedirs(os.path.dirname(os.path.abspath(a.saida)), exist_ok=True)
    subprocess.run(cmd, check=True)
    print(a.saida)


if __name__ == "__main__":
    main()
