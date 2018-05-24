<<<<<<< HEAD
import time
import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(31, GPIO.OUT)
#GPIO.setup(6, GPIO.OUT)
GPIO.output(31, GPIO.LOW)

for x in range(20):
    GPIO.output(31, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(31, GPIO.LOW)
    time.sleep(0.5)

GPIO.cleanup()   
=======
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
>>>>>>> 07199942460ee8a9de3ef410ca6ff460e689055c
