import time
import RPi.GPIO as GPIO

SIGNAL_PIN = 29

GPIO.setmode(GPIO.BOARD)

timeout = 0.020

def distance():
    GPIO.setup(SIGNAL_PIN, GPIO.OUT)
    #cleanup output
    GPIO.output(SIGNAL_PIN, 0)

    time.sleep(0.000002)

    #send signal
    GPIO.output(SIGNAL_PIN, 1)

    time.sleep(0.000005)

    GPIO.output(SIGNAL_PIN, 0)

    GPIO.setup(SIGNAL_PIN, GPIO.IN)
    
    goodread=True
    watchtime=time.time()
    while GPIO.input(SIGNAL_PIN)==0 and goodread:
            starttime=time.time()
            if (starttime-watchtime > timeout):
                    goodread=False

    if goodread:
            watchtime=time.time()
            while GPIO.input(SIGNAL_PIN)==1 and goodread:
                    endtime=time.time()
                    if (endtime-watchtime > timeout):
                            goodread=False
    
    if goodread:
            duration=endtime-starttime
            distance=duration*34000/2
            yield distance

