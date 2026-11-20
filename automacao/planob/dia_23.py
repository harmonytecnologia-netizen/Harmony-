"""23/11 (segunda): feed obra real Balneário (sala de cinema), carrossel REDE 'cabo mal crimpado' (capa = quadro do Reel 3D),
stories 09h (bastidor real Florianópolis), 15h (enquete viagem/simulação de presença), 21h (cena Boa noite).
Imagens: ChatGPT (img_1123) + quadros reais (ballneario/VID-20240902-WA0023, floripa/VID-20250317-WA0129) + quadros do Reel 3D rj45."""
import sys, os
R = os.path.abspath(os.path.dirname(__file__) + '/../..'); sys.path.insert(0, R + '/automacao/scripts')
import premium as P
from carrossel_3d import slide, story3d, VERM
from PIL import Image
I = R + '/automacao/planob/img_1123/'; OUT = R + '/fila/2026-11-23/'; os.makedirs(OUT, exist_ok=True)
def f(n): return Image.open(I + n).convert('RGB')
# 12h feed + story (obra real)
P.feed(f('bal_cinema.jpg'), 'OBRA REAL · BALNEÁRIO CAMBORIÚ', ['Você trocaria a TV', 'por uma tela assim?'], 'Projeção, som no forro e LED no ripado.', OUT + 'feed.jpg')
P.story(f('bal_cinema.jpg'), 'NOVO POST · OBRA REAL', ['Você trocaria', 'a TV por uma', 'tela assim?'], 'Veja no feed como ficou.', OUT + 'story_feed.jpg')
# 19h carrossel 6 (REDE)
if os.path.exists(I + 'c1_3d.jpg'):
    slide(f('c1_3d.jpg'), None, 'REDE · CABO MAL CRIMPADO', ['500 mega no plano,', '94 no cabo?'], 'Arrasta: o culpado cabe na mão', OUT + 'carrossel_1.jpg', 1, 6)
    story3d(f('c1_3d.jpg'), 'NOVO CARROSSEL NO FEED', ['500 mega no', 'plano, 94', 'no cabo?'], 'O culpado cabe na mão.', OUT + 'story_carrossel.jpg')
slide(f('c2.jpg'), '01', 'CONECTOR MAL CRIMPADO', ['Um par solto derruba', 'o cabo para 100 Mb.'], 'O gigabit usa os 4 pares. Faltou um,|a placa conecta a 100.', OUT + 'carrossel_2.jpg', 2, 6, cor_num=VERM)
slide(f('c3.jpg'), '02', 'O JEITO CERTO', ['8 fios na ordem,', 'até o fim.'], 'Mesmo padrão nas duas pontas|e a capa presa pela trava.', OUT + 'carrossel_3.jpg', 3, 6)
slide(f('c4.jpg'), '03', 'TESTE ANTES DE FECHAR', ['As 8 luzes', 'têm que acender.'], 'Testador em cada ponto: é rápido|e evita abrir parede depois.', OUT + 'carrossel_4.jpg', 4, 6)
slide(f('c5.jpg'), '04', 'O QUE É FIXO, NO CABO', ['TV, console e', 'escritório no cabo.'], 'Cabo do rack até cada ponto fixo.|O Wi-Fi fica livre para o celular.', OUT + 'carrossel_5.jpg', 5, 6)
if os.path.exists(I + 'c6_3d.jpg'):
    slide(f('c6_3d.jpg'), None, 'O JEITO CERTO', ['Rede pensada', 'antes da obra.'], 'Rack, cabos e pontos no projeto,|tudo testado. Fale com a MOVE.', OUT + 'carrossel_6.jpg', 6, 6)
# stories próprios
P.story(f('flo_terraco.jpg'), 'SEGUNDA · BASTIDOR REAL', ['A semana', 'começa', 'na obra.'], 'Obra em Florianópolis.', OUT + 'story_09h_1.jpg')
story3d(f('s15.jpg'), 'ENQUETE · RESPONDE NO DIRECT', ['Viajando, sua casa', 'parece ocupada?'], 'O jeito certo está no Reel de hoje.', OUT + 'story_15h_1.jpg', extra=['SIM', 'NÃO', 'NUNCA PENSEI'])
P.story(f('s21.jpg'), 'SEGUNDA À NOITE', ['Um toque', 'e a casa', 'dorme.'], 'Cena "Boa noite": luz baixa e cortina fechando.', OUT + 'story_21h_1.jpg')
print('ok 23/11')
