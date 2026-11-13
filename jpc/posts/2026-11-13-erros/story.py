import sys, asyncio
sys.path.insert(0,'/home/claude/harmony-/jpc/scripts')
from carrossel import CSS
from mascote import gabi
from playwright.async_api import async_playwright
from PIL import Image
html=f'''<html><head><style>{CSS} body{{height:1920px}}</style></head><body><div class="grid"></div>
<div style="position:absolute;top:300px;left:80px;right:80px;text-align:center">
<div style="font-size:44px;font-weight:800;letter-spacing:4px;color:#b9a8ff">NOVO POST 🔥</div>
<h1 style="margin-top:30px;font-size:100px">5 erros que<br>deixam seu<br><span class="hl">PC gamer</span> <span class="pk">fraco</span></h1>
<div style="font-size:44px;font-weight:600;margin-top:40px">Qual desses tem no seu PC? 👀</div></div>
<div style="position:absolute;left:50%;transform:translateX(-50%);top:1060px">{gabi("alerta",380)}</div>
<div style="position:absolute;bottom:260px;left:0;right:0;text-align:center;font-size:40px;font-weight:700;color:#22d3ee">Toca no post no perfil @harmony_computer</div>
</body></html>'''
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        await pg.set_content(html); await pg.wait_for_timeout(300); await pg.screenshot(path='/tmp/st.png'); await b.close()
    Image.open('/tmp/st.png').convert('RGB').save('story.jpg',quality=92)
asyncio.run(m())
