import os
import glob
import time
import smbus

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

num_temp = 5
device_file = []

for i in range(0,num_temp):
    device_folder = glob.glob(base_dir + '28*')[i]
    device_file.append(device_folder + '/w1_slave')

bus = smbus.SMBus(1)

def read_pressure():
	data = []
	pressure = []
    # MPL3115A2 address, 0x60(96)
    # Select control register, 0x26(38)
    #		0x39(57)	Active mode, OSR = 128, Barometer mode
    bus.write_byte_data(0x60, 0x26, 0x39)
    # MPL3115A2 address, 0x60(96)
	# Read data back from 0x00(00), 4 bytes
	# status, pres MSB1, pres MSB, pres LSB
    data[0] = bus.read_i2c_block_data(0x60, 0x00, 4)

    bus.write_byte_data(0x68, 0x26, 0x39)

    data[1] = bus.read_i2c_block_data(0x68, 0x00, 4)

    # Convert the data to 20-bits
    for i in range(0,2):
    	pres[i] = ((data[i][1] * 65536) + (data[i][2] * 256) + (data[i][3] & 0xF0)) / 16
    	pressure[i] = (pres[i] / 4.0) / 1000.0
    return pressure

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
    
def read_sensors():
	print("Reading...")
	pressure = read_pressure()
	print("Pressure: ", end="")
	for i in range(0,num_temp):
			print(("Pressure: %.2f kPa ") % (pressure[i]), end="")
	temperature = read_temp()
	print("Temperature: ", end="")
	for i in range(0,num_temp):
			print(("%.2f C ") % (temperature[i]), end="")
	print("")
        
while True:
	read_sensors()
	time.sleep(0.5)