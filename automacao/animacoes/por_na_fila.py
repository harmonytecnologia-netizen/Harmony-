# uso: python3 por_na_fila.py pasta_cena AAAA-MM-DD 12h|19h thumb_ms
import sys, json, shutil, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legendas_reels_1115 import L
cena, dia, hora, thumb = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
d = os.path.join(R, 'fila', dia); arq = f'reel_{hora}.mp4'
shutil.copy(os.path.join(R, 'automacao/animacoes', cena, 'MOVE_explica.mp4'), os.path.join(d, arq))
p = json.load(open(os.path.join(d, 'plano.json'), encoding='utf-8'))
p[hora] = [i for i in p.get(hora, []) if i.get('arquivo') != arq]
p[hora] += [{"acao": "create_video_post", "arquivo": arq, "legenda": L[cena], "thumb_offset": thumb}, {"acao": "create_story", "arquivo": arq}]
json.dump(p, open(os.path.join(d, 'plano.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', dia, hora, arq)
