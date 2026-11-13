# Kit Crescimento Instagram — pacote de ferramentas
Para o Claude (ou quem for usar): anexe este .zip numa conversa com o Claude e diga
"Use o kit de crescimento para o Instagram da minha empresa". O Claude le KIT_PASSO_A_PASSO.md,
faz as perguntas sobre a empresa e o nicho e vai adaptando tudo conforme as respostas.

## Primeiros passos (o Claude faz)
1. Descompactar e rodar `bash instalar.sh` (ffmpeg, Python, Piper, Playwright — tudo gratis).
2. Entrevista (secao 0 do KIT_PASSO_A_PASSO.md) e preencher `marca.json` (nome, @, cores, estilo premium/direto, frases finais).
3. Colocar o logo da empresa como `logo.png` (fundo transparente) ao lado do marca.json.
4. Testar com os exemplos da pasta `exemplos/` trocando as fotos/videos pelos da empresa.

## Ferramentas (pasta scripts/)
| Script | Faz | Uso |
|---|---|---|
| reel_videos.py | Reel PRO a partir de videos reais do celular (estabiliza, cor, cortes no ritmo, legendas animadas, tela final) | `python3 scripts/reel_videos.py exemplos/reel_videos.json saida.mp4` |
| reel_imagens.py | Reel a partir de fotos (reais ou do ChatGPT) com movimento de camera | `python3 scripts/reel_imagens.py exemplos/reel_fotos.json saida.mp4` |
| arte_post.py | Arte de feed (1080x1350) + story (1080x1920) com logo e textos | `python3 scripts/arte_post.py foto.jpg "CHAMADA" "Titulo|linha 2" "detalhe" feed.jpg story.jpg [--ia]` |
| narracao.py | Voz em portugues gratis (Piper, voz faber ja inclusa em modelos/) | `python3 scripts/narracao.py "texto" fala.wav 0.95` |
| efeitos_sonoros.py | Cliques, pop, ding, erro, alarme, whoosh por tempo (sem direito autoral) | `python3 scripts/efeitos_sonoros.py exemplos/efeitos.json 30 sfx.wav` |
| montar_explicativo.py | Video final da serie "Explica": animacao + cartoes de texto + voz + efeitos + musica abaixando sob a voz | `python3 scripts/montar_explicativo.py exemplos/explicativo.json final.mp4` |
| youtube_transcricao.js | Copia a transcricao de um video do YouTube no navegador (estudar cursos) | colar no console da pagina do video |
| animacao2d/ | Desenho animado 2D em HTML/SVG + render.js (quadro a quadro) | `node animacao2d/render.js pagina.html anim.mp4` |
| animacao3d/ | Personagens 3D no Blender + ativar_gpu.py + RENDERIZAR.bat para a placa de video do PC | ver animacao3d/LEIA-ME.md |

Musica: Biblioteca de audio do YouTube Studio ou Pixabay (gratis, sem direitos). Uma faixa diferente por post.
Fontes inclusas: Inter e Playfair Display (licenca OFL). Voz: Piper pt_BR faber (licenca livre).

## Regras que nao mudam
Somente a conta da empresa informada; conteudo so do nicho dela; IA marcada como "Ambiente conceito";
sem depoimento falso; senha, documentos e pagamento sempre com a pessoa; verba de anuncio so com OK.
