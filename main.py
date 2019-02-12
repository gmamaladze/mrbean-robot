#!/usr/bin/python

import motor
import time

import arrow
import voice
import sonar
import head
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


hans = voice.Voice()
# hans.say('Hallo, mein name ist Mister Bean.')
head = head.Head()
sonar = sonar.Sonar()

distances = list()
for i in range(0, head.nr_of_positions):
    head.set_position(i)
    time.sleep(0.05)
    distance = sonar.get_distance()
    distances.append(distance)

motor_left = motor.Motor(motor_id=3)
motor_right = motor.Motor(motor_id=4)

arrow_back = arrow.Arrow(1)
arrow_left = arrow.Arrow(2)
arrow_forward = arrow.Arrow(3)
arrow_right = arrow.Arrow(4)

arrows = [arrow_right, arrow_forward, arrow_left]
arrow_index = 0


# Main loop
while True:
    position = head.next()
    time.sleep(0.05)
    distance = sonar.get_distance()
    distances[position] = distance
    preferred_direction = distances.index(max(distances))
    delta_v = round((preferred_direction - head.nr_of_positions / 2) * 10)
    motor_left.forward(50 + delta_v)
    motor_right.forward(50 - delta_v)

    arrows[arrow_index].off()
    arrow_index = preferred_direction * 3 // head.nr_of_positions
    arrows[arrow_index].on()
