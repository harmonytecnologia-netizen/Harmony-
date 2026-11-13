---
name: automacao-residencial-move
description: Usar ao projetar, explicar, vender ou responder dúvidas sobre automação residencial/corporativa da MOVE — iluminação, cortinas, clima, cenas, protocolos (Matter, Zigbee, Z-Wave, KNX, Wi-Fi), centrais e infraestrutura elétrica.
---

# Automação residencial — MOVE
Complementa: som-home-theater-move (áudio), redes-move (rede), leitura-projeto-move (plantas). Preço/prazo/marca final só o João.

## 1. O que é (para explicar ao cliente)
Automação = a casa obedecer a CENAS, não só "ligar pelo celular". Ex.: "Chegar" (acende hall e cozinha, abre cortina, liga o som baixinho), "Cinema" (apaga luzes, fecha blackout, desce tela, liga receiver), "Jantar", "Dormir" (desliga tudo, fecha tudo, ativa alarme), "Sair". Controle por teclado na parede, app, voz (Alexa/Google/Siri) e horários/sensores.

## 2. O que automatizar (escopo típico)
- Iluminação: liga/desliga e dimerização por circuito; fitas LED em sanca/marcenaria; cenas.
- Cortinas e persianas motorizadas (trilho para cortina de tecido; motor tubular para rolô/blackout; toldos externos).
- Clima: ar-condicionado por infravermelho (blaster IR) ou integração Wi-Fi/VRF.
- Áudio multiroom e home theater (receiver/amplificador na rede).
- Segurança: câmeras, fechadura digital, sensores de porta/presença, alarme, interfone/vídeo porteiro.
- Outros: irrigação, piscina (bomba, aquecimento, iluminação), portão, tomadas inteligentes, aquecedor.

## 3. Tecnologias (2026) e quando usar
- Matter (padrão universal que conversa com Apple/Google/Alexa/SmartThings) sobre Thread (mesh de baixo consumo, precisa "border router") ou Wi-Fi. Preferir dispositivos Matter em compras novas.
- Zigbee: maduro, barato, mesh (dispositivos na tomada repetem sinal), precisa hub/coordenador; usa 2,4 GHz (escolher canal longe do Wi-Fi).
- Z-Wave: sub-GHz, sem disputa com Wi-Fi, muito confiável para fechaduras e sensores; mais caro, comprar versão da região.
- Wi-Fi: sem hub, bom para câmeras e aparelhos de energia; muitos dispositivos Wi-Fi sobrecarregam a rede (por isso rede bem projetada).
- Cabeado (KNX e sistemas proprietários de alto padrão como Control4, Savant, Crestron; ou módulos na central/quadro): mais robusto e sem pilha/sinal, exige planejamento antes do gesso. Ideal para obra nova de alto padrão.
- Plataforma/central: app do fabricante (simples) → hub (SmartThings, Home Assistant, Hubitat) → central profissional. Regra MOVE: um só app para o cliente, com cenas prontas; nada de 6 apps diferentes.
- Sempre funcionar SEM internet para o básico (teclado na parede acende luz mesmo com internet caída).

## 3b. Wi-Fi x Zigbee x Cabeada — como decidir (Play Casa Inteligente)
- Wi-Fi: cada dispositivo conecta direto no roteador/AP (só 2,4 GHz) e na nuvem. Simples e barato, bom para casa/apartamento pequeno com poucos itens. Muitos dispositivos pesam no roteador e dependem de cobertura em todo canto → exige rede bem projetada (redes-move).
- Zigbee: um HUB (ligado no roteador por cabo, ou Wi-Fi) conversa com todos os dispositivos numa rede própria; para o roteador é 1 aparelho só. Rede mesh: um dispositivo repassa o sinal do outro, então alcança longe sem mais roteadores. Escala melhor e é modular (começa por um cômodo e cresce). Zigbee usa principalmente 2,4 GHz (existem variantes sub-GHz pouco comuns) — ajustar canal para não brigar com o Wi-Fi.
- Cabeada/centralizada (quadro de automação): módulos ficam num QUADRO em área técnica de fácil acesso (lavanderia, depósito, circulação), ligados às cargas por cabo; na parede ficam KEYPADS (teclados) que só mandam comando ao quadro. Quando usar:
  - cargas grandes (lustres, muitos metros de fita LED, dimerização pesada) cujo módulo/dimmer não cabe na caixinha 4x2;
  - motores maiores (contatores), fontes de LED e fontes dimerizáveis organizadas no quadro;
  - muitos circuitos de iluminação, casa grande, distâncias longas (sem oscilação de sinal);
  - cliente decidido a automatizar a casa toda desde a obra;
  - integração forte com áudio/vídeo (receivers, projetor, zonas de som) — centrais profissionais têm drivers e processamento para isso; Zigbee/Wi-Fi "travam" em projetos grandes.
- Keypads: cada tecla programável (1 toque = cena A, segurar = cena B, 2 toques = cena C), modelos de design, com gravação/iluminação nas teclas — o arquiteto escolhe acabamento.
- Regra de bolso MOVE:
  - Apartamento/reforma, poucos pontos, cliente quer começar aos poucos → Zigbee/Matter-Thread (modular), Wi-Fi só para itens pontuais.
  - Obra nova alto padrão, casa grande, muita iluminação dimerizável, home theater e som integrados → cabeada/centralizada com keypads (+ rádio só onde não der cabo).
  - Sempre combinar carga x módulo (potência do driver/dimmer compatível com a carga).

## 4. Infraestrutura elétrica (combinar com o eletricista ANTES do gesso)
- Neutro em todas as caixas de interruptor (a maioria dos módulos/teclados inteligentes exige neutro).
- Caixas 4x2 mais profundas (ou 4x4) onde vão módulos; evitar caixa lotada de fios.
- Circuitos de iluminação separados por "grupo de cena" (não juntar sanca + spots + pendente no mesmo circuito se precisarem acender separados).
- LED: driver compatível com o tipo de dimerização escolhido (dimmer de corte de fase/TRIAC, 0‑10 V, DALI ou PWM para fita 12/24 V). Driver em local acessível para manutenção (alçapão no forro, nicho).
- Cortinas: ponto de energia no forro/sanca na ponta do trilho onde fica o motor (lado definido no projeto); sanca/cortineiro com profundidade para trilho duplo (blackout + voil), em geral ≥ 15–20 cm, e altura livre conforme o trilho; persiana rolô: ponto no topo, lado do motor. Medir vão real depois do reboco.
- Ar-condicionado: blaster IR com linha de visada para a evaporadora, ou ponto de rede/integração do fabricante.
- Central/quadro de automação: perto do rack de rede, ventilado, com tomadas e nobreak; tubulação seca ligando quadro de automação ↔ rack ↔ quadro elétrico.
- Sensores de presença/abertura: ponto e tubulação se forem cabeados.
- Fechadura/vídeo porteiro/portão: tubulação até o rack (cabo de rede) e alimentação.
- Deixar ESPERAS (tubulação vazia com guia) para expansão futura; é barato na obra e caríssimo depois.
- Eletricista executa elétrica conforme NBR 5410; MOVE define pontos e passa cabos de baixa tensão/dados.

## 5. Projeto de automação (o que a MOVE entrega)
1. Entrevista: rotina da família, ambientes, cenas desejadas, nível de investimento, marcas da obra.
2. Planta de pontos: teclados, módulos, motores de cortina, sensores, blasters, caixas de som, APs, câmeras, rack.
3. Lista de infraestrutura para eletricista/gesseiro/marceneiro (pontos, alturas, tubulação, neutro, sancas, nichos).
4. Lista de materiais e orçamento (João).
5. Instalação, programação de cenas, treinamento do cliente, manual simples e suporte.
6. Pós-venda: ajustes de cena, atualizações, manutenção.

## 6. Problemas comuns e como evitar
- Sem neutro na caixa → módulo não funciona/pisca. Prever neutro.
- LED piscando/zumbindo com dimmer → driver incompatível. Testar antes.
- Wi-Fi fraco → dispositivos "offline". Projetar rede (redes-move).
- Muitos apps → cliente desiste. Centralizar.
- Cortina com trilho curto/sanca rasa → refazer. Medir no projeto.
- Tudo dependente de internet → casa "trava". Priorizar controle local.

## 7. Argumentos de venda (honestos)
Conforto (um toque), segurança (simular presença, câmeras, alertas), economia (desligar tudo ao sair, cortina contra calor), valorização do imóvel, acessibilidade (idosos), e principalmente: planejar agora custa uma fração de quebrar depois.
