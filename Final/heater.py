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
#Payload heater
def heaterPayload(x):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7,GPIO.OUT)
	while True:
		GPIO.output(7,x)

#Valve heaters
def heaterValve(x):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(8,GPIO.OUT)
	while True:
		GPIO.output(8,x)

