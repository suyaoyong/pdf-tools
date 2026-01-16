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

pyinstaller --noconsole --name $Name --add-data $addData -m pdf_toolbox.app

Write-Host "Build done. Output in dist/$Name"
