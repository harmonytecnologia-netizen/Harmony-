# Lote 13/11 a 26/11/2026 — status (execução de 12/11)

**Bloqueio:** as pastas `C:\Users\PC\Downloads` e `C:\Users\PC\Videos` não estavam conectadas a esta execução e o pedido de acesso falhou
("janela do app Claude não disponível"). Sem isso não dá para trazer as imagens do ChatGPT, baixar músicas nem ler os vídeos de obra.

**O que ficou pronto:**
- Roteiro completo dos 14 dias (Reel 12h com 5 cenas, post 19h, story extra, legendas e hashtags): `lote_2026-11-13_a_26.py` (segue a planilha).
- Script que monta um dia inteiro a partir das imagens + música: `build_dia.py`.
- Imagens geradas no ChatGPT do João (uma conversa por dia, na ordem r1..r5, p1..pN, s1 do roteiro). Falta só baixar e trazer.

## Conversas do ChatGPT (imagens já geradas)
| Dia | Conversa |
|---|---|
| 13/11 | https://chatgpt.com/c/6af5d4c6-a86c-83e9-8867-0bc4580a4c3a (corredor saiu em 2 versões; usar a 1ª) |
| 14/11 | https://chatgpt.com/c/6af5da79-6438-83e8-8fae-3d8dc0bb6b45 |
| 15/11 | https://chatgpt.com/c/6af5dbea-af0c-83ea-a658-3629dbd692b3 |
| 16/11 | https://chatgpt.com/c/6af5dd38-9f68-83e9-9a73-e7f6baf9661b |
| 17/11 | https://chatgpt.com/c/6af5df95-ffb4-83e9-a9e2-b784433b606d |
| 18/11 | https://chatgpt.com/c/6af5e0cb-7414-83e9-b2cf-cc05abd1f313 |
| 19/11 | https://chatgpt.com/c/6af5e25d-3530-83e8-8297-450881f3c298 |
| 20/11 | https://chatgpt.com/c/6af5e525-992c-83e9-ab76-53385b17ac80 |
| 21/11 | https://chatgpt.com/c/6af5e700-03b4-83e9-814b-0464be2e1fe1 |
| 22/11 | https://chatgpt.com/c/6af5e8dd-b650-83e8-a66b-ab95dc401746 |
| 23/11 | https://chatgpt.com/c/6af5eae2-c5c8-83e9-93c4-e2ece9da999e |
| 24/11 | https://chatgpt.com/c/6af5ee26-dfd4-83e9-a8a5-bfcb6a72d063 |
| 25/11 | https://chatgpt.com/c/6af5eff7-0004-83e9-89ca-5ff59416ded0 |
| 26/11 | https://chatgpt.com/c/6af5f1c4-6bc0-83ea-ad5a-52ce47fd227c |

Ordem das imagens em cada conversa = ordem do roteiro: cenas do Reel (r1..r5), imagens do post 19h (p1..pN), story extra (s1).
Algumas mensagens saíram com 2 variações: usar a primeira.

## Para concluir (próxima execução com as pastas conectadas)
1. Baixar as imagens de cada conversa (ícone de download) e trazer de Downloads, salvando como r1..r5, p1..pN, s1.
2. Baixar 1 música nova por dia (YouTube Studio > Biblioteca de áudio; Jazz & Blues / Soul), nunca repetida do historico.md.
3. Conferir a pasta "MOVE para postar" para os dias 14, 18, 24 e 26 (Reel de obra); sem vídeo novo, usar o Reel conceito do roteiro.
4. `python3 automacao/lote/build_dia.py AAAA-MM-DD <pasta> <musica.mp3> "<Faixa — Artista>"`, conferir quadros, commit/push, planilha e historico.md.
