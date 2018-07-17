##################################################################
# Miura 2: Light Functions (downlink.py)
# Created: 6/5/2018
# Modified: 6/30/2018
# Purpose: Functions to turn on lights and control celebration
##################################################################
import RPi.GPIO as GPIO
import time

lights_pin = 11
stage_1 = 38
stage_2 = 35
stage_3 = 36
stage_4 = 33
stage_5 = 32
emergency_pressure_led = 31
emergency_temperature_led = 29

GPIO.setup(lights_pin, GPIO.OUT)
GPIO.setup(stage_1, GPIO.OUT)
GPIO.setup(stage_2, GPIO.OUT)
GPIO.setup(stage_3, GPIO.OUT)
GPIO.setup(stage_4, GPIO.OUT)
GPIO.setup(stage_5, GPIO.OUT)
GPIO.setup(emergency_pressure_led, GPIO.OUT)
GPIO.setup(emergency_temperature_led, GPIO.OUT)

# Functions
def lights_on():
	GPIO.output(lights_pin, True)

def epilepsy():
	for x in range(0,5):
		GPIO.output(lights_pin, True)
		GPIO.output(stage_1, True)
		GPIO.output(stage_3, True)
		GPIO.output(stage_5, True)
		GPIO.output(emergency_temperature_led, True)

		GPIO.output(stage_2, False)
		GPIO.output(stage_4, False)
		GPIO.output(emergency_pressure_led, False)

		time.sleep(0.5)

		GPIO.output(lights_pin, False)
		GPIO.output(stage_1, False)
		GPIO.output(stage_3, False)
		GPIO.output(stage_5, False)
		GPIO.output(emergency_temperature_led, False)

		GPIO.output(stage_2, True)
		GPIO.output(stage_4, True)
		GPIO.output(emergency_pressure_led, True)

		time.sleep(0.5)
	GPIO.output(lights_pin, True)

lights_on()
