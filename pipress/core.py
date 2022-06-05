from subprocess import call
import requests
import uuid
import re
import psutil
import urllib3
import platform
import os
import sys
import json

try:
    import RPi.GPIO as GPIO

    device = 'pi'
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()

    device = 'fake-pi'


root_dir = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))


def mac():
    return ':'.join(re.findall('..', '%012x' % uuid.getnode()))


def check_dir(dir_abs_path):

    if not os.path.isdir(dir_abs_path):
        os.mkdir(dir_abs_path)

    return dir_abs_path


def reboot():
    os_command('sudo reboot')


def os_command(command):
    call(command, shell=True)


def file_save(file, content=' '):
    fh = open(file, 'w')
    fh.write(content)
    fh.close()


def download_file(file_name_remote, file_name_local):

    http = urllib3.PoolManager()
    r = http.request(
        'GET', file_name_remote, preload_content=False)

    if r.status == 200:

        with open(file_name_local, 'wb') as f:

            for chunk in r.stream(32768):

                f.write(chunk)
                f.flush()
                os.fsync(f.fileno())

            f.close()

"""
    r = requests.get(file_name_remote, stream=True)
    if r.status_code == 200:
        with open(file_name_local, 'wb') as f:

            for chunk in r.iter_content(1024):

                if not chunk:
                    break

                f.write(chunk)
                f.flush()
                os.fsync(f.fileno())

            f.close() """


def refresh_browser():
    os_command(
        'export XAUTHORITY=/home/pi/.Xauthority; export DISPLAY=:0; xdotool getactivewindow key ctrl+F5')


def report():
    r = {'device': device}
    r['system'], r['node'], r['release'], r['version'], r['machine'], r['processor'] = platform.uname()
    r['version_parsed'] = r['version'].split('-')[0]
    r['cores'] = psutil.cpu_count()
    r['cpu_percent'] = psutil.cpu_percent()
    r['memory_percent'] = psutil.virtual_memory()[2]
    r['disk_total'] = psutil.disk_usage('/')[0]
    r['disk_used'] = psutil.disk_usage('/')[1]
    r['disk_free'] = psutil.disk_usage('/')[2]
    r['disk_percent'] = psutil.disk_usage('/')[3]
    r['boot_time'] = psutil.boot_time()

    print(json.dumps(r, indent = 4))
    # api('mac-report/?mac='+mac()+'&report='+json.dumps(r))


def debug(s):
    print(f"---- PIPRESS ----> {str(s)}")
