##################################################################
# Miura 2: Motor Code (motor.py)
# Created: 5/30/2018
# Modified: 6/20/2018
# Purpose: Function to run motor
##################################################################
import time
import atexit

def main():
	from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor

	mh = Adafruit_MotorHAT()

	myStepper = mh.getStepper(200, 1)
	myStepper.setSpeed(70)

	myStepper.step(7500, Adafruit_MotorHAT.BACKWARD,  Adafruit_MotorHAT.DOUBLE)
	return

def test():
	from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor

	mh = Adafruit_MotorHAT()

	myStepper = mh.getStepper(200, 1)
	myStepper.setSpeed(70)

	counter = 0
	while True:
		myStepper.step(100, Adafruit_MotorHAT.BACKWARD,  Adafruit_MotorHAT.DOUBLE)
		counter += 1
		print(counter*100)
		time.sleep(0.5)
	return
