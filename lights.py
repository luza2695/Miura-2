##################################################################
# Purpose: Controls/tests the outside luminati lights
# Created: 6/5/2018
# Modified: 6/7/2018
# Miura2 - lights.py
##################################################################
# Imports
import time
import smbus
import RPi.GPIO as GPIO
##################################################################
# Setup
lights = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setwarning(False)
GPIO.setup(lights, GPIO.OUT)

# Functions
def lights_on():
    GPIO.output(lights, HIGH)


def epilepsy():
    
