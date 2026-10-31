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
