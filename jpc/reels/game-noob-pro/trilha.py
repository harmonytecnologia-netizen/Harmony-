import numpy as np, wave
SR=44100; D=31.5; n=int(SR*D); out=np.zeros(n)
def sq(f,dur,vol=.12,duty=.5):
    t=np.arange(int(SR*dur))/SR; w=np.where((t*f)%1<duty,1.0,-1.0); e=np.minimum(1,t*200)*np.exp(-t*2.5); return vol*w*e
def tri(f,dur,vol=.18):
    t=np.arange(int(SR*dur))/SR; w=2*np.abs(2*((t*f)%1)-1)-1; return vol*w*np.minimum(1,t*300)
def put(sig,at):
    i=int(at*SR); j=min(n,i+len(sig)); out[i:j]+=sig[:j-i]
def noise(dur,vol=.08,dec=40):
    t=np.arange(int(SR*dur))/SR; return vol*np.random.default_rng(int(dur*1e4)).choice([-1,1],len(t))*np.exp(-t*dec)
N=lambda m:440*2**((m-69)/12)
bpm=140; b=60/bpm
# progressão Am F C G (melodia chiptune original)
bass=[45,41,48,43]; mel=[[69,72,76,72],[65,69,72,69],[72,76,79,76],[67,71,74,71]]
music_end=31.5
k=0; t0=0
while t0<music_end:
    bar=(k//1)%4
    for s in range(8):
        tt=t0+s*b/2
        if tt>=music_end: break
        put(tri(N(bass[bar]) if s%2==0 else N(bass[bar]+12),b/2*.9),tt)
        put(sq(N(mel[bar][s%4]+12),b/2*.8,.06,.25),tt)
        if s%2==0: put(noise(.12,.10,30),tt)  # kick-ish
        else: put(noise(.04,.05,120),tt)       # hat
    k+=1; t0+=b*4
out*=0.8
def coin(at): put(sq(988,.08,.18),at); put(sq(1319,.25,.18),at+.08)
def gameover(at):
    for i,m in enumerate([72,67,64,60,59,55]): put(sq(N(m),.22,.2,.5),at+i*.2)
def levelup(at):
    for i,m in enumerate([60,64,67,72,76,79,84]): put(sq(N(m),.12,.2,.25),at+i*.08)
def blip(at,f=660): put(sq(f,.06,.15),at)
def crash(at): put(noise(.5,.35,6),at)
coin(0.3); blip(3.6,880); gameover(6.7); blip(10.2,220); crash(10.2); coin(13.9); blip(16.6,880)
for i in range(6): blip(17+i*.5,330)
coin(20.3); levelup(22.4); coin(27.2); coin(29.5)
out=out/np.max(np.abs(out))*.85
# fade final
f=int(1.0*SR); out[-f:]*=np.linspace(1,0,f)
w=wave.open('trilha.wav','w');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype(np.int16).tobytes());w.close()
