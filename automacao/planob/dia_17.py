"""Plano B 17/11/2026 (terça)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
sp = importlib.util.spec_from_file_location('d', os.path.dirname(os.path.abspath(__file__)) + '/dias_14a16.py'); D = importlib.util.module_from_spec(sp); sp.loader.exec_module(D)
S, FECHO, OQ, carrossel = D.S, D.FECHO, D.OQ, D.carrossel
D.DIAS['2026-11-17'] = {
 '09h': [S('site/img/r_portao.jpg', 'AUTOMAÇÃO · PROJETO MOVE', ['O portão abre', 'antes de você descer.'], 'Fachada, luz e portão pelo app.', (0, 0.05, 1, 1))],
 '12h': dict(foto=S('anuncios/jornada/s3.png', 'DIA DE INSTALAÇÃO', ['Pontual, limpo', 'e sem improviso.'], 'Equipe MOVE no litoral norte de SC.', (0.22, 0.04, 1, 1)),
    legenda="Pontual, limpo e sem improviso.\n\nDia de instalação na MOVE começa muito antes de entrarmos no apartamento: projeto aprovado, lista de equipamentos conferida, pontos marcados na planta. Na obra, cuidado com o acabamento, organização e teste de cada ambiente antes da entrega.\n\nO que mais pesa para você na hora de escolher quem instala: projeto, acabamento ou prazo? Conte nos comentários.\n\n" + FECHO + "\n\nAmbiente conceito.\n\n#BastidoresMOVE #InstalaçãoProfissional #AutomaçãoResidencial #Sonorização #BalneárioCamboriú #MOVE"),
 '15h': [S('automacao/iamin/iamin_close_pad.png', 'DICA DA IAMIN', ['Embutir ou', 'aparente?'], 'Responde no direct: embutir · aparente', (0, 0, 1, 0.9))],
 '19h': carrossel(S(OQ + '7.jpg', 'CHECKLIST · OBRA REAL', ['6 itens antes', 'de fechar o forro.'], 'Arraste e salve para a sua obra →', (0, 0, 1, 0.66)), [
         S(OQ + '20.jpg', '01 · CABO DE SOM', ['Bitola certa,', 'até cada caixa.'], 'Do rack à caixa, sem emendas.', (0, 0, 1, 0.66), dk=True),
         S(OQ + '11.jpg', '02 · REDE', ['Eletroduto para', 'cabo de rede.'], 'TV, rack e pontos de Wi-Fi no forro.', (0, 0, 1, 0.55), dk=True),
         S('site/img/r_forro.jpg', '03 · CAIXAS', ['Pontos de som', 'marcados na planta.'], 'Posição definida antes do gesso.', dk=True),
         S('site/img/r_tv.jpg', '04 · REFORÇO', ['TV, projetor e', 'tela com apoio.'], 'Estrutura prevista no forro e na parede.', dk=True),
         S(OQ + '22.jpg', '05 · ACESSO', ['Alçapão onde', 'precisa de acesso.'], 'Manutenção sem quebrar o gesso.', (0, 0, 1, 0.66), dk=True),
         S('site/img/rack.jpg', '06 · RACK', ['Tudo chega', 'ao mesmo lugar.'], 'Cabos identificados nas duas pontas.', (0, 0.1, 1, 0.9), dk=True)],
    "6 itens para conferir antes de fechar o forro.\n\nDepois do gesso, qualquer mudança vira quebra-quebra. Por isso, na obra a gente confere:\n01 · Cabo de som com bitola certa até cada caixa.\n02 · Eletroduto para rede (TV, rack e Wi-Fi no forro).\n03 · Pontos das caixas marcados na planta.\n04 · Reforço para TV, projetor e tela.\n05 · Alçapão onde vai precisar de acesso.\n06 · Tudo chegando organizado ao rack.\n\nSalve e envie para o seu arquiteto ou mestre de obras. Dúvidas? Chama a gente no direct.\n\n" + FECHO + "\n\n#ChecklistDeObra #AntesDoForro #Infraestrutura #AutomaçãoResidencial #ObraDeAltoPadrão #MOVE"),
 '21h': [S('anuncios/jornada/s2.png', 'AGENDA ABERTA', ['Visitas técnicas', 'em BC e Itapema.'], 'Agende pelo direct e envie a planta.', (0.08, 0, 1, 0.92))],
}
D.build('2026-11-17')
