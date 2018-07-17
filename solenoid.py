##################################################################
# Miura 2: Solenoid Control (solenoid.py)
# Created: 5/24/2018
# Modified: 6/20/2018
# Purpose: Control solenoids for pressurization process
##################################################################
import RPi.GPIO as GPIO
import time

pressurize_pin1 = 15
pressurize_pin2 = 12
exhaust_pin = 16
motor_driver_pin = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(pressurize_pin1, GPIO.OUT)
GPIO.setup(pressurize_pin2, GPIO.OUT)
GPIO.setup(exhaust_pin, GPIO.OUT)
GPIO.setup(motor_driver_pin, GPIO.OUT)
GPIO.output(motor_driver_pin, False)

def openPressurize(solenoid_id):
	GPIO.output(motor_driver_pin, False)
	time.sleep(0.3)
	if solenoid_id == 1:
		GPIO.output(pressurize_pin1, True)
	elif solenoid_id == 2:
		GPIO.output(pressurize_pin2, True)

def closePressurize(solenoid_id):
	if solenoid_id == 1:
		GPIO.output(pressurize_pin1, False)
	elif solenoid_id == 2:
		GPIO.output(pressurize_pin2, False)

def openExhaust():
	GPIO.output(exhaust_pin, True)
	GPIO.output(motor_driver_pin, True)

def closeExhaust():
	GPIO.output(exhaust_pin, False)

#openPressurize(2)
#time.sleep(1)
#closePressurize(2)
#time.sleep(3)
#openExhaust()
