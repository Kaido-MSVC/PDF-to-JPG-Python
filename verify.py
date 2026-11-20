# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Kaido-MSVC
"""Run focused source, GUI and portable EXE checks without changing packages."""
import argparse
import ctypes
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pefile
from PyInstaller.archive.readers import CArchiveReader

ROOT = Path(__file__).resolve().parent
# SHA-256 of the native members of the verified official PyMuPDF 2.1 Windows x64 wheel.
NATIVE_HASHES = {
    'mupdfcpp64.dll': 'dc45b1d83f15c668f9f85ee92614a31f51c63d22937473fd03ab709a747523c3',
    '_mupdf.pyd': '016a5a99b104c56d3773f3e205fcfd53de8f7096999ece1234392f1a392813a2',
    '_extra.pyd': '6a4893a3771381da3b5ca98aa3cf367756671df50b1165a2c16232615e7f5541',
    '_features.pyd': 'e1816fe79825c2f15d41065ec71a6bf07de5ed684bbaa6fb5be1a4f0b78b2e89',
    '_tgif.pyd': '9480132fe6d17909608a1a3d0fbef3ed63aeed422ddfb305dfbd03974089db1a',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exe', type=Path, default=ROOT / 'dist' / 'PDF-to-JPG.exe')
    parser.add_argument('--unit-test-log', type=Path, help='Reuse the unit test result from build.ps1')
    args = parser.parse_args()
    exe = args.exe.resolve()
    if not exe.is_file():
        raise SystemExit(f'Build {exe} first using build.ps1.')
    run = ROOT / 'work' / ('verify-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
    run.mkdir(parents=True)
    report = {'passed': False, 'exe': str(exe)}
    def execute(command, name, env=None, cwd=ROOT):
        result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, timeout=120)
        (run / (name + '.log')).write_bytes(result.stdout + result.stderr)
        if result.returncode:
            raise RuntimeError(f'{name} failed, see {run}')
    if args.unit_test_log:
        unit_log = args.unit_test_log.read_text(encoding='utf-8-sig')
        if '\nRan ' not in unit_log or not unit_log.rstrip().endswith('\nOK'):
            raise SystemExit(f'The build unit test log does not show a pass: {args.unit_test_log}')
        (run / 'unit-tests.log').write_text(unit_log, encoding='utf-8')
    else:
        execute([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], 'unit-tests')
    archive = CArchiveReader(str(exe))
    native = {}
    for member in archive.toc:
        name = Path(member)
        if name.name.lower() != 'mupdfcpp64.dll' and not (
            name.parts[0] == 'pymupdf' and name.suffix.lower() in ('.dll', '.pyd')
        ):
            continue
        digest = hashlib.sha256(archive.extract(member)).hexdigest()
        assert digest == NATIVE_HASHES.get(name.name), f'Unexpected PDF native binary: {member} {digest}'
        assert name.name not in native, f'Duplicate PDF native binary: {member}'
        native[name.name] = digest
    assert {'mupdfcpp64.dll', '_mupdf.pyd'} <= native.keys(), native
    execute([sys.executable, 'app.py', '--smoke-test', str(run / 'source')], 'source-gui')
    source = json.loads((run / 'source' / 'report.json').read_text(encoding='utf8'))
    assert source['passed'] and not source['frozen'], source
    portable = run / '可攜驗證 日本語'
    portable.mkdir()
    target = portable / exe.name
    shutil.copy2(exe, target)
    env = os.environ.copy()
    windows = ctypes.create_unicode_buffer(32768)
    assert ctypes.windll.kernel32.GetWindowsDirectoryW(windows, len(windows))
    env['SystemRoot'] = windows.value
    env['PATH'] = str(Path(windows.value) / 'System32') + os.pathsep + windows.value
    for key in ('PYTHONPATH', 'PYTHONHOME', 'TCL_LIBRARY', 'TK_LIBRARY'):
        env.pop(key, None)
    execute([str(target), '--smoke-test', str(run / 'frozen')], 'exe-gui', env, portable)
    frozen = json.loads((run / 'frozen' / 'report.json').read_text(encoding='utf8'))
    assert frozen['passed'] and frozen['frozen'], frozen
    for gui in (source, frozen):
        assert (gui['pymupdf'], gui['mupdf']) == ('2.1', '1.28.6'), gui
        assert gui['mupdf_dll_sha256'] == NATIVE_HASHES['mupdfcpp64.dll'], gui
    with pefile.PE(str(exe)) as pe:
        assert pe.FILE_HEADER.Machine == 0x8664, 'EXE is not Windows x64'
        ids = [entry.id for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries]
        assert 3 in ids and 14 in ids and 16 in ids, 'EXE icon / version resources missing'
        version = pe.VS_FIXEDFILEINFO[0]
        assert (version.FileVersionMS, version.FileVersionLS) == (65536, 65536)
    report.update(passed=True, bytes=exe.stat().st_size,
                  sha256=hashlib.sha256(exe.read_bytes()).hexdigest(),
                  source_gui=source, frozen_gui=frozen, pymupdf_native_sha256=native,
                  exe_icon_and_version_resources=True, python_removed_from_child_path=True)
    (run / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    print('PASS: unit tests, source and portable GUI, Windows x64 EXE resources and native PDF binaries.')
    print('Report:', run / 'verification.json')


if __name__ == '__main__':
    main()
