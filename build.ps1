# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Kaido-MSVC
param(
    [string]$PythonPath = (Join-Path $PSScriptRoot '.venv\Scripts\python.exe'),
    [string]$OutputDirectory = (Join-Path $PSScriptRoot 'dist')
)

$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
if (-not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) {
    throw '.venv not found. Create it: py -3.13 -m venv .venv; .venv\Scripts\python.exe -m pip install -r requirements-lock.txt'
}
$commit = $null
if (Test-Path -LiteralPath (Join-Path $PSScriptRoot '.git')) {
    $dirty = git status --porcelain
    if ($LASTEXITCODE -ne 0 -or $dirty) { throw 'Build requires a clean Git checkout.' }
    $commit = git rev-parse HEAD
    if ($LASTEXITCODE -ne 0) { throw 'Unable to read Git HEAD.' }
}

$checkVersions = @'
import sys
from importlib.metadata import version
from pathlib import Path

assert sys.version_info[:3] == (3, 13, 17), sys.version
assert sys.platform == 'win32' and sys.maxsize == 2**63 - 1, 'Windows x64 Python required'
for line in Path('requirements-lock.txt').read_text(encoding='utf-8').splitlines():
    if line and not line.startswith('#'):
        name, expected = line.split('==')
        actual = version(name)
        assert actual == expected, f'{name}: {actual} != {expected}'
'@
& $PythonPath -I -c $checkVersions
if ($LASTEXITCODE -ne 0) { throw 'Python or locked package version mismatch.' }

# Each build gets a new work directory and cache. Committed icons are build inputs.
$buildDirectory = Join-Path $PSScriptRoot ('work\build-' + [guid]::NewGuid().ToString('N'))
$env:PYINSTALLER_CONFIG_DIR = Join-Path $buildDirectory 'cache'
New-Item -ItemType Directory -Path $buildDirectory | Out-Null
$testLog = Join-Path $buildDirectory 'unit-tests.log'
$runTests = @'
import sys
import unittest

suite = unittest.defaultTestLoader.discover('tests')
result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
sys.exit(not result.wasSuccessful())
'@
$testLines = & $PythonPath -c $runTests
$testExit = $LASTEXITCODE
[IO.File]::WriteAllLines($testLog, [string[]]$testLines)
$testLines | Write-Host
if ($testExit -ne 0) { throw "Tests failed. See $testLog" }
$stage = Join-Path $buildDirectory 'dist'
& $PythonPath -I -m PyInstaller --noconfirm --distpath $stage --workpath (Join-Path $buildDirectory 'pyinstaller') PDF-to-JPG.spec
if ($LASTEXITCODE -ne 0) { throw 'EXE build failed.' }

if ($commit) {
    $endCommit = git rev-parse HEAD
    if ($LASTEXITCODE -ne 0 -or $endCommit -cne $commit) { throw 'Git HEAD changed during build.' }
    $dirty = git status --porcelain
    if ($LASTEXITCODE -ne 0 -or $dirty) { throw 'The Git checkout changed during build.' }
}

$stagedExe = Join-Path $stage 'PDF-to-JPG.exe'
$buildInfo = [ordered]@{
    commit = $commit
    exe_sha256 = (Get-FileHash -LiteralPath $stagedExe -Algorithm SHA256).Hash.ToLowerInvariant()
}
$outputPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputDirectory)
New-Item -ItemType Directory -Path $outputPath -Force | Out-Null
$exe = Join-Path $outputPath 'PDF-to-JPG.exe'
Copy-Item -LiteralPath $stagedExe -Destination $exe -Force
if ((Get-FileHash -LiteralPath $exe -Algorithm SHA256).Hash.ToLowerInvariant() -cne $buildInfo.exe_sha256) {
    throw 'Copied EXE differs from the build output.'
}
[IO.File]::WriteAllText((Join-Path $outputPath 'BUILD-INFO.json'), (($buildInfo | ConvertTo-Json) + "`n"))
Write-Host "Built: $exe"
Write-Host "Unit test log: $testLog"
