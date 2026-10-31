# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

root = Path(SPECPATH)
datas = collect_data_files('customtkinter') + [
    (str(root / 'assets'), 'assets'),
    (str(root / 'LICENSE'), '.'),
    (str(root / 'THIRD-PARTY-NOTICES.md'), '.'),
    (str(root / 'licenses'), 'licenses'),
]
binaries = collect_dynamic_libs('pymupdf')
a = Analysis(
    [str(root / 'app.py')],
    pathex=[str(root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=['pymupdf.mupdf', 'pymupdf.extra', 'PIL.ImageGrab'],
    hookspath=[],
    runtime_hooks=[],
    # Optional layout / LLM / table analysis is not used by page rendering.
    excludes=['pymupdf.layout', 'pymupdf_layout', 'pymupdf4llm', 'pymupdf_fonts',
              'onnxruntime', 'torch', 'tensorflow', 'matplotlib', 'pandas',
              'scipy', 'IPython', 'pytest', 'cv2'],
    noarchive=False,
)
# The Universal CRT (ucrtbase.dll, api-ms-win-*.dll) is part of Windows 10/11.
# PyInstaller would copy it from C:\Windows\System32, which are OS files without
# a redistribution grant, so leave it to the OS.
a.binaries = [b for b in a.binaries
              if not (Path(b[0]).name.lower() == 'ucrtbase.dll'
                      or Path(b[0]).name.lower().startswith('api-ms-win-'))]

# MSVCP140.dll (needed by PyMuPDF) is Microsoft Distributable Code. The VS 2026
# license grants redistribution only for files listed at
# https://aka.ms/vs/18/redistribution, i.e. files under [VS]\VC\redist, so take
# it from the stable (non-preview) VS 2026 Redist folder instead of the
# System32 copy PyInstaller finds. Pinned to version and SHA-256.
import subprocess
MSVC_REDIST_VERSION = '14.51.36231'
MSVCP140_SHA256 = '7c26614e1d733892c2deac7e245ce115504b1d80592dd0a01b08e3e5a55f89ca'


def vs_redist_msvcp140():
    import hashlib, os
    vswhere = Path(os.environ.get('ProgramFiles(x86)', r'C:\Program Files (x86)'),
                   'Microsoft Visual Studio', 'Installer', 'vswhere.exe')
    if not vswhere.is_file():
        raise SystemExit(f'vswhere.exe not found: {vswhere} (Visual Studio 2026 required)')
    roots = subprocess.run(
        [str(vswhere), '-version', '[18.0,19.0)', '-products', '*',
         '-requires', 'Microsoft.VisualStudio.Component.VC.Tools.x86.x64',
         '-property', 'installationPath'],
        capture_output=True, text=True, check=True).stdout.split('\n')
    for vs_root in filter(None, (r.strip() for r in roots)):
        dll = (Path(vs_root) / 'VC' / 'Redist' / 'MSVC' / MSVC_REDIST_VERSION
               / 'x64' / 'Microsoft.VC145.CRT' / 'msvcp140.dll')
        if dll.is_file():
            digest = hashlib.sha256(dll.read_bytes()).hexdigest()
            if digest != MSVCP140_SHA256:
                raise SystemExit(f'{dll}: SHA-256 {digest} != pinned {MSVCP140_SHA256}')
            return dll
    raise SystemExit(f'VS 2026 Redist {MSVC_REDIST_VERSION} x64 msvcp140.dll not found')


msvcp140 = [b for b in a.binaries if b[0].lower() == 'msvcp140.dll']
if len(msvcp140) != 1:
    raise SystemExit(f'Expected one MSVCP140.dll in the bundle, found {msvcp140}')
redist_dll = str(vs_redist_msvcp140())
a.binaries = [(b[0], redist_dll, b[2]) if b[0].lower() == 'msvcp140.dll' else b
              for b in a.binaries]
print(f'MSVCP140.dll from {redist_dll}')
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name='PDF-to-JPG',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    icon=str(root / 'assets' / 'app.ico'),
    version=str(root / 'version_info.txt'),
)
