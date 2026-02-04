#!/bin/bash

# ==========================================
# SysAdmin Toolbox v1.1
# Developer: Futhark1393
# Description: System Monitoring, Backups, and File Integrity (FIM)
# License: MIT
# ==========================================

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# --- Configuration ---
BASELINE_FILE="fim_baseline.db"

# --- Functions ---

pause() {
    read -p "Press [Enter] to return to menu..."
}

header() {
    clear
    echo -e "${CYAN}======================================${NC}"
    echo -e "${CYAN}    SYSADMIN TOOLBOX - v1.1           ${NC}"
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
    
    # Advanced: Find files larger than 100MB
    echo ""
    echo -e "${BLUE}Scanning for large files (>100MB) in /var/log...${NC}"
    find /var/log -type f -size +100M -exec ls -lh {} \; 2>/dev/null
    
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
        BATTERY_PATH=$(upower -e | grep 'BAT')
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

# --- NEW: Advanced Log Analyzer Module ---
log_analyze() {
    header
    echo -e "${YELLOW}[*] Security Intrusion & Log Analysis${NC}"
    echo "---------------------------------------"
    
    if command -v journalctl &> /dev/null; then
        
        # --- 1. SSH: Invalid User Attempts (Brute Force on Usernames) ---
        echo -e "${CYAN}--- SSH: Invalid Usernames (Top 5) ---${NC}"
        # "Invalid user" geçen satırları bul, IP'leri ayıkla
        if journalctl -u sshd | grep -q "Invalid user"; then
            journalctl -u sshd | grep "Invalid user" | awk '{print $(NF-2)}' | sort | uniq -c | sort -nr | head -n 5
        else
            echo -e "${GREEN}No invalid user attempts detected.${NC}"
        fi
        echo ""

        # --- 2. SSH: Failed Passwords (Brute Force on Valid Users) ---
        echo -e "${RED}--- SSH: Failed Password Attempts (Last 5) ---${NC}"
        # Tarih, Saat, Kullanıcı ve IP bilgisini düzenli göster
        if journalctl -u sshd | grep -q "Failed password"; then
            # Format: Month Day Time ... User ... IP
            journalctl -u sshd | grep "Failed password" | tail -n 5 | awk '{print $1, $2, $3, "-> User:", $(NF-5), "from IP:", $(NF-3)}'
        else
            echo -e "${GREEN}No failed password attempts detected.${NC}"
        fi
        echo ""

        # --- 3. SUDO: Unauthorized Root Access Attempts ---
        echo -e "${YELLOW}--- SUDO: Internal Security Incidents ---${NC}"
        # "COMMAND" çalıştırırken hata alanları bul
        if journalctl _COMM=sudo | grep -q "COMMAND"; then
             journalctl _COMM=sudo | grep "NOT in sudoers" | tail -n 5
             journalctl _COMM=sudo | grep "incorrect password" | tail -n 5
        else
             echo -e "${GREEN}No sudo violations found.${NC}"
        fi

    else
        echo -e "${RED}Error: journalctl not found. Cannot analyze logs.${NC}"
    fi
    
    echo ""
    pause
}

# --- NEW: File Integrity Monitor Module ---
fim_ops() {
    while true; do
        header
        echo -e "${YELLOW}[*] File Integrity Monitor (FIM)${NC}"
        echo "---------------------------------"
        echo "1. Initialize Baseline (Learn Hashes)"
        echo "2. Check Integrity (Scan for Changes)"
        echo "3. Back to Main Menu"
        echo ""
        read -p "Select FIM Option: " fim_choice

        case $fim_choice in
            1)
                echo ""
                read -p "Enter files to monitor (e.g. *.txt or /etc/passwd): " TARGET_FILES
                echo -e "${BLUE}Calculating hashes for: $TARGET_FILES ...${NC}"
                
                # Overwrite old baseline
                if [ -f "$BASELINE_FILE" ]; then rm "$BASELINE_FILE"; fi
                
                # Loop through files and hash them
                for f in $TARGET_FILES; do
                    if [ -f "$f" ]; then
                        sha256sum "$f" >> "$BASELINE_FILE"
                        echo "  [+] Added: $f"
                    fi
                done
                echo -e "${GREEN}[DONE] Baseline saved to $BASELINE_FILE${NC}"
                read -p "Press Enter..."
                ;;
            2)
                echo ""
                if [ ! -f "$BASELINE_FILE" ]; then
                    echo -e "${RED}[ERROR] No baseline found! Run Init first.${NC}"
                else
                    echo -e "${BLUE}Checking integrity...${NC}"
                    while read -r saved_hash filename; do
                        if [ -f "$filename" ]; then
                            current_hash=$(sha256sum "$filename" | awk '{print $1}')
                            if [ "$current_hash" == "$saved_hash" ]; then
                                echo -e "${GREEN}[OK] $filename${NC}"
                            else
                                echo -e "${RED}[ALERT] MODIFIED: $filename${NC}"
                            fi
                        else
                            echo -e "${RED}[MISSING] DELETED: $filename${NC}"
                        fi
                    done < "$BASELINE_FILE"
                fi
                read -p "Press Enter..."
                ;;
            3) return ;;
            *) echo "Invalid option." ;;
        esac
    done
}

# --- Main Menu Loop ---
while true; do
    header
    echo "1. System Monitor"
    echo "2. Disk Usage"
    echo "3. Backup Tool"
    echo "4. Battery Health"
    echo "5. File Integrity Monitor (FIM)"
    echo "6. Log Analyzer (Intruder Detect) [NEW]"
    echo "7. Exit"
    echo ""
    read -p "Select an option [1-7]: " choice

    case $choice in
        1) sys_monitor ;;
        2) disk_usage ;;
        3) backup_ops ;;
        4) battery_check ;;
        5) fim_ops ;;
        6) log_analyze ;;  # <--- YENİ EKLENEN
        7) echo -e "${GREEN}Exiting. Have a secure day, Futhark!${NC}"; exit 0 ;;
        *) echo -e "${RED}Invalid option!${NC}"; sleep 1 ;;
    esac
done

