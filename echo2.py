#!/bin/env python
#
# echo2.py
# loop over nmea example data
# sould be used with socat:
# socat -ddd -ddd PTY,raw,echo=0 "EXEC:'python ./echo2.py',pty,raw,echo=0"
import time

filename = "./nmea_sample_data/valid_nmea"
n=0

while True:
	afile = open(filename,'r')
	for aline in afile:
		values = aline.split(",")
		print(aline.rstrip())
		n+=1
		time.sleep(.3)
	afile.close()




