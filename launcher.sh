#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home
#
# My note: Note sure if all "cd X" are needed. If yes, why?

cd /
cd home/pi/attendance/
sudo python attendance.py
cd /