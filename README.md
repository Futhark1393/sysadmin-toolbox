# SysAdmin Toolbox 🛠️

![Bash](https://img.shields.io/badge/Shell-Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Status](https://img.shields.io/badge/Status-Educational-orange?style=for-the-badge)

A lightweight CLI tool for basic system monitoring, backup operations, and battery health checks on Linux systems.

> **🎓 Educational Project:** This tool was developed as a capstone project for my **Bash Scripting Learning Journey**. It is designed to demonstrate core concepts like functions, loops, case statements, and system interaction, rather than being a production-ready enterprise solution.

## 🚀 Features

* **System Information:** Displays kernel version, uptime, and hostname.
* **Disk Usage Analyzer:** Calculates root partition usage with precision (using `bc`).
* **Battery Health Monitor:** Checks battery capacity and status (using `upower`).
* **Automated Backups:** Archives specific directories into `.tar.gz` format.
* **Interactive Menu:** Simple navigation with color-coded output.

## 📋 Requirements

This script is developed and tested on **Fedora Linux**, but should work on most distros.

* `bash` (4.0+)
* `bc` (Basic Calculator for math ops)
* `upower` (For battery monitoring)
* `tar` (For backups)

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
* Modular programming with **Functions**.
* User interaction using **read** and **case statements**.
* String manipulation and arithmetic operations.
* File system management and conditional logic (`if`, `test`).

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
