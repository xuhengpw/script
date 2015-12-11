#! /usr/bin/python
import sys
import time
import socket
import subprocess
 
def cmd (script):
    ret = subprocess.call(script, shell=True)
    if ret != 0:
        print "script execution problems encountered!!!"
        sys.exit(1)
    time.sleep(2)
 
host_type = socket.gethostname().split('-')[1]
 
# services offline
if host_type == 'mh' or host_type == 'culverin':
    cmd("/usr/bin/f5node stop")
else:
    cmd("/usr/bin/scf")
 
print "Offline is ok!!!"