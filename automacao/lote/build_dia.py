"""Monta um dia do lote: build_dia.py AAAA-MM-DD <pasta_imagens> <musica.mp3> "<nome da música>" [music_start]
Imagens esperadas na pasta: r1..r5 (cenas do Reel), p1..pN (feed/carrossel), s1 (story extra), qualquer extensão.
Gera fila/AAAA-MM-DD/{reel.mp4, feed.jpg | carrossel_N.jpg, story_feed.jpg, story_extra.jpg, plano.json}.
"""
import sys, os, json, glob, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(HERE + '/../..')
sys.path.insert(0, HERE); sys.path.insert(0, REPO + '/automacao/scripts')
import importlib.util
spec = importlib.util.spec_from_file_location('lote', HERE + '/lote_2026-11-13_a_26.py'); L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
import premium as P
from PIL import Image

def find(folder, stem):
    m = [f for f in glob.glob(f'{folder}/{stem}.*')]
    return m[0] if m else None

def main(data, folder, music, music_name, mstart=0):
    d = next(x for x in L.DIAS if x['data'] == data)
    out = f'{REPO}/fila/{data}'; os.makedirs(out, exist_ok=True)
    # Reel
    scenes = []
    for k, s in enumerate(d['reel']['scenes']):
        scenes.append({'img': find(folder, f'r{k+1}'), 'kicker': s['kicker'], 'title': s['title'], 'zoom': 'in' if k % 2 == 0 else 'out'})
    cfg = {'music': music, 'music_start': mstart, 'intro': REPO + '/automacao/assets/intro_som.mp4', 'scenes': scenes,
           'end_title': 'Agende uma conversa.', 'end_sub': 'Projetos de som, cinema e automação.'}
    json.dump(cfg, open(f'{folder}/cfg.json', 'w'), ensure_ascii=False)
    rc = subprocess.call(['python3', REPO + '/automacao/scripts/reel_premium.py', f'{folder}/cfg.json', f'{out}/reel.mp4'])
    assert rc == 0, 'reel falhou'
    # Post 19h
    post = d['post']; sl = post['slides']; acts19 = []
    if post['formato'] == 'feed':
        s = sl[0]; ph = Image.open(find(folder, 'p1')).convert('RGB')
        P.feed(ph, s['kicker'], s['title'], s['body'], f'{out}/feed.jpg')
        P.story(ph, s['kicker'], s['title'], s['body'], f'{out}/story_feed.jpg')
        acts19.append({'acao': 'create_image_post', 'arquivo': 'feed.jpg', 'legenda': post['legenda']})
    else:
        files = []
        for k, s in enumerate(sl):
            ph = Image.open(find(folder, f'p{k+1}')).convert('RGB')
            fn = f'carrossel_{k+1}.jpg'; P.feed(ph, s['kicker'], s['title'], s['body'], f'{out}/{fn}'); files.append(fn)
        s = sl[0]; P.story(Image.open(find(folder, 'p1')).convert('RGB'), s['kicker'], s['title'], 'Novo post no perfil. Arraste e salve.', f'{out}/story_feed.jpg')
        acts19.append({'acao': 'create_carousel_post', 'arquivos': files, 'legenda': post['legenda']})
    acts19.append({'acao': 'create_story', 'arquivo': 'story_feed.jpg'})
    st = d['story']; P.story(Image.open(find(folder, 's1')).convert('RGB'), st['kicker'], st['title'], st['body'], f'{out}/story_extra.jpg')
    acts19.append({'acao': 'create_story', 'arquivo': 'story_extra.jpg'})
    plano = {'12h': [{'acao': 'create_video_post', 'arquivo': 'reel.mp4', 'legenda': d['reel']['legenda'], 'thumb_offset': 5500},
                     {'acao': 'create_story', 'arquivo': 'reel.mp4'}],
             '19h': acts19, 'videos_usados': [], 'musica': music_name,
             'tema': d['reel']['tema'] + ' + ' + post['tema']}
    json.dump(plano, open(f'{out}/plano.json', 'w'), ensure_ascii=False, indent=1)
    print('ok', out)

if __name__ == '__main__':
    a = sys.argv; main(a[1], a[2], a[3], a[4], float(a[5]) if len(a) > 5 else 0)
