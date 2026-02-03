' VBScript to create a Windows desktop shortcut with icon
' Auto-creates shortcut on desktop with game icon

Set WshShell = WScript.CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get script directory
scriptPath = fso.GetParentFolderName(WScript.ScriptFullName)

' Desktop path
desktopPath = WshShell.SpecialFolders("Desktop")
shortcutPath = desktopPath & "\What's Left.lnk"

' Create shortcut
Set oShellLink = WshShell.CreateShortcut(shortcutPath)
oShellLink.TargetPath = scriptPath & "\launch_game.bat"
oShellLink.WorkingDirectory = scriptPath
oShellLink.IconLocation = scriptPath & "\assets\game_icon.ico,0"
oShellLink.Description = "What's Left - Post-apocalyptic Adventure Game"
oShellLink.Save

WScript.Echo "Desktop shortcut created successfully!"
WScript.Echo "Location: " & shortcutPath
WScript.Echo ""
WScript.Echo "You can now launch the game from your desktop."
