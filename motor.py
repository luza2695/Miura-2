##################################################################
# Miura 2: Motor Code (sensors.py)
# Created: 5/30/2018
# Modified: 6/20/2018
# Purpose: Defines functions to initialize, turn on, and turn off the motor
##################################################################

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor
import time
import atexit
import RPi.GPIO as GPIO

mh = Adafruit_MotorHAT()

def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

myStepper = mh.getStepper(200, 1)
myStepper.setSpeed(70)

def main():
	myStepper.step(4500, Adafruit_MotorHAT.BACKWARD,  Adafruit_MotorHAT.DOUBLE)
	return
