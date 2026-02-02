# scripts/run.ps1
$ErrorActionPreference = "Stop"

if (!(Test-Path ".venv")) {
  Write-Host "venv not found. Run: just setup"
  exit 1
}

.\.venv\Scripts\python -m streamlit run app.py