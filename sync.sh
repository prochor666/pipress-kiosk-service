#!/bin/bash

while true
do
    # run sync
    python3 api_sync.py

    # sleep for n minutes
    minutes = 5
    sleep 60*minutes
done
