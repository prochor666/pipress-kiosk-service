#!/bin/bash

echo "Pipress service installer"

PYTHON="$(which python3)"
PIP="$(which pip)"

if [[ ! -x "$PYTHON" ]];
then
    echo  "Python 3 is required, exiting..."
    exit 1
fi

VERSIONRAW="$($PYTHON -V)"
EMPT=""
CLEAN="${VERSIONRAW/Python /$EMPT}"
NUM="${CLEAN//./$EMPT}"

echo $NUM

if [[ "$NUM" -lt "373" ]];
then
    echo "Python 3.7.3 or newer is required"
    exit 1
fi

if [[ ! -x "$PIP" ]];
then
    echo  "PIP is required, exiting..."
    exit 1
fi

if [[ -x "$PYTHON" ]] & [[ -x "$PIP" ]];
then
    pip install psutil
    pip install passlib
    pip install websocket
    pip install websocket-client
    pip install requests
    pip install fake-rpigpio

    if [[ ! -d temp ]];
    then
        mkdir -p logs
        echo "Created directory /temp created"
    else
        echo "Directory /temp exists"
    fi
fi


sudo echo "[Unit]
Description=Pipress data sync service
After=network.target
[Service]
User=root
WorkingDirectory=/opt/pipress-kiosk-service
ExecStart=/opt/pipress-kiosk-service/sync.sh
Restart=always
[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/pipress-kiosk-service.service

sudo systemctl enable pipress-kiosk-service
sudo systemctl start pipress-kiosk-service
sudo systemctl status pipress-kiosk-service
