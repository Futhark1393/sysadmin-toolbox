#!/bin/bash

# ==========================================
# SysAdmin Toolbox Uninstaller
# Description: Removes the desktop entry and cleans up generated data.
# ==========================================

APP_NAME="SysAdmin Toolbox"
DESKTOP_FILE_PATH="$HOME/.local/share/applications/SysAdminToolbox.desktop"

echo -e "🗑️  Uninstalling $APP_NAME..."

# 1. Remove the Desktop Entry (Shortcut)
if [ -f "$DESKTOP_FILE_PATH" ]; then
    rm "$DESKTOP_FILE_PATH"
    echo "✅ Desktop shortcut removed."
else
    echo "⚠️  Desktop shortcut not found (maybe already removed?)."
fi

# 2. Refresh Desktop Database
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null
echo "🔄 Application menu refreshed."

# 3. Clean up generated data (Optional)
read -p "❓ Do you want to delete generated data (baseline.db, logs)? [y/N]: " confirm
if [[ "$confirm" =~ ^[Yy]$ ]]; then
    echo "🧹 Cleaning up project data..."
    rm -f data/*.db
    rm -f data/*.txt
    rm -rf src/__pycache__
    echo "✅ Temporary files deleted."
else
    echo "ℹ️  Data files kept."
fi

echo ""
echo "=========================================="
echo "❌ Uninstallation Complete."
echo "⚠️  To completely remove the tool, delete this folder:"
echo "   rm -rf $(pwd)"
echo "=========================================="
