#!/bin/bash
# renderiza em sequência as cenas passadas (pastas), 12 qps (STEP=2), SAMPLES=8
cd "$(dirname "$0")"
for d in "$@"; do
  while pgrep -f "cena.py 1:516" >/dev/null; do sleep 20; done
  (cd "$d" && SAMPLES=8 STEP=2 python3 cena.py 1:516 > render.log 2>&1; echo FIM >> render.log)
done
