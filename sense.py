from pipress import config, compat, sensor
import time

conf = config.configure()

# If compat = False, break
compat.check_version()

while True:

    s = sensor.read_sensor(conf)
    time.sleep(2)
