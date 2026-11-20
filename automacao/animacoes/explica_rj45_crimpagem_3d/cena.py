# MOVE Explica 3D premium — REDE: cabo de rede mal crimpado (par curto / capa fora) = link de 100 Mb
# Referência técnica: Gigabit Ethernet (1000BASE-T) usa os 4 pares; se um par não faz contato,
# a placa negocia Fast Ethernet (100BASE-TX, 2 pares) e o teste fica em ~94 Mb/s.
# Certo: padrão T568B, 8 fios na ordem até o fim do conector, capa presa pela trava, testar com testador (8 LEDs).
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib3d import *
OUT = os.path.dirname(os.path.abspath(__file__))
DUR = 21.0
sc = iniciar(DUR); materiais()
estudio(sanca=True, parede_y=3.2)

# ---------- conector RJ45 (escala grande: 1 un = ~2 cm reais) ----------
CLARO = mat('plastico', (0.85, 0.9, 0.92), 0.06)
b = CLARO.node_tree.nodes['Principled BSDF']; b.inputs['Transmission Weight'].default_value = 0.92; b.inputs['IOR'].default_value = 1.45
Z0 = 0.16  # altura do centro do conector
corpo = cube('corpo', (0, 0, Z0), (0.19, 0.31, 0.12), CLARO, 0.02)
trava = cube('trava', (0, 0.12, Z0 + 0.15), (0.07, 0.16, 0.012), CLARO, 0.006)
trava.rotation_euler = (math.radians(-12), 0, 0)
# contatos dourados no topo da frente
for k in range(8):
    x = -0.1225 + k * 0.035
    cube(f'contato{k}', (x, -0.2, Z0 + 0.105), (0.007, 0.08, 0.018), M['ouro'], 0.002)

# ---------- fios (T568B) ----------
CORES = [((0.95, 0.92, 0.88), (1.0, 0.45, 0.05)), ((1.0, 0.45, 0.05), None),
         ((0.95, 0.92, 0.88), (0.1, 0.65, 0.2)), ((0.05, 0.25, 0.85), None),
         ((0.95, 0.92, 0.88), (0.05, 0.25, 0.85)), ((0.1, 0.65, 0.2), None),
         ((0.95, 0.92, 0.88), (0.42, 0.24, 0.1)), ((0.42, 0.24, 0.1), None)]
FIOS = []
YF = -0.27   # ponta certa (encostada nos contatos)
YT = 0.62    # traseira (dentro da capa)
for k, (c1, c2) in enumerate(CORES):
    x = -0.1225 + k * 0.035
    base = c1 if c2 is None else (0.5 * c1[0] + 0.5 * c2[0], 0.5 * c1[1] + 0.5 * c2[1], 0.5 * c1[2] + 0.5 * c2[2])
    m = mat(f'fio{k}', base, 0.35, clearcoat=0.3)
    L = YT - YF
    f = cil(f'fio{k}', (x, (YF + YT) / 2, Z0 + 0.03), 0.0145, L, m, rot=(math.pi / 2, 0, 0), v=24)
    FIOS.append((f, x, L))

# par marrom (7 e 8) curto e torto no começo; depois desliza até os contatos
T0, T1 = 9.3, 10.5
CURTO = 0.24  # quanto falta até os contatos
for k in (6, 7):
    f, x, L = FIOS[k]
    for tt, dy, dz, rz in ((0, CURTO, 0.035, 0.12 if k == 6 else -0.1), (T0, CURTO, 0.035, 0.12 if k == 6 else -0.1), (T1, 0, 0, 0)):
        f.location = (x, (YF + YT) / 2 + dy, Z0 + 0.03 + dz); f.keyframe_insert('location', frame=T(tt))
        f.rotation_euler = (math.pi / 2, 0, rz); f.keyframe_insert('rotation_euler', frame=T(tt))
# brilho de alerta no próprio par marrom (vermelho pulsando -> verde ao encaixar)
VRM = (1.0, 0.06, 0.04)
for k in (6, 7):
    m = FIOS[k][0].data.materials[0]
    cor_k(m, [(0, VRM), (T1, VRM), (T1 + 0.1, VERDE)])
    emis_k(m, [(0, 0), (4.6, 0), (5.2, 2.5), (6.5, 0.6), (7.5, 2.5), (8.5, 0.6), (T0, 2), (T1 + 0.2, 2.5), (12.0, 0), (DUR, 0)])

# ---------- capa azul do cabo: começa para fora, entra no conector ----------
AZUL = mat('capa', (0.04, 0.22, 0.75), 0.4, clearcoat=0.3)
capa, sp = cabo('capa', [(0, 0.48, Z0), (0, 1.0, Z0), (0.15, 1.8, Z0 - 0.01), (0.7, 2.6, 0.12)], AZUL, esp=0.11)
capa.scale = (1.3, 1, 0.95)
for tt, y in ((0, 0.12), (T0, 0.12), (T1, -0.28)):
    capa.location.y = y; capa.keyframe_insert('location', frame=T(tt))

# ---------- testador com 8 LEDs ----------
TX, TY = 0.95, 0.35
tst = amplificador('testador', (TX, TY, 0.12), esc=(0.34, 0.2, 0.12), led=VERDE, botoes=False)
LEDS = []
for k in range(8):
    m = mat(f'led{k}', (0, 0, 0), emis=VERM if k >= 6 else VERDE, es=0)
    l = cil(f'ledo{k}', (TX - 0.245 + k * 0.07, TY - 0.205, 0.15), 0.022, 0.02, m, v=32)
    LEDS.append(m)
# antes da correção (2,5-8 s): 1-6 verdes, 7-8 vermelhos piscando; depois (14,4 s+) acendem em sequência, todos verdes
for k, m in enumerate(LEDS):
    if k < 6:
        emis_k(m, [(0, 0), (2.6, 0), (2.8, 6), (9.0, 6), (9.2, 0), (14.4 + k * 0.22, 0), (14.5 + k * 0.22, 9), (DUR, 9)])
    else:
        emis_k(m, [(0, 0), (2.6, 0), (2.8, 7), (3.4, 0), (4.0, 7), (4.6, 0), (5.2, 7), (5.8, 0), (6.4, 7), (7.0, 0), (7.6, 7), (9.0, 0),
                   (14.4 + k * 0.22, 0), (14.5 + k * 0.22, 9), (DUR, 9)])
        cor_k(m, [(0, VERM), (12.0, VERM), (12.1, VERDE)])

# ---------- números 3D ----------
t94, m94 = texto('t94', '94 Mb', (0.0, 0.35, 0.56), 0.13, (1.0, 0.06, 0.04), es=3, rot=(math.radians(80), 0, 0))
visivel(t94, [(0, False), (0.6, True), (9.0, False)])
t500, m500 = texto('t500', '500 MEGA', (0.4, 0.35, 0.62), 0.15, VERDE, es=4, rot=(math.radians(80), 0, 0))
visivel(t500, [(0, False), (16.6, True), (DUR, True)])
EV += [(0.0, 'impacto'), (T0 - 1.2, 'riser'), (T1, 'impacto')]

luzes(chave=120, verde=130, quente=90)
kc = camera(lente=35, fstop=4.0)
CD = bpy.context.scene.camera.data
def lente(tt, l): CD.lens = l; CD.keyframe_insert('lens', frame=T(tt))
kc(0.0, (-0.7, -1.25, 0.75), (0.0, 0.05, 0.3)); lente(0.0, 35)          # conector inteiro + 94 Mb
kc(2.4, (-0.55, -1.3, 0.8), (0.05, 0.05, 0.3)); lente(2.4, 35)
kc(4.4, (0.6, -1.0, 0.62), (0.08, 0.1, 0.2)); lente(4.4, 42)          # par marrom curto (vermelho)
kc(8.6, (0.7, -0.9, 0.58), (0.08, 0.1, 0.2)); lente(8.6, 42)
kc(9.3, (0.0, -1.0, 0.75), (0.0, 0.1, 0.18)); lente(9.3, 40)            # correção: fios até o fim, capa entra
kc(12.4, (-0.45, -0.9, 0.7), (0.0, 0.1, 0.18)); lente(12.4, 40)
kc(14.2, (0.55, -1.25, 0.6), (0.9, 0.3, 0.14)); lente(14.2, 40)         # testador: 8 luzes verdes
kc(16.4, (0.75, -1.2, 0.55), (0.92, 0.3, 0.14)); lente(16.4, 40)
kc(16.8, (0.3, -2.3, 1.1), (0.4, 0.25, 0.35)); lente(16.8, 35)          # resultado: 500 MEGA
kc(DUR, (0.1, -2.15, 1.05), (0.4, 0.25, 0.37)); lente(DUR, 35)
finalizar(OUT)
