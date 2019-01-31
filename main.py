#!/usr/bin/python

import PiMotor
import time
import _thread
import polly
import sonar

hans = polly.Polly('Hans')
hans.say('Hallo, mein name ist Mister Bean. Ich bin ein selbstgebastelter Roboter. Ich kann reden, sehen und fahren.')

while True:
    dist = sonar.distance()
    text = 'Abstand {} Centimeter.'.format(round(dist))
    hans.say(text)
    time.sleep(1)

# Antriebe
stepper = PiMotor.Stepper("STEPPER1")

def head_rotation():
    while True:
        stepper.forward(0.01,180)  # Delay and rotations
        time.sleep(1)
        stepper.backward(0.01,360)
        time.sleep(1)
        stepper.forward(0.01,180)  # Delay and rotations
        time.sleep(1)

exit(0)

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
