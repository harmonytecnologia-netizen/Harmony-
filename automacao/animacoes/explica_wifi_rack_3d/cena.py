# MOVE Explica 3D premium — Roteador fechado no rack: Wi-Fi fraco na casa (maquete arquitetônica)
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib3d import *
OUT = os.path.dirname(os.path.abspath(__file__))
DUR = 21.5
sc = iniciar(DUR); materiais(); estudio(sanca=False, parede_y=6)

# ---------- maquete: laje + paredes baixas ----------
M_maq = mat('maquete', (0.62, 0.6, 0.56), 0.6)
M_piso_m = mat('piso_maq', (0.2, 0.12, 0.07), 0.35, clearcoat=0.4)
cube('laje', (0, 0, 0.03), (1.15, 1.55, 0.03), M_maq, 0.005)
cube('piso_madeira', (0, 0, 0.062), (1.1, 1.5, 0.002), M_piso_m)
H = 0.36; E = 0.02
def parede(n, a, b):
    (x0, y0), (x1, y1) = a, b
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; sx = abs(x1 - x0) / 2 or E; sy = abs(y1 - y0) / 2 or E
    cube(n, (cx, cy, 0.064 + H / 2), (sx, sy, H / 2), M_maq, 0.003)
parede('fundo', (-1.12, 1.52), (1.12, 1.52)); parede('esq', (-1.12, -1.52), (-1.12, 1.52)); parede('dir', (1.12, -1.52), (1.12, 1.52))
parede('meio_a', (0, -1.52), (0, -0.35)); parede('meio_b', (0, -0.05), (0, 1.52))
parede('trans_e', (-1.12, 0), (-0.45, 0)); parede('trans_d', (0.4, 0), (1.12, 0))
SALAS = [(-0.56, -0.76), (0.56, -0.76), (-0.56, 0.76), (0.56, 0.76)]
# móveis simples (escala)
cube('sofa', (0.56, -1.05, 0.11), (0.35, 0.12, 0.05), mat('sofa', (0.35, 0.33, 0.3), 0.8), 0.02)
cube('cama1', (-0.56, 0.95, 0.1), (0.25, 0.32, 0.04), mat('cama', (0.7, 0.68, 0.64), 0.8), 0.02)
cube('cama2', (0.56, 0.95, 0.1), (0.22, 0.3, 0.04), mat('cama', (0.7, 0.68, 0.64), 0.8), 0.02)
cube('mesa', (-0.5, -0.7, 0.13), (0.22, 0.14, 0.01), M['madeira'], 0.005)

# ---------- rack fechado com o roteador ----------
RK = (-0.95, -1.35)
cube('rack', (RK[0], RK[1], 0.064 + 0.14), (0.12, 0.1, 0.14), mat('rackm', (0.05, 0.05, 0.055), 0.3, metal=0.9), 0.004)
cil('rack_led', (RK[0] + 0.07, RK[1] - 0.102, 0.3), 0.006, 0.004, mat('rled', (0, 0, 0), emis=VERDE, es=15))

# ---------- indicadores de sinal em cada ambiente ----------
INDS = []
for i, (x, y) in enumerate(SALAS):
    m = mat(f'ind{i}', (0, 0, 0), emis=VERM, es=0)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.07, minor_radius=0.008, location=(x, y + 0.25, 0.075)); o = bpy.context.object; o.data.materials.append(m)
    INDS.append(m)
T_FIX = 12.4
for i, m in enumerate(INDS):
    perto = (i == 0)
    cor_k(m, [(0, VERDE if perto else VERM), (T_FIX + 1.6 + i * 0.25, VERDE if perto else VERM), (T_FIX + 1.7 + i * 0.25, VERDE)])
    emis_k(m, [(0, 0), (3.6, 0), (4.2, 12), (T_FIX + 1.6 + i * 0.25, 12), (T_FIX + 1.7 + i * 0.25, 18)])
    if not perto: EV.append((T_FIX + 1.7 + i * 0.25, 'plim'))

# ---------- ondas ----------
def onda(loc, t0, cor, alc, es):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.1, minor_radius=0.0035, location=loc); o = bpy.context.object
    m = mat('onda', (0, 0, 0), emis=cor, es=0); o.data.materials.append(m)
    em = m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
    for f, s, e in ((max(1, T(t0) - 1), 0.01, 0), (T(t0), 1.0, es), (T(t0 + 1.4), alc, 0), (T(t0 + 1.4) + 1, 0.0, 0)):
        o.scale = (s, s, s); o.keyframe_insert('scale', frame=f); em.default_value = e; em.keyframe_insert('default_value', frame=f)
APS = [(-0.56, -0.62), (0.56, -0.62), (-0.56, 0.62), (0.56, 0.62)]
t = 0.4
while t < DUR - 1.2:
    if t < T_FIX - 1.4: onda((RK[0], RK[1], 0.3), t, VERM, 4.0, 6); t += 0.6
    elif t < T_FIX + 1.3: t += 0.3
    else:
        for (x, y) in APS: onda((x, y, H + 0.03), t, VERDE, 5.5, 10)
        t += 0.6

# ---------- correção: cabos de rede pelo forro até os access points ----------
M_rede = mat('rede', (0, 0, 0), emis=VERDE, es=6)
for i, (x, y) in enumerate(APS):
    cb, _ = cabo(f'rede{i}', [(RK[0], RK[1], 0.36), (RK[0], RK[1], H + 0.07), ((RK[0] + x) / 2, (RK[1] + y) / 2, H + 0.08), (x, y, H + 0.07)], M_rede, esp=0.004)
    cb.data.bevel_factor_mapping_end = 'SPLINE'
    cb.data.bevel_factor_end = 0.0; cb.data.keyframe_insert('bevel_factor_end', frame=T(T_FIX + 0.1))
    cb.data.bevel_factor_end = 1.0; cb.data.keyframe_insert('bevel_factor_end', frame=T(T_FIX + 1.0 + i * 0.1))
    ap = cil(f'ap{i}', (x, y, H + 0.075), 0.055, 0.016, mat('apm', (0.85, 0.85, 0.83), 0.35), rot=(0, 0, 0))
    led = cil(f'apled{i}', (x, y, H + 0.084), 0.012, 0.004, mat('apled', (0, 0, 0), emis=VERDE, es=14), rot=(0, 0, 0))
    for o in (ap, led): visivel(o, [(0, False), (T_FIX + 1.0 + i * 0.1, True)])
EV += [(0.3, 'batida'), (3.6, 'whoosh'), (8.2, 'erro'), (T_FIX, 'whoosh'), (T_FIX + 1.2, 'ding')]

luzes(chave=320, verde=120, quente=110)
kc = camera(lente=30, fstop=4.0)
kc(0.0, (-0.6, -2.0, 0.55), (RK[0], RK[1], 0.22))          # close no rack fechado
kc(3.0, (-0.45, -2.4, 1.0), (RK[0] + 0.2, RK[1] + 0.3, 0.2))
kc(4.0, (0.2, -3.0, 3.6), (0, 0.05, 0.1))                 # maquete de cima
kc(11.6, (0.45, -2.8, 3.5), (0, 0.05, 0.1))
kc(12.6, (-0.2, -2.3, 2.2), (-0.3, -0.5, 0.3))            # cabos subindo para o forro
kc(15.0, (0.0, -2.9, 3.4), (0, 0.05, 0.15))
kc(DUR, (-0.35, -3.1, 3.7), (0, 0.1, 0.1))
finalizar(OUT)
