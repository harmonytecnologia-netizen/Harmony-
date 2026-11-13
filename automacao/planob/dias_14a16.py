"""Plano B 14 a 16/11/2026: imagens do repositório (projetos reais em site/img/r_*, quadros reais de obra,
imagens conceito antigas em novo enquadramento). Uso: python3 dias_14a16.py AAAA-MM-DD"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arte import img, dark, feed, story, check, REPO

FECHO = ("A MOVE projeta e integra som, cinema, iluminação e automação para casas e apartamentos de alto padrão "
         "no litoral norte de SC. Agende uma conversa e envie a planta do seu projeto.")
OQ = 'automacao/planob/obra_quadro_'

def S(src, k, t, b, crop=None, flip=False, dk=False):
    return dict(src=src, k=k, t=t, b=b, crop=crop, flip=flip, dk=dk)

def carrossel(capa, slides, legenda):
    return dict(capa=capa, slides=slides, legenda=legenda)

DIAS = {
 '2026-11-14': {
  '09h': [S(OQ + '15.jpg', 'BASTIDORES · OBRA REAL', ['Antes do forro,', 'cada cabo no lugar.'], 'Infraestrutura de som e automação.', (0, 0, 1, 0.64)),
          S('site/img/instala.jpg', 'DICA RÁPIDA', ['Caixa de embutir?', 'Decida antes do gesso.'], 'Posição marcada na planta, sem retrabalho.', (0.05, 0, 1, 1))],
  '12h': dict(foto=S('site/img/r_gourmet.jpg', 'ÁREA GOURMET · PROJETO MOVE', ['O verão começa', 'no som.'], 'Som, luz e piscina no mesmo app.', (0, 0.04, 1, 1)),
     legenda="O verão começa no som. ☀️\n\nNesta área gourmet, som ambiente, iluminação e a piscina respondem ao mesmo aplicativo. Música para o dia todo, luz certa ao anoitecer e nenhum fio aparente.\n\nPiscina com música: indispensável ou dispensável? Conte nos comentários e salve para o seu projeto de verão.\n\n" + FECHO + "\n\n#ÁreaGourmet #SomAmbiente #CasaDePraia #AutomaçãoResidencial #BalneárioCamboriú #MOVE"),
  '15h': [S('site/img/app.jpg', 'PERGUNTA DO DIA', ['Sua área externa', 'já tem trilha?'], 'Responde no direct: sim · quero ter', (0, 0.05, 1, 1))],
  '19h': carrossel(S('site/img/rack.jpg', 'RACK TÉCNICO', ['5 cuidados com a', 'central da sua casa.'], 'Arraste para ver cada um →', (0, 0, 1, 1)), [
          S('site/img/rack.jpg', '01 · VENTILAÇÃO', ['Equipamento', 'precisa respirar.'], 'Saída de ar e espaço entre aparelhos.', (0, 0.1, 1, 0.9), dk=True),
          S('site/img/r_hifi.jpg', '02 · IDENTIFICAÇÃO', ['Cada cabo com', 'nome e destino.'], 'Etiqueta nas duas pontas.', dk=True),
          S('site/img/teclado.jpg', '03 · ENERGIA', ['Proteção antes', 'de tudo ligar.'], 'Circuito dedicado e proteção elétrica.', dk=True),
          S('site/img/voz.jpg', '04 · FOLGA', ['Espaço para', 'o que vem depois.'], 'Previsão para novos equipamentos.', dk=True),
          S('site/img/hero.jpg', '05 · ACESSO', ['Manutenção sem', 'desmontar nada.'], 'Porta e fundo de fácil acesso.', dk=True)],
     "5 cuidados com a central da sua casa.\n\nO rack é onde som, rede, câmeras e automação se encontram. Bem planejado, a casa funciona melhor e a manutenção fica simples:\n01 · Ventilação de verdade.\n02 · Cabos identificados nas duas pontas.\n03 · Energia protegida.\n04 · Espaço para crescer.\n05 · Acesso fácil para manutenção.\n\nQual desses cuidados a sua obra já tem? Arraste, salve e mostre ao seu arquiteto.\n\n" + FECHO + "\n\nImagem conceito.\n\n#RackTécnico #Infraestrutura #AutomaçãoResidencial #Sonorização #ObraDeAltoPadrão #Itapema #MOVE"),
  '21h': [S('site/img/voz.jpg', 'SÁBADO À NOITE', ['Um toque.', 'A sessão começa.'], 'Luz, tela, cortinas e som em uma cena.', (0.1, 0.05, 1, 1))],
 },
 '2026-11-15': {
  '09h': [S('anuncios/jornada/s6.png', 'DOMINGO EM CASA', ['Sessão em família,', 'tudo em um toque.'], 'Pelo app ou pela voz, sem procurar controle.', (0.05, 0.08, 1, 1))],
  '12h': dict(foto=S('site/img/r_cozinha.jpg', 'ILUMINAÇÃO · PROJETO MOVE', ['Luz que desenha', 'a cozinha.'], 'LED embutido na marcenaria, em cena.', (0, 0.02, 1, 0.98)),
     legenda="Luz que desenha a cozinha.\n\nNeste projeto, a iluminação em LED foi embutida na marcenaria e nos nichos: valoriza os materiais, ilumina a bancada na medida certa e entra em cena com um toque, junto com o som ambiente.\n\nLuz quente ou luz neutra na cozinha: qual você prefere? Conte aqui e salve para a sua reforma.\n\n" + FECHO + "\n\n#IluminaçãoLED #CozinhaPlanejada #Marcenaria #CasaInteligente #Itajaí #MOVE"),
  '15h': [S('site/img/r_hifi.jpg', 'DETALHE · SOM', ['Som de referência', 'começa na escolha.'], 'Caixa, amplificador e sala pensados juntos.', (0.1, 0, 1, 1))],
  '19h': carrossel(S('site/img/teclado.jpg', 'DICA DE OBRA', ['Fio neutro no', 'interruptor.'], 'O detalhe que libera a automação →', (0.15, 0.1, 1, 1)), [
          S(OQ + '9.jpg', '01 · O QUE É', ['O neutro chega', 'até a caixinha.'], 'Junto da fase, no ponto do interruptor.', (0, 0, 1, 0.6), dk=True),
          S('site/img/teclado.jpg', '02 · POR QUÊ', ['Muitos módulos', 'precisam dele.'], 'Para ficarem sempre alimentados.', dk=True),
          S(OQ + '15.jpg', '03 · QUANDO', ['Antes da', 'fiação passar.'], 'Previsto no projeto elétrico.', (0, 0, 1, 0.6), dk=True),
          S('site/img/config.jpg', '04 · CONFERIR', ['Combine com', 'o eletricista.'], 'Em cada ponto que terá automação.', dk=True),
          S('site/img/r_sala.jpg', '05 · RESULTADO', ['Um item simples', 'que evita retrabalho.'], 'Automação completa, sem quebra-quebra.', dk=True)],
     "O detalhe da obra que libera a automação.\n\nMuitos interruptores inteligentes precisam do fio neutro na caixinha. Quando ele não é previsto, a automação fica limitada depois:\n01 · O que é o neutro na caixinha.\n02 · Por que muitos módulos precisam dele.\n03 · Quando prever: antes da fiação.\n04 · Como conferir com o eletricista.\n05 · Um item simples que evita retrabalho.\n\nSalve e envie para o seu eletricista. Dúvidas? Chama a gente no direct.\n\n" + FECHO + "\n\nImagem conceito na capa.\n\n#FioNeutro #InstalaçãoElétrica #AutomaçãoResidencial #DicaDeObra #Blumenau #MOVE"),
  '21h': [S(OQ + '18.jpg', 'BASTIDORES · OBRA REAL', ['Cada eletroduto', 'no lugar certo.'], 'Hoje é infraestrutura. Amanhã, conforto.', (0.1, 0, 1, 0.64))],
 },
 '2026-11-16': {
  '09h': [S('site/img/r_forro.jpg', 'SEMANA NOVA · PROJETO MOVE', ['Sua obra começa?', 'Fale antes do forro.'], 'Envie a planta pelo direct.', (0, 0, 1, 0.92))],
  '12h': dict(foto=S('site/img/r_tv.jpg', 'AUTOMAÇÃO · PROJETO MOVE', ['A TV desce do forro.', 'E some depois.'], 'Suporte retrátil no forro de madeira.', (0.12, 0, 0.88, 1)),
     legenda="A TV desce do forro. E some depois.\n\nNesta varanda, a TV fica guardada no forro de madeira e desce com um toque, no ângulo certo para quem está no sofá. Fim do filme, ela volta e a vista fica livre de novo.\n\nVocê esconderia a TV na sua sala ou varanda? Conte nos comentários.\n\n" + FECHO + "\n\n#TVRetrátil #AutomaçãoResidencial #Varanda #DesignDeInteriores #AltoPadrão #MOVE"),
  'reel': dict(scenes=[('site/img/r_gourmet.jpg', 'PROJETOS MOVE', 'Do projeto|ao dia a dia.'),
                       ('site/img/r_sala.jpg', '01 · SALA INTEGRADA', 'Luz embutida|em cena.'),
                       ('site/img/r_piscina.jpg', '02 · ÁREA EXTERNA', 'Piscina e fachada|iluminadas.'),
                       ('site/img/r_appreal.jpg', '03 · PELO APP', 'A casa inteira|na palma da mão.'),
                       ('site/img/r_hifi.jpg', '04 · SOM', 'Som de referência,|do jeito certo.')],
     legenda="Do projeto ao dia a dia. 🎬\n\nAlguns projetos entregues pela MOVE no litoral norte de SC:\n01 · Área gourmet integrada à piscina, tudo pelo app.\n02 · Sala integrada com luz embutida em cena.\n03 · Piscina e fachada iluminadas.\n04 · A casa inteira controlada pelo app.\n05 · Sistema hi-fi para ouvir música do jeito certo.\n\nQual desses ambientes você quer na sua casa? Conte aqui e salve para o seu projeto.\n\n" + FECHO + "\n\n#ProjetosMOVE #AutomaçãoResidencial #HomeTheater #Iluminação #BalneárioCamboriú #CasaInteligente #MOVE"),
  '15h': [S('anuncios/jornada/s5.png', 'ENQUETE', ['App ou voz?', 'Como você comanda?'], 'Responde no direct: app · voz', (0.0, 0.05, 1, 1))],
  '19h': carrossel(S('site/img/config.jpg', 'SOM POR ZONAS', ['Cada ambiente', 'com a sua música.'], 'Arraste e entenda o multiroom →', (0.05, 0.02, 1, 1)), [
          S('site/img/r_gourmet.jpg', '01 · ZONAS', ['Sala, varanda,', 'suíte: cada uma a sua.'], 'Músicas diferentes ao mesmo tempo.', dk=True),
          S('site/img/r_cozinha.jpg', '02 · VOLUME', ['Volume próprio', 'em cada ambiente.'], 'Alto na festa, baixo no escritório.', dk=True),
          S('site/img/r_forro.jpg', '03 · DISCRETO', ['Caixas embutidas,', 'nada à vista.'], 'Forro, parede ou jardim.', dk=True),
          S('site/img/app.jpg', '04 · CONTROLE', ['Tudo no celular', 'ou pela voz.'], 'Uma tela para a casa inteira.', dk=True),
          S('site/img/r_tv.jpg', '05 · PROJETO', ['Pensado na planta,', 'antes da obra.'], 'Cabos e pontos no lugar certo.', dk=True)],
     "Cada ambiente com a sua música.\n\nO som por zonas (multiroom) deixa a casa inteira sonorizada, mas com liberdade:\n01 · Músicas diferentes em cada ambiente.\n02 · Volume próprio em cada zona.\n03 · Caixas embutidas, sem nada à vista.\n04 · Controle pelo celular ou pela voz.\n05 · Tudo pensado na planta, antes da obra.\n\nEm qual ambiente você mais ouve música? Arraste, salve e envie para quem está construindo.\n\n" + FECHO + "\n\nImagem conceito na capa.\n\n#SomAmbiente #Multiroom #Sonorização #CasaInteligente #Florianópolis #MOVE"),
  '21h': [S(OQ + '9.jpg', 'DICA RÁPIDA · OBRA REAL', ['Cabo de som:', 'identifique as pontas.'], 'Etiqueta no forro e no rack.', (0, 0, 1, 0.6))],
 },
}

def render(s, kind, out, k=None, t=None, b=None):
    ph = dark(s['src'], s['crop']) if s['dk'] else img(s['src'], s['crop'], s['flip'])
    fn = feed if kind == 'feed' else story
    check(t or s['t'], kind)
    fn(ph, k or s['k'], t or s['t'], b or s['b'], out)

def build(data):
    D = DIAS[data]; out = f'{REPO}/fila/{data}'; os.makedirs(out, exist_ok=True); plano = {}
    for h in ('09h', '15h', '21h'):
        plano[h] = []
        for i, s in enumerate(D[h], 1):
            fn = f'story_{h}_{i}.jpg'; render(s, 'story', f'{out}/{fn}'); plano[h].append({'acao': 'create_story', 'arquivo': fn})
    f = D['12h']; render(f['foto'], 'feed', f'{out}/feed.jpg'); render(f['foto'], 'story', f'{out}/story_feed.jpg')
    plano['12h'] = [{'acao': 'create_image_post', 'arquivo': 'feed.jpg', 'legenda': f['legenda']},
                    {'acao': 'create_story', 'arquivo': 'story_feed.jpg'}]
    if 'reel' in D:
        plano['12h'] += [{'acao': 'create_video_post', 'arquivo': 'reel.mp4', 'legenda': D['reel']['legenda'], 'thumb_offset': 1500},
                         {'acao': 'create_story', 'arquivo': 'reel.mp4'}]
    c = D['19h']; files = ['carrossel_1.jpg']; render(c['capa'], 'feed', f'{out}/carrossel_1.jpg')
    for i, s in enumerate(c['slides'], 2):
        fn = f'carrossel_{i}.jpg'; render(s, 'feed', f'{out}/{fn}'); files.append(fn)
    render(c['capa'], 'story', f'{out}/story_carrossel.jpg', b='Novo carrossel no perfil. Arraste e salve.')
    plano['19h'] = [{'acao': 'create_carousel_post', 'arquivos': files, 'legenda': c['legenda']},
                    {'acao': 'create_story', 'arquivo': 'story_carrossel.jpg'}]
    plano['videos_usados'] = []; plano['plano_b'] = True
    json.dump(plano, open(f'{out}/plano.json', 'w'), ensure_ascii=False, indent=1)
    print('ok', data)

if __name__ == '__main__':
    build(sys.argv[1])
