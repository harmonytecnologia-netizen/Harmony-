import numpy as np, wave
SR=44100; D=26; n=int(SR*D); out=np.zeros(n); rng=np.random.default_rng(3)
def put(s,at,g=1):
    i=int(at*SR); j=min(n,i+len(s)); out[i:j]+=g*s[:j-i]
T=lambda d:np.arange(int(SR*d))/SR
N=lambda m:440*2**((m-69)/12)
def saw(f,d,v): t=T(d); return v*(2*((t*f)%1)-1)*np.minimum(1,t*80)*np.exp(-t*3)
def kick(at): t=T(.3); put(.9*np.sin(2*np.pi*(45+120*np.exp(-t*30))*t)*np.exp(-t*10),at)
def snare(at): t=T(.2); put(.35*rng.standard_normal(len(t))*np.exp(-t*20)+.2*np.sin(2*np.pi*190*t)*np.exp(-t*25),at)
def hat(at): t=T(.05); put(.08*rng.standard_normal(len(t))*np.exp(-t*90),at)
bpm=150; b=60/bpm; bass=[40,40,43,38]
t0=0;k=0
while t0<D:
    for s in range(8):
        tt=t0+s*b/2
        if tt>=D: break
        if s in(0,3,4): kick(tt)
        if s in(2,6): snare(tt)
        hat(tt)
        put(saw(N(bass[k%4]),b/2*.9,.18),tt)
        if s%2==0: put(saw(N(bass[k%4]+24+[0,3,7,10][s//2]),b/2*.6,.06),tt)
    k+=1; t0+=b*4
out*=.55
def zap(at,d=.5):  # raio
    t=T(d); put(.4*np.sign(np.sin(2*np.pi*(900-700*t/d)*t))*np.exp(-t*4)*(rng.random(len(t))>.3),at)
def hit(at): t=T(.35); put(.9*rng.standard_normal(len(t))*np.exp(-t*18)+.8*np.sin(2*np.pi*70*t)*np.exp(-t*12),at)
def charge(at,d): t=T(d); put(.25*np.sin(2*np.pi*(200+800*(t/d)**2)*t)*np.minimum(1,t*3),at)
def boom(at): t=T(1.2); put(1.2*rng.standard_normal(len(t))*np.exp(-t*4)+np.sin(2*np.pi*50*t)*np.exp(-t*3),at)
def gong(at,f=220): t=T(1.5); put(.5*(np.sin(2*np.pi*f*t)+.6*np.sin(2*np.pi*f*2.76*t)+.3*np.sin(2*np.pi*f*5.4*t))*np.exp(-t*2.5),at)
def whoosh(at): t=T(.4); x=np.convolve(rng.standard_normal(len(t)),np.ones(25)/25,'same'); put(.7*x*np.sin(np.pi*t/.4),at)
def power_down(at): t=T(1.0); put(.4*np.sin(2*np.pi*(400*np.exp(-t*3))*t)*np.exp(-t*1.5),at)
gong(0.1,180); whoosh(1.2); gong(1.25,240)
zap(2.6,.6); hit(3.2)
for a in(4.9,5.3,5.7): zap(a,.3)
for h in(5.2,5.6,6.0): hit(h)
power_down(6.2); charge(10.4,1.8); whoosh(12.0); zap(12.2,1.0); boom(13.3); gong(14.1,140); gong(16.4,300); whoosh(21.2); gong(21.4,260)
# silencia música na tela preta
i0,i1=int(6.25*SR),int(7.5*SR); out[i0:i1]*=0.25
out=out/np.max(np.abs(out))*.9; f=int(SR*.8); out[-f:]*=np.linspace(1,0,f)
w=wave.open('trilha.wav','w');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype(np.int16).tobytes());w.close()
