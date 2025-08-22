# Fix EM061K-GL on Ubuntu 24.04.2 LTS

This guide helps you set up and run the 5G modem tray script for the Quectel EM061K-GL on Ubuntu 24.04.2 LTS (ThinkPad T14 Gen 5).

---

## 0️⃣ Clone the Repository and Enter Directory

```bash
# Clone your project repository
git clone https://github.com/yourusername/auto_script.git

# Change directory into the project
cd auto_script/opnradio


## 1️⃣ Setup Python Virtual Environment and Activate

```bash
# Create venv if not exist
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Or if already created
source /home/<username>/code/auto_script/opnradio/venv/bin/python

```

## 2️⃣ Install Required Python Packages
```bash
# Upgrade pip
pip install --upgrade pip

# Install PyQt6
pip install PyQt6

# Verify installation
python -m pip show PyQt6

```

## 3️⃣ Run the Tray Script
```bash
python modem_tray.py
```

The tray icon will appear in the system tray.

Click Activate 5G Modem to enable the modem.

Reference: [AskUbuntu - Fix Mobile Broadband WWAN with Quectel EM061K-GL](https://askubuntu.com/questions/1536697/how-do-i-fix-mobile-broadband-wwan-with-quectel-em061k-gl-on-thinkpad-t14-gen-5)

## 4️⃣ Run Script on Startup
```bash
mkdir -p ~/.config/autostart
nano ~/.config/autostart/activate_5g_modem_tray.desktop

```
```bash
[Desktop Entry]
Type=Application
Name=Activate 5G Modem Tray
Exec=/home/<username>/code/auto_script/opnradio/venv/bin/python /home/<username>/code/auto_script/opnradio/modem_tray.py
Icon=network-wireless
Comment=Tray icon to activate 5G modem
Terminal=false

```
```bash
chmod +x ~/.config/autostart/activate_5g_modem_tray.desktop
```

## 5️⃣ Optional: Test Tray Script Manually
```bash
/home/<username>/code/auto_script/opnradio/venv/bin/python /home/<username>/code/auto_script/opnradio/modem_tray.py
```