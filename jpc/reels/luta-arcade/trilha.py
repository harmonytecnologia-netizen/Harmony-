import numpy as np, wave
SR=44100; D=25.5; n=int(SR*D); mus=np.zeros(n); sfx=np.zeros(n); rng=np.random.default_rng(5)
T=lambda d:np.arange(int(SR*d))/SR; N=lambda m:440*2**((m-69)/12)
def put(buf,s,at,g=1.0):
    i=int(at*SR); j=min(n,i+len(s)); buf[i:j]+=g*s[:j-i]
def saw(f,d,v,det=.004):
    t=T(d); w=sum((2*((t*f*(1+k*det))%1)-1) for k in(-1,0,1))/3; return v*w*np.minimum(1,t*120)*np.exp(-t*2.2)
def kick(at): t=T(.32); put(mus,1.0*np.sin(2*np.pi*(42+140*np.exp(-t*28))*t)*np.exp(-t*9),at)
def snare(at): t=T(.22); put(mus,.45*rng.standard_normal(len(t))*np.exp(-t*18)+.25*np.sin(2*np.pi*200*t)*np.exp(-t*22),at)
def hat(at,o=False): t=T(.12 if o else .04); put(mus,.09*rng.standard_normal(len(t))*np.exp(-t*(30 if o else 100)),at)
bpm=152; b=60/bpm
prog=[(45,[57,60,64]),(41,[53,57,60]),(43,[55,59,62]),(40,[52,55,59])]
lead=[76,74,72,74,76,79,76,74, 72,72,74,76,72,69,67,69]
t0=0;bar=0
while t0<D:
    root,ch=prog[bar%4]
    for s in range(8):
        tt=t0+s*b/2
        if tt>=D: break
        if s in(0,3,5): kick(tt)
        if s in(2,6): snare(tt)
        hat(tt,s%2==1)
        put(mus,saw(N(root-12+(12 if s%2 else 0)),b/2*.95,.22),tt)
        if bar>=1: put(mus,saw(N(lead[(bar*8+s)%16]),b/2*.8,.07),tt)
    for f in ch: put(mus,saw(N(f),b*4,.035,.008),t0)
    bar+=1; t0+=b*4
# calmaria no apagão
i0,i1=int(6.9*SR),int(11.6*SR); mus[i0:i1]*=0.18
def zap(at,d): t=T(d); put(sfx,.45*np.sign(np.sin(2*np.pi*(1200-900*t/d)*t))*np.exp(-t*3)*(rng.random(len(t))>.35),at)
def hit(at,g=1): t=T(.45); put(sfx,g*(rng.standard_normal(len(t))*np.exp(-t*14)+1.2*np.sin(2*np.pi*60*t)*np.exp(-t*8)),at)
def boom(at): t=T(1.6); put(sfx,1.3*rng.standard_normal(len(t))*np.exp(-t*3.5)+1.4*np.sin(2*np.pi*45*t)*np.exp(-t*2.5),at)
def gong(at,f): t=T(1.8); put(sfx,.55*(np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*f*2.76*t)+.3*np.sin(2*np.pi*f*5.4*t))*np.exp(-t*2),at)
def whoosh(at,d=.45): t=T(d); x=np.convolve(rng.standard_normal(len(t)),np.ones(30)/30,'same'); put(sfx,.9*x*np.sin(np.pi*t/d),at)
def pdown(at): t=T(1.2); put(sfx,.5*np.sin(2*np.pi*(500*np.exp(-t*3))*t)*np.exp(-t*1.2),at)
def charge(at,d): t=T(d); put(sfx,.35*np.sin(2*np.pi*(150+900*(t/d)**2)*t)*np.minimum(1,t*4),at)
def thunder(at): t=T(2.0); x=np.convolve(rng.standard_normal(len(t)),np.ones(60)/60,'same'); put(sfx,1.5*x*np.exp(-t*1.5),at)
thunder(0.0); hit(0.05,1.2); gong(0.35,150); whoosh(1.5); gong(1.55,220)
zap(2.9,.6); hit(3.35,1.2); whoosh(6.5); pdown(6.7); thunder(7.2)
charge(11.6,2.6); whoosh(14.2); boom(14.4); hit(16.1,1.3); gong(16.1,110); whoosh(17.1); gong(17.4,330); whoosh(20.9); gong(21.0,260)
def wr(name,x):
    w=wave.open(name,'w');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(x,-1,1)*32767).astype(np.int16).tobytes());w.close()
wr('mus.wav',mus/np.max(np.abs(mus))*.8); wr('sfx.wav',sfx/np.max(np.abs(sfx))*.9)
