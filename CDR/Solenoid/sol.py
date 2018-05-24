import RPi.GPIO as GPIO
import time

solenoid_pin = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(solenoid_pin, GPIO.OUT)

def openSolenoid():
	GPIO.output(solenoid_pin, True)

def closeSolenoid():
	GPIO.output(solenoid_pin, False)