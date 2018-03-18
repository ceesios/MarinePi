#!/usr/bin/python

import time, pika

mquser = "nimmerzat"
mqpass = "Naceo1oh"
mqserver = "mqtt.cmoerkerken.nl"
mqport = 5672
mqqueuename = "nimmerzat"

credentials = pika.PlainCredentials(mquser, mqpass)
parameters = pika.ConnectionParameters(mqserver,mqport,'/',credentials)

# Connect
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# declare the que (idempotent)
channel.queue_declare(queue=mqqueuename)

# callback function
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

# receive from queue
channel.basic_consume(callback,
                      queue=mqqueuename,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

# close connection
connection.close()



