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

# defines lis of commands
commands = {
	'0x01 0x01':'Ping Pi',
	'0x01 0x02':'Manual Mode',
	'0x01 0x03':'Continue Automation Mode',
	'0x01 0x04':'Restart Automation Mode',
	'0x01 0x05':'Retract Motor',
	'0x01 0x06':'Take Picture',
	'0x01 0x07':'Reboot Pi',
	'0x02 0x01':'Open Solenoid Valve 1',
	'0x02 0x02':'Close Solenoid Valve 1',
	'0x02 0x03':'Open Solenoid Valve 2',
	'0x02 0x04':'Close Solenoid Valve 2',
	'0x02 0x05':'Open Exhaust Value',
	'0x02 0x06':'Close Exhaust Valve',
	'0x03 0x01':'Disable Valve 1',
	'0x03 0x02':'Enable Valve 1',
	'0x03 0x03':'Disable Valve 2',
	'0x03 0x04':'Enable Valve 2',
	'0x04 0x01':'Turn On Solenoid Heaters',
	'0x04 0x02':'Turn Off Solenoid Heaters',
	'0x04 0x03':'Turn On Payload Heaters',
	'0x04 0x04':'Turn Off Payload Heaters'
}

# prompts user for valid command
print('\nCommands:')
for key, value in zip(commands.keys(),commands.values()):
	if key.endswith('0x01'):
		print('\n')
	print('\t' + key + ": " + value + '\r')

complete = False

while (not complete):
	time.sleep(0.5)
	command_string = input('\nEnter Command: ')

	if not any(command_string in command for command in commands.keys()):
		print('Invalid Command')
	elif (command_string[0:2] != '0x') or (command_string[4:7] != ' 0x') or (len(command_string) != 9):
		print('Invalid Command')
	else:
		target = bytes([int(command_string[0:4],16)])
		command = bytes([int(command_string[5:9],16)])
		serial.write(target)
		serial.write(command)

	time.sleep(1)
