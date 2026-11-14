#!/usr/bin/env python3
"""Robô de produção JPC (@harmony_computer).
Uso: python3 jpc/scripts/produzir.py            -> garante fila de hoje + 3 dias
     python3 jpc/scripts/produzir.py --data 2026-11-15 [--forcar]
     python3 jpc/scripts/produzir.py --emergencia HHh   -> gera peça avulsa para hoje no horário
Plano B: usa só o que já está no repositório (banco/pautas.json, biblioteca/fundos, biblioteca/videos, reels/prontos)."""
import json, os, sys, random, datetime, subprocess, asyncio, glob, shutil, zoneinfo
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../jpc
REPO=os.path.dirname(R)
RAW="https://raw.githubusercontent.com/harmonytecnologia-netizen/Harmony-/jpc/jpc/"
TZ=zoneinfo.ZoneInfo("America/Sao_Paulo")
BANCO=json.load(open(f"{R}/banco/pautas.json"))
USADOS_F=f"{R}/banco/usados.json"
USADOS=json.load(open(USADOS_F)) if os.path.exists(USADOS_F) else {"feed":[],"carrosseis":[],"stories":[],"fundos":[],"musicas":[]}
FONTS=f"file://{R}/fonts/"
CSS=f"""@font-face{{font-family:A;src:url({FONTS}anton-latin-400-normal.woff2)}}
@font-face{{font-family:B;src:url({FONTS}bangers-latin-400-normal.woff2)}}
@font-face{{font-family:P;src:url({FONTS}Poppins-Regular.ttf)}}@font-face{{font-family:P;font-weight:700;src:url({FONTS}Poppins-Bold.ttf)}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{overflow:hidden;color:#fff;font-family:P;background:#07040f}}
.bg{{position:absolute;inset:0;background-size:cover;background-position:center}}
.shade{{position:absolute;inset:0}}
.brand{{position:absolute;top:56px;left:60px;display:flex;gap:14px;align-items:center;font-family:A;font-size:34px;letter-spacing:4px;padding:12px 26px;border-radius:999px;background:rgba(10,5,25,.6);border:2px solid rgba(255,255,255,.25);backdrop-filter:blur(8px)}}
.brand i{{width:14px;height:14px;border-radius:50%;background:#22d3ee;box-shadow:0 0 14px #22d3ee}}
.ia{{position:absolute;right:40px;font:600 22px P;color:rgba(255,255,255,.75);background:rgba(0,0,0,.45);padding:6px 14px;border-radius:8px}}
.h{{font-family:A;text-transform:uppercase;line-height:.98;letter-spacing:1px;text-shadow:0 6px 30px rgba(0,0,0,.6)}}
.hl{{color:#22d3ee}} .pk{{color:#ff4fd8}} .yl{{color:#ffe14f}} .gn{{color:#3dff9a}}
.glass{{background:rgba(14,7,32,.72);border:2px solid rgba(255,255,255,.14);border-radius:34px;backdrop-filter:blur(18px);box-shadow:0 30px 80px rgba(0,0,0,.5)}}
.cta{{display:inline-block;font-family:A;letter-spacing:2px;padding:20px 40px;border-radius:999px;background:linear-gradient(90deg,#7a3cff,#ff4fd8);box-shadow:0 10px 0 rgba(0,0,0,.35),0 0 50px rgba(255,79,216,.45)}}
"""
def fundo_url(nome): return f"file://{R}/biblioteca/fundos/{nome}"
def escolhe_fundo(rng, evitar=()):
    fs=sorted(os.listdir(f"{R}/biblioteca/fundos"))
    rec=USADOS["fundos"][-6:]
    cand=[f for f in fs if f not in rec and f not in evitar] or fs
    f=rng.choice(cand); USADOS["fundos"].append(f); return f
def ia_tag(f): return f.startswith("ia_")
def hl(titulo,dest):
    return titulo.replace(dest,f'<span class="hl">{dest}</span>',1) if dest and dest in titulo else titulo

async def shots(jobs):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page()
        for html,w,h,out in jobs:
            await pg.set_viewport_size({"width":w,"height":h}); tmp=out+".html"; open(tmp,"w").write(html)
            await pg.goto("file://"+tmp); await pg.wait_for_load_state("networkidle"); await pg.wait_for_timeout(250); os.remove(tmp)
            await pg.screenshot(path=out,type="jpeg",quality=92)
        await b.close()
def page(body,w,h,extra=""): return f"<html><head><meta charset='utf-8'><style>{CSS} body{{width:{w}px;height:{h}px}} {extra}</style></head><body>{body}</body></html>"

def html_feed(it,f):
    t=hl(it["titulo"],it.get("destaque",""))
    return page(f"""<div class='bg' style="background-image:url('{fundo_url(f)}')"></div>
<div class='shade' style='background:linear-gradient(180deg,rgba(7,4,15,.35) 0%,rgba(7,4,15,.05) 30%,rgba(7,4,15,.75) 62%,rgba(7,4,15,.97) 100%)'></div>
<div class='brand'><i></i>JPC · PC GAMER</div>
{"<div class='ia' style='top:66px'>imagem ilustrativa</div>" if ia_tag(f) else ""}
<div style='position:absolute;left:60px;right:60px;bottom:250px'><div class='h' style='font-size:128px'>{t}</div>
<div style='margin-top:26px;font-size:40px;font-weight:700;line-height:1.3;max-width:900px'>{it["sub"]}</div></div>
<div style='position:absolute;left:60px;bottom:80px;font-size:34px' class='cta'>MANDA "ORÇAMENTO" NO DIRECT</div>
<div style='position:absolute;right:60px;bottom:96px;font:700 28px P;color:#b9a8ff'>@harmony_computer</div>""",1080,1350)

def html_slide(c,i,n,f):
    if i==0:
        return page(f"""<div class='bg' style="background-image:url('{fundo_url(f)}')"></div>
<div class='shade' style='background:linear-gradient(180deg,rgba(7,4,15,.4),rgba(7,4,15,.15) 35%,rgba(7,4,15,.92) 75%)'></div>
<div class='brand'><i></i>JPC · PC GAMER</div>{"<div class='ia' style='top:66px'>imagem ilustrativa</div>" if ia_tag(f) else ""}
<div style='position:absolute;left:60px;right:60px;bottom:200px'><div class='h' style='font-size:110px'>{c["capa"]}</div>
<div style='margin-top:30px;font:700 36px P;color:#22d3ee'>ARRASTA PRO LADO ➜</div></div>""",1080,1350)
    if i==n-1:
        return page(f"""<div class='bg' style="background-image:url('{fundo_url(f)}');filter:blur(14px) brightness(.45);transform:scale(1.1)"></div>
<div class='brand'><i></i>JPC · PC GAMER</div>
<div class='glass' style='position:absolute;left:70px;right:70px;top:300px;padding:70px 60px;text-align:center'>
<div class='h' style='font-size:92px'>Quer um PC <span class='hl'>sem esses problemas</span>?</div>
<div style='margin-top:34px;font:700 40px P;line-height:1.35'>A JPC monta, organiza e testa.<br>Enviamos para todo o Brasil.</div>
<div style='margin-top:50px;font-size:42px' class='cta'>MANDA "ORÇAMENTO" NO DIRECT</div>
<div style='margin-top:40px;font:700 32px P;color:#b9a8ff'>💾 Salva e manda pro seu duo</div></div>""",1080,1350)
    s=c["slides"][i-1]
    return page(f"""<div class='bg' style="background-image:url('{fundo_url(f)}');filter:blur(16px) brightness(.4);transform:scale(1.1)"></div>
<div class='brand'><i></i>JPC · PC GAMER</div><div style='position:absolute;top:70px;right:60px;font:700 30px P;color:#b9a8ff'>{i}/{n-2}</div>
<div class='glass' style='position:absolute;left:60px;right:60px;top:260px;bottom:180px;padding:70px 60px;display:flex;flex-direction:column;justify-content:center'>
<div class='h' style='font-size:170px;color:transparent;-webkit-text-stroke:3px #22d3ee'>{i:02d}</div>
<div class='h' style='font-size:92px;margin-top:20px'>{s["t"]}</div>
<div style='margin-top:36px;font:700 44px P;line-height:1.38;color:#e9e4ff'>{s["b"]}</div></div>
<div style='position:absolute;left:0;right:0;bottom:80px;text-align:center;font:700 30px P;color:#22d3ee'>{"ARRASTA ➜" if i<n-2 else "ÚLTIMO ➜"}</div>""",1080,1350)

def html_story(st,f):
    tipo,tx=st["tipo"],st["texto"]
    base=f"""<div class='bg' style="background-image:url('{fundo_url(f)}')"></div>
<div class='shade' style='background:linear-gradient(180deg,rgba(7,4,15,.55),rgba(7,4,15,.2) 30%,rgba(7,4,15,.85) 70%,rgba(7,4,15,.95))'></div>
<div class='brand' style='top:250px'><i></i>JPC · PC GAMER</div>{"<div class='ia' style='top:262px'>imagem ilustrativa</div>" if ia_tag(f) else ""}"""
    if tipo=="ab":
        a,b=tx.split("|")
        body=f"""<div style='position:absolute;left:60px;right:60px;top:820px;text-align:center'><div class='h yl' style='font-size:120px'>A ou B?</div>
<div style='display:flex;gap:30px;margin-top:40px'><div class='glass' style='flex:1;padding:50px 20px;font:700 50px P'>🅰️<br>{a}</div><div class='glass' style='flex:1;padding:50px 20px;font:700 50px P'>🅱️<br>{b}</div></div>
<div style='margin-top:50px;font-size:44px' class='cta'>RESPONDE NO DIRECT 👇</div></div>"""
    else:
        lab={"dica":("DICA RÁPIDA","hl"),"pergunta":("PERGUNTA DO DIA","pk"),"curiosidade":("VOCÊ SABIA?","yl"),"agenda":("AGENDA ABERTA","gn")}[tipo]
        cta={"pergunta":"RESPONDE NO DIRECT 👇","agenda":'MANDA "ORÇAMENTO" NO DIRECT',"dica":"SALVA E MANDA PRO DUO 💾","curiosidade":"SABIA DISSO? RESPONDE 👇"}[tipo]
        body=f"""<div class='glass' style='position:absolute;left:60px;right:60px;top:860px;padding:60px 54px'>
<div class='h {lab[1]}' style='font-size:70px'>{lab[0]}</div><div style='margin-top:26px;font:700 {58 if len(tx)<70 else 48}px P;line-height:1.3'>{tx}</div></div>
<div style='position:absolute;left:0;right:0;top:1440px;text-align:center'><div class='cta' style='font-size:40px'>{cta}</div></div>"""
    return page(base+body,1080,1920)

def html_story_repost(img_url,label):
    return page(f"""<div class='bg' style="background-image:url('{img_url}');filter:blur(30px) brightness(.5);transform:scale(1.2)"></div>
<div style='position:absolute;left:0;right:0;top:300px;text-align:center'><span class='cta' style='font-size:40px'>{label}</span></div>
<img src='{img_url}' style='position:absolute;left:115px;top:420px;width:850px;border-radius:30px;box-shadow:0 40px 90px rgba(0,0,0,.7)'>
<div style='position:absolute;left:0;right:0;top:1520px;text-align:center;font:700 40px P'>Toca no perfil pra ver 👆<br><span style='color:#22d3ee'>@harmony_computer</span></div>""",1080,1920)

def proximo(lista,chave):
    usados=USADOS[chave]
    for it in lista:
        if it["id"] not in usados: usados.append(it["id"]); return it
    # banco acabou: recomeça pelo mais antigo (e avisa no log)
    print(f"AVISO: banco '{chave}' esgotado, reutilizando o mais antigo. Escreva novas pautas em banco/gerar_banco.py.")
    it=next(x for x in lista if x["id"]==usados[0]); usados.remove(it["id"]); usados.append(it["id"]); return it

def musica(rng):
    ms=sorted(glob.glob(f"{R}/biblioteca/musicas/*.mp3"))
    rec=[m for d,m in USADOS["musicas"][-21:]]
    livres=[m for m in ms if os.path.basename(m) not in rec]
    if livres: return rng.choice(livres)
    return None

def trilha_sintetizada(path,dur,seed):
    import numpy as np, wave
    SR=44100;n=int(SR*dur);rng=np.random.default_rng(seed);out=np.zeros(n)
    T=lambda d:np.arange(int(SR*d))/SR;N=lambda m:440*2**((m-69)/12)
    def put(s,at):
        i=int(at*SR);j=min(n,i+len(s));out[i:j]+=s[:j-i]
    bpm=rng.integers(100,150);b=60/bpm;root=int(rng.integers(38,46))
    prog=[[0,3,7],[-4,0,3],[3,7,10],[-2,2,5]];rng.shuffle(prog)
    t0=0;k=0
    while t0<dur:
        ch=prog[k%4]
        for s in range(8):
            tt=t0+s*b/2
            if tt>=dur:break
            if s in(0,4)or(s==3 and k%2):t=T(.3);put(.9*np.sin(2*np.pi*(45+110*np.exp(-t*28))*t)*np.exp(-t*9),tt)
            if s in(2,6):t=T(.18);put(.3*rng.standard_normal(len(t))*np.exp(-t*20),tt)
            t=T(.04);put(.06*rng.standard_normal(len(t))*np.exp(-t*90),tt)
            t=T(b/2*.9);f=N(root+ch[0]+(12 if s%2 else 0));put(.18*(2*((t*f)%1)-1)*np.exp(-t*3),tt)
            t=T(b/2*.7);f=N(root+24+ch[s%3]);put(.05*np.sin(2*np.pi*f*t)*np.exp(-t*6),tt)
        k+=1;t0+=b*4
    out=out/np.max(np.abs(out))*.8;fl=int(SR*.8);out[-fl:]*=np.linspace(1,0,fl)
    w=wave.open(path,'w');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype('int16').tobytes());w.close()

def reel_planoB(dia_dir,it,rng):
    """Reel de dica com vídeos da biblioteca + textos animados (cartões renderizados) + música."""
    vids=sorted(glob.glob(f"{R}/biblioteca/videos/*.mp4"));rng.shuffle(vids);vids=vids[:3]
    segs=[];tmp=f"{dia_dir}/_tmp";os.makedirs(tmp,exist_ok=True)
    for i,v in enumerate(vids):
        o=f"{tmp}/v{i}.mp4";subprocess.run(["ffmpeg","-loglevel","error","-y","-ss","0.5","-t","6","-i",v,"-vf","scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,eq=brightness=-0.12:saturation=1.2","-an","-c:v","libx264","-preset","veryfast","-crf","20",o],check=True);segs.append(o)
    open(f"{tmp}/l.txt","w").write("".join(f"file '{s}'\n" for s in segs))
    subprocess.run(["ffmpeg","-loglevel","error","-y","-f","concat","-safe","0","-i",f"{tmp}/l.txt","-c","copy",f"{tmp}/bg.mp4"],check=True)
    dur=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{tmp}/bg.mp4"]))
    cards=[("gancho",it["titulo"]),("txt",it["sub"]),("cta",'Manda "ORÇAMENTO" no Direct')]
    jobs=[]
    for i,(k,tx) in enumerate(cards):
        if k=="gancho": b=f"<div style='position:absolute;left:60px;right:60px;top:560px;text-align:center'><div class='h' style='font-size:150px'>{hl(tx,it.get('destaque',''))}</div></div>"
        elif k=="txt": b=f"<div class='glass' style='position:absolute;left:60px;right:60px;top:1150px;padding:50px;text-align:center;font:700 52px P;line-height:1.3'>{tx}</div>"
        else: b=f"<div style='position:absolute;left:0;right:0;top:700px;text-align:center'><div class='h' style='font-size:100px'>Quer um PC <span class='hl'>nível PRO</span>?</div><div class='cta' style='margin-top:40px;font-size:48px'>{tx}</div><div style='margin-top:30px;font:700 36px P'>JPC · enviamos pra todo o Brasil</div></div>"
        b="<div class='brand' style='top:250px'><i></i>JPC · PC GAMER</div>"+b
        jobs.append((page(b,1080,1920,"body{background:transparent}"),1080,1920,f"{tmp}/c{i}.png"))
    async def png(jobs):
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            br=await p.chromium.launch();pg=await br.new_page(viewport={"width":1080,"height":1920})
            for h,w,hh,o in jobs:
                tmp=o+".html";open(tmp,"w").write(h);await pg.goto("file://"+tmp);await pg.wait_for_load_state("networkidle");await pg.wait_for_timeout(250);os.remove(tmp)
                await pg.screenshot(path=o,omit_background=True)
            await br.close()
    asyncio.run(png(jobs))
    m=musica(rng); aud=f"{tmp}/a.wav"
    if m: subprocess.run(["ffmpeg","-loglevel","error","-y","-i",m,"-t",str(dur),"-af",f"afade=t=out:st={dur-1}:d=1",aud],check=True); nome=os.path.basename(m)
    else: seed=rng.randint(1,10**6); trilha_sintetizada(aud,dur,seed); nome=f"trilha própria sintetizada #{seed}"
    a,bm,c=0.3,dur*0.38,dur*0.75
    fc=(f"[0][1]overlay=0:0:enable='between(t,{a},{bm})'[x1];[x1][2]overlay=0:0:enable='between(t,{bm},{c})'[x2];"
        f"[x2][3]overlay=0:0:enable='between(t,{c},{dur})',format=yuv420p[v]")
    out=f"{dia_dir}/reel.mp4"
    subprocess.run(["ffmpeg","-loglevel","error","-y","-i",f"{tmp}/bg.mp4","-i",f"{tmp}/c0.png","-i",f"{tmp}/c1.png","-i",f"{tmp}/c2.png","-i",aud,
        "-filter_complex",fc,"-map","[v]","-map","4:a","-c:v","libx264","-preset","veryfast","-crf","20","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",out],check=True)
    shutil.rmtree(tmp); return "reel.mp4",nome

def reel_pronto():
    """Usa primeiro um Reel caprichado da fila reels/prontos/*.json (feito com arte do ChatGPT)."""
    for j in sorted(glob.glob(f"{R}/reels/prontos/*.json")):
        d=json.load(open(j))
        if not d.get("usado"): d["usado"]=True; json.dump(d,open(j,"w"),ensure_ascii=False,indent=1); return d
    return None

def legenda(txt): return txt.strip()+"\n\nQuer montar o seu? Manda ORÇAMENTO no Direct. Enviamos para todo o Brasil 🚚\n\n"+BANCO["hashtags"]

def produzir_dia(data,forcar=False):
    dia_dir=f"{R}/fila/{data}"; pj=f"{dia_dir}/plano.json"
    if os.path.exists(pj) and not forcar: print("já existe",data); return False
    os.makedirs(dia_dir,exist_ok=True); rng=random.Random(data)
    dt=datetime.date.fromisoformat(data); url=lambda n:f"{RAW}fila/{data}/{n}"
    plano={"data":data,"perfil":"harmony_computer","conta_windsor":"17841445277894628","09h":[],"12h":[],"15h":[],"19h":[],"21h":[]}
    jobs=[]
    # 12h feed
    it=proximo(BANCO["feed"],"feed"); f=escolhe_fundo(rng)
    jobs.append((html_feed(it,f),1080,1350,f"{dia_dir}/feed.jpg"))
    # 19h carrossel
    c=proximo(BANCO["carrosseis"],"carrosseis"); n=len(c["slides"])+2; fc=escolhe_fundo(rng,(f,))
    for i in range(n): jobs.append((html_slide(c,i,n,fc),1080,1350,f"{dia_dir}/car_{i+1:02d}.jpg"))
    # stories próprios: 2 às 09h,1 às 15h, 2 às 21h (5 por dia)
    sts=[proximo(BANCO["stories"],"stories") for _ in range(5)]
    for i,st in enumerate(sts): jobs.append((html_story(st,escolhe_fundo(rng)),1080,1920,f"{dia_dir}/story_{i+1}.jpg"))
    asyncio.run(shots(jobs))
    # stories de repost (usam a arte já renderizada)
    asyncio.run(shots([(html_story_repost(f"file://{dia_dir}/feed.jpg","NOVO POST 🔥"),1080,1920,f"{dia_dir}/story_feed.jpg"),
                       (html_story_repost(f"file://{dia_dir}/car_01.jpg","CARROSSEL NOVO 👉"),1080,1920,f"{dia_dir}/story_car.jpg")]))
    plano["12h"].append({"acao":"create_image_post","arquivo":url("feed.jpg"),"legenda":legenda(it["legenda"]),"pauta":it["id"]})
    plano["12h"].append({"acao":"create_story","arquivo":url("story_feed.jpg")})
    if dt.weekday() in (0,2,4):
        pr=reel_pronto()
        if pr: plano["12h"]+= [{"acao":"create_video_post","arquivo":pr["video_url"],"legenda":pr["legenda"],"thumb_offset":pr.get("thumb_offset",1500),"musica":pr.get("musica","")},
                               {"acao":"create_story","arquivo":pr["video_url"],"tipo":"video"}]
        else:
            ri=proximo(BANCO["feed"],"feed"); arq,mus=reel_planoB(dia_dir,ri,rng); USADOS["musicas"].append([data,mus if not mus.startswith("trilha") else mus])
            plano["12h"]+= [{"acao":"create_video_post","arquivo":url(arq),"legenda":legenda(ri["legenda"]),"thumb_offset":1000,"musica":mus,"pauta":ri["id"]},
                            {"acao":"create_story","arquivo":url(arq),"tipo":"video"}]
    plano["19h"].append({"acao":"create_carousel_post","arquivos":[url(f"car_{i+1:02d}.jpg") for i in range(n)],"legenda":legenda(c["capa"]+" 👉 arrasta pro lado!\n\n💾 Salva pra consultar depois e manda pro amigo."),"pauta":c["id"]})
    plano["19h"].append({"acao":"create_story","arquivo":url("story_car.jpg")})
    plano["09h"]=[{"acao":"create_story","arquivo":url("story_1.jpg"),"pauta":sts[0]["id"]},{"acao":"create_story","arquivo":url("story_2.jpg"),"pauta":sts[1]["id"]}]
    plano["15h"]=[{"acao":"create_story","arquivo":url("story_3.jpg"),"pauta":sts[2]["id"]}]
    plano["21h"]=[{"acao":"create_story","arquivo":url("story_4.jpg"),"pauta":sts[3]["id"]},{"acao":"create_story","arquivo":url("story_5.jpg"),"pauta":sts[4]["id"]}]
    json.dump(plano,open(pj,"w"),ensure_ascii=False,indent=1)
    json.dump(USADOS,open(USADOS_F,"w"),ensure_ascii=False,indent=1)
    print("pronto",data); return True

def emergencia(hora):
    hoje=datetime.datetime.now(TZ).date().isoformat(); dia_dir=f"{R}/fila/{hoje}/emergencia_{hora}"; os.makedirs(dia_dir,exist_ok=True)
    rng=random.Random(hoje+hora); st=proximo(BANCO["stories"],"stories")
    asyncio.run(shots([(html_story(st,escolhe_fundo(rng)),1080,1920,f"{dia_dir}/story.jpg")]))
    json.dump(USADOS,open(USADOS_F,"w"),ensure_ascii=False,indent=1)
    print(json.dumps({"acao":"create_story","arquivo":f"{RAW}fila/{hoje}/emergencia_{hora}/story.jpg"}))

if __name__=="__main__":
    a=sys.argv[1:]
    if "--emergencia" in a: emergencia(a[a.index("--emergencia")+1]); sys.exit()
    if "--data" in a: produzir_dia(a[a.index("--data")+1],"--forcar" in a); sys.exit()
    hoje=datetime.datetime.now(TZ).date()
    for k in range(4): produzir_dia((hoje+datetime.timedelta(k)).isoformat())
