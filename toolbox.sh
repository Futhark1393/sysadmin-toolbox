#!/bin/bash

# ==========================================
# SysAdmin Toolbox v2.1 (Hybrid Edition)
# Developer: Futhark1393
# Description: CLI for System Monitoring, Security & Management
# License: MIT
# ==========================================

# --- Configuration ---
# Veritabanı ve loglar artık 'data' klasöründe tutulacak
DATA_DIR="data"
BASELINE_FILE="$DATA_DIR/fim_baseline.db"

# Klasör yoksa oluştur (Hata almamak için)
mkdir -p "$DATA_DIR"

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# --- Functions ---

pause() {
    read -p "Press [Enter] to return to menu..."
}

header() {
    clear
    echo -e "${CYAN}======================================${NC}"
    echo -e "${CYAN}    SYSADMIN TOOLBOX - v2.1 (CLI)     ${NC}"
    echo -e "${CYAN}    User: $USER | Host: $HOSTNAME     ${NC}"
    echo -e "${CYAN}======================================${NC}"
}

sys_monitor() {
    header
    echo -e "${YELLOW}[*] System Monitoring${NC}"
    echo "---------------------------------"
    echo -e "Kernel Version : $(uname -r)"
    echo -e "Uptime         : $(uptime -p)"
    echo -e "Load Average   : $(uptime | awk -F'load average:' '{ print $2 }')"
    echo -e "Memory Usage   : $(free -h | grep Mem | awk '{print $3 "/" $2}')"
    echo ""
    pause
}

disk_usage() {
    header
    echo -e "${YELLOW}[*] Disk Usage Analysis (Root)${NC}"
    echo "---------------------------------"
    df -h / | awk 'NR==2 {print "Total: " $2, "| Used: " $3, "| Free: " $4, "| Use%: " $5}'
    
    echo ""
    echo -e "${BLUE}Scanning for large files (>100MB) in /var/log...${NC}"
    find /var/log -type f -size +100M -exec ls -lh {} \; 2>/dev/null || echo "No large files found."
    
    echo ""
    pause
}

backup_ops() {
    header
    echo -e "${YELLOW}[*] Automated Backup${NC}"
    echo "---------------------------------"
    read -p "Enter directory to backup (Full Path): " TARGET_DIR
    
    if [ -d "$TARGET_DIR" ]; then
        BACKUP_NAME="backup_$(date +%Y%m%d_%H%M%S).tar.gz"
        echo -e "${BLUE}Compressing $TARGET_DIR ...${NC}"
        tar -czf "$BACKUP_NAME" "$TARGET_DIR" 2>/dev/null
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[SUCCESS] Backup saved as: $BACKUP_NAME${NC}"
        else
            echo -e "${RED}[ERROR] Backup failed! Check permissions.${NC}"
        fi
    else
        echo -e "${RED}[ERROR] Directory not found!${NC}"
    fi
    pause
}

battery_check() {
    header
    echo -e "${YELLOW}[*] Battery Health Status${NC}"
    echo "---------------------------------"
    if command -v upower &> /dev/null; then
        BATTERY_PATH=$(upower -e | grep 'BAT' | head -n 1)
        if [ -n "$BATTERY_PATH" ]; then
            upower -i "$BATTERY_PATH" | grep -E "state|to\ full|percentage|capacity"
        else
            echo -e "${RED}No battery detected.${NC}"
        fi
    else
        echo -e "${RED}'upower' tool not installed.${NC}"
    fi
    pause
}

log_analyze() {
    header
    echo -e "${YELLOW}[*] Security Intrusion & Log Analysis${NC}"
    echo "---------------------------------------"
    if command -v journalctl &> /dev/null; then
        echo -e "${CYAN}--- SSH: Invalid Usernames (Top 5) ---${NC}"
        journalctl -u sshd | grep "Invalid user" | awk '{print $(NF-2)}' | sort | uniq -c | sort -nr | head -n 5 || echo "Clean."
        echo ""
        echo -e "${RED}--- SSH: Failed Password Attempts (Last 5) ---${NC}"
        journalctl -u sshd | grep "Failed password" | tail -n 5 | awk '{print $1, $2, $3, "-> User:", $(NF-5), "from IP:", $(NF-3)}' || echo "Clean."
        echo ""
        echo -e "${YELLOW}--- SUDO: Internal Security Incidents ---${NC}"
        journalctl _COMM=sudo | grep -E "NOT in sudoers|incorrect password" | tail -n 5 || echo "Clean."
    else
        echo -e "${RED}Error: journalctl not found.${NC}"
    fi
    echo ""
    pause
}

fim_ops() {
    while true; do
        header
        echo -e "${YELLOW}[*] File Integrity Monitor (FIM)${NC}"
        echo -e "Database Path: ${BLUE}$BASELINE_FILE${NC}"
        echo "---------------------------------"
        echo "1. Initialize Baseline (Auto-scan .txt, .sh, src/*.py)"
        echo "2. Check Integrity (Scan for Changes)"
        echo "3. Back to Main Menu"
        echo ""
        read -p "Select FIM Option: " fim_choice

        case $fim_choice in
            1)
                echo ""
                read -p "Enter directory to scan (Press Enter for current dir): " SCAN_DIR
                if [ -z "$SCAN_DIR" ]; then SCAN_DIR="."; fi
                
                echo -e "${BLUE}Creating baseline in $DATA_DIR ...${NC}"
                if [ -f "$BASELINE_FILE" ]; then rm "$BASELINE_FILE"; fi
                
                # src klasöründeki py dosyalarını da kapsayacak şekilde find
                find "$SCAN_DIR" -maxdepth 2 -type f \( -name "*.txt" -o -name "*.sh" -o -name "*.py" \) -not -path "*/__pycache__/*" -exec sha256sum {} + > "$BASELINE_FILE" 2>/dev/null
                
                if [ -s "$BASELINE_FILE" ]; then
                    echo -e "${GREEN}[DONE] Baseline saved to $BASELINE_FILE${NC}"
                else
                    echo -e "${RED}[ERROR] No matching files found.${NC}"
                fi
                read -p "Press Enter..."
                ;;
            2)
                echo ""
                if [ ! -f "$BASELINE_FILE" ]; then
                    echo -e "${RED}[ERROR] No baseline found in $DATA_DIR! Run Init first.${NC}"
                else
                    echo -e "${BLUE}Checking integrity using $BASELINE_FILE...${NC}"
                    sha256sum -c "$BASELINE_FILE"
                fi
                read -p "Press Enter..."
                ;;
            3) return ;;
            *) echo "Invalid option." ;;
        esac
    done
}

service_manager() {
    header
    echo -e "${YELLOW}[*] Service Manager (Systemd)${NC}"
    echo "---------------------------------"
    read -p "Enter Service Name (e.g. sshd, cron): " SVC_NAME
    if [ -z "$SVC_NAME" ]; then echo -e "${RED}No name entered.${NC}"; pause; return; fi

    echo ""
    echo "1. Check Status"
    echo "2. Restart Service (Sudo)"
    echo "3. Stop Service (Sudo)"
    echo "4. Cancel"
    echo ""
    read -p "Select Action: " svc_action

    case $svc_action in
        1) systemctl status "$SVC_NAME" --no-pager ;;
        2) sudo systemctl restart "$SVC_NAME" && echo -e "${GREEN}Restarted.${NC}" ;;
        3) sudo systemctl stop "$SVC_NAME" && echo -e "${GREEN}Stopped.${NC}" ;;
        *) echo "Cancelled." ;;
    esac
    pause
}

# --- Main Menu Loop ---
while true; do
    header
    echo "1. System Monitor"
    echo "2. Disk Usage"
    echo "3. Backup Tool"
    echo "4. Battery Health"
    echo "5. File Integrity Monitor (FIM)"
    echo "6. Log Analyzer (Intruder Detect)"
    echo "7. Service Manager"
    echo "8. Exit"
    echo ""
    read -p "Select an option [1-8]: " choice

    case $choice in
        1) sys_monitor ;;
        2) disk_usage ;;
        3) backup_ops ;;
        4) battery_check ;;
        5) fim_ops ;;
        6) log_analyze ;;
        7) service_manager ;;
        8) echo -e "${GREEN}Exiting. Secure days!${NC}"; exit 0 ;;
        *) echo -e "${RED}Invalid option!${NC}"; sleep 1 ;;
    esac
done
