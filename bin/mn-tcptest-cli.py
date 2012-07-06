#!/usr/bin/env python

# Used by mininet for the tcp command (testing tcp connectivity between
# hosts)

import socket
import socket
import sys
import datetime

if len(sys.argv)!=4:
    sys.stderr.write("Internal command for mininet's tcp testing\n")
    sys.stderr.write("Usage: %s TIMEOUT IP PORT\n", sys.argv[0])
    sys.exit(2)

TIMEOUT = float(sys.argv[1])
HOST = sys.argv[2]
PORT = sys.argv[3]  
try:
    s = socket.create_connection((HOST,PORT), timeout=TIMEOUT)
except socket.timeout:
    print "CONN TIMEOUT"
    sys.exit(1)
except socket.error, msg:
    print "CONN ERROR", msg
    sys.exit(1)

s.settimeout(TIMEOUT)
# A somewhat random string to send to the server
data = str(datetime.datetime.today())
# Make sure its just over 2000 bytes long ==> 
# more than 1 pkt
data = data * (2000/len(data)+1)

try: 
    s.sendall(data)
    while 1:
        indata = s.recv(1024)
        if not indata: break
        if not data.startswith(indata): break
        data = data[len(indata):]
        if len(data)== 0: break
    s.close()
    if len(data) != 0:
        print "NODATA"
        sys.exit(1)
except socket.timeout:
    print "XFER TIMEOUT"
    sys.exit(1)
except socket.error, msg:
    print "XFER ERROR", msg
    sys.exit(1)
print "OK"
