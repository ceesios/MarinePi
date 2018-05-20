#!/bin/bash
mkdir -p /var/tmp/_socat_received/

while true; do socat -t0 file:/dev/ttyUSB0,b38400,cs8,parenb=0,cstopb=0,clocal=0,raw,echo=0,setlk,flock-ex-nb,nonblock=1 STDOUT,nonblock=1 | ./socat_write.sh; done

