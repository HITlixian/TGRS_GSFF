#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python main.py --dataset ZJK_10 --test --grid "$@"
