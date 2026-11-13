# Animacao 3D (Blender) — personagens com rosto
1. Instalar Blender: no Windows, pela Microsoft Store ("Blender") — evita bloqueio do Controle Inteligente de Aplicativos. No ambiente do Claude: `pip install bpy` (Python 3.11) ou baixar do blender.org.
2. Claude escreve `cena.py` para o tema (use `cena_exemplo_impedancia.py` como modelo: personagens = caixas/aparelhos com olhos e boca, rosto que muda de cor verde/vermelho, cabos Bezier que "crescem", camera animada, eventos gravados em events.json para os efeitos sonoros).
   - Teste rapido no ambiente do Claude: renderizar 4-5 quadros pequenos e OLHAR antes do render completo.
   - Gerar o .blend: `python3 cena.py save` (ou `blender -b -P cena.py -- save`) -> cena.blend.
3. Copiar cena.blend + ativar_gpu.py + RENDERIZAR.bat para uma pasta no PC da pessoa e rodar RENDERIZAR.bat.
   Referencia: GTX 1060 + OptiX, 720x1280, 24 amostras = ~2,4 s/quadro (720 quadros ~ 30 min). Sem placa de video: 3-10x mais lento.
4. Trazer os quadros e montar com `scripts/montar_explicativo.py` (sobe para 1080x1920, cartoes de texto, voz, efeitos, musica).
