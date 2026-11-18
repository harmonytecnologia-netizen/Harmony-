---
name: cortes-gta6-jpc
description: Usar ao escolher, pedir autorização, editar ou publicar cortes de streamers jogando GTA 6 (ou outros jogos) nos canais da JPC — YouTube Shorts, TikTok e Reels.
---

# Cortes de GTA 6 — JPC (@harmony_computer)

Objetivo: usar a onda do GTA 6 (lançou 19/11/2026, só PS5/Xbox; PC sai depois) para trazer público gamer
para a JPC. O corte é a isca; a JPC aparece como "o canal que comenta e entende de PC".
Regras gerais da JPC: ver `jpc/README.md` e a skill `jpc-gamer`. Nada de MOVE aqui.

## 1. Regra nº 1 — só com autorização (sem exceção)
- Lei 9.610: corte de vídeo alheio precisa de autorização prévia e expressa. Canal com cortes sem
  autorização leva strike/derrubada e pode perder a conta inteira (inclusive o Instagram da JPC).
- Antes de cortar alguém, conferir nesta ordem:
  1. Streamer tem **programa de cortes aberto** (Discord "clipadores/cortes", regra na bio da Twitch/YouTube,
     painel "cortes liberados")? → seguir a regra dele (tag, nome no título, link, forma de envio).
  2. Não tem? → pedir por e-mail comercial → Discord (moderador) → DM, nesta ordem. Modelo no fim.
  3. Sem resposta = NÃO pode. Nunca cortar "e ver se reclama".
- Registrar cada autorização em `jpc/cortes/autorizacoes/<streamer>.md`: print/link da regra ou da resposta,
  data, condições (crédito, link, monetização permitida?, plataformas permitidas).
- Política do streamer muda (ex.: alguns revogaram cortes livres a partir de 01/01/2026): reconferir a cada
  30 dias e antes de cada lote.
- Preferir streamers médios (10 a 200 mil) em português, que jogam GTA 6 ao vivo e topam divulgação.
  Gigantes já têm exército de clipadores; os pequenos demais não têm material.

## 2. Regra nº 2 — transformar (senão não monetiza nem é entregue)
YouTube (conteúdo reutilizado), TikTok e Instagram derrubam alcance e monetização de repost sem nada novo,
**mesmo com autorização**. Todo corte da JPC precisa de, no mínimo, 3 destes:
- Gancho próprio em texto (0–2 s) escrito pela JPC.
- Legenda palavra por palavra (estilo karaokê, Anton/Bangers, amarelo #ffe14f no destaque).
- Comentário da JPC: narração (Piper pt_BR-faber) ou "balão" do mascote JPC reagindo/explicando.
- Contexto/explicação: o que aconteceu, segredo do jogo, curiosidade de Leonida/Vice City.
- Ângulo de PC (o diferencial da JPC): "Que PC roda isso quando sair no PC?", FPS, gráfico, peça.
- Edição que conta história: setup → tensão → virada, zooms, sons, cortes secos.
- Final com pergunta ("você faria o quê?") — nunca "curte e compartilha".
Nunca: marca d'água de outra plataforma, vídeo espelhado/acelerado para "enganar" o Content ID,
música com direitos (só Biblioteca de áudio do YouTube ou trilha própria).

## 3. Achar o momento certo
- Fonte: VOD da Twitch/YouTube do streamer autorizado, clipes oficiais da Twitch dele ou o arquivo bruto que o
  programa de cortes fornece.
- Bons momentos de GTA: fuga da polícia que dá errado, crash/bug engraçado, reação a um gráfico absurdo,
  descoberta de segredo/easter egg, roubo com virada, fala engraçada no chat, primeira vez em lugar famoso.
- Duração: 20–45 s (Shorts/Reels/TikTok). O pico tem que aparecer até o segundo 3 (começar no meio da ação).
- Uma ideia por corte. Se precisar explicar muito, vira vídeo longo de YouTube (compilado comentado, 6–10 min).

## 3b. OpenClip (plugin instalado em 18/11/2026)
- Conta OpenClip criada com Google harmonytecnologia@gmail.com; conector "openclip" conectado no Claude.
- Plano grátis: 0 créditos de corte (achar clipes em vídeo longo exige teste de 3 dias com cartão ou plano pago — NÃO ativar sem o João mandar) e só 2 vídeos legendados por mês.
- Uso: legenda animada em corte já pronto (≤3 min) quando valer a pena; o corte em si continua pelo corte.py (grátis, sem limite).

## 4. Edição (no workspace, com ffmpeg)
- Arquivos brutos: o João (ou Claude pelo navegador do PC) salva em `Documentos\JPC para postar\GTA6\`;
  traz para o workspace com device_stage_files. O workspace não baixa da Twitch/YouTube direto.
- Script: `python3 jpc/scripts/corte.py --entrada bruto.mp4 --inicio 00:12:31 --fim 00:13:05 \
  --gancho "ELE NÃO ESPERAVA ISSO" --credito "@streamer" --layout cam-cima --cam x,y,w,h`
  - layouts: `cam-cima` (webcam em cima 1/3, jogo embaixo 2/3), `jogo-cheio` (jogo cortado no centro, fundo borrado).
  - gera 1080x1920, 30 fps, texto fora dos 250 px de cima e 400 px de baixo, crédito fixo
    "Corte autorizado • @streamer" e cartão final JPC (2 s).
- Legenda: transcrever o áudio (Whisper, se instalado) e conferir os nomes; se não houver transcrição, legendar
  só as falas-chave à mão.
- Comentário da JPC: roteiro de 1–3 frases, narração Piper, áudio do streamer abaixado (-12 dB) enquanto a JPC fala.
- Conferir antes de publicar: assistir 1 vez inteiro, sem cortes de áudio, nome do streamer certo, sem palavrão
  pesado no gancho, sem conteúdo +18 na capa.

## 5. Publicar
- Canais: YouTube "JPC | PC Gamer" (conta Google joaoeinha@gmail.com, canal de marca separado da MOVE),
  TikTok da JPC, Instagram @harmony_computer (Windsor conta 17841445277894628). NUNCA na MOVE.
- Título/legenda: "[gancho] | GTA 6 com @streamer" + 3–5 hashtags (#gta6 #gtavi #gta6brasil #pcgamer #cortes).
- Descrição: crédito + link da live do streamer + "Corte autorizado pelo criador." + chamada da JPC
  ("Quer um PC pronto para o GTA 6 no PC? Manda ORÇAMENTO no Direct do @harmony_computer").
- Ritmo inicial: 1–2 cortes por dia por canal, mesmo corte nas 3 plataformas (é nosso: editado pela JPC).
- No Instagram da JPC, cortes não substituem a grade fixa (feed 12h, carrossel 19h, Reels seg/qua/sex):
  entram como Reel extra, no máximo 1 por dia, para o perfil não virar "canal de cortes".
- Tudo publicado vai para `jpc/historico.md` (plataforma, streamer, link, id).

## 6. Dinheiro (honesto)
- Monetizar o canal com cortes é o caminho mais difícil: só com autorização que permita monetização +
  transformação real. Rotas melhores: campanhas pagas por view do próprio streamer/programa de cortes,
  e levar o público para a JPC (orçamento de PC).
- YouTube: Shorts só conta views de conteúdo original; não criar canal que vive só de cortes sem comentário.

## 7. Modelo de pedido de autorização
> Oi, [nome]! Sou o João, da JPC (@harmony_computer), loja de PC gamer. Curto muito suas lives de GTA 6 e
> queria fazer cortes seus para YouTube Shorts, TikTok e Instagram, sempre com seu nome e o link da sua
> live na descrição e no vídeo. Separei 3 exemplos prontos (link privado): [link]. Posso seguir? Se tiver
> regras (tag, título, monetização), me fala que eu sigo à risca. Valeu!
