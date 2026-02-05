# SysAdmin Toolbox 🛠️ v2.5 (Banner Grabbing Edition)

![Bash](https://img.shields.io/badge/Shell-Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Qt](https://img.shields.io/badge/GUI-PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Build](https://img.shields.io/badge/Build-PyInstaller-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

A powerful system administration tool designed for Linux (Fedora), featuring both a **Classic CLI (Terminal)** and a **Modern GUI (Graphical Interface)**.

> **🎓 Educational Project:** This tool represents my journey from **Bash Scripting** to **Python GUI Development**. It combines system-level commands with a user-friendly interface to perform security audits, monitoring, backups, and **advanced network scanning**.

## 📸 Screenshots

### 1. The Dashboard (System & Services)
![Dashboard Screenshot](screenshots/dashboard.png)
*Real-time monitoring, service management, and security logs.*

### 2. Network Scanner (Banner Grabbing)
![Scanner Screenshot](screenshots/scanner.png)
*Multi-threaded port scanner with **Service Version Detection** (Banner Grabbing).*

---

## 🚀 Features

### 🕵️‍♂️ Network & Security (v2.5 Update)
* **Advanced Port Scanner:** Multithreaded scanning preventing UI freeze.
* **Banner Grabbing (New!):** Detects service versions (e.g., `SSH-2.0-OpenSSH_8.7`) running on open ports.
* **Log Analyzer (IDS):** Detects SSH brute-force attacks and Sudo violations.
* **File Integrity Monitor (FIM):** Automatically creates baselines and detects unauthorized file changes.

### ⚙️ System Utilities
* **Tabbed Interface:** Clean separation between System Dashboard and Network Tools.
* **Service Manager:** Start, Stop, and Restart systemd services (e.g., `sshd`, `cron`) with root privileges (`pkexec`).
* **System Monitor:** Real-time kernel, uptime, and RAM usage stats.
* **Disk & Battery:** Partition analysis and battery health checks.
* **Automated Backups:** Easy-to-use directory backup tool.

## 📂 Project Structure

We follow a clean, standard Linux project hierarchy:

```text
sysadmin-toolbox/
├── src/            # Source Code (Python Logic)
│   └── main_gui.py
├── assets/         # UI Resources
│   └── toolbox.ui
├── screenshots/    # Project Images
│   ├── dashboard.png
│   └── scanner.png
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
* **PyQt6 & Qt Designer:** Creating complex, tabbed user interfaces.
* **Socket Programming:** Implementing raw socket connections for network analysis.
* **Multithreading (`QThread`):** Running background tasks without freezing the UI.
* **Hybrid Architecture:** Connecting Python GUI with Bash system commands.
* **Software Packaging:** Building portable binaries with **PyInstaller**.

## ⚠️ Legal Disclaimer

**For Educational Purposes Only.**
This tool is designed for system administrators and security enthusiasts to audit their *own* networks and systems.

* **Do not use this tool on networks or systems you do not own or do not have explicit permission to test.**
* The author (@Futhark1393) is not responsible for any damage, data loss, or legal consequences caused by the misuse of this tool.
* By downloading and using this software, you agree to use it responsibly and in accordance with all applicable local and international laws.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

