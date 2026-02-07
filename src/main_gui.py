import sys
import subprocess
import os
import socket
from datetime import datetime
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QPoint
from fpdf import FPDF

# --- HEADLESS SCANNER FUNCTION (GUI'siz Tarama) ---
def headless_scan(target_ip):
    """Cronjob tarafından çağrıldığında çalışacak fonksiyon."""
    print(f"[*] Starting Headless Scan on {target_ip}...")
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    report_file = os.path.join(os.getcwd(), f"scan_report_{target_ip}_{timestamp}.txt")
    
    common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1433, 3306, 3389, 5900, 8080]
    results = []
    
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.0)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                service = "unknown"
                try: service = socket.getservbyport(port, "tcp")
                except: pass
                results.append(f"OPEN: Port {port} ({service})")
            sock.close()
        except: pass
        
    with open(report_file, "w") as f:
        f.write(f"--- AUTOSCAN REPORT: {target_ip} ---\n")
        f.write(f"Date: {datetime.now()}\n\n")
        if not results:
            f.write("No open ports found.\n")
        else:
            f.write("\n".join(results))
            
    print(f"[+] Scan Complete. Report saved to: {report_file}")

# --- WORKER THREAD (GUI Scanner) ---
class PortScannerWorker(QThread):
    update_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, target_ip):
        super().__init__()
        self.target_ip = target_ip

    def run(self):
        self.update_signal.emit(f"🚀 Starting Deep Scan on {self.target_ip}...\n")
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1433, 3306, 3389, 5900, 8080]
        
        open_ports = 0
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.0)
                result = sock.connect_ex((self.target_ip, port))
                
                if result == 0:
                    try: service_name = socket.getservbyport(port, "tcp")
                    except: service_name = "unknown"
                    
                    banner = ""
                    try:
                        if port in [80, 8080, 443]: sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
                        banner_bytes = sock.recv(1024)
                        banner = banner_bytes.decode('utf-8', errors='ignore').strip().split('\n')[0]
                    except: pass
                    
                    if banner: display_msg = f"✅ OPEN: Port {port} ({service_name}) | 📝 {banner}"
                    else: display_msg = f"✅ OPEN: Port {port} ({service_name})"
                    
                    self.update_signal.emit(display_msg)
                    open_ports += 1
                sock.close()
            except Exception: pass
        
        if open_ports == 0: self.update_signal.emit(f"\n🚫 No open ports found.")
        else: self.update_signal.emit(f"\n🏁 Scan Complete. Found {open_ports} open ports.")
        self.finished_signal.emit()

# --- PDF REPORT CLASS ---
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'SysAdmin Toolbox - Security Scan Report', 0, 1, 'C')
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# --- MAIN APPLICATION ---
class SysAdminToolbox(QMainWindow):
    def __init__(self):
        super().__init__()
        
        if hasattr(sys, '_MEIPASS'):
            self.base_dir = sys._MEIPASS
        else:
            self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        ui_path = os.path.join(self.base_dir, "assets", "toolbox.ui")
        self.data_dir = os.path.join(os.getcwd(), "data")
        if not os.path.exists(self.data_dir): os.makedirs(self.data_dir)
        self.db_path = os.path.join(self.data_dir, "fim_baseline.db")
        
        uic.loadUi(ui_path, self)

        # 1. Dashboard Connections
        try:
            self.btn_monitor_2.clicked.connect(self.run_monitor)
            self.btn_disk_2.clicked.connect(self.run_disk)
            self.btn_fim_init_2.clicked.connect(self.run_fim_init)
            self.btn_fim_check_2.clicked.connect(self.run_fim_check)
            self.btn_logs_2.clicked.connect(self.run_logs)
            self.btn_backup_2.clicked.connect(self.run_backup)
            self.btn_battery_2.clicked.connect(self.run_battery)
        except AttributeError: pass

        # 2. Service Manager
        try:
            self.btn_svc_status_2.clicked.connect(self.service_status)
            self.btn_svc_restart_2.clicked.connect(self.service_restart)
            self.btn_svc_stop_2.clicked.connect(self.service_stop)
        except AttributeError: pass

        # 3. Network Scanner
        try:
            self.btn_scan.clicked.connect(self.start_port_scan)
            self.input_ip.returnPressed.connect(self.start_port_scan)
            self.text_scan_result.setReadOnly(True)
            self.text_scan_result.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.text_scan_result.customContextMenuRequested.connect(self.show_context_menu)
        except AttributeError: pass

        # 4. TASK SCHEDULER (New Feature)
        try:
            self.btn_add_task.clicked.connect(self.add_scheduler_task)
            self.btn_delete_task.clicked.connect(self.delete_scheduler_task)
            self.refresh_task_list()
        except AttributeError:
            print("⚠️ Scheduler widgets not found in UI. Please update toolbox.ui")

        self.setWindowTitle("Futhark's SysAdmin Toolbox v3.0 (Automation Edition)")

    # --- SCHEDULER LOGIC ---
    def get_python_path(self):
        return sys.executable

    def get_script_path(self):
        return os.path.abspath(__file__)

    def refresh_task_list(self):
        self.list_tasks.clear()
        try:
            # Crontab listesini çek
            output = subprocess.check_output("crontab -l", shell=True, text=True)
            for line in output.splitlines():
                if "SysAdminToolbox" in line:
                    self.list_tasks.addItem(line)
        except subprocess.CalledProcessError:
            pass # Crontab boş olabilir

    def add_scheduler_task(self):
        time = self.time_scheduler.time()
        hour = time.hour()
        minute = time.minute()
        
        task_type = self.combo_task_type.currentText()
        target = self.input_task_target.text().strip()
        
        if not target:
            QMessageBox.warning(self, "Error", "Please enter a Target IP or Path!")
            return

        # Cron komutunu oluştur (Headless mod çağrısı)
        # Örn: 30 14 * * * /usr/bin/python3 /path/to/main.py --scan 192.168.1.1 # SysAdminToolbox
        
        py_exec = self.get_python_path()
        script = self.get_script_path()
        
        if "Scan" in task_type:
            cmd = f"{minute} {hour} * * * {py_exec} {script} --scan {target} # SysAdminToolbox-Scan"
        elif "Backup" in task_type:
            # Backup için basit bir tar komutu
            backup_name = f"/tmp/backup_$(date +\%Y\%m\%d).tar.gz"
            cmd = f"{minute} {hour} * * * tar -czf {backup_name} {target} # SysAdminToolbox-Backup"
        else:
            return

        # Crontab'a ekle
        try:
            # Mevcut cronları al
            current_cron = subprocess.run("crontab -l", shell=True, capture_output=True, text=True).stdout
            
            # Yeni satırı ekle
            new_cron = current_cron + "\n" + cmd + "\n"
            
            # Yaz (echo "..." | crontab -)
            process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
            process.communicate(new_cron)
            
            QMessageBox.information(self, "Success", f"Task Scheduled for {hour}:{minute}!")
            self.refresh_task_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def delete_scheduler_task(self):
        selected_item = self.list_tasks.currentItem()
        if not selected_item: return
        
        task_line = selected_item.text()
        
        try:
            current_cron = subprocess.check_output("crontab -l", shell=True, text=True)
            # Seçilen satır hariç diğerlerini tut
            new_cron = "\n".join([line for line in current_cron.splitlines() if line.strip() != task_line.strip()])
            new_cron += "\n"
            
            process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
            process.communicate(new_cron)
            
            self.refresh_task_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # --- EXISTING FUNCTIONS ---
    def show_context_menu(self, pos: QPoint):
        menu = QMenu(self)
        export_action = menu.addAction("📄 Export to PDF")
        action = menu.exec(self.text_scan_result.mapToGlobal(pos))
        if action == export_action: self.export_pdf()

    def export_pdf(self):
        content = self.text_scan_result.toPlainText()
        target_ip = self.input_ip.text()
        if not content.strip(): return
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Report", f"ScanReport_{target_ip}.pdf", "PDF Files (*.pdf)")
        if file_name:
            try:
                safe_content = content.encode('latin-1', 'ignore').decode('latin-1')
                pdf = PDFReport()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(0, 10, f"Target IP: {target_ip}", 0, 1)
                pdf.cell(0, 10, f"Date: {datetime.now()}", 0, 1)
                pdf.ln(10)
                pdf.set_font("Courier", size=10) 
                pdf.multi_cell(0, 10, safe_content)
                pdf.output(file_name)
                self.text_scan_result.append(f"\n💾 Report saved: {file_name}")
            except Exception as e: self.text_scan_result.append(f"\n❌ PDF Error: {str(e)}")

    def run_command(self, command):
        output_widget = getattr(self, "text_output", getattr(self, "text_output_2", None))
        if output_widget:
            output_widget.clear()
            output_widget.append(f"> Executing: {command}\n")
            output_widget.repaint()
            try:
                result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT, cwd=self.base_dir)
                output_widget.append(result)
            except subprocess.CalledProcessError as e:
                output_widget.append(f"❌ Error (Code {e.returncode}):\n{e.output}\n")
            scrollbar = output_widget.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    def start_port_scan(self):
        target_ip = self.input_ip.text().strip()
        if not target_ip: target_ip = "127.0.0.1"; self.input_ip.setText(target_ip)
        self.output_area = self.text_scan_result
        self.output_area.clear()
        self.output_area.append(f"📡 Initializing Deep Scan on {target_ip}...\n")
        self.btn_scan.setEnabled(False)
        self.worker = PortScannerWorker(target_ip)
        self.worker.update_signal.connect(self.update_scan_log)
        self.worker.finished_signal.connect(self.scan_finished)
        self.worker.start()

    def update_scan_log(self, message):
        if "OPEN" in message: self.output_area.append(f"<span style='color:#00ff00; font-weight:bold;'>{message}</span>")
        else: self.output_area.append(f"<span style='color:#aaaaaa;'>{message}</span>")

    def scan_finished(self):
        self.btn_scan.setEnabled(True)
        self.output_area.append("\n✅ <b style='color:white;'>Scan Finished. (Right-click to Export PDF)</b>")

    def run_monitor(self): self.run_command("echo '--- Kernel ---'; uname -r; echo ''; echo '--- Uptime ---'; uptime -p; echo ''; echo '--- Memory ---'; free -h")
    def run_disk(self): self.text_output.append("🔵 Analyzing Disk Usage..."); cmd = r"echo '--- Partition Usage ---'; df -h /; echo ''; echo '--- Large Files in /var/log ---'; find /var/log -type f -size +100M -exec ls -lh {} \; 2>/dev/null || echo 'No large files found.'"; self.run_command(cmd)
    def run_fim_init(self): cmd = ("rm -f data/fim_baseline.db; " "find . -maxdepth 2 -type f \\( -name '*.txt' -o -name '*.sh' -o -name '*.py' \\) " "-not -path '*/.*' " "-exec sha256sum {} + > data/fim_baseline.db 2>/dev/null && " "echo '✅ Baseline Created!'"); self.run_command(cmd)
    def run_fim_check(self):
        if not os.path.exists(self.db_path): self.run_command("echo '⚠️ Error: Baseline not found.'"); return
        self.run_command("sha256sum -c data/fim_baseline.db")
    def run_logs(self): cmd = """echo "--- 1. SSH: Invalid Users ---"; journalctl -u sshd | grep "Invalid user" | tail -n 5 || echo "Clean."; echo "\n--- 2. SUDO: Violations ---"; journalctl _COMM=sudo | grep "NOT in sudoers" | tail -n 5 || echo "Clean." """; self.run_command(cmd)
    def run_backup(self):
        target_dir = QFileDialog.getExistingDirectory(self, "Select Directory")
        if target_dir: name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"; self.run_command(f"tar -czf {name} '{target_dir}' && echo '✅ Done: {name}'")
    def run_battery(self): cmd = r"upower -i $(upower -e | grep 'BAT' | head -n 1) | grep -E 'state|to full|percentage|capacity' || true"; self.run_command(cmd)
    def get_service_name(self):
        try: name = self.input_service_2.text().strip()
        except AttributeError:
            try: name = self.input_service.text().strip()
            except AttributeError: name = ""
        if not name: self.run_command("echo '⚠️ Enter service name.'"); return None
        return name
    def service_status(self): svc = self.get_service_name(); 
    if svc: self.run_command(f"systemctl status {svc} --no-pager")
    def service_restart(self): svc = self.get_service_name(); 
    if svc: self.run_command(f"pkexec systemctl restart {svc} && echo '✅ Service {svc} restarted!'")
    def service_stop(self): svc = self.get_service_name(); 
    if svc: self.run_command(f"pkexec systemctl stop {svc} && echo '✅ Service {svc} stopped.'")

# --- ENTRY POINT (CLI + GUI) ---
if __name__ == "__main__":
    # Eğer komut satırından "--scan" argümanı gelirse GUI'yi başlatma!
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scan" and len(sys.argv) > 2:
            target = sys.argv[2]
            headless_scan(target)
            sys.exit(0) # Programı burada bitir
    
    # Argüman yoksa GUI'yi başlat
    app = QApplication(sys.argv)
    window = SysAdminToolbox()
    window.show()
    sys.exit(app.exec())
