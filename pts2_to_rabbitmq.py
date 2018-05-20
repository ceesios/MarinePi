#!/usr/bin/python

from __future__ import print_function
import serial, time, io, datetime, pika, os, logging
logging.basicConfig(level=logging.INFO)


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
        joined_seq = ''.join(str(v) for v in seq) ## Make a string from array

        if i == '\n':
            data=(str(count) + "," + str(datetime.datetime.now()) + "," + joined_seq) ## append a timestamp to each row of data
            seq = []
            count += 1
            ## publish message
            channel.basic_publish(exchange='',routing_key=os.environ['MQ_QUEUENAME'],body=data)
            break


## close connection
connection.close()

print(" [x] Sent 'Hello World!'")


