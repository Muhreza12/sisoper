;
; crypto_insight_installer.iss — Inno Setup script sederhana
#define MyAppName "Crypto Insight"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Reza Team"
#define MyAppExeName "main.exe"

[Setup]
AppId={{2C8E3B61-FA8E-4F5D-9A1C-EXAMPLEA1B2C3}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableDirPage=no
DisableProgramGroupPage=no
OutputBaseFilename=CryptoInsight_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\config.ini"; DestDir: "{app}"; Flags: onlyifdoesntexist
Source: "README.txt"; DestDir: "{app}"; Flags: onlyifdoesntexist

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{userdesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked
