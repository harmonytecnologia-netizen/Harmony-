"""Roteiro do lote 13/11 a 26/11/2026 (segue a planilha "Cronograma Instagram MOVE").
Cada dia: reel (12h, 5 cenas) + post (19h, feed ou carrossel) + story extra.
'prompt' = cena pedida ao ChatGPT (entra no PROMPT BASE). Títulos: '|' quebra linha no Reel.
"""
BASE = ("Crie uma imagem fotográfica ultrarrealista, formato vertical {fmt}. {cena} "
        "Luz quente e baixa, contraste cinematográfico, atmosfera de revista de arquitetura (Architectural Digest), "
        "lente 24mm, materiais nobres com textura real. Sem pessoas, sem textos, sem logotipos e sem marcas visíveis.")

def prompt(cena, fmt='9:16'):
    return BASE.format(fmt=fmt, cena=cena)

FECHO = "A MOVE projeta e integra som, cinema, iluminação e automação para casas e apartamentos de alto padrão no litoral norte de SC. Agende uma conversa e envie a planta do seu projeto."

DIAS = [
 {"data": "2026-11-13",
  "reel": {"tema": "Wi-Fi em toda a casa (access points no teto)", "titulo": "Sinal forte em cada canto, sem aparelho à vista.",
   "scenes": [
    {"kicker": "WI-FI DE PROJETO", "title": "Sinal forte em|cada canto.", "cena": "Living amplo de apartamento de frente para o mar em Balneário Camboriú, ao entardecer, forro de gesso liso com um pequeno ponto de acesso branco circular embutido no teto, quase imperceptível."},
    {"kicker": "01 · NO FORRO", "title": "O ponto de acesso|some no teto.", "cena": "Close de um forro de gesso branco com um ponto de acesso Wi-Fi circular branco, discreto, ao lado de spots embutidos; luz rasante quente."},
    {"kicker": "02 · POR AMBIENTE", "title": "Um ponto por área,|sem zona sem sinal.", "cena": "Corredor longo de residência de alto padrão com piso de madeira e forro de gesso, pequenos pontos de acesso discretos no teto, luz quente indireta."},
    {"kicker": "03 · POR CABO", "title": "Ligado por cabo,|estável de verdade.", "cena": "Rack técnico organizado dentro de armário de marcenaria escura, cabos de rede identificados e penteados, switch discreto, luz quente suave."},
    {"kicker": "04 · INVISÍVEL", "title": "Conexão em toda|a casa, sem nada|à vista.", "cena": "Varanda gourmet integrada à sala, noite, mesa posta, tudo limpo e sem aparelhos visíveis, cidade iluminada ao fundo."}],
   "legenda": "Sinal forte em cada canto, sem aparelho à vista.\n\nWi-Fi bom em casa grande não depende de um roteador mais potente, e sim de projeto:\n01 · Pontos de acesso discretos no forro.\n02 · Um ponto por área, pensado na planta.\n03 · Ligação por cabo até o rack, para ser estável.\n04 · Nada de caixinhas espalhadas pela sala.\n\nNa sua casa, onde o sinal mais falha? Conte nos comentários e salve para a sua obra.\n\n" + FECHO + "\n\nImagens conceito.\n\n#WiFi #CasaInteligente #AutomaçãoResidencial #BalneárioCamboriú #AltoPadrão #MOVE"},
  "post": {"formato": "carrossel", "tema": "Rack técnico organizado", "legenda": "5 cuidados com a central da sua casa.\n\nO rack é onde som, rede, câmeras e automação se encontram. Quando ele é bem planejado, a casa funciona melhor e a manutenção fica simples:\n01 · Ventilação de verdade.\n02 · Cabos identificados nas duas pontas.\n03 · Energia protegida.\n04 · Espaço para crescer.\n05 · Acesso fácil para manutenção.\n\nArraste para ver cada cuidado e salve para mostrar ao seu arquiteto.\n\n" + FECHO + "\n\nAmbientes conceito.\n\n#RackTécnico #Infraestrutura #AutomaçãoResidencial #Sonorização #ObraDeAltoPadrão #MOVE",
   "slides": [
    {"kicker": "RACK TÉCNICO", "title": ["5 cuidados com a", "central da sua casa."], "body": "Arraste para ver cada um →", "cena": "Armário técnico de marcenaria escura com porta aberta revelando rack organizado, cabos penteados, luz quente interna, em casa de alto padrão."},
    {"kicker": "01 · VENTILAÇÃO", "title": ["Equipamento", "precisa respirar."], "body": "Saída de ar e espaço entre aparelhos.", "cena": "Detalhe de marcenaria com grelha de ventilação discreta em armário técnico, luz quente rasante."},
    {"kicker": "02 · IDENTIFICAÇÃO", "title": ["Cada cabo com", "nome e destino."], "body": "Etiqueta nas duas pontas.", "cena": "Close de cabos de rede e de som identificados com etiquetas brancas, organizados em feixes paralelos, luz quente."},
    {"kicker": "03 · ENERGIA", "title": ["Proteção antes", "de tudo ligar."], "body": "Circuito dedicado e proteção elétrica.", "cena": "Painel elétrico residencial moderno e organizado em ambiente técnico limpo, luz quente suave."},
    {"kicker": "04 · FOLGA", "title": ["Espaço para", "o que vem depois."], "body": "Previsão para novos equipamentos.", "cena": "Rack técnico com prateleiras livres e equipamentos discretos, marcenaria em madeira escura, luz quente."},
    {"kicker": "05 · ACESSO", "title": ["Manutenção sem", "desmontar nada."], "body": "Porta e fundo de fácil acesso.", "cena": "Armário técnico com portas de correr abertas em living de alto padrão, acesso fácil, luz quente."}]},
  "story": {"kicker": "BASTIDORES", "title": ["Sua central", "está organizada?"], "body": "Responda: sim · ainda não", "cena": "Rack técnico organizado visto de frente com leds suaves, marcenaria escura, luz quente."}},

 {"data": "2026-11-14",
  "reel": {"tema": "Obra: do cabeamento ao acabamento", "titulo": "Antes do gesso, a parte mais importante.", "obra": True,
   "scenes": [
    {"kicker": "ANTES DO GESSO", "title": "A parte mais|importante.", "cena": "Obra de apartamento de alto padrão antes do forro, estrutura metálica do gesso exposta, eletrodutos organizados, luz quente de fim de tarde entrando pela janela de vidro com vista para o mar."},
    {"kicker": "01 · INFRAESTRUTURA", "title": "Cada cabo no|caminho certo.", "cena": "Close de eletrodutos corrugados identificados presos à estrutura metálica de forro, obra limpa e organizada, luz quente."},
    {"kicker": "02 · PONTOS", "title": "Som, luz e rede|marcados na planta.", "cena": "Planta arquitetônica impressa sobre bancada de obra, com régua metálica e lápis, luz quente rasante, sem textos legíveis."},
    {"kicker": "03 · FORRO", "title": "O gesso fecha,|a estrutura fica.", "cena": "Forro de gesso recém-instalado e liso com recortes circulares prontos para caixas de som e spots, luz quente."},
    {"kicker": "04 · ACABAMENTO", "title": "Tudo pronto,|nada aparente.", "cena": "Sala de estar finalizada de alto padrão com forro liso, caixas de som embutidas com grelha branca discreta e spots, luz quente."}],
   "legenda": "Antes do gesso, a parte mais importante.\n\nO que faz um projeto de som e automação funcionar por muitos anos fica escondido no forro:\n01 · Infraestrutura com caminho certo para cada cabo.\n02 · Pontos de som, luz e rede marcados na planta.\n03 · Forro fechado sobre uma estrutura pensada.\n04 · Acabamento limpo, nada aparente.\n\nSua obra está em qual etapa? Conte aqui e salve este vídeo.\n\n" + FECHO + "\n\n#ObraDeAltoPadrão #Infraestrutura #AutomaçãoResidencial #Itapema #Sonorização #MOVE"},
  "post": {"formato": "feed", "tema": "Área de piscina com som externo", "legenda": "O verão começa no som.\n\nNa área da piscina, as caixas para ambiente externo ficam integradas ao paisagismo e ao forro da varanda, com som distribuído e volume controlado pelo celular. Música para o dia todo, sem fio aparente.\n\nPiscina com música: indispensável ou dispensável? Conte nos comentários.\n\n" + FECHO + "\n\nAmbiente conceito.\n\n#ÁreaDePiscina #SomExterno #CasaDePraia #Paisagismo #AltoPadrão #MOVE",
   "slides": [{"kicker": "ÁREA DE PISCINA", "title": ["O verão começa", "no som."], "body": "Som externo integrado ao paisagismo.", "cena": "Área de piscina de residência de alto padrão no litoral, fim de tarde dourado, deck de madeira, espreguiçadeiras, paisagismo tropical com caixas de som externas discretas entre as plantas."}]},
  "story": {"kicker": "VERÃO 2027", "title": ["Sua área externa", "já tem trilha?"], "body": "Responda: sim · quero ter", "cena": "Borda infinita de piscina ao entardecer com vista para o mar, luz dourada, deck de madeira."}},

 {"data": "2026-11-15",
  "reel": {"tema": "Cena Boa noite", "titulo": "Um toque e a casa dorme com você.",
   "scenes": [
    {"kicker": "CENA BOA NOITE", "title": "Um toque e a casa|dorme com você.", "cena": "Suíte master de alto padrão à noite, cama arrumada com roupa de cama clara, abajures acesos com luz âmbar baixa, cortinas fechando."},
    {"kicker": "01 · LUZES", "title": "As luzes da casa|se apagam.", "cena": "Living de alto padrão à noite com luzes apagando, apenas uma faixa de luz indireta suave no rodapé, cidade ao fundo."},
    {"kicker": "02 · CORTINAS", "title": "As cortinas|se fecham.", "cena": "Cortinas de linho fechadas em suíte de alto padrão, luz âmbar suave, ambiente silencioso."},
    {"kicker": "03 · CAMINHO", "title": "Uma luz baixa|guia o caminho.", "cena": "Corredor residencial à noite com balizadores de luz baixa no rodapé, piso de madeira, atmosfera calma."},
    {"kicker": "04 · SILÊNCIO", "title": "A casa descansa.|Você também.", "cena": "Suíte em penumbra, apenas um abajur de luz muito baixa, cama arrumada, janela com cortina fechada."}],
   "legenda": "Um toque e a casa dorme com você.\n\nA cena “Boa noite” faz em um único comando o que antes era uma volta pela casa:\n01 · As luzes se apagam.\n02 · As cortinas se fecham.\n03 · Uma luz baixa guia o caminho.\n04 · A casa descansa, e você também.\n\nQual seria a primeira cena da sua casa? Conte nos comentários.\n\n" + FECHO + "\n\nImagens conceito.\n\n#CenaBoaNoite #AutomaçãoResidencial #CasaInteligente #Iluminação #SuíteMaster #MOVE"},
  "post": {"formato": "feed", "tema": "Adega climatizada com luz em cena", "legenda": "O vinho também merece luz certa.\n\nNa adega, a iluminação entra em cena quando você chega: luz baixa, sem calor sobre as garrafas, e uma playlist suave para receber. Tudo integrado ao restante da casa.\n\nTinto ou branco para receber os amigos?\n\n" + FECHO + "\n\nAmbiente conceito.\n\n#Adega #Iluminação #DesignDeInteriores #CasaInteligente #AltoPadrão #MOVE",
   "slides": [{"kicker": "ADEGA EM CENA", "title": ["O vinho também", "merece luz certa."], "body": "Iluminação em cena e som ambiente.", "cena": "Adega climatizada de residência de alto padrão com porta de vidro, garrafas em nichos de madeira escura iluminadas por fita de luz âmbar, mesa de degustação em mármore."}]},
  "story": {"kicker": "DETALHE", "title": ["Luz baixa,", "sem calor."], "body": "Iluminação pensada para cada ambiente.", "cena": "Close de garrafas de vinho deitadas em nicho de madeira com luz âmbar indireta."}},

 {"data": "2026-11-16",
  "reel": {"tema": "Altura da TV e distância do sofá", "titulo": "A medida certa para assistir sem cansar.",
   "scenes": [
    {"kicker": "SALA DE TV", "title": "A medida certa para|assistir sem cansar.", "cena": "Sala de TV de alto padrão com painel de madeira ripada, TV grande embutida, sofá de linho em frente, luz quente baixa."},
    {"kicker": "01 · ALTURA", "title": "O centro da tela|na altura dos olhos.", "cena": "Vista lateral de sala de estar com sofá e TV embutida em painel de madeira, enquadramento que mostra a relação de altura, luz quente."},
    {"kicker": "02 · DISTÂNCIA", "title": "Quanto maior a tela,|mais longe o sofá.", "cena": "Plano aberto de sala de estar ampla com TV grande e sofá a boa distância, tapete, luz quente."},
    {"kicker": "03 · ÂNGULO", "title": "Sem pescoço|para cima.", "cena": "Sala íntima com poltrona e TV na parede, posicionamento confortável, luz âmbar suave."},
    {"kicker": "04 · LUZ", "title": "Sem reflexo|na tela.", "cena": "Sala de TV com cortinas fechadas e luz indireta atrás do painel, sem reflexo na tela, atmosfera cinematográfica."}],
   "legenda": "A medida certa para assistir sem cansar.\n\nTV bonita é a que fica confortável de assistir:\n01 · Centro da tela próximo da altura dos olhos sentado.\n02 · Distância do sofá proporcional ao tamanho da tela.\n03 · Nada de olhar para cima por horas.\n04 · Luz e cortinas pensadas para evitar reflexo.\n\nCada sala tem a sua medida, por isso vale medir no projeto. Salve para consultar na sua obra.\n\n" + FECHO + "\n\nImagens conceito.\n\n#SalaDeTV #HomeTheater #DesignDeInteriores #ArquiteturaDeInteriores #Itajaí #MOVE"},
  "post": {"formato": "carrossel", "tema": "Projetor ou TV: qual escolher", "legenda": "Seu cinema em casa começa nessa escolha.\n\nProjetor ou TV? Os dois funcionam muito bem, desde que combinem com a sala:\n01 · Tamanho de imagem que você quer.\n02 · Controle de luz no ambiente.\n03 · Uso no dia a dia.\n04 · Espaço e distância de projeção.\n05 · Integração com som e automação.\n\nE você, time projetor ou time TV? Conte nos comentários.\n\n" + FECHO + "\n\nAmbientes conceito.\n\n#Projetor #HomeCinema #CinemaEmCasa #HomeTheater #AltoPadrão #MOVE",
   "slides": [
    {"kicker": "CINEMA EM CASA", "title": ["Projetor ou TV:", "qual escolher?"], "body": "Arraste para comparar →", "cena": "Home cinema de alto padrão com tela de projeção grande e poltronas reclináveis de couro, luz âmbar baixa nas laterais."},
    {"kicker": "01 · TAMANHO", "title": ["Tela grande pede", "projetor."], "body": "Acima de 100\", a projeção ganha.", "cena": "Tela de projeção grande em sala escura com imagem de paisagem luminosa projetada, poltronas em silhueta."},
    {"kicker": "02 · LUZ", "title": ["Sala clara", "pede TV."], "body": "Ambientes com muita luz natural.", "cena": "Living claro com grandes janelas e TV embutida em painel de madeira, luz do dia suave."},
    {"kicker": "03 · USO", "title": ["Dia a dia ou", "sessão de cinema?"], "body": "Frequência muda a escolha.", "cena": "Sala de TV aconchegante com mantas no sofá e TV, luz quente noturna."},
    {"kicker": "04 · ESPAÇO", "title": ["Distância", "é projeto."], "body": "Projeção e tela medidas na planta.", "cena": "Sala de cinema com projetor discreto embutido no forro de gesso, luz âmbar."},
    {"kicker": "05 · INTEGRAÇÃO", "title": ["Os dois ficam", "melhores com som."], "body": "Som, luz e cortinas na mesma cena.", "cena": "Home theater com caixas de som embutidas na parede revestida em tecido, luz baixa."}]},
  "story": {"kicker": "DICA DA IAMIN", "title": ["Projetor ou TV?", "Depende da luz."], "body": "Responda: projetor · TV", "cena": "Home cinema com tela de projeção e luz âmbar, poltronas de couro.", "iamin": True}},

 {"data": "2026-11-17",
  "reel": {"tema": "Posição das caixas no 5.1", "titulo": "Onde cada caixa fica no seu home theater.",
   "scenes": [
    {"kicker": "HOME THEATER 5.1", "title": "Onde cada caixa|fica na sua sala.", "cena": "Home theater de alto padrão com tela grande, sofá central e caixas de som embutidas nas paredes, luz âmbar baixa."},
    {"kicker": "01 · CENTRAL", "title": "Os diálogos saem|do centro da tela.", "cena": "Parede frontal de home theater com tela e caixa de som central embutida logo abaixo, grelha em tecido escuro, luz quente."},
    {"kicker": "02 · FRONTAIS", "title": "Esquerda e direita|abrem a cena.", "cena": "Vista frontal de sala de cinema com duas caixas embutidas laterais à tela, simétricas, luz âmbar."},
    {"kicker": "03 · SURROUND", "title": "Atrás e ao lado,|o som te envolve.", "cena": "Parede lateral de home theater revestida em tecido com caixa de som embutida discreta acima da altura dos ouvidos, poltronas."},
    {"kicker": "04 · SUBWOOFER", "title": "O grave no ponto|certo da sala.", "cena": "Subwoofer discreto embutido em marcenaria de home theater, luz âmbar baixa, ambiente escuro elegante."}],
   "legenda": "Onde cada caixa fica no seu home theater.\n\nNo 5.1, cada caixa tem uma função:\n01 · Central: os diálogos, junto à tela.\n02 · Frontais: abrem a cena, esquerda e direita.\n03 · Surround: ao lado ou atrás de quem assiste.\n04 · Subwoofer: o grave, no ponto certo da sala.\n\nA posição exata depende da sala e é definida no projeto. Salve e envie para quem está planejando o cinema em casa.\n\n" + FECHO + "\n\nImagens conceito.\n\n#HomeTheater #Som51 #CinemaEmCasa #Sonorização #Florianópolis #MOVE"},
  "post": {"formato": "feed", "tema": "Sala de cinema dedicada", "legenda": "Uma sessão privada, todos os dias.\n\nUma sala de cinema dedicada reúne tela, som envolvente, acústica tratada e luz em cena. Um comando, e a sessão começa do jeito que você gosta.\n\nQual filme abriria a sua primeira sessão?\n\n" + FECHO + "\n\nAmbiente conceito.\n\n#SalaDeCinema #HomeCinema #AcústicaArquitetônica #CinemaEmCasa #AltoPadrão #MOVE",
   "slides": [{"kicker": "SALA DE CINEMA", "title": ["Uma sessão privada,", "todos os dias."], "body": "Tela, som e acústica pensados juntos.", "cena": "Sala de cinema dedicada em residência de alto padrão, poltronas reclináveis de couro em dois níveis, paredes em tecido acústico escuro, tela grande, luz âmbar lateral."}]},
  "story": {"kicker": "SESSÃO PRIVADA", "title": ["Seu cinema", "começa no projeto."], "body": "Agende uma conversa pelo direct.", "cena": "Poltronas de cinema em couro caramelo em sala escura com feixe de luz do projetor."}},

 {"data": "2026-11-18",
  "reel": {"tema": "Obra em andamento", "titulo": "Infraestrutura pensada antes do forro.", "obra": True,
   "scenes": [
    {"kicker": "OBRA EM ANDAMENTO", "title": "Pensado antes|do forro.", "cena": "Apartamento de alto padrão em obra, estrutura de forro exposta, grandes janelas com vista para a orla ao entardecer, obra organizada."},
    {"kicker": "01 · CAIXAS", "title": "Caixas de embutir|já posicionadas.", "cena": "Caixas de som de embutir redondas posicionadas em forro de gesso aberto durante a obra, luz quente."},
    {"kicker": "02 · CABOS", "title": "Bitola certa,|cada um identificado.", "cena": "Feixe de cabos de som e rede identificados saindo de eletroduto na parede durante obra, luz quente."},
    {"kicker": "03 · QUADRO", "title": "O rack recebe|tudo organizado.", "cena": "Nicho técnico em obra com cabos chegando organizados, antes da marcenaria, luz quente."},
    {"kicker": "04 · PRÓXIMA ETAPA", "title": "Agora sim,|o acabamento.", "cena": "Ambiente de living com forro de gesso já fechado e pintado, recortes limpos, aguardando móveis, luz quente do entardecer."}],
   "legenda": "Infraestrutura pensada antes do forro.\n\nO melhor momento para planejar som e automação é antes do gesso:\n01 · Caixas de embutir já posicionadas.\n02 · Cabos com bitola certa e identificados.\n03 · Tudo chegando organizado ao rack.\n04 · Depois, o acabamento sem quebra-quebra.\n\nVai começar uma obra? Salve este vídeo e mande para o seu arquiteto.\n\n" + FECHO + "\n\n#ObraEmAndamento #Infraestrutura #AutomaçãoResidencial #Camboriú #ConstruçãoCivil #MOVE"},
  "post": {"formato": "feed", "tema": "Home office com som ambiente", "legenda": "Foco, conforto e o som na medida.\n\nNo home office, o som ambiente embutido toca baixinho, a luz ajusta a temperatura ao longo do dia e as persianas controlam o reflexo na tela. Um espaço que ajuda você a render.\n\nVocê trabalha melhor com música ou em silêncio?\n\n" + FECHO + "\n\nAmbiente conceito.\n\n#HomeOffice #SomAmbiente #CasaInteligente #DesignDeInteriores #AltoPadrão #MOVE",
   "slides": [{"kicker": "HOME OFFICE", "title": ["Foco, conforto e", "o som na medida."], "body": "Som ambiente, luz e persianas integrados.", "cena": "Home office de alto padrão com mesa de madeira maciça, estante iluminada, janela com persiana, caixas de som embutidas discretas no forro, luz quente de fim de tarde."}]},
  "story": {"kicker": "DETALHE", "title": ["O som está aí.", "Você não vê."], "body": "Caixas de embutir com grelha discreta.", "cena": "Close de caixa de som embutida no forro de gesso com grelha branca fina, ao lado de spot, luz rasante quente."}},

 {"data": "2026-11-19",
  "reel": {"tema": "Cena Cheguei", "titulo": "A casa te recebe do seu jeito.",
   "scenes": [
    {"kicker": "CENA CHEGUEI", "title": "A casa te recebe|do seu jeito.", "cena": "Hall de entrada de residência de alto padrão ao anoitecer, porta pivotante de madeira, luz quente acendendo, piso de mármore."},
    {"kicker": "01 · ENTRADA", "title": "A luz do hall|acende sozinha.", "cena": "Hall de entrada com arandelas acesas em luz âmbar e console de madeira, porta de madeira, atmosfera acolhedora."},
    {"kicker": "02 · LIVING", "title": "A sala se prepara|em cena.", "cena": "Living de alto padrão com luzes em cena quente, abajures acesos e vista noturna da cidade."},
    {"kicker": "03 · CLIMA", "title": "A temperatura|já está no ponto.", "cena": "Sala de estar com ar-condicionado embutido em forro com difusor linear discreto, luz quente, ambiente acolhedor."},
    {"kicker": "04 · PLAYLIST", "title": "E a sua música|começa a tocar.", "cena": "Cozinha integrada de alto padrão à noite com bancada de mármore, luz pendente quente, caixas de som embutidas no forro."}],
   "legenda": "A casa te recebe do seu jeito.\n\nCom a cena “Cheguei”, um toque no celular ou a chegada pela porta prepara a casa:\n01 · A luz do hall acende.\n02 · A sala entra em cena.\n03 · A temperatura já está no ponto.\n04 · A sua playlist começa a tocar.\n\nO que você ligaria primeiro ao chegar em casa?\n\n" + FECHO + "\n\nImagens conceito.\n\n#CenaCheguei #AutomaçãoResidencial #CasaInteligente #SmartHome #Joinville #MOVE"},
  "post": {"formato": "carrossel", "tema": "Fio neutro no interruptor", "legenda": "O detalhe da obra que libera a automação.\n\nMuitos interruptores inteligentes precisam do fio neutro na caixinha. Quando ele não é previsto, a automação fica limitada depois:\n01 · O que é o neutro na caixinha.\n02 · Por que muitos módulos precisam dele.\n03 · Quando prever: antes da fiação.\n04 · Como conferir com o eletricista.\n05 · Um item simples que evita retrabalho.\n\nSalve e envie para o seu eletricista. Dúvidas? Chama a gente no direct.\n\n" + FECHO + "\n\nAmbientes conceito.\n\n#FioNeutro #InstalaçãoElétrica #AutomaçãoResidencial #ObraDeAltoPadrão #DicaDeObra #MOVE",
   "slides": [
    {"kicker": "DICA DE OBRA", "title": ["Fio neutro no", "interruptor."], "body": "O detalhe que libera a automação →", "cena": "Close de interruptor touch de vidro preto elegante em parede de pedra clara, luz quente rasante.", "iamin_capa": True},
    {"kicker": "01 · O QUE É", "title": ["O neutro chega", "até a caixinha."], "body": "Junto da fase, no ponto do interruptor.", "cena": "Caixinha elétrica embutida na parede com fios organizados durante obra, close limpo, luz quente."},
    {"kicker": "02 · POR QUÊ", "title": ["Muitos módulos", "precisam dele."], "body": "Para ficar sempre alimentados.", "cena": "Interruptor inteligente de vidro com teclas iluminadas suavemente em parede neutra, luz quente."},
    {"kicker": "03 · QUANDO", "title": ["Antes da", "fiação passar."], "body": "Previsto no projeto elétrico.", "cena": "Obra com eletrodutos chegando às caixinhas na parede antes do reboco, luz quente de fim de tarde."},
    {"kicker": "04 · CONFERIR", "title": ["Combine com", "o eletricista."], "body": "Em cada ponto que terá automação.", "cena": "Planta elétrica sobre bancada com régua e lápis, luz quente, sem textos legíveis."},
    {"kicker": "05 · RESULTADO", "title": ["Automação", "sem limite depois."], "body": "Um item simples evita retrabalho.", "cena": "Living de alto padrão finalizado com teclado de automação elegante na parede, luz quente."}]},
  "story": {"kicker": "RESPONDA", "title": ["Sua obra já", "prevê o neutro?"], "body": "Sim · Não sei · Ainda não", "cena": "Interruptor touch de vidro preto com leds suaves em parede de madeira."}},

 {"data": "2026-11-20",
  "reel": {"tema": "Som por zonas (multiroom)", "titulo": "Cada ambiente com a sua música.",
   "scenes": [
    {"kicker": "SOM POR ZONAS", "title": "Cada ambiente com|a sua música.", "cena": "Vista ampla de casa de alto padrão integrada, living, cozinha e varanda, com caixas de som embutidas discretas no forro, luz quente."},
    {"kicker": "01 · LIVING", "title": "Jazz baixinho|na sala.", "cena": "Living de alto padrão com poltrona de leitura, vitrola e luz quente, caixas embutidas no forro."},
    {"kicker": "02 · COZINHA", "title": "Playlist animada|na cozinha.", "cena": "Cozinha gourmet de alto padrão com ilha de mármore, ingredientes frescos, luz pendente quente."},
    {"kicker": "03 · VARANDA", "title": "Bossa nova|na varanda.", "cena": "Varanda com vista para o mar ao entardecer, sofá externo e caixas de som externas discretas."},
    {"kicker": "04 · SUÍTE", "title": "Silêncio|onde você quiser.", "cena": "Suíte master tranquila em luz baixa, cama arrumada, cortinas de linho."}],
   "legenda": "Cada ambiente com a sua música.\n\nNo som por zonas (multiroom), a casa inteira fica conectada, mas cada ambiente escolhe o que toca:\n01 · Jazz baixinho na sala.\n02 · Playlist animada na cozinha.\n03 · Bossa nova na varanda.\n04 · Silêncio onde você quiser.\n\nQue música tocaria na sua varanda agora?\n\n" + FECHO + "\n\nImagens conceito.\n\n#Multiroom #SomAmbiente #Sonorização #CasaInteligente #Brusque #MOVE"},
  "post": {"formato": "feed", "tema": "Living integrado", "legenda": "Som, luz e cortinas em harmonia.\n\nNo living integrado, cada sistema conversa com o outro: a luz muda de cena, as cortinas acompanham o sol e o som ocupa o espaço sem nada aparente. Projeto que se percebe pelo conforto.\n\nQual destes você mais usaria: som, luz ou cortinas?\n\n" + FECHO + "\n\nAmbiente conceito.\n\n#LivingIntegrado #ArquiteturaDeInteriores #AutomaçãoResidencial #Iluminação #AltoPadrão #MOVE",
   "slides": [{"kicker": "LIVING INTEGRADO", "title": ["Som, luz e cortinas", "em harmonia."], "body": "Tudo integrado, nada aparente.", "cena": "Living integrado de apartamento de alto padrão com pé-direito duplo, cortinas de linho, sofá modular, luz quente em cena e vista para o mar ao anoitecer."}]},
  "story": {"kicker": "RESPONDA", "title": ["Som, luz ou", "cortinas?"], "body": "Qual você automatizaria primeiro?", "cena": "Detalhe de cortina de linho parcialmente aberta com luz dourada entrando em living elegante."}},

 {"data": "2026-11-21",
  "reel": {"tema": "Gourmet e piscina: dia de receber", "titulo": "A festa começa antes do primeiro convidado.",
   "scenes": [
    {"kicker": "DIA DE RECEBER", "title": "A festa começa|antes do convidado.", "cena": "Espaço gourmet de alto padrão com churrasqueira, bancada de pedra e mesa posta, integrado à área de piscina ao entardecer."},
    {"kicker": "01 · LUZ", "title": "A iluminação|entra em cena.", "cena": "Área gourmet ao anoitecer com pendentes quentes acesos sobre a bancada e luz no paisagismo."},
    {"kicker": "02 · SOM", "title": "A trilha toca|no gourmet e na piscina.", "cena": "Piscina iluminada à noite com caixas de som externas discretas no paisagismo, deck de madeira."},
    {"kicker": "03 · MESA", "title": "Tudo pronto|para receber.", "cena": "Mesa posta elegante com taças, louças e flores na varanda gourmet, luz âmbar."},
    {"kicker": "04 · NOITE", "title": "E a noite|segue leve.", "cena": "Vista ampla da área de piscina e gourmet à noite, iluminação cênica quente, céu azul profundo."}],
   "legenda": "A festa começa antes do primeiro convidado.\n\nEm dia de receber, a casa se prepara junto com você:\n01 · A iluminação do gourmet e do jardim entra em cena.\n02 · O som toca no gourmet e na piscina, cada um no seu volume.\n03 · Tudo pronto para a mesa.\n04 · E a noite segue leve.\n\nQuem você chamaria para estrear um espaço assim? Marque aqui.\n\n" + FECHO + "\n\nImagens conceito.\n\n#EspaçoGourmet #ÁreaDePiscina #SomAmbiente #Receber #BalneárioCamboriú #MOVE"},
  "post": {"formato": "feed", "tema": "Varanda à noite", "legenda": "A noite fica melhor com trilha sonora.\n\nNa varanda, as caixas embutidas no forro tocam no volume certo, a luz fica baixa e a vista faz o resto. Conforto que não aparece, mas se sente.\n\nVaranda é lugar de jantar, de vinho ou de música?\n\n" + FECHO + "\n\nAmbiente conceito.\n\n#Varanda #SomAmbiente #ApartamentoDecorado #Itapema #AltoPadrão #MOVE",
   "slides": [{"kicker": "VARANDA À NOITE", "title": ["A noite fica melhor", "com trilha sonora."], "body": "Som embutido no forro da varanda.", "cena": "Varanda de apartamento de alto padrão à noite com vista da orla iluminada, sofá externo, mesa baixa com taças de vinho, forro de madeira com caixas embutidas discretas, luz âmbar baixa."}]},
  "story": {"kicker": "DETALHE", "title": ["Volume certo,", "vista perfeita."], "body": "Som externo pensado para o vento e a maresia.", "cena": "Detalhe de forro de madeira de varanda com caixa de som embutida discreta e luz quente, mar ao fundo desfocado."}},

 {"data": "2026-11-22",
  "reel": {"tema": "Iluminação em cena", "titulo": "A luz certa muda o ambiente inteiro.",
   "scenes": [
    {"kicker": "ILUMINAÇÃO EM CENA", "title": "A luz certa muda|o ambiente inteiro.", "cena": "Living de alto padrão com iluminação cênica: sancas de luz indireta, abajures e spots direcionados em quadros, atmosfera quente."},
    {"kicker": "01 · RECEBER", "title": "Luz alta|para receber.", "cena": "Sala de jantar de alto padrão bem iluminada com pendente escultural sobre mesa de madeira, luz quente plena."},
    {"kicker": "02 · JANTAR", "title": "Luz baixa|sobre a mesa.", "cena": "Mesa de jantar posta com luz pendente baixa e velas, ambiente íntimo, restante em penumbra."},
    {"kicker": "03 · CINEMA", "title": "Penumbra|para o filme.", "cena": "Sala de TV em penumbra com apenas luz indireta atrás do painel, atmosfera de cinema."},
    {"kicker": "04 · LEITURA", "title": "Foco onde|você precisa.", "cena": "Canto de leitura com poltrona de couro e luminária de piso direcionando luz, estante ao fundo."}],
   "legenda": "A luz certa muda o ambiente inteiro.\n\nCom iluminação em cena, o mesmo espaço vive momentos diferentes com um toque:\n01 · Luz alta para receber.\n02 · Luz baixa sobre a mesa.\n03 · Penumbra para o filme.\n04 · Foco para a leitura.\n\nQual dessas cenas é a sua cara? Conte nos comentários e salve.\n\n" + FECHO + "\n\nImagens conceito.\n\n#Iluminação #LuminotécnicaResidencial #CasaInteligente #DesignDeInteriores #AltoPadrão #MOVE"},
  "post": {"formato": "feed", "tema": "Hall de entrada com fechadura digital", "legenda": "Chegar em casa ficou mais simples.\n\nNo hall, a fechadura digital se integra à automação: ao destravar, a luz de entrada acende e a casa começa a se preparar. Praticidade com o acabamento à altura do projeto.\n\nVocê ainda anda com chave no bolso?\n\n" + FECHO + "\n\nAmbiente conceito.\n\n#FechaduraDigital #HallDeEntrada #CasaInteligente #AutomaçãoResidencial #AltoPadrão #MOVE",
   "slides": [{"kicker": "HALL DE ENTRADA", "title": ["Chegar em casa", "ficou mais simples."], "body": "Fechadura digital integrada à automação.", "cena": "Hall de entrada de apartamento de alto padrão com porta de madeira escura alta e fechadura digital preta elegante sem marca, console de mármore e arandela quente."}]},
  "story": {"kicker": "RESPONDA", "title": ["Chave, senha", "ou digital?"], "body": "Como você entra em casa hoje?", "cena": "Close de fechadura digital preta fosca em porta de madeira escura, luz quente rasante, sem marca."}},

 {"data": "2026-11-23",
  "reel": {"tema": "Persianas automatizadas", "titulo": "A luz natural no seu tempo.",
   "scenes": [
    {"kicker": "PERSIANAS", "title": "A luz natural|no seu tempo.", "cena": "Living de alto padrão com grandes janelas e persianas de madeira automatizadas parcialmente abertas, feixes de luz dourada da manhã."},
    {"kicker": "01 · MANHÃ", "title": "Abrem com|o primeiro sol.", "cena": "Suíte com persiana abrindo e luz suave da manhã entrando, roupa de cama clara."},
    {"kicker": "02 · TARDE", "title": "Filtram o calor|da tarde.", "cena": "Sala de estar com persianas semiabertas criando listras de luz no piso de madeira, tarde quente."},
    {"kicker": "03 · TELA", "title": "Sem reflexo|na hora do filme.", "cena": "Sala de TV com persianas fechadas e luz indireta suave, ambiente escuro elegante."},
    {"kicker": "04 · NOITE", "title": "Fecham sozinhas|ao anoitecer.", "cena": "Living ao anoitecer com persianas fechadas e luz quente interna acesa, aconchegante."}],
   "legenda": "A luz natural no seu tempo.\n\nPersianas e cortinas automatizadas acompanham a sua rotina:\n01 · Abrem com o primeiro sol.\n02 · Filtram o calor da tarde.\n03 · Fecham na hora do filme.\n04 · Fecham sozinhas ao anoitecer.\n\nVocê prefere acordar com luz natural ou no escuro total?\n\n" + FECHO + "\n\nImagens conceito.\n\n#Persianas #AutomaçãoDeCortinas #CasaInteligente #LuzNatural #ArquiteturaDeInteriores #MOVE"},
  "post": {"formato": "carrossel", "tema": "Checklist antes do forro", "legenda": "6 itens para não esquecer na sua obra.\n\nAntes de fechar o forro, vale conferir:\n01 · Pontos de som marcados na planta.\n02 · Cabos de som e rede passados e identificados.\n03 · Fio neutro nas caixinhas de interruptor.\n04 · Pontos de acesso Wi-Fi no teto.\n05 · Infra para cortinas e persianas.\n06 · Rack técnico com ventilação.\n\nSalve este checklist e envie para o seu arquiteto.\n\n" + FECHO + "\n\nAmbientes conceito.\n\n#ChecklistDeObra #AntesDoForro #AutomaçãoResidencial #Sonorização #ObraDeAltoPadrão #MOVE",
   "slides": [
    {"kicker": "CHECKLIST DE OBRA", "title": ["6 itens antes", "do forro."], "body": "Salve para a sua obra →", "cena": "Obra de alto padrão com forro de gesso aberto e estrutura metálica, eletrodutos organizados, luz quente de fim de tarde.", "iamin_capa": True},
    {"kicker": "01 · SOM", "title": ["Pontos de som", "marcados."], "body": "Posição das caixas definida na planta.", "cena": "Caixas de som de embutir redondas posicionadas em forro aberto durante a obra, luz quente."},
    {"kicker": "02 · CABOS", "title": ["Cabos passados", "e identificados."], "body": "Som e rede até o rack.", "cena": "Cabos identificados com etiquetas saindo de eletrodutos em obra, close organizado, luz quente."},
    {"kicker": "03 · NEUTRO", "title": ["Fio neutro nas", "caixinhas."], "body": "Para os interruptores inteligentes.", "cena": "Caixinha elétrica embutida em parede com fios organizados, obra limpa, luz quente."},
    {"kicker": "04 · WI-FI", "title": ["Pontos de acesso", "no teto."], "body": "Um por área, ligados por cabo.", "cena": "Forro de gesso com ponto de acesso Wi-Fi branco circular discreto, luz rasante quente."},
    {"kicker": "05 · CORTINAS", "title": ["Infra para", "cortinas e persianas."], "body": "Energia e espaço no cortineiro.", "cena": "Cortineiro embutido em forro de gesso com cortina de linho, luz quente da tarde."},
    {"kicker": "06 · RACK", "title": ["Rack técnico", "com ventilação."], "body": "A central da casa bem planejada.", "cena": "Rack técnico organizado em armário de marcenaria escura com ventilação, luz quente."}]},
  "story": {"kicker": "DICA DA IAMIN", "title": ["Antes do forro,", "confira a lista."], "body": "Salve o post de hoje.", "cena": "Forro de gesso aberto em obra com estrutura metálica, luz dourada.", "iamin": True}},

 {"data": "2026-11-24",
  "reel": {"tema": "Obra: evolução", "titulo": "Cada etapa no lugar certo.", "obra": True,
   "scenes": [
    {"kicker": "EVOLUÇÃO DA OBRA", "title": "Cada etapa no|lugar certo.", "cena": "Vista aérea ao entardecer de prédio residencial de alto padrão na orla de Balneário Camboriú, mar e cidade iluminada."},
    {"kicker": "01 · ESTRUTURA", "title": "Primeiro,|o que não se vê.", "cena": "Apartamento em obra com estrutura de forro metálica exposta e eletrodutos, janelas amplas com vista para o mar."},
    {"kicker": "02 · INSTALAÇÃO", "title": "Depois, cada|ponto instalado.", "cena": "Ferramentas de instalação organizadas sobre pano em obra limpa, caixa de som de embutir ao lado, luz quente."},
    {"kicker": "03 · AJUSTE", "title": "Tudo testado|e configurado.", "cena": "Tablet sobre bancada de mármore em living quase pronto, tela escura sem textos, luz quente."},
    {"kicker": "04 · ENTREGA", "title": "Pronto para|viver.", "cena": "Living finalizado de alto padrão com vista para o mar ao entardecer, forro liso com caixas embutidas e luz em cena."}],
   "legenda": "Cada etapa no lugar certo.\n\nUm projeto de som e automação acompanha a obra do começo ao fim:\n01 · Primeiro, a infraestrutura que não se vê.\n02 · Depois, cada ponto instalado.\n03 · Tudo testado e configurado.\n04 · Entrega pronta para viver.\n\nQuer acompanhar a sua obra com a gente? Chama no direct.\n\n" + FECHO + "\n\n#EvoluçãoDaObra #ObraDeAltoPadrão #AutomaçãoResidencial #BalneárioCamboriú #Sonorização #MOVE"},
  "post": {"formato": "feed", "tema": "Suíte com cena Boa noite", "legenda": "Silêncio, penumbra e descanso.\n\nNa suíte, a cena “Boa noite” fecha as cortinas, baixa a luz até o mínimo e desliga o som da casa. O quarto fica pronto para o sono, sem levantar da cama.\n\nVocê dorme melhor no escuro total ou com uma luz baixinha?\n\n" + FECHO + "\n\nAmbiente conceito.\n\n#SuíteMaster #CenaBoaNoite #AutomaçãoResidencial #Descanso #AltoPadrão #MOVE",
   "slides": [{"kicker": "SUÍTE MASTER", "title": ["Silêncio, penumbra", "e descanso."], "body": "Cena Boa noite: cortinas, luz e som.", "cena": "Suíte master de alto padrão em penumbra, cabeceira estofada alta com fita de luz âmbar suave, cortinas blackout fechadas, roupa de cama de linho."}]},
  "story": {"kicker": "DETALHE", "title": ["Um toque", "ao lado da cama."], "body": "Teclado de cena na cabeceira.", "cena": "Close de teclado de automação elegante embutido na cabeceira de madeira ao lado da cama, luz âmbar baixa, sem textos."}},

 {"data": "2026-11-25",
  "reel": {"tema": "Controle pelo celular", "titulo": "Sua casa na palma da mão, conforme compatibilidade.",
   "scenes": [
    {"kicker": "CONTROLE NA MÃO", "title": "Sua casa na|palma da mão.", "cena": "Smartphone com tela escura sem textos sobre braço de sofá de linho em living de alto padrão ao anoitecer, luz quente."},
    {"kicker": "01 · LUZ", "title": "Cenas de luz|em um toque.", "cena": "Living de alto padrão com iluminação em cena quente, sancas e abajures, vista noturna."},
    {"kicker": "02 · SOM", "title": "A música de|cada ambiente.", "cena": "Cozinha integrada à noite com caixas de som embutidas discretas no forro, luz pendente quente."},
    {"kicker": "03 · CORTINAS", "title": "Cortinas abrindo|de onde você estiver.", "cena": "Cortinas de linho abertas parcialmente em living com vista para o mar ao entardecer."},
    {"kicker": "04 · DE LONGE", "title": "Tudo conferido,|mesmo fora de casa.", "cena": "Fachada de casa de alto padrão ao anoitecer com iluminação de paisagismo acesa, arquitetura contemporânea."}],
   "legenda": "Sua casa na palma da mão.\n\nCom a automação integrada, o celular vira o controle da casa, conforme a compatibilidade de cada equipamento:\n01 · Cenas de luz em um toque.\n02 · A música de cada ambiente.\n03 · Cortinas de onde você estiver.\n04 · Tudo conferido, mesmo fora de casa.\n\nO que você mais gostaria de controlar pelo celular?\n\n" + FECHO + "\n\nImagens conceito.\n\n#CasaInteligente #SmartHome #AutomaçãoResidencial #ControlePeloCelular #Blumenau #MOVE"},
  "post": {"formato": "feed", "tema": "Cinema ao ar livre na varanda", "legenda": "Sessão sob as estrelas.\n\nNa varanda, a tela desce do forro, a luz baixa e o som externo assume o filme. Um cinema ao ar livre pensado para o clima do litoral.\n\nQual filme você assistiria ao ar livre?\n\n" + FECHO + "\n\nAmbiente conceito.\n\n#CinemaAoArLivre #Varanda #HomeCinema #CasaDePraia #AltoPadrão #MOVE",
   "slides": [{"kicker": "CINEMA AO AR LIVRE", "title": ["Sessão sob", "as estrelas."], "body": "Tela, som externo e luz em cena.", "cena": "Varanda de casa de alto padrão à noite com tela de projeção grande descida do forro de madeira, sofás externos com mantas, céu estrelado, luz âmbar baixa."}]},
  "story": {"kicker": "RESPONDA", "title": ["Cinema na sala", "ou ao ar livre?"], "body": "Vote: sala · varanda", "cena": "Sofá externo com mantas e almofadas em varanda à noite, céu estrelado, luz âmbar."}},

 {"data": "2026-11-26",
  "reel": {"tema": "Bastidores MOVE: equipe em obra", "titulo": "Quem faz o invisível funcionar.", "obra": True,
   "scenes": [
    {"kicker": "BASTIDORES", "title": "Quem faz o|invisível funcionar.", "cena": "Ferramentas profissionais de instalação organizadas em maleta aberta sobre piso de obra limpa em apartamento de alto padrão, luz quente da janela."},
    {"kicker": "01 · PLANEJAR", "title": "Tudo começa|na planta.", "cena": "Planta arquitetônica sobre mesa de madeira com régua e lápis, luz quente rasante, sem textos legíveis."},
    {"kicker": "02 · INSTALAR", "title": "Cuidado em|cada detalhe.", "cena": "Close de caixa de som de embutir sendo encaixada em recorte perfeito no forro de gesso, sem pessoas visíveis, luz quente."},
    {"kicker": "03 · ORGANIZAR", "title": "Cabos limpos,|rack em ordem.", "cena": "Rack técnico finalizado e organizado com cabos penteados, marcenaria escura, luz quente."},
    {"kicker": "04 · ENTREGAR", "title": "O resultado|aparece no conforto.", "cena": "Living de alto padrão pronto ao anoitecer com luz em cena e vista para o mar."}],
   "legenda": "Quem faz o invisível funcionar.\n\nPor trás de uma casa que funciona no toque, existe um trabalho que quase ninguém vê:\n01 · Planejamento na planta.\n02 · Cuidado em cada instalação.\n03 · Cabos limpos e rack em ordem.\n04 · O resultado aparece no conforto.\n\nQuer ver mais bastidores das nossas obras? Comente “sim”.\n\n" + FECHO + "\n\n#Bastidores #EquipeMOVE #AutomaçãoResidencial #Sonorização #ObraDeAltoPadrão #MOVE"},
  "post": {"formato": "carrossel", "tema": "Perguntas frequentes", "legenda": "As dúvidas que mais ouvimos antes do projeto.\n\nReunimos as perguntas mais comuns de quem está planejando som, cinema e automação:\n01 · Preciso decidir tudo antes da obra?\n02 · Dá para fazer em apartamento pronto?\n03 · Vou depender de um app só?\n04 · E se eu quiser ampliar depois?\n05 · Como começa o projeto?\n\nFicou alguma dúvida? Deixe nos comentários ou chame no direct.\n\n" + FECHO + "\n\nAmbientes conceito.\n\n#PerguntasFrequentes #AutomaçãoResidencial #Sonorização #HomeTheater #CasaInteligente #MOVE",
   "slides": [
    {"kicker": "PERGUNTAS FREQUENTES", "title": ["As dúvidas antes", "do projeto."], "body": "Arraste para ver as respostas →", "cena": "Living de alto padrão ao anoitecer com poltrona e mesa lateral com planta arquitetônica enrolada, luz quente."},
    {"kicker": "01 · ANTES DA OBRA?", "title": ["O ideal é planejar", "antes do forro."], "body": "A infraestrutura fica pronta e escondida.", "cena": "Obra com forro aberto e eletrodutos organizados, luz quente de fim de tarde."},
    {"kicker": "02 · APARTAMENTO PRONTO?", "title": ["Dá, com soluções", "sob medida."], "body": "Cada caso é avaliado na visita.", "cena": "Apartamento pronto de alto padrão com living elegante, luz quente."},
    {"kicker": "03 · UM APP SÓ?", "title": ["Integração pensada", "para simplificar."], "body": "Conforme compatibilidade dos equipamentos.", "cena": "Smartphone de tela escura sem textos sobre mesa de mármore em living elegante, luz quente."},
    {"kicker": "04 · AMPLIAR DEPOIS?", "title": ["Projeto com", "espaço para crescer."], "body": "Infra prevista para novas etapas.", "cena": "Rack técnico organizado com espaço livre em marcenaria escura, luz quente."},
    {"kicker": "05 · COMO COMEÇA?", "title": ["Com uma conversa", "e a sua planta."], "body": "Agende pelo direct.", "cena": "Mesa de reunião de madeira com planta arquitetônica, xícaras de café e luz quente da tarde."}]},
  "story": {"kicker": "CAIXA DE PERGUNTAS", "title": ["Qual a sua dúvida", "sobre o projeto?"], "body": "Responda aqui que a gente explica.", "cena": "Living de alto padrão ao anoitecer, poltrona de couro e luz quente."}},
]
