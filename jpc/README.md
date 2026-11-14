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
