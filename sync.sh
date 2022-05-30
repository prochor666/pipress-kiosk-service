#!/bin/bash

while true
do
    # run sync
    python3 api_sync.py

    # sleep for n minutes
    sleep 60
done
