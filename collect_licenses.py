# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Kaido-MSVC
"""Copy the license files of every bundled third-party component into ./licenses.

Run with the project's .venv:  .venv\\Scripts\\python.exe collect_licenses.py
The result is committed and embedded in the EXE (see PDF-to-JPG.spec).
"""
import importlib.metadata as md
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'licenses'

# distribution name -> folder name in ./licenses
PACKAGES = {
    'pymupdf': 'PyMuPDF',
    'pillow': 'Pillow',
    'customtkinter': 'CustomTkinter',
    'darkdetect': 'darkdetect',
    'numpy': 'NumPy',
    'packaging': 'packaging',
    'psutil': 'psutil',
    'PyYAML': 'PyYAML',
    'pyinstaller': 'PyInstaller',
}
LICENSE_HINTS = ('license', 'copying', 'notice')


def license_files(dist):
    for f in dist.files or ():
        parts = Path(str(f)).parts
        if '.dist-info' not in parts[0]:
            continue
        rel = Path(*parts[1:])
        if parts[1:2] == ('licenses',) or any(h in rel.name.lower() for h in LICENSE_HINTS):
            yield Path(dist.locate_file(f)), Path(*parts[2:]) if parts[1] == 'licenses' else rel


def copy(src, dst):
    if not src.is_file():
        raise SystemExit(f'Missing license file: {src}')
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    print(f'{src} -> {dst.relative_to(ROOT)}')


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    for dist_name, folder in PACKAGES.items():
        dist = md.distribution(dist_name)
        found = list(license_files(dist))
        if not found:
            raise SystemExit(f'No license files found for {dist_name}')
        for src, rel in found:
            copy(src, OUT / f'{folder}-{dist.version}' / rel)

    base = Path(sys.base_prefix)
    # Python's LICENSE.txt also carries the notices of bundled libraries
    # (OpenSSL, libffi, bzip2, zlib, Tcl/Tk, ...) and the MSVC runtime terms.
    copy(base / 'LICENSE.txt', OUT / f'Python-{sys.version.split()[0]}' / 'LICENSE.txt')
    copy(base / 'tcl' / 'tk8.6' / 'license.terms', OUT / 'Tcl-Tk-8.6' / 'license.terms')

    # Roboto (shipped inside CustomTkinter) states "Licensed under the Apache
    # License, Version 2.0" in its font metadata; packaging ships that exact text.
    apache = OUT / f'packaging-{md.version("packaging")}' / 'LICENSE.APACHE'
    copy(apache, OUT / 'Roboto' / 'LICENSE-Apache-2.0.txt')


if __name__ == '__main__':
    main()
