# SysAdmin Toolbox 🛠️ v2.1 (Hybrid Edition)

![Bash](https://img.shields.io/badge/Shell-Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Qt](https://img.shields.io/badge/GUI-PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Systemd](https://img.shields.io/badge/Manage-Systemd-red?style=for-the-badge&logo=linux&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

A powerful system administration tool designed for Linux (Fedora), featuring both a **Classic CLI (Terminal)** and a **Modern GUI (Graphical Interface)**.

> **🎓 Educational Project:** This tool represents my journey from **Bash Scripting** to **Python GUI Development**. It combines system-level commands with a user-friendly interface to perform security audits, monitoring, backups, and **service management**.

## 🚀 Features

### 🛡️ Security Modules
* **Advanced Log Analyzer (Intrusion Detection):**
    * **SSH Brute-Force Detection:** Tracks failed logins and identifies attacking IPs.
    * **Sudo Violation Monitor:** Detects unauthorized root access attempts.
* **File Integrity Monitor (FIM):**
    * **Auto-Baseline:** Automatically secures `.txt`, `.sh`, and `.py` files.
    * **Integrity Check:** Instantly detects silent file modifications or deletions.

### ⚙️ System Utilities
* **Service Manager (Systemd):** **[NEW]** Manage Linux services (e.g., `sshd`, `cron`) directly.
    * **Actions:** Check Status, Start, Stop, and Restart services.
    * **Privilege Handling:** Uses `pkexec` (GUI) or `sudo` (CLI) for secure root authentication.
* **System Monitor:** Real-time kernel, uptime, load average, and RAM usage.
* **Disk Usage Analyzer:** Scans partitions and detects large files (>100MB) in logs.
* **Battery Health:** Displays battery percentage, status, and capacity (optimized for primary battery detection).
* **Automated Backups:**
    * *CLI:* Manual path entry.
    * *GUI:* Modern file-picker dialog to select backup targets easily.

## 📋 Requirements

Designed for **Fedora Linux**, but compatible with most systemd-based distributions.

### Core Requirements
* `bash` (4.0+)
* `journalctl` (For Log Analysis)
* `systemctl` (For Service Management)
* `sha256sum` (For FIM)
* `upower` (For Battery Check)

### GUI Requirements (Python)
* `python3`
* `PyQt6` (Can be installed via DNF on Fedora: `sudo dnf install python3-pyqt6`)
* `polkit` (For `pkexec` password prompts in GUI)

## 📦 Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Futhark1393/sysadmin-toolbox.git](https://github.com/Futhark1393/sysadmin-toolbox.git)
    cd sysadmin-toolbox
    ```

### 🖥️ Option 1: Terminal Mode (CLI)
Best for headless servers or quick access.

1.  **Make executable:**
    ```bash
    chmod +x toolbox.sh
    ```
2.  **Run:**
    ```bash
    ./toolbox.sh
    ```

### 🎨 Option 2: Graphical Mode (GUI)
Best for desktop experience with visual reports.

1.  **Install Dependencies:**
    ```bash
    sudo dnf install python3-pyqt6
    ```
2.  **Run:**
    ```bash
    python3 main_gui.py
    ```

## 🧠 Learning Outcomes

By building this tool, I mastered:
* **Hybrid Development:** Integrating Bash logic into Python automation.
* **Systemd Management:** Interacting with Linux services and handling status codes.
* **Privilege Escalation in GUI:** Using `pkexec` to run specific commands as root within a graphical app.
* **Cyber Security:** Implementing Intrusion Detection Systems (IDS) and File Integrity Monitoring.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
