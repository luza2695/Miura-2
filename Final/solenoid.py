##################################################################
# Miura 2: Solenoid Control (solenoid.py)
# Created: 5/24/2018
# Modified: 5/29/2018
# Purpose: Control solenoids for pressurization process
##################################################################

import RPi.GPIO as GPIO
import time

pressurize_pin = 12
exhaust_pin = 16
motor_pin = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pressurize_pin, GPIO.OUT)
GPIO.setup(exhaust_pin, GPIO.OUT)
GPIO.setup(motor_pin, GPIO.OUT)

def openPressurize():
	GPIO.output(motor_pin, False)
	time.sleep(0.3)
	GPIO.output(pressurize_pin, True)

def closePressurize():
	GPIO.output(pressurize_pin, False)

def openExhaust():
	GPIO.output(exhaust_pin, True)
	GPIO.output(motor_pin, True)

def closeExhaust():
	GPIO.output(exhaust_pin, False)

def burp():
	burp_rate = 0.05
	for i in range(0,50):
		GPIO.output(exhaust_pin, True)
		time.sleep(burp_rate)
		GPIO.output(exhaust_pin, False)
		time.sleep(burp_rate)
