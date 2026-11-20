"""22/11 (domingo): feed obra real House Beer, carrossel 'Home cinema: 5 erros que roubam o som do filme',
stories 09h (domingo + bastidor real), 15h (enquete surround), 21h (cinema de domingo). Imagens: ChatGPT (img_1122) + fotos reais House Beer."""
import sys, os
R = os.path.abspath(os.path.dirname(__file__) + '/../..'); sys.path.insert(0, R + '/automacao/scripts')
import premium as P
from carrossel_3d import slide, story3d, VERM
from PIL import Image
I = R + '/automacao/planob/img_1122/'; OUT = R + '/fila/2026-11-22/'; os.makedirs(OUT, exist_ok=True)
def f(n): return Image.open(I + n).convert('RGB')
# 12h feed + story (obra real)
P.feed(f('hb_salao.jpg'), 'OBRA REAL · HOUSE BEER', ['Som de bar que não', 'briga com a conversa.'], 'Caixas no forro e volume certo em cada canto.', OUT + 'feed.jpg')
P.story(f('hb_salao.jpg'), 'NOVO POST · OBRA REAL', ['Som de bar', 'que não briga', 'com a conversa.'], 'Veja no feed como ficou.', OUT + 'story_feed.jpg')
# 19h carrossel 6
slide(f('c1.jpg'), None, 'HOME CINEMA · 4 ERROS', ['4 erros que roubam', 'o som do filme.'], 'Arrasta e confere quantos', OUT + 'carrossel_1.jpg', 1, 6)
slide(f('c2.jpg'), '01', 'SURROUND NO CHÃO', ['O som bate no sofá', 'e se perde.'], 'Laterais, um pouco atrás e|30–60 cm acima do ouvido.', OUT + 'carrossel_2.jpg', 2, 6, cor_num=VERM)
slide(f('c3.jpg'), '02', 'SUB PRESO NO MÓVEL', ['Grave embolado', 'e móvel vibrando.'], 'Sub precisa de ar: fora do nicho|ou em nicho ventilado e aberto.', OUT + 'carrossel_3.jpg', 3, 6, cor_num=VERM)
slide(f('c4.jpg'), '03', 'TV ALTA DEMAIS', ['Pescoço cansado', 'no meio do filme.'], 'O centro da tela perto da altura|dos olhos de quem está sentado.', OUT + 'carrossel_4.jpg', 4, 6, cor_num=VERM)
slide(f('c5.jpg'), '04', 'SALA SÓ DE VIDRO E PISO', ['Eco que embola', 'os diálogos.'], 'Tapete, cortina e painéis de tecido|deixam a voz clara.', OUT + 'carrossel_5.jpg', 5, 6, cor_num=VERM)
slide(f('c6.jpg'), None, 'O JEITO CERTO', ['Projeto antes', 'da obra.'], 'Posição das caixas, infra e acústica|pensadas juntas. Fale com a MOVE.', OUT + 'carrossel_6.jpg', 6, 6)
story3d(f('c1.jpg'), 'NOVO CARROSSEL NO FEED', ['4 erros que', 'roubam o som', 'do filme.'], 'Quantos tem na sua sala?', OUT + 'story_carrossel.jpg')
# stories próprios
P.story(f('s09.jpg'), 'DOMINGO', ['Café, mar', 'e a playlist', 'certa.'], 'Som no forro, sem caixa à vista.', OUT + 'story_09h_1.jpg')
P.story(f('hb_bastidor.jpg'), 'BASTIDOR · OBRA REAL', ['Antes de abrir', 'as portas.'], 'Instalação de som na House Beer.', OUT + 'story_09h_2.jpg')
story3d(f('s15.jpg'), 'ENQUETE · RESPONDE NO DIRECT', ['Sua surround', 'está onde?'], 'O lugar certo está no Reel de hoje.', OUT + 'story_15h_1.jpg', extra=['NO CHÃO', 'NA PAREDE', 'NÃO TENHO'])
P.story(f('s21.jpg'), 'DOMINGO À NOITE', ['Pipoca pronta.', 'Qual filme', 'hoje?'], 'Responde no direct.', OUT + 'story_21h_1.jpg')
print('ok 22/11')
