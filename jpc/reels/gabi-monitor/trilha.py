import numpy as np, wave
SR=44100; D=26.5; n=int(SR*D); t=np.arange(n)/SR; out=np.zeros(n)
bpm=118; beat=60/bpm
def env(x,a,d): return np.where(x<0,0,np.where(x<a,x/a,np.exp(-(x-a)/d)))
# kick
for k in np.arange(0,D,beat):
    i=int(k*SR); L=int(.35*SR); tt=np.arange(min(L,n-i))/SR
    out[i:i+len(tt)]+=0.55*np.sin(2*np.pi*(50+90*np.exp(-tt*25))*tt)*np.exp(-tt*9)
# hat
rng=np.random.default_rng(1)
for k in np.arange(beat/2,D,beat):
    i=int(k*SR); L=int(.06*SR); tt=np.arange(min(L,n-i))/SR
    out[i:i+len(tt)]+=0.08*rng.standard_normal(len(tt))*np.exp(-tt*60)
# acordes (Am F C G) synth pad
ch=[[220,261.6,329.6],[174.6,220,261.6],[196,261.6,329.6],[196,246.9,293.7]]
bar=beat*4
for j,s in enumerate(np.arange(0,D,bar)):
    i=int(s*SR); L=int(bar*SR); tt=np.arange(min(L,n-i))/SR
    for f in ch[j%4]:
        out[i:i+len(tt)]+=0.05*(np.sign(np.sin(2*np.pi*f*tt))*0.4+np.sin(2*np.pi*f*tt))*np.minimum(1,tt*4)*np.exp(-tt*0.4)
# arpejo
for j,s in enumerate(np.arange(0,D,beat/2)):
    f=ch[int(s//bar)%4][j%3]*2; i=int(s*SR); L=int(.2*SR); tt=np.arange(min(L,n-i))/SR
    out[i:i+len(tt)]+=0.05*np.sin(2*np.pi*f*tt)*np.exp(-tt*14)
# sfx
def whoosh(at):
    i=int(at*SR); L=int(.45*SR); tt=np.arange(min(L,n-i))/SR
    nz=rng.standard_normal(len(tt)); nz=np.convolve(nz,np.ones(30)/30,'same')
    out[i:i+len(tt)]+=0.5*nz*np.sin(np.pi*tt/.45)
def click(at):
    i=int(at*SR); L=int(.08*SR); tt=np.arange(min(L,n-i))/SR
    out[i:i+len(tt)]+=0.5*np.sin(2*np.pi*1800*tt)*np.exp(-tt*80)
def ding(at,f=1318):
    i=int(at*SR); L=int(.8*SR); tt=np.arange(min(L,n-i))/SR
    out[i:i+len(tt)]+=0.25*(np.sin(2*np.pi*f*tt)+.5*np.sin(2*np.pi*f*1.5*tt))*np.exp(-tt*5)
def buzz(at):
    i=int(at*SR); L=int(.4*SR); tt=np.arange(min(L,n-i))/SR
    out[i:i+len(tt)]+=0.18*np.sign(np.sin(2*np.pi*110*tt))*np.exp(-tt*6)
for a in [3.1,16.9,22.4]: whoosh(a)
click(1.2); buzz(4.5); click(11.8); ding(12.0); ding(23.0,1046)
out=out/np.max(np.abs(out))*0.85
w=wave.open('trilha.wav','w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
