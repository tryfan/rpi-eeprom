#!/usr/bin/env python3

import os
import time
import string
uname = os.uname()
if 'arm' in uname.machine:
    import RPi.GPIO as GPIO
else:
    import FakeRPi.GPIO as GPIO


def round_down(num, divisor):
    return num - (num % divisor)


def hexdump(src, length=16, sep='.'):
    """Hex dump bytes to ASCII string, padded neatly
    In [107]: x = b'\x01\x02\x03\x04AAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBB'

    In [108]: print('\n'.join(hexdump(x)))
    00000000  01 02 03 04 41 41 41 41  41 41 41 41 41 41 41 41 |....AAAAAAAAAAAA|
    00000010  41 41 41 41 41 41 41 41  41 41 41 41 41 41 42 42 |AAAAAAAAAAAAAABB|
    00000020  42 42 42 42 42 42 42 42  42 42 42 42 42 42 42 42 |BBBBBBBBBBBBBBBB|
    00000030  42 42 42 42 42 42 42 42                          |BBBBBBBB        |
    """
    _filter = ''.join([(len(repr(chr(x))) == 3) and chr(x) or sep for x in range(256)])
    lines = []
    for c in range(0, len(src), length):
        chars = src[c: c + length]
        hex_ = ' '.join(['{:02x}'.format(x) for x in chars])
        if len(hex_) > 24:
            hex_ = '{} {}'.format(hex_[:24], hex_[24:])
        printable = ''.join(['{}'.format((x <= 127 and _filter[x]) or sep) for x in chars])
        lines.append('{0:08x}  {1:{2}s} |{3:{4}s}|'.format(c, hex_, length * 3, printable, length))
    return lines


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
endaddress = "0"
try:
    while i == 0:
        endainput = input("Type memory address to end read at in hex < 7ff: ")

        try:
            endaddress = int(endainput, 16)
        except ValueError:
            print("That's not hex")
            quit(1)

        # print("INT address start: %s end: %s" % (beginaddress, endaddress))
        # print("Hex Address: %s end: %s" % (hex(beginaddress), hex(endaddress)))
        # print("Binary Address: %s end: %s" % (bin(beginaddress), bin(endaddress)))

        if 0 >= endaddress >= 2047:
            print("Address out of range, quitting...")
            quit(1)

        i = 1

except KeyboardInterrupt:
    print("Keyboard Interrupt.\nPerforming GPIO cleanup.")
    GPIO.cleanup()

binendaddress = bin(endaddress)[2:].zfill(11)
print("bin addresses: end: %s" % binendaddress)
data = {}
databytes = bytearray()

for address in range(0, endaddress):

    binaddress = bin(address)[2:].zfill(11)
    print("setting address to %s" % binaddress)
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

# Operation Loop
    try:
        print("Turning on the chip and setting it to output mode.")
        GPIO.output(3, 0)  # OE - low - enable output
        GPIO.output(2, 0)  # CE - low - turn on the chip
        time.sleep(0.01)
        print("Reading the address.")

        D = [0, 0, 0, 0, 0, 0, 0, 0]

        # set data variables
        D[0] = GPIO.input(pinD0)
        D[1] = GPIO.input(pinD1)
        D[2] = GPIO.input(pinD2)
        D[3] = GPIO.input(pinD3)
        D[4] = GPIO.input(pinD4)
        D[5] = GPIO.input(pinD5)
        D[6] = GPIO.input(pinD6)
        D[7] = GPIO.input(pinD7)

        if 'arm' not in uname.machine:
            D = [0, 1, 0, 0, 0, 0, 1, 0]
        D.reverse()
        data[address] = bin(sum(c << i for i, c in enumerate(D)))
        print(sum(c << i for i, c in enumerate(D)))
        databytes.append(sum(c << i for i, c in enumerate(D)))
        # data = bin(int(''.join(map(str, D)), 2) << 1)
        # print(D)
        # print(data)

        # print(str(D0)+" "+str(D1)+" "+str(D2)+" "+str(D3)+" "+str(D4)+" "+str(D5)+" "+str(D6)+" "+str(D7))
        GPIO.output(2, 1)  # CE - high - standby mode
        GPIO.output(3, 1)  # OE - high - disable output

    except KeyboardInterrupt:
        print("Keyboard Interrupt.\nPerforming GPIO cleanup.")
        GPIO.cleanup()

print("\n".join(hexdump(databytes)))

GPIO.cleanup()
