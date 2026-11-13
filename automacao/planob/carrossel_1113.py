"""Carrossel extra de 13/11 (sai às 21h): Projetor ou TV — responde a enquete do story."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arte import img, dark, feed, story, check, REPO
out = REPO + '/fila/2026-11-13'
FECHO = ("A MOVE projeta e integra som, cinema, iluminação e automação para casas e apartamentos de alto padrão "
         "no litoral norte de SC. Agende uma conversa e envie a planta do seu projeto.")
capa = ('site/img/hero.jpg', (0.3, 0.12, 1, 0.75))
sl = [('CINEMA EM CASA', ['Projetor ou TV:', 'qual escolher?'], 'Arraste para comparar →'),
      ('01 · TAMANHO', ['Tela muito grande', 'pede projetor.'], 'Imagens gigantes cabem melhor na projeção.', 'site/img/hero.jpg', (0, 0.1, 1, 0.6)),
      ('02 · LUZ', ['Sala clara', 'pede TV.'], 'Muita luz natural favorece a TV.', 'site/img/r_sala.jpg', None),
      ('03 · USO', ['Dia a dia ou', 'sessão de cinema?'], 'A frequência de uso muda a escolha.', 'anuncios/jornada/s6.png', None),
      ('04 · ESPAÇO', ['Distância', 'é projeto.'], 'Tela e projeção medidas na planta.', 'site/img/r_tv.jpg', None),
      ('05 · INTEGRAÇÃO', ['Os dois ficam', 'melhores com som.'], 'Som, luz e cortinas na mesma cena.', 'site/img/voz.jpg', None)]
files = []
k, t, b = sl[0]; check(t, 'feed'); feed(img(*capa), k, t, b, f'{out}/carrossel_1.jpg'); files.append('carrossel_1.jpg')
for i, (k, t, b, src, crop) in enumerate(sl[1:], 2):
    check(t, 'feed'); feed(dark(src, crop), k, t, b, f'{out}/carrossel_{i}.jpg'); files.append(f'carrossel_{i}.jpg')
story(img(*capa), sl[0][0], sl[0][1], 'Novo carrossel no perfil. Arraste e salve.', f'{out}/story_carrossel.jpg')
leg = ("Projetor ou TV? A resposta está na sua sala.\n\nOs dois funcionam muito bem, desde que combinem com o ambiente:\n01 · Tamanho de imagem que você quer.\n02 · Quanta luz natural a sala recebe.\n03 · Uso no dia a dia ou sessões de cinema.\n04 · Espaço e distância, medidos no projeto.\n05 · Integração com som, luz e cortinas.\n\nE você, time projetor ou time TV? Conte nos comentários e salve para o seu projeto.\n\n"
       + FECHO + "\n\nImagens conceito e projetos MOVE.\n\n#Projetor #HomeCinema #CinemaEmCasa #HomeTheater #AltoPadrão #Itapema #MOVE")
p = f'{out}/plano.json'; d = json.load(open(p))
d['21h'] = [{'acao': 'create_carousel_post', 'arquivos': files, 'legenda': leg}, {'acao': 'create_story', 'arquivo': 'story_carrossel.jpg'},
            {'acao': 'create_story', 'arquivo': 'story_21h_1.jpg'}, {'acao': 'create_story', 'arquivo': 'story_21h_2.jpg'}]
json.dump(d, open(p, 'w'), ensure_ascii=False, indent=1); print('ok')
