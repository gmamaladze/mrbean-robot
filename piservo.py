import RPi.GPIO as GPIO
import time
import os


class Head:
	def __init__(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(40, GPIO.OUT)
		self.servo = GPIO.PWM(11, 50)						
		self.servo.start(2.5)

	def left(self):
		self.servo.ChangeDutyCycle(2.5)

	def right(self):
		self.servo.ChangeDutyCycle(12.5)
		
	def center(self):
		self.servo.ChangeDutyCycle(7.5)