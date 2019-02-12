import RPi.GPIO as GPIO


class Head:
    MIN = 25
    MAX = 125

    def __init__(self, nr_of_positions=15, pin_number=40):
        GPIO.setup(pin_number, GPIO.OUT)
        self.nr_of_positions = nr_of_positions
        self.servo = GPIO.PWM(40, 50)
        self.position = nr_of_positions // 2
        self.direction = 1
        self.step = (Head.MAX - Head.MIN) / nr_of_positions
        self.servo.start(self.position)

    def center(self):
        self.set_position(self.nr_of_positions // 2)

    def set_position(self, position):
        if position < 0:
            self.direction = 1
            return self.set_position(1)
        elif position >= self.nr_of_positions:
            self.direction = -1
            return self.set_position(self.nr_of_positions - 2)
        self.position = position
        self.servo.ChangeDutyCycle(self.step * position, 2)

    def next(self):
        next_position = self.position + self.direction
        return self.set_position(next_position)
