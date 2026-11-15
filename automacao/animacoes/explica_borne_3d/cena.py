# MOVE Explica 3D premium — Fio solto no borne: curto e amplificador em proteção
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib3d import *
OUT = os.path.dirname(os.path.abspath(__file__))
DUR = 21.5
sc = iniciar(DUR); materiais(); estudio(parede_y=3.0)

# amplificador de costas para a câmera (painel traseiro com bornes)
AZ = 0.34
cube('apoio', (0, 0.0, 0.135), (0.42, 0.3, 0.135), M['madeira'], 0.01)
cube('amp', (0, 0.0, AZ), (0.34, 0.24, 0.07), M['alu'], 0.01)
cube('painel_tras', (0, -0.241, AZ), (0.33, 0.002, 0.065), mat('painel', (0.012, 0.012, 0.013), 0.5), 0)
# aletas de dissipação em cima
for k in range(9):
    cube(f'aleta{k}', (-0.24 + k * 0.06, 0.02, AZ + 0.075), (0.008, 0.2, 0.008), M['alu_claro'])
# LED de status (verde -> vermelho em proteção -> verde)
led_m = mat('led', (0, 0, 0), emis=VERDE, es=5)
cil('led', (0.25, -0.245, AZ + 0.035), 0.008, 0.006, led_m)
T_CURTO = 7.4; T_FIX = 12.4
cor_k(led_m, [(0, VERDE), (T_CURTO, VERDE), (T_CURTO + 0.05, VERM), (T_FIX + 1.2, VERM), (T_FIX + 1.25, VERDE)])
tp, mp = texto('protect', 'PROTEÇÃO', (0.13, -0.25, AZ + 0.115), 0.03, VERM, es=4)
visivel(tp, [(0, False), (T_CURTO + 0.6, True), (T_FIX + 1.2, False)])

# bornes: canal E (x<0) e canal D (x>0)
BZ = AZ - 0.015
BOR = {}
for lado, x0 in (('E', -0.17), ('D', 0.05)):
    for k, (dx, m) in enumerate(((0.0, M['verm']), (0.075, M['preto']))):
        x = x0 + dx
        cil(f'b{lado}{k}', (x, -0.262, BZ), 0.02, 0.04, m)
        cil(f'bp{lado}{k}', (x, -0.284, BZ), 0.009, 0.012, M['ouro'])
        BOR[(lado, k)] = (x, -0.29, BZ)

# cabos saindo dos bornes e descendo
for (lado, k), (x, y, z) in BOR.items():
    m = M['verm'] if k == 0 else M['preto']
    s = -1 if lado == 'E' else 1
    cabo(f'c{lado}{k}', [(x, y - 0.005, z - 0.01), (x + s * 0.05, y - 0.12, z - 0.12), (x + s * 0.35, y - 0.25, 0.01), (s * 1.6, y + 0.4, 0.01)], m, esp=0.006)

# fios soltos (fiapos de cobre) do + esquerdo encostando no − esquerdo
xr, yr, zr = BOR[('E', 0)]; xb = BOR[('E', 1)][0]
fio_m = mat('fiapo', (0.85, 0.42, 0.22), 0.25, metal=1.0, emis=(1.0, 0.55, 0.25), es=0)
FIAPOS = []
for j, (dz, alt) in enumerate(((-0.004, 0.012), (0.0, 0.02), (0.005, 0.016))):
    o, _ = cabo(f'fiapo{j}', [(xr + 0.01, yr - 0.004, zr + dz), ((xr + xb) / 2, yr - 0.012 - j * 0.003, zr + alt), (xb - 0.012 + j * 0.004, yr + 0.004, zr + dz * 0.5)], fio_m, esp=0.0011)
    o.data.materials.clear(); o.data.materials.append(fio_m); FIAPOS.append(o)
    visivel(o, [(0, True), (T_FIX, False)])
# ponta bem feita (torcida e apertada) + pino banana dourado, aparecem na correção
pt = cil('ponta_ok', (xr, yr - 0.006, zr), 0.0065, 0.016, M['cobre'], rot=(math.pi / 2, 0, 0))
visivel(pt, [(0, False), (T_FIX + 0.2, True)])
# faíscas
for tc in (1.1, 2.3, 5.2, T_CURTO):
    emis_k(fio_m, [(tc - 0.08, 0), (tc, 60), (tc + 0.12, 0)])
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.012, location=((xr + xb) / 2, yr - 0.015, zr + 0.012)); f = bpy.context.object
    fm = mat('faisca', (0, 0, 0), emis=(1.0, 0.8, 0.5), es=0); f.data.materials.append(fm)
    for t, s, e in ((tc - 0.1, 0.0, 0), (tc - 0.06, 0.01, 0), (tc, 1.0, 80), (tc + 0.15, 2.2, 0), (tc + 0.2, 0.0, 0)):
        f.scale = (s, s, s); f.keyframe_insert('scale', frame=T(t)); emis_k(fm, [(t, e)])
    EV.append((tc, 'clique'))
EV += [(T_CURTO + 0.1, 'erro'), (T_FIX, 'whoosh'), (T_FIX + 1.25, 'ding')]

# caixas ao fundo: tocam, param na proteção, voltam
CONES = []
for i, x in enumerate((-1.15, 1.15)):
    c, _ = caixa(f'cx{i}', x, 1.6, rotz=math.radians(15 if x < 0 else -15)); c['y0'] = c.location.y; CONES.append(c)
cones(CONES, DUR, lambda i, t: 0.009 if t < T_CURTO else (0.0 if t < T_FIX + 1.3 else 0.012))
t = 0.6
while t < DUR - 1.2:
    if t < T_CURTO - 0.3 or t > T_FIX + 1.4:
        for i, x in enumerate((-1.15, 1.15)):
            anel((x, 1.4, 0.5), t, VERDE, t > T_FIX, rot=(math.pi / 2, 0, math.radians(15 if x < 0 else -15)), alcance=3.0)
    t += 0.5

luzes()
kc = camera(lente=40, fstop=2.8)
kc(0.0, (-0.06, -0.62, BZ + 0.1), ((xr + xb) / 2, -0.27, BZ))         # macro: fiapos entre os bornes
kc(3.2, (-0.02, -0.7, BZ + 0.14), ((xr + xb) / 2, -0.27, BZ))
kc(4.0, (0.55, -1.5, 0.75), (0.0, -0.15, 0.36))                       # amplificador + caixas
kc(6.9, (0.45, -1.35, 0.7), (-0.05, -0.2, 0.35))
kc(7.6, (0.12, -1.0, 0.52), (0.14, -0.25, BZ + 0.06))                 # LED de proteção
kc(11.8, (0.16, -0.95, 0.52), (0.14, -0.25, BZ + 0.06))
kc(12.6, (-0.1, -0.6, BZ + 0.1), (xr, -0.28, BZ))                     # correção no borne
kc(14.6, (-0.05, -0.65, BZ + 0.12), (xr, -0.28, BZ))
kc(16.0, (0.2, -3.4, 1.25), (0, 0.6, 0.45))                           # geral, tocando de novo
kc(DUR, (-0.15, -3.1, 1.15), (0, 0.6, 0.45))
finalizar(OUT)
