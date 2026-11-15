# Biblioteca comum dos Reels "MOVE Explica 3D premium" (Blender/bpy).
# Mesmo visual do explica_polaridade_3d: estúdio escuro, piso com reflexo, nogueira, luz verde de recorte + quente.
import bpy, math, os, sys, json
FPS = 24
VERDE = (0.27, 0.85, 0.65); VERM = (1.0, 0.2, 0.17); QUENTE = (1.0, 0.78, 0.5)
EV = []
def T(s): return int(s * FPS) + 1

def iniciar(dur):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene; sc.render.fps = FPS; sc.frame_start = 1; sc.frame_end = int(dur * FPS)
    return sc

def mat(nome, cor, rough=0.4, metal=0.0, emis=None, es=0.0, clearcoat=0.0):
    m = bpy.data.materials.new(nome); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*cor, 1); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if clearcoat: b.inputs['Coat Weight'].default_value = clearcoat
    if emis: b.inputs['Emission Color'].default_value = (*emis, 1); b.inputs['Emission Strength'].default_value = es
    return m

def obj(o, m): o.data.materials.append(m); return o
def cube(nome, loc, esc, m, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc); o = bpy.context.object; o.name = nome; o.scale = esc
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        md = o.modifiers.new('b', 'BEVEL'); md.width = bevel; md.segments = 4
    bpy.ops.object.shade_smooth(); return obj(o, m)
def cil(nome, loc, r, d, m, rot=(math.pi / 2, 0, 0), v=64):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=d, location=loc, rotation=rot); o = bpy.context.object; o.name = nome
    bpy.ops.object.shade_smooth(); return obj(o, m)

M = {}
def materiais():
    M['piso'] = mat('piso', (0.012, 0.014, 0.014), 0.18, clearcoat=0.6)
    M['parede'] = mat('parede', (0.02, 0.022, 0.022), 0.7)
    M['madeira'] = mat('nogueira', (0.16, 0.075, 0.035), 0.35, clearcoat=0.5)
    M['frente'] = mat('frente', (0.008, 0.008, 0.009), 0.45)
    M['cone'] = mat('cone', (0.03, 0.03, 0.032), 0.55)
    M['aro'] = mat('aro', (0.6, 0.6, 0.62), 0.25, metal=1.0)
    M['tw'] = mat('tweeter', (0.75, 0.72, 0.66), 0.2, metal=1.0)
    M['verm'] = mat('vermelho', (0.55, 0.02, 0.02), 0.3, clearcoat=0.4)
    M['preto'] = mat('preto', (0.015, 0.015, 0.015), 0.3, clearcoat=0.4)
    M['ouro'] = mat('ouro', (0.9, 0.62, 0.25), 0.2, metal=1.0)
    M['cobre'] = mat('cobre', (0.85, 0.42, 0.22), 0.25, metal=1.0)
    M['alu'] = mat('alu', (0.06, 0.06, 0.065), 0.3, metal=0.8)
    M['alu_claro'] = mat('alu_claro', (0.5, 0.5, 0.52), 0.28, metal=1.0)
    M['gesso'] = mat('gesso', (0.55, 0.53, 0.5), 0.8)
    return M

def estudio(sanca=True, parede_y=4):
    bpy.ops.mesh.primitive_plane_add(size=40); obj(bpy.context.object, M['piso'])
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, parede_y, 0), rotation=(math.pi / 2, 0, 0)); obj(bpy.context.object, M['parede'])
    if sanca:
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, parede_y - 0.05, 2.6), rotation=(math.pi / 2, 0, 0))
        f = bpy.context.object; f.scale = (8, 0.03, 1); obj(f, mat('sanca', (0, 0, 0), emis=QUENTE, es=6))

def caixa(nome, x, y, z=0.62, s=1.0, pedestal=True, rotz=0.0):
    """Caixa bookshelf de nogueira. Retorna (cone, centro_do_woofer, posicao_bornes)."""
    vazio = bpy.data.objects.new(nome, None); bpy.context.collection.objects.link(vazio); vazio.location = (x, y, 0); vazio.rotation_euler = (0, 0, rotz)
    partes = []
    partes.append(cube(f'gab{nome}', (0, 0, z), (0.2 * s, 0.17 * s, 0.33 * s), M['madeira'], 0.02 * s))
    partes.append(cube(f'fr{nome}', (0, -0.171 * s, z), (0.185 * s, 0.005, 0.315 * s), M['frente'], 0.006))
    zw = z - 0.12 * s; zt = z + 0.2 * s
    partes.append(cil(f'aroW{nome}', (0, -0.18 * s, zw), 0.135 * s, 0.012, M['aro']))
    c = cil(f'cone{nome}', (0, -0.182 * s, zw), 0.118 * s, 0.01, M['cone'])
    partes.append(cil(f'cap{nome}', (0, -0.19 * s, zw), 0.04 * s, 0.01, M['aro']))
    partes.append(cil(f'aroT{nome}', (0, -0.18 * s, zt), 0.05 * s, 0.012, M['aro']))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.03 * s, location=(0, -0.18 * s, zt)); t = bpy.context.object; t.scale = (1, 0.45, 1); bpy.ops.object.shade_smooth(); partes.append(obj(t, M['tw']))
    zb = z - 0.33 * s
    if pedestal:
        partes.append(cube(f'base{nome}', (0, 0, zb / 2), (0.16 * s, 0.14 * s, zb / 2), M['frente'], 0.01))
    for k, (dx, m) in enumerate(((-0.05, M['verm']), (0.05, M['preto']))):
        partes.append(cil(f'borne{nome}{k}', (dx * s, -0.145 * s, max(0.16, zb - 0.08)), 0.018, 0.04, m))
    for p in partes + [c]:
        p.parent = vazio
    c['y0'] = c.location.y
    return c, vazio

def amplificador(nome, loc, esc=(0.32, 0.22, 0.06), led=VERDE, botoes=True):
    a = cube(nome, loc, esc, M['alu'], 0.01)
    x, y, z = loc
    l = cube(nome + '_led', (x + esc[0] * 0.55, y - esc[1] - 0.002, z + esc[2] * 0.25), (esc[0] * 0.25, 0.002, esc[2] * 0.08), mat(nome + 'led', (0, 0, 0), emis=led, es=8))
    l.parent = a; l.matrix_parent_inverse = a.matrix_world.inverted()
    if botoes:
        for k in range(2):
            b = cil(nome + f'_knob{k}', (x - esc[0] * 0.6 + k * esc[0] * 0.35, y - esc[1] - 0.012, z), esc[2] * 0.45, 0.025, M['alu_claro'])
            b.parent = a; b.matrix_parent_inverse = a.matrix_world.inverted()
    return a

def cabo(nome, pts, m, esp=0.008):
    cu = bpy.data.curves.new(nome, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = esp; cu.bevel_resolution = 6
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(pts) - 1)
    for p, co in zip(sp.bezier_points, pts):
        p.co = co; p.handle_left_type = p.handle_right_type = 'AUTO'
    o = bpy.data.objects.new(nome, cu); bpy.context.collection.objects.link(o); o.data.materials.append(m); return o, sp

def texto(nome, s, loc, tam, cor, es=8, rot=(math.pi / 2, 0, 0), alinhar='CENTER', extr=0.004):
    cu = bpy.data.curves.new(nome, 'FONT'); cu.body = s; cu.size = tam; cu.align_x = alinhar; cu.align_y = 'CENTER'; cu.extrude = extr
    o = bpy.data.objects.new(nome, cu); bpy.context.collection.objects.link(o); o.location = loc; o.rotation_euler = rot
    m = mat(nome + 'm', (0, 0, 0), emis=cor, es=es); o.data.materials.append(m)
    return o, m

def visivel(o, quadros):
    """quadros: lista de (t, True/False)."""
    for t, v in quadros:
        o.hide_render = not v; o.keyframe_insert('hide_render', frame=T(t))
        o.hide_viewport = not v; o.keyframe_insert('hide_viewport', frame=T(t))
    if o.animation_data and o.animation_data.action:
        try:
            for fc in o.animation_data.action.fcurves:
                for k in fc.keyframe_points: k.interpolation = 'CONSTANT'
        except Exception:
            pass

def emis_k(m, quadros):
    em = m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
    for t, e in quadros: em.default_value = e; em.keyframe_insert('default_value', frame=T(t))
def cor_k(m, quadros):
    ec = m.node_tree.nodes['Principled BSDF'].inputs['Emission Color']
    for t, c in quadros: ec.default_value = (*c, 1); ec.keyframe_insert('default_value', frame=T(t))

def anel(loc, t0, cor, forte, rot=(math.pi / 2, 0, 0), r=0.13, alcance=None):
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=0.004, location=loc, rotation=rot)
    o = bpy.context.object
    m = mat('anel', (0, 0, 0), emis=cor, es=0); o.data.materials.append(m)
    em = m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
    f0 = T(t0); f1 = T(t0 + 1.3)
    big = alcance or (3.6 if forte else 2.0)
    for f, sc_, e in ((max(1, f0 - 1), 0.01, 0), (f0, 1.0, 14 if forte else 8), (f1, big, 0), (f1 + 1, 0.0, 0)):
        o.scale = (sc_, sc_, sc_); o.keyframe_insert('scale', frame=f); em.default_value = e; em.keyframe_insert('default_value', frame=f)
    return o

def cones(lista, dur, regra):
    """regra(i, t) -> amplitude (m) do cone i no tempo t (0 = parado)."""
    NF = int(dur * FPS)
    for f in range(1, NF + 1):
        t = (f - 1) / FPS
        s = math.sin(2 * math.pi * 2.2 * t)
        for i, c in enumerate(lista):
            a = regra(i, t)
            c.location.y = c['y0'] - a * s; c.keyframe_insert('location', index=1, frame=f)

def luzes(chave=260, verde=140, quente=90):
    def area(loc, rot, en, cor, tam):
        l = bpy.data.lights.new('a', 'AREA'); l.energy = en; l.color = cor; l.size = tam
        o = bpy.data.objects.new('a', l); o.location = loc; o.rotation_euler = rot; bpy.context.collection.objects.link(o); return l
    area((-1.6, -1.8, 2.2), (math.radians(55), 0, math.radians(-40)), chave, (1, 0.93, 0.85), 1.6)
    area((1.8, 1.2, 1.4), (math.radians(70), 0, math.radians(130)), verde, VERDE, 1.0)
    area((-1.8, 1.4, 1.2), (math.radians(70), 0, math.radians(-130)), quente, (1, 0.7, 0.45), 1.0)
    sc = bpy.context.scene
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.02

def camera(lente=38, fstop=2.2):
    sc = bpy.context.scene
    cd = bpy.data.cameras.new('cam'); cd.lens = lente; cd.dof.use_dof = True; cd.dof.aperture_fstop = fstop
    cam = bpy.data.objects.new('cam', cd); bpy.context.collection.objects.link(cam); sc.camera = cam
    alvo = bpy.data.objects.new('alvo', None); bpy.context.collection.objects.link(alvo)
    tc = cam.constraints.new('TRACK_TO'); tc.target = alvo; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'
    cd.dof.focus_object = alvo
    def kc(tt, pos, alv):
        cam.location = pos; cam.keyframe_insert('location', frame=T(tt)); alvo.location = alv; alvo.keyframe_insert('location', frame=T(tt))
    return kc

def finalizar(out_dir):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = int(os.environ.get('SAMPLES', 12)); sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.transmission_bounces = 0
    sc.render.resolution_x = int(os.environ.get('LARG', 540)); sc.render.resolution_y = int(os.environ.get('ALT', 960))
    sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 94
    sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
    sc.render.threads_mode = 'AUTO'
    json.dump(sorted(EV), open(os.path.join(out_dir, 'events.json'), 'w'))
    modo = sys.argv[-1]
    if modo == 'save':
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out_dir, 'cena.blend')); return
    if modo.startswith('test'):
        for f in [int(x) for x in modo.split(':')[1].split(',')]:
            sc.frame_set(f); sc.render.filepath = os.path.join(out_dir, f'test_{f:04d}.jpg'); bpy.ops.render.render(write_still=True)
    else:
        a, b = [int(x) for x in modo.split(':')]; os.makedirs(os.path.join(out_dir, 'frames'), exist_ok=True)
        for f in range(a, b + 1, int(os.environ.get('STEP', 1))):
            p = os.path.join(out_dir, 'frames', f'{f:04d}.jpg')
            if os.path.exists(p): continue
            sc.frame_set(f); sc.render.filepath = p; bpy.ops.render.render(write_still=True)
