##################################################################
# Miura 2: Light Functions (downlink.py)
# Created: 6/5/2018
# Modified: 6/30/2018
# Purpose: Functions to turn on lights and control celebration
##################################################################
import time
import smbus
import RPi.GPIO as GPIO

lights = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setwarning(False)
GPIO.setup(lights, GPIO.OUT)

# Functions
def lights_on():
	GPIO.output(lights, HIGH)


def epilepsy():
	for x in range(0,3)
		GPIO.output(lights, HIGH)
		time.sleep(0.5)
		GPIO.output(lights,LOW)
		time.sleep(0.5)