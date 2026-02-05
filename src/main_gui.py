import sys
import subprocess
import os
import socket
from datetime import datetime
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtCore import QThread, pyqtSignal

# --- WORKER THREAD (Port Scanner İçin) ---
class PortScannerWorker(QThread):
    update_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, target_ip):
        super().__init__()
        self.target_ip = target_ip

    def run(self):
        self.update_signal.emit(f"🚀 Starting scan on {self.target_ip}...\n")
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1433, 3306, 3389, 5900, 8080]
        
        open_ports = 0
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((self.target_ip, port))
                
                if result == 0:
                    service_name = socket.getservbyport(port, "tcp")
                    self.update_signal.emit(f"✅ OPEN: Port {port} ({service_name})")
                    open_ports += 1
                sock.close()
            except Exception as e:
                pass
        
        if open_ports == 0:
            self.update_signal.emit(f"\n🚫 No open ports found (checked top 20).")
        else:
            self.update_signal.emit(f"\n🏁 Scan Complete. Found {open_ports} open ports.")
        
        self.finished_signal.emit()

# --- ANA UYGULAMA ---
class SysAdminToolbox(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # --- PATH CONFIG ---
        if hasattr(sys, '_MEIPASS'):
            self.base_dir = sys._MEIPASS
        else:
            self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        ui_path = os.path.join(self.base_dir, "assets", "toolbox.ui")
        self.data_dir = os.path.join(os.getcwd(), "data")
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.db_path = os.path.join(self.data_dir, "fim_baseline.db")
        
        # UI Yükle
        uic.loadUi(ui_path, self)

        # ---------------------------------------------------------
        # BUTON BAĞLANTILARI (_2 EKLİ HALİYLE)
        # Qt Designer kopyalama yapınca sonlarına _2 eklediği için kodları buna uydurduk.
        # ---------------------------------------------------------
        
        # 1. Dashboard Butonları (Sonlarında _2 var)
        self.btn_monitor_2.clicked.connect(self.run_monitor)
        self.btn_disk_2.clicked.connect(self.run_disk)
        self.btn_fim_init_2.clicked.connect(self.run_fim_init)
        self.btn_fim_check_2.clicked.connect(self.run_fim_check)
        self.btn_logs_2.clicked.connect(self.run_logs)
        self.btn_backup_2.clicked.connect(self.run_backup)
        self.btn_battery_2.clicked.connect(self.run_battery)

        # 2. Service Manager Butonları (Muhtemelen bunlarda da _2 var)
        # Hata almamak için try-except ile bağlıyoruz, eğer _2 yoksa normalini dener.
        try:
            self.btn_svc_status_2.clicked.connect(self.service_status)
            self.btn_svc_restart_2.clicked.connect(self.service_restart)
            self.btn_svc_stop_2.clicked.connect(self.service_stop)
        except AttributeError:
            # Eğer _2 yoksa orijinallerini dene
            self.btn_svc_status.clicked.connect(self.service_status)
            self.btn_svc_restart.clicked.connect(self.service_restart)
            self.btn_svc_stop.clicked.connect(self.service_stop)

        # 3. Network Scanner (Tab 2 - Bunlar yeni olduğu için _2 yoktur)
        try:
            self.btn_scan.clicked.connect(self.start_port_scan)
        except AttributeError:
            print("⚠️ Hata: Network Scanner butonları bulunamadı.")

        self.setWindowTitle("Futhark's SysAdmin Toolbox v2.4")

    # --- KOMUT MOTORU ---
    def run_command(self, command):
        # Ekran görüntüsünde text_output'un adında _2 yoktu, o yüzden normal bırakıyorum.
        # Eğer hata verirse burayı self.text_output_2 yapman gerekebilir.
        self.text_output.clear()
        self.text_output.append(f"> Executing: {command}\n")
        self.text_output.repaint()
        
        try:
            result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT, cwd=self.base_dir)
            self.text_output.append(result)
        except subprocess.CalledProcessError as e:
            self.text_output.append(f"❌ Error (Code {e.returncode}):\n{e.output}\n")
        
        scrollbar = self.text_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    # --- NETWORK SCANNER ---
    def start_port_scan(self):
        target_ip = self.input_ip.text().strip()
        if not target_ip:
            target_ip = "127.0.0.1"
            self.input_ip.setText(target_ip)
        
        # Sonuç ekranı (Tab 2'deki)
        self.output_area = self.text_scan_result
        self.output_area.clear()
        self.output_area.append(f"📡 Initializing scan on {target_ip}...\n")
        
        self.btn_scan.setEnabled(False)
        
        self.worker = PortScannerWorker(target_ip)
        self.worker.update_signal.connect(self.update_scan_log)
        self.worker.finished_signal.connect(self.scan_finished)
        self.worker.start()

    def update_scan_log(self, message):
        if "OPEN" in message:
            self.output_area.append(f"<span style='color:#00ff00; font-weight:bold;'>{message}</span>")
        else:
            self.output_area.append(f"<span style='color:#aaaaaa;'>{message}</span>")

    def scan_finished(self):
        self.btn_scan.setEnabled(True)
        self.output_area.append("\n✅ <b style='color:white;'>Scan Finished.</b>")

    # --- FONKSİYONLAR ---
    def run_monitor(self):
        self.run_command("echo '--- Kernel ---'; uname -r; echo ''; echo '--- Uptime ---'; uptime -p; echo ''; echo '--- Memory ---'; free -h")
    
    def run_disk(self):
        self.text_output.append("🔵 Analyzing Disk Usage...")
        cmd = r"echo '--- Partition Usage ---'; df -h /; echo ''; echo '--- Large Files in /var/log ---'; find /var/log -type f -size +100M -exec ls -lh {} \; 2>/dev/null || echo 'No large files found.'"
        self.run_command(cmd)

    def run_fim_init(self):
        self.text_output.append(f"🔵 Creating Baseline in data/...")
        cmd = f"rm -f data/fim_baseline.db; sha256sum *.txt *.sh src/*.py > data/fim_baseline.db 2>/dev/null && echo '✅ Baseline Created!'"
        self.run_command(cmd)

    def run_fim_check(self):
        if not os.path.exists(self.db_path):
            self.text_output.append("⚠️ Error: Baseline not found.")
            return
        self.text_output.append("🔵 Checking Integrity...")
        cmd = "sha256sum -c data/fim_baseline.db"
        self.run_command(cmd)

    def run_logs(self):
        self.text_output.append("🔵 Security Audit...")
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

    # --- SERVICE MANAGER (GÜNCELLENDİ: input_service_2) ---
    def get_service_name(self):
        # Ekran görüntüsünde input_ce_2 (input_service_2) görünüyordu
        try:
            name = self.input_service_2.text().strip()
        except AttributeError:
            name = self.input_service.text().strip()
            
        if not name:
            self.text_output.append("⚠️ Enter service name.")
            return None
        return name

    def service_status(self):
        svc = self.get_service_name()
        if svc:
            self.text_output.append(f"🔍 Status: {svc}...")
            self.run_command(f"systemctl status {svc} --no-pager")

    def service_restart(self):
        svc = self.get_service_name()
        if svc:
            self.text_output.append(f"🔄 Restarting {svc}...")
            cmd = f"pkexec systemctl restart {svc} && echo '✅ Service {svc} restarted!'"
            self.run_command(cmd)

    def service_stop(self):
        svc = self.get_service_name()
        if svc:
            self.text_output.append(f"🛑 Stopping {svc}...")
            cmd = f"pkexec systemctl stop {svc} && echo '✅ Service {svc} stopped.'"
            self.run_command(cmd)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SysAdminToolbox()
    window.show()
    sys.exit(app.exec())
