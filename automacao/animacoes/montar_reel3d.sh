#!/bin/bash
# uso: ./montar_reel3d.sh pasta   -> pasta/MOVE_explica.mp4 (quadros 12 qps -> 24 qps interpolado + cartões + efeitos + música)
set -e
cd "$(dirname "$0")/$1"
ffmpeg -y -loglevel error -framerate 12 -pattern_type glob -i 'frames/*.jpg' -vf "minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,scale=1080:1920:flags=lanczos" -c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p anim24.mp4
python3 ../../../kit_instagram/scripts/efeitos_sonoros.py efeitos.json 22.8 sfx.wav
MARCA=marca_move.json python3 ../../../kit_instagram/scripts/montar_explicativo.py montagem.json MOVE_explica.mp4
