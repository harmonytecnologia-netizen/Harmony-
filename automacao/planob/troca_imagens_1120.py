"""20/11: carrossel 'Faltou luz' e enquete 15h refeitos sem repetir o mesmo quadro 3D (pedido do João 17/11).
Imagens novas do ChatGPT em automacao/planob/img_1120/. Slide 6 (obra real) mantido."""
import sys, os
R = os.path.abspath(os.path.dirname(__file__) + '/../..'); sys.path.insert(0, R + '/automacao/scripts')
from carrossel_3d import slide, story3d, VERM
from premium import KICK
from PIL import Image
I = R + '/automacao/planob/img_1120/'; OUT = R + '/fila/2026-11-20/'
def f(n): return Image.open(I + n).convert('RGB')
slide(f('capa_apagao.jpg'), None, 'SEGURANÇA · 5 PONTOS', ['Faltou luz.', 'Sua casa fica cega?'], 'Arrasta para conferir o que precisa|continuar ligado.', OUT + 'carrossel_1.jpg', 1, 6)
slide(f('s01_gravador.jpg'), '01', 'CÂMERAS E GRAVADOR', ['Sem energia,', 'sem imagem.'], 'A queda de luz é justamente quando|a casa fica mais vulnerável.', OUT + 'carrossel_2.jpg', 2, 6, cor_num=VERM)
slide(f('s02_internet.jpg'), '02', 'WI-FI E INTERNET', ['O alerta não', 'chega ao celular.'], 'Roteador e switch desligados = câmera|sem acesso remoto.', OUT + 'carrossel_3.jpg', 3, 6, cor_num=VERM)
slide(f('s03_nobreak.jpg'), '03', 'A SOLUÇÃO', ['Nobreak', 'no rack.'], 'Mantém câmeras, gravador e rede|ligados e protege contra picos.', OUT + 'carrossel_4.jpg', 4, 6)
slide(f('s04_dimensionar.jpg'), '04', 'DIMENSIONAMENTO', ['Potência × tempo', 'de bateria.'], 'Some o consumo dos aparelhos e defina|quanto tempo precisa segurar.', OUT + 'carrossel_5.jpg', 5, 6)
story3d(f('capa_apagao.jpg'), 'NOVO CARROSSEL NO FEED', ['Faltou luz.', 'Sua casa', 'fica cega?'], '5 pontos para conferir no seu rack.', OUT + 'story_carrossel.jpg')
story3d(f('st15_camera_pousada_real.jpg'), 'ENQUETE · RESPONDE NO DIRECT', ['Faltou luz agora:', 'sua câmera', 'continua gravando?'], 'Às 19h tem Reel mostrando a solução.', OUT + 'story_15h_2.jpg', extra=['SIM', 'NÃO', 'NÃO SEI'])
print('ok 20/11')
