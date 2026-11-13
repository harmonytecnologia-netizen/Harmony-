// Grava a animacao 2D (HTML/SVG) quadro a quadro e gera o video.
// uso: node render.js pagina.html saida_sem_som.mp4
// A pagina precisa ter: function render(t) {...}  (desenha o instante t em segundos)
//                       window.DURACAO = 28;      (duracao total em segundos)
const {chromium} = require('playwright'); const fs = require('fs'); const {execSync} = require('child_process'); const path = require('path');
const [page, out] = [process.argv[2] || 'exemplo_impedancia.html', process.argv[3] || 'animacao.mp4']; const FPS = 30;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({viewport: {width: 1080, height: 1920}});
  await p.goto('file://' + path.resolve(page)); await p.evaluate(() => document.fonts.ready);
  const D = await p.evaluate(() => window.DURACAO || 28); const dir = '_quadros2d'; fs.rmSync(dir, {recursive: true, force: true}); fs.mkdirSync(dir);
  const n = Math.round(D * FPS);
  for (let i = 0; i < n; i++) { await p.evaluate(t => render(t), i / FPS); await p.screenshot({path: `${dir}/${String(i).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 92}); if (i % 150 == 0) console.log(`${i}/${n}`); }
  await b.close();
  execSync(`ffmpeg -y -loglevel error -framerate ${FPS} -i ${dir}/%05d.jpg -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p ${out}`);
  console.log('ok', out);
})();
