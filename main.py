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

arrows = [ar, af, al]
arrow_index = 0

def emergency_turn():
    ab.on()
    m3.forward(0)
    m4.forward(0)
    while True:
        time.sleep(1)
        m3.forward(0)
        m4.forward(0)
        for i in range(0, len(head.positions)):
            head.set_position(i)
            time.sleep(0.1)
            distances[i] = sonar.get_distance()
        if distances[4]>20 and distances[5]>20 and distances[6]>20:
            break
        m3.forward(100)
        m4.reverse(100)
    ab.off()

while True:
    position = head.next()
    time.sleep(0.1)
    distance = sonar.get_distance()
    distances[position] = distance
    preferred_direction = distances.index(max(distances))
    delta_v = (preferred_direction - 5) * 10
    m3.forward(50 + delta_v)
    m4.forward(50 - delta_v)

    if distances[4]<20 or distances[5]<20 or distances[6]<20:
        emergency_turn()
        for i in range(0, len(head.positions)):
            head.set_position(i)
            time.sleep(0.1)
            distances[i] = sonar.get_distance()

    arrows[arrow_index].off()
    arrow_index = preferred_direction * 3 // len(head.positions)
    arrows[arrow_index].on()

