"""19/11/2026 (quinta): adega e Wi-Fi (ChatGPT, 14/11) + fotos reais e quadros de obra do repositório."""
import sys, os
import importlib.util
H = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location('d', H + '/dias_14a16.py'); D = importlib.util.module_from_spec(sp); sp.loader.exec_module(D)
S, FECHO, OQ, carrossel = D.S, D.FECHO, D.OQ, D.carrossel
AD = 'automacao/planob/ia_adega_1119.jpg'; WF = 'automacao/planob/ia_wifi_1119.jpg'
D.DIAS['2026-11-19'] = {
 '09h': [S(OQ + '11.jpg', 'BASTIDORES · OBRA REAL', ['Rede pensada', 'antes do forro.'], 'Eletroduto até cada ponto de Wi-Fi.', (0, 0, 1, 0.55))],
 '12h': dict(foto=S(AD, 'ADEGA · AMBIENTE CONCEITO', ['O vinho também', 'merece luz certa.'], 'LED quente nas prateleiras, som no forro.', (0, 0, 1, 1)),
    legenda="O vinho também merece luz certa.\n\nNa adega integrada ao living, a iluminação em LED quente valoriza cada prateleira sem aquecer as garrafas, e entra em cena junto com o som ambiente quando os convidados chegam. Tudo pelo app, ou numa cena só: \"Receber\".\n\nTinto, branco ou espumante: qual não pode faltar na sua adega? Conte nos comentários e salve para o seu projeto.\n\n" + FECHO + "\n\nAmbiente conceito.\n\n#Adega #IluminaçãoLED #SomAmbiente #ArquiteturaDeInteriores #BalneárioCamboriú #MOVE"),
 '15h': [S('site/img/r_appreal.jpg', 'PERGUNTA DO DIA', ['O Wi-Fi chega bem', 'em todos os cômodos?'], 'Responde no direct: sim · nem sempre', (0, 0.04, 1, 1))],
 '19h': carrossel(S(WF, 'WI-FI EM TODA A CASA', ['Sinal forte em', 'cada canto.'], 'Sem aparelho à vista. Arraste →', (0, 0, 1, 1)), [
         S('site/img/r_sala.jpg', '01 · O PROBLEMA', ['Um roteador só', 'não dá conta.'], 'Paredes, lajes e distância enfraquecem o sinal.', (0, 0.12, 1, 0.8), dk=True),
         S(WF, '02 · ACCESS POINTS', ['Pontos discretos', 'no teto.'], 'Um por ambiente ou por andar, conforme a planta.', (0, 0, 1, 0.5), dk=True),
         S(OQ + '20.jpg', '03 · CABO DE REDE', ['Cada ponto ligado', 'ao rack por cabo.'], 'Previsto em eletroduto, antes do forro.', (0, 0.05, 1, 0.6), dk=True),
         S('site/img/app.jpg', '04 · UMA REDE SÓ', ['Mesmo nome de', 'rede na casa toda.'], 'Você anda e o celular segue conectado.', (0, 0.1, 1, 0.75), dk=True),
         S('site/img/r_gourmet.jpg', '05 · ÁREA EXTERNA', ['Sinal na varanda', 'e na piscina.'], 'Música e câmeras sem cair a conexão.', (0, 0.1, 1, 0.7), dk=True)],
    "Wi-Fi forte em cada canto da casa.\n\nEm casas e apartamentos grandes, um roteador sozinho não dá conta. O caminho é projetar a rede:\n01 · Paredes, lajes e distância enfraquecem o sinal.\n02 · Access points discretos no teto, por ambiente ou andar.\n03 · Cada ponto ligado ao rack por cabo de rede, em eletroduto.\n04 · Uma rede só, com o mesmo nome na casa toda.\n05 · Sinal também na varanda, na área gourmet e na piscina.\n\nEm qual cômodo o seu Wi-Fi mais falha? Conte aqui, salve e envie para quem está construindo.\n\n" + FECHO + "\n\nImagens conceito (capa e slides 2 e 4).\n\n#WiFi #RedeDomestica #CasaConectada #AutomaçãoResidencial #Infraestrutura #Camboriú #MOVE"),
 '21h': [S('site/img/hero.jpg', 'SESSÃO DE QUINTA', ['Poltrona, tela', 'e som envolvente.'], 'Sala de cinema dedicada. Ambiente conceito.', (0.08, 0.05, 1, 1))],
}
D.build('2026-11-19')
