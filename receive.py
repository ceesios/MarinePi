#!/usr/bin/python

import time, pika, os

credentials = pika.PlainCredentials(os.environ['MQ_USER'], os.environ['MQ_PASS'])
parameters = pika.ConnectionParameters(os.environ['MQ_SERVER'],int(os.environ['MQ_PORT']),'/',credentials)

## Connect
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

## declare the que (idempotent)
channel.queue_declare(queue=os.environ['MQ_QUEUENAME'])

file = open("receive_output", "w")

# callback function
def callback(ch, method, properties, body):
##	if "ECZDA" in
    print("%s" % body)
    file.write("%s" % body + "\n")


# receive from queue
channel.basic_consume(callback,
                      queue=os.environ['MQ_QUEUENAME'],
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

# close connection
connection.close()
file.close()


