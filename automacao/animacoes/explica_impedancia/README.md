# MOVE Explica — modelo de animação
Vídeo desenhado em código (SVG + JS), sem IA de vídeo: diagramas tecnicamente corretos.
- index.html: cena + função render(t). Personagens: amplificador (rosto no display) e caixas de som com olhos.
- render.js: gera quadros JPEG por cena (Playwright, 30 fps). Depois: ffmpeg por cena → concat → música + efeitos (sfx sintetizados em Python).
- Para novo episódio: copiar a pasta, trocar textos/diagrama/timeline em render(t).
Saída: ../../anuncios/MOVE_explica_impedancia.mp4 (28 s, 1080x1920).
