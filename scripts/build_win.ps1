param(
    [string]$Name = "pdf-toolbox-qt"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "PyInstaller not found. Installing..."
    pip install pyinstaller
}

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$assets = "assets"
$addData = "$assets;$assets"
$distDir = Join-Path $root "dist"
$oldDir = Join-Path $distDir $Name
if (Test-Path $oldDir) {
    Remove-Item -Recurse -Force $oldDir
}

pyinstaller --noconsole --onefile --name $Name --add-data $addData --add-data "qrcode_wetchat.png;." src\pdf_toolbox\app.py

Write-Host "Build done. Output in dist/$Name.exe"
