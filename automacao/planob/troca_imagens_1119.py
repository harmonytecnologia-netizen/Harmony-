"""19/11: troca de imagens repetidas/reaproveitadas (pedido do João 17/11). Mantém textos, nomes de arquivo e plano.json.
Imagens novas do ChatGPT em automacao/planob/img_1119/. Capa (ia_wifi_1119) e feed (adega) já eram inéditos."""
import os, json, importlib.util
H = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location('d', H + '/dias_14a16.py'); D = importlib.util.module_from_spec(sp); sp.loader.exec_module(D)
S = D.S; I = 'automacao/planob/img_1119/'; OUT = f'{D.REPO}/fila/2026-11-19'
J = [
 ('story_09h_1.jpg', 'story', S(I + 'st09_cabos_forro.jpg', 'BASTIDORES · DICA DE OBRA', ['Rede pensada', 'antes do forro.'], 'Eletroduto até cada ponto de Wi-Fi.')),
 ('story_15h_1.jpg', 'story', S(I + 'st15_pousada_real.jpg', 'PERGUNTA DO DIA · OBRA REAL', ['O Wi-Fi chega bem', 'em todos os cômodos?'], 'Responde no direct: sim · nem sempre')),
 ('story_21h_1.jpg', 'story', S(I + 'st21_suite.jpg', 'QUINTA À NOITE', ['Luz de leitura,', 'casa em silêncio.'], 'Uma cena no app apaga o resto. Ambiente conceito.')),
 ('carrossel_2.jpg', 'feed', S(I + 's01_casa_grande.jpg', '01 · O PROBLEMA', ['Um roteador só', 'não dá conta.'], 'Paredes, lajes e distância enfraquecem o sinal.')),
 ('carrossel_3.jpg', 'feed', S(I + 's02_access_point.jpg', '02 · ACCESS POINTS', ['Pontos discretos', 'no teto.'], 'Um por ambiente ou por andar, conforme a planta.')),
 ('carrossel_4.jpg', 'feed', S(I + 's03_rack_rede.jpg', '03 · CABO DE REDE', ['Cada ponto ligado', 'ao rack por cabo.'], 'Previsto em eletroduto, antes do forro.')),
 ('carrossel_5.jpg', 'feed', S(I + 's04_caminhando.jpg', '04 · UMA REDE SÓ', ['Mesmo nome de', 'rede na casa toda.'], 'Você anda e o celular segue conectado.')),
 ('carrossel_6.jpg', 'feed', S(I + 's05_varanda_pousada_real.jpg', '05 · ÁREA EXTERNA', ['Sinal na varanda', 'e na piscina.'], 'Música e câmeras sem cair. Obra real MOVE.')),
]
for fn, kind, s in J:
    if os.path.exists(f'{D.REPO}/{s["src"]}'): D.render(s, kind, f'{OUT}/{fn}'); print('ok', fn)
    else: print('FALTA', s['src'])
p = f'{OUT}/plano.json'; j = json.load(open(p))
for it in j['19h']:
    if it['acao'] == 'create_carousel_post':
        it['legenda'] = it['legenda'].replace('Imagens conceito (capa e slides 2 e 4).', 'Imagens conceito e obra real MOVE (slide 6).')
json.dump(j, open(p, 'w'), ensure_ascii=False, indent=1)
