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
	'0x01 0x01':'0x01 0x01 : Ping Pi',
	'0x01 0x02':'0x01 0x02 : Manual Mode',
	'0x01 0x03':'0x01 0x03 : Automation Mode',
	'0x01 0x04':'0x01 0x04 : Retract Motor',
	'0x01 0x05':'0x01 0x05 : Reboot Pi',
	'0x01 0x06':'0x01 0x06 : Take Video',
	'0x02 0x01':'0x02 0x01 : Start Cycle',
	'0x02 0x02':'0x02 0x02 : Finish Retraction',
	'0x02 0x03':'0x02 0x03 : Finish Inflation',
	'0x03 0x01':'0x03 0x01 : Open Solenoid Valve 1',
	'0x03 0x02':'0x03 0x02 : Close Solenoid Valve 1',
	'0x03 0x03':'0x03 0x03 : Open Solenoid Valve 2',
	'0x03 0x04':'0x03 0x04 : Close Solenoid Valve 2',
	'0x03 0x05':'0x03 0x05 : Open Exhaust Value',
	'0x03 0x06':'0x03 0x06 : Close Exhaust Valve',
	'0x04 0x01':'0x04 0x01 : Disable Valve 1',
	'0x04 0x02':'0x04 0x02 : Enable Valve 1',
	'0x04 0x03':'0x04 0x03 : Disable Valve 2',
	'0x04 0x04':'0x04 0x04 : Enable Valve 2',
	'0x05 0x01':'0x05 0x01 : Turn On Solenoid Heaters',
	'0x05 0x02':'0x05 0x02 : Turn Off Solenoid Heaters',
	'0x05 0x03':'0x05 0x03 : Turn On Payload Heaters',
	'0x05 0x04':'0x05 0x04 : Turn Off Payload Heaters'
}

# prompts user for valid command
print('\nCommands:\r')
for value in commands.values():
	print('\t' + value + '\r')
	
complete = False

while (not complete):
	time.sleep(0.5)
	command_string = input('\nEnter Command: ')

	if not any(command_string in command for command in commands.keys()) and False:
		print('Invalid Command')
	elif (command_string[0:2] != '0x') or (command_string[4:7] != ' 0x') or (len(command_string) != 9):
		print('Invalid Command')
	else: 
		target = hex(int(command_string[0:4],16))
		command = hex(int(command_string[5:9],16))
		ser.write(target.encode())
		ser.write(command.encode())

	while ser.inWaiting():
		cmd = ser.read()
		packet = cmd.decode("utf-8")
		print(packet)
