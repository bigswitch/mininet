#!/usr/bin/env python

# Used by mininet for the tcp command (testing tcp connectivity between
# hosts)

import socket
import sys

if len(sys.argv)!=3:
    sys.stderr.write("Internal command for mininet's tcp testing\n")
    sys.stderr.write("Usage: %s TIMEOUT PORT\n", sys.argv[0])
    sys.exit(2)

TIMEOUT = float(sys.argv[1])
HOST = ''    # listen on all ifaces
PORT = int(sys.argv[2])

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    s.settimeout(TIMEOUT)
    print "LISTENING"
    conn, addr = s.accept()
except socket.timeout:
    print "CONN TIMEOUT"
    sys.exit(1)
except socket.error, msg:
    print "CONN ERROR", msg
    sys.exit(1)

try:
    conn.settimeout(TIMEOUT)
    while 1:
        data = conn.recv(1024)
        if not data: break
        conn.sendall(data)
    conn.close()
except socket.timeout:
    print "XFER TIMEOUT"
    sys.exit(1)
except socket.error, msg:
    print "XFER ERROR", msg
    sys.exit(1)
print "OK"
