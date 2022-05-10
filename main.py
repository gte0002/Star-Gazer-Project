### Gabriel Emerson
### Updated 03-27-22

## Main script for Star Tracker Telescope

import os
import requests
import json
from stel import coords, getAlt, getAz
from mpu6050 import *
from bn880 import *
import time
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

#Setup Motors
try:
    kit = MotorKit()
except:
    print("\nMotor(s) are not connected. Please connect and try again.\n")
    input("Press Enter to continue...")
    quit()

#Setup Gyro/Accel (MPU6050)
try:
    current_measure = AngleMeterAlpha()
    current_measure.measure()
except:
    print("\nGyro/Accel (MPU6050) is not connected. Please connect and try again.\n")
    input("Press Enter to continue...")
    quit()

#Setup GPS/Magnetometer (BN880)
try:
    ser = serial.Serial("/dev/ttyS0")
    gpgga_info = "$GPGGA"
    updateGPS()
    print(getTime())
    #SET LAT AND LONG IN STEL??
except:
    y_n = input("No GPS/Magnetometer found. Would you like to manually enter Location, Date, and Time? [Y/n]")
    if (y_n == 'Y' or y_n == 'y' or y_n == 'yes'):
        latitude = input("Latitude: ")
        longitude = input("Longitude: ")
        date = input("Date[yyyy-mm-dd]: ")
        set_time = input("Time[hh:mm:ss]: ")
        date_time = str(date + ' ' + set_time)
        set_time_date = 'sudo date --set \"' + date_time + '\" '
        os.system(set_time_date)
        set_location_url = 'http://localhost:8090/api/location/setlocationfields?latitude=' + str(latitude) + '&longitude=' + str(longitude)
        requests.post(set_location_url)
        #wait = input('wait')
    else:
        pass
    

#PERFORM ACTION WITH LOCATION/DATE/TIME

#az_count is used to find current degree.
#Az Degree = az_count * 0.0375
#az_count = Degree * 16(MICROSTEP) * 3(GEARDOWN)
az_count = 0
alt_count = 0

os.system('clear')
print('Calibrating Altitude')
while (True):
    while (current_measure.get_kalman_pitch() == 0):
        #print(current_measure.get_kalman_pitch())
        pass
    set_alt = float("{:.1f}".format(current_measure.get_kalman_pitch()))
    set_alt = set_alt - 1.9 ## For calibrating
    if (set_alt == 0.0):
        kit.stepper1.release()
        break
    if (set_alt > 0.0):    
        kit.stepper1.onestep(style=stepper.MICROSTEP,direction=stepper.FORWARD)
        time.sleep(0.01)
        #print(set_alt)

###Calibrating Azimuth is impossible without working magnetometer
#os.system('clear')
#print('Calibrate Azimuth')
#while (True):
#    polaris = (coords('polaris'))
#    print(polaris)


os.system('clear')
while (True):
    cel_object = input('Please Enter the celestial Object you wish to see \nor \'exit\' to end program: ')
    if (cel_object == "exit"): 
        break
    
    desired_coords = (coords(cel_object))
    
    if (desired_coords == 0):
        print('\n###Please enter a valid celestial object###\n')
    else:
        #print('\n' + str(desired_coords) + '\n')
        desired_alt = getAlt()
        desired_az = getAz()
        if (desired_alt < 0):
            print('Object is not visible at this current time. ' + cel_object + ' is below horizon.')
            continue


        ##Get values of where we are currently looking
        #current_alt = current_measure.get_kalman_pitch()
        current_alt = alt_count * 0.0375
        current_az = az_count * 0.0375
        

        #Format values to 1 decimal places
        desired_alt = float("{:.1f}".format(desired_alt))
        desired_az = float("{:.1f}".format(desired_az))
        current_alt = float("{:.1f}".format(current_alt))
        current_az = float("{:.1f}".format(current_az))

        while (desired_alt != current_alt or desired_az != current_az):
            if (desired_alt - current_alt > 0):
                kit.stepper1.onestep(style=stepper.MICROSTEP,direction=stepper.BACKWARD)
                alt_count = alt_count + 1
            if (desired_alt - current_alt < 0):
                kit.stepper1.onestep(style=stepper.MICROSTEP,direction=stepper.FORWARD)
                alt_count = alt_count - 1
            
            #AZIMUTH SUX
            if (abs(desired_az - current_az) <= 180):
                if (desired_az - current_az > 0):
                    kit.stepper2.onestep(style=stepper.MICROSTEP,direction=stepper.FORWARD)
                    if (az_count == 9599):
                        az_count = 0
                    else:
                        az_count = az_count + 1
                else:
                    kit.stepper2.onestep(style=stepper.MICROSTEP,direction=stepper.BACKWARD)
                    if (az_count == 0):
                        az_count = 9599
                    else:
                        az_count = az_count - 1
            else:
                if (desired_az < 180):
                    kit.stepper2.onestep(style=stepper.MICROSTEP,direction=stepper.FORWARD)
                    if (az_count == 9599):
                        az_count = 0
                    else:
                        az_count = az_count + 1
                else:
                    kit.stepper2.onestep(style=stepper.MICROSTEP,direction=stepper.BACKWARD)
                    if (az_count == 0):
                        az_count = 9599
                    else:
                        az_count = az_count - 1
                    

            #Update values for Step Loop
            #current_alt = float("{:.1f}".format(current_measure.get_kalman_pitch()))
            alt_count = alt_count % 2400
            current_alt = float("{:.1f}".format(alt_count * 0.0375))
            az_count = az_count % 9600
            current_az = float("{:.1f}".format(az_count * 0.0375))
            
            time.sleep(0.01) #Small delay for motors

            #print('desired_alt = ' + str(desired_alt))
            #print('desired_az = ' + str(desired_az))
            #print('current_alt = ' + str(current_alt))
            #print('current_az = ' + str(current_az))

        kit.stepper1.release()
        kit.stepper2.release()

os._exit(os.EX_OK) 
