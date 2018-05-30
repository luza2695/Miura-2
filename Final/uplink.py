##################################################################
# Miura 2: Uplink Code (uplink.py)
# Created: 3/13/2018
# Modified: 5/29/2018
# Purpose: Accept uplink commands
##################################################################

#import RPi.GPIO as GPIO
import time
import serial
import sys
sys.path.append('../')
#from Camera import cameratest
import examples.StepperTest as StepperTest
import solenoid

#led_pin = 33
#GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)
#GPIO.setup(led_pin,GPIO.OUT)
#GPIO.output(led_pin,GPIO.LOW)
#GPIO.cleanup()

# sets current pi usb port
current_port = "/dev/ttyUSB0"

# Create serial object
serial = serial.Serial(port=current_port,
            baudrate=4800,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)

#LED ping when called
#def led():
#    GPIO.output(led_pin,GPIO.HIGH)
#    time.sleep(0.5)
#    GPIO.output(led_pin,GPIO.LOW)
#    GPIO.cleanup()

def uplink(serial):
    serial.flushInput() # Clears the serial communication channel before attempting to use it
    while True:
        if serial.inWaiting(): # Reads uplink command
            cmd = serial.read()  # gets command
            packet = hex(int.from_bytes((cmd), byteorder='big')) # Convert from hex into bytes
            print(packet)
            if cmd == b"\x01": # ping pi
                cmdTime = time.asctime(time.localtime(time.time()))
                serial.write(bytes(5))
                print("Command Recieved :", cmdTime)
                pass
            elif cmd == b"\x02": # demo motor
                print("Begin Motor Command")
                StepperTest.main()
            elif cmd == b"\x03": # open pressurization valve
                print("Opening Pressurize Valve")
                solenoid.openPressurize()
            elif cmd == b"\x04": # close pressurization valve
                print("Closing Pressurize Valve")
                solenoid.closePressurize()
            elif cmd == b"\x05": # open exhaust valve
                print("Opening Exhaust Valve")
                solenoid.openExhaust()
            elif cmd == b"\x06": # close exhaust valve
                print("Closing Exhaust Valve")
                solenoid.closeExhaust()
            elif cmd == b"\x07": # burp exhaust valve
                print("Burping Exhaust Valve")
                solenoid.burp()
            elif cmd == b"\x0C": # take picture
                print("Begin Camera Command")
                #cameratest.main()
                cmd = bytes('Nice picture!', 'utf-8')
                testDownlink.downlink(cmd)
            else:
                print("invalid command")
        time.sleep(1)

# intializes loop to detect uplink
while True:
    uplink(serial)