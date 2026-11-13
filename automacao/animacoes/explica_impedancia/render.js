const {chromium}=require('playwright');const fs=require('fs');
const scenes=[[0,4],[4,11.5],[11.5,19.5],[19.5,24],[24,28]];const FPS=30;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/index.html');await p.evaluate(()=>document.fonts.ready);
for(let s=0;s<scenes.length;s++){const d=`f${s}`;fs.rmSync(d,{recursive:true,force:true});fs.mkdirSync(d);
 const [a,z]=scenes[s];const n=Math.round((z-a)*FPS);
 for(let i=0;i<n;i++){const t=a+i/FPS;await p.evaluate(t=>render(t),t);await p.screenshot({path:`${d}/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}
 console.log('scene',s,n);}
await b.close();})();
