# MOVE Explica 3D premium — Crossover em 80 Hz: caixas pequenas não devem tocar o grave profundo
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib3d import *
OUT = os.path.dirname(os.path.abspath(__file__))
DUR = 21.5
sc = iniciar(DUR); materiais(); estudio()
random.seed(3)

# ---------- receiver com display ----------
RZ = 0.09
rec = cube('receiver', (0, -0.75, RZ), (0.4, 0.3, 0.09), M['alu'], 0.01)
cube('display', (-0.05, -1.052, RZ + 0.02), (0.2, 0.002, 0.035), mat('disp', (0.002, 0.002, 0.002), 0.1), 0)
cil('volume', (0.27, -1.06, RZ), 0.05, 0.03, M['alu_claro'])
T_FIX = 12.4
d1, m1 = texto('disp1', 'CAIXAS: GRANDE', (-0.05, -1.056, RZ + 0.02), 0.026, VERM, es=10)
d2, m2 = texto('disp2', 'PEQUENA · 80 Hz', (-0.05, -1.056, RZ + 0.02), 0.026, VERDE, es=10)
visivel(d1, [(0, True), (T_FIX + 0.4, False)]); visivel(d2, [(0, False), (T_FIX + 0.4, True)])
EV += [(T_FIX + 0.3, 'clique'), (T_FIX + 0.45, 'clique')]

# ---------- 2 caixas pequenas + subwoofer ----------
CONES = []
for i, x in enumerate((-0.75, 0.75)):
    c, _ = caixa(f'cx{i}', x, 0.2, z=0.95, s=0.75, rotz=math.radians(8 if x < 0 else -8)); c['y0'] = c.location.y; CONES.append(c)
SUB = bpy.data.objects.new('sub', None); bpy.context.collection.objects.link(SUB); SUB.location = (1.12, 0.5, 0)
sp = [cube('subcx', (0, 0, 0.21), (0.2, 0.2, 0.2), mat('subcx', (0.02, 0.02, 0.022), 0.4, clearcoat=0.3), 0.012), cil('subaro', (0, -0.202, 0.21), 0.16, 0.012, M['aro'])]
scone = cil('subcone', (0, -0.205, 0.21), 0.145, 0.012, M['cone']); sp.append(cil('subcap', (0, -0.215, 0.21), 0.05, 0.012, M['aro']))
for p in sp + [scone]: p.parent = SUB
scone['y0'] = scone.location.y
SUB.rotation_euler = (0, 0, math.radians(-20))

# cones: pequenas "sofrendo" (curso exagerado + tremor) até a correção
def regra(i, t):
    if t < T_FIX: return 0.02 + random.uniform(-0.008, 0.008)
    return 0.006
cones(CONES, DUR, regra)
cones([scone], DUR, lambda i, t: 0.0 if t < T_FIX + 0.8 else 0.016)

# ---------- linhas de frequência (grave longo × médio/agudo curto) ----------
def linha(nome, ciclos, amp, cor, larg=0.9):
    N = 140
    vs = [(-larg / 2 + larg * i / (N - 1), 0, math.sin(i / (N - 1) * ciclos * 2 * math.pi) * amp) for i in range(N)]
    me = bpy.data.meshes.new(nome); me.from_pydata(vs, [(i, i + 1) for i in range(N - 1)], [])
    o = bpy.data.objects.new(nome, me); bpy.context.collection.objects.link(o)
    o.modifiers.new('sk', 'SKIN')
    for v in o.data.skin_vertices[0].data: v.radius = (0.006, 0.006)
    o.modifiers.new('ss', 'SUBSURF').levels = 1
    m = mat(nome + 'm', (0, 0, 0), emis=cor, es=10); o.data.materials.append(m)
    return o, m
grave, mg = linha('grave', 1.5, 0.11, VERM)
agudo, ma = linha('agudo', 12, 0.03, VERDE, larg=0.7)
def kl(o, t, loc, rz, s=1.0):
    o.location = loc; o.rotation_euler = (0, 0, rz); o.scale = (s, s, s)
    for p in ('location', 'rotation_euler', 'scale'): o.keyframe_insert(p, frame=T(t))
# grave indo para as caixas pequenas (errado)
kl(grave, 0, (-0.38, -0.25, 0.9), math.radians(-25), 0.01); kl(grave, 3.6, (-0.38, -0.25, 0.9), math.radians(-25), 0.01)
kl(grave, 4.3, (-0.38, -0.25, 0.9), math.radians(-25), 1.0); kl(grave, T_FIX, (-0.38, -0.25, 0.9), math.radians(-25), 1.0)
# correção: o grave vira para o subwoofer (no piso, à direita)
kl(grave, T_FIX + 1.0, (0.6, 0.0, 0.42), math.radians(20), 1.0); kl(grave, DUR, (0.6, 0.0, 0.42), math.radians(20), 1.0)
cor_k(mg, [(0, VERM), (T_FIX + 0.6, VERM), (T_FIX + 1.0, VERDE)])
kl(agudo, 0, (0.38, -0.25, 1.05), math.radians(25), 0.01); kl(agudo, 4.3, (0.38, -0.25, 1.05), math.radians(25), 0.01)
kl(agudo, 5.0, (0.38, -0.25, 1.05), math.radians(25), 1.0); kl(agudo, DUR, (0.38, -0.25, 1.05), math.radians(25), 1.0)
t80, _ = texto('t80', '80 Hz', (0.62, -0.1, 0.66), 0.14, VERDE, es=10)
visivel(t80, [(0, False), (T_FIX + 1.0, True)])
EV += [(0.3, 'batida'), (4.3, 'whoosh'), (8.2, 'erro'), (8.6, 'zumbido'), (T_FIX + 1.0, 'whoosh'), (T_FIX + 1.4, 'ding')]

# anéis
t = 0.5
while t < DUR - 1.2:
    if t < T_FIX:
        for c, x in zip(CONES, (-0.75, 0.75)):
            anel((x, 0.03, 0.86), t, VERM, False, r=0.1, alcance=1.8)
        t += 0.4
    elif t < T_FIX + 1.4: t += 0.45
    else:
        for x in (-0.75, 0.75): anel((x, 0.03, 0.86), t, VERDE, False, r=0.1, alcance=2.6)
        anel((1.05, 0.3, 0.21), t, VERDE, True, r=0.15, rot=(math.pi / 2, 0, math.radians(-20)), alcance=3.4)
        t += 0.45

luzes()
kc = camera(lente=34)
kc(0.0, (-0.55, -0.55, 1.05), (-0.75, 0.05, 0.86))         # close na caixa pequena sofrendo
kc(3.0, (-0.45, -0.85, 1.05), (-0.7, 0.05, 0.86))
kc(3.9, (0.15, -4.0, 1.5), (0.2, 0.0, 0.62))              # geral: receiver, caixas, sub
kc(8.0, (0.3, -3.8, 1.45), (0.2, 0.0, 0.62))
kc(8.4, (-0.05, -1.55, 0.25), (-0.05, -1.05, RZ + 0.02))   # display do receiver
kc(11.9, (0.0, -1.5, 0.27), (-0.05, -1.05, RZ + 0.02))
kc(12.9, (0.05, -1.5, 0.27), (-0.05, -1.05, RZ + 0.02))
kc(14.2, (0.5, -3.9, 1.4), (0.25, 0.05, 0.55))            # grave indo para o sub
kc(DUR, (0.3, -4.1, 1.45), (0.22, 0.0, 0.6))
finalizar(OUT)
