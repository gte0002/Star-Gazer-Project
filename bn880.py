import serial
from time import sleep
import sys

# converts NMEA values into readable degree format
# NMEA is in the form (d)dddmm_mmmm - degrees and min
def toDegree(rawFloat):
    decVal = rawFloat/100.00
    degreeVal = int(decVal)
    mm_mmmm = (decVal - degreeVal)/0.6
    conPos = degreeVal + mm_mmmm
    conPos = "%.4f" %(conPos)
    return conPos

# takes GPS data and parses it into system variables and arrays
def infoGPS():
    global latDeg
    global longDeg
    global NMEA_buff
    global timeNMEA

    timeNMEA = NMEA_buff[0]     # parse time from NMEA string into global variables
    latNMEA = NMEA_buff[1]      # parse latitude from NMEA string into global variables
    longNMEA = NMEA_buff[3]     # parse longitude from NMEA string into global variables

    # need lat and long in type float in order to do calculation, so that is converted here
    latFloat = float(latNMEA)
    longFloat = float(longNMEA)

    # finaly, convert lat and long into decimal form rather than NMEA format
    # https://www.nmea.org/content/STANDARDS/NMEA_2000
    latDeg = toDegree(latFloat)
    longDeg = toDegree(longFloat)

# reads data from GPS serial port and sends it to buffer to be read
def updateGPS():
    received = (str)(ser.readline())
    availGPGGA = received.find(gpgga_info)
    if (availGPGGA > 0):
        GPGGA_buffer = received.split("GPGGA,",1)[1]
        NMEA_buff = (GPGGA_buffer.split(','))
        infoGPS()

        
def getLat():
    return latDeg

def getLong():
    return longDeg

def getTime():
    #return timeNMEA
    return NMEA_buff[0]

ser = serial.Serial("/dev/ttyS0")
gpgga_info = "$GPGGA"
GPGGA_buffer = 0
NMEA_buff= 0







