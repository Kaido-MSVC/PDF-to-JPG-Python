# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Kaido-MSVC
# Prepare the source files that must be shared in the same place as
# dist\PDF-to-JPG.exe (AGPL-3.0 section 6):
#   dist\PDF-to-JPG-<version>-source.zip   this project, from the committed HEAD
#   dist\pymupdf-2.0.tar.gz                PyMuPDF 2.0 official sdist (unmodified)
#   dist\mupdf-1.28.5-source.tar.gz        MuPDF 1.28.5 official source (unmodified)
#   dist\SHA256SUMS.txt                    SHA-256 of the EXE and the files above
# Run after committing and then running .\build.ps1.
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

# Pinned upstream sources. Hashes: PyPI JSON API / GitHub release asset digest.
$upstream = @(
    @{ Name = 'pymupdf-2.0.tar.gz'
       Url = 'https://files.pythonhosted.org/packages/b0/23/3575cf6652171bba33fd4b41d34ab92c7ee75bb5e5790f5a2a044b9ba49b/pymupdf-2.0.tar.gz'
       Sha256 = '7733136f626fffe98677daa53c906eb45f2eb486a6450dbcfd652cbbd760f1e2' },
    @{ Name = 'mupdf-1.28.5-source.tar.gz'
       Url = 'https://github.com/ArtifexSoftware/mupdf-downloads/releases/download/1.28.5/mupdf-1.28.5-source.tar.gz'
       Sha256 = '98a5c10cda20c3992cdf76ff6b2a1149c32bd79cc796d3f703230b1185b7e934' }
)

$dirty = git status --porcelain
if ($LASTEXITCODE -ne 0) { throw 'git status failed.' }
if ($dirty) { throw "Working tree has uncommitted changes; commit first so the zip matches the EXE source.`n$dirty" }
$match = Select-String -LiteralPath app.py -Pattern "^VERSION = '([^']+)'"
if (-not $match) { throw 'VERSION not found in app.py.' }
$version = $match.Matches[0].Groups[1].Value

$exe = Join-Path 'dist' 'PDF-to-JPG.exe'
if (-not (Test-Path -LiteralPath $exe)) { throw 'dist\PDF-to-JPG.exe not found; run .\build.ps1 first.' }
$commitTime = [DateTimeOffset]::FromUnixTimeSeconds([int64](git log -1 --format=%ct)).LocalDateTime
if ((Get-Item -LiteralPath $exe).LastWriteTime -lt $commitTime) {
    throw 'dist\PDF-to-JPG.exe is older than HEAD; run .\build.ps1 again so the EXE matches the source.'
}

# Upstream archives are cached in work\ and verified before every use.
$cache = Join-Path 'work' 'upstream-sources'
New-Item -ItemType Directory -Force $cache, 'dist' | Out-Null
foreach ($item in $upstream) {
    $cached = Join-Path $cache $item.Name
    if (-not (Test-Path -LiteralPath $cached)) {
        Write-Host "Downloading $($item.Url)"
        Invoke-WebRequest -Uri $item.Url -OutFile "$cached.part"
        Move-Item -LiteralPath "$cached.part" -Destination $cached
    }
    $hash = (Get-FileHash -LiteralPath $cached -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($hash -ne $item.Sha256) {
        throw "SHA-256 mismatch for $cached`n expected $($item.Sha256)`n actual   $hash"
    }
    Copy-Item -LiteralPath $cached -Destination (Join-Path 'dist' $item.Name) -Force
}

$name = "PDF-to-JPG-$version-source"
$zip = Join-Path 'dist' "$name.zip"
git archive --format=zip --prefix="$name/" -o $zip HEAD
if ($LASTEXITCODE -ne 0) { throw 'git archive failed.' }

$files = @('PDF-to-JPG.exe', "$name.zip") + ($upstream | ForEach-Object { $_.Name })
$lines = foreach ($f in $files) {
    $h = (Get-FileHash -LiteralPath (Join-Path 'dist' $f) -Algorithm SHA256).Hash.ToLowerInvariant()
    "$h *$f"
}
$sums = Join-Path 'dist' 'SHA256SUMS.txt'
[IO.File]::WriteAllText((Join-Path $PSScriptRoot $sums), (($lines -join "`r`n") + "`r`n"))
Write-Host "Commit: $(git rev-parse HEAD)"
Get-Content -LiteralPath $sums
Write-Host 'Share all files listed above together, in the same place.'
