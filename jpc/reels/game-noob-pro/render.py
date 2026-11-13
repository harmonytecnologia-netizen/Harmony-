import asyncio, os
from playwright.async_api import async_playwright
FPS=30; DUR=31.5
async def m():
    os.makedirs('f',exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto('file://'+os.getcwd()+'/index.html'); await pg.wait_for_timeout(600)
        for i in range(int(DUR*FPS)):
            await pg.evaluate(f'render({i/FPS})')
            await pg.screenshot(path=f'f/{i:04d}.png',omit_background=True)
        await b.close()
asyncio.run(m())
