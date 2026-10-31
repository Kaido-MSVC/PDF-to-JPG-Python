# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Kaido-MSVC
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
# Keep the PyInstaller cache and generated files in this project.
$env:PYINSTALLER_CONFIG_DIR = Join-Path $PSScriptRoot 'work\pyinstaller-cache'
# Always use this project's .venv (Python 3.13), never the global `python`.
$venvPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $venvPython)) {
    throw '.venv not found. Create it: py -3.13 -m venv .venv; .venv\Scripts\python.exe -m pip install -r requirements-lock.txt'
}
function python { & $venvPython @args }
python -c "import sys,importlib.metadata as m; assert sys.version_info[:2] == (3,13); expected={'customtkinter':'6.0.0','pymupdf':'2.0','pillow':'13.0.0','pyinstaller':'6.22.3'}; actual={k:m.version(k) for k in expected}; print(actual); assert actual == expected, 'Package version mismatch'"
if ($LASTEXITCODE -ne 0) { throw 'Python or package version mismatch.' }
python -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw 'Tests failed.' }
python make_icon.py
if ($LASTEXITCODE -ne 0) { throw 'Icon generation failed.' }
python -m PyInstaller --noconfirm --distpath dist --workpath work\build PDF-to-JPG.spec
if ($LASTEXITCODE -ne 0) { throw 'EXE build failed.' }
Write-Host 'Built: dist\PDF-to-JPG.exe'
