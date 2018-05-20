#!/usr/bin/python

from __future__ import print_function
import serial, time, io, datetime, pika
#from serial import Serial

addr = "/dev/pts/2" ## serial port to read data from
baud = 9600 ## baud rate for instrument
filename = "/var/tmp/usb0.out"

ser = serial.Serial(
    port = addr,\
    baudrate = baud,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    rtscts=True,dsrdtr=True, ## This line is needed for serial port emulation \
    timeout=0)

datafile=open(filename, 'a', 0)

## this will store each line of data
seq = []
count = 1 ## row index

while True:
    for i in ser.read():
        seq.append(i) ## convert from ACSII?
        joined_seq = ''.join(str(v) for v in seq) ## Make a string from array

        if i == '\n':
            datafile.write(str(count) + "," + str(datetime.datetime.now()) + "," + joined_seq) ## append a timestamp to each row of data
            seq = []
            count += 1
            break

datafile.close()
ser.close()
