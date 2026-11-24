"""28/11 (sábado): feed OBRA REAL (cliente Katia: espelho com perfil de LED), carrossel SOM 'ganho do amplificador' (capa = quadro do Reel 3D),
stories 09h (bastidor real obra Romanza), 15h (enquete etapa da obra), 21h (sexta de cinema).
Imagens: ChatGPT (img_1128: p7 cinema, p8 amplificador, p9 living) + quadros reais (cliente katia/VID-20250507-WA0020, romanza/VID-20250415-WA0071)
+ quadros 3D do Reel do ganho (g_*.jpg)."""
import sys, os
R = os.path.abspath(os.path.dirname(__file__) + '/../..'); sys.path.insert(0, R + '/automacao/scripts')
import premium as P
from carrossel_3d import slide, story3d, VERM
from PIL import Image
I = R + '/automacao/planob/img_1128/'; OUT = R + '/fila/2026-11-28/'; os.makedirs(OUT, exist_ok=True)
def f(n): return Image.open(I + n).convert('RGB')
# 12h feed + story (obra real)
P.feed(f('katia_espelho.jpg'), 'OBRA REAL · ILUMINAÇÃO', ['Espelho com luz que', 'não faz sombra.'], 'Perfil de LED no forro, alinhado à bancada.', OUT + 'feed.jpg')
P.story(f('katia_espelho.jpg'), 'NOVO POST · OBRA REAL', ['Luz que não', 'faz sombra', 'no rosto.'], 'Veja no feed como ficou.', OUT + 'story_feed.jpg')
# stories próprios
P.story(f('rom_obra_a.jpg'), 'SÁBADO · BASTIDOR REAL', ['Obra boa', 'começa antes', 'do forro.'], 'Infra pronta antes do acabamento.', OUT + 'story_09h_1.jpg')
story3d(f('rom_obra_b.jpg'), 'ENQUETE · RESPONDE NO DIRECT', ['Sua obra está', 'em qual etapa?'], 'A gente te diz o que pensar agora.', OUT + 'story_15h_1.jpg', extra=['FORRO', 'ACABAMENTO', 'MUDANÇA'])
P.story(f('p7.png'), 'SÁBADO À NOITE', ['Pipoca,', 'luz baixa', 'e cinema.'], 'Cena "Cinema": um toque e a sala se prepara.', OUT + 'story_21h_1.jpg')
# 19h carrossel 6 (SOM: ganho do amplificador)
if os.path.exists(I + 'g_capa.jpg'):
    slide(f('g_capa.jpg'), None, 'SOM · GANHO DO AMPLIFICADOR', ['Volume no meio', 'e já distorce?'], 'Arrasta: 3 sinais de ganho errado', OUT + 'carrossel_1.jpg', 1, 6, focus=0.45)
    story3d(f('g_capa.jpg'), 'NOVO CARROSSEL NO FEED', ['Volume no', 'meio e já', 'distorce?'], '3 sinais de ganho errado.', OUT + 'story_carrossel.jpg')
    slide(f('p8.png'), None, 'ANTES DE TUDO', ['Ganho não', 'é volume.'], 'Ele ajusta a sensibilidade da entrada.|No máximo, o amplificador satura cedo.', OUT + 'carrossel_2.jpg', 2, 6)
    slide(f('g_cortada.jpg'), '01', 'A ONDA É CORTADA', ['Distorce antes', 'da metade.'], 'Com ganho no máximo, o sinal bate no|limite do amplificador e é "cortado".', OUT + 'carrossel_3.jpg', 3, 6, cor_num=VERM)
    slide(f('g_clip.jpg'), '02', 'LUZ DE CLIP PISCANDO', ['O aparelho', 'está avisando.'], 'Clip ou proteção acendendo no ritmo|da música = ganho alto demais.', OUT + 'carrossel_4.jpg', 4, 6, cor_num=VERM)
    slide(f('p9.png'), '03', 'SOM QUE CANSA', ['Agudo ardido em', 'meia hora de música.'], 'Distorção cansa o ouvido e esquenta|o tweeter, mesmo com volume moderado.', OUT + 'carrossel_5.jpg', 5, 6, cor_num=VERM)
    slide(f('g_limpa.jpg'), None, 'O JEITO CERTO', ['Ganho só até', 'antes de distorcer.'], 'Fonte em ~80% e ganho ajustado no|volume mais alto que você usa. Fale com a MOVE.', OUT + 'carrossel_6.jpg', 6, 6)
print('ok 28/11')
