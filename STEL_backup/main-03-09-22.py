## Main script for Star Tracker Telescope

from stel import coords

while (True):
    cel_object = input('Please Enter the celestial Object you wish to see: ')
    desired_coords = (coords(cel_object))
    if (desired_coords == 0):
        print('\n###Please enter a valid celestial object###\n')
    else:
        print(str(desired_coords) + '\n')
