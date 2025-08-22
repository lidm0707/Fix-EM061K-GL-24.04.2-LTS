#!/usr/bin/env python3
import sys
import subprocess
import glob
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QAction, QIcon

APN = "h2g2"

def run_command(cmd):
    try:
        output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return output.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def find_quectel_device():
    """ค้นหา /dev/cdc-wdmX ของ Quectel EM061K-GL อัตโนมัติ"""
    for dev in glob.glob("/dev/cdc-wdm*"):
        cmd = f"udevadm info -a -n {dev}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if "EM061K-GL" in result.stdout:
            return dev
    return None

def find_modem_id():
    """ค้นหา modem id ของ Quectel EM061K-GL ใน ModemManager"""
    output = run_command("mmcli -L")
    for line in output.splitlines():
        if "EM061K-GL" in line:
            # line: /org/freedesktop/ModemManager1/Modem/0 [Quectel] EM061K-GL
            parts = line.split("/")
            if len(parts) > 0:
                return parts[-1].split()[0]  # modem id
    return None

def check_radio(device):
    cmd = f"sudo mbimcli -p -d {device} -v --quectel-query-radio-state"
    return run_command(cmd)

def unlock_radio(device):
    cmd = f"sudo mbimcli -p -d {device} -v --quectel-set-radio-state=on"
    return run_command(cmd)

def enable_modem(modem_id):
    cmd = f"sudo mmcli --modem {modem_id} --enable"
    return run_command(cmd)

def set_apn(modem_id):
    cmd = f"sudo mmcli -m {modem_id} --simple-connect='apn={APN}'"
    return run_command(cmd)

def activate_modem():
    device = find_quectel_device()
    if not device:
        print("Quectel EM061K-GL device not found!")
        return

    modem_id = find_modem_id()
    if not modem_id:
        print("ModemManager does not detect EM061K-GL!")
        return

    status = check_radio(device)
    if "fcc-locked" in status.lower():
        unlock_radio(device)
    enable_modem(modem_id)
    set_apn(modem_id)
    print("Modem activated!")

# --- GUI tray ---
app = QApplication(sys.argv)
tray = QSystemTrayIcon()
tray.setIcon(QIcon.fromTheme("network-wireless"))

menu = QMenu()
action_activate = QAction("Activate 5G Modem")
action_quit = QAction("Quit")

action_activate.triggered.connect(activate_modem)
action_quit.triggered.connect(app.quit)

menu.addAction(action_activate)
menu.addAction(action_quit)
tray.setContextMenu(menu)
tray.show()

sys.exit(app.exec())
