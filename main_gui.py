import sys
import subprocess
import os
from datetime import datetime
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog

class SysAdminToolbox(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1. Tasarımı Yükle (.ui dosyası)
        ui_path = os.path.join(os.path.dirname(__file__), "toolbox.ui")
        uic.loadUi(ui_path, self)

        # 2. Butonları Fonksiyonlara Bağla
        self.btn_monitor.clicked.connect(self.run_monitor)
        self.btn_disk.clicked.connect(self.run_disk)
        self.btn_fim_init.clicked.connect(self.run_fim_init)
        self.btn_fim_check.clicked.connect(self.run_fim_check)
        self.btn_logs.clicked.connect(self.run_logs)
        self.btn_backup.clicked.connect(self.run_backup)
        self.btn_battery.clicked.connect(self.run_battery)

        # Pencere Başlığı
        self.setWindowTitle("Futhark's SysAdmin Toolbox GUI v1.1")

    # --- Komut Çalıştırma Motoru ---
    def run_command(self, command):
        self.text_output.clear() # Ekranı temizle
        self.text_output.append(f"> Executing: {command}\n")
        self.text_output.repaint()
        
        try:
            # Komutu çalıştır
            result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
            self.text_output.append(result)
        except subprocess.CalledProcessError as e:
            # Hata kodunu göster
            self.text_output.append(f"❌ Error (Code {e.returncode}):\n{e.output}\n")
        
        # Scroll'u en alta indir
        scrollbar = self.text_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    # --- 1. System Monitor ---
    def run_monitor(self):
        cmd = "echo '--- Kernel ---'; uname -r; echo ''; echo '--- Uptime ---'; uptime -p; echo ''; echo '--- Memory ---'; free -h"
        self.run_command(cmd)

    # --- 2. Disk Usage ---
    def run_disk(self):
        self.text_output.append("🔵 Analyzing Disk Usage & Scanning for Large Files (>100MB)...")
        # raw string (r"") kullanımı
        cmd = r"echo '--- Partition Usage ---'; df -h /; echo ''; echo '--- Large Files in /var/log ---'; find /var/log -type f -size +100M -exec ls -lh {} \; 2>/dev/null || echo 'No large files found.'"
        self.run_command(cmd)

    # --- 3. FIM: Init ---
    def run_fim_init(self):
        self.text_output.append("🔵 Creating Baseline (Targeting .txt, .sh, .py files)...")
        cmd = "rm -f fim_baseline.db; sha256sum *.txt *.sh *.py > fim_baseline.db 2>/dev/null && echo '✅ Baseline Created Successfully!'"
        self.run_command(cmd)

    # --- 4. FIM: Check ---
    def run_fim_check(self):
        if not os.path.exists("fim_baseline.db"):
            self.text_output.append("⚠️ Error: Baseline file not found. Please run 'Create Baseline' first.\n")
            return
        
        self.text_output.append("🔵 Checking File Integrity...")
        cmd = "sha256sum -c fim_baseline.db"
        self.run_command(cmd)

    # --- 5. Log Analyzer ---
    def run_logs(self):
        self.text_output.append("🔵 Running Advanced Security Audit...")
        
        cmd = """
        echo "--- 1. SSH: Invalid Usernames (Top 5) ---"
        journalctl -u sshd | grep "Invalid user" | awk '{print $(NF-2)}' | sort | uniq -c | sort -nr | head -n 5 || echo "No invalid user attempts."
        
        echo "\n--- 2. SSH: Failed Passwords (Last 5) ---"
        journalctl -u sshd | grep "Failed password" | tail -n 5 || echo "No failed password attempts."
        
        echo "\n--- 3. SUDO: Violations ---"
        journalctl _COMM=sudo | grep -E "NOT in sudoers|incorrect password" | tail -n 5 || echo "No sudo violations."
        """
        self.run_command(cmd)

    # --- 6. Automated Backup ---
    def run_backup(self):
        target_dir = QFileDialog.getExistingDirectory(self, "Select Directory to Backup")
        
        if target_dir:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}.tar.gz"
            self.text_output.append(f"📦 Compressing directory: {target_dir} ...")
            
            cmd = f"tar -czf {backup_name} '{target_dir}' && echo '✅ Backup created: {backup_name}'"
            self.run_command(cmd)
        else:
            self.text_output.append("⚠️ Backup cancelled (No directory selected).")

    # --- 7. Battery Health (KESİN ÇÖZÜM) ---
    def run_battery(self):
        self.text_output.append("🔋 Checking Battery Stats...")
        
        # DÜZELTME 1: 'head -n 1' ekledik -> Sadece ilk (gerçek) pili al.
        # DÜZELTME 2: '|| true' ekledik -> Hata kodunu (exit 1) yut, sadece çıktıyı göster.
        # Böylece 'No battery detected' yazısı ve kırmızı hata kodu tamamen kalkacak.
        cmd = r"upower -i $(upower -e | grep 'BAT' | head -n 1) | grep -E 'state|to full|percentage|capacity' || true"
        
        self.run_command(cmd)

# --- Uygulamayı Başlat ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SysAdminToolbox()
    window.show()
    sys.exit(app.exec())
