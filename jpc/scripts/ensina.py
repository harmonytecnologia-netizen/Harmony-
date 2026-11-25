"""JPC ENSINA — Reel tutorial (12h) + capa 1080x1920. Pedido do João em 24/11/2026.
Usado por produzir.py:  arq, capa, musica = ensina.reel_ensina(dia_dir, pauta, rng, usados)
Cada trecho (gancho, passo 1..N, final) tem narração Piper própria e o cartão aparece sincronizado com a fala.
Fundos: vídeos reais do João (biblioteca/reais) para hardware/defeitos; Pexels (biblioteca/videos) para Windows."""
import os, glob, json, subprocess, asyncio, shutil, html
import produzir as P

REAIS_HW=["20260521_202918.mp4","20260521_202944.mp4","20260525_095620.mp4","20260530_235102.mp4","20260506_175215.mp4"]
SELO="<div style='display:inline-flex;align-items:center;gap:14px;font-family:A;font-size:40px;letter-spacing:4px;padding:14px 30px;border-radius:16px;background:linear-gradient(90deg,#7a3cff,#ff4fd8);box-shadow:0 8px 0 rgba(0,0,0,.35),0 0 40px rgba(255,79,216,.45)'>🎓 JPC ENSINA</div>"
STROKE="-webkit-text-stroke:{w}px #000;paint-order:stroke fill;"
E=html.escape

def _hl(txt,dest,cls="hl"):
    t=E(txt)
    return t.replace(E(dest),f"<span class='{cls}'>{E(dest)}</span>",1) if dest and E(dest) in t else t

def _caminho(c):
    """Caminho de menu em 'janela' estilo Windows, com chips separados por ›."""
    if not c: return ""
    partes=[p.strip() for p in c.split(">")]
    chips="<span style='color:#22d3ee;margin:0 10px'>›</span>".join(
        f"<span style='display:inline-block;background:rgba(34,211,238,.14);border:2px solid rgba(34,211,238,.55);border-radius:12px;padding:6px 16px;margin:6px 0'>{E(p)}</span>" for p in partes)
    fs=40 if len(c)<55 else 34 if len(c)<85 else 30
    return f"""<div style='margin-top:40px;border-radius:22px;overflow:hidden;background:rgba(12,10,24,.88);border:2px solid rgba(255,255,255,.18);box-shadow:0 20px 60px rgba(0,0,0,.6)'>
<div style='display:flex;justify-content:space-between;align-items:center;padding:12px 22px;background:rgba(255,255,255,.08);font:700 26px P;color:#cfc6ff'><span>🪟 No seu PC</span><span style='letter-spacing:18px'>─ ▢ ✕</span></div>
<div style='padding:22px 26px 26px;font:700 {fs}px P;line-height:1.5'>{chips}</div></div>"""

def _cards(r):
    scrim="<div style='position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,4,15,.35),rgba(7,4,15,.72) 22%,rgba(7,4,15,.72) 78%,rgba(7,4,15,.45))'></div>"
    topo=f"<div style='position:absolute;top:262px;left:60px'>{SELO}</div>"
    n=len(r["passos"]); out=[]
    g=r["gancho"]; fs=150 if len(g)<20 else 128 if len(g)<28 else 110
    out.append(scrim+topo+f"""<div style='position:absolute;left:50px;right:50px;top:560px;text-align:center'>
<div class='h yl' style='font-size:{fs}px;{STROKE.format(w=14)}'>{_hl(g,r.get('destaque',''))}</div>
<div style='margin-top:50px;display:inline-block;font:700 50px P;padding:16px 36px;border-radius:999px;background:rgba(0,0,0,.6);border:2px solid #ffe14f'>PASSO A PASSO 👇</div></div>""")
    for i,(t,c,_) in enumerate(r["passos"]):
        barra="".join(f"<div style='flex:1;height:14px;border-radius:8px;background:{'#ffe14f' if k<=i else 'rgba(255,255,255,.22)'}'></div>" for k in range(n))
        fs=96 if len(t)<22 else 80 if len(t)<30 else 68
        out.append(scrim+topo+f"""<div style='position:absolute;left:60px;right:60px;top:420px;display:flex;gap:12px'>{barra}</div>
<div style='position:absolute;left:60px;right:60px;top:500px'>
<div style='display:flex;align-items:center;gap:34px'>
<div style='flex:none;width:230px;height:230px;border-radius:50%;background:#ffe14f;color:#07040f;font-family:A;font-size:190px;line-height:230px;text-align:center;box-shadow:0 0 0 10px #07040f,0 0 60px rgba(255,225,79,.6)'>{i+1}</div>
<div style='font:700 36px P;color:#cfc6ff'>PASSO {i+1} DE {n}</div></div>
<div class='h' style='margin-top:40px;font-size:{fs}px;{STROKE.format(w=10)}'>{E(t)}</div>
{_caminho(c)}</div>""")
    if r.get("tecnico"):
        fim=f"""<div class='h' style='font-size:110px;{STROKE.format(w=12)}'>Não resolveu?<br><span class='yl'>Chama a JPC</span></div>
<div class='cta' style='margin-top:50px;font-size:56px'>MANDA "TÉCNICO" NO DIRECT</div>
<div style='margin-top:36px;font:700 40px P'>Manutenção e upgrade · a gente resolve</div>"""
    else:
        fim=f"""<div class='h yl' style='font-size:116px;{STROKE.format(w=12)}'>💾 Salva<br>e manda pro amigo</div>
<div class='cta' style='margin-top:50px;font-size:50px'>MANDA "TÉCNICO" NO DIRECT</div>
<div style='margin-top:36px;font:700 40px P'>JPC · PC gamer, upgrade e manutenção</div>"""
    out.append(scrim+topo+f"<div style='position:absolute;left:50px;right:50px;top:560px;text-align:center'>{fim}</div>")
    return out

def html_capa(r):
    f=r["fundo_capa"]; t=r["capa"]; fs=200 if len(t)<14 else 172 if len(t)<19 else 150 if len(t)<24 else 128
    ia="<div class='ia' style='top:262px'>imagem ilustrativa</div>" if f.startswith("ia_") else ""
    return P.page(f"""<div class='bg' style="background-image:url('{P.fundo_url(f)}');filter:saturate(1.25) contrast(1.08)"></div>
<div class='shade' style='background:linear-gradient(180deg,rgba(7,4,15,.55) 0%,rgba(7,4,15,.15) 25%,rgba(7,4,15,.55) 50%,rgba(7,4,15,.92) 85%)'></div>
{ia}<div style='position:absolute;left:0;right:0;top:330px;text-align:center'>{SELO}</div>
<div style='position:absolute;left:50px;right:50px;top:700px;text-align:center'>
<div class='h yl' style='font-size:{fs}px;line-height:.95;{STROKE.format(w=18)}'>{_hl(t,r['capa_dest'],'hl')}</div>
<div style='margin-top:44px;display:inline-block;font:700 46px P;padding:14px 34px;border-radius:999px;background:#7a3cff;box-shadow:0 8px 0 rgba(0,0,0,.4)'>PASSO A PASSO EM {len(r['passos'])} ETAPAS</div></div>
<div style='position:absolute;left:0;right:0;top:1450px;text-align:center;font:700 34px P;color:#cfc6ff'>@harmony_computer</div>""",1080,1920)

def falas(r):
    fim=("Não resolveu? Chama a JPC: manda TÉCNICO no Direct que a gente resolve." if r.get("tecnico")
         else "Salva esse vídeo e manda pro amigo que tem PC lento. Precisa de ajuda? Manda TÉCNICO no Direct da JPC.")
    return [r["fala_gancho"]]+[p[2] for p in r["passos"]]+[fim]

def legenda(r,hashtags):
    num="\n".join(f"{i+1}️⃣ {x}" for i,x in enumerate(r["resumo"]))
    ext=("\n\n⚠️ Não resolveu? Chama a JPC: manda TÉCNICO no Direct que a gente resolve (manutenção e upgrade)." if r.get("tecnico") else "")
    tags=" ".join(dict.fromkeys((hashtags+" "+r.get("tags","")).split()))
    return (f"🎓 JPC ENSINA: {r['gancho']} 👇\n\n{num}{ext}\n\n💾 Salva pra fazer depois e manda pro amigo que tem PC lento\n\n{r['pergunta']}\n\n"
            f"Precisa de ajuda? Manda TÉCNICO ou ORÇAMENTO no Direct. Enviamos para todo o Brasil 🚚\n\n{tags}")

def _musica(usados,data):
    ms=sorted(glob.glob(f"{P.R}/biblioteca/musicas/*.mp3"))
    if not ms: return None
    ult=lambda m:max([i for i,u in enumerate(usados["musicas"]) if u[1]==os.path.basename(m)],default=-1)
    return sorted(ms,key=ult)[0]   # a usada há mais tempo

def _png(jobs):
    async def run():
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            br=await p.chromium.launch();pg=await br.new_page(viewport={"width":1080,"height":1920})
            for h,o,transp in jobs:
                t=o+".html";open(t,"w").write(h);await pg.goto("file://"+t);await pg.wait_for_load_state("networkidle");await pg.wait_for_timeout(300);os.remove(t)
                if transp: await pg.screenshot(path=o,omit_background=True)
                else: await pg.screenshot(path=o,type="jpeg",quality=90)
            await br.close()
    asyncio.run(run())

def reel_ensina(dia_dir,r,rng,usados,data):
    tmp=f"{dia_dir}/_tmp";os.makedirs(tmp,exist_ok=True)
    # 1) narração por trecho
    durs=[]
    for i,tx in enumerate(falas(r)):
        d=P.narrar(tx,f"{tmp}/n{i}.wav"); durs.append(round(max(2.6 if i==0 else 3.2, d+0.45),2))
    n=len(durs); dur=round(sum(durs)+0.6,2); durs[-1]+=0.6
    # 2) fundos: um clipe diferente por trecho (cortes rápidos)
    pex=sorted(glob.glob(f"{P.R}/biblioteca/videos/*.mp4"))
    reais=[f"{P.R}/biblioteca/reais/{x}" for x in REAIS_HW if os.path.exists(f"{P.R}/biblioteca/reais/{x}")]
    rng.shuffle(pex); rng.shuffle(reais)
    pool=(reais+pex) if r.get("videos")=="reais" else (pex+reais[:2])
    segs=[]
    for i,d in enumerate(durs):
        v=pool[i%len(pool)]; o=f"{tmp}/v{i}.mp4"
        vf=(f"scale=1200:2134:force_original_aspect_ratio=increase,crop=1080:1920:x='(iw-1080)*t/{d:.2f}':y='(ih-1920)/2',"
            "fps=30,eq=brightness=0.0:saturation=1.25,colorbalance=rs=.08:bs=.10")
        subprocess.run(["ffmpeg","-loglevel","error","-y","-stream_loop","-1","-ss","0.3","-t",f"{d:.2f}","-i",v,"-vf",vf,"-an","-c:v","libx264","-preset","veryfast","-crf","20",o],check=True);segs.append(o)
    open(f"{tmp}/l.txt","w").write("".join(f"file '{s}'\n" for s in segs))
    subprocess.run(["ffmpeg","-loglevel","error","-y","-f","concat","-safe","0","-i",f"{tmp}/l.txt","-c","copy",f"{tmp}/bg.mp4"],check=True)
    # 3) cartões + capa
    cards=_cards(r)
    jobs=[(P.page(b,1080,1920,"body{background:transparent}"),f"{tmp}/c{i}.png",True) for i,b in enumerate(cards)]
    jobs.append((html_capa(r),f"{dia_dir}/capa.jpg",False))
    _png(jobs)
    # 4) voz concatenada com o tempo de cada trecho
    ins=[];fa="";t0=0.0;tempos=[]
    for i,d in enumerate(durs):
        tempos.append((t0,t0+d)); ins+=["-i",f"{tmp}/n{i}.wav"]
        fa+=f"[{i}:a]adelay={int(t0*1000+200)}|{int(t0*1000+200)}[a{i}];"; t0+=d
    fa+="".join(f"[a{i}]" for i in range(n))+f"amix=inputs={n}:normalize=0,volume=1.7,atrim=0:{dur}[v]"
    subprocess.run(["ffmpeg","-loglevel","error","-y"]+ins+["-filter_complex",fa,"-map","[v]","-ar","44100","-ac","1",f"{tmp}/voz.wav"],check=True)
    m=_musica(usados,data)
    if m: mus=os.path.basename(m); mi=["-stream_loop","-1","-i",m]
    else:
        seed=rng.randint(1,10**6); P.trilha_sintetizada(f"{tmp}/t.wav",dur,seed); mus=f"trilha própria sintetizada #{seed}"; mi=["-i",f"{tmp}/t.wav"]
    args=["ffmpeg","-loglevel","error","-y","-i",f"{tmp}/bg.mp4"]
    for i in range(n): args+=["-loop","1","-t",str(dur),"-i",f"{tmp}/c{i}.png"]
    args+=["-i",f"{tmp}/voz.wav"]+mi
    fc="";last="0:v"
    for i,(a,b) in enumerate(tempos):
        fc+=f"[{i+1}:v]format=rgba,fade=t=in:st={a:.2f}:d=0.2:alpha=1[c{i}];"
        fc+=f"[{last}][c{i}]overlay=0:0:enable='between(t,{a:.2f},{b:.2f})'[x{i}];"; last=f"x{i}"
    fc+=(f"[{last}]format=yuv420p[v];[{n+2}:a]atrim=0:{dur},volume=0.09,afade=t=in:d=0.6,afade=t=out:st={dur-1.5}:d=1.5[mv];"
         f"[{n+1}:a][mv]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
    out=f"{dia_dir}/reel.mp4"
    subprocess.run(args+["-filter_complex",fc,"-map","[v]","-map","[a]","-t",str(dur),"-c:v","libx264","-preset","veryfast","-crf","21","-c:a","aac","-b:a","160k","-ar","44100","-movflags","+faststart",out],check=True)
    shutil.rmtree(tmp)
    return "reel.mp4","capa.jpg",(mus+" (Biblioteca de áudio do YouTube) + narração Piper") if m else mus+" + narração Piper", mus, dur
