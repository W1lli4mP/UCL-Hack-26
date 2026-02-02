#!/usr/bin/env bash
set -euo pipefail

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

.venv/bin/python -m pip install -U pip
.venv/bin/pip install -r requirements.txt

echo
echo "Setup complete."