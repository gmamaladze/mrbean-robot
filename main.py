#!/usr/bin/python

import PiMotor
import time
import _thread
import polly
import sonar
import piservo

hans = polly.Polly('Hans')
hans.unmute()
#hans.say('Hallo, mein name ist Mister Bean.')
head = piservo.Head()

distances = list()
for i in range(0, len(head.positions)):
    head.set_position(i)
    time.sleep(0.1)
    distance = sonar.get_distance()
    distances.append(distance)

m3 = PiMotor.Motor("MOTOR3",1)
m4 = PiMotor.Motor("MOTOR4",1)

# Arrows
ab = PiMotor.Arrow(1)
al = PiMotor.Arrow(2)
af = PiMotor.Arrow(3) 
ar = PiMotor.Arrow(4)

arrows = [al, af, ar]
arrow_index = 0

def emergency_turn():
    m3.stop()
    m4.stop()
    time.sleep(1)
    head.set_position(5)
    m3.forward(25)
    m4.reverse(25)
    while True:
        distance = sonar.get_distance()
        if distance>50:
            break
    m3.stop()
    m4.stop()

while True:
    position = head.next()
    time.sleep(0.1)
    distance = sonar.get_distance()
    distances[position] = distance
    preferred_direction = distances.index(max(distances))
    delta_v = (preferred_direction - 5) * 10
    m3.forward(50 + delta_v)
    m4.forward(50 - delta_v)

    if min(distances)<20:
        emergency_turn()

    arrows[arrow_index].off()
    arrow_index = round(preferred_direction * 3 / len(head.positions))
    arrows[arrow_index].on()

