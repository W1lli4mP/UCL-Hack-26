#!/usr/bin/env bash
set -euo pipefail

if [ ! -d ".venv" ]; then
  echo "venv not found. Run: just setup"
  exit 1
fi

.venv/bin/python -m streamlit run app.py