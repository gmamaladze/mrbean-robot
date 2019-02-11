#!/usr/bin/python

import PiMotor
import time
import _thread
import polly
import sonar
import piservo

hans = polly.Polly('Hans')
hans.unmute()
hans.say('Hallo, mein name ist Mister Bean.')
head = piservo.Head()

while True:
    head.center()
    time.sleep(2)
    distance = round(sonar.get_distance())
    hans.say('Vorne {}'.format(distance))

    head.right()
    time.sleep(2)
    distance = round(sonar.get_distance())
    hans.say('Rechts {}'.format(distance))

    head.left()
    time.sleep(2)
    distance = round(sonar.get_distance())
    hans.say('Links {}'.format(distance))

exit(0)

def head_rotation():
    pass

_thread.start_new_thread(head_rotation)

m3 = PiMotor.Motor("MOTOR3",1)
m4 = PiMotor.Motor("MOTOR4",1)

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
