import time
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
kit = MotorKit()


for i in range(9600): ##16 microstep, gear down 3, Full circle = 9600
    #If alt correct skip
    #kit.stepper1.onestep(style=stepper.MICROSTEP,direction=stepper.FORWARD)
    #IF azi correct skip
    kit.stepper2.onestep(style=stepper.MICROSTEP,direction=stepper.FORWARD)
    time.sleep(0.01)
