#!/bin/bash

cd /opt/pipress-kiosk-service

while true
do
    # clear command file
    if [[ -f "/tmp/pipress-remote-command.ended" && ! -f "/tmp/pipress-remote-command.running" ]];
    then

        rm -rf /tmp/pipress-remote-command.sh
        rm -rf /tmp/pipress-remote-command.ended
    fi

    # run sync
    if [[ -f "/tmp/pipress-remote-command.sh" ]];
    then

        dos2unix /tmp/pipress-remote-command.sh
        chmod +x /tmp/pipress-remote-command.sh
        echo 'running' > /tmp/pipress-remote-command.running
        source /tmp/pipress-remote-command.sh
        rm -rf /tmp/pipress-remote-command.running
        sleep 1
        echo 'ended' > /tmp/pipress-remote-command.ended
    fi

    # sleep for n minutes
    sleep 10
done
