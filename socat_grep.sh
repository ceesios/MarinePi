socat -t0 file:/dev/ttyUSB0,b38400,cs8,parenb=0,cstopb=0,clocal=0,raw,echo=0,setlk,flock-ex-nb,nonblock=1 STDOUT,nonblock=1 | grep -v -e DUAIQ -e ECDTM -e ECGGA -e ECGLL -e ECGSA -e ECGSV -e ECRMC -e ECVTG -e SDDBT -e SDDPT

