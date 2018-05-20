#!/bin/bash
DELAY=60
SOCAT_PID=$(/bin/ps -eo pid,args | grep "socat -t0 file:/dev/ttyUSB0" | grep -v grep | awk '{ print $1 }')

while `kill -0 $SOCAT_PID`
do  
  touch /var/tmp/out.txt
  NEXT_STOP=`date +%s --date "$DELAY second"`
  while  `kill -0 $SOCAT_PID` && [ "$(date +%s)" -lt "$NEXT_STOP" ]
  do
    head -q - >> /var/tmp/out.txt
  done
  mv /var/tmp/out.txt "/var/tmp/_socat_received/"$(date +"%Y-%m-%d-%T")"__out.txt"
done
