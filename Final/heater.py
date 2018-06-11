##############################################################################
# Purpose:
#	- Be able to control the heaters individually with GPIO pins
#	- Four heaters: payload, exhaust valve, solenoid 1, solenoid 2
#	- 2 functions: 1) payload 2) solenoid 1, solenoid 2, exhaust valve
# Created: 5/30/2018
# Modified: -/-
# Miura2 -  heater.py
# Creator: Lucas Zardini

import RPi.GPIO as GPIO
import time

payload_heater_pin = 7
solenoid_heater_pin = 8
regulator_heater_pin = 9

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(payload_heater_pin, GPIO.OUT)
GPIO.setup(solenoid_heater_pin, GPIO.OUT)
GPIO.setup(regulator_heater_pin, GPIO.OUT)

# turns payload heater on or off
def payload_heater(state):
	GPIO.output(payload_heater_pin,state)
	return

# Turns solenoid heater on or off
def solenoid_heater(state):
	GPIO.output(solenoid_heater_pin,state)
	return

# Turns regular heater on or off
def regulator_heater(state):
	GPIO.output(regulator_heater_pin,state)
	return

