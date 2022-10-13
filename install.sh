#!/bin/bash

echo "Pipress service installer" > install.log

# Logging
exec > >(tee -a install.log) 2>&1


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
    pip install urllib3

    if [[ ! -d temp ]];
    then
        mkdir -p temp
        echo "Created directory /temp created"
    else
        echo "Directory /temp exists"
    fi
fi

# Sensor service installer into /opt

echo "
[Unit]
Description=Pipress kiosk sensor service
After=network.target

[Service]
User=root
WorkingDirectory=/opt/pipress-kiosk-service
ExecStart=/usr/bin/python /opt/pipress-kiosk-service/sense.py
Restart=always

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/pipress-kiosk-sensor.service

# Data service installer into /opt

echo "
[Unit]
Description=Pipress kiosk communication service
After=network.target

[Service]
User=root
WorkingDirectory=/opt/pipress-kiosk-service
ExecStart=/opt/pipress-kiosk-service/sync.sh
Restart=always

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/pipress-kiosk-service.service

# System wide updater

cp /opt/pipress-kiosk-service/system-update.sh /opt/system-update.sh
dos2unix /opt/system-update.sh
chmod +x /opt/system-update.sh

echo "
[Unit]
Description=Pipress kiosk updater service
After=network.target

[Service]
User=root
WorkingDirectory=/opt
ExecStart=/opt/system-update.sh
Restart=always

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/pipress-kiosk-system-update.service


# Run services

systemctl enable pipress-kiosk-sensor
systemctl start pipress-kiosk-sensor

systemctl enable pipress-kiosk-service
systemctl start pipress-kiosk-service

systemctl enable pipress-kiosk-system-update
systemctl start pipress-kiosk-system-update
