
# build_simple.ps1 — FINAL (PyInstaller + optional UPX + auto-copy config.ini + auto-open dist)
param(
  [string]$Main = "main.py",
  [bool]$Console = $false
)

$ErrorActionPreference = 'Stop'

function Ensure-Package($name) {
  $null = & pip show $name 2>$null
  if (-not $?) {
    Write-Host "Installing $name ..." -ForegroundColor Yellow
    & pip install $name | Out-Null
  }
}

# 0) Check entry file
if (-not (Test-Path -LiteralPath $Main)) {
  Write-Error "Entry file '$Main' not found in $(Get-Location)"
  exit 1
}

# 1) Ensure pyinstaller
Ensure-Package -name "pyinstaller"

# 2) Detect UPX (optional)
$upxDir = $null
if (Test-Path "C:\tools\upx\upx.exe") {
  $upxDir = "C:\tools\upx"
} elseif (Test-Path ".\upx\upx.exe") {
  $upxDir = (Resolve-Path ".\upx").Path
}

# 3) Clean previous build
Remove-Item -Recurse -Force dist, build, *.spec -ErrorAction SilentlyContinue

# 4) Assemble PyInstaller arguments
$pyArgs = @("--onefile")
if (-not $Console) { $pyArgs += "--noconsole" }

# include common assets if exist
if (Test-Path ".\style.qss") { $pyArgs += @("--add-data", "style.qss;.") }
if (Test-Path ".\register_form.py") { $pyArgs += @("--add-data", "register_form.py;.") }
if (Test-Path ".\posts_ui.py") { $pyArgs += @("--add-data", "posts_ui.py;.") }
if (Test-Path ".\posts_repo.py") { $pyArgs += @("--add-data", "posts_repo.py;.") }

if ($upxDir) {
  Write-Host "UPX detected at: $upxDir" -ForegroundColor Green
  $pyArgs += @("--upx-dir", $upxDir)
} else {
  Write-Host "UPX not found (optional). To enable, put upx.exe at C:\tools\upx or .\upx" -ForegroundColor Yellow
}

$pyArgs += $Main

Write-Host "Running: pyinstaller $($pyArgs -join ' ')" -ForegroundColor Cyan

# 5) Build
& pyinstaller @pyArgs

# 6) Show result
$exeName = [System.IO.Path]::GetFileNameWithoutExtension($Main) + ".exe"
$distRoot = Resolve-Path ".\dist"
$outPath = Join-Path -Path $distRoot.Path -ChildPath $exeName

if (Test-Path $outPath) {
  Write-Host ""
  Write-Host "✅ Build success." -ForegroundColor Green
  Write-Host "Output: $outPath" -ForegroundColor Green

  # === Copy config.ini automatically to dist ===
  $configFile = "config.ini"
  if (Test-Path $configFile) {
      $distCfg = Join-Path -Path $distRoot.Path -ChildPath $configFile
      Copy-Item $configFile -Destination $distCfg -Force
      Write-Host "🗂️  config.ini disalin ke folder dist." -ForegroundColor Green
  } else {
      Write-Host "⚠️  File config.ini tidak ditemukan di folder project." -ForegroundColor Yellow
  }

  try {
    # Open dist folder for convenience
    Invoke-Item $distRoot
  } catch {}
} else {
  Write-Host "❌ Build failed. Check logs above." -ForegroundColor Red
}

# Pause for visibility when double-clicked
if ($Host.Name -notlike "*ConsoleHost*") {
  Read-Host "Press Enter to close"
}
