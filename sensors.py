##################################################################
# Miura 2: Sensor Code (sensors.py)
# Created: 5/30/2018
# Modified: 6/20/2018
# Purpose: Functions to take sensor data
##################################################################
import os
import glob
import time
import smbus
import RPi.GPIO as GPIO
import Adafruit_ADS1x15

# i2c sensor ids
pres_id = 0x60
hum_id = 0x40
bus = smbus.SMBus(1)

# defines number of temp sensors
num_temp = 8

# pressure sensors setup
bus.write_byte_data(pres_id, 0x26, 0x00)

# humidity sensors setup
#bus.write_byte(0x40,0xE5)

# automatically finds temp sensor addresses
device_file = ['/sys/bus/w1/devices/28-000009958138/w1_slave','/sys/bus/w1/devices/28-000009957683/w1_slave','/sys/bus/w1/devices/28-000009958549/w1_slave','/sys/bus/w1/devices/28-0000099577b3/w1_slave','/sys/bus/w1/devices/28-00000995861d/w1_slave','/sys/bus/w1/devices/28-0000099566dc/w1_slave','/sys/bus/w1/devices/28-000009957c5d/w1_slave','/sys/bus/w1/devices/28-00000995853b/w1_slave']
#base_dir = '/sys/bus/w1/devices/'
#for i in range(0,num_temp):
#	device_folder = glob.glob(base_dir + '28*')[i]
#	device_file.append(device_folder + '/w1_slave')

# cleans up gpio outputs
def cleanup():
	GPIO.cleanup()

# reads external pressure sensor
def read_pressure():
	data = bus.read_i2c_block_data(pres_id, 0x00, 4)
	print(data[1],data[2],data[3])
	pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
	pressure = (pres) / 4000
	return pressure

# reads external humidity
def read_humid():
	data0 = bus.read_byte(0x40)
	data1 = bus.read_byte(0x40)
	print(data0)
	print(data1)
	humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
	return humidity

# reads temp from each sensor
def read_temp():
	temp_c = ()
	for i in range(0,num_temp):
		f = open(device_file[i], 'r')
		lines = f.readlines()
		f.close()
		equals_pos = lines[1].find('t=')
		if equals_pos != -1:
			temp_string = lines[1][equals_pos+2:]
			temp_c = temp_c + (float(temp_string)/1000.0,)
	return temp_c

# initializes adc
adc = Adafruit_ADS1x15.ADS1115()

# sets gain
# - 2/3 = +/- 6.144V
# - 1 = +/- 4.096V
# - 2 = +/- 2.048V
# - 4 = +/- 1.024V
# - 8 = +/- 0.512V
# - 16 = +/- 0.256V
GAIN = 1

# reads pressure of pressure system from transducer
def read_pressure_system():
	value1 = adc.read_adc(0, gain=GAIN)
	value2 = adc.read_adc(1, gain=GAIN)
	value3 = adc.read_adc(2, gain=GAIN)
	pressureSol1 = value1*0.00125
	pressureSol2 = value2*0.00125
	pressureMain  = value3*0.00125
	return [pressureSol1, pressureSol2, pressureMain]

# prints value of each sensor
def print_sensors():
	print('Reading...')

	#print ambient pressure data
	pressure = read_pressure()
	print('Pressure: {:.2f} kPa '.format(pressure))

	#print ambient humidity data
	#humidity = read_humid()
	#print('Humidity: {:.2f} %% '.format(humidity))

	#print ambient temperature data
	temperature = read_temp()
	print('Temperature: {:.2f} C  {:.2f} C  {:.2f} C  {:.2f} C {:.2f} C  {:.2f} C  {:.2f} C  {:.2f} C'.format(*temperature))

	#print pressure transducer data
	pressure_system = read_pressure_system()
	print('Pressure Transducer: {:.2f} PSI {:.2f} PSI {:.2f} PSI'.format(*pressure_system))
	return

# returns value of each sensor in downlinking format
def read_sensors():
	#read and downlink ambient pressure data
	#pressure = read_pressure()
	pres_downlink = ['SE','PR','{:.2f}'.format(0)] #pressure)]

	#read and downlink ambient humidity data
	#humidity = read_humid()
	#hum_downlink = ['SE','HU','{:.2f}'.format(humidity)]

	#read and downlink ambient temperature data
	temperature = read_temp()
	temp_downlink = ['SE','TE','{:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f}'.format(*temperature)]

	return [pres_downlink,temp_downlink]

# returns value of each system transducer in downlinking format
def read_transducers():
	#read and downlink pressure transducer data
	pressure_system = read_pressure_system()
	pres_trans_downlink = ['SE', 'PT','{:.2f} {:.2f} {:.2f}'.format(*pressure_system)]
	return pres_trans_downlink
