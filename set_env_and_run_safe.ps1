
# set_env_and_run_safe.ps1
# Safer runner: shows errors, pauses at the end, and bypasses common pitfalls

# Stop on first error
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

Write-Host "== Railway Connector (Safe Mode) ==" -ForegroundColor Cyan

# 1) Check Python
try {
    $pyVer = & python -c "import sys; print(sys.version)"
    Write-Host "Python found: $pyVer"
} catch {
    Write-Host "❌ Python tidak ditemukan di PATH. Instal Python atau buka PowerShell yang sudah punya Python." -ForegroundColor Red
    Read-Host "Tekan Enter untuk keluar"
    exit 1
}

# 2) Set DATABASE_URL for this session
$env:DATABASE_URL = "postgresql://postgres:WuZnoaOPPcCPpsPQcpJZdiswoenTjoXE@yamabiko.proxy.rlwy.net:28518/railway"
Write-Host "DATABASE_URL set." -ForegroundColor Green

# 3) Test connection (optional)
if (Test-Path ".\connect_test.py") {
    try {
        Write-Host "Menjalankan connect_test.py..." -ForegroundColor Yellow
        python .\connect_test.py
        if ($LASTEXITCODE -ne 0) { throw "connect_test.py exit code: $LASTEXITCODE" }
        Write-Host "✅ Connection OK." -ForegroundColor Green
    } catch {
        Write-Host "❌ Connection test failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Tips:" -ForegroundColor Yellow
        Write-Host " - Cek koneksi internet / firewall" 
        Write-Host " - Coba tambahkan ?sslmode=require di akhir URL bila perlu"
        Read-Host "Tekan Enter untuk keluar"
        exit 1
    }
} else {
    Write-Host "connect_test.py tidak ditemukan (melewati tes)."
}

# 4) Set admin (optional)
if (Test-Path ".\set_admin_pw.py") {
    try {
        Write-Host "Menjalankan set_admin_pw.py (opsional)..." -ForegroundColor Yellow
        python .\set_admin_pw.py
        if ($LASTEXITCODE -ne 0) { throw "set_admin_pw.py exit code: $LASTEXITCODE" }
        Write-Host "✅ Admin user dibuat/diupdate." -ForegroundColor Green
    } catch {
        Write-Host "❌ set_admin_pw.py gagal: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Lanjut tanpa update admin."
    }
}

# 5) Jalankan aplikasi
if (Test-Path ".\main.py") {
    try {
        Write-Host "Menjalankan aplikasi..." -ForegroundColor Cyan
        python .\main.py
        if ($LASTEXITCODE -ne 0) { throw "main.py exit code: $LASTEXITCODE" }
    } catch {
        Write-Host "❌ Aplikasi error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Cek pesan error di atas untuk detail."
        Read-Host "Tekan Enter untuk keluar"
        exit 1
    }
} else {
    Write-Host "❌ main.py tidak ditemukan di folder ini." -ForegroundColor Red
    Read-Host "Tekan Enter untuk keluar"
    exit 1
}

Read-Host "Selesai. Tekan Enter untuk menutup jendela"
