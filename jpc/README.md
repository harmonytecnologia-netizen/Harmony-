# VÍDEOS: máx. 3 por dia — 12h JPC Ensina (tutorial prático: configuração/desempenho, vírus, limpeza, hardware na mão, defeitos e quando chamar técnico; capa obrigatória) + 2 cortes GTA 6 às 15h e 20h (24/11/2026)
- JPC Ensina: pautas em `banco/ensina_pautas.py` (25 pautas, 5 grupos em rodízio, sem repetir tema em 14 dias); gerador `scripts/ensina.py` (narração Piper por passo sincronizada com os cartões numerados, caminho do menu em "janela", fundos reais/Pexels, música da biblioteca baixinha, CTA TÉCNICO) + `capa.jpg` 1080x1920. No plano.json o item create_video_post leva "capa" (sem thumb_offset). Cortes de GTA 6 NÃO entram no plano.json (outra tarefa publica às 15h e 20h).
- Refazer só o Reel de um dia já pronto: `python3 jpc/scripts/produzir.py --refazer12h AAAA-MM-DD` (o modo padrão já faz isso nos dias sem JPC Ensina; hoje só antes das 12h).
- Segurança: nada de registro, BIOS avançada, overclock ou abrir fonte; sempre "desligue da tomada antes de abrir"; defeitos terminam com "não resolveu? manda TÉCNICO no Direct".

# MODO GTA 6 desde 19/11/2026 (pedido do João em 18/11; vale até ele mandar parar)
- GTA 6 saiu em 19/11/2026 SÓ para PS5 e Xbox Series X|S. NÃO há versão de PC anunciada nem requisitos oficiais de PC (conferir no dia com WebSearch; se a Rockstar anunciar, atualizar `banco/gta6_pautas.py`). Nunca inventar requisito "oficial": falar em "PC pronto para quando o GTA 6 chegar ao PC" e "o que deve pesar" (ESTIMATIVA marcada, base em open world atuais/GTA 5 Enhanced), sem prometer FPS.
- Todo conteúdo novo (feed, carrossel, stories, Reels) = GTA 6: novidades do dia (notícias recentes, nada de GTA 5 antigo), Leonida/Vice City, Jason e Lucia, recordes, bugs/memes, e o ângulo de PC (RAM 16x32 GB, dual channel, frequência, placa/VRAM, SSD NVMe x HD, processador, upgrade, erros de montagem). CTA: "manda GTA6 / ORÇAMENTO no Direct".
- Imagens: nada de arte oficial, logo, capa ou personagem da Rockstar; só fundos da biblioteca/IA genéricos (PC RGB, cidade neon) + texto. Marcas só no texto.
- (ATÉ 24/11; agora o Reel 12h é JPC Ensina, ver topo) Reel TODO DIA na chave "12h" (feed + story + Reel GTA 6 + story). 1º: corte GTA 6 autorizado mais novo ainda não publicado (`cortes/prontos/<nome>.mp4` + `<nome>.json` com {"jogo":"gta6","streamer","legenda"}; só streamer com autorização em `cortes/autorizacoes/`, hoje Paulinho o LOKO; regras em `playbooks/cortes-gta6-jpc/SKILL.md`). Sem corte novo → Reel próprio do banco `reels` (texto animado + narração Piper pt_BR-faber + música da biblioteca). Nunca vídeo de terceiros sem autorização nem trailer/gameplay copiado.
- Pautas: `banco/gta6_pautas.py` (MODO_GTA6=True pausa as antigas; `produzir.py` pula pautas com "pausada"). Feed 16, carrosséis 14, stories 70 (14 dias), reels 14. Antes de acabar, escrever mais no mesmo arquivo e rodar `python3 jpc/banco/gerar_banco.py` na raiz.
- Notícias do dia que mudam rápido: ajustar as pautas do dia em `gta6_pautas.py` ou refazer a peça com `--data AAAA-MM-DD --forcar` (só horários que ainda não passaram).

# JPC — @harmony_computer — automação diária do Instagram

## Conta (NUNCA publicar em outra)
- Windsor.ai, conector instagram, conta **17841445277894628** = jpc (harmony_computer). Confirmado pelo João em 13/11/2026.
- Proibido publicar em MOVE (17841461939593135) ou Metalize (17841449079341071).

## Nicho e tom
- PC gamer montado sob medida, peças, upgrade e manutenção. Enviamos para todo o Brasil (Facebook diz Bombinhas/Balneário Camboriú e região).
- Público popular, tom de amigo gamer, frases curtas. Contato: Direct ("manda ORÇAMENTO"). Ainda sem WhatsApp.
- Conteúdo 100% PC/games/hardware (e dicas de IA/Claude quando ligadas a PC). NADA de som/automação (MOVE).
- Sem depoimento falso, sem cliente inventado, sem preço/prazo em público. IA = "imagem ilustrativa"/"ambiente conceito". Marcas de terceiros só no texto, sem logo.
- Personagens/golpes de jogos famosos: só inspiração de estilo, NUNCA copiar personagem, nome ou bordão (nada de Hadouken/Fatality/Mario etc.).

## Padrão visual
- Cores: roxo #7a3cff/#8b5cff, ciano #22d3ee, rosa #ff4fd8, amarelo #ffe14f, fundo #07040f. Fontes: Anton (títulos), Poppins Bold (texto), Bangers (gritos de jogo). Pasta fonts/.
- Feed/carrossel 1080x1350, story/Reel 1080x1920. Texto fora dos 250 px de cima e 400 px de baixo nos 9:16.
- Artes "de verdade": fundos gerados no ChatGPT do João (biblioteca/fundos/ia_*) ou vídeos livres Pexels (biblioteca/videos, licença Pexels) ou material real da pasta do PC "Documentos\JPC para postar". Nada de desenho quadrado feito só em código.
- Reels caprichados (arte ChatGPT + animação + narração Piper pt_BR-faber + trilha) vão para reels/prontos/*.json e entram nos dias de Reel.

## Frequência obrigatória (todo dia)
- 09h: 2 stories próprios · 12h: post de feed + story dele (seg/qua/sex também Reel + story dele) · 15h: 1 story próprio · 19h: carrossel 5–7 slides + story dele · 21h: 2 stories próprios.
- Story próprio = feito só para story (dica, pergunta, A ou B, você sabia, agenda). Repost NÃO conta.

## Como funciona
- `python3 jpc/scripts/produzir.py` garante a fila de hoje + 3 dias em `fila/AAAA-MM-DD/` (plano.json + artes). Plano B: usa só o repositório.
- `python3 jpc/scripts/produzir.py --emergencia 15h` gera um story avulso de hoje (imprime o item JSON).
- Banco de pautas: `banco/gerar_banco.py` → `banco/pautas.json`; já usados em `banco/usados.json`. Quando faltar < 7 dias de pauta, escrever novas pautas no gerar_banco.py (nunca repetir tema da última semana).
- Música: `biblioteca/musicas/*.mp3` (Biblioteca de áudio do YouTube, sem repetir em 7 dias); sem música livre → trilha própria sintetizada.
- Links públicos: `https://raw.githubusercontent.com/harmonytecnologia-netizen/Harmony-/jpc/jpc/<caminho>` (branch **jpc**).
- Tudo publicado vai para `historico.md` (data, horário, ação, arquivo, música, media id).
- Plano B de publicação: se o Windsor falhar/expirar, publicar pelo navegador do app Claude no PC do João (instagram.com, conta harmony_computer já salva) quando o PC estiver ligado; senão avisar o João.

## Canais de vídeo (18/11/2026)
- YouTube: canal de marca **"JPC | PC Gamer"** (@harmony_computer), criado em 18/11/2026 na conta Google harmonytecnologia@gmail.com (a mesma do canal da MOVE "Harmony Tecnologia", mas é outro canal). Nunca postar JPC no canal da MOVE.
- TikTok: o @moveautomacao é da MOVE (já no Windsor). TikTok da JPC: ver histórico (criação pendente/feita).
- Shorts/TikTok recebem os Reels da JPC + cortes de GTA 6.
- YouTube: descrição do canal publicada em 18/11 (falta foto de perfil e banner, a gerar no ChatGPT do João). O Windsor só LÊ dados do YouTube (escopo youtube.readonly), não publica: upload dos Shorts é pelo YouTube Studio no navegador do app (conta harmonytecnologia@gmail.com, canal JPC | PC Gamer).

## Cortes de GTA 6 (e outros jogos)
- Skill: `playbooks/cortes-gta6-jpc/SKILL.md` (só streamer com autorização registrada em `cortes/autorizacoes/`; sempre transformar).
- Script: `python3 jpc/scripts/corte.py --help` (1080x1920, gancho, crédito "Corte autorizado", cartão final JPC).
- Brutos no PC: `Documentos\JPC para postar\GTA6\`. Prontos: `cortes/prontos/`.
- Skill base da JPC: `playbooks/jpc-gamer/SKILL.md`.

## TikTok da JPC (18/11/2026)
- Decisão do João: usar a conta TikTok @jp.yas (logada no navegador do app) como TikTok da JPC.
- Pendente (bloqueado por verificação anti-robô do TikTok — quebra-cabeça que só o João resolve): foto (jpc/artes/canais/perfil_800.jpg, cópia em Downloads\JPC_foto_perfil_TikTok.jpg), nome "JPC | PC Gamer", bio "PC gamer montado • Cortes GTA 6 e dicas • Orçamento: IG @harmony_computer" e @ novo (harmony_computer; se não der, jpc.pcgamer).
- Windsor não publica no TikTok (sem ações de escrita): postar pelo navegador do app.
