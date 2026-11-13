---
name: edicao-video-move
description: Usar ao editar, tratar som, colorir, legendar ou exportar vídeos da MOVE (Reels, anúncios, YouTube) — seja editando aqui com ffmpeg/Python ou orientando o João no CapCut/Premiere.
---

# Edição de vídeo — MOVE
Base: curso "Edição de vídeos com Adobe Premiere PRO 2026" (Creators Academy, 20 aulas; transcrições em automacao/cursos/) + manual conteudo-viral-move (gancho, ritmo, roteiro). Aqui = COMO executar.

## 1. Fluxo de trabalho (ordem do curso)
1. Organizar: pasta por vídeo com subpastas 01_brutos, 02_audio, 03_musica, 04_graficos, 05_export. Nomear arquivos com número/cena.
2. Specs: Reels/Shorts/TikTok = 1080x1920 (9:16); YouTube = 1920x1080. Gravar 30 fps normal; 60/120 fps só nas cenas que vão virar câmera lenta (menos de 60 fps em câmera lenta trava).
3. Cortes principais (corte seco). Corte seco é a transição nº 1 — vídeos institucionais bons quase só usam corte seco.
4. Zoom/movimento com keyframes, sempre com suavização (ease in/out). Movimento linear parece robótico.
5. Correção de cor (básica) numa "camada de ajuste" única por cima de tudo, para ficar igual em todas as cenas.
6. Tratamento de áudio.
7. Legendas.
8. Exportar e REVISAR no celular antes de postar (cor e som mudam de tela para tela).

## 2. Transições (só 3 tipos importam)
- Corte seco (99% das vezes).
- Transição de efeito (deslizar, abertura…): pouco, só quando combina com o tema. Para a MOVE: no máximo um "whip"/desfoque de movimento entre ambientes.
- Transição de zoom (punch-in): zoom rápido para destacar algo (botão do app, tela descendo) e volta. Keyframes perto um do outro = zoom rápido; aplicar ease.
- Zoom lento contínuo (ex.: 100%→108% em toda a cena) cria tensão/sofisticação, linguagem de cinema. Ótimo para home cinema e fachada.

## 3. Velocidade (time remapping / speed ramp)
- Rápido → câmera lenta no momento "wow" (luz acende, cortina abre) → rápido. Transições de velocidade com curva suave.
- Exige captação em 60 fps+ no trecho lento.

## 4. Som = 80% da qualidade percebida
- Prioridade de investimento: microfone (lapela sem fio) antes de câmera.
- Ordem: reduzir ruído (ar-condicionado, obra, rua) → controlar o "S" (de-esser) → equalização de voz (preset "podcast" no Premiere funciona bem) → volume final.
- Criar preset e usar o mesmo em todos os vídeos (consistência).
- Música abaixo da voz (ducking). Efeitos sonoros reais: clique do interruptor, motor da cortina, "whoosh".

## 5. Cor
- Objetivo é sentimento, não "deixar bonito": MOVE = quente/acolhedor nos ambientes + pretos profundos (cinema); azul transmite confiança.
- Fazer só correção básica (temperatura, exposição, brancos/pretos, saturação) e às vezes curvas. Temperatura no máximo +15/+20. Exagerar estraga fácil.
- Olhar o waveform: nada encostando no teto (branco estourado) nem no chão (preto sem detalhe).
- Nitidez leve só no final, sem exagero.
- Conferir no celular (iPhone/Samsung mostram diferente; Samsung costuma saturar mais).

## 6. Texto, gráficos e máscaras
- Texto curto, fonte da marca (Archivo/Manrope), dentro da área segura (fora dos 250 px de cima e 400 px de baixo no 9:16).
- Animação de texto com keyframes + ease (entra suave, sai suave). Gráficos simples prontos (templates) aceleram.
- Máscara + desfoque: borrar placas, rostos de terceiros, endereço, telas com dados do cliente. Sempre que filmar casa de cliente, revisar isso.

## 7. Legendas
- Gerar automático (Premiere "Transcrever" com IA, ou CapCut "Legendas automáticas") e REVISAR erros.
- Reels: legenda queimada no vídeo, grande, 2–4 palavras por vez. YouTube: arquivo .srt separado.

## 8. Exportar
- H.264, áudio AAC 48 kHz 320 kbps.
- YouTube: 1440p (16–24 Mbps VBR 2 passagens) ou 4K; mínimo 1080p. Nome do arquivo = título do vídeo (ajuda SEO).
- Reels/TikTok: 1080x1920, 30 fps, ~10–16 Mbps. Exportar 4K para o Instagram não ajuda (ele recomprime).
- Salvar preset de exportação. Exportar um trecho de teste antes do vídeo inteiro.

## 9. Equivalentes aqui no workspace (ffmpeg)
- Zoom lento: `zoompan=z='min(zoom+0.0006,1.08)':d=N:s=1080x1920:fps=30` (ou scale+crop com expressão suavizada).
- Punch-in rápido: duas versões do trecho (normal e crop 115%) cortadas no beat, ou zoompan com easing (smoothstep).
- Speed ramp: dividir em trechos e usar `setpts=0.5*PTS` (rápido) / `setpts=2*PTS` (lento, só de fonte 60 fps), depois concat; `minterpolate` só como último recurso.
- Som: `highpass=f=80,afftdn=nf=-25,deesser,acompressor,loudnorm=I=-14:TP=-1.5:LRA=11`; música com `sidechaincompress` para abaixar sob a voz.
- Cor: `eq=contrast=1.06:saturation=1.08:gamma=0.98,colortemperature=temperature=5800` ou `lut3d=arquivo.cube`; checar com filtro `waveform`.
- Desfoque de área: `split` → `crop` → `boxblur=20` → `overlay` na posição.
- Legenda queimada: arquivo .ass com estilo da marca + `subtitles=leg.ass`.
- Saída Reels: `-c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -r 30 -c:a aac -b:a 320k -ar 48000 -movflags +faststart`.
- Seguir também a skill video-making (renderizar por cena, concat sem reencodar).

## 10. Para o João (CapCut grátis faz quase tudo do curso)
- Keyframe (losango) = zoom/movimento; "Curva de velocidade" = speed ramp; "Reduzir ruído" e "Aprimorar voz" = tratamento de áudio; "Ajustar" = cor; "Legendas automáticas"; "Máscara" + "Desfocar".
- Premiere é pago (Creative Cloud); só vale se for editar muito vídeo longo.
