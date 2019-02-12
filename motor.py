import RPi.GPIO as GPIO


class Motor:
    """ Class to handle interaction with the motor pins
    Supports redefinition of "forward" and "backward" depending on how motors are connected
    Use the supplied Motorshieldtest module to test the correct configuration for your project.

    Arguments:
    motor = string motor pin label (i.e. "MOTOR1","MOTOR2","MOTOR3","MOTOR4") identifying the pins to which
            the motor is connected.
    config = int defining which pins control "forward" and "backward" movement.
    """
    motor_pins = {"MOTOR4": {"config": {1: {"e": 32, "f": 24, "r": 26}, 2: {"e": 32, "f": 26, "r": 24}}, "arrow": 1},
                  "MOTOR3": {"config": {1: {"e": 19, "f": 21, "r": 23}, 2: {"e": 19, "f": 23, "r": 21}}, "arrow": 2},
                  "MOTOR2": {"config": {1: {"e": 22, "f": 16, "r": 18}, 2: {"e": 22, "f": 18, "r": 16}}, "arrow": 3},
                  "MOTOR1": {"config": {1: {"e": 11, "f": 15, "r": 13}, 2: {"e": 11, "f": 13, "r": 15}}, "arrow": 4}}

    def __init__(self, motor_id, config = 1):
        motor = 'MOTOR' + str(motor_id)
        self.pins = self.motor_pins[motor]["config"][config]
        GPIO.setup(self.pins['e'], GPIO.OUT)
        GPIO.setup(self.pins['f'], GPIO.OUT)
        GPIO.setup(self.pins['r'], GPIO.OUT)
        self.PWM = GPIO.PWM(self.pins['e'], 50)  # 50Hz frequency
        self.PWM.start(0)
        GPIO.output(self.pins['e'], GPIO.HIGH)
        GPIO.output(self.pins['f'], GPIO.LOW)
        GPIO.output(self.pins['r'], GPIO.LOW)

    def forward(self, speed):
        """ Starts the motor turning in its configured "forward" direction.

        Arguments:
        speed = Duty Cycle Percentage from 0 to 100.
        0 - stop and 100 - maximum speed
        """
        self.PWM.ChangeDutyCycle(speed)
        GPIO.output(self.pins['f'], GPIO.HIGH)
        GPIO.output(self.pins['r'], GPIO.LOW)

    def reverse(self, speed):
        """ Starts the motor turning in its configured "reverse" direction.

        Arguments:
        speed = Duty Cycle Percentage from 0 to 100.
        0 - stop and 100 - maximum speed
        """
        self.PWM.ChangeDutyCycle(speed)
        GPIO.output(self.pins['f'], GPIO.LOW)
        GPIO.output(self.pins['r'], GPIO.HIGH)

    def stop(self):
        """ Stops power to the motor,
        """
        self.PWM.ChangeDutyCycle(0)
        GPIO.output(self.pins['f'], GPIO.LOW)
        GPIO.output(self.pins['r'], GPIO.LOW)


