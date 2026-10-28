#!/bin/bash
# Mac: 双击运行
cd "$(dirname "$0")"
python3 peps_piscine.py "$@"
open .
