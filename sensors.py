##################################################################
# Miura 2: Sensor Code (sensors.py)
# Created: 5/30/2018
# Modified: 6/20/2018
# Purpose: Defines functions to take sensor data
##################################################################

import os
import glob
import time
import smbus
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
#import board
#import busio
#import digitalio
#import adafruit_max31865

# i2c sensor ids
pres_id = 0x60
hum_id = 0x68
bus = smbus.SMBus(1)

# defines number of temp sensors
num_temp = 0

# automatically finds temp sensor addresses
device_file = []
base_dir = '/sys/bus/w1/devices/'

for i in range(0,num_temp):
	device_folder = glob.glob(base_dir + '28*')[i]
	device_file.append(device_folder + '/w1_slave')

# reads external pressure sensor
def read_pressure():
	bus.write_byte_data(pres_id, 0x26, 0x39)
	data = bus.read_i2c_block_data(pres_id, 0x00, 4)
	temp = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
	pressure = (temp * 101.324998) / 4000
	return pressure

# reads external humidity
def read_humid():
	data = bus.read_i2c_block_data(hum_id, 0x00, 4)
	humidity = ((((data[0] & 0x3F) * 256) + data[1]) * 100.0) / 16383.0
	return humidity

# reads temp from each sensor
def read_temp():
	temp_c = ()
	for i in range(0,num_temp):
		f = open(device_file[i], 'r')
		start = time.time()
		lines = f.readlines()
		print(time.time() - start)
		f.close()
		equals_pos = lines[1].find('t=')
		if equals_pos != -1:
			temp_string = lines[1][equals_pos+2:]
			temp_c = temp_c + (float(temp_string)/1000.0,)
	return temp_c

# Temperature Transducer 
# Initialize SPI bus and sensor.
# def read_temperature_system():
# 	spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# 	cs = digitalio.DigitalInOut(board.D5)  # Chip select of the MAX31865 board.
# 	sensor = adafruit_max31865.MAX31865(spi, cs)
# 	temperature_system = sensor.temperature
# 	return temperature_system

#16 bit for the ADC
#input solenoid 1
adc1 = Adafruit_ADS1x15.ADS1115()
#input solenoid 2
adc2 = Adafruit_ADS1x15.ADS1115()
#exhaust solenoid
adc3 = Adafruit_ADS1x15.ADS1115()

#Gains
# - 2/3 = +/- 6.144V
# - 1 = +/- 4.096V
# - 2 = +/- 2.048V
# - 4 = +/- 1.024V
# - 8 = +/- 0.512V
# - 16 = +/- 0.256V
GAIN = 1

adc1.start_adc(0, gain = GAIN)
adc2.start_adc(1, gain = GAIN)
adc3.start_adc(2, gain = GAIN)

# clears channel
throwaway = adc1.get_last_result()
throwaway = adc2.get_last_result()
throwaway = adc3.get_last_result()

# reads pressure of pressure system from transducer
def read_pressure_system():
        value1 = adc1.get_last_result()
        value2 = adc2.get_last_result()
        value3 = adc3.get_last_result()
        pressureSol1 = value1*50/65536
        pressureSol2 = value2*50/65536
        pressureMain  = value3*50/65536
        return [pressureSol1, pressureSol2, pressureMain]

# prints value of each sensor
def print_sensors():
	print('Reading...')
	#print ambient pressure data
	pressure = read_pressure()
	print('Pressure: {:.2f} atm '.format(pressure), end='')
	
	#print ambient humidity data
	humidity = read_humid()
	print('Humidity: {:.2f} %% '.format(humidity), end='')
	
	#print ambient temperature data
	temperature = read_temp()
	print('Temperature: {:.2f} C  {:.2f} C  {:.2f} C  {:.2f} C'.format(*temperature), end='')

	#print temperature transducer data
	#temperature_system = read_temperature_system()
	#print('Temperature Transducer: {:.2f} %% '.format(temperature_system), end='')

	#print pressure transducer data
	pressure_system = read_pressure_system()
	print('Pressure Transducer: {:.2f} C {:.2f} C {:.2f} C'.format(pressure_system), end='')
	return

# returns value of each sensor in downlinking format
def read_sensors():
	#read and downlink ambient pressure data
	pressure = read_pressure()
	pres_downlink = ['SE','PR','{:.2f}'.format(pressure)]

	#read and downlink ambient humidity data
	humidity = read_humid()
	hum_downlink = ['SE','HU','{:.2f}'.format(humidity)]

	#read and downlink ambient temperature data
	temperature = read_temp()
	temp_downlink = ['SE','TE','{:.2f} {:.2f} {:.2f} {:.2f}'.format(0,0,0,0)]

	#read and downlink temperature transducer data
	# temperature_system = read_temperature_system()
	# temp_trans_downlink = ['SE','TT','{:.2f}'.format(temperature_system)]

	return [pres_downlink,hum_downlink,temp_downlink]

# returns value of each system transducer in downlinking format
def read_transducers():
	#read and downlink pressure transducer data
	pressure_system = read_pressure_system()
	pres_trans_downlink = ['SE', 'PT','{:.2f} {:.2f} {:.2f}'.format(*pressure_system)]
	return pres_trans_downlink


