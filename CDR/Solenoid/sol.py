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
