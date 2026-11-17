"""Carrossel 'Fio neutro no interruptor' REFEITO a pedido do João (17/11/2026): cada slide com imagem própria.
Capa/01/03/04: ChatGPT do João (imagens conceito). 02/05: quadros reais da obra Mariscal (VID-20250918-WA0039.mp4, 7,3 s e 6,0 s).
Uso: python3 refeito_neutro_1117.py <pasta_imagens>"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arte import feed, story, check, REPO
from PIL import Image, ImageFilter, ImageDraw

SRC = sys.argv[1]
OUT = f'{REPO}/fila/2026-11-17/refeito_neutro'; os.makedirs(OUT, exist_ok=True)

def load(name, box=None, hide=None):
    im = Image.open(f'{SRC}/{name}').convert('RGB')
    if hide:  # apaga a marca do fabricante (inpaint só nos pixels claros do texto)
        import cv2, numpy as np
        a = np.array(im); x0, y0, x1, y1 = hide
        g = cv2.cvtColor(a[y0:y1, x0:x1], cv2.COLOR_RGB2GRAY)
        m = np.zeros(a.shape[:2], np.uint8); m[y0:y1, x0:x1] = (g > np.percentile(g, 55)).astype(np.uint8) * 255
        m = cv2.dilate(m, np.ones((5, 5), np.uint8))
        im = Image.fromarray(cv2.inpaint(a, m, 7, cv2.INPAINT_TELEA))
    if box: im = im.crop(box)
    return im.resize((1080, 1350), Image.LANCZOS) if im.size != (1080, 1350) else im

SL = [
 ('capa.png', None, None, 'DICA DE OBRA', ['Fio neutro no', 'interruptor.'], 'O detalhe que libera a automação →'),
 ('s01.png', None, None, '01 · O QUE É', ['O neutro chega', 'até a caixinha.'], 'Junto da fase, no ponto do interruptor.'),
 ('m02.jpg', (0, 150, 720, 1050), (420, 795, 525, 840), '02 · POR QUÊ', ['Muitos módulos', 'precisam dele.'], 'Para ficarem sempre alimentados.'),
 ('s03.png', None, None, '03 · QUANDO', ['Antes da', 'fiação passar.'], 'Previsto no projeto elétrico.'),
 ('s04.png', None, None, '04 · CONFERIR', ['Combine com', 'o eletricista.'], 'Em cada ponto que terá automação.'),
 ('m05.jpg', (0, 230, 720, 1130), (360, 845, 490, 900), '05 · RESULTADO', ['Um item simples', 'que evita retrabalho.'], 'Automação completa, sem quebra-quebra.'),
]
files = []
for i, (n, box, hide, k, t, b) in enumerate(SL, 1):
    check(t, 'feed'); fn = f'carrossel_{i}.jpg'
    feed(load(n, box, hide), k, t, b, f'{OUT}/{fn}'); files.append(fn)
c = SL[0]; story(load(c[0]), c[3], c[4], 'Novo carrossel no perfil. Arraste e salve.', f'{OUT}/story_carrossel.jpg')
print('ok', files)
