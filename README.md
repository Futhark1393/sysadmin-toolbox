# SysAdmin Toolbox 🛠️ v1.2

![Bash](https://img.shields.io/badge/Shell-Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Security](https://img.shields.io/badge/Security-Blue_Team-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

A lightweight CLI tool for system monitoring, automated backups, and **comprehensive security auditing** on Linux systems.

> **🎓 Educational Project:** This tool was developed as a capstone project for my **Bash Scripting Learning Journey**. It demonstrates core concepts like log parsing (`journalctl`), file integrity hashing (`sha256sum`), and modular script architecture.

## 🚀 Features

### 🛡️ Security Modules
* **Advanced Log Analyzer (Intrusion Detection):** **[NEW]** Audits system logs for potential threats.
    * **SSH Brute-Force Detection:** Tracks failed login attempts, invalid username trials, and identifies top attacking IPs.
    * **Sudo Violation Monitor:** Detects unauthorized root access attempts and privilege escalation incidents.
    * **Detailed Reporting:** Provides timestamps, usernames, and IP addresses for every alert.
* **File Integrity Monitor (FIM):** Detects unauthorized file changes using SHA256 hashing.
    * *Init Mode:* Creates a secure baseline of critical files.
    * *Check Mode:* Scans for silent modifications or deletions.

### ⚙️ System Utilities
* **System Information:** Displays kernel version, uptime, load average, and memory usage.
* **Disk Usage Analyzer:** Calculates partition usage and intelligently scans for large files (>100MB).
* **Battery Health Monitor:** Checks battery capacity and status (using `upower`).
* **Automated Backups:** Archives specific directories into `.tar.gz` format with timestamping.

## 📋 Requirements

Designed for **Fedora Linux** (uses `journalctl`), but compatible with most systemd-based distributions.

* `bash` (4.0+)
* `journalctl` (For Log Analysis)
* `sha256sum` (For FIM)
* `bc` & `upower` (For utilities)

## 📦 Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Futhark1393/sysadmin-toolbox.git](https://github.com/Futhark1393/sysadmin-toolbox.git)
    cd sysadmin-toolbox
    ```

2.  **Make the script executable:**
    ```bash
    chmod +x toolbox.sh
    ```

3.  **Run the tool:**
    ```bash
    ./toolbox.sh
    ```

## 🧠 Learning Outcomes

By building this tool, I practiced:
* **Cyber Security:** Log analysis for intrusion detection and File Integrity Monitoring (FIM).
* **System Administration:** Parsing system logs (`journalctl`), user management, and process monitoring.
* **Bash Scripting:** Advanced text processing (`awk`, `grep`, `sed`), functions, and interactive menus.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
