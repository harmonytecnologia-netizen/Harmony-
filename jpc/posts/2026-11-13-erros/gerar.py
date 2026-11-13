import sys, asyncio
sys.path.insert(0,'/home/claude/harmony-/jpc/scripts')
from carrossel import page, render
T=7
def erro(n, titulo, errado, certo, mood="alerta"):
    return page(f'''<div style="position:absolute;top:190px;left:70px;right:70px">
<div class="num">#{n}</div><h2>{titulo}</h2>
<div class="box err" style="margin-right:300px"><div class="tag">✖ ERRADO</div>{errado}</div>
<div class="box ok" style="margin-right:300px"><div class="tag">✔ CERTO</div>{certo}</div></div>''', n+1, T, mood, "right:20px;bottom:110px", 290)
s=[]
s.append(page('''<div style="position:absolute;top:230px;left:70px;right:70px">
<div style="font-size:40px;font-weight:700;color:#b9a8ff;margin-bottom:20px">MESMO COM PLACA BOA…</div>
<h1>5 erros que<br>deixam seu<br><span class="hl">PC gamer</span><br><span class="pk">fraco</span></h1>
<div style="font-size:38px;font-weight:600;margin-top:34px;max-width:560px">O <span class="hl">nº 3</span> quase todo mundo comete 👀</div></div>''',1,T,"alerta","right:30px;bottom:110px",400))
s.append(erro(1,'Memória em <span class="hl">1 pente só</span>','1 pente de 16 GB e o XMP desligado na BIOS: a memória roda mais lenta que pode.','2 pentes de 8 GB (dual channel) e XMP/EXPO ligado. Mais FPS sem trocar a placa.'))
s.append(erro(2,'Fonte <span class="pk">genérica</span>','Fonte sem marca, sem selo, “500 W” no adesivo. Na carga cai, desliga ou leva peça junto.','Fonte de marca com selo 80 Plus e potência certa para a placa. É ela que protege o resto.'))
s.append(erro(3,'Monitor na <span class="hl">placa-mãe</span>','Cabo do monitor ligado na saída da placa-mãe. A placa de vídeo nem é usada!','Cabo HDMI/DisplayPort na saída da PLACA DE VÍDEO (as saídas mais baixas, na horizontal).',"triste"))
s.append(erro(4,'Jogo e Windows no <span class="pk">HD</span>','Sistema e jogos num HD comum: demora pra ligar, travadinha ao carregar mapa.','SSD (de preferência NVMe) para o Windows e os jogos. HD só para guardar arquivo.'))
s.append(erro(5,'PC <span class="hl">fervendo</span>','Gabinete fechado, sem ventoinha, cheio de poeira. Esquenta e a placa reduz o desempenho.','Ventoinha na frente puxando ar, atrás/em cima soltando. Limpeza a cada 6 meses.'))
s.append(page('''<div style="position:absolute;top:240px;left:70px;right:70px">
<h1 style="font-size:84px">Quer montar o seu <span class="hl">sem erro</span>?</h1>
<div style="font-size:40px;font-weight:600;margin-top:40px;line-height:1.4;max-width:600px">A JPC monta e envia para <span class="hl">todo o Brasil</span> 🚚</div>
<div style="margin-top:50px;display:inline-block;padding:26px 44px;border-radius:999px;background:linear-gradient(90deg,#8b5cff,#22d3ee);font-size:42px;font-weight:800">Manda ORÇAMENTO no Direct</div>
<div style="font-size:34px;margin-top:40px;color:#b9a8ff;font-weight:600">💾 Salva e envia pro amigo que vai montar PC</div></div>''',7,T,"feliz","right:30px;bottom:110px",340))
asyncio.run(render(s,'/home/claude/harmony-/jpc/posts/2026-11-13-erros'))
