from bn880 import *
from mpu6050 import *
#from kalman import *
from mpu6050 import AngleMeterAlpha
import time

x = AngleMeterAlpha()
x.measure()

ser = serial.Serial("/dev/ttyS0")
gpgga_info = "$GPGGA"

updateGPS()
print(getTime())

#while (True):
    #print(x.get_complementary_pitch())
    #print(x.get_kalman_roll())
