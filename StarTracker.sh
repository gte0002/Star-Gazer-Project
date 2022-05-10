#!/bin/bash
sleep 1

#Check if terminal is open for interface
term_check=$(xdotool getactivewindow getwindowname)
if [ "${term_check}" != "pi@raspberrypi: ~" ] && [ "${term_check}" !=  "StarTracker.sh" ]; then
	xdotool key ctrl+alt+t
#	xdotool search --onlyvisible --name "pi@raspberrypi: ~" activatewindow
fi

#Shell executible for Star Tracker system.
xdotool getactivewindow set_window --name "Star Tracker"
cd
fc-cache
xrdb -merge ~/.Xdefaults
python terminal.py --wait sudo stellarium&

sleep 2
xdotool search --onlyvisible --name "stellarium" set_window --name stel_datab1
sleep 3
xdotool search --onlyvisible --name "stel_datab1" windowunmap

#Loop to look for Stellarium open, then immediately set background
count=0
while :
do
	window=$(xdotool getactivewindow getwindowname)
#	echo "${window}"
	if [ "${window}" == "Stellarium 0.18.3" ]; then
		xdotool getactivewindow set_window --name stel_datab2
		xdotool search --onlyvisible --name "stel_datab2" windowunmap
		sleep 0.1
		break
	else
		###Loading screen
		x=$((count % 3))
		clear
		if [ "${x}" == 0 ]; then
			echo 'Loading .'
		elif [ "${x}" == 1 ]; then
			echo 'Loading ..'
		elif [ "${x}" == 2 ]; then
			echo 'Loading ...'
		else
			echo 'Loading'
		fi
	count=$((count + 1))
	sleep 0.7
	fi
done
clear

sleep 0.1
xdotool key alt+F11
sudo python3 main.py #Call Main Python Script

xdotool search --name "stel_datab2" windowkill
xdotool search --name "stel_datab1" windowkill

clear
xdotool search --name "Star Tracker" windowkill
