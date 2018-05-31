##################################################################
# Miura 2: Send Uplink (send_uplink.py)
# Created: 3/13/2018
# Modified: 5/29/2018
# Purpose: Send Uplink Commands to Pi
##################################################################

import serial
import time
import glob
from sys import platform

if platform == "linux" or platform == "linux2":
    current_port = "/dev/ttyUSB0"
elif platform == "darwin":
    current_port = glob.glob("/dev/tty.USA*")[0]

# sets up serial object for use
ser = serial.Serial(port=current_port,
                    baudrate=4800,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1)

# sets list of valid commands
commands = ['x01','x02','x03','x04','x05','x06','x07','x0C']
commands_usage = ['Ping Pi','Demo Motor','Open Pressurize','Close Pressurize','Open Exhaust','Close Exhaust','Burp Exhaust','Camera Demo']

# prompts user for valid command
print('\nCommands:\r')
for i in range(len(commands)):
	print('\t' + commands[i] + ': ' + commands_usage[i] + '\r')
	
complete = False

while (not complete):
	time.sleep(0.5)
	cmd_str = input('\nEnter Command: ')

	if not any(cmd_str in command for command in commands) and False:
		print('Invalid Command')
	else: 
		cmd = int(cmd_str,16)
		cmd = bytes([cmd])#, 'utf-8')
		ser.write(cmd)

	while ser.inWaiting():
		cmd = ser.read()
		packet = cmd.decode("utf-8")
		print(packet)
