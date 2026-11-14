# MOVE Explica 3D premium — Polaridade invertida (o grave some)
# uso: python3 cena.py test:30,120,250   |  python3 cena.py a:b   |  python3 cena.py save
import bpy, math, os, sys, json
OUT = os.path.dirname(os.path.abspath(__file__))
FPS = 24; DUR = 21.5; NF = int(DUR * FPS)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.fps = FPS; sc.frame_start = 1; sc.frame_end = NF
EV = []
def T(s): return int(s * FPS) + 1

def mat(nome, cor, rough=0.4, metal=0.0, emis=None, es=0.0, alpha=1.0, clearcoat=0.0):
    m = bpy.data.materials.new(nome); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*cor, 1); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if clearcoat: b.inputs['Coat Weight'].default_value = clearcoat
    if emis: b.inputs['Emission Color'].default_value = (*emis, 1); b.inputs['Emission Strength'].default_value = es
    if alpha < 1: b.inputs['Alpha'].default_value = alpha
    return m

def obj(o, m): o.data.materials.append(m); return o
def cube(nome, loc, esc, m, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc); o = bpy.context.object; o.name = nome; o.scale = esc
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        md = o.modifiers.new('b', 'BEVEL'); md.width = bevel; md.segments = 4
    bpy.ops.object.shade_smooth(); return obj(o, m)
def cil(nome, loc, r, d, m, rot=(math.pi/2, 0, 0), v=64):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d, location=loc, rotation=rot); o = bpy.context.object; o.name = nome
    bpy.ops.object.shade_smooth(); return obj(o, m)

# ---------- materiais ----------
M_piso = mat('piso', (0.012, 0.014, 0.014), 0.18, clearcoat=0.6)
M_parede = mat('parede', (0.02, 0.022, 0.022), 0.7)
M_madeira = mat('nogueira', (0.16, 0.075, 0.035), 0.35, clearcoat=0.5)
M_frente = mat('frente', (0.008, 0.008, 0.009), 0.45)
M_cone = mat('cone', (0.03, 0.03, 0.032), 0.55)
M_aro = mat('aro', (0.6, 0.6, 0.62), 0.25, metal=1.0)
M_tw = mat('tweeter', (0.75, 0.72, 0.66), 0.2, metal=1.0)
M_verm = mat('vermelho', (0.55, 0.02, 0.02), 0.3, clearcoat=0.4)
M_preto = mat('preto', (0.015, 0.015, 0.015), 0.3, clearcoat=0.4)
M_ouro = mat('ouro', (0.9, 0.62, 0.25), 0.2, metal=1.0)
VERDE = (0.27, 0.85, 0.65); VERM = (1.0, 0.2, 0.17)

# ---------- ambiente ----------
bpy.ops.mesh.primitive_plane_add(size=30); obj(bpy.context.object, M_piso)
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 4, 0), rotation=(math.pi/2, 0, 0)); obj(bpy.context.object, M_parede)
# faixa de luz na parede (sanca)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 3.95, 2.6), rotation=(math.pi/2, 0, 0))
f = bpy.context.object; f.scale = (6, 0.03, 1); obj(f, mat('sanca', (0, 0, 0), emis=(1.0, 0.78, 0.5), es=6))

# ---------- caixas ----------
CONES = []; CX = 0.56
for lado, x in (('E', -CX), ('D', CX)):
    cube(f'gab{lado}', (x, 0, 0.62), (0.2, 0.17, 0.33), M_madeira, 0.02)
    cube(f'fr{lado}', (x, -0.171, 0.62), (0.185, 0.005, 0.315), M_frente, 0.006)
    cil(f'aroW{lado}', (x, -0.18, 0.5), 0.135, 0.012, M_aro)
    c = cil(f'cone{lado}', (x, -0.182, 0.5), 0.118, 0.01, M_cone)
    d = cil(f'cap{lado}', (x, -0.19, 0.5), 0.04, 0.01, M_aro); d.parent = c; d.location = (0, 0, 0); d.matrix_parent_inverse = c.matrix_world.inverted()
    cil(f'aroT{lado}', (x, -0.18, 0.82), 0.05, 0.012, M_aro)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.03, location=(x, -0.18, 0.82)); s = bpy.context.object; s.scale = (1, 0.45, 1); bpy.ops.object.shade_smooth(); obj(s, M_tw)
    cube(f'base{lado}', (x, 0, 0.14), (0.16, 0.14, 0.14), M_frente, 0.01)  # pedestal
    CONES.append(c)
    # bornes na frente do pedestal
    for k, (dx, m) in enumerate(((-0.05, M_verm), (0.05, M_preto))):
        cil(f'borne{lado}{k}', (x + dx, -0.145, 0.16), 0.018, 0.04, m)

# ---------- cabos (do amplificador no chão, à frente) ----------
cube('amp', (0, -0.75, 0.06), (0.32, 0.22, 0.06), mat('amp', (0.06, 0.06, 0.065), 0.3, metal=0.8), 0.01)
cube('amp_luz', (0, -0.972, 0.07), (0.25, 0.002, 0.006), mat('ampled', (0, 0, 0), emis=VERDE, es=8), 0)
def cabo(nome, pts, m, esp=0.008):
    cu = bpy.data.curves.new(nome, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = esp; cu.bevel_resolution = 6
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(pts) - 1)
    for p, co in zip(sp.bezier_points, pts):
        p.co = co; p.handle_left_type = p.handle_right_type = 'AUTO'
    o = bpy.data.objects.new(nome, cu); bpy.context.collection.objects.link(o); o.data.materials.append(m); return o, sp
CAB = {}
for lado, x in (('E', -CX), ('D', CX)):
    for k, (dx, m) in enumerate(((-0.05, M_verm), (0.05, M_preto))):
        sx = (-0.12 if lado == 'E' else 0.12) + dx * 0.6
        o, sp = cabo(f'cabo{lado}{k}', [(sx, -0.53, 0.07), (sx + (x - sx) * 0.4, -0.38, 0.02), (x + dx, -0.19, 0.16)], m)
        CAB[(lado, k)] = sp

# Caixa D começa INVERTIDA: o cabo vermelho vai no borne preto e vice-versa
pD0, pD1 = CAB[('D', 0)].bezier_points[-1], CAB[('D', 1)].bezier_points[-1]
certo0, certo1 = tuple(pD0.co), tuple(pD1.co)
def ponta(p, co, f):
    p.co = co; p.keyframe_insert('co', frame=f)
ponta(pD0, certo1, 1); ponta(pD1, certo0, 1)
t_troca = 12.4
ponta(pD0, certo1, T(t_troca)); ponta(pD1, certo0, T(t_troca))
# levanta e cruza
up = lambda c, dz: (c[0], c[1] - 0.06, c[2] + dz)
ponta(pD0, up(((certo0[0] + certo1[0]) / 2, certo0[1], certo0[2]), 0.12), T(t_troca + 0.5))
ponta(pD1, up(((certo0[0] + certo1[0]) / 2, certo0[1], certo0[2]), 0.08), T(t_troca + 0.5))
ponta(pD0, certo0, T(t_troca + 1.0)); ponta(pD1, certo1, T(t_troca + 1.1))
EV += [(t_troca + 1.0, 'clique'), (t_troca + 1.1, 'clique')]

# ---------- movimento dos cones ----------
FASE_OK = 13.6  # a partir daqui as duas caixas em fase
for f in range(1, NF + 1):
    t = (f - 1) / FPS
    amp = 0.012 * min(1, t / 0.4)
    s = math.sin(2 * math.pi * 2.2 * t)
    for i, c in enumerate(CONES):
        sinal = 1 if (i == 0 or t >= FASE_OK) else -1
        c.location.y = -0.182 - amp * s * sinal; c.keyframe_insert('location', index=1, frame=f)

# ---------- anéis de som (pulsos) ----------
def anel(x, t0, cor, forte):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.13, minor_radius=0.004, location=(x, -0.2, 0.5), rotation=(math.pi/2, 0, 0))
    o = bpy.context.object
    m = mat('anel', (0, 0, 0), emis=cor, es=0); o.data.materials.append(m)
    em = m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
    f0 = T(t0); f1 = T(t0 + 1.3)
    for f, sc_, e in ((max(1, f0 - 1), 0.01, 0), (f0, 1.0, 14 if forte else 9), (f1, 3.6 if forte else 2.6, 0), (f1 + 1, 0.0, 0)):
        o.scale = (sc_, sc_, sc_); o.keyframe_insert('scale', frame=f); em.default_value = e; em.keyframe_insert('default_value', frame=f)
t = 0.6
while t < DUR - 1.2:
    errado = t < FASE_OK
    if 1.5 < t < 3.0 or 12.0 < t < 13.6:
        t += 0.45; continue
    cor = VERM if errado else VERDE
    for x in (-CX, CX): anel(x, t, cor, not errado)
    t += 0.45

# ---------- linha do grave (soma das ondas) entre as caixas ----------
N = 90
me = bpy.data.meshes.new('ondaM'); vs = [((-0.42 + 0.84 * i / (N - 1)), 0, math.sin(i / (N - 1) * 4 * math.pi) * 0.09) for i in range(N)]
me.from_pydata(vs, [(i, i + 1) for i in range(N - 1)], []); onda = bpy.data.objects.new('onda', me); bpy.context.collection.objects.link(onda)
onda.location = (0, -0.25, 1.12)
md = onda.modifiers.new('sk', 'SKIN')
for v in onda.data.skin_vertices[0].data: v.radius = (0.006, 0.006)
onda.modifiers.new('ss', 'SUBSURF').levels = 1
M_onda = mat('onda', (0, 0, 0), emis=VERM, es=10); onda.data.materials.append(M_onda)
ec = M_onda.node_tree.nodes['Principled BSDF'].inputs['Emission Color']
def k_onda(tt, z, cor):
    onda.scale = (1, 1, z); onda.keyframe_insert('scale', index=2, frame=T(tt)); ec.default_value = (*cor, 1); ec.keyframe_insert('default_value', frame=T(tt))
k_onda(0, 0.01, VERM); k_onda(3.0, 0.01, VERM); k_onda(4.0, 1.0, VERM); k_onda(6.8, 1.0, VERM); k_onda(8.2, 0.04, VERM); k_onda(12.0, 0.04, VERM)
k_onda(13.4, 0.04, VERDE); k_onda(14.6, 1.6, VERDE); k_onda(DUR, 1.6, VERDE)
EV += [(8.0, 'erro'), (14.4, 'ding'), (0.3, 'batida'), (3.2, 'whoosh'), (12.2, 'whoosh')]

# ---------- luzes ----------
def area(loc, rot, en, cor, tam):
    l = bpy.data.lights.new('a', 'AREA'); l.energy = en; l.color = cor; l.size = tam
    o = bpy.data.objects.new('a', l); o.location = loc; o.rotation_euler = rot; bpy.context.collection.objects.link(o); return l
area((-1.6, -1.8, 2.2), (math.radians(55), 0, math.radians(-40)), 260, (1, 0.93, 0.85), 1.6)
area((1.8, 1.2, 1.4), (math.radians(70), 0, math.radians(130)), 140, VERDE, 1.0)
area((-1.8, 1.4, 1.2), (math.radians(70), 0, math.radians(-130)), 90, (1, 0.7, 0.45), 1.0)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.02

# ---------- câmera ----------
cd = bpy.data.cameras.new('cam'); cd.lens = 38; cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.2
cam = bpy.data.objects.new('cam', cd); bpy.context.collection.objects.link(cam); sc.camera = cam
alvo = bpy.data.objects.new('alvo', None); bpy.context.collection.objects.link(alvo)
tc = cam.constraints.new('TRACK_TO'); tc.target = alvo; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'
cd.dof.focus_object = alvo
def kc(tt, pos, alv):
    cam.location = pos; cam.keyframe_insert('location', frame=T(tt)); alvo.location = alv; alvo.keyframe_insert('location', frame=T(tt))
kc(0.0, (0.75, -0.95, 0.55), (CX, -0.18, 0.5))        # gancho: close no woofer
kc(2.6, (0.45, -1.35, 0.7), (CX * 0.6, -0.18, 0.55))
kc(4.0, (0, -3.3, 1.05), (0, 0, 0.62))               # plano geral, as duas
kc(11.4, (0.15, -3.1, 1.08), (0, 0, 0.62))
kc(12.4, (CX + 0.22, -0.62, 0.26), (CX, -0.15, 0.17))      # close nos bornes
kc(13.8, (CX + 0.18, -0.6, 0.27), (CX, -0.15, 0.17))
kc(15.2, (-0.1, -3.2, 1.08), (0, 0, 0.64))              # geral de novo, em fase
kc(DUR, (0.1, -2.8, 1.0), (0, 0, 0.66))
for fc in cam.animation_data.action.fcurves if cam.animation_data and hasattr(cam.animation_data.action, 'fcurves') else []:
    for k in fc.keyframe_points: k.interpolation = 'BEZIER'

# ---------- render ----------
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = int(os.environ.get('SAMPLES', 12)); sc.cycles.use_denoising = True
sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.transmission_bounces = 0
sc.render.resolution_x = int(os.environ.get('LARG', 540)); sc.render.resolution_y = int(os.environ.get('ALT', 960))
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 94
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
json.dump(sorted(EV), open(os.path.join(OUT, 'events.json'), 'w'))
modo = sys.argv[-1]
if modo == 'save':
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'cena.blend')); sys.exit(0)
if modo.startswith('test'):
    for f in [int(x) for x in modo.split(':')[1].split(',')]:
        sc.frame_set(f); sc.render.filepath = os.path.join(OUT, f'test_{f:04d}.jpg'); bpy.ops.render.render(write_still=True)
else:
    a, b = [int(x) for x in modo.split(':')]; os.makedirs(os.path.join(OUT, 'frames'), exist_ok=True)
    for f in range(a, b + 1, int(os.environ.get('STEP', 1))):
        p = os.path.join(OUT, 'frames', f'{f:04d}.jpg')
        if os.path.exists(p): continue
        sc.frame_set(f); sc.render.filepath = p; bpy.ops.render.render(write_still=True)
