# MOVE Explica 3D premium — Caiu a luz: câmeras, gravador e Wi-Fi apagam. Nobreak no rack segura tudo.
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib3d import *
OUT = os.path.dirname(os.path.abspath(__file__))
DUR = 21.5
sc = iniciar(DUR); materiais(); estudio(sanca=True, parede_y=1.2)
T_OUT = 1.3; T_FIX = 4.6; T_ON = 5.6
AMBAR = (1.0, 0.6, 0.12)

# ---------- rack aberto ----------
RX, RY = 0.0, 0.4
M_rk = mat('rack', (0.03, 0.03, 0.032), 0.35, metal=0.9)
for dx in (-0.27, 0.27):
    for dy in (-0.2, 0.2):
        cube('poste', (RX + dx, RY + dy, 0.6), (0.012, 0.012, 0.6), M_rk)
for z in (0.02, 1.2):
    cube('quadro', (RX, RY, z), (0.28, 0.21, 0.012), M_rk)
LEDS = []
def equip(nome, z, alt, nled, cor=VERDE):
    cube(nome, (RX, RY, z), (0.25, 0.19, alt), M['alu'], 0.004)
    cube(nome + 'f', (RX, RY - 0.191, z), (0.245, 0.002, alt * 0.85), mat(nome + 'fm', (0.32, 0.32, 0.33), 0.45))
    for k in range(nled):
        m = mat(f'{nome}led{k}', (0, 0, 0), emis=cor, es=10)
        cil(f'{nome}l{k}', (RX - 0.2 + k * (0.3 / max(1, nled - 1)), RY - 0.195, z + alt * 0.3), 0.0045, 0.004, m)
        LEDS.append((m, k))
equip('switch', 1.02, 0.022, 10)
equip('roteador', 0.9, 0.03, 4)
equip('gravador', 0.74, 0.045, 3)
# nobreak (entra na correção)
nb = cube('nobreak', (RX, RY, 0.16), (0.25, 0.19, 0.11), mat('nbm', (0.02, 0.02, 0.022), 0.3, clearcoat=0.5), 0.006)
nbf = _f = cube('nbfrente', (RX, RY - 0.191, 0.16), (0.245, 0.002, 0.1), mat('nbfr', (0.32, 0.32, 0.33), 0.45)); _f.parent = nb; _f.matrix_parent_inverse = nb.matrix_world.inverted()
nbf = cube('nbtela', (RX + 0.12, RY - 0.194, 0.2), (0.06, 0.002, 0.025), mat('nbtela', (0, 0, 0), emis=AMBAR, es=0))
nbf.parent = nb; nbf.matrix_parent_inverse = nb.matrix_world.inverted()
nbl_m = mat('nbled', (0, 0, 0), emis=VERDE, es=0)
l = cil('nbl', (RX - 0.18, RY - 0.197, 0.2), 0.01, 0.004, nbl_m); l.parent = nb; l.matrix_parent_inverse = nb.matrix_world.inverted()
for t, x in ((0, RX + 1.6), (T_FIX, RX + 1.6), (T_FIX + 0.9, RX)):
    nb.location = (x, RY, 0.16); nb.keyframe_insert('location', frame=T(t))
emis_k(nbf.data.materials[0], [(0, 0), (T_FIX + 0.9, 0), (T_ON, 6)])
emis_k(nbl_m, [(0, 0), (T_ON, 12)])

# ---------- câmera de segurança na parede ----------
CX, CZ = 0.75, 1.55
M_br = mat('branco', (0.85, 0.85, 0.83), 0.3, clearcoat=0.5)
cube('base_cam', (CX, 1.15, CZ), (0.05, 0.02, 0.05), M_br, 0.008)
cil('braco', (CX, 1.08, CZ), 0.012, 0.12, M_br)
corpo = cil('corpo_cam', (CX - 0.02, 0.98, CZ - 0.02), 0.045, 0.22, M_br)
cil('lente', (CX - 0.02, 0.868, CZ - 0.02), 0.03, 0.01, mat('vidro', (0.0, 0.0, 0.0), 0.05, clearcoat=1.0))
cam_led = mat('camled', (0, 0, 0), emis=VERDE, es=10)
cil('camled', (CX + 0.012, 0.869, CZ + 0.012), 0.005, 0.004, cam_led)
# cabo de energia/rede descendo da câmera ao rack
cabo('cabo_cam', [(CX, 1.15, CZ - 0.05), (CX, 1.1, 1.2), (RX + 0.3, RY + 0.1, 1.1), (RX + 0.25, RY + 0.1, 1.0)], mat('cabocinza', (0.4, 0.4, 0.4), 0.5), esp=0.004)

# ---------- queda de energia ----------
ALL = [m for m, _ in LEDS] + [cam_led]
for m in ALL:
    emis_k(m, [(0, 10), (T_OUT - 0.05, 10), (T_OUT, 0), (T_ON, 0), (T_ON + 0.05, 10)])
# sanca (luz da casa) apaga e não volta (só o rack volta com o nobreak)
sanca = [o for o in bpy.data.objects if o.data and hasattr(o.data, 'materials') and o.data.materials and o.data.materials[0].name.startswith('sanca')]
for o in sanca:
    emis_k(o.data.materials[0], [(0, 6), (T_OUT - 0.05, 6), (T_OUT, 0.15)])
# LED da câmera: vermelho piscando sem energia
cor_k(cam_led, [(0, VERDE), (T_OUT, VERM), (T_ON, VERM), (T_ON + 0.05, VERDE)])
emis_k(cam_led, [(T_OUT + 0.3, 12), (T_OUT + 0.7, 0), (T_OUT + 1.1, 12), (T_OUT + 1.5, 0), (T_OUT + 1.9, 12), (T_OUT + 2.3, 0), (T_OUT + 2.7, 12), (T_ON - 0.05, 0)])
EV += [(0.3, 'batida'), (T_OUT, 'erro'), (T_FIX, 'whoosh'), (T_ON, 'ding')]

# ---------- anéis de energia saindo do nobreak (alpha) ----------
def anel2(loc, t0, cor, r=0.12, alc=3.0):
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=0.004, location=loc, rotation=(math.pi / 2, 0, 0)); o = bpy.context.object
    m = mat('anel', (0, 0, 0), emis=cor, es=0); o.data.materials.append(m)
    b = m.node_tree.nodes['Principled BSDF']; em = b.inputs['Emission Strength']; al = b.inputs['Alpha']
    f0 = T(t0); f1 = T(t0 + 1.2)
    for f, s_, e, a in ((max(1, f0 - 1), 0.01, 0, 0), (f0, 1.0, 12, 1), (f1, alc, 0, 0), (f1 + 1, 0.0, 0, 0)):
        o.scale = (s_, s_, s_); o.keyframe_insert('scale', frame=f); em.default_value = e; em.keyframe_insert('default_value', frame=f); al.default_value = a; al.keyframe_insert('default_value', frame=f)
t = T_ON + 0.2
while t < DUR - 1.0:
    anel2((RX, RY - 0.2, 0.16), t, VERDE)
    t += 0.7
t = 0.3
while t < T_OUT:
    anel2((RX, RY - 0.2, 0.9), t, VERDE, alc=2.2); t += 0.5

luzes(chave=230, verde=120, quente=90)
kc = camera(lente=32, fstop=3.2)
kc(0.0, (-0.35, -0.9, 1.05), (0.15, RY, 1.0))          # rack + câmera ligados
kc(T_OUT + 1.5, (-0.25, -1.0, 1.1), (0.25, RY, 1.05))
kc(T_FIX - 0.2, (0.45, -1.4, 0.65), (0.0, RY, 0.42))      # nobreak entrando
kc(T_ON + 1.2, (0.35, -1.3, 0.6), (0.0, RY, 0.4))
kc(8.6, (-0.5, -1.6, 1.0), (0.1, RY, 0.75))            # tudo funcionando com nobreak
kc(12.5, (-0.3, -1.5, 1.1), (0.2, RY, 0.8))
kc(13.4, (0.42, 0.3, 1.5), (CX - 0.05, 0.95, CZ - 0.03))  # câmera gravando
kc(16.6, (0.36, 0.25, 1.46), (CX - 0.05, 0.95, CZ - 0.03))
kc(17.4, (-0.1, -1.9, 1.05), (0.25, RY, 0.8))
kc(DUR, (0.15, -2.1, 1.1), (0.25, RY, 0.8))
finalizar(OUT)
