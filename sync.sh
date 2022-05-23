#!/bin/bash

while true
do
    # run sync
    python3 media_sync.py

    # sleep for 30 minutes
    sleep 60*30
done

