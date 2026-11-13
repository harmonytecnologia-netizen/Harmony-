---
name: redes-move
description: Usar ao projetar, explicar ou resolver rede de dados/Wi-Fi de casas, apartamentos e escritórios atendidos pela MOVE — cabeamento, rack, access points, PoE, VLAN para automação, câmeras e diagnóstico.
---

# Redes — MOVE
Rede é a base de tudo (automação, som em streaming, câmeras, TVs). Rede ruim = cliente acha que a automação é ruim.

## 1. Topologia padrão de alto padrão
Internet (operadora/ONU) → roteador/firewall próprio (não depender do aparelho da operadora; colocá-lo em modo bridge quando possível) → switch gerenciável PoE → access points (APs) no teto + pontos cabeados (TV, receiver, console, PC, central de automação, NVR de câmeras).
- Tudo concentrado num rack (8U–12U+) ventilado, com nobreak, régua de tomadas e organizador de cabos, em local acessível (não dentro de armário fechado sem ventilação).

## 2. Cabeamento (passar na obra)
- Cabo de rede Cat6 (Cat6A em casas grandes/futuro 10 Gb) de cada ponto até o rack, em topologia estrela (cada ponto um cabo, sem emendas).
- Pontos: cada AP (teto), cada TV, rack de som/receiver, escritório(s), central de automação, câmeras, vídeo porteiro, smart TV dos quartos, área gourmet; reserva extra.
- Tubulação exclusiva para dados (≥ 3/4", melhor 1"), separada da elétrica (não dividir eletroduto com energia; cruzar em 90°), curvas suaves, caixas de passagem, guia deixada.
- Limite de 90 m por lance (canal 100 m). Conectorizar padrão T568A ou T568B (o mesmo em toda a obra), patch panel no rack, identificar cada ponto (etiqueta igual na tomada e no patch panel).
- Testar cada cabo (testador; ideal certificar) e entregar planilha/mapa dos pontos.
- Fibra da operadora: prever tubulação da entrada até o rack.
- Normas de referência: NBR 14565 (cabeamento estruturado) e NBR 16264 (cabeamento estruturado residencial).

## 3. Wi-Fi
- Access points no TETO, cabeados (PoE), um sistema único com roaming (mesmo nome de rede em toda a casa). Evitar repetidores; "mesh" só com backhaul cabeado sempre que possível.
- Quantidade: em geral 1 AP por pavimento pequeno ou a cada ~70–100 m², mais um por área externa/gourmet; paredes de concreto/laje e vidro espelhado pedem mais. Fazer estudo de cobertura (site survey) quando possível.
- Padrão atual: Wi-Fi 6/6E, Wi-Fi 7 em projetos novos de alto padrão.
- Redes (SSIDs): Principal (família), Convidados (isolada), IoT/Automação (2,4 GHz, separada). Idealmente cada uma numa VLAN.
- Canais: 2,4 GHz em 1, 6 ou 11 com largura 20 MHz; 5 GHz 40/80 MHz; não colocar potência no máximo em todos os APs.

## 4. Configuração para automação e som
- IP fixo (reserva DHCP) para receiver, central de automação, NVR, hubs e impressoras.
- VLAN de IoT com acesso só ao necessário; mDNS/AirPlay/Chromecast funcionando entre redes quando o cliente precisar (configurar repetidor mDNS) — ou manter som e celulares na mesma rede para simplicidade.
- Receiver/streaming e TVs principais no CABO, não no Wi-Fi.
- Câmeras PoE em VLAN própria, gravando no NVR local; acesso remoto pelo app oficial com senha forte e 2FA.
- Atualizar firmware, trocar senhas padrão, desativar WPS e UPnP desnecessário. Senhas do cliente: o cliente cria/guarda (MOVE não guarda senha em texto).

## 5. Diagnóstico rápido (cliente reclamando)
1. Internet ou rede interna? Testar velocidade no cabo direto no roteador.
2. Sinal fraco num ponto? Medir RSSI (bom > −65 dBm). Falta AP ou AP mal posicionado.
3. Dispositivo cai? IP mudou (fixar), rede 2,4 GHz congestionada, canal ruim, dispositivo longe do hub/border router.
4. Tudo trava ao mesmo tempo? Roteador/switch travando, falta de energia (nobreak), loop de rede.
5. Reiniciar na ordem: ONU → roteador → switch → APs → dispositivos.

## 6. Equipamentos de mercado (referência, confirmar com fornecedor)
Linhas profissionais/prosumer comuns em projetos residenciais: Ubiquiti UniFi, TP-Link Omada, Aruba Instant On, Ruckus (alto padrão), MikroTik (roteamento). Switch PoE com orçamento de potência suficiente para APs + câmeras.

## 7. Wi-Fi a fundo (curso "Redes WiFi" — NASeros)
- Por que Wi-Fi satura: o ar é um MEIO COMPARTILHADO — num mesmo canal só um aparelho "fala" por vez (como a rede antiga de cabo coaxial com colisões). No cabo, cada aparelho tem sua "estrada" até o switch. Por isso: tudo que puder ir no cabo, vai no cabo.
- 2,4 GHz: faixa livre desde os micro-ondas → lotada (Bluetooth, controles, teclados, micro-ondas, vizinhos). Só ~60 MHz: 3 canais sem sobreposição (1, 6, 11) em 20 MHz; 40 MHz não cabe bem. Alcance maior e atravessa paredes melhor. Automação/IoT vive aqui.
- 5 GHz: muito mais espaço, canais de 20/40/80/160 MHz. DFS: parte dos canais é compartilhada com radares (meteorológicos/militares), que têm prioridade; o AP precisa escanear ao ligar (por isso o 5 GHz demora alguns minutos para aparecer) e troca de canal se detectar radar. TPC limita potência. Configurar o PAÍS correto no AP/roteador. Canais baixos (36–48) não têm DFS. Alcance menor que 2,4.
- 6 GHz (Wi-Fi 6E/7): faixa larga e limpa (no Brasil a Anatel liberou a faixa de 6 GHz), canais de 160 MHz (320 MHz no Wi-Fi 7), só aparelhos 6E/7 usam; alcance e penetração ainda menores → precisa de AP por ambiente.
- Wi-Fi 7 MLO (Multi-Link Operation): o aparelho usa 2,4 + 5 + 6 GHz ao mesmo tempo → mais velocidade e menos latência; exige cliente Wi-Fi 7.
- MU-MIMO e streams: "2x2, 4x4" (ou 2T2R) = número de fluxos/antenas de transmissão × recepção. AP com MU-MIMO conversa com vários aparelhos ao mesmo tempo (SU-MIMO atende um por vez e um aparelho lento atrasa todos). No Wi-Fi 5, MU-MIMO só em 5 GHz; no Wi-Fi 6 também em 2,4 (bom para muita automação). Firmware/processador bons pesam tanto quanto o número de antenas.
- Mesh ≠ roaming ≠ band steering:
  - Mesh = topologia (nós interligados entre si). Backhaul sem fio perde desempenho a cada salto (o mesmo ar é dividido); backhaul cabeado não perde.
  - Roaming = o aparelho passar de um AP para outro sem cair (protocolos 802.11k/v/r). Repetidor comum não faz isso: o celular "gruda" no repetidor longe com sinal ruim.
  - Band steering = 2,4/5/6 GHz com o mesmo nome; o AP decide a banda do aparelho.
- Mesh doméstico (Deco, Eero, Orbi, ZenWiFi…): plug-and-play, bonito, bom para casa de até ~4–6 nós; só funciona "inteligente" com nós da MESMA marca; pouco controle. Se misturar modelos, o mais potente fica na base e no meio do caminho (por onde passa todo o tráfego) e o mais fraco na ponta, senão vira gargalo. Preferir ligar os nós por cabo.
- Rede profissional (APs PoE no teto/parede + controladora): escala para dezenas/centenas de APs, VLANs, RADIUS, potência por AP, métricas e diagnóstico antes do problema virar reclamação → escolha MOVE para casa grande ou complexa (muitos dispositivos, automação, câmeras), escritório, pousada, área gourmet extensa. Preço próximo do mesh bom.
- Antenas: antena omnidirecional irradia em forma de "donut" perpendicular a ela. Antenas verticais cobrem bem o MESMO andar; para cobrir andar de cima/baixo, inclinar parte delas na horizontal. AP de teto (cobertura em cone para baixo) e AP de parede são modelos diferentes — escolher conforme a instalação. A posição da antena do aparelho também conta (notebook horizontal, TV vertical).
- Segmentação na prática: redes separadas por função — Principal, Convidados, Crianças, IoT/Automação, VPN — cada uma numa VLAN e sub-rede própria (ex.: 192.168.1.x e 192.168.53.x), sem enxergar as outras (teste: ping falha). Se um aparelho IoT ou o PC das crianças for infectado, não atinge o resto. Muitos roteadores atuais fazem isso com perfis prontos (ex.: ASUS Smart Home Master).
- Planejamento com software (heatmap): carregar a planta, calibrar a escala (ex.: porta = 0,80 m), marcar materiais das paredes (fina ~9 dB, média ~20 dB, concreto/vidro espelhado mais), deixar o software sugerir posição dos APs (ex.: Ruijie online gratuito com IA; profissionais: Ekahau, Hamina, UniFi Design Center), adicionar câmeras e switches PoE (conferir orçamento de potência PoE), traçar cabos e gerar lista de materiais + relatório PDF com mapas de calor 2,4/5/6 GHz → ótimo entregável para o cliente da MOVE.
- Saúde (objeção comum): Wi-Fi é radiação NÃO ionizante, de baixa potência e com limites definidos por norma; não tem a energia de raio X/ultravioleta. Responder com calma e base técnica, sem prometer o que não se sabe.

## 8. Entregáveis MOVE de rede
Planta com pontos de rede e APs, lista de tubulação para o eletricista, rack especificado, mapa de pontos testados, documento com nomes de rede (sem senhas) e diagrama simples, treinamento do cliente.
