##################################################################
# Miura 2: Heater Functions (heater.py)
# Created: 5/30/2018
# Modified: 6/20/2018
# Purpose: Control individual heaters throughout payload
##################################################################
import RPi.GPIO as GPIO
import time

payload_heater_pin = 22
solenoid_heater_pin = 37
regulator_heater_pin = 40

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

