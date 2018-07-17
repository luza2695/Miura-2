##################################################################
# Miura 2: GPIO Setup (gpiosetup.py)
# Created: 5/1/2018
# Modified: 6/30/2018
# Purpose: Cleans and initializes gpio
##################################################################
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
