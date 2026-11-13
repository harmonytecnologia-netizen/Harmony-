---
name: prompts-video-ia-move
description: Usar ao escrever prompts para gerar vídeos ou imagens com IA (Sora/ChatGPT, Veo/Gemini, Kling, Runway) para Reels, anúncios e tutoriais da MOVE — som, home cinema, automação.
---

# Prompts de vídeo com IA — MOVE
Fontes: guia oficial de prompts do Veo (Google), guias de Sora 2 e de vídeo de produto com Kling (2026). Complementa conteudo-viral-move (roteiro) e edicao-video-move (montagem).

## 1. O que a IA faz bem e o que ainda erra (decidir ANTES de gerar)
- Bem: ambientes de alto padrão, luz acendendo/mudando de cor, cortina abrindo, tela descendo, movimentos de câmera (dolly, drone, travelling), pessoas relaxando no sofá, "momento wow", texturas e clima.
- Erra: detalhes técnicos finos (bornes, cores de fio, terminais, conectores), mãos manipulando objetos pequenos, texto/telas de app (sai ilegível), logotipos, várias ações ao mesmo tempo, física de fios.
- Regra MOVE: cena técnica que ENSINA (ligação de fios, parafuso no borne, configuração no app) = imagem REAL. IA = abertura, resultado, ambientação, "como usar". Vídeo híbrido montado na edição.
- Todo trecho de IA: marcar "Ambiente conceito" / "imagem gerada por IA" quando puder parecer obra real. Nunca apresentar IA como obra feita pela MOVE nem como depoimento.

## 2. Estrutura do prompt (escrever em INGLÊS — os modelos entendem melhor; legenda final em português na edição)
Ordem: [câmera/plano] + [sujeito] + [ação única] + [ambiente] + [luz/clima] + [estilo/lente] + [estabilidade] + [áudio].
- Câmera: "static locked-off shot", "slow dolly-in", "slow push-in", "smooth tracking shot", "overhead top-down shot", "POV first-person", "aerial drone reveal", "low-angle". Lente: "35mm", "50mm", "macro close-up", "shallow depth of field".
- Plano: wide / medium / close-up / extreme close-up.
- Ação: UMA ação principal por clipe, com verbo concreto ("the curtain slowly slides open from left to right", "warm cove lighting fades in from off to on").
- Tempo: clipes de 4–8 s; para sequência, roteiro com marcas ("At 0s… at 3s… at 6s…").
- Luz/clima: "warm 2700K cove lighting", "golden hour sunlight through floor-to-ceiling windows", "dim cinema lighting", "soft diffused daylight".
- Estilo: "photorealistic, cinematic, high-end architectural interior, luxury apartment in Balneário Camboriú with ocean view".
- Estabilidade (positiva, não usar "no/don't"): "objects keep their shape and proportions", "consistent geometry", "natural realistic motion", "stable camera, no flicker".
- Negativo (onde a ferramenta tiver campo próprio, listar sem "no"): "text, watermark, logo, extra fingers, distorted hands, warped furniture, flicker, cartoon".
- Áudio (Sora/Veo geram som): frase separada: "Audio: soft click of a wall switch, quiet hum of a curtain motor, ambient room tone." Música colocamos na edição.
- Formato: 9:16 para Reels/Shorts; 16:9 para YouTube/site.

## 3. Image-to-video = o segredo da precisão
- Usar FOTO REAL como primeiro quadro (foto da obra MOVE, foto oficial do produto, ou imagem conceito já aprovada) e pedir só um movimento sutil: o produto e o ambiente ficam fiéis.
- Foto: alta resolução (≥ 2048 px), fundo limpo, luz difusa, produto centralizado com margem, ângulo combinando com o movimento (frontal para revelação, 3/4 para órbita, de cima para flat lay).
- Movimento baixo/médio para produto premium; alto só para gancho. Se deformar, reduzir movimento e encurtar o clipe.
- Mãos: só entrar/sair do quadro ou tocar um botão grande (keypad). Nada de mão parafusando fio.
- Quadro inicial + quadro final (quando a ferramenta permite): foto da sala apagada → foto da sala acesa = transição perfeita.
- Consistência de personagem/ambiente: mesma imagem de referência em todos os clipes (ex.: Iamin, ver automacao/iamin/FICHA.md), mesma descrição copiada.

## 4. Modelos de prompt MOVE (adaptar)
- Gancho luz: "Static locked-off wide shot of a luxury living room at night, floor-to-ceiling windows with city lights. Warm cove lighting and recessed spots fade in smoothly from off to on in two seconds. Photorealistic, cinematic, 35mm, shallow depth of field, consistent geometry, stable camera. Audio: soft click of a wall switch, quiet room tone. 9:16."
- Cortina: "Slow push-in medium shot of a minimalist bedroom at sunrise. A motorized linen curtain slowly slides open from left to right, revealing the ocean. Soft golden light fills the room. Photorealistic, natural motion, objects keep their shape. Audio: quiet hum of a curtain motor, distant waves."
- Cinema: "Slow dolly-in from behind a leather sofa in a dark home cinema. The lights dim to black and a large screen glows on. Dim cinema lighting, deep blacks, photorealistic. Audio: deep subwoofer rumble starting softly."
- Keypad (image-to-video da foto real do keypad): "Extreme close-up, static camera. A finger gently taps the top button of the wall keypad; its backlight turns on. Keypad keeps exact shape, buttons and engraving unchanged. Soft side light."
- Drone fachada: "Aerial drone reveal shot rising slowly over a modern beach house in Santa Catarina, Brazil, at blue hour, interior lights warm, ocean in background. Photorealistic, smooth motion."
- Iamin dica: usar a imagem aprovada da Iamin como referência + "she smiles and gestures toward the living room; static medium shot; warm interior light".

## 5. Processo de produção
1. Roteiro do vídeo (conteudo-viral-move): marcar quais cenas são REAIS e quais IA.
2. Escrever 2–3 variações de prompt por cena; gerar em baixa resolução/rápido para testar; escolher; gerar a final em 1080p+.
3. Controle de qualidade de cada clipe (assistir quadro a quadro): dedos e mãos, objetos que mudam de forma, texto/logos estranhos, fios e eletrônicos inventados, cintilação, física impossível, marca d'água. Reprovou → refazer ou cortar o trecho.
4. Montar na edição (edicao-video-move): texto em português, legendas, música, sons reais, cor igual entre trechos reais e IA.
5. Legenda/postagem: indicar conteúdo gerado por IA quando a plataforma pedir (Meta/YouTube têm rótulo de IA) e "Ambiente conceito" quando parecer obra real.

## 6. Ferramentas (2026)
- Sora (dentro do ChatGPT do João; acessível pelo navegador do app) — bom em realismo e som.
- Veo 3.x (Gemini / Google Flow) — ótimo com câmera e áudio; aceita imagem inicial.
- Kling — forte em image-to-video de produto, quadro inicial/final, controle de movimento.
- Runway — edição e efeitos.
Gerar quantas variações precisar, mas só publicar o que passou no controle de qualidade.
