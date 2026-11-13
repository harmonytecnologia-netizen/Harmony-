# MOVE Explica — Impedância (3D, Blender)
Modelo 3D da série MOVE Explica (personagens: amplificador com rosto no display, 4 caixas com olhos, cabos Bezier que "crescem" com plugues dourados).

Pipeline:
1. `scene.py` (Blender 5.x, bpy): monta cena + animação. `blender -b -P scene.py -- save` gera o .blend (Cycles). Também grava `events.json` (momentos de plugue/pop/alarme para o SFX).
2. Render no PC do João (GTX 1060, OptiX + CPU): 720x1280, 24 amostras, denoise OptiX → ~2,4 s/quadro, 720 quadros (30 s a 24 fps) em ~30 min. Script `ativar_gpu3.py` + `RENDER_RAPIDO.bat` ficam em Downloads\MOVE_render3D.
3. Narração: Piper TTS `pt_BR-faber-medium` (5 falas, s1–s5.wav).
4. `assemble.sh`: upscale 1080x1920, cartões de texto (ov/a–e.png) por tempo, voz posicionada, SFX (`sfx.wav`), música ducking sob a voz → MP4 final.
Resultado: anuncios/MOVE_explica_impedancia_3D.mp4
Para novo episódio: copiar scene.py, trocar personagens/ações e os cartões, refazer falas e tempos no assemble.sh.
