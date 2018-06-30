##################################################################
# Miura 2: Receive Downlinked Data (receive_downlink.py)
# Created: 6/4/2018
# Modified: 6/4/2018
# Purpose: Receive and print downlinked data
##################################################################
import serial
import time
import glob
from sys import platform

if platform == 'linux' or platform == 'linux2':
    current_port = '/dev/ttyUSB0'
elif platform == 'darwin':
    current_port = glob.glob('/dev/tty.USA*')[0]

# sets up serial object for use
serial = serial.Serial(port=current_port,
                    baudrate=4800,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1)

print("Serial object initialized...")
print("Waiting for downlink...")

while True:
	while serial.inWaiting():
		response = serial.readline()
		packet = response.decode()
		print(packet)
	time.sleep(1)
