"""Narracao gratis em portugues com Piper TTS.
uso: python3 narracao.py "texto da fala" saida.wav [velocidade]
velocidade: 1.0 normal, 0.9 mais rapido, 1.1 mais devagar.
Modelo: pt_BR-faber-medium (.onnx + .onnx.json). Procura em ./modelos ou na variavel PIPER_MODELO.
Se nao tiver: baixar de https://huggingface.co/rhasspy/piper-voices/tree/main/pt/pt_BR/faber/medium
(se o ambiente bloquear o download, baixar pelo navegador da pessoa e anexar).
"""
import sys, os, subprocess, glob
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mod = os.environ.get('PIPER_MODELO') or next(iter(glob.glob(os.path.join(KIT, 'modelos', '*.onnx'))), None)
if not mod: sys.exit('Modelo de voz nao encontrado: coloque pt_BR-faber-medium.onnx e .onnx.json em kit/modelos/')
texto, out = sys.argv[1], sys.argv[2]; vel = sys.argv[3] if len(sys.argv) > 3 else '1.0'
r = subprocess.run([sys.executable, '-m', 'piper', '-m', mod, '--length-scale', vel, '-f', out], input=texto, text=True)
if r.returncode == 0:
    d = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout.strip()
    print(f'ok {out} {d}s')
sys.exit(r.returncode)
