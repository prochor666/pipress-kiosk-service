@ECHO OFF
cls
WHERE /Q python

ECHO Pipress service installer

IF %ERRORLEVEL% NEQ 0 (
    ECHO Python 3 is required
    EXIT /B 0
)

FOR /F "tokens=2" %%G IN ('python -V') do (SET version_raw=%%G)

SET modified=%version_raw:.=%
SET /A num=%modified%+0

IF %num% LSS 373 (
    ECHO Python 3.7.3 or newer is required
    EXIT /B 0
) ELSE (
    ECHO Python %version_raw% found
)

WHERE /Q pip

IF %ERRORLEVEL% NEQ 0 (
    ECHO PIP is required
    EXIT /B 0
) ELSE (
    pip install psutil
    pip install passlib
    pip install websocket
    pip install websocket-client
    pip install requests
    pip install fake-rpigpio
    pip install urllib3

    IF exist temp (
        echo Directory /temp exists
    ) ELSE (
        mkdir logs && echo Directory /temp created
    )
)
