# Automação de conteúdo — MOVE (@move.s.a)

Manual que a rotina diária segue. Tudo aqui foi definido com o João.

## Conta e publicação
- Instagram: **@move.s.a**. Publicar pelo conector Windsor.ai, conta `17841461939593135` (MOVE).
  Nunca publicar nas outras contas conectadas (metalize.metalurgica, harmony_computer).
- Hospedagem dos arquivos: este repositório, branch `reels-move`. Link público:
  `https://raw.githubusercontent.com/harmonytecnologia-netizen/Harmony-/reels-move/<caminho>`
- **Tudo que vai para o feed também vai para o story** (create_story com o mesmo vídeo ou com uma arte 1080x1920 de divulgação).
- Publicar direto, sem esperar aprovação (pedido do João).
- Post diário às **12h** (horário de Brasília).

## Fluxo diário
1. Verificar `C:\Users\PC\Videos\MOVE para postar` no computador do João.
   Comparar com `historico.md` para saber quais vídeos já foram usados.
2. **Se tiver vídeo novo:** fazer um Reel PRO (ver "Padrão de edição"), publicar como Reel e também como Story.
3. **Se não tiver vídeo:** fazer conteúdo educativo sobre instalação (lista de temas abaixo), em vídeo com a avatar **Iamin** quando ela estiver pronta (`iamin/`). Até lá, fazer Reel explicativo ilustrado (desenhos/ícones animados, textos) ou carrossel.
4. Registrar no `historico.md`: data, tipo, tema, vídeos usados, música usada, media id.

## Padrão de edição (Reel PRO)
- Formato 1080x1920, 30 fps, H.264 + AAC 48 kHz, até ~30 s.
- Começa com `assets/intro_som.mp4` (intro de Som escolhida pelo João) e termina com `assets/tela_final.mp4`.
- Estabilização (vidstabdetect/vidstabtransform), hqdn3d, cas (nitidez), cor vintage quente (ver `scripts/pro.py`).
- Cortes no tempo da música (librosa beat_track), transições xfade variadas (circleopen, smoothleft, hblur, zoomin, fadewhite, slideup, fadeblack), zoom lento alternado por cena.
- Legendas numeradas (01, 02…) em caixa alta, Inter SemiBold, com animação de subida.
- **Música diferente a cada post** — nunca repetir uma faixa do `historico.md`. Fonte: Biblioteca de áudio do YouTube Studio (já logado no navegador do app Claude), gêneros Jazz & Blues / vintage / soul. Baixa para `C:\Users\PC\Downloads`.

## PADRÃO PREMIUM (obrigatório desde 11/11/2026)
Público de ALTO PADRÃO. Nada de desenho simples/casinha. Visual realista, ultra fino, estilo revista de arquitetura:
- Foto em tela cheia (real da obra/projeto, ou gerada no ChatGPT), luz quente e baixa, materiais nobres, muito respiro.
- Título em serif elegante (automacao/fonts/Playfair-400-normal.ttf), texto curto; detalhes em Inter Light com espaçamento largo; kicker em verde-menta.
- Logo MOVE pequeno no topo, @move.s.a discreto embaixo. Ver automacao/scripts/premium.py (feed 1080x1350 e story 1080x1920).
- Marcas (JBL, Bose, Klipsch, Harman Kardon, etc.): podem ser citadas como referência no texto. NUNCA usar logos ou fotos oficiais das marcas.
- Imagens geradas por IA: sempre escrever "Ambiente conceito." na legenda. Nunca apresentar como obra real.

## REGRA: parte gráfica sempre pelo ChatGPT (pedido do João, 11/11/2026)
Toda arte visual (fundos, ambientes, texturas, capas, cartões, peças impressas, personagem) é gerada no ChatGPT do João com prompt bem escrito. O logo MOVE e os textos pequenos são aplicados por cima no script (o ChatGPT deforma letras de logotipo e textos miúdos). Nada de desenho feito só com código quando o ChatGPT puder gerar.

## Gerar imagens realistas (ChatGPT do João)
- No navegador do app Claude (aba chatgpt.com, já logada na conta Plus do João), escrever o prompt e pedir a imagem.
- Prompt base: "Crie uma imagem fotográfica ultrarrealista, formato vertical 4:5. [ambiente de alto padrão: home cinema, living com som embutido, área gourmet, suíte com automação de cortinas, adega...]. Luz quente e baixa, contraste cinematográfico, atmosfera de revista de arquitetura (Architectural Digest), lente 24mm, materiais nobres com textura real. Sem pessoas, sem textos, sem logotipos e sem marcas visíveis."
- Abrir a imagem e clicar no ícone de download (topo). O arquivo cai em C:\Users\PC\Downloads como .png ou .tmp (o .tmp já é o PNG completo). Trazer com device_stage_files LOGO após cada download: se o João cancelar a janela "Salvar", o .tmp some. Reel com imagens: scripts/reel_premium.py (zoom supersampling, sem tremido).

## Identidade visual
- Cores: verde-menta `#54DFAE`, fundo `#0D1B17`, texto `#F2F5EF`, secundário `#A9BBB3`, contorno `#2C443A`.
- Fonte: Inter (títulos Bold/SemiBold). Logo sempre como imagem (`assets/logo_claro.png` em fundo escuro, `assets/logo_escuro.png` em fundo claro).
- Tom: moderno, profissional, sofisticado e próximo. Evitar promessas como "segurança total", "funciona com qualquer equipamento".
- Fim das legendas: convite para falar com a MOVE / enviar a planta. Hashtags: #AutomaçãoResidencial #Sonorização #CasaInteligente #HomeTheater #SmartHome #MOVE (variar).

## Temas para dias sem vídeo (rodar, sem repetir)
1. Como medir a posição das caixas de som de embutir no forro
2. Como recortar o gesso para a caixa de embutir (gabarito, serra copo, acabamento)
3. Como passar o cabo de som antes do forro (bitola, identificação)
4. Altura ideal da TV e distância do sofá
5. Projetor e telão: distância e tamanho de tela
6. Posição das caixas no home theater 5.1
7. Som ambiente por zonas (multiroom)
8. Onde colocar access points de Wi-Fi
9. Fio neutro no interruptor: por que importa na automação
10. Cenas de automação: "Cheguei", "Boa noite", "Cinema"
11. Cuidados com o rack: ventilação e organização
12. Antes e depois de uma obra

## Iamin (personagem ilustrada)
Ver automacao/iamin/FICHA.md. Estilo pintura digital aprovado. Story "Dica da Iamin" 1x por semana + capas de carrossel.

## Cronograma (fonte da verdade)
Planilha "Cronograma Instagram MOVE": https://claude.ai/artifact/U6qvqshwLh2DwVRFHhDJE8
- Aba "Cronograma": cada dia tem 12h (Reel + story) e 19h (feed/carrossel + 2 stories), com tema, título, status e música.
- Ao produzir um lote, seguir os temas da planilha, na ordem, e atualizar a coluna Status ("Pronto (na fila)", depois "Publicado").
- Dias marcados "Aguardando vídeo": usar vídeos da pasta MOVE para postar; se não houver, fazer Reel conceito do mesmo tema.

## Dica da Iamin (Reel semanal)
- 1 Reel por semana com a Iamin ilustrada explicando um tema (ver lista de temas). Modelo: `fila`/reel `reels/iamin_dica_01_home_theater.mp4`.
- Estrutura: cena 1 Iamin de corpo inteiro (`iamin/iamin_full_pad.png`) com a pergunta-gancho; 4 cenas de ambiente com dica numerada e selo da Iamin (`"badge": "automacao/iamin/avatar.png"` no cfg do `scripts/reel_premium.py`); cena final Iamin mais próxima (`iamin/iamin_close_pad.png`) com "Salve para a sua obra"; tela final.
- Ela explica, não dá depoimento nem diz que instalou nada. Legenda termina com pergunta + "Salve" + "Ambientes conceito.".
- Versão GRÁTIS (decisão do João em 11/11): Iamin em imagem com movimento de câmera, sem voz. Vídeo com ela andando/falando (Veo/Kling) só mais para frente, se ele decidir assinar. Roteiros falados prontos em `iamin/roteiros.md`.
- Temas da série, em ordem (1 por semana, sem repetir):
  1. (feito 11/11) Home theater: posição das caixas
  2. Caixa de embutir × caixa aparente: o que muda no som e na decoração
  3. Qualidade de som: por que caixa boa sozinha não basta (amplificador, cabo, acústica)
  4. Cenas de automação: "Cheguei", "Boa noite", "Cinema" (uma por cena)
  5. Som por zonas: cada ambiente com sua música
  6. Níveis de projeto: de bom a referência (marcas só no texto, nunca logos)
  7. Telão × TV: quando cada um vale a pena
  8. Automação de cortinas e luz: o que pensar antes da obra

## Engajamento (todas as legendas)
- Primeira linha = gancho (pergunta ou afirmação forte), antes do "mais".
- Terminar com: uma pergunta simples para comentar ("Qual você escolheria: A ou B?"), um pedido de salvar/enviar, e o convite para o direct.
- Stories: usar enquete/pergunta no texto da arte ("Responda: sua sala já tem…?") e repostar o Reel do dia.
- Responder comentários 2x por dia (tarefa agendada). Registro em `automacao/comentarios.md`.

## Respostas a comentários (regras)
- Tom: educado, sofisticado e próximo, 1–2 frases, chamar pelo nome quando der, no máximo 1 emoji.
- Nunca falar preço, prazo ou prometer resultado; para orçamento: "Te chamamos no direct" / "Chama a gente no direct".
- Elogio → agradecer. Dúvida técnica simples → responder curto e convidar para o direct. Pergunta de preço → direct.
- Reclamação, crítica, spam, ofensa ou assunto delicado → NÃO responder, NÃO ocultar, NÃO apagar: só registrar e avisar o João.
- Nunca responder comentários da própria conta (move.s.a). Responder cada comentário uma única vez.
- Direct (DM) não é acessível pelo conector; esses o João responde no app.

## Aprendizados das métricas (11/11/2026)
- Reels com 71–100% de pulo nos 3 primeiros segundos: o gancho tem que aparecer no 1º segundo. A intro do logo NÃO abre mais o Reel: começar direto na imagem mais forte + frase-gancho; logo MOVE só na tela final.
- Público real: 56% homens, 35–54 anos (60%), litoral norte de SC (Balneário Camboriú, Itapema, Itajaí, Camboriú, Blumenau, Florianópolis, Brusque, Joinville). Citar essas cidades nas legendas/obras.
- Melhores posicionamentos no anúncio: Reels e Feed do Facebook (~R$ 15 por conversa).
