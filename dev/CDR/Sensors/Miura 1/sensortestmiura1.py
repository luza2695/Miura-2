################################################################
#Purpose:
#
#Created: 4/6/2018
#Modified: -/-
#
#Miura 2: Prototype (sensortest.py)
################################################################
import sched
import os
import time
import smbus
import RPi.GPIO as GPIO
import math
import re
from w1thermsensor import W1ThermSensor
#humidity sensor
bus.write_byte(0x40, 0xF5)
time.sleep(0.3)
data0 = bus.read_byte(0x40)
data1 = bus.read_byte(0x40)
humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
time.sleep(0.3)

#temperature sensor
for sensor in W1ThermSensor.get_available_sensors(): # Grab temp values from all available sensors in a round robin fashion
	data.append(temp_find(sensor.id))
	data.append(sensor.get_temperature())

#pressure sensor
data = bus.read_i2c_block_data(0x60, 0x00, 4)
pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16 # Use with humidity sensor?
pressure = (pres / 4.0) / 1000.0
