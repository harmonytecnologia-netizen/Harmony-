#!/bin/bash
cd "$(dirname "$0")"
for d in "$@"; do
  until grep -q FIM $d/render.log 2>/dev/null; do sleep 30; done
  nice -n 5 ./montar_reel3d.sh $d > $d/montar.log 2>&1; echo PRONTO >> $d/montar.log
done
