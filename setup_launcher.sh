#!/bin/bash

# Setup script to automatically detect OS and install the appropriate game launcher
# Supports Linux, Windows (WSL/Git Bash/Native), and macOS

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DESKTOP_FILE="$SCRIPT_DIR/Whats_Left.desktop"
DESKTOP_DEST="$HOME/.local/share/applications/Whats_Left.desktop"
LAUNCHER_SCRIPT="$SCRIPT_DIR/launch_game.sh"
LAUNCHER_MACOS="$SCRIPT_DIR/launch_game_macos.sh"
LAUNCHER_BAT="$SCRIPT_DIR/launch_game.bat"
LAUNCH_PY="$SCRIPT_DIR/launch.py"

echo "=== What's Left Game Installer ==="
echo ""
echo "Detecting your operating system..."

# Make all launcher scripts executable
chmod +x "$LAUNCH_PY" 2>/dev/null || true
chmod +x "$LAUNCHER_SCRIPT" 2>/dev/null || true
chmod +x "$LAUNCHER_MACOS" 2>/dev/null || true

# Detect OS
OS_TYPE=""
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS_TYPE="macos"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    OS_TYPE="windows_native"
elif [[ -f "/proc/version" ]] && grep -qi microsoft /proc/version; then
    OS_TYPE="wsl"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS_TYPE="linux"
else
    OS_TYPE="unix"
fi

echo "Detected: $OS_TYPE"
echo ""

# Install based on OS
case $OS_TYPE in
    macos)
        echo "Installing for macOS..."
        echo ""
        
        # Create a simple launcher in Applications
        APP_DIR="$HOME/Applications/WhatsLeft.app"
        mkdir -p "$APP_DIR/Contents/MacOS"
        
        cat > "$APP_DIR/Contents/MacOS/WhatsLeft" << EOF
#!/bin/bash
cd "$SCRIPT_DIR"
if [ -x ".venv/bin/python" ]; then
    .venv/bin/python launch.py
else
    python3 launch.py
fi
EOF
        
        chmod +x "$APP_DIR/Contents/MacOS/WhatsLeft"
        
        # Create Info.plist with icon
        cat > "$APP_DIR/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>WhatsLeft</string>
    <key>CFBundleName</key>
    <string>What's Left</string>
    <key>CFBundleIdentifier</key>
    <string>com.maximeF97.whatsleft</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleIconFile</key>
    <string>game_icon</string>
</dict>
</plist>
EOF
        
        # Copy icon file to Resources folder
        mkdir -p "$APP_DIR/Contents/Resources"
        if [ -f "$SCRIPT_DIR/assets/game_icon.ico" ]; then
            cp "$SCRIPT_DIR/assets/game_icon.ico" "$APP_DIR/Contents/Resources/game_icon.ico"
        fi
        if [ -f "$SCRIPT_DIR/assets/IMG_5863.png" ]; then
            cp "$SCRIPT_DIR/assets/IMG_5863.png" "$APP_DIR/Contents/Resources/game_icon.png"
        fi
        
        echo "✓ Installed to: $APP_DIR"
        echo "✓ You can launch the game from Applications/WhatsLeft.app"
        echo "  Or double-click launch_game_macos.sh"
        ;;
        
    windows_native)
        echo "Installing for Windows (Native)..."
        echo ""
        
        echo "✓ Windows batch launcher is ready: launch_game.bat"
        echo "✓ Icon file available: assets\\game_icon.ico"
        echo ""
        echo "To create a desktop shortcut WITH ICON:"
        echo "  1. Double-click 'create_windows_shortcut.vbs'"
        echo "     This will automatically create a shortcut on your desktop with the game icon!"
        echo ""
        echo "OR manually:"
        echo "  1. Right-click launch_game.bat"
        echo "  2. Select 'Send to > Desktop (create shortcut)'"
        echo "  3. Right-click the new shortcut → Properties → Change Icon"
        echo "  4. Browse to: assets\\game_icon.ico"
        ;;
        
    wsl)
        echo "Installing for Windows Subsystem for Linux..."
        echo ""
        
        # Install both Linux launcher AND Windows launcher
        mkdir -p "$HOME/.local/share/applications"
        
        # Create icons directory
        mkdir -p "$HOME/.local/share/icons/hicolor/256x256/apps"
        
        # Copy icon to standard location (if PNG exists)
        if [ -f "$SCRIPT_DIR/assets/IMG_5863.png" ]; then
            cp "$SCRIPT_DIR/assets/IMG_5863.png" "$HOME/.local/share/icons/hicolor/256x256/apps/whatsleft.png"
            echo "✓ Icon copied to system icons directory"
        fi
        
        # Create Linux desktop entry for WSL with icon
        sed -e "s|%U|$SCRIPT_DIR|g" "$DESKTOP_FILE" > "$DESKTOP_DEST"
        
        # Update icon path to use system icon location
        sed -i "s|Icon=.*|Icon=whatsleft|g" "$DESKTOP_DEST"
        
        chmod +x "$DESKTOP_DEST" 2>/dev/null || true
        
        # Update desktop database if available
        if command -v update-desktop-database &> /dev/null; then
            update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
        fi
        
        # Try to refresh icon cache
        if command -v gtk-update-icon-cache &> /dev/null; then
            gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
        fi
        
        # Alternative: use xdg-icon-resource if available
        if command -v xdg-icon-resource &> /dev/null && [ -f "$SCRIPT_DIR/assets/IMG_5863.png" ]; then
            xdg-icon-resource install --novendor --size 256 "$SCRIPT_DIR/assets/IMG_5863.png" whatsleft 2>/dev/null || true
        fi
        
        echo "✓ Installed Linux launcher in WSL applications menu"
        echo "✓ Windows batch launcher also available: launch_game.bat"
        echo ""
        echo "You can launch the game using:"
        echo "  1. Search 'What's Left' in your WSL application launcher, OR"
        echo "  2. Double-click launch_game.bat from Windows Explorer"
        echo ""
        echo "To create a Windows desktop shortcut with icon:"
        echo "  - Double-click 'create_windows_shortcut.vbs' from Windows Explorer"
        echo "    (This will create a shortcut on your Windows desktop with the game icon)"
        ;;
        
    linux|unix)
        echo "Installing for Linux..."
        echo ""
        
        # Create applications directory if it doesn't exist
        mkdir -p "$HOME/.local/share/applications"
        
        # Create icons directory
        mkdir -p "$HOME/.local/share/icons/hicolor/256x256/apps"
        
        # Copy icon to standard location (if PNG exists)
        if [ -f "$SCRIPT_DIR/assets/IMG_5863.png" ]; then
            cp "$SCRIPT_DIR/assets/IMG_5863.png" "$HOME/.local/share/icons/hicolor/256x256/apps/whatsleft.png"
            echo "✓ Icon copied to system icons directory"
        fi
        
        # Copy the desktop file with correct path and icon
        sed -e "s|%U|$SCRIPT_DIR|g" "$DESKTOP_FILE" > "$DESKTOP_DEST"
        
        # Update icon path to use system icon location
        sed -i "s|Icon=.*|Icon=whatsleft|g" "$DESKTOP_DEST"
        
        # Make it executable
        chmod +x "$DESKTOP_DEST"
        
        # Update desktop database if available
        if command -v update-desktop-database &> /dev/null; then
            update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
        fi
        
        # Try to refresh icon cache
        if command -v gtk-update-icon-cache &> /dev/null; then
            gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
        fi
        
        # Alternative: use xdg-icon-resource if available
        if command -v xdg-icon-resource &> /dev/null && [ -f "$SCRIPT_DIR/assets/IMG_5863.png" ]; then
            xdg-icon-resource install --novendor --size 256 "$SCRIPT_DIR/assets/IMG_5863.png" whatsleft 2>/dev/null || true
        fi
        
        echo "✓ Installation complete!"
        echo "✓ Desktop entry installed to: $DESKTOP_DEST"
        echo ""
        echo "The game launcher should now appear in your applications menu."
        echo "Search for 'What's Left' in your application launcher, or"
        echo "run: ./launch_game.sh"
        ;;
esac

echo ""
echo "=== Installation Complete ==="

