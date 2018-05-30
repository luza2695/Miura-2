##################################################################
# Miura 2: Sensor Code (sensors.py)
# Created: 5/30/2018
# Modified: 5/30/2018
# Purpose: Defines functions to take sensor data
##################################################################

import os
import glob
import time
import smbus

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

pres_id = 0x60
hum_id = 0x68
bus = smbus.SMBus(1)

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

num_temp = 4
device_file = []

for i in range(0,num_temp):
    device_folder = glob.glob(base_dir + '28*')[i]
    device_file.append(device_folder + '/w1_slave')

def read_pressure():
	bus.write_byte_data(pres_id, 0x26, 0x39)
	data = bus.read_i2c_block_data(pres_id, 0x00, 4)
	temp = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
	pressure = (temp / 4.0) / 1000.0
	return pressure

def read_humid():
	data = bus.read_i2c_block_data(hum_id, 0x00, 4)
	humidity = ((((data[0] & 0x3F) * 256) + data[1]) * 100.0) / 16383.0
	return humidity

def read_temp_raw():
    lines = []
    for i in range(0,num_temp):
        f = open(device_file[i], 'r')
        lines.append(f.readlines())
        f.close()
    return lines

def read_temp():
    lines_list = read_temp_raw()
    temp_c = []
    for i in range(0,num_temp):
        lines = lines_list[i]
        while lines[0].strip()[-3:] != 'YES':
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            current = float(temp_string) / 1000.0
            temp_c.append(current)
    return temp_c
    
def print_sensors():
	print("Reading...")
	pressure = read_pressure()
	print(("Pressure: %.2f kPa ") % (pressure), end="")
	humidity = read_humid()
	print(("Humidity: %.2f %% ") % (humidity), end="")
	temperature = read_temp()
	print("Temperature: ", end="")
	for i in range(0,num_temp):
			print(("%.2f C ") % (temperature[i]), end="")
	print("")
	return

def read_sensors():
	pressure = read_pressure()
	humidity = read_humid()
	temperature = read_temp()
	return pressure, humidity, temperature