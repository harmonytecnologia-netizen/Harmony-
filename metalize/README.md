# METALIZE — Instagram @metalize.metalurgica (automação)

Branch `metalize`, pasta `metalize/`. Conta no Windsor.ai: **17841449079341071**. NUNCA publicar conteúdo da Metalize na MOVE (17841461939593135) nem na JPC (17841445277894628), e nunca o contrário.

## Empresa (só fatos confirmados pelo João)
- Metalize Metalúrgica, Marcelândia (MT). Atende também Cláudia, União do Sul, Atlântica e Itaúba (confirmado pelo João em 24/11/2026). Residencial, comercial e industrial. Orçamento: WhatsApp (66) 99632-0774.
- Serviços: calhas e rufos; portões residenciais e comerciais; galpões e estruturas metálicas; coberturas metálicas; escadas metálicas; corrimãos; pilares e outras estruturas sob medida.
- **A confirmar com o João** (não afirmar até ele confirmar): anos de mercado, obras feitas, equipe, se faz pintura eletrostática, se trabalha com inox/vidro/cobre, garantia, se faz visita técnica gratuita.
- **Nunca inventar** avaliações, certificações, números, obras ou depoimentos. Imagens 3D/IA sempre com "Imagem ilustrativa." na arte e na legenda.

## Dois públicos
1. Alto padrão (proprietários, empresários, fazendeiros, construtores, arquitetos, engenheiros): valor, acabamento, durabilidade, segurança, design. Nunca falar de preço baixo.
2. Quem está aprendendo metalurgia (soldadores, serralheiros, estudantes): dicas práticas que dão vontade de salvar e compartilhar.

## Identidade visual
Preto, **amarelo da logomarca #FBCF0E**, branco, cinza grafite, metal discreto. Premium e minimalista: título Inter Bold, texto Inter Light, muito espaço, nada de panfleto. Feed 4:5 (1080x1350), stories e Reels 9:16.
- `logo.png` = logo original (MTZ amarelo + METALIZE branco), recortado da imagem enviada pelo João em 24/11/2026. Amarelo da marca #FBCF0E. Títulos em Inter Bold (combina com o logo).
- Fundos 3D: `fundos/3d_*.jpg`, gerados por `animacoes/fundos3d.py <cena> <saida>` (calha, portao, escada, pergolado, chapa). Criar cenas novas aos poucos (galpão, cobertura, rufo, corrimão, pilar) para não repetir fundo.
- Fotos reais do João têm prioridade sobre 3D: Google Drive, pasta **"Metalize para postar"** (e, com o PC ligado, `Documentos\Metalize para postar`). Foto real nova → usar em feed/stories com o mesmo layout e registrar em `banco/reais.json`.

## FREQUÊNCIA OBRIGATÓRIA (pedido do João, 24/11/2026)
- **09h:** 3 stories próprios.
- **15h:** 3 stories próprios.
- **20h:** 1 story (pergunta ou convite) + nos dias de post, o post e o story dele.
- **3 posts por semana, às 20h:** segunda = Reel "Metalize Explica 3D" (se não houver Reel pronto, feed); quarta = carrossel; sexta = feed.

## Produção
- `python3 metalize/scripts/produzir.py [--dias 4] [--data AAAA-MM-DD] [--forcar]` gera `fila/AAAA-MM-DD/plano.json` + artes, a partir de `banco/pautas.json` (ids usados em `banco/usados.json`). A fila deve ter sempre hoje + 3 dias.
- Banco: ao acrescentar pautas, conferir fatos técnicos (WebSearch) e citar norma só com certeza. Tipos de story: curiosidade, aprendiz, detalhe, pergunta, cta. Manter pelo menos 14 dias de stories de cada tipo.
- plano.json: chaves "09h", "15h", "20h"; itens {acao: create_story | create_image_post | create_carousel_post (arquivos) | create_video_post (thumb_offset), arquivo (link raw completo), legenda, pauta}.
- Links raw: `https://raw.githubusercontent.com/harmonytecnologia-netizen/Harmony-/metalize/metalize/fila/<data>/<arquivo>` (conferir 200 antes de publicar).

## Reels "Metalize Explica 3D"
- Formato vencedor da MOVE: 20–23 s, gancho-pergunta em 0–3 s, o porquê visual até 8 s, o erro até 13 s, a correção até 18 s, resultado + "salva pra conferir" no fim. Visual 3D realista (Blender/bpy, `pip install bpy==5.3.0`), sem cartoon.
- Primeiro: `animacoes/explica_calha_3d/cena.py` (calha sem caimento transborda × caimento mínimo de 0,5% = 5 mm por metro levando a água até o condutor, com trilha luminosa do caminho da água).
- Render na nuvem: `cd animacoes/<pasta> && SAMPLES=10 LARG=540 ALT=960 STEP=2 python3 cena.py 1:540` em partes de até 9 min (pula quadros já feitos), depois interpolar 12→24 qps (ffmpeg minterpolate) e montar com `kit_instagram/scripts/montar_explicativo.py` usando `MARCA=metalize/marca.json`.
- Música: faixa real de `automacao/musicas` (nunca MOVE_original_*), diferente a cada Reel. Efeitos poucos e com propósito.
- Pronto → `metalize/reels/prontos/<data>_<tema>.mp4` + `.json` {video_url raw, legenda, thumb_offset, tema}. O produzir.py coloca na próxima segunda.
- Próximos temas: rufo e pingadeira (por que a parede mancha), portão que arria (diagonal), solda bem feita × mal feita, galpão (contraventamento), escada confortável (conta de Blondel), calha × condutor (quantos tubos).

## Legendas
Tom elegante e próximo, 3–5 linhas, uma pergunta ou "salve para conferir", CTA leve (direct ou WhatsApp), 5–7 hashtags (#metalurgia #serralheria #altopadrao #arquitetura #marcelandia + tema).

## Registro
`metalize/historico.md` (data | hora | ação | pauta | media id). Commits com user.name "Metalize", user.email metalize@users.noreply.github.com; push com `git -c push.negotiate=true push origin metalize`.
