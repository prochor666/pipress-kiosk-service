import os
import json
from pipress import core

try:
    import RPi.GPIO as GPIO

except (RuntimeError, ModuleNotFoundError):

    import fake_rpigpio.utils
    fake_rpigpio.utils.install()


def read_sensor(conf):
    GPIO.setmode(GPIO.BOARD)  # set GPIO pin numbering
    data_pin = 26  # associate pin 26 to pir
    GPIO.setup(data_pin, GPIO.IN)  # set sensor pin

    # print(core.device)

    if core.device == 'pi':
        web_data_dir = f"{conf['storage']['web_data_dir_prod']}"
    else:
        web_data_dir = f"{conf['storage']['web_data_dir_dev']}"

    local_json_dir = core.check_dir(
        f"{web_data_dir}/json")

    data = {
        'active': True
    }

    if conf['sensor'] == True:
        if GPIO.input(data_pin):
            data['active'] = True
        else:
            data['active'] = False

    # print(f"{local_json_dir}/activity.json")
    core.file_save(
        f"{local_json_dir}/activity.json", json.dumps(data))


