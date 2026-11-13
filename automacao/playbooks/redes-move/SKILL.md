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

## 7. Entregáveis MOVE de rede
Planta com pontos de rede e APs, lista de tubulação para o eletricista, rack especificado, mapa de pontos testados, documento com nomes de rede (sem senhas) e diagrama simples, treinamento do cliente.
