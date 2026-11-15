# MOVE Explica 3D premium — Subwoofer fechado dentro do móvel (grave embolado, móvel vibrando)
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib3d import *
OUT = os.path.dirname(os.path.abspath(__file__))
DUR = 21.5
sc = iniciar(DUR); materiais(); estudio(parede_y=1.0)

# ---------- painel + TV ----------
cube('painel', (0, 0.93, 1.3), (3.2, 0.03, 1.3), mat('painelm', (0.035, 0.02, 0.012), 0.55), 0.005)
cube('tv', (0, 0.86, 1.32), (0.78, 0.02, 0.45), mat('tela', (0.004, 0.004, 0.005), 0.12, emis=(0.06, 0.09, 0.1), es=0.6), 0.004)

# ---------- móvel (rack) com nicho de ripas ----------
RACK = bpy.data.objects.new('rack', None); bpy.context.collection.objects.link(RACK); RACK.location = (0, 0.55, 0)
M_lac = mat('laca', (0.03, 0.032, 0.03), 0.35, clearcoat=0.5)
pecas = [
    cube('tampo', (0, 0, 0.47), (1.05, 0.26, 0.02), M['madeira'], 0.006),
    cube('fundo', (0, 0.24, 0.27), (1.05, 0.02, 0.2), M_lac),
    cube('base', (0, 0, 0.07), (1.05, 0.26, 0.02), M_lac),
    cube('ladoE', (-1.04, 0, 0.27), (0.02, 0.26, 0.2), M_lac),
    cube('ladoD', (1.04, 0, 0.27), (0.02, 0.26, 0.2), M_lac),
    cube('div', (-0.2, 0, 0.27), (0.02, 0.26, 0.2), M_lac),
    cube('portaD', (0.42, -0.255, 0.27), (0.6, 0.012, 0.19), M['madeira'], 0.004),
]
for k in range(13):  # ripas na frente do nicho do sub
    pecas.append(cube(f'ripa{k}', (-1.0 + 0.0315 + k * 0.064, -0.255, 0.27), (0.02, 0.014, 0.19), M['madeira'], 0.003))
RIPAS = []
for p in pecas:
    p.parent = RACK
    if p.name.startswith('ripa'): RIPAS.append(p)
for k in range(2):  # pés
    cube(f'pe{k}', (-0.9 + k * 1.8, 0.55, 0.025), (0.03, 0.2, 0.025), M['alu'])

# ---------- subwoofer ----------
SUB = bpy.data.objects.new('sub', None); bpy.context.collection.objects.link(SUB)
sp = [cube('subcx', (0, 0, 0.19), (0.17, 0.17, 0.17), mat('subcx', (0.02, 0.02, 0.022), 0.4, clearcoat=0.3), 0.012)]
sp.append(cil('subaro', (0, -0.172, 0.19), 0.135, 0.012, M['aro']))
cone = cil('subcone', (0, -0.175, 0.19), 0.12, 0.012, M['cone'])
sp.append(cil('subcap', (0, -0.185, 0.19), 0.045, 0.012, M['aro']))
sp.append(cil('subduto', (0.12, -0.172, 0.06), 0.022, 0.02, mat('duto', (0.002, 0.002, 0.002), 0.9)))
for p in sp + [cone]: p.parent = SUB
cone['y0'] = cone.location.y
# dentro do nicho -> sai para o piso, ao lado do móvel
P_DENTRO = (-0.6, 0.6, 0.085); P_FORA1 = (-0.6, -0.15, 0.0); P_FORA = (-1.4, -0.3, 0.0)
T_SAI = 12.4
for t, p in ((0, P_DENTRO), (T_SAI, P_DENTRO), (T_SAI + 0.6, P_FORA1), (T_SAI + 1.3, P_FORA)):
    SUB.location = p; SUB.keyframe_insert('location', frame=T(t))
for r in RIPAS: visivel(r, [(0, True), (T_SAI - 0.1, False), (T_SAI + 1.5, True)])
EV += [(T_SAI, 'whoosh')]

# ---------- vibração do móvel enquanto o sub está preso ----------
for f in range(1, int(DUR * FPS) + 1):
    t = (f - 1) / FPS
    a = 0.0 if t < 1.0 or t > T_SAI else 0.0022 * min(1, (t - 1.0) / 1.5)
    RACK.location = (math.sin(t * 2 * math.pi * 11) * a, 0.55, abs(math.sin(t * 2 * math.pi * 7.3)) * a * 0.6)
    RACK.keyframe_insert('location', frame=f)
    RACK.rotation_euler = (0, math.sin(t * 2 * math.pi * 9) * a * 0.8, 0); RACK.keyframe_insert('rotation_euler', frame=f)

# ---------- cone e anéis ----------
cones([cone], DUR, lambda i, t: 0.01 * min(1, t / 0.4) if t < T_SAI else (0.004 if t < T_SAI + 1.3 else 0.014))
t = 0.6
while t < DUR - 1.2:
    if t < T_SAI - 0.3:
        anel((P_DENTRO[0], 0.41, 0.275), t, VERM, False, r=0.1, alcance=2.4)   # preso: aparece só entre as ripas
        t += 0.5
    elif t < T_SAI + 1.4:
        t += 0.45
    else:
        anel((P_FORA[0], P_FORA[1] - 0.2, 0.19), t, VERDE, True, r=0.12, alcance=4.2)
        t += 0.45
# linhas de vibração vermelhas saindo do tampo
for k, x in enumerate((-0.9, -0.55, -0.25)):
    o, m = texto(f'vib{k}', '~', (x, 0.42, 0.62), 0.12, VERM, es=10)
    visivel(o, [(0, False), (8.2, True), (T_SAI, False)])
EV += [(8.2, 'erro'), (T_SAI + 1.4, 'ding')]

luzes(chave=150, verde=160, quente=90)
kc = camera(lente=34)
kc(0.0, (-0.25, -0.55, 0.32), (-0.6, 0.3, 0.27))        # close nas ripas, sub lá dentro
kc(3.0, (-0.1, -0.9, 0.45), (-0.55, 0.3, 0.3))
kc(3.9, (0.35, -3.0, 1.15), (-0.1, 0.4, 0.55))           # geral: rack, TV, sub preso
kc(11.8, (0.1, -2.8, 1.05), (-0.15, 0.4, 0.5))
kc(12.6, (-0.4, -2.4, 0.7), (-0.9, 0.1, 0.25))           # acompanha o sub saindo
kc(14.2, (-0.8, -1.8, 0.5), (-1.3, -0.25, 0.2))
kc(16.0, (-0.55, -3.3, 1.1), (-0.85, 0.1, 0.45))           # geral com o grave livre
kc(DUR, (-0.7, -2.9, 1.0), (-0.95, 0.05, 0.42))
finalizar(OUT)
