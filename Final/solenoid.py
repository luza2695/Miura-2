import RPi.GPIO as GPIO
import time

solenoid_pin = 18
exhaust_pin = 16
GPIO.setmode(GPIO.BOARD)
GPIO.setup(solenoid_pin, GPIO.OUT)
GPIO.setwarnings(False)
GPIO.cleanup()

def openPressurize():
	print("attempting to open")
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(solenoid_pin, GPIO.OUT)
	GPIO.output(solenoid_pin, True)

def closePressurize():
	print("attempting to close")
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(solenoid_pin, GPIO.OUT)
	GPIO.output(solenoid_pin, False)

def openExhaust():
	print("attempting to open")
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(exhaust_pin, GPIO.OUT)
	GPIO.output(exhaust_pin, True)

def closeExhaust():
	print("attempting to close")
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(exhaust_pin, GPIO.OUT)
	GPIO.output(exhaust_pin, False)
