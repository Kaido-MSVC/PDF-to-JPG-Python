# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Kaido-MSVC
# Prepare the source files that must be shared in the same place as
# dist\PDF-to-JPG.exe (AGPL-3.0 section 6):
#   dist\PDF-to-JPG-<version>-source.zip   this project, from the committed HEAD
#   dist\pymupdf-2.1.tar.gz                PyMuPDF 2.1 official sdist (unmodified)
#   dist\mupdf-1.28.6-source.tar.gz        MuPDF 1.28.6 official source (unmodified)
#   dist\BUILD-INFO.json                   Source commit and built EXE SHA-256
#   dist\SHA256SUMS.txt                    SHA-256 of the EXE and the files above
# Run after committing and then running .\build.ps1.
param([string]$OutputDirectory = (Join-Path $PSScriptRoot 'dist'))

$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

# Pinned upstream sources. Hashes: PyPI JSON API / GitHub release asset digest.
$upstream = @(
    @{ Name = 'pymupdf-2.1.tar.gz'
       Url = 'https://files.pythonhosted.org/packages/13/d9/5ae3cce31a4a62de4f6979331b4d8d5b86a8f2520f06754cf5e69065c887/pymupdf-2.1.tar.gz'
       Sha256 = '9ac95f98016e83eafb8f1d786396f9c60e400d559590596e5b2df9eb6384948b' },
    @{ Name = 'mupdf-1.28.6-source.tar.gz'
       Url = 'https://github.com/ArtifexSoftware/mupdf-downloads/releases/download/1.28.6/mupdf-1.28.6-source.tar.gz'
       Sha256 = 'dc85000640a45d90ca9b77b061f6ca67cce0c4d4fbecf8819647baf573eef101' }
)

$dirty = git status --porcelain
if ($LASTEXITCODE -ne 0) { throw 'git status failed.' }
if ($dirty) { throw "Working tree has uncommitted changes; commit first so the zip matches the EXE source.`n$dirty" }
$commit = git rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw 'Unable to read Git HEAD.' }
$match = Select-String -LiteralPath app.py -Pattern "^VERSION = '([^']+)'"
if (-not $match) { throw 'VERSION not found in app.py.' }
$version = $match.Matches[0].Groups[1].Value

$outputPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputDirectory)
$exe = Join-Path $outputPath 'PDF-to-JPG.exe'
$infoPath = Join-Path $outputPath 'BUILD-INFO.json'
if (-not (Test-Path -LiteralPath $exe -PathType Leaf) -or -not (Test-Path -LiteralPath $infoPath -PathType Leaf)) {
    throw 'EXE or BUILD-INFO.json missing; run .\build.ps1 for this output directory.'
}
$buildInfo = Get-Content -LiteralPath $infoPath -Raw | ConvertFrom-Json
if ($buildInfo.commit -cne $commit) {
    throw 'EXE build commit differs from Git HEAD.'
}
$exeHash = (Get-FileHash -LiteralPath $exe -Algorithm SHA256).Hash.ToLowerInvariant()
if ($buildInfo.exe_sha256 -cne $exeHash) {
    throw 'EXE SHA-256 differs from BUILD-INFO.json.'
}

# Upstream archives are cached in work\ and verified before every use.
$cache = Join-Path 'work' 'upstream-sources'
New-Item -ItemType Directory -Force $cache | Out-Null
foreach ($item in $upstream) {
    $cached = Join-Path $cache $item.Name
    if (-not (Test-Path -LiteralPath $cached)) {
        Write-Host "Downloading $($item.Url)"
        Invoke-WebRequest -Uri $item.Url -OutFile "$cached.part"
        $hash = (Get-FileHash -LiteralPath "$cached.part" -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($hash -ne $item.Sha256) { throw "SHA-256 mismatch for $cached.part" }
        Move-Item -LiteralPath "$cached.part" -Destination $cached
    }
    $hash = (Get-FileHash -LiteralPath $cached -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($hash -ne $item.Sha256) {
        throw "SHA-256 mismatch for $cached`n expected $($item.Sha256)`n actual   $hash"
    }
    Copy-Item -LiteralPath $cached -Destination (Join-Path $outputPath $item.Name) -Force
}

$name = "PDF-to-JPG-$version-source"
$zip = Join-Path $outputPath "$name.zip"
git archive --format=zip --prefix="$name/" -o $zip $commit
if ($LASTEXITCODE -ne 0) { throw 'git archive failed.' }

$files = @('PDF-to-JPG.exe', 'BUILD-INFO.json', "$name.zip") + ($upstream | ForEach-Object { $_.Name })
$lines = foreach ($f in $files) {
    $h = (Get-FileHash -LiteralPath (Join-Path $outputPath $f) -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($f -eq 'PDF-to-JPG.exe' -and $h -cne $exeHash) { throw 'EXE changed during packaging.' }
    "$h *$f"
}
$sums = Join-Path $outputPath 'SHA256SUMS.txt'
# LF line endings so both `sha256sum -c` (Git Bash) and PowerShell can read it.
[IO.File]::WriteAllText($sums, (($lines -join "`n") + "`n"))
Write-Host "Commit: $commit"
Get-Content -LiteralPath $sums
Write-Host 'Share all files listed above together, in the same place.'
