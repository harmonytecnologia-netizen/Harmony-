import bpy, math, sys, os
from mathutils import Vector
OUT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene; sc.render.fps=24; sc.frame_start=1; sc.frame_end=720
def mat(name,col,rough=.4,metal=0,emit=None,es=4):
    m=bpy.data.materials.new(name); m.use_nodes=True; b=m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=(*col,1); b.inputs['Roughness'].default_value=rough; b.inputs['Metallic'].default_value=metal
    if emit: b.inputs['Emission Color'].default_value=(*emit,1); b.inputs['Emission Strength'].default_value=es
    return m
M=dict(body=mat('body',(0.035,0.045,0.045),.3),mint=mat('mint',(0.2,0.75,0.55),.25,emit=(0.27,0.85,0.65),es=.6),
 cone=mat('cone',(0.012,0.014,0.014),.75),white=mat('white',(0.92,0.92,0.9),.25),black=mat('black',(0,0,0),.15),
 floor=mat('floor',(0.015,0.02,0.02),.25),metal=mat('metal',(0.6,0.6,0.6),.25,1),
 red=mat('red',(0.9,0.12,0.08),.35),wht=mat('wht',(0.85,0.85,0.82),.35),org=mat('org',(1.0,0.55,0.1),.35),
 gold=mat('gold',(0.9,0.65,0.25),.2,1))
# face material animated (green->red)
face=mat('face',(0,0,0),.4,emit=(0.27,0.85,0.65),es=3)
def sel(o): bpy.context.view_layer.objects.active=o
def smooth(o):
    for p in o.data.polygons: p.use_smooth=True
def add_bevel(o,w,seg=6):
    b=o.modifiers.new('b','BEVEL'); b.width=w; b.segments=seg; smooth(o)
def parent(c,p):
    c.parent=p; c.matrix_parent_inverse=p.matrix_world.inverted()

# floor + world
bpy.ops.mesh.primitive_plane_add(size=60,location=(0,0,0)); bpy.context.object.data.materials.append(M['floor'])
w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; w.node_tree.nodes['Background'].inputs[0].default_value=(0.003,0.005,0.005,1)

# ---------- AMPLIFIER ----------
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,2.4,0.5)); ped=bpy.context.object; ped.scale=(3.0,1.3,1.0); ped.data.materials.append(M['body']); add_bevel(ped,0.05)
bpy.ops.object.empty_add(location=(0,0,0)); AMP=bpy.context.object; AMP.name='AMP'
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,2.4,1.55)); a=bpy.context.object; a.scale=(2.6,1.0,1.0); a.data.materials.append(M['body']); add_bevel(a,0.1); parent(a,AMP)
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,1.88,1.62)); d=bpy.context.object; d.scale=(1.5,0.05,0.55); d.data.materials.append(M['black']); add_bevel(d,0.04); parent(d,AMP)
eyes=[]
for x in (-0.3,0.3):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1,location=(x,1.84,1.72)); e=bpy.context.object; e.scale=(1,0.3,1.3); e.data.materials.append(face); smooth(e); parent(e,AMP); eyes.append(e)
# mouths: smile / frown as torus halves
def mouth(up,name):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.22,minor_radius=0.035,location=(0,1.84,1.5 if up else 1.38),rotation=(math.pi/2,0,0))
    m=bpy.context.object; m.name=name; m.data.materials.append(face); smooth(m)
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='DESELECT'); bpy.ops.object.mode_set(mode='OBJECT')
    for v in m.data.vertices:
        if (v.co.y>0) if up else (v.co.y<0): v.select=True
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.delete(type='VERT'); bpy.ops.object.mode_set(mode='OBJECT')
    parent(m,AMP); return m
smile=mouth(True,'smile'); frown=mouth(False,'frown')
for x in (-1.05,1.05):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.13,depth=0.08,location=(x,1.88,1.7),rotation=(math.pi/2,0,0)); k=bpy.context.object; k.data.materials.append(M['metal']); parent(k,AMP)
# amp terminals on top front
AT={}
for nm,x,mt in (('+',-0.35,'red'),('-',0.35,'wht')):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07,depth=0.16,location=(x,2.1,2.1)); t=bpy.context.object; t.data.materials.append(M[mt]); parent(t,AMP)
    AT[nm]=Vector((x,2.1,2.18))
# LED
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05,location=(1.05,1.88,1.35)); led=bpy.context.object; ledm=mat('led',(0,0,0),.3,emit=(1,0.1,0.05),es=0); led.data.materials.append(ledm); parent(led,AMP)

# ---------- SPEAKERS ----------
SX=[-1.65,-0.55,0.55,1.65]; SPK=[]; ST=[]
for i,x in enumerate(SX):
    bpy.ops.object.empty_add(location=(x,-0.6,0)); E=bpy.context.object; E.name=f'SPK{i}'
    bpy.ops.mesh.primitive_cube_add(size=1,location=(x,-0.6,0.72)); b=bpy.context.object; b.scale=(0.9,0.75,1.4); b.data.materials.append(M['body']); add_bevel(b,0.11); parent(b,E)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.3,minor_radius=0.04,location=(x,-0.985,0.5),rotation=(math.pi/2,0,0)); r=bpy.context.object; r.data.materials.append(M['mint']); smooth(r); parent(r,E)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.28,location=(x,-0.93,0.5)); c=bpy.context.object; c.scale=(1,0.3,1); c.data.materials.append(M['cone']); smooth(c); parent(c,E)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.07,location=(x,-1.0,0.5)); dc=bpy.context.object; dc.data.materials.append(M['metal']); smooth(dc); parent(dc,E)
    ee=[]
    for dx in (-0.18,0.18):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11,location=(x+dx,-0.98,1.07)); e=bpy.context.object; e.scale=(1,0.45,1.25); e.data.materials.append(M['white']); smooth(e); parent(e,E)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05,location=(x+dx+0.015,-1.03,1.05)); p=bpy.context.object; p.data.materials.append(M['black']); smooth(p); parent(p,E); ee.append((e,p))
    T={}
    for nm,dx,mt in (('+',-0.2,'red'),('-',0.2,'wht')):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.055,depth=0.12,location=(x+dx,-0.6,1.48)); t=bpy.context.object; t.data.materials.append(M[mt]); parent(t,E)
        T[nm]=Vector((x+dx,-0.6,1.54))
    # 8 ohm plate
    bpy.ops.mesh.primitive_cube_add(size=1,location=(x,-0.985,0.1)); pl=bpy.context.object; pl.scale=(0.4,0.02,0.12); pl.data.materials.append(M['mint']); parent(pl,E)
    SPK.append((E,ee)); ST.append(T)

# ---------- CABLES ----------
def cable(p0,p1,matname,lift=0.9,bev=0.035):
    cu=bpy.data.curves.new('c','CURVE'); cu.dimensions='3D'; cu.bevel_depth=bev; cu.bevel_resolution=4; cu.use_fill_caps=True
    sp=cu.splines.new('BEZIER'); sp.bezier_points.add(1)
    a,b=sp.bezier_points
    a.co=p0; b.co=p1
    mid=(p0+p1)/2; up=Vector((0,0,lift))
    a.handle_right=p0+up+(mid-p0)*0.3; a.handle_left=p0-up
    b.handle_left=p1+up+(mid-p1)*0.3; b.handle_right=p1-up
    o=bpy.data.objects.new('cable',cu); sc.collection.objects.link(o); o.data.materials.append(M[matname])
    cu.bevel_factor_end=0.0; cu.keyframe_insert('bevel_factor_end',frame=1)
    # plug at end
    bpy.ops.mesh.primitive_cylinder_add(radius=bev*2.2,depth=0.12,location=p1+Vector((0,0,0.08))); g=bpy.context.object; g.data.materials.append(M['gold']); g.scale=(0,0,0)
    g.keyframe_insert('scale',frame=1)
    return o,g
def grow(cab,f0,f1):
    o,g=cab; cu=o.data
    cu.bevel_factor_end=0; cu.keyframe_insert('bevel_factor_end',frame=f0)
    cu.bevel_factor_end=1; cu.keyframe_insert('bevel_factor_end',frame=f1)
    g.scale=(0,0,0); g.keyframe_insert('scale',frame=f1-1)
    g.scale=(1.3,1.3,1.3); g.keyframe_insert('scale',frame=f1+2)
    g.scale=(1,1,1); g.keyframe_insert('scale',frame=f1+5)
def shrink(cab,f0,f1):
    o,g=cab; cu=o.data
    cu.bevel_factor_end=1; cu.keyframe_insert('bevel_factor_end',frame=f0)
    cu.bevel_factor_end=0; cu.keyframe_insert('bevel_factor_end',frame=f1)
    g.scale=(1,1,1); g.keyframe_insert('scale',frame=f0)
    g.scale=(0,0,0); g.keyframe_insert('scale',frame=f0+3)

EVENTS=[]  # (frame, sfx)
# parallel: 4 red + 4 white
par=[]
for i in range(4):
    par.append(cable(AT['+'],ST[i]['+'],'red',0.6+0.12*i))
    par.append(cable(AT['-'],ST[i]['-'],'wht',0.6+0.12*i))
for j,c in enumerate(par):
    f0=220+j*9; grow(c,f0,f0+16); EVENTS.append((f0+16,'click'))
for c in par: shrink(c,360,378)
# series-parallel
sp=[cable(AT['+'],ST[0]['+'],'red',1.1),
    cable(ST[0]['-'],ST[1]['+'],'org',0.45),
    cable(ST[1]['-'],AT['-'],'wht',1.0),
    cable(AT['+'],ST[2]['+'],'red',1.1),
    cable(ST[2]['-'],ST[3]['+'],'org',0.45),
    cable(ST[3]['-'],AT['-'],'wht',1.0)]
for j,c in enumerate(sp):
    f0=392+j*13; grow(c,f0,f0+18); EVENTS.append((f0+18,'click'))

# ---------- ANIMATION: speakers pop / blink / bob ----------
for i,(E,ee) in enumerate(SPK):
    E.scale=(0,0,0); E.keyframe_insert('scale',frame=1); E.keyframe_insert('scale',frame=100+i*10)
    E.scale=(1.15,1.15,1.15); E.keyframe_insert('scale',frame=110+i*10)
    E.scale=(1,1,1); E.keyframe_insert('scale',frame=116+i*10)
    EVENTS.append((106+i*10,'pop'))
    for f in range(130,720,70+i*7):
        for e,p in ee:
            e.scale=(1,0.45,1.25); e.keyframe_insert('scale',frame=f)
            e.scale=(1,0.45,0.1); e.keyframe_insert('scale',frame=f+2)
            e.scale=(1,0.45,1.25); e.keyframe_insert('scale',frame=f+5)
# amp mood: hot in 1..96 and 300..470, cool otherwise
fe=face.node_tree.nodes['Principled BSDF'].inputs['Emission Color']
GREEN=(0.27,0.85,0.65,1); RED=(1.0,0.015,0.005,1)
def mood(f,hot):
    fe.default_value=RED if hot else GREEN; fe.keyframe_insert('default_value',frame=f)
    smile.hide_render= hot; smile.keyframe_insert('hide_render',frame=f)
    frown.hide_render= not hot; frown.keyframe_insert('hide_render',frame=f)
mood(1,True); mood(90,True); mood(100,False); mood(300,False); mood(320,True); mood(480,True); mood(505,False)
le=ledm.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']
for f in range(1,720,8):
    hot = f<96 or 310<=f<490
    le.default_value= (12 if (f//8)%2==0 else 0) if hot else 0; le.keyframe_insert('default_value',frame=f)
# shake when hot
for f in range(1,720,2):
    hot = f<96 or 320<=f<480
    AMP.location=(0.04*math.sin(f*2.3) if hot else 0, 0, 0); AMP.keyframe_insert('location',frame=f)
EVENTS += [(10,'alarm'),(320,'alarm'),(505,'ding')]

# ---------- LIGHTS ----------
def area(loc,rot,en,size,col=(1,1,1)):
    bpy.ops.object.light_add(type='AREA',location=loc); L=bpy.context.object; L.data.energy=en; L.data.size=size; L.data.color=col; L.rotation_euler=[math.radians(r) for r in rot]; return L
area((3,-5,6),(45,0,30),1400,5)
area((-5,0,3),(70,0,-100),500,4,(0.3,0.9,0.7))
area((0,5,4),(-60,0,180),600,5,(0.5,0.7,1.0))

# ---------- CAMERA ----------
bpy.ops.object.empty_add(location=(0,0.6,0.9)); TGT=bpy.context.object
bpy.ops.object.camera_add(); cam=bpy.context.object; sc.camera=cam; cam.data.lens=35
tc=cam.constraints.new('TRACK_TO'); tc.target=TGT; tc.track_axis='TRACK_NEGATIVE_Z'; tc.up_axis='UP_Y'
def camk(f,loc,tgt,lens):
    cam.location=loc; cam.keyframe_insert('location',frame=f)
    TGT.location=tgt; TGT.keyframe_insert('location',frame=f)
    cam.data.lens=lens; cam.data.keyframe_insert('lens',frame=f)
camk(1,(1.0,-2.2,2.5),(0,2.2,1.6),35); camk(90,(0.6,-1.4,2.3),(0,2.2,1.6),38)
camk(115,(0,-9.2,5.6),(0,0.8,1.2),38); camk(300,(0.5,-8.8,5.8),(0,0.8,1.2),38)
camk(330,(0.2,-8.0,5.0),(0,0.9,1.3),38); camk(500,(-0.5,-8.4,5.9),(0,0.8,1.2),38)
camk(560,(0,-8.8,5.3),(0,0.8,1.2),38); camk(720,(1.2,-7.6,4.4),(0,0.9,1.3),38)
for fc in (cam.animation_data.action.fcurves if cam.animation_data and hasattr(cam.animation_data.action,'fcurves') else []):
    for k in fc.keyframe_points: k.interpolation='BEZIER'

# ---------- RENDER SETTINGS ----------
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=int(os.environ.get('SAMPLES',10)); sc.cycles.use_denoising=True
sc.cycles.max_bounces=4; sc.cycles.diffuse_bounces=2; sc.cycles.glossy_bounces=2; sc.cycles.transmission_bounces=0
sc.render.resolution_x=540; sc.render.resolution_y=960; sc.render.image_settings.file_format='JPEG'; sc.render.image_settings.quality=94
sc.view_settings.view_transform='Standard'; sc.view_settings.look='Medium High Contrast'
import json; json.dump(sorted(EVENTS),open(os.path.join(OUT,'events.json'),'w'))
mode=sys.argv[-1]
if mode=='save':
    sc.cycles.device='GPU'; sc.cycles.samples=64; sc.render.resolution_x=1080; sc.render.resolution_y=1920
    sc.render.filepath='//frames/####'; sc.render.image_settings.file_format='JPEG'; sc.render.image_settings.quality=95
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'pacote','MOVE_cena_impedancia.blend')); sys.exit(0)
if mode.startswith('test'):
    for f in [int(x) for x in mode.split(':')[1].split(',')]:
        sc.frame_set(f); sc.render.filepath=os.path.join(OUT,f'test_{f:04d}.jpg'); bpy.ops.render.render(write_still=True)
else:
    a,b=[int(x) for x in mode.split(':')]
    step=int(os.environ.get('STEP',1))
    for f in range(a,b+1,step):
        p=os.path.join(OUT,'frames',f'{f:04d}.jpg')
        if os.path.exists(p): continue
        sc.frame_set(f); sc.render.filepath=p; bpy.ops.render.render(write_still=True)
