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
# commands = ['x01','x02','x03','x04','x05','x06','x07','x0C']
# commands_usage = ['Ping Pi','Demo Motor','Open Pressurize','Close Pressurize','Open Exhaust','Close Exhaust','Burp Exhaust','Camera Demo']

commands = {
	'\\x01 \\x01':'Ping Pi',
	'\\x01 \\x02':'Manual Mode',
	'\\x01 \\x03':'Automation Mode',
	'\\x01 \\x04':'Retract Motor',
	'\\x01 \\x05':'Reboot Pi',
	'\\x01 \\x06':'Take Video',
	'\\x02 \\x01':'Start Cycle',
	'\\x02 \\x02':'Finish Retraction',
	'\\x02 \\x03':'Finish Inflation',
	'\\x03 \\x01':'Open Solenoid Valve 1',
	'\\x03 \\x02':'Close Solenoid Valve 1',
	'\\x03 \\x03':'Open Solenoid Valve 2',
	'\\x03 \\x04':'Close Solenoid Valve 2',
	'\\x03 \\x05':'Open Exhaust Value',
	'\\x03 \\x06':'Close Exhaust Valve',
	'\\x04 \\x01':'Disable Valve 1',
	'\\x04 \\x02':'Enable Valve 1',
	'\\x04 \\x03':'Disable Valve 2',
	'\\x04 \\x04':'Enable Valve 2',
	'\\x05 \\x01':'Turn On Solenoid Heaters',
	'\\x05 \\x02':'Turn Off Solenoid Heaters',
	'\\x05 \\x03':'Turn On Payload Heaters',
	'\\x05 \\x04':'Turn Off Payload Heaters'
}

# prompts user for valid command
print('\nCommands:\r')
for key, value in zip(commands.keys(), commands.values()):
	print('\t' + key + ': ' + value + '\r')
	
complete = False

while (not complete):
	time.sleep(0.5)
	cmd = input('\nEnter Command: ')

	if not any(cmd in command for command in commands.keys()) and False:
		print('Invalid Command')
	else: 
		ser.write(cmd.encode())

	while ser.inWaiting():
		cmd = ser.read()
		packet = cmd.decode("utf-8")
		print(packet)
