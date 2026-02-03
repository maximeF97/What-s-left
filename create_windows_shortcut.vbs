' VBScript to create a Windows desktop shortcut with icon
Set WshShell = WScript.CreateObject("WScript.Shell")
Set oArgs = WScript.Arguments

If oArgs.Length < 3 Then
    WScript.Echo "Usage: create_windows_shortcut.vbs <shortcut_path> <target_path> <icon_path>"
    WScript.Quit 1
End If

shortcutPath = oArgs(0)
targetPath = oArgs(1)
iconPath = oArgs(2)

Set oShellLink = WshShell.CreateShortcut(shortcutPath)
oShellLink.TargetPath = targetPath
oShellLink.WorkingDirectory = WshShell.CurrentDirectory
oShellLink.IconLocation = iconPath & ",0"
oShellLink.Description = "What's Left - Post-apocalyptic Adventure Game"
oShellLink.Save

WScript.Echo "Shortcut created successfully at: " & shortcutPath
