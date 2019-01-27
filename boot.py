#!/usr/bin/python

import os
import sys
import signal
import subprocess
from time import sleep
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library

pro = None

def restart():
    global pro
    if pro is not None:
        print('Stopping previous program.')
        os.killpg(os.getpgid(pro.pid), signal.SIGTERM)  # Send the signal to all the process groups
        sleep(1)

    subprocess.call('if [ -d ./app ]; then rm -Rf ./mrbean-robot-master; fi', shell=True)
    subprocess.call('wget https://github.com/gmamaladze/mrbean-robot/archive/master.zip', shell=True)
    subprocess.call('unzip master.zip -d ./', shell=True)
    subprocess.call('pip3 install -r ./mrbean-robot-master/requirements.txt', shell=True)
    command='python3 ./mrbean-robot-master/main.py'
    print('Starting new program.')
    pro = subprocess.Popen(command, stdout=sys.stdout, stderr=subprocess.STDOUT, shell=True, preexec_fn=os.setsid)


def button_callback(channel):
    print('Button was pressed.')

def init():
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
    GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(7, GPIO.RISING, callback=button_callback)  # Setup event on pin 10 rising edge
    input("Press enter to quit\n\n")
