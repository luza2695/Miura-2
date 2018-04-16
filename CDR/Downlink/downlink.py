import time
from zlib import adler32
import RPi.GPIO as GPIO

#led_pin = 29
#GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)
#GPIO.setup(led_pin,GPIO.OUT)
#GPIO.output(led_pin,False)

def main(downlink,ground):
    led_on = False
    led_timer = 0
    while True:
#        if not led_on and time.time() > led_timer + 1:
#            GPIO.output(led_pin,True)
#            led_timer = time.time()
#            led_on = True
#        if led_on and time.time() > led_timer + 1:
#            GPIO.output(led_pin,False)
#            led_on = False
#            led_timer = time.time()
        # All downlinked data must be in this form:
        # [2 char sender, 2 char record type, string of data]
        # Multi-item data needs to be in the form of ###, ###, ###
        packet = downlink.get() # Pop the first item of the queue: a list of that contains the labels for the packet
        sender, record, data = packet[0], packet[1], str(packet[2]) # Package the elements of the popped list into three separate variables
        l = len(data) # Calculate the length of the data
        #        print("pre-packet: ", packet)
        if type(data) is not bytes: # Necessary for sending strings
            a_data = data.encode('utf-8')
        else:
            a_data = data # Useful for sending raw data
        ck = adler32(a_data) & 0xffffffff # Use data to calculate checksum
        t = time.time()  # Unix time. Seconds since epoch.
        packet = "\x01CU MI %s %s %.2f %i %i\x02" % (sender, record, t, l, ck) + " " + data + "\x03\n" # Follows HASP guidelines
        packet = "Nice picture!" # camera demo message

#        with open("/home/pi/downlink.log", 'a') as log: # Keeps a central record of everything that was downlinked
#            log.write(packet)
        ground.write(packet) # Downlink packet through serial
#        logdata(packet, sender) # Log data received
