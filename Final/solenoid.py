import RPi.GPIO as GPIO
import time

pressurize_pin = 18
exhaust_pin = 16
motor_pin = 12
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pressurize_pin, GPIO.OUT)
GPIO.setup(motor_pin, GPIO.OUT)


def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pressurize_pin, GPIO.OUT)
	GPIO.setup(exhaust_pin, GPIO.OUT)
	GPIO.setup(motor_pin, GPIO.OUT)

def openPressurize():
	print("attempting to open")
	GPIO.output(motor_pin, False)
	time.sleep(0.3)
	GPIO.output(pressurize_pin, True)
	

def closePressurize():
	print("attempting to close")
	setup()
	GPIO.output(pressurize_pin, False)

def openExhaust():
	print("attempting to open")
	setup()
	GPIO.output(pressurize_pin, True)
	GPIO.output(motor_pin, True)

def closeExhaust():
	print("attempting to close")
	setup()
	GPIO.output(pressurize_pin, False)
