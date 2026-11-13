---
name: leitura-projeto-move
description: Usar quando o João ou um cliente/arquiteto mandar planta, projeto arquitetônico, elétrico, luminotécnico, forro ou marcenaria (PDF, imagem, DWG/DXF) para ler, extrair pontos e montar o projeto de som, automação e rede da MOVE.
---

# Ler projeto e transformar em projeto MOVE

## 1. Como abrir os arquivos
- PDF: ler direto (texto e imagem de cada prancha; rasterizar em alta resolução para ver legendas e símbolos pequenos).
- Imagem/foto da planta: ler visualmente; pedir foto reta, inteira e nítida se estiver ruim.
- DXF: dá para processar em código (ezdxf: camadas, blocos, textos, cotas).
- DWG/Revit/SketchUp: pedir ao arquiteto exportação em PDF (vetorial, com escala) e, se possível, DXF.
- Sempre conferir o CARIMBO: cliente, endereço, prancha, escala, data e REVISÃO (usar a mais recente; perguntar se há revisão nova).

## 2. Conjunto de pranchas e o que tirar de cada uma
- Planta baixa/layout: ambientes, medidas, onde ficam TV, sofá, cama, mesa, bancada → posiciona caixas de som, telas, teclados.
- Planta de forro / teto refletido: rebaixos, sancas, cortineiros, alçapões, luminárias, difusores de ar → onde cabem caixas de embutir, motores de cortina, APs, sem conflitar com spots e dutos.
- Cortes e elevações (vistas): pé-direito, altura do forro rebaixado, altura de bancadas, janelas e portas → altura de tela/projetor, viabilidade de caixas no teto (pé-direito > ~3 m muda a solução), cortinas.
- Luminotécnico: circuitos, tipo de luminária, fitas LED, drivers, cenas previstas → define módulos/dimerização.
- Elétrico: pontos de luz, tomadas, interruptores, circuitos, quadro (QDC), diagrama unifilar, quadro de cargas → onde trocar interruptor por teclado, onde precisa neutro, carga dos circuitos, espaço no quadro.
- Marcenaria/detalhamento: rack/painel da TV, nichos, profundidades → ventilação do receiver (~50 cm de profundidade ideal, espaço livre acima), nicho do sub, passagem de cabos.
- Ar-condicionado/hidráulico/estrutural: dutos, tubulação, vigas → evitar conflito com caixas, trilhos e eletrodutos.

## 3. Ler a escala e as cotas
- Escala 1:50 = 1 cm no papel são 50 cm reais (2 cm = 1 m). 1:100 = 1 cm = 1 m. 1:25/1:20 = detalhes.
- Cotas em centímetros ou metros (ver nota da prancha). Preferir sempre a COTA escrita à medida feita com régua no desenho.
- Níveis (ex.: +0,00, −0,15) e pé-direito aparecem nos cortes.

## 4. Simbologia elétrica (padrão brasileiro de uso comum — NBR 5444, ainda muito usada; sempre confirmar na LEGENDA da prancha)
- Quadro de distribuição: retângulo preenchido. Ponto de luz no teto: círculo (com letra do comando e potência/circuito). Arandela: meio círculo na parede.
- Tomadas: triângulo; preenchimento vazio/meio/cheio indica altura (baixa, média, alta). Interruptores: símbolo com letra(s) que ligam aos pontos de luz de mesma letra (simples, paralelo/three-way, intermediário/four-way).
- Eletroduto: linha contínua = no teto/parede; tracejada = no piso. Riscos sobre a linha = fios (fase, neutro, retorno, terra).
- Alturas usuais de obra (confirmar no projeto): tomada baixa ~0,30 m; média/bancada ~1,10–1,20 m; alta (ar-condicionado) ~2,00–2,20 m; interruptor ~1,10–1,20 m.
- Leitura recomendada: legenda → quadro → circuitos → pontos → trajeto → unifilar → quadro de cargas → cruzar com arquitetônico/forro.

## 5. O que a MOVE marca na planta (projeto MOVE)
Legenda própria por cor/camada:
- Som: caixas de embutir (L, C, R, SL, SR, SBL/SBR, Atmos), sub, receiver/amplificador, zonas.
- Vídeo: TV/tela/projetor, HDMI e eARC, rack.
- Automação: teclados/keypads, módulos, motores de cortina (lado do motor), sensores, blasters IR, central.
- Rede: pontos de rede, APs, rack/patch panel, câmeras.
- Infraestrutura: tubulação (diâmetro), caixas, esperas, pontos de energia para motores/drivers, alçapões.
Gerar: planta marcada (PDF), lista de pontos com ambiente/altura/tipo, lista de tubulação para eletricista, observações para gesseiro (sancas, recortes, alçapões) e marceneiro (rack, nichos, ventilação), lista de materiais para orçamento.

## 6. Checklist de conflitos (achar antes da obra)
- Caixa de som em cima de viga, sob duto de ar ou colada em spot/luminária.
- Pé-direito duplo ou forro alto demais para caixas de teto.
- Sofá encostado na parede de trás sem lugar para surround.
- TV sem ponto de energia/HDMI/rede atrás; painel sem rebaixo para suporte articulado.
- Rack fechado sem ventilação; sub dentro do móvel.
- Cortineiro raso ou sem ponto de energia no lado do motor.
- Caixa de interruptor sem neutro onde vai teclado.
- Tubulação de dados junto com elétrica; sem caminho até o rack.
- Wi-Fi: rack num canto da casa e nenhum ponto para AP.

## 7. Limites
- Projeto elétrico (dimensionamento, quadro, disjuntores) é responsabilidade de engenheiro/técnico habilitado; a MOVE indica necessidades e compatibiliza, não assina elétrico.
- Não divulgar plantas/endereço do cliente em conteúdo; borrar se aparecer.
- Dados pessoais da planta (nome, endereço) ficam só no projeto.
