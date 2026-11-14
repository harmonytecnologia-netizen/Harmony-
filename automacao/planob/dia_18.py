"""18/11/2026 (quarta): 2 imagens novas do ChatGPT (home office, living TV) + quadros reais de obra no Reel (plano B p/ vídeo)."""
import sys, os
import importlib.util
H = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location('d', H + '/dias_14a16.py'); D = importlib.util.module_from_spec(sp); sp.loader.exec_module(D)
S, FECHO, OQ, carrossel = D.S, D.FECHO, D.OQ, D.carrossel
HO = 'automacao/planob/ia_homeoffice_1118.jpg'; TV = 'automacao/planob/ia_living_tv_1118.jpg'
D.DIAS['2026-11-18'] = {
 '09h': [S('site/img/r_sala.jpg', 'PERGUNTA DO DIA', ['Você trabalha com', 'música ou silêncio?'], 'Responde no direct: música · silêncio', (0, 0.06, 1, 1))],
 '12h': dict(foto=S(HO, 'HOME OFFICE · AMBIENTE CONCEITO', ['Foco, conforto e', 'o som na medida.'], 'Caixa embutida no forro, luz em cena, vista livre.', (0, 0, 1, 1)),
    legenda="Trabalhar em casa pode ser o melhor momento do dia.\n\nNo home office, o som fica embutido no forro, em volume baixo e só para aquele ambiente. A luz da estante entra em cena com um toque e a cortina acompanha o sol da tarde, sem tirar a vista do lugar.\n\nVocê trabalha ouvindo música ou prefere silêncio? Conte nos comentários e salve para o seu projeto.\n\n" + FECHO + "\n\nAmbiente conceito.\n\n#HomeOffice #SomAmbiente #AutomaçãoResidencial #DesignDeInteriores #BalneárioCamboriú #MOVE"),
 'reel': dict(legenda="Antes do forro, o que ninguém vê. 🎬\n\nBastidores de uma obra acompanhada pela MOVE:\n01 · Eletrodutos para som, rede e automação.\n02 · Cada ponto marcado na planta.\n03 · Visita técnica em cada etapa.\n04 · Conferir agora para não quebrar depois.\nNo fim, o resultado: som embutido e nada aparente.\n\nSua obra está em qual etapa? Conte aqui e envie para quem está construindo com você.\n\n" + FECHO + "\n\n#BastidoresDeObra #Infraestrutura #AntesDoForro #Sonorização #ObraDeAltoPadrão #Itapema #MOVE"),
 '15h': [S(HO, 'DETALHE · SOM EMBUTIDO', ['Discreta no forro,', 'presente no som.'], 'Caixa de embutir com tela pintável.', (0.45, 0.06, 1, 0.62))],
 '19h': carrossel(S(TV, 'TV NA MEDIDA CERTA', ['Altura e distância', 'da TV ao sofá.'], 'Arraste e salve para o seu projeto →', (0, 0, 1, 1)), [
         S(TV, '01 · ALTURA', ['Centro da tela na', 'altura dos olhos.'], 'Sentado, em torno de 1 m a 1,10 m do piso.', (0.2, 0.36, 0.8, 0.72), dk=True),
         S('site/img/r_sala.jpg', '02 · DISTÂNCIA', ['De 1 a 1,5 vez', 'a diagonal da tela.'], 'TV 4K de 65": algo entre 1,7 m e 2,5 m.', (0, 0.1, 1, 0.75), dk=True),
         S(TV, '03 · CONFORTO', ['Nada de olhar', 'para cima.'], 'TV alta demais cansa o pescoço.', (0, 0.38, 1, 0.95), dk=True),
         S('site/img/voz.jpg', '04 · REFLEXO', ['Janela de frente', 'apaga a imagem.'], 'Cortina automatizada resolve com um toque.', (0, 0.05, 1, 0.75), dk=True),
         S(OQ + '15.jpg', '05 · INFRAESTRUTURA', ['Reforço, energia', 'e rede atrás da TV.'], 'Eletroduto até o rack, previsto antes da obra.', (0, 0, 1, 0.62), dk=True)],
    "TV na medida certa: altura e distância do sofá.\n\nUm detalhe de projeto que muda o conforto de todos os dias:\n01 · Centro da tela na altura dos olhos de quem está sentado (em torno de 1 m a 1,10 m do piso).\n02 · Distância de 1 a 1,5 vez a diagonal da tela (TV 4K de 65\": algo entre 1,7 m e 2,5 m).\n03 · Nada de TV alta demais: o pescoço agradece.\n04 · Cuidado com o reflexo da janela de frente.\n05 · Reforço, energia e rede atrás da TV, com eletroduto até o rack.\n\nSua TV está na altura certa? Arraste, salve e envie para o seu arquiteto.\n\n" + FECHO + "\n\nImagens conceito (capa e slides 1 e 3).\n\n#AlturaDaTV #HomeTheater #ProjetoDeInteriores #SalaDeTV #Itajaí #MOVE"),
 '21h': [S(TV, 'QUARTA À NOITE', ['Luz baixa,', 'tela acesa.'], 'Cena Cinema em um toque. Ambiente conceito.', (0, 0.25, 0.72, 1))],
}
D.build('2026-11-18')
