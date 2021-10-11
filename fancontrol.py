from gpiozero import OutputDevice
import subprocess
from datetime import datetime
import time
import sys

######################################################################
# nohup sudo python3 fancontrol.py --auto >> fancontrol.log 2>&1 &
######################################################################

pin = 18
upperThreshold = 65.0
lowerThreshold = 50.0
sleep_value = 30
args = sys.argv

MODE_AUTO = '--auto'
MODE_CHECK = '--check-temp'
LOG_FILE = 'fancontrol.log'


def logger(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        time_format = '%Y-%m-%d %H:%m:%S'
        with open(LOG_FILE, 'a') as f:
            f.write(f"[{datetime.now().strftime(time_format)}] -> FUNCTION: {func.__name__}\n")
            f.write(f"[{datetime.now().strftime(time_format)}] -> results: {result}\n")
        return result
    return wrapper


@logger
def check_temp():
    output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
    temp = output.stdout.decode()
    temp = temp.split('=')[1].split('\'')[0]
    return temp
 

def fancontrol(fan):
    temp = float(check_temp())
    if temp >= upperThreshold:
        turnFan(fan, "on")
    elif temp <= lowerThreshold:
        turnFan(fan, "off")


@logger
def turnFan(fan, onoff):
    if onoff == "on":
        fan.on()
    if onoff == "off":
        fan.off()
    return onoff


def main(args):
    if len(args) <= 1:
        print(f"Mode not recognized. Please type {MODE_AUTO} or {MODE_CHECK}")
    else:
        mode = args[1]
        if mode == MODE_AUTO:
            fan = OutputDevice(pin)
            turnFan(fan, "on")
            while True:
                fancontrol(fan)
                time.sleep(sleep_value)
        elif mode == MODE_CHECK:
            temp = float(check_temp())
        else:
            print(f"Mode not recognized. Please type {MODE_AUTO} or {MODE_CHECK}")


if __name__ == '__main__':
    main(args)
