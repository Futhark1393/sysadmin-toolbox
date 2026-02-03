#!/bin/bash

# --- Configuration & Colors ---
# ANSI Color Codes for pretty output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Backup directory (current folder for demo purposes)
BACKUP_DIR="./backups"

# --- Helper Functions ---

# Function to pause and wait for user input
pause() {
    read -p "Press [Enter] to return to the menu..."
}

# Function 1: Display System Information
# Uses: Variables, String Manipulation, Command Substitution
show_sys_info() {
    echo -e "${BLUE}--- System Information ---${NC}"
    echo "Hostname : $(hostname)"
    echo "Kernel   : $(uname -r)"
    echo "Uptime   : $(uptime -p)"
    echo "User     : $USER"
    echo -e "${BLUE}--------------------------${NC}"
    pause
}

# Function 2: Disk Usage Analyzer
# Uses: Arithmetic, bc (Floating point), If/Else
check_disk_usage() {
    echo -e "${YELLOW}Checking Disk Usage...${NC}"
    
    # Get usage percentage of root partition / (removes % sign)
    usage=$(df / | grep / | awk '{ print $5 }' | sed 's/%//g')
    
    # Example of floating point calculation using bc
    # Let's pretend we want to calculate free space ratio precisely
    free_ratio=$(echo "scale=2; (100 - $usage) / 100" | bc)
    
    echo "Root Partition Usage: ${usage}%"
    echo "Free Space Ratio: $free_ratio"

    if [ $usage -ge 80 ]; then
        echo -e "${RED}WARNING: Disk space is critically low!${NC}"
    elif [ $usage -ge 50 ]; then
        echo -e "${YELLOW}WARNING: Disk space is getting full.${NC}"
    else
        echo -e "${GREEN}STATUS: Disk space is healthy.${NC}"
    fi
    pause
}

# Function 3: Backup Tool
# Uses: Arrays, For Loops, File Tests (-d), Date command
backup_files() {
    echo -e "${BLUE}--- Starting Backup Process ---${NC}"
    
    # Create backup directory if it doesn't exist
    if [ ! -d "$BACKUP_DIR" ]; then
        mkdir -p "$BACKUP_DIR"
        echo "Created backup directory: $BACKUP_DIR"
    fi

    # Array of folders to backup (We will backup our codes folder)
    folders_to_backup=("codes" "non_existent_folder_test")

    for folder in "${folders_to_backup[@]}"; do
        if [ -d "$folder" ]; then
            archive_name="backup_$(basename $folder)_$(date +%Y%m%d).tar.gz"
            echo "Backing up '$folder' to '$BACKUP_DIR/$archive_name'..."
            
            # Create archive (suppress output with > /dev/null)
            tar -czf "$BACKUP_DIR/$archive_name" "$folder" 2>/dev/null
            
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}Success: $folder backed up.${NC}"
            else
                echo -e "${RED}Error: Failed to backup $folder.${NC}"
            fi
        else
            echo -e "${RED}Skipping: Folder '$folder' does not exist.${NC}"
        fi
    done
    pause
}

# Function 4: Battery Health Monitor
# Uses: upower, grep, awk
check_battery_status() {
    echo -e "${YELLOW}Checking Battery Status...${NC}"
    
    # Find the battery path (usually /org/freedesktop/UPower/devices/battery_BAT0)
    # We take the first BAT result we find.
    BAT_PATH=$(upower -e | grep 'BAT' | head -n 1)

    if [ -z "$BAT_PATH" ]; then
        echo -e "${RED}Error: No battery detected.${NC}"
    else
        # Extract specific info using upower -i
        # We grab state, percentage, and capacity (which is health)
        echo -e "${BLUE}--- Battery Details ---${NC}"
        
        upower -i "$BAT_PATH" | grep -E "state|percentage|capacity|time to empty|time to full"
        
        echo -e "${BLUE}-----------------------${NC}"
        echo "Note: 'capacity' shows your battery health (100% is new)."
    fi
    pause
}

# --- Main Logic (Menu System) ---
# Uses: While Loop, Case Statement, User Input

while true; do
    clear # Clears the terminal screen
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}   SYSADMIN TOOLBOX v1.0        ${NC}"
    echo -e "${GREEN}================================${NC}"
    echo "1. Show System Information"
    echo "2. Check Disk Usage"
    echo "3. Backup Project Files"
    echo "4. Check Battery Status"   
    echo "5. Exit"                   
    echo -e "${GREEN}================================${NC}"
    
    read -p "Enter your choice [1-5]: " choice
    case $choice in
        1)
            show_sys_info
            ;;
        2)
            check_disk_usage
            ;;
        3)
            backup_files
            ;;
        4)                       
            check_battery_status
            ;;
        5)                      
            echo "Exiting... Goodbye, $USER!"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option! Please try again.${NC}"
            sleep 1
            ;;
    esac
done