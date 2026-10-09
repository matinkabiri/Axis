$ErrorActionPreference = "Stop"

Set-Location (Split-Path -Parent $PSScriptRoot)
python -m pip install -r requirements.txt -r requirements-build.txt
python -m PyInstaller --noconfirm --clean packaging\Axis.spec

$portable = Join-Path (Get-Location) "dist\Axis-Portable"
if (Test-Path -LiteralPath $portable) {
    Remove-Item -LiteralPath $portable -Recurse -Force
}
New-Item -ItemType Directory -Path $portable | Out-Null
Copy-Item -LiteralPath "dist\Axis\*" -Destination $portable -Recurse
Copy-Item -LiteralPath "README.md" -Destination $portable
$artifact = "dist\Axis-0.1.0-alpha.1-windows-x64-portable.zip"
Compress-Archive -Path "$portable\*" -DestinationPath $artifact -Force
Write-Host "Created $artifact"
