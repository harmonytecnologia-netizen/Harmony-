#!/usr/bin/env bash
# Instala o que o kit precisa no ambiente do Claude (Linux). Tudo gratis.
set -e
command -v ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg) || echo "instale o ffmpeg"
pip install -q --break-system-packages pillow numpy librosa piper-tts 2>/dev/null || pip install -q pillow numpy librosa piper-tts
command -v node >/dev/null && (node -e "require('playwright')" 2>/dev/null || npm i -g playwright) || echo "Node ausente: animacao 2D precisa de Node + Playwright"
mkdir -p "$(dirname "$0")/modelos"
echo "Pronto. Falta: modelo de voz em kit/modelos (ver scripts/narracao.py) e o logo.png + marca.json da empresa."
