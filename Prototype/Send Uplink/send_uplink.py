# Sample Uplink Code
import serial
from sys import platform

if platform == "linux" or platform == "linux2":
    current_port = "/dev/ttyAMAO"
elif platform == "darwin":
    current_port = "/dev/tty.KeySerial1"

# sets up serial object for use
ser = serial.Serial(port=current_port,
                    baudrate=4800,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1)

# sets list of valid commands
commands = ['x01','x02']
commands_usage = ['Ping Pi','Demo Motor']

# prompts user for valid command

print('\nCommands:\r')
for i in range(len(commands)):
	print('\t' + commands[i] + ': ' + commands_usage[i] + '\r')

while True:
	cmd_str = input('\nEnter Command: ')
	if not any(cmd_str in command for command in commands) and False:
		print('Invalid Command')
	else: 
		cmd = bytes(cmd_str, 'utf-8')
		ser.write(cmd)
