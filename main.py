#!/usr/bin/python

import PiMotor
import time


# Antriebe
stepper = PiMotor.Stepper("STEPPER1")

stepper.forward(0.0,50)  # Delay and rotations
time.sleep(2)
stepper.backward(0.0,50)
time.sleep(2)
exit(0)

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
