# MOVE Explica 3D premium — Caixas surround no chão atrás do sofá x nas laterais, acima do ouvido
# Referência técnica (Dolby 5.1): surround nas laterais, levemente atrás do ponto de escuta (90–110°),
# 30–60 cm acima do ouvido de quem está sentado.
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib3d import *
OUT = os.path.dirname(os.path.abspath(__file__))
DUR = 22.5
sc = iniciar(DUR); materiais()
# ---------- sala: piso, parede do fundo (atrás do sofá) com sanca, paredes laterais com painel ripado ----------
bpy.ops.mesh.primitive_plane_add(size=40); obj(bpy.context.object, M['piso'])
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, -2.1, 0), rotation=(math.pi / 2, 0, 0)); obj(bpy.context.object, M['parede'])
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -2.05, 2.55), rotation=(math.pi / 2, 0, 0))
f = bpy.context.object; f.scale = (8, 0.03, 1); obj(f, mat('sanca', (0, 0, 0), emis=QUENTE, es=6))
for sx in (-1, 1):
    cube(f'parL{sx}', (sx * 1.52, 0, 1.5), (0.02, 3.0, 1.5), M['parede'])
    for k in range(18):  # ripado de nogueira
        cube(f'ripa{sx}_{k}', (sx * 1.49, -1.45 + k * 0.1, 1.35), (0.012, 0.03, 1.35), M['madeira'], 0.003)
# TV ao fundo (frente do sofá)
cube('painel', (0, 2.3, 1.25), (1.6, 0.03, 1.25), mat('painelm', (0.035, 0.02, 0.012), 0.55), 0.005)
cube('tv', (0, 2.25, 1.25), (0.85, 0.02, 0.48), mat('tela', (0, 0, 0), 0.12, emis=(0.12, 0.16, 0.2), es=1.2), 0.004)
# ---------- sofá de couro ----------
COURO = mat('couro', (0.09, 0.055, 0.035), 0.42, clearcoat=0.25)
cube('assento', (0, -0.05, 0.3), (0.95, 0.42, 0.14), COURO, 0.06)
cube('almof', (0, -0.08, 0.47), (0.9, 0.38, 0.05), COURO, 0.05)
cube('encosto', (0, -0.42, 0.68), (0.95, 0.1, 0.36), COURO, 0.06)
for sx in (-1, 1):
    cube(f'braco{sx}', (sx * 0.98, -0.05, 0.48), (0.08, 0.44, 0.2), COURO, 0.05)
cube('base_sofa', (0, -0.05, 0.08), (0.9, 0.38, 0.08), M['frente'])
# ponto de escuta (altura do ouvido, sentado ~1,1 m)
EAR = (0, -0.12, 1.08)
bpy.ops.mesh.primitive_torus_add(major_radius=0.13, minor_radius=0.006, location=EAR, rotation=(0, 0, 0))
ESC = bpy.context.object; MESC = mat('escuta', (0, 0, 0), emis=VERM, es=3); ESC.data.materials.append(MESC)
cor_k(MESC, [(0, VERM), (7.5, VERM), (7.6, VERDE)])
emis_k(MESC, [(0, 0), (1.0, 3), (7.5, 2), (7.9, 6), (DUR, 6)])

# ---------- caixas surround: começam no chão atrás do sofá e sobem para as laterais ----------
S = 0.8
T0, T1 = 6.7, 7.7  # virada
CAIXAS = []
for sx in (-1, 1):
    c, v = caixa(f'surr{sx}', 0, 0, z=0.33 * S + 0.005, s=S, pedestal=False)
    # pose errada: chão, atrás do encosto, virada para o sofá
    ini = (sx * 0.6, -1.15, 0.0); rini = (0, 0, math.pi)
    # pose certa: parede lateral, um pouco atrás do ouvido, ~40 cm acima dele, virada para o sofá
    fim = (sx * 1.36, -0.42, 1.18); rfim = (0, 0, -sx * math.pi / 2)
    for tt, p, r in ((0, ini, rini), (T0, ini, rini), (T0 + 0.45, (sx * 1.0, -0.9, 0.9), (0, 0, math.pi - sx * math.pi / 4)), (T1, fim, rfim)):
        v.location = p; v.keyframe_insert('location', frame=T(tt)); v.rotation_euler = r; v.keyframe_insert('rotation_euler', frame=T(tt))
    CAIXAS.append((sx, c))
EV += [(0.0, 'impacto'), (T0 - 1.2, 'riser'), (T1, 'impacto')]

cones([c for _, c in CAIXAS], DUR, lambda i, t: 0.006 if t < T0 else (0.0 if t < T1 + 0.2 else 0.008))

# ---------- anéis de som ----------
zc = 0.33 * S + 0.005 - 0.12 * S  # altura do woofer no chão
t = 0.5
while t < DUR - 1.0:
    if t < T0 - 0.2:   # no chão: o som bate no encosto e morre (vermelho, curto)
        for sx, _ in CAIXAS:
            anel((sx * 0.6, -1.0, zc), t, VERM, False, r=0.09, alcance=2.6)
        t += 0.55
    elif t < T1 + 0.2:
        t += 0.3
    elif 12.5 < t < 17.0:  # close da altura: sem anéis para ler a medida
        t += 0.5
    else:              # nas laterais: o som cruza o ponto de escuta (verde, forte)
        for sx, _ in CAIXAS:
            anel((sx * 1.2, -0.42, 1.18 + 0.33 * S + 0.005 - 0.12 * S), t, VERDE, True, r=0.1, rot=(0, math.pi / 2, 0), alcance=6.0)
        t += 0.5

# ---------- marcação de altura: ouvido -> caixa (30-60 cm) ----------
LIN = mat('linha', (0, 0, 0), emis=VERDE, es=8)
zt = 1.18 + 0.33 * S
for sx in (-1,):
    l1 = cube('alt_v', (sx * 1.15, -0.2, (EAR[2] + zt) / 2), (0.006, 0.006, (zt - EAR[2]) / 2), LIN)
    l2 = cube('alt_ouvido', (sx * 0.575, -0.2, EAR[2]), (0.575, 0.004, 0.004), LIN)
    tx, _ = texto('alt_txt', '30-60 cm', (sx * 0.93, -0.2, (EAR[2] + zt) / 2 + 0.02), 0.075, VERDE, es=10, rot=(math.pi / 2, 0, math.pi))
    for o in (l1, l2, tx): visivel(o, [(0, False), (12.4, True), (17.2, False)])

luzes(chave=150, verde=150, quente=110)
# luz de destaque nas caixas certas
kc = camera(lente=28, fstop=2.4)
CD = bpy.context.scene.camera.data
def lente(tt, l): CD.lens = l; CD.keyframe_insert('lens', frame=T(tt))
kc(0.0, (-1.25, -0.6, 0.38), (-0.55, -1.15, 0.22)); lente(0.0, 28)   # close: caixa no chão atrás do sofá
kc(2.6, (-1.12, -0.78, 0.5), (-0.5, -1.12, 0.28)); lente(2.6, 28)
kc(3.4, (0.0, -2.0, 2.1), (0.0, -0.5, 0.5)); lente(3.4, 20)           # geral por trás: o som morre no encosto
kc(6.4, (0.25, -1.95, 2.0), (0.0, -0.55, 0.55)); lente(6.4, 20)
kc(7.9, (0.0, 2.15, 2.0), (0.0, -0.5, 1.1)); lente(7.9, 18)            # de frente: caixas nas laterais, som cruzando
kc(12.2, (0.15, 2.1, 1.9), (0.0, -0.5, 1.1)); lente(12.2, 18)
kc(12.9, (-0.35, 0.75, 1.3), (-1.25, -0.42, 1.25)); lente(12.9, 30)   # close na altura: 30-60 cm acima do ouvido
kc(16.8, (-0.45, 0.65, 1.35), (-1.3, -0.42, 1.28)); lente(16.8, 30)
kc(17.6, (0.0, 2.15, 2.1), (0.0, -0.5, 1.0)); lente(17.6, 18)         # resultado: sala envolvida
kc(DUR, (-0.2, 2.1, 1.95), (0.0, -0.5, 1.05)); lente(DUR, 18)
finalizar(OUT)
