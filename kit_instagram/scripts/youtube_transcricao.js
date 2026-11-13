// Copia a transcricao de um video do YouTube (rodar no console/javascript do navegador, na pagina do video).
// Pula anuncio, pausa, abre "Mostrar transcricao" e devolve o texto. Use para estudar cursos e transformar em regras da empresa.
(async () => {
  const sl = ms => new Promise(r => setTimeout(r, ms)); await sl(3000);
  for (let i = 0; i < 20; i++) { const s = [...document.querySelectorAll('button')].find(b => /^(Skip|Pular)/i.test((b.innerText || '').trim())); if (s) s.click(); if (!document.querySelector('.ad-showing')) break; await sl(1500); }
  const v = document.querySelector('video'); if (v) { v.muted = true; v.pause(); }
  document.querySelector('#expand')?.click(); await sl(1500);
  [...document.querySelectorAll('button')].find(x => /transcri/i.test((x.innerText || '') + (x.getAttribute('aria-label') || '')))?.click();
  let s = []; for (let k = 0; k < 15; k++) { await sl(1000); s = [...document.querySelectorAll('ytd-transcript-segment-renderer .segment-text, transcript-segment-view-model span')].map(e => e.innerText.trim()).filter(Boolean); if (s.length > 5) break; }
  return document.title + '\n\n' + s.join(' ');
})();
