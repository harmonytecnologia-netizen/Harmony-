# MOVE Explica 3D premium — Módulo de automação sem fio neutro: luz piscando / módulo reiniciando
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib3d import *
OUT = os.path.dirname(os.path.abspath(__file__))
DUR = 21.5
sc = iniciar(DUR); materiais(); estudio(sanca=False, parede_y=3.0)

# parede de gesso com a caixinha 4x2 aberta
WY = 0.0
M_parede = mat('parede_gesso', (0.11, 0.1, 0.095), 0.8)
cube('parede_obra', (0, WY + 0.05, 1.0), (1.4, 0.05, 1.0), M_parede, 0.004)
BX, BZ = (0.0, 0.95)
cube('caixinha', (BX, WY - 0.004, BZ), (0.055, 0.008, 0.1), mat('caixinha', (0.75, 0.42, 0.06), 0.45), 0.003)
# módulo de automação dentro da caixinha
mod = cube('modulo', (BX, WY - 0.03, BZ), (0.04, 0.02, 0.04), mat('modm', (0.04, 0.04, 0.045), 0.35, clearcoat=0.4), 0.004)
led_m = mat('modled', (0, 0, 0), emis=VERM, es=12)
cil('modled', (BX + 0.022, WY - 0.052, BZ + 0.022), 0.0045, 0.004, led_m)
for k in range(4):
    cube(f'bornemod{k}', (BX - 0.024 + k * 0.016, WY - 0.051, BZ - 0.026), (0.005, 0.002, 0.006), M['ouro'])
T_FIX = 12.6
# fios chegando por cima (eletroduto no gesso) até o módulo
def fio(nome, dx, m, t_in=None):
    pts = [(BX + dx, WY - 0.012, BZ + 0.95), (BX + dx, WY - 0.012, BZ + 0.2), (BX + dx * 0.6, WY - 0.03, BZ + 0.06), (BX + dx * 0.3, WY - 0.035, BZ + 0.035)]
    o, _ = cabo(nome, pts, m, esp=0.0035)
    if t_in is not None:
        o.data.bevel_factor_mapping_end = 'SPLINE'
        o.data.bevel_factor_end = 0.0; o.data.keyframe_insert('bevel_factor_end', frame=T(t_in))
        o.data.bevel_factor_end = 1.0; o.data.keyframe_insert('bevel_factor_end', frame=T(t_in + 1.1))
    return o
fio('fase', -0.03, mat('fase_m', (0.6, 0.03, 0.03), 0.35, clearcoat=0.3))
fio('retorno', -0.012, mat('ret_m', (0.02, 0.02, 0.02), 0.35, clearcoat=0.3))
# neutro: fantasma (onde deveria estar) e depois real
gh_m = mat('neutro_fant', (0, 0, 0), emis=VERM, es=0)
gh = fio('neutro_fantasma', 0.03, gh_m)
emis_k(gh_m, [(0, 0), (4.6, 0), (5.0, 5), (5.6, 1.5), (6.2, 5), (6.8, 1.5), (7.4, 5), (8.0, 1.5), (T_FIX - 0.2, 1.5), (T_FIX, 0)])
visivel(gh, [(0, True), (T_FIX, False)])
neu_m = mat('neutro_m', (0.15, 0.4, 0.85), 0.3, clearcoat=0.3, emis=(0.25, 0.55, 1.0), es=0)
fio('neutro', 0.03, neu_m, t_in=T_FIX)
emis_k(neu_m, [(T_FIX, 0), (T_FIX + 0.5, 6), (T_FIX + 2.2, 0.6)])
cor_k(led_m, [(0, VERM), (T_FIX + 1.1, VERM), (T_FIX + 1.15, VERDE)])
# LED do módulo piscando (reinicia) até a correção
pisca = []
t = 0.2
while t < T_FIX + 1.0:
    pisca += [(t, 14), (t + 0.18, 0)]; t += 0.7
emis_k(led_m, pisca + [(T_FIX + 1.15, 14)])

# luminária pendente no alto, piscando até a correção
LZ = 1.42; LX = -0.2
cil('haste', (LX, -0.25, LZ + 0.2), 0.004, 0.4, M['alu_claro'], rot=(0, 0, 0))
cup = cil('cupula', (LX, -0.25, LZ), 0.09, 0.08, mat('cupm', (0.02, 0.02, 0.02), 0.3, metal=0.8), rot=(0, 0, 0))
lamp_m = mat('lampm', (0, 0, 0), emis=QUENTE, es=0)
cil('difusor', (LX, -0.25, LZ - 0.042), 0.075, 0.004, lamp_m, rot=(0, 0, 0))
ld = bpy.data.lights.new('lamp', 'SPOT'); ld.spot_size = math.radians(80); ld.color = QUENTE
lo = bpy.data.objects.new('lamp', ld); lo.location = (LX, -0.25, LZ - 0.05); bpy.context.collection.objects.link(lo)
seq = []
t = 0.0
import random; random.seed(7)
while t < T_FIX + 1.0:
    on = random.random() > 0.45
    seq.append((t, on)); t += random.choice((0.08, 0.12, 0.2, 0.35))
for tt, on in seq:
    ld.energy = 30 if on else 1.5; ld.keyframe_insert('energy', frame=T(tt))
    emis_k(lamp_m, [(tt, 9 if on else 0.3)])
ld.energy = 40; ld.keyframe_insert('energy', frame=T(T_FIX + 1.15)); emis_k(lamp_m, [(T_FIX + 1.15, 12)])
EV += [(0.2, 'erro'), (3.3, 'whoosh'), (5.0, 'clique'), (8.4, 'erro'), (T_FIX, 'whoosh'), (T_FIX + 1.15, 'ding')]
def anel(loc, t0, cor, forte, r=0.08, alcance=2.6):
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=0.003, location=loc, rotation=(math.pi / 2, 0, 0)); o = bpy.context.object
    m = mat('anel', (0, 0, 0), emis=cor, es=0); o.data.materials.append(m)
    b = m.node_tree.nodes['Principled BSDF']; em = b.inputs['Emission Strength']; al = b.inputs['Alpha']
    f0 = T(t0); f1 = T(t0 + 1.2)
    for f, s_, e, a in ((max(1, f0 - 1), 0.01, 0, 0), (f0, 1.0, 14 if forte else 10, 1), (f1, alcance, 0, 0), (f1 + 1, 0.0, 0, 0)):
        o.scale = (s_, s_, s_); o.keyframe_insert('scale', frame=f); em.default_value = e; em.keyframe_insert('default_value', frame=f); al.default_value = a; al.keyframe_insert('default_value', frame=f)
# anéis: vermelhos no módulo antes, verdes depois
t = 1.0
while t < DUR - 1.0:
    if t < 3.0 or (8.2 < t < T_FIX - 0.3):
        anel((BX, WY - 0.06, BZ), t, VERM, False, r=0.08, alcance=2.6)
    elif t > T_FIX + 1.2:
        anel((BX, WY - 0.06, BZ), t, VERDE, True, r=0.08, alcance=3.2)
    t += 0.55

luzes(chave=240, verde=110, quente=100)
kc = camera(lente=35, fstop=3.5)
kc(0.0, (-0.3, -1.0, 1.2), (-0.1, -0.1, 1.15))       # interruptor + luminária piscando
kc(3.1, (-0.25, -0.95, 1.18), (-0.08, -0.08, 1.15))
kc(4.1, (0.05, -0.42, 1.02), (BX, WY - 0.03, BZ + 0.02))  # dentro da caixinha: falta o neutro
kc(8.2, (0.1, -0.38, 1.0), (BX, WY - 0.03, BZ + 0.03))
kc(9.2, (-0.35, -1.0, 1.2), (-0.1, -0.1, 1.15))        # módulo + luz piscando
kc(12.2, (-0.28, -0.92, 1.18), (-0.08, -0.1, 1.15))
kc(13.0, (0.08, -0.45, 1.15), (BX, WY - 0.03, BZ + 0.15))  # neutro entrando
kc(16.0, (0.02, -0.5, 1.05), (BX, WY - 0.03, BZ + 0.03))
kc(17.0, (-0.38, -1.05, 1.22), (-0.1, -0.1, 1.15))
kc(DUR, (-0.2, -1.2, 1.25), (-0.08, -0.1, 1.15))
finalizar(OUT)
