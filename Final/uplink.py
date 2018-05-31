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
import queue

#led_pin = 33
#GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)
#GPIO.setup(led_pin,GPIO.OUT)
#GPIO.output(led_pin,GPIO.LOW)
#GPIO.cleanup()

# sets current pi usb port
current_port = '/dev/ttyUSB0'

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

def main(serial, downlink_queue):
    if serial.inWaiting(): # reads uplink command
        #heading = serial.read() # start of heading
        #start = serial.read() # start of text
        target = serial.read()
        command = serial.read()
        #end = serial.read() # end of text
        #cr_ = serial.read() # carriage return
        #lf_ = serial.read() # line feed
        downlink_queue.put(['UP','RE',target+command])
        if target == b'\x01':
            if command == b'\x01': # ping pi
                commandTime = time.strftime('%b %m %G %H:%M:%S')
                print('Command Recieved: {}'.format(commandTime))
                pass
            elif command == b'\x02': # manual mode
                pass
            elif command == b'\x03': # automation mode
                pass
            elif command == b'\x04': # retract motor
                StepperTest.main()
            elif command == b'\x05': # take picture
                #cameratest.main()
                pass
            elif command == b'\x06': # reboot pi
                pass
            else:
                print('invalid command')
        elif target == b'\x02': # cycle control
            if command == b'\x01': # start cycle
                pass
            elif command == b'\x02': # finish retraction
                pass
            elif command == b'\x03': # finish inflation
                pass
            else:
                print('invalid command')
        elif target == b'\x03': # manual pressure system control
            if command == b'\x01': # open pressurization valve
                print('Opening Pressurize Valve')
                solenoid.openPressurize()
            elif command == b'\x02': # close pressurization valve
                print('Closing Pressurize Valve')
                solenoid.closePressurize()
            elif command == b'\x05': # open exhaust valve
                print('Opening Exhaust Valve')
                solenoid.openExhaust()
            elif command == b'\x06': # close exhaust valve
                print('Closing Exhaust Valve')
                solenoid.closeExhaust()
            else:
                print('invalid command')
        elif target == b'\x04': # pressure system enabling control
            if command == b'\x01': # disable system 1
                pass
            elif command == b'\x02': # enable system 1
                pass
            elif command == b'\x03': # disable system 2
                pass
            elif command == b'\x04': # enable system 2
                pass
            else:
                print('invalid command')
        elif target == b'\x05': # heater system control
            if command == b'\x01': # turn on solenoid heaters
                heater.solenoid_heater(True)
            elif command == b'\x02': # turn off solenoid heaters
                heater.solenoid_heater(False)
            elif command == b'\x03': # turn on payload heaters
                heater.payload_heater(True)
            elif command == b'\x04': # turn off payload heaters
                heater.payload_heater(False)
            else:
                print('invalid command')
        else:
            print('invalid target')
    return

while True:
    main(serial,queue.Queue())

