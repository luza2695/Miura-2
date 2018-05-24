# imports
import serial
import time
import testDownlink

# sets current pi usb port
#current_port = "/dev/ttyUSB0"

# Create serial object
#ground = serial.Serial(port=current_port,
#                       baudrate=4800,
#                       parity=serial.PARITY_NONE,
#                       stopbits=serial.STOPBITS_ONE,
#                       bytesize=serial.EIGHTBITS,
#                       timeout=1)
#
# downlinks given pakcet
#def downlink(packet):
#    ground.write(packet)



def main():
	for i in range(0,4):
		testDownlink.downlink(bytes(str(i),'utf-8'))
	#time.sleep(1)
	#downlink(bytes('b','utf-8'))
	#time.sleep(1)
	#downlink(bytes('b','utf-8'))
	#time.sleep(1)
