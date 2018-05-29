############################################################################
# Purpose:
#	- Read Pressure data from pressure transducer
#	- Create function that can be called for pressure checks
#
# Created: 5/25/2018
# Modified: 5/29/2018
#
# pressure.py
############################################################################
# Imports
import time
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
############################################################################
#16 bit for the ADC
adc = Adafruit_ADS1x15.ADS1115()

#Gains
# - 2/3 = +/- 6.144V
# - 1 = +/- 4.096V
# - 2 = +/- 2.048V
# - 4 = +/- 1.024V
# - 8 = +/- 0.512V
# - 16 = +/- 0.256V
GAIN = 1

adc.start_adc(0, gain = GAIN)

def pressureRead():
	while True:
		value = adc.get_last_result()
		volts = value*5/65536
		pressure = volts*10
		print('Volts: {} V'.format(volts))
		print('Pressure: {} psi'.format(pressure))
		time.sleep(1)

pressureRead()
