# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Kaido-MSVC
# Create dist\PDF-to-JPG-<version>-source.zip from the committed HEAD.
# Share this zip in the same place as dist\PDF-to-JPG.exe (AGPL-3.0 section 6).
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$dirty = git status --porcelain
if ($LASTEXITCODE -ne 0) { throw 'git status failed.' }
if ($dirty) { throw "Working tree has uncommitted changes; commit first so the zip matches the EXE source.`n$dirty" }
$match = Select-String -LiteralPath app.py -Pattern "^VERSION = '([^']+)'"
if (-not $match) { throw 'VERSION not found in app.py.' }
$version = $match.Matches[0].Groups[1].Value
$name = "PDF-to-JPG-$version-source"
New-Item -ItemType Directory -Force dist | Out-Null
$zip = Join-Path 'dist' "$name.zip"
git archive --format=zip --prefix="$name/" -o $zip HEAD
if ($LASTEXITCODE -ne 0) { throw 'git archive failed.' }
$commit = git rev-parse HEAD
$hash = (Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash
Write-Host "Built: $zip"
Write-Host "Commit: $commit"
Write-Host "SHA-256: $hash"
