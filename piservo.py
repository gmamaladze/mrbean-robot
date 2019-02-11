import RPi.GPIO as GPIO


class Head():

	def __init__(self, start=25, stop=125+10, step=10):
		GPIO.setup(40, GPIO.OUT)
		self.servo = GPIO.PWM(40, 50)						
		self.position = 0
		self.direction = 1
		self.positions=[round(p/10, 1) for p in [pint for pint in range(start, stop, step)]]
		pos_value = self.positions[self.position]
		self.servo.start(pos_value)
		
	def set_position(self, position):
		self.position=position 
		pos_value = self.positions[self.position]
		self.servo.ChangeDutyCycle(pos_value)

	def next(self):
		current_position = self.position
		pos_value = self.positions[current_position]
		self.servo.ChangeDutyCycle(pos_value)
		self.position = self.position + self.direction
		if self.position>=len(self.positions)-1:
			self.direction = -1
			self.position = len(self.positions)-1
		elif self.position==0:
			self.direction = 1
			self.position = 0
		return current_position
