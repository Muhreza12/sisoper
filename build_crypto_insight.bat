@echo off
setlocal ENABLEDELAYEDEXECUTION
title Build Crypto Insight (PyInstaller)

REM === Path setup ===
set "BASE=%~dp0"
pushd "%BASE%"

REM === App meta ===
set "APP_NAME=Crypto Insight"
set "ENTRY=main.py"

REM === Clean previous build (optional) ===
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "%APP_NAME%.spec" del /q "%APP_NAME%.spec"

REM === Ensure venv exists ===
if not exist ".venv\Scripts\activate.bat" (
  echo [i] Membuat virtual environment...
  py -3 -m venv .venv 2>nul || python -m venv .venv
)

REM === Activate venv ===
call ".venv\Scripts\activate.bat"

REM === Upgrade dist tools and deps ===
echo [i] Upgrade pip / setuptools / wheel...
python -m pip install --upgrade pip setuptools wheel

REM === Install project deps ===
if exist "requirements.txt" (
  echo [i] Menginstal dependensi dari requirements.txt...
  pip install -r requirements.txt
) else (
  echo [!] requirements.txt tidak ditemukan, lanjutkan tanpa file tersebut.
)

REM === Ensure PyInstaller ===
pip install --upgrade pyinstaller

REM === Build options ===
set "ICON_OPT="
set "ADD_DATA_OPT="

REM gunakan logo.ico jika ada sebagai icon .exe
if exist "logo.ico" (
  set "ICON_OPT=--icon=logo.ico"
)

REM sertakan logo.jpg ke dalam bundle jika ada
if exist "logo.jpg" (
  set "ADD_DATA_OPT=--add-data "logo.jpg;.""
)

REM Tambahkan folder assets jika ada
if exist "assets" (
  set "ADD_DATA_OPT=%ADD_DATA_OPT% --add-data "assets\*;assets""
)

REM === Run PyInstaller ===
echo [i] Membuat EXE...
pyinstaller --onefile --noconsole --name "%APP_NAME%" %ICON_OPT% %ADD_DATA_OPT% "%ENTRY%"
set BUILDERR=%ERRORLEVEL%

if not "%BUILDERR%"=="0" (
  echo [x] Build gagal dengan kode %BUILDERR%.
  goto :end
)

echo [✓] Build selesai. File EXE:
echo    "%CD%\dist\%APP_NAME%.exe"

REM === Buka folder dist ===
explorer "%CD%\dist"

:end
popd
endlocal
