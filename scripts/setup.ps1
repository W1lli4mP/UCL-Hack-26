# scripts/setup.ps1
$ErrorActionPreference = "Stop"

# create venv if it doesn't exist
if (!(Test-Path ".venv")) {
  python -m venv .venv
}

# upgrade pip and install deps
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\pip install -r requirements.txt

Write-Host ""
Write-Host "Setup complete."