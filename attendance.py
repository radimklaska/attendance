#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import time
import RPi.GPIO as GPIO
import MFRC522
import signal
import urllib2



continue_reading = True

# GPIO setup
GPIO.setmode(GPIO.BOARD)

# Internet connection LED
pin_led_internet = 16
GPIO.setup(pin_led_internet, GPIO.OUT)

# RGB Status LED
pin_rgbled_r = 11
pin_rgbled_g = 13
pin_rgbled_b = 15
GPIO.setup(pin_rgbled_r, GPIO.OUT)
GPIO.setup(pin_rgbled_g, GPIO.OUT)
GPIO.setup(pin_rgbled_b, GPIO.OUT)

# Buzzer for feedback
pin_buzzer = 18
GPIO.setup(pin_buzzer, GPIO.OUT)


def preflight_test():
  # Test Buzzer, Internet LED, RGB LED, End with buzzer again
  pins = [pin_buzzer, pin_led_internet, pin_rgbled_r, pin_rgbled_g, pin_rgbled_b, pin_buzzer]
  for pin in pins:
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(pin,GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(pin,GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(pin,GPIO.LOW)
    time.sleep(0.3)

def signal_read():
  GPIO.output(pin_rgbled_b,GPIO.HIGH)
  GPIO.output(pin_buzzer,GPIO.HIGH)
  time.sleep(0.1)
  GPIO.output(pin_rgbled_b,GPIO.LOW)
  GPIO.output(pin_buzzer,GPIO.LOW)

def signal_ok():
  GPIO.output(pin_rgbled_g,GPIO.HIGH)
  GPIO.output(pin_buzzer,GPIO.HIGH)
  time.sleep(0.1)
  GPIO.output(pin_rgbled_g,GPIO.LOW)
  GPIO.output(pin_buzzer,GPIO.LOW)
  time.sleep(0.1)
  GPIO.output(pin_rgbled_g,GPIO.HIGH)
  GPIO.output(pin_buzzer,GPIO.HIGH)
  time.sleep(0.1)
  GPIO.output(pin_rgbled_g,GPIO.LOW)
  GPIO.output(pin_buzzer,GPIO.LOW)

def signal_fail():
  GPIO.output(pin_rgbled_r,GPIO.HIGH)
  GPIO.output(pin_buzzer,GPIO.HIGH)
  time.sleep(0.7)
  GPIO.output(pin_rgbled_r,GPIO.LOW)
  GPIO.output(pin_buzzer,GPIO.LOW)

def internet_on():
    try:
        response=urllib2.urlopen('http://google.com',timeout=1)
        GPIO.output(pin_led_internet,GPIO.HIGH)
        return
    except urllib2.URLError as err: pass
    GPIO.output(pin_led_internet,GPIO.LOW)
    return

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)



# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

# Run tests
preflight_test()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Indicate Internet connection
    internet_on()

    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])

        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()

            signal_read()
            time.sleep(2)
            signal_ok()
            time.sleep(2)
            signal_fail()

        else:
            print "Authentication error"