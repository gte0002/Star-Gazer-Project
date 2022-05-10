# Gabriel Emerson
# Updated 03/09/22

# This is a script that calls GET to Stellarium Remote Server
# to obtain the Azimuth and Altitude of the current middle of
# the screen.

import json
import requests

def coords(celestial_object):
    #Format string to get correct object
    data_url_test = 'http://localhost:8090/api/objects/find?str=' + celestial_object
    data_url = 'http://localhost:8090/api/objects/info?name=' + celestial_object + '&format=json'

    ##Get data to test if that object exists
    data = requests.get(data_url_test)
    data = data.text

    #Check if user input is valid
    #If data is empty, there was no object with that name
    if (data == '[]'):
        return 0
    
    ##If data is not empty, get data and create az and alt floats
    data = requests.get(data_url)
    data = data.text
    data = data.encode('UTF-8')
    data = json.loads(data)
    az = data['azimuth']
    alt = data['altitude']

    return az,alt
