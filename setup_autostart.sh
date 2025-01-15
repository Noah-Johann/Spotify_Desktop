#!/bin/bash

# Prüfen ob das Skript mit root-Rechten ausgeführt wird
if [ "$EUID" -ne 0 ]; then 
    echo "Bitte Skript mit sudo ausführen"
    echo "Beispiel: sudo ./setup.sh"
    exit 1
fi

# Aktuelles Verzeichnis ermitteln
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Erstelle Service-Datei für systemd
cat > /etc/systemd/system/python-fullscreen.service << EOF
[Unit]
Description=Python Fullscreen Autostart
After=network.target

[Service]
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/pi/.Xauthority
User=pi
WorkingDirectory=$SCRIPT_DIR
ExecStart=$SCRIPT_DIR/venv/bin/python3 -c '
import tkinter as tk
import os
import sys

root = tk.Tk()
root.attributes("-fullscreen", True)
root.config(cursor="none")  # Versteckt den Mauszeiger

# Füge das aktuelle Verzeichnis zum Python-Pfad hinzu
program_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(program_dir)

# Importiere das Hauptprogramm
import main
'
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Aktiviere den Autostart des X-Servers für den pi Benutzer
raspi-config nonint do_boot_behaviour B4

# Aktiviere und starte den Service
systemctl enable python-fullscreen.service
systemctl start python-fullscreen.service

echo "Installation erfolgreich!"
echo "Spotify wird nun automatisch im Vollbildmodus gestartet"
echo "Um den Autostart zu deaktivieren, führe aus: sudo systemctl disable python-fullscreen.service"

