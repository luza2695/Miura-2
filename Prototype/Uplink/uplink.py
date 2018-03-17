# Sample Uplink Code
import serial

def uplink():
	# sets up serial object for use
	ser = serial.Serial(port='/dev/',
						baudrate=4800,
						parity=serial.PARITY_NONE,
						stopbits=serial.STOPBITS_ONE,
						bytesize=serial.EIGHTBITS,
						writeTimeout=None,
						timeout=0)

	# sets list of valid commands
	commands = ['xAA','xAB','xAC','xAC','xAD']
	commands_usage = ['Ping Pi','Extend Structure','Retract Structure','Infinite Loop']

	# prompts user for valid command
	print('Commands:\n')
	for i in range(commands.len()):
		print(commands[i] + ': ' + commands_usage + '\n')
	print('\n')

	cmd = input('Enter Command: ')

	while not any(cmd in command for command in commands):
		cmd = input('Invalid Command\n\n Enter Command: ')

	ser.write(cmd)
	ser.close