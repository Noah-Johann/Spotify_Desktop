#!/bin/bash

# Variablen
SCRIPT_DIR=$(dirname "$(realpath "$0")")
PYTHON_SCRIPT="$SCRIPT_DIR/main.py"
SERVICE_NAME="main_script.service"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME"

echo "=== Automatische Einrichtung des Systemd-Services für main.py ==="

# Prüfe, ob die main.py existiert
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Fehler: $PYTHON_SCRIPT wurde nicht gefunden!"
    echo "Bitte stelle sicher, dass die Datei main.py im gleichen Ordner wie dieses Skript existiert."
    exit 1
fi

# Erstelle die systemd-Service-Datei
echo "Erstelle die systemd-Service-Datei..."
sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Python Main Script Autostart
After=graphical.target

[Service]
ExecStart=/usr/bin/python3 $PYTHON_SCRIPT
WorkingDirectory=$SCRIPT_DIR
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi
Environment=DISPLAY=:0

[Install]
WantedBy=graphical.target
EOL

# Berechtigungen setzen und Service aktivieren
echo "Lade die Systemd-Daemon-Konfiguration neu..."
sudo systemctl daemon-reload

echo "Aktiviere den Service $SERVICE_NAME..."
sudo systemctl enable $SERVICE_NAME

echo "Starte den Service $SERVICE_NAME..."
sudo systemctl start $SERVICE_NAME

echo "Überprüfe den Status des Services..."
sudo systemctl status $SERVICE_NAME

echo "=== Einrichtung abgeschlossen! ==="
echo "Dein Skript wird jetzt automatisch im Vollbildmodus beim Start des Raspberry Pi ausgeführt."