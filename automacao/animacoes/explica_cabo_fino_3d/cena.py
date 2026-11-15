# MOVE Explica 3D premium — Cabo de caixa fino demais em trecho longo
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib3d import *
OUT = os.path.dirname(os.path.abspath(__file__))
DUR = 21.5
sc = iniciar(DUR); materiais(); estudio(parede_y=3.2)

# ---------- amplificador (frente, à esquerda) e caixa longe (fundo, à direita) ----------
AMP = (-0.55, -1.0, 0.07)
amplificador('amp', AMP, esc=(0.3, 0.22, 0.07))
CX = (0.75, 2.2)
cone, _ = caixa('cx', CX[0], CX[1], rotz=math.radians(-12))
cone['y0'] = cone.location.y
# um vaso / banco para dar escala de "outro ambiente"
cube('banco', (-0.9, 2.1, 0.22), (0.5, 0.18, 0.22), M['madeira'], 0.01)

PTS = [(-0.45, -0.78, 0.012), (-0.2, 0.2, 0.012), (0.5, 0.6, 0.012), (0.2, 1.4, 0.012), (0.68, 1.95, 0.2)]
fino, _ = cabo('cabo_fino', PTS, M['verm'], esp=0.0035)
grosso, _ = cabo('cabo_grosso', [(x + 0.02, y, z + 0.004) for x, y, z in PTS], M['verm'], esp=0.011)
fino.data.use_path = True; grosso.data.use_path = True
T_TROCA = 12.4
visivel(fino, [(0, True), (T_TROCA, False)])
visivel(grosso, [(0, False), (T_TROCA, True)])
EV += [(T_TROCA, 'whoosh'), (T_TROCA + 0.1, 'clique')]

# ---------- pulsos de energia correndo no cabo ----------
def pulso(curva, t0, cor, perde):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.03, location=(0, 0, 0)); o = bpy.context.object
    m = mat('pulso', (0, 0, 0), emis=cor, es=0); o.data.materials.append(m)
    c = o.constraints.new('FOLLOW_PATH'); c.target = curva; c.use_fixed_location = True
    em = m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
    dur = 1.4
    for t, fct, e, s in ((t0 - 0.05, 0.0, 0, 0.01), (t0, 0.0, 30, 1.0), (t0 + dur, 1.0, 1.5 if perde else 30, 0.25 if perde else 1.0), (t0 + dur + 0.05, 1.0, 0, 0.01)):
        c.offset_factor = fct; c.keyframe_insert('offset_factor', frame=T(t))
        em.default_value = e; em.keyframe_insert('default_value', frame=T(t))
        o.scale = (s, s, s); o.keyframe_insert('scale', frame=T(t))
    return o
t = 0.3
while t < DUR - 1.6:
    if t < T_TROCA - 1.4: pulso(fino, t, VERM, True)
    elif t > T_TROCA + 0.3: pulso(grosso, t, VERDE, False)
    t += 0.55

# ---------- corte dos cabos (comparação) ----------
def corte(nome, x, r_ext, r_cu, cor_txt, rotulo):
    base = (x, -1.55, 0.3)
    a = cil(nome + 'iso', base, r_ext, 0.05, M['verm'])
    b = cil(nome + 'cu', (x, -1.55 - 0.006, 0.3), r_cu, 0.05, M['cobre'])
    tx, _ = texto(nome + 'tx', rotulo, (x, -1.6, 0.41), 0.032, cor_txt, es=8)
    for o in (a, b, tx): visivel(o, [(0, False), (8.2, True), (T_TROCA, False)])
corte('fino', -0.73, 0.022, 0.012, VERM, '0,5 mm²')
corte('grosso', -0.43, 0.045, 0.029, VERDE, '2,5 mm²')
EV += [(8.2, 'whoosh'), (8.4, 'erro'), (T_TROCA + 1.6, 'ding')]

# ---------- caixa: fraca × forte ----------
cones([cone], DUR, lambda i, t: 0.003 if t < T_TROCA + 1.5 else 0.013)
t = 1.7
while t < DUR - 1.2:
    loc = (CX[0] - 0.04, CX[1] - 0.2, 0.5)
    if t < T_TROCA: anel(loc, t, VERM, False, rot=(math.pi / 2, 0, math.radians(-12)), alcance=1.4); t += 0.55
    elif t < T_TROCA + 1.5: t += 0.45
    else: anel(loc, t, VERDE, True, rot=(math.pi / 2, 0, math.radians(-12)), alcance=3.2); t += 0.45

luzes()
kc = camera(lente=34)
kc(0.0, (0.15, -0.3, 0.22), (-0.42, -0.72, 0.04))        # close: cabo fininho saindo do amplificador
kc(3.0, (0.25, -0.1, 0.35), (-0.25, -0.4, 0.05))
kc(3.9, (-0.1, -3.6, 1.6), (0.15, 0.7, 0.35))            # geral: o caminho longo até a caixa
kc(7.6, (0.25, -3.4, 1.5), (0.2, 0.8, 0.4))
kc(8.4, (-0.58, -2.8, 0.36), (-0.58, -1.58, 0.33))      # corte dos cabos
kc(11.9, (-0.56, -2.7, 0.37), (-0.58, -1.58, 0.33))
kc(13.0, (-0.1, -3.5, 1.55), (0.15, 0.75, 0.38))         # cabo novo, potência chegando
kc(16.0, (0.55, 0.9, 0.65), (0.75, 2.05, 0.5))           # chega na caixa
kc(DUR, (0.35, 0.6, 0.75), (0.72, 2.05, 0.55))
finalizar(OUT)
