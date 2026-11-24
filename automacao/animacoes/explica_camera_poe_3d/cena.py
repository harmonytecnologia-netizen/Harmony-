# MOVE Explica 3D premium — SEGURANÇA: câmera no Wi-Fi fraco trava; certo = cabo de rede com PoE até a câmera.
# Referência técnica: PoE (IEEE 802.3af/at) leva energia e dados no mesmo cabo de rede (até 100 m) a partir de um
# switch PoE no rack; a câmera deixa de depender do sinal Wi-Fi e da tomada local.
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib3d import *
OUT = os.path.dirname(os.path.abspath(__file__))
DUR = 21.0
sc = iniciar(DUR); materiais(); estudio(sanca=True, parede_y=1.2)
T_FIX = 6.8; T_ON = 8.6
AMBAR = (1.0, 0.6, 0.12)

# ---------- rack à direita ----------
RX, RY = 0.5, 0.75
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
    ms = []
    for k in range(nled):
        m = mat(f'{nome}led{k}', (0, 0, 0), emis=cor, es=10)
        cil(f'{nome}l{k}', (RX - 0.2 + k * (0.3 / max(1, nled - 1)), RY - 0.195, z + alt * 0.3), 0.0045, 0.004, m)
        ms.append(m)
    return ms
sw_leds = equip('switch', 1.02, 0.022, 8)
equip('roteador', 0.88, 0.03, 4)
equip('gravador', 0.72, 0.045, 3)
equip('nobreak', 0.3, 0.1, 2)
# antenas do roteador
for dx in (-0.18, 0.18):
    a = cil('antena', (RX + dx, RY + 0.12, 1.02), 0.008, 0.22, M['preto'], rot=(0, 0, 0))
# switch PoE: LEDs da porta da câmera ficam apagados até a correção
emis_k(sw_leds[0], [(0, 0), (T_ON - 0.05, 0), (T_ON, 12)])
cor_k(sw_leds[0], [(0, AMBAR)])

# ---------- câmera de segurança na parede, à esquerda ----------
CX, CZ = -0.5, 1.75
M_br = mat('branco', (0.85, 0.85, 0.83), 0.3, clearcoat=0.5)
cube('base_cam', (CX, 1.17, CZ), (0.06, 0.02, 0.06), M_br, 0.008)
cil('braco', (CX, 1.09, CZ), 0.014, 0.14, M_br)
cil('corpo_cam', (CX + 0.02, 0.97, CZ - 0.03), 0.05, 0.25, M_br)
cube('pala', (CX + 0.02, 0.95, CZ + 0.03), (0.065, 0.14, 0.006), M_br, 0.004)
cil('lente', (CX + 0.02, 0.843, CZ - 0.03), 0.034, 0.012, mat('vidro', (0.0, 0.0, 0.0), 0.05, clearcoat=1.0))
cil('aro_lente', (CX + 0.02, 0.846, CZ - 0.03), 0.04, 0.008, M['alu_claro'])
cam_led = mat('camled', (0, 0, 0), emis=VERM, es=0)
cil('camled', (CX + 0.055, 0.842, CZ + 0.005), 0.006, 0.004, cam_led)
# LED vermelho piscando (sem sinal) -> verde fixo depois do cabo
pis = []
t = 0.4
while t < T_ON:
    pis += [(t, 14), (t + 0.25, 0)]; t += 0.6
emis_k(cam_led, [(0, 0)] + pis + [(T_ON, 12)])
cor_k(cam_led, [(0, VERM), (T_ON - 0.05, VERM), (T_ON, VERDE)])

# ---------- Wi-Fi fraco: anéis vermelhos que morrem no meio do caminho ----------
def onda(loc, t0, cor, r0=0.1, alc=7.0, dur=1.6, es=10, rot=(math.pi / 2, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=r0, minor_radius=0.0025, location=loc, rotation=rot); o = bpy.context.object
    m = mat('onda', (0, 0, 0), emis=cor, es=0); o.data.materials.append(m)
    b = m.node_tree.nodes['Principled BSDF']; em = b.inputs['Emission Strength']
    f0 = T(t0); f1 = T(t0 + dur)
    for f, s_, e in ((max(1, f0 - 1), 0.01, 0), (f0, 1.0, es), (f1, alc, 0), (f1 + 1, 0.0, 0)):
        o.scale = (s_, s_, s_); o.keyframe_insert('scale', frame=f); em.default_value = e; em.keyframe_insert('default_value', frame=f)
t = 0.2
while t < T_FIX - 0.4:
    onda((RX, RY - 0.25, 1.12), t, VERM, r0=0.08, alc=5.0, es=9); t += 0.55

# ---------- cabo de rede PoE: nasce do switch e vai até a câmera ----------
M_cabo = mat('cabo_poe', (0.02, 0.12, 0.08), 0.4, emis=VERDE, es=0)
pts = [(RX - 0.2, RY - 0.2, 1.02), (RX - 0.32, RY - 0.22, 1.18), (RX - 0.35, 1.1, 1.75), (0.05, 1.12, 2.15), (CX, 1.12, 2.1), (CX, 1.15, CZ + 0.07)]
cb, _ = cabo('cabo', pts, M_cabo, esp=0.009)
cb.data.bevel_factor_mapping_end = 'SPLINE'
cb.data.bevel_factor_end = 0.0; cb.data.keyframe_insert('bevel_factor_end', frame=T(T_FIX))
cb.data.bevel_factor_end = 1.0; cb.data.keyframe_insert('bevel_factor_end', frame=T(T_ON))
emis_k(M_cabo, [(0, 0), (T_FIX, 3), (T_ON, 6), (T_ON + 1.5, 1.5)])
# pulsos de dados/energia correndo no cabo (esferas verdes seguindo a curva)
bpy.ops.object.select_all(action='DESELECT')
for i in range(5):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.018, location=(0, 0, 0)); p = bpy.context.object
    pm = mat('pulso', (0, 0, 0), emis=VERDE, es=25); p.data.materials.append(pm)
    fp = p.constraints.new('FOLLOW_PATH'); fp.target = cb; fp.use_fixed_location = True
    for tt, v in ((0, 0.0), (T_ON, 0.0)):
        fp.offset_factor = v; fp.keyframe_insert('offset_factor', frame=T(tt))
    t0 = T_ON + i * 0.35
    k = 0
    while t0 < DUR:
        fp.offset_factor = 0.0; fp.keyframe_insert('offset_factor', frame=T(t0))
        fp.offset_factor = 1.0; fp.keyframe_insert('offset_factor', frame=T(t0 + 1.7) - 1)
        t0 += 1.75; k += 1
    visivel(p, [(0, False), (T_ON, True)])

# ---------- gravando: anéis verdes saindo da lente ----------
t = T_ON + 0.2
while t < DUR - 0.8:
    onda((CX + 0.02, 0.83, CZ - 0.03), t, VERDE, r0=0.05, alc=3.0, dur=1.2, es=8); t += 0.8

EV += [(0.0, 'impacto'), (T_FIX - 1.2, 'riser'), (T_ON, 'impacto')]

luzes(chave=230, verde=120, quente=90)
kc = camera(lente=32, fstop=3.0)
kc(0.0, (-0.05, 0.15, 1.55), (CX + 0.02, 0.9, CZ - 0.03))     # close na câmera (LED vermelho)
kc(2.4, (-0.12, 0.05, 1.6), (CX + 0.02, 0.9, CZ - 0.03))
kc(4.0, (0.0, -2.3, 1.35), (0.0, RY, 1.3))                  # recua: roteador longe, Wi-Fi morrendo
kc(6.6, (0.05, -2.5, 1.4), (0.0, RY, 1.3))
kc(T_ON + 0.4, (0.0, -2.7, 1.5), (0.0, 0.9, 1.35))          # cabo nascendo do switch até a câmera
kc(11.4, (0.75, -0.6, 1.1), (RX - 0.1, RY, 1.0))           # switch PoE aceso
kc(12.6, (0.0, 0.1, 1.6), (CX + 0.02, 0.9, CZ - 0.03))     # câmera gravando
kc(15.6, (-0.12, 0.0, 1.65), (CX + 0.02, 0.9, CZ - 0.03))
kc(16.6, (0.0, -2.4, 1.4), (0.0, 0.9, 1.35))
kc(DUR, (0.0, -2.9, 1.45), (0.0, 0.9, 1.35))
finalizar(OUT)
