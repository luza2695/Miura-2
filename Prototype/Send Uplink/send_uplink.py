# Sample Uplink Code
import serial

sets up serial object for use
ser = serial.Serial(port='/dev/tty.KeySerial1',
                    baudrate=115200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    writeTimeout=None,
                    timeout=0)

# sets list of valid commands
commands = ['xAA','xAB','xAC','xAC','xAD']
commands_usage = ['Ping Pi','Extend Structure','Retract Structure','Infinite Loop']

# prompts user for valid command

print('\nCommands:\r')
for i in range(len(commands)-1):
	print('\t' + commands[i] + ': ' + commands_usage[i] + '\r')

while True:
	cmd_str = input('\nEnter Command: ')
	if not any(cmd_str in command for command in commands):
		print('Invalid Command')
	else: 
		cmd = bytes(cmd_str, 'utf-8')
		ser.write(cmd)