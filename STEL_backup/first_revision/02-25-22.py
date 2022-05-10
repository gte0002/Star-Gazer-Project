# Gabriel Emerson
# Updated 2/25/22

# This is a script that calls GET to Stellarium Remote Server
# to obtain the Azimuth and Altitude of the current middle of
# the screen.

import json
import requests
import math

while(True):
    ##Get data and convert it to type list
    data = requests.get('http://localhost:8090/api/main/view?coord=altAz')
    data = data.text
    data = data.encode('UTF-8')
    data = json.loads(data)
    data = data.values()
    data = str(data)
    data = data.split(",", 3)
    
    ##Use list of data and make 3 seperate variables for Azimuth X, Y and Altitude
    AzX = data[0]
    AzX = AzX.replace("[u'[", "")
    AzY = data[1]
    AzY = AzY.replace(" ", "")
    Alt = data[2]
    Alt = Alt.replace(" ", "")
    Alt = Alt.replace("]']", "")
    
    ##Convert all variables to be a float
    AzX = float(AzX)
    AzY = float(AzY)
    Alt = float(Alt)

    ##Load used numbers back into data list
    data[0] = AzX
    data[1] = AzY
    data[2] = Alt
    
    ##Convert AzX and AzY to degrees
    ## Standard coordinates: South = 0, East = 90, North = 180, West = 270 | CCW
    
    ## TO SET NORTH = 0, AND REVERSE COORDINATES TO COUNT CW, SET north_as_zero_flag to 1
    ## Modified Coordinates: North = 0, West = 90, South = 180, East = 270 | CW
    
    north_as_zero_flag = 1 #Flag used to set North/South as 0, and coordinate direction
    
    r = math.sqrt(AzX ** 2 + AzY ** 2)
    Az_degrees = math.degrees(math.acos(AzX / r))
    if AzY < 0:
        Az_degrees = 180 + (180 - Az_degrees)
    
    ##Function if north_as_zero_flag is enabled
    ##THIS FUNCTION ALSO FLIPS COORDINATE DIRECTION
    if north_as_zero_flag == 1:
        AzX = -AzX
        AzY = -AzY
        Az_degrees = (abs(Az_degrees - 360)) % 180
        if AzY > 0:
            Az_degrees = 180 + Az_degrees

    ##Convert Alt to degrees
    Alt_degrees = math.degrees(math.asin(Alt))



    ### These prints are used for DEBUG ONLY ####
    #print(data)                                #
    #print(type(data))                          #
    #print(AzX)                                 #
    #print(type(AzX))                           #
    #print(AzY)                                 #
    #print(type(AzY))                           #
    print(Az_degrees)                          # 
    #print(type(Az_degrees))                    #
    #print(r)                                   #
    #print(Alt)                                 #
    #print(type(Alt))                           #
    print(Alt_degrees)                         #
    #############################################

    exit() ###COMMENT TO RUN INFINITE ITERATION OF PROGRAM
