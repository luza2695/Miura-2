import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'

num_temp = 2
device_file = []

for i in range(0,num_temp):
    device_folder = glob.glob(base_dir + '28*')[i]
    device_file.append(device_folder + '/w1_slave')

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
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            current = float(temp_string) / 1000.0
            temp_c.append(current)
    return temp_c
	
while True:
    temp = read_temp()
    print(("Temperature: %.2f C, %.2f C") % (temp[0],temp[1]))
    time.sleep(1)
