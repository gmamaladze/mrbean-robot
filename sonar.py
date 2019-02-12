import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

timeout = 0.020


class Sonar:

    def __init__(self, signal_pin=29):
        self.signal_pin = signal_pin
        GPIO.setup(self.signal_pin, GPIO.OUT)

    def get_distance(self):
        while True:

            # reset
            GPIO.output(self.signal_pin, 0)
            time.sleep(0.000002)

            # send signal
            GPIO.output(self.signal_pin, 1)
            time.sleep(0.000005)
            GPIO.output(self.signal_pin, 0)

            # Wait for echo
            GPIO.setup(self.signal_pin, GPIO.IN)
            good_read = True
            watch_time = time.time()
            while GPIO.input(self.signal_pin) == 0 and good_read:
                start_time = time.time()
                if start_time - watch_time > timeout:
                    good_read = False

            if good_read:
                watch_time = time.time()
                while GPIO.input(self.signal_pin) == 1 and good_read:
                    end_time = time.time()
                    if end_time - watch_time > timeout:
                        good_read = False

            if good_read:
                duration = end_time - start_time
                distance = duration * 34000 / 2
                return distance
