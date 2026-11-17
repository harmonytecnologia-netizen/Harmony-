"""20/11/2026 (sexta): obra real Clube Candeias (BC) + quadros 3D do Reel do nobreak.
uso: python3 dia_20.py fotos | carrossel"""
import sys, os, json, importlib.util
H = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location('d', H + '/dias_14a16.py'); D = importlib.util.module_from_spec(sp); sp.loader.exec_module(D)
S, FECHO, render, REPO = D.S, D.FECHO, D.render, D.REPO
HT = 'automacao/planob/hotel/'; NB = 'automacao/planob/nobreak/'
OUT = f'{REPO}/fila/2026-11-20'; os.makedirs(OUT, exist_ok=True)
FEED_LEG = ("Som que acompanha, sem aparecer.\n\nNo Clube Candeias, em Balneário Camboriú, a música chega a cada espaço por caixas embutidas no forro: "
            "do redário ao lounge, o som cria o clima e ninguém vê de onde ele vem.\n\n"
            "Em espaços comerciais, som ambiente bem feito é parte da experiência do cliente. Qual trilha combina com o seu espaço? Conte aqui.\n\n"
            + FECHO.replace('para casas e apartamentos de alto padrão', 'para casas, apartamentos e espaços comerciais de alto padrão') +
            "\n\nObra real MOVE.\n\n#SomAmbiente #Sonorização #ProjetoComercial #BalneárioCamboriú #Hotelaria #MOVE")
CARR_LEG = ("Faltou luz. Sua casa fica cega?\n\nSem energia, câmeras, gravador e internet desligam juntos, justamente quando a casa mais precisa delas. O que resolve:\n"
            "01 · Entender o que desliga junto: gravador, switch PoE e roteador.\n"
            "02 · Nobreak no rack alimentando esses três.\n"
            "03 · Câmeras PoE recebem energia pelo switch: ficam ligadas também.\n"
            "04 · Autonomia calculada pela potência dos aparelhos.\n"
            "05 · Bônus: o nobreak também protege contra picos e oscilações.\n\n"
            "Se a luz cair agora, sua câmera continua gravando? Conte aqui, salve e envie para quem está construindo.\n\n"
            + FECHO.replace('som, cinema, iluminação e automação', 'segurança, rede, som, cinema e automação') +
            "\n\nImagens: animação 3D conceito.\n\n#Nobreak #SegurançaResidencial #CâmeraDeSegurança #RackTécnico #CasaInteligente #Itapema #MOVE")
modo = sys.argv[1]
if modo == 'fotos':
    render(S(HT + 'quadro_fachada_esc.jpg', 'OBRA REAL · BALNEÁRIO CAMBORIÚ', ['Clube Candeias:', 'som em cada espaço.'], 'Hoje às 12h, o vídeo da obra no perfil.', (0, 0, 1, 1)), 'story', f'{OUT}/story_09h_1.jpg')
    render(S(HT + 'foto_redario.jpg', 'OBRA REAL · CLUBE CANDEIAS', ['Som que acompanha,', 'sem aparecer.'], 'Caixas embutidas no forro. Balneário Camboriú.', (0, 0.06, 1, 1)), 'feed', f'{OUT}/feed.jpg')
    render(S(HT + 'foto_redario.jpg', 'OBRA REAL · CLUBE CANDEIAS', ['Som que acompanha,', 'sem aparecer.'], 'Novo post no perfil.', (0, 0.0, 1, 1)), 'story', f'{OUT}/story_feed.jpg')
    render(S(HT + 'quadro_escada_esc.jpg', 'OBRA REAL · CLUBE CANDEIAS', ['Viajar é…', 'ouvir bem.'], 'Som ambiente do térreo ao lounge.', (0, 0, 1, 0.62)), 'story', f'{OUT}/story_21h_1.jpg')
    json.dump({'feed_legenda': FEED_LEG}, open(f'{OUT}/_leg.json', 'w'), ensure_ascii=False)
else:
    render(S(NB + 'cam.jpg', 'PERGUNTA DO DIA', ['Faltou luz agora:', 'sua câmera grava?'], 'Responde no direct: sim · não sei', (0, 0, 1, 1)), 'story', f'{OUT}/story_15h_1.jpg')
    capa = S(NB + 'escuro.jpg', 'SEGURANÇA · DICA MOVE', ['Faltou luz.', 'Sua casa fica cega?'], 'Arraste e veja o que resolve →', (0, 0, 1, 1))
    slides = [S(NB + 'escuro.jpg', '01 · O QUE DESLIGA', ['Gravador, switch', 'e internet juntos.'], 'Sem energia, a câmera não grava nem avisa.', (0, 0.1, 1, 0.9), dk=True),
              S(NB + 'nobreak.jpg', '02 · NOBREAK NO RACK', ['Energia de reserva', 'para o essencial.'], 'Gravador, switch PoE e roteador ligados nele.', (0, 0, 1, 1), dk=True),
              S(NB + 'cam_ok.jpg', '03 · CÂMERAS POE', ['A câmera recebe', 'energia pelo cabo.'], 'Switch no nobreak = câmera ligada.', (0, 0, 1, 1), dk=True),
              S(NB + 'rack_ok.jpg', '04 · AUTONOMIA', ['Calculada pela', 'potência do rack.'], 'Quanto tempo você quer gravando sem luz.', (0, 0, 1, 1), dk=True),
              S(NB + 'geral.jpg', '05 · PROTEÇÃO', ['Também segura', 'picos e oscilações.'], 'Equipamento protegido o ano todo.', (0, 0, 1, 1), dk=True)]
    files = ['carrossel_1.jpg']; render(capa, 'feed', f'{OUT}/carrossel_1.jpg')
    for i, s in enumerate(slides, 2):
        fn = f'carrossel_{i}.jpg'; render(s, 'feed', f'{OUT}/{fn}'); files.append(fn)
    render(capa, 'story', f'{OUT}/story_carrossel.jpg', b='Novo carrossel no perfil. Arraste e salve.')
    json.dump({'carrossel': files, 'carr_legenda': CARR_LEG}, open(f'{OUT}/_carr.json', 'w'), ensure_ascii=False)
print('ok', modo)
