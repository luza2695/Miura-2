##################################################################
# Miura 2: Motor Code (motor.py)
# Created: 5/30/2018
# Modified: 6/20/2018
# Purpose: Function to run motor
##################################################################

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor
import time
import atexit

mh = Adafruit_MotorHAT()

def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

myStepper = mh.getStepper(200, 1)
myStepper.setSpeed(70)

def main():
	myStepper.step(9000, Adafruit_MotorHAT.BACKWARD,  Adafruit_MotorHAT.DOUBLE)
	return
