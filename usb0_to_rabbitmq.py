#!/usr/bin/python

from __future__ import print_function
import serial, time, io, datetime, pika, os

import logging
logging.basicConfig(level=logging.INFO)


addr = "/dev/ttyUSB0" ## serial port to read data from
baud = 38400 ## baud rate for instrument
filename = "/var/tmp/usb0.out"

ingnoredsentences = ["DUAIQ", "ECDTM", "ECGGA", "ECGSA", "ECGSV", "ECRMC", "ECZDA", "SDDBT"]


ser = serial.Serial(
    port = addr,\
    baudrate = baud,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    rtscts=True,dsrdtr=True, ## This line is needed for serial port emulation \
    timeout=0)


print("Connected to: " + ser.portstr)


credentials = pika.PlainCredentials(os.environ['MQ_USER'], os.environ['MQ_PASS'])
parameters = pika.ConnectionParameters(os.environ['MQ_SERVER'],int(os.environ['MQ_PORT']),'/',credentials)

## Connect
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

## declare the que (idempotent)
channel.queue_declare(queue=os.environ['MQ_QUEUENAME'])

seq = [] ## this will store each line of data
count = 1 ## row index

while True:
    for i in ser.read():
        seq.append(i) ## convert from ACSII?
        #if (i != '\n') and (i != '\r'):
        if i not in ['\n', '\r']:
            joined_seq = ''.join(str(v) for v in seq) ## Make a string from array

        if i == '\n':
            if any(x in joined_seq for x in ingnoredsentences):
                ## reset the seq
                seq = []
            else:
                ## assemble message,  append a timestamp to each row of data
                data=(str(count) + "," + str(datetime.datetime.now()) + "," + joined_seq)
                ## reset the seq
                seq = []
                ## up the rowcount
                count += 1
                ## publish message
                channel.basic_publish(exchange='',routing_key=mqqueuename,body=data)

            break


## close connection
connection.close()

#print(" [x] Sent 'Hello World!'")


