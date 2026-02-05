#!/bin/bash

# ==========================================
# SysAdmin Toolbox Installer
# Developer: Futhark1393
# Description: Creates a dynamic .desktop entry for the GUI
# ==========================================

echo "🔵 Starting SysAdmin Toolbox Installation..."

# 1. Get the current working directory
CURRENT_DIR=$(pwd)
USERNAME=$(whoami)

echo "📂 Current Directory: $CURRENT_DIR"

# 2. Dynamically create the .desktop file
# The Exec path is automatically set to the current location
cat > SysAdminToolbox.desktop <<EOF
[Desktop Entry]
Version=2.1
Name=SysAdmin Toolbox
Comment=System Monitor, Security Audit & Service Manager
Exec=python3 $CURRENT_DIR/src/main_gui.py
Icon=utilities-system-monitor
Terminal=false
Type=Application
Categories=System;Utility;Security;
Keywords=admin;system;monitor;security;
EOF

# 3. Define target directory for user applications
TARGET_DIR="/home/$USERNAME/.local/share/applications"

# Ensure the directory exists
mkdir -p "$TARGET_DIR"

# Move the created file to the target directory
mv SysAdminToolbox.desktop "$TARGET_DIR/"

# 4. Set executable permissions
chmod +x "$TARGET_DIR/SysAdminToolbox.desktop"

# 5. Update desktop database to refresh the menu
update-desktop-database "$TARGET_DIR" 2>/dev/null

echo "✅ Installation Successful!"
echo "🚀 You can now search for 'SysAdmin Toolbox' in your applications menu."
