#!/usr/bin/env python3

import os
import time
uname = os.uname()
if 'arm' in uname.machine:
    import RPi.GPIO as GPIO
else:
    import FakeRPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)  # Use chip numbering scheme

# Pin Aliases
pinCE = 2
pinOE = 3
pinWE = 4

pinA0 = 10
pinA1 = 9
pinA2 = 11
pinA3 = 25
pinA4 = 8
pinA5 = 7
pinA6 = 5
pinA7 = 6
pinA8 = 12
pinA9 = 13
pinA10 = 19

pinD0 = 14
pinD1 = 15
pinD2 = 18
pinD3 = 17
pinD4 = 27
pinD5 = 22
pinD6 = 23
pinD7 = 24

# CE, WE, OE pins (pull down to activate each mode):
GPIO.setup(pinCE, GPIO.OUT)  # CE
GPIO.setup(pinOE, GPIO.OUT)  # OE
GPIO.setup(pinWE, GPIO.OUT)  # WE

# Set the chip in standby mode:
GPIO.output(pinCE, GPIO.HIGH)  # CE - high
GPIO.output(pinOE, GPIO.HIGH)  # OE - high
GPIO.output(pinWE, GPIO.HIGH)  # WE - high

# Address pins set for output (A15, A16, A17 connected to ground):

GPIO.setup(pinA0, GPIO.OUT)  # A0
GPIO.setup(pinA1, GPIO.OUT)  # A1
GPIO.setup(pinA2, GPIO.OUT)  # A2
GPIO.setup(pinA3, GPIO.OUT)  # A3
GPIO.setup(pinA4, GPIO.OUT)  # A4
GPIO.setup(pinA5, GPIO.OUT)  # A5
GPIO.setup(pinA6, GPIO.OUT)  # A6
GPIO.setup(pinA7, GPIO.OUT)  # A7
GPIO.setup(pinA8, GPIO.OUT)  # A8
GPIO.setup(pinA9, GPIO.OUT)  # A9
GPIO.setup(pinA10, GPIO.OUT)  # A10
# GPIO.setup (26, GPIO.OUT) #A11
# GPIO.setup (16, GPIO.OUT) #A12
# GPIO.setup (20, GPIO.OUT) #A13
# GPIO.setup (21, GPIO.OUT) #A14

# Data pins set for input (pull down for zeroes):
GPIO.setup(pinD0, GPIO.IN)  # D0
GPIO.setup(pinD1, GPIO.IN)  # D1
GPIO.setup(pinD2, GPIO.IN)  # D2
GPIO.setup(pinD3, GPIO.IN)  # D3
GPIO.setup(pinD4, GPIO.IN)  # D4
GPIO.setup(pinD5, GPIO.IN)  # D5
GPIO.setup(pinD6, GPIO.IN)  # D6
GPIO.setup(pinD7, GPIO.IN)  # D7

i = 0
try:
    while i == 0:
        ainput = input("Type memory address to read in hex < 7ff: ")
        try:
            address = int(ainput, 16)
        except ValueError:
            print("That's not hex")
            quit(1)

        if address > 2047 or address < 0:
            print("Address exceeds 0x7ff, quitting...")
            quit(1)

        print("INT address %s" % address)
        print("Hex Address: %s" % hex(address))
        print("Binary Address: %s" % bin(address))
        print("Binary LSB: %s" % bin(address)[1])
        i = 1

except KeyboardInterrupt:
    print("Keyboard Interrupt.\nPerforming GPIO cleanup.")
    GPIO.cleanup()

binaddress = bin(address)[2:].zfill(11)
print("bin address: %s" % binaddress)
# Set address bus:
GPIO.output(pinA0, bool(binaddress[0]))    # A0
GPIO.output(pinA1, bool(binaddress[1]))    # A1
GPIO.output(pinA2, bool(binaddress[2]))    # A2
GPIO.output(pinA3, bool(binaddress[3]))    # A3
GPIO.output(pinA4, bool(binaddress[4]))    # A4
GPIO.output(pinA5, bool(binaddress[5]))    # A5
GPIO.output(pinA6, bool(binaddress[6]))    # A6
GPIO.output(pinA7, bool(binaddress[7]))    # A7
GPIO.output(pinA8, bool(binaddress[8]))    # A8
GPIO.output(pinA9, bool(binaddress[9]))    # A9
GPIO.output(pinA10, bool(binaddress[10]))  # A10
# GPIO.output(26,A[11])   #A11
# GPIO.output(16,A[12])   #A12
# GPIO.output(20,A[13])   #A13
# GPIO.output(21,A[14])   #A14

# Operation Loop
try:
    print("Turning on the chip and setting it to output mode.")
    GPIO.output(3, 0)  # OE - low - enable output
    GPIO.output(2, 0)  # CE - low - turn on the chip
    time.sleep(0.1)
    print("Reading the address.")

    # set data variables
    D0 = GPIO.input(pinD0)
    D1 = GPIO.input(pinD1)
    D2 = GPIO.input(pinD2)
    D3 = GPIO.input(pinD3)
    D4 = GPIO.input(pinD4)
    D5 = GPIO.input(pinD5)
    D6 = GPIO.input(pinD6)
    D7 = GPIO.input(pinD7)

    print(str(D0)+" "+str(D1)+" "+str(D2)+" "+str(D3)+" "+str(D4)+" "+str(D5)+" "+str(D6)+" "+str(D7))
    GPIO.output(2, 1)  # CE - high - standby mode
    GPIO.output(3, 1)  # OE - high - disable output
    GPIO.cleanup()

except KeyboardInterrupt:
    print("Keyboard Interrupt.\nPerforming GPIO cleanup.")
    GPIO.cleanup()
