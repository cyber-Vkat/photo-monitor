; Inno Setup Script for Photo Monitor
; Download Inno Setup from: https://jrsoftware.org/isinfo.php

[Setup]
AppName=Photo Monitor
AppVersion=1.0
AppPublisher=Photo Monitor
DefaultDirName={autopf}\PhotoMonitor
DefaultGroupName=Photo Monitor
OutputDir=installer_output
OutputBaseFilename=PhotoMonitor_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\PhotoMonitor.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "config.ini"; DestDir: "{userappdata}\PhotoMonitor"; Flags: ignoreversion onlyifdoesntexist
Source: "templates\*"; DestDir: "{userappdata}\PhotoMonitor\templates"; Flags: ignoreversion recursesubdirs createallsubdirs onlyifdoesntexist

[Dirs]
Name: "{userappdata}\PhotoMonitor\watch_folder"
Name: "{userappdata}\PhotoMonitor\processed"

[Icons]
Name: "{group}\Photo Monitor"; Filename: "{app}\PhotoMonitor.exe"; WorkingDir: "{userappdata}\PhotoMonitor"
Name: "{group}\{cm:UninstallProgram,Photo Monitor}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Photo Monitor"; Filename: "{app}\PhotoMonitor.exe"; WorkingDir: "{userappdata}\PhotoMonitor"; Tasks: desktopicon
Name: "{group}\Open Config Folder"; Filename: "{userappdata}\PhotoMonitor"

[Run]
Filename: "{app}\PhotoMonitor.exe"; Description: "{cm:LaunchProgram,Photo Monitor}"; WorkingDir: "{userappdata}\PhotoMonitor"; Flags: nowait postinstall skipifsilent

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    SaveStringToFile(ExpandConstant('{userappdata}\PhotoMonitor\README.txt'), 
      'Photo Monitor' + #13#10 + 
      '=============' + #13#10 + #13#10 +
      'Configuration files are stored in this folder.' + #13#10 +
      'Place photos in the watch_folder to process them.' + #13#10 +
      'Processed images will be saved to the processed folder.' + #13#10 +
      'Edit config.ini to change settings.' + #13#10,
      False);
  end;
end;
