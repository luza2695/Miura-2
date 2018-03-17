# Sample Uplink Code
import serial

#def uplink():
# sets up serial object for use
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

print('Commands:\n')
# for i in range(len(commands)):
# 	print(commands[i] + ': ' + commands_usage + '\n')
# print('\n')
while True:
	cmd =bytes(input('Enter Command: '), 'utf-8')
	ser.write(cmd)

# while not any(cmd in command for command in commands):
# 	cmd = input('Invalid Command\n\n Enter Command: ')

ser.write(cmd)
ser.close
