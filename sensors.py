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
import heater
import lights

# i2c sensor ids
pres_id = 0x60
hum_id = 0x40
bus = smbus.SMBus(1)

# defines number of temp sensors
num_temp = 9

# pressure sensors setup
bus.write_byte_data(pres_id, 0x26, 0x39)

# humidity sensors setup
#bus.write_byte(0x40,0xE5)

# automatically finds temp sensor addresses
device_file = ['/sys/bus/w1/devices/28-000009958138/w1_slave','/sys/bus/w1/devices/28-000009957683/w1_slave','/sys/bus/w1/devices/28-000009958549/w1_slave','/sys/bus/w1/devices/28-0000099577b3/w1_slave','/sys/bus/w1/devices/28-00000995861d/w1_slave','/sys/bus/w1/devices/28-0000099566dc/w1_slave','/sys/bus/w1/devices/28-000009957c5d/w1_slave','/sys/bus/w1/devices/28-00000995853b/w1_slave','/sys/bus/w1/devices/28-000009957f18/w1_slave']
#base_dir = '/sys/bus/w1/devices/'
#for i in range(0,num_temp):
#	device_folder = glob.glob(base_dir + '28*')[i]
#	device_file.append(device_folder + '/w1_slave')

def cleanup():
	GPIO.cleanup()

# reads external pressure sensor
def read_pressure():
	data = bus.read_i2c_block_data(pres_id, 0x00, 4)
	#print(data[1],data[2],data[3])
	pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
	pressure = (pres / 4.0) / 1000.0
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

def heater_control(temp_data):
	# solenoid control
	if temp_data[0] > 30 or temp_data[1] > 30 or temp_data[2] > 30:
		heater.solenoid_heater(False)
	else:
		heater.solenoid_heater(True)
	# regulator control
	if temp_data[3] > 30 or temp_data[4] > 30:
		heater.regulator_heater(False)
	else:
		heater.regulator_heater(True)

def emergency_temperature(temp_data):
	#solenoid 1 temperature ranges
	if temp_data[0] <= -20 and temp_data[0] >= 80:
		temp_emergency_downlink = ['EM','TE','1', '{:.2f}'.format(*temp_data[0])]
		emergencyLED = True

	#solenoid 2 temperature ranges
	elif temp_data[1] <= -20 and temp_data[1] >= 80:
		temp_emergency_downlink = ['EM','TE','2', '{:.2f}'.format(*temp_data[1])]
		emergencyLED = True

	#solenoid 3 temperature ranges
	elif temp_data[2] <= -20 and temp_data[2] >= 80:
		temp_emergency_downlink = ['EM','TE','3', '{:.2f}'.format(*temp_data[2])]
		emergencyLED = True

	#Regulator 1 temperature ranges
	elif temp_data[3] <= 0 and temp_data[3] >= 40:
		temp_emergency_downlink = ['EM','TE','4', '{:.2f}'.format(*temp_data[3])]
		emergencyLED = True

	#Regulator 2 temperature ranges
	elif temp_data[4] <= 0 and temp_data[4] >= 40:
		temp_emergency_downlink = ['EM','TE','5', '{:.2f}'.format(*temp_data[4])]
		emergencyLED = True

	#30 - 5v buck temperature ranges
	elif temp_data[5] <= -40 and temp_data[5] >= 60:
		temp_emergency_downlink = ['EM','TE','6', '{:.2f}'.format(*temp_data[5])]
		emergencyLED = True

	#Habitat temperature ranges
	elif temp_data[6] <= -50 and temp_data[6] >= 100:
		temp_emergency_downlink = ['EM','TE','7', '{:.2f}'.format(*temp_data[6])]
		emergencyLED = True

	#motor temperature ranges
	elif temp_data[8] <= -40 and temp_data[8] >= 60:
		temp_emergency_downlink = ['EM','TE','9 {:.2f}'.format(*temp_data[8])]
		emergencyLED = True

	else:
		temp_emergency_downlink = [0,0,0]
		emergencyLED = False

	GPIO.output(lights.emergency_temperature_led, emergencyLED)

	return temp_emergency_downlink


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
	print('Temperature: {:.2f} C  {:.2f} C  {:.2f} C  {:.2f} C {:.2f} C  {:.2f} C  {:.2f} C  {:.2f} C {:.2f}C'.format(*temperature))

	#print pressure transducer data
	pressure_system = read_pressure_system()
	print('Pressure Transducer: {:.2f} PSI {:.2f} PSI {:.2f} PSI'.format(*pressure_system))
	return

# returns value of each sensor in downlinking format
def read_sensors():
	#read and downlink ambient pressure data
	pressure = read_pressure()
	pres_downlink = ['SE','PR','{:.2f}'.format(pressure)]

	#read and downlink ambient humidity data
	#humidity = read_humid()
	#hum_downlink = ['SE','HU','{:.2f}'.format(humidity)]

	#read and downlink ambient temperature data
	temperature = read_temp()
	temp_downlink = ['SE','TE','{:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f} {:.2f}'.format(*temperature)]

	#heater control
	heater_control(temperature)

	#emergency temperature downlink
	temp_emergency = emergency_temperature(temperature)

	if temp_emergency == [0,0,0]:
		return [pres_downlink, temp_downlink]
	else:
		return [pres_downlink, temp_downlink, temp_emergency]

# returns value of each system transducer in downlinking format
def read_transducers():
	#read and downlink pressure transducer data
	pressure_system = read_pressure_system()
	pres_trans_downlink = ['SE', 'PT','{:.2f} {:.2f} {:.2f}'.format(*pressure_system)]
	return pres_trans_downlink

#print_sensors()
