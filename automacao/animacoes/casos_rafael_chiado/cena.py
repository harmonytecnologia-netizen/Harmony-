# Casos da MOVE — Rafael: som chiando (cabo de áudio junto da energia no mesmo eletroduto)
# uso: python3.11 cena.py test:30,120  |  python3.11 cena.py a:b  (STEP=2 renderiza quadros pares)
import bpy, math, os, sys, json, random
OUT = os.path.dirname(os.path.abspath(__file__))
FPS = 24; DUR = 22.0; NF = int(DUR * FPS)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.fps = FPS; sc.frame_start = 1; sc.frame_end = NF
EV = []
def T(s): return int(s * FPS) + 1
random.seed(7)

def mat(nome, cor, rough=0.4, metal=0.0, emis=None, es=0.0, alpha=1.0, clearcoat=0.0, trans=0.0):
    m = bpy.data.materials.new(nome); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*cor, 1); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if clearcoat: b.inputs['Coat Weight'].default_value = clearcoat
    if emis: b.inputs['Emission Color'].default_value = (*emis, 1); b.inputs['Emission Strength'].default_value = es
    if alpha < 1: b.inputs['Alpha'].default_value = alpha
    if trans: b.inputs['Transmission Weight'].default_value = trans
    return m
def obj(o, m): o.data.materials.append(m); return o
def cube(nome, loc, esc, m, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc); o = bpy.context.object; o.name = nome; o.scale = esc
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        md = o.modifiers.new('b', 'BEVEL'); md.width = bevel; md.segments = 4
    bpy.ops.object.shade_smooth(); return obj(o, m)
def cil(nome, loc, r, d, m, rot=(math.pi/2, 0, 0), v=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d, location=loc, rotation=rot); o = bpy.context.object; o.name = nome
    bpy.ops.object.shade_smooth(); return obj(o, m)

VERDE = (0.27, 0.85, 0.65); VERM = (1.0, 0.06, 0.04)
M_piso = mat('piso', (0.012, 0.014, 0.014), 0.18, clearcoat=0.6)
M_parede = mat('parede', (0.012, 0.013, 0.013), 0.75)
M_gesso = mat('gesso', (0.3, 0.29, 0.27), 0.85)
M_madeira = mat('nogueira', (0.16, 0.075, 0.035), 0.35, clearcoat=0.5)
M_frente = mat('frente', (0.008, 0.008, 0.009), 0.45)
M_cone = mat('cone', (0.03, 0.03, 0.032), 0.55)
M_aro = mat('aro', (0.6, 0.6, 0.62), 0.25, metal=1.0)
M_tw = mat('tweeter', (0.75, 0.72, 0.66), 0.2, metal=1.0)
M_ouro = mat('ouro', (0.9, 0.62, 0.25), 0.2, metal=1.0)
M_tubo1 = mat('eletroduto1', (0.85, 0.42, 0.08), 0.35, alpha=0.32)   # corrugado laranja (energia)
M_tubo2 = mat('eletroduto2', (0.55, 0.58, 0.6), 0.35, alpha=0.30)    # cinza (só sinal)
M_fase = mat('fase', (0.02, 0.02, 0.02), 0.35, clearcoat=0.3)
M_neutro = mat('neutro', (0.03, 0.12, 0.55), 0.35, clearcoat=0.3)
M_audio = mat('audio', (0.5, 0.52, 0.55), 0.3, clearcoat=0.4)

# ---------- ambiente ----------
bpy.ops.mesh.primitive_plane_add(size=30); obj(bpy.context.object, M_piso)
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0.35, 0), rotation=(math.pi/2, 0, 0)); obj(bpy.context.object, M_parede)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0.33, 2.15), rotation=(math.pi/2, 0, 0))
f = bpy.context.object; f.scale = (6, 0.03, 1); obj(f, mat('sanca', (0, 0, 0), emis=(1.0, 0.78, 0.5), es=6))

# ---------- eletrodutos na parede (corte) ----------
Z1, Z2 = 1.42, 1.18; X0, X1 = -0.9, 0.9
def tubo(nome, z, m):
    o = cil(nome, (0, 0.18, z), 0.055, X1 - X0, m, rot=(0, math.pi/2, 0), v=40)
    # anéis do corrugado
    for i in range(36):
        x = X0 + 0.03 + i * (X1 - X0 - 0.06) / 35
        bpy.ops.mesh.primitive_torus_add(major_radius=0.056, minor_radius=0.006, location=(x, 0.18, z), rotation=(0, math.pi/2, 0))
        obj(bpy.context.object, m)
    return o
tubo('tubo_energia', Z1, M_tubo1)
tubo2 = tubo('tubo_sinal', Z2, M_tubo2)
# caixinhas 4x2 nas pontas
for x in (X0 - 0.06, X1 + 0.06):
    for z in (Z1, Z2): cube('cx', (x, 0.2, z), (0.06, 0.05, 0.09), M_frente, 0.006)

def cabo(nome, pts, m, esp=0.012):
    cu = bpy.data.curves.new(nome, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = esp; cu.bevel_resolution = 5
    sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
    for p, co in zip(sp.points, pts):
        p.co = (*co, 1)
    o = bpy.data.objects.new(nome, cu); bpy.context.collection.objects.link(o); o.data.materials.append(m); return o, sp
NP = 31
xs = [X0 + (X1 - X0) * i / (NP - 1) for i in range(NP)]
cabo('fase', [(x, 0.18, Z1 + 0.022) for x in xs], M_fase, 0.014)
cabo('neutro', [(x, 0.195, Z1 - 0.02) for x in xs], M_neutro, 0.014)
_, AUD = cabo('audio', [(x, 0.16, Z1 - 0.005) for x in xs], M_audio, 0.008)
# plugue RCA dourado na ponta direita do cabo de áudio
rca = cil('rca', (X1 + 0.02, 0.16, Z1 - 0.005), 0.012, 0.06, M_ouro, rot=(0, math.pi/2, 0))

# cabo de áudio muda de eletroduto: sobe, sai e desce para o tubo de baixo
TM0, TM1 = 12.7, 14.3
for i, p in enumerate(AUD.points):
    x = xs[i]; a = (x, 0.16, Z1 - 0.005); b = (x, 0.16, Z2)
    atraso = 0.016 * i
    p.co = (*a, 1); p.keyframe_insert('co', frame=T(TM0 + atraso))
    p.co = (x, 0.02, (Z1 + Z2) / 2 + 0.05, 1); p.keyframe_insert('co', frame=T(TM0 + 0.55 + atraso))
    p.co = (*b, 1); p.keyframe_insert('co', frame=T(TM1 - 0.4 + atraso))
for (fr, z) in ((T(TM0), Z1 - 0.005), (T(TM0 + 0.55 + 0.48), (Z1 + Z2) / 2 + 0.05), (T(TM1 + 0.08), Z2)):
    rca.location = (X1 + 0.02, 0.16 if z != (Z1 + Z2) / 2 + 0.05 else 0.02, z); rca.keyframe_insert('location', frame=fr)
EV += [(TM0, 'whoosh'), (TM1 + 0.1, 'clique'), (TM1 + 0.25, 'clique'), (TM1 + 0.6, 'ding')]

# ---------- placa de gesso cobrindo os tubos (abre aos 8 s) ----------
gesso = cube('gesso', (0, 0.07, 1.3), (1.05, 0.02, 0.32), M_gesso, 0.004)
T_ABRE = 8.0
gesso.keyframe_insert('location', frame=T(T_ABRE))
gesso.location = (0, -0.25, 2.6); gesso.rotation_euler = (math.radians(-35), 0, 0)
gesso.keyframe_insert('location', frame=T(T_ABRE + 0.9)); gesso.keyframe_insert('rotation_euler', frame=T(T_ABRE + 0.9))
gesso.rotation_euler = (0, 0, 0); gesso.keyframe_insert('rotation_euler', frame=T(T_ABRE))
gesso.location = (0, -0.3, 4.0); gesso.keyframe_insert('location', frame=T(T_ABRE + 1.6))
EV += [(T_ABRE, 'whoosh')]

# ---------- interferência: arcos vermelhos entre energia e áudio ----------
def arco(x0, t0, t1):
    n = 7; vs = [(x0 + random.uniform(-0.02, 0.02), 0.17, Z1 + 0.02 - 0.05 * k / (n - 1)) for k in range(n)]
    me = bpy.data.meshes.new('arcoM'); me.from_pydata(vs, [(k, k + 1) for k in range(n - 1)], [])
    o = bpy.data.objects.new('arco', me); bpy.context.collection.objects.link(o)
    o.modifiers.new('sk', 'SKIN')
    for v in o.data.skin_vertices[0].data: v.radius = (0.0045, 0.0045)
    m = mat('arcoM', (0, 0, 0), emis=VERM, es=0); o.data.materials.append(m)
    em = m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
    f = T(t0)
    while f < T(t1):
        em.default_value = random.choice((0, 6, 12, 20)); em.keyframe_insert('default_value', frame=f); f += 2
    em.default_value = 0; em.keyframe_insert('default_value', frame=T(t1))
    for fc in m.node_tree.animation_data.action.fcurves if hasattr(m.node_tree.animation_data.action, 'fcurves') else []:
        for k in fc.keyframe_points: k.interpolation = 'CONSTANT'
for x in [X0 + 0.1 + i * 0.075 for i in range(22)]:
    arco(x, 0.0, TM0)

# ---------- caixa de som (embaixo) ----------
CX, CZ = 0.0, 0.42
cube('gab', (CX, -0.05, CZ), (0.2, 0.17, 0.33), M_madeira, 0.02)
cube('fr', (CX, -0.221, CZ), (0.185, 0.005, 0.315), M_frente, 0.006)
cil('aroW', (CX, -0.23, CZ - 0.12), 0.135, 0.012, M_aro)
cone = cil('cone', (CX, -0.232, CZ - 0.12), 0.118, 0.01, M_cone)
cil('aroT', (CX, -0.23, CZ + 0.2), 0.05, 0.012, M_aro)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.03, location=(CX, -0.23, CZ + 0.2)); s = bpy.context.object; s.scale = (1, 0.45, 1); bpy.ops.object.shade_smooth(); obj(s, M_tw)
cube('ped', (CX, -0.05, 0.045), (0.16, 0.14, 0.045), M_frente, 0.01)
# amplificador ao lado
cube('amp', (0.62, -0.05, 0.07), (0.3, 0.2, 0.07), mat('ampm', (0.06, 0.06, 0.065), 0.3, metal=0.8), 0.01)
cube('amp_luz', (0.62, -0.252, 0.08), (0.2, 0.002, 0.006), mat('ampled', (0, 0, 0), emis=VERDE, es=8), 0)

T_OK = 14.4
for f in range(1, NF + 1):
    t = (f - 1) / FPS
    if t < T_OK: d = random.uniform(-0.004, 0.004)          # tremido do chiado
    else: d = 0.01 * math.sin(2 * math.pi * 2.0 * t)       # música limpa
    cone.location.y = -0.232 - d; cone.keyframe_insert('location', index=1, frame=f)

def anel(t0, cor, forte):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.13, minor_radius=0.004, location=(CX, -0.25, CZ - 0.12), rotation=(math.pi/2, 0, 0))
    o = bpy.context.object; m = mat('anel', (0, 0, 0), emis=cor, es=0); o.data.materials.append(m)
    em = m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
    f0 = T(t0); f1 = T(t0 + 1.2)
    for f, s_, e in ((max(1, f0 - 1), 0.01, 0), (f0, 1.0, 7 if forte else 6), (f1, 3.4 if forte else 2.2, 0), (f1 + 1, 0.0, 0)):
        o.scale = (s_, s_, s_); o.keyframe_insert('scale', frame=f); em.default_value = e; em.keyframe_insert('default_value', frame=f)
t = 0.3
while t < DUR - 1.0:
    if TM0 - 0.3 < t < T_OK: t += 0.4; continue
    anel(t, VERM if t < T_OK else VERDE, t >= T_OK); t += 0.4

# linha do som acima da caixa: chiado (serrilhada vermelha) -> onda limpa (verde)
def linha(nome, fn, cor, es):
    N = 120; vs = [(-0.42 + 0.84 * i / (N - 1), 0, fn(i / (N - 1))) for i in range(N)]
    me = bpy.data.meshes.new(nome); me.from_pydata(vs, [(i, i + 1) for i in range(N - 1)], [])
    o = bpy.data.objects.new(nome, me); bpy.context.collection.objects.link(o); o.location = (CX, -0.3, 0.92)
    o.modifiers.new('sk', 'SKIN')
    for v in o.data.skin_vertices[0].data: v.radius = (0.005, 0.005)
    o.data.materials.append(mat(nome + 'm', (0, 0, 0), emis=cor, es=es*0.6)); return o
ruido = linha('ruido', lambda u: math.sin(u * 4 * math.pi) * 0.05 + random.uniform(-0.06, 0.06), VERM, 10)
limpa = linha('limpa', lambda u: math.sin(u * 4 * math.pi) * 0.09, VERDE, 10)
for f in range(1, NF + 1):
    t = (f - 1) / FPS
    zr = (1.0 if t < TM0 - 0.2 else max(0.0, 1 - (t - (TM0 - 0.2)) / 0.4)) * (0.6 + 0.6 * random.random()) if t > 0.15 else 0.01
    ruido.scale = (0.0 if t > TM0 + 0.3 else 1, 1, max(zr, 0.01)); ruido.keyframe_insert('scale', frame=f)
    zl = 0.01 if t < T_OK else min(1.0, (t - T_OK) / 0.6)
    limpa.scale = (0.0 if t < T_OK else 1, 1, max(zl, 0.01)); limpa.keyframe_insert('scale', frame=f)
EV += [(0.2, 'batida'), (3.6, 'whoosh'), (9.0, 'erro'), (T_OK, 'plim'), (0.25, 'zumbido', 3.4), (4.0, 'zumbido', 4.0)]

# ---------- luzes ----------
def area(loc, rot, en, cor, tam):
    l = bpy.data.lights.new('a', 'AREA'); l.energy = en; l.color = cor; l.size = tam
    o = bpy.data.objects.new('a', l); o.location = loc; o.rotation_euler = rot; bpy.context.collection.objects.link(o); return l
area((-1.6, -1.8, 2.4), (math.radians(55), 0, math.radians(-40)), 130, (1, 0.93, 0.85), 1.6)
area((1.8, -0.4, 1.6), (math.radians(70), 0, math.radians(100)), 80, VERDE, 1.0)
area((-1.6, -0.2, 1.4), (math.radians(70), 0, math.radians(-100)), 60, (1, 0.7, 0.45), 1.0)
area((0, -1.2, 1.3), (math.radians(80), 0, 0), 12, (1, 0.9, 0.8), 2.0)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.02

# ---------- câmera ----------
cd = bpy.data.cameras.new('cam'); cd.lens = 36; cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.4
cam = bpy.data.objects.new('cam', cd); bpy.context.collection.objects.link(cam); sc.camera = cam
alvo = bpy.data.objects.new('alvo', None); bpy.context.collection.objects.link(alvo)
tc = cam.constraints.new('TRACK_TO'); tc.target = alvo; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'
cd.dof.focus_object = alvo
def kc(tt, pos, alv):
    cam.location = pos; cam.keyframe_insert('location', frame=T(tt)); alvo.location = alv; alvo.keyframe_insert('location', frame=T(tt))
kc(0.0, (0.28, -0.95, 0.42), (CX, -0.23, CZ - 0.05))      # gancho: close no woofer tremendo
kc(3.4, (0.15, -1.25, 0.6), (CX, -0.2, CZ + 0.05))
kc(5.0, (-0.2, -2.9, 1.05), (0, 0, 0.85))                 # geral: caixa + parede fechada
kc(7.6, (0.1, -2.7, 1.1), (0, 0, 0.9))
kc(9.2, (0.25, -1.45, 1.35), (0, 0.15, Z1 - 0.05))       # parede aberta: eletroduto
kc(12.3, (0.05, -1.3, 1.34), (0, 0.15, Z1 - 0.05))
kc(14.6, (-0.1, -1.5, 1.28), (0, 0.15, (Z1 + Z2) / 2))    # cabo indo para o outro tubo
kc(16.0, (-0.1, -3.0, 1.05), (0, 0, 0.85))                # geral: som limpo
kc(DUR, (0.15, -2.6, 1.0), (0, 0, 0.82))

# ---------- render ----------
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = int(os.environ.get('SAMPLES', 12)); sc.cycles.use_denoising = True
sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.transmission_bounces = 2; sc.cycles.transparent_max_bounces = 8
sc.render.resolution_x = int(os.environ.get('LARG', 540)); sc.render.resolution_y = int(os.environ.get('ALT', 960))
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 94
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
json.dump(sorted(EV, key=lambda e: e[0]), open(os.path.join(OUT, 'events.json'), 'w'))
modo = sys.argv[-1]
if modo == 'save':
    sc.render.image_settings.file_format = 'JPEG'; bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'MOVE_cena_casos_rafael.blend')); sys.exit(0)
if modo.startswith('test'):
    for f in [int(x) for x in modo.split(':')[1].split(',')]:
        sc.frame_set(f); sc.render.filepath = os.path.join(OUT, f'test_{f:04d}.jpg'); bpy.ops.render.render(write_still=True)
elif ':' in modo:
    a, b = [int(x) for x in modo.split(':')]; os.makedirs(os.path.join(OUT, 'frames'), exist_ok=True)
    for f in range(a, b + 1, int(os.environ.get('STEP', 1))):
        p = os.path.join(OUT, 'frames', f'{f:04d}.jpg')
        if os.path.exists(p): continue
        sc.frame_set(f); sc.render.filepath = p; bpy.ops.render.render(write_still=True)
