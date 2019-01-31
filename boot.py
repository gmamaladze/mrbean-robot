import os
import sys
import signal
import subprocess
from time import sleep
import RPi.GPIO as GPIO
import threading

pro = None
e = None

def start():
    global pro
    if pro is not None:
        stop()
    flash_on(leds_green_on)
    subprocess.call('if [ -f ./master.zip ]; then rm -Rf ./master.zip; fi', shell=True)
    subprocess.call('if [ -d ./mrbean-robot-master ]; then rm -Rf ./mrbean-robot-master; fi', shell=True)
    subprocess.call('wget https://github.com/gmamaladze/mrbean-robot/archive/master.zip', shell=True)
    subprocess.call('unzip master.zip -d ./', shell=True)
    subprocess.call('pip3 install -r ./mrbean-robot-master/requirements.txt', shell=True)
    command='python3 ./mrbean-robot-master/main.py'
    print('Starting new program.')
    flash_off()
    pro = subprocess.Popen(command, stdout=sys.stdout, stderr=subprocess.STDOUT, shell=True, preexec_fn=os.setsid)
    pro.wait()
    stop()
    
def stop():
    global pro
    if pro is not None:
        print('Stopping previous program.')
        try:
            os.killpg(os.getpgid(pro.pid), signal.SIGTERM)  # Send the signal to all the process groups
            sleep(1)
        except ProcessLookupError:
            pass
        pro = None
    flash_on(leds_red_on)

pins={1:33,2:35,3:37,4:36}

def leds_off():
    for pin in pins.values():
        GPIO.output(pin, GPIO.LOW)

def leds_red_on():
    leds_off()
    GPIO.output(pins[2], GPIO.HIGH)
    GPIO.output(pins[4], GPIO.HIGH)

def leds_green_on():
    leds_off()
    GPIO.output(pins[1], GPIO.HIGH)
    GPIO.output(pins[3], GPIO.HIGH)


def flash_async(e, led_func):
    while not e.isSet():
        led_func()
        sleep(0.5)
        leds_off()
        sleep(0.5)

def flash_on(led_func):
    flash_off()
    global e
    e = threading.Event()
    t = threading.Thread(name='non-block', target=flash_async, args=(e, led_func))
    t.start()

def flash_off():
    global e
    if e is not None:
        e.set()
        sleep(1)
    leds_off()


def button_callback(channel):
    print('Button was pressed.')
    if pro is None:
        start()
    else:
        stop()

def init():
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
    GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(7, GPIO.RISING, callback=button_callback)  # Setup event on pin 10 rising edge
    for pin in pins.values():
        GPIO.setup(pin,GPIO.OUT)


init()
stop()
print('Press button on mrbean-robot to get the new version of code from github and restart.')
while True:
    sleep(10)