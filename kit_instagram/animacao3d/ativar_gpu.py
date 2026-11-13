# Roda DENTRO do Blender antes de renderizar: liga a placa de video (OptiX/CUDA/HIP/Metal) e ajusta qualidade x tempo.
# uso: blender -b cena.blend -P ativar_gpu.py -a
import bpy, os
prefs = bpy.context.preferences.addons['cycles'].preferences
usado = 'CPU'
for tipo in ('OPTIX', 'CUDA', 'HIP', 'METAL', 'ONEAPI'):
    try:
        prefs.compute_device_type = tipo; prefs.refresh_devices()
        if any(d.type == tipo for d in prefs.devices): usado = tipo; break
    except TypeError:
        pass
for d in prefs.devices: d.use = d.type in (usado, 'CPU')
sc = bpy.context.scene; sc.render.engine = 'CYCLES'
sc.cycles.device = 'GPU' if usado != 'CPU' else 'CPU'
sc.render.resolution_x, sc.render.resolution_y = int(os.environ.get('LARG', 720)), int(os.environ.get('ALT', 1280))
sc.cycles.samples = int(os.environ.get('AMOSTRAS', 24)); sc.cycles.use_adaptive_sampling = True; sc.cycles.use_denoising = True
try: sc.cycles.denoiser = 'OPTIX' if usado == 'OPTIX' else 'OPENIMAGEDENOISE'
except Exception: pass
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 92
sc.render.filepath = '//quadros/####'; sc.render.use_overwrite = False; sc.render.use_placeholder = True
open(bpy.path.abspath('//gpu_status.txt'), 'w').write(f'{usado}: ' + ', '.join(d.name for d in prefs.devices if d.use))
print('RENDER COM', usado)
