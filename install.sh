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
    sudo pip install psutil
    sudo pip install passlib
    sudo pip install websocket
    sudo pip install websocket-client
    sudo pip install requests
    sudo pip install fake-rpigpio

    if [[ ! -d temp ]];
    then
        sudo mkdir -p temp
        echo "Created directory /temp created"
    else
        echo "Directory /temp exists"
    fi
fi

# Sensor service installer into /opt

sudo echo "
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

sudo echo "
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

# Run services

#sudo systemctl enable pipress-kiosk-sensor
#sudo systemctl start pipress-kiosk-sensor

#sudo systemctl enable pipress-kiosk-service
#sudo systemctl start pipress-kiosk-service
