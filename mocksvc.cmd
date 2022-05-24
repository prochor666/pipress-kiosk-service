@ECHO OFF

:loop
    cls
    ECHO Pipress service emulation for Windows
    ECHO -------------------------------------
    python media_sync.py
    ping -n 11 127.0.0.1 > nul

goto loop