# attendance


## Requirements
* Based on https://github.com/mxgxw/MFRC522-python/blob/master/Read.py
* Based on http://www.instructables.com/id/Attendance-system-using-Raspberry-Pi-and-NFC-Tag-r/?ALLSTEPS
* Enable SPI ```sudo raspi-config``` (more info: http://www.raspberrypi.org/forums/viewtopic.php?t=97314 )
* ```git clone https://github.com/lthiery/SPI-Py```
* cd to SPI-Py
* ```sudo python setup.py install```
* ```wget https://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.5.11.tar.gz```
* ```tar zxf RPi.GPIO-0.5.11.tar.gz```
* cd to RPi.GPIO-0.5.11
* ```sudo python setup.py install```

## Installation
* See Requirements!
* Git clone attendance directory in Pi's home folder ```sudo python setup.py install```
* Run this once: sudo sh add_cron.sh
* Reboot

## ToDo
* Separate config file for card key + .gitignore
* Figure out how card ID, key and data work. How and what to write to the card.
* Are card IDs unique?
* Buy more cards http://www.dx.com/p/contactless-rewritable-13-56mhz-smart-rfid-ic-cards-white-20-pcs-368849#.VSL6QXV7jUY
* Send data to server http://stackoverflow.com/questions/9733638/post-json-using-python-request
* The server :D
