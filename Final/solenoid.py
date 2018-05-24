import RPi.GPIO as GPIO
import time

def openSolenoid():
	solenoid_pin = 18
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(solenoid_pin, GPIO.OUT)
	GPIO.output(solenoid_pin, True)
	GPIO.cleanup()

def closeSolenoid():
	solenoid_pin = 18
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(solenoid_pin, GPIO.OUT)
	GPIO.output(solenoid_pin, False)
	GPIO.cleanup()