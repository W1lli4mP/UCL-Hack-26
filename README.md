**Setup & Run**

- Windows (PowerShell):
	1. Install Python from https://python.org/downloads
	2. In the repo folder, run:
		 - `py -m venv .venv`
		 - `.\.venv\Scripts\Activate.ps1`
		 - `py -m pip install --upgrade pip`
		 - `py -m pip install -r requirements.txt`
		 - `py -m streamlit run app.py`

- macOS (zsh):
	- `python3 -m venv .venv`
	- `source .venv/bin/activate`
	- `python3 -m pip install --upgrade pip`
	- `python3 -m pip install -r requirements.txt`
	- `python3 -m streamlit run app.py`

Troubleshooting: If you see `No Python at "/opt/anaconda3/bin\python.exe"`, VS Code is pointing to a macOS Anaconda path. Fix by:

- Open Command Palette → `Python: Select Interpreter` → choose the `.venv` interpreter for this workspace:
	- Windows: `.venv\\Scripts\\python.exe`
	- macOS: `.venv/bin/python`
- Or open `.vscode/settings.json` and ensure:
	- `"python.venvPath": "${workspaceFolder}"`
	- `"python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"`

Notes: This repo stays private until the hackathon is over.
