# Metalize Explica 3D — "Sua calha transborda?" (trajetória da água: telhado -> calha -> condutor)
# uso: python3 cena.py test:1,60,200   |   python3 cena.py 1:540  (env: SAMPLES, LARG, ALT, STEP)
import sys, os, math, random
sys.path.insert(0, '/home/claude/harmony-/automacao/animacoes')
import bpy
from lib3d import iniciar, mat, cube, cil, M, camera, cabo, finalizar, T, FPS

AQUI = os.path.dirname(os.path.abspath(__file__))
DUR = 22.5
sc = iniciar(DUR)
random.seed(7)

# ---------- materiais ----------
M['piso'] = mat('piso', (0.02, 0.02, 0.021), 0.25, clearcoat=0.4)
M['parede'] = mat('parede', (0.5, 0.48, 0.45), 0.85)
M['telha'] = mat('telha', (0.025, 0.026, 0.028), 0.35, metal=0.85)
M['calha'] = mat('calha', (0.62, 0.63, 0.65), 0.3, metal=1.0)  # galvalume
M['agua'] = mat('agua', (0.08, 0.3, 0.5), 0.05, emis=(0.25, 0.6, 0.95), es=0.8, clearcoat=1.0)
M['gota'] = mat('gota', (0.2, 0.5, 0.8), 0.05, emis=(0.35, 0.75, 1.0), es=3.0)
M['trilha'] = mat('trilha', (0, 0, 0), emis=(0.35, 0.8, 1.0), es=6)
M['furo'] = mat('furo', (0.0, 0.0, 0.0), 0.9)

# ---------- cenário ----------
bpy.ops.mesh.primitive_plane_add(size=60); bpy.context.object.data.materials.append(M['piso'])
cube('parede', (0, 0.35, 1.2), (2.7, 0.25, 1.2), M['parede'])
ANG = math.atan2(0.65, 2.15)
bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 1.125, 2.875), rotation=(ANG, 0, 0))
r = bpy.context.object; r.scale = (2.8, 1.12, 1); r.data.materials.append(M['telha'])

def zroof(y):  # altura da superfície do telhado em y
    return 2.55 + (y - 0.05) * (0.65 / 2.15)

# ---------- calha 1 (sem caimento) ----------
L = 2.4
def perfil(pref, parent=None, x0=0.0, z0=0.0):
    ps = [cube(pref + 'fundo', (x0, 0, z0), (L, 0.12, 0.006), M['calha']),
          cube(pref + 'frente', (x0, -0.12, z0 + 0.1), (L, 0.006, 0.1), M['calha'], 0.003),
          cube(pref + 'tras', (x0, 0.12, z0 + 0.1), (L, 0.006, 0.1), M['calha']),
          cube(pref + 'tampaE', (x0 - L, 0, z0 + 0.1), (0.006, 0.12, 0.1), M['calha']),
          cube(pref + 'tampaD', (x0 + L, 0, z0 + 0.1), (0.006, 0.12, 0.1), M['calha'])]
    f = cil(pref + 'bocal', (x0 + 2.1 + (0 if parent is None else 0), 0, z0 + 0.008), 0.045, 0.004, M['furo'], rot=(0, 0, 0))
    ps.append(f)
    if parent:
        for p in ps: p.parent = parent
    return ps

Y = -0.14; Z1 = 2.22
c1 = perfil('c1_')
for p in c1: p.location.y += Y; p.location.z += Z1
# calha 2 (com caimento): pivô na ponta esquerda, desce para o condutor
PHI = math.radians(1.6); ZP = 2.34
piv = bpy.data.objects.new('pivo', None); bpy.context.collection.objects.link(piv)
piv.location = (-L, Y, ZP); piv.rotation_euler = (0, PHI, 0)
c2 = perfil('c2_', piv, x0=L)
def zc2(x): return ZP - (x + L) * math.tan(PHI)
XC = 2.1
cil('condutor', (XC, Y, 1.22), 0.05, 1.96, M['calha'], rot=(0, 0, 0))
cil('cotovelo', (XC, Y - 0.16, 0.2), 0.05, 0.34, M['calha'], rot=(math.pi / 2, 0, 0))
for zb in (0.7, 1.4, 2.0):
    cube(f'abraca{zb}', (XC, Y + 0.06, zb), (0.06, 0.03, 0.012), M['calha'])

def vis(objs, faixas):
    for o in objs:
        for t, v in faixas:
            o.hide_render = not v; o.keyframe_insert('hide_render', frame=max(1, T(t)))
for o in c1: o.hide_render = False
vis(c1, [(0, True), (13.0, False)])
vis(c2, [(0, False), (13.0, True)])

# ---------- água parada na calha 1 ----------
bpy.ops.mesh.primitive_cube_add(); ag = bpy.context.object; ag.data.materials.append(M['agua'])
def nivel(t):
    if t < 4: return 0.19
    if t < 9: return 0.02 + 0.05 * (t - 4) / 5
    if t < 12: return 0.07 + 0.12 * (t - 9) / 3
    return 0.19
NF = int(DUR * FPS)
for f in range(1, NF + 1):
    t = (f - 1) / FPS; h = nivel(t)
    ag.scale = (L - 0.01, 0.112, h / 2); ag.location = (0, Y, Z1 + 0.006 + h / 2)
    ag.keyframe_insert('scale', frame=f); ag.keyframe_insert('location', frame=f)
vis([ag], [(0, True), (13.0, False)])

# ---------- gotas ----------
G = 9.8
LONGE = (0, 0, -5)
def caminho_chuva(x0, ta, t, modo):
    """posição de uma gota nascida em ta no topo do telhado. modo: 'plana' ou 'caimento'."""
    s = t - ta
    if s < 0: return None
    if s < 0.9:  # escorre pelo telhado
        y = 2.0 - (2.0 - 0.05) * (s / 0.9) ** 1.4
        return (x0, y, zroof(y) + 0.02)
    s -= 0.9
    zfundo = (Z1 + 0.02) if modo == 'plana' else zc2(x0) + 0.02
    if s < 0.22:  # cai na calha
        k = s / 0.22
        return (x0, 0.05 + (Y - 0.05) * k, 2.57 - (2.57 - zfundo) * k * k)
    s -= 0.22
    if modo == 'plana':
        return None  # some na água parada
    v = 2.6; x = x0 + v * s
    if x < XC: return (x, Y, zc2(x) + 0.02)
    s2 = s - (XC - x0) / v
    if s2 < 0.55: return None  # dentro do condutor
    s3 = s2 - 0.55
    if s3 < 0.5:  # sai no cotovelo e cai
        return (XC, Y - 0.33 - 1.2 * s3, max(0.01, 0.2 - 0.5 * G * s3 * s3))
    return None

def transborda(x0, ta, t):
    s = t - ta
    if s < 0 or s > 0.75: return None
    return (x0, Y - 0.13 - 0.25 * s, max(0.0, 2.43 - 0.5 * G * s * s))

def modo_em(t): return 'caimento' if t >= 13.0 else 'plana'
def enchendo(t): return t < 4 or 11.0 <= t < 13.0

eventos = []  # (tipo, x0, ta, modo)
t = -1.5
while t < DUR:
    for _ in range(2):
        eventos.append(('chuva', random.uniform(-2.2, 1.8), t, modo_em(t + 1.1)))
    t += 0.09
t = -0.8
while t < DUR:
    if enchendo(t):
        eventos.append(('transb', random.uniform(-2.2, 2.2), t, ''))
    t += 0.025

NG = 130
gotas = []
for i in range(NG):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.02, segments=12, ring_count=8, location=LONGE)
    g = bpy.context.object; g.data.materials.append(M['gota']); g.scale = (1, 1, 1.6); gotas.append(g)

for f in range(1, NF + 1):
    t = (f - 1) / FPS; ativos = []
    for tipo, x0, ta, modo in eventos:
        p = caminho_chuva(x0, ta, t, modo) if tipo == 'chuva' else transborda(x0, ta, t)
        if p: ativos.append(p)
    for i, g in enumerate(gotas):
        g.location = ativos[i] if i < len(ativos) else LONGE
        g.keyframe_insert('location', frame=f)
for g in gotas:
    for fc in g.animation_data.action.fcurves if hasattr(g.animation_data.action, 'fcurves') else []:
        for k in fc.keyframe_points: k.interpolation = 'CONSTANT'

# ---------- trilha luminosa (caminho certo da água) ----------
XT = -1.2
pts = [(XT, 2.0, zroof(2.0) + 0.05), (XT, 0.05, 2.62), (XT, Y, zc2(XT) + 0.06), (0.6, Y, zc2(0.6) + 0.06),
       (XC - 0.05, Y, zc2(XC) + 0.06), (XC, Y - 0.09, 1.2), (XC, Y - 0.09, 0.32), (XC, Y - 0.6, 0.2)]
tr, sp = cabo('trilha', pts, M['trilha'], esp=0.008)
tr.data.bevel_factor_mapping_end = 'SPLINE'
for tt, v in ((0, 0.0), (13.6, 0.0), (17.2, 1.0), (DUR, 1.0)):
    tr.data.bevel_factor_end = v; tr.data.keyframe_insert('bevel_factor_end', frame=max(1, T(tt)))
vis([tr], [(0, False), (13.5, True)])

# ---------- luz ----------
def area(loc, rot, en, cor, tam):
    l = bpy.data.lights.new('a', 'AREA'); l.energy = en; l.color = cor; l.size = tam
    o = bpy.data.objects.new('a', l); o.location = loc; o.rotation_euler = [math.radians(v) for v in rot]; bpy.context.collection.objects.link(o)
area((-2.5, -3.5, 4.5), (50, 0, -30), 520, (1.0, 0.78, 0.55), 3)
area((3.2, -1.5, 1.5), (80, 0, 70), 160, (0.55, 0.7, 1.0), 2)
area((0, -2.0, 0.4), (110, 0, 0), 60, (0.55, 0.7, 1.0), 4)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes['Background']; bg.inputs['Strength'].default_value = 0.12; bg.inputs['Color'].default_value = (0.35, 0.45, 0.65, 1)

# ---------- câmera (cortes secos) ----------
kc = camera(lente=34, fstop=4.0)
def corte(t0, t1, a, b):
    kc(t0, *a); kc(t1 - 1 / FPS, *b)
corte(0, 4, ((0.2, -1.9, 3.15), (0.6, -0.15, 2.3)), ((0.1, -1.7, 3.1), (0.6, -0.15, 2.3)))
corte(4, 9, ((-0.6, -4.6, 3.5), (0.2, 0.4, 2.3)), ((0.3, -4.3, 3.6), (0.2, 0.4, 2.35)))
corte(9, 13, ((-1.5, -2.0, 3.25), (0.4, -0.15, 2.3)), ((-1.2, -1.8, 3.2), (0.5, -0.15, 2.3)))
corte(13, 18, ((-2.4, -2.1, 3.2), (-0.3, -0.12, 2.3)), ((0.9, -2.8, 2.6), (2.0, -0.12, 1.4)))
corte(18, DUR, ((0.1, -5.4, 2.9), (0.4, 0.3, 1.8)), ((0.4, -5.1, 2.95), (0.5, 0.3, 1.85)))
cam = sc.camera
for o in (cam, bpy.data.objects['alvo']):
    ac = o.animation_data.action
    for fc in getattr(ac, 'fcurves', []):
        for k in fc.keyframe_points: k.interpolation = 'LINEAR'

finalizar(AQUI)
