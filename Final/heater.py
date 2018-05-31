##############################################################################
# Purpose:
#	- Be able to control the heaters individually with GPIO pins
#	- Four heaters: payload, exhaust valve, solenoid 1, solenoid 2
#	- 2 functions: 1) payload 2) solenoid 1, solenoid 2, exhaust valve
# Created: 5/30/2018
# Modified: -/-
# Miura2 -  heater.py
# Creator: Lucas Zardini

##############################################################################
#imports
import RPi.GPIO as GPIO
import time

##############################################################################
# turns payload heater on or off
def payload_heater(state):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7,GPIO.OUT)
	GPIO.output(7,state)
	return

# Turns solenoid heater on or off
def solenoid_heater(state):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(8,GPIO.OUT)
	GPIO.output(8,state)
	return

