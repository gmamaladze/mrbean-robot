import RPi.GPIO as GPIO
import logging


class Head:
    MIN = 2.5
    MAX = 12.5

    def __init__(self, nr_of_positions=15, pin_number=40):
        self.pin_number = pin_number
        self.nr_of_positions = nr_of_positions
        self.position = nr_of_positions // 2
        self.direction = 1
        self.step = (Head.MAX - Head.MIN) / nr_of_positions

    def __enter__(self):
        GPIO.setup(self.pin_number, GPIO.OUT)
        self.servo = GPIO.PWM(40, 50)
        self.servo.start(self.position)
        logging.debug('head entered.')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.servo.stop()
        GPIO.cleanup(self.pin_number)
        logging.debug('head exited.')

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
        duty_cycle_value = Head.MIN + self.step * position
        self.servo.ChangeDutyCycle(duty_cycle_value)
        return self.position

    def next(self):
        next_position = self.position + self.direction
        return self.set_position(next_position)
