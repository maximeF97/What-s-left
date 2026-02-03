#!/bin/bash

# Setup script to automatically install the game launcher

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DESKTOP_FILE="$SCRIPT_DIR/Whats_Left.desktop"
DESKTOP_DEST="$HOME/.local/share/applications/Whats_Left.desktop"

echo "Installing What's Left launcher..."

# Create applications directory if it doesn't exist
mkdir -p "$HOME/.local/share/applications"

# Copy the desktop file
cp "$DESKTOP_FILE" "$DESKTOP_DEST"

# Make it executable
chmod +x "$DESKTOP_DEST"

# Ensure launcher script is executable
chmod +x "$SCRIPT_DIR/launch_game.sh"

# Update desktop database
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true

echo "✓ Installation complete!"
echo "The game launcher should now appear in your applications menu."
echo "You can also find it by searching 'What's Left' in your application launcher."
