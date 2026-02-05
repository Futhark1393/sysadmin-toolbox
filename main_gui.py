import sys
import subprocess
import os
from datetime import datetime
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog

class SysAdminToolbox(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1. Tasarımı Yükle
        ui_path = os.path.join(os.path.dirname(__file__), "toolbox.ui")
        uic.loadUi(ui_path, self)

        # 2. Buton Bağlantıları (Eskiler)
        self.btn_monitor.clicked.connect(self.run_monitor)
        self.btn_disk.clicked.connect(self.run_disk)
        self.btn_fim_init.clicked.connect(self.run_fim_init)
        self.btn_fim_check.clicked.connect(self.run_fim_check)
        self.btn_logs.clicked.connect(self.run_logs)
        self.btn_backup.clicked.connect(self.run_backup)
        self.btn_battery.clicked.connect(self.run_battery)

        # --- YENİ: Service Manager Bağlantıları ---
        # Tasarımda eklediğin objelerin isimleri burayla aynı olmalı!
        self.btn_svc_status.clicked.connect(self.service_status)
        self.btn_svc_restart.clicked.connect(self.service_restart)
        self.btn_svc_stop.clicked.connect(self.service_stop)

        self.setWindowTitle("Futhark's SysAdmin Toolbox v2.1 (Service Manager)")

    # --- Komut Motoru ---
    def run_command(self, command):
        self.text_output.clear()
        self.text_output.append(f"> Executing: {command}\n")
        self.text_output.repaint()
        
        try:
            # Komutu çalıştır
            result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
            self.text_output.append(result)
        except subprocess.CalledProcessError as e:
            self.text_output.append(f"❌ Error (Code {e.returncode}):\n{e.output}\n")
        
        scrollbar = self.text_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    # --- Eski Fonksiyonlar (Özet geçiyorum, bunlar sende zaten var) ---
    def run_monitor(self):
        self.run_command("echo '--- Kernel ---'; uname -r; echo ''; echo '--- Uptime ---'; uptime -p; echo ''; echo '--- Memory ---'; free -h")
    
    def run_disk(self):
        self.text_output.append("🔵 Analyzing Disk Usage...")
        cmd = r"echo '--- Partition Usage ---'; df -h /; echo ''; echo '--- Large Files in /var/log ---'; find /var/log -type f -size +100M -exec ls -lh {} \; 2>/dev/null || echo 'No large files found.'"
        self.run_command(cmd)

    def run_fim_init(self):
        self.text_output.append("🔵 Creating Baseline...")
        cmd = "rm -f fim_baseline.db; sha256sum *.txt *.sh *.py > fim_baseline.db 2>/dev/null && echo '✅ Baseline Created!'"
        self.run_command(cmd)

    def run_fim_check(self):
        if not os.path.exists("fim_baseline.db"):
            self.text_output.append("⚠️ Error: Baseline not found.")
            return
        self.text_output.append("🔵 Checking Integrity...")
        self.run_command("sha256sum -c fim_baseline.db")

    def run_logs(self):
        self.text_output.append("🔵 Running Security Audit...")
        cmd = """
        echo "--- 1. SSH: Invalid Users ---"
        journalctl -u sshd | grep "Invalid user" | tail -n 5 || echo "Clean."
        echo "\n--- 2. SUDO: Violations ---"
        journalctl _COMM=sudo | grep "NOT in sudoers" | tail -n 5 || echo "Clean."
        """
        self.run_command(cmd)

    def run_backup(self):
        target_dir = QFileDialog.getExistingDirectory(self, "Select Directory")
        if target_dir:
            name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
            self.text_output.append(f"📦 Backing up {target_dir}...")
            self.run_command(f"tar -czf {name} '{target_dir}' && echo '✅ Done: {name}'")

    def run_battery(self):
        self.text_output.append("🔋 Battery Stats...")
        cmd = r"upower -i $(upower -e | grep 'BAT' | head -n 1) | grep -E 'state|to full|percentage|capacity' || true"
        self.run_command(cmd)

    # =================================================
    # --- YENİ: Service Manager Fonksiyonları ---
    # =================================================
    
    def get_service_name(self):
        # Kullanıcının metin kutusuna yazdığı ismi alıyoruz
        name = self.input_service.text().strip()
        if not name:
            self.text_output.append("⚠️ Please enter a service name first (e.g. sshd, cron, firewalld).")
            return None
        return name

    def service_status(self):
        svc = self.get_service_name()
        if svc:
            self.text_output.append(f"🔍 Checking status of: {svc}...")
            # Status için root gerekmez
            self.run_command(f"systemctl status {svc} --no-pager")

    def service_restart(self):
        svc = self.get_service_name()
        if svc:
            self.text_output.append(f"🔄 Restarting {svc} (Authentication required)...")
            # pkexec: Grafik arayüzde şifre sormasını sağlar
            cmd = f"pkexec systemctl restart {svc} && echo '✅ Service {svc} restarted successfully!'"
            self.run_command(cmd)

    def service_stop(self):
        svc = self.get_service_name()
        if svc:
            self.text_output.append(f"🛑 Stopping {svc} (Authentication required)...")
            cmd = f"pkexec systemctl stop {svc} && echo '✅ Service {svc} stopped.'"
            self.run_command(cmd)

# --- Uygulamayı Başlat ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SysAdminToolbox()
    window.show()
    sys.exit(app.exec())
