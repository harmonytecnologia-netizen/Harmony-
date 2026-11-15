# MOVE Explica 3D premium / Gato por lebre — "60 W" para 4 caixas = 15 W em cada
# uso: blender-python: python3 cena.py test:30,120,250 | python3 cena.py a:b
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib3d import *
import lib3d
OUT = os.path.dirname(os.path.abspath(__file__))
DUR = 21.5
sc = iniciar(DUR); materiais(); estudio()

# ---------- 4 caixas: 2 por canal ----------
POS = [(-0.45, 0.0), (-1.05, 0.75), (0.45, 0.0), (1.05, 0.75)]   # E1, E2, D1, D2
CONES = []
for i, (x, y) in enumerate(POS):
    c, v = caixa(f'cx{i}', x, y); CONES.append(c)

# ---------- amplificadores ----------
AMP_Y = -0.85
amp1 = amplificador('amp60', (0, AMP_Y, 0.07), esc=(0.34, 0.24, 0.07), led=QUENTE)
t60, m60 = texto('lbl60', '60 W', (0.03, AMP_Y - 0.245, 0.07), 0.05, (1, 0.9, 0.75), es=5)
t60.parent = amp1; t60.matrix_parent_inverse = amp1.matrix_world.inverted()
amp2 = amplificador('amp100', (0, AMP_Y + 0.02, 0.05), esc=(0.2, 0.17, 0.045), led=VERDE, botoes=False)
t100, m100 = texto('lbl100', 'CLASSE D', (-0.04, AMP_Y + 0.02 - 0.175, 0.055), 0.03, VERDE, es=6)
t100.parent = amp2; t100.matrix_parent_inverse = amp2.matrix_world.inverted()
T_TROCA = 12.5
for o, ks in ((amp1, ((0, 1), (T_TROCA, 1), (T_TROCA + 0.45, 0.001))), (amp2, ((0, 0.001), (T_TROCA + 0.3, 0.001), (T_TROCA + 0.8, 1.08), (T_TROCA + 1.0, 1.0)))):
    for t, s in ks:
        o.scale = (s, s, s); o.keyframe_insert('scale', frame=T(t))
EV += [(T_TROCA, 'whoosh'), (T_TROCA + 0.8, 'clique')]

# ---------- cabos: cada canal vai em 2 caixas ----------
for i, (x, y) in enumerate(POS):
    lado = -1 if x < 0 else 1
    for k, (dx, m) in enumerate(((-0.05, M['verm']), (0.05, M['preto']))):
        sx = lado * 0.12 + dx * 0.5
        cabo(f'cabo{i}{k}', [(sx, AMP_Y + 0.2, 0.03), (sx + (x - sx) * 0.45, (AMP_Y + y) / 2 - 0.1, 0.012), (x + dx, y - 0.19, 0.21)], m)

# ---------- números flutuando ----------
n60, mn60 = texto('n60', '60 W', (0, 0.35, 1.6), 0.24, (1, 0.92, 0.8), es=7)
visivel(n60, [(0, False), (3.7, True), (6.0, False)])
n30 = []
for lado in (-1, 1):
    o, m = texto(f'n30{lado}', '30 W', (lado * 0.75, 0.35, 1.32), 0.17, (1, 0.92, 0.8), es=7); n30.append(o)
    visivel(o, [(0, False), (5.6, True), (8.4, False)])
n15 = []
for i, (x, y) in enumerate(POS):
    o, m = texto(f'n15{i}', '15 W', (x, y - 0.1, 1.22), 0.12, VERM, es=10); n15.append(o)
    visivel(o, [(0, False), (8.3, True), (T_TROCA, False)])
EV += [(3.7, 'batida'), (5.6, 'batida'), (8.3, 'erro')]
EV += [(T_TROCA + 1.0, 'ding')]

# ---------- cones e anéis ----------
for c in CONES: c['y0'] = c.location.y
FORTE = T_TROCA + 1.4
cones(CONES, DUR, lambda i, t: (0.004 * min(1, t / 0.4)) if t < FORTE else 0.013)
t = 0.5
while t < DUR - 1.2:
    if t < T_TROCA:
        if t > 1.2:
            for (x, y) in POS: anel((x, y - 0.2, 0.5), t, VERM, False, alcance=1.5)
        t += 0.9
    elif t < FORTE:
        t += 0.45
    else:
        for (x, y) in POS: anel((x, y - 0.2, 0.5), t, VERDE, True, alcance=2.6)
        t += 0.45
EV += [(0.2, 'batida')]

luzes()
kc = camera(lente=36)
kc(0.0, (0.14, AMP_Y - 0.62, 0.17), (0.02, AMP_Y - 0.24, 0.075))       # close no "60 W"
kc(3.0, (0.08, AMP_Y - 0.8, 0.26), (0, AMP_Y - 0.2, 0.09))
kc(3.9, (0.0, -4.1, 1.35), (0, 0.15, 0.62))                           # plano geral
kc(11.6, (0.35, -3.9, 1.3), (0, 0.15, 0.62))
kc(12.6, (-0.35, AMP_Y - 0.75, 0.32), (0, AMP_Y, 0.08))               # troca do amplificador
kc(14.6, (-0.25, AMP_Y - 0.85, 0.36), (0, AMP_Y, 0.1))
kc(15.8, (-0.2, -4.0, 1.35), (0, 0.15, 0.64))                         # geral, som forte
kc(DUR, (0.15, -3.5, 1.22), (0, 0.15, 0.66))
finalizar(OUT)
