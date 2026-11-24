# Metalize Explica 3D v2 — "Como a calha protege a sua casa" — com calha x sem calha, casa real no MT, chuva.
# uso: python3 cena.py test:1,100   |   python3 cena.py 1:672   (env: SAMPLES, LARG, ALT, STEP, TRANS)
import sys, os, math, random
sys.path.insert(0, '/home/claude/harmony-/automacao/animacoes')
os.environ.setdefault('TRANS', '4')
import bpy
from lib3d import iniciar, mat, cube, cil, camera, cabo, finalizar, T, FPS

AQUI = os.path.dirname(os.path.abspath(__file__))
DUR = 26.0
sc = iniciar(DUR)
random.seed(11)
NF = int(DUR * FPS)
S0, S1 = 13.2, 21.2     # trecho SEM CALHA
TROCA = 0.0

# ---------------- materiais ----------------
def mat_ruido(nome, cor1, cor2, rough, escala=8.0, bump=0.15, metal=0.0):
    m = bpy.data.materials.new(nome); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = escala; nz.inputs['Detail'].default_value = 8
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (*cor1, 1); cr.color_ramp.elements[1].color = (*cor2, 1)
    nt.links.new(nz.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], b.inputs['Base Color'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    return m

def mat_agua(nome, tint=(0.75, 0.86, 0.92), ondas=True, fluxo=None):
    m = bpy.data.materials.new(nome); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*tint, 1); b.inputs['Roughness'].default_value = 0.03
    b.inputs['Transmission Weight'].default_value = 1.0; b.inputs['IOR'].default_value = 1.33
    if ondas:
        tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
        nz = nt.nodes.new('ShaderNodeTexNoise'); nz.noise_dimensions = '4D'; nz.inputs['Scale'].default_value = 18; nz.inputs['Detail'].default_value = 4
        nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
        bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.35
        nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
        w = nz.inputs['W']
        for f in (1, NF): w.default_value = f * 0.04; w.keyframe_insert('default_value', frame=f)
        if fluxo:  # textura andando (direção do escoamento)
            for f, v in ((1, (0, 0, 0)), (NF, fluxo)):
                mp.inputs['Location'].default_value = v; mp.inputs['Location'].keyframe_insert('default_value', frame=f)
    return m

def mat_cortina(nome):
    """lâmina de água caindo: faixas verticais transparentes que descem."""
    m = bpy.data.materials.new(nome); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (0.8, 0.88, 0.93, 1); b.inputs['Roughness'].default_value = 0.05
    b.inputs['Transmission Weight'].default_value = 0.85; b.inputs['IOR'].default_value = 1.33
    b.inputs['Emission Color'].default_value = (0.85, 0.92, 1.0, 1); b.inputs['Emission Strength'].default_value = 0.12
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (60, 2.5, 1)
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3; nz.inputs['Detail'].default_value = 6
    nt.links.new(tc.outputs['UV'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.56; cr.color_ramp.elements[1].position = 0.72
    nt.links.new(nz.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], b.inputs['Alpha'])
    for f, v in ((1, (0, 0, 0)), (NF, (0, 2.5 * DUR * 1.6, 0))):
        mp.inputs['Location'].default_value = v; mp.inputs['Location'].keyframe_insert('default_value', frame=f)
    return m

M = {}
M['grama'] = mat_ruido('terra_mt', (0.32, 0.09, 0.03), (0.09, 0.16, 0.04), 0.55, 3.5, 0.3)  # terra vermelha do MT com grama
M['copa'] = mat_ruido('copa', (0.03, 0.08, 0.02), (0.08, 0.16, 0.04), 0.8, 6, 0.6)
M['tronco'] = mat('tronco', (0.12, 0.08, 0.05), 0.8)
M['calcada'] = mat_ruido('calcada', (0.36, 0.36, 0.35), (0.5, 0.5, 0.48), 0.45, 30, 0.2)   # molhada: brilha
M['parede'] = mat_ruido('parede', (0.78, 0.76, 0.72), (0.86, 0.84, 0.8), 0.85, 25, 0.08)
M['parede_molhada'] = mat_ruido('parede_m', (0.3, 0.25, 0.19), (0.62, 0.58, 0.52), 0.3, 5, 0.1)
M['telha'] = mat('telha', (0.18, 0.19, 0.2), 0.35, metal=0.9)
M['forro'] = mat('forro', (0.85, 0.85, 0.83), 0.7)
M['galv'] = mat_ruido('galvalume', (0.55, 0.56, 0.58), (0.68, 0.69, 0.7), 0.28, 120, 0.02, metal=1.0)
M['vidro'] = mat('vidro', (0.02, 0.025, 0.03), 0.05, clearcoat=1.0)
M['alu'] = mat('alu_preto', (0.02, 0.02, 0.02), 0.4, metal=0.6)
M['grelha'] = mat('grelha', (0.05, 0.05, 0.05), 0.5, metal=0.8)
M['agua'] = mat_agua('agua', tint=(0.45, 0.62, 0.72))
b_ = M['agua'].node_tree.nodes['Principled BSDF']; b_.inputs['Transmission Weight'].default_value = 0.55; b_.inputs['Emission Color'].default_value = (0.5, 0.7, 0.85, 1); b_.inputs['Emission Strength'].default_value = 0.18
M['filete'] = mat('filete', (0.6, 0.72, 0.8), 0.05, emis=(0.7, 0.82, 0.95), es=0.35)
M['agua_fluxo'] = mat_agua('agua_fluxo', tint=(0.45, 0.62, 0.72), fluxo=(-3.0 * DUR, 0, 0))
b_ = M['agua_fluxo'].node_tree.nodes['Principled BSDF']; b_.inputs['Transmission Weight'].default_value = 0.55; b_.inputs['Emission Color'].default_value = (0.5, 0.7, 0.85, 1); b_.inputs['Emission Strength'].default_value = 0.18
M['cortina'] = mat_cortina('cortina')
M['espuma'] = mat('espuma', (0.9, 0.93, 0.95), 0.6)
M['chuva'] = mat('chuva', (0.8, 0.85, 0.9), 0.1, emis=(0.75, 0.82, 0.9), es=1.2)
M['amarelo'] = mat('amarelo', (0, 0, 0), emis=(0.98, 0.78, 0.03), es=5)

# ---------------- casa ----------------
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, -10, 0)); bpy.context.object.data.materials.append(M['grama'])
cube('calcada', (0, -0.6, 0.01), (5, 0.6, 0.01), M['calcada'])
# mata/fazenda ao fundo (cara de Mato Grosso)
for i in range(26):
    tx = random.uniform(-26, 26); ty = random.uniform(10, 30); hh = random.uniform(4, 9)
    cil(f'tronco{i}', (tx, ty, hh * 0.4), 0.18, hh * 0.8, M['tronco'], rot=(0, 0, 0), v=8)
    for k in range(3):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=random.uniform(1.6, 2.8), location=(tx + random.uniform(-1, 1), ty + random.uniform(-1, 1), hh + random.uniform(-0.5, 1.2)))
        o = bpy.context.object; o.scale = (1.2, 1.2, 0.75); o.data.materials.append(M['copa'])

cube('parede', (0, 1.6, 1.4), (4.2, 1.6, 1.4), M['parede'])
# janela
cube('jan_moldura', (-1.4, -0.005, 1.55), (0.62, 0.02, 0.62), M['alu'])
cube('jan_vidro', (-1.4, -0.02, 1.55), (0.56, 0.01, 0.56), M['vidro'])
cube('jan_div', (-1.4, -0.03, 1.55), (0.015, 0.01, 0.56), M['alu'])
# mancha de água na parede (aparece quando transborda)
mancha = cube('mancha', (0.3, -0.004, 2.55), (3.6, 0.002, 0.28), M['parede_molhada'])
# beiral: forro + telhado trapezoidal
EZ = 2.98; EY = -0.5
cube('forro', (0, (EY + 0) / 2 - 0.02, 2.84), (4.3, 0.27, 0.012), M['forro'])
ANG = math.radians(15)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, EY + 1.9 * math.cos(ANG), EZ + 1.9 * math.sin(ANG)), rotation=(ANG, 0, 0))
tel = bpy.context.object; tel.scale = (8.6, 3.8, 1); tel.data.materials.append(M['telha'])
for i in range(-17, 18):
    x = i * 0.25
    c = cube(f'onda{i}', (0, 0, 0), (0.035, 1.9, 0.014), M['telha'], 0.006); c.rotation_euler = (ANG, 0, 0)
    c.location = (x, tel.location.y - 0.012 * math.sin(ANG), tel.location.z + 0.012 * math.cos(ANG))

def zroof(y): return EZ + (y - EY) * math.tan(ANG)

# ---------------- calhas ----------------
L = 4.2; CW = 0.16; CH = 0.13
CY = EY - 0.08 - CW / 2        # centro da calha em y (a frente fica para fora do beiral)
def calha(pref, z0, parent=None, x0=0.0):
    ps = [cube(pref + 'fundo', (x0, CY, z0), (L, CW / 2, 0.004), M['galv']),
          cube(pref + 'frente', (x0, CY - CW / 2, z0 + CH / 2), (L, 0.004, CH / 2), M['galv']),
          cube(pref + 'tras', (x0, CY + CW / 2, z0 + CH / 2 + 0.02), (L, 0.004, CH / 2 + 0.02), M['galv']),
          cube(pref + 'tE', (x0 - L, CY, z0 + CH / 2), (0.004, CW / 2, CH / 2), M['galv']),
          cube(pref + 'tD', (x0 + L, CY, z0 + CH / 2), (0.004, CW / 2, CH / 2), M['galv'])]
    ps.append(cube(pref + 'friso', (x0, CY - CW / 2 - 0.012, z0 + CH - 0.006), (L, 0.012, 0.006), M['galv']))  # aba reta dobrada
    for k in range(-7, 8):  # suportes
        xs = x0 + k * 0.58
        ps.append(cube(pref + f'sup{k}', (xs, CY, z0 - 0.006), (0.015, CW / 2 + 0.01, 0.003), M['galv']))
        ps.append(cube(pref + f'supf{k}', (xs, CY - CW / 2 - 0.006, z0 + CH / 2), (0.015, 0.003, CH / 2), M['galv']))
    ps.append(cil(pref + 'bocal', (x0 + 3.5, CY, z0 + 0.006), 0.045, 0.004, mat('furo', (0, 0, 0), 0.9), rot=(0, 0, 0)))
    if parent:
        for p in ps: p.parent = parent
    return ps

ZA = 2.80
cA = calha('A_', ZA)
PHI = math.atan(0.005); ZP = 2.82   # caimento real de 0,5% (5 mm por metro): a calha fica reta aos olhos
piv = bpy.data.objects.new('pivo', None); bpy.context.collection.objects.link(piv)
piv.location = (-L, 0, ZP); piv.rotation_euler = (0, PHI, 0)
cB = calha('B_', 0.0, piv, x0=L)
for o in cB: o.location.y += 0  # já em CY
def zB(x): return ZP - (x + L) * math.tan(PHI)

XC = 3.5
ZTOP = min(ZA, zB(XC))
from mathutils import Vector
def tubo_reto(nome, a, b, r=0.04):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=r, depth=d.length, location=(a + b) / 2)
    o = bpy.context.object; o.name = nome; o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y')
    bpy.ops.object.shade_smooth(); o.data.materials.append(M['galv']); return o
PTS = [(XC, CY, ZTOP + 0.01), (XC, CY, ZTOP - 0.22), (XC, -0.07, ZTOP - 0.22 - (CY * -1 - 0.07)), (XC, -0.07, 0.3), (XC, -0.27, 0.1)]
tubo = tubo_reto('condutor', PTS[0], PTS[1])
TUBOS = [tubo] + [tubo_reto(f'condutor{k}', PTS[k], PTS[k + 1]) for k in range(1, len(PTS) - 1)]
for k, pt in enumerate(PTS[1:-1]):  # curvas de 45° (luvas)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.046, location=pt); j = bpy.context.object; j.name = f'curva{k}'; bpy.ops.object.shade_smooth(); j.data.materials.append(M['galv']); TUBOS.append(j)
for zb in (0.8, 1.5, 2.0):
    cube(f'abraca{zb}', (XC, -0.03, zb), (0.05, 0.03, 0.01), M['galv'])
cube('grelha', (XC, -0.4, 0.022), (0.15, 0.15, 0.004), M['grelha'])
TUBO = TUBOS + [o for o in bpy.data.objects if o.name.startswith('abraca')]

def vis(objs, faixas):
    for o in objs:
        for t, v in faixas:
            o.hide_render = not v; o.keyframe_insert('hide_render', frame=max(1, T(t)))
vis(cA, [(0, False)])
SEMV = [(0, True), (S0, False), (S1, True)]
vis(cB, SEMV); vis(TUBO, SEMV)

# ---------------- água na calha A (reta): enche e transborda ----------------
def nivel(t):
    if t < 3.0: return CH
    if t < 5.6: return 0.03
    if t < 8.5: return 0.03 + (CH - 0.03) * (t - 5.6) / 2.9
    return CH
bpy.ops.mesh.primitive_cube_add(); agA = bpy.context.object; agA.data.materials.append(M['agua'])
for f in range(1, NF + 1, 2):
    t = (f - 1) / FPS; h = nivel(t) + 0.004
    agA.scale = (L - 0.01, CW / 2 - 0.004, h / 2); agA.location = (0, CY, ZA + 0.004 + h / 2)
    agA.keyframe_insert('scale', frame=f); agA.keyframe_insert('location', frame=f)
vis([agA], [(0, False)])
transb = lambda t: t < 3.0 or 8.5 <= t < TROCA

# lâmina de água que derrama pela borda: sai para fora, cai em parábola e se desfaz em filetes
def mat_lamina(nome):
    m = bpy.data.materials.new(nome); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (0.7, 0.82, 0.9, 1); b.inputs['Roughness'].default_value = 0.04
    b.inputs['Transmission Weight'].default_value = 0.7; b.inputs['IOR'].default_value = 1.33
    b.inputs['Emission Color'].default_value = (0.8, 0.9, 1.0, 1); b.inputs['Emission Strength'].default_value = 0.05
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['UV'], sep.inputs['Vector'])
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (90, 3, 1); nt.links.new(tc.outputs['UV'], mp.inputs['Vector'])
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 2.5; nz.inputs['Detail'].default_value = 6
    nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
    a1 = nt.nodes.new('ShaderNodeMath'); a1.operation = 'MULTIPLY_ADD'; a1.inputs[1].default_value = 0.3; a1.inputs[2].default_value = 0.4
    nt.links.new(sep.outputs['Y'], a1.inputs[0])
    a2 = nt.nodes.new('ShaderNodeMath'); a2.operation = 'SUBTRACT'; nt.links.new(nz.outputs['Fac'], a2.inputs[0]); nt.links.new(a1.outputs[0], a2.inputs[1])
    a3 = nt.nodes.new('ShaderNodeMath'); a3.operation = 'MULTIPLY'; a3.use_clamp = True; a3.inputs[1].default_value = 10
    nt.links.new(a2.outputs[0], a3.inputs[0]); nt.links.new(a3.outputs[0], b.inputs['Alpha'])
    for f, v in ((1, (0, 0, 0)), (NF, (0, -3 * DUR * 1.4, 0))):
        mp.inputs['Location'].default_value = v; mp.inputs['Location'].keyframe_insert('default_value', frame=f)
    return m
Y0 = EY - 0.03; Z0 = EZ - 0.005; VY = 0.55; TQ = math.sqrt(2 * Z0 / 9.8)  # sem calha: a água despenca da beira do telhado
verts, faces, uvs = [], [], []
NX, NZ = 60, 40
for iz in range(NZ + 1):
    t = TQ * (iz / NZ) ** 1.3
    for ix in range(NX + 1):
        x = -L + 0.05 + (2 * L - 0.1) * ix / NX
        verts.append((x, Y0 - VY * t, Z0 - 4.9 * t * t))
for iz in range(NZ):
    for ix in range(NX):
        a = iz * (NX + 1) + ix; faces.append((a, a + 1, a + NX + 2, a + NX + 1))
me = bpy.data.meshes.new('lamina'); me.from_pydata(verts, [], faces); me.update()
uv = me.uv_layers.new(name='UVMap')
for poly in me.polygons:
    for li in poly.loop_indices:
        vi = me.loops[li].vertex_index; ix = vi % (NX + 1); iz = vi // (NX + 1)
        uv.data[li].uv = (ix / NX, iz / NZ)
cort = bpy.data.objects.new('lamina', me); bpy.context.collection.objects.link(cort); me.materials.append(mat_lamina('lamina'))
for p_ in me.polygons: p_.use_smooth = True
for t, v in ((0, False), (S0, True), (S1, False)):
    cort.hide_render = not v; cort.keyframe_insert('hide_render', frame=max(1, T(t)))

# gotas soltas que se desprendem da borda + respingos no chão (partículas com gravidade)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.006, segments=8, ring_count=6, location=(0, 0, -20)); gt = bpy.context.object
gt.scale = (1, 1, 2.2); gt.data.materials.append(M['filete'])
def emissor(nome, loc, esc, f0, f1, n, vel, rnd, vida):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc); e = bpy.context.object; e.name = nome; e.scale = esc
    e.show_instancer_for_render = False
    p = e.modifiers.new(nome, 'PARTICLE_SYSTEM').particle_system.settings
    p.count = n; p.frame_start = f0; p.frame_end = f1; p.lifetime = vida; p.normal_factor = 0
    p.object_align_factor = vel; p.factor_random = rnd; p.render_type = 'OBJECT'; p.instance_object = gt
    p.particle_size = 1.0; p.use_rotations = True; p.rotation_mode = 'VEL'; p.emit_from = 'FACE'; p.use_emit_random = True
    return e
# borda (dois períodos de transbordamento)
emissor('gotas', (0, Y0, Z0), (L - 0.1, 0.01, 1), T(S0) - 10, T(S1), 6000, (0, -0.55, 0), 0.25, 30)
# respingos onde a água bate no chão
YCH = Y0 - VY * TQ
emissor('resp', (0, YCH, 0.03), (L - 0.1, 0.12, 1), T(S0) + 10, T(S1), 9000, (0, 0.5, 1.7), 1.2, 14)  # respinga na parede
mancha.hide_render = True
umid = cube('umidade', (0.3, -0.004, 0.32), (3.6, 0.002, 0.32), M['parede_molhada'])
for t, v in ((0, False), (S0 + 1.5, True), (S1, False)):
    umid.hide_render = not v; umid.keyframe_insert('hide_render', frame=max(1, T(t)))
for t, v in ((0, False), (S0 + 2.5, True), (S1, False)):
    mancha.hide_render = not v; mancha.keyframe_insert('hide_render', frame=max(1, T(t)))
# poça na calçada
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, YCH + 0.05, 0.023)); poca = bpy.context.object
poca.scale = (2 * L - 0.5, 0.45, 1); poca.data.materials.append(M['agua'])
vis([poca], [(0, False), (S0 + 1.0, True), (S1, False)])

# ---------------- água na calha B (com caimento): corre para o cano ----------------
bpy.ops.mesh.primitive_cube_add(); agB = bpy.context.object; agB.data.materials.append(M['agua_fluxo'])
agB.parent = piv; agB.location = (L, CY, 0.012); agB.scale = (L - 0.01, CW / 2 - 0.004, 0.018)
vis([agB], SEMV)
# espuma/folhinhas boiando: mostram a direção da água
esp = []
for i in range(26):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.018, segments=10, ring_count=6); e = bpy.context.object
    e.scale = (1.6, 1, 0.35); e.data.materials.append(M['espuma']); esp.append(e)
    x0 = random.uniform(-L + 0.1, XC); yo = random.uniform(-CW / 2 + 0.02, CW / 2 - 0.02); v = 0.9
    for f in range(1, NF + 1, 2):
        t = (f - 1) / FPS
        if S0 <= t < S1: x = 99
        else:
            x = -L + 0.1 + ((x0 + L + v * (t - TROCA)) % (XC - (-L + 0.1)))
        e.location = (x, CY + yo, zB(x) + 0.04) if x < 50 else (0, 0, -5)
        e.keyframe_insert('location', frame=f)
# jato saindo do cano
emissor('jato1', (XC, -0.31, 0.07), (0.025, 0.01, 1), 1, T(S0), 3000, (0, -0.9, 0.1), 0.15, 12)
emissor('jato2', (XC, -0.31, 0.07), (0.025, 0.01, 1), T(S1), NF, 1500, (0, -0.9, 0.1), 0.15, 12)

# ---------------- água descendo pelo telhado (filetes) ----------------
fil = []
for i in range(40):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=0.22, vertices=8); g = bpy.context.object
    g.data.materials.append(M['filete']); fil.append(g)
    x = random.uniform(-3.9, 3.9); x = round(x / 0.25) * 0.25 + 0.125; ta = random.uniform(0, 1.4)
    for f in range(1, NF + 1, 2):
        t = (f - 1) / FPS; s = ((t - ta) % 1.4) / 1.4
        y = 2.6 - (2.6 - EY) * s; z = zroof(y) + 0.012
        g.location = (x, y, z); g.rotation_euler = (math.radians(90) + ANG, 0, 0)
        g.keyframe_insert('location', frame=f)
    g.keyframe_insert('rotation_euler', frame=1)

# ---------------- chuva (partículas) ----------------
bpy.ops.mesh.primitive_cylinder_add(radius=0.004, depth=0.3, vertices=6, location=(0, 0, -20)); gota = bpy.context.object
gota.data.materials.append(M['chuva'])
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -3.0, 7.0)); em = bpy.context.object; em.scale = (9, 7, 1)
em.hide_render = True
ps = em.modifiers.new('chuva', 'PARTICLE_SYSTEM').particle_system.settings
ps.count = 40000; ps.frame_start = -40; ps.frame_end = NF; ps.lifetime = 40
ps.normal_factor = 0; ps.object_align_factor[2] = -9.0; ps.effector_weights.gravity = 0.0
ps.render_type = 'OBJECT'; ps.instance_object = gota; ps.particle_size = 1.0; ps.use_rotations = True
ps.rotation_mode = 'VEL'; em.show_instancer_for_render = False
ps.emit_from = 'FACE'; ps.use_emit_random = True

# ---------------- anotação do caimento (linha amarela) ----------------
anot, _ = cabo('anot', [(-L + 0.05, CY - CW / 2 - 0.05, zB(-L) + CH + 0.06), (XC, CY - CW / 2 - 0.05, zB(XC) + CH + 0.06)], M['amarelo'], esp=0.006)
vis([anot], [(0, False), (6.7, True), (10.2, False)])

# ---------------- luz: dia nublado de chuva ----------------
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (0.4, 0.46, 0.55, 1); bg.inputs['Strength'].default_value = 1.15
sd = bpy.data.lights.new('sol', 'SUN'); sd.energy = 1.2; sd.angle = math.radians(25); sd.color = (0.9, 0.93, 1.0)
so = bpy.data.objects.new('sol', sd); so.rotation_euler = (math.radians(50), 0, math.radians(-35)); bpy.context.collection.objects.link(so)
l = bpy.data.lights.new('frente', 'AREA'); l.energy = 180; l.size = 4; lo = bpy.data.objects.new('frente', l)
lo.location = (0, -4, 3.5); lo.rotation_euler = (math.radians(60), 0, 0); bpy.context.collection.objects.link(lo)

# ---------------- câmera: olhar de gente ----------------
kc = camera(lente=30, fstop=5.6)
def corte(t0, t1, a, b):
    kc(t0, *a); kc(t1 - 1 / FPS, *b)
OLHO_A = ((-0.6, -3.4, 1.65), (0.3, CY, 2.2)); OLHO_B = ((-0.4, -3.2, 1.65), (0.35, CY, 2.15))
corte(0, 3.0, ((-0.4, -5.4, 1.6), (0.4, 0, 1.9)), ((-0.2, -4.9, 1.62), (0.4, 0, 1.95)))              # casa moderna na chuva
corte(3.0, 6.6, ((-1.0, 1.3, 4.7), (0.2, CY, 2.85)), ((-0.8, 1.0, 4.5), (0.3, CY, 2.85)))              # telhado -> calha
corte(6.6, 10.2, ((-3.2, -1.3, 3.55), (0.0, CY, 2.8)), ((0.8, -1.2, 3.45), (3.2, CY, 2.72)))          # corre pela calha até o tubo
corte(10.2, S0, ((2.3, -1.9, 2.5), (XC, -0.1, 2.5)), ((2.3, -1.9, 0.75), (XC, -0.1, 0.75)))   # câmera nivelada: tubo fica no prumo               # desce pelo tubo até o ralo
corte(S0, 17.0, OLHO_A, OLHO_B)                                                                        # SEM CALHA: despenca do telhado
corte(17.0, S1, ((0.9, -2.3, 0.5), (0.2, -0.3, 0.45)), ((0.7, -2.1, 0.55), (0.2, -0.3, 0.5)))          # respinga na base, umidade
corte(S1, DUR, OLHO_A, ((-0.2, -3.7, 1.7), (0.5, CY, 2.1)))                                            # COM CALHA: fachada seca
for o in (sc.camera, bpy.data.objects['alvo']):
    ac = o.animation_data.action
    for fc in getattr(ac, 'fcurves', []):
        for k in fc.keyframe_points: k.interpolation = 'LINEAR'

sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.6
finalizar(AQUI)
