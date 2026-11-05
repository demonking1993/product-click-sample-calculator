$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot

python .\make_icon.py
python -m unittest -v .\test_app.py

pyinstaller --noconfirm --clean --onefile --windowed `
  --name "StyleTestTool" `
  --icon .\app.ico `
  --version-file .\version_info.txt `
  .\app.py

Write-Host ""
Write-Host "Build complete: $PSScriptRoot\dist\StyleTestTool.exe"
