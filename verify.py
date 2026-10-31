# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Kaido-MSVC
"""Run focused source, GUI and portable EXE checks without changing packages."""
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

ROOT = Path(__file__).resolve().parent


def main():
    run = ROOT / 'work' / ('verify-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
    run.mkdir(parents=True)
    exe = ROOT / 'dist' / 'PDF-to-JPG.exe'
    if not exe.is_file():
        raise SystemExit('Build dist/PDF-to-JPG.exe first using build.ps1.')
    report = {'passed': False, 'exe': str(exe)}
    def execute(command, name, env=None, cwd=ROOT):
        result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, timeout=120)
        (run / (name + '.log')).write_bytes(result.stdout + result.stderr)
        if result.returncode:
            raise RuntimeError(f'{name} failed, see {run}')
    execute([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], 'unit-tests')
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
    with pefile.PE(str(exe)) as pe:
        ids = [entry.id for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries]
        assert 3 in ids and 14 in ids and 16 in ids, 'EXE icon / version resources missing'
        version = pe.VS_FIXEDFILEINFO[0]
        assert version.FileVersionMS == 65536 and version.FileVersionLS == 0
    report.update(passed=True, bytes=exe.stat().st_size,
                  sha256=hashlib.sha256(exe.read_bytes()).hexdigest(),
                  source_gui=source, frozen_gui=frozen,
                  exe_icon_and_version_resources=True, python_removed_from_child_path=True)
    (run / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    print('PASS: 11 unit tests, source GUI, portable EXE GUI, icon and version resources.')
    print('Report:', run / 'verification.json')


if __name__ == '__main__':
    main()
