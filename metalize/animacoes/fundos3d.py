# Fundos 3D premium da Metalize (stills 9:16). uso: python3 fundos3d.py <cena> <saida.jpg>
# cenas: calha, portao, escada, guarda_corpo, pergolado, galpao, chapa
import sys, math, os
sys.path.insert(0, '/home/claude/harmony-/automacao/animacoes')
import bpy
from lib3d import iniciar, mat, cube, cil, M, camera, T

cena, out = sys.argv[-2], sys.argv[-1]
iniciar(1)
QUENTE = (1.0, 0.72, 0.45)
M['piso'] = mat('piso', (0.02, 0.02, 0.021), 0.22, clearcoat=0.5)
M['concreto'] = mat('concreto', (0.32, 0.31, 0.29), 0.85)
M['parede_clara'] = mat('parede', (0.55, 0.53, 0.5), 0.8)
M['preto'] = mat('aco_preto', (0.02, 0.02, 0.022), 0.38, metal=0.9, clearcoat=0.3)
M['inox'] = mat('inox', (0.72, 0.72, 0.74), 0.18, metal=1.0)
M['cobre'] = mat('galvalume', (0.62, 0.63, 0.65), 0.3, metal=1.0)
M['madeira'] = mat('madeira', (0.2, 0.095, 0.045), 0.4, clearcoat=0.4)
M['vidro'] = mat('vidro', (0.6, 0.7, 0.7), 0.02, metal=0.0)
b = M['vidro'].node_tree.nodes['Principled BSDF']; b.inputs['Transmission Weight'].default_value = 1.0; b.inputs['IOR'].default_value = 1.45
M['corten'] = mat('corten', (0.35, 0.12, 0.04), 0.75, metal=0.3)
os.environ.setdefault('TRANS', '2')

def area(loc, rot, en, cor, tam):
    l = bpy.data.lights.new('a', 'AREA'); l.energy = en; l.color = cor; l.size = tam
    o = bpy.data.objects.new('a', l); o.location = loc; o.rotation_euler = [math.radians(r) for r in rot]; bpy.context.collection.objects.link(o)

def mundo(f=0.03, cor=(0.6, 0.7, 0.85)):
    w = bpy.data.worlds.new('w'); bpy.context.scene.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']; bg.inputs['Strength'].default_value = f; bg.inputs['Color'].default_value = (*cor, 1)

def piso():
    bpy.ops.mesh.primitive_plane_add(size=60); bpy.context.object.data.materials.append(M['piso'])

kc = camera(lente=35, fstop=2.8)

if cena == 'calha':
    piso(); mundo(0.25, (0.45, 0.55, 0.75))
    cube('parede', (0, 0.6, 1.4), (5, 0.5, 1.4), M['parede_clara'])
    # telhado metálico escuro
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 1.2, 3.05)); r = bpy.context.object; r.scale = (5, 1.3, 1); r.rotation_euler = (math.radians(-17), 0, 0); r.data.materials.append(M['preto'])
    for i in range(-10, 11):
        cube(f'onda{i}', (i * 0.45, 1.2, 3.07), (0.02, 1.25, 0.02), M['preto']).rotation_euler = (math.radians(-17), 0, 0)
    # calha de cobre
    cube('fundo', (0, -0.18, 2.62), (5, 0.12, 0.008), M['cobre'])
    cube('frente', (0, -0.3, 2.72), (5, 0.008, 0.1), M['cobre'], 0.004)
    cube('tras', (0, -0.06, 2.72), (5, 0.008, 0.1), M['cobre'])
    cil('condutor', (1.6, -0.18, 1.3), 0.06, 2.6, M['cobre'], rot=(0, 0, 0))
    area((-2, -3, 4), (55, 0, -30), 400, QUENTE, 3); area((3, -1, 1), (80, 0, 70), 150, (0.6, 0.75, 1.0), 2)
    kc(0, (-0.9, -1.6, 2.35), (0.7, -0.2, 2.65))
elif cena == 'portao':
    piso(); mundo(0.02)
    cube('muro', (0, 0.3, 1.5), (4, 0.25, 1.5), M['concreto'])
    for i in range(24):
        x = -1.6 + i * 0.14
        cube(f'lam{i}', (x, 0.0, 1.25), (0.045, 0.03, 1.2), M['preto'] if i % 6 else M['madeira'], 0.004)
    cube('trilho', (0, 0, 0.03), (1.8, 0.04, 0.03), M['inox'])
    area((-1.5, -2.5, 3), (50, 0, -25), 300, QUENTE, 1.5)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -0.15, 2.55)); f = bpy.context.object; f.scale = (1.8, 0.02, 1)
    f.data.materials.append(mat('led', (0, 0, 0), emis=QUENTE, es=8))
    kc(0, (-1.4, -3.4, 1.0), (0.1, 0, 1.3))
elif cena == 'escada':
    piso(); mundo(0.03)
    cube('parede', (0, 0.4, 2), (3, 0.1, 2), M['concreto'])
    cube('viga', (0, 0.12, 1.5), (0.04, 0.04, 2.1), M['preto']).rotation_euler = (0, math.radians(-50), 0)
    for i in range(12):
        x = -1.2 + i * 0.24; z = 0.18 + i * 0.19
        cube(f'deg{i}', (x, 0.0, z), (0.14, 0.4, 0.025), M['madeira'], 0.006)
        cube(f'sup{i}', (x, 0.25, z - 0.04), (0.12, 0.12, 0.015), M['preto'])
    for i in range(7):
        cil(f'cabo{i}', (-1.2 + i * 0.45, -0.38, 1.6), 0.005, 3.2, M['inox'], rot=(0, 0, 0))
    area((-2, -2, 3.5), (45, 0, -35), 350, QUENTE, 2); area((2, -1, 4), (30, 0, 40), 120, (0.7, 0.8, 1.0), 2)
    kc(0, (-1.9, -3.2, 1.2), (0.0, 0.0, 1.3))
elif cena == 'guarda_corpo':
    mundo(0.6, (0.55, 0.65, 0.85))
    cube('laje', (0, 0.5, -0.1), (4, 2.5, 0.1), M['concreto'])
    bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 0, -6)); bpy.context.object.data.materials.append(mat('mar', (0.02, 0.08, 0.12), 0.05))
    cube('vidro', (0, -1.95, 0.55), (3.5, 0.01, 0.55), M['vidro'])
    cube('corrimao', (0, -1.95, 1.12), (3.5, 0.03, 0.02), M['inox'], 0.01)
    for i in range(-3, 4):
        cube(f'botao{i}', (i * 1.0, -1.93, 0.15), (0.03, 0.02, 0.06), M['inox'])
    area((-3, -5, 6), (40, 0, -30), 800, QUENTE, 4)
    kc(0, (-2.6, -0.6, 1.5), (0.6, -2.0, 0.8))
elif cena == 'pergolado':
    piso(); mundo(0.5, (0.5, 0.6, 0.8))
    for x in (-1.5, 1.5):
        for y in (-1.0, 1.0): cube(f'pil{x}{y}', (x, y, 1.3), (0.05, 0.05, 1.3), M['preto'])
    for i in range(14):
        cube(f'rip{i}', (-1.6 + i * 0.246, 0, 2.62), (0.03, 1.15, 0.06), M['preto'])
    cube('banco', (0, 0.3, 0.22), (1.0, 0.25, 0.04), M['madeira'], 0.01)
    area((2, -1, 6), (15, 0, 30), 900, QUENTE, 1.0)
    kc(0, (-2.4, -3.6, 1.1), (0.2, 0, 1.5))
elif cena == 'galpao':
    # galpão metálico ao entardecer: pórticos, terças, contraventamento em X e cobertura em galvalume
    piso(); mundo(0.35, (0.75, 0.55, 0.45))
    vao, alt, n = 4.0, 2.6, 7
    inc = math.radians(15)
    for k in range(n):
        y = k * 1.6
        for s in (-1, 1):
            cube(f'col{k}{s}', (s * vao, y, alt / 2), (0.07, 0.11, alt / 2), M['preto'])
            # tesoura/viga inclinada até a cumeeira
            L = vao / math.cos(inc)
            v = cube(f'viga{k}{s}', (s * vao / 2, y, alt + math.tan(inc) * vao / 2), (L / 2, 0.08, 0.1), M['preto'])
            v.rotation_euler = (0, s * inc, 0)
    comp = (n - 1) * 1.6
    for j in range(-4, 5):  # terças
        x = j * vao / 4.4; z = alt + 0.14 + math.tan(inc) * (vao - abs(x))
        cube(f'terca{j}', (x, comp / 2, z), (0.03, comp / 2 + 0.3, 0.04), M['inox'])
    for s in (-1, 1):  # contraventamento em X nas laterais do 1º vão
        for d in (-1, 1):
            b = cube(f'x{s}{d}', (s * vao, 0.8, alt / 2), (0.012, math.hypot(1.6, alt) / 2, 0.012), M['inox'])
            b.rotation_euler = (d * math.atan2(alt, 1.6), 0, 0)
    # cobertura: só a metade de trás coberta, para mostrar a estrutura na frente
    for s in (-1, 1):
        L = vao / math.cos(inc) + 0.3
        t = cube(f'telha{s}', (s * vao / 2, (comp + 1.6) / 2 + 0.15, alt + 0.2 + math.tan(inc) * vao / 2), (L / 2, (comp - 1.6) / 2 + 0.3, 0.008), M['cobre'])
        t.rotation_euler = (0, s * inc, 0)
    cube('fundo', (0, comp + 0.1, alt / 2), (vao, 0.02, alt / 2), M['concreto'])
    cube('laje', (0, comp / 2, 0.03), (vao + 0.6, comp / 2 + 0.6, 0.03), M['concreto'])
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, comp - 0.05, 0.02)); f = bpy.context.object; f.scale = (vao * 1.6, 0.4, 1)
    f.data.materials.append(mat('luz_int', (0, 0, 0), emis=QUENTE, es=3))
    area((6, -6, 5), (60, 0, 45), 1400, QUENTE, 5); area((-5, 4, 6), (30, 0, -140), 300, (0.6, 0.72, 1.0), 4)
    kc(0, (-6.5, -7.5, 1.7), (0.3, 3.0, 2.6))
else:  # chapa
    mundo(0.0)
    c = cube('chapa', (0, 0, 0), (2, 0.02, 3), mat('escovado', (0.5, 0.5, 0.52), 0.32, metal=1.0))
    for i in range(40):
        cube(f'risco{i}', (0, -0.021, -3 + i * 0.15), (2, 0.0005, 0.002), mat(f'r{i}', (0.7, 0.7, 0.72), 0.15, metal=1.0))
    area((-2.5, -2, 1.5), (80, 0, -60), 250, QUENTE, 0.6); area((2.5, -2, -1), (100, 0, 60), 80, (0.6, 0.75, 1.0), 0.6)
    kc(0, (0.4, -3.0, 0.3), (0, 0, 0))

sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = int(os.environ.get('SAMPLES', 24)); sc.cycles.use_denoising = True
sc.cycles.max_bounces = 6; sc.cycles.transmission_bounces = 4
sc.render.resolution_x = int(os.environ.get('LARG', 720)); sc.render.resolution_y = int(os.environ.get('ALT', 1280))
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 94
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
sc.frame_set(1); sc.render.filepath = out; bpy.ops.render.render(write_still=True)
print('ok', out)
