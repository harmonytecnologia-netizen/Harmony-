# MOVE Explica 3D premium — SOM: ganho do amplificador no máximo = som distorcendo com volume no meio
# Técnica: o GANHO ajusta a sensibilidade de entrada, não a potência. No máximo, o amplificador chega ao
# limite (clipa) com pouco volume: a onda é cortada (vira quase quadrada), distorce e esquenta o tweeter.
# Certo: fonte (celular/streamer) em ~80%, subir o ganho só até antes de distorcer no volume mais alto que se usa.
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib3d import *
OUT = os.path.dirname(os.path.abspath(__file__))
DUR = 21.0
T_FIX0, T_FIX1 = 6.4, 7.6
sc = iniciar(DUR); materiais(); estudio(sanca=True, parede_y=3.2)

# ---------- amplificador grande ----------
AZ = 0.1
amp = cube('amp', (0, -0.35, AZ), (0.46, 0.32, 0.1), M['alu'], 0.012)
FY = -0.35 - 0.32  # face frontal
cube('painel', (0, FY - 0.003, AZ), (0.44, 0.003, 0.085), mat('painel', (0.01, 0.01, 0.011), 0.25, metal=0.6), 0.004)
# botão de GANHO grande (gira de MAX para ~60%)
KX = -0.2
knob = cil('ganho', (KX, FY - 0.03, AZ), 0.062, 0.05, M['alu_claro'])
saia = cil('saia', (KX, FY - 0.008, AZ), 0.075, 0.012, M['preto'])
ind = cube('ind', (KX, FY - 0.058, AZ + 0.04), (0.006, 0.004, 0.02), mat('indm', (0, 0, 0), emis=(1, 1, 1), es=6))
ind.parent = knob; ind.matrix_parent_inverse = knob.matrix_world.inverted()
# rotação: ângulo em torno do eixo Y (face frontal). 0 = 12h; +135° = máximo (sentido horário visto de frente)
def gira(tt, graus):
    knob.rotation_euler = (math.pi / 2, math.radians(-graus), 0); knob.keyframe_insert('rotation_euler', frame=T(tt))
gira(0, 135); gira(T_FIX0, 135); gira(T_FIX1, 25); gira(DUR, 25)
# marcações MIN / MAX e rótulo GANHO
for s, dx, dz, cor in (('GANHO', 0, 0.075, (0.9, 0.9, 0.9)), ('MAX', 0.105, -0.06, VERM), ('MIN', -0.105, -0.06, (0.6, 0.6, 0.6))):
    texto('l' + s, s, (KX + dx, FY - 0.006, AZ + dz), 0.022, cor, es=6)
# LED CLIP
clipm = mat('clip', (0, 0, 0), emis=VERM, es=0)
cube('clipled', (0.12, FY - 0.005, AZ + 0.03), (0.018, 0.004, 0.012), clipm, 0.003)
texto('lclip', 'CLIP', (0.12, FY - 0.006, AZ - 0.01), 0.02, (0.8, 0.8, 0.8), es=5)
pisca = [(0, 0)]
t = 0.2
while t < T_FIX1:
    pisca += [(t, 9), (t + 0.18, 0)]; t += 0.42
emis_k(clipm, pisca + [(DUR, 0)])
pm = mat('pwr', (0, 0, 0), emis=VERDE, es=6)
cube('pwr', (0.34, FY - 0.005, AZ + 0.03), (0.02, 0.004, 0.006), pm, 0.002)

# ---------- caixa ----------
c, vz = caixa('cx', 0.95, 0.35, z=0.95, s=0.85, rotz=math.radians(-14))
c['y0'] = c.location.y
cones([c], DUR, lambda i, tt: 0.022 if tt < T_FIX1 else 0.012)
tw = [o for o in bpy.data.objects if o.name.startswith('Sphere')]

# ---------- ondas: cortada (vermelha) × limpa (verde) ----------
def onda(nome, cor, clip):
    N = 220; larg = 1.1; amp_ = 0.16
    vs = []
    for i in range(N):
        s = math.sin(i / (N - 1) * 3 * 2 * math.pi) * 1.6 if clip else math.sin(i / (N - 1) * 3 * 2 * math.pi)
        s = max(-1, min(1, s)) * amp_ * (0.62 if clip else 1)
        vs.append((-larg / 2 + larg * i / (N - 1), 0, s))
    me = bpy.data.meshes.new(nome); me.from_pydata(vs, [(i, i + 1) for i in range(N - 1)], [])
    o = bpy.data.objects.new(nome, me); bpy.context.collection.objects.link(o)
    o.modifiers.new('sk', 'SKIN')
    for v in o.data.skin_vertices[0].data: v.radius = (0.007, 0.007)
    m = mat(nome + 'm', (0, 0, 0), emis=cor, es=3.2); o.data.materials.append(m)
    o.location = (-0.05, -0.2, 0.62)
    return o, m
ocut, mcut = onda('cortada', (1.0, 0.02, 0.01), True)
olimp, mlimp = onda('limpa', VERDE, False)
visivel(ocut, [(0, True), (T_FIX1 - 0.3, False)])
visivel(olimp, [(0, False), (T_FIX1 - 0.3, True)])
# "teto" do amplificador (linhas tracejadas) onde a onda bate
for z in (0.62 + 0.099, 0.62 - 0.099):
    for k in range(11):
        o = cube(f'teto{z}{k}', (-0.58 + k * 0.106, -0.2, z), (0.03, 0.002, 0.002), mat(f'tetom{z}{k}', (0, 0, 0), emis=(0.8, 0.8, 0.8), es=2))
        visivel(o, [(0, True), (T_FIX1 - 0.3, False)])
def anel2(loc, t0, cor, forte, rot, r, alcance):
    o = anel(loc, t0, cor, forte, rot=rot, r=r, alcance=alcance)
    m = o.data.materials[0]; em = m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
    fc = [f for f in m.node_tree.animation_data.action.fcurves] if hasattr(m.node_tree.animation_data.action,'fcurves') else []
    for f in fc:
        for k in f.keyframe_points: k.co[1] *= 0.3
    return o
# anéis da caixa: vermelhos curtos (distorção) → verdes amplos
t = 0.6
while t < DUR - 1.2:
    if t < T_FIX1:
        anel2((0.95 + 0.05, 0.12, 0.84), t, VERM, False, r=0.1, alcance=1.6, rot=(math.pi / 2, 0, math.radians(-14))); t += 0.38
    else:
        anel2((0.95 + 0.05, 0.12, 0.84), t, VERDE, True, r=0.11, alcance=3.2, rot=(math.pi / 2, 0, math.radians(-14))); t += 0.5

# número 3D
t60, _ = texto('t60', 'SOM LIMPO', (0.0, -0.2, 0.92), 0.1, VERDE, es=5)
visivel(t60, [(0, False), (13.0, True), (DUR, True)])
EV += [(0.0, 'impacto'), (T_FIX0 - 1.2, 'riser'), (T_FIX1, 'impacto')]

luzes(chave=150, verde=140, quente=90)
kc = camera(lente=38, fstop=3.2)
CD = bpy.context.scene.camera.data
def lente(tt, l): CD.lens = l; CD.keyframe_insert('lens', frame=T(tt))
kc(0.0, (-0.42, -1.25, 0.3), (KX, FY, AZ + 0.01)); lente(0.0, 45)              # close no botão em MAX + CLIP piscando
kc(2.6, (-0.3, -1.35, 0.34), (KX + 0.05, FY, AZ + 0.02)); lente(2.6, 45)
kc(3.4, (0.15, -2.1, 0.75), (0.15, -0.2, 0.6)); lente(3.4, 34)                # onda cortada + caixa
kc(6.0, (0.25, -2.0, 0.78), (0.15, -0.2, 0.6)); lente(6.0, 34)
kc(6.4, (-0.3, -1.3, 0.32), (KX, FY, AZ + 0.01)); lente(6.4, 44)               # correção: botão desce
kc(8.6, (-0.12, -1.35, 0.36), (KX, FY, AZ + 0.01)); lente(8.6, 44)
kc(9.2, (-0.1, -2.05, 0.8), (0.1, -0.2, 0.62)); lente(9.2, 34)                 # onda limpa verde
kc(12.6, (0.1, -2.1, 0.82), (0.1, -0.2, 0.62)); lente(12.6, 34)
kc(13.2, (0.1, -1.2, 1.05), (0.85, 0.25, 0.8)); lente(13.2, 36)               # caixa com anéis verdes
kc(16.4, (0.3, -1.1, 1.0), (0.85, 0.25, 0.8)); lente(16.4, 36)
kc(16.8, (0.3, -2.6, 1.15), (0.35, 0.0, 0.55)); lente(16.8, 32)                # geral
kc(DUR, (0.15, -2.45, 1.1), (0.35, 0.0, 0.57)); lente(DUR, 32)
finalizar(OUT)
