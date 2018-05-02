# Sample Uplink Code
import serial
import time
from sys import platform


if platform == "linux" or platform == "linux2":
    current_port = "/dev/ttyUSB0"
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
commands = ['x01','x02','x0C']
commands_usage = ['Ping Pi','Demo Motor','Camera Demo']

# prompts user for valid command

# print('\nCommands:\r')
# for i in range(len(commands)):
# 	print('\t' + commands[i] + ': ' + commands_usage[i] + '\r')



# cmd_str = input('\nEnter Command: ')
# if not any(cmd_str in command for command in commands) and False:
# 	print('Invalid Command')
# else: 
# 	cmd = int(cmd_str,16)

# 	cmd = bytes([cmd])#, 'utf-8')
		
# 	ser.write(cmd)
	
complete = False

while (not complete):
	time.sleep(0.5)
	#print (ser.inWaiting())

	# cmd_str = input('\nEnter Command: ')
	# if not any(cmd_str in command for command in commands) and False:
	# 	print('Invalid Command')
	# else: 
	# 	cmd = int(cmd_str,16)

	# 	cmd = bytes([cmd])#, 'utf-8')
		
	# 	ser.write(cmd)
	while ser.inWaiting():
		
		#print("",end='')
		cmd = ser.read()
            #packet = hex(int.from_bytes((cmd),byteorder = 'big'))
		packet = cmd.decode("utf-8")
		print(packet)
		#complete = True
