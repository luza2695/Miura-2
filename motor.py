##################################################################
# Miura 2: Motor Code (motor.py)
# Created: 5/30/2018
# Modified: 6/20/2018
# Purpose: Function to run motor
##################################################################
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x70)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

myStepper = mh.getStepper(200, 1)  # 200 steps/rev, motor port #1
myStepper.setSpeed(70)             # 70 RPM

def main():
	myStepper.step(7000, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.DOUBLE)
	turnOffMotors()
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
