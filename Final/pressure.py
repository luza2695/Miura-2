############################################################################
# Purpose:
# Created:
# Modified:
# pressure.py
############################################################################
# Imports
import time
import RPi.GPIO as GPIO
import smbus
############################################################################
bus = smbus.SMBus(0)
address = 0x48


def pressureRead():
	while True:
		pres_input = bus.read_byte_data(address,1)
		print("Pressure: " + str(pres_input) + "PSI")
		time.sleep(1)

pressureRead()
