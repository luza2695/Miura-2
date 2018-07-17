##################################################################
# Miura 2: Light Functions (downlink.py)
# Created: 6/5/2018
# Modified: 6/30/2018
# Purpose: Functions to turn on lights and control celebration
##################################################################
#import time
#import smbus
import RPi.GPIO as GPIO
import time
import smbus
#import glob

lights_pin = 11
stage_1 = 38
stage_2 = 35
stage_3 = 36
stage_4 = 33
stage_5 = 32
emergency_pressure_led = 31
emergency_temperature_led = 29

#GPIO.cleanup()
GPIO.setwarning(False)
GPIO.setmode(GPIO.BOARD)

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
	GPIO.output(lights_pin, GPIO.HIGH)


def epilepsy():
	for x in range(0,5):
		GPIO.output(lights, HIGH)
		GPIO.output(stage_1, HIGH)
		GPIO.output(stage_3, HIGH)
		GPIO.output(stage_5, HIGH)
		GPIO.output(emergency_temperature_led, HIGH)

		GPIO.output(stage_2, LOW)
		GPIO.output(stage_4, LOW)
		GPIO.output(emergency_pressure_led, LOW)

		time.sleep(0.5)

		GPIO.output(lights,LOW)
		GPIO.output(stage_1, LOW)
		GPIO.output(stage_3, LOW)
		GPIO.output(stage_5, LOW)
		GPIO.output(emergency_temperature_led, LOW)

		GPIO.output(stage_2, HIGH)
		GPIO.output(stage_4, HIGH)
		GPIO.output(emergency_pressure_led, HIGH)

		time.sleep(0.5)
	GPIO.output(lights, HIGH)

lights_on()
