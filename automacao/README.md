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
