##################################################################
# Miura 2: Heater Functions (heater.py)
# Created: 5/30/2018
# Modified: 6/20/2018
# Purpose: Control individual heaters throughout payload
##################################################################
import RPi.GPIO as GPIO

solenoid_heater_pin = 22
regulator_heater_pin = 40

GPIO.setup(solenoid_heater_pin, GPIO.OUT)
GPIO.setup(regulator_heater_pin, GPIO.OUT)

# Turns solenoid heater on or off
def solenoid_heater(state):
	GPIO.output(solenoid_heater_pin,state)
	return

# Turns regulator heater on or off
def regulator_heater(state):
	GPIO.output(regulator_heater_pin,state)
	return
