# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

root = Path(SPECPATH)
datas = collect_data_files('customtkinter') + [
    (str(root / 'assets'), 'assets'),
    (str(root / 'LICENSE'), '.'),
    (str(root / 'THIRD-PARTY-NOTICES.md'), '.'),
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
