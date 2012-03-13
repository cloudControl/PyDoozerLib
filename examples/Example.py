# -*- coding: utf-8 -*-
"""
    Copyright (c) 2012 cloudControl GmbH

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following
    conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.

"""
import socket
import sys
from pydoozerlib import PyDoozerLib

# Provide at least 1 IP address and port of the Doozer cluster
host = '192.168.29.174'
port = 8046
timeout = 15.0

# A sample configuration to write ...
ssh_config = '''X11Forwarding yes
X11DisplayOffset 10
PrintMotd no
PrintLastLog yes
TCPKeepAlive yes
#UseLogin no'''

# Create the Doozer client and connect to the Doozerd server/cluster
client = PyDoozerLib(host, port, timeout)

try:
    client.connect()
except socket.timeout:
    print "Cannot connect to host={0} on port={1}!".format(host, port)
    sys.exit(1)

# Get the value at '/watch2'
resp = client.get('/watch2')
print "REV: {0}".format(resp.rev)
print "VALUE: {0}".format(resp.value)
print "TAG: {0}".format(resp.tag)
print ""

# Overwrite the given value at '/watch2' with a new value
client.set('/watch2', ssh_config)
resp = client.get('/watch2')
print "REV: {0}".format(resp.rev)
print "VALUE: {0}".format(resp.value)
print "TAG: {0}".format(resp.tag)
print ""

# Write a new value at a new path '/watch4'
client.set('/watch4', "Audiiii")
resp = client.get('/watch4')
print "REV: {0}".format(resp.rev)
print "VALUE: {0}".format(resp.value)
print "TAG: {0}".format(resp.tag)
print ""

# Write a new value at a new path '/watch4'
rev = client.get('/watch4').rev
client.delete('/watch4', rev)
resp = client.get('/watch4')
print "REV: {0}".format(resp.rev)
print "VALUE: {0}".format(resp.value)
print "TAG: {0}".format(resp.tag)
print ""

# ... and disconnect!
client.disconnect()