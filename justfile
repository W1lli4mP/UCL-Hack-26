# justfile
@default:
    just --list

# detect Windows via env var OS=Windows_NT
is_windows := env_var_or_default("OS", "") == "Windows_NT"

setup:
    {{ if is_windows { "powershell -NoProfile -ExecutionPolicy Bypass -File scripts\\setup.ps1" } else { "bash scripts/setup.sh" } }}

run:
    {{ if is_windows { "powershell -NoProfile -ExecutionPolicy Bypass -File scripts\\run.ps1" } else { "bash scripts/run.sh" } }}
