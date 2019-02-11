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
    time.sleep(1)
    distance = sonar.get_distance()
    distances.append(distance)

m3 = PiMotor.Motor("MOTOR3",1)
m4 = PiMotor.Motor("MOTOR4",1)

while True:
    position = head.next()
    time.sleep(1)
    distance = sonar.get_distance()
    distances[position] = (distances[position] + 3 * distance) / 4
    preferred_direction = distances.index(max(distances))
    delta_v = (preferred_direction - 5) * 10
    m3.forward(50 - delta_v)
    m4.forward(50 + delta_v)

exit(0)

def head_rotation():
    pass

_thread.start_new_thread(head_rotation)


# Pfeile
ab = PiMotor.Arrow(1)
al = PiMotor.Arrow(2)
af = PiMotor.Arrow(3) 
ar = PiMotor.Arrow(4)

# gerade aus
af.on()
m3.forward(100)
m4.forward(100)
time.sleep(5)

# rückwärts
af.off()
ab.on()
m3.reverse(100)
m4.reverse(100)
time.sleep(5)

# links
ab.off()
al.on()
m3.forward(100)
m4.reverse(100)
time.sleep(5)

# rechts
ar.on()
al.off()
m3.reverse(100)
m4.forward(100)
time.sleep(5)

# stop
al.off()
af.off()
ar.off()
m3.stop()
m4.stop()
time.sleep(1)
