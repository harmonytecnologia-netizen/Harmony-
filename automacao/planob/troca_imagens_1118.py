"""18/11: troca de imagens repetidas/reaproveitadas (pedido do João 17/11). Mantém textos, nomes de arquivo e plano.json.
Novas imagens do ChatGPT em automacao/planob/img_1118/. Capa (ia_living_tv_1118) e feed (home office) já eram inéditos."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
H = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location('d', H + '/dias_14a16.py'); D = importlib.util.module_from_spec(sp); sp.loader.exec_module(D)
S = D.S; I = 'automacao/planob/img_1118/'; OUT = f'{D.REPO}/fila/2026-11-18'
TV = 'automacao/planob/ia_living_tv_1118.jpg'
J = [  # (arquivo, tipo, S)
 ('story_09h_1.jpg', 'story', S(I + 'st09_homeoffice.jpg', 'PERGUNTA DO DIA', ['Você trabalha com', 'música ou silêncio?'], 'Responde no direct: música · silêncio')),
 ('story_15h_1.jpg', 'story', S(I + 'st15_forro_caixa.jpg', 'DETALHE · SOM EMBUTIDO', ['Discreta no forro,', 'presente no som.'], 'Caixa de embutir com tela pintável.')),
 ('story_21h_1.jpg', 'story', S(I + 'st21_noite.jpg', 'QUARTA À NOITE', ['Luz baixa,', 'tela acesa.'], 'Cena Cinema em um toque. Ambiente conceito.')),
 ('carrossel_2.jpg', 'feed', S(I + 'tv_altura.jpg', '01 · ALTURA', ['Centro da tela na', 'altura dos olhos.'], 'Sentado, em torno de 1 m a 1,10 m do piso.')),
 ('carrossel_3.jpg', 'feed', S(I + 'tv_distancia_diptico.jpg', '02 · DISTÂNCIA', ['De 1 a 1,5 vez', 'a diagonal da tela.'], 'TV 4K de 65": algo entre 1,7 m e 2,5 m.', (0, 0, 1, 0.485), dk=True)),
 ('carrossel_4.jpg', 'feed', S(I + 'tv_conforto.jpg', '03 · CONFORTO', ['Nada de olhar', 'para cima.'], 'TV alta demais cansa o pescoço.')),
 ('carrossel_5.jpg', 'feed', S(I + 'tv_cortina.jpg', '04 · REFLEXO', ['Janela de frente', 'apaga a imagem.'], 'Cortina automatizada resolve com um toque.')),
 ('carrossel_6.jpg', 'feed', S(I + 'tv_infra.jpg', '05 · INFRAESTRUTURA', ['Reforço, energia', 'e rede atrás da TV.'], 'Eletroduto até o rack, previsto antes da obra.')),
]
for fn, kind, s in J: D.render(s, kind, f'{OUT}/{fn}')
p = f'{OUT}/plano.json'; j = json.load(open(p))
for it in j['19h']:
    if it['acao'] == 'create_carousel_post':
        it['legenda'] = it['legenda'].replace('Imagens conceito (capa e slides 1 e 3).', 'Imagens conceito.')
json.dump(j, open(p, 'w'), ensure_ascii=False, indent=1)
print('ok 18/11')
