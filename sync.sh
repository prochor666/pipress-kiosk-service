#!/bin/bash

cd /opt/pipress-kiosk-service

while true
do
    # run sync
    python api_sync.py

    # sleep for n minutes
    sleep 60
done
