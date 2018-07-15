#!/usr/bin/python

import time, pika, sys, os, MySQLdb

credentials = pika.PlainCredentials(os.environ['MQ_USER'], os.environ['MQ_PASS'])
parameters = pika.ConnectionParameters(os.environ['MQ_SERVER'],int(os.environ['MQ_PORT']),'/',credentials)

######################
## Connect to rabbitmq
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

## declare the que (idempotent)
channel.queue_declare(queue=os.environ['MQ_QUEUENAME'])

################
## Open the file
#file = open("receive_output", "a")


###################
## Connect to MySQL
db = MySQLdb.connect(host=os.environ['SQL_SERVER'],    # your host, usually localhost
                     user=os.environ['SQL_USER'],         # your username
                     passwd=os.environ['SQL_PASS'],  # your password
                     db=os.environ['SQL_DB'])        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cursor = db.cursor()

## callback function for basic_cosume
def consumer_callback(ch, method, properties, body):
    ## print rabbitmq message on screen
    print("%s" % body)
    ## write rabbitmq message to file
    file = open("receive_output", "a")
    file.write("%s" % body + "\n")
    file.close()

    ## split message into values
    fields = body.split(",")
    while len(fields) < 11:
        fields.append('')

    datetimestripped=fields[1].replace(" ", "").replace("-", "").replace(":", "").split(".")[0]
    messagetype=fields[2].replace("$", "")
    cursor.execute('INSERT INTO nmea_raw_data(datetime, messagetype, f1, f2, f3, f4, f5, f6, f7, f8 ) \
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
        (datetimestripped, messagetype, fields[3], fields[4], fields[5], fields[6], fields[7], fields[8], fields[9], fields[10]))
    if "noack" not in properties:
        db.commit()


## argument is given, process as log file
if len(sys.argv) > 1:
    file = open(sys.argv[1], "r")
    for line in file:
        consumer_callback("","","noack",line)
    db.commit()
    file.close()

else:
    # receive from queue
    channel.basic_consume(consumer_callback,
                          queue=os.environ['MQ_QUEUENAME'],
                          no_ack=True)

    db.commit()
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

# close connection
connection.close()
#file.close()
#close the connection to the database.
cursor.close()
db.close()

