import motor
import arrow
import voice
import sonar
import head
import mouse
import vision
import RPi.GPIO as GPIO
import logging


class Robot:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        self.voice = voice.Voice()
        self.head = head.Head()
        self.sonar = sonar.Sonar()
        self.mouse = mouse.Mouse()

        self.motor_right = motor.Motor(motor_id=3)
        self.motor_left = motor.Motor(motor_id=4)

        self.arrow_back = arrow.Arrow(1)
        self.arrow_left = arrow.Arrow(2)
        self.arrow_forward = arrow.Arrow(3)
        self.arrow_right = arrow.Arrow(4)
        self.vision = vision.Vision(rotation=90)

    def __enter__(self):
        self.mouse.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mouse.__exit__(exc_val, exc_tb)
        logging.debug(exc_val)
        GPIO.cleanup()

    def drive(self, speed_left, speed_right):
        self.motor_right.drive(speed_right)
        self.motor_left.drive(speed_left)

    def turn(self, speed=100):
        self.motor_left.drive(speed)
        self.motor_right.drive(-speed)
