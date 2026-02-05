# SysAdmin Toolbox 🛠️ v2.2 (Hybrid Edition)

![Bash](https://img.shields.io/badge/Shell-Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Qt](https://img.shields.io/badge/GUI-PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Build](https://img.shields.io/badge/Build-PyInstaller-blue?style=for-the-badge&logo=python&logoColor=white)
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
    * **Centralized Data:** Uses `data/` directory for database synchronization between CLI and GUI.
    * **Integrity Check:** Instantly detects silent file modifications or deletions.

### ⚙️ System Utilities
* **Service Manager (Systemd):** Manage Linux services (e.g., `sshd`, `cron`) directly.
    * **Actions:** Check Status, Start, Stop, and Restart services.
    * **Privilege Handling:** Uses `pkexec` (GUI) or `sudo` (CLI) for secure root authentication.
* **System Monitor:** Real-time kernel, uptime, load average, and RAM usage.
* **Disk Usage Analyzer:** Scans partitions and detects large files (>100MB) in logs.
* **Battery Health:** Displays battery percentage, status, and capacity (optimized for primary battery detection).
* **Automated Backups:** Modern file-picker dialog (GUI) or manual path entry (CLI).

## 📂 Project Structure

We follow a clean, standard Linux project hierarchy:

```text
sysadmin-toolbox/
├── src/            # Source Code (Python Logic)
│   └── main_gui.py
├── assets/         # UI Resources
│   └── toolbox.ui
├── data/           # Databases & Logs (Generated files)
│   └── fim_baseline.db
├── install.sh      # Desktop Installer
├── uninstall.sh    # Uninstaller
└── toolbox.sh      # CLI Version (Bash Script)
```

## 📋 Requirements

Designed for **Fedora Linux**, but compatible with most systemd-based distributions.

### Core Requirements
* `bash` (4.0+)
* `journalctl` & `systemctl`
* `sha256sum`
* `upower`

### GUI Requirements
* `python3`
* `PyQt6` (Fedora: `sudo dnf install python3-pyqt6`)
* `polkit` (For `pkexec` password prompts in GUI)

## 📦 Installation & Usage

Clone the repository:
```bash
git clone [https://github.com/Futhark1393/sysadmin-toolbox.git](https://github.com/Futhark1393/sysadmin-toolbox.git)
cd sysadmin-toolbox
```

---

### 🎨 Option 1: GUI Mode (Recommended)
Add the application to your system menu for easy access.

**Step 1: Install Dependencies**
```bash
sudo dnf install python3-pyqt6
```

**Step 2: Run the Installer**
This script creates a dynamic desktop shortcut.
```bash
chmod +x install.sh
./install.sh
```
*🎉 Now simply search for **"SysAdmin Toolbox"** in your Application Menu!*

---

### 🎒 Option 2: Portable Binary (Standalone)
Build a single executable file that runs without Python installed.

**Step 1: Install PyInstaller**
```bash
pip install pyinstaller
```

**Step 2: Build the Project**
```bash
pyinstaller --name "SysAdminToolbox" --onefile --windowed --add-data "assets/toolbox.ui:assets" src/main_gui.py
```

**Step 3: Run**
The executable is generated in the `dist/` folder.
```bash
./dist/SysAdminToolbox
```

---

### 🖥️ Option 3: CLI Mode (Terminal)
Best for headless servers or quick SSH access.

**Run:**
```bash
chmod +x toolbox.sh
./toolbox.sh
```

## 🗑️ Uninstallation

To remove the desktop shortcut and clean up generated data:

```bash
chmod +x uninstall.sh
./uninstall.sh
```
*(Then you can safely delete the project folder if desired.)*

## 🧠 Learning Outcomes

By building this tool, I mastered:
* **Hybrid Development:** Integrating Bash logic into Python automation.
* **Project Architecture:** Structuring files into `src`, `assets`, and `data` for scalability.
* **Software Packaging:** Creating portable Linux binaries using **PyInstaller**.
* **Systemd Management:** Interacting with Linux services and handling status codes.
* **Cyber Security:** Implementing Intrusion Detection Systems (IDS) and FIM.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
