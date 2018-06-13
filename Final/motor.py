from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

import time
import atexit
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
motor_pin = 18
GPIO.setup(motor_pin, GPIO.OUT)
GPIO.output(motor_pin, True)

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

myStepper = mh.getStepper(50, 1)  # 50 steps/rev, motor port #1
myStepper.setSpeed(50)             # 30 RPM

while (True):
    print("Single coil steps")
    myStepper.step(100, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.SINGLE)
    myStepper.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)

    print("Double coil steps")
    myStepper.step(100, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.DOUBLE)
    myStepper.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE)

    print("Interleaved coil steps")
    myStepper.step(100, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.INTERLEAVE)
    myStepper.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)

    print("Microsteps")
    myStepper.step(100, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.MICROSTEP)
    myStepper.step(100, Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
