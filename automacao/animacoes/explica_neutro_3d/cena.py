# MOVE Explica 3D premium — AUTOMAÇÃO: módulo sem neutro = LED piscando
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib3d import *
OUT = os.path.dirname(os.path.abspath(__file__))
DUR = 21.5
sc = iniciar(DUR); materiais(); estudio(sanca=True, parede_y=3)
T_POR = 3.6; T_FIX = 7.8; T_OK = 9.6

# ---------- painel de parede (gesso) com caixa 4x2 aberta ----------
M_branco = mat('placa', (0.82, 0.8, 0.76), 0.35, clearcoat=0.3)
M_pg = mat('parede_escura', (0.07, 0.068, 0.064), 0.55)
cube('parede_gesso', (0, 0.12, 1.25), (1.4, 0.06, 1.25), M_pg, 0.004)
cube('caixa4x2', (0, 0.055, 1.12), (0.06, 0.02, 0.1), mat('caixa', (0.85, 0.55, 0.12), 0.5), 0.004)   # caixa amarela de PVC
cube('fundo_caixa', (0, 0.07, 1.12), (0.052, 0.002, 0.092), mat('fundoc', (0.05, 0.04, 0.03), 0.6))
# módulo inteligente dentro da caixa
mod = cube('modulo', (0, 0.03, 1.12), (0.04, 0.012, 0.055), mat('mod', (0.03, 0.03, 0.035), 0.3, clearcoat=0.5), 0.004)
M_ml = mat('modled', (0, 0, 0), emis=VERM, es=10)
cil('modled', (0.022, 0.017, 1.16), 0.005, 0.004, M_ml)
# bornes do módulo (3 parafusos dourados no topo)
for k, dx in enumerate((-0.022, 0, 0.022)):
    cil(f'bm{k}', (dx, 0.03, 1.177), 0.006, 0.01, M['ouro'], rot=(0, 0, 0))
# placa do interruptor encostada ao lado (acabamento retirado)
cube('placa_int', (0.26, 0.04, 1.12), (0.06, 0.006, 0.1), M_branco, 0.006)
cube('tecla', (0.26, 0.032, 1.12), (0.045, 0.004, 0.08), M_branco, 0.006)
# eletroduto saindo do forro até a caixa
cil('eletroduto', (0, 0.055, 1.72), 0.016, 1.0, mat('corrug', (0.85, 0.6, 0.1), 0.6), rot=(0, 0, 0))

# fios: fase (vermelho) e retorno (preto) já ligados
M_fase = mat('fase', (0.6, 0.03, 0.03), 0.35, clearcoat=0.4)
M_ret = mat('retorno', (0.02, 0.02, 0.02), 0.35, clearcoat=0.4)
M_neu = mat('neutro', (0.15, 0.45, 0.85), 0.3, clearcoat=0.4, emis=(0.2, 0.55, 1.0), es=0)
cabo('fio_fase', [(-0.006, 0.055, 1.25), (-0.03, 0.03, 1.22), (-0.022, 0.03, 1.185)], M_fase, esp=0.0035)
cabo('fio_ret', [(0.006, 0.055, 1.25), (0.0, 0.025, 1.215), (0.0, 0.03, 1.185)], M_ret, esp=0.0035)
# neutro (azul) cresce na correção
cb, _ = cabo('fio_neutro', [(0.0, 0.055, 1.6), (0.003, 0.055, 1.3), (0.035, 0.02, 1.215), (0.022, 0.03, 1.185)], M_neu, esp=0.0038)
cb.data.bevel_factor_mapping_end = 'SPLINE'
cb.data.bevel_factor_end = 0.0; cb.data.keyframe_insert('bevel_factor_end', frame=T(T_FIX))
cb.data.bevel_factor_end = 1.0; cb.data.keyframe_insert('bevel_factor_end', frame=T(T_FIX + 1.4))
emis_k(M_neu, [(0, 0), (T_FIX, 0), (T_FIX + 0.3, 3), (T_FIX + 1.6, 3), (T_FIX + 2.4, 0)])

# ---------- luminária: plafon/spot no forro + pendente ----------
cube('forro', (0, -0.5, 2.5), (1.5, 0.75, 0.02), mat('forro_esc', (0.05, 0.05, 0.05), 0.6), 0.004)
M_lamp = mat('led', (0.9, 0.85, 0.75), 0.3, emis=QUENTE, es=0)
spots = []
for i, x in enumerate((-0.55, 0.0, 0.55)):
    cil(f'aro_spot{i}', (x, -0.55, 2.478), 0.07, 0.008, M['alu_claro'], rot=(0, 0, 0))
    cil(f'spot{i}', (x, -0.55, 2.474), 0.055, 0.006, M_lamp, rot=(0, 0, 0))
    l = bpy.data.lights.new(f'spot{i}', 'SPOT'); l.energy = 0; l.color = QUENTE; l.spot_size = math.radians(70); l.spot_blend = 0.6
    o = bpy.data.objects.new(f'spot{i}', l); o.location = (x, -0.55, 2.45); bpy.context.collection.objects.link(o); spots.append(l)
# brilho: 0-3.6 pisca irregular (erro), depois firme
random.seed(4)
kk = []
t = 0.0
while t < T_OK:
    on = random.random() > 0.45
    kk.append((t, 1.0 if on else 0.15)); t += random.choice((0.08, 0.12, 0.17, 0.25))
kk.append((T_OK, 1.0)); kk.append((DUR, 1.0))
for t, v in kk:
    M_lamp.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 12 * v
    M_lamp.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].keyframe_insert('default_value', frame=T(t))
    for l in spots:
        l.energy = 220 * v; l.keyframe_insert('energy', frame=T(t))
for fc in ([M_lamp.node_tree.animation_data.action] if M_lamp.node_tree.animation_data else []):
    pass
# LED do módulo: vermelho piscando -> verde fixo
cor_k(M_ml, [(0, VERM), (T_OK - 0.05, VERM), (T_OK, VERDE)])
k = []
t = 0.0
while t < T_OK:
    k.append((t, 12)); k.append((t + 0.15, 0)); t += 0.5
k.append((T_OK, 14)); k.append((DUR, 14))
emis_k(M_ml, k)
def anel(loc, t0, cor, forte, r=0.08, alcance=3.0):
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=0.003, location=loc, rotation=(math.pi / 2, 0, 0))
    o = bpy.context.object
    m = bpy.data.materials.new('anelA'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (*cor, 1)
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader'); out = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(e.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
    o.data.materials.append(m)
    f0 = T(t0); f1 = T(t0 + 1.3)
    for f, s_, fa, es in ((max(1, f0 - 1), 0.01, 0, 0), (f0, 1.0, 1, 12 if forte else 8), (f1, alcance, 0, 0), (f1 + 1, 0.0, 0, 0)):
        o.scale = (s_, s_, s_); o.keyframe_insert('scale', frame=f)
        mx.inputs[0].default_value = fa; mx.inputs[0].keyframe_insert('default_value', frame=f)
        e.inputs['Strength'].default_value = es; e.inputs['Strength'].keyframe_insert('default_value', frame=f)
    return o
# anéis: vermelho (erro) no módulo, verde no resultado
for t0 in (0.4, 1.6, 2.8, 4.2, 5.4, 6.6):
    anel((0, 0.0, 1.12), t0, VERM, False, r=0.08, alcance=2.6)
for t0 in (T_OK + 0.2, T_OK + 1.4, 12.6, 14.0, 15.4, 17.0, 18.6):
    anel((0, 0.0, 1.12), t0, VERDE, True, r=0.08, alcance=3.2)
EV += [(0.3, 'batida'), (1.2, 'erro'), (T_POR, 'whoosh'), (T_FIX, 'whoosh'), (T_OK, 'ding'), (16.8, 'plim')]

luzes(chave=200, verde=150, quente=80)
kc = camera(lente=34, fstop=2.8)
kc(0.0, (0.18, -0.55, 1.2), (0.0, 0.03, 1.13))        # close no módulo com LED vermelho
kc(3.4, (0.12, -0.75, 1.25), (0.0, 0.03, 1.15))
kc(4.4, (0.55, -1.75, 1.35), (0.0, -0.15, 1.78))          # abre: luz do forro piscando
kc(7.4, (0.4, -1.6, 1.35), (0.0, -0.15, 1.75))
kc(8.2, (-0.15, -0.5, 1.3), (0.0, 0.03, 1.2))         # neutro azul entrando na caixa
kc(11.6, (-0.1, -0.6, 1.25), (0.0, 0.03, 1.15))
kc(12.6, (-0.55, -1.75, 1.35), (0.0, -0.15, 1.78))        # resultado: luz firme
kc(DUR, (-0.3, -2.0, 1.4), (0.0, -0.1, 1.72))
finalizar(OUT)
