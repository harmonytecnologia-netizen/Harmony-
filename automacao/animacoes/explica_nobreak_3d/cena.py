# MOVE Explica 3D premium — SEGURANÇA: faltou luz, a câmera apagou (nobreak no rack)
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib3d import *
OUT = os.path.dirname(os.path.abspath(__file__))
DUR = 21.5
sc = iniciar(DUR); materiais(); estudio(sanca=False, parede_y=3)
T_QUEDA = 2.2; T_FIX = 7.8; T_OK = 9.4

M_pe = mat('parede_escura', (0.07, 0.068, 0.064), 0.55)
cube('parede', (0, 0.45, 1.3), (1.6, 0.05, 1.3), M_pe, 0.004)
# sanca quente na parede (apaga na queda e volta como "energia da rua" só no fim? não: fica apagada; casa no escuro)
M_sanca = mat('sanca2', (0, 0, 0), emis=QUENTE, es=7)
cube('sanca', (0, 0.39, 2.45), (1.5, 0.01, 0.012), M_sanca)
emis_k(M_sanca, [(0, 7), (T_QUEDA, 7), (T_QUEDA + 0.08, 0), (DUR, 0)])

# ---------- rack aberto ----------
RX = -0.45
M_rk = mat('rack', (0.03, 0.03, 0.032), 0.3, metal=0.9)
for dx in (-0.24, 0.24):
    for dy in (0.06, 0.34):
        cube(f'col{dx}{dy}', (RX + dx, dy, 0.55), (0.012, 0.012, 0.55), M_rk)
cube('topo', (RX, 0.2, 1.1), (0.25, 0.16, 0.01), M_rk); cube('base', (RX, 0.2, 0.02), (0.25, 0.16, 0.02), M_rk)
leds = []
def aparelho(nome, z, n_leds, h=0.035):
    a = cube(nome, (RX, 0.2, z), (0.225, 0.14, h), M['alu'], 0.006)
    ms = []
    for k in range(n_leds):
        m = mat(f'{nome}led{k}', (0, 0, 0), emis=VERDE, es=10)
        cube(f'{nome}l{k}', (RX - 0.18 + k * (0.3 / max(1, n_leds - 1)) if n_leds > 1 else RX + 0.15, 0.058, z + h * 0.35), (0.008, 0.002, 0.004), m)
        ms.append(m)
    leds.extend(ms); return a
aparelho('gravador', 0.92, 3, 0.045)
aparelho('switch_poe', 0.78, 12, 0.025)
aparelho('roteador', 0.66, 4, 0.025)
# portas RJ45 do switch
for k in range(12):
    cube(f'porta{k}', (RX - 0.18 + k * 0.0327, 0.057, 0.772), (0.011, 0.002, 0.009), M['preto'])
for m in leds:
    emis_k(m, [(0, 10), (T_QUEDA, 10), (T_QUEDA + 0.05, 0), (T_OK, 0), (T_OK + 0.05, 12), (DUR, 12)])

# ---------- nobreak (entra na correção) ----------
nb = cube('nobreak', (RX, 0.2, 0.2), (0.2, 0.14, 0.13), mat('nb', (0.025, 0.025, 0.027), 0.35, clearcoat=0.5), 0.01)
nbl = cube('nb_painel', (RX, 0.058, 0.25), (0.06, 0.002, 0.025), mat('nbp', (0, 0, 0), emis=VERDE, es=9))
nbb = cil('nb_bt', (RX + 0.12, 0.055, 0.25), 0.015, 0.006, mat('nbb', (0, 0, 0), emis=VERDE, es=12))
for o in (nb, nbl, nbb):
    o.location.z += 0.5; o.keyframe_insert('location', index=2, frame=1); o.keyframe_insert('location', index=2, frame=T(T_FIX))
    o.location.z -= 0.5; o.keyframe_insert('location', index=2, frame=T(T_FIX + 0.6))
    visivel(o, [(0, False), (T_FIX, True)])
# cabo de energia do nobreak até os aparelhos (cresce)
M_en = mat('energia', (0.02, 0.02, 0.02), 0.4, emis=VERDE, es=0)
cb, _ = cabo('cabo_nb', [(RX + 0.21, 0.25, 0.25), (RX + 0.3, 0.25, 0.5), (RX + 0.27, 0.25, 0.92)], M_en, esp=0.006)
cb.data.bevel_factor_mapping_end = 'SPLINE'
cb.data.bevel_factor_end = 0.0; cb.data.keyframe_insert('bevel_factor_end', frame=T(T_FIX + 0.6))
cb.data.bevel_factor_end = 1.0; cb.data.keyframe_insert('bevel_factor_end', frame=T(T_OK))
emis_k(M_en, [(0, 0), (T_FIX + 0.6, 0), (T_FIX + 0.8, 5), (DUR, 5)])

# ---------- câmera bullet na parede ----------
CX, CZ = 0.05, 1.8
cube('suporte', (CX, 0.37, CZ), (0.05, 0.03, 0.05), M_rk, 0.006)
cil('braco', (CX, 0.3, CZ), 0.015, 0.12, M_rk)
corpo = cil('corpo_cam', (CX, 0.15, CZ - 0.02), 0.06, 0.26, mat('camb', (0.85, 0.85, 0.83), 0.3, clearcoat=0.6))
cube('viseira', (CX, 0.13, CZ + 0.045), (0.07, 0.15, 0.008), mat('camv', (0.85, 0.85, 0.83), 0.3), 0.004)
cil('lente', (CX, 0.018, CZ - 0.02), 0.042, 0.01, mat('vidro', (0.01, 0.01, 0.012), 0.05, clearcoat=1.0))
M_ir = mat('ir', (0.05, 0.0, 0.0), emis=(0.6, 0.05, 0.05), es=0)
for k in range(6):
    a = k * math.pi / 3
    cil(f'ir{k}', (CX + 0.032 * math.cos(a), 0.012, CZ - 0.02 + 0.032 * math.sin(a)), 0.006, 0.004, M_ir)
M_st = mat('status', (0, 0, 0), emis=VERDE, es=10)
cil('status', (CX + 0.045, 0.06, CZ - 0.065), 0.006, 0.004, M_st, rot=(0, 0, 0))
emis_k(M_st, [(0, 10), (T_QUEDA, 10), (T_QUEDA + 0.05, 0), (T_OK + 0.3, 0), (T_OK + 0.35, 12), (DUR, 12)])
emis_k(M_ir, [(0, 1.5), (T_QUEDA, 1.5), (T_QUEDA + 0.05, 0), (T_OK + 0.3, 0), (T_OK + 0.35, 1.5), (DUR, 1.5)])
# cabo de rede do switch até a câmera (PoE)
M_rede = mat('rede', (0.02, 0.02, 0.02), 0.4, emis=VERDE, es=4)
cabo('poe', [(RX + 0.15, 0.36, 0.8), (RX + 0.2, 0.39, 1.15), (CX - 0.05, 0.39, CZ - 0.25), (CX, 0.385, CZ - 0.03)], M_rede, esp=0.005)
emis_k(M_rede, [(0, 4), (T_QUEDA, 4), (T_QUEDA + 0.05, 0), (T_OK + 0.2, 0), (T_OK + 0.3, 6), (DUR, 6)])

def anel(loc, t0, cor, forte, r=0.08, alcance=3.0, rot=(math.pi / 2, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=0.003, location=loc, rotation=rot)
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
for t0 in (0.3, 1.2):
    anel((CX, 0.0, CZ - 0.02), t0, VERDE, False, r=0.06, alcance=2.5)
for t0 in (T_QUEDA + 0.3, 3.6, 4.9, 6.2):
    anel((CX, 0.0, CZ - 0.02), t0, VERM, False, r=0.06, alcance=2.5)
for t0 in (T_OK + 0.4, 11.0, 12.6, 14.2, 15.8, 17.4, 19.0):
    anel((CX, 0.0, CZ - 0.02), t0, VERDE, True, r=0.06, alcance=3.0)
EV += [(0.3, 'batida'), (T_QUEDA, 'erro'), (T_FIX, 'whoosh'), (T_OK, 'ding'), (T_OK + 0.35, 'plim')]

# luz principal: cai na queda (fica luz de recorte, clima escuro)
def area(loc, rot, en, cor, tam):
    l = bpy.data.lights.new('a', 'AREA'); l.energy = en; l.color = cor; l.size = tam
    o = bpy.data.objects.new('a', l); o.location = loc; o.rotation_euler = rot; bpy.context.collection.objects.link(o); return l
ch = area((-1.2, -1.8, 2.2), (math.radians(55), 0, math.radians(-35)), 240, (1, 0.93, 0.85), 1.6)
for t, e in ((0, 240), (T_QUEDA, 240), (T_QUEDA + 0.08, 45), (DUR, 45)):
    ch.energy = e; ch.keyframe_insert('energy', frame=T(t))
vd = area((1.6, -0.6, 1.6), (math.radians(70), 0, math.radians(100)), 110, VERDE, 1.0)
for t, e in ((0, 110), (T_QUEDA, 110), (T_QUEDA + 0.08, 35), (T_OK, 35), (T_OK + 0.3, 110), (DUR, 110)):
    vd.energy = e; vd.keyframe_insert('energy', frame=T(t))
area((-1.8, -0.4, 1.2), (math.radians(70), 0, math.radians(-110)), 70, (1, 0.7, 0.45), 1.0)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.02

kc = camera(lente=34, fstop=2.8)
kc(0.0, (0.3, -0.5, 1.68), (CX, 0.05, CZ - 0.02))        # close na câmera gravando
kc(2.6, (0.25, -0.65, 1.66), (CX, 0.05, CZ - 0.03))
kc(3.8, (0.05, -2.2, 1.25), (-0.22, 0.2, 1.0))                # abre: rack e câmera apagados
kc(7.4, (-0.05, -2.1, 1.2), (-0.22, 0.2, 1.0))
kc(8.0, (-0.1, -1.1, 0.55), (RX, 0.2, 0.4))                # nobreak entrando no rack
kc(11.6, (-0.25, -1.0, 0.75), (RX, 0.2, 0.6))
kc(12.6, (-0.5, -2.2, 1.3), (-0.22, 0.2, 1.0))             # resultado
kc(DUR, (-0.1, -2.35, 1.35), (-0.22, 0.2, 1.0))
finalizar(OUT)
