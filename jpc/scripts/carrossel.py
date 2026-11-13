import sys, json, asyncio
sys.path.insert(0, '/home/claude/harmony-/jpc/scripts')
from mascote import gabi
from playwright.async_api import async_playwright
from PIL import Image

CSS = '''
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:radial-gradient(circle at 80% 10%,#3a1a7a 0,#140a2b 45%,#07040f 100%);font-family:Poppins,sans-serif;color:#fff;position:relative;overflow:hidden}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(139,92,255,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(139,92,255,.08) 1px,transparent 1px);background-size:60px 60px}
.brand{position:absolute;top:56px;left:70px;font-weight:800;font-size:44px;letter-spacing:3px;background:linear-gradient(90deg,#8b5cff,#22d3ee,#ff4fd8);-webkit-background-clip:text;color:transparent}
.brand small{display:block;font-size:20px;letter-spacing:6px;color:#b9a8ff;-webkit-text-fill-color:#b9a8ff;font-weight:600}
.pg{position:absolute;top:66px;right:70px;font-size:26px;color:#b9a8ff;font-weight:600}
.num{font-size:150px;font-weight:900;line-height:1;background:linear-gradient(90deg,#8b5cff,#22d3ee);-webkit-background-clip:text;color:transparent}
h1{font-size:96px;line-height:1.02;font-weight:900;text-transform:uppercase}
h2{font-size:64px;line-height:1.08;font-weight:800}
.hl{color:#22d3ee}.pk{color:#ff4fd8}
.box{border-radius:28px;padding:30px 36px;font-size:36px;line-height:1.3;font-weight:600;margin-top:26px}
.err{background:rgba(255,60,90,.14);border:3px solid #ff3c5a}
.ok{background:rgba(34,238,140,.12);border:3px solid #22ee8c}
.tag{font-size:28px;font-weight:800;letter-spacing:2px;margin-bottom:8px}
.err .tag{color:#ff6b84}.ok .tag{color:#4dffa6}
.foot{position:absolute;bottom:56px;left:70px;right:70px;font-size:28px;color:#b9a8ff;font-weight:600;display:flex;justify-content:space-between}
.mas{position:absolute}
'''

def page(content, n, total, mood="feliz", mas_pos="right:40px;bottom:120px", mas_size=330):
    return f'''<html><head><style>{CSS}</style></head><body><div class="grid"></div>
<div class="brand">JPC<small>PC GAMER</small></div><div class="pg">{n}/{total}</div>
{content}
<div class="mas" style="{mas_pos}">{gabi(mood, mas_size)}</div>
<div class="foot"><span>@harmony_computer</span><span>{"arrasta ➜" if n<total else ""}</span></div></body></html>'''

async def render(slides, outdir):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width':1080,'height':1350})
        for i, html in enumerate(slides, 1):
            await pg.set_content(html); await pg.wait_for_timeout(300)
            png = f'{outdir}/s{i:02d}.png'
            await pg.screenshot(path=png)
            Image.open(png).convert('RGB').save(f'{outdir}/s{i:02d}.jpg', quality=92)
        await b.close()
