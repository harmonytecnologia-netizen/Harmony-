"""29/11 (domingo) e 30/11 (segunda).
29: 09h story obra real (suíte, cliente Itajaí); 12h feed OBRA REAL posto (BC) à noite; 15h enquete TV × telão (obra real BC);
    19h carrossel AUTOMAÇÃO cena "Boa noite" (capa com número) + story; 21h cinema de domingo.
30: 09h story bastidor real House Beer; 12h feed OBRA REAL rede antes do forro + Reel OBRA REAL sala com caixas de torre (áudio real);
    15h enquete cabo × Wi-Fi (obra real); 19h carrossel REDE "40 aparelhos" + story; 21h living segunda à noite.
Imagens: ChatGPT (img_1129 a1–a7, b1–b7) + quadros reais (posto, cliente itajai, ballneario, House Beer, clientes)."""
import sys, os
R = os.path.abspath(os.path.dirname(__file__) + '/../..'); sys.path.insert(0, R + '/automacao/scripts')
import premium as P
from carrossel_3d import slide, story3d, VERM
from PIL import Image
I = R + '/automacao/planob/img_1129/'
def f(n): return Image.open(I + n).convert('RGB')
dia = sys.argv[1] if len(sys.argv) > 1 else 'ambos'

if dia in ('29', 'ambos'):
    O = R + '/fila/2026-11-29/'; os.makedirs(O, exist_ok=True)
    P.story(f('itajai.jpg'), 'DOMINGO · OBRA REAL', ['Ar no ponto', 'antes de você', 'chegar.'], 'Climatização no app, pensada na obra.', O + 'story_09h_1.jpg')
    P.feed(f('posto_a.jpg'), 'OBRA REAL · POSTO EM BALNEÁRIO CAMBORIÚ', ['Música da bomba', 'à conveniência.'], 'Som ambiente por zonas, de dia e de noite.', O + 'feed.jpg')
    P.story(f('posto_b.jpg'), 'NOVO POST · OBRA REAL', ['Som que', 'acompanha', 'quem chega.'], 'Posto em Balneário Camboriú. Veja no feed.', O + 'story_feed.jpg')
    story3d(f('proj.jpg'), 'ENQUETE · RESPONDE NO DIRECT', ['Domingo de filme:', 'TV ou telão?'], 'Obra real em Balneário Camboriú.', O + 'story_15h_1.jpg', extra=['TV', 'TELÃO', 'OS DOIS'])
    P.story(f('a7.png'), 'DOMINGO À NOITE', ['Luz baixa,', 'manta e', 'cinema.'], 'Cena "Cinema": um toque e a sala se prepara.', O + 'story_21h_1.jpg')
    slide(f('a1.png'), None, 'AUTOMAÇÃO · CENA "BOA NOITE"', ['9 interruptores', 'antes de dormir?'], 'Arrasta: 1 toque faz tudo isso', O + 'carrossel_1.jpg', 1, 6)
    story3d(f('a1.png'), 'NOVO CARROSSEL NO FEED', ['9 interruptores', 'antes de', 'dormir?'], 'Com 1 toque a casa inteira se ajeita.', O + 'story_carrossel.jpg')
    slide(f('a2.png'), '01', 'UM BOTÃO NA CABECEIRA', ['"Boa noite"', 'num toque só.'], 'Teclado ao lado da cama, no app|ou por voz. Você não levanta mais.', O + 'carrossel_2.jpg', 2, 6)
    slide(f('a3.png'), '02', 'LUZES', ['Apaga tudo e', 'deixa o caminho.'], 'As luzes da casa apagam; fica só um|LED baixo até a escada ou o banheiro.', O + 'carrossel_3.jpg', 3, 6)
    slide(f('a4.png'), '03', 'CORTINAS', ['Fecham', 'sozinhas.'], 'Blackout no quarto e cortinas da sala|fechadas, sem passar de janela em janela.', O + 'carrossel_4.jpg', 4, 6)
    slide(f('a5.png'), '04', 'CASA EM MODO NOITE', ['Portão fechado,', 'alarme armado.'], 'A cena confere o portão, arma o alarme|e deixa só a luz de segurança da entrada.', O + 'carrossel_5.jpg', 5, 6)
    slide(f('a6.png'), None, 'O JEITO CERTO', ['Pensar a cena', 'antes do forro.'], 'Neutro nas caixinhas, motor de cortina|e teclados previstos na obra. Fale com a MOVE.', O + 'carrossel_6.jpg', 6, 6)
    print('ok 29/11')

if dia in ('30', 'ambos'):
    O = R + '/fila/2026-11-30/'; os.makedirs(O, exist_ok=True)
    P.story(f('hb_obra.jpg'), 'SEGUNDA · BASTIDOR REAL', ['Semana', 'começa', 'em obra.'], 'Instalação limpa, sem improviso.', O + 'story_09h_1.jpg')
    P.feed(f('caixas.jpg'), 'OBRA REAL · REDE ANTES DO FORRO', ['Cabo de rede', 'antes do gesso.'], 'Ponto de rede para TV, câmera e Wi-Fi.', O + 'feed.jpg')
    P.story(f('caixas.jpg'), 'NOVO POST · OBRA REAL', ['O cabo', 'nasce antes', 'do gesso.'], 'Depois, só tomada e acabamento.', O + 'story_feed.jpg')
    story3d(f('crimpa.jpg'), 'ENQUETE · RESPONDE NO DIRECT', ['Sua TV está no', 'cabo ou no Wi-Fi?'], 'Obra real: ponto de rede crimpado na hora.', O + 'story_15h_1.jpg', extra=['CABO', 'WI-FI', 'NÃO SEI'])
    P.story(f('b7.png'), 'SEGUNDA À NOITE', ['Som baixo,', 'luz quente', 'e vista.'], 'Som no forro: aparece só a música.', O + 'story_21h_1.jpg')
    slide(f('b1.png'), None, 'REDE · CASA CONECTADA', ['40 aparelhos', 'no seu Wi-Fi?'], 'Arrasta: 4 pontos de uma rede que aguenta', O + 'carrossel_1.jpg', 1, 6)
    story3d(f('b1.png'), 'NOVO CARROSSEL NO FEED', ['40 aparelhos', 'no seu', 'Wi-Fi?'], '4 pontos de uma rede que aguenta.', O + 'story_carrossel.jpg')
    slide(f('b2.png'), '01', 'O ERRO MAIS COMUM', ['Roteador da', 'operadora no nicho.'], 'Fechado na marcenaria, ele perde|sinal e não dá conta de tanto aparelho.', O + 'carrossel_2.jpg', 2, 6, cor_num=VERM)
    slide(f('b3.png'), '02', 'O QUE NÃO SE MEXE, VAI NO CABO', ['TV e câmeras', 'no cabo de rede.'], 'Tira peso do Wi-Fi e acaba com a|imagem travando no meio do filme.', O + 'carrossel_3.jpg', 3, 6)
    slide(f('b4.png'), '03', 'ACCESS POINT NO TETO', ['Wi-Fi que vem', 'de cima, por igual.'], 'Um ponto por área, com cabo, em vez|de repetidor na tomada.', O + 'carrossel_4.jpg', 4, 6)
    slide(f('b5.png'), '04', 'REDE DE VISITAS', ['Convidado não', 'entra na sua rede.'], 'Wi-Fi separado para visitas e para|a automação: mais segurança e estabilidade.', O + 'carrossel_5.jpg', 5, 6)
    slide(f('b6.png'), None, 'O JEITO CERTO', ['Rack organizado,', 'tudo no lugar.'], 'Switch, cabos identificados e nobreak.|Planeje antes do forro com a MOVE.', O + 'carrossel_6.jpg', 6, 6)
    print('ok 30/11')
